use crate::*;

pub struct Environment;

// String
impl Environment {

    /// Get a string from the environment, optional default
    pub fn get(name: &str, default: Option<&str>) -> Option<String> {
        std::env::var(name).ok().or(default.map(|x| x.to_string()))
    }

    /// Set an environment variable to a value
    pub fn set(name: &str, value: impl Display) {
        unsafe {std::env::set_var(name, format!("{}", value))}
    }

    /// Remove a variable from the environment
    pub fn unset(name: &str) {
        unsafe {std::env::remove_var(name)}
    }

    /// Calls `set()` if the variable does not exist
    pub fn setdefault(name: &str, value: impl Display) {
        if std::env::var(name).is_err() {
            Environment::set(name, value);
        }
    }

    /// Get a string from the environment, required default
    pub fn uget(name: &str, default: &str) -> String {
        Environment::get(name, Some(default)).unwrap()
    }
}

// Boolean
impl Environment {

    /// Parse a bool from an environment variable, optional default
    pub fn bool(name: &str, default: Option<bool>) -> Option<bool> {
        match std::env::var(name).ok() {
            Some(value) => match value.to_lowercase().as_str() {
                "false" | "0" | "no"  | "off" => Some(false),
                "true"  | "1" | "yes" | "on"  => Some(true),
                _ => None,
            },
            None => default,
        }
    }

    /// Parse a bool from an environment variable, required default
    pub fn ubool(name: &str, default: bool) -> bool {
        Environment::bool(name, Some(default)).unwrap()
    }
}

// Exporting and printing
impl Environment {

    /// Print an environment variable
    pub fn print(name: &str) {
        println!("{}={}", name, Environment::uget(name, "#Unset#"))
    }

    /// Pass a compile time environment variable to the binary
    /// - Warn: Must be acessed via env!(literal) at runtime
    pub fn rustc_export(name: &str, value: impl Display) {
        println!("cargo:rustc-env={}={}", name, value);
    }

    /// Path where Cargo.toml is located
    pub fn cargo_toml() -> PathBuf {
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
    }
}
