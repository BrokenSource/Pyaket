---
icon: material/git
---

You can install latest pyaket git as a package:

```sh title="Command"
$ pip install git+https://github.com/BrokenSource/Pyaket
```

Or add into your `pyproject.toml`:

```toml title="pyproject.toml"
[project]
dependencies = [
    "pyaket @ git+https://github.com/BrokenSource/Pyaket",
    # ...
]
```
