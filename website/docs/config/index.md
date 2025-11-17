# Documentation

!!! warning
    This section is outdated and needs a cleanup/rewrite:

    - Better visuals and wordings needed
    - Many variables were simplified


:material-arrow-right: 📦 Pyaket's configuration is done via environment variables read by rust at compile time, which are processed and passed through to the executable to load at runtime.

This page documents all :simple-rust: Rust side environment variables and extra information. You don't need the Python package to build a Pyaket executable if you're skilled with cargo, although most of these have python cognates and follows the same structure seen here, which is the main way to build your project.

!!! note "Some settings are exclusive to python"
    - The `--upx` flag can't currently be supported by the rust side yet, as cargo lacks post-build hooks. You can do it yourself though, e.g. find the binary at `target/*/pyaket` and run `upx` on it.
    - The `--standalone` flag is a syntatic sugar for other options; exporting all deps wheels is annoying in rust.
