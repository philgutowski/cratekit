"""Read-only detectors. Tempo is measured. It is never emitted as a grid.

The no-beatgrid rule is about writing. Computing a tempo from audio is how the
drift and its verdict get a number; this module never assigns into a tag
mapping and never writes XML.

NO KEY IS MEASURED (U343): a track's key, and the head carrying it, come only
from rekordbox's own analysis after the visit, through ``analyze adopt``.
"""

from __future__ import annotations

import copy
import time
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from typing import Any, Iterator, MutableMapping

from cratekit.analysis.energy import MEASURE_RATE
from cratekit.core import drift as drift_words
from cratekit.core.config import DEFAULT_DRIFT_CUT, DEFAULT_TEMPO_CEILING, DEFAULT_TEMPO_FLOOR

#: The terminal status for a file the decoder could not read at all.
TERMINAL_UNDECODABLE = "skipped-undecodable"
#: The terminal status for a file that decoded and could not be analysed: too
#: short for a tempo, or a signal a step raised on.
TERMINAL_UNANALYSABLE = "skipped-unanalysable"
#: The terminal status for a file libsndfile cannot open on a machine with no
#: ffmpeg to try it (U263). Apart from ``TERMINAL_UNDECODABLE``, which every
#: decoder that could read the file refused.
TERMINAL_NO_DECODER = "skipped-no-decoder"

#: The frame hop of the onset envelope and the tempogram, in samples of
#: ``MEASURE_RATE``. It sets the raw precision: near 128 beats per minute the
#: bins sit about six apart (R-744), which the interpolation below recovers.
TEMPO_HOP = 512
#: The prior over metrical levels, a log-normal in octaves with librosa's
#: centre and width, multiplied into the linear strength rather than added to
#: a log one: the form measured, 22 more exact agreements in 299 than a flat
#: window (docs/cutover.md, sitting 22). A change to it is re-measured.
TEMPO_PRIOR_CENTRE = 120.0
TEMPO_PRIOR_OCTAVES = 1.0

#: How far the measured tempo agrees with rekordbox's own analysis of the
#: same files, measured 2026-09-30 over 299 library files whose stored tempo
#: is not a whole number (a whole one may be a tag's), so the tempo the drift
#: is read against is presented as a measurement with a known error. The shape
#: is the tempo half of ``analysis.agreement.Agreement.as_dict``'s, so
#: re-recording is a copy. Every count was measured, none is a target.
#: Re-measure with ``scripts/head_agreement.py --analyse 300 --step 4`` after
#: any change here and replace every number in the same commit.
#:
#: NO KEY BUCKETS (U343): the run measures no key, so it carries no key's
#: agreement; a head's key comes from rekordbox.
_HEAD_AGREEMENT: dict[str, Any] = {
    "measured_on": date(2026, 9, 30).isoformat(),
    "reference": "rekordbox 7.2.19, its own analysis of the same files",
    "window": {"floor": DEFAULT_TEMPO_FLOOR, "ceiling": DEFAULT_TEMPO_CEILING},
    "files": 299,
    "tempo": {
        "equal": 194,
        "off_one_to_three": 53,
        "half_or_double": 1,
        "other_level": 51,
    },
    "within_one": 226,
}


def head_agreement(window: tuple[int, int] | None = None) -> dict[str, Any]:
    """A fresh copy of the recorded agreement, safe to place in an envelope.

    ``window`` is the floor and ceiling the run bound; ``applies_to_window``
    says whether it is the one measured, and the numbers stay either way.
    """
    record = copy.deepcopy(_HEAD_AGREEMENT)
    measured = (record["window"]["floor"], record["window"]["ceiling"])
    record["applies_to_window"] = window is None or tuple(window) == measured
    return record


def heavy_available() -> bool:
    """Whether the analysis extra is importable HERE, in this process.

    ``analyse_file`` answers a missing extra with None, which reads as no
    answer at all, so a worker asks this first.
    """
    try:
        import librosa  # noqa: F401
        import numpy  # noqa: F401
    except ImportError:
        return False
    return True


def _interpolated_peak(strength: Any, index: int) -> float:
    """The peak's position between bins, by the parabola through three points.

    The strongest bin alone is off by up to half a bin, three beats per minute
    near 128. An edge bin, or a flat run that makes no parabola, answers the
    bin itself. THE OFFSET IS HELD TO HALF A BIN: the bin was chosen on the
    scored strength and the parabola is fitted on the raw one, and past the
    midpoint the neighbour would have been the bin.
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
    offset = 0.5 * (left - right) / curvature
    return index + max(-0.5, min(0.5, offset))


def tempo_from_autocorrelation(
    strength: Any,
    *,
    rate: int = MEASURE_RATE,
    hop: int = TEMPO_HOP,
    floor: int = DEFAULT_TEMPO_FLOOR,
    ceiling: int = DEFAULT_TEMPO_CEILING,
) -> float | None:
    """The tempo the window and the prior pick out of an aggregated tempogram.

    ``strength`` is one autocorrelation over lag in frames. Only a bin from
    ``floor`` to ``ceiling``, both included, is a candidate, and the
    interpolated answer is held inside the window too: the window is the
    contract. None when no bin falls inside it, as a short envelope can.
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
    inside = (frequencies >= floor) & (frequencies <= ceiling)
    if not np.any(inside):
        return None
    score = np.where(inside, np.nan_to_num(strength * prior, nan=-np.inf), -np.inf)
    index = int(np.argmax(score))
    lag = _interpolated_peak(strength, index)
    if lag <= 0.0:
        return None
    return float(min(max(60.0 * rate / (hop * lag), float(floor)), float(ceiling)))


