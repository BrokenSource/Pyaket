<div align="center">
  <img src="https://raw.githubusercontent.com/BrokenSource/Pyaket/main/Pyaket/Resources/Images/Pyaket.png" width="210" onerror='this.src="Pyaket/Resources/Images/Pyaket.png"'>
  <h1 style="margin-top: 0">Pyaket</h1>
  <span>📦 Easy Python to → Fast Executables 📦</span>
  <br>
  <br>
    <a href="https://crates.io/crates/pyaket/"><img src="https://img.shields.io/crates/v/pyaket?label=Crates.io&color=orange"></a>
    <a href="https://crates.io/crates/pyaket/"><img src="https://img.shields.io/crates/d/pyaket?label=Downloads&color=orange"></a>
    <a href="https://pypi.org/project/pyaket/"><img src="https://img.shields.io/pypi/v/pyaket?label=PyPI&color=blue"></a>
    <a href="https://pypi.org/project/pyaket/"><img src="https://img.shields.io/pypi/dw/pyaket?label=Installs&color=blue"></a>
    <a href="https://github.com/BrokenSource/Pyaket/"><img src="https://img.shields.io/github/v/tag/BrokenSource/Pyaket?label=GitHub&color=orange"></a>
    <a href="https://github.com/BrokenSource/Pyaket/stargazers"><img src="https://img.shields.io/github/stars/BrokenSource/Pyaket?label=Stars&style=flat&color=orange"></a>
    <a href="https://discord.gg/KjqvcYwRHm"><img src="https://img.shields.io/discord/1184696441298485370?label=Discord&style=flat&color=purple"></a>
  <br>
  <br>
  <b>
    Links •
    <a href="https://pyaket.dev/get/">✅ Installation</a> •
    <a href="https://pyaket.dev/examples/">⭐️ Examples</a> •
    <a href="https://pyaket.dev/docs/">📝 Documentation</a> •
    <a href="https://github.com/BrokenSource/Pyaket/issues">🔥 Issues</a>
  </b>
  <br>
  <sub>
    <a href="https://www.github.com/BrokenSource/Pyaket">GitHub</a> •
    <a href="https://pyaket.dev/contact">Contact</a> •
    <a href="https://pyaket.dev/changelog">Changelog</a> •
    <a href="https://pyaket.dev/license">License</a>
  </sub>
  <br>
  <br>
</div>

> [!WARNING]
> This project is under active development, certain parts are incomplete and not fully tested yet.
>
> - Install with `pip install git+https://github.com/BrokenSource/Pyaket` for now!
>

<!-- Todo: Demo video here, as always -->

## 🔥 Description

📦 **Pyaket** is a tool that bundles and generates portable executables of your Python projects for all platforms. No more convoluted installation instructions for casual users, give them the exe file they want [[1]](https://github.com/sherlock-project/sherlock/issues/2011), without reinventing the _wheel_ on alternative packaging solutions.

✨ Major features include:

- [x] **Fast** installation, automatically manages python, venvs, and dependencies.
- [x] **Cross** compilation to multiple platforms and architectures made easy [#](#cross-compilation)
- [ ] **Standalone** executables without network calls at runtime (planned).
- [x] **Iterative** development in mind, reinstalls a version if the binary changes.
- [x] **Smart** and safe, detects partial installs, downloads, unpacks.
- [x] **First class** monorepo support, bundle many wheels to be installed at runtime.
- [x] **Rolling** releases are supported, single binary that runs last version always [#](https://pyaket.dev/docs/configuration/#rolling)
- [x] **PyTorch** optional installation at runtime, automatic backend detection. [#](https://pyaket.dev/docs/configuration/#torch-backend)
- [ ] **Version** management, easy uninstallation and updates notifications (planned).
- [ ] **Splash** screen to look fancy, custom icons for your app (planned).

<sup><b>🚀 Powered by:</b> [astral-sh/uv](https://github.com/astral-sh/uv) • [rust-lang](https://www.rust-lang.org/) • [cargo-zigbuild](https://github.com/rust-cross/cargo-zigbuild) • [rust-embed](https://crates.io/crates/rust-embed) • [mkdocs](https://www.mkdocs.org/) • [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) • and others!</sup>

## ⚔️ Cross compilation

Thanks to Rust's amazing toolchain, coupled with [cargo-zigbuild](https://github.com/rust-cross/cargo-zigbuild), and mostly using pure Rust crates, Pyaket can pretty much compile executables _from any_ platform _to any_ platform.

- No Docker or Virtual Machines required!

The table below shows the known status for all combinations, help me with feedback!

<br>

<div align="center" markdown>

  <b>Cross compilation compatibility</b>

  | From / To | <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/linux.svg" width="70"> <p> N/A | <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/apple.svg" width="70"> <p> N/A | <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/windows.svg" width="70"> <p> GNU| <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/windows.svg" width="70"> <p> MSVC |
  | :-------------- | :---------------- | :---------------- | :----------------- | :---------------- |
  | 🐧 **Linux** x86   | ✅ x86 <p> ☑️ Arm | ☑️ x86 <p> ☑️ Arm | ✅ x86 <p> ☑️ Arm | 🚫 x86 <p> 🚫 Arm |
  | 🐧 **Linux** Arm   | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | 🚫 x86 <p> 🚫 Arm |
  | 💠 **Windows** x86 | ✅ x86 <p> ☑️ Arm | ☑️ x86 <p> ☑️ Arm | ✅ x86 <p> ☑️ Arm | ✅ x86 <p> 🤏 Arm |
  | 💠 **Windows** Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm |
  | 🍎 **MacOS** x86   | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | 🚫 x86 <p> 🚫 Arm |
  | 🍎 **MacOS** Arm   | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | 🚫 x86 <p> 🚫 Arm |

  <sup><b>Note:</b> The table says if it simply <i>compiles or run</i>, your Python project may not work on all platforms.</sup>

</div>

**Legend:**

- ✅ Verified and supported
- ☑️ Compiled, but untested
- ✔️ Should work, untested
- 🤏 Almost compiled
- 🚫 Impractical

## 📦 Installation

Head out to the [**website**](https://pyaket.dev/get) for the latest installation instructions and more!

<!-- Todo: Website screenshot, as always -->

## 💰 Commercial

Pyaket is free to use for open source projects that distributes releases at no cost.

Commercial usage (including selling executables, for-profit deployments) or bundling proprietary software requires an appropriate [sponsorship tier](https://github.com/sponsors/Tremeschin). You may freely evaluate the viability beforehand, or use it to get started at a limited budget. Fair and enables me to keep the project alive and improve it over time.

Get in touch if you have any questions, need support or features, or want a custom agreement!

## ♻️ Community

<small>✅ **Be featured here** if you're using Pyaket in your projects!</small>

_🌵 Such an empty place here, for now.._
