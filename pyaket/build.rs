#![allow(dead_code)]
#![allow(unused_imports)]

use anyhow::Result;
use anyhow::bail;

#[path="pyaket/logging.rs"]
mod logging;

#[path="pyaket/envy.rs"]
mod envy;


pub static PYAKET_PACKER: &str = "PYAKET_PACKER";

fn main() -> Result<()> {

    // Workaround to always trigger a rebuild
    println!("cargo:rerun-if-changed=NULL");

    // Workaround for conditional compilation build.rs shared lib:
    // - Code marked as `#[cfg(not(runtime))]` is build-only
    // - Code marked as `#[cfg(runtime)]` is runtime-only
    #[cfg(not(rust_analyzer))]
    println!("cargo:rustc-cfg=runtime");

    // Skip build script if not in packaging mode
    if !envy::ubool(PYAKET_PACKER, false) {
        logging::info!("Skipping build script per non-packaging mode");
        return Ok(());
    }

    logging::info!("Building Pyaket executable");

    /* ------------------------------ */

    // Fixme: Options without pyaket crate
    // // Executable resources (icon, metadata, etc)
    // if project.triple.contains("windows") {
    //     logging::info!("Making Windows executable resources");
    //     let mut meta = winresource::WindowsResource::new();
    //     meta.set("ProductName",      &project.app.name);
    //     meta.set("CompanyName",      &project.app.author);
    //     meta.set("FileVersion",      &project.app.version);
    //     meta.set("FileDescription",  &project.app.about);
    //     meta.set("OriginalFilename", &envy::uget("OriginalFilename", "pyaket.exe"));
    //     meta.set("LegalCopyright",   &envy::uget("LegalCopyright", "Unknown"));
    //     if let Some(icon) = &project.app.icon {
    //         meta.set_icon(icon);
    //     }
    //     meta.compile()?;
    // } else {
    //     // Linux: .desktop points to a file
    //     if let Some(icon) = &project.app.icon {
    //         ArchiveAssets::write(ASSET_ICON, &read(icon)?)?;
    //     }
    // }

    // Export a const configured project to be loaded at runtime
    if let Some(project) = envy::get("PYAKET_PROJECT") {
        envy::rustc_export("PYAKET_PROJECT", &project);
        logging::info!("Configuration: {}", &project);
    } else {
        bail!(logging::error!("No project configuration set"));
    }

    Ok(())
}