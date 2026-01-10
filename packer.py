from pyaket import PyaketProject

project = PyaketProject.from_toml("pyaket.toml")
project.compile()
