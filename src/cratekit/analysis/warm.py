"""Compile the head's kernels one process at a time, before any worker measures (U241).

librosa compiles a handful of its inner loops with numba the first time each
is called, and keeps the compiled code in a cache on disk so the next process
loads it. That cache is not safe to fill from two processes at once. Driven
by the review of U241, on a fresh cache, with two light workers starting
together: five runs in seven ended with a segmentation fault inside a numba
kernel, first in a worker and then in the driver, which had fallen back to
the same call. And the cache was left damaged, so every later analysis on that
machine crashed the same way until the cache files were deleted by hand. One
process at a time, on the same cold cache, ran clean six times in six, and so
did two workers on a cache already filled.

A fresh cache is not exotic. It is every new install, every new virtual
environment, and every upgrade of librosa or numba. So before this unit no
two librosa processes ever started together, and the first code that starts
them owns this.

THE FIX IS TO NEVER FILL THE CACHE FROM TWO PROCESSES. Every process, before
its first head, runs one whole head over a few seconds of audio it makes
itself, under a lock no other process of this user holds at the same time.
``detect.analyse_file`` asks for it, so a worker, the driver, a script and a
second command started beside the first all take the same turn. The first
process in compiles every kernel and writes the cache; each one after it
finds the cache whole and loads it. After that a process's kernels are in its
own memory and the cache is not touched again.

THE WARM UP HAS TO REACH EVERY KERNEL A REAL HEAD REACHES, or the one it
missed is compiled later by two workers at once, which is the defect again.
That is held by a test and not by this paragraph:
``tests/test_analysis_warm.py`` warms an empty cache, then measures real
files of several lengths and shapes against it, and fails if the cache gained
or changed a single file.

WHAT IT DOES NOT COVER. A path to librosa that does not go through the
detector: ``analyze restamp`` and ``analyze calibrate`` measure energy from
the file themselves, one process at a time, and ``analyze vocals`` decodes
for the model. Each is a single process, as it was before this unit, so two
of those commands started together on a cold cache are not held apart. And a
platform with no ``fcntl`` takes no lock at all, so its workers warm together.

Reads nothing of anybody's, writes one small audio file in a temporary
directory of its own and removes it, and writes no tag, no tempo and no grid.

Layer: modules. The heavy stack is imported inside the functions.
"""

from __future__ import annotations

import contextlib
import os
import tempfile
import wave
from pathlib import Path
from typing import Iterator

from cratekit.core.config import DEFAULT_TEMPO_CEILING, DEFAULT_TEMPO_FLOOR

#: How long the audio a warm up measures runs. Long enough for every stage to
#: do its ordinary work, the tempogram's window and the transform's lowest
#: octave included, and short enough to cost about a second on a filled cache.
WARM_SECONDS = 12.0
#: The rate the warm up's file is written at, so the decode resamples as it
#: does for a real file.
WARM_FILE_RATE = 44100

_WARMED = False
#: True while this process is inside its own warm up, whose head asks to be
#: warmed like any other and must not wait on the lock it is holding.
_WARMING = False


def lock_path() -> Path:
    """The lock every process of this user warms under, in the temporary directory.

    Named for the user, so one account's lock is not another's to hold. The
    file stays behind, since unlinking a lock file races its live holder.
    """
    user = getattr(os, "getuid", lambda: "any")()
    return Path(tempfile.gettempdir()) / f"cratekit-analysis-warm-{user}.lock"


@contextlib.contextmanager
def exclusive(path: Path | None = None) -> Iterator[None]:
    """Hold the warm up lock: no other process is inside this block at the same time.

    Waits for as long as the holder takes. A lock held by a process that died
    is released by the platform, so nothing here can wait for ever on a
    corpse. Where the lock cannot be taken at all, no ``fcntl`` or a lock file
    that cannot be opened, the block runs unlocked: a worker that never
    starts is a worse failure than the one this guards against.
    """
    target = path or lock_path()
    handle = None
    try:
        import fcntl

        descriptor = os.open(target, os.O_CREAT | os.O_RDWR, 0o600)
        handle = os.fdopen(descriptor, "r+b")
        fcntl.flock(handle, fcntl.LOCK_EX)
    except (ImportError, OSError):
        if handle is not None:
            handle.close()
            handle = None
    try:
        yield
    finally:
        if handle is not None:
            handle.close()  # closing the descriptor releases the lock


def _signal(rate: int, seconds: float):
    """Drums and a chord, made here: something with a pulse and a key to measure."""
    import numpy as np

    count = int(rate * seconds)
    at = np.arange(count) / rate
    chord = sum(np.sin(2 * np.pi * hz * at) for hz in (130.81, 164.81, 196.0, 261.63))
    out = (0.08 * chord).astype(np.float32)
    burst = np.hanning(int(0.01 * rate)).astype(np.float32)
    for beat in range(int(seconds * 2)):
        start = int(beat * 0.5 * rate)
        stop = min(count, start + burst.size)
        out[start:stop] += 0.6 * burst[: stop - start]
    return out


def _measure_one_head() -> None:
    """One whole head, decode included, over audio made here.

    The same calls ``detect.analyse_file`` makes, on the same types, because a
    compiled kernel is kept per type and a warm up on other types would warm
    other kernels. The energy is measured directly, since the detector skips
    it without a calibration and a calibrated run does not.
    """
    import numpy as np

    from cratekit.analysis import detect, energy

    with tempfile.TemporaryDirectory(prefix="cratekit-warm-") as folder:
        path = Path(folder) / "warm.wav"
        samples = _signal(WARM_FILE_RATE, WARM_SECONDS)
        with wave.open(str(path), "wb") as written:
            written.setnchannels(2)
            written.setsampwidth(2)
            written.setframerate(WARM_FILE_RATE)
            stereo = np.repeat((samples * 32767.0).astype("<i2")[:, None], 2, axis=1)
            written.writeframes(stereo.tobytes())
        detect.analyse_file(
            path, tempo_window=(DEFAULT_TEMPO_FLOOR, DEFAULT_TEMPO_CEILING)
        )
    energy.features_from_samples(_signal(energy.MEASURE_RATE, WARM_SECONDS), energy.MEASURE_RATE)


def kernels() -> bool:
    """Warm this process's kernels, once, alone. True when a warm up ran here.

    Does nothing where the analysis extra is absent, and nothing the second
    time it is called in one process. A warm up that raises is not a reason to
    refuse a worker: the head it was standing in for will raise the same thing
    over a real file, by name, where the person can read it.
    """
    global _WARMED, _WARMING
    if _WARMED or _WARMING:
        return False
    from cratekit.analysis import detect

    if not detect.heavy_available():
        return False
    _WARMING = True
    try:
        with exclusive():
            try:
                _measure_one_head()
            except Exception:  # noqa: BLE001 - the real head reports what the warm up met
                pass
    finally:
        _WARMING = False
    _WARMED = True
    return True


__all__ = ["WARM_SECONDS", "exclusive", "kernels", "lock_path"]
