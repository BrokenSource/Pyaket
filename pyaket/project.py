import os
import shutil
import subprocess
import sys
import uuid
from enum import Enum
from pathlib import Path
from typing import Annotated, Optional, Self

import tomlkit
from dotmap import DotMap
from pydantic import BaseModel, ConfigDict, Field
from typer import Option

from pyaket import PYAKET_PATH, __version__


class PyaketModel(BaseModel):
    model_config = ConfigDict(use_attribute_docstrings=True)

# ---------------------------------------------- #
# https://pyaket.dev/docs/project/application/

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

# ---------------------------------------------- #
# https://pyaket.dev/docs/project/dependencies/

class PyaketDependencies(PyaketModel):
    """Configuration for the dependencies of the project"""

    wheels: Annotated[list[Path], Option("--wheel", "-w")] = []
    """List of wheels to bundle and install at runtime"""

    pypi: Annotated[list[str], Option("--pypi", "-p")] = []
    """List of dependencies to install at runtime from PyPI"""

    reqtxt: Annotated[Optional[Path], Option("--requirements", "-r")] = None
    """Path to a requirements.txt to install at runtime (legacy)"""

    rolling: Annotated[bool, Option("--rolling")] = False
    """Always upgrade dependencies at startup"""

    def resolve_wheels(self) -> None:
        def globinator():
            for path in map(Path, self.wheels):
                if path.is_file():
                    yield path
                elif path.is_dir():
                    yield from path.glob("*.tar.gz")
                    yield from path.glob("*.whl")
                elif "*" in path.name:
                    yield from Path(path.parent).glob(path.name)
                else:
                    raise Warning(f"Wheel pattern ({path}) did not match any files")
        self.wheels = list(globinator())

    def copy_wheels(self) -> None:
        raise NotImplementedError

# ---------------------------------------------- #
# https://pyaket.dev/docs/project/directories/

class PyaketDirectories(PyaketModel):
    """Configuration for the directories used by the project"""

    common: Annotated[str, Option("--common")] = "Pyaket"
    """Subdirectory of the workspace to use for all installed files"""

    versions: Annotated[str, Option("--versions")] = "Versions"
    """Subdirectory of the common dir to install versions of the application"""

# ---------------------------------------------- #
# https://pyaket.dev/docs/project/python/

class PyaketPython(PyaketModel):
    """Configuration for a Python interpreter to use for the project"""

    version: Annotated[str, Option("--version", "-v")] = "3.13"
    """A target python version to use at runtime"""

    bundle: Annotated[bool, Option("--bundle", "-b")] = False
    """Whether to bundle python in the executable"""

# ---------------------------------------------- #
# https://pyaket.dev/docs/project/pytorch/

class PyaketTorch(PyaketModel):
    """Optional configuration to install PyTorch at runtime"""

    version: Annotated[Optional[str], Option("--version", "-v")] = None
    """A target torch version to use at runtime, empty disables it"""

    backend: Annotated[str, Option("--backend", "-b")] = "auto"
    """The backend to use for PyTorch, auto, cpu, xpu, cu128, cu118, etc"""

# ---------------------------------------------- #
# https://pyaket.dev/docs/project/entry/

class PyaketEntry(PyaketModel):
    """Configuration for the entry point of the application"""

    module: Annotated[Optional[str], Option("--module", "-m")] = None
    """A module to run at runtime as (python -m module ...)"""

    command: Annotated[Optional[str], Option("--command", "-c")] = None
    """A command to run at runtime (command ...)"""

# ---------------------------------------------- #

class PyaketRelease(PyaketModel):
    """Release configuration for the application"""

    # From: https://doc.rust-lang.org/stable/rustc/platform-support.html
    target: Annotated[Optional[str], Option("--target", "-t")] = None
    """A rust target platform triple to compile for (passed as-is)"""

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

    msvc: Annotated[bool, Option("--msvc")] = False
    """(Windows) Use MSVC to build the binary"""

    zigbuild: Annotated[bool, Option("--zig", "-z")] = False
    """Use cargo-zigbuild to build the binary"""

    xwin: Annotated[bool, Option("--xwin", "-x")] = False
    """Use cargo-xwin to build msvc binaries from non-windows hosts"""

    upx: Annotated[bool, Option("--upx")] = False
    """Use UPX to compress the binary"""

    tarball: Annotated[bool, Option("--tarball")] = False
    """(Unix   ) Create a .tar.gz for unix releases (preserves chmod +x)"""

    def extension(self) -> str:
        if "windows" in str(self.target):
            return ".exe"
        return ""

# ---------------------------------------------- #

