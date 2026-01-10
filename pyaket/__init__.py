import importlib.metadata
import os
import site
from pathlib import Path

__version__ = importlib.metadata.version(__package__)

PYAKET_PATH: Path = Path(__file__).parent.resolve()
"""Path to the pyaket python package"""

from pyaket.project import PyaketProject

# Ensure zig binary can be found for zigbuild
for path in map(Path, site.getsitepackages()):
    os.environ["PATH"] += f"{os.pathsep}{path/'ziglang'}"
