---
icon: material/package-variant-closed
---

## Wheels

Glob patterns of wheels and sdists to bundle and install at runtime.

=== ":simple-python: Python"
    ```python
    project.dependencies.wheels.append("dist/*.whl")
    project.dependencies.wheels.append("/path/to/foo.whl")
    project.dependencies.wheels.append("/path/to/sdists/*.tar.gz")
    ```

=== ":simple-toml: Toml"
    ```toml
    [dependencies]
    wheels = [
        "dist/*.whl",
        "/path/to/foo.whl",
        "/path/to/sdists/*.tar.gz",
    ]
    ```

This is the recommended way to specify dependencies, although third party packages may still be installed at runtime from the dependency chain.

If we get them all, a standalone install is achieved, with zero network calls to get missing packages at cost of large binary size.

- Beware that sdists may need compilation at runtime in the user's machine, prefer wheels.
- If you have a monorepo with uv, it's as simple as `uv build --all` and include `dist/*`.
- This option allows to bundle private wheels without pushing to a registry.

<hr>

## Packages

List of PyPI packages to be installed at runtime.

!!! tip "For iterative development, make and use local [wheels](#wheels) from your project first!"

=== ":simple-python: Python"
    ```python
    # Solve for latest compatible version
    project.dependencies.pypi.append("numpy")

    # Specific stable version of a package
    project.dependencies.pypi.append("altair==6.0.0")
    project.dependencies.pypi.append("pillow>=9.0.0,<10.0.0")

    # Or even git dependencies, targetting specific branches or tags
    project.dependencies.pypi.append("git+https://github.com/BrokenSource/TurboPipe")
    project.dependencies.pypi.append("git+...@main")
    project.dependencies.pypi.append("git+...@v1.2.4")
    ```

=== ":simple-toml: Toml"
    ```toml
    [dependencies]
    pypi = [
        "numpy",
        "altair==6.0.0",
        "pillow>=9.0.0,<10.0.0",
        "git+...@main",
        "git+...@v1.2.4",
    ]
    ```

<hr>

## requirements.txt {#requirements-txt}

A local `requirements.txt` file to be installed at runtime.

=== ":simple-python: Python"
    ```python
    project.dependencies.reqtxt = Path("/path/to/requirements.txt")
    ```

=== ":simple-toml: Toml"
    ```toml
    [dependencies]
    reqtxt = "/path/to/requirements.txt"
    ```

This option mostly exists for legacy reasons. You really should move to a `pyproject.toml` as it allows easier build backends to create portable wheels for your project that includes your code. The only use I can think of is to run a project-less script with a requirements file alongside it.

<hr>

## Rolling

Always reinstall the project's dependencies when running the executable.

=== ":simple-python: Python"
    ```python
    project.dependencies.rolling = True
    ```

=== ":simple-toml: Toml"
    ```toml
    [dependencies]
    rolling = true
    ```

This option is best combined with a `git+` dependency or `package` without a `==version` specifier, to create a one-time binary that self-updates. This is obviously discouraged for any production use, unless very controlled, or in ephemeral runtimes for a couple of reasons:

- **Security**: Any malicious update (on the developer or third party side) will be downloaded and executed on the user's/your machine, _blindly_, without a way to recall.
- **Performance**: The executable will be slower to start and require mandatory network calls at every run, which could give a temporary IP ban if abusing the registry.
- **Stability**: The dependencies may change and break the project.

A valid, but unconventional, use case is to pin all your dependencies to a specific version and target your latest stable PyPI releases (or git main branch) for clients after heavy testing.
