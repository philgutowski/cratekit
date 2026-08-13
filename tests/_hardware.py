"""Hardware backed verification fixtures: repeated timing, a FAT volume, a read only volume.

Three fixtures the review wave's remaining units need so they can be verified
against real hardware behavior rather than against doubles:

1. ``time_repeated`` runs a callable a declared number of times and returns a
   ``TimingTable`` holding every duration, the repeat count, and the pass rate
   against a threshold. METHOD's driver rule is that a timing row carries a
   repeat count and a pass rate, never one number, and this runner makes that
   shape the only one it can produce.

2. ``fat_volume`` creates a real FAT32 disk image with hdiutil, mounts it at a
   private mountpoint, and tears it down. U23's adoption work meets FAT on
   every rekordbox USB export, and FAT behavior is not something a temp
   directory on APFS can stand in for.

3. ``read_only_volume`` builds an image, lets the caller populate it while it
   is writable, then remounts it read only. U27's doctor must distinguish a
   volume that is present but not writable from one that is absent, and a
   chmod on a directory is not the same refusal: a read only MOUNT refuses at
   the filesystem with EROFS no matter who asks.

Two facts probed on 2026-08-13, kept here so nobody re-learns them:

- ``newfs_msdos`` cannot lay out FAT32 under roughly 33 MB, and hdiutil
  reports that failure as the misleading summary line "create failed,
  Operation not permitted". ``fat_volume`` therefore refuses sizes under
  ``FAT32_MIN_MB`` with an error that names the real limit.
- The macOS msdos driver ALLOWS symlinks on a mounted FAT volume, so symlink
  refusal is not a usable FAT detector here. Assert the filesystem kind
  through ``filesystem_kind``, which reads the mount table, instead.

Mountpoints are private temp directories, never children of the system mount
root, both so concurrent fixtures cannot collide on a volume name and because
tracked text naming the system mount root would trip the portability scan's
shape patterns.

Timing calibration lives in ``tests/fixtures/timing_calibration.json``,
written by ``scripts/calibrate_timing.py`` on a QUIET machine, never while
other agents run. A threshold for a timing verification is expressed as a
multiple of the calibrated median through ``threshold_seconds``, so the number
in a claim says how much slack it gets relative to the machine that measured
it, not an absolute guess that breaks on the next machine. Recalibrate when
the machine changes.
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from pathlib import Path

CALIBRATION_PATH = Path(__file__).resolve().parent / "fixtures" / "timing_calibration.json"
CALIBRATION_SCHEMA = 1

# newfs_msdos refuses FAT32 below roughly 33 MB. The probe on 2026-08-13 saw a
# 8 MB request die inside hdiutil with a summary line blaming permissions, so
# the floor is enforced here with an error that names the real cause.
FAT32_MIN_MB = 34

_DETACH_ATTEMPTS = 5
_DETACH_WAIT_SECONDS = 0.6


# ---------------------------------------------------------------------------
# Timing: a repeat count and a pass rate, never one number.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TimingTable:
    """One repeated timing measurement, whole.

    Every duration is kept, so a later reader can recompute any summary this
    class offers. The class is frozen because a measurement is a record of
    what happened, not a workspace.
    """

    repeats: int
    threshold_seconds: float
    durations: tuple[float, ...]

    @property
    def passes(self) -> int:
        return sum(1 for d in self.durations if d <= self.threshold_seconds)

    @property
    def pass_rate(self) -> float:
        return self.passes / self.repeats

    @property
    def median_seconds(self) -> float:
        return statistics.median(self.durations)

    @property
    def worst_seconds(self) -> float:
        return max(self.durations)

    def row(self) -> str:
        """The one line a report quotes: count, threshold, rate, median, worst."""
        return (
            f"{self.passes}/{self.repeats} under {self.threshold_seconds:.4f}s "
            f"(pass rate {self.pass_rate:.2f}, median {self.median_seconds:.4f}s, "
            f"worst {self.worst_seconds:.4f}s)"
        )


def time_repeated(
    fn: Callable[[], object],
    *,
    repeats: int,
    threshold_seconds: float,
    clock: Callable[[], float] = time.perf_counter,
) -> TimingTable:
    """Run ``fn`` ``repeats`` times against ``threshold_seconds`` and keep every duration.

    The clock is injectable so the pass rate arithmetic is testable without a
    single real sleep. A repeat count under two is refused because a single
    run is exactly the one number measurement METHOD forbids.
    """
    if repeats < 2:
        raise ValueError(
            f"a timing measurement carries a repeat count, and {repeats} is a single "
            "number wearing a loop; use at least 2, and 25 for a reportable row"
        )
    if threshold_seconds <= 0:
        raise ValueError(f"threshold_seconds must be positive, got {threshold_seconds}")
    durations: list[float] = []
    for _ in range(repeats):
        start = clock()
        fn()
        durations.append(clock() - start)
    return TimingTable(
        repeats=repeats,
        threshold_seconds=threshold_seconds,
        durations=tuple(durations),
    )


def reference_workload() -> int:
    """Fixed interpreter bound work, the yardstick the calibration measures.

    Mostly bytecode dispatch with a periodic sha256 so the number tracks the
    interpreter this suite actually runs on. The amount of work is a constant
    of this file: changing it invalidates every stored calibration, which is
    what ``CALIBRATION_SCHEMA`` exists to version.
    """
    import hashlib

    digest = b"cratekit timing reference"
    total = 0
    for i in range(1_000_000):
        total += i * i
        if i % 100_000 == 0:
            digest = hashlib.sha256(digest).digest()
    return total ^ int.from_bytes(digest[:4], "big")


def calibrate(*, repeats: int = 25) -> dict:
    """Measure the reference workload ``repeats`` times and return the payload to store.

    The payload carries the full spread, not one number, and records only
    machine facts that identify capability rather than a person: interpreter
    version and CPU count, never a hostname, account, or path.
    """
    durations: list[float] = []
    for _ in range(repeats):
        start = time.perf_counter()
        reference_workload()
        durations.append(time.perf_counter() - start)
    med = statistics.median(durations)
    return {
        "schema": CALIBRATION_SCHEMA,
        "captured": date.today().isoformat(),
        "repeats": repeats,
        "workload": "reference_workload, fixed interpreter bound loop with periodic sha256",
        "seconds": {
            "min": min(durations),
            "median": med,
            "mean": statistics.fmean(durations),
            "max": max(durations),
        },
        "relative_spread": (max(durations) - min(durations)) / med,
        "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
    }


@dataclass(frozen=True)
class Calibration:
    """The stored baseline a timing threshold is expressed against."""

    median_seconds: float
    repeats: int
    captured: str
    relative_spread: float


def write_calibration(payload: dict, path: Path = CALIBRATION_PATH) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def load_calibration(path: Path = CALIBRATION_PATH) -> Calibration:
    data = json.loads(path.read_text())
    if data.get("schema") != CALIBRATION_SCHEMA:
        raise ValueError(
            f"calibration schema {data.get('schema')!r} is not {CALIBRATION_SCHEMA}; "
            "re-run scripts/calibrate_timing.py on a quiet machine"
        )
    median_seconds = float(data["seconds"]["median"])
    if median_seconds <= 0:
        raise ValueError(f"calibrated median {median_seconds} is not a duration")
    return Calibration(
        median_seconds=median_seconds,
        repeats=int(data["repeats"]),
        captured=str(data["captured"]),
        relative_spread=float(data["relative_spread"]),
    )


def threshold_seconds(multiplier: float, calibration: Calibration | None = None) -> float:
    """A timing threshold as a multiple of the calibrated median.

    A verification that says ``threshold_seconds(3.0)`` claims the measured
    operation stays within three reference workloads on the machine that
    calibrated, which survives a machine change the way an absolute number
    cannot.
    """
    if multiplier <= 0:
        raise ValueError(f"multiplier must be positive, got {multiplier}")
    cal = calibration if calibration is not None else load_calibration()
    return multiplier * cal.median_seconds


# ---------------------------------------------------------------------------
# Volumes: real images, mounted and torn down.
# ---------------------------------------------------------------------------


def hdiutil_available() -> bool:
    return sys.platform == "darwin" and shutil.which("hdiutil") is not None


def _run(argv: Sequence[str]) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(list(argv), capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"{argv[0]} exited {proc.returncode} for: {' '.join(argv)}\n"
            f"{proc.stderr.strip()}"
        )
    return proc


def _mount_entry(mountpoint: Path) -> str:
    """The parenthesized attribute list the mount table shows for ``mountpoint``.

    The path is resolved first because the temp root this module mounts under
    is reached through a symlink on macOS, and the mount table records the
    real path.
    """
    resolved = str(Path(mountpoint).resolve())
    for line in _run(["mount"]).stdout.splitlines():
        marker = f" on {resolved} ("
        if marker in line:
            return line.split("(", 1)[1].rsplit(")", 1)[0]
    raise LookupError(f"nothing in the mount table is mounted at {resolved}")


def filesystem_kind(mountpoint: Path) -> str:
    """The filesystem kind mounted at ``mountpoint``: msdos, hfs, apfs.

    This is the honest FAT detector. Behavioral probes are weaker than they
    look: the macOS msdos driver allows symlinks, and case folding matches
    the platform default filesystem too.
    """
    return _mount_entry(mountpoint).split(",", 1)[0].strip()


def mount_flags(mountpoint: Path) -> tuple[str, ...]:
    return tuple(part.strip() for part in _mount_entry(mountpoint).split(","))


def _detach(mountpoint: Path) -> None:
    """Detach, retrying briefly, then force.

    A just used mount can hold a straggling reference for a moment, which
    makes the first detach report resource busy. Retries absorb that, and the
    force is last because it is the option that can strand a dirty buffer.
    """
    for _ in range(_DETACH_ATTEMPTS):
        try:
            _run(["hdiutil", "detach", str(mountpoint)])
            return
        except RuntimeError:
            time.sleep(_DETACH_WAIT_SECONDS)
    _run(["hdiutil", "detach", str(mountpoint), "-force"])


@contextmanager
def fat_volume(*, size_mb: int = 64, label: str = "CKFAT") -> Iterator[Path]:
    """A mounted FAT32 volume, yielded as its mountpoint, torn down on exit.

    Teardown detaches the volume and deletes the image whether the body
    returned or raised. The label rules are FAT's own: at most 11 characters,
    uppercase alphanumeric.
    """
    if size_mb < FAT32_MIN_MB:
        raise ValueError(
            f"FAT32 needs at least {FAT32_MIN_MB} MB; newfs_msdos refuses less, and "
            "hdiutil reports that refusal as a misleading permissions failure"
        )
    if not label.isalnum() or label != label.upper() or len(label) > 11:
        raise ValueError(f"a FAT label is at most 11 uppercase alphanumeric characters, got {label!r}")
    workdir = Path(tempfile.mkdtemp(prefix="cratekit-fat-"))
    image = workdir / "volume.dmg"
    mountpoint = workdir / "mnt"
    mountpoint.mkdir()
    try:
        _run(
            [
                "hdiutil", "create", "-size", f"{size_mb}m",
                "-fs", "MS-DOS FAT32", "-volname", label, "-quiet", str(image),
            ]
        )
        _run(["hdiutil", "attach", str(image), "-mountpoint", str(mountpoint), "-nobrowse", "-quiet"])
        try:
            yield mountpoint
        finally:
            _detach(mountpoint)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


@contextmanager
def read_only_volume(
    populate: Callable[[Path], None], *, size_mb: int = 16, label: str = "CKRO"
) -> Iterator[Path]:
    """A really read only volume, populated by the caller, yielded as its mountpoint.

    The image is attached writable exactly once, for ``populate``, then
    remounted with the readonly option. HFS plus is the image format because
    it mounts as a single volume with no container indirection, and what the
    consumers assert is mount level refusal, not filesystem flavor.
    """
    workdir = Path(tempfile.mkdtemp(prefix="cratekit-ro-"))
    image = workdir / "volume.dmg"
    mountpoint = workdir / "mnt"
    mountpoint.mkdir()
    try:
        _run(
            [
                "hdiutil", "create", "-size", f"{size_mb}m",
                "-fs", "HFS+", "-volname", label, "-quiet", str(image),
            ]
        )
        _run(["hdiutil", "attach", str(image), "-mountpoint", str(mountpoint), "-nobrowse", "-quiet"])
        try:
            populate(mountpoint)
        finally:
            _detach(mountpoint)
        _run(
            [
                "hdiutil", "attach", str(image), "-mountpoint", str(mountpoint),
                "-nobrowse", "-readonly", "-quiet",
            ]
        )
        try:
            yield mountpoint
        finally:
            _detach(mountpoint)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
