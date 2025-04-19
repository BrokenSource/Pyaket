import site
import subprocess
import tempfile
from pathlib import Path
from typing import Annotated, Iterable

from attrs import Factory, define
from pydantic import Field
from typer import Option

from Broken import (
    ArchEnum,
    BrokenEnum,
    BrokenModel,
    BrokenPath,
    BrokenPlatform,
    BrokenTyper,
    Environment,
    PlatformEnum,
    SystemEnum,
    log,
    shell,
)
from Broken.Manager.Project import CodeProject
from Pyaket import PYAKET

# ---------------------------------------------- #

class AppConfig(BrokenModel):
    """
    General metadata and dependencies definitions of the project

    • [Documentation](https://pyaket.dev/docs/configuration/#app)
    """

    name: Annotated[str, Option("--name", "-n")] = "Pyaket"
    """
    The application name, used for

    • [Documentation](https://pyaket.dev/docs/configuration/#app-name)
    """

    author: Annotated[str, Option("--author", "-a")] = "BrokenSource"
    """
    Subdirectory of the platform's user data directory to install the application

    • [Documentation](https://pyaket.dev/docs/configuration/#app-author)
    """

    version: Annotated[str, Option("--version", "-v")] = "0.0.0"
    """
    The release version matching PyPI, codename, branch, latest, etc.

    • [Documentation](https://pyaket.dev/docs/configuration/#app-version)
    """

    versions_dir: Annotated[str, Option("--versions-dir")] = "Versions"
    """
    Subdirectory of the workspace to install versions of the application.

    • [Documentation](https://pyaket.dev/docs/configuration/#app-versions-dir)
    """

    wheels: Annotated[list[Path], Option("--wheels", "-w")] = Field([])
    """
    List of wheels to bundle and install at runtime, supports glob patterns.

    • [Documentation](https://pyaket.dev/docs/configuration/#app-wheels)
    """

    pypi: Annotated[list[str], Option("--pypi", "-p")] = []
    """
    List of dependencies to install at runtime from PyPI, plain or pinned.

    • [Documentation](https://pyaket.dev/docs/configuration/#app-pypi)
    """

    reqtxt: Annotated[Path, Option("--requirements", "-r")] = ""
    """
    Path to a requirements.txt to install at runtime (legacy)

    • [Documentation](https://pyaket.dev/docs/configuration/#app-requirements-txt)
    """

    rolling: Annotated[bool, Option("--rolling")] = False
    """
    Always upgrade dependencies at startup for a rolling-release mechanism

    • [Documentation](https://pyaket.dev/docs/configuration/#rolling)
    """

    keep_open: Annotated[bool, Option("--keep-open", "-k")] = False
    """
    Keep the terminal open after errors or finish

    • [Documentation](https://pyaket.dev/docs/configuration/#keep-open)
    """

    @property
    def _wheels(self) -> Iterable[Path]:
        """Gets all self.wheels as absolute paths"""
        yield from map(BrokenPath.get, self.wheels)

    @property
    def _pypi(self) -> Iterable[str]:
        for package in self.pypi:
            yield str(package).strip()

    def export(self) -> None:
        Environment.update(
            PYAKET_APP_NAME=self.name,
            PYAKET_APP_VERSION=self.version,
            PYAKET_APP_AUTHOR=self.author,
            PYAKET_APP_SUBDIR=self.versions_dir,
            PYAKET_APP_WHEELS=';'.join(self._wheels),
            PYAKET_APP_PYPI=';'.join(self._pypi),
            PYAKET_APP_REQTXT=self.reqtxt,
            PYAKET_ROLLING=self.rolling,
            PYAKET_KEEP_OPEN=self.keep_open,
        )

# ---------------------------------------------- #

