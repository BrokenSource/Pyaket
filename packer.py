from pyaket import PyaketProject, Target
import pyaket

for target in Target.recommended():
    project = PyaketProject()
    project.app.name      = "Pyaket"
    project.app.author    = "BrokenSource"
    project.app.about     = pyaket.__about__
    project.app.version   = pyaket.__version__
    project.entry.module  = pyaket.__package__
    project.build.target  = target
    project.build.profile = "smallest"
    project.compile()
