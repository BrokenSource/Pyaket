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
    <a href="https://github.com/BrokenSource/Pyaket/"><img src="https://img.shields.io/github/v/tag/BrokenSource/BrokenSource?label=GitHub&color=orange"></a>
    <a href="https://github.com/BrokenSource/Pyaket/stargazers"><img src="https://img.shields.io/github/stars/BrokenSource/Pyaket?label=Stars&style=flat&color=orange"></a>
    <a href="https://discord.gg/KjqvcYwRHm"><img src="https://img.shields.io/discord/1184696441298485370?label=Discord&style=flat&color=purple"></a>
  <br>
  <br>
  <b>
    Links •
    <a href="https://pyaket.dev/get/">Installation</a> •
    <a href="https://pyaket.dev/examples/">Examples</a> •
    <a href="https://pyaket.dev/docs/">Documentation</a> •
    <a href="https://github.com/BrokenSource/Pyaket/issues">Issues</a>
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

<!-- Todo: Demo video here, as always -->

## 🔥 Description

**📦 Pyaket** is a tool that bundles and generates portable executables of your python projects for all platforms. No more convoluted installation steps for casual users, give the comfort [they want](https://github.com/sherlock-project/sherlock/issues/2011) with maximum compatibility and ease of use compared to alternative solutions.

<small>✨ It's the solution you've been dreaming of, but never knew you needed!</small>

- [x] ⚡️ **Lightning fast** installation that automatically manages python, virtual environments, and dependencies without user intervention that just works.
- [x] ♻️ **Cross compile** _from any_ platform _to any_ platform and architecture, no docker or virtual machines needed, see the table below for details!
- [x] 🧠 **Intelligently** reinstalls itself when the executable changes or partial installs, making iterative development easy and safe against users
- [x] 🎩 **Free to use** for open source projects that distributes releases at no cost, get a cheap [sponsor](https://github.com/sponsors/Tremeschin) tier to sell users convenience otherwise!
- [x] 🔦 **PyTorch** installation at runtime, automatic backend detection (optional). [#](https://pyaket.dev/docs/rust/#torch-backend)
- [ ] 📦 **Standalone** executables with no network calls at runtime that bundles all dependencies [#](https://github.com/BrokenSource/Pyaket/issues/2)
- [x] 🚀 **Monorepo** support in mind, decoupled dependencies and entry point specification
- [x] 🧀 **Rolling** releases where a single binary always runs latest pypi or git branch/tag [#](https://pyaket.dev/docs/rust/#rolling)

## ⚔️ Cross compilation

Thanks to Rust's amazing toolchain, coupled with [cargo-zigbuild](https://github.com/rust-cross/cargo-zigbuild), and using pure crates, Pyaket can pretty much compile executables _from any_ platform _to any_ platform without docker or vms.

<br>

<div align="center" markdown>
  <b>Cross compilation compatibility</b>

  | From / To | <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/linux.svg" width="70"> <p> N/A | <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/apple.svg" width="70"> <p> N/A | <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/windows.svg" width="70"> <p> GNU| <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/windows.svg" width="70"> <p> MSVC |
  | :----------------- | :---------------- | :---------------- | :----------------- | :---------------- |
  | 🐧 **Linux** x86   | ✅ x86 <p> ☑️ Arm | ☑️ x86 <p> ☑️ Arm | ✅ x86 <p> ☑️ Arm | 🚫 x86 <p> 🚫 Arm |
  | 🐧 **Linux** Arm   | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | 🚫 x86 <p> 🚫 Arm |
  | 💠 **Windows** x86 | ✅ x86 <p> ☑️ Arm | ☑️ x86 <p> ☑️ Arm | ✅ x86 <p> ☑️ Arm | ✅ x86 <p> 🤏 Arm |
  | 💠 **Windows** Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm |
  | 🍎 **MacOS** x86   | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | 🚫 x86 <p> 🚫 Arm |
  | 🍎 **MacOS** Arm   | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | 🚫 x86 <p> 🚫 Arm |

  <sup><b>Note:</b> The table simply states if it <i>compile and/or run</i>. Your Python project may not work on all platforms.</sup>
</div>

**Legend:**

- ✅ Verified and supported
- ☑️ Compiled, but untested
- ✔️ Should work, untested
- 🚫 Impractical

## 📦 Installation

> [!WARNING]
> This project is under active development, certain parts are incomplete and not fully tested yet.
>
> - Install with `pip install git+https://github.com/BrokenSource/Pyaket` for now!

Head out to the [**website**](https://pyaket.dev/get) for the latest installation instructions and more!

<!-- Todo: Website screenshot, as always -->

## 💰 Commercial

Pyaket is free to use for open source projects that distributes releases at no cost.

Commercial usage (including selling executables, for-profit deployments) or bundling proprietary software requires an appropriate [sponsorship tier](https://github.com/sponsors/Tremeschin). You may freely evaluate the viability beforehand, or use it to get started at a limited budget. Fair and enables me to keep the project alive and improve it over time.

Get in touch if you have any questions, need support or features, or want a custom agreement!

## ♻️ Community

<small>✅ **Be featured here** if you're using Pyaket in your projects!</small>

_🌵 Such an empty place here, for now.._
