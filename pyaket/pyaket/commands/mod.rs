use crate::*;
pub mod version;

#[derive(Parser)]
#[command(author, about, long_about=None)]
pub enum Manager {
    Version(version::VersionCommand),
}

impl Manager {
    pub fn as_dyn(&self) -> &dyn PyaketCommand {
        match self {
            Manager::Version(x) => x,
        }
    }
}

pub trait PyaketCommand {
    fn run(&self, project: &PyaketProject) -> Result<(), anyhow::Error>;
}

impl Manager {
    pub fn run(self, project: &PyaketProject) -> Result<()> {
        self.as_dyn().run(&project)
    }
}