# Examples

!!! warning "Work in Progress"
    Section yet to be actually written 😉

📦 Pyaket's configuration is done via environment variables read by rust at compile time, which are processed and passed through to the executable to load at runtime.

```python
from pyaket import PyaketProject, Target

for target in Target.recommended():
    project = PyaketProject()

    project.app.name   = "MyApp"
    project.app.author = "MyName"

    project.python.version = "3.13"
    project.deps.pypi.append("numpy")
    project.deps.wheels.append("./dist/project-0.0.1-py3-none-any.whl")

    project.build.target = target
    project.entry.module = "myapp.main"

    executable = project.compile()
```

**Note:** It's recommended to always recreate a `PyaketProject` class for each build.



### Simple to use

Compile a [cowsay](https://pypi.org/project/cowsay/) binary for the current platform and run it:

```sh hl_lines="1"
$ pyaket app --name cowsay dep --pypi "cowsay==6.1" run --module cowsay compile
  Compiling libc v0.2.172
  Compiling typenum v1.18.0
  ...
  Finished `release` profile [optimized] target(s) in 9.88s
```

```sh hl_lines="1"
$ ./release/cowsay-v0.0.0-x86_64-unknown-linux-gnu -t "Hello, Pyaket!"
  ______________
| Hello, Pyaket! |
  ==============
     \
      \
        ^__^
        (oo)\_______
        (__)\       )\/\
            ||----w |
            ||     ||
```

### Blazingly fast

after the first installation:

```sh hl_lines="1 5"
$ hyperfine "./release/cowsay-v0.0.0-x86_64-unknown-linux-gnu -t anyhow"
  Time (mean ± σ):      23.3 ms ±   0.3 ms    [User: 15.8 ms, System: 7.2 ms]
  Range (min … max):    22.9 ms …  24.8 ms    100 runs

$ hyperfine "python -m cowsay -t anyhow"
  Time (mean ± σ):      18.5 ms ±   0.1 ms    [User: 14.2 ms, System: 4.1 ms]
  Range (min … max):    18.2 ms …  19.0 ms    100 runs
```

<sup><b>Note:</b> The actual benchmark command was `nice -20 taskset -c 2 hyperfine -w 50 -r 100 -N (...)`</sup>

### Cross compile

to most platforms and architectures easily:

```sh hl_lines="2 5"
# Intel Macbook @ ./release/cowsay-v0.0.0-x86_64-apple-darwin
$ pyaket ... build --target x86_64-apple-darwin compile

# Apple Silicon @ ./release/cowsay-v0.0.0-aarch64-apple-darwin
$ pyaket ... build --target aarch64-apple-darwin compile
```

```sh hl_lines="2 5"
# Windows executables compiled from linux, needs a mingw64 toolchain!
$ pyaket ... build -t x86_64-pc-windows-gnu compile
  Finished `release` profile [optimized] target(s) in 8.11s

$ wine ./Release/cowsay-v0.0.0-x86_64-pc-windows-gnu.exe -t "Hello, Wine!"
  ____________
| Hello, Wine! |
  ============
            \
             \
               ^__^
               (oo)\_______
               (__)\       )\/\
                   ||----w |
                   ||     ||
```

### Bundle wheels

and install them at runtime, perfect for monorepos:

```sh hl_lines="1 6"
$ uv build --all-packages --wheel
  Successfully built dist/shared-1.0.0-py3-none-any.whl
  Successfully built dist/project_a-1.0.0-py3-none-any.whl
  Successfully built dist/project_b-1.0.0-py3-none-any.whl

# Both will share the same virtual environment 🤯
# ./release/{project_a,project_b}-v0.0.0-x86_64-unknown-linux-gnu
$ pyaket app -n project_a dep -w "dist/*.whl" run -m project_a compile
$ pyaket app -n project_b dep -w "dist/*.whl" run -m project_b compile
```

### Install pytorch

at runtime, with automatic backend detection:

```sh hl_lines="2 5"
# ./release/app-v0.0.0+auto-unknown-linux-gnu
$ pyaket ... torch -v 2.7.0 -b auto compile

# ./release/app-v0.0.0+cu128-unknown-linux-gnu
$ pyaket ... torch -v 2.7.0 -b cu128 compile
```
