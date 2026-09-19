"""U58: the analysis workers, the wav plumbing, and the energy that was never computed.

Three claims, each driven rather than read:

1. ``analyze.run`` and ``analyze.restamp`` execute their queued items, pending
   to done, through the real dispatcher and the real resume argv, with the
   files read back off disk afterwards.
2. The vocal pass scores a partial that carries nothing but a path. The first
   version waited on a ``wav`` key nothing set and reported every track as
   ``voxlevel=0``; the pin below fails if any line of the module reads that
   key again.
3. Energy is either a level from a calibration or an honest absence with a
   status, and the routing reader is driven on both.

EVERY WORKER CASE GOES THROUGH THE VERB rather than through the handler, so a
key still sitting in ``HANDLERS_NOT_YET_BOUND`` fails here rather than passing
against a worker called by hand. The seams are bound on the modules with
``monkeypatch`` so each test starts from an unbound process.
"""

from __future__ import annotations

import ast
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import pytest

from cratekit.analysis import artifacts, detect, energy, light, vocals
from cratekit.analysis import cli as analysis_cli
from cratekit.cli import handlers, registry
from cratekit.core import config, jobs, routing, tags, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.write import metadata_cli
from tests._containers import synth_container
from tests.cli_drive import drive
from tests.test_analysis import _FakeModel
from tests.test_config import valid_data

SRC_ROOT = Path(__file__).resolve().parent.parent / "src"
VOCALS_SOURCE = SRC_ROOT / "cratekit" / "analysis" / "vocals.py"


# ---------------------------------------------------------------------------
# Fixtures and seams
# ---------------------------------------------------------------------------


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    """A configured machine. This is the configuration a job freezes."""
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    # THE FULL PROFILE, because the analysis verbs are not members of the slim
    # one and a slim configuration builds a parser with no ``analyze`` at all.
    built = config.from_dict(valid_data(library, profile={"name": "full"}))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    return synth_container(tmp_path_factory.mktemp("silence"), ".flac")


@pytest.fixture
def folder(tmp_path) -> Path:
    out = tmp_path / "downloads"
    out.mkdir()
    return out


@pytest.fixture(autouse=True)
def unbound(monkeypatch):
    """Every test starts with nothing bound, the state a fresh worker process is in."""
    monkeypatch.setattr(light, "_DETECT", None)
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", None)
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    monkeypatch.setattr(vocals, "_DECODER", None)
    monkeypatch.setattr(energy, "_EXTRACTOR", None)


def place(folder: Path, silence: Path, name: str, **fields) -> Path:
    path = folder / f"{name}.flac"
    shutil.copy2(silence, path)
    if fields:
        assert tags.write_tags(path, fields), f"the fixture could not tag {name}"
    return path


def detector(level: int | None = 6, status: str = energy.STATUS_CALIBRATED):
    """A head that finds the same key and tempo on every file and records the asks."""
    seen: list[str] = []

    def detect_(path: Path):
        seen.append(path.name)
        return {
            "path": path,
            "camelot": "8A",
            "rate": 124,
            "energy": level,
            "energy_status": status,
        }

    detect_.seen = seen  # type: ignore[attr-defined]
    return detect_


def voiced(samples: int = 16000, level: float = 0.2):
    """A decoder that hands the fake model a signal it scores as vocal."""
    return lambda path: np.full(samples, level, dtype=np.float32)


def bind_scoring(monkeypatch, *, detect_=None, decoder=None, loader=None):
    monkeypatch.setattr(light, "_DETECT", detect_ if detect_ is not None else detector())
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", loader if loader is not None else _FakeModel)
    monkeypatch.setattr(vocals, "_DECODER", decoder if decoder is not None else voiced())


def analysis_job(key: str):
    with jobs.open_store() as store:
        held = [
            job
            for job in jobs.list_jobs(store)
            if job.handler_key == registry.entry(key).handler_key
        ]
    assert len(held) == 1, f"expected exactly one {key} job, found {len(held)}"
    return held[0]


def resume_argv(job_id: str) -> list[str]:
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def item_states(job_id: str) -> dict[str, jobs.ItemState]:
    with jobs.open_store() as store:
        return {item.item_id: item.state for item in jobs.items(store, job_id)}


def item_causes(job_id: str) -> dict[str, str]:
    with jobs.open_store() as store:
        return {
            item.item_id: item.cause.reason
            for item in jobs.items(store, job_id)
            if item.cause is not None
        }


def features(seed: int) -> dict[str, float]:
    """A deterministic feature vector whose energy rises with ``seed``."""
    base = {name: 0.0 for name in energy.FEATURE_ORDER}
    base["rms_mean"] = 0.05 * seed
    base["loudness_db"] = -30.0 + seed
    base["onset_density"] = 0.5 + 0.1 * seed
    base["centroid_mean"] = 1000.0 + 100.0 * seed
    base["percussive_fraction"] = 0.3 + 0.02 * seed
    base["tempo"] = 120.0 + seed
    return base


def calibration_over(count: int = 12) -> energy.Calibration:
    return energy.calibrate([features(i) for i in range(count)])


# ---------------------------------------------------------------------------
# The binding
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("key", ["analyze.run", "analyze.restamp"])
def test_the_analysis_keys_resolve_to_workers(key):
    """The R-203 half this unit closes, asserted against the table itself."""
    handler_key = registry.entry(key).handler_key
    assert handlers.is_known(handler_key), f"{handler_key} still has no worker"
    assert handlers.unbound_reason(handler_key) is None
    assert callable(handlers.resolve(handler_key))


def test_the_two_workers_are_different_functions():
    assert handlers.resolve("analyze.run") is not handlers.resolve("analyze.restamp")


# ---------------------------------------------------------------------------
# analyze.run, pending to done through the real resume
# ---------------------------------------------------------------------------


def test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result(
    cfg, folder, silence, monkeypatch
):
    """The whole seam: queue, resume, write, rename, and read back off disk."""
    place(folder, silence, "a")
    place(folder, silence, "b")
    head = detector()
    bind_scoring(monkeypatch, detect_=head)

    code, queued = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), queued
    job = analysis_job("analyze.run")
    assert list(item_states(job.job_id)) == ["a.flac", "b.flac"], (
        "the items are the folder's audio filenames, sorted, relative to the folder"
    )
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.PENDING}

    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert head.seen == ["a.flac", "b.flac"]

    renamed = sorted(path.name for path in folder.iterdir())
    assert renamed == ["08A - 124 - a.flac", "08A - 124 - b.flac"]
    done = folder / "08A - 124 - a.flac"
    assert tags.read_tag(done, "initialkey") == "08A"
    assert tags.read_tag(done, "title") == "08A - 124 - a"
    assert tags.read_energy_from_file(done) == 6
    assert tags.read_vox_from_file(done) is not None
    assert tags.read_vox_from_file(done) > 0
    assert tags.read_voxgender_from_file(done) == "M", "the model's call, not a constant"

    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert set(reports) == {"a.flac", "b.flac"}
    assert reports["a.flac"]["status"] == "analyzed"
    assert reports["a.flac"]["renamed_to"] == "08A - 124 - a.flac"
    assert reports["a.flac"]["vocal_active"] is True
    assert reports["a.flac"]["voxlevel"] > 0
    assert resumed["data"]["progress"]["analysis"]["by_status"] == {"analyzed": 2}