class PythonConfig(BrokenModel):
    """
    Configuration for a Python interpreter to use for the project

    • [Documentation](https://pyaket.dev/docs/configuration/#python)
    """

    version: Annotated[str, Option("--python-version", "-v")] = "3.13"
    """
    A target python version to use at runtime

    • [Documentation](https://pyaket.dev/docs/configuration/#python-version)
    """

    bundle: Annotated[bool, Option("--bundle-python", "-b")] = False
    """
    Whether to bundle the python distribution in the executable

    • [Documentation](https://pyaket.dev/docs/configuration/#python-bundle)
    """

    def export(self) -> None:
        Environment.update(
            PYAKET_PYTHON_VERSION=self.version,
            PYAKET_PYTHON_BUNDLE=self.bundle,
        )

# ---------------------------------------------- #

class AstralConfig(BrokenModel):
    """
    Configuration for uv project and package manager to use

    • [Documentation](https://pyaket.dev/docs/configuration/#uv)
    """

    version: Annotated[str, Option("--uv-version", "-v")] = "0.6.13"
    """
    A target uv version to use at runtime

    • [Documentation](https://pyaket.dev/docs/configuration/#uv-version)
    """

    bundle: Annotated[bool, Option("--bundle-uv", "-b")] = False
    """
    Whether to bundle uv in the executable

    • [Documentation](https://pyaket.dev/docs/configuration/#uv-bundle)
    """

    def export(self) -> None:
        Environment.update(
            PYAKET_UV_VERSION=self.version,
            PYAKET_UV_BUNDLE=self.bundle,
        )

# ---------------------------------------------- #

class TorchConfig(BrokenModel):
    """
    Optional configuration to install PyTorch at runtime

    • [Documentation](https://pyaket.dev/docs/configuration/#pytorch)
    """

    version: Annotated[str, Option("--torch-version", "-v")] = ""
    """
    A target torch version to use at runtime, empty disables it

    • [Documentation](https://pyaket.dev/docs/configuration/#torch-version)
    """

    backend: Annotated[str, Option("--torch-backend", "-b")] = "auto"
    """

    • [Documentation](https://pyaket.dev/docs/configuration/#torch-backend)
    """

    def export(self) -> None:
        Environment.update(
            PYAKET_TORCH_VERSION=self.version,
            PYAKET_TORCH_BACKEND=self.backend,
        )

# ---------------------------------------------- #

class EntryConfig(BrokenModel):
    """
    Configuration for the entry point of the application

    • [Documentation](https://pyaket.dev/docs/configuration/#entry-points)
    """

    module: Annotated[str, Option("--module", "-m")] = None
    """
    A module to run at runtime (python -m module ...)

    • [Documentation](https://pyaket.dev/docs/configuration/#entry-module)
    """

    script: Annotated[Path, Option("--script", "-f")] = None
    """
    A script to bundle and run at runtime (python script.py ...)

    • [Documentation](https://pyaket.dev/docs/configuration/#entry-script)
    """

    code: Annotated[str, Option("--code", "-c")] = None
    """
    A inline code snippet to run at runtime (python -c "code")

    • [Documentation](https://pyaket.dev/docs/configuration/#entry-code)
    """

    command: Annotated[str, Option("--command", "-x")] = None
    """
    A command to run at runtime (command ...)

    • [Documentation](https://pyaket.dev/docs/configuration/#entry-command)
    """

    def export(self) -> None:
        Environment.update(
            PYAKET_ENTRY_MODULE=self.module,
            PYAKET_ENTRY_SCRIPT=self.script,
            PYAKET_ENTRY_CODE=self.code,
            PYAKET_ENTRY_COMMAND=self.command,
        )

# ---------------------------------------------- #

