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


def analyse_file(path: Path) -> dict[str, Any] | None:
    """Return camelot, bpm, and energy, or None when detection cannot run.

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
            return None
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
    return {"path": path, "camelot": camelot, "rate": bpm, "energy": None}
