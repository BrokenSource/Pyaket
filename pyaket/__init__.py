import time

if not hasattr(time, "start"):
    time.start = time.perf_counter()

import contextlib
import sys

__version__: str = "0.10.0"
__author__:  str = "Tremeschin"

# Simple and early version flag
with contextlib.suppress(IndexError):
    if sys.argv[1] in {"--version", "-v"}:
        print(__version__)
        sys.exit(0)

import os
import subprocess
from pathlib import Path

PYAKET_ROOT: Path = Path(__file__).parent.resolve()
"""Path to the pyaket python package"""

PYAKET_CARGO: Path = (PYAKET_ROOT/"Cargo.toml")
"""Path to pyaket's rust cargo manifest"""

HOST_TRIPLE: str = subprocess.run(
    ("rustc", "--print", "host-tuple"),
    capture_output=True, text=True
).stdout.strip()
"""The host platform rust target triple"""

import structlog

logger = structlog.get_logger(__package__)

from pyaket.project import (
    PyaketApplication,
    PyaketBuild,
    PyaketDependencies,
    PyaketDirectories,
    PyaketEntry,
    PyaketProject,
    PyaketPython,
    PyaketTorch,
)

# Ensure ziglang binary can be found
with contextlib.suppress(ImportError):
    import ziglang
    _ziglang = Path(ziglang.__file__).parent
    os.environ["PATH"] += f"{os.pathsep}{_ziglang}"
