import sys

def main():
    from pyaket import PyaketProject
    pyaket = PyaketProject()
    pyaket.cli(*sys.argv[1:])

if __name__ == "__main__":
    main()
