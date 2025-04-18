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
    <a href="https://pyaket.dev/docs/">📦 Documentation</a> •
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

<!-- Todo: Demo video here, as always -->

## 🔥 Description

**Pyaket** bundles and generates portable executables of your Python projects for all platforms!

- [x] **Fast** and portable executables for your python projects,

- [x] **First class** monorepo support • bundle all your wheels to be installed at runtime

<!--
(Powered by uv and rust - fast)
(Multiple platforms supported)
(First class monorepo support)
(Bundling wheels to the project)
(Offline executables are planned)
(Smart detects partial installs)
(Easy uninstallation, version management)
(Common directory for multiple releases)
-->

## ⚔️ Cross compilation

Thanks to Rust's amazing toolchain, coupled with [cargo-zigbuild](https://github.com/rust-cross/cargo-zigbuild), and using only pure Rust crates, Pyaket can pretty much compile executables _from any_ platform _to any_ platform, no Docker or Virtual Machines required!

- The table below shows known status of each combinations:

<br>

<div align="center" text-align="left">
  <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/linux.svg"   width="60">
  <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/apple.svg"   width="60">
  <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/windows.svg" width="60">

  | From / To       | Linux             | MacOS             | Win GNU            | Win MSVC          |
  | :-------------- | :---------------- | :---------------  | :----------------  | :---------------  |
  | **Windows x86** | ✅ x86 <p> ☑️ Arm | ☑️ x86 <p> ☑️ Arm | ✅ x86 <p> ☑️ Arm | ✅ x86 <p> ⚠️ Arm |
  | **Windows Arm** | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm |
  | **Linux x86**   | ✅ x86 <p> ☑️ Arm | ☑️ x86 <p> ☑️ Arm | ✅ x86 <p> ☑️ Arm | 🚫 x86 <p> 🚫 Arm |
  | **Linux Arm**   | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | 🚫 x86 <p> 🚫 Arm |
  | **MacOS x86**   | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | 🚫 x86 <p> 🚫 Arm |
  | **MacOS Arm**   | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | 🚫 x86 <p> 🚫 Arm |

</div>

**Legend:**
- ✅ Verified and supported
- ☑️ Compiled, untested
- ✔️ Should work, untested
- ⚠️ Almost compiled
- 🚫 Impractical
- ❓ Unknown

<sup><b>Note:</b> The table says if it simply <i>compiles</i>, your Python project may not work on all platforms.</sup>

## 📦 Installation

Head out to the [**website**](https://pyaket.dev/get) for the latest installation instructions and more!

<!-- Todo: Website screenshot, as always -->

## 💰 Commercial

Pyaket is free to use for Open Source projects and non-commercial purposes. Commercial usage (including selling executables, for-profit deployments) or bundling proprietary software requires an appropriate [sponsorship tier](https://github.com/sponsors/Tremeschin), you may freely evaluate the viability beforehand. Get in touch if the pricing is not suitable for you, new features and support, or altruistic reasons!

## ♻️ Community

<small>✅ **Be featured here** if you're using Pyaket in your projects!</small>

_🌵 Such an empty place here, for now.._
