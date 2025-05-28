import site
from pathlib import Path

from broken import BrokenProject, Environment, __version__

PYAKET_ABOUT = "📦 Easy Python to → Fast Executables"

PYAKET = BrokenProject(
    PACKAGE=__file__,
    APP_NAME="Pyaket",
    ABOUT=PYAKET_ABOUT,
)

from pyaket.project import PyaketProject

# ------------------------------------------------------------------------------------------------ #

# Ensure zig binary can be found for zigbuild
for path in map(Path, site.getsitepackages()):
    Environment.add_to_path(path/"ziglang")
