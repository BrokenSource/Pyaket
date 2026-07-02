import os
import subprocess
import sys
import tarfile
import tomllib
import uuid
from enum import Enum
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable, Optional

from pydantic import BaseModel, Field, PrivateAttr

import pyaket
from pyaket import logger
from pyaket.targets import Target

# ---------------------------------------------------------------------------- #

class PyaketApplication(BaseModel):
    """General metadata and dependencies definitions of the project"""

    name: str = "Pyaket"
    """The application name, used for"""

    author: str = "BrokenSource"
    """Subdirectory of the platform's user data directory to install the application"""

    vendor: Optional[str] = None
    """Overrides platform directory workspace"""

    version: str = pyaket.__version__
    """The release version matching PyPI, codename, branch, latest, etc"""

    about: str = "No description provided"
    """A short description of the application, used for metadata, shortcuts"""

    # Todo: Ensure PNG for Unix, 256x256 .ico for Windows
    icon: Optional[Path] = None
    """Path to an icon file to use for the application"""

# ---------------------------------------------------------------------------- #

class PyaketDependencies(BaseModel):
    """Configuration for the dependencies of the project"""

    wheels: list[Path] = Field(default_factory=list)
    """List of wheels to bundle and install at runtime"""

    pypi: list[str] = Field(default_factory=list)
    """List of dependencies to install at runtime from PyPI"""

    rolling: bool = False
    """Always upgrade dependencies at startup"""

    standalone: bool = False
    """Bundle all dependencies in a single executable"""

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

class PyaketDirectories(BaseModel):
    """Configuration for the directories used by the project"""

    common: str = "Pyaket"
    """Subdirectory of the workspace to use for all installed files"""

    versions: str = "Versions"
    """Subdirectory of the common dir to install versions of the application"""

# ---------------------------------------------------------------------------- #

class PyaketPython(BaseModel):
    """Configuration for a Python interpreter to use for the project"""

    version: str = "3.14"
    """A target python version to use at runtime"""

    bundle: bool = False
    """Whether to bundle python in the executable"""

# ---------------------------------------------------------------------------- #

class PyaketTorch(BaseModel):
    """Optional configuration to install PyTorch at runtime"""

    version: Optional[str] = None
    """A target torch version to use at runtime, empty disables it"""

    backend: str = "auto"
    """The backend to use for PyTorch, auto, cpu, xpu, cu128, cu118, etc"""

# ---------------------------------------------------------------------------- #

class PyaketEntry(BaseModel):
    """Configuration for the entry point of the application"""

    module: Optional[str] = None
    """A module to run at runtime as (python -m module ...)"""

    command: Optional[str] = None
    """A command to run at runtime (command ...)"""

# ---------------------------------------------------------------------------- #

class CargoProfile(str, Enum):
    Develop  = "develop"
    Fast     = "fast"
    Fastest  = "fastest"
    Small    = "small"
    Smallest = "smallest"

class CargoWrapper(str, Enum):
    Build = "build"
    Zig   = "zigbuild"
    Xwin  = "xwin"

    @property
    def build(self) -> Iterable[str]:
        """
        Get base command:
        - `cargo build ...`
        - `cargo zigbuild ...`
        - `cargo xwin build ...`
        """
        yield self.value

        if (self is self.Xwin):
            yield "build"


class PyaketBuild(BaseModel):
    """Release configuration for the application"""

    host: Target = Target.host()
    """Host platform building the application"""

    target: Target = Target.host()
    """A rust target platform to compile for"""

    profile: CargoProfile = CargoProfile.Small
    """Build profile to use"""

    standalone: bool = False
    """Create a standalone offline executable"""

    cargo: CargoWrapper = CargoWrapper.Build
    """Cargo wrapper to use to build the binary"""

    def autocargo(self) -> None:
        if (os.getenv(_FLAG := "AUTO_ZIGBUILD", "1") == "1") and any((
            self.host.is_windows() and (not self.target.is_windows()),
            self.host.is_linux() and self.target.is_macos(),
        )):
            logger.info("Enabling cargo-zigbuild for easier cross compilation")
            logger.info(f"• You can opt-out of it by setting {_FLAG}=0")
            self.cargo = CargoWrapper.Zig

    target_dir: Path = Field(
        default=Path(os.getenv("CARGO_TARGET_DIR") or (Path.cwd()/"target")),
        exclude=True)
    """Cargo target directory for cache build files"""

    output: Path = Field(
        default=(Path.cwd()/"release"),
        exclude=True)
    """Output directory for the compiled renamed binary"""

    upx: bool = False
    """Use UPX to compress the binary"""

    tarball: bool = False
    """Create a .tar.gz for unix releases (preserves chmod +x)"""

# ---------------------------------------------------------------------------- #

