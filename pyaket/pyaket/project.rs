use crate::*;

use directories::BaseDirs;
use serde::Deserialize;
use serde::Serialize;
use smart_default::SmartDefault;
use uuid::Uuid;

/* -------------------------------------------- */
// https://pyaket.dev/docs/config/application/

pub static PYAKET_APP_NAME:    &str = "PYAKET_APP_NAME";
pub static PYAKET_APP_AUTHOR:  &str = "PYAKET_APP_AUTHOR";
pub static PYAKET_APP_VERSION: &str = "PYAKET_APP_VERSION";
pub static PYAKET_APP_ABOUT:   &str = "PYAKET_APP_ABOUT";
pub static PYAKET_APP_ICON:    &str = "PYAKET_APP_ICON";
pub static PYAKET_KEEP_OPEN:   &str = "PYAKET_KEEP_OPEN";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketApplication {

    #[default(envy::uget(PYAKET_APP_NAME, "Pyaket"))]
    pub name: String,

    #[default(envy::uget(PYAKET_APP_AUTHOR, "BrokenSource"))]
    pub author: String,

    #[default(envy::uget(PYAKET_APP_VERSION, "0.0.0"))]
    pub version: String,

    #[default(envy::uget(PYAKET_APP_ABOUT, "No description provided"))]
    pub about: String,

    #[serde(skip)]
    #[default(envy::get(PYAKET_APP_ICON, None))]
    pub icon: Option<String>,

    #[default(envy::ubool(PYAKET_KEEP_OPEN, false))]
    pub keep_open: bool,
}

impl PyaketApplication {

    /// Workspace root identifier, either `author or name`
    /// - Makes having an author name optional
    /// - Disallows root being the data local
    pub fn vendor(&self) -> String {
        match self.author.is_empty() {
            false => self.author.clone(),
            true  => self.name.clone(),
        }
    }
}

/* -------------------------------------------- */
// https://pyaket.dev/docs/config/dependencies/

pub static PYAKET_APP_WHEELS:  &str = "PYAKET_APP_WHEELS";
pub static PYAKET_APP_PYPI:    &str = "PYAKET_APP_PYPI";
pub static PYAKET_APP_REQTXT:  &str = "PYAKET_APP_REQTXT";
pub static PYAKET_APP_ROLLING: &str = "PYAKET_APP_ROLLING";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketDependencies {

    #[serde(skip)]
    #[default(envy::get(PYAKET_APP_WHEELS, None))]
    pub wheels: Option<String>,

    #[default(envy::get(PYAKET_APP_PYPI, None))]
    pub pypi: Option<String>,

    #[default(envy::get(PYAKET_APP_REQTXT, None))]
    pub reqtxt: Option<String>,

    #[default(envy::ubool(PYAKET_APP_ROLLING, false))]
    pub rolling: bool,
}

/* -------------------------------------------- */
// https://pyaket.dev/docs/config/directories/

pub static PYAKET_COMMON_DIR:   &str = "PYAKET_COMMON_DIR";
pub static PYAKET_VERSIONS_DIR: &str = "PYAKET_VERSIONS_DIR";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketDirectories {

    #[default(envy::uget(PYAKET_COMMON_DIR, "Pyaket"))]
    pub common: String,

    #[default(envy::uget(PYAKET_VERSIONS_DIR, "Versions"))]
    pub versions: String,
}

/* -------------------------------------------- */
// https://pyaket.dev/docs/config/python

pub static PYAKET_PYTHON_VERSION: &str = "PYAKET_PYTHON_VERSION";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketPython {

    #[default(envy::uget(PYAKET_PYTHON_VERSION, "3.13"))]
    pub version: String,
}

/* -------------------------------------------- */
// https://pyaket.dev/docs/config/pytorch

pub static PYAKET_TORCH_VERSION: &str = "PYAKET_TORCH_VERSION";
pub static PYAKET_TORCH_BACKEND: &str = "PYAKET_TORCH_BACKEND";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketTorch {

    #[default(envy::get(PYAKET_TORCH_VERSION, None))]
    pub version: Option<String>,

    #[default(envy::uget(PYAKET_TORCH_BACKEND, "auto"))]
    pub backend: String,
}

/* -------------------------------------------- */
// https://pyaket.dev/docs/config/entry

pub static PYAKET_ENTRY_MODULE:  &str = "PYAKET_ENTRY_MODULE";
pub static PYAKET_ENTRY_SCRIPT:  &str = "PYAKET_ENTRY_SCRIPT";
pub static PYAKET_ENTRY_COMMAND: &str = "PYAKET_ENTRY_COMMAND";
pub static PYAKET_ENTRY_CODE:    &str = "PYAKET_ENTRY_CODE";

#[derive(Serialize, Deserialize)]
#[serde(rename_all="lowercase")]
pub enum PyaketEntry {
    Command(String),
    Module(String),
    Script(String),
    Code(String),
    Interpreter,
}

impl Default for PyaketEntry {
    fn default() -> Self {
        type G = fn(String) -> PyaketEntry;

        for (key, from) in [
            (PYAKET_ENTRY_COMMAND, Self::Command as G),
            (PYAKET_ENTRY_MODULE,  Self::Module  as G),
            (PYAKET_ENTRY_SCRIPT,  Self::Script  as G),
            (PYAKET_ENTRY_CODE,    Self::Code    as G),
        ] {
            if let Some(value) = envy::get(key, None) {
                return from(value);
            }
        }

        PyaketEntry::Interpreter
    }
}

/* -------------------------------------------- */

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct PyaketProject {
    pub app:    PyaketApplication,
    pub deps:   PyaketDependencies,
    pub dirs:   PyaketDirectories,
    pub python: PyaketPython,
    pub torch:  PyaketTorch,
    pub entry:  PyaketEntry,

    /// Unique identifier for any compiled binary
    #[default(Uuid::new_v4().to_string())]
    pub uuid: String,

    /// The platform target triple of the build
    #[default(std::env::var("TARGET").unwrap())]
    pub triple: String,
}

impl PyaketProject {
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
            if let Some(path) = envy::get("WORKSPACE", None) {
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
