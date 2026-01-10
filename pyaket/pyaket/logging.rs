//! Pretty printing log macros that works both in build.rs and main.rs
pub use crate::error;
pub use crate::info;
pub use crate::note;
pub use crate::warn;

use std::sync::LazyLock;
use std::time::Instant;

/// Time at which the program started
pub static START_TIME: LazyLock<Instant> = LazyLock::new(Instant::now);

#[macro_export]
macro_rules! make_log {
    ($level:expr, $color:expr, $($tokens:tt)*) => {{
        use crate::logging::START_TIME;
        let elapsed: f32 = (START_TIME.elapsed().as_millis() as f32)/1000.0;
        let message = format!($($tokens)*);
        println!(
            "cargo::warning=\r\
            │\x1b[38;2;255;180;70m{}\x1b[0m├\
            ┤\x1b[{}m{}\x1b[0m│ ▸ {}",
            format!("{}'{:06.3}", (elapsed/60.0).floor(), (elapsed%60.0)),
            $color, $level, message
        );
        message
    }};
}
#[macro_export]
macro_rules! info  {($($tokens:tt)*) =>
    {$crate::make_log!("INFO ", 97, $($tokens)*)}}
#[macro_export]
macro_rules! warn  {($($tokens:tt)*) =>
    {$crate::make_log!("WARN ", 33, $($tokens)*)}}
#[macro_export]
macro_rules! note  {($($tokens:tt)*) =>
    {$crate::make_log!("NOTE ", 34, $($tokens)*)}}
#[macro_export]
macro_rules! error {($($tokens:tt)*) =>
    {$crate::make_log!("ERROR", 31, $($tokens)*)}}
