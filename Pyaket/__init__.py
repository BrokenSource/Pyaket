from Broken import BrokenProject, __version__

PYAKET_ABOUT = "📦 Easy Python to → Fast Executables"

PYAKET = BrokenProject(
    PACKAGE=__file__,
    APP_NAME="Pyaket",
    APP_AUTHOR="BrokenSource",
    ABOUT=PYAKET_ABOUT,
)

from Pyaket.Project import PyaketProject
