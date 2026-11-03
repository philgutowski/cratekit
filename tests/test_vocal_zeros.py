"""U171: why most of a landed batch stamps a vocal level of exactly 0.

A64 measured what the frame model heard on the 116 files of sitting 47 and on
ten known sung leads, and found the stamp to be exactly the share of frames
whose Singing score reaches the floor, rounded to a whole percent. Of the 80
zeros, 68 never reach the floor on a single frame and 12 reach it on under half
a percent of their frames. No decode, chunking or column defect was involved.

These tests drive ``vocals.analyse`` end to end with a fake model that plays
back a Singing series shaped on those measurements, so each shape is scored
through the same chunk walk, reduction and rounding a real track takes. The
decode is bound to a constant signal, so ``vocal.decode`` is not exercised
here; a real file's decode is A64's to measure.
The shapes are synthetic: the frame values A64 printed are summaries (max,
95th percentile, share at the floor), and each series below is built to match
the summary of the row it names, not copied from a file.
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
    """A frame model that replays a Singing series across however it is chunked.

    Each call to ``inference`` returns the next frames of ``singing`` for the
    width it is handed, so the chunked walk reassembles the whole series, and a
    silent piece of signal is always answered from the series rather than from
    its own level. Gender columns carry a fixed female lean wherever singing
    is heard, which only the gender call reads.
    """

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
    """A Singing series with ``heard`` of its frames at ``at`` and the rest low.

    The heard frames are spread evenly through the track, so every chunk the
    walk cuts carries its share and a chunk boundary cannot hide them.
    """
    series = np.full(frames, floor_noise, dtype=np.float32)
    count = int(round(frames * heard))
    if count:
        index = np.linspace(0, frames - 1, count).round().astype(int)
        series[index] = at
    return series


def _score(monkeypatch, singing: np.ndarray, *, signal: np.ndarray | None = None) -> dict:
    """Score one track through ``analyse`` with the playback model bound."""
    frames = int(singing.size)
    samples = signal if signal is not None else np.full(frames * SAMPLES_PER_FRAME, 0.1, np.float32)
    model = _Playback(singing)
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", lambda: model)
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    monkeypatch.setattr(vocals, "_VOCAL_FAILURE", None)
    monkeypatch.setattr(vocals, "_VOCAL_COLUMNS", None)
    monkeypatch.setattr(vocals, "_DECODER", lambda path: samples)
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
    """A frame model whose Singing follows the level of what it is handed.

    Used for silence, where the answer has to come from the signal: a
    playback model would answer from its series whatever it was fed.
    """

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
    """A silent file is a track the model listened to, so 0, never None.

    The same model scores a loud signal 100, so the zero is the silence's.
    """
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", _Listening)
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    monkeypatch.setattr(vocals, "_VOCAL_FAILURE", None)
    monkeypatch.setattr(vocals, "_VOCAL_COLUMNS", None)
    monkeypatch.setattr(vocals, "_DECODER", lambda path: np.zeros(FRAMES * SAMPLES_PER_FRAME, np.float32))
    scored = vocals.analyse({"path": "silence.flac"})
    assert scored["vocal_active"] is True
    assert scored["vocal_reason"] is None
    assert scored["voxlevel"] == 0
    assert scored["voxgender"] == "U"
    assert vocal_tag_values(scored["voxlevel"], scored["voxgender"], LIBRARY_CUT) == []

    monkeypatch.setattr(vocals, "_DECODER", lambda path: np.full(FRAMES * SAMPLES_PER_FRAME, 0.2, np.float32))
    assert vocals.analyse({"path": "loud.flac"})["voxlevel"] == 100


def test_a_lead_the_model_never_hears_at_the_floor_scores_zero(monkeypatch):
    """I Feel Love's row: a sung lead whose loudest Singing frame is 0.034.

    This is the model's miss, not the pipeline's, and the zero is the honest
    stamp of what the model heard. It is pinned so that a change claiming to
    rescue such a lead is measured against it rather than assumed.
    """
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
