use rust_embed::Embed;
use anyhow::Result;

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
/// impl PyaketAssets for MyAssets {}
/// ```
pub trait PyaketAssets: Embed {

    /// Check if a file exists in the bundle
    fn exists(asset: &str) -> bool {
        Self::get(asset).is_some()
    }

    /// Read a single known file from the bundle
    fn read(asset: &str) -> Option<Vec<u8>> {
        Self::get(asset).map(|file| file.data.to_vec())
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
#[folder="${PYAKET_ASSETS:-../.cache/wheels}"]
pub struct WheelAssets;

impl PyaketAssets for WheelAssets {}

#[derive(Embed)]
#[allow_missing=true]
#[folder="${PYAKET_ASSETS:-../.cache/archives}"]
pub struct ArchiveAssets;

impl PyaketAssets for ArchiveAssets {}

/* -------------------------------------------------------------------------- */
// Common assets names

pub static ASSET_ICON: &str = "icon";
