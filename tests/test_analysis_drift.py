"""U157: how far a track's tempo moves, measured on tracks whose tempo is known.

The drift is the spread of the tempo the tempogram reads window by window, as
a percent of its middle. Driven here on synthetic signals built to a known
tempo curve: a click train with off beat hats and a little noise, the shape a
drum machine plays, held constant, ramped, stepped, and broken by a long
beatless pad; plus noise, a pad alone and a clip too short to judge. Skipped
where the analysis extra is absent, because the tempogram is librosa's.

The thresholds the assertions hold are the shipped cut's two sides, so a
steady reading is one a landing would never mark and a variable one is one it
always would. What the drift of a real library's tracks reads is not measured
here, and is owed to an attended sitting.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest

from cratekit.analysis import detect
from cratekit.core import config, drift

np = pytest.importorskip("numpy")
librosa = pytest.importorskip("librosa")
soundfile = pytest.importorskip("soundfile")

RATE = detect.MEASURE_RATE
CUT = config.DEFAULT_DRIFT_CUT
SECONDS = 120.0


def _train(tempo_at: Callable[[float], float], seconds: float, *, every: float = 1.0) -> np.ndarray:
    """One short burst per beat, the beat's length read off ``tempo_at`` as it goes.

    ``every`` is the fraction of a beat between bursts, so a half puts one on
    each off beat as well.
    """
    samples = np.zeros(int(RATE * seconds), dtype=np.float32)
    burst = np.hanning(200).astype(np.float32)
    at = 0.0
    while True:
        start = int(round(at * RATE))
        if start + burst.size > samples.size:
            break
        samples[start : start + burst.size] += burst
        at += every * 60.0 / tempo_at(at)
    return samples


def _drums(tempo_at: Callable[[float], float], seconds: float = SECONDS, *, seed: int = 0):
    """A kick on every beat, hats between them, and a little noise under both."""
    rng = np.random.default_rng(seed)
    kick = _train(tempo_at, seconds)
    hats = 0.3 * _train(tempo_at, seconds, every=0.5)
    return kick + hats + 0.02 * rng.standard_normal(kick.size).astype(np.float32)


def _pad(seconds: float = SECONDS) -> np.ndarray:
    """Four sustained tones, slowly swelling: harmony with no pulse in it."""
    t = np.arange(int(RATE * seconds)) / RATE
    swell = 0.6 + 0.4 * np.sin(2 * np.pi * 0.05 * t)
    tone = sum(np.sin(2 * np.pi * hz * t) for hz in (110.0, 165.0, 220.0, 277.0))
    return (0.05 * tone * swell).astype(np.float32)


def _drift(samples: np.ndarray) -> tuple[float | None, float | None]:
    return detect.measure_tempo_and_drift(samples, RATE, floor=80, ceiling=160)


# ---------------------------------------------------------------------------
# Steady reads steady
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("known", [96.0, 124.0, 128.0, 140.0])
def test_a_constant_tempo_scores_steady(known):
    tempo, moved = _drift(_drums(lambda _at: known))
    assert tempo == pytest.approx(known, abs=1.0)
    assert moved is not None and moved < 0.5, moved
    assert drift.verdict(moved, CUT) == drift.STEADY


def test_a_constant_tempo_with_a_long_beatless_breakdown_still_scores_steady():
    """Forty seconds of pad and hiss in the middle of a steady track. Read
    window by window with no gate, those windows read 125, 130 and 136 and
    the track scores variable; gated, they are passed over."""
    samples = _drums(lambda _at: 124.0)
    rng = np.random.default_rng(1)
    start, stop = int(40 * RATE), int(80 * RATE)
    samples[start:stop] = _pad()[start:stop] + 0.01 * rng.standard_normal(stop - start)
    _tempo, moved = _drift(samples)
    assert moved is not None and moved < 0.5, moved
    assert drift.verdict(moved, CUT) == drift.STEADY


def test_a_human_timing_wobble_on_a_constant_tempo_scores_steady():
    """Every hit up to about a dozen milliseconds off the grid, the looseness of
    a played part, around a tempo that does not move."""
    rng = np.random.default_rng(2)
    clean = _drums(lambda _at: 112.0)
    shifted = np.zeros_like(clean)
    hop = int(0.25 * RATE)
    for start in range(0, clean.size - hop, hop):
        offset = int(rng.normal(0.0, 0.012) * RATE)
        lo = min(max(start + offset, 0), clean.size - hop)
        shifted[lo : lo + hop] += clean[start : start + hop]
    _tempo, moved = _drift(shifted)
    assert moved is not None and moved < CUT, moved


# ---------------------------------------------------------------------------
# Moving reads variable
# ---------------------------------------------------------------------------


def test_a_tempo_ramp_scores_variable():
    """118 to 126 over two minutes, a band pushing through a track."""
    _tempo, moved = _drift(_drums(lambda at: 118.0 + 8.0 * at / SECONDS))
    assert moved is not None and moved > 3.0, moved
    assert drift.verdict(moved, CUT) == drift.VARIABLE


def test_a_stepped_change_scores_variable():
    """120 for the first minute and 128 for the second, an edit of two takes."""
    _tempo, moved = _drift(_drums(lambda at: 120.0 if at < 60.0 else 128.0))
    assert moved is not None and moved > 5.0, moved
    assert drift.verdict(moved, CUT) == drift.VARIABLE


@pytest.mark.parametrize(
    ("first", "second"),
    [(120.0, 140.0), (112.0, 130.0), (100.0, 125.0), (140.0, 120.0)],
    ids=["up-a-sixth", "up-a-sixth-slower", "up-a-quarter", "down-a-seventh"],
)
def test_a_step_wider_than_the_heads_own_section_still_scores_variable(first, second):
    """The head names the tempo of one section; the other section's windows
    must still be read, or a two tempo track is tagged steady and analysed
    Normal, which the first band of twelve percent did to every one of these."""
    _tempo, moved = _drift(_drums(lambda at: first if at < 60.0 else second))
    assert moved is not None and moved > 10.0, moved
    assert drift.verdict(moved, CUT) == drift.VARIABLE


def test_a_section_of_hats_at_three_to_two_over_a_steady_pulse_is_not_a_drift():
    """Forty seconds where only hats play, three to every two beats, over a
    pulse at 100 that does not move. A window searched wide enough to reach
    the hats' own rate would read 150 there and call the track variable."""
    samples = _drums(lambda _at: 100.0)
    start, stop = int(40 * RATE), int(80 * RATE)
    hats = 0.6 * _train(lambda _at: 150.0, SECONDS)
    noise = 0.02 * np.random.default_rng(5).standard_normal(stop - start)
    samples[start:stop] = hats[start:stop] + noise.astype(np.float32)
    _tempo, moved = _drift(samples)
    assert moved is not None and moved < 0.5, moved
    assert drift.verdict(moved, CUT) == drift.STEADY


