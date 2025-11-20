import sys
from pathlib import Path
from typing import Annotated

import tomli
from attrs import Factory, define
from dotmap import DotMap
from loguru import logger
from typer import Option

from broken.enumx import BrokenEnum
from broken.envy import Environment
from broken.model import BrokenModel
from broken.path import BrokenPath
from broken.system import ArchEnum, Host, PlatformEnum, SystemEnum
from broken.typerx import BrokenTyper
from broken.utils import BrokenCache, shell
from pyaket import PYAKET, PYAKET_ABOUT, __version__

# Warn: Must match lib.rs
SEPARATOR: str = ";"

# ---------------------------------------------- #
# https://pyaket.dev/docs#app

class PyaketApplication(BrokenModel):
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
    icon: Annotated[Path, Option("--icon", "-i")] = None
    """Path to an icon file to use for the application"""

    keep_open: Annotated[bool, Option("--keep-open", "-k")] = False
    """Keep the terminal open after errors or finish"""

# ---------------------------------------------- #

class PyaketDependencies(BrokenModel):
    """Configuration for the dependencies of the project"""

    wheels: Annotated[list[Path], Option("--wheel", "-w")] = []
    """List of wheels to bundle and install at runtime"""

    pypi: Annotated[list[str], Option("--pypi", "-p")] = []
    """List of dependencies to install at runtime from PyPI"""

    reqtxt: Annotated[Path, Option("--requirements", "-r")] = None
    """Path to a requirements.txt to install at runtime (legacy)"""

    rolling: Annotated[bool, Option("--rolling")] = False
    """Always upgrade dependencies at startup"""

    @property
    def r_wheels(self) -> str:
        """Gets all self.wheels as absolute paths"""
        return SEPARATOR.join(map(str, map(BrokenPath.get, self.wheels))) or None

    @property
    def r_pypi(self) -> str:
        return SEPARATOR.join(map(str, self.pypi)) or None

# ---------------------------------------------- #
# https://pyaket.dev/docs#directories

class PyaketDirectories(BrokenModel):
    """Configuration for the directories used by the project"""

    common: Annotated[str, Option("--common", "-c")] = "pyaket"
    """Subdirectory of the workspace to use for all installed files"""

    versions: Annotated[str, Option("--versions", "-v")] = "versions"
    """Subdirectory of the common dir to install versions of the application"""

# ---------------------------------------------- #
# https://pyaket.dev/docs#python

class PyaketPython(BrokenModel):
    """Configuration for a Python interpreter to use for the project"""

    version: Annotated[str, Option("--version", "-v")] = "3.13"
    """A target python version to use at runtime"""

    bundle: Annotated[bool, Option("--bundle", "-b")] = False
    """Whether to bundle python in the executable"""

# ---------------------------------------------- #
# https://pyaket.dev/docs#pytorch

class PyaketTorch(BrokenModel):
    """Optional configuration to install PyTorch at runtime"""

    version: Annotated[str, Option("--version", "-v")] = None
    """A target torch version to use at runtime, empty disables it"""

    backend: Annotated[str, Option("--backend", "-b")] = "auto"
    """The backend to use for PyTorch, auto, cpu, xpu, cu128, cu118, etc"""

# ---------------------------------------------- #
# https://pyaket.dev/docs#entry-points

class PyaketEntry(BrokenModel):
    """Configuration for the entry point of the application"""

    module: Annotated[str, Option("--module", "-m")] = None
    """A module to run at runtime as (python -m module ...)"""

    script: Annotated[Path, Option("--script", "-f")] = None
    """A script to bundle and run at runtime (python script.py ...)"""

    code: Annotated[str, Option("--code", "-c")] = None
    """A inline code snippet to run at runtime (python -c "code")"""

    command: Annotated[str, Option("--command", "-x")] = None
    """A command to run at runtime (command ...)"""

# ---------------------------------------------- #
# https://pyaket.dev/docs#release

class PyaketRelease(BrokenModel):
    """Release configuration for the application"""

    system: Annotated[SystemEnum, Option("--target", "-t")] = Host.System
    """Target Operating System to build binaries for"""

    arch: Annotated[ArchEnum, Option("--arch", "-a")] = Host.Arch
    """Target Architecture to build binaries for"""

    @property
    def platform(self) -> PlatformEnum:
        return PlatformEnum.from_parts(self.system, self.arch)

    class Profile(str, BrokenEnum):
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

