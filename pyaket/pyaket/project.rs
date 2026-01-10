use crate::*;

use serde::Deserialize;
use serde::Serialize;
use smart_default::SmartDefault;

/* -------------------------------------------- */
// https://pyaket.dev/docs/config/application/

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
pub struct PyaketApplication {
    pub name: String,
    pub author: String,
    pub vendor: Option<String>,
    pub version: String,
    pub about: String,
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

/* -------------------------------------------- */
// https://pyaket.dev/docs/config/dependencies/

// Note: Wheels go in assets glob
#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
pub struct PyaketDependencies {
    pub pypi: Vec<String>,
    pub reqtxt: Option<String>,
    pub rolling: bool,
}

/* -------------------------------------------- */
// https://pyaket.dev/docs/config/directories/

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
pub struct PyaketDirectories {
    pub common: String,
    pub versions: String,
}

/* -------------------------------------------- */
// https://pyaket.dev/docs/config/python

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
pub struct PyaketPython {
    pub version: String,
}

impl PyaketPython {
    pub fn is_freethreaded(&self) -> bool {
        self.version.contains("t")
    }
}

/* -------------------------------------------- */
// https://pyaket.dev/docs/config/pytorch

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
pub struct PyaketTorch {
    pub version: Option<String>,
    pub backend: String,
}

/* -------------------------------------------- */
// https://pyaket.dev/docs/config/entry

// Fixme: Should be enum, teach pydantic variants
#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
pub struct PyaketEntry {
    pub module:  Option<String>,
    pub command: Option<String>,
}

/* -------------------------------------------- */

#[derive(SmartDefault)]
#[derive(Serialize, Deserialize)]
pub struct PyaketProject {
    pub app:    PyaketApplication,
    pub deps:   PyaketDependencies,
    pub dirs:   PyaketDirectories,
    pub python: PyaketPython,
    pub torch:  PyaketTorch,
    pub entry:  PyaketEntry,
    pub uuid:   String,

    #[default(false)]
    #[serde(default)]
    pub keep_open: bool,

    /// The platform target triple of the build
    #[serde(default)]
    #[default(envy::get("TARGET").unwrap())]
    pub triple: String,
}

/* -------------------------------------------- */

impl PyaketProject {
    pub fn json(&self) -> String {
        serde_json::to_string(&self).unwrap()
    }

    pub fn from_json(json: &str) -> Self {
        serde_json::from_str(json).unwrap()
    }
}
