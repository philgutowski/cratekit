"""U241: where the windowed key reads, and how a profile becomes a key.

The windowed key is one of two cheaper ways to take the key's chroma, built
and NOT shipped as the default: its bar is agreement with rekordbox's own keys
on the library, read at an attended sitting. What is held here needs no
audio: the geometry of the windows, which is what makes "a key that changes
late is still heard" and "a stinger is read whole" true by construction, and
the profile to key step both methods share. The audio side is
``tests/test_analysis_key_methods.py``, skipped without the analysis extra.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.analysis import detect

np = pytest.importorskip("numpy")

RATE = detect.MEASURE_RATE


def test_the_shipped_windows_are_six_of_thirty_seconds():
    assert (detect.KEY_WINDOW_COUNT, detect.KEY_WINDOW_SECONDS) == (6, 30.0)
    assert detect.KEY_METHODS == ("whole", "windows", "plain")
    assert detect.KEY_WHOLE == "whole", "the whole track is the method every caller defaults to"


@pytest.mark.parametrize("seconds", [181, 265, 420, 600, 3600])
def test_a_long_track_is_read_in_one_window_from_the_middle_of_each_sixth(seconds):
    length = seconds * RATE
    ranges = detect.key_windows(length, RATE)
    assert ranges is not None and len(ranges) == 6
    width = int(30.0 * RATE)
    part = length / 6
    for index, (start, stop) in enumerate(ranges):
        assert stop - start == width
        assert 0 <= start and stop <= length, "a window runs off the track"
        centre = (start + stop) / 2
        assert centre == pytest.approx(part * (index + 0.5), abs=1.0)
        assert part * index <= start and stop <= part * (index + 1) + 1, (
            "a window leaves its own sixth, so two could overlap"
        )


def test_the_last_window_sits_in_the_last_sixth_so_a_late_key_change_is_heard():
    """The opening minutes alone would never hear a key that arrives at the end."""
    length = 420 * RATE
    start, stop = detect.key_windows(length, RATE)[-1]
    assert start >= length * 5 / 6
    assert (start + stop) / 2 == pytest.approx(length * 11 / 12, abs=1.0)


@pytest.mark.parametrize("seconds", [0.5, 2, 29, 30, 31, 120, 180])
def test_a_track_no_longer_than_its_windows_is_read_whole(seconds):
    """A stinger shorter than one window, and anything up to six of them: no windows at all."""
    assert detect.key_windows(int(seconds * RATE), RATE) is None


def test_one_sample_past_six_windows_is_the_first_length_read_in_windows():
    edge = 6 * int(30.0 * RATE)
    assert detect.key_windows(edge, RATE) is None
    assert detect.key_windows(edge + 1, RATE) is not None


@pytest.mark.parametrize("count,seconds", [(0, 30.0), (-1, 30.0), (6, 0.0)])
def test_no_windows_or_windows_of_no_length_read_the_whole_track(count, seconds):
    assert detect.key_windows(600 * RATE, RATE, count=count, seconds=seconds) is None


@pytest.mark.parametrize(
    "tonic,mode,camelot",
    [(0, "major", "8B"), (9, "minor", "8A"), (7, "major", "9B"), (4, "minor", "9A"),
     (6, "major", "2B"), (2, "minor", "7A")],
)
def test_a_profile_shaped_like_a_keys_template_is_named_that_key(tonic, mode, camelot):
    template = np.asarray(detect._MAJOR if mode == "major" else detect._MINOR)
    assert detect.camelot_of(np.roll(template, tonic)) == camelot


def test_a_profile_with_nothing_in_it_has_no_key():
    assert detect.camelot_of(np.zeros(12)) is None


def test_a_profile_that_is_not_a_number_has_no_key():
    """What a signal the transform could not read leaves: every correlation is not a number."""
    with np.errstate(invalid="ignore", divide="ignore"):
        assert detect.camelot_of(np.full(12, np.nan)) is None


def test_a_key_method_nobody_built_is_refused_before_the_file_is_opened(tmp_path):
    with pytest.raises(ValueError, match="the key method is one of"):
        detect.analyse_file(tmp_path / "never read.flac", key="first-minute")


def test_the_timer_adds_to_a_mapping_and_costs_a_caller_without_one_nothing():
    timings: dict[str, float] = {"decode": 1.0}
    with detect.timed(timings, "decode"):
        pass
    with detect.timed(timings, "energy"):
        pass
    assert timings["decode"] >= 1.0 and timings["energy"] >= 0.0
    with detect.timed(None, "decode"):
        pass
    assert set(timings) == {"decode", "energy"}
    assert detect.STAGES == ("decode", "tempo_drift", "harmonic", "chroma_key", "energy")


def test_the_timer_keeps_its_time_when_the_stage_raises():
    timings: dict[str, float] = {}
    with pytest.raises(RuntimeError):
        with detect.timed(timings, "harmonic"):
            raise RuntimeError("the separation raised")
    assert "harmonic" in timings


def test_the_scripts_stage_names_are_the_detectors_and_the_vocal_passs():
    """The instrument prints what the shipped functions time, under the same names."""
    import importlib.util

    path = Path(__file__).resolve().parent.parent / "scripts" / "analyze_stages.py"
    spec = importlib.util.spec_from_file_location("analyze_stages_for_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert tuple(key for key, _words in module.STAGE_WORDS) == (
        *detect.STAGES,
        "vocal_decode",
        "vocal_model",
    )
    assert len(module.SYNTHETIC_SET) >= 20, "the card asks for a set of at least twenty"
    lengths = [row[0] for row in module.SYNTHETIC_SET]
    assert min(lengths) < 30 and max(lengths) > 600, "the set is not of mixed length"
    assert module.stride(list(range(10)), 4) == [0, 3, 6, 9]
    assert module.stride(list(range(3)), 20) == [0, 1, 2]
    assert module.stride(list(range(9)), 1) == [0]
