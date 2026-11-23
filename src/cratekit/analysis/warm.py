"""Compile the head's kernels one process at a time, before any worker measures (U241).

librosa's numba kernels are cached on disk, and two processes filling that
cache at once crashed and left it damaged for every later run (U241 review);
a fresh cache is every new install or upgrade.

THE FIX IS TO NEVER FILL THE CACHE FROM TWO PROCESSES: before its first head,
``detect.analyse_file`` runs one whole head over audio made here, under a
lock no other process of this user holds at the same time. The warm up must
reach every kernel a real head reaches, which ``tests/test_analysis_warm.py``
holds.

THE ENERGY MEASURE ASKS FOR IT TOO (U344, closing R-1491): every head,
restamp and calibrate scores energy through ``energy.features_from_path``,
which warms first, and the warm up measures energy from its file as well as
from samples, since on an empty cache that path wrote a second
specialisation of ``utils._cabs2`` that a warmed cache did not hold
(R-1491's measurement, under the librosa of its day). A kernel keeps the code it was first compiled to, so warming first in every
process also gives a head in a worker and a restamp in the driver the same
features to the last bit. NOT COVERED: a platform with no ``fcntl`` takes no
lock. A WAIT ON THE LOCK IS NOT BOUNDED: a holder
suspended with Ctrl-Z holds every later run (U241's residual).

Writes one small audio file in a temporary directory and removes it; no tag,
no tempo, no grid.

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

#: How long the warm up's audio runs: a length, not a tuned minimum; the
#: coverage test is what holds it.
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

    A dead holder's lock is released by the platform. Where the lock cannot be
    taken at all the block runs unlocked: a worker that never starts is worse.
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

    The same calls on the same types, since a kernel is compiled per type. The
    energy is measured directly, from the file and from samples, as the
    detector skips it uncalibrated.
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
        # The energy measure every verb scores through (U344), from the file.
        energy.features_from_path(path)
    energy.features_from_samples(_signal(energy.MEASURE_RATE, WARM_SECONDS), energy.MEASURE_RATE)


def kernels() -> bool:
    """Warm this process's kernels, once, alone. True when a warm up ran here.

    A warm up that raises refuses nothing: the real head will raise the same
    thing over a real file, by name.
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
