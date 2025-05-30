import subprocess
import tempfile
from pathlib import Path
from typing import Annotated

from attr import Factory, define
from typer import Option

from broken import (
    ArchEnum,
    BrokenEnum,
    BrokenModel,
    BrokenPath,
    BrokenPlatform,
    BrokenTyper,
    Environment,
    PlatformEnum,
    Runtime,
    SystemEnum,
    Tools,
    log,
    shell,
)
from pyaket import PYAKET, PYAKET_ABOUT

# ---------------------------------------------- #

class Application(BrokenModel):
    """
    General metadata and dependencies definitions of the project

    • [Documentation](https://pyaket.dev/docs#app)
    """

    name: Annotated[str, Option("--name", "-n")] = "pyaket"
    """
    The application name, used for

    • [Documentation](https://pyaket.dev/docs#app-name)
    """

    author: Annotated[str, Option("--author", "-a")] = "brokensource"
    """
    Subdirectory of the platform's user data directory to install the application

    • [Documentation](https://pyaket.dev/docs#app-author)
    """

    version: Annotated[str, Option("--version", "-v")] = "0.0.0"
    """
    The release version matching PyPI, codename, branch, latest, etc.

    • [Documentation](https://pyaket.dev/docs#app-version)
    """

    wheels: Annotated[list[Path], Option("--wheel", "-w")] = []
    """
    List of wheels to bundle and install at runtime, supports glob patterns.

    • [Documentation](https://pyaket.dev/docs#app-wheels)
    """

    pypi: Annotated[list[str], Option("--pypi", "-p")] = []
    """
    List of dependencies to install at runtime from PyPI, plain or pinned.

    • [Documentation](https://pyaket.dev/docs#app-pypi)
    """

    reqtxt: Annotated[Path, Option("--requirements", "-r")] = None
    """
    Path to a requirements.txt to install at runtime (legacy)

    • [Documentation](https://pyaket.dev/docs#app-requirements-txt)
    """

    rolling: Annotated[bool, Option("--rolling")] = False
    """
    Always upgrade dependencies at startup for a rolling-release mechanism

    • [Documentation](https://pyaket.dev/docs#rolling)
    """

    keep_open: Annotated[bool, Option("--keep-open", "-k")] = False
    """
    Keep the terminal open after errors or finish

    • [Documentation](https://pyaket.dev/docs#keep-open)
    """

    @property
    def r_wheels(self) -> str:
        """Gets all self.wheels as absolute paths"""
        return ';'.join(map(str, map(BrokenPath.get, self.wheels)))

    @property
    def r_pypi(self) -> str:
        return ';'.join(map(str, self.pypi))

# ---------------------------------------------- #

class Directories(BrokenModel):

    common: Annotated[str, Option("--common", "-c")] = "pyaket"
    """
    Subdirectory of the workspace to use for all installed files

    • [Documentation](https://pyaket.dev/docs#common-dir)
    """

    versions: Annotated[str, Option("--versions", "-v")] = "versions"
    """
    Subdirectory of the common dir to install versions of the application

    • [Documentation](https://pyaket.dev/docs#versions-dir)
    """

# ---------------------------------------------- #

class Python(BrokenModel):
    """
    Configuration for a Python interpreter to use for the project

    • [Documentation](https://pyaket.dev/docs#python)
    """

    version: Annotated[str, Option("--version", "-v")] = "3.13"
    """
    A target python version to use at runtime

    • [Documentation](https://pyaket.dev/docs#python-version)
    """

    bundle: Annotated[bool, Option("--bundle", "-b")] = False
    """
    Whether to bundle the python distribution in the executable

    • [Documentation](https://pyaket.dev/docs#python-bundle)
    """

# ---------------------------------------------- #

class Astral(BrokenModel):
    """
    Configuration for uv project and package manager to use

    • [Documentation](https://pyaket.dev/docs#uv)
    """

    version: Annotated[str, Option("--version", "-v")] = "0.7.9"
    """
    A target uv version to use at runtime

    • [Documentation](https://pyaket.dev/docs#uv-version)
    """

    bundle: Annotated[bool, Option("--bundle", "-b")] = False
    """
    Whether to bundle uv in the executable

    • [Documentation](https://pyaket.dev/docs#uv-bundle)
    """

# ---------------------------------------------- #

class Torch(BrokenModel):
    """
    Optional configuration to install PyTorch at runtime

    • [Documentation](https://pyaket.dev/docs#pytorch)
    """

    version: Annotated[str, Option("--version", "-v")] = None
    """
    A target torch version to use at runtime, empty disables it

    • [Documentation](https://pyaket.dev/docs#torch-version)
    """

    backend: Annotated[str, Option("--backend", "-b")] = "auto"
    """

    • [Documentation](https://pyaket.dev/docs#torch-backend)
    """

# ---------------------------------------------- #

