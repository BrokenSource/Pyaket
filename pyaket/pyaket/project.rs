use crate::*;

/* -------------------------------------------- */

pub static PYAKET_APP_NAME:    &str = "PYAKET_APP_NAME";
pub static PYAKET_APP_AUTHOR:  &str = "PYAKET_APP_AUTHOR";
pub static PYAKET_APP_VERSION: &str = "PYAKET_APP_VERSION";
pub static PYAKET_APP_WHEELS:  &str = "PYAKET_APP_WHEELS";
pub static PYAKET_APP_PYPI:    &str = "PYAKET_APP_PYPI";
pub static PYAKET_APP_REQTXT:  &str = "PYAKET_APP_REQTXT";
pub static PYAKET_APP_ROLLING: &str = "PYAKET_APP_ROLLING";
pub static PYAKET_KEEP_OPEN:   &str = "PYAKET_KEEP_OPEN";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketApplication {

    /// [Documentation](https://pyaket.dev/docs#app-name)
    #[default(Environment::uget(PYAKET_APP_NAME, "Pyaket"))]
    pub name: String,

    /// [Documentation](https://pyaket.dev/docs#app-author)
    #[default(Environment::uget(PYAKET_APP_AUTHOR, "BrokenSource"))]
    pub author: String,

    /// [Documentation](https://pyaket.dev/docs#app-version)
    #[default(Environment::uget(PYAKET_APP_VERSION, "0.0.0"))]
    pub version: String,

    /// [Documentation](https://pyaket.dev/docs#app-wheels)
    #[serde(skip)]
    #[default(Environment::uget(PYAKET_APP_WHEELS, ""))]
    pub wheels: String,

    /// [Documentation](https://pyaket.dev/docs#app-pypi)
    #[default(Environment::uget(PYAKET_APP_PYPI, ""))]
    pub pypi: String,

    /// [Documentation](https://pyaket.dev/docs#app-requirements-txt)
    #[default(Environment::uget(PYAKET_APP_REQTXT, ""))]
    pub reqtxt: String,

    /// [Documentation](https://pyaket.dev/docs#rolling)
    #[default(Environment::ubool(PYAKET_APP_ROLLING, false))]
    pub rolling: bool,

    /// [Documentation](https://pyaket.dev/docs#keep-open)
    #[default(Environment::ubool(PYAKET_KEEP_OPEN, false))]
    pub keep_open: bool,
}

/* -------------------------------------------- */

pub static PYAKET_COMMON_DIR:   &str = "PYAKET_COMMON_DIR";
pub static PYAKET_VERSIONS_DIR: &str = "PYAKET_VERSIONS_DIR";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketDirectories {

    /// [Documentation](https://pyaket.dev/docs#common-dir)
    #[default(Environment::uget(PYAKET_COMMON_DIR, "pyaket"))]
    pub common: String,

    /// [Documentation](https://pyaket.dev/docs#versions-dir)
    #[default(Environment::uget(PYAKET_VERSIONS_DIR, "versions"))]
    pub versions: String,
}

/* -------------------------------------------- */

pub static PYAKET_PYTHON_VERSION: &str = "PYAKET_PYTHON_VERSION";
pub static PYAKET_PYTHON_BUNDLE:  &str = "PYAKET_PYTHON_BUNDLE";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketPython {

    /// [Documentation](https://pyaket.dev/docs#python-version)
    #[default(Environment::uget(PYAKET_PYTHON_VERSION, "3.13"))]
    pub version: String,

    /// [Documentation](https://pyaket.dev/docs#python-bundle)
    #[default(Environment::ubool(PYAKET_PYTHON_BUNDLE, false))]
    pub bundle: bool,
}

/* -------------------------------------------- */

pub static PYAKET_UV_VERSION: &str = "PYAKET_UV_VERSION";
pub static PYAKET_UV_BUNDLE:  &str = "PYAKET_UV_BUNDLE";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketUV {

    /// [Documentation](https://pyaket.dev/docs#uv-version)
    #[default(Environment::uget(PYAKET_UV_VERSION, "0.7.9"))]
    pub version: String,

    /// [Documentation](https://pyaket.dev/docs#uv-bundle)
    #[default(Environment::ubool(PYAKET_UV_BUNDLE, false))]
    pub bundle: bool,
}

/* -------------------------------------------- */

pub static PYAKET_TORCH_VERSION: &str = "PYAKET_TORCH_VERSION";
pub static PYAKET_TORCH_BACKEND: &str = "PYAKET_TORCH_BACKEND";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketTorch {

    /// [Documentation](https://pyaket.dev/docs#torch-version)
    #[default(Environment::uget(PYAKET_TORCH_VERSION, ""))]
    pub version: String,

    /// [Documentation](https://pyaket.dev/docs#torch-backend)
    #[default(Environment::uget(PYAKET_TORCH_BACKEND, "auto"))]
    pub backend: String,
}

/* -------------------------------------------- */

