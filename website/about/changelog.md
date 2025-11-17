---
icon: material/file-document-edit
---

<style>
    li {margin-bottom: 2px !important;}
    p  {margin-bottom: 2px !important;}
</style>

### ✏️ v0.10.0 <small>Unreleased</small> {#0.10.0}

!!! quote ""
    - Project version is now decoupled and independent from the monorepo
    - Develop and use [rustbin](https://github.com/BrokenSource/Rustbin) - fastest rustup shims provider
    - Use [uv](https://github.com/astral-sh/uv) directly as a crate dependency instead of managing a download externally
        - This severely improves the resiliency and maintainability of the project
        - Compilation is now trickier and slower, but well worth it
    - Port the website to [Zensical](https://zensical.org) over [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)

### 📦 v0.9.0 <small>June 2, 2025</small> {#0.9.0}

!!! success ""
    - Initial version, will match the monorepo due heavy integration and use of already existing infrastructure
    - Basic feature set supported as seen on the readme
