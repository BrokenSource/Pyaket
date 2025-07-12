#[path="pyaket/lib.rs"]
mod lib;
use lib::*;

/* ---------------------------------------------------------------------------------------------- */

mod manage {
    use super::*;

    // Todo: Find a way to match against uv
    pub fn python(project: &Project) -> Result<()> {
        if project.python.bundle {
            logging::warn!("Bundling Python is not implemented yet")
        }
        Ok(())
    }

    pub fn astral(project: &Project) -> Result<()> {
        network::must_exist(&project.uv_download_url())?;

        if project.astral.bundle {
            ArchiveAssets::download(
                &project.uv_archive_name(),
                &project.uv_download_url(),
            )?;
        }

        Ok(())
    }

    pub fn wheels(project: &Project) -> Result<()> {

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

    pub fn reqtxt(project: &mut Project) -> Result<()> {
        // Todo: .read_file_or_keep() sugar
        if Path::new(&project.app.reqtxt).exists() {
            project.app.reqtxt = read_string(&project.app.reqtxt)?;
        }
        Ok(())
    }
}

/* ---------------------------------------------------------------------------------------------- */

fn build() -> Result<()> {
    // Workaround to always trigger a rebuild
    println!("cargo:rerun-if-changed=NULL");

    // Build the project from current settings
    let mut project = Project::default();

    ArchiveAssets::reset()?;
    manage::python(&project)?;
    manage::astral(&project)?;

    WheelAssets::reset()?;
    manage::wheels(&project)?;
    manage::reqtxt(&mut project)?;

    // Windows executable resources metadata
    if std::env::var("CARGO_CFG_TARGET_OS").unwrap() == "windows" {
        logging::info!("Making windows executable resources");
        let mut meta = winresource::WindowsResource::new();
        meta.set("ProductName",      &project.app.name);
        meta.set("CompanyName",      &project.app.author);
        meta.set("FileVersion",      &project.app.version);
        meta.set("FileDescription",  &project.app.description);
        meta.set("OriginalFilename", &envy::uget("OriginalFilename", "pyaket.exe"));
        meta.set("LegalCopyright",   &envy::uget("LegalCopyright", "Unknown"));
        if let Some(icon) = &project.app.icon {
            meta.set_icon(icon)}
        meta.compile()?;
    }

    // Export a const configured project to be loaded at runtime
    envy::rustc_export("PYAKET_PROJECT", project.json());
    logging::note!("Project: {}", project.json());

    Ok(())
}

fn main() {
    LazyLock::force(&START_TIME);
    envy::set("BUILD", "1");
    logging::info!("Building pyaket project");
    build().unwrap();
}
