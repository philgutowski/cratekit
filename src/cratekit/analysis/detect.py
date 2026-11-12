"""Read-only detectors. Tempo is measured. It is never emitted as a grid.

The no-beatgrid rule is about writing: a grid element, a tempo tag, an
average-tempo field, an analysis-file grid. Reading a tempo tag or
computing a tempo from audio is how energy scoring and the filename head
get a number. This module never assigns into a tag mapping and never
writes XML.
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
#: short for a tempo, or a signal the chroma or separation step raised on.
#: Kept apart from keyless, which is a track the analyser READ and found
#: atonal, for the reason ``TERMINAL_UNDECODABLE`` is kept apart from it.
TERMINAL_UNANALYSABLE = "skipped-unanalysable"
#: The terminal status for a file librosa did not read and libsndfile cannot
#: open, on a machine with no ffmpeg to try it (U263): an M4A, or a file too
#: damaged to open, which only ffmpeg could have judged. The decoder that was
#: never tried is named, so it is kept apart from ``TERMINAL_UNDECODABLE``,
#: which every decoder that could read the file has refused.
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


#: The frame hop the onset envelope and the tempogram are computed at, in
#: samples of ``MEASURE_RATE``. Named because it sets the estimator's raw
#: precision: a tempogram bin is one frame of lag, and at this rate and hop the
#: bins near 128 beats per minute sit about six apart (lag 20 reads 129.2, lag
#: 21 reads 123.0), which is the whole of the "off by one to three" bucket
#: R-744 recorded. The interpolation below is what recovers the precision.
TEMPO_HOP = 512
#: The prior over metrical levels, a log-normal in octaves around a centre,
#: with the centre and the width librosa's own estimator defaults to. The FORM
#: is not librosa's: it adds the prior to a log-compressed strength, and this
#: multiplies the prior into the linear strength, which pulls harder toward
#: the centre when two levels are close. Kept in this form because it is the
#: form that was measured: on the sample it beat a flat window by 22 exact
#: agreements in 299 (docs/cutover.md, sitting 22). The window is the setting,
#: the prior is the method, and a change to either is re-measured.
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
#: exactly and 19 keys of 22 matched. The shape is the one
#: ``analysis.agreement.Agreement.as_dict`` answers and the script prints
#: with ``--json``, so re-recording is a copy: the four tempo buckets, the
#: count within one beat beside them, and the two key buckets. "Other level"
#: is a pulse read at a related level rekordbox did not choose, three to two
#: or four to three, and is the method's own rate rather than a setting. Every
#: count was measured, none is a target. Re-measure with
#: ``scripts/head_agreement.py --analyse 300 --step 4`` after any change to
#: this module and replace every number here in the same commit.
#:
#: THE KEY BUCKETS WERE READ WITH THE WHOLE TRACK METHOD, which was the default
#: then, and ``key_read_with`` says so (U276). The run reads the key with
#: :data:`KEY_DEFAULT` since, and A121's reading of 2026-11-12 is carried
#: beside the record under ``key_by_method``, every method over one sample:
#: the keys equal to rekordbox's, and the wall time of the 300. That sitting
#: recorded the equal counts and the tempo's equal count only, not the
#: other buckets, so the record is not replaced whole and no ``differs`` is
#: written for it: a record's buckets come from one run of the script, and
#: none here is derived.
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

    ``key_method`` is the method the run reads the key with, which the
    ``key`` buckets were not read with when it differs from
    ``key_read_with``; ``key_by_method`` is the reading of every method over
    one sample, the run's own among them.

    ``window`` is the floor and ceiling the run bound to the detector. The
    record was measured under one window, and a DJ who raised theirs is not
    shown a rate nobody measured for it: ``applies_to_window`` says whether
    the bound window is the measured one, and the numbers stay so the reader
    can see what was measured rather than an absence.
    """
    record = copy.deepcopy(_HEAD_AGREEMENT)
    measured = (record["window"]["floor"], record["window"]["ceiling"])
    record["applies_to_window"] = window is None or tuple(window) == measured
    # THE METHOD THE RUN READS THE KEY WITH, beside the method the buckets
    # were read with, so a reader can tell the two apart (U276).
    record["key_method"] = KEY_DEFAULT
    return record


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

    THE OFFSET IS HELD TO HALF A BIN EITHER WAY. The bin was chosen on the
    scored strength, prior and window applied, and the parabola is fitted on
    the raw strength, so a stronger raw neighbour can put the vertex past the
    midpoint toward it. Past the midpoint the neighbour would have been the
    bin, had the score allowed it, so the answer stays on this bin's side.
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

    ``strength`` is one autocorrelation over lag, in frames, bin zero the zero
    lag. The prior is the log-normal over metrical levels the constants above
    describe, and the window is applied on top of it: a bin whose tempo falls
    from ``floor`` to ``ceiling``, both included, is a candidate, every other
    bin is not, so a pulse that reads at 166 with a window of 80 to 160 is
    named 83, and named 166 when the window is raised. The interpolated answer
    is held inside the window too, because a bin at the window's edge can
    have its parabola lean past the edge, and the window is the contract.
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
    inside = (frequencies >= floor) & (frequencies <= ceiling)
    if not np.any(inside):
        return None
    score = np.where(inside, np.nan_to_num(strength * prior, nan=-np.inf), -np.inf)
    index = int(np.argmax(score))
    lag = _interpolated_peak(strength, index)
    if lag <= 0.0:
        return None
    return float(min(max(60.0 * rate / (hop * lag), float(floor)), float(ceiling)))


