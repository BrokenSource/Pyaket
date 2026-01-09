use crate::*;

use clap::Args;
use clap::ValueEnum;

#[derive(Clone, ValueEnum)]
pub enum Query {
    Project,
    Pyaket,
    Python,
    Torch,
    Uv,
}

/// Query the project, python, pyaket or torch versions
#[derive(Args)]
pub struct VersionCommand {

    #[arg(short, long, value_enum, default_value_t=Query::Project)]
    pub query: Query,
}

impl PyaketCommand for VersionCommand {
    fn run(&self, project: &PyaketProject) -> Result<()> {
        match self.query {
            Query::Pyaket =>
                println!("{}", env!("CARGO_PKG_VERSION")),

            Query::Project =>
                println!("{}", project.application.version),

            Query::Python =>
                println!("{}", project.python.version),

            Query::Torch =>
                match &project.torch.version {
                    Some(ver) => println!("{}+{}", ver, project.torch.backend),
                    None => println!("None"),
                },

            Query::Uv => {
                super::uv::UvCommand {
                    args: vec!("--version".to_string()),
                }.run();
            }
        }
        Ok(())
    }
}

