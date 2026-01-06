use crate::*;
use clap::Parser;

mod version;


#[derive(Parser)]
#[command(author, about, long_about=None)]
pub enum Commands {
    Version(version::VersionCommand),
}

impl Commands {
    pub fn as_dyn(&self) -> &dyn PyaketCommand {
        match self {
            Commands::Version(x) => x,
        }
    }
}

pub trait PyaketCommand {
    fn run(&self, project: &PyaketProject) -> Result<(), anyhow::Error>;
}

impl Commands {
    pub fn run(self, project: &PyaketProject) -> Result<()> {
        self.as_dyn().run(project)
    }
}