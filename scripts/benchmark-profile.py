"""
Please ensure your idle cpu usage is minimal before benchmarking:
- Set power mode/governor to 'performance'
- Close all unnecessary applications

Tests are made and run for the host target only

Estimated total time:
- Ryzen 9 5900X: ~25 minutes
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
    PyaketProject,
    PyaketRelease,
)


@contextlib.contextmanager
def stopwatch(self) -> callable:
    start = time.perf_counter()
    yield lambda: time.perf_counter() - start

@define
class Benchmark:
    profile: PyaketRelease.Profile
    cold: float = 0.0
    warm: float = 0.0
    over: float = 0.0
    size: float = 0.0

    def run(self, warmup: int=50, runs: int=100) -> Self:
        project = PyaketProject()
        project.release.profile = self.profile
        subprocess.check_call(("rustup", "default", "stable"))
        subprocess.check_call(("cargo", "clean", "--manifest-path", str(PYAKET_CARGO)))

        # # Cold compilation

        with stopwatch(self) as took:
            release = project.compile()
        self.cold = took()

        # # # Warm compilation

        with stopwatch(self) as took:
            release = project.compile()
        self.warm = took()

        # # Measure size (Yes, 1000 for MB, 1024 for MiB)

        self.size = len(release.read_bytes()) / (1000 * 1000)

        # # Measure overhead

        command = tuple()

        # Linux/macOS can set niceness
        if sys.platform in ("linux", "darwin"):
            command += ("nice", "-20")

        # Linux can pin to a specific core
        # - Reduce jitter by avoiding core/ccd migrations
        # - Avoid core 0 as it may handle kernel interrupts
        # - Find physical second core, as core 1 might be SMT/HT
        if sys.platform == "linux":
            for cpu in Path("/sys/devices/system/cpu").glob("cpu[0-9]*"):
                if int((cpu/"topology"/"core_id").read_text()) == 1:
                    command += ("taskset", "--cpu", cpu.name.removeprefix("cpu"))
                    break

        # Actual benchmark
        with tempfile.NamedTemporaryFile(
            prefix="pyaket-benchmark-",
            suffix=".json",
            mode="w+b",
        ) as result:
            subprocess.check_call(command + (
                "hyperfine",
                "--warmup", str(warmup),
                "--runs", str(runs),
                "--shell=none",
                "--export-json",
                str(result.name),
                str(release),
            ))

            result.seek(0)
            result: dict = json.load(result)
            self.over = result["results"][0]["mean"]

        return self

@define
class Benchmarker:
    samples: list[Benchmark] = Factory(list)

    def run(self) -> None:
        for profile in PyaketRelease.Profile:
            benchmark =Benchmark(profile=profile).run()
            self.samples.append(benchmark)
            self.table()

    def table(self) -> str:
        print(f"### {PyaketRelease.host()}")
        print("")
        print("| Profile  | Size     | Startup | Cold    | Warm    |")
        print("| :------- | --------:| ------: | ------: | ------: |")
        for sample in self.samples:
            print((
                f"| {sample.profile.value.ljust(8)} |"
                f" {sample.size:5.2f} MB |"
                f" {sample.over*1000:4.1f} ms |"
                f" {sample.cold:5.1f} s |"
                f" {sample.warm:5.1f} s |"
            ))

if __name__ == "__main__":
    app = Benchmarker()
    app.run()
