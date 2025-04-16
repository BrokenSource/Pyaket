#![allow(unused_imports)]
#![allow(non_snake_case)]
#![allow(dead_code)]

pub use std::{env, fs, io};
pub use std::process::{Command, ExitStatus, ExitCode};
pub use std::fmt::Display;
pub use std::path::{PathBuf, Path};
pub use std::time::Instant;
pub use std::fs::read_to_string as read_string;
pub use std::fs::create_dir_all as mkdir;
pub use std::fs::remove_dir_all as rmdir;
pub use std::fs::{read, write, rename};
pub use std::sync::{OnceLock, LazyLock};

pub use xxhash_rust::xxh3::xxh3_64;
pub use serde::{Serialize, Deserialize};
pub use spinners::{Spinner, Spinners};
pub use smart_default::SmartDefault;
pub use anyhow::{bail, Result};
pub use directories::BaseDirs;
pub use rust_embed::Embed;
pub use uuid::Uuid;
pub use temp_dir::TempDir;

/* -------------------------------------------------------------------------- */
// Pretty printing log macros that works both in build.rs and main.rs

pub static START_TIME: LazyLock<Instant> = LazyLock::new(Instant::now);

pub mod log {

    #[allow(unused_imports)]
    pub use crate::{info, warn, error, note};

    #[macro_export]
    macro_rules! make_log {
        ($level:expr, $color:expr, $($tokens:tt)*) => {
            let elapsed: f32 = (START_TIME.elapsed().as_millis() as f32)/1000.0;
            println!(
                "cargo::warning=\r\
                │\x1b[34mPyaket\x1b[0m├\
                ┤\x1b[\x1b[32m{}\x1b[0m├\
                ┤\x1b[{}m{}\x1b[0m│ ▸ {}",
                format!("{}'{:06.3}", (elapsed/60.0).floor(), (elapsed%60.0)),
                $color, $level, format!($($tokens)*)
            );
        };
    }

    #[macro_export] macro_rules! info  {
        ($($tokens:tt)*) => {$crate::make_log!("INFO ", 39, $($tokens)*)}}
    #[macro_export] macro_rules! warn  {
        ($($tokens:tt)*) => {$crate::make_log!("WARN ", 33, $($tokens)*)}}
    #[macro_export] macro_rules! note  {
        ($($tokens:tt)*) => {$crate::make_log!("NOTE ", 34, $($tokens)*)}}
    #[macro_export] macro_rules! error {
        ($($tokens:tt)*) => {$crate::make_log!("ERROR", 31, $($tokens)*)}}
}

/* -------------------------------------------------------------------------- */

pub struct Environment;

impl Environment {

    /// Set an environment variable to a value
    pub fn set(name: &str, value: impl Display) {
        unsafe {env::set_var(name, format!("{}", value))}
    }

    /// Calls `set()` if the variable does not exist
    pub fn setdefault(name: &str, value: impl Display) {
        if env::var(name).is_err() {
            Environment::set(name, value);
        }
    }

    /// Remove a variable from the environment
    pub fn unset(name: &str) {
        unsafe {env::remove_var(name)}
    }

    /// Get a string from the environment, optional default
    pub fn get(name: &str, default: Option<&str>) -> Option<String> {
        env::var(name).ok().or(default.map(|x| x.to_string()))
    }

    /// Get a string from the environment, required default
    pub fn uget(name: &str, default: &str) -> String {
        Environment::get(name, Some(default)).unwrap()
    }

    /// Parse a bool from an environment variable, optional default
    pub fn bool(name: &str, default: Option<bool>) -> Option<bool> {
        match env::var(name).ok() {
            Some(value) => match value.to_lowercase().as_str() {
                "false" | "0" | "no"  | "off" => Some(false),
                "true"  | "1" | "yes" | "on"  => Some(true),
                _ => None,
            },
            None => default,
        }
    }

    /// Parse a bool from an environment variable, required default
    pub fn ubool(name: &str, default: bool) -> bool {
        Environment::bool(name, Some(default)).unwrap()
    }

    /// Get all environment variables names
    pub fn keys() -> Vec<String> {
        env::vars().map(|(k, _)| k).collect()
    }

    /// Check if an environment variable exists
    pub fn exists(name: &str) -> bool {
        env::var(name).is_ok()
    }

    /* ---------------------------------------- */
    // Exporting and printing

    /// Print an environment variable
    pub fn print(name: &str) {
        println!("{}={}", name, Environment::uget(name, "#Unset#"))
    }