def test_the_score_grows_with_how_far_the_tempo_moves():
    small = _drift(_drums(lambda at: 120.0 + 3.0 * at / SECONDS))[1]
    large = _drift(_drums(lambda at: 120.0 + 9.0 * at / SECONDS))[1]
    assert small is not None and large is not None
    assert 0.5 < small < large


# ---------------------------------------------------------------------------
# Too little to judge is unknown
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "samples",
    [
        pytest.param(
            lambda: 0.1 * np.random.default_rng(3).standard_normal(int(RATE * SECONDS)).astype(
                np.float32
            ),
            id="noise",
        ),
        pytest.param(_pad, id="pad"),
        pytest.param(lambda: _drums(lambda _at: 124.0, 20.0), id="twenty-seconds"),
    ],
)
def test_a_beatless_or_very_short_file_scores_unknown(samples):
    _tempo, moved = _drift(samples())
    assert moved is None
    assert drift.verdict(moved, CUT) == drift.UNKNOWN


# ---------------------------------------------------------------------------
# The detector carries it
# ---------------------------------------------------------------------------


def test_the_tempo_is_the_one_measure_tempo_names():
    samples = _drums(lambda at: 120.0 if at < 60.0 else 128.0)
    assert detect.measure_tempo(samples, RATE, floor=80, ceiling=160) == _drift(samples)[0]


def _chord(seconds: float = SECONDS) -> np.ndarray:
    t = np.arange(int(RATE * seconds)) / RATE
    tone = np.zeros_like(t, dtype=np.float32)
    for hz in (220.0, 261.63, 329.63):
        for octave in (0.5, 1.0, 2.0):
            tone += (0.1 * np.sin(2 * np.pi * hz * octave * t)).astype(np.float32)
    return tone


@pytest.mark.parametrize(
    ("curve", "expected"),
    [
        (lambda _at: 124.0, drift.STEADY),
        (lambda at: 120.0 if at < 60.0 else 128.0, drift.VARIABLE),
    ],
    ids=["steady", "stepped"],
)
def test_analyse_file_answers_the_drift_and_its_verdict(tmp_path: Path, curve, expected):
    path = tmp_path / "track.wav"
    soundfile.write(str(path), _drums(curve) + _chord(), RATE, subtype="PCM_16")
    found = detect.analyse_file(path)
    assert found is not None and found.get("terminal") is None, found
    assert found["drift_verdict"] == expected
    assert isinstance(found["drift"], float)


def test_the_verdict_follows_the_cut_the_run_binds(tmp_path: Path):
    path = tmp_path / "track.wav"
    soundfile.write(str(path), _drums(lambda at: 120.0 if at < 60.0 else 128.0) + _chord(), RATE)
    found = detect.analyse_file(path, drift_cut=50.0)
    assert found is not None and found["drift_verdict"] == drift.STEADY


def test_a_pulse_with_too_little_pulse_to_judge_carries_unknown_and_no_drift(tmp_path: Path):
    path = tmp_path / "short.wav"
    soundfile.write(str(path), _drums(lambda _at: 124.0, 20.0) + _chord(20.0), RATE)
    found = detect.analyse_file(path)
    assert found is not None and found.get("terminal") is None, found
    assert found["drift"] is None and found["drift_verdict"] == drift.UNKNOWN


def test_the_payload_carries_no_tempo_key_beyond_the_head_rate(tmp_path: Path):
    from tests.test_no_beatgrid_ever import FORBIDDEN_TAG_KEYS

    path = tmp_path / "track.wav"
    soundfile.write(str(path), _drums(lambda _at: 124.0) + _chord(), RATE)
    found = detect.analyse_file(path)
    assert found is not None
    assert not set(found) & FORBIDDEN_TAG_KEYS
