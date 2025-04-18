import shutil
import site
import subprocess
import tempfile
from pathlib import Path
from typing import Annotated

from attrs import Factory, define
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
    """General metadata and dependencies for the application"""

    name: Annotated[str, Option("--name")] = "Pyaket"
    """https://pyaket.dev/docs/configuration/#app-name"""

    author: Annotated[str, Option("--author")] = "BrokenSource"
    """https://pyaket.dev/docs/configuration/#app-author"""

    version: Annotated[str, Option("--version")] = "0.0.0"
    """https://pyaket.dev/docs/configuration/#app-version"""

    versions_dir: Annotated[str, Option("--subdir")] = None
    """https://pyaket.dev/docs/configuration/#app-versions-dir"""

    wheels: Annotated[str, Option("--wheels")] = None
    """https://pyaket.dev/docs/configuration/#app-wheels"""

    pypi: Annotated[str, Option("--pypi")] = None
    """https://pyaket.dev/docs/configuration/#app-pypi"""

    reqtxt: Annotated[str, Option("--requirements")] = None
    """https://pyaket.dev/docs/configuration/#app-requirements-txt"""

    def export(self) -> None:
        Environment.update(
            PYAKET_APP_NAME=self.name,
            PYAKET_APP_VERSION=self.version,
            PYAKET_APP_AUTHOR=self.author,
            PYAKET_APP_SUBDIR=self.versions_dir,
            PYAKET_APP_WHEELS=self.wheels,
            PYAKET_APP_PYPI=self.pypi,
            PYAKET_APP_REQTXT=self.reqtxt,
        )

# ---------------------------------------------- #

class PythonConfig(BrokenModel):
    """Python configuration"""

    version: Annotated[str, Option("--python-version")] = "3.13"
    """https://pyaket.dev/docs/configuration/#python-version"""

    bundle: Annotated[bool, Option("--bundle-python")] = False
    """https://pyaket.dev/docs/configuration/#python-bundle"""

    def export(self) -> None:
        Environment.update(
            PYAKET_PYTHON_VERSION=self.version,
            PYAKET_PYTHON_BUNDLE=self.bundle,
        )

# ---------------------------------------------- #

class AstralConfig(BrokenModel):
    version: Annotated[str, Option("--uv-version")] = "0.6.13"
    """https://pyaket.dev/docs/configuration/#uv-version"""

    bundle: Annotated[bool, Option("--bundle-uv")] = False
    """https://pyaket.dev/docs/configuration/#uv-bundle"""

    def export(self) -> None:
        Environment.update(
            PYAKET_UV_VERSION=self.version,
            PYAKET_UV_BUNDLE=self.bundle,
        )

# ---------------------------------------------- #

class TorchConfig(BrokenModel):
    """Install a PyTorch version at runtime"""

    version: Annotated[str, Option("--torch-version")] = None
    """https://pyaket.dev/docs/configuration/#torch-version"""

    backend: Annotated[str, Option("--torch-backend")] = "auto"
    """https://pyaket.dev/docs/configuration/#torch-backend"""

    def export(self) -> None:
        Environment.update(
            PYAKET_TORCH_VERSION=self.version,
            PYAKET_TORCH_BACKEND=self.backend,
        )

# ---------------------------------------------- #

class EntryConfig(BrokenModel):
    """Define the entry points of the application"""

    module: Annotated[str, Option("--module")] = None
    """https://pyaket.dev/docs/configuration/#entry-module"""

    script: Annotated[Path, Option("--script")] = None
    """https://pyaket.dev/docs/configuration/#entry-script"""

    code: Annotated[str, Option("--code")] = None
    """https://pyaket.dev/docs/configuration/#entry-code"""

    command: Annotated[str, Option("--command")] = None
    """https://pyaket.dev/docs/configuration/#entry-command"""

    def export(self) -> None:
        Environment.update(
            PYAKET_ENTRY_MODULE=self.module,
            PYAKET_ENTRY_SCRIPT=self.script,
            PYAKET_ENTRY_CODE=self.code,
            PYAKET_ENTRY_COMMAND=self.command,
        )

# ---------------------------------------------- #

