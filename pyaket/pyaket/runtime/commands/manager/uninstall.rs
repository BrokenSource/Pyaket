use crate::*;

use clap::Args;
use clap::ValueEnum;
use dialoguer::Confirm;
use dialoguer::theme::ColorfulTheme;

#[derive(Clone, ValueEnum, Debug)]
pub enum What {
    Interactive,
    Workspace,
    Version,
    Cache,
}

impl What {
    fn cache(&self, project: &PyaketProject) -> Result<()> {
        let mut uv = subprocess::uv()?;
        uv.arg("cache").arg("clear");
        subprocess::run(&mut uv)
    }
}

impl PyaketCommand for What {
    fn run(&self, project: &PyaketProject) -> Result<()> {
        match self {
            Self::Cache => self.cache(project)?,
        }
        Ok(())
    }
}


/// Selectively remove parts of the project installation
#[derive(Args)]
pub struct UninstallCommand {

    #[arg(short, long, value_enum)]
    #[arg(default_value_t=What::Interactive)]
    pub what: What,
}

impl UninstallCommand {

}

impl PyaketCommand for UninstallCommand {
    fn run(&self, project: &PyaketProject) -> Result<()> {
        // for item in &self.what {
        //     println!("Uninstalling {:?}", item);
        // }
        Ok(())
    }
}