"""Read-only detectors. Tempo is measured. It is never emitted as a grid.

The no-beatgrid rule is about writing. Computing a tempo from audio is how
energy scoring and the filename head get a number; this module never assigns
into a tag mapping and never writes XML.
"""

from __future__ import annotations

import copy
import time
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from typing import Any, Iterator, MutableMapping

from cratekit.analysis.energy import MEASURE_RATE
from cratekit.core.config import DEFAULT_DRIFT_CUT, DEFAULT_TEMPO_CEILING, DEFAULT_TEMPO_FLOOR
from cratekit.intake import drift as drift_words

#: The terminal status for a file the decoder could not read at all.
TERMINAL_UNDECODABLE = "skipped-undecodable"
#: The terminal status for a file that decoded and could not be analysed: too
#: short for a tempo, or a signal a step raised on. Kept apart from keyless,
#: a track READ and found atonal.
TERMINAL_UNANALYSABLE = "skipped-unanalysable"
#: The terminal status for a file libsndfile cannot open on a machine with no
#: ffmpeg to try it (U263). Apart from ``TERMINAL_UNDECODABLE``, which every
#: decoder that could read the file refused.
TERMINAL_NO_DECODER = "skipped-no-decoder"

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

#: How far a head's tempo and key agree with rekordbox's own analysis of the
#: same files, measured 2026-09-30 over 299 library files whose stored tempo
#: is not a whole number (a whole one may be a tag's), so a head is presented
#: as a measurement with a known error. The shape is
#: ``analysis.agreement.Agreement.as_dict``'s, so re-recording is a copy.
#: Every count was measured, none is a target. Re-measure with
#: ``scripts/head_agreement.py --analyse 300 --step 4`` after any change here
#: and replace every number in the same commit.
#:
#: THE KEY BUCKETS WERE READ WITH THE WHOLE TRACK METHOD, ``key_read_with``
#: (U276). A121's reading of every method over one sample (2026-11-12) rides
#: under ``key_by_method``; it recorded only equal counts, so nothing here is
#: derived from it.
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
    "key": {"equal": 158, "differs": 141},
    "key_read_with": "whole",
    "key_by_method": {
        "measured_on": date(2026, 11, 12).isoformat(),
        "files": 300,
        "equal": {"whole": 159, "windows": 157, "plain": 161},
        "seconds": {"whole": 663, "windows": 453, "plain": 341},
    },
}


def head_agreement(window: tuple[int, int] | None = None) -> dict[str, Any]:
    """A fresh copy of the recorded agreement, safe to place in an envelope.

    ``window`` is the floor and ceiling the run bound; ``applies_to_window``
    says whether it is the one measured, and the numbers stay either way.
    """
    record = copy.deepcopy(_HEAD_AGREEMENT)
    measured = (record["window"]["floor"], record["window"]["ceiling"])
    record["applies_to_window"] = window is None or tuple(window) == measured
    # Beside ``key_read_with``, so a reader can tell the two apart (U276).
    record["key_method"] = KEY_DEFAULT
    return record


