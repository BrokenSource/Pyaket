import os
import sys
from enum import Enum
from pathlib import Path
from typing import Annotated, Optional, Self

import tomli
from dotmap import DotMap
from loguru import logger
from pydantic import BaseModel, Field, PrivateAttr
from typer import Option

from broken.envy import Environment
from broken.path import BrokenPath
from broken.system import ArchEnum, Host, PlatformEnum, SystemEnum
from broken.typerx import BrokenTyper
from broken.utils import BrokenCache, shell
from pyaket import PYAKET, PYAKET_ABOUT, __version__

# ---------------------------------------------- #
# https://pyaket.dev/docs/config/application/

class PyaketApplication(BaseModel):
    """General metadata and dependencies definitions of the project"""

    name: Annotated[str, Option("--name", "-n")] = "Pyaket"
    """The application name, used for"""

    author: Annotated[str, Option("--author", "-a")] = "BrokenSource"
    """Subdirectory of the platform's user data directory to install the application"""

    version: Annotated[str, Option("--version", "-v")] = "0.0.0"
    """The release version matching PyPI, codename, branch, latest, etc"""

    about: Annotated[str, Option("--about", "-d")] = "No description provided"
    """A short description of the application, used for metadata, shortcuts"""

    # Todo: Ensure PNG for Unix, 256x256 .ico for Windows
    icon: Annotated[Optional[Path], Option("--icon", "-i")] = None
    """Path to an icon file to use for the application"""

    keep_open: Annotated[bool, Option("--keep-open", "-k")] = False
    """Keep the terminal open after errors or finish"""

# ---------------------------------------------- #
# https://pyaket.dev/docs/config/dependencies/

class PyaketDependencies(BaseModel):
    """Configuration for the dependencies of the project"""

    wheels: Annotated[list[Path], Option("--wheel", "-w")] = []
    """List of wheels to bundle and install at runtime"""

    pypi: Annotated[list[str], Option("--pypi", "-p")] = []
    """List of dependencies to install at runtime from PyPI"""

    reqtxt: Annotated[Optional[Path], Option("--requirements", "-r")] = None
    """Path to a requirements.txt to install at runtime (legacy)"""

    rolling: Annotated[bool, Option("--rolling")] = False
    """Always upgrade dependencies at startup"""

    # def resolve_wheel_globs(self) -> None:

# ---------------------------------------------- #
# https://pyaket.dev/docs/config/directories/

class PyaketDirectories(BaseModel):
    """Configuration for the directories used by the project"""

    common: Annotated[str, Option("--common", "-c")] = "Pyaket"
    """Subdirectory of the workspace to use for all installed files"""

    versions: Annotated[str, Option("--versions", "-v")] = "Versions"
    """Subdirectory of the common dir to install versions of the application"""

# ---------------------------------------------- #
# https://pyaket.dev/docs/config/python/

class PyaketPython(BaseModel):
    """Configuration for a Python interpreter to use for the project"""

    version: Annotated[str, Option("--version", "-v")] = "3.13"
    """A target python version to use at runtime"""

    bundle: Annotated[bool, Option("--bundle", "-b")] = False
    """Whether to bundle python in the executable"""

# ---------------------------------------------- #
# https://pyaket.dev/docs/config/pytorch/

class PyaketTorch(BaseModel):
    """Optional configuration to install PyTorch at runtime"""

    version: Annotated[str, Option("--version", "-v")] = None
    """A target torch version to use at runtime, empty disables it"""

    backend: Annotated[str, Option("--backend", "-b")] = "auto"
    """The backend to use for PyTorch, auto, cpu, xpu, cu128, cu118, etc"""

# ---------------------------------------------- #
# https://pyaket.dev/docs/config/entry/

class PyaketEntry(BaseModel):
    """Configuration for the entry point of the application"""

    module: Annotated[str, Option("--module", "-m")] = None
    """A module to run at runtime as (python -m module ...)"""

    script: Annotated[str, Option("--script", "-f")] = None
    """A script to bundle and run at runtime (python script.py ...)"""

    code: Annotated[str, Option("--code", "-c")] = None
    """A inline code snippet to run at runtime (python -c "code")"""

    command: Annotated[str, Option("--command", "-x")] = None
    """A command to run at runtime (command ...)"""

# ---------------------------------------------- #

