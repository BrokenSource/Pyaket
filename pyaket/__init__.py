import importlib.metadata
import site
from pathlib import Path

from broken.envy import Environment
from broken.project import BrokenProject

__version__ = importlib.metadata.version(__package__)

PYAKET_ABOUT = "📦 Easy Python to Fast Executables"

PYAKET = BrokenProject(
    PACKAGE=__file__,
    APP_NAME="Pyaket",
    ABOUT=PYAKET_ABOUT,
)

from pyaket.project import PyaketProject

# ---------------------------------------------------------------------------- #

# Ensure zig binary can be found for zigbuild
for path in map(Path, site.getsitepackages()):
    Environment.add_to_path(path/"ziglang")
