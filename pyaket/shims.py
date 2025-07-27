import os
import shutil
import subprocess
import sys
from typing import NoReturn


def _shim(proxy: str) -> NoReturn:
    rustup = shutil.which("rustup")
    args = (proxy, *sys.argv[1:])

    if (os.name == "nt"):
        sys.exit(subprocess.run(
            executable=rustup,
            args=args,
        ).returncode)

    os.execv(rustup, args)

def init() -> NoReturn:
    _shim("rustup-init")

def cargo() -> NoReturn:
    _shim("cargo")

def cargo_clippy() -> NoReturn:
    _shim("cargo-clippy")

def cargo_fmt() -> NoReturn:
    _shim("cargo-fmt")

def cargo_miri() -> NoReturn:
    _shim("cargo-miri")

def clippy_driver() -> NoReturn:
    _shim("clippy-driver")

def rls() -> NoReturn:
    _shim("rls")

def rust_analyzer() -> NoReturn:
    _shim("rust-analyzer")

def rust_gdb() -> NoReturn:
    _shim("rust-gdb")

def rust_gdbgui() -> NoReturn:
    _shim("rust-gdbgui")

def rust_lldb() -> NoReturn:
    _shim("rust-lldb")

def rustc() -> NoReturn:
    _shim("rustc")

def rustdoc() -> NoReturn:
    _shim("rustdoc")

def rustfmt() -> NoReturn:
    _shim("rustfmt")
