use crate::*;

pub trait BrokenAssets: RustEmbed {

    /// Must match RustEmbed's `folder` attribute
    fn path() -> &'static str;

    /// Get a path to download assets to before bundling
    fn cache(path: &str) -> PathBuf {
        envy::cargo_toml()
            .parent().unwrap()
            .join(".cache/assets")
            .join(path)
    }

    /// Smart bundle a download (build.rs only!)
    fn download(path: &str, url: &str) -> Result<Vec<u8>> {
        let cache = Self::cache(path);
        let bytes = network::download(url, Some(&cache))?;
        Self::write(&path, &bytes)?;
        Ok(bytes)
    }

    /// Delete and recreate the bundle directory
    fn reset() -> Result<()> {
        rmdir(Self::path()).ok();
        mkdir(Self::path())?;
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
            None => network::download(url, Some(&path.into())),
            Some(data) => Ok(data),
        }
    }

    /// Write a file to be bundled (build.rs only!)
    fn write(path: impl AsRef<Path>, data: &[u8]) -> Result<()> {
        let file = envy::cargo_toml()
            .join(Self::path())
            .join(path);
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
#[folder="../.cache/bundle/wheels"]
pub struct WheelAssets;

impl BrokenAssets for WheelAssets {
    fn path() -> &'static str {
        "../.cache/bundle/wheels"
    }
}

#[derive(RustEmbed)]
#[allow_missing=true]
#[folder="../.cache/bundle/archives"]
pub struct ArchiveAssets;

impl BrokenAssets for ArchiveAssets {
    fn path() -> &'static str {
        "../.cache/bundle/archives"
    }
}