class BuildConfig(BrokenModel):
    """
    Configuration for rust and the build process of the application
    """

    system: Annotated[SystemEnum, Option("--target", "-t")] = BrokenPlatform.System
    """Target Operating System to build binaries for"""

    arch: Annotated[ArchEnum, Option("--arch", "-a")]   = BrokenPlatform.Arch
    """Target Architecture to build binaries for"""

    class Profile(str, BrokenEnum):
        Debug   = "debug"
        Release = "release"
        Small   = "small"

        @property
        def cargo(self) -> str:
            return self.value.replace("debug", "dev")

    profile: Annotated[Profile, Option("--profile", "-p")] = Profile.Release
    """Build profile to use"""

    standalone: Annotated[bool, Option("--standalone", "-s")] = False
    """Create a standalone offline installer"""

    upx: Annotated[bool, Option("--upx", "-u")] = False
    """Use UPX to compress the binary"""

    zigbuild: Annotated[bool, Option("--zig", "-z")] = False
    """Use Cargo zigbuild to build the binary"""

    msvc: Annotated[bool, Option("--msvc", "-m")] = False
    """Use MSVC to build the binary"""

    tarball: Annotated[bool, Option("--tarball", "-x")] = False
    """Create a .tar.gz for unix releases (preserves chmod +x)"""

    @property
    def platform(self) -> PlatformEnum:
        return PlatformEnum.from_parts(self.system, self.arch)

    @property
    def triple(self) -> str:
        return self.platform.triple

    # # Actions

    def should_zigbuild(self) -> None:
        """Force enable zigbuild in configurations where it's easier"""
        if any((
            BrokenPlatform.OnWindows and (not self.system.is_windows()),
            BrokenPlatform.OnWindows and (self.platform == PlatformEnum.WindowsARM64),
            BrokenPlatform.OnLinux and (self.platform == PlatformEnum.LinuxARM64),
            BrokenPlatform.OnLinux and (self.system.is_macos()),
        )):
            log.note("Force enable Zigbuild for cross compilation")
            self.zigbuild = True

    def install_tools(self) -> None:
        if BrokenPlatform.OnWindows:
            Environment.set("MSVC", self.msvc)

            # MSYS2 Configuration
            if (not self.msvc):
                if not (msys2 := Path(Environment.get("MSYS2_PATH", r"C:\\msys64"))).exists():
                    log.error(r"Please install MSYS2 from https://www.msys2.org at default location")

                def install_msys2_packages(*packages: str) -> subprocess.CompletedProcess:
                    return shell(msys2/"usr/bin/bash.exe", "-lc", f"pacman -S {' '.join(packages)} --noconfirm --needed")

                # Native x86_64 => Other platforms
                if BrokenPlatform.Arch.is_amd():
                    if (self.platform == PlatformEnum.WindowsAMD64):
                        install_msys2_packages("mingw-w64-x86_64-gcc")
                        BrokenPath.add_to_path(msys2/"ucrt64/bin")

                    elif (self.platform == PlatformEnum.WindowsARM64):
                        # Fixme: Almost got it, clang linking errors
                        ...

            # Ensure zig.exe is found
            for path in site.getsitepackages():
                BrokenPath.add_to_path(Path(path)/"ziglang")

        elif BrokenPlatform.OnLinux:
            get = Environment.flag("AUTO_PACKAGES")

            # Need MinGW64 for cross compilation
            if get and (self.target == PlatformEnum.WindowsAMD64):
                if BrokenPlatform.ArchLike:
                    shell("sudo", "pacman", "-S", "mingw-w64-toolchain")
                elif BrokenPlatform.UbuntuLike:
                    shell("sudo", "apt", "install", "mingw-w64")

        shell("rustup", "target", "add", self.triple)

# ---------------------------------------------- #

class PyaketConfig(BrokenModel):
    app:    AppConfig    = Field(default_factory=AppConfig)
    python: PythonConfig = Field(default_factory=PythonConfig)
    astral: AstralConfig = Field(default_factory=AstralConfig)
    torch:  TorchConfig  = Field(default_factory=TorchConfig)
    entry:  EntryConfig  = Field(default_factory=EntryConfig)
    build:  BuildConfig  = Field(default_factory=BuildConfig)

    def export_all(self) -> None:
        Environment.update(PYAKET_RELEASE=1)
        self.app.export()
        self.python.export()
        self.astral.export()
        self.torch.export()
        self.entry.export()

