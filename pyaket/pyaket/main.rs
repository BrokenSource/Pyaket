use pyaket::*;

fn run(project: &Project) -> Result<()> {

    // Send the executable path to Python, also flags a Pyaket app
    let executable = std::env::current_exe()?.canonicalize()?;
    Environment::set("PYAKET", executable.display());

    // Load environment variables where the shell (executable) is
    for file in glob::glob("*.env").unwrap().map(|x| x.unwrap()) {
        dotenvy::from_path(file)?;
    }

    Environment::set("UV_PYTHON_INSTALL_DIR", project.python_install_dir().display());
    Environment::set("VIRTUAL_ENV",      project.installation_dir().display());
    Environment::set("UV_CACHE_DIR",     project.uv_cache_dir().display());
    Environment::set("UV_SYSTEM_PYTHON", false);
    Environment::set("UV_NO_CONFIG",     true);

    // Force disable the GIL on freethreaded python
    if project.python.version.contains('t') {
        Environment::set("UNSAFE_PYO3_BUILD_FREE_THREADED", 1);
        Environment::set("PYTHON_GIL", 0);
    }

    if match read(project.uuid_tracker_file()) {
        Ok(bytes) => {bytes != project.uuid.as_bytes()},
        Err(_)    => true,
    } || project.app.rolling {

        /* Create the virtual environment */ {
            let mut setup = project.uv()?;

            setup.arg("venv")
                .arg(project.installation_dir())
                .arg("--python").arg(&project.python.version)
                .arg("--seed").arg("--quiet");
            if project.app.rolling {setup
                .arg("--allow-existing");}
            subprocess::run(&mut setup)?;
        }

        // Install PyTorch first, as other dependencies might
        // install a platform's default backend
        if !project.torch.version.is_empty() {
            let mut torch = project.uv()?;

            torch.arg("pip").arg("install")
                .arg(format!("torch=={}", project.torch.version))
                .arg(format!("--torch-backend={}", project.torch.backend))
                .arg("--preview");

            subprocess::run(&mut torch)?;
        }

        // Gets cleaned up when out of scope
        let container = TempDir::with_prefix("pyaket-").unwrap();

        let mut command = project.uv()?;
        command.arg("pip").arg("install");
        command.arg("--upgrade");
        command.arg("pip");

        // Write temp wheel/sdist packages and mark to install
        for (name, bytes) in ["*.whl", "*.tar.gz"].into_iter()
            .flat_map(|x| WheelAssets::glob(x).unwrap())
        {
            let file = container.child(name);
            write(&file, bytes)?;
            command.arg(&file);
        }

        // Add PyPI packages to be installed
        if !project.app.pypi.is_empty() {
            command.args(project.app.pypi.split(";"));
            // command.args(&project.app.pypi);
        }

        // Add the requirements.txt file to be installed
        if !project.app.reqtxt.is_empty() {
            let file = container.child("requirements.txt");
            write(&file, &project.app.reqtxt)?;
            command.arg("-r").arg(&file);
        }

        subprocess::run(&mut command)?;
    }

    // Flag this was a successful install
    write(project.uuid_tracker_file(), &project.uuid)?;

    /* ---------------------------------------- */
    // Entry points

    let mut main = project.uv()?;
    main.arg("run");
    main.arg("--no-project");
    main.arg("--active");

    if !project.entry.module.is_empty() {
        main.arg("python")
            .arg("-m").arg(&project.entry.module);

    } else if !project.entry.script.is_empty() {
        main.arg("run")
            .arg(&project.entry.script);

    } else if !project.entry.code.is_empty() {
        main.arg("python")
            .arg("-c").arg(&project.entry.code);

    } else if !project.entry.command.is_empty() {
        let args = shlex::split(&project.entry.command)
            .expect("Failed to parse entry command");
        main = Command::new(&args[0]);
        main.args(&args[..]);

    // Effectively a Python installer without entry points
    } else {
        main.arg("python");
    }

    // Passthrough incoming arguments
    for arg in std::env::args().skip(1) {
        main.arg(arg);
    }

    // Execute the main program
    main.spawn()?.wait()?;
    Ok(())
}

fn main() {
    LazyLock::force(&START_TIME);
    Environment::unset("BUILD");

    // Read the project configurion sent at the end of build.rs
    let project: Project = Project::from_json(env!("PYAKET_PROJECT"));
    let runtime = run(&project);

    if runtime.is_err() {
        println!("\nError: {}", runtime.unwrap_err());
    }

    // Hold the terminal open with any Rust or Python errors for convenience
    // - Opt-out with the same variable that enables the feature
    if project.app.keep_open && Environment::ubool(PYAKET_KEEP_OPEN, true) {
        print!("\nPress enter to exit...");
        let _ = std::io::stdin().read_line(&mut String::new());
    }
}
