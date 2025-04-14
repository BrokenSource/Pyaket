import shutil
import tempfile
from pathlib import Path
from typing import Annotated

from attrs import define
from typer import Option

from Broken import (
    ArchEnum,
    BrokenEnum,
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


class PyaketProfile(str, BrokenEnum):
    Debug   = "dev"
    Release = "release"
    Small   = "small"

# Aliases for formatting
_Pro = PyaketProfile
_Sys = SystemEnum
_Arc = ArchEnum


@define(eq=False)
class PyaketProject(CodeProject):
    def __attrs_post_init__(self):
        self.cli = BrokenTyper()
        self.cli.command(target=self.compile)

    # Todo: Maybe a PyDantic model for the CLI and Config file?
    def compile(self,
        system:         Annotated[_Sys, Option("--os",             help="[red](Platform)[/] Target Operating System to build binaries for")]=BrokenPlatform.System,
        arch:           Annotated[_Arc, Option("--arch",           help="[red](Platform)[/] Target Architecture to build binaries for")]=BrokenPlatform.Arch,
        tarball:        Annotated[bool, Option("--tarball",        help="[red](Platform)[/] Create a .tar.gz for unix releases (preserves chmod +x)")]=False,
        app_name:       Annotated[str,  Option("--name",           help="[orange3](Metadata)[/] Name of the application")]="Pyaket",
        app_author:     Annotated[str,  Option("--author",         help="[orange3](Metadata)[/] Author of the application")]="BrokenSource",
        app_version:    Annotated[str,  Option("--version",        help="[orange3](Metadata)[/] Version of the application")]="0.0.0",
        app_subdir:     Annotated[str,  Option("--subdir",         help="[orange3](Metadata)[/] Subdirectory to install versions")]=None,
        app_wheels:     Annotated[str,  Option("--wheels",         help="[yellow](Packages)[/] Wheels/sdists to bundle and install at runtime")]=None,
        app_pypi:       Annotated[str,  Option("--pypi",           help="[yellow](Packages)[/] Dependencies to bundle and install at runtime")]=None,
        app_reqtxt:     Annotated[str,  Option("--requirements",   help="[yellow](Packages)[/] requirements.txt to bundle and install at runtime")]=None,
        python_version: Annotated[str,  Option("--python-version", help="[spring_green3](Python  )[/] Python version to use at runtime")]="3.13",
        python_bundle:  Annotated[bool, Option("--bundle-python",  help="[spring_green3](Python  )[/] Bundle the Python interpreter in the executable")]=False,
        uv_version:     Annotated[str,  Option("--uv-version",     help="[spring_green3](AstralUV)[/] Version of uv to use")]="0.6.13",
        uv_bundle:      Annotated[bool, Option("--bundle-uv",      help="[spring_green3](AstralUV)[/] Bundle the uv runtime in the executable")]=False,
        torch_version:  Annotated[str,  Option("--torch-version",  help="[spring_green3](Torch   )[/] Version of PyTorch to use")]=None,
        torch_backend:  Annotated[str,  Option("--torch-backend",  help="[spring_green3](Torch   )[/] Backend to use from")]="auto",
        entry_module:   Annotated[str,  Option("--module",         help="[blue](Entry   )[/] Entry module to run at runtime as 'python -m module'")]=None,
        entry_script:   Annotated[Path, Option("--script",         help="[blue](Entry   )[/] Entry script to run at runtime as 'python script.py'")]=None,
        entry_code:     Annotated[str,  Option("--code",           help="[blue](Entry   )[/] Entry code to run at runtime as 'python -c (code)'")]=None,
        entry_command:  Annotated[str,  Option("--command",        help="[blue](Entry   )[/] Entry command to run at runtime as '(command)'")]=None,
        profile:        Annotated[_Pro, Option("--profile",        help="[magenta](Special )[/] Build profile to use")]=PyaketProfile.Release,
        rolling:        Annotated[bool, Option("--rolling",        help="[magenta](Special )[/] Create a rolling release")]=False,
        build_dir:      Annotated[Path, Option("--build-dir",      help="[magenta](Special )[/] Directory to build the project")]=(Path(tempfile.gettempdir())/"pyaket"),
        output:         Annotated[Path, Option("--output",         help="[magenta](Special )[/] Directory to output the compiled binary")]="Release",
        keep_open:      Annotated[bool, Option("--keep-open",      help="[magenta](Special )[/] Keep the terminal open after errors or finish")]=False,
        standalone:     Annotated[bool, Option("--standalone",     help="[magenta](Special )[/] Create a standalone offline installer")]=False,
        upx:            Annotated[bool, Option("--upx",            help="[magenta](Special )[/] Use UPX to compress the binary")]=False,
    ) -> Path:

        # Build the target platform enum from options
        platform = PlatformEnum.get(f"{system.value}-{arch.value}")
        shell("rustup", "target", "add", platform.triple)

        # Filter problematic or invalid (Host -> Target) combinations
        if BrokenPlatform.OnLinux and (platform.system.is_macos()):
            return log.skip(f"Linux can't [italic]easily[/] compile for {platform.system}")
        elif BrokenPlatform.OnMacOS and (not platform.system.is_macos()):
            return log.skip("macOS can only [italic]easily[/] compile for itself")
        elif BrokenPlatform.OnWindows and (not platform.system.is_windows()):
            return log.skip("Windows can only [italic]easily[/] compile for itself")
        elif (platform == PlatformEnum.WindowsARM64):
            return log.skip("Windows on ARM is not supported yet")

        # Fixme: Wait for uv's implementation of pip wheel for my own sanity
        if standalone and (platform != BrokenPlatform.Host):
            log.error("Standalone releases are best built in a host matching the target platform")
            log.error("• Awaiting implementation of (https://github.com/astral-sh/uv/issues/1681)")
            log.error(f"• Attempted to build for '{platform.value}' on '{BrokenPlatform.Host.value}'")
            return None

        Environment.update(
            # Passthrough configuration variables
            PYAKET_APP_NAME       = app_name,
            PYAKET_APP_AUTHOR     = app_author,
            PYAKET_APP_VERSION    = app_version,
            PYAKET_VERSIONS_DIR   = app_subdir,
            PYAKET_APP_WHEELS     = app_wheels,
            PYAKET_APP_PYPI       = app_pypi,
            PYAKET_APP_REQTXT     = app_reqtxt,
            PYAKET_PYTHON_VERSION = python_version,
            PYAKET_PYTHON_BUNDLE  = python_bundle,
            PYAKET_UV_VERSION     = uv_version,
            PYAKET_UV_BUNDLE      = uv_bundle,
            PYAKET_TORCH_VERSION  = torch_version,
            PYAKET_TORCH_BACKEND  = torch_backend,
            PYAKET_ENTRY_MODULE   = entry_module,
            PYAKET_ENTRY_SCRIPT   = entry_script,
            PYAKET_ENTRY_CODE     = entry_code,
            PYAKET_ENTRY_COMMAND  = entry_command,
            PYAKET_ROLLING        = rolling,
            PYAKET_KEEP_OPEN      = keep_open,
            # Notify build hooks to pin dependencies
            PYAKET_RELEASE=1,
            # Minor fixes to cross compilation
            CARGO_TARGET_AARCH64_UNKNOWN_LINUX_GNU_LINKER=shutil.which("aarch64-linux-gnu-gcc"),
        )

        # Cargo warning: We're not 'installing' a utility
        BrokenPath.add_to_path(build_dir/"bin")

        if shell(
            "cargo", "install",
            "--path", PYAKET.PACKAGE,
            "--root", build_dir,
            "--target", platform.triple,
            "--profile", profile.value,
            cwd=self.path,
        ).returncode != 0:
            raise RuntimeError(log.error("Failed to compile Pyaket"))

        # Find the compiled binary
        binary = next((build_dir/"bin").glob("pyaket*"))
        log.info(f"Compiled Pyaket binary at ({binary})")
        BrokenPath.make_executable(binary)

        # Rename the compiled binary to the final release name
        release_path = output / ''.join((
            f"{self.name.lower()}",
            f"-{platform.value}",
            f"-v{app_version}",
            f"-{torch_backend}" if (torch_version and standalone) else "",
            f"{platform.extension}",
        ))
        BrokenPath.copy(src=binary, dst=release_path)
        BrokenPath.make_executable(release_path)

        # Compress the final release with upx
        if upx and (shell("upx", "--best", "--lzma", release_path).returncode != 0):
            raise RuntimeError(log.error("Failed to compress executable with upx"))

        # Release a tar.gz to keep chmod +x attributes
        if tarball and (not platform.system.is_windows()):
            release_path = BrokenPath.gzip(release_path, remove=True)

        log.success(f"Built Project release at ({release_path})")
        return release_path
