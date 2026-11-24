"""Hardware backed verification fixtures: repeated timing, a FAT volume, a read only volume.

1. ``time_repeated`` keeps every duration, the repeat count and the pass
   rate, the only shape METHOD's driver rule allows for a timing row.
2. ``fat_volume`` mounts a real FAT32 image, since every rekordbox USB export
   is FAT (U23) and a temp directory on APFS is not.
3. ``read_only_volume`` remounts a populated image read only, since U27's
   doctor must tell an EROFS mount from an absent volume, which chmod cannot.

Probed on 2026-08-13: the macOS msdos driver allows symlinks, so
``filesystem_kind``, reading the mount table, is the FAT detector. Mountpoints
are private temp directories, never under the system mount root.

The calibration, ``tests/fixtures/timing_calibration.json``, is written by
``scripts/calibrate_timing.py`` on a QUIET machine; loading refuses one whose
interpreter or CPU facts are another machine's.
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

# A calibration whose runs spread wider than this was not taken on a quiet
# machine and would loosen every threshold; refused on the write path.
SPREAD_LIMIT = 0.25

# newfs_msdos refuses FAT32 below about 33 MB, and hdiutil blames
# permissions, so the floor is enforced here naming the real cause.
FAT32_MIN_MB = 34

_DETACH_ATTEMPTS = 5
_DETACH_WAIT_SECONDS = 0.6


# ── Timing: a repeat count and a pass rate, never one number. ────────────────


@dataclass(frozen=True)
class TimingTable:
    """One repeated timing measurement, whole and frozen, every duration kept."""

    repeats: int
    threshold_seconds: float
    durations: tuple[float, ...]

    def __post_init__(self) -> None:
        # The constructor is public, so the record holds its own invariant: the
        # headline count agrees with the evidence.
        if self.repeats < 1 or self.repeats != len(self.durations):
            raise ValueError(
                f"repeats is {self.repeats} but {len(self.durations)} durations were "
                "recorded; a timing record carries exactly the runs it measured"
            )

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
            f"{self.passes}/{self.repeats} within {self.threshold_seconds:.4f}s "
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

    The clock is injectable; fewer than two repeats is the one-number
    measurement METHOD forbids.
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

    Changing the amount of work invalidates every stored calibration, which
    ``CALIBRATION_SCHEMA`` versions.
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

    The full spread, and machine facts only (interpreter version, CPU count),
    never a hostname, account or path.
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
    python_version: str
    cpu_count: int


def write_calibration(payload: dict, path: Path = CALIBRATION_PATH, *, force: bool = False) -> None:
    """Store a calibration, refusing a noisy spread unless a human passes ``force``."""
    spread = float(payload["relative_spread"])
    if spread > SPREAD_LIMIT and not force:
        raise ValueError(
            f"relative spread {spread:.3f} is over {SPREAD_LIMIT}, so this machine was "
            "not quiet; rerun on a quiet machine, or force past this refusal knowingly"
        )
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def load_calibration(path: Path = CALIBRATION_PATH) -> Calibration:
    """Load a stored calibration, refusing one another machine wrote (interpreter, CPU count)."""
    data = json.loads(path.read_text())
    if data.get("schema") != CALIBRATION_SCHEMA:
        raise ValueError(
            f"calibration schema {data.get('schema')!r} is not {CALIBRATION_SCHEMA}; "
            "re-run scripts/calibrate_timing.py on a quiet machine"
        )
    median_seconds = float(data["seconds"]["median"])
    if median_seconds <= 0:
        raise ValueError(f"calibrated median {median_seconds} is not a duration")
    stored_python = str(data["python"])
    stored_cpus = int(data["cpu_count"])
    running_python = platform.python_version()
    running_cpus = os.cpu_count()
    same_interpreter = stored_python.split(".")[:2] == running_python.split(".")[:2]
    if not same_interpreter or stored_cpus != running_cpus:
        raise ValueError(
            f"this calibration was captured on python {stored_python} with "
            f"{stored_cpus} CPUs and this machine runs python {running_python} with "
            f"{running_cpus}; a baseline from a different machine sizes every "
            "threshold wrongly, so re-run scripts/calibrate_timing.py here"
        )
    return Calibration(
        median_seconds=median_seconds,
        repeats=int(data["repeats"]),
        captured=str(data["captured"]),
        relative_spread=float(data["relative_spread"]),
        python_version=stored_python,
        cpu_count=stored_cpus,
    )


def threshold_seconds(multiplier: float, calibration: Calibration | None = None) -> float:
    """A timing threshold as a multiple of the calibrated median, surviving a machine change."""
    if multiplier <= 0:
        raise ValueError(f"multiplier must be positive, got {multiplier}")
    cal = calibration if calibration is not None else load_calibration()
    return multiplier * cal.median_seconds


# ── Volumes: real images, mounted and torn down. ─────────────────────────────


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


def _scratch(prefix: str) -> tuple[Path, Path, Path]:
    """A private workdir, the image path inside it and its made mountpoint."""
    workdir = Path(tempfile.mkdtemp(prefix=prefix))
    mountpoint = workdir / "mnt"
    mountpoint.mkdir()
    return workdir, workdir / "volume.dmg", mountpoint


def _create(image: Path, size_mb: int, filesystem: str, label: str) -> None:
    _run(
        [
            "hdiutil", "create", "-size", f"{size_mb}m",
            "-fs", filesystem, "-volname", label, "-quiet", str(image),
        ]
    )


def _attach(image: Path, mountpoint: Path, *flags: str) -> None:
    _run(["hdiutil", "attach", str(image), "-mountpoint", str(mountpoint), "-nobrowse", *flags, "-quiet"])


def _mount_entry(mountpoint: Path) -> str:
    """The parenthesized attribute list the mount table shows for ``mountpoint``.

    Resolved first, since macOS reaches the temp root through a symlink. A line
    reads ``device on path (attrs)``, the path compared EXACTLY up to the LAST
    group, since macOS mounts a duplicate label at ``NAME (1)``.
    """
    resolved = str(Path(mountpoint).resolve())
    for line in _run(["mount"]).stdout.splitlines():
        if " on " not in line or not line.endswith(")"):
            continue
        rest = line.split(" on ", 1)[1]
        attrs_at = rest.rfind(" (")
        if attrs_at < 0:
            continue
        path = rest[:attrs_at]
        if path == resolved:
            return rest[attrs_at + 2 : -1]
    raise LookupError(f"nothing in the mount table is mounted at {resolved}")


def filesystem_kind(mountpoint: Path) -> str:
    """The filesystem kind mounted at ``mountpoint``: msdos, hfs, apfs; the honest FAT detector."""
    return _mount_entry(mountpoint).split(",", 1)[0].strip()


def mount_flags(mountpoint: Path) -> tuple[str, ...]:
    return tuple(part.strip() for part in _mount_entry(mountpoint).split(","))


def _detach(mountpoint: Path) -> None:
    """Detach, retrying briefly for a straggling reference, then force.

    Force can strand a dirty buffer, which is why ``read_only_volume`` verifies
    its content after the remount.
    """
    for _ in range(_DETACH_ATTEMPTS):
        try:
            _run(["hdiutil", "detach", str(mountpoint)])
            return
        except RuntimeError:
            time.sleep(_DETACH_WAIT_SECONDS)
    _run(["hdiutil", "detach", str(mountpoint), "-force"])


def _remove_workdir(workdir: Path, mountpoint: Path) -> None:
    """Delete the fixture's scratch, but never through a live mount.

    An rmtree over an attached volume would delete its contents and the backing
    image and swallow the error; the workdir is left as evidence instead.
    """
    if not os.path.ismount(mountpoint):
        shutil.rmtree(workdir, ignore_errors=True)


# Directories the platform writes onto a volume itself, ignored at the top
# level so the manifest pins only what ``populate`` declared.
_PLATFORM_NOISE = frozenset(
    {".fseventsd", ".Spotlight-V100", ".Trashes", ".TemporaryItems", ".DS_Store"}
)


def _content_manifest(root: Path) -> dict[str, str]:
    """Every file under ``root`` mapped to its content digest, platform noise excluded."""
    import hashlib

    manifest: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if relative.parts[0] in _PLATFORM_NOISE:
            continue
        if path.is_file():
            manifest[str(relative)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return manifest


@contextmanager
def fat_volume(*, size_mb: int = 64, label: str = "CKFAT") -> Iterator[Path]:
    """A mounted FAT32 volume at its mountpoint, torn down on exit, FAT labels."""
    if size_mb < FAT32_MIN_MB:
        raise ValueError(
            f"FAT32 needs at least {FAT32_MIN_MB} MB; newfs_msdos refuses less, and "
            "hdiutil reports that refusal as a misleading permissions failure"
        )
    if not label.isalnum() or label != label.upper() or len(label) > 11:
        raise ValueError(f"a FAT label is at most 11 uppercase alphanumeric characters, got {label!r}")
    workdir, image, mountpoint = _scratch("cratekit-fat-")
    try:
        _create(image, size_mb, "MS-DOS FAT32", label)
        _attach(image, mountpoint)
        try:
            yield mountpoint
        finally:
            _detach(mountpoint)
    finally:
        _remove_workdir(workdir, mountpoint)


@contextmanager
def read_only_volume(
    populate: Callable[[Path], None], *, size_mb: int = 16, label: str = "CKRO"
) -> Iterator[Path]:
    """A really read only volume, populated by the caller, yielded as its mountpoint.

    HFS plus, since it mounts as a single volume. What ``populate`` wrote is
    fingerprinted before the detach and verified after the readonly remount,
    since a forced detach can strand unflushed data.
    """
    workdir, image, mountpoint = _scratch("cratekit-ro-")
    try:
        _create(image, size_mb, "HFS+", label)
        _attach(image, mountpoint)
        try:
            populate(mountpoint)
            declared = _content_manifest(mountpoint)
            os.sync()
        finally:
            _detach(mountpoint)
        _attach(image, mountpoint, "-readonly")
        try:
            served = _content_manifest(mountpoint)
            if served != declared:
                missing = sorted(set(declared) - set(served))
                changed = sorted(
                    name for name in set(declared) & set(served) if declared[name] != served[name]
                )
                raise RuntimeError(
                    "the readonly remount does not serve what populate declared; "
                    f"missing: {missing or 'none'}; changed: {changed or 'none'}"
                )
            yield mountpoint
        finally:
            _detach(mountpoint)
    finally:
        _remove_workdir(workdir, mountpoint)
