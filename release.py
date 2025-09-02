import sys

from pyaket import PyaketProject

project = PyaketProject()
project.app.name   = "pyaket"
project.app.author = "brokensource"
project.build(all=True)
# project.app.wheels.append("dist/*.whl")
project.cli(*sys.argv[1:])