class Entry(BrokenModel):
    """
    Configuration for the entry point of the application

    • [Documentation](https://pyaket.dev/docs#entry-points)
    """

    module: Annotated[str, Option("--module", "-m")] = None
    """
    A module to run at runtime as (python -m module ...)

    • [Documentation](https://pyaket.dev/docs#entry-module)
    """

    script: Annotated[Path, Option("--script", "-f")] = None
    """
    A script to bundle and run at runtime (python script.py ...)

    • [Documentation](https://pyaket.dev/docs#entry-script)
    """

    code: Annotated[str, Option("--code", "-c")] = None
    """
    A inline code snippet to run at runtime (python -c "code")

    • [Documentation](https://pyaket.dev/docs#entry-code)
    """

    command: Annotated[str, Option("--command", "-x")] = None
    """
    A command to run at runtime (command ...)

    • [Documentation](https://pyaket.dev/docs#entry-command)
    """

# ---------------------------------------------- #

class Release(BrokenModel):
    """
    Release configuration for the application
    """

    system: Annotated[SystemEnum, Option("--target", "-t")] = BrokenPlatform.System
    """Target Operating System to build binaries for"""

    arch: Annotated[ArchEnum, Option("--arch", "-a")] = BrokenPlatform.Arch
    """Target Architecture to build binaries for"""

    @property
    def platform(self) -> PlatformEnum:
        return PlatformEnum.from_parts(self.system, self.arch)

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
    """(Windows) Use MSVC to build the binary"""

    tarball: Annotated[bool, Option("--tarball", "-x")] = False
    """(Unix   ) Create a .tar.gz for unix releases (preserves chmod +x)"""

    @property
    def triple(self) -> str:
        return self.platform.triple()

    # # Actions

    def should_zigbuild(self) -> None:
        """Force enable zigbuild in configurations where it's easier"""
        if Environment.flag("AUTO_ZIGBUILD", 1) and any((
            BrokenPlatform.OnWindows and (not self.system.is_windows()),
            BrokenPlatform.OnWindows and (self.platform == PlatformEnum.WindowsARM64),
            BrokenPlatform.OnLinux   and (self.platform == PlatformEnum.LinuxARM64),
            BrokenPlatform.OnLinux   and (self.system.is_macos()),
        )):
            log.note("Force enabling Zigbuild for cross compilation")
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
                        Environment.add_to_path(msys2/"ucrt64/bin")

                    elif (self.platform == PlatformEnum.WindowsARM64):
                        # Fixme: Almost got it, clang linking errors
                        ...

        elif BrokenPlatform.OnLinux:
            get = Environment.flag("AUTO_PACKAGES")

            # Need MinGW64 for cross compilation
            if get and (self.target == PlatformEnum.WindowsAMD64):
                if BrokenPlatform.ArchLike:
                    shell("sudo", "pacman", "-S", "mingw-w64-toolchain")
                elif BrokenPlatform.UbuntuLike:
                    shell("sudo", "apt", "install", "mingw-w64")
            if get and (self.target == PlatformEnum.WindowsAMD64):
                if BrokenPlatform.ArchLike:
                    # Todo: Is it https://aur.archlinux.org/packages/mingw-w64-llvm (fat) ?
                    shell("yay", "-S", "mingw-w64-llvm", "--noconfirm", skip=1)

# ---------------------------------------------- #

class RustToolchain(str, BrokenEnum):
    Stable  = "stable"
    Nightly = "nightly"

# ---------------------------------------------- #

