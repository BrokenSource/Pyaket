use crate::*;

/* -------------------------------------------- */
// https://pyaket.dev/docs#app

pub static PYAKET_APP_NAME:    &str = "PYAKET_APP_NAME";
pub static PYAKET_APP_AUTHOR:  &str = "PYAKET_APP_AUTHOR";
pub static PYAKET_APP_VERSION: &str = "PYAKET_APP_VERSION";
pub static PYAKET_APP_ABOUT:   &str = "PYAKET_APP_ABOUT";
pub static PYAKET_APP_ICON:    &str = "PYAKET_APP_ICON";
pub static PYAKET_APP_WHEELS:  &str = "PYAKET_APP_WHEELS";
pub static PYAKET_APP_PYPI:    &str = "PYAKET_APP_PYPI";
pub static PYAKET_APP_REQTXT:  &str = "PYAKET_APP_REQTXT";
pub static PYAKET_APP_ROLLING: &str = "PYAKET_APP_ROLLING";
pub static PYAKET_KEEP_OPEN:   &str = "PYAKET_KEEP_OPEN";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketApplication {

    #[default(envy::uget(PYAKET_APP_NAME, "pyaket"))]
    pub name: String,

    #[default(envy::uget(PYAKET_APP_AUTHOR, "brokensource"))]
    pub author: String,

    #[default(envy::uget(PYAKET_APP_VERSION, "0.0.0"))]
    pub version: String,

    #[default(envy::uget(PYAKET_APP_ABOUT, "No description provided"))]
    pub about: String,

    #[serde(skip)]
    #[default(envy::get(PYAKET_APP_ICON, None))]
    pub icon: Option<String>,

    #[serde(skip)]
    #[default(envy::uget(PYAKET_APP_WHEELS, ""))]
    pub wheels: String,

    #[default(envy::uget(PYAKET_APP_PYPI, ""))]
    pub pypi: String,

    #[default(envy::uget(PYAKET_APP_REQTXT, ""))]
    pub reqtxt: String,

    #[default(envy::ubool(PYAKET_APP_ROLLING, false))]
    pub rolling: bool,

    #[default(envy::ubool(PYAKET_KEEP_OPEN, false))]
    pub keep_open: bool,
}

/* -------------------------------------------- */
// https://pyaket.dev/docs#directories

pub static PYAKET_COMMON_DIR:   &str = "PYAKET_COMMON_DIR";
pub static PYAKET_VERSIONS_DIR: &str = "PYAKET_VERSIONS_DIR";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketDirectories {

    #[default(envy::uget(PYAKET_COMMON_DIR, "pyaket"))]
    pub common: String,

    #[default(envy::uget(PYAKET_VERSIONS_DIR, "versions"))]
    pub versions: String,
}

/* -------------------------------------------- */
// https://pyaket.dev/docs#python

pub static PYAKET_PYTHON_VERSION: &str = "PYAKET_PYTHON_VERSION";
pub static PYAKET_PYTHON_BUNDLE:  &str = "PYAKET_PYTHON_BUNDLE";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketPython {

    #[default(envy::uget(PYAKET_PYTHON_VERSION, "3.13"))]
    pub version: String,

    #[default(envy::ubool(PYAKET_PYTHON_BUNDLE, false))]
    pub bundle: bool,
}

/* -------------------------------------------- */
// https://pyaket.dev/docs#uv

pub static PYAKET_UV_VERSION: &str = "PYAKET_UV_VERSION";
pub static PYAKET_UV_BUNDLE:  &str = "PYAKET_UV_BUNDLE";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketUV {

    #[default(envy::uget(PYAKET_UV_VERSION, "0.8.3"))]
    pub version: String,

    #[default(envy::ubool(PYAKET_UV_BUNDLE, false))]
    pub bundle: bool,
}

/* -------------------------------------------- */
// https://pyaket.dev/docs#pytorch

pub static PYAKET_TORCH_VERSION: &str = "PYAKET_TORCH_VERSION";
pub static PYAKET_TORCH_BACKEND: &str = "PYAKET_TORCH_BACKEND";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketTorch {

    #[default(envy::uget(PYAKET_TORCH_VERSION, ""))]
    pub version: String,

    #[default(envy::uget(PYAKET_TORCH_BACKEND, "auto"))]
    pub backend: String,
}

/* -------------------------------------------- */
// https://pyaket.dev/docs#entry-points

pub static PYAKET_ENTRY_MODULE:  &str = "PYAKET_ENTRY_MODULE";
pub static PYAKET_ENTRY_SCRIPT:  &str = "PYAKET_ENTRY_SCRIPT";
pub static PYAKET_ENTRY_CODE:    &str = "PYAKET_ENTRY_CODE";
pub static PYAKET_ENTRY_COMMAND: &str = "PYAKET_ENTRY_COMMAND";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketEntry {

    #[default(envy::uget(PYAKET_ENTRY_MODULE, ""))]
    pub module: String,

    #[default(envy::uget(PYAKET_ENTRY_SCRIPT, ""))]
    pub script: String,

    #[default(envy::uget(PYAKET_ENTRY_CODE, ""))]
    pub code: String,

    #[default(envy::uget(PYAKET_ENTRY_COMMAND, ""))]
    pub command: String,
}

