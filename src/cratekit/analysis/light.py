"""Pass A: key, tempo, energy. Wide pool, no vocal model.

The count comes from plan_pool. A ProcessPoolExecutor of our own would be a
second answer to R23.

WHAT A LIGHT WORKER COSTS IS MEASURED, AND IT IS NOT SMALL (U241). The first
version declared 64 megabytes, "librosa-scale, tens of megabytes", and no
pool ever ran at that figure because the job never reached this module's
pool. Measured in a fresh process per track, one head held 374 megabytes for
a 45 second track and 2.0 gigabytes for an eleven minute one, the whole of
the transform and its medians at once. With the separation in
``analysis.separation`` it holds 345 megabytes and 1.18 gigabytes for the
same two, and the peak is now shared between the decode, the tempogram and
the constant Q transform, which are librosa's own. The cost is a line in the
track's length, so it is declared as one, from the LONGEST track in the batch:
a folder of radio edits affords more workers than a folder of ten minute
tracks, and a folder holding one hour long mix affords the count that mix
allows. A length the header will not give is bounded by the file's size.

THE CEILING IS THE CORES LESS TWO, HANDED TO THE PLANNER. A light worker is a
processor's worth of arithmetic, so past the core count a further one only
waits; two are kept back, one for the process driving the job, which scores
vocals and writes, and one for whatever else the machine is doing. The
ceiling can only lower the plan: the memory reading, the reserve, the
headroom and the swap and used percent gates decide underneath it, as for
every pool.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Sequence

from cratekit.core import cores, pool, tags

#: What a light worker holds before it has read a sample: the interpreter,
#: numpy, scipy, librosa and its compiled kernels. Measured at 238 megabytes
#: on a two second file and 284 as the intercept of the line through nine
#: lengths; declared above both.
LIGHT_BASE_BYTES = 320 * 1024 * 1024
#: What each second of the longest track adds at the peak. Measured at 1.35
#: megabytes a second (345 megabytes at 45 seconds, 1175 at 660, on Linux);
#: declared a ninth above it, because the probe that would raise a low figure
#: cannot run here, and the planner's own ceiling is the brake on its being
#: wrong.
LIGHT_BYTES_PER_SECOND = 3 * 1024 * 1024 // 2
#: The slowest audio a file is assumed to hold when its header gives no
#: length, in bytes a second: 32 kilobits. Slower than any file a DJ plays, so
#: the length it implies is an upper bound, and an unreadable header can make
#: the plan narrower and never wider than the file deserves.
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
    """Spawn initializer. Children re-import this module and start unbound.

    Tests bind before map_workers. The in-process plan (one worker) keeps
    the bound callable. A spawned child would need an importable detector;
    the default detect.analyse_file is that function.
    """
    if detect_name == "default" or _DETECT is None:
        from cratekit.analysis.detect import analyse_file

        bind_detect(analyse_file)


def analyse(path: str) -> dict[str, Any]:
    """One file's cheap head. Importable, so spawn can find it by name."""
    target = Path(path)
    detector = _DETECT
    if detector is None:
        from cratekit.analysis.detect import analyse_file

        detector = analyse_file
    found = detector(target)
    if found is None:
        return {"path": path, "terminal": "skipped-no-key"}
    if found.get("terminal") is not None:
        # The detector's own terminal, a file it could not decode, passes
        # through under its own name rather than being read as keyless.
        return {"path": path, "terminal": str(found["terminal"])}
    payload = {"path": path, "terminal": None}
    payload.update(found)
    payload["path"] = path
    return payload


def worker_bytes(seconds: float) -> int:
    """What one light worker holds at its peak over a track ``seconds`` long."""
    if not seconds >= 0.0:
        raise ValueError("a track's length is a number of seconds, so never negative")
    return LIGHT_BASE_BYTES + int(seconds * LIGHT_BYTES_PER_SECOND)


def seconds_of(path: str | Path) -> float:
    """How long ``path`` runs, or the longest it could run when its header will not say.

    The header's own length where there is one. Otherwise the file's size at
    the slowest audio there is, which no real file is longer than. A file that
    cannot even be sized is read as empty: the decode will refuse it at once,
    and a file that is not there holds no memory.
    """
    target = Path(path)
    stated = tags.audio_seconds(target)
    if stated is not None:
        return stated
    try:
        return target.stat().st_size / SLOWEST_BYTES_PER_SECOND
    except OSError:
        return 0.0


def longest_seconds(paths: Sequence[str | Path]) -> float:
    """The length of the longest track in the batch, which is what sets a worker's cost."""
    return max((seconds_of(path) for path in paths), default=0.0)


def plan(
    paths: Sequence[str | Path],
    *,
    cost: int | None = None,
    reserve_bytes: int = pool.DEFAULT_MEMORY_RESERVE_BYTES,
) -> pool.PoolPlan:
    """The light pool for these files: as wide as memory affords, up to the cores less two.

    ``cost`` None is the measured cost of the batch's longest track.
    ``reserve_bytes`` is the planner's own reserve unless the caller is about
    to hold more than that itself, which a job that scores vocals in the
    driver is.
    """
    return pool.plan_pool(
        worker_bytes=worker_bytes(longest_seconds(paths)) if cost is None else cost,
        items=len(paths),
        ceiling=cores.worker_ceiling(reserved=LIGHT_RESERVED_CORES),
        reserve_bytes=reserve_bytes,
    )


def run(paths: list[str], cost: int | None = None) -> list[dict[str, Any]]:
    return pool.map_workers(plan(paths, cost=cost), analyse, paths)
