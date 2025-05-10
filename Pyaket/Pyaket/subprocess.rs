use crate::*;

pub fn run(command: &mut Command) -> Result<()> {
    logging::info!("Call ({:?})", command);
    command.spawn()?.wait()?;
    Ok(())
}
