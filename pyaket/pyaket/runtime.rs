use crate::*;

use temp_dir::TempDir;
use directories::BaseDirs;

/* -------------------------------------------------------------------------- */

static WORKSPACE_ROOT: OnceLock<PathBuf> = OnceLock::new();

impl PyaketProject {

    /// Centralized working directory for all pyaket files
    ///
    /// | Platform | Path                                        |
    /// | :------- | :------------------------------------------ |
    /// | Windows  | `%LocalAppData%\<vendor>\`                  |
    /// | Linux    | `~/.local/share/<vendor>/`                  |
    /// | MacOS    | `~/Library/Application Support/<vendor>/`   |
    /// | Custom   | `$WORKSPACE/`                               |
    ///
    pub fn workspace_root(&self) -> &'static PathBuf {
        WORKSPACE_ROOT.get_or_init(|| {
            if let Some(path) = envy::get("WORKSPACE") {
                PathBuf::from(path)
            } else {
                BaseDirs::new().unwrap()
                    .data_local_dir()
                    .join(self.app.vendor())
            }
        })
    }

    /// A common directory to store shared data
    pub fn workspace_common(&self) -> PathBuf {
        self.workspace_root()
            .join(&self.dirs.common)
    }

    /// Where to install the Python's virtual environment:
    /// - `$WORKSPACE/versions/1.0.0`
    pub fn installation_dir(&self) -> PathBuf {
        self.workspace_common()
            .join(&self.dirs.versions)
            .join(&self.app.version)
    }

    // Fixme: Shared installation shouldn't be wiped
    /// A file that tracks installs from unique binaries for a few purposes:
    /// - Flags if the installation was successful to skip bootstrapping
    /// - Triggers a reinstall if the hash differs for same versions
    pub fn uuid_tracker_file(&self) -> PathBuf {
        self.installation_dir()
            .join(format!("{}.uuid", self.app.name))
    }
}

/* -------------------------------------------------------------------------- */

impl PyaketProject {

    pub fn run(&self) -> Result<()> {
        self._export()?;
        self._install()?;
        self._entry()?;
        Ok(())
    }

    /// Export base environment variables
    pub fn _export(&self) -> Result<()> {

        // Send the executable path to Python, also flags a Pyaket app
        let executable = current_exe()?.canonicalize()?;
        envy::set("PYAKET", executable.display());

        // Load environment variables where the shell (executable) is
        for file in glob::glob("*.env").unwrap().map(|x| x.unwrap()) {
            dotenvy::from_path(file)?;
        }

        envy::setdefault("VIRTUAL_ENV",      self.installation_dir().display());
        envy::setdefault("UV_VENV_CLEAR",    1); // Skip destructive confirmation prompt
        envy::setdefault("UV_SYSTEM_PYTHON", 0); // Always use a managed distribution
        envy::setdefault("UV_NO_CONFIG",     1); // Do not look for a pyproject.toml

        // Force disable the GIL on freethreaded python
        if self.python.version.contains('t') {
            envy::setdefault("UNSAFE_PYO3_BUILD_FREE_THREADED", 1);
            envy::setdefault("PYTHON_GIL", 0);
        }

        Ok(())
    }

    pub fn _install(&self) -> Result<()> {
        if match read(self.uuid_tracker_file()) {
            Ok(bytes) => {bytes != self.uuid.as_bytes()},
            Err(_)    => true,
        } || self.deps.rolling {

            /* Create the virtual environment */ {
                let mut setup = subprocess::uv()?;

                setup.arg("venv")
                    .arg(self.installation_dir())
                    .arg("--python").arg(&self.python.version)
                    .arg("--seed").arg("--quiet");
                if self.deps.rolling {setup
                    .arg("--allow-existing");}
                subprocess::run(&mut setup)?;
            }

            // Install PyTorch first, as other dependencies might
            // use a platform's default backend than specified
            if let Some(version) = &self.torch.version {
                let mut torch = subprocess::uv()?;

                torch.arg("pip").arg("install")
                    .arg(format!("torch=={}", version))
                    .arg("torchvision")
                    .arg("torchaudio")
                    .arg(format!("--torch-backend={}", self.torch.backend))
                    .arg("--preview");

                subprocess::run(&mut torch)?;
            }

            let tempdir = TempDir::with_prefix("pyaket-").unwrap();

            // Must have at least one package
            let mut command = subprocess::uv()?;
            command.arg("pip").arg("install");
            command.arg("--upgrade");
            command.arg("pip");

            // Write temp wheel/sdist packages and mark to install
            for (name, bytes) in ["*.whl", "*.tar.gz"].into_iter()
                .flat_map(|x| WheelAssets::glob(x).unwrap())
            {
                let file = tempdir.child(name);
                write(&file, bytes)?;
                command.arg(&file);
            }

            // Add PyPI packages to be installed
            command.args(&self.deps.pypi);

            // Add the requirements.txt file to be installed
            if let Some(content) = &self.deps.reqtxt {
                let file = tempdir.child("requirements.txt");
                command.arg("-r").arg(&file);
                write(&file, content)?;
            }

            subprocess::run(&mut command)?;
        }

        // Flag this was a successful install
        write(self.uuid_tracker_file(), &self.uuid)?;
        Ok(())
    }

    pub fn _entry(&self) -> Result<()> {
        let mut main = subprocess::uv()?;
        main.arg("run");
        main.arg("--active");

        match &self.entry {
            PyaketEntry::Command(command) => {
                let args = shlex::split(command)
                    .expect("Failed to parse entry command");
                main = Command::new(&args[0]);
                main.args(&args[1..]);
            },
            PyaketEntry::Module(module) => {
                main.arg("python").arg("-m").arg(module);
            },
            PyaketEntry::Code(code) => {
                main.arg("python").arg("-c").arg(code);
            },
            PyaketEntry::Interpreter => {
                main.arg("python");
            },
            PyaketEntry::Script(script) => {
                main.arg(script);
            },
        }

        // Passthrough arguments, execute
        main.args(std::env::args().skip(1));
        main.spawn()?.wait()?;
        Ok(())
    }
}