@define
class PyaketProject:
    app:     PyaketApplication  = Factory(PyaketApplication)
    deps:    PyaketDependencies = Factory(PyaketDependencies)
    dirs:    PyaketDirectories  = Factory(PyaketDirectories)
    python:  PyaketPython       = Factory(PyaketPython)
    torch:   PyaketTorch        = Factory(PyaketTorch)
    entry:   PyaketEntry        = Factory(PyaketEntry)
    release: PyaketRelease      = Factory(PyaketRelease)

    @property
    def release_name(self) -> str:
        return ''.join((
            f"{self.app.name.lower()}",
            f"-{self.release.platform.value}",
            f"-v{self.app.version}",
            f"-{self.torch.backend}" if (self.torch.version) else "",
            f"{self.release.platform.extension}",
        ))

    cli: BrokenTyper = None

    def __attrs_post_init__(self):
        self.cli = BrokenTyper(chain=True, help=False, version=__version__)
        self.cli.description = PYAKET_ABOUT

        with self.cli.panel("🔴 Project"):
            self.cli.command(self.app,   name="app")
            self.cli.command(self.entry, name="run")

        with self.cli.panel("🟡 Dependencies"):
            self.cli.command(self.python, name="python")
            self.cli.command(self.torch,  name="torch")

        with self.cli.panel("🟢 Building"):
            self.cli.command(self.release, name="release")
            self.cli.command(self.compile, name="compile")

        with self.cli.panel("🔵 Special"):
            self.cli.command(self.build, name="build")

    # -------------------------------------------------------------------------------------------- #

    def build(self,
        standalone: Annotated[bool, Option("--standalone", "-s")]=False,
        all:        Annotated[bool, Option("--all",        "-a")]=False,
    ):
        """Build wheels for the project and bundle them on the executable"""
        wheels: Path = BrokenPath.recreate(PYAKET.DIRECTORIES.DATA/"Wheels")
        shell(sys.executable, "-m", "uv", "build", "--wheel", ("--all-packages"*all), "-o", wheels)
        self.deps.wheels.extend(wheels.glob("*.whl"))

    def compile(self,
        target: Annotated[Path, Option("--target", "-t", help="Directory to build the project (target)")]=(Path.cwd()/"target"),
        output: Annotated[Path, Option("--output", "-o", help="Directory to output the compiled binary")]=(Path.cwd()/"release"),
    ) -> Path:
        Environment.set("MSVC", self.release.msvc)

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
        shell("rustup", "target", "add", self.release.platform.triple())
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
        BrokenPath.mkdir(release.parent)
        BrokenPath.move(src=binary, dst=release, echo=False)

        # Compress the final release with upx
        if self.release.upx and (shell("upx", "--best", "--lzma", release).returncode != 0):
            raise RuntimeError(logger.error("Failed to compress executable with upx"))

        # Release a tar.gz to keep chmod +x attributes
        if self.release.tarball and self.release.system.is_unix():
            release = BrokenPath.gzip(release, remove=True)

        logger.ok(f"Final project release at ({release})")
        return release

    # -------------------------------------------------------------------------------------------- #

    def export(self) -> None:
        Environment.update(
            PYAKET_RELEASE        = 1,
            PYAKET_APP_NAME       = self.app.name,
            PYAKET_APP_VERSION    = self.app.version,
            PYAKET_APP_AUTHOR     = self.app.author,
            PYAKET_APP_ABOUT      = self.app.about,
            PYAKET_APP_ICON       = self.app.icon,
            PYAKET_APP_WHEELS     = self.deps.r_wheels,
            PYAKET_APP_PYPI       = self.deps.r_pypi,
            PYAKET_APP_REQTXT     = self.deps.reqtxt,
            PYAKET_APP_ROLLING    = self.deps.rolling,
            PYAKET_KEEP_OPEN      = self.app.keep_open,
            PYAKET_COMMON_DIR     = self.dirs.common,
            PYAKET_VERSIONS_DIR   = self.dirs.versions,
            PYAKET_PYTHON_VERSION = self.python.version,
            PYAKET_PYTHON_BUNDLE  = self.python.bundle,
            PYAKET_TORCH_VERSION  = self.torch.version,
            PYAKET_TORCH_BACKEND  = self.torch.backend,
            PYAKET_ENTRY_MODULE   = self.entry.module,
            PYAKET_ENTRY_SCRIPT   = self.entry.script,
            PYAKET_ENTRY_CODE     = self.entry.code,
            PYAKET_ENTRY_COMMAND  = self.entry.command,
            OriginalFilename      = self.release_name
        )

    # -------------------------------------------------------------------------------------------- #

    def pyproject(self,
        path: Annotated[Path, Option("--pyproject", "-p", help="Path to a pyproject.toml file")],
        pin:  Annotated[bool, Option("--pin",             help="Pin dependencies versions")]=False,
    ) -> None:
        """Update project metadata from a pyproject.toml file"""
        data = DotMap(tomli.loads(Path(path).read_text(encoding="utf-8")))
        self.app.name   = data.project.get("name", self.app.name)
        self.app.author = "" # Secret mode for independent projects

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
            self.deps.pypi.append(_pin(package))
