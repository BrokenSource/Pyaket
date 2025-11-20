---
icon: material/road-variant
---

Pyaket is under heavy development and experimentation. Features are being added, changed or removed constantly, as seen in the [changelog](./changelog.md) and [issues](https://github.com/BrokenSource/Pyaket/issues) boards.

!!! tip "Be part of the journey!"
    Your feedback is very important to shape the project. Join the [Community Groups](./contact.md) to ask questions, give suggestions, or report issues directly with the authors, from an end-user or developer perspective!

<small><b>Note:</b> This page may not be up to date with latest changes</small>

## Website

Currently porting over to [Zensical](https://zensical.org/) and improving the documentation.

- [x] **Deployment**: Setup a GitHub Actions workflow to publish the site (you are reading it now!)
- [ ] **Content**: Find a visually pleasing and organized way to present the many options pyaket provides for application, python, torch, directories, etc. configuration.
- [ ] **Examples**: Create a set of examples for common use-cases and configurations.

## Deployment

- [ ] **Build Scripts**: Find a nice way to automate and manage the build pipeline from either a command line interface or a configuration file, most likely a python script itself.
- [ ] **Lockfiles**: Setup a project from locked dependencies file instead of pyproject complexity.
- [ ] **Versioning**: Rethink how to version all projects vs main library and packages.
    - [ ] [**Hook**](https://github.com/BrokenSource/Hook): Make pyaket wheels buildable outside the monorepo

## Easier Compilation

- [ ] **Target MacOS**: Automatically download an SDK and set `SDKROOT` for [`cargo-zigbuild`](https://github.com/rust-cross/cargo-zigbuild) to link against System Foundations and other required libraries, include it by default in Docker images.
- [ ] Figure out and implement [rootless docker](https://docs.docker.com/engine/security/rootless/) for easier use and security.

**Windows**:

- [ ] **MSVC Toolchain**: Automate a [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2026) installation with winget for compiling msvc rust targets, add documentation about it.
- [ ] **MSYS2**: Automate a [MSYS2](https://www.msys2.org/) installation with winget and use [`mingw-w64-ucrt-x86_64-gcc`](https://packages.msys2.org/packages/mingw-w64-ucrt-x86_64-gcc?repo=ucrt64)

