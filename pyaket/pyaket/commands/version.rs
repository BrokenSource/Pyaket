use crate::*;

#[derive(Default, Clone, ValueEnum)]
enum VersionQuery {
    #[default]
    Project,
    Pyaket,
    Python,
}

#[derive(Args)]
pub struct VersionCommand {

    #[arg(short, long, value_enum, default_value_t=VersionQuery::Project)]
    query: VersionQuery,
}

impl PyaketCommand for VersionCommand {
    fn run(&self, project: &PyaketProject) -> Result<()> {
        match self.query {
            VersionQuery::Project =>
                println!("{}", project.app.version),

            VersionQuery::Pyaket =>
                println!("{}", env!("CARGO_PKG_VERSION")),

            VersionQuery::Python =>
                println!("{}", project.python.version),
        }
        Ok(())
    }
}

