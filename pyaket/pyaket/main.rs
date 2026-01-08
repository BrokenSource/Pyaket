use pyaket::*;

use clap::Parser;

mod commands;
use commands::*;

fn main() -> Result<()> {
    LazyLock::force(&START_TIME);

    // Read the project configuration sent at the end of build.rs
    let project = PyaketProject::from_json(env!("PYAKET_PROJECT"));
    let runtime = PyaketCLI::try_parse()?.run(&project);

    // Hold the terminal open with any Rust or Python errors for convenience
    // - Opt-out with the same variable that enables the feature
    if let Err(_) = runtime {
        if project.keep_open && envy::ubool(PYAKET_KEEP_OPEN, true) {
            println!("\nPress enter to exit...");
            let _ = std::io::stdin().read_line(&mut String::new());
        }
    }

    Ok(())
}
