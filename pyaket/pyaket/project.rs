use crate::*;

use serde::Deserialize;
use serde::Serialize;
use smart_default::SmartDefault;
use uuid::Uuid;

/* -------------------------------------------------------------------------- */
// https://pyaket.dev/docs/config/application/

pub static PYAKET_APP_NAME:    &str = "PYAKET_APP_NAME";
pub static PYAKET_APP_AUTHOR:  &str = "PYAKET_APP_AUTHOR";
pub static PYAKET_APP_VENDOR:  &str = "PYAKET_APP_VENDOR";
pub static PYAKET_APP_VERSION: &str = "PYAKET_APP_VERSION";
pub static PYAKET_APP_ABOUT:   &str = "PYAKET_APP_ABOUT";
pub static PYAKET_APP_ICON:    &str = "PYAKET_APP_ICON";

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
pub struct PyaketApplication {

    #[default(envy::uget(PYAKET_APP_NAME, "Pyaket"))]
    pub name: String,

    #[default(envy::uget(PYAKET_APP_AUTHOR, "BrokenSource"))]
    pub author: String,

    #[default(envy::get(PYAKET_APP_VENDOR))]
    pub vendor: Option<String>,

    /// The release version matching PyPI, codename, branch, latest, etc
    #[default(envy::uget(PYAKET_APP_VERSION, "0.0.0"))]
    pub version: String,

    /// A short description of the application, used for metadata, shortcuts
    #[default(envy::uget(PYAKET_APP_ABOUT, "No description provided"))]
    pub about: String,

    /// Path to an icon file to use for the application (platform dependent)
    #[serde(skip)]
    #[default(envy::get(PYAKET_APP_ICON))]
    pub icon: Option<String>,
}

impl PyaketApplication {

    /// Workspace root identifier, either `author or name`
    /// - Makes having an author name optional
    /// - Disallows root being the data local
    pub fn vendor(&self) -> String {
        if let Some(vendor) = &self.vendor {
            vendor.clone()
        } else {
            match self.author.is_empty() {
                false => self.author.clone(),
                true  => self.name.clone(),
            }
        }
    }
}

/* -------------------------------------------------------------------------- */
// https://pyaket.dev/docs/config/dependencies/

pub static PYAKET_APP_WHEELS:  &str = "PYAKET_APP_WHEELS";
pub static PYAKET_APP_PYPI:    &str = "PYAKET_APP_PYPI";
pub static PYAKET_APP_REQTXT:  &str = "PYAKET_APP_REQTXT";
pub static PYAKET_APP_ROLLING: &str = "PYAKET_APP_ROLLING";

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
#[serde(default)]
pub struct PyaketDependencies {

    /// Glob of wheels to bundle and install at runtime
    #[default(envy::vec(PYAKET_APP_WHEELS, SEPARATOR))]
    pub wheels: Vec<String>,

    /// List of dependencies to install at runtime from PyPI
    #[default(envy::vec(PYAKET_APP_PYPI, SEPARATOR))]
    pub pypi: Vec<String>,

    /// Path to a requirements.txt to install at runtime (legacy)
    #[default(envy::get(PYAKET_APP_REQTXT))]
    pub reqtxt: Option<String>,

    /// Always update dependencies at startup (dynamic)
    #[default(envy::ubool(PYAKET_APP_ROLLING, false))]
    pub rolling: bool,
}

/* -------------------------------------------------------------------------- */
// https://pyaket.dev/docs/config/directories/

pub static PYAKET_COMMON_DIR:   &str = "PYAKET_COMMON_DIR";
pub static PYAKET_VERSIONS_DIR: &str = "PYAKET_VERSIONS_DIR";

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
#[serde(default)]
pub struct PyaketDirectories {

    /// Subdirectory of the workspace to use for all installed files
    #[default(envy::uget(PYAKET_COMMON_DIR, "Pyaket"))]
    pub common: String,

    /// Subdirectory of the common dir to install versions of the application
    #[default(envy::uget(PYAKET_VERSIONS_DIR, "Versions"))]
    pub versions: String,
}

/* -------------------------------------------------------------------------- */
// https://pyaket.dev/docs/config/python

pub static PYAKET_PYTHON_VERSION: &str = "PYAKET_PYTHON_VERSION";

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
#[serde(default)]
pub struct PyaketPython {

    /// Configuration for a Python interpreter to use for the project
    #[default(envy::uget(PYAKET_PYTHON_VERSION, "3.13"))]
    pub version: String,
}

/* -------------------------------------------------------------------------- */
// https://pyaket.dev/docs/config/pytorch

pub static PYAKET_TORCH_VERSION: &str = "PYAKET_TORCH_VERSION";
pub static PYAKET_TORCH_BACKEND: &str = "PYAKET_TORCH_BACKEND";

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
#[serde(default)]
pub struct PyaketTorch {

    /// A target torch version to install at runtime
    #[default(envy::get(PYAKET_TORCH_VERSION))]
    pub version: Option<String>,

