---
icon: material/folder-outline
---

## Directories {#dirs}

:material-arrow-right: Directories used by Pyaket to store the application data.

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>WORKSPACE</kbd> {#workspace}
> 📦 <b>Type:</b> Path • <b>Default:</b> Dynamic

The workspace root directory Pyaket will use for the project.

This is a special variable that can be overriden at runtime and is dynamic if unset. By default, Pyaket uses proper and intended platform directories to store the application data:

!!! tip ""
    <table markdown>
        <tbody class="slim-table">
            <tr>
                <td style="width: 20%">:material-microsoft: Windows</td>
                <td><kbd>C:\\Users\\User\\AppData\\Local\\Author</kbd></td>
            </tr>
            <tr>
                <td>:simple-apple: MacOS</td>
                <td><kbd>~/Library/Application Support/Author</kbd></td>
            </tr>
            <tr>
                <td>:simple-linux: Linux</td>
                <td><kbd>~/.share/Author</kbd></td>
            </tr>
        </tbody>
    </table>

Shall a user set it, the value is used as is. This is especially useful if folks have a full C:\\ drive or want a custom directory than the above for large application data. A Python project should follow the same pattern, so all files are in the same place for easier uninstallation.

```sh title="Example"
$ export WORKSPACE="/tmp/workspace"
$ ./pyaket-project.bin
```

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>PYAKET_COMMON_DIR</kbd> {#common-dir}
> 📦 <b>Type:</b> Path • <b>Default:</b> Pyaket

The subdirectory of the [workspace](#workspace) to use for all Pyaket installation and runtime files.

By default, things are stored in a `Pyaket` directory (due lack of a better name). All other internal directories derives from this one. It can be left empty if you'll not use platformdirs yourself.

!!! tip ""
    <table markdown>
        <tbody class="slim-table">
            <tr>
                <td style="width: 20%">:material-microsoft: Windows</td>
                <td><kbd>C:\\Users\\User\\AppData\\Local\\Author\\Pyaket</kbd></td>
            </tr>
            <tr>
                <td>:simple-apple: MacOS</td>
                <td><kbd>~/Library/Application Support/Author/Pyaket</kbd></td>
            </tr>
            <tr>
                <td>:simple-linux: Linux</td>
                <td><kbd>~/.share/Author/Pyaket</kbd></td>
            </tr>
            <tr>
                <td style="width: 20%">:material-cube: Custom</td>
                <td><kbd>Workspace/Pyaket</kbd></td>
            </tr>
        </tbody>
    </table>

You may find the following directories inside the composition:

- **Astral**: Stores uv versions, archives and unpacked files.
- **Cache**: Used for `UV_CACHE_DIR`, primarily package download caches.
- **Python**: Stores multiple versions of Python distributions.
- **Versions**: See [versions dir](#versions-dir) for more details.

<!------------------------------------------------------------------------------------------------->
<hr>

### <kbd>PYAKET_VERSIONS_DIR</kbd> {#versions-dir}
> 📦 <b>Type:</b> String • <b>Default:</b> Versions

The subdirectory of the [common](#common-directory) directory to install the virtual environments.

Multiple versions of the same application(s) are stored in a shared directory (venv). From the table below, `(...)` is replaced with the [version](#app-version), yielding the full installation path.

!!! tip ""
    <table markdown>
        <tbody class="slim-table">
            <tr>
                <td style="width: 20%">:material-microsoft: Windows</td>
                <td><kbd>C:\\Users\\User\\AppData\\Local\\Author\\Pyaket\\Versions\\(...)</kbd></td>
            </tr>
            <tr>
                <td>:simple-apple: MacOS</td>
                <td><kbd>~/Library/Application Support/Author/Pyaket/Versions/(...)</kbd></td>
            </tr>
            <tr>
                <td>:simple-linux: Linux</td>
                <td><kbd>~/.share/Author/Pyaket/Versions/(...)</kbd></td>
            </tr>
            <tr>
                <td style="width: 20%">:material-cube: Custom</td>
                <td><kbd>Workspace/Pyaket/Versions/(...)</kbd></td>
            </tr>
        </tbody>
    </table>

- **Note**: Applications of an author that shares the same versions dir **must** be coupled together. If they are independent, a workaround is to set this value to `Versions/<app_name>`, so each application have a separate versions directory. Default is shared for monorepos in mind.
