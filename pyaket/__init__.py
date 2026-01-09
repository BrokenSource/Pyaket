# pyright: reportUndefinedVariable=false

import os
from pathlib import Path

from ._pyaket import *

PACKAGE: Path = Path(__file__).parent.resolve()
"""Path to the pyaket package root"""

# Warn: Must export for the rust packer
os.environ["PYAKET_ROOT"] = str(PACKAGE)

# ------------------------------------ #

def packer(*args: str) -> None:
    return _pyaket.cli(*args)
