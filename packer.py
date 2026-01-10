from pyaket import PyaketProject

project = PyaketProject.from_toml("pyaket.toml")
project.python.version = "3.14"
project.compile()
