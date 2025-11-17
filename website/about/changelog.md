---
icon: material/file-document-edit
---

### ✏️ v0.10.0 <small>Unreleased</small> {#v0.10.0}

!!! quote ""
    - Project version is now decoupled and independent from the monorepo
    - Create and use [rustbin](https://github.com/BrokenSource/Rustbin) - the fastest rustup shims provider, written in rust
    - Use [uv](https://github.com/astral-sh/uv) directly as a crate dependency instead of managing a download externally
        - This severely improves the resiliency and maintainability of the project
        - Pure-rust releases are halted until uv is available on the registry
    - Port the website to [Zensical](https://zensical.org) over [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)

### 📦 v0.9.0 <small>June 2, 2025</small> {#v0.9.0}

!!! success ""
    - Initial version, will match the monorepo due heavy integration and use of already existing infrastructure
    - Basic feature set supported as seen on the readme
