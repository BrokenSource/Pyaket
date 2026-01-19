import os
import subprocess
import sys
import uuid
from enum import Enum
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated, Iterable, Optional, Self

import tomllib
from dotmap import DotMap
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from typer import Option

from pyaket import (
    PYAKET_CARGO,
    __version__,
    logger,
)
from pyaket.targets import Target


class PyaketModel(BaseModel):
    model_config = ConfigDict(use_attribute_docstrings=True)

# ---------------------------------------------------------------------------- #

class PyaketApplication(PyaketModel):
    """General metadata and dependencies definitions of the project"""

    name: Annotated[str, Option("--name", "-n")] = "Pyaket"
    """The application name, used for"""

    author: Annotated[str, Option("--author", "-a")] = "BrokenSource"
    """Subdirectory of the platform's user data directory to install the application"""

    vendor: Annotated[Optional[str], Option("--vendor")] = None
    """Overrides platform directory workspace"""

    version: Annotated[str, Option("--version", "-v")] = "0.0.0"
    """The release version matching PyPI, codename, branch, latest, etc"""

    about: Annotated[str, Option("--about", "-d")] = "No description provided"
    """A short description of the application, used for metadata, shortcuts"""

    # Todo: Ensure PNG for Unix, 256x256 .ico for Windows
    icon: Annotated[Optional[Path], Option("--icon", "-i")] = None
    """Path to an icon file to use for the application"""

    keep_open: Annotated[bool, Option("--keep-open")] = False
    """Keep the terminal open after errors or finish"""

# ---------------------------------------------------------------------------- #
# https://pyaket.dev/docs/project/dependencies/

class PyaketDependencies(PyaketModel):
    """Configuration for the dependencies of the project"""

    wheels: Annotated[list[Path], Option("--wheel", "-w")] = []
    """List of wheels to bundle and install at runtime"""

    pypi: Annotated[list[str], Option("--pypi", "-p")] = []
    """List of dependencies to install at runtime from PyPI"""

    rolling: Annotated[bool, Option("--rolling")] = False
    """Always upgrade dependencies at startup"""

    def unwheel(self) -> Iterable[Path]:
        for path in map(Path, self.wheels):
            if path.is_file():
                yield path
            elif path.is_dir():
                yield from path.glob("*.tar.gz")
                yield from path.glob("*.whl")
            elif "*" in path.name:
                yield from Path(path.parent).glob(path.name)

# ---------------------------------------------------------------------------- #
# https://pyaket.dev/docs/project/directories/

class PyaketDirectories(PyaketModel):
    """Configuration for the directories used by the project"""

    common: Annotated[str, Option("--common")] = "Pyaket"
    """Subdirectory of the workspace to use for all installed files"""

    versions: Annotated[str, Option("--versions")] = "Versions"
    """Subdirectory of the common dir to install versions of the application"""

# ---------------------------------------------------------------------------- #
# https://pyaket.dev/docs/project/python/

class PyaketPython(PyaketModel):
    """Configuration for a Python interpreter to use for the project"""

    version: Annotated[str, Option("--version", "-v")] = "3.13"
    """A target python version to use at runtime"""

    bundle: Annotated[bool, Option("--bundle", "-b")] = False
    """Whether to bundle python in the executable"""

# ---------------------------------------------------------------------------- #
# https://pyaket.dev/docs/project/pytorch/

class PyaketTorch(PyaketModel):
    """Optional configuration to install PyTorch at runtime"""

    version: Annotated[Optional[str], Option("--version", "-v")] = None
    """A target torch version to use at runtime, empty disables it"""

    backend: Annotated[str, Option("--backend", "-b")] = "auto"
    """The backend to use for PyTorch, auto, cpu, xpu, cu128, cu118, etc"""

# ---------------------------------------------------------------------------- #
# https://pyaket.dev/docs/project/entry/

class PyaketEntry(PyaketModel):
    """Configuration for the entry point of the application"""

    module: Annotated[Optional[str], Option("--module", "-m")] = None
    """A module to run at runtime as (python -m module ...)"""

    command: Annotated[Optional[str], Option("--command", "-c")] = None
    """A command to run at runtime (command ...)"""

# ---------------------------------------------------------------------------- #

class PyaketBuild(PyaketModel):
    """Release configuration for the application"""

    # From: https://doc.rust-lang.org/stable/rustc/platform-support.html
    target: Annotated[Target, Option("--target", "-t", show_choices=False)] = Target.host()
    """A rust target platform to compile for"""

    def extension(self) -> str:
        if "windows" in str(self.target):
            return ".exe"
        return ""

    class Profile(str, Enum):
        Develop  = "develop"
        Fast     = "fast"
        Fastest  = "fastest"
        Small    = "small"
        Smallest = "smallest"

    profile: Annotated[Profile, Option("--profile", "-p")] = Profile.Small
    """Build profile to use"""

    standalone: Annotated[bool, Option("--standalone")] = False
    """Create a standalone offline executable"""

    class Cargo(str, Enum):
        Build = "build"
        Zig   = "zigbuild"
        Xwin  = "xwin"

        @property
        def xwin(self) -> bool:
            return (self == PyaketBuild.Cargo.Xwin)

        @property
        def zig(self) -> bool:
            return (self == PyaketBuild.Cargo.Zig)

    cargo: Annotated[Cargo, Option("--cargo", "-c")] = Cargo.Build
    """Cargo wrapper to use to build the binary"""

    upx: Annotated[bool, Option("--upx")] = False
    """Use UPX to compress the binary"""

    tarball: Annotated[bool, Option("--tarball")] = False
    """(Unix   ) Create a .tar.gz for unix releases (preserves chmod +x)"""

