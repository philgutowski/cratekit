"""U171: why most of a landed batch stamps a vocal level of exactly 0.

The stamp is the share of frames whose Singing score reaches the floor (A64); a
fake model replays A64's series through the real walk, reduction and rounding.
"""

from __future__ import annotations

import numpy as np
import pytest

from cratekit.analysis import vocal, vocals
from cratekit.write.metadata_cli import VALUE_VOX, vocal_tag_values

#: The library's with vox cut, set by hand on 2026-10-27 after sitting 47.
LIBRARY_CUT = 3.0
#: The model's frame rate, measured by A64 at 100.1 frames a second on all 126
#: rows. The fake emits one frame per 320 samples at 32 kilohertz to match it.
SAMPLES_PER_FRAME = vocal.MODEL_SAMPLE_RATE // 100


class _Playback:
    """A frame model replaying a Singing series however chunked, leaning female where sung."""

    labels = ("Singing", "Male singing", "Female singing")

    def __init__(self, singing: np.ndarray) -> None:
        self.singing = np.asarray(singing, dtype=np.float32)
        self.cursor = 0

    def inference(self, wav):
        width = int(np.asarray(wav).shape[-1])
        frames = max(1, width // SAMPLES_PER_FRAME)
        piece = self.singing[self.cursor : self.cursor + frames]
        self.cursor += frames
        if piece.size < frames:
            piece = np.concatenate([piece, np.zeros(frames - piece.size, np.float32)])
        row = np.zeros((frames, 527), dtype=np.float32)
        row[:, 0] = piece
        row[:, 1] = piece * 0.05
        row[:, 2] = piece * 0.4
        return row[None, :, :]


def _series(frames: int, *, heard: float, at: float, floor_noise: float) -> np.ndarray:
    """A Singing series with ``heard`` frames at ``at``, spread evenly so no chunk hides them."""
    series = np.full(frames, floor_noise, dtype=np.float32)
    count = int(round(frames * heard))
    if count:
        index = np.linspace(0, frames - 1, count).round().astype(int)
        series[index] = at
    return series


def _bind(monkeypatch, loader, samples: np.ndarray) -> None:
    """A fresh model slot loading through ``loader``, every file decoding to ``samples``."""
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", loader)
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    monkeypatch.setattr(vocals, "_VOCAL_FAILURE", None)
    monkeypatch.setattr(vocals, "_VOCAL_COLUMNS", None)
    monkeypatch.setattr(vocals, "_DECODER", lambda path: samples)


def _score(monkeypatch, singing: np.ndarray, *, signal: np.ndarray | None = None) -> dict:
    """Score one track through ``analyse`` with the playback model bound."""
    frames = int(singing.size)
    samples = signal if signal is not None else np.full(frames * SAMPLES_PER_FRAME, 0.1, np.float32)
    model = _Playback(singing)
    _bind(monkeypatch, lambda: model, samples)
    return vocals.analyse({"path": "track.flac"})


#: Five minutes of frames, about the length of the sitting's median track, so
#: the walk cuts the series into some forty chunks of eight seconds.
FRAMES = 30_000


def test_a_sung_lead_shaped_like_a64s_known_vocals_scores_above_the_cut(monkeypatch):
    """Angie Stone's row: 59.82 percent of frames at the floor, p95 0.1518."""
    scored = _score(monkeypatch, _series(FRAMES, heard=0.5982, at=0.15, floor_noise=0.01))
    assert scored["vocal_active"] is True
    assert scored["voxlevel"] == 60
    assert scored["voxlevel"] >= LIBRARY_CUT
    assert VALUE_VOX in vocal_tag_values(scored["voxlevel"], scored["voxgender"], LIBRARY_CUT)
    assert scored["voxgender"] == "F"


class _Listening(_Playback):
    """A frame model whose Singing follows the level it is handed, for silence."""

    def __init__(self) -> None:
        super().__init__(np.zeros(0, np.float32))

    def inference(self, wav):
        batch = np.asarray(wav, dtype=np.float32)
        frames = max(1, int(batch.shape[-1]) // SAMPLES_PER_FRAME)
        level = min(1.0, float(np.mean(np.abs(batch))))
        row = np.zeros((frames, 527), dtype=np.float32)
        row[:, 0] = level
        row[:, 2] = level * 0.4
        return row[None, :, :]


def test_silence_is_heard_and_scores_zero_rather_than_no_score(monkeypatch):
    """A silent file was listened to, so 0, never None; a loud signal scores 100."""
    _bind(monkeypatch, _Listening, np.zeros(FRAMES * SAMPLES_PER_FRAME, np.float32))
    scored = vocals.analyse({"path": "silence.flac"})
    assert scored["vocal_active"] is True
    assert scored["vocal_reason"] is None
    assert scored["voxlevel"] == 0
    assert scored["voxgender"] == "U"
    assert vocal_tag_values(scored["voxlevel"], scored["voxgender"], LIBRARY_CUT) == []

    monkeypatch.setattr(vocals, "_DECODER", lambda path: np.full(FRAMES * SAMPLES_PER_FRAME, 0.2, np.float32))
    assert vocals.analyse({"path": "loud.flac"})["voxlevel"] == 100


def test_a_lead_the_model_never_hears_at_the_floor_scores_zero(monkeypatch):
    """I Feel Love's row, loudest frame 0.034: the model's miss, pinned so a rescue is measured."""
    singing = _series(FRAMES, heard=0.0099, at=0.034, floor_noise=0.003)
    assert float(singing.max()) < vocal.DEFAULT_FRAME_FLOOR
    scored = _score(monkeypatch, singing)
    assert scored["vocal_active"] is True
    assert scored["voxlevel"] == 0


@pytest.mark.parametrize(
    ("share", "stamped"),
    [
        (0.0008, 0),  # the fewest frames at the floor among A64's 12 traces
        (0.0049, 0),  # the most, still under half a percent
        (0.0060, 1),  # just over half a percent stamps 1
        (0.0140, 1),
    ],
)
def test_a_trace_under_half_a_percent_of_frames_rounds_to_zero(monkeypatch, share, stamped):
    """The 12 of 80 zeros that heard singing briefly, and the line they sit under."""
    scored = _score(monkeypatch, _series(FRAMES, heard=share, at=0.08, floor_noise=0.004))
    assert scored["vocal_active"] is True
    assert scored["voxlevel"] == stamped


def test_the_stamp_is_the_share_of_frames_at_the_floor_rounded():
    """The reduction A64 reproduced on all 126 rows, stated as arithmetic."""
    for share in (0.0, 0.002, 0.0049, 0.0051, 0.0350, 0.5982):
        singing = _series(10_000, heard=share, at=0.2, floor_noise=0.0)
        score = vocal.reduce_frames(singing, singing * 0.05, singing * 0.4)
        assert score.presence == pytest.approx(100.0 * share, abs=0.011)


def test_the_floor_is_reached_at_exactly_its_value_and_not_just_under():
    """A frame at exactly the floor counts, and one just under it does not."""
    at = np.full(100, vocal.DEFAULT_FRAME_FLOOR, dtype=np.float64)
    under = np.full(100, 0.0499, dtype=np.float64)
    assert vocal.presence_score(at) == 100.0
    assert vocal.presence_score(under) == 0.0
