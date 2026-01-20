use std::env::var;

fn main() {

    // Workaround to always trigger a rebuild
    println!("cargo:rerun-if-changed=NULL");

    // Passthrough project configuration (empty for rust-analyzer)
    let project = var("PYAKET_PROJECT").unwrap_or_default();
    println!("cargo:rustc-env={}={}", "PYAKET_PROJECT", project);

    // Executable resources (icon, metadata, etc)
    if var("TARGET").unwrap().contains("windows") {
        let mut meta = winresource::WindowsResource::new();

        // Passthrough
        for name in &[
            "ProductName", "CompanyName", "FileVersion",
            "OriginalFilename", "FileDescription",
            "LegalCopyright",
        ] {
            let value = var(name).unwrap_or("Unknown".to_string());
            meta.set(name, &value);
        }

        // Warn: Must be .ico 256x256 format
        if let Ok(icon) = var("PYAKET_ICON") {
            meta.set_icon(&icon);
        }

        meta.compile().unwrap();
    }
}
