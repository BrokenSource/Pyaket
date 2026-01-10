use std::fmt::Display;

/* -------------------------------------------------------------------------- */
// String

/// Get a string from an environment variable
pub fn get(name: &str) -> Option<String> {
    std::env::var(name).ok()
}

/// Get a string from an environment variable with a default
pub fn uget(name: &str, default: &str) -> String {
    self::get(name).unwrap_or_else(|| default.to_string())
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
        self::set(name, value);
    }
}

/* -------------------------------------------------------------------------- */
// Boolean

/// Parse a bool from an environment variable
pub fn bool(name: &str) -> Option<bool> {
    match std::env::var(name).ok() {
        Some(value) => match value.to_lowercase().as_str() {
            "false" | "0" | "no"  | "off" => Some(false),
            "true"  | "1" | "yes" | "on"  => Some(true),
            _ => None,
        },
        None => None,
    }
}

/// Parse a bool from an environment variable with a default
pub fn ubool(name: &str, default: bool) -> bool {
    self::bool(name).unwrap_or(default)
}

/* -------------------------------------------------------------------------- */
// Exporting and printing

/// Print an environment variable
pub fn printenv(name: &str) {
    println!("{}={}", name, self::uget(name, "#Unset#"))
}
