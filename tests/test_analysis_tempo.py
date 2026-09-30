"""R-744: the tempo a head names is the one inside the window, to the beat.

The estimator's raw precision is one tempogram bin, about six beats per minute
near 128, which is where every "off by one to three" case came from. The
interpolation below recovers the fraction of a bin, and the window decides
which metrical level is named. Both are driven here on signals whose tempo is
known by construction: a click train, and a sustained chord for the key.
Skipped where the analysis extra is absent, because the estimator is
librosa's tempogram and there is nothing to drive without it.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.analysis import detect
from cratekit.core import config

np = pytest.importorskip("numpy")
librosa = pytest.importorskip("librosa")
soundfile = pytest.importorskip("soundfile")

RATE = detect.MEASURE_RATE


def _clicks(tempo: float, *, seconds: float = 24.0) -> np.ndarray:
    """A click train at ``tempo``, one short burst per beat."""
    samples = np.zeros(int(RATE * seconds), dtype=np.float32)
    period = 60.0 / tempo
    burst = np.hanning(200).astype(np.float32)
    beat = 0
    while True:
        start = int(round(beat * period * RATE))
        if start + burst.size > samples.size:
            break
        samples[start : start + burst.size] += burst
        beat += 1
    return samples


def _chord(pitches: tuple[float, ...], *, seconds: float = 24.0) -> np.ndarray:
    """Sustained sine tones at ``pitches`` in hertz, three octaves each."""
    t = np.arange(int(RATE * seconds)) / RATE
    tone = np.zeros_like(t, dtype=np.float32)
    for hz in pitches:
        for octave in (0.5, 1.0, 2.0):
            tone += (0.1 * np.sin(2 * np.pi * hz * octave * t)).astype(np.float32)
    return tone


A_MINOR = (220.0, 261.63, 329.63)  # A, C, E
C_MAJOR = (261.63, 329.63, 392.0)  # C, E, G


def _write(path: Path, samples: np.ndarray) -> Path:
    soundfile.write(str(path), samples, RATE, subtype="PCM_16")
    return path


# ---------------------------------------------------------------------------
# The pure estimator
# ---------------------------------------------------------------------------


def _autocorrelation_peaked_at(lag: float, size: int = 384) -> np.ndarray:
    """A synthetic tempogram aggregate with one narrow peak at a fractional lag."""
    bins = np.arange(size, dtype=float)
    return np.exp(-0.5 * ((bins - lag) / 0.8) ** 2)


def test_the_peak_between_bins_is_named_to_a_fraction_of_a_bin():
    strength = _autocorrelation_peaked_at(20.19)
    tempo = detect.tempo_from_autocorrelation(strength)
    assert tempo is not None
    # A bin near 128 is six wide; the parabola names the peak to under half a beat.
    assert abs(tempo - 60.0 * RATE / (detect.TEMPO_HOP * 20.19)) < 0.5


def test_the_strongest_bin_alone_would_be_off_by_bins():
    """What the interpolation buys: the bin nearest lag 20.19 reads 129.2."""
    strength = _autocorrelation_peaked_at(20.19)
    index = int(np.argmax(strength))
    assert index == 20
    bare = 60.0 * RATE / (detect.TEMPO_HOP * index)
    assert bare > 129.0
    assert abs(detect.tempo_from_autocorrelation(strength) - 127.9) < 0.5


def test_an_edge_bin_or_a_flat_run_answers_the_bin_itself():
    flat = np.ones(8)
    assert detect._interpolated_peak(flat, 3) == 3.0
    assert detect._interpolated_peak(flat, 0) == 0.0
    assert detect._interpolated_peak(flat, 7) == 7.0
    assert detect._interpolated_peak(np.array([0.0, 1.0, 0.0]), 1) == 1.0


def test_a_peak_outside_the_window_is_not_named_and_the_one_inside_is():
    # lag 15.57 is 166 beats per minute, lag 31.14 its half at 83.
    strength = _autocorrelation_peaked_at(15.57) + 0.6 * _autocorrelation_peaked_at(31.14)
    inside_default = detect.tempo_from_autocorrelation(strength, floor=80, ceiling=160)
    raised = detect.tempo_from_autocorrelation(strength, floor=100, ceiling=200)
    assert inside_default is not None and abs(inside_default - 83.0) < 1.0
    assert raised is not None and abs(raised - 166.0) < 1.0


def test_a_window_no_bin_falls_in_answers_none():
    strength = _autocorrelation_peaked_at(20.0, size=4)
    assert detect.tempo_from_autocorrelation(strength, floor=1000, ceiling=1001) is None
    assert detect.tempo_from_autocorrelation(np.ones(1)) is None


def test_the_prior_prefers_the_level_nearer_the_centre_inside_the_window():
    """Two equal peaks, at 90 and 135, both inside the window: the prior at
    120 picks the one nearer it, so a flat window would have been a coin
    toss and is not."""
    lag_90 = 60.0 * RATE / (detect.TEMPO_HOP * 90.0)
    lag_135 = 60.0 * RATE / (detect.TEMPO_HOP * 135.0)
    strength = _autocorrelation_peaked_at(lag_90) + _autocorrelation_peaked_at(lag_135)
    tempo = detect.tempo_from_autocorrelation(strength)
    assert tempo is not None and abs(tempo - 135.0) < 1.5


# ---------------------------------------------------------------------------
# Driven on audio
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("known", [100.0, 122.0, 128.0, 140.0])
def test_a_click_train_is_named_within_a_beat_of_its_tempo(known):
    tempo = detect.measure_tempo(_clicks(known), RATE, floor=80, ceiling=160)
    assert tempo is not None
    assert abs(tempo - known) < 1.0, (known, tempo)


def test_a_pulse_above_the_ceiling_is_named_by_its_value_inside_the_window():
    """A file at 166 is headed 83 under the shipped window, and 166 when the
    window is raised: the window is the setting that decides."""
    fast = _clicks(166.0)
    default = detect.measure_tempo(fast, RATE, floor=80, ceiling=160)
    raised = detect.measure_tempo(fast, RATE, floor=100, ceiling=200)
    assert default is not None and abs(default - 83.0) < 1.0
    assert raised is not None and abs(raised - 166.0) < 1.0


def test_a_pulse_below_the_floor_is_named_by_its_subdivision():
    """A 70 beat pulse with its eighth notes sounded, as a played track has
    them: the window holds 140 and not 70, so 140 is named. A bare click
    train at 70 carries no energy at 140 and would be named by noise, which
    is what the interpolated autocorrelation can and cannot see."""
    slow = _clicks(70.0) + 0.5 * _clicks(140.0)
    default = detect.measure_tempo(slow, RATE, floor=80, ceiling=160)
    assert default is not None and abs(default - 140.0) < 1.0


def test_the_head_equals_the_known_tempo_and_key_of_a_fixture_set(tmp_path):
    """The fixture set the brief asks for: files with a known tempo and key,
    and the head the detector would stamp equals them."""
    cases = [
        ("one.wav", 128.0, A_MINOR, "8A"),
        ("two.wav", 122.0, C_MAJOR, "8B"),
        ("three.wav", 100.0, A_MINOR, "8A"),
    ]
    for name, tempo, pitches, camelot in cases:
        path = _write(tmp_path / name, _clicks(tempo) + _chord(pitches))
        found = detect.analyse_file(path)
        assert found is not None and "terminal" not in found, (name, found)
        assert found["camelot"] == camelot, (name, found)
        assert found["rate"] == int(tempo), (name, found)


def test_the_window_the_file_is_analysed_under_is_the_one_handed_in(tmp_path):
    path = _write(tmp_path / "fast.wav", _clicks(166.0) + _chord(A_MINOR))
    shipped = detect.analyse_file(path)
    raised = detect.analyse_file(path, tempo_window=(100, 200))
    assert shipped is not None and abs(shipped["rate"] - 83) <= 1
    assert raised is not None and abs(raised["rate"] - 166) <= 1


def test_the_shipped_window_is_the_configured_default():
    import inspect

    signature = inspect.signature(detect.analyse_file)
    assert signature.parameters["tempo_window"].default == (
        config.DEFAULT_TEMPO_FLOOR,
        config.DEFAULT_TEMPO_CEILING,
    )


def test_a_signal_too_short_for_a_period_is_unanalysable_not_keyless(tmp_path):
    """Half a second holds no beat inside the window; the terminal is the
    analyser's, not a claim that the track has no key."""
    path = _write(tmp_path / "stinger.wav", _chord(A_MINOR, seconds=0.5))
    found = detect.analyse_file(path)
    assert found == {"path": path, "terminal": detect.TERMINAL_UNANALYSABLE}