class PyaketRelease(BaseModel):
    """Release configuration for the application"""

    system: Annotated[SystemEnum, Option("--target", "-t")] = Host.System
    """Target Operating System to build binaries for"""

    arch: Annotated[ArchEnum, Option("--arch", "-a")] = Host.Arch
    """Target Architecture to build binaries for"""

    @property
    def platform(self) -> PlatformEnum:
        return PlatformEnum.from_parts(self.system, self.arch)

    class Profile(str, Enum):
        Develop  = "develop"
        Fast     = "fast"
        Fastest  = "fastest"
        Small    = "small"
        Smallest = "smallest"

    profile: Annotated[Profile, Option("--profile", "-p")] = Profile.Small
    """Build profile to use"""

    standalone: Annotated[bool, Option("--standalone", "-s")] = False
    """Create a standalone offline executable"""

    msvc: Annotated[bool, Option("--msvc", "-m")] = False
    """(Windows) Use MSVC to build the binary"""

    zigbuild: Annotated[bool, Option("--zig", "-z")] = False
    """Use cargo-zigbuild to build the binary"""

    xwin: Annotated[bool, Option("--xwin")] = False
    """Use cargo-xwin to build msvc binaries from non-windows hosts"""

    upx: Annotated[bool, Option("--upx", "-u")] = False
    """Use UPX to compress the binary"""

    tarball: Annotated[bool, Option("--tarball", "-x")] = False
    """(Unix   ) Create a .tar.gz for unix releases (preserves chmod +x)"""

# ---------------------------------------------- #

