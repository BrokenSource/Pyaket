---
icon: simple/rust
---

!!! warning
    This section is outdated and needs a cleanup/rewrite:

    - Cross compilation to MacOS needs an SDK
    - Rust is now auto-provided by [Rustbin](https://github.com/BrokenSource/Rustbin)


📦 Pyaket uses the rust programming language for its core functionality.

<b><span class="the">D</span>eveloping</b> or compiling rust projects requires a toolchain - collection of a compiler, project manager, standard library, and other tools. Luckily, the official installation method [rustup](https://www.rust-lang.org/tools/install) manages it all for you, including cross compilation (except for a few external dependencies).

:material-arrow-right: All major platforms are [supported](https://doc.rust-lang.org/nightly/rustc/platform-support.html#tier-1-with-host-tools), though some might be problematic for your project.

## Native {#native}

<!------------------------------------------------------------------------------------------------->
<hr>

### :simple-linux: Linux

Install [rustup](https://www.rust-lang.org/tools/install) with the official installation script, or from your package manager:

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Ensure you have your Distro's equivalent of a `base-devel` package installed and/or mingw:

=== ":material-ubuntu: Ubuntu"
    ```sh
    # Native compilation
    sudo apt install build-essential

    # Cross compilation
    sudo apt install mingw-w64
    ```
=== ":material-arch: Arch Linux"
    ```sh
    # Native compilation
    sudo pacman -Syu base-devel

    # Cross compilation
    sudo pacman -Syu mingw-w64-toolchain
    ```
=== ":material-fedora: Fedora"
    ```sh
    # Native compilation
    sudo dnf install gcc

    # Cross compilation
    sudo dnf install mingw64-gcc
    ```
=== ":material-debian: Debian"
    ```sh
    # Native compilation
    sudo apt install build-essential

    # Cross compilation
    sudo apt install mingw-w64
    ```

This script should have added `~/.cargo/bin` to your `PATH` environment based on your shell.

:material-arrow-right: **Note**: You may need to restart the terminal to have `cargo` and `rustc` available, ensure it.

<!------------------------------------------------------------------------------------------------->
<hr>

### :material-microsoft: Windows

Ensure you have [WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/) installed, open a powershell and run:

```python
winget install --id=Rustlang.Rustup -e
```

There's two options for a C linker/compiler now, :simple-gnu: MinGW or :material-microsoft: Visual C++ Build Tools (MSVC).

:material-arrow-right: **Reason**: Rust can't bundle Build Tools due licensing, out of two let the user choose one. Some crates links against system libraries, such as zstd or networking, and need to interface with C.

Overall, it's easier to get started with MinGW, which is needed for cross compiling to macOS and Linux anyway. Go with MSVC if you prefer official Microsoft tools or will only target Windows.

<br>

#### :simple-gnu: MinGW

Download and install [MSYS2](https://www.msys2.org/), a lightweight Linux-like shell and package manager for Windows, in the default location at `C:\msys64`.

!!! success "**That's it:** The python package will auto install dependencies for the platform you're compiling for"

<br>

#### :material-microsoft: MSVC

To avoid any potential confusion, here's a brief clarification on product names:

- :material-microsoft-visual-studio: **Visual Studio** is a full IDE for C#, C++, .NET development, the original one (purple) [#](https://visualstudio.microsoft.com/)
- :material-microsoft-visual-studio-code: **Visual Studio Code** is a lightweight code editor with many extensions (blue) [#](https://code.visualstudio.com/)
- :octicons-tools-16: **Visual Studio Build Tools** is just the compiler, linker for C/C++, without the IDE [#](https://visualstudio.microsoft.com/downloads/?q=build+tools#build-tools-for-visual-studio-2022)

Download and install [Build Tools for Visual Studio](https://visualstudio.microsoft.com/downloads/?q=build+tools#build-tools-for-visual-studio-2022), enable the following components:

1. Visual C++ Build Tools
2. Windows 10 SDK
3. Windows 11 SDK

This process can be somewhat reliabily automated by running:

```ps1 title="PowerShell"
winget install --id Microsoft.VisualStudio.2022.BuildTools `
    --override " `
        --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 `
        --add Microsoft.VisualStudio.Component.Windows10SDK `
        --add Microsoft.VisualStudio.Component.Windows11SDK `
    " `
    --wait --passive
```

You should have `cl.exe`, `link.exe` and `msvc.exe` available in your shell.

<!------------------------------------------------------------------------------------------------->
<hr>

### :simple-apple: macOS

Install [Homebrew](https://brew.sh/) and [Xcode](https://developer.apple.com/xcode/), then rustup with:

```sh
brew install rustup
```

:material-microsoft: Windows cross compilation:

```sh
brew install mingw-w64
```

:simple-linux: Linux cross compilation:

```sh
brew install gcc
```

<!------------------------------------------------------------------------------------------------->
<br>

## Workflows

### GitHub Actions

Runners seem to already have rustup installed by default. Better be safe than sorry though - you can add the following action in your workflow job steps by [@dtolnay](https://github.com/dtolnay/rust-toolchain) _(unofficial)_:

```yaml
- name: Setup Rust
  uses: dtol/rust-toolchain@stable
```

For compiling Linux ARM binaries, you might need:

```yaml
- name: Install gcc aarch64
  run: sudo apt install -y gcc-aarch64-linux-gnu
```

A full workflow file could look like this:

!!! note "Ensure wider compatibility by compiling with the oldest Linux runner you can get"
    The final binary will only work with the glibc version greater than or equal to the one used to compile it of the host. This is a core part of the Linux ABI, desktop distros are well updated but servers or embedded systems may not be.

```yaml title="<small>.github/workflows/make-pyaket.yml</small>"
name: make-pyaket

on:
  workflow_dispatch:

jobs:
  main:
    name: Compile on (${{matrix.os}})
    runs-on: ${{matrix.os}}
    strategy:
      matrix:
        os: [ubuntu-22.04, windows-latest, macos-latest]
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          submodules: recursive

      - name: Setup Rust
        uses: dtolnay/rust-toolchain@stable

      - name: Install gcc aarch64
        if: ${{matrix.os == 'ubuntu-22.04'}}
        run: sudo apt install -y gcc-aarch64-linux-gnu

      - name: Compile projects
        run: pyaket (...)

      - name: Upload releases
        uses: actions/upload-artifact@v4
        with:
          name: ${{matrix.os}}-release
          path: release/*
```

