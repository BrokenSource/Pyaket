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

!!! tip "**Suggestion:** Use smallest for releases, and develop for local testing."

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

<!-- Note: Feel free to run scripts/benchmark-profile.py and submit results! -->

- **Size:** Base compiled binary size, only including the uv runtime.
- **Overhead:** Startup overhead time added by Pyaket until Python runs an empty command.
- **Cold build:** Time to build without any prior build cache.
- **Rebuild:** Time to rebuild after a prior build cache exists.

### x86_64-unknown-linux-gnu

| Profile    | Size     | Startup | Cold    | Warm    |
| :--------- | --------:| ------: | ------: | ------: |
| develop  | 59.03 MB | 93.3 ms |  70.2 s |   9.3 s |
| fast     | 45.44 MB | 32.2 ms | 166.0 s | 108.0 s |
| fastest  | 40.70 MB | 31.0 ms | 274.0 s | 212.0 s |
| small    | 37.23 MB | 34.8 ms | 104.0 s |  61.0 s |
| smallest | 29.94 MB | 33.4 ms | 180.0 s | 136.0 s |

<sup><b>System:</b> Ryzen 9 5900X, 2x3200 MT/s DDR4 CL16 2Rx8<sup>
