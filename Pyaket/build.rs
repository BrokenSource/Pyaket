#[path="Rust/common.rs"]
mod common;
use common::*;

/* -------------------------------------------------------------------------- */

mod manage {
    use super::*;

    // Todo: Find a way to match against uv
    pub fn python(_project: &Project) -> Result<()> {
        Ok(())
    }

    pub fn astral(project: &Project) -> Result<()> {
        network::must_exist(&project.uv_download_url())?;

        if project.uv_bundle {
            ArchiveAssets::download(
                &project.uv_archive_name(),
                &project.uv_download_url(),
            )?;
        }

        Ok(())
    }

    pub fn wheels(project: &Project) -> Result<()> {

        // Don't trust the user on ';'.join(wheels) formatting
        for wheel in project.wheels.split(";")
            .map(|x| x.trim()).filter(|x| !x.is_empty())
        {
            log::info!("Resolving wheel glob: {}", wheel);

            // Interpret as glob pattern to allow `/path/*.whl` sugar
            for file in glob::glob(wheel)?.map(|x| x.unwrap()) {
                log::info!("• {}", file.display());
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
        if Path::new(&project.reqtxt).exists() {
            project.reqtxt = fs::read_to_string(&project.reqtxt)?;
        }
        Ok(())
    }
}

/* -------------------------------------------------------------------------- */

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

    // Export a const configured project to be loaded at runtime
    Environment::rustc_export("PYAKET_PROJECT", project.json());
    Ok(())
}

fn main() {
    LazyLock::force(&START_TIME);
    Environment::set("BUILD", "1");
    build().unwrap();
}
