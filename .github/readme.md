<div align="center">
  <img src="https://raw.githubusercontent.com/BrokenSource/Pyaket/main/pyaket/resources/images/logo.png" width="210">
  <h1>Pyaket</h1>
  <span>📦 Easy Python to → Fast Executables 📦</span>
  <br>
  <br>
    <a href="https://crates.io/crates/pyaket/"><img src="https://img.shields.io/crates/v/pyaket?label=Crates.io&color=orange"></a>
    <a href="https://crates.io/crates/pyaket/"><img src="https://img.shields.io/crates/d/pyaket?label=↓&color=orange"></a>
    <a href="https://pypi.org/project/pyaket/"><img src="https://img.shields.io/pypi/v/pyaket?label=PyPI&color=blue"></a>
    <a href="https://pypi.org/project/pyaket/"><img src="https://img.shields.io/pypi/dw/pyaket?label=↓&color=blue"></a>
    <a href="https://github.com/BrokenSource/Pyaket/"><img src="https://img.shields.io/github/v/tag/BrokenSource/BrokenSource?label=GitHub&color=orange"></a>
    <a href="https://github.com/BrokenSource/Pyaket/stargazers/"><img src="https://img.shields.io/github/stars/BrokenSource/Pyaket?label=Stars&style=flat&color=orange"></a>
    <a href="https://discord.gg/KjqvcYwRHm"><img src="https://img.shields.io/discord/1184696441298485370?label=Discord&style=flat&color=purple"></a>
  <br>
  <br>
  <b>
    Links •
    <a href="https://pyaket.dev/get/">Installation</a> •
    <a href="https://pyaket.dev/examples/">Examples</a> •
    <a href="https://pyaket.dev/docs/">Documentation</a> •
    <a href="https://github.com/BrokenSource/Pyaket/issues/">Issues</a>
  </b>
  <br>
  <sub>
    <a href="https://github.com/BrokenSource/Pyaket/">GitHub</a> •
    <a href="https://pyaket.dev/about/contact/">Contact</a> •
    <a href="https://pyaket.dev/about/changelog/">Changelog</a> •
    <a href="https://pyaket.dev/about/license">License</a>
  </sub>
  <br>
  <br>
</div>

> [!IMPORTANT]
> This project is under active development. Basic functionality works, but some features are incomplete, documentation needs improvement, and more testing is required. Feedback is welcome 🙂

<!-- Todo: Demo video here, as always -->

## 🔥 Description

