import sys

from Pyaket import PyaketProject


def main():
    pyaket = PyaketProject()
    pyaket.cli(*sys.argv[1:])

if __name__ == "__main__":
    main()