    /// Pass a compile time environment variable to the binary
    /// - Warn: Must be acessed via env!(literal) at runtime
    pub fn rustc_export(name: &str, value: impl Display) {
        println!("cargo:rustc-env={}={}", name, value);
    }

    /// Path where Cargo.toml is located
    fn repository_root() -> PathBuf {
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
    }
}

/* -------------------------------------------------------------------------- */
// Subprocess utils

pub mod subprocess {
    use super::*;

    pub fn run(command: &mut Command) -> Result<()> {
        log::info!("Call ({:?})", command);
        command.spawn()?.wait()?;
        Ok(())
    }
}

/* -------------------------------------------------------------------------- */
// Compression utils

pub mod archive {
    use super::*;
    use std::io::{Cursor, Read, Seek};
    use zstd::stream::read::Decoder as ZsDecoder;
    use flate2::read::GzDecoder;
    use bzip2::read::BzDecoder;
    use zip::ZipArchive;

    /// Writes a tar stream of data to a directory
    fn unpack_tar<R: Read>(decoder: R, path: &Path) -> Result<()> {
        tar::Archive::new(decoder).unpack(path)?;
        Ok(())
    }

    /// Unpack common archive formats in-memory to a directory
    pub fn unpack_bytes(
        bytes: &Vec<u8>,
        path:  impl AsRef<Path>,
        flag:  Option<&str>,
    ) -> Result<()> {

        // Unique identifer for unpacked data
        let hash = xxh3_64(bytes).to_string();
        let flag = path.as_ref()
            .join(flag.unwrap_or("archive"))
            .with_extension("unpack");

        // Skip unpacking on same ok once data
        if let Ok(data) = read_string(&flag) {
            if data == hash {
                return Ok(());
            } else {
                rmdir(&path)?;
            }
        }

        // Can take a while on weak Disks/CPU
        let mut spinner = Spinner::new(
            Spinners::Dots, format!("Unpacking file ({})",
            path.as_ref().display())
        );

        // Identify the archive format by the magic bytes
        let mut cursor = Cursor::new(bytes.as_slice());
        let mut magic = [0u8; 6];
        cursor.read_exact(&mut magic)?;
        cursor.seek(io::SeekFrom::Start(0))?;
        match magic {
            [0x50, 0x4B, 0x03, 0x04, ..] => ZipArchive::new(cursor)?.extract(path.as_ref())?,
            [0x28, 0xB5, 0x2F, 0xFD, ..] => unpack_tar(ZsDecoder::new(cursor)?, path.as_ref())?,
            [0x42, 0x5A, ..            ] => unpack_tar(BzDecoder::new(cursor),  path.as_ref())?,
            [0x1F, 0x8B, ..            ] => unpack_tar(GzDecoder::new(cursor),  path.as_ref())?,
            _ => bail!("Unknown archive format for magic bytes: {:?}", magic),
        }
        spinner.stop_with_message("\r".into());
        write(flag, hash)?;
        Ok(())
    }

    /// Unpack common archive formats from a file to a directory
    pub fn unpack_file(
        archive: impl AsRef<Path>,
        path:    impl AsRef<Path>,
        flag:    Option<&str>,
    ) -> Result<()> {
        archive::unpack_bytes(&read(archive)?, path, flag)
    }
}

/* -------------------------------------------------------------------------- */
// Network utils

pub mod network {
    use super::*;

    /// Check if URL is reachable and returns a 200 OK status
    pub fn exists(url: &str) -> Result<bool, ureq::Error> {
        let response = ureq::head(url).call()?;
        Ok(response.status().is_success())
    }

    /// Syntactic sugar for `bail!` on `!exists(url)`
    pub fn must_exist(url: &str) -> Result<()> {
        if !network::exists(url)? {
            bail!("Download url is not valid: {}", url)}
        Ok(())
    }

    /// In-memory download an url to a byte vector
    pub fn download_bytes(url: &str) -> Result<Vec<u8>> {
        Ok(ureq::get(url).call()?.body_mut()
            .with_config().limit(100 * 1024 * 1024)
            .read_to_vec()?)
    }

    /// Download to a file
    pub fn download_file(url: &str, path: &PathBuf) -> Result<Vec<u8>> {
        match path.exists() {
            true => Ok(read(path)?),
            false => {
                let bytes = network::download_bytes(&url)?;
                let temp = path.with_extension("part");
                mkdir(&path.parent().unwrap())?;
                write(&temp, &bytes)?;
                rename(&temp, &path)?;
                Ok(bytes)
            }
        }
    }

