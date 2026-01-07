use crate::*;
pub mod version;
pub mod uv;

use clap::Parser;
use clap::Subcommand;

pub trait PyaketCommand {
    fn run(&self, project: &PyaketProject) -> Result<()>;
}

/* -------------------------------------------------------------------------- */
// Main command parser, where the lack of a command
// implies launching the python project itself.

#[derive(Parser)]
#[command(allow_hyphen_values=true)]
#[command(disable_help_flag=true)]
pub struct PyaketCLI {

    #[command(subcommand)]
    pub command: Option<Commands>,

    #[arg(trailing_var_arg=true)]
    pub default: Vec<String>,
}

impl PyaketCLI {
    pub fn run(self, project: &PyaketProject) -> Result<()> {
        match self.command {
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

#[derive(Subcommand)]
#[command(
    // about="Special management commands",
    long_about=env!("CARGO_PKG_DESCRIPTION"),
)]
pub enum Manager {
    Version(version::VersionCommand),
    Uv(uv::UvCommand),
}

impl PyaketCommand for Manager {
    fn run(&self, project: &PyaketProject) -> Result<()> {
        match self {
            Manager::Version(cmd) => cmd.run(project)?,
            Manager::Uv(cmd) => cmd.run(),
        }
        Ok(())
    }
}