class BuildConfig(BrokenModel):

    system: Annotated[SystemEnum, Option("--system", "--os", "--target")] = BrokenPlatform.System
    """Target Operating System to build binaries for"""

    arch: Annotated[ArchEnum, Option("--arch")]   = BrokenPlatform.Arch
    """Target Architecture to build binaries for"""

    class Profile(str, BrokenEnum):
        Debug   = "debug"
        Release = "release"
        Small   = "small"

        @property
        def cargo(self) -> str:
            return self.value.replace("debug", "dev")

    profile: Annotated[Profile, Option("--profile")] = Profile.Release
    """Build profile to use"""

    rolling: Annotated[bool, Option("--rolling")] = False
    """https://pyaket.dev/docs/configuration/#rolling"""

    build_dir: Annotated[Path, Option("--build-dir")] = (Path(tempfile.gettempdir())/"pyaket")
    """Directory to build the project"""

    output: Annotated[Path, Option("--output")] = "Release"
    """Directory to output the compiled binary"""

    keep_open: Annotated[bool, Option("--keep-open")] = False
    """Keep the terminal open after errors or finish"""

    standalone: Annotated[bool, Option("--standalone")] = False
    """Create a standalone offline installer"""

    upx: Annotated[bool, Option("--upx")] = False
    """Use UPX to compress the binary"""

    zigbuild: Annotated[bool, Option("--zigbuild")] = False
    """Use Cargo zigbuild to build the binary"""

    msvc: Annotated[bool, Option("--msvc")] = False
    """Use MSVC to build the binary"""

    tarball: Annotated[bool, Option("--tarball")] = False
    """Create a .tar.gz for unix releases (preserves chmod +x)"""

    def export(self) -> None:
        Environment.update(
            PYAKET_ROLLING=self.rolling,
            PYAKET_KEEP_OPEN=self.keep_open,
        )

    @property
    def target(self) -> PlatformEnum:
        return PlatformEnum.from_parts(self.system, self.arch)

    @property
    def triple(self) -> str:
        return self.target.triple

    # # Actions

    def should_zigbuild(self) -> None:
        """Force enable zigbuild in configurations where it's easier"""
        if any((
            BrokenPlatform.OnWindows and (not self.system.is_windows()),
            BrokenPlatform.OnWindows and (self.target == PlatformEnum.WindowsARM64),
            BrokenPlatform.OnLinux and (self.target == PlatformEnum.LinuxARM64),
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
                    if (self.target == PlatformEnum.WindowsAMD64):
                        install_msys2_packages("mingw-w64-x86_64-gcc")
                        BrokenPath.add_to_path(msys2/"ucrt64/bin")

                    elif (self.target == PlatformEnum.WindowsARM64):
                        # Fixme: Almost got it, clang linking errors
                        ...

            # Ensure zig.exe is found
            for path in site.getsitepackages():
                BrokenPath.add_to_path(Path(path)/"ziglang")

        shell("rustup", "target", "add", self.triple)

# ---------------------------------------------- #

@define(eq=False)
class PyaketProject(CodeProject):
    app:    AppConfig    = Factory(AppConfig)
    python: PythonConfig = Factory(PythonConfig)
    astral: AstralConfig = Factory(AstralConfig)
    torch:  TorchConfig  = Factory(TorchConfig)
    entry:  EntryConfig  = Factory(EntryConfig)
    build:  BuildConfig  = Factory(BuildConfig)

    def export_all(self) -> None:
        Environment.update(PYAKET_RELEASE=1)
        self.app.export()
        self.python.export()
        self.astral.export()
        self.torch.export()
        self.entry.export()
        self.build.export()

    def __attrs_post_init__(self):
        self.cli = BrokenTyper(chain=True)

        with self.cli.panel("✅ Configuration"):
            self.cli.command(self.app,    name="app")
            self.cli.command(self.python, name="python")
            self.cli.command(self.astral, name="uv")
            self.cli.command(self.torch,  name="torch")
            self.cli.command(self.entry,  name="entry")
            self.cli.command(self.build,  name="build")

        with self.cli.panel("📦 Actions"):
            self.cli.command(self.compile)

    def compile(self,
        build_dir: Annotated[Path, Option("--build-dir", help="[magenta](Special )[/] Directory to build the project")]=(Path(tempfile.gettempdir())/"pyaket"),
        output:    Annotated[Path, Option("--output",    help="[magenta](Special )[/] Directory to output the compiled binary")]="Release",
    ) -> Path:

        # Fixme: Wait for uv's implementation of pip wheel for my own sanity
        if self.build.standalone and (self.build.target != BrokenPlatform.Host):
            log.error("Standalone releases are best built in a host matching the target platform")
            log.error("• Awaiting implementation of (https://github.com/astral-sh/uv/issues/1681)")
            log.error(f"• Attempted to build for '{self.build.target}' on '{BrokenPlatform.Host}'")
            return None

        self.build.should_zigbuild()
        self.build.install_tools()
        self.export_all()

        # Cargo warning: We're not 'installing' a utility
        BrokenPath.add_to_path(build_dir/"bin")

        if shell(
            "cargo", ("zigbuild" if self.build.zigbuild else "build"),
            "--manifest-path", (PYAKET.PACKAGE/"Cargo.toml"),
            "--target-dir", build_dir,
            "--target", self.build.triple,
            "--profile", self.build.profile.cargo,
            cwd=self.path,
        ).returncode != 0:
            raise RuntimeError(log.error("Failed to compile Pyaket"))

        # Find the compiled binary
        _filename = ("pyaket" + ".exe"*self.build.system.is_windows())
        binary = next((build_dir/self.build.triple/self.build.profile.value).glob(_filename))
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
            f"-{self.build.target.value}",
            f"-v{self.app.version}",
            f"-{self.torch.backend}" if (self.torch.version) else "",
            f"{self.build.target.extension}",
        ))
