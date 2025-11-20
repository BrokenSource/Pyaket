---
icon: octicons/package-16
---

## **Q:** How it works {#how-it-works}

Pyaket is highly inspired by [PyApp](https://github.com/ofek/pyapp), with opinionated and idiosyncratic design choices that makes it easier to use and understand, with improved resiliency, speeds, monorepo support, and a cli.

In short, the rust language supports [build scripts](https://doc.rust-lang.org/cargo/reference/build-scripts.html) that runs before the compilation of the main program, allowing us to process and pass a configuration from environment variables to the final release. At runtime, download [uv](https://docs.astral.sh/uv) and/or a [python-distribution](https://github.com/astral-sh/python-build-standalone/) archive (or pre-bundle it alongside wheels with [rust-embed](https://crates.io/crates/rust-embed)), create a venv, install dependencies, run the project with incoming argv.

- This guarantees _maximum compatibility_ with how the project is run on the user's machine, as we're doing the same steps an experienced python user would do with native tools.
- There is little runtime overhead, mostly checking if the project is already installed and files are properly unpacked, then calling a python interpreter child process.

There are lots of configuration options in the documentation.