#: The drift measurement (U157), every number a property of the method rather
#: than a setting, measured on synthetic tracks whose tempo is known by
#: construction (``tests/test_analysis_drift.py``); the setting is the cut,
#: ``analysis.drift_cut``. A window is about ten seconds of the tempogram's
#: frames, long enough to hold a dozen beats at the floor and short enough
#: that a six minute track gives three dozen readings.
DRIFT_WINDOW_SECONDS = 10.0
#: How far either side of the track's own tempo a window's peak is looked
#: for, as a factor of it: from the tempo over 1.25 to the tempo times 1.25.
#: Held to a band so a window cannot read a related metrical level, half or
#: double, three to two or four to three, which would be a jump in the
#: reading and not a drift in the music: a steady 100 with a section of hats
#: at 150 reads 48 percent at a band of 0.5 and 0.06 at this one. Wide enough
#: that a step to either side of the head reaches the other section, 120 to
#: 140 or 100 to 125, which the first band of 0.12 read as steady because
#: the head named one section and the other fell outside it (the review of
#: U157). A step past a quarter is read as the section the head named.
DRIFT_BAND = 0.25
#: A window counts only when it carries a pulse: its onset strength at least
#: this fraction of the track's median window, so a breakdown is passed over
#: rather than read as drift, and at least the absolute floor below, so a
#: track that is all pad is not judged on the noise in its envelope.
DRIFT_ONSET_RELATIVE = 0.5
DRIFT_ONSET_FLOOR = 0.2
#: And a clear peak: the band's strongest lag stands at least this fraction
#: above the mean of the lags from half to one and a half of its period. A
#: drum pattern stands 0.1 to 0.2 above it, white noise and a beatless pad
#: under 0.02, which is where the gate sits between.
DRIFT_PULSE_CONTRAST = 0.05
#: Fewer counted windows than this is too little rhythmic material to judge,
#: and the drift is unknown rather than a spread of two numbers.
DRIFT_MIN_WINDOWS = 3
#: The spread is from this percentile of the counted windows' tempos to its
#: complement, so one odd window in ten moves nothing.
DRIFT_PERCENTILE = 10.0


def _onset_and_tempogram(samples: Any, rate: int) -> tuple[Any, Any]:
    """The onset envelope and the tempogram librosa's estimator computes, taken once."""
    import librosa

    envelope = librosa.onset.onset_strength(y=samples, sr=rate, hop_length=TEMPO_HOP)
    tempogram = librosa.feature.tempogram(onset_envelope=envelope, sr=rate, hop_length=TEMPO_HOP)
    return envelope, tempogram


def measure_tempo(samples: Any, rate: int, *, floor: int, ceiling: int) -> float | None:
    """The tempo of decoded samples, inside the window, to a fraction of a beat.

    The onset envelope and the tempogram are the ones librosa's estimator
    computes; what differs is the window and the interpolation, for the
    reasons the constants above give. None when the envelope is too short to
    hold a period inside the window.
    """
    return measure_tempo_and_drift(samples, rate, floor=floor, ceiling=ceiling)[0]


