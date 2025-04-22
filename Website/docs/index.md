# Environment Variables

:material-arrow-right: 📦 Pyaket's configuration is done via environment variables read by rust at compile time, which are processed and passed through to the executable to load at runtime.

This page documents all :simple-rust: Rust side environment variables and extra information. You don't need the Python package to build a Pyaket executable if you're skilled with cargo, although most of these have python cognates and follows the same structure seen here.

!!! note "Some settings are exclusive to python"
    - The `--upx` flag can't currently be supported by the rust side yet, as cargo lacks post-build hooks. You can do it yourself though, finding the binary at `target/*/pyaket` and running `upx` on it.
    - The `--standalone` flag is a syntatic sugar for other options; exporting all deps wheels is annoying in rust.







<!-- ----------------------------------------------------------------------- -->
<br><br>

## Application {#app}

:material-arrow-right: General metadata of the project

### <kbd>PYAKET_APP_NAME</kbd> {#app-name}
> 📦 <b>Type:</b> String • <b>Default:</b> Application

The name of the application being built.

Currently only used for identifying • flagging successfull installations and recreating the virtual environment shall the binary hash changes. This is purely useful for iterative development.

<hr>

### <kbd>PYAKET_APP_AUTHOR</kbd> {#app-author}
> 📦 <b>Type:</b> String • <b>Default:</b> BrokenSource

The author's name, group, organization of the application being built.