def test_a_prefixed_file_is_the_resume_marker_and_is_skipped_without_a_read(
    cfg, folder, silence, monkeypatch
):
    place(folder, silence, "08A - 124 - done")
    place(folder, silence, "fresh")
    head = detector()
    bind_scoring(monkeypatch, detect_=head)

    code, queued = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), queued
    job = analysis_job("analyze.run")
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed

    assert head.seen == ["fresh.flac"]
    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert reports["08A - 124 - done.flac"]["status"] == "skipped-prefixed"
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}


def test_a_keyless_track_is_a_terminal_skip_with_nothing_written(
    cfg, folder, silence, monkeypatch
):
    path = place(folder, silence, "drone")
    before = path.read_bytes()
    bind_scoring(monkeypatch, detect_=lambda p: None)

    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed

    assert path.is_file() and path.read_bytes() == before
    assert tags.read_tag(path, "initialkey") is None
    reports = artifacts.committed(cfg, job.job_id)
    assert reports[0]["status"] == "skipped-no-key"


def test_a_folder_with_no_audio_queues_nothing_and_says_so(cfg, folder):
    code, envelope = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"] == {"job_id": "", "state": "no-audio", "cause": None, "progress": {}}
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_file_removed_between_queueing_and_drive_is_refused_by_name(
    cfg, folder, silence, monkeypatch
):
    place(folder, silence, "gone")
    bind_scoring(monkeypatch)
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    (folder / "gone.flac").unlink()

    code, resumed = drive(resume_argv(job.job_id))
    assert code != int(ExitCode.OK)
    assert item_causes(job.job_id) == {"gone.flac": "source-missing"}


def test_the_missing_extra_refuses_the_item_rather_than_skipping_it_as_keyless(
    cfg, folder, silence, monkeypatch
):
    """Nothing bound and no librosa is the state of a real slim worker process.

    The detector answers a missing extra and a keyless track with the same
    None. A job that skipped every file as keyless on a machine that had no
    librosa would be a clean report over work nothing could do.
    """
    place(folder, silence, "track")
    monkeypatch.setattr(detect, "heavy_available", lambda: False)
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")

    code, resumed = drive(resume_argv(job.job_id))
    # A one item job whose item failed is recorded by the engine as no-evidence
    # with the item's cause INSIDE it, which is the common failure path of a
    # one item job and the shape ``handlers.run_job`` documents.
    assert code != int(ExitCode.OK), resumed
    assert item_causes(job.job_id) == {"track.flac": "module-extras-missing"}
    inner = resumed["cause"]["inner"]
    assert inner["reason"] == "module-extras-missing"
    assert inner["code"] == int(ExitCode.MODULE_UNAVAILABLE)
    assert inner["detail"]["install"] == "pip install 'cratekit[analysis]'"
    # The same remedy token the parser stub renders for this slug, so the one
    # absence is not a bug in the worker and an installation gap at the parser.
    assert inner["remediation"]["remedy"] == "install-module-extra"


def test_a_worker_process_with_nothing_bound_binds_the_shipped_defaults(cfg, monkeypatch):
    monkeypatch.setattr(energy, "load_calibration", lambda cfg_: None)
    analysis_cli._bind_defaults(cfg)
    assert light.bound()
    assert vocals.loader_bound()
    assert light._DETECT.func is detect.analyse_file
    assert light._DETECT.keywords == {"calibration": None}


def test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone(
    cfg, folder, silence, monkeypatch
):
    path = place(folder, silence, "stuck")
    bind_scoring(monkeypatch)
    monkeypatch.setattr(tags, "write_tags", lambda p, fields: False)
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")

    code, _ = drive(resume_argv(job.job_id))
    assert code != int(ExitCode.OK)
    assert item_causes(job.job_id) == {"stuck.flac": "analysis-write-failed"}
    assert path.is_file(), "a failed tag write must not rename"


def test_a_taken_target_name_fails_the_item_and_keeps_the_written_head_in_the_title(
    cfg, folder, silence, monkeypatch
):
    path = place(folder, silence, "twin")
    place(folder, silence, "08A - 124 - twin")
    bind_scoring(monkeypatch)
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")

    code, _ = drive(resume_argv(job.job_id))
    assert code != int(ExitCode.OK)
    assert item_causes(job.job_id) == {"twin.flac": "analysis-write-failed"}
    assert path.is_file()
    assert tags.read_tag(path, "title") == "08A - 124 - twin", (
        "the tags landed before the rename, so the next pass converges"
    )


def test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one(cfg, tmp_path):
    missing = tmp_path / "nowhere"
    for verb in ("run", "restamp"):
        code, envelope = drive(["analyze", verb, str(missing)])
        assert code == int(ExitCode.OK), envelope
        assert envelope["outcome"] == "no_op"
        assert envelope["data"]["state"] == "folder-absent"
        assert [w["code"] for w in envelope["warnings"]] == ["folder-absent"]
    code, envelope = drive(["analyze", "calibrate", str(missing)])
    assert "not a folder" in envelope["data"]["checks"][0]["detail"]


def test_the_frozen_folder_is_absolute_so_a_resume_from_elsewhere_finds_it(
    cfg, folder, silence, monkeypatch
):
    place(folder, silence, "a")
    bind_scoring(monkeypatch)
    monkeypatch.chdir(folder.parent)
    code, queued = drive(["analyze", "run", folder.name])
    assert code == int(ExitCode.OK), queued
    job = analysis_job("analyze.run")
    assert job.payload["folder"] == str(folder.absolute())

    monkeypatch.chdir(folder.parent.parent)
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}


class _Killed(BaseException):
    """A process death, which the item boundary does not convert."""


def kill_after_the_rename(monkeypatch):
    """Arrange for the first finalized report to die before it is staged.

    ``jobs.drive`` converts ``Exception`` at the item boundary, and a kill is
    not one, so the row stays pending under its old name while the file is
    already under its head. The second attempt goes through untouched.
    """
    real = artifacts.produced
    calls: list[str] = []

    def produced(cfg, job, item, report):
        if report.get("status") == "analyzed" and not calls:
            calls.append(item.item_id)
            raise _Killed()
        return real(cfg, job, item, report)

    monkeypatch.setattr(artifacts, "produced", produced)
    return calls


def test_an_item_renamed_before_its_row_moved_resumes_as_finished(
    cfg, folder, silence, monkeypatch
):
    """The kill window between the rename and the row flipping to done.

    THE STEM IS ONE THE TEMPLATE REWRITES, a trailing segment repeating the
    lead, so the finished file's name is not the head plus the item. The
    first version guessed the twin from the folder by stripping heads and
    comparing stems, and refused exactly this file as missing.
    """
    place(folder, silence, "Daft Punk - Around the World - Daft Punk")
    bind_scoring(monkeypatch)
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    killed = kill_after_the_rename(monkeypatch)
    with pytest.raises(_Killed):
        drive(resume_argv(job.job_id))
    assert killed == ["Daft Punk - Around the World - Daft Punk.flac"]
    finished = folder / "08A - 124 - Daft Punk - Around the World.flac"
    assert finished.is_file(), sorted(p.name for p in folder.iterdir())
    assert item_states(job.job_id) != {killed[0]: jobs.ItemState.DONE}

    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    report = artifacts.committed(cfg, job.job_id)[0]
    assert report["status"] == "skipped-prefixed"
    assert report["resumed_after_rename"] is True
    assert report["path"] == str(finished)


