---
icon: material/git
---

## Directly

You can install the latest git repository code as a package:

```sh title="🔴🟡🟢 Command" linenums="1"
pip install git+https://github.com/BrokenSource/Pyaket
```

Or even better, using [uv](https://docs.astral.sh/uv/) • [tools](https://docs.astral.sh/uv/guides/tools/) ephemeral environment:

```sh title="🔴🟡🟢 Command" linenums="1"
uvx --from git+https://github.com/BrokenSource/Pyaket pyaket (...)
```

## Dependency

You can add it to your development dependencies:

```toml title="pyproject.toml" linenums="1"
[dependency-groups]
dev = ["pyaket @ git+https://github.com/BrokenSource/Pyaket"]
```

Run commands within an activated environment or import on scripts as usual.
