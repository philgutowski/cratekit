"""U25: analysis two-pass, extras stub, vocal degrade, chunked scores, resume."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path

import numpy as np
import pytest

from cratekit import cli
from cratekit.cli import registry
from cratekit.core import profiles
from cratekit.core.exit_codes import ExitCode


def _touch_audio(folder: Path, name: str) -> Path:
    path = folder / name
    path.write_bytes(b"not-audio")
    return path


class _FakeModel:
    """Deterministic stand-in: frame count tracks input length, values track mean."""

    def inference(self, wav):
        batch = np.asarray(wav, dtype=np.float32)
        if batch.ndim == 1:
            batch = batch[None, :]
        samples = int(batch.shape[-1])
        frames = max(1, samples // 3200)
        level = float(np.mean(np.abs(batch)))
        row = np.zeros((frames, 527), dtype=np.float32)
        row[:, 0] = min(1.0, level)
        row[:, 1] = min(1.0, level * 0.4)
        row[:, 2] = min(1.0, level * 0.1)
        return row[None, :, :]


def test_a_missing_analysis_extra_names_the_install_command():
    """R5: a verb behind the extra tells the user the exact pip line."""

    def importer(name: str):
        raise ImportError("librosa is not installed", name="librosa")

    entry = registry.entry("analyze.run")
    parser = cli.build_parser(
        [entry], membership=profiles.resolve("full"), importer=importer
    )
    help_text = io.StringIO()
    with contextlib.redirect_stdout(help_text), pytest.raises(SystemExit):
        parser.parse_args(["analyze", "--help"])
    listed = " ".join(help_text.getvalue().split())
    assert "requires the 'analysis' extra" in listed

    args = parser.parse_args(["analyze", "run"])
    assert args._stub is not None
    cause = cli._stub_cause(args._entry, args._stub)
    assert cause.code is ExitCode.MODULE_UNAVAILABLE
    assert cause.detail["install"] == "pip install 'cratekit[analysis]'"


def test_vocal_model_load_failure_leaves_key_and_energy_intact(tmp_path):
    from cratekit.analysis.run import run_batch

    path = _touch_audio(tmp_path, "track.flac")

    def detect(item: Path):
        return {"path": item, "camelot": "8A", "bpm": 124, "energy": 6}

    def explode():
        raise RuntimeError("panns checkpoint missing")

    results = run_batch([path], detect=detect, vocal_loader=explode)
    assert len(results) == 1
    result = results[0]
    assert result.camelot == "8A"
    assert result.bpm == 124
    assert result.energy == 6
    assert result.vocal_active is False
    assert result.voxlevel is None
    assert result.status != "error"


def test_chunked_inference_matches_unchunked_on_a_fixture():
    from cratekit.analysis.vocal import infer_frames, reduce_frames

    wav = np.full(16000, 0.2, dtype=np.float32)
    model = _FakeModel()
    whole = infer_frames(model, wav, chunk_samples=None)
    parts = infer_frames(model, wav, chunk_samples=3200)
    assert reduce_frames(*whole) == reduce_frames(*parts)


def test_chunked_inference_walks_the_signal_in_pieces():
    from cratekit.analysis.vocal import infer_frames

    class _Counting(_FakeModel):
        def __init__(self) -> None:
            self.widths: list[int] = []

        def inference(self, wav):
            self.widths.append(int(np.asarray(wav).shape[-1]))
            return super().inference(wav)

    wav = np.full(16000, 0.2, dtype=np.float32)
    model = _Counting()
    infer_frames(model, wav, chunk_samples=3200)
    assert model.widths == [3200, 3200, 3200, 3200, 3200]


def test_a_killed_batch_resumes_skipping_completed_tracks(tmp_path):
    from cratekit.analysis.run import run_batch

    first = _touch_audio(tmp_path, "8A - 124 - Done.flac")
    second = _touch_audio(tmp_path, "fresh.flac")
    seen: list[str] = []

    def detect(item: Path):
        seen.append(item.name)
        return {"path": item, "camelot": "4A", "bpm": 120, "energy": 3}

    results = run_batch([first, second], detect=detect, vocal=False)
    assert first.name not in seen
    names = {item.path.name: item for item in results}
    assert names[first.name].status == "skipped-prefixed"
    assert names[second.name].camelot == "4A"
    assert names[second.name].status != "skipped-prefixed"