    /// Smart download to a path or in-memory
    pub fn download(url: &str, path: Option<&PathBuf>) -> Result<Vec<u8>> {
        match path {
            Some(path) => network::download_file(&url, path),
            None => network::download_bytes(&url),
        }
    }
}

/* -------------------------------------------------------------------------- */

pub trait BrokenAssets: Embed {

    /// Must match `#[derive(Embed)]`'s `folder` attribute
    fn path() -> &'static str;

    /// Get a path to download assets to before bundling
    fn cache(path: &str) -> PathBuf {
        Environment::repository_root()
            .join(".cache/pyaket")
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
    fn exists(path: &str) -> bool {
        Self::get(path).is_some()
    }

    /// Read a single known file from the bundle
    fn read(path: &str) -> Option<Vec<u8>> {
        Self::get(path).map(|file| file.data.to_vec())
    }

    fn read_or_download(bundle: &str, cache: &PathBuf, url: &str) -> Result<Vec<u8>> {
        match Self::read(bundle) {
            None => network::download(url, Some(&cache.into())),
            Some(data) => Ok(data),
        }
    }

    /// Write a file to be bundled (build.rs only!)
    fn write(path: impl AsRef<Path>, data: &Vec<u8>) -> Result<()> {
        let file = Environment::repository_root()
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

#[derive(Embed)] #[allow_missing=true]
#[folder="../.cache/bundle/wheels"]
pub struct WheelAssets;

impl BrokenAssets for WheelAssets {
    fn path() -> &'static str {
        "../.cache/bundle/wheels"
    }
}

#[derive(Embed)] #[allow_missing=true]
#[folder="../.cache/bundle/archives"]
pub struct ArchiveAssets;

impl BrokenAssets for ArchiveAssets {
    fn path() -> &'static str {
        "../.cache/bundle/archives"
    }
}

/* -------------------------------------------------------------------------- */

static WORKSPACE_ROOT: OnceLock<PathBuf> = OnceLock::new();

// Define environment configuration literals for consistency
pub static PYAKET_APP_NAME:           &str = "PYAKET_APP_NAME";
pub static PYAKET_APP_AUTHOR:         &str = "PYAKET_APP_AUTHOR";
pub static PYAKET_APP_VERSION:        &str = "PYAKET_APP_VERSION";
pub static PYAKET_VERSIONS_DIR:       &str = "PYAKET_VERSIONS_DIR";
pub static PYAKET_APP_WHEELS:         &str = "PYAKET_APP_WHEELS";
pub static PYAKET_APP_PYPI:           &str = "PYAKET_APP_PYPI";
pub static PYAKET_APP_REQTXT:         &str = "PYAKET_APP_REQTXT";
pub static PYAKET_PYTHON_VERSION:     &str = "PYAKET_PYTHON_VERSION";
pub static PYAKET_PYTHON_BUNDLE:      &str = "PYAKET_PYTHON_BUNDLE";
pub static PYAKET_UV_VERSION:         &str = "PYAKET_UV_VERSION";
pub static PYAKET_UV_BUNDLE:          &str = "PYAKET_UV_BUNDLE";
pub static PYAKET_TORCH_VERSION:      &str = "PYAKET_TORCH_VERSION";
pub static PYAKET_TORCH_BACKEND:      &str = "PYAKET_TORCH_BACKEND";
pub static PYAKET_ENTRY_MODULE:       &str = "PYAKET_ENTRY_MODULE";
pub static PYAKET_ENTRY_SCRIPT:       &str = "PYAKET_ENTRY_SCRIPT";
pub static PYAKET_ENTRY_CODE:         &str = "PYAKET_ENTRY_CODE";
pub static PYAKET_ENTRY_COMMAND:      &str = "PYAKET_ENTRY_COMMAND";
pub static PYAKET_COMMON_DIR:         &str = "PYAKET_COMMON_DIR";
pub static PYAKET_TARGET_TRIPLE:      &str = "PYAKET_TARGET_TRIPLE";
pub static PYAKET_ROLLING:            &str = "PYAKET_ROLLING";
pub static PYAKET_KEEP_OPEN:          &str = "PYAKET_KEEP_OPEN";

#[derive(Serialize, Deserialize, SmartDefault)]
pub struct Project {

    /* ---------------------------------------- */
    // Application configuration

