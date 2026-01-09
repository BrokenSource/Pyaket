#[path="pyaket/lib.rs"]
mod lib;
use lib::*;

pub static PYAKET_PACKAGING: &str = "PYAKET_PACKAGING";

fn main() -> Result<()> {

    // Workaround to always trigger a rebuild
    println!("cargo:rerun-if-changed=NULL");

    // Workaround for conditional compilation build.rs shared lib:
    // - Code marked as `#[cfg(not(runtime))]` is build-only
    // - Code marked as `#[cfg(runtime)]` is runtime-only
    #[cfg(not(rust_analyzer))]
    println!("cargo:rustc-cfg=runtime");

    // Skip build script if not in packaging mode
    if !envy::ubool(PYAKET_PACKAGING, false) {
        logging::info!("Skipping build script per non-packaging mode");
        return Ok(());
    }

    LazyLock::force(&START_TIME);
    logging::info!("Building Pyaket executable");

    // Get options from environment variables
    let mut project = PyaketProject::default();

    // Common assertions
    if project.app.name.is_empty() {
        bail!(logging::error!("Application name cannot be empty"))
    }

    ArchiveAssets::clear_files()?;
    WheelAssets::clear_files()?;

    // Bundle wheel files
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

    // Bundle requirements.txt content
    if let Some(path) = &project.deps.reqtxt {
        project.deps.reqtxt = Some(read_string(path)?);
    }

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
