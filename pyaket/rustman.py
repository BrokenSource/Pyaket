import subprocess
from pathlib import Path
from typing import Annotated

from loguru import logger
from typer import Option

from broken.enumx import BrokenEnum
from broken.envy import Environment, Runtime
from broken.system import Host, PlatformEnum
from broken.utils import shell


class RustToolchain(str, BrokenEnum):
    Stable  = "stable"
    Nightly = "nightly"

class Rustman:

    @staticmethod
    def install_rust(
        toolchain:   Annotated[RustToolchain, Option("--toolchain",   "-t", help="(Any    ) Rust toolchain to use (stable, nightly)")]="stable",
        build_tools: Annotated[bool,          Option("--build-tools", "-b", help="(Windows) Install Visual C++ Build Tools")]=True,
    ) -> None:
        """Installs a rust toolchain"""

        # Actions has its own workflow setup
        if (Runtime.GitHub):
            return

        # Install Visual C++ Build Tools on Windows
        if (Host.OnWindows and build_tools):
            logger.warn("You must have Microsoft Visual C++ Build Tools installed to compile Rust projects")
            logger.warn("• Will try installing it, you might need to restart your shell, good luck!")
            shell("winget", "install", "-e", "--id", "Microsoft.VisualStudio.2022.BuildTools", "--override", (
                " --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64"
                " --add Microsoft.VisualStudio.Component.Windows10SDK"
                " --add Microsoft.VisualStudio.Component.Windows11SDK"
                "--wait --passive"
            ))

    def install_tools(self) -> None:
        if Host.OnWindows:
            Environment.set("MSVC", self.release.msvc)

            # MSYS2 Configuration
            if (not self.release.msvc):

                # Automatically install MSYS2 if not found
                if not (msys2 := Path(Environment.get("MSYS2_PATH", r"C:\\msys64"))).exists():
                    shell("winget", "install", "-e", "--id", "MSYS2.MSYS2")

                def install_msys2_packages(*packages: str) -> subprocess.CompletedProcess:
                    return shell(msys2/"usr"/"bin"/"bash.exe", "-lc",
                        f"pacman -S {' '.join(packages)} --noconfirm --needed")

                # Native x86_64 => Other platforms
                if Host.Arch.is_amd():
                    if (self.release.platform == PlatformEnum.WindowsAMD64):
                        install_msys2_packages("mingw-w64-ucrt-x86_64-gcc")
                        Environment.add_to_path(msys2/"ucrt64"/"bin")

                    elif (self.release.platform == PlatformEnum.WindowsARM64):
                        # Fixme: Almost got it, clang linking errors
                        ...

        elif Host.OnLinux:
            get = Environment.flag("AUTO_PACKAGES")

            # Need MinGW64 for cross compilation
            if get and (self.release.platform == PlatformEnum.WindowsAMD64):
                if Host.ArchLike:
                    shell("sudo", "pacman", "-S", "mingw-w64-toolchain")
                elif Host.UbuntuLike:
                    shell("sudo", "apt", "install", "mingw-w64")
            if get and (self.release.platform == PlatformEnum.WindowsAMD64):
                if Host.ArchLike:
                    # Todo: Is it https://aur.archlinux.org/packages/mingw-w64-llvm (fat) ?
                    shell("yay", "-S", "mingw-w64-llvm", "--noconfirm", skip=1)
