import contextlib
import inspect
import sys
from contextlib import nullcontext

from pydantic import BaseModel
from typer import Typer
from typer.models import OptionInfo

from pyaket import PyaketProject, __version__


def pydantic2typer(cls: BaseModel) -> callable:
    signature = type(cls)

    def wrapper(**options):
        for name, value in options.items():
            setattr(cls, name, value)

    # Copy the signatures to the wrapper function
    wrapper.__signature__ = inspect.signature(signature)
    wrapper.__doc__ = cls.__doc__

    # Inject docstring into typer.Option help
    for value in cls.model_fields.values():
        for metadata in value.metadata:
            if isinstance(metadata, OptionInfo):
                if (help := (metadata.help or value.description)):
                    metadata.help = help.split("\n")[0]

    return wrapper


def main():
    app: Typer = Typer(
        chain=True,
        no_args_is_help=True,
        add_completion=False,
    )

    pyaket = PyaketProject()

    # Think about it.
    def common() -> dict:
        nonlocal panel
        return dict(
            no_args_is_help=True,
            rich_help_panel=panel
        )

    with nullcontext("🔴 Project") as panel:
        app.command(name="app", **common())(pydantic2typer(pyaket.app))
        app.command(name="run", **common())(pydantic2typer(pyaket.entry))
        app.command(name="dir", **common())(pydantic2typer(pyaket.dirs))

    with nullcontext("🟡 Dependencies") as panel:
        app.command(name="dep",    **common())(pydantic2typer(pyaket.deps))
        app.command(name="python", **common())(pydantic2typer(pyaket.python))
        app.command(name="torch",  **common())(pydantic2typer(pyaket.torch))

    with nullcontext("🟢 Building") as panel:
        app.command(name="build", **common())(pydantic2typer(pyaket.build))
        app.command(name="compile", rich_help_panel=panel)(pyaket.compile)

    with contextlib.suppress(SystemExit):
        app(sys.argv[1:])

if __name__ == "__main__":
    main()
