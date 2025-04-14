mod Common;
use Common::*;

fn run(project: &Project) -> Result<()> {
    project.ensure_uv()?;

    // Send the executable path to Python, also flags a Pyaket app
    let executable = env::current_exe()?.canonicalize()?;
    Environment::set("PYAKET", executable.display());

    // Load environment variables where the executable is
    for file in glob::glob("*.env").unwrap().map(|x| x.unwrap()) {
        dotenvy::from_path(file)?;
    }

    Environment::set("UV_PYTHON_INSTALL_DIR", project.python_install_dir().display());
    Environment::set("VIRTUAL_ENV",      project.installation_dir().display());
    Environment::set("UV_CACHE_DIR",     project.uv_cache_dir().display());
    Environment::set("UV_SYSTEM_PYTHON", false);
    Environment::set("UV_NO_CONFIG",     true);

    if match read(project.uuid_tracker_file()) {
        Ok(bytes) => {bytes != project.uuid.as_bytes()},
        Err(_) => true,
    } || project.rolling {

        /* Create the virtual environment */ {
            let mut setup = project.uv();

            setup.arg("venv")
                .arg(project.installation_dir())
                .arg("--python").arg(&project.python_version)
                .arg("--seed").arg("--quiet");
            if project.rolling {setup
                .arg("--allow-existing");}
            subprocess::run(&mut setup)?;
        }

        // Install PyTorch first
        if !project.torch_version.is_empty() {
            Environment::setdefault("UV_TORCH_BACKEND", &project.torch_backend);
            project.uv()
                .arg("pip").arg("install")
                .arg(format!("torch=={}", project.torch_version))
                .arg("--preview")
                .spawn()?;
        }

        // Gets cleaned up when out of scope
        let container = TempDir::with_prefix("pyaket-").unwrap();

        let mut command = project.uv();
        command.arg("pip").arg("install");
        command.arg("--upgrade");

        // Add at least pip so the command fails ok when empty
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
        command.args(project.pypi.split(":")
            .map(|x| x.trim()).filter(|x| !x.is_empty()));

        // Add the requirements.txt file to be installed
        if !project.reqtxt.is_empty() {
            let file = container.child("requirements.txt");
            write(&file, &project.reqtxt)?;
            command.arg("-r").arg(&file);
        }

        subprocess::run(&mut command)?;
    }

    // Flag this was a successful install
    write(project.uuid_tracker_file(), &project.uuid)?;

    /* ---------------------------------------- */
    // Entry points

    let mut main = project.uv();
    main.arg("run");
    main.arg("--no-project");
    main.arg("--active");

    if !project.entry_module.is_empty() {
        main.arg("python")
            .arg("-m").arg(&project.entry_module);

    } else if !project.entry_script.is_empty() {
        main.arg("python")
            .arg(&project.entry_script);

    } else if !project.entry_code.is_empty() {
        main.arg("python")
            .arg("-c").arg(&project.entry_code);

    } else if !project.entry_command.is_empty() {
        let args = shlex::split(&project.entry_command)
            .expect("Failed to parse entry command");
        main = Command::new(&args[0]);
        main.args(&args[..]);

    // Effectively a Python installer without entry points
    } else {
        main.arg("python");
    }

    // Passthrough incoming arguments
    for arg in env::args().skip(1) {
        main.arg(arg);
    }

    // Execute the main program
    main.spawn()?.wait()?;
    Ok(())
}

fn main() {
    Lazy::force(&START_TIME);
    Environment::unset("BUILD");

    // Read the project configurion sent at the end of build.rs
    let project: Project = serde_json::from_str(env!("PYAKET_PROJECT")).unwrap();
    let runtime = run(&project);

    if runtime.is_err() {
        println!("\nError: {}", runtime.unwrap_err());
    }

    // Hold the terminal open with any Rust or Python errors for convenience
    // - Opt-out with the same variable that enables the feature
    if project.keep_open && Environment::ubool(PYAKET_KEEP_OPEN, true) {
        println!("\nPress enter to exit...");
        let _ = std::io::stdin().read_line(&mut String::new());
    }
}
