import os
import shutil
import subprocess
import sys

# ------------------------------------------------------------------------------------------------ #

def _shim(proxy: str) -> None:
    rustup = shutil.which("rustup")
    args = (proxy, *sys.argv[1:])

    if (os.name == "nt"):
        sys.exit(subprocess.run(
            executable=rustup,
            args=args,
        ).returncode)

    os.execv(rustup, args)

# ------------------------------------------------------------------------------------------------ #

def init() -> None:
    _shim("rustup-init")

def cargo() -> None:
    _shim("cargo")

def cargo_clippy() -> None:
    _shim("cargo-clippy")

def cargo_fmt() -> None:
    _shim("cargo-fmt")

def cargo_miri() -> None:
    _shim("cargo-miri")

def clippy_driver() -> None:
    _shim("clippy-driver")

def rls() -> None:
    _shim("rls")

def rust_analyzer() -> None:
    _shim("rust-analyzer")

def rust_gdb() -> None:
    _shim("rust-gdb")

def rust_gdbgui() -> None:
    _shim("rust-gdbgui")

def rust_lldb() -> None:
    _shim("rust-lldb")

def rustc() -> None:
    _shim("rustc")

def rustdoc() -> None:
    _shim("rustdoc")

def rustfmt() -> None:
    _shim("rustfmt")
