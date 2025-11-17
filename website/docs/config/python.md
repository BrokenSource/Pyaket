---
icon: material/language-python
---

## Python {#python}

:material-arrow-right: This section is about the Python interpreter to be used at runtime.

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>PYAKET_PYTHON_VERSION</kbd> {#python-version}
> 📦 <b>Type:</b> Version string • <b>Default:</b> 3.13

The version of Python to be used at runtime, from [astral-sh/python-build-standalone](https://github.com/astral-sh/python-build-standalone/).

- **Note**: Specific versions support, such as `3.10.17`, depends on the [uv-version](#uv-version) in use, as the URLs are hard-coded in their binary. For example, `3.13.3` was added in [v0.6.14](https://github.com/astral-sh/uv/releases/tag/0.6.14).

- Please chose carefully to ensure all your wheels and dependencies are compatible with the target version. Users may not have compilers and headers for sdists.

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>PYAKET_PYTHON_BUNDLE</kbd> {#python-bundle}
> 📦 <b>Type:</b> Bool • <b>Default:</b> False

Whether to embed the python distribution in the executable, instead of a runtime download.

Having this enabled increases binary size by roughly 20 MB, but greatly increases reliability and improves first startup times. However, it may trigger antivirus heuristics on giving false positives, as it is a sketchy thing to include archives and decompressors in a binary - this is mostly a non-issue Windows only moment. Disabled by default for easy to share small executables.

<small><b>⚠️ Warning:</b> This feature is not yet implemented</small>
