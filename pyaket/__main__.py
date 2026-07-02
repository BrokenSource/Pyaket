import contextlib
import sys
from contextlib import nullcontext

from cyclopts import App
from parsenaut._cyclopts import Launcher
from pydantic import BaseModel

import pyaket
from pyaket import (
    PyaketApplication,
    PyaketBuild,
    PyaketDependencies,
    PyaketDirectories,
    PyaketEntry,
    PyaketProject,
    PyaketPython,
    PyaketTorch,
)


def main():
    app: App = Launcher.chain(App(
        result_action="return_value",
        help_flags=["--help"],
        version=pyaket.__version__,
    ))

    project = PyaketProject()

    with nullcontext("🔴 Project") as panel:
        app.command(PyaketApplication, name="app", group=panel, result_action=lambda x: setattr(project, "app", x))
        app.command(PyaketEntry,       name="run", group=panel, result_action=lambda x: setattr(project, "entry", x))
        app.command(PyaketDirectories, name="dir", group=panel, result_action=lambda x: setattr(project, "directories", x))

    with nullcontext("🟡 Dependencies") as panel:
        app.command(PyaketDependencies,  name="dep",    group=panel, result_action=lambda x: setattr(project, "deps", x))
        app.command(PyaketPython,        name="python", group=panel, result_action=lambda x: setattr(project, "python", x))
        app.command(PyaketTorch,         name="torch",  group=panel, result_action=lambda x: setattr(project, "torch", x))

    with nullcontext("🟢 Building") as panel:
        app.command(PyaketBuild, name="build", group=panel, result_action=lambda x: setattr(project, "build", x))
        app.command(project.compile, name="compile", group=panel, result_action=lambda x: setattr(project, "compile", x))

    with contextlib.suppress(SystemExit):
        app(sys.argv[1:])