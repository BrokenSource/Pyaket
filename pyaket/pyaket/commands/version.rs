use crate::*;

use clap::Args;
use clap::ValueEnum;

#[derive(Default, Clone, ValueEnum)]
enum Query {
    #[default]
    Project,
    Pyaket,
    Python,
    Torch,
}

#[derive(Args)]
pub struct VersionCommand {

    #[arg(short, long, value_enum, default_value_t=Query::Project)]
    query: Query,
}

impl PyaketCommand for VersionCommand {
    fn run(&self, project: &PyaketProject) -> Result<()> {
        match self.query {
            Query::Pyaket =>
                println!("{}", env!("CARGO_PKG_VERSION")),

            Query::Project =>
                println!("{}", project.app.version),

            Query::Python =>
                println!("{}", project.python.version),

            Query::Torch =>
                match &project.torch.version {
                    Some(v) => println!("{}+{}", v, project.torch.backend),
                    None => println!("None"),
                },
        }
        Ok(())
    }
}

