---
icon: material/tag-multiple-outline
---

Many [:simple-rust: Build Profiles](https://github.com/BrokenSource/Pyaket/blob/main/pyaket/Cargo.toml) are defined to optimize for different use cases.

## Flowchart

As a general rule of thumb for what [option](#options) to use, you can follow:

```mermaid
graph LR
    Start((**Start**)) --> Release("`
        Final Release?
        <small>(Slow compilation)</small>
    `")
    Release --> |No| UseDevelop([_develop_])
    Release --> |Yes| Flavor(Optimizing for)
    Flavor --> |Speed| Speed("`
        Best size and speeds?
        <small>(slower compilation)</small>
    `")
    Flavor --> |Size| Size("`
        Smallest binary
        <small>(slower compilation)</small>
    `")
    Speed --> |No| UseFast([_fast_])
    Speed --> |Yes| UseFastest([_fastest_])
    Size --> |No| UseSmall([_small_])
    Size --> |Yes| UseSmallest([_smallest_])
```

<!-- Todo: Better wording, presentation, visual clutter -->

## Options

### `develop`

Development mode, ideal for iterative development.

<div class="grid cards" markdown>
- 🟢 **Strengths**
    - Iterative development
    - Fastest build times
- 🔴 **Trade-offs**
    - Larger binary size
    - Slower runtime
</div>

### `fast`

Optimizes for speed, similar to rust's default `release` profile.

<div class="grid cards" markdown>
- 🟢 **Strengths**
    - Balanced binary size
    - Fast execution speed
- 🔴 **Trade-offs**
    - Slower build times
</div>

### `fastest`

Same as [fast](#fast), but with [Fat LTO](https://doc.rust-lang.org/cargo/reference/profiles.html#lto) enabled, vs it:

<div class="grid cards" markdown>
- 🟢 **Strengths**
    - Slightly smaller binaries
    - Slightly faster binaries
- 🔴 **Trade-offs**
    - Slowest build times
</div>

### `small`

Optimizes for smaller binary sizes.

<div class="grid cards" markdown>
- 🟢 **Strengths**
    - Smaller binary sizes
- 🔴 **Trade-offs**
    - Slower build times
    - Slower execution speed
</div>

### `smallest`

Same as [small](#small), but with [Fat LTO](https://doc.rust-lang.org/cargo/reference/profiles.html#lto) enabled, vs it:

<div class="grid cards" markdown>
- 🟢 **Strengths**
    - Smallest binary sizes
- 🔴 **Trade-offs**
    - Slowest build times
</div>

## Using a profile

=== ":simple-python: Python"
    ```python
    project.release.profile = "fast"
    ```

=== ":fontawesome-solid-terminal: Command"
    ```bash
    pyaket release --profile fast
    ```

=== ":simple-rust: Rust"
    ```bash
    cargo build --profile fast
    ```


