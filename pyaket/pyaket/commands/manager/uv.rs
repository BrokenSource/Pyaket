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
    pub fn run(&self) -> Result<()> {
        let mut command = subproc::uv()?;
        command.args(&self.args);
        subproc::run(&mut command)?;
        Ok(())
    }
}
