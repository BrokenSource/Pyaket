---
icon: material/git
---

## Directly

You can install the latest pyaket code as a package:

```sh
pip install git+https://github.com/BrokenSource/Pyaket
```

## Dependency

Add into your `pyproject.toml`:

```toml title="pyproject.toml"
[project]
dependencies = [
    "pyaket @ git+https://github.com/BrokenSource/Pyaket",
    # ...
]
```
