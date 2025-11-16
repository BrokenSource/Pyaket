#[path="pyaket/lib.rs"]
mod lib;
use lib::*;

/* -------------------------------------------------------------------------- */

mod manage {
    use super::*;

    pub fn wheels(project: &PyaketProject) -> Result<()> {

        // Don't trust the user on ';'.join(wheels) formatting
        for wheel in project.app.wheels.split(";")
            .map(|x| x.trim()).filter(|x| !x.is_empty())
        {
            // Interpret as glob pattern to allow `/path/*.whl` sugar
            for file in glob::glob(wheel)?.map(|x| x.unwrap()) {
                logging::info!("Wheel: {}", file.display());
                WheelAssets::write(
                    file.file_name().unwrap(),
                    &read(&file).unwrap(),
                )?;
            }
        }

        Ok(())
    }

    pub fn reqtxt(project: &mut PyaketProject) -> Result<()> {
        // Todo: .read_file_or_keep() sugar
        if Path::new(&project.app.reqtxt).exists() {
            project.app.reqtxt = read_string(&project.app.reqtxt)?;
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
        if let Some(icon) = &project.app.icon {
            ArchiveAssets::write(ASSET_ICON, &read(icon)?)?;
        }
    }

    // Export a const configured project to be loaded at runtime
    envy::rustc_export("PYAKET_PROJECT", project.json());
    logging::info!("Project: {}", project.json());

    Ok(())
}

fn main() {
    LazyLock::force(&START_TIME);
    logging::info!("Building pyaket project");
    build().unwrap();
}