The value is mostly used for dictating the [workspace](#workspace) root when dynamic. Centralizes installation paths and caches for a given author, while being independent enough to not interfere with others.

<hr>

### <kbd>PYAKET_APP_VERSION</kbd> {#app-version}
> 📦 <b>Type:</b> String • <b>Default:</b> 0.0.0

The version of the application being built.

Should follow the version of the project to be released alonside a registry itself. Not necessarily a semantic version, can be a codename, branch, latest, etc. Value is added to [versions dir](#versions-dir), building the full installation path of the venv to be used.

To get the current version in python, use:

```python
from importlib.metadata import version as get_version

version = get_version("package")
```

Or better yet, if using [Hatch](https://hatch.pypa.io/latest/), define a `__version__` at `__init__.py` and use in `pyproject.toml`:

```python
[tool.hatch.version]
path = "package/__init__.py"

[project]
dynamic = ["version"]
```

<hr>

### <kbd>PYAKET_APP_ROLLING</kbd> {#app-rolling}
> 📦 <b>Type:</b> Bool • <b>Default:</b> False

Always reinstall the project's dependencies when running the executable.

This option is best combined with a `git+` dependency or `package` without a `==version` specifier, to create a one-time binary that self-updates. This is obviously discouraged for any production use, unless very controlled, or in ephemeral runtimes for a couple of reasons:

- **Security**: Any malicious update (on the developer or third party side) will be downloaded and executed on the user's/your machine, _blindly_, without a way to recall.
- **Performance**: The executable will be slower to start and require mandatory network calls at every run, which could give a temporary IP ban if abusing the registry.
- **Stability**: The dependencies may change and break the project.

A valid, but unconventional, use case is to pin all your dependencies to a specific version and target your latest stable PyPI releases (or git main branch) for clients after heavy testing.







<!-- ----------------------------------------------------------------------- -->
<br><br>

## Dependencies {#dependencies}

:material-arrow-right: A continuation of the [application](#app) section for listing dependencies.

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

<hr>

### <kbd>PYAKET_APP_PYPI</kbd> {#app-pypi}
> 📦 <b>Type:</b> String • <b>Default:</b> None

List of PyPI packages to be installed at runtime, separated by `:` (colon).

```sh title="Example"
# Regular dependencies, latest version
export PYAKET_APP_PYPI="numpy:plotly:pillow"

# Specific stable version of a package
export PYAKET_APP_PYPI="shaderflow==0.9.0"

# Or even git dependencies, targetting specific branches or tags
export PYAKET_APP_PYPI="git+https://github.com/BrokenSource/DepthFlow"
export PYAKET_APP_PYPI="git+...@develop"
export PYAKET_APP_PYPI="git+...@v1.0.0"
```

This option is partially recommended, as it requires a network download at runtime and pushing to a registry for iterative development. [Bundling wheels](#app-wheels) is often a better option if binary size is not a concern, you can test with wheels first then push a stable version to a registry too.

<hr>

### <kbd>PYAKET_APP_REQTXT</kbd> {#app-requirements-txt}
> 📦 <b>Type:</b> Local Path • <b>Default:</b> None

A local `requirements.txt` file to be installed at runtime.

This option mostly exists for legacy reasons. You really should move to a `pyproject.toml` as it allows easier build backends to create portable wheels for your project that includes your code. The only use I can think of is to run a project-less script with a requirements file alongside it.






<!-- ----------------------------------------------------------------------- -->
<br><br>

## Entry Points

:material-arrow-right: This section is about the entry points of the executable run after the installation.

- At least one entry point is required, otherwise it'll boot to the Python shell.
- All incoming args of the executable are passed through to the final command.

<hr>

### <kbd>PYAKET_ENTRY_MODULE</kbd> {#entry-module}
> 📦 <b>Type:</b> String • <b>Default:</b> None

A module's name to be called as `python -m <module> (args)` after installation.

- The file `<module>/__main__.py` must exist, otherwise it will error out.

<small>✅ This is the recommended and reliable way to run your project, have a top-level cli for multiple entries</small>

<hr>

### <kbd>PYAKET_ENTRY_SCRIPT</kbd> {#entry-script}
> 📦 <b>Type:</b> String • <b>Default:</b> None

A local script to be bundled and called as `python <script.py> (args)` after installation.

<hr>

### <kbd>PYAKET_ENTRY_CODE</kbd> {#entry-code}
> 📦 <b>Type:</b> String • <b>Default:</b> None

An inline Python code to be executed as `python -c <code> (args)` after installation.

- Slightly more reliable than an [entry script](#entry-script), as it doesn't write a temp file.
- Less flexible and readable because it must be a single line of code.

<hr>

### <kbd>PYAKET_ENTRY_COMMAND</kbd> {#entry-command}
> 📦 <b>Type:</b> String • <b>Default:f</b> None

A command to be executed as `<command> (args)` after installation.

- The venv is activated and the bin directory is added to PATH, so this can be a script defined in your `pyproject.toml` • `[project.scripts]` section.

It may be used if you have multiple entry points, like `depthflow {main,gradio}`, and want to hardcode pin one to be used, or set fixed arguments to some command.

!!! warning "**Discouraged**: Security implications, man in the middle attack, may use wrong command"






<!-- ----------------------------------------------------------------------- -->
<br><br>

## Directories {#dirs}

:material-arrow-right: Directories used by Pyaket to store the application data.

### <kbd>WORKSPACE</kbd> {#workspace}
> 📦 <b>Type:</b> Path • <b>Default:</b> Dynamic

The workspace root directory Pyaket will use for the project.

This is a special variable that can be overriden at runtime and is dynamic if unset. By default, Pyaket uses proper and intended platform directories to store the application data:

!!! tip ""
    <table markdown>
        <tbody class="slim-table">
            <tr>
                <td style="width: 20%">:material-microsoft: Windows</td>
                <td><kbd>C:\\\\Users\\User\\AppData\\Local\\Author</kbd></td>
            </tr>
            <tr>
                <td>:simple-apple: MacOS</td>
                <td><kbd>~/Library/Application Support/Author</kbd></td>
            </tr>
            <tr>
                <td>:simple-linux: Linux</td>
                <td><kbd>~/.share/Author</kbd></td>
            </tr>
        </tbody>
    </table>

Shall a user set it, the value is used as is. This is especially useful if folks have a full C:\\\\ drive or want a custom directory than the above for large application data. A Python project should follow the same pattern, so all files are in the same place for easier uninstallation.

```sh title="Example"
$ export WORKSPACE="/tmp/workspace"
$ ./pyaket-project.bin
```

<hr>

### <kbd>PYAKET_COMMON_DIR</kbd> {#common-dir}
> 📦 <b>Type:</b> Path • <b>Default:</b> Pyaket

The subdirectory of the [workspace](#workspace) to use for all Pyaket installation and runtime files.

By default, things are stored in a `Pyaket` directory (due lack of a better name). All other internal directories derives from this one. It can be left empty if you'll not use platformdirs yourself.

!!! tip ""
    <table markdown>
        <tbody class="slim-table">
            <tr>
                <td style="width: 20%">:material-microsoft: Windows</td>
                <td><kbd>C:\\\\Users\\User\\AppData\\Local\\Author\\Pyaket</kbd></td>
            </tr>
            <tr>
                <td>:simple-apple: MacOS</td>
                <td><kbd>~/Library/Application Support/Author/Pyaket</kbd></td>
            </tr>
            <tr>
                <td>:simple-linux: Linux</td>
                <td><kbd>~/.share/Author/Pyaket</kbd></td>
            </tr>
            <tr>
                <td style="width: 20%">:material-cube: Custom</td>
                <td><kbd>Workspace/Pyaket</kbd></td>
            </tr>
        </tbody>
    </table>

You may find the following directories inside the composition:

- **Astral**: Stores uv versions, archives and unpacked files.
- **Cache**: Used for `UV_CACHE_DIR`, primarily package download caches.
- **Python**: Stores multiple versions of Python distributions.
- **Versions**: See [versions dir](#versions-dir) for more details.

<hr>

### <kbd>PYAKET_VERSIONS_DIR</kbd> {#versions-dir}
> 📦 <b>Type:</b> String • <b>Default:</b> Versions

The subdirectory of the [common](#common-directory) directory to install the virtual environments.

Multiple versions of the same application(s) are stored in a shared directory (venv). From the table below, `(...)` is replaced with the [version](#app-version), yielding the full installation path.

!!! tip ""
    <table markdown>
        <tbody class="slim-table">
            <tr>
                <td style="width: 20%">:material-microsoft: Windows</td>
                <td><kbd>C:\\\\Users\\User\\AppData\\Local\\Author\\Pyaket\\Versions\\(...)</kbd></td>
            </tr>
            <tr>
                <td>:simple-apple: MacOS</td>
                <td><kbd>~/Library/Application Support/Author/Pyaket/Versions/(...)</kbd></td>
            </tr>
            <tr>
                <td>:simple-linux: Linux</td>
                <td><kbd>~/.share/Author/Pyaket/Versions/(...)</kbd></td>
            </tr>
            <tr>
                <td style="width: 20%">:material-cube: Custom</td>
                <td><kbd>Workspace/Pyaket/Versions/(...)</kbd></td>
            </tr>
        </tbody>
    </table>

- **Note**: Applications of an author that shares the same versions dir **must** be coupled together. If they are independent, a workaround is to set this value to `Versions/<app_name>`, so each application have a separate versions directory. Default is shared for monorepos in mind.







<!-- ----------------------------------------------------------------------- -->
<br><br>

## Python {#python}

:material-arrow-right: This section is about the Python interpreter to be used at runtime.

### <kbd>PYAKET_PYTHON_VERSION</kbd> {#python-version}
> 📦 <b>Type:</b> Version string • <b>Default:</b> 3.13

The version of Python to be used at runtime, from [astral-sh/python-build-standalone](https://github.com/astral-sh/python-build-standalone/).

- **Note**: Specific versions support, such as `3.10.17`, depends on the [uv-version](#uv-version) in use, as the URLs are hard-coded in their binary. For example, `3.13.3` was added in [v0.6.14](https://github.com/astral-sh/uv/releases/tag/0.6.14).

- Please chose carefully to ensure all your wheels and dependencies are compatible with the target version. Users may not have compilers and headers for sdists.

<hr>

### <kbd>PYAKET_PYTHON_BUNDLE</kbd> {#python-bundle}
> 📦 <b>Type:</b> Bool • <b>Default:</b> False

Whether to embed the python distribution in the executable, instead of a runtime download.

Having this enabled increases binary size by roughly 20 MB, but greatly increases reliability and improves first startup times. However, it may trigger antivirus heuristics on giving false positives, as it is a sketchy thing to include archives and decompressors in a binary - this is mostly a non-issue Windows only moment. Disabled by default for easy to share small executables.

<small><b>⚠️ Warning:</b> This feature is not yet implemented</small>







<!-- ----------------------------------------------------------------------- -->
<br><br>

## UV {#uv}

:material-arrow-right: This section is about [uv](https://github.com/astral-sh/uv), a fast python and project manager, to be used at runtime.

Pyaket wouldn't be possible without it, huge kudos to the Astral Team!

### <kbd>PYAKET_UV_VERSION</kbd> {#uv-version}
> 📦 <b>Type:</b> Version string • <b>Default:</b> 0.6.14

The version of uv to be used at runtime, from official [astral-sh/uv](https://github.com/astral-sh/uv/) releases.

- **Note**: This value shouldn't really be changed. Older versions may miss features, newer ones might have breaking changes. Pyaket guarantees only the default version to work.

<hr>

### <kbd>PYAKET_UV_BUNDLE</kbd> {#uv-bundle}
> 📦 <b>Type:</b> Bool • <b>Default:</b> True

Whether to embed the uv distribution in the executable, instead of a runtime download.

Having this enabled increases binary size by roughly 20 MB, but greatly increases reliability and improves first startup times. However, it may trigger antivirus heuristics on giving false positives, as it is a sketchy thing to include archives and decompressors in a binary - this is mostly a non-issue Windows only moment. Disabled by default for easy to share small executables.






<!-- ----------------------------------------------------------------------- -->
<br><br>

## PyTorch

This section covers [PyTorch](https://pytorch.org/) configuration for ML and AI projects.

- **Note**: Will be installed before others, to avoid using a platform default in the dependencies. Pip should skip ok, unless you specify `x.y.z==flavor`, which errors out.

- **Warn**: Version 2.7.0+ with cu128 is required for RTX 5000+ series! [[1]](https://en.wikipedia.org/wiki/CUDA#GPUs_supported)

<hr>

### <kbd>PYAKET_TORCH_VERSION</kbd> {#torch-version}
> 📦 <b>Type:</b> Version string • <b>Default:</b> None

An optional version of PyTorch to be installed at runtime.

<hr>

### <kbd>PYAKET_TORCH_BACKEND</kbd> {#torch-backend}
> 📦 <b>Type:</b> String • <b>Default:</b> auto

The hardware acceleration backend of PyTorch to be installed at runtime.

- When set to auto, uv will decide the best one ([experimental](https://docs.astral.sh/uv/guides/integration/pytorch/#automatic-backend-selection))
- Other values will be passed to the `--extra-index-url` as:

```sh
uv pip install torch==${VERSION}$+${BACKEND}
    --extra-index-url https://download.pytorch.org/whl/${BACKEND}
```

:material-arrow-right: The allowed values depends on the PyTorch version. You can check [this page](https://pytorch.org/get-started/locally/) for the latest values, and this [other page](https://pytorch.org/get-started/previous-versions/) for older ones. ROCm is for AMD GPUs. Use empty for default.