    /// The name of the application
    #[default(Environment::uget(PYAKET_APP_NAME, "Application"))]
    pub app_name: String,

    /// The author of the application
    #[default(Environment::uget(PYAKET_APP_AUTHOR, "BrokenSource"))]
    pub app_author: String,

    /// The version of the application
    #[default(Environment::uget(PYAKET_APP_VERSION, "0.0.0"))]
    pub app_version: String,

    /// Subdirectory of the workspace for versions to coexist
    /// - Default: `$WORKSPACE/Versions/`
    #[default(Environment::uget(PYAKET_VERSIONS_DIR, "Versions"))]
    pub versions_dir: String,

    /// List of local Python wheels to install at runtime separated by ':'
    /// - Example: "./dist/foo.whl:./dist/bar.whl:./dist/baz.whl"
    #[serde(skip)]
    #[default(Environment::uget(PYAKET_APP_WHEELS, ""))]
    pub wheels: String,

    /// List of PyPI packages to install at runtime separated by ':'
    /// - Example: "numpy:pydantic==2.11.2:uv>=0.6.10"
    #[default(Environment::uget(PYAKET_APP_PYPI, ""))]
    pub pypi: String,

    /// A requirements.txt file to install at runtime
    /// - Example: "./requirements.txt"
    #[default(Environment::uget(PYAKET_APP_REQTXT, ""))]
    pub reqtxt: String,

    /* ---------------------------------------- */
    // Python distribution

    /// Python version to use at runtime
    #[default(Environment::uget(PYAKET_PYTHON_VERSION, "3.13"))]
    pub python_version: String,

    /// Whether to bundle Python in the application or download at runtime
    #[default(Environment::ubool(PYAKET_PYTHON_BUNDLE, false))]
    pub python_bundle: bool,

    /* ---------------------------------------- */
    // Astral uv distribution

    /// The version of uv to use at runtime
    #[default(Environment::uget(PYAKET_UV_VERSION, "0.6.13"))]
    pub uv_version: String,

    /// Whether to bundle uv in the application
    #[default(Environment::ubool(PYAKET_UV_BUNDLE, false))]
    pub uv_bundle: bool,

    /* ---------------------------------------- */
    // PyTorch

    /// Installs a specific version of PyTorch, e.g. `2.6.0` or none (unset)
    /// - **Warning**: Runtime only installation, collect and bundle wheels for offline
    /// - **Experimental**: https://docs.astral.sh/uv/guides/integration/pytorch/
    #[default(Environment::uget(PYAKET_TORCH_VERSION, ""))]
    pub torch_version: String,

    /// A PyTorch backend to install at runtime, e.g. `auto`, `cpu`, `cu124`, `rocm6.2`
    /// - **Warning**: Runtime only installation, collect and bundle wheels for offline
    /// - **Experimental**: https://docs.astral.sh/uv/guides/integration/pytorch/
    #[default(Environment::uget(PYAKET_TORCH_BACKEND, "auto"))]
    pub torch_backend: String,

    /* ---------------------------------------- */
    // Entry points

    /// Run an installed module to be run as `python -m module`
    #[default(Environment::uget(PYAKET_ENTRY_MODULE, ""))]
    pub entry_module: String,

    /// Run a bundled script at runtime
    #[default(Environment::uget(PYAKET_ENTRY_SCRIPT, ""))]
    pub entry_script: String,

    /// Run a single line of python code at runtime
    /// - Example: `from module import main; main()`
    #[default(Environment::uget(PYAKET_ENTRY_CODE, ""))]
    pub entry_code: String,

    /// Run a custom command inside the virtual environment at runtime
    /// - Scripts are often defined in `[project.scripts]` in `pyproject.toml`
    /// - This can be used to hardcode arguments, like `depthflow gradio`
    #[default(Environment::uget(PYAKET_ENTRY_COMMAND, ""))]
    pub entry_command: String,

    /* ---------------------------------------- */

    /// A unique identifier to this compiled binary
    #[default(Uuid::new_v4().to_string())]
    pub uuid: String,

    /// The platform target triple of the build
    #[default(Environment::uget(PYAKET_TARGET_TRIPLE, env::var("TARGET").unwrap().as_str()))]
    pub triple: String,

    #[default(Environment::uget(PYAKET_COMMON_DIR, "Pyaket"))]
    pub common_dir: String,

