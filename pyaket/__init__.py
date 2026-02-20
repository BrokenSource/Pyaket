from dearlog import logger  # isort: split

from importlib.metadata import metadata

__meta__:   dict = metadata(__package__)
__about__:   str = __meta__.get("Summary")
__author__:  str = __meta__.get("Author")
__version__: str = __meta__.get("Version")

import contextlib
import os
from pathlib import Path

package: Path = Path(__file__).parent.resolve()
"""Path to the pyaket python package"""

manifest: Path = (package/"Cargo.toml")
"""Path to pyaket's rust cargo manifest"""

resources: Path = (package/"resources")
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
    _package = Path(ziglang.__file__).parent
    os.environ["PATH"] += f"{os.pathsep}{_package}"
