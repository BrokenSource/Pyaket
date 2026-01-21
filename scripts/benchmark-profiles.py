"""
1. Please ensure your idle cpu usage is minimal before benchmarking:
  - Set power profile/cpu governor to 'performance' mode
  - Close all unnecessary applications

2. Required tools:
  - [hyperfine](https://github.com/sharkdp/hyperfine)
  - Host-specific rust compiling dependencies

Tests are made and run for the host target only

Estimated total time:
- Ryzen 9 5900X: ~25 minutes
- Apple M2 Pro:  ~30 minutes
"""
import contextlib
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Self

from attrs import Factory, define
from pyaket import (
    PYAKET_CARGO,
    CargoProfile,
    PyaketBuild,
    PyaketProject,
)


@contextlib.contextmanager
def stopwatch(self) -> callable:
    start = time.perf_counter()
    yield lambda: time.perf_counter() - start

@define
class Benchmark:
    profile: CargoProfile
    cold: float = 0.0
    warm: float = 0.0
    size: float = 0.0

    baseline: dict = Factory(dict)
    overhead: dict = Factory(dict)

    def run(self) -> Self:
        project = PyaketProject()
        project.build.profile = self.profile
        subprocess.check_call(("rustup", "default", "stable"))
        subprocess.check_call(("rustup", "update", "stable"))
        subprocess.check_call(("cargo", "fetch", "--manifest-path", str(PYAKET_CARGO)))
        subprocess.check_call(("cargo", "clean", "--manifest-path", str(PYAKET_CARGO)))

        # Cold compilation
        with stopwatch(self) as took:
            release = project.compile()
        self.cold = took()

        # Warm compilation
        with stopwatch(self) as took:
            release = project.compile()
        self.warm = took()

        # Measure size (Yes, 1000 for MB, 1024 for MiB)
        self.size = len(release.read_bytes()) / (1000 * 1000)

        # Measure overhead
        self.baseline = self.hyperfine(sys.executable, "-c", "")
        self.overhead = self.hyperfine(release, "-c", "")

        return self

    def hyperfine(self,
        *benchmark: str,
        warmup: int=50,
        runs: int=100
    ) -> dict:
        command = tuple()

        # Linux/macOS can set niceness
        if sys.platform in ("linux", "darwin"):
            command += ("nice", "-20")

        # Linux can pin to a specific core
        # - Reduce jitter by avoiding migrations (core, ccd)
        # - Avoid core 0 as it may handle kernel interrupts
        # - Find second physical core, as core 1 might be SMT/HT
        if sys.platform == "linux":
            for cpu in Path("/sys/devices/system/cpu").glob("cpu[0-9]*"):
                if int((cpu/"topology"/"core_id").read_text()) == 1:
                    command += ("taskset", "--cpu", cpu.name.removeprefix("cpu"))
                    break

        # Convert arguments to shell string
        benchmark = ' '.join(f'"{x}"' for x in benchmark)

        with tempfile.NamedTemporaryFile(
            prefix="pyaket-hyperfine-",
            suffix=".json",
            mode="w+b",
        ) as results:
            subprocess.check_call((
                "hyperfine",
                "--warmup", str(warmup),
                "--runs", str(runs),
                "--shell=none",
                "--export-json",
                str(results.name),
                benchmark
            ))

            results.seek(0)
            return json.load(results)

    @property
    def mean(self) -> float:
        return sum((
            self.overhead["results"][0]["mean"],
            self.baseline["results"][0]["mean"]*(-1),
        ))

@define
class Benchmarker:
    samples: list[Benchmark] = Factory(list)

    def run(self) -> None:
        for profile in CargoProfile:
            benchmark =Benchmark(profile=profile).run()
            self.samples.append(benchmark)
            self.table()

    def table(self) -> str:
        print(f"### {PyaketBuild.host()}")
        print("")
        print("| Profile  | Size     | Startup | Cold    | Warm    |")
        print("| :------- | -------: | ------: | ------: | ------: |")
        for sample in self.samples:
            print((
                f"| {sample.profile.value.ljust(8)} "
                f"| {sample.size:5.2f} MB "
                f"| {sample.mean*1000:4.1f} ms "
                f"| {sample.cold:5.1f} s "
                f"| {sample.warm:5.1f} s |"
            ))

if __name__ == "__main__":
    app = Benchmarker()
    app.run()
