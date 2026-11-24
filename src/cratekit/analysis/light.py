"""Pass A: tempo, drift, energy, and no key since U343. Wide pool, no vocal model.

The count comes from plan_pool. A ProcessPoolExecutor of our own would be a
second answer to R23.

WHAT A LIGHT WORKER COSTS IS MEASURED, AND IT IS NOT SMALL (U241): a line in
the track's length, declared at the Mac's steeper slope (U275) so no machine is
planned wider than its peaks, from the COSTLIEST track in the batch. A length
the header will not give is bounded by the file's size.

THE DECODE IS ITS OWN LINE, at the file's own rate and channels before the mix
down: most of the worker for a 192 kilohertz file. A worker costs the larger.

THE CEILING IS THE CORES LESS TWO, one for the driver and one for the machine,
handed to the planner, whose memory gates decide underneath it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Sequence

from cratekit.core import cores, pool, tags

#: What a light worker holds before it reads a sample. Measured at 284
#: megabytes on Linux (U241) and 336 on the Mac (A121, U275); declared an
#: eighth above the higher, one figure on every platform.
LIGHT_BASE_BYTES = 384 * 1024 * 1024
#: What each second of the longest track adds at the peak: measured 1.35
#: megabytes a second on Linux and 2.76 on the Mac (U275), declared a ninth
#: above the steeper and rounded up, 13 to 22 percent over each measured peak.
LIGHT_BYTES_PER_SECOND = 25 * 1024 * 1024 // 8
#: What the decode holds for each sample frame at the file's own rate: four
#: bytes a channel, four for the mix, eight for the resampler's copies.
#: Declared above two loose readings at 192 kilohertz (U241 review).
DECODE_BYTES_PER_CHANNEL = 4
DECODE_EXTRA_CHANNELS = 3
#: The rate and channels assumed when the header gives a length and not
#: these: the largest plausible, so not knowing never widens the plan.
ASSUMED_RATE = 192000
ASSUMED_CHANNELS = 2
#: The slowest audio assumed when the header gives no length, 32 kilobits, so
#: the length it implies is an upper bound.
SLOWEST_BYTES_PER_SECOND = 4000
#: The cores kept back from the light pool: the driver's, and the machine's.
LIGHT_RESERVED_CORES = 2

_DETECT: Callable[[Path], dict[str, Any] | None] | None = None


def bind_detect(detect: Callable[[Path], dict[str, Any] | None] | None) -> None:
    global _DETECT
    _DETECT = detect


def bound() -> bool:
    """Whether a detector is bound in this process, without naming which."""
    return _DETECT is not None


def init_pass(detect_name: str | None = None) -> None:
    """Spawn initializer: a child starts unbound and binds the importable default."""
    if detect_name == "default" or _DETECT is None:
        from cratekit.analysis.detect import analyse_file

        bind_detect(analyse_file)


def analyse(path: str) -> dict[str, Any]:
    """One file's cheap measure. Importable, so spawn can find it by name.

    A detector answering None, the shipped one only without the extra, settles
    the file ``skipped-no-key``, the terminal's name from when it meant keyless.
    """
    target = Path(path)
    detector = _DETECT
    if detector is None:
        from cratekit.analysis.detect import analyse_file

        detector = analyse_file
    found = detector(target)
    if found is None:
        return {"path": path, "terminal": "skipped-no-key"}
    if found.get("terminal") is not None:
        # The detector's own terminal passes through rather than reading as keyless.
        return {"path": path, "terminal": str(found["terminal"])}
    payload = {"path": path, "terminal": None}
    payload.update(found)
    payload["path"] = path
    return payload


def worker_bytes(
    seconds: float, *, rate: int = 44100, channels: int = 2
) -> int:
    """What one light worker holds at its peak over one track.

    The larger of the analysis, a line in the track's length, and the decode,
    a line in its length at the file's own rate and channels.
    """
    if not seconds >= 0.0:
        raise ValueError("a track's length is a number of seconds, so never negative")
    if rate < 1 or channels < 1:
        raise ValueError("a file's rate and channels are counts, so at least one")
    analysis = int(seconds * LIGHT_BYTES_PER_SECOND)
    decode = int(
        seconds * rate * DECODE_BYTES_PER_CHANNEL * (channels + DECODE_EXTRA_CHANNELS)
    )
    return LIGHT_BASE_BYTES + max(analysis, decode)


def seconds_of(path: str | Path) -> float:
    """How long ``path`` runs, or the longest it could run when its header will not say.

    Otherwise the size at the slowest audio there is. A file that cannot be
    sized is read as empty: the decode refuses it at once.
    """
    return _shape_of(path)[0]


def _shape_of(path: str | Path) -> tuple[float, int, int]:
    """Seconds, rate and channels of ``path``, each bounded from above when unknown."""
    target = Path(path)
    seconds, rate, channels = tags.audio_shape(target)
    if seconds is None:
        # NO LENGTH: the size bound already covers any decode the file could
        # hold, so the assumed rate is not laid on top.
        try:
            seconds = target.stat().st_size / SLOWEST_BYTES_PER_SECOND
        except OSError:
            seconds = 0.0
        return seconds, 1, 1
    return seconds, rate or ASSUMED_RATE, channels or ASSUMED_CHANNELS


def cost_of(path: str | Path) -> int:
    """What a light worker holds at its peak over ``path``."""
    seconds, rate, channels = _shape_of(path)
    return worker_bytes(seconds, rate=rate, channels=channels)


def longest_seconds(paths: Sequence[str | Path]) -> float:
    """The length of the longest track in the batch."""
    return max((seconds_of(path) for path in paths), default=0.0)


def costliest(paths: Sequence[str | Path]) -> int:
    """The largest worker cost any track in the batch asks for, which is the plan's."""
    return max((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)


def plan(
    paths: Sequence[str | Path],
    *,
    cost: int | None = None,
    reserve_bytes: int = pool.DEFAULT_MEMORY_RESERVE_BYTES,
    reserved_cores: int = LIGHT_RESERVED_CORES,
) -> pool.PoolPlan:
    """The light pool for these files: as wide as memory affords, up to the cores less two.

    ``cost`` None is the batch's costliest track. ``reserve_bytes`` is raised
    by a caller that scores vocals in the driver.
    """
    return pool.plan_pool(
        worker_bytes=costliest(paths) if cost is None else cost,
        items=len(paths),
        ceiling=cores.worker_ceiling(reserved=reserved_cores),
        reserve_bytes=reserve_bytes,
    )


def run(paths: list[str], cost: int | None = None) -> list[dict[str, Any]]:
    return pool.map_workers(plan(paths, cost=cost), analyse, paths)
