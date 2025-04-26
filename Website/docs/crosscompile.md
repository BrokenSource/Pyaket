
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
