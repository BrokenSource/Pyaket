---
icon: material/tag-multiple-outline
---

Many [:simple-rust: Build Profiles](https://doc.rust-lang.org/cargo/reference/profiles.html) are defined to optimize for different use cases.

## Flowchart

As a general rule of thumb for what option to use, you can follow:

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

!!! tip "**Suggestion:** Always use smallest for releases, plenty fast and portable 😉"

## Usage

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

## Benchmarks

<!-- Note: Feel free to run scripts/benchmark-profiles.py and submit results! -->

Tests are made with this [script](https://github.com/BrokenSource/Pyaket/blob/main/scripts/benchmark-profiles.py), measuring:

- **Size:** Base compiled binary size, only including the uv runtime.
- **Startup:** Overhead until the python interpreter is called[^startup].
- **Cold:** Time to build without any prior cargo build cache.
- **Warm:** Time to rebuild after a prior cargo build cache exists.

[^startup]: Difference between system's `python -c ''` and `pyaket -c ''`

### x86_64-unknown-linux-gnu

| Profile  | Size     | Startup | Cold    | Warm    |
| :------- | -------: | ------: | ------: | ------: |
| develop  | 59.03 MB | 32.2 ms |  65.7 s |   8.7 s |
| fast     | 45.10 MB | 25.1 ms | 158.3 s | 100.7 s |
| fastest  | 40.54 MB | 24.1 ms | 255.2 s | 198.7 s |
| small    | 36.87 MB | 28.2 ms |  98.8 s |  57.1 s |
| smallest | 29.74 MB | 26.0 ms | 170.0 s | 132.3 s |

<sup><b>System:</b> Ryzen 9 5900X, 2x3200 MT/s DDR4 CL16 2Rx8<sup>
