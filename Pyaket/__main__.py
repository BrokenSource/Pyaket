import shutil
import sys
from pathlib import Path
from typing import Annotated

from attrs import define
from typer import Option

from Broken import (
    BrokenEnum,
    BrokenPath,
    BrokenPlatform,
    Runtime,
    denum,
    log,
    shell,
)
from Broken.Manager.Project import CodeProject, ProjectManager
from Pyaket import PYAKET_ABOUT, PyaketProject


class RustToolchain(str, BrokenEnum):
    Stable  = "stable"
    Nightly = "nightly"


@define
class PyaketManager(ProjectManager):
    cls: CodeProject = PyaketProject

    def __attrs_post_init__(self):
        with self.cli.panel("🚀 Core"):
            self.cli.command(self.rust)

        self.cli.description = PYAKET_ABOUT
        self.find_projects(Path.cwd())

    @staticmethod
    def rust(
        toolchain:   Annotated[RustToolchain, Option("--toolchain",   "-t", help="(Any    ) Rust toolchain to use (stable, nightly)")]="stable",
        build_tools: Annotated[bool,          Option("--build-tools", "-b", help="(Windows) Install Visual C++ Build Tools")]=True,
    ):
        """🦀 Installs rustup and a rust toolchain"""
        import requests

        # Actions has its own workflow setup
        if (Runtime.GitHub):
            return

        # Install rustup based on platform
        if not shutil.which("rustup"):
            log.info("Rustup wasn't found, will install it")

            if BrokenPlatform.OnWindows:
                shell("winget", "install", "-e", "--id", "Rustlang.Rustup")
            elif BrokenPlatform.OnUnix:
                shell("sh", "-c", requests.get("https://sh.rustup.rs").text, "-y", echo=False)
            elif BrokenPlatform.OnMacOS:
                # Xcode? Idk, buy me a mac
                ...

            # If rustup isn't found, ask user to restart shell
            BrokenPath.add_to_path(Path.home()/".cargo"/"bin")

            if not BrokenPath.which("rustup"):
                log.warning("Rustup was likely installed but wasn't found adding '~/.cargo/bin' to Path")
                log.warning("• Maybe you changed the CARGO_HOME or RUSTUP_HOME environment variables")
                log.warning("• Please restart your shell for Rust toolchain to be on PATH")
                exit(0)

        # Install Visual C++ Build Tools on Windows
        if (BrokenPlatform.OnWindows and build_tools):
            log.warning("You must have Microsoft Visual C++ Build Tools installed to compile Rust projects")
            log.warning("• Will try installing it, you might need to restart your shell, good luck!")
            shell("winget", "install", "-e", "--id", "Microsoft.VisualStudio.2022.BuildTools", "--override", (
                " --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64"
                " --add Microsoft.VisualStudio.Component.Windows10SDK"
                " --add Microsoft.VisualStudio.Component.Windows11SDK.22000"
                "--wait --passive"
            ))

        shell("rustup", "default", denum(toolchain))

def main():
    pyaket = PyaketManager()
    pyaket.cli(*sys.argv[1:])

if __name__ == "__main__":
    main()
