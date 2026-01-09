use crate::*;

use clap::Args;

/// Run astral-sh/uv commands within the project environment
#[derive(Args)]
#[command(allow_hyphen_values=true)]
pub struct UvCommand {

    #[arg(trailing_var_arg=true)]
    pub args: Vec<String>,
}

impl UvCommand {

    #[cfg(feature="uv")]
    pub fn run(&self) {
        unsafe {
            match ::uv::main(&self.args) {
                ExitCode::SUCCESS => std::process::exit(0),
                ExitCode::FAILURE => std::process::exit(1),
                _ => std::process::exit(1),
            }
        }
    }

    #[cfg(not(feature="uv"))]
    pub fn run(&self) {
        let mut cmd = Command::new("uv");
        cmd.args(&self.args);

        let status = cmd.status().expect("Failed to execute system 'uv' command");
        std::process::exit(status.code().unwrap_or(1));
    }
}

