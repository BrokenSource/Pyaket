// Shared code in build.rs
#![allow(unused_imports)]
#![allow(dead_code)]

pub use std::env::current_dir;
pub use std::env::current_exe;
pub use std::fmt::Display;
pub use std::fs::copy;
pub use std::fs::create_dir_all as mkdir;
pub use std::fs::read_to_string as read_string;
pub use std::fs::read;
pub use std::fs::remove_dir_all as rmdir;
pub use std::fs::remove_file;
pub use std::fs::rename;
pub use std::fs::write;
pub use std::path::Path;
pub use std::path::PathBuf;
pub use std::process::Command;
pub use std::process::ExitCode;
pub use std::sync::LazyLock;
pub use std::sync::OnceLock;

pub use anyhow::bail;
pub use anyhow::Result;

pub mod assets;
pub mod envy;
pub mod logging;
pub mod project;
pub mod subprocess;
pub use assets::*;
pub use logging::*;
pub use project::*;

#[cfg(runtime)]
pub mod runtime;

/// Separator for environment variable lists
pub static SEPARATOR: &str = ";";

pub fn uv() -> Result<Command> {
    let mut cmd = Command::new(current_exe()?);
    cmd.arg("self").arg("uv");
    Ok(cmd)
}

// Idea: Bundle rustup on packer?
pub fn rustup() -> Result<Command> {
    let cmd = Command::new("rustup");
    Ok(cmd)
}

/* -------------------------------------------------------------------------- */

#[cfg(feature="pyo3")]
use pyo3::prelude::*;

#[pymodule]
#[cfg(feature="pyo3")]
mod _pyaket {
    use super::*;

    #[pyfunction]
    #[pyo3(signature = (*args))]
    fn cli(args: Vec<String>) -> PyResult<()> {
        println!("Futurely running packer cli with args: {:?}", args);
        // crate::packer::main::PackerCLI::parse_from(args);
        Ok(())
    }
}
