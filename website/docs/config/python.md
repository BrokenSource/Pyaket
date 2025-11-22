---
icon: material/language-python
---


:material-arrow-right: This section is about the Python interpreter to be used at runtime.

## Version

The version of Python to be used at runtime, from [astral-sh/python-build-standalone](https://github.com/astral-sh/python-build-standalone/).

=== ":simple-python: Python"

    ```python
    project.python.version = "3.13"
    ```

=== ":simple-rust: Rust"

    ```bash
    export PYAKET_PYTHON_VERSION="3.13"
    ```

- **Note**: Specific versions support, such as `3.10.17`, depends on the [uv version](https://github.com/BrokenSource/Pyaket/blob/main/pyaket/Cargo.toml) in use, as the URLs are hard-coded in their binary. For example, `3.13.3` was added in [v0.6.14](https://github.com/astral-sh/uv/releases/tag/0.6.14).

- Please chose carefully to ensure all your wheels and dependencies are compatible with the target version. Users may not have compilers, headers, git for sdists.


## Bundle

!!! warning "Not implemented [#2](https://github.com/BrokenSource/Pyaket/issues/2)"

Whether to embed the python distribution in the executable, instead of a runtime download.

=== ":simple-python: Python"

    ```python
    project.python.bundle = False
    ```

=== ":simple-rust: Rust"

    ```bash
    export PYAKET_PYTHON_BUNDLE="0"
    ```