class PyaketProject(PyaketModel):
    app:     PyaketApplication  = Field(default_factory=PyaketApplication)
    deps:    PyaketDependencies = Field(default_factory=PyaketDependencies)
    dirs:    PyaketDirectories  = Field(default_factory=PyaketDirectories)
    python:  PyaketPython       = Field(default_factory=PyaketPython)
    torch:   PyaketTorch        = Field(default_factory=PyaketTorch)
    entry:   PyaketEntry        = Field(default_factory=PyaketEntry)
    release: PyaketRelease      = Field(default_factory=PyaketRelease)
    uuid: str = None

    def release_name(self) -> str:
        return ''.join((
            f"{self.app.name.lower()}",
            f"-{self.release.target}",
            f"-v{self.app.version}",
            f"-{self.torch.backend}" if (self.torch.version) else "",
            self.release.extension()
        ))

    def dict(self) -> dict:
        return self.model_dump()

    def json(self) -> str:
        return self.model_dump_json()

    @staticmethod
    def from_toml(path: Path="pyaket.toml") -> Self:
        data = tomlkit.loads(Path(path).read_text("utf-8"))
        return PyaketProject.model_validate(data)

    # -------------------------------------------------------------------------------------------- #

    def compile(self,
        target: Annotated[Path, Option("--target", "-t", help="Directory to build the project (target)")]=
            Path(os.environ.get("CARGO_TARGET_DIR") or (Path.cwd()/"target")),
        output: Annotated[Path, Option("--output", "-o", help="Directory to output the compiled binary")]=
            Path(os.environ.get("PYAKET_RELEASE_DIR") or (Path.cwd()/"release")),
    ) -> Path:

        # Must have the host toolchain for any rustup shim commands
        subprocess.check_call(("rustup", "default", "stable"))

        # Use host target if not specified
        if self.release.target is None:
            for line in subprocess.run(
                ("rustc", "--version", "--verbose"),
                capture_output=True, text=True,
            ).stdout.splitlines():
                if line.startswith("host:"):
                    self.release.target = line.split("host:")[1].strip()
                    break

        # Must have target toolchain for (cross)compilation
        subprocess.check_call(("rustup", "target", "add", self.release.target))

        # All binaries must have a unique uuid
        self.uuid = str(uuid.uuid4())

        # Fixme (standalone)
        if self.release.standalone:
            raise NotImplementedError((
                "Standalone releases aren't implemented, awaiting:\n"
                "• https://github.com/astral-sh/uv/issues/1681"
            ))

        # Todo: MacOS ulimit

        # Cannot use multiple cargo wrappers at once
        if sum((self.release.zigbuild, self.release.xwin)) > 1:
            raise RuntimeError("Cannot use multiple cargo wrappers at the same time")

        if self.release.zigbuild and (shutil.which("zig") is None):
            raise RuntimeError(
                "Missing group 'pip install pyaket[zig]' "
                "for cross compilation with ziglang"
            )

        if self.release.xwin:
            raise NotImplementedError("cargo-xwin is not yet implemented")

        # https://github.com/rust-cross/cargo-zigbuild/issues/329
        if sys.platform == "darwin":
            subprocess.run(("ulimit", "-n", "8192"))

        self.export()

        subprocess.check_call((
            "cargo", ("zig"*self.release.zigbuild) + "build",
            "--manifest-path", str(PYAKET_PATH/"Cargo.toml"),
            "--profile", self.release.profile.value,
            "--target", self.release.target,
            "--target-dir", str(target),
        ))

        # Find the compiled binary
        binary = next(
            (Path(target)/self.release.target/self.release.profile.value)
            .glob(("pyaket" + self.release.extension())),
        )

        # Rename the compiled binary to the final release name
        release = (Path(output) / self.release_name())
        release.parent.mkdir(parents=True, exist_ok=True)
        release.write_bytes(binary.read_bytes())
        release.chmod(0o755)
        binary.unlink()

        # Compress the final release with upx
        if self.release.upx and subprocess.run(("upx", "--best", "--lzma", str(release))).returncode != 0:
            raise RuntimeError("Failed to compress executable with upx")

        # Release a tar.gz to keep chmod +x attributes
        if self.release.tarball and self.release.system.is_unix():
            subprocess.run((
                "tar", "-czf", f"{release}.tar.gz",
                "-C", release.parent, release.name
            ), check=True)

        return release

    # -------------------------------------------------------------------------------------------- #

    def export(self) -> None:
        os.environ.update(
            PYAKET_PROJECT   = self.json(),
            ProductName      = self.app.name,
            CompanyName      = self.app.author,
            FileVersion      = self.app.version,
            FileDescription  = self.app.about,
            OriginalFilename = self.release_name(),
        )

    # -------------------------------------------------------------------------------------------- #

    def pyproject(self,
        path: Path=Path("pyproject.toml"),
        pin:  bool=False,
    ) -> None:
        """Update project metadata from a pyproject.toml file"""
        data = DotMap(tomlkit.loads(Path(path).read_text(encoding="utf-8")))
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