def test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed(
    cfg, folder, silence, monkeypatch
):
    """The folder already holds a headed file of the same stem from an
    earlier pass. The queued source is then deleted. Nothing this job did
    produced the headed file, and the first version reported it as this
    item, done, resumed after a rename that never happened."""
    place(folder, silence, "twin")
    place(folder, silence, "08A - 124 - twin")
    bind_scoring(monkeypatch)
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    (folder / "twin.flac").unlink()

    code, _ = drive(resume_argv(job.job_id))
    assert code != int(ExitCode.OK)
    assert item_causes(job.job_id) == {"twin.flac": "source-missing"}
    # The older headed file is an item of its own and is the resume marker;
    # nothing was committed FOR the deleted one.
    assert [r["item"] for r in artifacts.committed(cfg, job.job_id)] == ["08A - 124 - twin.flac"]


def test_a_rename_intent_for_another_item_or_a_gone_target_is_not_a_twin(cfg, folder):
    class Job:
        job_id = "j1"

    class Item:
        item_id = "a.flac"
        ordinal = 1

    assert analysis_cli._finalized_twin(cfg, Job, Item) is None
    artifacts.record_rename_intent(cfg, Job, Item, folder / "08A - 124 - a.flac")
    assert analysis_cli._finalized_twin(cfg, Job, Item) is None, "the target is not there"
    (folder / "08A - 124 - a.flac").write_bytes(b"")
    assert analysis_cli._finalized_twin(cfg, Job, Item) == folder / "08A - 124 - a.flac"
    Item.item_id = "b.flac"
    assert analysis_cli._finalized_twin(cfg, Job, Item) is None, "another item's intent"


def test_a_detector_shaped_like_the_batch_fakes_is_accepted(cfg, folder, silence, monkeypatch):
    place(folder, silence, "a")
    bind_scoring(
        monkeypatch,
        detect_=lambda p: {"path": p, "camelot": "8A", "bpm": 128, "energy": 4},
    )
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert (folder / "08A - 128 - a.flac").is_file()
    assert artifacts.committed(cfg, job.job_id)[0]["tempo"] == 128


def test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug(
    cfg, folder, silence, monkeypatch
):
    """``AUDIO_EXTS`` is wider than the containers ``write_tags`` knows, and the
    writer RAISES on the ones it does not, rather than returning False."""
    path = folder / "odd.webm"
    path.write_bytes(b"not-audio")
    bind_scoring(monkeypatch)
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    code, _ = drive(resume_argv(job.job_id))
    assert code != int(ExitCode.OK)
    assert item_causes(job.job_id) == {"odd.webm": "analysis-write-failed"}
    assert path.is_file()


def test_an_undecodable_file_is_its_own_terminal_and_not_a_keyless_track(
    cfg, folder, silence, monkeypatch
):
    place(folder, silence, "broken")
    bind_scoring(
        monkeypatch,
        detect_=lambda p: {"path": p, "terminal": detect.TERMINAL_UNDECODABLE},
    )
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    report = artifacts.committed(cfg, job.job_id)[0]
    assert report["status"] == "skipped-undecodable"
    assert (folder / "broken.flac").is_file()


def test_the_light_pass_passes_a_detector_terminal_through_by_name():
    light.bind_detect(lambda p: {"path": p, "terminal": "skipped-undecodable"})
    assert light.analyse("x.flac") == {"path": "x.flac", "terminal": "skipped-undecodable"}
    light.bind_detect(lambda p: None)
    assert light.analyse("x.flac") == {"path": "x.flac", "terminal": "skipped-no-key"}


def test_the_default_detector_is_rebound_with_a_fresh_calibration_per_item(cfg):
    analysis_cli._bind_defaults(cfg)
    assert light._DETECT.keywords == {"calibration": None}
    energy.save_calibration(cfg, calibration_over())
    analysis_cli._bind_defaults(cfg)
    assert light._DETECT.keywords["calibration"] == energy.load_calibration(cfg)


def test_a_test_bound_detector_is_left_alone_by_the_default_binding(cfg, monkeypatch):
    fake = detector()
    monkeypatch.setattr(light, "_DETECT", fake)
    analysis_cli._bind_defaults(cfg)
    assert light._DETECT is fake


# ---------------------------------------------------------------------------
# The wav plumbing
# ---------------------------------------------------------------------------


def test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path(monkeypatch):
    """The R-133 agent half: a loaded model now produces a real score."""
    bind_scoring(monkeypatch)
    scored = vocals.analyse({"path": "anything.flac", "terminal": None, "camelot": "8A"})
    assert scored["vocal_active"] is True
    assert scored["vocal_reason"] is None
    assert scored["voxlevel"] > 0
    # THE GENDER IS THE MODEL'S CALL, NOT A CONSTANT. The fake model scores the
    # male class at four times the female class on this signal, so the
    # reduction must say M; the mutation table's one zero row was a worker
    # that reported every track as U with a green suite.
    assert scored["voxgender"] == "M"
    assert scored["voxgenderconf"] == 60


def test_the_vocal_pass_never_reads_a_wav_key_off_the_partial():
    """The regression pin. The first version read ``result.get("wav")`` and
    nothing in the package set it, so every track scored zero with a model
    loaded. A partial carrying samples would also be the memory shape the
    package exists to avoid, so the key must not come back under any name."""
    tree = ast.parse(VOCALS_SOURCE.read_text(encoding="utf-8"))
    literals = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }
    assert "wav" not in literals, "vocals.py reads a wav key off the partial again"
    assert "samples" not in literals


def test_the_decoder_receives_the_partials_path(monkeypatch):
    asked: list[object] = []

    def decoder(path):
        asked.append(path)
        return np.full(16000, 0.2, dtype=np.float32)

    bind_scoring(monkeypatch, decoder=decoder)
    vocals.analyse({"path": "the-track.flac", "terminal": None})
    assert asked == ["the-track.flac"]


def test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero(monkeypatch):
    bind_scoring(monkeypatch, decoder=lambda path: None)
    scored = vocals.analyse({"path": "unreadable.flac", "terminal": None})
    assert scored["vocal_active"] is False
    assert scored["vocal_reason"] == "vocal-audio-undecodable"
    assert scored["voxlevel"] is None
    assert scored["voxgender"] is None


def test_a_model_that_did_not_load_is_a_named_absence(monkeypatch):
    def explode():
        raise RuntimeError("checkpoint missing")

    bind_scoring(monkeypatch, loader=explode)
    scored = vocals.analyse({"path": "x.flac", "terminal": None})
    assert scored["vocal_active"] is False
    assert scored["vocal_reason"] == "vocal-model-unavailable"
    assert scored["voxlevel"] is None


def test_a_terminal_head_is_not_decoded_at_all(monkeypatch):
    asked: list[object] = []
    bind_scoring(monkeypatch, decoder=lambda path: asked.append(path))
    scored = vocals.analyse({"path": "x.flac", "terminal": "skipped-no-key"})
    assert asked == []
    assert scored["vocal_reason"] == "vocal-head-terminal"


