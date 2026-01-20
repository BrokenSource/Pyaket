import json
import os
import subprocess
from enum import Enum
from functools import cache
from pathlib import Path
from typing import Iterable, Optional, Self

from dotmap import DotMap

from pyaket import PYAKET_RESOURCES

# Last sync (json + enum): Rust 1.95.0-nightly (2026-01-18)

TARGET_SPECS_JSON: Path = (PYAKET_RESOURCES/"targets.json")
"""Json file with all rust target specs"""

TARGET_SPECS: DotMap = DotMap(json.loads(TARGET_SPECS_JSON.read_text("utf-8")))
"""Dictionary from `rustc -Z unstable-options --print all-target-specs-json`"""

class Target(str, Enum):
    """
    Exhaustive list and utilities for Rust target triples.

    [Reference](https://doc.rust-lang.org/stable/rustc/platform-support.html)
    """

    # -------------------------------- #
    # Meta

    @cache
    @staticmethod
    def host() -> Self:
        """Get the current host triple"""
        if (value := os.getenv("PYAKET_HOST_TRIPLE")):
            return Target(value)
        return Target(subprocess.run(
            ("rustc", "--print", "host-tuple"),
            capture_output=True, text=True
        ).stdout.strip())

    # -------------------------------- #
    # Specifications

    @property
    def spec(self) -> DotMap:
        """Same as `rustc --print target-spec-json --target <this>`"""
        return TARGET_SPECS[self.value]

    @property
    def description(self) -> str:
        """Human-readable description of this target"""
        return self.spec.metadata.description

    @property
    def tier(self) -> int:
        """Support tier level for this target"""
        return self.spec.metadata.tier

    @property
    def stdlib(self) -> bool:
        """Does this target have rust stdlib available?"""
        return bool(self.spec.metadata.std)

    @property
    def host_tools(self) -> bool:
        """Does this target support compiling rust?"""
        return bool(self.spec.metadata.host_tools)

    # -------------------------------- #
    # Operating Systems

    def is_windows(self) -> bool:
        return (self.spec.os == "windows")

    def is_linux(self) -> bool:
        return (self.spec.os == "linux")

    def is_macos(self) -> bool:
        return (self.spec.os == "macos")

    def is_bsd(self) -> bool:
        return self.spec.os in ("freebsd", "netbsd", "openbsd")

    def is_unix(self) -> bool:
        return any((
            self.is_linux(),
            self.is_macos(),
            self.is_bsd(),
        ))

    # -------------------------------- #
    # Architectures

    # Intel x86

    def is_x86_32(self) -> bool:
        return (self.spec.arch == "x86")

    def is_x86_64(self) -> bool:
        return (self.spec.arch == "x86_64")

    def is_x86(self) -> bool:
        return self.spec.arch.startswith("x86")

    # ARM

    def is_arm(self) -> bool:
        # for prefix in ("aarch", "arm", "thumbv"):
        #     if self.value.startswith(prefix):
        #         return True
        # return False
        ...

    # RISC-V

    ...

    # -------------------------------- #

    @classmethod
    def wheel(cls) -> Optional[str]:
        """Best-effort for a matching python wheel platform tag"""
        return {
            cls.aarch64_apple_darwin:          "macosx_11_0_arm64",
            cls.x86_64_apple_darwin:           "macosx_10_9_x86_64",
            cls.aarch64_unknown_linux_gnu:     "manylinux2014_aarch64",
            cls.aarch64_unknown_linux_musl:    "musllinux_1_1_aarch64",
            cls.x86_64_unknown_linux_gnu:      "manylinux2014_x86_64",
            cls.x86_64_unknown_linux_musl:     "musllinux_1_1_x86_64",
            cls.i686_unknown_linux_gnu:        "manylinux2014_i686",
            cls.i686_unknown_linux_musl:       "musllinux_1_1_i686",
            cls.x86_64_pc_windows_gnu:         "win_amd64",
            cls.x86_64_pc_windows_msvc:        "win_amd64",
            cls.i686_pc_windows_gnu:           "win32",
            cls.i686_pc_windows_msvc:          "win32",
            cls.arm_unknown_linux_gnueabi:     "manylinux2014_armv7l",
            cls.arm_unknown_linux_gnueabihf:   "manylinux2014_armv7l",
            cls.armv7_unknown_linux_gnueabihf: "manylinux2014_armv7l",
            cls.armv7_unknown_linux_musleabi:  "musllinux_1_1_armv7l",
            # ...
        }.get(cls)

    # ------------------------------------------------------------------------ #
    # Lists

    @classmethod
    def uv_list(cls) -> Iterable[Self]:
        """
        List of targets that astral-sh/uv provides prebuilt binaries for
        - All are known to be buildable in their workflows
        - Full list might be overkill for python apps
        """
        yield from (
            cls.aarch64_apple_darwin,
            cls.aarch64_pc_windows_msvc,
            cls.aarch64_unknown_linux_gnu,
            cls.aarch64_unknown_linux_musl,
            cls.arm_unknown_linux_musleabihf,
            cls.armv7_unknown_linux_gnueabihf,
            cls.armv7_unknown_linux_musleabi,
            cls.i686_pc_windows_msvc,
            cls.i686_unknown_linux_gnu,
            cls.i686_unknown_linux_musl,
            cls.powerpc64_unknown_linux_gnu,
            cls.powerpc64le_unknown_linux_gnu,
            cls.riscv64gc_unknown_linux_gnu,
            cls.s390x_unknown_linux_gnu,
            cls.x86_64_apple_darwin,
            cls.x86_64_pc_windows_msvc,
            cls.x86_64_unknown_linux_gnu,
            cls.x86_64_unknown_linux_musl,
        )

    @cache
    def in_uv_list(self) -> bool:
        return self in self.uv_list()

    @classmethod
    def recommended(cls) -> Iterable[Self]:
        """
        Recommended targets for pyaket binaries distributions
        - Covers all major desktop platforms (OSs, Archs)
        - Known to be easily buildable in workflows
        """
        yield from (
            cls.aarch64_apple_darwin,
            cls.aarch64_unknown_linux_gnu,
            cls.x86_64_apple_darwin,
            cls.x86_64_pc_windows_gnu,
            cls.x86_64_unknown_linux_gnu,
        )

    @cache
    def in_recommended_list(self) -> bool:
        return self in self.recommended()

    # ------------------------------------------------------------------------ #
    # Last generation: Rust 1.92.0

    aarch64_apple_darwin                 = "aarch64-apple-darwin"
    aarch64_apple_ios                    = "aarch64-apple-ios"
    aarch64_apple_ios_macabi             = "aarch64-apple-ios-macabi"
    aarch64_apple_ios_sim                = "aarch64-apple-ios-sim"
    aarch64_apple_tvos                   = "aarch64-apple-tvos"
    aarch64_apple_tvos_sim               = "aarch64-apple-tvos-sim"
    aarch64_apple_visionos               = "aarch64-apple-visionos"
    aarch64_apple_visionos_sim           = "aarch64-apple-visionos-sim"
    aarch64_apple_watchos                = "aarch64-apple-watchos"
    aarch64_apple_watchos_sim            = "aarch64-apple-watchos-sim"
    aarch64_kmc_solid_asp3               = "aarch64-kmc-solid_asp3"
    aarch64_linux_android                = "aarch64-linux-android"
    aarch64_nintendo_switch_freestanding = "aarch64-nintendo-switch-freestanding"
    aarch64_pc_windows_gnullvm           = "aarch64-pc-windows-gnullvm"
    aarch64_pc_windows_msvc              = "aarch64-pc-windows-msvc"
    aarch64_unknown_freebsd              = "aarch64-unknown-freebsd"
    aarch64_unknown_fuchsia              = "aarch64-unknown-fuchsia"
    aarch64_unknown_helenos              = "aarch64-unknown-helenos"
    aarch64_unknown_hermit               = "aarch64-unknown-hermit"
    aarch64_unknown_illumos              = "aarch64-unknown-illumos"
    aarch64_unknown_linux_gnu            = "aarch64-unknown-linux-gnu"
    aarch64_unknown_linux_gnu_ilp32      = "aarch64-unknown-linux-gnu_ilp32"
    aarch64_unknown_linux_musl           = "aarch64-unknown-linux-musl"
    aarch64_unknown_linux_ohos           = "aarch64-unknown-linux-ohos"
    aarch64_unknown_managarm_mlibc       = "aarch64-unknown-managarm-mlibc"
    aarch64_unknown_netbsd               = "aarch64-unknown-netbsd"
    aarch64_unknown_none                 = "aarch64-unknown-none"
    aarch64_unknown_none_softfloat       = "aarch64-unknown-none-softfloat"
    aarch64_unknown_nto_qnx700           = "aarch64-unknown-nto-qnx700"
    aarch64_unknown_nto_qnx710           = "aarch64-unknown-nto-qnx710"
    aarch64_unknown_nto_qnx710_iosock    = "aarch64-unknown-nto-qnx710_iosock"
    aarch64_unknown_nto_qnx800           = "aarch64-unknown-nto-qnx800"
    aarch64_unknown_nuttx                = "aarch64-unknown-nuttx"
    aarch64_unknown_openbsd              = "aarch64-unknown-openbsd"
    aarch64_unknown_redox                = "aarch64-unknown-redox"
    aarch64_unknown_teeos                = "aarch64-unknown-teeos"
    aarch64_unknown_trusty               = "aarch64-unknown-trusty"
    aarch64_unknown_uefi                 = "aarch64-unknown-uefi"
    aarch64_uwp_windows_msvc             = "aarch64-uwp-windows-msvc"
    aarch64_wrs_vxworks                  = "aarch64-wrs-vxworks"
    aarch64_be_unknown_hermit            = "aarch64_be-unknown-hermit"
    aarch64_be_unknown_linux_gnu         = "aarch64_be-unknown-linux-gnu"
    aarch64_be_unknown_linux_gnu_ilp32   = "aarch64_be-unknown-linux-gnu_ilp32"
    aarch64_be_unknown_linux_musl        = "aarch64_be-unknown-linux-musl"
    aarch64_be_unknown_netbsd            = "aarch64_be-unknown-netbsd"
    aarch64_be_unknown_none_softfloat    = "aarch64_be-unknown-none-softfloat"
    amdgcn_amd_amdhsa                    = "amdgcn-amd-amdhsa"
    arm_linux_androideabi                = "arm-linux-androideabi"
    arm_unknown_linux_gnueabi            = "arm-unknown-linux-gnueabi"
    arm_unknown_linux_gnueabihf          = "arm-unknown-linux-gnueabihf"
    arm_unknown_linux_musleabi           = "arm-unknown-linux-musleabi"
    arm_unknown_linux_musleabihf         = "arm-unknown-linux-musleabihf"
    arm64_32_apple_watchos               = "arm64_32-apple-watchos"
    arm64e_apple_darwin                  = "arm64e-apple-darwin"
    arm64e_apple_ios                     = "arm64e-apple-ios"
    arm64e_apple_tvos                    = "arm64e-apple-tvos"
    arm64ec_pc_windows_msvc              = "arm64ec-pc-windows-msvc"
    armeb_unknown_linux_gnueabi          = "armeb-unknown-linux-gnueabi"
    armebv7r_none_eabi                   = "armebv7r-none-eabi"
    armebv7r_none_eabihf                 = "armebv7r-none-eabihf"
    armv4t_none_eabi                     = "armv4t-none-eabi"
    armv4t_unknown_linux_gnueabi         = "armv4t-unknown-linux-gnueabi"
    armv5te_none_eabi                    = "armv5te-none-eabi"
    armv5te_unknown_linux_gnueabi        = "armv5te-unknown-linux-gnueabi"
    armv5te_unknown_linux_musleabi       = "armv5te-unknown-linux-musleabi"
    armv5te_unknown_linux_uclibceabi     = "armv5te-unknown-linux-uclibceabi"
    armv6_unknown_freebsd                = "armv6-unknown-freebsd"
    armv6_unknown_netbsd_eabihf          = "armv6-unknown-netbsd-eabihf"
    armv6k_nintendo_3ds                  = "armv6k-nintendo-3ds"
    armv7_linux_androideabi              = "armv7-linux-androideabi"
    armv7_rtems_eabihf                   = "armv7-rtems-eabihf"
    armv7_sony_vita_newlibeabihf         = "armv7-sony-vita-newlibeabihf"
    armv7_unknown_freebsd                = "armv7-unknown-freebsd"
    armv7_unknown_linux_gnueabi          = "armv7-unknown-linux-gnueabi"
    armv7_unknown_linux_gnueabihf        = "armv7-unknown-linux-gnueabihf"
    armv7_unknown_linux_musleabi         = "armv7-unknown-linux-musleabi"
    armv7_unknown_linux_musleabihf       = "armv7-unknown-linux-musleabihf"
    armv7_unknown_linux_ohos             = "armv7-unknown-linux-ohos"
    armv7_unknown_linux_uclibceabi       = "armv7-unknown-linux-uclibceabi"
    armv7_unknown_linux_uclibceabihf     = "armv7-unknown-linux-uclibceabihf"
    armv7_unknown_netbsd_eabihf          = "armv7-unknown-netbsd-eabihf"
    armv7_unknown_trusty                 = "armv7-unknown-trusty"
    armv7_wrs_vxworks_eabihf             = "armv7-wrs-vxworks-eabihf"
    armv7a_kmc_solid_asp3_eabi           = "armv7a-kmc-solid_asp3-eabi"
    armv7a_kmc_solid_asp3_eabihf         = "armv7a-kmc-solid_asp3-eabihf"
    armv7a_none_eabi                     = "armv7a-none-eabi"
    armv7a_none_eabihf                   = "armv7a-none-eabihf"
    armv7a_nuttx_eabi                    = "armv7a-nuttx-eabi"
    armv7a_nuttx_eabihf                  = "armv7a-nuttx-eabihf"
    armv7a_vex_v5                        = "armv7a-vex-v5"
    armv7k_apple_watchos                 = "armv7k-apple-watchos"
    armv7r_none_eabi                     = "armv7r-none-eabi"
    armv7r_none_eabihf                   = "armv7r-none-eabihf"
    armv7s_apple_ios                     = "armv7s-apple-ios"
    armv8r_none_eabihf                   = "armv8r-none-eabihf"
    avr_none                             = "avr-none"
    bpfeb_unknown_none                   = "bpfeb-unknown-none"
    bpfel_unknown_none                   = "bpfel-unknown-none"
    csky_unknown_linux_gnuabiv2          = "csky-unknown-linux-gnuabiv2"
    csky_unknown_linux_gnuabiv2hf        = "csky-unknown-linux-gnuabiv2hf"
    hexagon_unknown_linux_musl           = "hexagon-unknown-linux-musl"
    hexagon_unknown_none_elf             = "hexagon-unknown-none-elf"
    hexagon_unknown_qurt                 = "hexagon-unknown-qurt"
    i386_apple_ios                       = "i386-apple-ios"
    i586_unknown_linux_gnu               = "i586-unknown-linux-gnu"
    i586_unknown_linux_musl              = "i586-unknown-linux-musl"
    i586_unknown_netbsd                  = "i586-unknown-netbsd"
    i586_unknown_redox                   = "i586-unknown-redox"
    i686_apple_darwin                    = "i686-apple-darwin"
    i686_linux_android                   = "i686-linux-android"
    i686_pc_nto_qnx700                   = "i686-pc-nto-qnx700"
    i686_pc_windows_gnu                  = "i686-pc-windows-gnu"
    i686_pc_windows_gnullvm              = "i686-pc-windows-gnullvm"
    i686_pc_windows_msvc                 = "i686-pc-windows-msvc"
    i686_unknown_freebsd                 = "i686-unknown-freebsd"
    i686_unknown_haiku                   = "i686-unknown-haiku"
    i686_unknown_helenos                 = "i686-unknown-helenos"
    i686_unknown_hurd_gnu                = "i686-unknown-hurd-gnu"
    i686_unknown_linux_gnu               = "i686-unknown-linux-gnu"
    i686_unknown_linux_musl              = "i686-unknown-linux-musl"
    i686_unknown_netbsd                  = "i686-unknown-netbsd"
    i686_unknown_openbsd                 = "i686-unknown-openbsd"
    i686_unknown_uefi                    = "i686-unknown-uefi"
    i686_uwp_windows_gnu                 = "i686-uwp-windows-gnu"
    i686_uwp_windows_msvc                = "i686-uwp-windows-msvc"
    i686_win7_windows_gnu                = "i686-win7-windows-gnu"
    i686_win7_windows_msvc               = "i686-win7-windows-msvc"
    i686_wrs_vxworks                     = "i686-wrs-vxworks"
    loongarch32_unknown_none             = "loongarch32-unknown-none"
    loongarch32_unknown_none_softfloat   = "loongarch32-unknown-none-softfloat"
    loongarch64_unknown_linux_gnu        = "loongarch64-unknown-linux-gnu"
    loongarch64_unknown_linux_musl       = "loongarch64-unknown-linux-musl"
    loongarch64_unknown_linux_ohos       = "loongarch64-unknown-linux-ohos"
    loongarch64_unknown_none             = "loongarch64-unknown-none"
    loongarch64_unknown_none_softfloat   = "loongarch64-unknown-none-softfloat"
    m68k_unknown_linux_gnu               = "m68k-unknown-linux-gnu"
    m68k_unknown_none_elf                = "m68k-unknown-none-elf"
    mips_mti_none_elf                    = "mips-mti-none-elf"
    mips_unknown_linux_gnu               = "mips-unknown-linux-gnu"
    mips_unknown_linux_musl              = "mips-unknown-linux-musl"
    mips_unknown_linux_uclibc            = "mips-unknown-linux-uclibc"
    mips64_openwrt_linux_musl            = "mips64-openwrt-linux-musl"
    mips64_unknown_linux_gnuabi64        = "mips64-unknown-linux-gnuabi64"
    mips64_unknown_linux_muslabi64       = "mips64-unknown-linux-muslabi64"
    mips64el_unknown_linux_gnuabi64      = "mips64el-unknown-linux-gnuabi64"
    mips64el_unknown_linux_muslabi64     = "mips64el-unknown-linux-muslabi64"
    mipsel_mti_none_elf                  = "mipsel-mti-none-elf"
    mipsel_sony_psp                      = "mipsel-sony-psp"
    mipsel_sony_psx                      = "mipsel-sony-psx"
    mipsel_unknown_linux_gnu             = "mipsel-unknown-linux-gnu"
    mipsel_unknown_linux_musl            = "mipsel-unknown-linux-musl"
    mipsel_unknown_linux_uclibc          = "mipsel-unknown-linux-uclibc"
    mipsel_unknown_netbsd                = "mipsel-unknown-netbsd"
    mipsel_unknown_none                  = "mipsel-unknown-none"
    mipsisa32r6_unknown_linux_gnu        = "mipsisa32r6-unknown-linux-gnu"
    mipsisa32r6el_unknown_linux_gnu      = "mipsisa32r6el-unknown-linux-gnu"
    mipsisa64r6_unknown_linux_gnuabi64   = "mipsisa64r6-unknown-linux-gnuabi64"
    mipsisa64r6el_unknown_linux_gnuabi64 = "mipsisa64r6el-unknown-linux-gnuabi64"
    msp430_none_elf                      = "msp430-none-elf"
    nvptx64_nvidia_cuda                  = "nvptx64-nvidia-cuda"
    powerpc_unknown_freebsd              = "powerpc-unknown-freebsd"
    powerpc_unknown_helenos              = "powerpc-unknown-helenos"
    powerpc_unknown_linux_gnu            = "powerpc-unknown-linux-gnu"
    powerpc_unknown_linux_gnuspe         = "powerpc-unknown-linux-gnuspe"
    powerpc_unknown_linux_musl           = "powerpc-unknown-linux-musl"
    powerpc_unknown_linux_muslspe        = "powerpc-unknown-linux-muslspe"
    powerpc_unknown_netbsd               = "powerpc-unknown-netbsd"
    powerpc_unknown_openbsd              = "powerpc-unknown-openbsd"
    powerpc_wrs_vxworks                  = "powerpc-wrs-vxworks"
    powerpc_wrs_vxworks_spe              = "powerpc-wrs-vxworks-spe"
    powerpc64_ibm_aix                    = "powerpc64-ibm-aix"
    powerpc64_unknown_freebsd            = "powerpc64-unknown-freebsd"
    powerpc64_unknown_linux_gnu          = "powerpc64-unknown-linux-gnu"
    powerpc64_unknown_linux_musl         = "powerpc64-unknown-linux-musl"
    powerpc64_unknown_openbsd            = "powerpc64-unknown-openbsd"
    powerpc64_wrs_vxworks                = "powerpc64-wrs-vxworks"
    powerpc64le_unknown_freebsd          = "powerpc64le-unknown-freebsd"
    powerpc64le_unknown_linux_gnu        = "powerpc64le-unknown-linux-gnu"
    powerpc64le_unknown_linux_musl       = "powerpc64le-unknown-linux-musl"
    riscv32_wrs_vxworks                  = "riscv32-wrs-vxworks"
    riscv32e_unknown_none_elf            = "riscv32e-unknown-none-elf"
    riscv32em_unknown_none_elf           = "riscv32em-unknown-none-elf"
    riscv32emc_unknown_none_elf          = "riscv32emc-unknown-none-elf"
    riscv32gc_unknown_linux_gnu          = "riscv32gc-unknown-linux-gnu"
    riscv32gc_unknown_linux_musl         = "riscv32gc-unknown-linux-musl"
    riscv32i_unknown_none_elf            = "riscv32i-unknown-none-elf"
    riscv32im_risc0_zkvm_elf             = "riscv32im-risc0-zkvm-elf"
    riscv32im_unknown_none_elf           = "riscv32im-unknown-none-elf"
    riscv32ima_unknown_none_elf          = "riscv32ima-unknown-none-elf"
    riscv32imac_esp_espidf               = "riscv32imac-esp-espidf"
    riscv32imac_unknown_none_elf         = "riscv32imac-unknown-none-elf"
    riscv32imac_unknown_nuttx_elf        = "riscv32imac-unknown-nuttx-elf"
    riscv32imac_unknown_xous_elf         = "riscv32imac-unknown-xous-elf"
    riscv32imafc_esp_espidf              = "riscv32imafc-esp-espidf"
    riscv32imafc_unknown_none_elf        = "riscv32imafc-unknown-none-elf"
    riscv32imafc_unknown_nuttx_elf       = "riscv32imafc-unknown-nuttx-elf"
    riscv32imc_esp_espidf                = "riscv32imc-esp-espidf"
    riscv32imc_unknown_none_elf          = "riscv32imc-unknown-none-elf"
    riscv32imc_unknown_nuttx_elf         = "riscv32imc-unknown-nuttx-elf"
    riscv64_linux_android                = "riscv64-linux-android"
    riscv64_wrs_vxworks                  = "riscv64-wrs-vxworks"
    riscv64a23_unknown_linux_gnu         = "riscv64a23-unknown-linux-gnu"
    riscv64gc_unknown_freebsd            = "riscv64gc-unknown-freebsd"
    riscv64gc_unknown_fuchsia            = "riscv64gc-unknown-fuchsia"
    riscv64gc_unknown_hermit             = "riscv64gc-unknown-hermit"
    riscv64gc_unknown_linux_gnu          = "riscv64gc-unknown-linux-gnu"
    riscv64gc_unknown_linux_musl         = "riscv64gc-unknown-linux-musl"
    riscv64gc_unknown_managarm_mlibc     = "riscv64gc-unknown-managarm-mlibc"
    riscv64gc_unknown_netbsd             = "riscv64gc-unknown-netbsd"
    riscv64gc_unknown_none_elf           = "riscv64gc-unknown-none-elf"
    riscv64gc_unknown_nuttx_elf          = "riscv64gc-unknown-nuttx-elf"
    riscv64gc_unknown_openbsd            = "riscv64gc-unknown-openbsd"
    riscv64gc_unknown_redox              = "riscv64gc-unknown-redox"
    riscv64im_unknown_none_elf           = "riscv64im-unknown-none-elf"
    riscv64imac_unknown_none_elf         = "riscv64imac-unknown-none-elf"
    riscv64imac_unknown_nuttx_elf        = "riscv64imac-unknown-nuttx-elf"
    s390x_unknown_linux_gnu              = "s390x-unknown-linux-gnu"
    s390x_unknown_linux_musl             = "s390x-unknown-linux-musl"
    sparc_unknown_linux_gnu              = "sparc-unknown-linux-gnu"
    sparc_unknown_none_elf               = "sparc-unknown-none-elf"
    sparc64_unknown_helenos              = "sparc64-unknown-helenos"
    sparc64_unknown_linux_gnu            = "sparc64-unknown-linux-gnu"
    sparc64_unknown_netbsd               = "sparc64-unknown-netbsd"
    sparc64_unknown_openbsd              = "sparc64-unknown-openbsd"
    sparcv9_sun_solaris                  = "sparcv9-sun-solaris"
    thumbv4t_none_eabi                   = "thumbv4t-none-eabi"
    thumbv5te_none_eabi                  = "thumbv5te-none-eabi"
    thumbv6m_none_eabi                   = "thumbv6m-none-eabi"
    thumbv6m_nuttx_eabi                  = "thumbv6m-nuttx-eabi"
    thumbv7a_nuttx_eabi                  = "thumbv7a-nuttx-eabi"
    thumbv7a_nuttx_eabihf                = "thumbv7a-nuttx-eabihf"
    thumbv7a_pc_windows_msvc             = "thumbv7a-pc-windows-msvc"
    thumbv7a_uwp_windows_msvc            = "thumbv7a-uwp-windows-msvc"
    thumbv7em_none_eabi                  = "thumbv7em-none-eabi"
    thumbv7em_none_eabihf                = "thumbv7em-none-eabihf"
    thumbv7em_nuttx_eabi                 = "thumbv7em-nuttx-eabi"
    thumbv7em_nuttx_eabihf               = "thumbv7em-nuttx-eabihf"
    thumbv7m_none_eabi                   = "thumbv7m-none-eabi"
    thumbv7m_nuttx_eabi                  = "thumbv7m-nuttx-eabi"
    thumbv7neon_linux_androideabi        = "thumbv7neon-linux-androideabi"
    thumbv7neon_unknown_linux_gnueabihf  = "thumbv7neon-unknown-linux-gnueabihf"
    thumbv7neon_unknown_linux_musleabihf = "thumbv7neon-unknown-linux-musleabihf"
    thumbv8m_base_none_eabi              = "thumbv8m.base-none-eabi"
    thumbv8m_base_nuttx_eabi             = "thumbv8m.base-nuttx-eabi"
    thumbv8m_main_none_eabi              = "thumbv8m.main-none-eabi"
    thumbv8m_main_none_eabihf            = "thumbv8m.main-none-eabihf"
    thumbv8m_main_nuttx_eabi             = "thumbv8m.main-nuttx-eabi"
    thumbv8m_main_nuttx_eabihf           = "thumbv8m.main-nuttx-eabihf"
    wasm32_unknown_emscripten            = "wasm32-unknown-emscripten"
    wasm32_unknown_unknown               = "wasm32-unknown-unknown"
    wasm32_wali_linux_musl               = "wasm32-wali-linux-musl"
    wasm32_wasip1                        = "wasm32-wasip1"
    wasm32_wasip1_threads                = "wasm32-wasip1-threads"
    wasm32_wasip2                        = "wasm32-wasip2"
    wasm32_wasip3                        = "wasm32-wasip3"
    wasm32v1_none                        = "wasm32v1-none"
    wasm64_unknown_unknown               = "wasm64-unknown-unknown"
    x86_64_apple_darwin                  = "x86_64-apple-darwin"
    x86_64_apple_ios                     = "x86_64-apple-ios"
    x86_64_apple_ios_macabi              = "x86_64-apple-ios-macabi"
    x86_64_apple_tvos                    = "x86_64-apple-tvos"
    x86_64_apple_watchos_sim             = "x86_64-apple-watchos-sim"
    x86_64_fortanix_unknown_sgx          = "x86_64-fortanix-unknown-sgx"
    x86_64_linux_android                 = "x86_64-linux-android"
    x86_64_lynx_lynxos178                = "x86_64-lynx-lynxos178"
    x86_64_pc_cygwin                     = "x86_64-pc-cygwin"
    x86_64_pc_nto_qnx710                 = "x86_64-pc-nto-qnx710"
    x86_64_pc_nto_qnx710_iosock          = "x86_64-pc-nto-qnx710_iosock"
    x86_64_pc_nto_qnx800                 = "x86_64-pc-nto-qnx800"
    x86_64_pc_solaris                    = "x86_64-pc-solaris"
    x86_64_pc_windows_gnu                = "x86_64-pc-windows-gnu"
    x86_64_pc_windows_gnullvm            = "x86_64-pc-windows-gnullvm"
    x86_64_pc_windows_msvc               = "x86_64-pc-windows-msvc"
    x86_64_unikraft_linux_musl           = "x86_64-unikraft-linux-musl"
    x86_64_unknown_dragonfly             = "x86_64-unknown-dragonfly"
    x86_64_unknown_freebsd               = "x86_64-unknown-freebsd"
    x86_64_unknown_fuchsia               = "x86_64-unknown-fuchsia"
    x86_64_unknown_haiku                 = "x86_64-unknown-haiku"
    x86_64_unknown_helenos               = "x86_64-unknown-helenos"
    x86_64_unknown_hermit                = "x86_64-unknown-hermit"
    x86_64_unknown_hurd_gnu              = "x86_64-unknown-hurd-gnu"
    x86_64_unknown_illumos               = "x86_64-unknown-illumos"
    x86_64_unknown_l4re_uclibc           = "x86_64-unknown-l4re-uclibc"
    x86_64_unknown_linux_gnu             = "x86_64-unknown-linux-gnu"
    x86_64_unknown_linux_gnux32          = "x86_64-unknown-linux-gnux32"
    x86_64_unknown_linux_musl            = "x86_64-unknown-linux-musl"
    x86_64_unknown_linux_none            = "x86_64-unknown-linux-none"
    x86_64_unknown_linux_ohos            = "x86_64-unknown-linux-ohos"
    x86_64_unknown_managarm_mlibc        = "x86_64-unknown-managarm-mlibc"
    x86_64_unknown_motor                 = "x86_64-unknown-motor"
    x86_64_unknown_netbsd                = "x86_64-unknown-netbsd"
    x86_64_unknown_none                  = "x86_64-unknown-none"
    x86_64_unknown_openbsd               = "x86_64-unknown-openbsd"
    x86_64_unknown_redox                 = "x86_64-unknown-redox"
    x86_64_unknown_trusty                = "x86_64-unknown-trusty"
    x86_64_unknown_uefi                  = "x86_64-unknown-uefi"
    x86_64_uwp_windows_gnu               = "x86_64-uwp-windows-gnu"
    x86_64_uwp_windows_msvc              = "x86_64-uwp-windows-msvc"
    x86_64_win7_windows_gnu              = "x86_64-win7-windows-gnu"
    x86_64_win7_windows_msvc             = "x86_64-win7-windows-msvc"
    x86_64_wrs_vxworks                   = "x86_64-wrs-vxworks"
    x86_64h_apple_darwin                 = "x86_64h-apple-darwin"
    xtensa_esp32_espidf                  = "xtensa-esp32-espidf"
    xtensa_esp32_none_elf                = "xtensa-esp32-none-elf"
    xtensa_esp32s2_espidf                = "xtensa-esp32s2-espidf"
    xtensa_esp32s2_none_elf              = "xtensa-esp32s2-none-elf"
    xtensa_esp32s3_espidf                = "xtensa-esp32s3-espidf"
    xtensa_esp32s3_none_elf              = "xtensa-esp32s3-none-elf"

# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    import re
    import subprocess

    # Must have nightly toolchain for print all-target-specs-json
    subprocess.check_call(("rustup", "set", "profile", "minimal"))
    subprocess.check_call(("rustup", "default", "nightly"))
    subprocess.check_call((
        "rustc", "-Z", "unstable-options",
        "--print", "all-target-specs-json",
        "-o", str(TARGET_SPECS_JSON),
    ))

    # Generate and print enum entries
    targets: dict = json.loads(TARGET_SPECS_JSON.read_text())
    longest: int  = max(map(len, targets.keys()))

    for target in targets:
        key: str = re.sub(r"[-\.]", "_", target).ljust(longest)
        print(f'{key} = "{target}"')
