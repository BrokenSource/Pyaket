---
icon: material/package-variant-closed
---

## Dependencies {#dependencies}

:material-arrow-right: A continuation of the [application](#app) section for listing dependencies.

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>PYAKET_APP_WHEELS</kbd> {#app-wheels}
> 📦 <b>Type:</b> Paths • <b>Default:</b> None

Glob patterns separated by `;` (semi colon) of wheels and sdists to bundle and install at runtime.

```sh title="Example"
export PYAKET_APP_WHEELS="/path/to/wheel1.whl;/path/to/wheel2.whl"
export PYAKET_APP_WHEELS="/path/to/*.whl;/other/*.whl"
export PYAKET_APP_WHEELS="/path/to/sdists/*.tar.gz"
```

!!! warning "Paths must be absolute, as they are relative to `build.rs`"

This is the recommended way to specify dependencies, although third party packages may still be installed at runtime, comparing to [PyPI](#app-pypi). If we get them all, a standalone install is achieved, with zero network calls to get missing packages at cost of large binary size.

- Beware that sdists may need compilation at runtime in the user's machine, prefer wheels.
- If you have a monorepo with uv, it's as simple as `uv build --all` and include `dist/*`.
- This option allows to bundle private wheels without pushing to a registry.

<small>✅ This is the recommended way to specify dependencies</small>

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>PYAKET_APP_PYPI</kbd> {#app-pypi}
> 📦 <b>Type:</b> String • <b>Default:</b> None

List of PyPI packages to be installed at runtime, separated by `;` (semi colon).

```sh title="Example"
# Regular dependencies, latest version
export PYAKET_APP_PYPI="numpy;plotly;pillow"

# Specific stable version of a package
export PYAKET_APP_PYPI="shaderflow==0.9.0"

# Or even git dependencies, targetting specific branches or tags
export PYAKET_APP_PYPI="git+https://github.com/BrokenSource/DepthFlow"
export PYAKET_APP_PYPI="git+...@develop"
export PYAKET_APP_PYPI="git+...@v1.0.0"
```

This option is partially recommended, as it requires a network download at runtime and pushing to a registry for iterative development. [Bundling wheels](#app-wheels) is often a better option if binary size is not a concern, you can test with wheels first then push a stable version to a registry too.

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>PYAKET_APP_REQTXT</kbd> {#app-requirements-txt}
> 📦 <b>Type:</b> Local Path • <b>Default:</b> None

A local `requirements.txt` file to be installed at runtime.

This option mostly exists for legacy reasons. You really should move to a `pyproject.toml` as it allows easier build backends to create portable wheels for your project that includes your code. The only use I can think of is to run a project-less script with a requirements file alongside it.

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>PYAKET_APP_ROLLING</kbd> {#app-rolling}
> 📦 <b>Type:</b> Bool • <b>Default:</b> False

Always reinstall the project's dependencies when running the executable.

This option is best combined with a `git+` dependency or `package` without a `==version` specifier, to create a one-time binary that self-updates. This is obviously discouraged for any production use, unless very controlled, or in ephemeral runtimes for a couple of reasons:

- **Security**: Any malicious update (on the developer or third party side) will be downloaded and executed on the user's/your machine, _blindly_, without a way to recall.
- **Performance**: The executable will be slower to start and require mandatory network calls at every run, which could give a temporary IP ban if abusing the registry.
- **Stability**: The dependencies may change and break the project.

A valid, but unconventional, use case is to pin all your dependencies to a specific version and target your latest stable PyPI releases (or git main branch) for clients after heavy testing.
