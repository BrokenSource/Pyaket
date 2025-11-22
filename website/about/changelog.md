---
icon: material/file-document-edit
---

<style>
  ul li {
    line-height: 1.1;
  }
</style>

### ✏️ v0.10.0 <small>Unreleased</small> {#v0.10.0}

!!! quote ""
    - Port the website to [Zensical](https://zensical.org) over [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
    - Project version is now decoupled and independent from the monorepo
    - Create and use [rustbin](https://github.com/BrokenSource/Rustbin) - the fastest rustup shims provider, written in rust
    - Use [uv](https://github.com/astral-sh/uv) directly as a [crate](https://crates.io/crates/uv) dependency instead of managing a download externally
        - This severely improves the resiliency and maintainability of the project
        - Pure-rust releases are halted until uv is available on the registry
        - Keeping an [`external-uv`](https://github.com/BrokenSource/Pyaket/tree/external-uv) branch for future reference if needed
    - Sketch compiling with [`cargo-xwin`](https://github.com/rust-cross/cargo-xwin) MSVC targets from non-windows hosts
    - Many `PyaketProject` variables are now safer `Option<String>` and idiomatic
    - Minify the readme, use [mrmarble/termsvg](https://github.com/mrmarble/termsvg) and [screenshot.rocks](https://screenshot.rocks) presentation

### 📦 v0.9.0 <small>June 2, 2025</small> {#v0.9.0}

!!! success ""
    - Initial version, will match the monorepo due heavy integration and use of already existing infrastructure
    - Basic feature set supported as seen on the readme