def heavy_available() -> bool:
    """Whether the analysis extra is importable HERE, in this process.

    ``analyse_file`` answers a missing extra and a keyless track with the same
    None, so a worker asks this first.
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
    interpolated as the head's is; a window without a pulse is passed over.
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


#: How the key's chroma is taken (U241): ``KEY_WHOLE`` from the harmonic part
#: of the whole track, ``KEY_WINDOWS`` the same from windows spread over it,
#: ``KEY_PLAIN`` from the whole track without the separation.
#:
#: ``KEY_PLAIN`` IS THE DEFAULT SINCE U276: over 300 library files (A121,
#: 2026-11-12) it agreed with rekordbox the most, 161 against whole's 159, in
#: about half the time. A toneless file the whole chroma read as keyless now
#: gets a key and a head. The other two stay selectable for a later reading.
KEY_WHOLE = "whole"
KEY_WINDOWS = "windows"
KEY_PLAIN = "plain"
KEY_METHODS = (KEY_WHOLE, KEY_WINDOWS, KEY_PLAIN)
#: The method a caller that names none gets: ``analyze run``, its workers, the
#: warm up and both measuring scripts.
KEY_DEFAULT = KEY_PLAIN
#: The harmonic margin the key's separation has always used.
KEY_HARMONIC_MARGIN = 4
#: The windowed method's windows, one centred in each sixth, so a key that
#: changes late is heard in proportion to how much of the track it holds.
KEY_WINDOW_COUNT = 6
KEY_WINDOW_SECONDS = 30.0

#: The stages a run's time is reported under (U241), in order, as a method
#: that separates meets them. ``scripts/analyze_stages.py`` prints them.
STAGES = ("decode", "tempo_drift", "harmonic", "chroma_key", "energy")


def stages_of(method: str) -> tuple[str, ...]:
    """The stages a head read with the key ``method`` meets: plain has no ``harmonic`` (U276)."""
    if method not in KEY_METHODS:
        raise ValueError(f"the key method is one of {KEY_METHODS}, not {method!r}")
    if method == KEY_PLAIN:
        return tuple(stage for stage in STAGES if stage != "harmonic")
    return STAGES


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


def key_windows(
    length: int,
    rate: int,
    *,
    count: int = KEY_WINDOW_COUNT,
    seconds: float = KEY_WINDOW_SECONDS,
) -> list[tuple[int, int]] | None:
    """Where the windowed key reads, as sample ranges, or None for the whole track.

    None when the windows would cover the track anyway, so the two methods are
    one on short material.
    """
    width = int(seconds * rate)
    if count < 1 or width < 1 or length <= count * width:
        return None
    part = length / count
    ranges: list[tuple[int, int]] = []
    for index in range(count):
        start = int(part * (index + 0.5) - width / 2)
        ranges.append((start, start + width))
    return ranges


def key_profile(
    samples: Any,
    rate: int,
    *,
    method: str = KEY_DEFAULT,
    timings: MutableMapping[str, float] | None = None,
) -> Any:
    """The twelve bin chroma profile the key is read from: the mean over every frame read.

    Each window is separated and transformed by itself, so it costs the
    windows' length and not the track's.
    """
    import librosa
    import numpy as np

    from cratekit.analysis import separation

    if method not in KEY_METHODS:
        raise ValueError(f"the key method is one of {KEY_METHODS}, not {method!r}")
    pieces = [samples]
    if method == KEY_WINDOWS:
        ranges = key_windows(int(samples.shape[-1]), rate)
        if ranges is not None:
            pieces = [samples[start:stop] for start, stop in ranges]
    frames = []
    for piece in pieces:
        if method != KEY_PLAIN:
            with timed(timings, "harmonic"):
                piece = separation.harmonic(piece, margin=KEY_HARMONIC_MARGIN)
        with timed(timings, "chroma_key"):
            frames.append(librosa.feature.chroma_cqt(y=piece, sr=rate))
    if len(frames) == 1:
        return frames[0].mean(axis=1)
    return np.concatenate(frames, axis=1).mean(axis=1)


def camelot_of(profile: Any) -> str | None:
    """The Camelot key whose template the chroma correlates with best, first best kept.

    None for a profile with no energy in it or one that is not a number.
    """
    import numpy as np

    profile = np.asarray(profile)
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
    return _KEY_TO_CAMELOT.get(best_key or "")


def analyse_file(
    path: Path,
    *,
    calibration: Any = None,
    tempo_window: tuple[int, int] = (DEFAULT_TEMPO_FLOOR, DEFAULT_TEMPO_CEILING),
    drift_cut: float = DEFAULT_DRIFT_CUT,
    key: str = KEY_DEFAULT,
    timings: MutableMapping[str, float] | None = None,
) -> dict[str, Any] | None:
    """Return camelot, tempo, drift and energy, or None when detection cannot run.

    ``key`` is a :data:`KEY_METHODS` name (U241, U276); ``timings`` collects
    each stage's wall time when given. ``tempo_window`` and ``drift_cut`` are
    the configured values the run binds (U157). Energy is measured under a
    calibration by the restamp's own measure, so a file the run scored needs no
    restamp (U344), and is otherwise an honest absence whose ``energy_status``
    names why (U58). librosa is imported here so a slim install can still
    import the package.
    """
    if key not in KEY_METHODS:
        # A DEFECT IN THE CALLER, raised before anything is opened.
        raise ValueError(f"the key method is one of {KEY_METHODS}, not {key!r}")
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
        # AT THE ENERGY MEASURE RATE, the rate the head's tempo and key are
        # read at, and THROUGH THE ONE DECODER (U263). The energy is measured
        # from the file, as the restamp measures it (U344).
        with timed(timings, "decode"):
            y, sr = decode.load(path, MEASURE_RATE)
        if y.size == 0:
            return {"path": path, "terminal": TERMINAL_UNDECODABLE}
    except decode.DecoderMissing:
        return {"path": path, "terminal": TERMINAL_NO_DECODER}
    except Exception:
        # A FILE THE DECODER COULD NOT READ IS NOT A TRACK WITH NO KEY.
        return {"path": path, "terminal": TERMINAL_UNDECODABLE}
    try:
        floor, ceiling = tempo_window
        # THE DRIFT IS READ OVER THE WHOLE TRACK, always (U241).
        with timed(timings, "tempo_drift"):
            tempo, drift = measure_tempo_and_drift(y, sr, floor=floor, ceiling=ceiling)
        if tempo is None:
            return {"path": path, "terminal": TERMINAL_UNANALYSABLE}
        rate = int(tempo + 0.5)
        profile = key_profile(y, sr, method=key, timings=timings)
    except Exception:
        # DECODED AND NOT ANALYSABLE IS NOT KEYLESS EITHER.
        return {"path": path, "terminal": TERMINAL_UNANALYSABLE}
    camelot = camelot_of(profile)
    if camelot is None:
        return None
    with timed(timings, "energy"):
        level, status = energy_from_path(path, calibration=calibration)
    return {
        "path": path,
        "camelot": camelot,
        "rate": rate,
        # None and unknown for a track with too little pulse to judge (U157).
        "drift": drift,
        "drift_verdict": drift_words.verdict(drift, drift_cut),
        "energy": level,
        "energy_status": status,
    }


def energy_from_path(path: Any, *, calibration: Any) -> tuple[int | None, str]:
    """The level and its status for ``path``, measured as ``analyze restamp`` measures it.

    No calibration measures nothing. NOT FROM THE HEAD'S SAMPLES: the head
    resamples the whole track before it slices, and the restamp decodes the
    slice alone, so the two differed in every feature of a track longer than
    the slice, and a track on a decile cut took two levels (U344). Through
    :func:`energy.measure`, the restamp's own call, so one file under one
    calibration has one level, and the head's tempo is not handed down.
    """
    from cratekit.analysis import energy

    if calibration is None:
        return None, energy.STATUS_UNCALIBRATED
    features = energy.measure(Path(path))
    if features is None:
        return None, energy.STATUS_FEATURES_UNAVAILABLE
    return energy.level_for(features, calibration), energy.STATUS_CALIBRATED
