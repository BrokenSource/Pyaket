import sys

import pyaket


def packer():
    pyaket.packer(*sys.argv[1:])
