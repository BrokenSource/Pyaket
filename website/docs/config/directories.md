---
icon: material/folder-outline
---

## Workspace

Path where all application data is stored.

This is a special variable that can be overriden at runtime and is _dynamic_ if unset

| System                       | Path |
| ---------------------------- | ---- |
| :simple-linux:       Linux   | <kbd>~/.local/share/Vendor</kbd> |
| :material-microsoft: Windows | <kbd>C:\\Users\\User\\AppData\\Local\\Vendor</kbd> |
| :simple-apple:       MacOS   | <kbd>~/Library/Application Support/Vendor</kbd> |
| :material-cube:      Custom  | <kbd>$WORKSPACE</kbd> |

!!! tip "All .env files where the project is run are loaded"
    ```env title="<small>custom.env</small>"
    WORKSPACE=/custom/workspace/path
    ```

<hr>

## Common

Subdirectory of the [Workspace](#workspace) to use for all Pyaket files.

=== ":simple-python: Python"

    ```python
    project.directories.common = "Pyaket"
    ```

=== "":simple-rust: Rust"

    ```bash
    export PYAKET_COMMON_DIR="Pyaket"
    ```

<hr>

## Versions

Subdirectory of the [Workspace](#workspace) to install virtual environments.

=== ":simple-python: Python"

    ```python
    project.directories.versions = "Versions"
    ```

=== "":simple-rust: Rust"

    ```bash
    export PYAKET_VERSIONS_DIR="Versions"
    ```

| System                       | Path |
| ---------------------------- | ---- |
| :simple-linux:       Linux   | <kbd>~/.local/share/Vendor/Versions</kbd> |
| :material-microsoft: Windows | <kbd>C:\\Users\\User\\AppData\\Local\\Vendor\\Versions</kbd> |
| :simple-apple:       MacOS   | <kbd>~/Library/Application Support/Vendor/Versions</kbd> |
| :material-cube:      Custom  | <kbd>$WORKSPACE/Versions</kbd> |
