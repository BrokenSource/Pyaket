use pyaket::*;

use clap::Parser;

pub static PYAKET_ROOT: OnceLock<PathBuf> = OnceLock::new();

/// Path where Cargo.toml is (Python package)
pub fn pyaket_root() -> &'static PathBuf {
    PYAKET_ROOT.get_or_init(|| {
        std::env::var_os("PYAKET_ROOT")
            .map(PathBuf::from)
            .unwrap_or_else(|| {
                current_dir().expect("Couldn't find cwd")
            })
    })
}

#[derive(Parser)]
pub struct PackerCLI {

    /// Path to a base pyaket.toml configuration file
    #[arg(env="PYAKET_CONFIG")]
    #[arg(short, long, default_value="pyaket.toml")]
    pub config: PathBuf,

    /// Cargo cache directory for compiled artifacts
    #[arg(env="CARGO_TARGET_DIR")]
    #[arg(long, default_value="target")]
    pub cache: PathBuf,

    /// Output directory for compiled binaries
    #[arg(env="PYAKET_RELEASE_DIR")]
    #[arg(short, long, default_value="release")]
    pub output: PathBuf,

    /// Rust target triple to compile, default to host (not checked)
    #[arg(env="PYAKET_TARGET")]
    #[arg(short, long)]
    pub target: Option<String>,
}

impl PackerCLI {
    fn compile(&self) -> Result<()> {

        // Todo: Parts from pyproject?
        let mut project = match &read_string(&self.config) {
            Ok(toml) => PyaketProject::from_toml(&toml),
            Err(_) => bail!(
                "Could not read configuration file {}",
                self.config.display()
            ),
        };

        logging::info!("Packer configuration: {}", project.json());

        ArchiveAssets::clear_files()?;
        WheelAssets::clear_files()?;

        // Copy wheels to assets
        for pattern in &project.dependencies.wheels {
            for entry in glob::glob(&pattern)?.flatten() {
                logging::info!("Wheel: {}", entry.display());
                WheelAssets::write(
                    entry.file_name().unwrap(),
                    &read(&entry)?,
                )?;
            }
        }

        // Bundle requirements.txt content
        if let Some(path) = &project.dependencies.reqtxt {
            project.dependencies.reqtxt = Some(read_string(path)?);
        }

        // Export winresource variables
        envy::set("ProductName",      &project.application.name);
        envy::set("CompanyName",      &project.application.author);
        envy::set("FileVersion",      &project.application.version);
        envy::set("FileDescription",  &project.application.about);
        envy::set("OriginalFilename", &project.release_name());
        envy::set("LegalCopyright",   &envy::uget("LegalCopyright", "Unknown"));

        // --------------------------------|

        /* Install host's toolchain */ {
            let mut rustup = subprocess::rustup()?;
            rustup.arg("default").arg("stable");
            subprocess::run(&mut rustup)?;
        }

        /* Install target toolchain */
        if let Some(target) = &self.target {
            let mut rustup = subprocess::rustup()?;
            rustup.arg("target").arg("add");
            rustup.arg(target);
            subprocess::run(&mut rustup)?;
        }

        // Export configuration for packer
        envy::set("PYAKET_PROJECT", &project.json());

        /* Compile a pyaket executable */ {
            let mut packer = Command::new("cargo");
            packer.arg(&project.release.cargo.to_string());
            packer.arg("--manifest-path").arg(pyaket_root().join("Cargo.toml"));
            packer.arg("--profile").arg(&project.release.profile.to_string());
            if let Some(target) = &self.target {
                packer.arg("--target").arg(target);
            }
            packer.arg("--target-dir").arg(&self.cache);
            // packer.arg("--features").arg("uv");
            packer.arg("--bin").arg("pyaket");
            subprocess::run(&mut packer)?;
        }

        /* Find the compiled binary */
        let compiled = self.cache
            .join(&project.triple)
            .join(&project.release.profile.to_string())
            .join("pyaket")
            .with_extension(project.extension());

        // Ensure the binary exists
        if !compiled.exists() {
            bail!(logging::error!("Missing compiled binary {}", compiled.display()));
        } else {
            logging::info!("Built binary at {}", compiled.display());
        }

        // Create output directory
        let release = self.output.join(project.release_name());
        mkdir(&self.output)?;
        copy(&compiled, &release)?;
        remove_file(&compiled)?;

        // Optional upx compression
        if project.release.upx {
            let mut cmd = Command::new("upx");
            cmd.arg("--best").arg("--lzma");
            cmd.arg(&release);
            subprocess::run(&mut cmd)?;
        }

        // Optional tar.gz to keep chmod +x attributes
        if project.release.tarball && !project.triple.contains("windows") {
            todo!("Should use external command or a crate for .tar.gz creation?");
        }

        logging::info!("Final project release at {}", release.display());
        Ok(())
    }

}

fn main() -> Result<()> {
    PackerCLI::try_parse()?.compile()
}