#: The drift measurement (U157): every number is the method's, measured on
#: synthetic tracks of known tempo (``tests/test_analysis_drift.py``); the
#: setting is ``analysis.drift_cut``. A window holds a dozen beats at the floor.
DRIFT_WINDOW_SECONDS = 10.0
#: How far either side of the track's tempo a window's peak is looked for, as
#: a factor: narrow enough that a window cannot read a related metrical level,
#: a jump in the reading rather than drift, and wide enough that a step of up
#: to a quarter reaches the other section (U157 review).
DRIFT_BAND = 0.25
#: A window counts only when it carries a pulse: onset strength at least this
#: fraction of the median window, so a breakdown is passed over, and at least
#: the floor, so a pad is not judged on its noise.
DRIFT_ONSET_RELATIVE = 0.5
DRIFT_ONSET_FLOOR = 0.2
#: And a clear peak, this fraction above the mean of the lags around it: a
#: drum pattern stands 0.1 to 0.2 above, noise and a pad under 0.02.
DRIFT_PULSE_CONTRAST = 0.05
#: Fewer counted windows than this is too little to judge: the drift is unknown.
DRIFT_MIN_WINDOWS = 3
#: The spread runs from this percentile to its complement, so one odd window
#: in ten moves nothing.
DRIFT_PERCENTILE = 10.0


def _onset_and_tempogram(samples: Any, rate: int) -> tuple[Any, Any]:
    """The onset envelope and the tempogram librosa's estimator computes, taken once."""
    import librosa

    envelope = librosa.onset.onset_strength(y=samples, sr=rate, hop_length=TEMPO_HOP)
    tempogram = librosa.feature.tempogram(onset_envelope=envelope, sr=rate, hop_length=TEMPO_HOP)
    return envelope, tempogram


def measure_tempo(samples: Any, rate: int, *, floor: int, ceiling: int) -> float | None:
    """The tempo of decoded samples, inside the window, to a fraction of a beat, or None."""
    return measure_tempo_and_drift(samples, rate, floor=floor, ceiling=ceiling)[0]


def measure_tempo_and_drift(
    samples: Any, rate: int, *, floor: int, ceiling: int
) -> tuple[float | None, float | None]:
    """The tempo, and how far it moves over the track, from ONE tempogram (U157).

    The drift is None when the tempo is, or the track holds too little pulse.
    """
    envelope, tempogram = _onset_and_tempogram(samples, rate)
    tempo = tempo_from_autocorrelation(
        tempogram.mean(axis=1), rate=rate, hop=TEMPO_HOP, floor=floor, ceiling=ceiling
    )
    if tempo is None:
        return None, None
    return tempo, drift_from_tempogram(envelope, tempogram, tempo, rate=rate, hop=TEMPO_HOP)


def drift_from_tempogram(
    envelope: Any, tempogram: Any, tempo: float, *, rate: int = MEASURE_RATE, hop: int = TEMPO_HOP
) -> float | None:
    """How far the tempo moves over the track, a percent of its middle, or None (U157).

    Each window's peak is found inside :data:`DRIFT_BAND` of ``tempo`` and
    interpolated as the track's tempo is; a window without a pulse is passed over.
    The answer is the percentile spread of the windows' tempos over their
    median, so a steady track reads near zero whatever its breakdowns.
    NONE IS NOT STEADY: too few windows with a pulse is unknown.
    """
    import librosa
    import numpy as np

    envelope = np.asarray(envelope, dtype=float).reshape(-1)
    tempogram = np.asarray(tempogram, dtype=float)
    if tempo <= 0.0 or tempogram.ndim != 2 or tempogram.shape[0] < 3:
        return None
    per = int(round(DRIFT_WINDOW_SECONDS * rate / hop))
    windows = min(tempogram.shape[1], envelope.size) // per
    # NO WINDOW AT ALL is answered before a median of nothing.
    if windows == 0:
        return None
    frequencies = librosa.tempo_frequencies(tempogram.shape[0], sr=rate, hop_length=hop)
    widest = 1.0 + DRIFT_BAND
    band = (frequencies >= tempo / widest) & (frequencies <= tempo * widest)
    around = (frequencies >= tempo / 1.5) & (frequencies <= tempo * 2.0)
    if not np.any(band):
        return None
    strength = np.array([envelope[i * per : (i + 1) * per].mean() for i in range(windows)])
    median = float(np.median(strength))
    tempos: list[float] = []
    for i in range(windows):
        if strength[i] < DRIFT_ONSET_FLOOR or strength[i] < DRIFT_ONSET_RELATIVE * median:
            continue
        column = tempogram[:, i * per : (i + 1) * per].mean(axis=1)
        index = int(np.argmax(np.where(band, column, -np.inf)))
        peak = float(column[index])
        if peak <= 0.0 or (peak - float(column[around].mean())) / peak < DRIFT_PULSE_CONTRAST:
            continue
        lag = _interpolated_peak(column, index)
        if lag <= 0.0:
            continue
        tempos.append(60.0 * rate / (hop * lag))
    if len(tempos) < DRIFT_MIN_WINDOWS:
        return None
    low, middle, high = np.percentile(
        tempos, [DRIFT_PERCENTILE, 50.0, 100.0 - DRIFT_PERCENTILE]
    )
    return float(100.0 * (high - low) / middle)


