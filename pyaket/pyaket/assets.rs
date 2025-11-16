use crate::*;

pub static PYAKET_ASSETS: &str = "PYAKET_ASSETS";

/// Global path for storing cache and/or final assets in subdirectories
/// - Always overriden by environment variable
/// - Editable install: `repository/.cache/`
/// - Python package: `site-packages/.cache/`
/// - Crates.io build: I don't know.
#[cfg(not(runtime))]
fn workspace() -> PathBuf {

    // Optional custom directory
    if let Some(path) = envy::get(PYAKET_ASSETS, None) {
        return PathBuf::from(path);
    }

    // Otherwise the repository root
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent().unwrap()
        .join(".cache")
}

/// All implementations **must** use the following:
///
/// ```rust
/// #[derive(RustEmbed)]
/// #[allow_missing=true]
/// #[folder="${PYAKET_ASSETS:-../.cache/name()/files}"]
/// pub struct MyAssets;
///
/// impl PyaketAssets for MyAssets { ... }
/// ```
pub trait PyaketAssets: RustEmbed {

    /// Subdirectory for this instance
    fn name() -> &'static str;

    // Unique workspace for this instance
    #[cfg(not(runtime))]
    fn _root() -> PathBuf {
        workspace().join(Self::name())
    }

    /// Directory for included files
    #[cfg(not(runtime))]
    fn files_dir() -> PathBuf {
        Self::_root().join("files")
    }

    /// Directory for downloads cache
    #[cfg(not(runtime))]
    fn cache_dir() -> PathBuf {
        Self::_root().join("cache")
    }

    /// Smart bundle a download
    #[cfg(not(runtime))]
    fn download(path: &str, url: &str) -> Result<Vec<u8>> {
        let cache = &Self::cache_dir().join(path);
        let bytes = network::download_file(url, &cache)?;
        Self::write(&path, &bytes)?;
        Ok(bytes)
    }

    /// Delete and recreate the files directory
    #[cfg(not(runtime))]
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

    /// Compound function to read from bundle or download to a static file at runtime
    fn read_or_download(asset: &str, url: &str, path: &PathBuf) -> Result<Vec<u8>> {
        match Self::read(asset) {
            None => network::download_file(url, &path),
            Some(data) => Ok(data),
        }
    }

    /// Write a file to be bundled
    #[cfg(not(runtime))]
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
        Ok(files.into_iter().zip(data.into_iter()).collect())
    }
}

/* -------------------------------------------------------------------------- */

#[derive(RustEmbed)]
#[allow_missing=true]
#[folder="${PYAKET_ASSETS:-../.cache/wheels/files}"]
pub struct WheelAssets;

impl PyaketAssets for WheelAssets {
    fn name() -> &'static str {
        "wheels"
    }
}

#[derive(RustEmbed)]
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