    /// The backend to use for PyTorch, auto, cpu, xpu, cu128, cu118, etc
    #[default(envy::uget(PYAKET_TORCH_BACKEND, "auto"))]
    pub backend: String,
}

/* -------------------------------------------------------------------------- */
// https://pyaket.dev/docs/config/entry

pub static PYAKET_ENTRY_MODULE:  &str = "PYAKET_ENTRY_MODULE";
pub static PYAKET_ENTRY_SCRIPT:  &str = "PYAKET_ENTRY_SCRIPT";
pub static PYAKET_ENTRY_COMMAND: &str = "PYAKET_ENTRY_COMMAND";
pub static PYAKET_ENTRY_CODE:    &str = "PYAKET_ENTRY_CODE";

#[derive(Serialize, Deserialize)]
#[serde(rename_all="lowercase")]
pub enum PyaketEntry {

    /// A module to run at runtime as (python -m module ...)
    Module(String),

    /// A script to bundle and run at runtime (python script.py ...)
    Script(String),

    /// A inline code snippet to run at runtime (python -c "code")
    Code(String),

    /// A command to run at runtime (command ...)
    Command(String),

    /// Launch the interpreter at runtime (fallback)
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
            if let Some(value) = envy::get(key) {
                return from(value);
            }
        }

        PyaketEntry::Interpreter
    }
}

/* -------------------------------------------------------------------------- */

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
#[serde(rename_all="lowercase")]
pub enum CargoProfile {
    #[default]
    Develop,
    Fast,
    Fastest,
    Small,
    Smallest,
}

impl Display for CargoProfile {
    fn fmt(&self, pipe: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let profile = match self {
            CargoProfile::Develop  => "develop",
            CargoProfile::Fast     => "fast",
            CargoProfile::Fastest  => "fastest",
            CargoProfile::Small    => "small",
            CargoProfile::Smallest => "smallest",
        };
        write!(pipe, "{}", profile)
    }
}

/* -------------------------------------------- */

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
#[serde(rename_all="lowercase")]
pub enum CargoType {
    #[default]
    Build,
    Zigbuild,
    Xwin,
}

impl Display for CargoType {
    fn fmt(&self, pipe: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let cargo = match self {
            CargoType::Build    => "build",
            CargoType::Zigbuild => "zigbuild",
            CargoType::Xwin     => "xwin",
        };
        write!(pipe, "{}", cargo)
    }
}

/* -------------------------------------------- */

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
#[serde(default)]
pub struct PyaketRelease {

    #[default(envy::uget("PYAKET_RELEASE_TARGET", ""))]
    pub target: String,

    // Fixme: How to enum env?
    pub profile: CargoProfile,
    pub cargo: CargoType,

    #[default(envy::ubool("PYAKET_RELEASE_UPX", false))]
    pub upx: bool,

    #[default(envy::ubool("PYAKET_RELEASE_TARBALL", false))]
    pub tarball: bool,
}

impl PyaketRelease {
    pub fn extension(&self) -> &str {
        if self.target.contains("windows") {
            "exe"
        } else {
            ""
        }
    }
}

/* -------------------------------------------------------------------------- */

pub static PYAKET_KEEP_OPEN: &str = "PYAKET_KEEP_OPEN";

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
#[serde(default)]
pub struct PyaketProject {
    pub application:  PyaketApplication,
    pub dependencies: PyaketDependencies,
    pub directories:  PyaketDirectories,
    pub python:       PyaketPython,
    pub torch:        PyaketTorch,
    pub entry:        PyaketEntry,
    pub release:      PyaketRelease,

    /// Hold the terminal open after runtime errors
    #[default(envy::ubool(PYAKET_KEEP_OPEN, false))]
    pub keep_open: bool,

    /// Unique identifier for any compiled binary
    #[default(Uuid::new_v4().to_string())]
    pub uuid: String,

    /// The platform target triple of the build
    #[cfg(not(runtime))]
    #[default(envy::get("TARGET").unwrap())]
    pub triple: String,
}

impl PyaketProject {
    pub fn release_name(&self) -> String {
        let mut name = String::new();
        name.push_str(&self.application.name.to_lowercase());
        name.push_str(&format!("-{}", self.release.target));
        name.push_str(&format!("-v{}", self.application.version));
        if let Some(_) = &self.torch.version {
            name.push_str(&format!("-{}", self.torch.backend));
        }
        if self.release.target.contains("windows") {
            name.push_str(".exe");
        }
        return name;
    }
}

/* -------------------------------------------- */

impl PyaketProject {
    pub fn json(&self) -> String {
        serde_json::to_string(&self).unwrap()
    }

    pub fn from_json(json: &str) -> Self {
        serde_json::from_str(json).unwrap()
    }

    pub fn toml(&self) -> String {
        toml::to_string(&self).unwrap()
    }

    pub fn from_toml(toml_str: &str) -> Self {
        toml::from_str(toml_str).unwrap()
    }
}
