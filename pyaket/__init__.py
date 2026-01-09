# Maturin shared library
from ._pyaket import *

# pyright: reportUndefinedVariable=false
__doc__ = _pyaket.__doc__

if hasattr(_pyaket, "__all__"):
    __all__ = _pyaket.__all__

# ---------------------------------------------------------------------------- #

import os
from pathlib import Path

PACKAGE: Path = Path(__file__).parent.resolve()
"""Path to the pyaket package root"""

# Warn: Must export for the rust packer
os.environ["PYAKET_ROOT"] = str(PACKAGE)

# ---------------------------------------------------------------------------- #

def packer(*args: str) -> None:
    return _pyaket.cli(*args)
