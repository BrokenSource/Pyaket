// Shared code in build.rs
#![allow(unused_imports)]
#![allow(dead_code)]

pub use std::fmt::Display;
pub use std::fs::create_dir_all as mkdir;
pub use std::fs::read_to_string as read_string;
pub use std::fs::read;
pub use std::fs::remove_dir_all as rmdir;
pub use std::fs::rename;
pub use std::fs::write;
pub use std::path::Path;
pub use std::path::PathBuf;
pub use std::process::Command;
pub use std::process::ExitCode;
pub use std::sync::LazyLock;
pub use std::sync::OnceLock;
pub use std::time::Instant;

pub use anyhow::bail;
pub use anyhow::Result;

pub mod assets;
pub mod envy;
pub mod logging;
pub mod project;
pub mod subprocess;
pub use assets::*;
pub use project::*;

#[cfg(runtime)]
pub mod runtime;

/// Time at which the program started
pub static START_TIME: LazyLock<Instant> = LazyLock::new(Instant::now);

/// Separator for environment variable lists
pub static SEPARATOR: &str = ";";

pub fn uv() -> Result<Command> {
    if cfg!(feature="uv") {
        let mut cmd = Command::new(std::env::current_exe()?);
        cmd.env("PYAKET_UV", "1");
        Ok(cmd)
    } else {
        Ok(Command::new("uv"))
    }
}
