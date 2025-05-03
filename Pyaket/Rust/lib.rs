// Most code is used in build.rs
#![allow(unused_imports)]
#![allow(dead_code)]

pub use std::fmt::Display;
pub use std::fs::create_dir_all as mkdir;
pub use std::fs::read;
pub use std::fs::read_to_string as read_string;
pub use std::fs::remove_dir_all as rmdir;
pub use std::fs::rename;
pub use std::fs::write;
pub use std::io::Cursor;
pub use std::io::Read;
pub use std::io::Seek;
pub use std::io::SeekFrom;
pub use std::path::Path;
pub use std::path::PathBuf;
pub use std::process::Command;
pub use std::sync::LazyLock;
pub use std::sync::OnceLock;
pub use std::time::Instant;

pub use anyhow::Result;
pub use anyhow::bail;
pub use directories::BaseDirs;
pub use rust_embed::Embed as RustEmbed;
pub use serde::Deserialize;
pub use serde::Serialize;
pub use smart_default::SmartDefault;
pub use temp_dir::TempDir;
pub use uuid::Uuid;
pub use xxhash_rust::xxh3::xxh3_64;

pub mod archive;
pub mod assets;
pub use assets::*;
pub mod environment;
pub use environment::*;
pub mod logging;
pub mod network;
pub use network::*;
pub mod project;
pub use project::*;
pub mod subprocess;

/// Time at which the program started, used for logging
pub static START_TIME: LazyLock<Instant> = LazyLock::new(Instant::now);
