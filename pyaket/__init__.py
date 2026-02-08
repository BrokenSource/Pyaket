from dearlog import logger  # isort: split

import contextlib
import sys

__version__: str = "0.10.0"
__author__:  str = "Tremeschin"
__about__:   str = "📦 Easy Python to Fast Executables"

# Simple and early version flag
with contextlib.suppress(IndexError):
    if sys.argv[1] in ("--version", "-v"):
        print(__version__)
        sys.exit(0)

import os
from pathlib import Path

PYAKET_ROOT: Path = Path(__file__).parent.resolve()
"""Path to the pyaket python package"""

PYAKET_CARGO: Path = (PYAKET_ROOT/"Cargo.toml")
"""Path to pyaket's rust cargo manifest"""

PYAKET_RESOURCES: Path = (PYAKET_ROOT/"resources")
"""Path to pyaket's resources directory"""

from pyaket.project import (
    CargoProfile,
    CargoWrapper,
    PyaketApplication,
    PyaketBuild,
    PyaketDependencies,
    PyaketDirectories,
    PyaketEntry,
    PyaketProject,
    PyaketPython,
    PyaketTorch,
)
from pyaket.targets import Target

# Ensure ziglang binary can be found
with contextlib.suppress(ImportError):
    import ziglang
    _ziglang = Path(ziglang.__file__).parent
    os.environ["PATH"] += f"{os.pathsep}{_ziglang}"