def test_the_shipped_decoder_reads_at_the_models_rate_and_is_absent_without_the_extra():
    from cratekit.analysis import vocal

    assert vocal.MODEL_SAMPLE_RATE == 32000
    assert vocal.DEFAULT_CHUNK_SAMPLES == 32000 * 8
    try:
        import librosa  # noqa: F401
    except ImportError:
        assert vocal.decode("nowhere.flac") is None
    # With the extra installed the absence cannot be driven, and a skip here
    # would be one the pending register does not count, so the test says
    # nothing rather than skipping.


def test_run_batch_threads_the_decoder_through_to_the_vocal_pass(tmp_path, monkeypatch):
    from cratekit.analysis.run import run_batch

    path = tmp_path / "track.flac"
    path.write_bytes(b"not-audio")
    results = run_batch(
        [path],
        detect=detector(),
        vocal_loader=_FakeModel,
        decode=voiced(),
    )
    assert results[0].vocal_active is True
    assert results[0].voxlevel > 0
    assert results[0].energy == 6
    assert results[0].energy_status == energy.STATUS_CALIBRATED


# ---------------------------------------------------------------------------
# Energy: a level or an honest absence, and the reader driven on both
# ---------------------------------------------------------------------------


def _energy_bucket() -> tuple[taxonomy.Taxonomy, taxonomy.Bucket]:
    declared = taxonomy.default_taxonomy()
    assert declared.energy.enabled
    bucket = next(
        b for b in declared.buckets if b.sub_by_source is None and b.energy.enabled
    )
    return declared, bucket


def test_an_uncalibrated_library_writes_no_energy_tag_and_routes_to_the_sink(
    cfg, folder, silence, monkeypatch
):
    place(folder, silence, "a")
    bind_scoring(monkeypatch, detect_=detector(level=None, status=energy.STATUS_UNCALIBRATED))
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    code, _ = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK)

    done = folder / "08A - 124 - a.flac"
    read = tags.read_energy_from_file(done)
    assert read is None, "an absent level must not become a tag"
    report = artifacts.committed(cfg, job.job_id)[0]
    assert report["energy"] is None
    assert report["energy_status"] == "uncalibrated"

    declared, bucket = _energy_bucket()
    assert routing.energy_sub(declared, bucket.id, read) == declared.energy.no_energy_sub


def test_a_calibrated_level_is_written_and_routes_to_a_band(
    cfg, folder, silence, monkeypatch
):
    place(folder, silence, "a")
    bind_scoring(monkeypatch, detect_=detector(level=9))
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    code, _ = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK)

    read = tags.read_energy_from_file(folder / "08A - 124 - a.flac")
    assert read == 9
    declared, bucket = _energy_bucket()
    placed = routing.energy_sub(declared, bucket.id, read)
    assert placed is not None
    assert placed != declared.energy.no_energy_sub
    assert placed.id in {band.id for band in declared.energy.bands}


def test_the_detector_names_why_energy_is_what_it_is(monkeypatch):
    samples = np.zeros(2205, dtype=np.float32)
    assert detect.energy_from_samples(samples, 22050, calibration=None) == (
        None,
        energy.STATUS_UNCALIBRATED,
    )
    calibration = calibration_over()
    monkeypatch.setattr(energy, "features_from_samples", lambda *a, **k: None)
    assert detect.energy_from_samples(samples, 22050, calibration=calibration) == (
        None,
        energy.STATUS_FEATURES_UNAVAILABLE,
    )
    monkeypatch.setattr(energy, "features_from_samples", lambda *a, **k: features(11))
    level, status = detect.energy_from_samples(samples, 22050, calibration=calibration)
    assert status == energy.STATUS_CALIBRATED
    assert level == energy.LEVEL_MAX


def test_the_detector_source_no_longer_returns_energy_as_a_literal_none():
    source = (SRC_ROOT / "cratekit" / "analysis" / "detect.py").read_text(encoding="utf-8")
    assert '"energy": None' not in source


def test_a_calibration_spreads_a_library_across_the_scale():
    calibration = calibration_over(count=20)
    assert len(calibration.thresholds) == 9
    assert list(calibration.thresholds) == sorted(calibration.thresholds)
    levels = [energy.level_for(features(i), calibration) for i in range(20)]
    assert levels == sorted(levels), "more energy must never score lower"
    assert min(levels) == energy.LEVEL_MIN
    assert max(levels) == energy.LEVEL_MAX
    assert len(set(levels)) >= 8


def test_the_beatless_guard_caps_a_loud_track_with_no_onsets():
    calibration = calibration_over(count=20)
    loud = features(19)
    assert energy.level_for(loud, calibration) == energy.LEVEL_MAX
    loud["onset_density"] = 0.0
    assert energy.level_for(loud, calibration) <= energy.BEATLESS_CAP


def test_a_missing_feature_imputes_to_the_mean_rather_than_failing():
    calibration = calibration_over()
    partial = {"rms_mean": 0.3}
    assert energy.LEVEL_MIN <= energy.level_for(partial, calibration) <= energy.LEVEL_MAX


def test_a_calibration_round_trips_through_its_state_file(cfg):
    calibration = calibration_over()
    assert energy.load_calibration(cfg) is None
    written = energy.save_calibration(cfg, calibration)
    assert written == config.state_path("energy_calibration", cfg)
    assert energy.load_calibration(cfg) == calibration


def test_a_calibration_with_the_wrong_number_of_cuts_is_refused():
    data = calibration_over().to_json()
    data["thresholds"] = data["thresholds"][:5]
    with pytest.raises(ValueError, match="cut points"):
        energy.Calibration.from_json(data)


def test_a_corrupt_calibration_raises_rather_than_reading_as_absent(cfg):
    path = energy.calibration_path(cfg)
    config._mkdir_private(path.parent)
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(CratekitError) as caught:
        energy.load_calibration(cfg)
    assert caught.value.cause.reason == "energy-calibration-unreadable"


_LIST_WHERE_A_MAPPING_BELONGS = json.dumps(
    {"thresholds": list(range(9)), "mean": [], "std": {}, "weights": {}, "n_tracks": 1}
)


@pytest.mark.parametrize("text", ["{not json", "{}", "[]", _LIST_WHERE_A_MAPPING_BELONGS])
def test_every_corrupt_calibration_shape_is_the_same_named_refusal(cfg, text):
    """The fourth shape raised ``AttributeError`` through the promise the
    loader's docstring makes, and reached the queue as a traceback."""
    path = energy.calibration_path(cfg)
    config._mkdir_private(path.parent)
    path.write_text(text, encoding="utf-8")
    with pytest.raises(CratekitError) as caught:
        energy.load_calibration(cfg)
    assert caught.value.cause.reason == "energy-calibration-unreadable"


