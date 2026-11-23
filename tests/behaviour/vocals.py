"""The vocals scenarios: `crate analyze vocals` re-scoring a folder's vocal tags (U306).

On a full profile machine with the vocals suite's fake model and decoder, a
folder is queued and scored, rescored unchanged, ``--unscored`` and
``--recursive`` run, and the size cap, a vanished file, a foreign job, an
unloadable model and empty and absent folders each answer as themselves. Self
contained, so the suites beside it can be trimmed without moving it.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from cratekit.analysis import light, vocals
from cratekit.core import config, tags
from cratekit.core.exit_codes import ExitCode
from tests._containers import synth_container
from tests.test_config import valid_data

OK = int(ExitCode.OK)
VERB = ("analyze", "vocals")


class FakeModel:
    """A deterministic stand in for the vocal model: values track the input's mean."""

    labels = ("Singing", "Male singing", "Female singing")

    def inference(self, wav):
        import numpy as np

        batch = np.asarray(wav, dtype=np.float32)
        if batch.ndim == 1:
            batch = batch[None, :]
        frames = max(1, int(batch.shape[-1]) // 3200)
        level = float(np.mean(np.abs(batch)))
        row = np.zeros((frames, 527), dtype=np.float32)
        row[:, 0] = min(1.0, level)
        row[:, 1] = min(1.0, level * 0.4)
        row[:, 2] = min(1.0, level * 0.1)
        return row[None, :, :]


@pytest.fixture
def machine(tmp_path, monkeypatch) -> config.Config:
    """A configured machine on the full profile, which carries the vocals verb."""
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    built = config.from_dict(valid_data(library, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def silence(tmp_path) -> Path:
    made = tmp_path / "silence"
    made.mkdir()
    return synth_container(made, ".flac")


@pytest.fixture(autouse=True)
def unbound(monkeypatch):
    """Nothing bound, and a model that cannot load here, whatever this machine holds."""
    monkeypatch.setattr(light, "_DETECT", None)
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", None)
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    monkeypatch.setattr(vocals, "_DECODER", None)
    monkeypatch.setattr(
        vocals, "missing_requirement", lambda: "the 'vocals' extra is not installed here"
    )


def place(folder: Path, silence: Path, relative: str, **fields) -> Path:
    path = folder / f"{relative}.flac"
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(silence, path)
    if fields:
        assert tags.write_tags(path, fields), f"the fixture could not tag {relative}"
    return path


def bind_scoring(monkeypatch) -> None:
    import numpy as np

    monkeypatch.setattr(vocals, "_VOCAL_LOADER", FakeModel)
    monkeypatch.setattr(vocals, "_DECODER", lambda path: np.full(16000, 0.2, dtype=np.float32))


def queue_and_drive(stage, *argv: str):
    queued = stage.json(*VERB, *argv)
    assert queued.code == OK, queued.stdout
    folder = next(one for one in argv if not one.startswith("--"))
    return stage.json(*VERB, folder, "--job", queued.envelope["data"]["job_id"])


def test_a_folder_scored_and_then_unchanged(stage, machine, silence, tmp_path, monkeypatch):
    folder = tmp_path / "downloads"
    headed = place(folder, silence, "08A - 124 - done")
    place(folder, silence, "fresh")
    bind_scoring(monkeypatch)

    queued = stage.crate(*VERB, str(folder))
    assert queued.code == OK, queued.stderr
    job_id = queued.stdout.split("job: ", 1)[1].split(",", 1)[0].strip()
    scored = stage.crate(*VERB, str(folder), "--job", job_id)
    assert scored.code == OK, scored.stderr
    assert headed.name == "08A - 124 - done.flac"
    assert tags.read_vox_from_file(headed)
    # Again: every score is where the model puts it, and nothing is written.
    assert queue_and_drive(stage, str(folder)).code == OK
    assert stage.json(*VERB, "--unscored", str(folder)).code == OK

    empty = tmp_path / "empty"
    empty.mkdir()
    assert stage.json(*VERB, str(empty)).code == OK
    assert stage.crate(*VERB, str(tmp_path / "absent")).code == OK


def test_a_tree_an_oversize_file_and_the_refusals(stage, machine, silence, tmp_path, monkeypatch):
    folder = tmp_path / "downloads"
    place(folder, silence, "07B - 122 - finalized")
    place(folder, silence, "09A - 125 - scored", voxlevel=40)
    place(folder, silence, "deeper/08A - 124 - nested")
    place(folder, silence, "unheaded")

    # A process that cannot load the model refuses before anything is queued.
    assert stage.json(*VERB, str(folder)).code != OK
    bind_scoring(monkeypatch)

    unscored = queue_and_drive(stage, "--unscored", "--recursive", str(folder))
    assert unscored.code == OK, unscored.stdout
    assert tags.read_vox_from_file(folder / "deeper" / "08A - 124 - nested.flac")
    assert tags.read_vox_from_file(folder / "unheaded.flac") is None

    live = tmp_path / "live"
    kept = place(live, silence, "a live set", voxlevel=7, voxgender="F")
    monkeypatch.setattr(vocals, "VOCAL_MAX_BYTES", 1)
    assert queue_and_drive(stage, str(live)).code == OK
    assert tags.read_vox_from_file(kept) == 7

    gone = tmp_path / "gone"
    place(gone, silence, "vanishing")
    queued = stage.json(*VERB, str(gone))
    assert queued.code == OK, queued.stdout
    (gone / "vanishing.flac").unlink()
    failed = stage.json(*VERB, str(gone), "--job", queued.envelope["data"]["job_id"])
    assert failed.code != OK, failed.stdout

    other = stage.json("analyze", "run", "--queue-only", str(live))
    assert other.code == OK, other.stdout
    foreign = stage.json(*VERB, str(live), "--job", other.envelope["data"]["job_id"])
    assert foreign.code != OK, foreign.stdout
