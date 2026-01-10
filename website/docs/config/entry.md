---
icon: material/exit-to-app
---

## Interpreter

When no entry point is specified, a python interpreter is launched.

## Module

A module's name to be called as `python -m module (args)` at runtime.

=== ":simple-python: Python"
    ```python
    project.entry.module = "name"
    ```

=== ":fontawesome-solid-terminal: Command"
    ```bash
    pyaket run --module "name"
    ```

=== ":simple-rust: Rust"
    ```bash
    export PYAKET_ENTRY_MODULE="name"
    ```

!!! tip "The actual file called must exist `module/__main__.py`"

<hr>

## Command

A command to be executed as `command (args)` after installation.

=== ":simple-python: Python"
    ```python
    project.entry.command = "command"
    ```

=== ":fontawesome-solid-terminal: Command"
    ```bash
    pyaket run --command "command"
    ```

=== ":simple-rust: Rust"
    ```bash
    export PYAKET_ENTRY_COMMAND="command"
    ```

- The venv is activated and the bin directory is added to PATH, so this can be a script defined in your `pyproject.toml` • `[project.scripts]` section.

- It may be used if you have multiple entry points, like `depthflow {main,gradio}`, and want to hardcode pin one to be used, or set fixed arguments to some command.

!!! warning "**Discouraged**: Security implications, man in the middle attack, may use wrong executable"
