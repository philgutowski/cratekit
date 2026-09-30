"""Read-only detectors. Tempo is measured. It is never emitted as a grid.

The no-beatgrid rule is about writing: a grid element, a tempo tag, an
average-tempo field, an analysis-file grid. Reading a tempo tag or
computing a tempo from audio is how energy scoring and the filename head
get a number. This module never assigns into a tag mapping and never
writes XML.
"""

from __future__ import annotations

import copy
from datetime import date
from pathlib import Path
from typing import Any

from cratekit.analysis.energy import MEASURE_RATE
from cratekit.core.config import DEFAULT_TEMPO_CEILING, DEFAULT_TEMPO_FLOOR

#: The terminal status for a file the decoder could not read at all.
TERMINAL_UNDECODABLE = "skipped-undecodable"
#: The terminal status for a file that decoded and could not be analysed: too
#: short for a tempo, or a signal the chroma or separation step raised on.
#: Kept apart from keyless, which is a track the analyser READ and found
#: atonal, for the reason ``TERMINAL_UNDECODABLE`` is kept apart from it.
TERMINAL_UNANALYSABLE = "skipped-unanalysable"

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


#: The frame hop the onset envelope and the tempogram are computed at, in
#: samples of ``MEASURE_RATE``. Named because it sets the estimator's raw
#: precision: a tempogram bin is one frame of lag, and at this rate and hop the
#: bins near 128 beats per minute sit about six apart (lag 20 reads 129.2, lag
#: 21 reads 123.0), which is the whole of the "off by one to three" bucket
#: R-744 recorded. The interpolation below is what recovers the precision.
TEMPO_HOP = 512
#: The prior over metrical levels, in octaves around a centre, the values
#: librosa's own estimator defaults to. Kept because on the measured sample it
#: beat a flat window by 22 exact agreements in 299 (docs/cutover.md). The
#: window is the setting, the prior is the method.
TEMPO_PRIOR_CENTRE = 120.0
TEMPO_PRIOR_OCTAVES = 1.0

#: How far a head's tempo and key agree with rekordbox's own analysis of the
#: same file, measured on 2026-09-30 over 299 library files rekordbox had
#: analysed itself, so the run's answer presents a head as a measurement with
#: a known error rather than as a fact. The sample is every row whose stored
#: tempo is not a whole number, because a whole number there may have been
#: imported from a tag rather than computed, so it leans toward tracks with an
#: unquantised pulse and understates agreement on programmed music: on the 22
#: files this product had headed and rekordbox then analysed, 16 agreed
#: exactly and 19 keys of 22 matched. The four tempo buckets are the ones
#: ``analysis.agreement`` prints. "Other level" is a pulse read at a related
#: level rekordbox did not choose, three to two or four to three, and is the
#: method's own rate rather than a setting. Every count was measured, none is
#: a target. Re-measure with ``scripts/head_agreement.py`` after any change
#: to this module and replace every number here in the same commit.
_HEAD_AGREEMENT: dict[str, Any] = {
    "measured_on": date(2026, 9, 30).isoformat(),
    "reference": "rekordbox 7.2.19, its own analysis of the same files",
    "files": 299,
    "tempo": {
        "equal": 193,
        "within_one": 225,
        "off_one_to_three": 54,
        "half_or_double": 1,
        "other_level": 51,
    },
    "key": {"equal": 158, "differs": 141},
    "window": {"floor": DEFAULT_TEMPO_FLOOR, "ceiling": DEFAULT_TEMPO_CEILING},
}


def head_agreement() -> dict[str, Any]:
    """A fresh copy of the recorded agreement, safe to place in an envelope."""
    return copy.deepcopy(_HEAD_AGREEMENT)


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


def _interpolated_peak(strength: Any, index: int) -> float:
    """The peak's position between bins, by the parabola through three points.

    A tempogram bin is one frame of lag, and the true period is almost never a
    whole number of frames, so the strongest bin alone is off by up to half a
    bin, which near 128 beats per minute is three. Fitting a parabola to the
    bin and its two neighbours puts the peak where the autocorrelation
    actually turns, to a fraction of a frame. An edge bin, or a flat run where
    the three points make no parabola, answers the bin itself.
    """
    if index <= 0 or index >= len(strength) - 1:
        return float(index)
    left, centre, right = (
        float(strength[index - 1]),
        float(strength[index]),
        float(strength[index + 1]),
    )
    curvature = left - 2.0 * centre + right
    if curvature >= 0.0:
        return float(index)
    return index + 0.5 * (left - right) / curvature


