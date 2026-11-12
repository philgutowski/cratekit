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
the constant Q transform, which are librosa's own. The same head on the Mac
peaks about twice as steeply, 2.35 gigabytes for a twelve minute track, so
the declared line is the Mac's (U275), and Linux is planned narrower than its
own peaks need rather than the Mac wider than its peaks allow. The cost is a line in the
track's length, so it is declared as one, from the COSTLIEST track in the
batch: a folder of radio edits affords more workers than a folder of ten
minute tracks, and a folder holding one hour long mix affords the count that
mix allows. A length the header will not give is bounded by the file's size.

THE DECODE IS ITS OWN LINE, IN THE FILE'S OWN RATE. Everything after the
decode works at 22050 hertz whatever the file, but the decode reads the whole
file at the rate it was stored at, every channel, before it is mixed down.
For CD audio that is under the analysis and changes nothing. For a 192
kilohertz file it is most of the worker: the review of U241 measured 2054
megabytes for an eleven minute track at 192 kilohertz against 1168 for the
same audio at 44.1, and a second reading gave 2180. So a worker costs the
larger of the two lines.

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
#: numpy, scipy, librosa and its compiled kernels. On Linux (a four core
#: container, 2026-11-10, U241) measured at 238 megabytes on a two second file
#: and 284 as the intercept of the line through nine lengths, and declared at
#: 320, an eighth above. On the Mac (arm64, Python 3.12.5, librosa 1.0.0,
#: 2026-11-12, A121 at sitting 94, U275) the line through six library tracks
#: from 236 to 729 seconds meets the axis at 336 megabytes through its ends
#: and 299 by least squares; declared at least an eighth above the higher, as
#: on Linux, and one figure on every platform, the larger, so no machine is
#: planned wider than its peaks.
LIGHT_BASE_BYTES = 384 * 1024 * 1024
#: What each second of the longest track adds at the peak. On Linux measured
#: at 1.35 megabytes a second (345 megabytes at 45 seconds, 1175 at 660). On
#: the Mac, the same six tracks, 44.1 kHz stereo FLAC: 987 megabytes at 236
#: seconds, 1281 at 376, 1805 at 576, 2105 at 668, 2162 at 690 and 2346 at
#: 729, every one over the 1.5 then declared, a line of 2.76 megabytes a
#: second through its ends and 2.72 by least squares. Declared a ninth above
#: the steeper, the margin the Linux figure had, and rounded up to three and an
#: eighth, so each of the six is declared 13 to 22 percent over its peak.
LIGHT_BYTES_PER_SECOND = 25 * 1024 * 1024 // 8
#: What the decode holds for each sample frame of the file at its own rate:
#: four bytes for each channel as it is read, four for the mono mix, and
#: eight more for the working copies the resampler takes. Measured twice at
#: 192 kilohertz stereo over 660 seconds, 2054 and 2180 megabytes at the
#: peak, 1770 and 1896 over the base; this declares 2417 over it, because two
#: readings 126 megabytes apart are not a tight figure.
DECODE_BYTES_PER_CHANNEL = 4
DECODE_EXTRA_CHANNELS = 3
#: The rate and channels a file is assumed to hold when its header gives a
#: length and not these: the largest a DJ's file plausibly is, so not knowing
#: can make the plan narrower and never wider.
ASSUMED_RATE = 192000
ASSUMED_CHANNELS = 2
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

    The header's own length where there is one. Otherwise the file's size at
    the slowest audio there is, which no real file is longer than. A file that
    cannot even be sized is read as empty: the decode will refuse it at once,
    and a file that is not there holds no memory.
    """
    return _shape_of(path)[0]


def _shape_of(path: str | Path) -> tuple[float, int, int]:
    """Seconds, rate and channels of ``path``, each bounded from above when unknown."""
    target = Path(path)
    seconds, rate, channels = tags.audio_shape(target)
    if seconds is None:
        # NO LENGTH, so the size bounds it, and that bound is already several
        # hundred times the file: the analysis line over it covers any decode
        # the file could hold, and the assumed rate is not laid on top.
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

    ``cost`` None is the measured cost of the batch's costliest track.
    ``reserve_bytes`` is the planner's own reserve unless the caller is about
    to hold more than that itself, which a job that scores vocals in the
    driver is. ``reserved_cores`` is the shipped two unless a measurement is
    asking what another figure would do, ``scripts/analyze_stages.py``.
    """
    return pool.plan_pool(
        worker_bytes=costliest(paths) if cost is None else cost,
        items=len(paths),
        ceiling=cores.worker_ceiling(reserved=reserved_cores),
        reserve_bytes=reserve_bytes,
    )


def run(paths: list[str], cost: int | None = None) -> list[dict[str, Any]]:
    return pool.map_workers(plan(paths, cost=cost), analyse, paths)