/* -------------------------------------------- */

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct Project {
    pub app:    PyaketApplication,
    pub dirs:   PyaketDirectories,
    pub python: PyaketPython,
    pub uv:     PyaketUV,
    pub torch:  PyaketTorch,
    pub entry:  PyaketEntry,

    /// A unique identifier to this compiled binary
    #[default(Uuid::new_v4().to_string())]
    pub uuid: String,

    /// The platform target triple of the build
    #[default(std::env::var("TARGET").unwrap())]
    pub triple: String,
}

impl Project {
    pub fn json(&self) -> String {
        serde_json::to_string(&self).unwrap()
    }

    pub fn from_json(json: &str) -> Self {
        serde_json::from_str(json).unwrap()
    }
}

/* -------------------------------------------------------------------------- */
// Workspace

static WORKSPACE_ROOT: OnceLock<PathBuf> = OnceLock::new();

impl Project {

    /// Automatic:
    /// - Windows: `%LocalAppData%/$author/`
    /// - Linux:   `~/.local/share/$author/`
    /// - MacOS:   `~/Library/Application Support/$author/`
    /// - Custom:  `$WORKSPACE/`
    pub fn workspace_root(&self) -> &'static PathBuf {
        WORKSPACE_ROOT.get_or_init(|| {
            if let Some(path) = envy::get("WORKSPACE", None) {
                PathBuf::from(path)
            } else {
                BaseDirs::new().unwrap()
                    .data_local_dir()
                    .join(&self.app.author)
            }
        })
    }

    /// A common directory to store shared data
    pub fn workspace_common(&self) -> PathBuf {
        self.workspace_root()
            .join(&self.dirs.common)
    }

    /// Directory to store uv assets
    pub fn astral_dir(&self) -> PathBuf {
        self.workspace_common()
            .join("astral")
    }

    /// Mirrored to `$UV_CACHE_DIR`
    pub fn uv_cache_dir(&self) -> PathBuf {
        self.workspace_common()
            .join("packages")
    }

    /// Where to install the Python's virtual environment:
    /// - `$WORKSPACE/versions/1.0.0`
    pub fn installation_dir(&self) -> PathBuf {
        self.workspace_common()
            .join(&self.dirs.versions)
            .join(&self.app.version)
    }

    /// A file that tracks installs from unique binaries for a few purposes:
    /// - Flags if the installation was successful to skip bootstrapping
    /// - Triggers a reinstall if the hash differs for same versions
    pub fn uuid_tracker_file(&self) -> PathBuf {
        self.installation_dir()
            .join(format!("{}.uuid", self.app.name))
    }
}

/* -------------------------------------------------------------------------- */

impl Project {

    /// Directory to store many python versions
    /// - Should mirror `UV_PYTHON_INSTALL_DIR`
    pub fn python_install_dir(&self) -> PathBuf {
        self.workspace_common().join("Python")
    }

    /// The uv archive filename without extensions, e.g.:
    /// - `uv-0.6.11-x86_64-unknown-linux-gnu`
    pub fn uv_download_stem(&self) -> String {
        format!("uv-{}", self.triple
            .replace("windows-gnu", "windows-msvc")
            .replace("msvcllvm", "msvc")
        )
    }

    /// The download filename of the uv distribution, e.g.:
    /// - `uv-0.6.11-x86_64-unknown-linux-gnu.tar.gz`
    pub fn uv_download_file(&self) -> String {
        format!("{}.{}", self.uv_download_stem(),
            if self.triple.contains("windows") {"zip"} else {"tar.gz"}
        )
    }

    /// The download URL of the uv distribution
    pub fn uv_download_url(&self) -> String {
        format!(
            "{}/releases/download/{}/{}",
            "https://github.com/astral-sh/uv",
            self.uv.version,
            self.uv_download_file(),
        )
    }

    /// Path to unpack uv at runtime
    pub fn uv_unpack_dir(&self) -> PathBuf {
        self.astral_dir()
            .join(&self.uv.version)
    }

    /// Path to download and cache uv at runtime
    pub fn uv_download_path(&self) -> PathBuf {
        self.uv_unpack_dir()
            .join(&self.uv_download_file())
    }

    pub fn ensure_uv(&self) -> Result<()> {
        let bytes = ArchiveAssets::read_or_download(
            &self.uv_download_file(),
            &self.uv_download_url(),
            &self.uv_download_path(),
        )?;
        archive::unpack_bytes(&bytes, self.uv_unpack_dir())?;
        Ok(())
    }

    /// Get a command starting with uv executable
    pub fn uv(&self) -> Result<Command> {
        let pattern = format!("{}/**/uv{}",
            self.uv_unpack_dir().display(),
            if cfg!(target_os="windows") {".exe"} else {""}
        );

        if !glob::glob(&pattern)?.any(|x| x.is_ok()) {
            self.ensure_uv()?;
        }

        Ok(Command::new(glob::glob(&pattern)?
            .filter_map(Result::ok).next()
            .expect("uv executable not found")))
    }
}