#: The stages a run's time is reported under (U241), in order. No harmonic
#: separation and no chroma since U343, which took the key out of the run.
#: ``scripts/analyze_stages.py`` prints them.
STAGES = ("decode", "tempo_drift", "energy")


@contextmanager
def timed(timings: MutableMapping[str, float] | None, stage: str) -> Iterator[None]:
    """Add the block's wall time to ``timings[stage]``, timing the shipped code in place."""
    if timings is None:
        yield
        return
    started = time.perf_counter()
    try:
        yield
    finally:
        timings[stage] = timings.get(stage, 0.0) + time.perf_counter() - started


def analyse_file(
    path: Path,
    *,
    calibration: Any = None,
    tempo_window: tuple[int, int] = (DEFAULT_TEMPO_FLOOR, DEFAULT_TEMPO_CEILING),
    drift_cut: float = DEFAULT_DRIFT_CUT,
    timings: MutableMapping[str, float] | None = None,
) -> dict[str, Any] | None:
    """Return tempo, drift and energy, or None when detection cannot run.

    No key (U343). ``timings`` collects each stage's wall time when given.
    ``tempo_window`` and ``drift_cut`` are the configured values the run binds
    (U157). Energy is measured under a
    calibration by the restamp's own measure, so a file the run scored needs no
    restamp (U344), and is otherwise an honest absence whose ``energy_status``
    names why (U58). librosa is imported here so a slim install can still
    import the package.
    """
    try:
        import librosa  # noqa: F401 - asked for so its absence is the extra's absence
        import numpy  # noqa: F401 - asked for so its absence is the extra's absence
    except ImportError:
        return None
    # THIS PROCESS'S FIRST HEAD IS PRECEDED BY A WARM UP, ALONE (U241), here so
    # every caller takes the same turn; ``analysis.warm`` says why.
    from cratekit.analysis import decode, warm

    warm.kernels()
    try:
        # AT THE ENERGY MEASURE RATE, the rate the tempo is read at, and THROUGH THE ONE DECODER (U263). The energy is measured
        # from the file, as the restamp measures it (U344).
        with timed(timings, "decode"):
            y, sr = decode.load(path, MEASURE_RATE)
        if y.size == 0:
            return {"path": path, "terminal": TERMINAL_UNDECODABLE}
    except decode.DecoderMissing:
        return {"path": path, "terminal": TERMINAL_NO_DECODER}
    except Exception:
        # A FILE THE DECODER COULD NOT READ IS ITS OWN TERMINAL.
        return {"path": path, "terminal": TERMINAL_UNDECODABLE}
    try:
        floor, ceiling = tempo_window
        # THE DRIFT IS READ OVER THE WHOLE TRACK, always (U241).
        with timed(timings, "tempo_drift"):
            tempo, drift = measure_tempo_and_drift(y, sr, floor=floor, ceiling=ceiling)
        if tempo is None:
            return {"path": path, "terminal": TERMINAL_UNANALYSABLE}
        rate = int(tempo + 0.5)
    except Exception:
        # DECODED AND NOT ANALYSABLE IS ITS OWN TERMINAL TOO.
        return {"path": path, "terminal": TERMINAL_UNANALYSABLE}
    with timed(timings, "energy"):
        level, status = energy_from_path(path, calibration=calibration)
    return {
        "path": path,
        "rate": rate,
        # None and unknown for a track with too little pulse to judge (U157).
        "drift": drift,
        "drift_verdict": drift_words.verdict(drift, drift_cut),
        "energy": level,
        "energy_status": status,
    }


def energy_from_path(path: Any, *, calibration: Any) -> tuple[int | None, str]:
    """The level and its status for ``path``, measured as ``analyze restamp`` measures it.

    No calibration measures nothing. NOT FROM THE RUN'S SAMPLES: the run
    resamples the whole track before it slices, and the restamp decodes the
    slice alone, so the two differed in every feature of a track longer than
    the slice, and a track on a decile cut took two levels (U344). Through
    :func:`energy.measure`, the restamp's own call, so one file under one
    calibration has one level, and the run's tempo is not handed down.
    """
    from cratekit.analysis import energy

    if calibration is None:
        return None, energy.STATUS_UNCALIBRATED
    features = energy.measure(Path(path))
    if features is None:
        return None, energy.STATUS_FEATURES_UNAVAILABLE
    return energy.level_for(features, calibration), energy.STATUS_CALIBRATED
