use pyaket::*;

use clap::Parser;

mod commands;
use commands::*;

fn main() -> Result<()> {

    // Short circuit on uv mode, bypass cli
    #[cfg(feature="uv")]
    if envy::flag(subproc::PYAKET_UV) {
        unsafe {
            match ::uv::main(std::env::args()) {
                ExitCode::SUCCESS => std::process::exit(0),
                ExitCode::FAILURE => std::process::exit(1),
                _ => std::process::exit(1),
            }
        }
    }

    LazyLock::force(&START_TIME);

    // Read the project configuration sent from build.rs
    let project = PyaketProject::from_json(env!("PYAKET_PROJECT"));
    let runtime = PyaketCLI::try_parse()?.run(&project);

    // Hold the terminal open with any Rust or Python errors for convenience
    // - Opt-out with the same variable that enables the feature
    if let Err(_) = runtime {
        if project.keep_open && envy::ubool("PYAKET_HOLD", true) {
            println!("\nPress enter to exit...");
            let _ = std::io::stdin().read_line(&mut String::new());
        }
    }

    Ok(())
}
