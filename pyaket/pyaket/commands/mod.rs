use crate::*;
pub mod manager;

use clap::Parser;
use clap::Subcommand;

pub trait PyaketCommand {
    fn run(&self, project: &PyaketProject) -> Result<()>;
}

/* -------------------------------------------------------------------------- */

#[derive(Parser)]
#[command(allow_hyphen_values=true)]
pub struct PyaketCLI {

    #[command(subcommand)]
    pub command: Option<Commands>,

    #[arg(trailing_var_arg=true)]
    pub default: Vec<String>,
}

impl PyaketCommand for PyaketCLI {
    fn run(&self, project: &PyaketProject) -> Result<()> {
        match &self.command {
            Some(cmd) => cmd.run(project),
            None => project.run(),
        }
    }
}

/* -------------------------------------------------------------------------- */
// Self command namespace

#[derive(Subcommand)]
pub enum Commands {

    #[command(name="self")]
    Selfy {
        #[command(subcommand)]
        command: Manager,
    },
}

impl PyaketCommand for Commands {
    fn run(&self, project: &PyaketProject) -> Result<()> {
        match self {
            Commands::Selfy{command} => command.run(project),
        }
    }
}

/* -------------------------------------------------------------------------- */
// Commands under 'pyaket self ...'

/// Special executable management commands from Pyaket
#[derive(Subcommand)]
pub enum Manager {
    Uv     (manager::UvCommand),
    Version(manager::VersionCommand),
}

impl PyaketCommand for Manager {
    fn run(&self, project: &PyaketProject) -> Result<()> {
        match self {
            Manager::Uv(cmd)      => cmd.run()?,
            Manager::Version(cmd) => cmd.run(project)?,
        }
        Ok(())
    }
}
