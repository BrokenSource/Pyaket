---
icon: material/language-python
---

!!! warning "Updated [v0.10](../about/changelog.md) releases are yet to be published!"

## Dependency

Simply add or install the [`pyaket` package](https://pypi.org/project/pyaket/) in your project _as a development dependency_[^development]:

[^development]: Users should not need `pyaket` installed to run your application, only during development and packaging.

=== ":simple-astral: uv"
    ```sh linenums="1"
    uv add pyaket --dev
    ```
=== ":simple-python: pip"
    ```sh linenums="1"
    pip install pyaket
    ```
=== ":simple-poetry: poetry"
    ```sh linenums="1"
    poetry add pyaket --dev
    ```
=== ":simple-pdm: pdm"
    ```sh linenums="1"
    pdm add pyaket --dev
    ```

!!! tip "Suggestions"
    - Pin the latest version as in `pyaket==x.y.z` for extra stability
    - Install with `pyaket[all]` groups for [cross-compilation](../docs/rust/crosscompiling.md)


## Managed

Following the concepts of [uv](https://docs.astral.sh/uv/) • [tools](https://docs.astral.sh/uv/guides/tools/), you can use pyaket independently from a project with:

```sh title="🔴🟡🟢 Command" linenums="1"
# Choose any version you want
uv tool install pyaket@latest

# Upgrade anytime
uv tool upgrade pyaket
```

And then run it with:

```sh title="🔴🟡🟢 Command" linenums="1"
uv tool run pyaket (...)
```
