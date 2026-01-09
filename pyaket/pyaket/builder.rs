use crate::*;

use clap::Parser;
use clap::Subcommand;
use smart_default::SmartDefault;


#[derive(Subcommand)]
pub enum BuilderCommands {
    Version,
    Test,
}

#[derive(Parser, SmartDefault)]
pub struct BuilderCLI {

    #[default("default")]
    #[arg(short, long, default_value="default")]
    pub test: String,
}

pub fn main() {
    LazyLock::force(&START_TIME);

    let here = current_exe().unwrap();
    println!("I am exe: {:?}", here);

    BuilderCLI::parse();
}
