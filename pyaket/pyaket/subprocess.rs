use crate::*;

pub fn run(command: &mut Command) -> Result<()> {
    logging::info!("Call ({:?})", command);
    command.spawn()?.wait()?;
    Ok(())
}

pub fn uv() -> Result<Command> {
    let mut cmd = Command::new(current_exe()?);
    cmd.arg("self").arg("uv");
    Ok(cmd)
}

pub fn rustup() -> Result<Command> {
    let cmd = Command::new("rustup");
    Ok(cmd)
}