pub static PYAKET_ENTRY_MODULE:  &str = "PYAKET_ENTRY_MODULE";
pub static PYAKET_ENTRY_SCRIPT:  &str = "PYAKET_ENTRY_SCRIPT";
pub static PYAKET_ENTRY_CODE:    &str = "PYAKET_ENTRY_CODE";
pub static PYAKET_ENTRY_COMMAND: &str = "PYAKET_ENTRY_COMMAND";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketEntry {

    /// [Documentation](https://pyaket.dev/docs#entry-module)
    #[default(Environment::uget(PYAKET_ENTRY_MODULE, ""))]
    pub module: String,

    /// [Documentation](https://pyaket.dev/docs#entry-script)
    #[default(Environment::uget(PYAKET_ENTRY_SCRIPT, ""))]
    pub script: String,

    /// [Documentation](https://pyaket.dev/docs#entry-code)
    #[default(Environment::uget(PYAKET_ENTRY_CODE, ""))]
    pub code: String,

    /// [Documentation](https://pyaket.dev/docs#entry-command)
    #[default(Environment::uget(PYAKET_ENTRY_COMMAND, ""))]
    pub command: String,
}

/* -------------------------------------------- */

pub static PYAKET_TARGET_TRIPLE: &str = "PYAKET_TARGET_TRIPLE";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct Project {

    #[default(PyaketApplication::default())]
    pub app: PyaketApplication,

    #[default(PyaketDirectories::default())]
    pub dirs: PyaketDirectories,

    #[default(PyaketPython::default())]
    pub python: PyaketPython,

    #[default(PyaketUV::default())]
    pub uv: PyaketUV,

    #[default(PyaketTorch::default())]
    pub torch: PyaketTorch,

    #[default(PyaketEntry::default())]
    pub entry: PyaketEntry,

    /* ---------------------------------------- */

    /// A unique identifier to this compiled binary
    #[default(Uuid::new_v4().to_string())]
    pub uuid: String,

    /// The platform target triple of the build
    #[default(Environment::uget(PYAKET_TARGET_TRIPLE, std::env::var("TARGET").unwrap().as_str()))]
    pub triple: String,
}

/* -------------------------------------------------------------------------- */

impl Project {

    /// Directory to store many python versions
    /// - Should mirror `UV_PYTHON_INSTALL_DIR`
    pub fn python_install_dir(&self) -> PathBuf {
        self.workspace_common().join("python")
    }

    /// The uv archive filename without extensions, e.g.:
    /// - `uv-0.6.11-x86_64-unknown-linux-gnu`
    pub fn uv_archive_stem(&self) -> String {
        format!("uv-{}", self.triple
            .replace("windows-gnu", "windows-msvc")
            .replace("msvcllvm", "msvc")
        )
    }

    /// The download filename of the uv distribution, e.g.:
    /// - `uv-0.6.11-x86_64-unknown-linux-gnu.tar.gz`
    pub fn uv_archive_name(&self) -> String {
        format!("{}.{}", self.uv_archive_stem(),
            if self.triple.contains("windows") {"zip"} else {"tar.gz"}
        )
    }

    /// The download URL of the uv distribution
    pub fn uv_download_url(&self) -> String {
        format!(
            "{}/releases/download/{}/{}",
            "https://github.com/astral-sh/uv",
            self.uv.version,
            self.uv_archive_name(),
        )
    }

    /// Path to unpack uv at runtime
    pub fn uv_unpack_dir(&self) -> PathBuf {
        self.astral_dir()
            .join(&self.uv.version)
    }

    /// Path to download and cache uv at runtime
    pub fn uv_download_file(&self) -> PathBuf {
        self.uv_unpack_dir()
            .join(&self.uv_archive_name())
    }

    pub fn ensure_uv(&self) -> Result<()> {
        let bytes = ArchiveAssets::read_or_download(
            &self.uv_archive_name(),
            &self.uv_download_file(),
            &self.uv_download_url(),
        )?;
        archive::unpack_bytes(
            &bytes, self.uv_unpack_dir(),
            Some(&self.uv_archive_stem())
        )?;
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

/* -------------------------------------------------------------------------- */
// Workspace

static WORKSPACE_ROOT: OnceLock<PathBuf> = OnceLock::new();

impl Project {

    /// - Automatic:
    ///   - Windows: `%LocalAppData%/Author/`
    ///   - Linux: `~/.local/share/Author/`
    ///   - MacOS: `~/Library/Application Support/Author/`
    ///
    /// - Custom:
    ///   - Any: `$WORKSPACE/`
    ///
    pub fn workspace_root(&self) -> &'static PathBuf {
        WORKSPACE_ROOT.get_or_init(|| {
            if let Ok(custom) = std::env::var("WORKSPACE") {
                PathBuf::from(custom)
            } else {
                BaseDirs::new().unwrap()
                    .data_local_dir()
                    .join(&self.app.author)
            }
        })
    }

    /// A common directory to store common unpacked assets
    pub fn workspace_common(&self) -> PathBuf {
        self.workspace_root()
            .join(&self.dirs.common)
    }

    pub fn astral_dir(&self) -> PathBuf {
        self.workspace_common()
            .join("astral")
    }

    pub fn uv_cache_dir(&self) -> PathBuf {
        self.workspace_common()
            .join("cache")
    }

    /// Where to install the Python's virtual environment:
    /// - `$WORKSPACE/Versions/1.0.0`
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

    /* ---------------------------------------- */
    // Serialization

    pub fn json(&self) -> String {
        serde_json::to_string(&self).unwrap()
    }

    pub fn from_json(json: &str) -> Self {
        serde_json::from_str(json).unwrap()
    }
}
