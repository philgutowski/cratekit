"""U241: the three ways the key's chroma is taken, on audio whose key is known.

The whole track without the harmonic separation is the shipped method since
U276, and ``tests/test_analysis_key_default.py`` holds that. The whole track
after the separation, and windows spread over it, are the other two. What is
asserted here is what a fixture can honestly say: that the windowed key hears
a key change wherever it falls, that a track shorter than its windows is the
whole track method bit for bit, and that the drift is still read over all of
the track. Whether either cheaper method AGREES WITH REKORDBOX on a real
library within the card's one percentage point is not a fixture's to say: it
was read at an attended sitting with ``scripts/head_agreement.py --key`` (A121).

Skipped where the analysis extra is absent, because the chroma is librosa's.
"""

from __future__ import annotations

import warnings

import pytest

from cratekit.analysis import detect
from cratekit.core import config, drift

np = pytest.importorskip("numpy")
librosa = pytest.importorskip("librosa")
soundfile = pytest.importorskip("soundfile")

RATE = detect.MEASURE_RATE
CUT = config.DEFAULT_DRIFT_CUT

#: C major and F sharp major, as far apart as two keys get, so a profile that
#: leans the wrong way is a different answer and not a near miss.
C_MAJOR, F_SHARP_MAJOR = "8B", "2B"


def _in_key(tonic: int, seconds: float) -> np.ndarray:
    """A major key's I, IV, V, I in sustained triads with a bass, two seconds a chord."""
    scale = [0, 2, 4, 5, 7, 9, 11]
    out = np.zeros(int(seconds * RATE), dtype=np.float32)
    chord = int(2.0 * RATE)
    t = np.arange(chord) / RATE
    fade = np.minimum(1.0, np.minimum(t, t[::-1]) / 0.05).astype(np.float32)
    for index, start in enumerate(range(0, out.size, chord)):
        degree = (0, 3, 4, 0)[index % 4]
        notes = [tonic + scale[(degree + step) % 7] + (12 if degree + step >= 7 else 0) for step in (0, 2, 4)]
        tone = sum(
            np.sin(2 * np.pi * 261.63 * 2 ** (note / 12.0) * t)
            + 0.4 * np.sin(2 * np.pi * 2 * 261.63 * 2 ** (note / 12.0) * t)
            for note in notes
        )
        tone = tone + 1.5 * np.sin(2 * np.pi * 65.41 * 2 ** (notes[0] / 12.0) * t)
        piece = (0.08 * tone * fade).astype(np.float32)
        stop = min(out.size, start + chord)
        out[start:stop] += piece[: stop - start]
    return out


def _two_keys(seconds: float, change_at: float) -> np.ndarray:
    """C major up to ``change_at`` of the way through, F sharp major after it."""
    first = _in_key(0, seconds * change_at)
    second = _in_key(6, seconds * (1.0 - change_at))
    return np.concatenate([first, second])


def _key(samples: np.ndarray, method: str) -> str | None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return detect.camelot_of(detect.key_profile(samples, RATE, method=method))


def test_the_fixture_is_heard_in_the_key_it_was_written_in():
    assert _key(_in_key(0, 40.0), detect.KEY_WHOLE) == C_MAJOR
    assert _key(_in_key(6, 40.0), detect.KEY_WHOLE) == F_SHARP_MAJOR


@pytest.mark.parametrize("method", [detect.KEY_WHOLE, detect.KEY_WINDOWS])
def test_a_key_that_changes_late_does_not_take_the_track(method):
    """The last quarter in another key: the track is still in the key it holds longest."""
    assert _key(_two_keys(260.0, 0.75), method) == C_MAJOR


@pytest.mark.parametrize("method", [detect.KEY_WHOLE, detect.KEY_WINDOWS])
def test_a_key_that_arrives_after_the_intro_is_the_tracks_key(method):
    """A quarter in one key, the rest in another: windows over the WHOLE track hear it.

    The opening thirty seconds alone are in the first key, which the last
    assertion shows, so a windowed method that read only the start of the
    track would name the wrong one. That is what the spread is for.
    """
    samples = _two_keys(260.0, 0.25)
    assert _key(samples, method) == F_SHARP_MAJOR
    assert _key(samples[: int(30.0 * RATE)], detect.KEY_WHOLE) == C_MAJOR