def measure_tempo_and_drift(
    samples: Any, rate: int, *, floor: int, ceiling: int
) -> tuple[float | None, float | None]:
    """The tempo, and how far it moves over the track, from ONE tempogram (U157).

    The drift is None when the tempo is, and when the track holds too little
    pulse to judge, :func:`drift_from_tempogram`'s answer.
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

    ``tempogram`` is librosa's, one autocorrelation column per frame, and
    ``envelope`` the onset strength it was taken from. The frames are cut
    into windows of :data:`DRIFT_WINDOW_SECONDS`; each window's columns are
    averaged and its peak is found inside :data:`DRIFT_BAND` of ``tempo``
    and interpolated as the head's is, so each window reads the track's own
    pulse to a fraction of a beat. A window without a pulse, the gates above,
    is passed over. The answer is the spread from the tenth to the ninetieth
    percentile of the windows' tempos as a percent of their median, so a
    steady track reads near zero whatever its breakdowns, and a ramp or a
    stepped change reads the distance it moves.

    NONE IS NOT STEADY. Fewer than :data:`DRIFT_MIN_WINDOWS` windows with a
    pulse, a beatless, ambient or very short file, has no drift to read, and
    the caller names it unknown rather than guessing either way.
    """
    import librosa
    import numpy as np

    envelope = np.asarray(envelope, dtype=float).reshape(-1)
    tempogram = np.asarray(tempogram, dtype=float)
    if tempo <= 0.0 or tempogram.ndim != 2 or tempogram.shape[0] < 3:
        return None
    per = int(round(DRIFT_WINDOW_SECONDS * rate / hop))
    windows = min(tempogram.shape[1], envelope.size) // per
    # NO WINDOW AT ALL is answered here, before a median of nothing; how many
    # windows are enough is asked once, of the windows that carry a pulse.
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


#: How the chroma the key is read from is taken (U241). ``KEY_WHOLE`` is the
#: harmonic part of the whole track, then its chroma, which shipped as the
#: default until U276. ``KEY_WINDOWS`` reads the same chroma from windows
#: spread evenly over the track. ``KEY_PLAIN`` reads the whole track's chroma
#: without the harmonic separation.
#:
#: ``KEY_PLAIN`` IS THE DEFAULT SINCE U276, on a reading of all three against
#: rekordbox's own keys. The bar U241 set was agreement with rekordbox on the
#: library within one percentage point of the whole track's rate, read at an
#: attended sitting and never on a fixture. A121 read it on 2026-11-12, over
#: 300 library files rekordbox analysed itself, every fourth eligible one
#: (``scripts/head_agreement.py --analyse 300 --step 4 --key ...``): whole 159
#: equal (53.0%) in 663 seconds, windows 157 (52.3%) in 453, plain 161 (53.7%)
#: in 341. Both cheaper methods met the bar; plain agreed the most and cost the
#: least, about half of whole's time, because the separation is what it skips.
#: The tempo, the drift and the energy do not read the key's chroma, so what
#: can move is the key and whether there is one: the review of U276 drove a
#: file of clicks with no tone, which the whole track's chroma read as keyless
#: (``skipped-no-key``) and the plain chroma keys, so ``analyze run`` now
#: writes it a key and a head. Four drum tools, noise and the 23 track
#: synthetic set were keyed under both. ``KEY_WHOLE`` and ``KEY_WINDOWS`` stay
#: selectable by name so a later sitting can read all three again.
KEY_WHOLE = "whole"
KEY_WINDOWS = "windows"
KEY_PLAIN = "plain"
KEY_METHODS = (KEY_WHOLE, KEY_WINDOWS, KEY_PLAIN)
#: The method a caller that names none gets: ``analyze run``, its workers, the
#: warm up and both measuring scripts.
KEY_DEFAULT = KEY_PLAIN
#: The harmonic margin the key's separation has always used.
KEY_HARMONIC_MARGIN = 4
#: The windowed method's windows: how many, and how long each is. Six of
#: thirty seconds is three minutes of a track however long it runs. They are
#: spread, one centred in each sixth, so a key that changes late is heard in
#: proportion to how much of the track it holds, where the opening minutes
#: alone would never hear it.
KEY_WINDOW_COUNT = 6
KEY_WINDOW_SECONDS = 30.0

#: The stages a run's time is reported under (U241), in the order they run.
#: ``scripts/analyze_stages.py`` prints them; the vocal pass adds its own two.
#: Every one of them is met by a method that separates; :func:`stages_of`
#: answers the ones a given method meets.
STAGES = ("decode", "tempo_drift", "harmonic", "chroma_key", "energy")


def stages_of(method: str) -> tuple[str, ...]:
    """The stages a head read with the key ``method`` meets, in the order they run.

    The plain chroma never separates, so it meets no ``harmonic`` stage
    (U276), and a report of its time does not count one.
    """
    if method not in KEY_METHODS:
        raise ValueError(f"the key method is one of {KEY_METHODS}, not {method!r}")
    if method == KEY_PLAIN:
        return tuple(stage for stage in STAGES if stage != "harmonic")
    return STAGES


