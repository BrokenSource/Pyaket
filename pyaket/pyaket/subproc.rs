use crate::*;

pub static PYAKET_UV: &str = "PYAKET_UV";

pub fn run(command: &mut Command) -> Result<()> {
    logging::info!("Call ({:?})", command);
    command.spawn()?.wait()?;
    Ok(())
}

pub fn uv() -> Result<Command> {
    if cfg!(feature="uv") {
        let mut command = Command::new(current_exe()?);
        command.env(PYAKET_UV, "1");
        Ok(command)
    } else {
        Ok(Command::new("uv"))
    }
}
