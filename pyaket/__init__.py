import importlib.metadata
import os
import site
from pathlib import Path

__version__ = importlib.metadata.version(__package__)

PYAKET_ROOT: Path = Path(__file__).parent.resolve()
"""Path to the pyaket python package"""

PYAKET_CARGO: Path = (PYAKET_ROOT/"Cargo.toml")
"""Path to pyaket's rust cargo manifest"""

from pyaket.project import (
    PyaketApplication,
    PyaketDependencies,
    PyaketDirectories,
    PyaketEntry,
    PyaketProject,
    PyaketPython,
    PyaketRelease,
    PyaketTorch,
)

# Ensure zig binary can be found for zigbuild
for path in map(Path, site.getsitepackages()):
    os.environ["PATH"] += f"{os.pathsep}{path/'ziglang'}"
