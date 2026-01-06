#[path="pyaket/lib.rs"]
mod lib;
use lib::*;

/* -------------------------------------------------------------------------- */

mod manage {
    use super::*;

    pub fn wheels(project: &PyaketProject) -> Result<()> {
        if let Some(wheels) = &project.deps.wheels {
            for pattern in wheels.split(SEPARATOR) {
                for entry in glob::glob(pattern)?.flatten() {
                    logging::info!("Wheel: {}", entry.display());
                    WheelAssets::write(
                        entry.file_name().unwrap(),
                        &read(&entry)?,
                    )?;
                }
            }
        }

        Ok(())
    }

    pub fn reqtxt(project: &mut PyaketProject) -> Result<()> {
        // Todo: .read_file_or_keep() sugar
        if let Some(path) = &project.deps.reqtxt {
            project.deps.reqtxt = Some(read_string(path)?);
        }
        Ok(())
    }
}

/* -------------------------------------------------------------------------- */

fn build() -> Result<()> {

    // Workaround to always trigger a rebuild
    println!("cargo:rerun-if-changed=NULL");

    // Workaround for conditional compilation in build.rs, where
    // code marked as `#[cfg(not(runtime))]` is disabled
    #[cfg(rust_analyzer)]
    println!("cargo:rustc-cfg=runtime");

    // Get options from environment variables
    let mut project = PyaketProject::default();

    // Common assertions
    if project.app.name.is_empty() {
        bail!(logging::error!("Application name cannot be empty"))
    }

    ArchiveAssets::clear_files()?;

    WheelAssets::clear_files()?;
    manage::wheels(&project)?;
    manage::reqtxt(&mut project)?;

    // Executable resources (icon, metadata, etc)
    if project.triple.contains("windows") {
        logging::info!("Making Windows executable resources");
        let mut meta = winresource::WindowsResource::new();
        meta.set("ProductName",      &project.app.name);
        meta.set("CompanyName",      &project.app.author);
        meta.set("FileVersion",      &project.app.version);
        meta.set("FileDescription",  &project.app.about);
        meta.set("OriginalFilename", &envy::uget("OriginalFilename", "pyaket.exe"));
        meta.set("LegalCopyright",   &envy::uget("LegalCopyright", "Unknown"));
        if let Some(icon) = &project.app.icon {
            meta.set_icon(icon);
        }
        meta.compile()?;
    } else {
        // Linux: .desktop points to a file
        if let Some(icon) = &project.app.icon {
            ArchiveAssets::write(ASSET_ICON, &read(icon)?)?;
        }
    }

    // Export a const configured project to be loaded at runtime
    envy::rustc_export("PYAKET_PROJECT", project.json());
    logging::info!("Configuration: {}", project.json());

    Ok(())
}

fn main() {
    LazyLock::force(&START_TIME);
    logging::info!("Building Pyaket executable");
    build().unwrap();
}