class PyaketProject(BaseModel):
    application:  PyaketApplication  = Field(default_factory=PyaketApplication)
    dependencies: PyaketDependencies = Field(default_factory=PyaketDependencies)
    directories:  PyaketDirectories  = Field(default_factory=PyaketDirectories)
    python:       PyaketPython       = Field(default_factory=PyaketPython)
    torch:        PyaketTorch        = Field(default_factory=PyaketTorch)
    entry:        PyaketEntry        = Field(default_factory=PyaketEntry)
    release:      PyaketRelease      = Field(default_factory=PyaketRelease)

    @property
    def release_name(self) -> str:
        return ''.join((
            f"{self.application.name.lower()}",
            f"-{self.release.platform.value}",
            f"-v{self.application.version}",
            f"-{self.torch.backend}" if (self.torch.version) else "",
            f"{self.release.platform.extension}",
        ))

    _cli: BrokenTyper = PrivateAttr(default_factory=BrokenTyper)

    def model_post_init(self, ctx):
        self._cli = BrokenTyper(chain=True, help=False, version=__version__)
        self._cli.description = PYAKET_ABOUT

        with self._cli.panel("🔴 Project"):
            self._cli.command(self.application, name="app")
            self._cli.command(self.directories, name="dir")
            self._cli.command(self.entry,       name="run")

        with self._cli.panel("🟡 Dependencies"):
            self._cli.command(self.dependencies,   name="deps")
            self._cli.command(self.python, name="python")
            self._cli.command(self.torch,  name="torch")

        with self._cli.panel("🟢 Building"):
            self._cli.command(self.release, name="release")
            self._cli.command(self.compile, name="compile")

        with self._cli.panel("🔵 Special"):
            self._cli.command(self.build, name="build")

    def dict(self) -> dict:
        return self.model_dump()

    def json(self) -> str:
        return self.model_dump_json()

    @staticmethod
    def from_toml(path: Path="pyaket.toml") -> Self:
        data = tomli.loads(Path(path).read_text("utf-8"))
        return PyaketProject.model_validate(data)

    # -------------------------------------------------------------------------------------------- #

    def build(self,
        standalone: Annotated[bool, Option("--standalone", "-s")]=False,
        all:        Annotated[bool, Option("--all",        "-a")]=False,
    ):
        """Build wheels for the project and bundle them on the executable"""
        wheels: Path = BrokenPath.recreate(PYAKET.DIRECTORIES.DATA/"Wheels")
        shell(sys.executable, "-m", "uv", "build", "--wheel", ("--all-packages"*all), "-o", wheels)
        self.dependencies.wheels.extend(wheels.glob("*.whl"))

    def compile(self,
        target: Annotated[Path, Option("--target", "-t", help="Directory to build the project (target)")]=
            Path(os.getenv("CARGO_TARGET_DIR") or (Path.cwd()/"target")),
        output: Annotated[Path, Option("--output", "-o", help="Directory to output the compiled binary")]=
            Path(os.getenv("PYAKET_RELEASE_DIR") or (Path.cwd()/"release")),
    ) -> Path:

        # Fixme: Wait for uv's implementation of pip wheel for my own sanity
        if self.release.standalone and (self.release.platform != Host.Platform):
            logger.error("Standalone releases are best built in a host matching the target platform")
            logger.error("• Awaiting implementation of (https://github.com/astral-sh/uv/issues/1681)")
            logger.error(f"• Attempted to build for {self.release.platform} on {Host.Platform}")
            return None
        elif self.release.standalone:
            logger.error("Standalone releases are not implemented yet")
            return None

        # Auto enable zigbuild in scenarios where it's easier
        if Environment.flag((_FLAG := "AUTO_ZIGBUILD"), 1) and any((
            Host.OnWindows and (not self.release.system.is_windows()),
            Host.OnWindows and (self.release.platform == PlatformEnum.WindowsARM64),
            Host.OnLinux   and (self.release.system.is_macos()),
            Host.OnLinux   and (self.release.platform == PlatformEnum.LinuxARM64),
            Host.OnMacOS   and (not self.release.system.is_macos()),
        )):
            logger.note((
                "Enabling zigbuild for easier cross compilation, "
                f"you can opt-out of this by setting {_FLAG}=0"
            ))
            self.release.zigbuild = True

        # Todo: MacOS ulimit

        # Cannot use multiple cargo wrappers at once
        if sum((self.release.zigbuild, self.release.xwin)) > 1:
            raise RuntimeError(logger.error((
                "Cannot use multiple cargo wrappers at the same time"
            )))

        try:
            if self.release.zigbuild:
                import ziglang  # pyright: ignore
        except ImportError:
            raise RuntimeError(logger.error(
                "Missing group 'pip install pyaket[zig]' "
                "for cross compilation with ziglang"
            ))

        if self.release.xwin:
            raise NotImplementedError(logger.error((
                "cargo-xwin is not yet implemented."
            )))

        shell("rustup", "default", f"stable-{Host.Platform.triple()}")
        shell("rustup", "target", "add", self.release.platform.triple(msvc=self.release.msvc))
        self.export()

        if shell(
            "cargo", ("zig"*self.release.zigbuild) + "build",
            "--manifest-path", (PYAKET.PACKAGE/"Cargo.toml"),
            "--profile", self.release.profile.value,
            "--target", self.release.platform.triple(),
            "--target-dir", Path(target),
        ).returncode != 0:
            raise RuntimeError(logger.error((
                "Failed to compile Pyaket, check the logs "
                "above for information on what went wrong"
            )))

        # Find the compiled binary
        binary = next(
            (Path(target)/self.release.platform.triple()/self.release.profile.value)
            .glob(("pyaket" + (".exe"*self.release.system.is_windows())))
        )
        logger.info(f"Compiled Pyaket binary at ({binary})")

        # Rename the compiled binary to the final release name
        release = (Path(output) / self.release_name)
        release.parent.mkdir(parents=True, exist_ok=True)
        binary.rename(release)

        # Compress the final release with upx
        if self.release.upx and (shell("upx", "--best", "--lzma", release).returncode != 0):
            raise RuntimeError(logger.error("Failed to compress executable with upx"))

        # Release a tar.gz to keep chmod +x attributes
        if self.release.tarball and self.release.system.is_unix():
            shell("tar", "-czf", f"{release}.tar.gz", "-C", release.parent, release.name)

        logger.ok(f"Final project release at ({release})")
        return release

    # -------------------------------------------------------------------------------------------- #

    def export(self) -> None:
        os.environ.update(
            PYAKET_PROJECT   = self.json(),
            ProductName      = self.application.name,
            CompanyName      = self.application.author,
            FileVersion      = self.application.version,
            FileDescription  = self.application.about,
            OriginalFilename = self.release_name,
        )

    # -------------------------------------------------------------------------------------------- #

    def pyproject(self,
        path: Annotated[Path, Option("--pyproject", "-p", help="Path to a pyproject.toml file")],
        pin:  Annotated[bool, Option("--pin",             help="Pin dependencies versions")]=False,
    ) -> None:
        """Update project metadata from a pyproject.toml file"""
        data = DotMap(tomli.loads(Path(path).read_text(encoding="utf-8")))
        self.application.name   = data.project.get("name", self.application.name)
        self.application.author = "" # Secret mode for independent projects

        def _pin(package: str) -> str:
            """"""
            if (not pin):
                return package

            package = package.replace(" ", "")

            # Todo: Pin @git+ dependencies

            # Simple known
            for marker in ("~=", ">=", "<=", "=="):
                if marker in package:
                    package = package.replace(marker, "==")
                    return

            # Get the latest version from PyPI dynamically
            with BrokenCache.package_info(package) as pypi:
                return f"{package}=={pypi.info.version}"

        # Standard dependencies
        for package in data.project.dependencies:
            self.dependencies.pypi.append(_pin(package))
