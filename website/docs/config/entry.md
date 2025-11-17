
## Entry Points

:material-arrow-right: This section is about the entry points of the executable run after the installation.

- At least one entry point is required, otherwise it'll boot to the Python shell.
- All incoming args of the executable are passed through to the final command.

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>PYAKET_ENTRY_MODULE</kbd> {#entry-module}
> 📦 <b>Type:</b> String • <b>Default:</b> None

A module's name to be called as `python -m <module> (args)` after installation.

- The file `<module>/__main__.py` must exist, otherwise it will error out.

<small>✅ This is the recommended and reliable way to run your project, have a top-level cli for multiple entries</small>

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>PYAKET_ENTRY_SCRIPT</kbd> {#entry-script}
> 📦 <b>Type:</b> String • <b>Default:</b> None

A local script to be bundled and called as `python <script.py> (args)` after installation.

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>PYAKET_ENTRY_CODE</kbd> {#entry-code}
> 📦 <b>Type:</b> String • <b>Default:</b> None

An inline Python code to be executed as `python -c <code> (args)` after installation.

- Slightly more reliable than an [entry script](#entry-script), as it doesn't write a temp file.
- Less flexible and readable because it must be a single line of code.

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>PYAKET_ENTRY_COMMAND</kbd> {#entry-command}
> 📦 <b>Type:</b> String • <b>Default:f</b> None

A command to be executed as `<command> (args)` after installation.

- The venv is activated and the bin directory is added to PATH, so this can be a script defined in your `pyproject.toml` • `[project.scripts]` section.

It may be used if you have multiple entry points, like `depthflow {main,gradio}`, and want to hardcode pin one to be used, or set fixed arguments to some command.

!!! warning "**Discouraged**: Security implications, man in the middle attack, may use wrong command"