def test_the_windowed_profile_reads_three_minutes_of_a_long_track(monkeypatch):
    """Six windows of thirty seconds, whatever the track's length: that is the saving."""
    from cratekit.analysis import separation

    lengths: list[int] = []
    real = separation.harmonic

    def counting(samples, **kwargs):
        lengths.append(int(samples.shape[-1]))
        return real(samples, **kwargs)

    monkeypatch.setattr(separation, "harmonic", counting)
    _key(_in_key(0, 260.0), detect.KEY_WINDOWS)
    assert lengths == [int(30.0 * RATE)] * 6
    lengths.clear()
    _key(_in_key(0, 260.0), detect.KEY_WHOLE)
    assert lengths == [int(260.0 * RATE)]


@pytest.mark.parametrize("seconds", [3.0, 29.0, 170.0], ids=["stinger", "under-one-window", "under-six"])
def test_a_track_shorter_than_its_windows_is_the_whole_track_method_exactly(seconds):
    samples = _in_key(0, seconds)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        whole = detect.key_profile(samples, RATE, method=detect.KEY_WHOLE)
        windowed = detect.key_profile(samples, RATE, method=detect.KEY_WINDOWS)
    assert np.array_equal(whole, windowed)


def test_the_plain_method_skips_the_separation_and_still_hears_a_clean_key(monkeypatch):
    from cratekit.analysis import separation

    def never(*args, **kwargs):
        raise AssertionError("the plain method ran the harmonic separation")

    monkeypatch.setattr(separation, "harmonic", never)
    assert _key(_in_key(0, 40.0), detect.KEY_PLAIN) == C_MAJOR


def test_the_whole_method_separates_with_the_margin_it_always_did(monkeypatch):
    from cratekit.analysis import separation

    asked: list[object] = []
    real = separation.harmonic

    def recording(samples, **kwargs):
        asked.append(kwargs.get("margin"))
        return real(samples, **kwargs)

    monkeypatch.setattr(separation, "harmonic", recording)
    _key(_in_key(0, 20.0), detect.KEY_WHOLE)
    assert asked == [4]


def test_the_timings_of_a_whole_file_name_every_stage(tmp_path):
    path = tmp_path / "timed.flac"
    click = np.zeros(int(40.0 * RATE), dtype=np.float32)
    for beat in range(int(40.0 * 2)):
        at = int(beat * 0.5 * RATE)
        click[at : at + 200] += np.hanning(200).astype(np.float32)
    soundfile.write(str(path), 0.5 * click + _in_key(0, 40.0), RATE)
    timings: dict[str, float] = {}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        found = detect.analyse_file(path, key=detect.KEY_WHOLE, timings=timings)
        again = detect.analyse_file(path, key=detect.KEY_WHOLE)
        windowed = detect.analyse_file(path, key=detect.KEY_WINDOWS)
    assert found is not None and found.get("terminal") is None, found
    assert set(timings) == set(detect.STAGES) == set(detect.stages_of(detect.KEY_WHOLE))
    assert all(seconds >= 0.0 for seconds in timings.values())
    assert found == again, "timing a run changed what it measured"
    assert windowed == found, "a forty second file is shorter than its windows"


def test_a_tempo_that_moves_only_in_its_last_third_is_still_variable(tmp_path):
    """The drift is read over the whole track, so a late move is found (U241 keeps it so)."""
    seconds = 180.0

    def tempo_at(at: float) -> float:
        late = max(0.0, at - 2.0 * seconds / 3.0) / (seconds / 3.0)
        return 124.0 * (1.0 + 0.10 * late)

    samples = np.zeros(int(RATE * seconds), dtype=np.float32)
    burst = np.hanning(200).astype(np.float32)
    rng = np.random.default_rng(0)
    for every, level in ((1.0, 1.0), (0.5, 0.3)):
        at = 0.0
        while True:
            start = int(round(at * RATE))
            if start + burst.size > samples.size:
                break
            samples[start : start + burst.size] += level * burst
            at += every * 60.0 / tempo_at(at)
    samples += 0.02 * rng.standard_normal(samples.size).astype(np.float32)

    first_two_thirds = samples[: int(RATE * 2.0 * seconds / 3.0)]
    _tempo, steady = detect.measure_tempo_and_drift(first_two_thirds, RATE, floor=80, ceiling=160)
    assert drift.verdict(steady, CUT) == drift.STEADY, "the fixture moves before its last third"

    _tempo, moved = detect.measure_tempo_and_drift(samples, RATE, floor=80, ceiling=160)
    assert moved is not None and drift.verdict(moved, CUT) == drift.VARIABLE, moved

    path = tmp_path / "late mover.flac"
    soundfile.write(str(path), samples + _in_key(0, seconds), RATE)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for method in detect.KEY_METHODS:
            found = detect.analyse_file(path, key=method)
            assert found["drift_verdict"] == drift.VARIABLE, (method, found)
