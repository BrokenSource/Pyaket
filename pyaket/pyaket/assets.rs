use rust_embed::Embed;
use std::fs::create_dir_all as mkdir;
use std::fs::remove_dir_all as rmdir;
use std::fs::write;
use std::path::Path;
use std::path::PathBuf;
use anyhow::Result;
use crate::envy;

pub static PYAKET_ASSETS: &str = "PYAKET_ASSETS";


/// All implementations **must** use the following:
///
/// ```rust
/// use pyaket::*;
///
/// #[derive(Embed)]
/// #[allow_missing=true]
/// #[folder="${PYAKET_ASSETS:-../.cache/<name>/files}"]
/// pub struct MyAssets;
///
/// impl PyaketAssets for MyAssets {
///     fn name() -> &'static str {
///         "MyAssets"
///     }
/// }
/// ```
pub trait PyaketAssets: Embed {

    /// Subdirectory for this instance
    fn name() -> &'static str;

    // Note: Non-runtime
    /// Global path for storing cache and final assets
    /// - Always overridden by $PYAKET_ASSETS variable
    /// - Editable install: `repository/.cache/`
    /// - Python package: `site-packages/.cache/`
    /// - Crates.io: I don't know.
    fn workspace() -> PathBuf {
        if let Some(path) = envy::get(PYAKET_ASSETS) {
            PathBuf::from(path)
        } else {
            PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .parent().unwrap()
                .join(".cache")
        }
    }

    // Note: Non-runtime
    // Unique workspace for this instance
    fn _root() -> PathBuf {
        Self::workspace().join(Self::name())
    }

    // Note: Non-runtime
    /// Directory for included files
    fn files_dir() -> PathBuf {
        Self::_root().join("files")
    }

    /// Directory for downloads cache
    #[cfg(not(runtime))]
    fn cache_dir() -> PathBuf {
        Self::_root().join("cache")
    }

    // Note: Non-runtime
    /// Delete and recreate the files directory
    fn clear_files() -> Result<()> {
        rmdir(Self::files_dir()).ok();
        mkdir(Self::files_dir())?;
        Ok(())
    }

    #[cfg(not(runtime))]
    fn clear_cache() -> Result<()> {
        rmdir(Self::cache_dir()).ok();
        mkdir(Self::cache_dir())?;
        Ok(())
    }

    /// Check if a file exists in the bundle
    fn exists(asset: &str) -> bool {
        Self::get(asset).is_some()
    }

    /// Read a single known file from the bundle
    fn read(asset: &str) -> Option<Vec<u8>> {
        Self::get(asset).map(|file| file.data.to_vec())
    }

    // Note: Non-runtime
    /// Write a file to be bundled
    fn write(path: impl AsRef<Path>, data: &Vec<u8>) -> Result<()> {
        let file = Self::files_dir().join(path);
        mkdir(file.parent().unwrap())?;
        write(file, data)?;
        Ok(())
    }

    /// Query all files in the bundle matching a path pattern
    fn glob_files(pattern: &str) -> Result<Vec<String>> {
        let engine = glob::Pattern::new(pattern)?;
        Ok(Self::iter()
            .filter(|file| engine.matches(file))
            .map(|file| file.to_string())
            .collect())
    }

    /// Returns the data of an `Self::glob_files()` query
    fn glob_data(pattern: &str) -> Result<Vec<Vec<u8>>> {
        Ok(Self::glob_files(pattern)?.iter()
            .map(|file| Self::get(file).unwrap().data.to_vec())
            .collect())
    }

    /// Returns the relative path and data matching a path pattern
    fn glob(pattern: &str) -> Result<Vec<(String, Vec<u8>)>> {
        let files = Self::glob_files(pattern)?;
        let data  = Self::glob_data(pattern)?;
        Ok(files.into_iter().zip(data).collect())
    }
}

/* -------------------------------------------------------------------------- */

#[derive(Embed)]
#[allow_missing=true]
#[folder="${PYAKET_ASSETS:-../.cache/wheels/files}"]
pub struct WheelAssets;

impl PyaketAssets for WheelAssets {
    fn name() -> &'static str {
        "wheels"
    }
}

#[derive(Embed)]
#[allow_missing=true]
#[folder="${PYAKET_ASSETS:-../.cache/archives/files}"]
pub struct ArchiveAssets;

impl PyaketAssets for ArchiveAssets {
    fn name() -> &'static str {
        "archives"
    }
}

/* -------------------------------------------------------------------------- */
// Common assets names

pub static ASSET_ICON: &str = "icon";