def test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect(
    cfg, folder, silence, monkeypatch
):
    """Driven through both verbs: the queue path and the worker path."""
    place(folder, silence, "a")
    path = energy.calibration_path(cfg)
    config._mkdir_private(path.parent)
    path.write_text("{not json", encoding="utf-8")

    code, refused = drive(["analyze", "restamp", str(folder)])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "energy-calibration-unreadable"
    assert "calibrate" in refused["cause"]["message"] or refused["cause"]["remediation"]

    # THE WORKER PATH: the run refuses the same file at its queue now, so the
    # calibration is corrupted AFTER the queue, which is a calibration written
    # between two jobs driven by one process and the reason the default
    # detector is rebound per item.
    path.unlink()
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", _FakeModel)
    monkeypatch.setattr(vocals, "_DECODER", voiced())
    monkeypatch.setattr(detect, "heavy_available", lambda: True)
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    path.write_text("{not json", encoding="utf-8")
    code, resumed = drive(resume_argv(job.job_id))
    assert code != int(ExitCode.OK)
    assert item_causes(job.job_id) == {"a.flac": "energy-calibration-unreadable"}


def test_calibrating_over_nothing_is_refused():
    with pytest.raises(ValueError):
        energy.calibrate([])


def test_the_feature_extractor_is_absent_without_the_extra(tmp_path):
    try:
        import librosa  # noqa: F401
    except ImportError:
        assert energy.features_from_samples(np.zeros(100, dtype=np.float32), 22050) is None
        assert energy.features_from_path(tmp_path / "none.flac") is None


# ---------------------------------------------------------------------------
# analyze.restamp
# ---------------------------------------------------------------------------


def bind_measuring(monkeypatch, table: dict[str, int]):
    """An extractor answering by filename stem with a feature vector of that seed."""
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: features(table[Path(path).stem]))


def test_a_restamp_job_runs_pending_to_done_and_records_the_previous_value(
    cfg, folder, silence, monkeypatch
):
    calibration = calibration_over(count=20)
    energy.save_calibration(cfg, calibration)
    low = place(folder, silence, "low", energylevel=7)
    high = place(folder, silence, "high", energylevel=7)
    untagged = place(folder, silence, "untagged")
    bind_measuring(monkeypatch, {"low": 0, "high": 19, "untagged": 10})

    code, queued = drive(["analyze", "restamp", str(folder)])
    assert code == int(ExitCode.OK), queued
    job = analysis_job("analyze.restamp")
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}

    assert tags.read_energy_from_file(low) == energy.LEVEL_MIN
    assert tags.read_energy_from_file(high) == energy.LEVEL_MAX
    assert tags.read_energy_from_file(untagged) is not None
    assert energy.read_undo_log(cfg) == {
        str(low): "7",
        str(high): "7",
        str(untagged): None,
    }
    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert reports["low.flac"] == {
        "item": "low.flac",
        "path": str(low),
        "status": "restamped",
        "previous": 7,
        "level": energy.LEVEL_MIN,
        "written": True,
        "db_written": False,
    }
    assert any(w["code"] == "db-metadata-not-written" for w in resumed["warnings"]), (
        "the registry declares a database write this build does not perform"
    )
    assert sorted(path.name for path in folder.iterdir()) == ["high.flac", "low.flac", "untagged.flac"], (
        "a restamp writes one tag and renames nothing"
    )


def test_a_file_whose_level_did_not_move_is_reported_unchanged_and_not_rewritten(
    cfg, folder, silence, monkeypatch
):
    calibration = calibration_over(count=20)
    energy.save_calibration(cfg, calibration)
    steady = place(folder, silence, "steady", energylevel=energy.LEVEL_MAX)
    before = steady.stat().st_mtime_ns
    bind_measuring(monkeypatch, {"steady": 19})
    drive(["analyze", "restamp", str(folder)])
    job = analysis_job("analyze.restamp")
    code, _ = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK)
    report = artifacts.committed(cfg, job.job_id)[0]
    assert report["status"] == "unchanged" and report["written"] is False
    assert steady.stat().st_mtime_ns == before
    assert energy.read_undo_log(cfg) == {str(steady): str(energy.LEVEL_MAX)}


def test_the_undo_log_keeps_the_first_previous_value_across_a_second_restamp(
    cfg, folder, silence, monkeypatch
):
    energy.save_calibration(cfg, calibration_over(count=20))
    track = place(folder, silence, "track", energylevel=4)
    bind_measuring(monkeypatch, {"track": 19})
    for _ in range(2):
        drive(["analyze", "restamp", str(folder)])
        with jobs.open_store() as store:
            job = max(jobs.list_jobs(store), key=lambda j: j.created)
        code, _ = drive(resume_argv(job.job_id))
        assert code == int(ExitCode.OK)
        bind_measuring(monkeypatch, {"track": 0})
    assert tags.read_energy_from_file(track) == energy.LEVEL_MIN
    assert energy.read_undo_log(cfg) == {str(track): "4"}


def test_a_restamp_with_no_calibration_refuses_at_the_queue(cfg, folder, silence):
    place(folder, silence, "a")
    code, refused = drive(["analyze", "restamp", str(folder)])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "energy-calibration-missing"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_restamp_over_an_empty_folder_is_the_honest_zero_whatever_the_calibration(
    cfg, folder
):
    code, envelope = drive(["analyze", "restamp", str(folder)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "no-audio"


def test_a_track_that_cannot_be_measured_is_reported_and_left_alone(
    cfg, folder, silence, monkeypatch
):
    energy.save_calibration(cfg, calibration_over())
    track = place(folder, silence, "odd", energylevel=5)
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: None)
    drive(["analyze", "restamp", str(folder)])
    job = analysis_job("analyze.restamp")
    code, _ = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK)
    report = artifacts.committed(cfg, job.job_id)[0]
    assert report["status"] == "features-unavailable"
    assert report["written"] is False
    assert tags.read_energy_from_file(track) == 5
    assert energy.read_undo_log(cfg) == {}


def test_a_restamp_worker_without_the_extra_refuses_rather_than_skipping(
    cfg, folder, silence, monkeypatch
):
    energy.save_calibration(cfg, calibration_over())
    place(folder, silence, "a")
    monkeypatch.setattr(detect, "heavy_available", lambda: False)
    drive(["analyze", "restamp", str(folder)])
    job = analysis_job("analyze.restamp")
    code, resumed = drive(resume_argv(job.job_id))
    assert code != int(ExitCode.OK), resumed
    assert item_causes(job.job_id) == {"a.flac": "module-extras-missing"}
    assert resumed["cause"]["inner"]["reason"] == "module-extras-missing"


# ---------------------------------------------------------------------------
# Calibrate and validate say something true
# ---------------------------------------------------------------------------


