---
icon: material/application-braces-outline
---

# Application

:material-arrow-right: General metadata of the project

### <kbd>PYAKET_APP_NAME</kbd> {#app-name}
> 📦 **Type:** string • **Default:** pyaket

The name of the application being built.

Currently only used for identifying • flagging successfull installations and recreating the virtual environment shall the binary hash changes. This is purely useful for iterative development.

<hr>

### <kbd>PYAKET_APP_AUTHOR</kbd> {#app-author}
> 📦 **Type:** string • **Default:** brokensource

The author's name, group, organization of the application being built.

The value is mostly used for dictating the [workspace](#workspace) root when dynamic. Centralizes installation paths and caches for a given author, while being independent enough to not interfere with others.

<hr>

### <kbd>PYAKET_APP_VERSION</kbd> {#app-version}
> 📦 **Type:** string • **Default:** 0.0.0

The version of the application being built.

Should follow the version of the project to be released alonside a registry itself. Not necessarily a semantic version, can be a codename, branch, latest, etc. Value is added to [versions dir](#versions-dir), building the full installation path of the venv to be used.

To get the current version in python, use:

```python
from importlib.metadata import version as get_version

version = get_version("package")
```

Or better yet, if using [Hatch](https://hatch.pypa.io/latest/)

```python
[tool.hatch.version]
path = "package/version.py"

[project]
dynamic = ["version"]
```

<hr>

### <kbd>PYAKET_APP_ABOUT</kbd> {#app-about}
> 📦 **Type:** string • **Default:** No description provided

A description of the application, exclusively for metadata or banner purposes.

<hr>

### <kbd>PYAKET_APP_ICON</kbd> {#app-icon}
> 📦 **Type:** Path • **Default:** None