@contextmanager
def timed(timings: MutableMapping[str, float] | None, stage: str) -> Iterator[None]:
    """Add the wall time of the block to ``timings[stage]``, or do nothing for None.

    The measurement U241's record is built from is the shipped functions timed
    in place, through this, never a copy of them timed beside them.
    """
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

    The track is cut into ``count`` equal parts and one window sits in the
    middle of each. None when the windows together would cover the track
    anyway: a track no longer than ``count`` windows, a stinger shorter than
    one above all, is read whole, so the windowed method and the whole track
    method are one method on short material.
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
    """The twelve bin chroma profile the key is read from, by ``method``.

    One profile whatever the method: the mean chroma over every frame read.
    For the windowed method the frames are the windows' own, each window
    separated and transformed by itself, so its cost is the windows' length
    and not the track's.
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
    """The Camelot key whose profile the chroma correlates with best, or None.

    The twenty four correlations against the major and minor templates, the
    first best kept, exactly as the detector has always chosen. None for a
    profile with no energy in it, and for one that is not a number, where no
    correlation compares greater than any other.
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

    ``key`` is how the key's chroma is taken, :data:`KEY_METHODS`, the plain
    chroma unless a caller names another (U241, U276). ``timings`` collects
    the wall time of each stage :func:`stages_of` the method names when a
    mapping is passed, and costs nothing when it is not.

    ``tempo_window`` is the configured floor and ceiling; the run binds it from
    ``analysis.tempo_floor`` and ``analysis.tempo_ceiling`` beside the
    calibration, and a caller that passes nothing gets the shipped default.
    ``drift_cut`` is ``analysis.drift_cut``, bound the same way, which the
    drift's verdict is read against (U157).

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
    if key not in KEY_METHODS:
        # A DEFECT IN THE CALLER, raised before anything is imported or opened
        # rather than swallowed below as a track that could not be analysed.
        raise ValueError(f"the key method is one of {KEY_METHODS}, not {key!r}")
    try:
        import librosa  # noqa: F401 - asked for so its absence is the extra's absence
        import numpy  # noqa: F401 - asked for so its absence is the extra's absence
    except ImportError:
        return None
    # THIS PROCESS'S FIRST HEAD IS PRECEDED BY A WARM UP, ALONE (U241). librosa's
    # compiled kernels are cached on disk, and two processes filling that cache
    # together crash and leave it damaged; ``analysis.warm`` says how that was
    # found. Here, rather than in a worker's initializer, so the driver, a
    # worker, a script and a second command all take the same turn. ``decode``
    # is the one decoder (U263).
    from cratekit.analysis import decode, warm

    warm.kernels()
    try:
        # AT THE ENERGY MEASURE RATE, one constant for both, because every
        # spectral feature is rate dependent and the calibration fitted on the
        # restamp path scores the samples decoded here.
        # THROUGH THE ONE DECODER (U263): ``librosa.load``'s samples, bit for
        # bit, for every file it reads, mixed to mono with one add (U264),
        # and ffmpeg only for a file libsndfile cannot open, an M4A on
        # librosa 1.0.
        with timed(timings, "decode"):
            y, sr = decode.load(path, MEASURE_RATE)
        if y.size == 0:
            return {"path": path, "terminal": TERMINAL_UNDECODABLE}
    except decode.DecoderMissing:
        return {"path": path, "terminal": TERMINAL_NO_DECODER}
    except Exception:
        # A FILE THE DECODER COULD NOT READ IS NOT A TRACK WITH NO KEY. The
        # first version returned None here, which the light pass reported as
        # skipped-no-key: a truncated download was told to the person as
        # atonal, a clean report over a file the tool could not read.
        return {"path": path, "terminal": TERMINAL_UNDECODABLE}
    try:
        floor, ceiling = tempo_window
        # THE DRIFT IS READ OVER THE WHOLE TRACK, always (U241): it exists to
        # find a tempo that moves somewhere in it, and it is two percent of
        # the run.
        with timed(timings, "tempo_drift"):
            tempo, drift = measure_tempo_and_drift(y, sr, floor=floor, ceiling=ceiling)
        if tempo is None:
            return {"path": path, "terminal": TERMINAL_UNANALYSABLE}
        rate = int(tempo + 0.5)
        profile = key_profile(y, sr, method=key, timings=timings)
    except Exception:
        # DECODED AND NOT ANALYSABLE IS NOT KEYLESS EITHER. A stinger too short
        # for a tempo estimate, or a signal the separation raised on, was
        # reported as atonal by the first version, the same shape as the
        # undecodable case above one step later.
        return {"path": path, "terminal": TERMINAL_UNANALYSABLE}
    camelot = camelot_of(profile)
    if camelot is None:
        return None
    with timed(timings, "energy"):
        level, status = energy_from_samples(y, sr, calibration=calibration)
    return {
        "path": path,
        "camelot": camelot,
        "rate": rate,
        # U157: the drift and its verdict, None and unknown for a track with
        # too little pulse to judge, which the finalize writes as it is.
        "drift": drift,
        "drift_verdict": drift_words.verdict(drift, drift_cut),
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