**📦 Pyaket** is a tool that bundles and generates portable executables of your python projects for all platforms. No more convoluted installation steps, give users the convenience [they want](https://github.com/sherlock-project/sherlock/issues/2011), with maximum compatibility and dev-centric ease of use compared to alternative solutions.

- [x] **Lightning fast** installation that automatically manages python, virtual environments, and dependencies without user intervention that just works, bundle wheels or install from pypi.
- [x] **Max compatibility** with how the project is run in the user's machine - pyaket does not _reinvent the wheel_ or compile python with an intermediate, use tools that already exists [#](https://pyaket.dev/faq/general/#how-it-works)
- [x] **Cross compile** from anywhere to most platforms and architectures, no docker or virtual machines required, portable immutable executables - see the table for details! [#](https://pyaket.dev/docs/crosscompiling/)
- [x] **Intelligently** detects partial installations, downloads, archive unpacks, and automatically takes appropriate action - making iterative development easy and resilient against users
- [ ] **Standalone** executables with no network calls at runtime that bundles all dependencies [#](https://github.com/BrokenSource/Pyaket/issues/2)
- [x] **Monorepo** support in mind, decoupled dependencies and entry point specification
- [x] **Rolling** releases where a single binary always runs latest pypi or git branch/tag [#](https://pyaket.dev/docs/rust/#rolling)
- [x] **PyTorch** installation at runtime, automatic backend detection (optional). [#](https://pyaket.dev/docs/rust/#torch-backend)

<!------------------------------------------------------------------------------------------------->

## ⭐️ Examples

### Simple to use

Compile a [cowsay](https://pypi.org/project/cowsay/) binary for the current platform and run it:

```sh hl_lines="1"
$ pyaket app --name cowsay --pypi "cowsay==6.1" run --module cowsay compile
  Compiling libc v0.2.172
  Compiling typenum v1.18.0
  ...
  Finished `release` profile [optimized] target(s) in 9.88s
```

```sh hl_lines="1"
$ ./release/cowsay-linux-amd64-v0.0.0.bin -t "Hello, Pyaket!"
  ______________
| Hello, Pyaket! |
  ==============
     \
      \
        ^__^
        (oo)\_______
        (__)\       )\/\
            ||----w |
            ||     ||
```

### Fast iterative development

with a warm build cache:

```sh hl_lines="1"
$ pyaket app -n cowsay -p "cowsay==6.1" run -m cowsay compile
  Finished `release` profile [optimized] target(s) in 1.54s
```

### Blazingly fast

after the first installation:

```sh hl_lines="1 5"
$ hyperfine "./release/cowsay-linux-amd64-v0.0.0.bin -t anyhow"
  Time (mean ± σ):      23.3 ms ±   0.3 ms    [User: 15.8 ms, System: 7.2 ms]
  Range (min … max):    22.9 ms …  24.8 ms    100 runs

$ hyperfine "python -m cowsay -t anyhow"
  Time (mean ± σ):      18.5 ms ±   0.1 ms    [User: 14.2 ms, System: 4.1 ms]
  Range (min … max):    18.2 ms …  19.0 ms    100 runs
```

<sup><b>Note:</b> The actual benchmark command was `nice -20 taskset -c 2 hyperfine -w 50 -r 100 -N (...)`</sup>

### Cross compile

to most platforms and architectures easily:

```sh hl_lines="2 5"
# Windows executables compiled from linux, needs a mingw64 toolchain!
$ pyaket app -n cowsay -p "cowsay==6.1" run -m cowsay release -t windows compile
  Finished `release` profile [optimized] target(s) in 8.11s

$ wine ./Release/cowsay-windows-amd64-v0.0.0.exe -t "Hello, Wine!"
  ____________
| Hello, Wine! |
  ============
            \
             \
               ^__^
               (oo)\_______
               (__)\       )\/\
                   ||----w |
                   ||     ||
```

```sh hl_lines="2 5"
# Intel Macbook @ ./release/cowsay-macos-amd64-v0.0.0.bin
$ pyaket ... release --target macos --arch amd64 compile

# Apple Silicon @ ./release/cowsay-macos-arm64-v0.0.0.bin
$ pyaket ... release --target macos --arch arm64 compile
```

### Bundle wheels

and install them at runtime, perfect for monorepos:

```sh hl_lines="1 6"
$ uv build --all-packages --wheel
  Successfully built dist/shared-1.0.0-py3-none-any.whl
  Successfully built dist/project_a-1.0.0-py3-none-any.whl
  Successfully built dist/project_b-1.0.0-py3-none-any.whl

# Both will share the same virtual environment 🤯
# ./release/{project_a,project_b}-linux-amd64-v0.0.0.bin
$ pyaket app -n project_a -w "dist/*.whl" run -m project_a compile
$ pyaket app -n project_b -w "dist/*.whl" run -m project_b compile
```

### Install pytorch

at runtime, with automatic backend detection:

```sh hl_lines="2 5"
# ./release/app-linux-amd64-v0.0.0-auto.bin
$ pyaket ... torch -v 2.7.0 -b auto compile

# ./release/app-linux-amd64-v0.0.0-cu128.bin
$ pyaket ... torch -v 2.7.0 -b cu128 compile
```

### More examples

For more examples, proper configuration and advanced features, check out the [**website**](https://pyaket.dev/examples) page!

<!-- Todo: Actual website examples page -->
<a href="https://pyaket.dev/examples">
  <img src="https://github.com/user-attachments/assets/8470c0d2-46de-4068-b9ce-a1261a6c0e69">
</a>

<!------------------------------------------------------------------------------------------------->

## 📦 Installation

For now, it is better to install pyaket directly from the source code for the latest features and fixes:

```sh
# Optional 'cross' feature for cross compilation support with cargo-zigbuild
python3 -m pip install git+https://github.com/BrokenSource/Pyaket[cross]
```

A PyPI and Rust Crate of the same name are also available, but might lag behind from git main.

For further setup, refer to the website [**installation**](https://pyaket.dev/get/) page.


### Python Package

> **Package**: https://pypi.org/project/pyaket/

Either add to your project's `dev-dependencies` with the tool you use:

- `uv add pyaket --dev`
- `pdm add pyaket --dev`
- `poetry add pyaket --dev`

Or install in the current venv directly:

- `python3 -m pip install pyaket`
- `uv pip install pyaket`

Or use it as a [uv tool](https://docs.astral.sh/uv/guides/tools/):

- `uvx pyaket app --name cowsay ... compile`


### Rust Crate

> Crate: https://crates.io/crates/pyaket

This is advanced usage, but also works:

```sh
$ export PYAKET_APP_NAME="cowsay"
$ export PYAKET_APP_PYPI="cowsay==6.1"
$ export PYAKET_ENTRY_MODULE="cowsay"

# Remove previous compilation
$ rm ./target/bin/pyaket

# Compile it from crates.io
$ cargo install pyaket --root ./target
    Finished `release` profile [optimized] target(s) in 10.27s
  Installing ./target/bin/pyaket

# Run your project, rename it to your choice!
$ ./target/bin/pyaket
```

<!------------------------------------------------------------------------------------------------->

## ♻️ Community

<sup>✅ **Be featured here** if you're using Pyaket in your projects!</sup>

_🌵 Such an empty place here, for now.._