class PyaketAssets(BaseModel):
    _root = PrivateAttr(default_factory=lambda:
        TemporaryDirectory(prefix=f"{__package__}-"))

    @property
    def root(self) -> Path:
        return Path(self._root.name)

    def write(self, relative: Path, data: bytes) -> None:
        path = (self.root / relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

# ---------------------------------------------------------------------------- #

class PyaketProject(BaseModel):
    app:     PyaketApplication  = Field(default_factory=PyaketApplication)
    deps:    PyaketDependencies = Field(default_factory=PyaketDependencies)
    dirs:    PyaketDirectories  = Field(default_factory=PyaketDirectories)
    python:  PyaketPython       = Field(default_factory=PyaketPython)
    torch:   PyaketTorch        = Field(default_factory=PyaketTorch)
    entry:   PyaketEntry        = Field(default_factory=PyaketEntry)
    build:   PyaketBuild        = Field(default_factory=PyaketBuild)
    assets:  PyaketAssets       = Field(default_factory=PyaketAssets)

    # Warn: Must use this for environment and parallel builds support
    environ: dict = Field(default_factory=os.environ.copy, exclude=True)
    """Safe and isolated environment variables for the build process"""

    uuid: str = None # type: ignore

    # ------------------------------------------------------------------------ #

    def release_name(self) -> str:
        return ''.join((
            f"{self.app.name.lower()}",
            f"-v{self.app.version}",
            f"+{self.torch.backend}" * bool(self.torch.version),
            f"-{self.build.target.value}",
            self.build.target.exe_suffix,
        ))

    def compile(self) -> Path:
        logger.info(f"Compiling for {self.build.target.description}")

        # Complaints session
        if self.build.target.tier == 2:
            logger.warn(f"Rust doesn't guarantee a working build for {self.build.target.value} (tier=2)")
        if self.build.target.tier == 3:
            logger.warn(f"Rust support for {self.build.target.value} is very limited (tier=3)")
        if not self.build.target.stdlib:
            logger.crit(f"No stdlib available for {self.build.target.value}, build might fail")
        if not self.build.target.host_tools:
            logger.crit(f"No host tools available for {self.build.target.value}, get rust on your own!")

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
            self.assets.write(
                relative=Path(f"dist/{wheel.name}"),
                data=wheel.read_bytes(),
            )

        # Export isolated environment
        self.environ.update(dict(
            PYAKET_PROJECT   = self.model_dump_json(),
            PYAKET_ASSETS    = str(self.assets.root),
            ProductName      = self.app.name,
            CompanyName      = self.app.author,
            FileVersion      = self.app.version,
            FileDescription  = self.app.about,
            OriginalFilename = self.release_name(),
        ))

        # Safety list known assets
        for file in self.assets.root.rglob("*"):
            logger.info(f"Asset: {file}")

        self.build.autocargo()
        subprocess.check_call((
            "cargo", *self.build.cargo.build,
            "--manifest-path", str(pyaket.manifest),
            "--profile", self.build.profile.value,
            "--target", self.build.target.value,
            "--target-dir", str(self.build.target_dir),
        ), env=self.environ, cwd=pyaket.package)

        # Find the compiled binary
        binary = next(
            (self.build.target_dir/self.build.target.value/self.build.profile.value)
            .glob(("pyaket" + self.build.target.exe_suffix))
        )

        # Rename the compiled binary to the final release name
        release = (self.build.output / self.release_name())
        release.parent.mkdir(parents=True, exist_ok=True)
        release.write_bytes(binary.read_bytes())
        release.chmod(0o755)
        binary.unlink()

        if self.build.upx:
            subprocess.check_call(("upx", "--best", "--lzma", str(release)))

        # Release a tar.gz to keep chmod +x attributes
        if self.build.tarball and self.build.target.is_unix():
            with tarfile.open(f"{release}.tar.gz", "w:gz") as archive:
                archive.add(release, arcname=release.name)
                release.unlink()
            release = Path(archive.name) # type: ignore

        # Ignore all binaries in version control
        self.build.output.joinpath(".gitignore").write_text("*")

        return release

    # ------------------------------------------------------------------------ #

    def from_pyproject(self,
        path: Path=Path("pyproject.toml"),
        pin:  bool=False,
    ) -> None:
        """Update project metadata from a pyproject.toml file"""
        data = tomllib.loads(path.read_text("utf-8"))

        # Multiple heuristics and assumptions:
        # - Project 'name' same as 'python -m name'
        self.app.name     = data.get("project", {}).get("name", self.app.name)
        self.app.version  = data.get("project", {}).get("version", "0.0.0")
        self.app.about    = data.get("project", {}).get("description", self.app.about)
        self.entry.module = self.app.name

        # Todo: Pin @git+ dependencies
        # Todo: Load from a lockfile?
        for package in data.get("project", {}).get("dependencies", []):
            self.deps.pypi.append(package)
