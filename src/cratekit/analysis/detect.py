"""Read-only detectors. Tempo is measured. It is never emitted as a grid.

The no-beatgrid rule is about writing: a grid element, a tempo tag, an
average-tempo field, an analysis-file grid. Reading a tempo tag or
computing a tempo from audio is how energy scoring and the filename head
get a number. This module never assigns into a tag mapping and never
writes XML.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

#: The terminal status for a file the decoder could not read at all.
TERMINAL_UNDECODABLE = "skipped-undecodable"

_PITCHES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
_MAJOR = (6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88)
_MINOR = (6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17)
_KEY_TO_CAMELOT = {
    "C major": "8B",
    "G major": "9B",
    "D major": "10B",
    "A major": "11B",
    "E major": "12B",
    "B major": "1B",
    "F# major": "2B",
    "C# major": "3B",
    "F major": "7B",
    "A# major": "6B",
    "D# major": "5B",
    "G# major": "4B",
    "A minor": "8A",
    "E minor": "9A",
    "B minor": "10A",
    "F# minor": "11A",
    "C# minor": "12A",
    "G# minor": "1A",
    "D# minor": "2A",
    "A# minor": "3A",
    "D minor": "7A",
    "G minor": "6A",
    "C minor": "5A",
    "F minor": "4A",
}


def heavy_available() -> bool:
    """Whether the analysis extra is importable HERE, in this process.

    Asked by a worker before it analyses an item, because ``analyse_file``
    answers a missing extra and a track with no detectable key with the same
    None, and a job that skipped every file as keyless on a machine that had
    no librosa would be a clean report over work nothing could do.
    """
    try:
        import librosa  # noqa: F401
        import numpy  # noqa: F401
    except ImportError:
        return False
    return True


def analyse_file(path: Path, *, calibration: Any = None) -> dict[str, Any] | None:
    """Return camelot, tempo and energy, or None when detection cannot run.

    Energy is computed from the same decoded samples when ``calibration`` is a
    :class:`cratekit.analysis.energy.Calibration`, and is an honest absence
    otherwise: ``energy`` is None and ``energy_status`` names why, so a
    consumer can tell "this library has no calibration" from "the measurement
    failed" and neither from "never computed", which is what the first version
    of this function returned for every track (U58).

    Tests inject a detect callable into run_batch and never reach here.
    librosa is imported inside the function so a slim install can still
    import the package.
    """
    try:
        import librosa
        import numpy as np
    except ImportError:
        return None
    try:
        y, sr = librosa.load(str(path), sr=22050, mono=True)
        if y.size == 0:
            return {"path": path, "terminal": TERMINAL_UNDECODABLE}
    except Exception:
        # A FILE THE DECODER COULD NOT READ IS NOT A TRACK WITH NO KEY. The
        # first version returned None here, which the light pass reported as
        # skipped-no-key: a truncated download was told to the person as
        # atonal, a clean report over a file the tool could not read.
        return {"path": path, "terminal": TERMINAL_UNDECODABLE}
    try:
        tempo = librosa.feature.tempo(y=y, sr=sr)
        bpm = int(float(np.asarray(tempo).reshape(-1)[0]) + 0.5)
        y_harm = librosa.effects.harmonic(y, margin=4)
        chroma = librosa.feature.chroma_cqt(y=y_harm, sr=sr)
        profile = chroma.mean(axis=1)
    except Exception:
        return None
    if not np.any(profile):
        return None
    best_corr = -2.0
    best_key = None
    maj = np.asarray(_MAJOR)
    minr = np.asarray(_MINOR)
    for tonic in range(12):
        rotated = np.roll(profile, -tonic)
        for mode, tmpl in (("major", maj), ("minor", minr)):
            corr = float(np.corrcoef(rotated, tmpl)[0, 1])
            if corr > best_corr:
                best_corr = corr
                best_key = f"{_PITCHES[tonic]} {mode}"
    camelot = _KEY_TO_CAMELOT.get(best_key or "")
    if camelot is None:
        return None
    level, status = energy_from_samples(y, sr, tempo=bpm, calibration=calibration)
    return {
        "path": path,
        "camelot": camelot,
        "rate": bpm,
        "energy": level,
        "energy_status": status,
    }


def energy_from_samples(
    samples: Any, rate: int, *, tempo: float | None, calibration: Any
) -> tuple[int | None, str]:
    """The level and its status for samples already decoded by the head.

    Split out of :func:`analyse_file` so the three answers are one function
    with one caller each way: no calibration is ``uncalibrated`` and measures
    nothing, a measurement that fails is ``features-unavailable``, and a level
    is ``calibrated``.
    """
    from cratekit.analysis import energy

    if calibration is None:
        return None, energy.STATUS_UNCALIBRATED
    features = energy.features_from_samples(samples, rate, tempo=tempo)
    if features is None:
        return None, energy.STATUS_FEATURES_UNAVAILABLE
    return energy.level_for(features, calibration), energy.STATUS_CALIBRATED