@define
class PyaketProject:
    app:     Application = Factory(Application)
    dirs:    Directories = Factory(Directories)
    python:  Python      = Factory(Python)
    astral:  Astral      = Factory(Astral)
    torch:   Torch       = Factory(Torch)
    entry:   Entry       = Factory(Entry)
    release: Release     = Factory(Release)

    cli: BrokenTyper = None

    def __attrs_post_init__(self):
        self.cli = BrokenTyper(chain=True, help=False)
        self.cli.description = PYAKET_ABOUT

        with self.cli.panel("🚀 Core"):
            self.cli.command(self.install_rust, name="rust")

        with self.cli.panel("🔴 Project"):
            self.cli.command(self.app,   name="app")
            self.cli.command(self.entry, name="run")

        with self.cli.panel("🟡 Dependencies"):
            self.cli.command(self.python, name="python")
            self.cli.command(self.astral, name="uv")
            self.cli.command(self.torch,  name="torch")

        with self.cli.panel("🟢 Building"):
            self.cli.command(self.release, name="release")
            self.cli.command(self.compile)

        with self.cli.panel("🔵 Special"):
            self.cli.command(self.build, name="build")

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
        if (BrokenPlatform.OnWindows and build_tools):
            log.warn("You must have Microsoft Visual C++ Build Tools installed to compile Rust projects")
            log.warn("• Will try installing it, you might need to restart your shell, good luck!")
            shell("winget", "install", "-e", "--id", "Microsoft.VisualStudio.2022.BuildTools", "--override", (
                " --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64"
                " --add Microsoft.VisualStudio.Component.Windows10SDK"
                " --add Microsoft.VisualStudio.Component.Windows11SDK"
                "--wait --passive"
            ))

        shell("rustup-init", "-y")

    def build(self,
        standalone: Annotated[bool, Option("--standalone", "-s")]=False,
        all:        Annotated[bool, Option("--all",        "-a")]=False,
    ):
        """Build wheels for the project and bundle them on the executable"""
        wheels: Path = BrokenPath.recreate(PYAKET.DIRECTORIES.DATA/"Wheels")
        shell(Tools.uv, "build", "--wheel", ("--all-packages"*all), "-o", wheels)
        self.app.wheels.extend(wheels.glob("*.whl"))

    def compile(self,
        cache:  Annotated[Path, Option("--cache",  "-c", help="Directory to build the project")]=(Path.cwd()/"target"),
        output: Annotated[Path, Option("--output", "-o", help="Directory to output the compiled binary")]=(Path.cwd()/"release"),
    ) -> Path:
        output = BrokenPath.get(output)

        # Fixme: Wait for uv's implementation of pip wheel for my own sanity
        if self.release.standalone and (self.release.platform != BrokenPlatform.Host):
            log.error("Standalone releases are best built in a host matching the target platform")
            log.error("• Awaiting implementation of (https://github.com/astral-sh/uv/issues/1681)")
            log.error(f"• Attempted to build for '{self.release.platform}' on '{BrokenPlatform.Host}'")
            return None

        shell("rustup", "install", "stable")
        shell("rustup", "default", "stable")
        shell("rustup", "target", "add", self.release.triple)

        self.release.should_zigbuild()
        self.release.install_tools()
        self.export()

        try:
            if self.release.zigbuild:
                import ziglang # noqa
        except ImportError:
            raise RuntimeError("Missing group 'pip install pyaket[cross]' for cross compilation")

        if shell(
            "cargo", ("zig"*self.release.zigbuild) + "build",
            "--manifest-path", (PYAKET.PACKAGE/"Cargo.toml"),
            "--profile", self.release.profile.cargo,
            "--target", self.release.triple,
            "--target-dir", cache,
        ).returncode != 0:
            raise RuntimeError(log.error("Failed to compile Pyaket"))

        # Find the compiled binary
        _filename = ("pyaket" + (".exe"*self.release.system.is_windows()))
        binary = next((cache/self.release.triple/self.release.profile.value).glob(_filename))
        log.info(f"Compiled Pyaket binary at ({binary})")

        # Rename the compiled binary to the final release name
        release_path = (output / self.release_name)
        BrokenPath.mkdir(release_path.parent)
        BrokenPath.move(src=binary, dst=release_path, echo=False)
        BrokenPath.make_executable(release_path)

        # Compress the final release with upx
        if self.release.upx and (shell("upx", "--best", "--lzma", release_path).returncode != 0):
            raise RuntimeError(log.error("Failed to compress executable with upx"))

        # Release a tar.gz to keep chmod +x attributes
        if self.release.tarball and (not self.release.system.is_windows()):
            release_path = BrokenPath.gzip(release_path, remove=True)

        log.ok(f"Built Project release at ({release_path})")
        return release_path

    @property
    def release_name(self) -> str:
        return ''.join((
            f"{self.app.name.lower()}",
            f"-{self.release.platform.value}",
            f"-v{self.app.version}",
            f"-{self.torch.backend}" if (self.torch.version) else "",
            f"{self.release.platform.extension}",
        ))

    def export(self) -> None:
        Environment.update(
            PYAKET_RELEASE        = 1,
            PYAKET_APP_NAME       = self.app.name,
            PYAKET_APP_VERSION    = self.app.version,
            PYAKET_APP_AUTHOR     = self.app.author,
            PYAKET_APP_WHEELS     = self.app.r_wheels,
            PYAKET_APP_PYPI       = self.app.r_pypi,
            PYAKET_APP_REQTXT     = self.app.reqtxt,
            PYAKET_APP_ROLLING    = self.app.rolling,
            PYAKET_KEEP_OPEN      = self.app.keep_open,
            PYAKET_VERSIONS_DIR   = self.dirs.versions,
            PYAKET_PYTHON_VERSION = self.python.version,
            PYAKET_PYTHON_BUNDLE  = self.python.bundle,
            PYAKET_UV_VERSION     = self.astral.version,
            PYAKET_UV_BUNDLE      = self.astral.bundle,
            PYAKET_TORCH_VERSION  = self.torch.version,
            PYAKET_TORCH_BACKEND  = self.torch.backend,
            PYAKET_ENTRY_MODULE   = self.entry.module,
            PYAKET_ENTRY_SCRIPT   = self.entry.script,
            PYAKET_ENTRY_CODE     = self.entry.code,
            PYAKET_ENTRY_COMMAND  = self.entry.command,
        )
