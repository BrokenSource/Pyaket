📦 Pyaket uses the rust programming language for its core functionality.

<b><span class="the">D</span>eveloping</b> or compiling rust projects requires a toolchain - collection of a compiler, project manager, standard library, and other tools. Luckily, [rustup](https://www.rust-lang.org/tools/install), the official installation method, manages it all for you, including cross compilation; except for few external dependencies.

:material-arrow-right: All major platforms are [supported](https://doc.rust-lang.org/nightly/rustc/platform-support.html#tier-1-with-host-tools), though some might be problematic for your dependencies.

## Native {#native}

✅ You can run `#!ps1 $ pyaket rust` to install everything you need for your platform!

### :material-microsoft: Windows

Ensure you have [Winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) installed, open a powershell and run:

```python
winget install --id=Rustlang.Rustup -e
```

There's two options for a C linker/compiler, :simple-gnu: MinGW or :material-microsoft: Visual C++ Build Tools (MSVC).

:material-arrow-right: **Reason**: Rust can't bundle Build Tools due licensing, out of two let the user choose one. Some crates links against system libraries, such as zstd or networking, and need to interface with C.

Overall, it's easier to get started with MSVC if you're in a hurry or prefer official Microsoft tools - at the cost of maybe needing a [license](https://visualstudio.microsoft.com/license-terms/vs2022-ga-diagnosticbuildtools/) for medium companies. MinGW isn't bad, just extra steps.

<br>

#### :material-microsoft: MSVC

To avoid any potential confusion, here's a brief clarification on confusing products:

- :material-microsoft-visual-studio: **Visual Studio** is a full IDE for C#, C++, .NET development, the original one (purple) [#](https://visualstudio.microsoft.com/)
- :material-microsoft-visual-studio-code: **Visual Studio Code** is a lightweight code editor with many extensions (blue) [#](https://code.visualstudio.com/)
- :octicons-tools-16: **Visual Studio Build Tools** is just the compiler, linker for C/C++, without the IDE [#](https://visualstudio.microsoft.com/downloads/?q=build+tools#build-tools-for-visual-studio-2022)

Download and install [Build Tools for Visual Studio](https://visualstudio.microsoft.com/downloads/?q=build+tools#build-tools-for-visual-studio-2022), enable the following components:

1. Visual C++ Build Tools
2. Windows 10 SDK
3. Windows 11 SDK

This process can be somewhat reliabily automated by running:

```ps1
winget install --id Microsoft.VisualStudio.2022.BuildTools `
    --override " `
        --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 `
        --add Microsoft.VisualStudio.Component.Windows10SDK `
        --add Microsoft.VisualStudio.Component.Windows11SDK.22000 `
    " `
    --wait --passive
```

You should have `cl.exe`, `link.exe` and `msvc.exe` available in your shell to verify.

<br>

#### :simple-gnu: MinGW

Download and install [MSYS2](https://www.msys2.org/), a lightweight Linux-like shell and package manager for Windows. Their homepage _conveniently_ lists instructions for installing the MinGW toolchain 🙂

Either way, search for a MSYS2 Terminal application in your system, and run:

```ps1
pacman -Sy mingw-w64-ucrt-x86_64-gcc
```

:material-arrow-right: **Note**: MinGW will only be available inside the MSYS2 terminal, you might need to cd into your project's directory with `#!sh cd /c/Users/user/.../Project`, activate the venv with `activate.sh`.

<hr>

### :simple-linux: Linux

Ensure you have your Distro's equivalent of a `base-devel` package installed, and `rustup`:

=== ":material-ubuntu: Ubuntu"
    ```sh
    # Update the package list
    sudo apt update

    # Native compilation and rustup
    sudo apt install rustup build-essential -y
    ```
=== ":material-arch: Arch Linux"
    ```sh
    # Native compilation and rustup
    sudo pacman -Syu rustup base-devel

    # Windows cross compilation
    sudo pacman -Syu mingw-w64-toolchain
    ```
=== ":material-fedora: Fedora"
    ```sh
    # Native compilation and rustup
    sudo dnf install rustup gcc

    # Windows cross compilation
    sudo dnf install mingw64-gcc
    ```
=== ":material-debian: Debian"
    ```sh
    # Update the package list
    sudo apt update

    # Native compilation and rustup
    sudo apt install rustup build-essential -y
    ```

Either way, running rustup's official command should work too:

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

This script should have added `~/.cargo/bin` to your `PATH` environment based on your shell.

:material-arrow-right: **Note**: You may need to restart the terminal to have `cargo` and `rustc` available.

<hr>

### :simple-apple: macOS

Ensure you have [Homebrew](https://brew.sh/) and [Xcode](https://developer.apple.com/xcode/) installed, install rustup with:

```sh
brew install rustup
```

<br>

## Workflows

### GitHub Actions

Runners seem to already have rustup installed by default. Better be safe than sorry though - you can add the following action in your workflow job steps by [@dtolnay](https://github.com/dtolnay/rust-toolchain) _(unofficial)_:

```yaml
- name: Install Rust
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

```yaml title=".github/workflows/make-pyaket.yml"
name: make-pyaket

jobs:
  main:
    name: Compile on (${{matrix.os}})
    runs-on: ${{matrix.os}}
    strategy:
      matrix:
        os: [ubuntu-22.04, windows-latest, macos-latest]
    steps:

      # Checkout repository, install dependencies, etc.

      - name: Install gcc aarch64
        if: ${{matrix.os == 'ubuntu-22.04'}}
        run: sudo apt install -y gcc-aarch64-linux-gnu

      - name: Compile projects
        run: pyaket (...)

      - name: Upload releases
        uses: actions/upload-artifact@v4
        with:
          name: ${{matrix.os}}-release
          path: Release/*
```

