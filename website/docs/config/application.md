---
icon: material/application-braces-outline
---

General metadata about the application being built.

## Name

The name of the application being built.

=== ":simple-python: Python"
    ```python
    project.app.name = "Pyaket"
    ```

=== ":simple-rust: Rust"
    ```bash
    export PYAKET_APP_NAME="Pyaket"
    ```

<hr>

## Author

The author's name, group, organization of the application being built.

=== ":simple-python: Python"
    ```python
    project.app.author = "BrokenSource"
    ```

=== ":simple-rust: Rust"
    ```bash
    export PYAKET_APP_AUTHOR="BrokenSource"
    ```

<hr>

## Vendor

Always equal to [Author](#author) if set, otherwise [Name](#name).

This value primarily determines the [Workspace Root](./directories.md#workspace) location when dynamic.

!!! tip "Using an empty [Author](#author) is a way to isolate each project virtual environment."
    - While not recommended due spamming the user data dir, it works for single banner-less projects. For that, set the python field to `#!python None` or unset it entirely.

<hr>

## Version

The version of the application being built.

Should follow the same number of the project to be released alonside a registry. Not necessarily a semantic version, can be a codename, branch name, _"latest"_, etc.

=== ":simple-python: Python"
    ```python
    project.app.version = "0.0.0"
    ```

=== ":simple-rust: Rust"
    ```bash
    export PYAKET_APP_VERSION="0.0.0"
    ```

The value is appended to the [Versions Directory](./directories.md#versions) to build the virtual environment path.

!!! tip "Projects with the same version and subdirectories shares the same venv!"
    - First-class monorepo support with a global versioning scheme.

<hr>

## About

A description of the application, exclusively for metadata or banner purposes.

=== ":simple-python: Python"
    ```python
    project.app.about = "No description provided"
    ```

=== ":simple-rust: Rust"
    ```bash
    export PYAKET_APP_ABOUT="No description provided"
    ```

<hr>

## Icon

!!! warning "Stub: Not implemented"

An image path to use as the application icon.

=== ":simple-python: Python"
    ```python
    # Can be Path, str, Image, numpy.
    project.app.icon = Path
    ```

=== ":simple-rust: Rust"
    ```bash
    # Must be a Path to an icon file
    export PYAKET_APP_ICON="/path/to/icon"
    ```

<br>

:material-arrow-right: **Platform** support:

<!-- Todo: Link against Self CLI documentation -->
=== ":simple-linux: Linux"
    !!! success "Supported via [Desktop Entries](https://wiki.archlinux.org/title/Desktop_entries) XDG Specification."
        - Run `#!ps1 ./project self desktop` to generate one at `#!ps1 ~/.local/share/applications/$project.{desktop,png}`
    !!! warning "Wayland/X11 does not support icons outside .desktop files"
        No matter what you do, launching outside a desktop entry won't show an icon.

=== ":material-microsoft: Windows"
    !!! success "Natively supported and implemented via [crates.io/winresource](https://crates.io/crates/winresource)"
        - Icon should appear in File Explorer and Task bar.

=== ":simple-apple: MacOS"
    !!! bug "Not implemented, but [seems to be possible](https://stackoverflow.com/a/65393488)."
        - Consider [supporting](https://github.com/sponsors/Tremeschin) my work or sending Apple hardware for development!