def test_calibrate_fits_the_energy_reference_over_a_folder_and_writes_it(
    cfg, folder, silence, monkeypatch
):
    names = [f"t{i:02d}" for i in range(12)]
    for name in names:
        place(folder, silence, name)
    bind_measuring(monkeypatch, {name: index for index, name in enumerate(names)})

    code, envelope = drive(["analyze", "calibrate", str(folder)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    checks = {check["key"]: check for check in envelope["data"]["checks"]}
    assert checks["calibrate.energy"]["status"] == "ok"
    assert checks["calibrate.energy"]["remedy"] is None
    assert "fitted over 12 tracks" in checks["calibrate.energy"]["detail"]
    assert checks["calibrate.vocals"]["status"] == "skipped", (
        "no file carries a vocal score yet, so there is no distribution to cut"
    )
    assert envelope["data"]["summary"] == {
        "folder": str(folder), "calibrated": True, "tracks": 12
    }
    loaded = energy.load_calibration(cfg)
    assert loaded is not None and loaded.n_tracks == 12


def test_calibrate_cuts_the_vocal_threshold_between_the_two_clusters(
    cfg, folder, silence, monkeypatch
):
    names = [f"t{i:02d}" for i in range(12)]
    for index, name in enumerate(names):
        place(folder, silence, name, voxlevel=2 if index < 8 else 40)
    bind_measuring(monkeypatch, {name: index for index, name in enumerate(names)})

    code, envelope = drive(["analyze", "calibrate", str(folder)])
    assert code == int(ExitCode.OK), envelope
    checks = {check["key"]: check for check in envelope["data"]["checks"]}
    assert checks["calibrate.vocals"]["status"] == "ok"
    written = json.loads(analysis_cli.vocal_calibration_path(cfg).read_text())
    assert 2 < written["threshold"] <= 40
    assert written["n_tracks"] == 12 and written["method"] == "otsu"


def test_otsu_separates_a_bimodal_distribution():
    cut = analysis_cli.otsu_threshold([0.0, 1.0, 2.0, 3.0] * 10 + [35.0, 40.0, 45.0] * 4)
    assert 3.0 < cut <= 35.0
    assert analysis_cli.otsu_threshold([]) == analysis_cli.DEFAULT_VOCAL_THRESHOLD


def test_a_single_cluster_is_not_cut_down_the_middle(cfg, folder, silence, monkeypatch):
    """Twelve instrumentals scored 0 to 5. Otsu still finds a best cut; the
    separation check is what says there is nothing on the other side of it."""
    names = [f"t{i:02d}" for i in range(12)]
    for index, name in enumerate(names):
        place(folder, silence, name, voxlevel=index % 6)
    bind_measuring(monkeypatch, {name: index for index, name in enumerate(names)})
    code, envelope = drive(["analyze", "calibrate", str(folder)])
    assert code == int(ExitCode.OK), envelope
    checks = {check["key"]: check for check in envelope["data"]["checks"]}
    assert checks["calibrate.vocals"]["status"] == "skipped"
    assert "do not split into two clusters" in checks["calibrate.vocals"]["detail"]
    assert not analysis_cli.vocal_calibration_path(cfg).exists()


def test_cluster_separation_is_none_with_nothing_on_one_side():
    assert analysis_cli.cluster_separation([1.0, 2.0], 50.0) is None
    assert analysis_cli.cluster_separation([1.0, 41.0], 20.0) == 40.0


# ---------------------------------------------------------------------------
# U90: ``--vocal-cut`` sets the with vox cut by hand
# ---------------------------------------------------------------------------

HAND_DAY = "2026-09-17"


@pytest.fixture
def hand_day(monkeypatch):
    monkeypatch.setattr(analysis_cli, "_today", lambda: HAND_DAY)


def test_a_hand_cut_is_written_and_the_one_loader_reads_it_back(cfg, hand_day):
    code, envelope = drive(["analyze", "calibrate", "--vocal-cut", "5"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert envelope["data"]["summary"] == {
        "folder": None, "vocal_cut": 5.0, "previous_vocal_cut": None
    }
    (check,) = envelope["data"]["checks"]
    assert check["key"] == "calibrate.vocals" and check["status"] == "ok"
    assert "cut set by hand at 5" in check["detail"]
    assert "My Tags used the default 12" in check["detail"]
    assert metadata_cli.load_vocal_threshold(cfg) == 5.0
    assert metadata_cli.vocal_cut(cfg) == 5.0
    record = metadata_cli.load_vocal_calibration(cfg)
    assert record["method"] == "hand"
    assert record["note"] == f"set by hand on {HAND_DAY}"
    assert record["set_on"] == HAND_DAY
    assert energy.load_calibration(cfg) is None, "the energy calibration is left alone"


def test_a_second_hand_cut_reports_the_cut_it_replaces(cfg, hand_day):
    drive(["analyze", "calibrate", "--vocal-cut", "5"])
    code, envelope = drive(["analyze", "calibrate", "--vocal-cut", "7.5"])
    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["previous_vocal_cut"], summary["vocal_cut"]) == (5.0, 7.5)
    assert (
        f"this replaces the cut of 5 set by hand on {HAND_DAY}"
        in envelope["data"]["checks"][0]["detail"]
    )
    assert metadata_cli.load_vocal_threshold(cfg) == 7.5


@pytest.mark.parametrize("cut", ["0", "100"])
def test_the_ends_of_the_score_range_are_cuts(cfg, cut):
    code, envelope = drive(["analyze", "calibrate", "--vocal-cut", cut])
    assert code == int(ExitCode.OK), envelope
    assert metadata_cli.load_vocal_threshold(cfg) == float(cut)


@pytest.mark.parametrize("cut", ["-1", "-0.5", "100.5", "nan", "inf", "-inf"])
def test_a_cut_outside_the_score_range_refuses_and_writes_nothing(cfg, cut):
    code, envelope = drive(["analyze", "calibrate", f"--vocal-cut={cut}"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "vocal-cut-out-of-range"
    assert not analysis_cli.vocal_calibration_path(cfg).exists()


def test_a_refused_cut_leaves_the_cut_on_record_byte_for_byte(cfg, hand_day):
    drive(["analyze", "calibrate", "--vocal-cut", "5"])
    path = analysis_cli.vocal_calibration_path(cfg)
    before = path.read_bytes()
    code, envelope = drive(["analyze", "calibrate", "--vocal-cut", "101"])
    assert code == int(ExitCode.PRECONDITION), envelope
    assert path.read_bytes() == before


def test_a_folder_and_a_hand_cut_together_are_refused_by_the_parser(cfg, folder):
    code, _ = drive(["analyze", "calibrate", str(folder), "--vocal-cut", "5"])
    assert code == int(ExitCode.USAGE)
    assert not analysis_cli.vocal_calibration_path(cfg).exists()


def test_a_hand_cut_replaces_an_unreadable_calibration_and_says_it_could_not_be_read(cfg):
    path = analysis_cli.vocal_calibration_path(cfg)
    config._mkdir_private(path.parent)
    path.write_text("{not json", encoding="utf-8")
    code, envelope = drive(["analyze", "calibrate", "--vocal-cut", "5"])
    assert code == int(ExitCode.OK), envelope
    assert "could not be read" in envelope["data"]["checks"][0]["detail"]
    assert metadata_cli.load_vocal_threshold(cfg) == 5.0


def test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float(cfg):
    """A hand edited file can carry "5.0". The reader checks and converts it, and
    the record it returns carries the converted number, not the text, so the
    calibrate report and every tagging comparison meet a float."""
    path = analysis_cli.vocal_calibration_path(cfg)
    config._mkdir_private(path.parent)
    path.write_text('{"threshold": "5.0", "method": "hand"}', encoding="utf-8")
    assert metadata_cli.load_vocal_calibration(cfg)["threshold"] == 5.0
    assert isinstance(metadata_cli.load_vocal_threshold(cfg), float)
    code, envelope = drive(["analyze", "calibrate", "--vocal-cut", "7"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["previous_vocal_cut"] == 5.0
    assert "this replaces the cut of 5 set by hand" in envelope["data"]["checks"][0]["detail"]


def test_a_calibration_the_account_cannot_read_refuses_and_is_not_replaced(cfg):
    """Not the unreadable slug the hand cut writes over: a permission refusal."""
    path = analysis_cli.vocal_calibration_path(cfg)
    config._mkdir_private(path.parent)
    path.write_text('{"threshold": 9.0, "method": "otsu"}', encoding="utf-8")
    path.chmod(0)
    try:
        code, envelope = drive(["analyze", "calibrate", "--vocal-cut", "5"])
    finally:
        path.chmod(0o600)
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "path-permission-denied"
    assert metadata_cli.load_vocal_threshold(cfg) == 9.0


def test_a_hand_cut_refuses_with_the_library_away(cfg):
    shutil.rmtree(cfg.library.root)
    code, envelope = drive(["analyze", "calibrate", "--vocal-cut", "5"])
    assert code == int(ExitCode.LIBRARY_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == "library-volume-unmounted"
    assert not analysis_cli.vocal_calibration_path(cfg).exists()


def test_a_fit_after_a_hand_cut_replaces_it_and_says_so(
    cfg, folder, silence, monkeypatch, hand_day
):
    drive(["analyze", "calibrate", "--vocal-cut", "5"])
    names = [f"t{i:02d}" for i in range(12)]
    for index, name in enumerate(names):
        place(folder, silence, name, voxlevel=2 if index < 8 else 40)
    bind_measuring(monkeypatch, {name: index for index, name in enumerate(names)})

    code, envelope = drive(["analyze", "calibrate", str(folder)])
    assert code == int(ExitCode.OK), envelope
    checks = {check["key"]: check for check in envelope["data"]["checks"]}
    assert checks["calibrate.vocals"]["status"] == "ok"
    assert (
        f"this replaces the cut of 5 set by hand on {HAND_DAY}"
        in checks["calibrate.vocals"]["detail"]
    )
    record = metadata_cli.load_vocal_calibration(cfg)
    assert record["method"] == "otsu" and record["note"] == f"fitted over {folder}"
    assert 2 < record["threshold"] <= 40 and record["threshold"] != 5.0


def test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces(cfg, folder, silence, monkeypatch):
    names = [f"t{i:02d}" for i in range(12)]
    for index, name in enumerate(names):
        place(folder, silence, name, voxlevel=2 if index < 8 else 40)
    bind_measuring(monkeypatch, {name: index for index, name in enumerate(names)})
    drive(["analyze", "calibrate", str(folder)])
    first = metadata_cli.load_vocal_threshold(cfg)
    code, envelope = drive(["analyze", "calibrate", str(folder)])
    assert code == int(ExitCode.OK), envelope
    checks = {check["key"]: check for check in envelope["data"]["checks"]}
    assert (
        f"this replaces the cut of {first:g} (fitted over {folder})"
        in checks["calibrate.vocals"]["detail"]
    )


def test_calibrate_over_too_few_tracks_writes_nothing_and_says_so(
    cfg, folder, silence, monkeypatch
):
    for name in ("a", "b"):
        place(folder, silence, name)
    bind_measuring(monkeypatch, {"a": 0, "b": 1})
    code, envelope = drive(["analyze", "calibrate", str(folder)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    checks = {check["key"]: check for check in envelope["data"]["checks"]}
    assert checks["calibrate.energy"]["status"] == "failed"
    assert "nothing was written" in checks["calibrate.energy"]["detail"]
    assert energy.load_calibration(cfg) is None


def test_calibrate_with_no_folder_measures_nothing(cfg):
    code, envelope = drive(["analyze", "calibrate"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["checks"][0]["status"] == "skipped"
    assert envelope["data"]["summary"]["calibrated"] is False


def test_calibrate_over_an_empty_folder_is_a_failed_check_not_a_traceback(cfg, folder):
    code, envelope = drive(["analyze", "calibrate", str(folder)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["checks"][0]["status"] == "failed"


def test_calibrate_without_the_extra_refuses_rather_than_fitting_over_nothing(
    cfg, folder, silence, monkeypatch
):
    place(folder, silence, "a")
    monkeypatch.setattr(detect, "heavy_available", lambda: False)
    code, envelope = drive(["analyze", "calibrate", str(folder)])
    assert code == int(ExitCode.MODULE_UNAVAILABLE), envelope
    assert energy.load_calibration(cfg) is None


def test_validate_says_plainly_that_nothing_was_scored(cfg):
    code, envelope = drive(["analyze", "validate"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    check = envelope["data"]["checks"][0]
    assert check["status"] == "unavailable"
    assert check["remedy"] is None
    assert "not been measured" in check["detail"]
    assert envelope["data"]["summary"]["validated"] is False
    assert "awaiting" not in json.dumps(envelope)
    assert "report-defect" not in json.dumps(envelope)


# ---------------------------------------------------------------------------
# The slim install stays slim
# ---------------------------------------------------------------------------


def test_the_analysis_package_imports_with_the_heavy_stack_blocked():
    """Nothing this unit added reaches for librosa, torch or the model at import.

    A fresh interpreter rather than a reload, because reloading a module in
    the running suite replaces function objects other tests hold.
    """
    import subprocess

    script = (
        "import sys\n"
        "for name in ('librosa', 'torch', 'panns_inference', 'scipy', 'numpy'):\n"
        "    sys.modules[name] = None\n"
        "import cratekit.analysis.energy, cratekit.analysis.vocals\n"
        "import cratekit.analysis.detect, cratekit.analysis.light\n"
        "import cratekit.analysis.artifacts, cratekit.analysis.cli\n"
        "import cratekit.cli.handlers\n"
        "from cratekit.cli import jobs as cli_jobs\n"
        "print('slim')\n"
    )
    proc = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "slim"


# ---------------------------------------------------------------------------
# The second fix round, from the review over the whole branch
# ---------------------------------------------------------------------------


def test_a_dotfile_sidecar_beside_a_track_is_not_an_item(cfg, folder, silence):
    """macOS writes ``._track.flac`` beside every file on an exFAT stick."""
    place(folder, silence, "track")
    place(folder, silence, "._track")
    (folder / ".DS_Store.flac").write_bytes(b"")
    assert analysis_cli._audio_in(folder) == ["track.flac"]


def test_a_corrupt_undo_log_refuses_by_name_rather_than_failing_every_item_as_a_defect(
    cfg, folder, silence, monkeypatch
):
    path = place(folder, silence, "a", energylevel=4)
    energy.save_calibration(cfg, calibration_over())
    log = energy.undo_log_path(cfg)
    config._mkdir_private(log.parent)
    log.write_text("[]", encoding="utf-8")
    bind_measuring(monkeypatch, {"a": 9})
    drive(["analyze", "restamp", str(folder)])
    job = analysis_job("analyze.restamp")

    code, resumed = drive(resume_argv(job.job_id))
    assert code != int(ExitCode.OK)
    assert item_causes(job.job_id) == {"a.flac": "analysis-write-failed"}
    inner = resumed["cause"]["inner"]
    assert inner["detail"]["undo_log"] == str(log)
    assert "only record" in inner["message"]
    assert tags.read_energy_from_file(path) == 4, "nothing was written over the file"
    assert log.read_text(encoding="utf-8") == "[]", "the unreadable text was kept"


def test_a_model_whose_inference_raises_is_a_named_absence_with_the_head_intact(monkeypatch):
    class Rejects:
        labels = ("Singing", "Male singing", "Female singing")

        def inference(self, wav):
            raise RuntimeError("shape the network does not take")

    monkeypatch.setattr(vocals, "_VOCAL_LOADER", Rejects)
    monkeypatch.setattr(vocals, "_DECODER", voiced())
    scored = vocals.analyse({"path": "x.flac", "terminal": None, "camelot": "8A", "rate": 124})
    assert scored["vocal_active"] is False
    assert scored["vocal_reason"] == vocals.REASON_INFERENCE_FAILED
    assert scored["voxlevel"] is None
    assert (scored["camelot"], scored["rate"]) == ("8A", 124)


def test_a_run_with_no_model_loaded_warns_on_the_envelope(cfg, folder, silence, monkeypatch):
    """The declared extra is ``analysis`` and the model is behind ``vocals``,
    so a machine with the first and not the second finalizes every track
    with no vocal tags. The item reports carried the absence; the envelope
    did not."""
    place(folder, silence, "a")

    def no_model():
        raise ImportError("panns_inference")

    bind_scoring(monkeypatch, loader=no_model)
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert [w["code"] for w in resumed["warnings"]] == [vocals.REASON_MODEL_UNAVAILABLE]
    assert "cratekit[vocals]" in resumed["warnings"][0]["message"]
    assert resumed["data"]["progress"]["analysis"]["by_vocal_reason"] == {
        vocals.REASON_MODEL_UNAVAILABLE: 1
    }


def test_a_run_with_the_model_loaded_carries_no_vocal_warning(cfg, folder, silence, monkeypatch):
    place(folder, silence, "a")
    bind_scoring(monkeypatch)
    drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert resumed["warnings"] == []
    assert resumed["data"]["progress"]["analysis"]["by_vocal_reason"] == {}


def test_a_decodable_file_the_analyser_raises_on_is_its_own_terminal_not_keyless(monkeypatch):
    """A stinger too short for a tempo decodes and then raises inside the
    analyser; the first version returned None there, which the light pass
    reported as atonal."""
    import types

    def tempo(**kwargs):
        raise ValueError("too short")

    fake = types.SimpleNamespace(
        load=lambda p, sr, mono: (np.ones(64, dtype=np.float32), sr),
        feature=types.SimpleNamespace(tempo=tempo),
        effects=types.SimpleNamespace(),
    )
    monkeypatch.setitem(sys.modules, "librosa", fake)
    found = detect.analyse_file(Path("stinger.flac"))
    assert found == {"path": Path("stinger.flac"), "terminal": detect.TERMINAL_UNANALYSABLE}
    assert light.analyse("stinger.flac")["terminal"] == "skipped-unanalysable"


def test_the_head_decodes_at_the_energy_measure_rate():
    source = (SRC_ROOT / "cratekit" / "analysis" / "detect.py").read_text(encoding="utf-8")
    assert "sr=MEASURE_RATE" in source
    assert "22050" not in source, "a second literal for the rate is how the two drift"


def test_the_feature_vector_measures_its_own_tempo_on_every_path():
    """The head's whole track integer tempo is no longer handed down, so a
    file scored by ``analyze run`` and by ``analyze restamp`` carries one
    tempo reading against one calibration."""
    import inspect

    assert "tempo" not in inspect.signature(energy.features_from_samples).parameters
    assert "tempo" not in inspect.signature(detect.energy_from_samples).parameters


def test_an_unreadable_calibration_refuses_a_run_at_the_queue(cfg, folder, silence, monkeypatch):
    place(folder, silence, "a")
    path = energy.calibration_path(cfg)
    config._mkdir_private(path.parent)
    path.write_text("{not json", encoding="utf-8")
    bind_scoring(monkeypatch)
    code, queued = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.PRECONDITION), queued
    assert queued["cause"]["reason"] == "energy-calibration-unreadable"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_an_absent_calibration_still_queues_a_run(cfg, folder, silence, monkeypatch):
    place(folder, silence, "a")
    bind_scoring(monkeypatch)
    code, queued = drive(["analyze", "run", str(folder)])
    assert code == int(ExitCode.OK), queued


def test_calibrate_refuses_with_the_library_away_rather_than_writing_beside_the_mount(
    cfg, folder, silence, monkeypatch
):
    for i in range(12):
        place(folder, silence, f"t{i}")
    table = {f"t{i}.flac": i for i in range(12)}
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda p: features(table[p.name]))
    shutil.rmtree(cfg.library.root)
    code, envelope = drive(["analyze", "calibrate", str(folder)])
    assert code == int(ExitCode.LIBRARY_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == "library-volume-unmounted"
    assert not energy.calibration_path(cfg).exists()
    assert not cfg.library.root.exists(), "nothing created the root on the way to the file"


def test_calibrate_declares_the_mount_check_its_state_writes_need():
    assert "library.mounted" in registry.entry("analyze.calibrate").doctor_checks


def test_an_unknown_tag_field_is_a_defect_and_not_a_container_refusal(folder, silence):
    """The writer's plain ``ValueError`` is the beat grid enforcement point,
    R17. Folding it into the container refusal would report a defect in this
    module as a folder of awkward files."""
    path = place(folder, silence, "a")
    with pytest.raises(ValueError, match="unknown tag fields"):
        analysis_cli._write_or_refuse(path, {"averagebpm": "124"}, untouched="untouched")
    odd = folder / "odd.webm"
    odd.write_bytes(b"not-audio")
    with pytest.raises(CratekitError) as caught:
        analysis_cli._write_or_refuse(odd, {"initialkey": "08A"}, untouched="untouched")
    assert caught.value.cause.reason == "analysis-write-failed"


def test_a_stray_json_beside_the_reports_does_not_take_the_summary_down(cfg):
    class Job:
        job_id = "j9"

    class Item:
        item_id = "a.flac"
        ordinal = 1

    produced = artifacts.produced(cfg, Job, Item, {"status": "analyzed"})
    jobs.commit_artifact(produced.staged, produced.final)
    (produced.final.parent / "notes.json").write_text("{}", encoding="utf-8")
    assert artifacts.committed(cfg, "j9") == ({"status": "analyzed"},)


def test_the_restamp_reads_the_tag_once_and_records_its_text(cfg, folder, silence, monkeypatch):
    """A tag another tool wrote as text is recorded as that text and compared
    as no level, from one read rather than two that could disagree."""
    path = place(folder, silence, "a")
    assert tags.write_tags(path, {"energylevel": "7/10"})
    energy.save_calibration(cfg, calibration_over())
    bind_measuring(monkeypatch, {"a": 9})
    drive(["analyze", "restamp", str(folder)])
    job = analysis_job("analyze.restamp")
    code, _ = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK)
    assert energy.read_undo_log(cfg) == {str(path): "7/10"}
    report = artifacts.committed(cfg, job.job_id)[0]
    assert report["previous"] is None
    assert report["written"] is True


def test_the_verb_module_never_imports_the_model_module_at_module_scope():
    """``cli.jobs.argv_for`` imports the verb module by name to build a resume
    command line, and the model module needs numpy at import time."""
    source = (SRC_ROOT / "cratekit" / "analysis" / "cli.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "cratekit.analysis":
            assert "vocal" not in {alias.name for alias in node.names}
