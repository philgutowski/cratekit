"""U344: ``analyze run`` scores a file's energy with the very measure ``analyze restamp`` uses.

Over real decoding, where the analysis extra is installed: on a track longer than the slice, the
head's old reading (the whole track resampled, then sliced) differs from the restamp's (the slice
decoded alone), and the head now gives the restamp's level and features exactly, so a restamp of a
file the run just scored would write nothing.
"""

from __future__ import annotations

from pathlib import Path

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("librosa")
soundfile = pytest.importorskip("soundfile")
pytest.importorskip("scipy")

from cratekit.analysis import decode, detect, energy, light  # noqa: E402

RATE = 44100
SECONDS = 14.0
SLICE = 6.0
TEMPO = 124.0


@pytest.fixture(autouse=True)
def nothing_bound(monkeypatch):
    monkeypatch.setattr(energy, "_EXTRACTOR", None)
    monkeypatch.setattr(light, "_DETECT", None)
    # Shortened so a short fixture is longer than the slice, as a real track is.
    monkeypatch.setattr(energy, "SEGMENT_SECONDS", SLICE)


@pytest.fixture(scope="module")
def track(tmp_path_factory) -> Path:
    """An A minor chord over a kick at 124, stereo, longer than the slice."""
    count = int(SECONDS * RATE)
    time = np.arange(count) / RATE
    tone = sum(np.sin(2 * np.pi * f * time) for f in (220.0, 261.63, 329.63)) / 3
    kick = np.zeros(count)
    beat = int(RATE * 60.0 / TEMPO)
    decay = np.exp(-np.arange(2000) / 300.0) * np.sin(2 * np.pi * 60 * np.arange(2000) / RATE)
    for start in range(0, count - 2000, beat):
        kick[start : start + 2000] += decay
    rng = np.random.default_rng(344)
    mix = 0.4 * tone + 0.5 * kick + 0.01 * rng.standard_normal(count)
    mix = (0.9 * mix / np.max(np.abs(mix))).astype(np.float32)
    path = tmp_path_factory.mktemp("one-measure") / "track.flac"
    soundfile.write(str(path), np.stack([mix, np.roll(mix, 11)], axis=1), RATE, subtype="PCM_16")
    return path


def calibration() -> energy.Calibration:
    """A calibration whose cuts sit around the track, so a level is a real reading."""
    rng = np.random.default_rng(7)
    rows = [{name: float(rng.normal(1.0, 0.5)) for name in energy.FEATURE_ORDER} for _ in range(40)]
    return energy.calibrate(rows)


def test_the_head_scores_the_restamps_features_and_level_exactly(track):
    calibrated = calibration()
    head = detect.analyse_file(track, calibration=calibrated)
    assert head is not None and head.get("terminal") is None, head
    restamped = energy.features_from_path(track)
    assert restamped is not None
    assert head["energy_status"] == energy.STATUS_CALIBRATED
    assert head["energy"] == energy.level_for(restamped, calibrated)


def test_the_heads_old_reading_differed_from_the_restamps_on_this_track(track):
    """The teeth: on a track longer than the slice the two decodes are not one."""
    whole, rate = decode.load(track, energy.MEASURE_RATE)
    old = energy.features_from_samples(whole, int(rate))
    restamped = energy.features_from_path(track)
    assert old is not None and restamped is not None
    assert old != restamped
    measured: list[Path] = []
    real = energy.features_from_path

    def spying(path):
        measured.append(Path(path))
        return real(path)
    energy.bind_extractor(spying)
    try:
        detect.analyse_file(track, calibration=calibration())
    finally:
        energy.bind_extractor(None)
    assert measured == [track], "the head measures energy through the restamp's own call"
