import site
from pathlib import Path

from Broken import BrokenProject, Environment, __version__

PYAKET_ABOUT = "📦 Easy Python to → Fast Executables"

PYAKET = BrokenProject(
    PACKAGE=__file__,
    APP_NAME="Pyaket",
    APP_AUTHOR="BrokenSource",
    ABOUT=PYAKET_ABOUT,
)

from Pyaket.Project import PyaketProject

# ------------------------------------------------------------------------------------------------ #

# Ensure zig binary can be found
for path in map(Path, site.getsitepackages()):
    Environment.add_to_path(path/"ziglang")

# Ensure rust toolchain can be found
if (_CARGO_HOME := Environment.get("CARGO_HOME")):
    Environment.add_to_path(Path(_CARGO_HOME)/"bin")
else:
    Environment.add_to_path(Path.home()/".cargo"/"bin")
