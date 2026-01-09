//! Pretty printing log macros that works both in build.rs and main.rs
pub use crate::error;
pub use crate::info;
pub use crate::note;
pub use crate::warn;

#[macro_export]
macro_rules! make_log {
    ($level:expr, $color:expr, $($tokens:tt)*) => {{
        let message = format!($($tokens)*);
        println!(
            "cargo::warning=\r\
            │\x1b[38;2;255;180;70mPyaket\x1b[0m├\
            ┤\x1b[{}m{}\x1b[0m│ ▸ {}",
            $color, $level, message
        );
        message
    }};
}
#[macro_export]
macro_rules! info  {($($tokens:tt)*) =>
    {$crate::make_log!("INFO ",  4, $($tokens)*)}}
#[macro_export]
macro_rules! warn  {($($tokens:tt)*) =>
    {$crate::make_log!("WARN ", 33, $($tokens)*)}}
#[macro_export]
macro_rules! note  {($($tokens:tt)*) =>
    {$crate::make_log!("NOTE ", 34, $($tokens)*)}}
#[macro_export]
macro_rules! error {($($tokens:tt)*) =>
    {$crate::make_log!("ERROR", 31, $($tokens)*)}}
