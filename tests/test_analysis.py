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
    """Deterministic stand-in: frame count tracks input length, values track mean.

    Carries a label table naming the three targets at the columns it fills,
    because the scorer resolves columns by name and scores nothing by number
    (R-370).
    """

    labels = ("Singing", "Male singing", "Female singing")

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


# R-370: the shipped loader built the clip level wrapper against a checkpoint
# this machine does not hold, and the scorer read Speech, not Singing.


class _LabelledModel(_FakeModel):
    """A fake whose targets sit at columns 3, 4 and 5, behind three speech columns.

    The speech columns are left at zero and the singing columns carry a
    level, so a read by number scores nothing and a read by name scores a
    sung, male lead. The two reads cannot agree.
    """

    labels = (
        "Speech",
        "Male speech, man speaking",
        "Female speech, woman speaking",
        "Singing",
        "Male singing",
        "Female singing",
    )

    def inference(self, wav):
        batch = np.asarray(wav, dtype=np.float32)
        if batch.ndim == 1:
            batch = batch[None, :]
        frames = max(1, int(batch.shape[-1]) // 3200)
        row = np.zeros((frames, 527), dtype=np.float32)
        row[:, 0] = 0.0
        row[:, 1] = 0.0
        row[:, 2] = 0.0
        row[:, 3] = 0.9
        row[:, 4] = 0.8
        row[:, 5] = 0.1
        return row[None, :, :]


def _fake_panns(monkeypatch, *, built: list | None = None):
    """A stand in for the extra: records the frame wrapper, refuses the clip one.

    torch is stubbed too, so the readiness check neither needs nor loads the
    real one.
    """
    import sys
    import types

    monkeypatch.setitem(sys.modules, "torch", types.ModuleType("torch"))
    module = types.ModuleType("panns_inference")

    class SoundEventDetection:
        def __init__(self, **kwargs):
            print("Checkpoint path: elsewhere")
            if built is not None:
                built.append(kwargs)

        labels = _LabelledModel.labels

    class AudioTagging:
        def __init__(self, **kwargs):
            raise AssertionError("the clip level wrapper has no frame output")

    module.SoundEventDetection = SoundEventDetection
    module.AudioTagging = AudioTagging
    monkeypatch.setitem(__import__("sys").modules, "panns_inference", module)
    return module


def test_class_indices_resolve_the_singing_columns_by_name():
    from cratekit.analysis import vocal

    assert vocal.class_indices(_LabelledModel()) == (3, 4, 5)
    assert vocal.class_indices(_FakeModel()) == (0, 1, 2)

    class _Wrong:
        labels = ("Speech", "Singing")

    with pytest.raises(ValueError, match="does not name"):
        vocal.class_indices(_Wrong())

    class _Unlabelled:
        def inference(self, wav):
            return np.zeros((1, 1, 527), dtype=np.float32)

    with pytest.raises(ValueError, match="no label table"):
        vocal.class_indices(_Unlabelled())
    with pytest.raises(ValueError, match="no label table"):
        vocal.infer_frames(_Unlabelled(), np.zeros(3200, dtype=np.float32))


def test_analyse_scores_the_singing_columns_not_the_first_three(monkeypatch):
    """A sung lead on a labelled model scores as vocal, and male, not silent."""
    from cratekit.analysis import vocals

    monkeypatch.setattr(vocals, "_VOCAL_LOADER", _LabelledModel)
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    monkeypatch.setattr(vocals, "_DECODER", lambda path: np.full(32000, 0.2, np.float32))

    scored = vocals.analyse({"path": "lead.flac"})
    assert scored["vocal_active"] is True
    assert scored["voxlevel"] == 100
    assert scored["voxgender"] == "M"


def test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track(monkeypatch):
    """The fault is knowable once beside the model, before any file is decoded."""
    from cratekit.analysis import vocals

    class _Wrong(_FakeModel):
        labels = ("Speech",)

    decoded: list[str] = []

    def decoder(path):
        decoded.append(str(path))
        return np.full(32000, 0.2, np.float32)

    monkeypatch.setattr(vocals, "_VOCAL_LOADER", _Wrong)
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    monkeypatch.setattr(vocals, "_VOCAL_FAILURE", None)
    monkeypatch.setattr(vocals, "_VOCAL_COLUMNS", None)
    monkeypatch.setattr(vocals, "_DECODER", decoder)

    scored = vocals.analyse({"path": "lead.flac"})
    assert scored["vocal_active"] is False
    assert scored["vocal_reason"] == vocals.REASON_MODEL_UNAVAILABLE
    assert decoded == [], "nothing is decoded for a model that cannot be read"
    assert "does not name" in (vocals._VOCAL_FAILURE or "")
    warning = vocals.unscored_warning({"by_vocal_reason": {vocals.REASON_MODEL_UNAVAILABLE: 3}}, verb="scored")
    assert warning is not None and "cratekit[vocals]" in warning["message"]


def test_default_loader_builds_the_frame_wrapper_from_the_checkpoint_on_disk(
    monkeypatch, tmp_path, capsys
):
    from cratekit.analysis import vocal, vocals

    checkpoint = tmp_path / "Cnn14_DecisionLevelMax.pth"
    checkpoint.write_bytes(b"x" * 16)
    labels = tmp_path / "class_labels_indices.csv"
    labels.write_text("index,mid,display_name\n", encoding="utf-8")
    monkeypatch.setattr(vocals, "CHECKPOINT", checkpoint)
    monkeypatch.setattr(vocals, "LABELS", labels)
    monkeypatch.setattr(vocals, "CHECKPOINT_MIN_BYTES", 16)
    built: list[dict] = []
    _fake_panns(monkeypatch, built=built)

    assert vocals.missing_requirement() is None
    model = vocal.default_loader()
    assert built == [{"checkpoint_path": str(checkpoint), "device": "cpu"}]
    assert vocal.class_indices(model) == (3, 4, 5)
    assert capsys.readouterr().out == "", "the wrapper's chatter must not reach stdout"


def test_default_loader_refuses_before_the_extra_is_asked_for_a_missing_checkpoint(
    monkeypatch, tmp_path
):
    from cratekit.analysis import vocal, vocals

    labels = tmp_path / "class_labels_indices.csv"
    monkeypatch.setattr(vocals, "LABELS", labels)
    monkeypatch.setattr(vocals, "CHECKPOINT", tmp_path / "absent.pth")
    built: list[dict] = []
    _fake_panns(monkeypatch, built=built)

    assert "class_labels_indices.csv" in (vocals.missing_requirement() or "")
    with pytest.raises(FileNotFoundError, match="class_labels_indices.csv"):
        vocal.default_loader()
    assert built == [], "a missing label table must never reach the library's fetch"

    labels.write_text("index,mid,display_name\n", encoding="utf-8")
    assert "absent.pth" in (vocals.missing_requirement() or "")
    with pytest.raises(FileNotFoundError, match="absent.pth"):
        vocal.default_loader()
    assert built == [], "a missing checkpoint must never reach the library's fetch"

    truncated = tmp_path / "short.pth"
    truncated.write_bytes(b"x" * 8)
    monkeypatch.setattr(vocals, "CHECKPOINT", truncated)
    assert "smaller" in (vocals.missing_requirement() or "")
    with pytest.raises(FileNotFoundError, match="smaller"):
        vocal.default_loader()
    assert built == []


def test_a_torch_that_will_not_load_is_the_first_missing_requirement(monkeypatch):
    import sys
    import types

    from cratekit.analysis import vocals

    class _Broken(types.ModuleType):
        def __getattr__(self, name):
            raise AttributeError(name)

    def explode(name, *args, **kwargs):
        if name == "torch":
            raise OSError("dlopen failed: libtorch_cpu")
        return real_import(name, *args, **kwargs)

    real_import = __builtins__["__import__"] if isinstance(__builtins__, dict) else __builtins__.__import__
    monkeypatch.delitem(sys.modules, "torch", raising=False)
    monkeypatch.setattr("builtins.__import__", explode)
    missing = vocals.missing_requirement()
    assert missing is not None and "dlopen failed" in missing and "cratekit[vocals]" in missing


# R-371: a tail chunk shorter than the network can pool failed the whole track.


class _NeedsWidth(_FakeModel):
    """Refuses a piece shorter than the network's minimum, the way CNN14 does."""

    def __init__(self, minimum: int) -> None:
        self.minimum = minimum
        self.widths: list[int] = []

    def inference(self, wav):
        width = int(np.asarray(wav).shape[-1])
        self.widths.append(width)
        if width < self.minimum:
            raise RuntimeError("Output size is too small")
        return super().inference(wav)


def test_a_short_tail_is_folded_into_the_chunk_before_it():
    from cratekit.analysis import vocal

    wav = np.full(3200 * 2 + 100, 0.2, dtype=np.float32)
    model = _NeedsWidth(minimum=1000)
    vocals, _, _ = vocal.infer_frames(model, wav, chunk_samples=3200)
    assert model.widths == [3200, 3300]
    assert vocals.size == 2


def test_a_lone_short_clip_is_padded_to_the_floor(monkeypatch):
    from cratekit.analysis import vocal

    monkeypatch.setattr(vocal, "MIN_CHUNK_SAMPLES", 1000)
    wav = np.full(100, 0.2, dtype=np.float32)
    model = _NeedsWidth(minimum=1000)
    vocal.infer_frames(model, wav, chunk_samples=3200)
    assert model.widths == [1000]


def test_the_unchunked_path_pads_a_short_signal_too():
    """The floor is the network's, so it applies whether or not the caller chunks."""
    from cratekit.analysis import vocal

    wav = np.full(8000, 0.2, dtype=np.float32)
    model = _NeedsWidth(minimum=vocal.MIN_CHUNK_SAMPLES)
    vocal.infer_frames(model, wav, chunk_samples=None)
    assert model.widths == [vocal.MIN_CHUNK_SAMPLES]


def test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length():
    """Half a second of singing padded to a second is still all singing."""
    from cratekit.analysis import vocal

    wav = np.full(16000, 0.2, dtype=np.float32)
    model = _NeedsWidth(minimum=vocal.MIN_CHUNK_SAMPLES)
    vocals, _, _ = vocal.infer_frames(model, wav)
    assert model.widths == [vocal.MIN_CHUNK_SAMPLES]
    assert vocals.size == 16000 // 3200, "the frames the padding added are gone"
    assert vocal.reduce_frames(*vocal.infer_frames(model, wav)).presence == 100.0


def test_at_the_real_chunk_size_only_a_tail_under_the_floor_is_folded():
    """The floor, not the chunk size, decides a fold: a three second tail stands alone."""
    from cratekit.analysis import vocal

    chunk = vocal.DEFAULT_CHUNK_SAMPLES
    model = _NeedsWidth(minimum=vocal.MIN_CHUNK_SAMPLES)
    long_tail = np.full(chunk + 96000, 0.2, dtype=np.float32)
    vocal.infer_frames(model, long_tail)
    assert model.widths == [chunk, 96000]

    model = _NeedsWidth(minimum=vocal.MIN_CHUNK_SAMPLES)
    short_tail = np.full(chunk + 8000, 0.2, dtype=np.float32)
    vocal.infer_frames(model, short_tail)
    assert model.widths == [chunk + 8000]


def test_an_exact_multiple_still_walks_in_equal_pieces():
    from cratekit.analysis import vocal

    wav = np.full(3200 * 3, 0.2, dtype=np.float32)
    model = _NeedsWidth(minimum=1000)
    vocal.infer_frames(model, wav, chunk_samples=3200)
    assert model.widths == [3200, 3200, 3200]
