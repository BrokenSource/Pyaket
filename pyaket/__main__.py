import sys

import pyaket


def packer() -> None:
    pyaket.packer(*sys.argv[1:])