# ---------------------------------------------------------------------------- #

class PyaketAssets(PyaketModel):
    _root = PrivateAttr(default_factory=lambda:
        TemporaryDirectory(prefix="pyaket-assets-"))

    @property
    def root(self) -> Path:
        return Path(self._root.name)

    def write(self, path: Path, data: bytes) -> None:
        path = (self.root / path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

# ---------------------------------------------------------------------------- #

class PyaketProject(PyaketModel):
    app:     PyaketApplication  = Field(default_factory=PyaketApplication)
    deps:    PyaketDependencies = Field(default_factory=PyaketDependencies)
    dirs:    PyaketDirectories  = Field(default_factory=PyaketDirectories)
    python:  PyaketPython       = Field(default_factory=PyaketPython)
    torch:   PyaketTorch        = Field(default_factory=PyaketTorch)
    entry:   PyaketEntry        = Field(default_factory=PyaketEntry)
    build:   PyaketBuild        = Field(default_factory=PyaketBuild)
    assets:  PyaketAssets       = Field(default_factory=PyaketAssets)

    environ: dict = Field(default_factory=os.environ.copy, exclude=True)
    """Safe and isolated environment variables for the build process"""

    uuid: str = None

    # ------------------------------------------------------------------------ #

    def release_name(self) -> str:
        return ''.join((
            f"{self.app.name.lower()}",
            f"-{self.build.target.value}",
            f"-v{self.app.version}",
            f"-{self.torch.backend}" * bool(self.torch.version),
            self.build.extension()
        ))

    def compile(self,
        cache: Annotated[Path, Option("--cache", "-c", help="Directory to build the project (target)")]=
            Path(os.environ.get("CARGO_TARGET_DIR") or (Path.cwd()/"target")),
        output: Annotated[Path, Option("--output", "-o", help="Directory to output the compiled binary")]=
            Path(os.environ.get("PYAKET_RELEASE_DIR") or (Path.cwd()/"release")),
    ) -> Path:
        logger.info(f"Compiling for {self.build.target.description}")

        # Complaints session
        if self.build.target.tier == 2:
            logger.warning(f"Rust doesn't guarantee a working build for {self.build.target.value} (tier=2)")
        if self.build.target.tier == 3:
            logger.warning(f"Rust support for {self.build.target.value} is very limited (tier=3)")
        if not self.build.target.stdlib:
            logger.critical(f"No stdlib available for {self.build.target.value}, build might fail")
        if not self.build.target.host_tools:
            logger.critical(f"No host tools available for {self.build.target.value}, get rust on your own!")

        # Todo: Auto zigbuild, xwin method

        # Must have the host and target toolchain
        subprocess.check_call(("rustup", "set", "profile", "minimal"))
        subprocess.check_call(("rustup", "default", "stable"))
        subprocess.check_call(("rustup", "target", "add", self.build.target.value))

        # All binaries are unique
        self.uuid = str(uuid.uuid4())

        # Fixme (standalone)
        if self.build.standalone:
            raise NotImplementedError((
                "Standalone releases aren't implemented, awaiting:\n"
                "• https://github.com/astral-sh/uv/issues/1681"
            ))

        # https://github.com/rust-cross/cargo-zigbuild/issues/329
        if sys.platform == "darwin":
            subprocess.run(("ulimit", "-n", "8192"))

        for wheel in self.deps.unwheel():
            logger.info(f"Bundling wheel: {wheel.name}")
            self.assets.write(
                path=f"{wheel.name}",
                data=wheel.read_bytes()
            )

        # Export isolated environment
        self.environ.update(dict(
            PYAKET_PROJECT   = self.json(),
            PYAKET_ASSETS    = str(self.assets.root),
            ProductName      = self.app.name,
            CompanyName      = self.app.author,
            FileVersion      = self.app.version,
            FileDescription  = self.app.about,
            OriginalFilename = self.release_name(),
        ))

        subprocess.check_call((
            "cargo", self.build.cargo.value,
            "--manifest-path", str(PYAKET_CARGO),
            "--profile", self.build.profile.value,
            "--target", self.build.target.value,
            "--target-dir", str(cache),
        ), env=self.environ)

        # Find the compiled binary
        binary = next(
            (Path(cache)/self.build.target.value/self.build.profile.value)
            .glob(("pyaket" + self.build.extension())),
        )

        # Rename the compiled binary to the final release name
        release = (Path(output) / self.release_name())
        release.parent.mkdir(parents=True, exist_ok=True)
        release.write_bytes(binary.read_bytes())
        release.chmod(0o755)
        binary.unlink()

        if self.build.upx:
            subprocess.check_call(("upx", "--best", "--lzma", str(release)))

        # Release a tar.gz to keep chmod +x attributes
        if self.build.tarball:
            subprocess.check_call((
                "tar", "-czf", f"{release}.tar.gz",
                "-C", release.parent, release.name
            ))

        return release

    # ------------------------------------------------------------------------ #

    def dict(self) -> dict:
        return self.model_dump()

    def json(self) -> str:
        return self.model_dump_json()

    @staticmethod
    def from_toml(path: Path="pyaket.toml") -> Self:
        data = tomllib.loads(Path(path).read_text("utf-8"))
        return PyaketProject.model_validate(data)

    def pyproject(self,
        path: Path=Path("pyproject.toml"),
        pin:  bool=False,
    ) -> None:
        """Update project metadata from a pyproject.toml file"""
        data = DotMap(tomllib.load(open(path, "r", encoding="utf-8")))
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

            # Todo: Get the latest version from PyPI dynamically

        # Standard dependencies
        for package in data.project.dependencies:
            self.deps.pypi.append(_pin(package))