    /// Shall a binary always reinstall latest pypi or git+ dependencies
    #[default(Environment::ubool(PYAKET_ROLLING, false))]
    pub rolling: bool,

    /// Keep the terminal open after errors
    #[default(Environment::ubool(PYAKET_KEEP_OPEN, false))]
    pub keep_open: bool,
}

/* -------------------------------------------------------------------------- */

impl Project {

    pub fn python_install_dir(&self) -> PathBuf {
        self.workspace_common().join("Python")
    }

    /// The uv archive filename without extensions, e.g.:
    /// - `uv-0.6.11-x86_64-unknown-linux-gnu`
    pub fn uv_archive_stem(&self) -> String {
        format!("uv-{}", self.triple.replace("windows-gnu", "windows-msvc"))
    }

    /// The download filename of the uv distribution, e.g.:
    /// - `uv-0.6.11-x86_64-unknown-linux-gnu.tar.gz`
    pub fn uv_archive_name(&self) -> String {
        format!("{}.{}", self.uv_archive_stem(),
            if self.triple.contains("windows") {"zip"} else {"tar.gz"}
        )
    }

    /// The download URL of the uv distribution
    pub fn uv_download_url(&self) -> String {
        format!(
            "{}/releases/download/{}/{}",
            "https://github.com/astral-sh/uv",
            self.uv_version,
            self.uv_archive_name(),
        )
    }

    /// Path to unpack uv at runtime
    pub fn uv_unpack_dir(&self) -> PathBuf {
        self.astral_dir()
            .join(&self.uv_version)
    }

    /// Path to download and cache uv at runtime
    pub fn uv_download_file(&self) -> PathBuf {
        self.uv_unpack_dir()
            .join(&self.uv_archive_name())
    }

    pub fn ensure_uv(&self) -> Result<()> {
        let bytes = ArchiveAssets::read_or_download(
            &self.uv_archive_name(),
            &self.uv_download_file(),
            &self.uv_download_url(),
        )?;
        archive::unpack_bytes(
            &bytes, self.uv_unpack_dir(),
            Some(&self.uv_archive_stem())
        )?;
        Ok(())
    }

    /// Get a command starting with uv executable
    pub fn uv(&self) -> Command {
        let pattern = format!("{}/**/uv{}",
            self.uv_unpack_dir().display(),
            env::consts::EXE_EXTENSION);

        Command::new(glob::glob(&pattern)
            .expect("Invalid glob pattern")
            .filter_map(Result::ok).next()
            .expect("uv executable not found"))
    }
}

/* -------------------------------------------------------------------------- */
// Workspace

impl Project {

    /// - Automatic:
    ///   - Windows: `%LocalAppData%/Author/`
    ///   - Linux: `~/.local/share/Author/`
    ///   - MacOS: `~/Library/Application Support/Author/`
    ///
    /// - Custom:
    ///   - Any: `$WORKSPACE/`
    ///
    pub fn workspace_root(&self) -> &'static PathBuf {
        WORKSPACE_ROOT.get_or_init(|| {
            if let Ok(custom) = env::var("WORKSPACE") {
                PathBuf::from(custom)
            } else {
                BaseDirs::new().unwrap()
                    .data_local_dir()
                    .join(&self.app_author)
            }
        })
    }

    /// A common directory to store common unpacked assets
    pub fn workspace_common(&self) -> PathBuf {
        self.workspace_root()
            .join(&self.common_dir)
    }

    pub fn astral_dir(&self) -> PathBuf {
        self.workspace_common()
            .join("Astral")
    }

    pub fn uv_cache_dir(&self) -> PathBuf {
        self.workspace_common()
            .join("Cache")
    }

    /// Where to install the Python's virtual environment:
    /// - `$WORKSPACE/Versions/1.0.0`
    pub fn installation_dir(&self) -> PathBuf {
        self.workspace_common()
            .join(&self.versions_dir)
            .join(&self.app_version)
    }

    /// A file that tracks installs from unique binaries for a few purposes:
    /// - Flags if the installation was successful to skip bootstrapping
    /// - Triggers a reinstall if the hash differs for same versions
    pub fn uuid_tracker_file(&self) -> PathBuf {
        self.installation_dir()
            .join(format!("{}.uuid", self.app_name))
    }

    /* ---------------------------------------- */
    // Serialization

    pub fn json(&self) -> String {
        serde_json::to_string(&self).unwrap()
    }

    pub fn from_json(json: &str) -> Project {
        serde_json::from_str(json).unwrap()
    }
}
