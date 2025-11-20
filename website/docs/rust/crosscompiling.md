---
icon: material/sword-cross
---

Under certain conditions[^conditions], Pyaket automatically uses [cargo-zigbuild](https://github.com/rust-cross/cargo-zigbuild) for an easier and streamlined cross-compilation experience, where [Zig](https://ziglang.org/) is used in the final -- and complex -- linking stage.

[^conditions]: Most often when the target operating system differs from the host one.

- Most of the code is pure-rust, but some crates may depend on specific syscalls or libraries.
- Instructions here only applies for hosts that differ from the target.

!!! tip "Have ziglang installed"
    Simply install `pyaket` with the `zig` dependency group, as in `#!bash pip install pyaket[zig]`

!!! info "Opting out of auto zigbuild"
    Whenever you have compatible tools for a target, you can set  the `#!bash AUTO_ZIGBUILD=0` environment variable to disable the automatic usage of `cargo-zigbuild` (eg. a working `mingw-w64` toolchain)

## Targets

### :simple-apple: MacOS

Compiling to Apple targets requires any of:

- Setting `#!bash SDKROOT=Path` to a MacOS SDK path, like [this one](https://github.com/phracker/MacOSX-SDKs/releases/download/11.3/MacOSX11.3.sdk.tar.xz) (easier).
- Setting `#!bash DEVELOPER_DIR=Path` to an [Xcode](https://developer.apple.com/xcode/) installation.

You're good to go, as simple as that :rocket:

!!! tip "Pyaket [Docker images](../../get/docker.md#section) already includes them! :simple-docker: "

<sup><b>Note:</b> Automatically managing an SDK is tracked in <a href="https://github.com/BrokenSource/Pyaket/issues/17">this issue</a>.</sup>

### :simple-linux: Linux

### :material-microsoft: Windows

#### MinGW

Compiling to a Windows target is easier done via `*-pc-windows-gnu`, which requires a `mingw-w64` toolchain

- :simple-apple: Install the [mingw-w64](https://formulae.brew.sh/formula/mingw-w64) homebrew package.
- :simple-archlinux:

#### MSVC

!!! example "Experimental"
    It may be possible to use [`cargo-xwin`](https://github.com/rust-cross/cargo-xwin) to build MSVC binaries from non-windows hosts, tracked in [#18](https://github.com/BrokenSource/Pyaket/issues/18).

## Compatibility table

Thanks to Rust's amazing toolchain, coupled with [cargo-zigbuild](https://github.com/rust-cross/cargo-zigbuild), and using pure crates, Pyaket can pretty much compile executables _from any_ platform _to any_ platform without docker or vms.

<div align="center" markdown>
  | From / To | <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/linux.svg" width="70"> <p> N/A | <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/apple.svg" width="70"> <p> N/A | <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/windows.svg" width="70"> <p> GNU| <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/windows.svg" width="70"> <p> MSVC |
  | :----------------- | :---------------- | :---------------- | :----------------- | :---------------- |
  | 🐧 **Linux** x86   | ✅ x86 <p> ☑️ Arm | ☑️ x86 <p> ☑️ Arm | ✅ x86 <p> ❌ Arm | 🚫 x86 <p> 🚫 Arm |
  | 🐧 **Linux** Arm   | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❌ Arm | 🚫 x86 <p> 🚫 Arm |
  | 💠 **Windows** x86 | ✅ x86 <p> ☑️ Arm | ☑️ x86 <p> ☑️ Arm | ✅ x86 <p> ☑️ Arm | ✅ x86 <p> 🤏 Arm |
  | 💠 **Windows** Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm | ❓ x86 <p> ❓ Arm |
  | 🍎 **MacOS** x86   | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | 🚫 x86 <p> 🚫 Arm |
  | 🍎 **MacOS** Arm   | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | ✔️ x86 <p> ✔️ Arm | 🚫 x86 <p> 🚫 Arm |

  <sup><b>Note:</b> The table simply states if it <i>compile and/or run</i>. Your Python project may not work on all platforms.</sup>
</div>

- ✅ Verified and supported
- ☑️ Compiled, but untested
- ✔️ Should work (untested)
- ❌ Impractical (possible)
- 🚫 Impossible
