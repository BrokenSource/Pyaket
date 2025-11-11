use pyaket::*;

fn main() {
    LazyLock::force(&START_TIME);

    // Read the project configurion sent at the end of build.rs
    let project = PyaketProject::from_json(env!("PYAKET_PROJECT"));

    // Self management command
    if let Some("self") = std::env::args().nth(1).as_deref() {
        let args: Vec<String> = std::env::args().skip(1).collect();

        match Manager::try_parse_from(args) {
            Ok(manager) => manager.run(&project).unwrap(),
            Err(e) => eprintln!("Error: {}", e),
        }
        return;
    }

    // Actually execute the project
    match project.run() {
        Err(e) => eprintln!("\nError: {}", e),
        Ok(_) => {},
    }

    // Hold the terminal open with any Rust or Python errors for convenience
    // - Opt-out with the same variable that enables the feature
    if project.app.keep_open && envy::ubool(PYAKET_KEEP_OPEN, true) {
        print!("\nPress enter to exit...");
        let _ = std::io::stdin().read_line(&mut String::new());
    }
}