def tempo_from_autocorrelation(
    strength: Any,
    *,
    rate: int = MEASURE_RATE,
    hop: int = TEMPO_HOP,
    floor: int = DEFAULT_TEMPO_FLOOR,
    ceiling: int = DEFAULT_TEMPO_CEILING,
) -> float | None:
    """The tempo the window and the prior pick out of an aggregated tempogram.

    ``strength`` is one autocorrelation over lag, in frames, bin zero the zero
    lag. The prior is librosa's own, a log-normal over metrical levels centred
    at ``TEMPO_PRIOR_CENTRE``, and the window is applied on top of it: a bin
    whose tempo falls at or above ``floor`` and below ``ceiling`` is a
    candidate, every other bin is not, so a pulse that reads at 166 with a
    window of 80 to 160 is named 83, and named 166 when the window is raised.
    None when no bin falls inside the window, which a configured window cannot
    produce (config refuses an empty one) and a short onset envelope can.
    """
    import librosa
    import numpy as np

    strength = np.asarray(strength, dtype=float).reshape(-1)
    if strength.size < 2:
        return None
    frequencies = librosa.tempo_frequencies(strength.size, sr=rate, hop_length=hop)
    positive = np.where(frequencies > 0, frequencies, np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        prior = np.exp(
            -0.5
            * ((np.log2(positive) - np.log2(TEMPO_PRIOR_CENTRE)) / TEMPO_PRIOR_OCTAVES) ** 2
        )
    inside = (frequencies >= floor) & (frequencies < ceiling)
    if not np.any(inside):
        return None
    score = np.where(inside, np.nan_to_num(strength * prior, nan=-np.inf), -np.inf)
    index = int(np.argmax(score))
    lag = _interpolated_peak(strength, index)
    if lag <= 0.0:
        return None
    return 60.0 * rate / (hop * lag)


def measure_tempo(samples: Any, rate: int, *, floor: int, ceiling: int) -> float | None:
    """The tempo of decoded samples, inside the window, to a fraction of a beat.

    The onset envelope and the tempogram are the ones librosa's estimator
    computes; what differs is the window and the interpolation, for the
    reasons the constants above give. None when the envelope is too short to
    hold a period inside the window.
    """
    import librosa

    envelope = librosa.onset.onset_strength(y=samples, sr=rate, hop_length=TEMPO_HOP)
    tempogram = librosa.feature.tempogram(onset_envelope=envelope, sr=rate, hop_length=TEMPO_HOP)
    return tempo_from_autocorrelation(
        tempogram.mean(axis=1), rate=rate, hop=TEMPO_HOP, floor=floor, ceiling=ceiling
    )


def analyse_file(
    path: Path,
    *,
    calibration: Any = None,
    tempo_window: tuple[int, int] = (DEFAULT_TEMPO_FLOOR, DEFAULT_TEMPO_CEILING),
) -> dict[str, Any] | None:
    """Return camelot, tempo and energy, or None when detection cannot run.

    ``tempo_window`` is the configured floor and ceiling; the run binds it from
    ``analysis.tempo_floor`` and ``analysis.tempo_ceiling`` beside the
    calibration, and a caller that passes nothing gets the shipped default.

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
        # AT THE ENERGY MEASURE RATE, one constant for both, because every
        # spectral feature is rate dependent and the calibration fitted on the
        # restamp path scores the samples decoded here.
        y, sr = librosa.load(str(path), sr=MEASURE_RATE, mono=True)
        if y.size == 0:
            return {"path": path, "terminal": TERMINAL_UNDECODABLE}
    except Exception:
        # A FILE THE DECODER COULD NOT READ IS NOT A TRACK WITH NO KEY. The
        # first version returned None here, which the light pass reported as
        # skipped-no-key: a truncated download was told to the person as
        # atonal, a clean report over a file the tool could not read.
        return {"path": path, "terminal": TERMINAL_UNDECODABLE}
    try:
        floor, ceiling = tempo_window
        tempo = measure_tempo(y, sr, floor=floor, ceiling=ceiling)
        if tempo is None:
            return {"path": path, "terminal": TERMINAL_UNANALYSABLE}
        rate = int(tempo + 0.5)
        y_harm = librosa.effects.harmonic(y, margin=4)
        chroma = librosa.feature.chroma_cqt(y=y_harm, sr=sr)
        profile = chroma.mean(axis=1)
    except Exception:
        # DECODED AND NOT ANALYSABLE IS NOT KEYLESS EITHER. A stinger too short
        # for a tempo estimate, or a signal the separation raised on, was
        # reported as atonal by the first version, the same shape as the
        # undecodable case above one step later.
        return {"path": path, "terminal": TERMINAL_UNANALYSABLE}
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
    level, status = energy_from_samples(y, sr, calibration=calibration)
    return {
        "path": path,
        "camelot": camelot,
        "rate": rate,
        "energy": level,
        "energy_status": status,
    }


def energy_from_samples(samples: Any, rate: int, *, calibration: Any) -> tuple[int | None, str]:
    """The level and its status for samples already decoded by the head.

    Split out of :func:`analyse_file` so the three answers are one function
    with one caller each way: no calibration is ``uncalibrated`` and measures
    nothing, a measurement that fails is ``features-unavailable``, and a level
    is ``calibrated``. The head's tempo is NOT handed down: the feature vector
    measures its own from the slice so the run and restamp paths agree.
    """
    from cratekit.analysis import energy

    if calibration is None:
        return None, energy.STATUS_UNCALIBRATED
    features = energy.features_from_samples(samples, rate)
    if features is None:
        return None, energy.STATUS_FEATURES_UNAVAILABLE
    return energy.level_for(features, calibration), energy.STATUS_CALIBRATED