# ---------------------------------------------- #

@define(eq=False)
class PyaketProject(CodeProject):
    config: PyaketConfig = Factory(PyaketConfig)

    def __attrs_post_init__(self):
        self.cli = BrokenTyper(chain=True)

        with self.cli.panel("✅ Configuration"):
            self.cli.command(self.config.app,    name="app")
            self.cli.command(self.config.python, name="python")
            self.cli.command(self.config.astral, name="uv")
            self.cli.command(self.config.torch,  name="torch")
            self.cli.command(self.config.entry,  name="entry")
            self.cli.command(self.config.build,  name="build")

        with self.cli.panel("📦 Actions"):
            self.cli.command(self.compile)

    def compile(self,
        cache:  Annotated[Path, Option("--cache",  "-c", help="Directory to build the project")]=(Path(tempfile.gettempdir())/"pyaket"),
        output: Annotated[Path, Option("--output", "-o", help="Directory to output the compiled binary")]="Release",
    ) -> Path:

        # Fixme: Wait for uv's implementation of pip wheel for my own sanity
        if self.build.standalone and (self.build.platform != BrokenPlatform.Host):
            log.error("Standalone releases are best built in a host matching the target platform")
            log.error("• Awaiting implementation of (https://github.com/astral-sh/uv/issues/1681)")
            log.error(f"• Attempted to build for '{self.build.platform}' on '{BrokenPlatform.Host}'")
            return None

        self.config.build.should_zigbuild()
        self.config.build.install_tools()
        self.config.export_all()

        # Cargo warning: We're not 'installing' a utility
        BrokenPath.add_to_path(cache/"bin")

        if shell(
            "cargo", ("zigbuild" if self.build.zigbuild else "build"),
            "--manifest-path", (PYAKET.PACKAGE/"Cargo.toml"),
            "--target-dir", cache,
            "--target", self.build.triple,
            "--profile", self.build.profile.cargo,
            cwd=self.path,
        ).returncode != 0:
            raise RuntimeError(log.error("Failed to compile Pyaket"))

        # Find the compiled binary
        _filename = ("pyaket" + ".exe"*self.build.system.is_windows())
        binary = next((cache/self.build.triple/self.build.profile.value).glob(_filename))
        log.info(f"Compiled Pyaket binary at ({binary})")

        # Rename the compiled binary to the final release name
        release_path = (output / self.release_name)
        BrokenPath.copy(src=binary, dst=release_path)
        BrokenPath.make_executable(release_path)

        # Compress the final release with upx
        if self.build.upx and (shell("upx", "--best", "--lzma", release_path).returncode != 0):
            raise RuntimeError(log.error("Failed to compress executable with upx"))

        # Release a tar.gz to keep chmod +x attributes
        if self.build.tarball and (not self.build.system.is_windows()):
            release_path = BrokenPath.gzip(release_path, remove=True)

        log.success(f"Built Project release at ({release_path})")
        return release_path

    @property
    def release_name(self) -> str:
        return ''.join((
            f"{self.name.lower()}",
            f"-{self.build.platform.value}",
            f"-v{self.app.version}",
            f"-{self.torch.backend}" if (self.torch.version) else "",
            f"{self.build.platform.extension}",
        ))

    # Likely temporary

    @property
    def app(self) -> AppConfig:
        return self.config.app

    @property
    def python(self) -> PythonConfig:
        return self.config.python

    @property
    def astral(self) -> AstralConfig:
        return self.config.astral

    @property
    def torch(self) -> TorchConfig:
        return self.config.torch

    @property
    def entry(self) -> EntryConfig:
        return self.config.entry

    @property
    def build(self) -> BuildConfig:
        return self.config.build
