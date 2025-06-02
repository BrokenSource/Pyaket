#[path="pyaket/lib.rs"]
mod lib;
use lib::*;

/* -------------------------------------------------------------------------- */

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
        Network::must_exist(&project.uv_download_url())?;

        if project.uv.bundle {
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
            WheelAssets::write(wheel, &read(&wheel).unwrap())?;
            logging::info!("• {}", wheel);
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
    logging::note!("Project: {}", project.json());
    Ok(())
}

fn main() {
    LazyLock::force(&START_TIME);
    Environment::set("BUILD", "1");
    build().unwrap();
}
