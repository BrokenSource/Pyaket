from pyaket import (
    PyaketProject,
    Target,
    __about__,
    __version__,
)

for target in Target.recommended():
    project = PyaketProject()
    project.app.name      = "Pyaket"
    project.app.author    = "BrokenSource"
    project.app.about     = __about__
    project.app.version   = __version__
    project.build.target  = target
    project.build.profile = "smallest"
    project.entry.module  = "pyaket"
    project.compile()
