---
title: Entry Points
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

=== ":material-console: CLI"
    ```sh
    pyaket run --module "name" (...)
    ```

=== ":simple-toml: Toml"
    ```toml
    [entry]
    module = "name"
    ```

!!! tip "The actual file called must exist `module/__main__.py`"

<hr>

## Command

A command to be executed as `command (args)` after installation.

=== ":simple-python: Python"
    ```python
    project.entry.command = "command"
    ```

=== ":material-console: CLI"
    ```sh
    pyaket run --command "command" (...)
    ```

=== ":simple-toml: Toml"
    ```toml
    [entry]
    command = "command"
    ```

- The venv is activated and the bin directory is added to PATH, so this can be a script defined in your `pyproject.toml` • `[project.scripts]` section.

- It may be used if you have multiple entry points, like `depthflow {main,gradio}`, and want to hardcode pin one to be used, or set fixed arguments to some command.

!!! warning "**Discouraged**: Security implications, man in the middle attack, may use wrong executable"
