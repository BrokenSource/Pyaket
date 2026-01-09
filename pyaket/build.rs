#![allow(dead_code)]
#![allow(unused_imports)]

use anyhow::Result;
use anyhow::bail;

#[path="pyaket/logging.rs"]
mod logging;

#[path="pyaket/assets.rs"]
mod assets;

#[path="pyaket/envy.rs"]
mod envy;


fn main() -> Result<()> {

    // Workaround to always trigger a rebuild
    println!("cargo:rerun-if-changed=NULL");

    // Workaround for conditional compilation build.rs shared lib:
    // - Code marked as `#[cfg(not(runtime))]` is build-only
    // - Code marked as `#[cfg(runtime)]` is runtime-only
    #[cfg(not(rust_analyzer))]
    println!("cargo:rustc-cfg=runtime");

    logging::info!("Building Pyaket executable");

    /* ------------------------------ */

    // Export a const configured project to be loaded at runtime
    if let Some(project) = envy::get("PYAKET_PROJECT") {
        envy::rustc_export("PYAKET_PROJECT", &project);
    } else {
        logging::warn!("No project configuration set (expected in maturin or packer)");
    }

    // Executable resources (icon, metadata, etc)
    if envy::uget("TARGET", "").contains("windows") {
        logging::info!("Making Windows executable resources");
        let mut meta = winresource::WindowsResource::new();

        // From packer export
        for name in &[
            "ProductName", "CompanyName", "FileVersion",
            "OriginalFilename", "FileDescription",
            "LegalCopyright",
        ] {
            meta.set(name, &envy::uget(name, "Unknown"));
        }

        // Warn: Must be .ico 256x256 format
        if let Some(icon) = envy::get("PYAKET_ICON") {
            meta.set_icon(&icon);
        }

        meta.compile()?;
    }

    Ok(())
}