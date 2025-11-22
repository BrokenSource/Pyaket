---
icon: material/language-rust
---

<!-- Fixme: Should we have this page at all? Advanced usage, lacks automation, no compile caching, shouldn't be used as a dependency.. -->

Pyaket can make executables directly from [crates.io](https://crates.io/) without the python package. For that, most options in the [documentation](../docs/) are exported via environment, then built with [`cargo install`](https://doc.rust-lang.org/cargo/commands/cargo-install.html):

```sh
export PYAKET_APP_NAME="cowsay"
export PYAKET_DEPS_PYPI="cowsay==6.1"
export PYAKET_ENTRY_MODULE="cowsay"
```

```sh
# Compile it from crates.io
cargo install pyaket --locked --force --root ./target

# Find your binary at
./target/bin/pyaket
```
