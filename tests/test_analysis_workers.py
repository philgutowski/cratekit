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
from cratekit.modules import extras
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

    code, queued = drive(["analyze", "run", "--queue-only", str(folder)])
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

    code, queued = drive(["analyze", "run", "--queue-only", str(folder)])
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

    drive(["analyze", "run", "--queue-only", str(folder)])
    job = analysis_job("analyze.run")
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed

    assert path.is_file() and path.read_bytes() == before
    assert tags.read_tag(path, "initialkey") is None
    reports = artifacts.committed(cfg, job.job_id)
    assert reports[0]["status"] == "skipped-no-key"


def test_a_folder_with_no_audio_queues_nothing_and_says_so(cfg, folder):
    code, envelope = drive(["analyze", "run", "--queue-only", str(folder)])
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
    drive(["analyze", "run", "--queue-only", str(folder)])
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
    drive(["analyze", "run", "--queue-only", str(folder)])
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
    assert inner["detail"]["install"] == extras.install_command("analysis")
    # The same remedy token the parser stub renders for this slug, so the one
    # absence is not a bug in the worker and an installation gap at the parser.
    assert inner["remediation"]["remedy"] == "install-module-extra"


def test_a_worker_process_with_nothing_bound_binds_the_shipped_defaults(cfg, monkeypatch):
    monkeypatch.setattr(energy, "load_calibration", lambda cfg_: None)
    analysis_cli._bind_defaults(cfg)
    assert light.bound()
    assert vocals.loader_bound()
    assert light._DETECT.func is detect.analyse_file
    assert light._DETECT.keywords == {
        "calibration": None,
        "tempo_window": (cfg.analysis.tempo_floor, cfg.analysis.tempo_ceiling),
        # U157: the drift's verdict is read against the configured cut.
        "drift_cut": cfg.analysis.drift_cut,
    }


def test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone(
    cfg, folder, silence, monkeypatch
):
    path = place(folder, silence, "stuck")
    bind_scoring(monkeypatch)
    monkeypatch.setattr(tags, "write_tags", lambda p, fields: False)
    drive(["analyze", "run", "--queue-only", str(folder)])
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
    drive(["analyze", "run", "--queue-only", str(folder)])
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
    code, queued = drive(["analyze", "run", "--queue-only", folder.name])
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
    drive(["analyze", "run", "--queue-only", str(folder)])
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
    drive(["analyze", "run", "--queue-only", str(folder)])
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


# ---------------------------------------------------------------------------
# U223: an interrupt between the staged report and the commit
# ---------------------------------------------------------------------------


def interrupt_once_staged(monkeypatch, *, status: str = "analyzed", times: int = 1):
    """A real SIGINT the moment an item's report is staged, before its commit.

    The window A60's live run hit (#423, sitting 72): the handler has renamed
    the file and returned its staged report, and the engine's own checkpoint
    finds the signal outstanding, releases the item uncommitted and cancels
    the job. Nothing here edits a store or a staging file by hand.
    """
    import os
    import signal

    real = artifacts.produced
    hits: list[str] = []

    def produced(cfg, job, item, report):
        staged = real(cfg, job, item, report)
        if report.get("status") == status and len(hits) < times:
            hits.append(item.item_id)
            os.kill(os.getpid(), signal.SIGINT)
        return staged

    monkeypatch.setattr(artifacts, "produced", produced)
    return hits


def _interrupted(stopped: dict) -> list[str]:
    """The resume argv the interrupted answer printed, checked against its line."""
    import shlex

    argv = stopped["cause"]["detail"]["resume"]
    step = stopped["cause"]["remediation"]["steps"][0]
    assert step == f"resume it with: {shlex.join(['crate', *argv])}", step
    return list(argv)


def test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command(
    cfg, folder, silence, monkeypatch
):
    """U223's bug, through the verb a person runs and the command it prints.

    The shipped ``staged_path`` cleared the item's whole staging directory,
    rename intent and all, in the same attempt that renamed the file, so the
    resume found the source gone, no intent, and failed the item for ever as
    ``source-missing`` over a file analysed and renamed on disk.
    """
    place(folder, silence, "a parade")
    place(folder, silence, "b untouched")
    seen = detector()
    bind_scoring(monkeypatch, detect_=seen)
    hits = interrupt_once_staged(monkeypatch)

    code, stopped = drive(["analyze", "run", str(folder)])

    assert code == int(ExitCode.INTERRUPTED), stopped
    assert hits == ["a parade.flac"]
    finished = folder / "08A - 124 - a parade.flac"
    assert finished.is_file() and not (folder / "a parade.flac").exists()
    job = analysis_job("analyze.run")
    assert item_states(job.job_id) == {
        "a parade.flac": jobs.ItemState.PENDING,
        "b untouched.flac": jobs.ItemState.PENDING,
    }

    code, resumed = drive(_interrupted(stopped))

    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    by_item = {r["item"]: r for r in artifacts.committed(cfg, job.job_id)}
    assert by_item["a parade.flac"]["status"] == "skipped-prefixed"
    assert by_item["a parade.flac"]["resumed_after_rename"] is True
    assert by_item["a parade.flac"]["path"] == str(finished)
    assert by_item["b untouched.flac"]["status"] == "analyzed"
    assert seen.seen == ["a parade.flac", "b untouched.flac"], "a track was analysed twice"


def test_a_resume_interrupted_in_the_same_window_is_resumed_again(
    cfg, folder, silence, monkeypatch
):
    """The resume's own report is staged and the signal lands again before its
    commit. The intent must outlive that attempt too, or the second resume is
    the shipped bug one attempt later."""
    place(folder, silence, "a")
    bind_scoring(monkeypatch)
    interrupt_once_staged(monkeypatch)
    _, stopped = drive(["analyze", "run", str(folder)])
    argv = _interrupted(stopped)

    hits = interrupt_once_staged(monkeypatch, status="skipped-prefixed")
    code, again = drive(argv)
    assert code == int(ExitCode.INTERRUPTED), again
    assert hits == ["a.flac"]

    # THE ``--job`` PATH LEAVES ITS JOB CANCELLED, which ``crate job resume``
    # re-arms before it drives; the arming is taken by hand here so the drive
    # stays in this process where the scoring is bound.
    job = analysis_job("analyze.run")
    with jobs.open_store() as store:
        jobs.retry(store, job.job_id)
    code, resumed = drive(argv)
    assert code == int(ExitCode.OK), resumed
    report = artifacts.committed(cfg, job.job_id)[0]
    assert report["resumed_after_rename"] is True
    assert report["path"] == str(folder / "08A - 124 - a.flac")


def test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report(
    cfg, folder, silence, monkeypatch
):
    """The state A60's job is in on the machine today: the file renamed, the
    staged report naming it, and no intent. The report is this item's own
    record of the rename, so it is the proof when the intent is gone."""
    place(folder, silence, "a")
    bind_scoring(monkeypatch)
    interrupt_once_staged(monkeypatch)
    _, stopped = drive(["analyze", "run", str(folder)])
    job = analysis_job("analyze.run")
    item = _item(job.job_id, "a.flac")
    intent = artifacts.intent_path(cfg, job.job_id, item.ordinal)
    assert intent.is_file(), "the attempt that renamed the file lost its intent"
    intent.unlink()

    code, resumed = drive(_interrupted(stopped))

    assert code == int(ExitCode.OK), resumed
    report = artifacts.committed(cfg, job.job_id)[0]
    assert report["resumed_after_rename"] is True
    assert report["path"] == str(folder / "08A - 124 - a.flac")


def _item(job_id: str, item_id: str) -> jobs.Item:
    with jobs.open_store() as store:
        return next(i for i in jobs.items(store, job_id) if i.item_id == item_id)


class _Job:
    job_id = "j1"


class _Item:
    item_id = "a.flac"
    ordinal = 1


def _job_over(folder: Path):
    class Job:
        job_id = "j1"
        payload = {"folder": str(folder)}

    return Job


def _stage(cfg, report: dict) -> Path:
    return artifacts.write(artifacts.staged_path(cfg, _Job.job_id, _Item.ordinal), report)


def test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder(
    cfg, folder, tmp_path
):
    """The fallback reads the item's own record, never the folder, and each
    field it trusts is driven alone."""
    job = _job_over(folder)
    twin = folder / "08A - 124 - a.flac"
    twin.write_bytes(b"x")
    analysed = {
        "item": "a.flac",
        "path": str(twin),
        "renamed_to": twin.name,
        "status": "analyzed",
    }
    assert analysis_cli._finalized_twin(cfg, job, _Item) is None, "nothing staged"
    _stage(cfg, analysed)
    assert analysis_cli._finalized_twin(cfg, job, _Item) == twin
    _stage(cfg, {**analysed, "item": "b.flac"})
    assert analysis_cli._finalized_twin(cfg, job, _Item) is None, "another item's report"
    _stage(cfg, {**analysed, "renamed_to": None})
    assert analysis_cli._finalized_twin(cfg, job, _Item) is None, "a report with no rename"
    _stage(cfg, {**analysed, "renamed_to": "08A - 125 - a.flac"})
    assert analysis_cli._finalized_twin(cfg, job, _Item) is None, "renamed_to is not its path"
    _stage(cfg, {**analysed, "status": "skipped-prefixed"})
    assert analysis_cli._finalized_twin(cfg, job, _Item) is None, "not an analysed report"
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / twin.name).write_bytes(b"x")
    _stage(cfg, {**analysed, "path": str(elsewhere / twin.name)})
    assert analysis_cli._finalized_twin(cfg, job, _Item) is None, "outside the folder"
    resumed = {"item": "a.flac", "path": str(twin), "status": "skipped-prefixed"}
    _stage(cfg, {**resumed, "resumed_after_rename": True})
    assert analysis_cli._finalized_twin(cfg, job, _Item) == twin, "a resume's own report"
    _stage(cfg, resumed)
    assert analysis_cli._finalized_twin(cfg, job, _Item) is None, "a prefixed skip"
    _stage(cfg, analysed)
    twin.unlink()
    assert analysis_cli._finalized_twin(cfg, job, _Item) is None, "the target is gone"


def test_a_staged_report_that_is_not_json_or_not_a_mapping_is_no_twin(cfg, folder):
    job = _job_over(folder)
    staged = artifacts.staged_path(cfg, _Job.job_id, _Item.ordinal)
    staged.write_text("{not json", encoding="utf-8")
    assert analysis_cli._finalized_twin(cfg, job, _Item) is None
    staged.write_text("[1, 2]", encoding="utf-8")
    assert analysis_cli._finalized_twin(cfg, job, _Item) is None


def test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent(cfg, folder):
    """A second attempt starts from a clean staging directory: a stale report
    never leaks into it. Only the intent, the resume's evidence, is kept."""
    first = _stage(cfg, {"item": "a.flac", "status": "analyzed"})
    (first.parent / "scratch.tmp").write_text("x", encoding="utf-8")
    intent = artifacts.record_rename_intent(cfg, _Job, _Item, folder / "08A - 124 - a.flac")

    second = artifacts.staged_path(cfg, _Job.job_id, _Item.ordinal)

    assert second == first
    assert sorted(p.name for p in second.parent.iterdir()) == [artifacts.RENAME_INTENT_FILENAME]
    assert intent.is_file()
    assert artifacts.rename_intent(cfg, _Job, _Item) == folder / "08A - 124 - a.flac"


def test_an_attempt_whose_source_is_still_there_drops_a_stale_intent(
    cfg, folder, silence, monkeypatch
):
    """An intent whose source is still a file names a rename that never landed.
    Left behind, it would name whatever later sits at that target as this
    item's twin once the source is deleted."""
    place(folder, silence, "a")
    bind_scoring(monkeypatch)
    drive(["analyze", "run", "--queue-only", str(folder)])
    job = analysis_job("analyze.run")
    item = _item(job.job_id, "a.flac")
    unrelated = folder / "unrelated.flac"
    artifacts.record_rename_intent(cfg, job, item, unrelated)

    code, resumed = drive(resume_argv(job.job_id))

    assert code == int(ExitCode.OK), resumed
    assert artifacts.rename_intent(cfg, job, item) == folder / "08A - 124 - a.flac", (
        "the attempt's own intent replaced the stale one"
    )


def test_a_prefixed_source_drops_a_stale_intent_too(cfg, folder, silence, monkeypatch):
    place(folder, silence, "08A - 124 - a")
    bind_scoring(monkeypatch)
    drive(["analyze", "run", "--queue-only", str(folder)])
    job = analysis_job("analyze.run")
    item = _item(job.job_id, "08A - 124 - a.flac")
    artifacts.record_rename_intent(cfg, job, item, folder / "unrelated.flac")

    code, resumed = drive(resume_argv(job.job_id))

    assert code == int(ExitCode.OK), resumed
    assert artifacts.rename_intent(cfg, job, item) is None


def test_a_taken_target_name_leaves_no_intent_behind(cfg, folder, silence, monkeypatch):
    """The rename never happened, so an intent naming the other file is false.
    A retry after the source is deleted would read it as this item's twin."""
    place(folder, silence, "twin")
    place(folder, silence, "08A - 124 - twin")
    bind_scoring(monkeypatch)
    drive(["analyze", "run", "--queue-only", str(folder)])
    job = analysis_job("analyze.run")

    drive(resume_argv(job.job_id))

    assert item_causes(job.job_id) == {"twin.flac": "analysis-write-failed"}
    item = _item(job.job_id, "twin.flac")
    assert artifacts.rename_intent(cfg, job, item) is None


def test_a_refused_rename_leaves_no_intent_behind(cfg, folder, silence, monkeypatch):
    place(folder, silence, "a")
    bind_scoring(monkeypatch)
    drive(["analyze", "run", "--queue-only", str(folder)])
    job = analysis_job("analyze.run")

    def refuse_rename(self, target):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(Path, "rename", refuse_rename)
    drive(resume_argv(job.job_id))

    assert item_causes(job.job_id) == {"a.flac": "analysis-write-failed"}
    assert (folder / "a.flac").is_file()
    assert not (folder / "08A - 124 - a.flac").exists(), "the claim was left behind"
    item = _item(job.job_id, "a.flac")
    assert artifacts.rename_intent(cfg, job, item) is None


def test_a_detector_shaped_like_the_batch_fakes_is_accepted(cfg, folder, silence, monkeypatch):
    place(folder, silence, "a")
    bind_scoring(
        monkeypatch,
        detect_=lambda p: {"path": p, "camelot": "8A", "bpm": 128, "energy": 4},
    )
    drive(["analyze", "run", "--queue-only", str(folder)])
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
    drive(["analyze", "run", "--queue-only", str(folder)])
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
    drive(["analyze", "run", "--queue-only", str(folder)])
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
    assert light._DETECT.keywords == {
        "calibration": None,
        "tempo_window": (cfg.analysis.tempo_floor, cfg.analysis.tempo_ceiling),
        # U157: the drift's verdict is read against the configured cut.
        "drift_cut": cfg.analysis.drift_cut,
    }
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


# ---------------------------------------------------------------------------
# U92: a file too large to decode is refused before the model is asked for
# ---------------------------------------------------------------------------


def sparse(path: Path, size: int) -> Path:
    """A file that IS ``size`` bytes long and occupies almost none of them.

    ``truncate`` sets the length without writing, so the real shipped cap can
    be driven at its real value and the suite never writes a quarter of a
    gigabyte to anybody's disk.
    """
    with path.open("wb") as handle:
        handle.truncate(size)
    assert path.stat().st_size == size, "the filesystem did not take the sparse length"
    return path


def test_the_shipped_oversize_cap_is_two_hundred_and_fifty_mebibytes():
    """The number itself, not only the comparison over a monkeypatched one.

    A suite that lowers the cap in every test proves the guard fires and says
    nothing about where it fires, so a cap edited to a megabyte or to a
    terabyte would pass all of them. This is the source system's number,
    ``DJ_analysis/vocal_detect.py``.
    """
    assert vocals.VOCAL_MAX_BYTES == 250 * 1024 * 1024


def test_a_file_over_the_cap_never_reaches_the_decoder(tmp_path, monkeypatch):
    """R-408. The decode is what hung the source system, so it is never begun."""
    asked: list[object] = []

    def spy(path):
        asked.append(path)
        return np.full(16000, 0.2, dtype=np.float32)

    track = sparse(tmp_path / "live-set.flac", vocals.VOCAL_MAX_BYTES + 1)
    bind_scoring(monkeypatch, decoder=spy)
    scored = vocals.analyse(
        {"path": str(track), "terminal": None, "camelot": "8A", "rate": 124}
    )
    assert asked == [], "the decoder was handed the file the guard exists to refuse"
    assert scored["vocal_active"] is False
    # THE SLUG'S TEXT, NOT ONLY THE SYMBOL. The mutation table's one zero row
    # was this reason reworded to vocal-file-oversize with every test still
    # green, because every assertion read the constant rather than the string.
    # The slug is a surface: it is the ``vocal_reason`` on the item artifact and
    # the key of ``by_vocal_reason`` on the envelope, so anything reading a run
    # would break on a rename nothing here noticed. Its two siblings are pinned
    # as literals for the same reason, a few tests below.
    assert scored["vocal_reason"] == "vocal-audio-too-large"
    assert scored["vocal_reason"] == vocals.REASON_AUDIO_TOO_LARGE
    # NOT A ZERO. The source system tagged this file voxlevel 0 and this package
    # cannot, because a zero here means the model listened and heard no singing.
    assert scored["voxlevel"] is None
    assert scored["voxgender"] is None
    assert scored["voxgenderconf"] is None
    assert (scored["camelot"], scored["rate"]) == ("8A", 124), "the head survived"


def test_an_oversize_file_is_refused_without_loading_the_model(tmp_path, monkeypatch):
    """The guard sits ahead of the load, not merely ahead of the decode.

    Oversize is a property of the file and true on every machine.
    ``vocal-model-unavailable`` is a property of this box and carries a warning
    telling the person that installing the extra will score these tracks, which
    is false about a file nothing would ever decode.
    """
    loaded: list[int] = []

    def loader():
        loaded.append(1)
        return _FakeModel()

    track = sparse(tmp_path / "mix.flac", vocals.VOCAL_MAX_BYTES + 1)
    bind_scoring(monkeypatch, decoder=voiced(), loader=loader)
    scored = vocals.analyse({"path": str(track), "terminal": None})
    assert loaded == [], "the model was loaded for a file that was never going to be scored"
    assert scored["vocal_reason"] == vocals.REASON_AUDIO_TOO_LARGE


def test_a_file_exactly_at_the_cap_is_still_decoded(tmp_path, monkeypatch):
    """Strictly greater. The cap is the largest size allowed through, not the
    first one refused, which is the source system's comparison too."""
    asked: list[object] = []

    def spy(path):
        asked.append(path)
        return np.full(16000, 0.2, dtype=np.float32)

    track = sparse(tmp_path / "long-track.flac", vocals.VOCAL_MAX_BYTES)
    bind_scoring(monkeypatch, decoder=spy)
    scored = vocals.analyse({"path": str(track), "terminal": None})
    assert asked == [str(track)]
    assert scored["vocal_active"] is True
    assert scored["vocal_reason"] is None
    assert scored["voxlevel"] > 0


def test_a_size_that_cannot_be_read_is_not_oversize_and_the_decode_path_reports(
    tmp_path, monkeypatch
):
    """A stat failure is the decode path's to report, not this guard's.

    Two reporters of one failure is how a missing file comes back as a size
    refusal, which names the wrong remedy.
    """
    gone = tmp_path / "gone.flac"
    assert vocals.is_oversize(gone) is False
    assert vocals.is_oversize(None) is False, "an absent path is not a size"
    bind_scoring(monkeypatch, decoder=lambda path: None)
    scored = vocals.analyse({"path": str(gone), "terminal": None})
    assert scored["vocal_reason"] == vocals.REASON_AUDIO_UNDECODABLE


def test_an_oversize_track_is_never_warned_about_as_a_missing_model(monkeypatch):
    """``unscored_warning`` counts one reason of the five, and this is not it.

    It tells the person to install the vocals extra. No install makes a live
    set decodable, so a summary holding only size refusals warns about nothing,
    and a mixed summary warns about the one track the install would help.

    ``missing_requirement`` is stubbed for the mixed half only because the real
    one imports ``panns_inference``, which is twelve seconds on this machine and
    is not what this test is about. The count is the assertion.
    """
    summary = {"by_vocal_reason": {vocals.REASON_AUDIO_TOO_LARGE: 4}}
    assert vocals.unscored_warning(summary, verb="analysed") is None
    monkeypatch.setattr(vocals, "missing_requirement", lambda: "the extra is not here")
    mixed = {
        "by_vocal_reason": {
            vocals.REASON_AUDIO_TOO_LARGE: 4,
            vocals.REASON_MODEL_UNAVAILABLE: 1,
        }
    }
    warning = vocals.unscored_warning(mixed, verb="analysed")
    assert warning is not None and warning["message"].startswith("1 track(s)")


def test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag(
    cfg, folder, silence, monkeypatch
):
    """End to end through the verb, with the cap lowered to meet the fixture.

    The shipped value is pinned by its own test above. Here the cap comes down
    to a byte so a real container, which the finalize step must be able to
    tag, stands in for a live set.

    IT DOES NOT SHOW THE LIGHT PASS IS GUARDED, and nothing does, because the
    light pass is faked here as it is in every test in this file. On a real
    ``analyze run`` the light decode reads the whole file first and is capped
    by nothing, R-583. What this proves is the vocal half: the reason reaches
    the item report and the summary, and no vox tag is written over the file.
    """
    place(folder, silence, "a", voxlevel=42, voxgender="F")
    bind_scoring(monkeypatch)
    monkeypatch.setattr(vocals, "VOCAL_MAX_BYTES", 1)
    drive(["analyze", "run", "--queue-only", str(folder)])
    job = analysis_job("analyze.run")
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert resumed["data"]["progress"]["analysis"]["by_vocal_reason"] == {
        vocals.REASON_AUDIO_TOO_LARGE: 1
    }
    assert resumed["warnings"] == [], "no install makes this file decodable"
    report = {item["item"]: item for item in artifacts.committed(cfg, job.job_id)}["a.flac"]
    assert report["vocal_active"] is False
    assert report["vocal_reason"] == vocals.REASON_AUDIO_TOO_LARGE
    assert report["voxlevel"] is None and report["voxgender"] is None
    final = Path(report["path"])
    assert tags.read_vox_from_file(final) == 42, "the vox tag already on the file was kept"
    assert tags.read_voxgender_from_file(final) == "F"


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
    drive(["analyze", "run", "--queue-only", str(folder)])
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
    drive(["analyze", "run", "--queue-only", str(folder)])
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

    code, refused = drive(["analyze", "restamp", "--queue-only", str(folder)])
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
    drive(["analyze", "run", "--queue-only", str(folder)])
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

    code, queued = drive(["analyze", "restamp", "--queue-only", str(folder)])
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
    drive(["analyze", "restamp", "--queue-only", str(folder)])
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
        drive(["analyze", "restamp", "--queue-only", str(folder)])
        with jobs.open_store() as store:
            job = max(jobs.list_jobs(store), key=lambda j: j.created)
        code, _ = drive(resume_argv(job.job_id))
        assert code == int(ExitCode.OK)
        bind_measuring(monkeypatch, {"track": 0})
    assert tags.read_energy_from_file(track) == energy.LEVEL_MIN
    assert energy.read_undo_log(cfg) == {str(track): "4"}


def test_a_restamp_with_no_calibration_refuses_at_the_queue(cfg, folder, silence):
    place(folder, silence, "a")
    code, refused = drive(["analyze", "restamp", "--queue-only", str(folder)])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "energy-calibration-missing"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_restamp_over_an_empty_folder_is_the_honest_zero_whatever_the_calibration(
    cfg, folder
):
    code, envelope = drive(["analyze", "restamp", "--queue-only", str(folder)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "no-audio"


def test_a_track_that_cannot_be_measured_is_reported_and_left_alone(
    cfg, folder, silence, monkeypatch
):
    energy.save_calibration(cfg, calibration_over())
    track = place(folder, silence, "odd", energylevel=5)
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: None)
    drive(["analyze", "restamp", "--queue-only", str(folder)])
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
    drive(["analyze", "restamp", "--queue-only", str(folder)])
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

    code, envelope = drive(["analyze", "calibrate", str(folder), "--accept-partial"])
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
        "folder": str(folder), "calibrated": True, "tracks": 12,
        "recursive": False, "sampled": 12,
    }
    loaded = energy.load_calibration(cfg)
    assert loaded is not None and loaded.n_tracks == 12
    assert loaded.note == f"fitted over 12 of 12 under {folder}"


def test_calibrate_cuts_the_vocal_threshold_between_the_two_clusters(
    cfg, folder, silence, monkeypatch
):
    names = [f"t{i:02d}" for i in range(12)]
    for index, name in enumerate(names):
        place(folder, silence, name, voxlevel=2 if index < 8 else 40)
    bind_measuring(monkeypatch, {name: index for index, name in enumerate(names)})

    code, envelope = drive(["analyze", "calibrate", str(folder), "--accept-partial"])
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
    code, envelope = drive(["analyze", "calibrate", str(folder), "--accept-partial"])
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


def test_a_fit_over_a_cut_it_cannot_open_reports_the_energy_it_wrote(
    cfg, folder, silence, monkeypatch
):
    """The energy half is written before the vocal half reads the old cut, so
    the vocal half fails in its check and the verb does not refuse over it."""
    names = [f"t{i:02d}" for i in range(12)]
    for index, name in enumerate(names):
        place(folder, silence, name, voxlevel=2 if index < 8 else 40)
    bind_measuring(monkeypatch, {name: index for index, name in enumerate(names)})
    path = analysis_cli.vocal_calibration_path(cfg)
    config._mkdir_private(path.parent)
    path.write_text('{"threshold": 9.0, "method": "hand"}', encoding="utf-8")
    path.chmod(0)
    try:
        code, envelope = drive(["analyze", "calibrate", str(folder), "--accept-partial"])
    finally:
        path.chmod(0o600)
    assert code == int(ExitCode.OK), envelope
    checks = {check["key"]: check for check in envelope["data"]["checks"]}
    assert checks["calibrate.energy"]["status"] == "ok"
    assert energy.load_calibration(cfg) is not None
    assert checks["calibrate.vocals"]["status"] == "failed"
    assert "no cut was written" in checks["calibrate.vocals"]["detail"]
    assert checks["calibrate.vocals"]["remedy"] is not None
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

    code, envelope = drive(["analyze", "calibrate", str(folder), "--accept-partial"])
    assert code == int(ExitCode.OK), envelope
    checks = {check["key"]: check for check in envelope["data"]["checks"]}
    assert checks["calibrate.vocals"]["status"] == "ok"
    assert (
        f"this replaces the cut of 5 set by hand on {HAND_DAY}"
        in checks["calibrate.vocals"]["detail"]
    )
    record = metadata_cli.load_vocal_calibration(cfg)
    assert record["method"] == "otsu" and record["note"] == f"fitted over 12 of 12 under {folder}"
    assert 2 < record["threshold"] <= 40 and record["threshold"] != 5.0


def test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces(cfg, folder, silence, monkeypatch):
    names = [f"t{i:02d}" for i in range(12)]
    for index, name in enumerate(names):
        place(folder, silence, name, voxlevel=2 if index < 8 else 40)
    bind_measuring(monkeypatch, {name: index for index, name in enumerate(names)})
    drive(["analyze", "calibrate", str(folder), "--accept-partial"])
    first = metadata_cli.load_vocal_threshold(cfg)
    code, envelope = drive(["analyze", "calibrate", str(folder), "--accept-partial"])
    assert code == int(ExitCode.OK), envelope
    checks = {check["key"]: check for check in envelope["data"]["checks"]}
    assert (
        f"this replaces the cut of {first:g} (fitted over 12 of 12 under {folder})"
        in checks["calibrate.vocals"]["detail"]
    )


def test_calibrate_over_too_few_tracks_writes_nothing_and_says_so(
    cfg, folder, silence, monkeypatch
):
    for name in ("a", "b"):
        place(folder, silence, name)
    bind_measuring(monkeypatch, {"a": 0, "b": 1})
    code, envelope = drive(["analyze", "calibrate", str(folder), "--accept-partial"])
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
    code, envelope = drive(["analyze", "calibrate", str(folder), "--accept-partial"])
    assert code == int(ExitCode.OK), envelope
    (check,) = envelope["data"]["checks"]
    assert check["key"] == "calibrate.folder" and check["status"] == "failed"
    assert "holds no audio files" in check["detail"]


def test_calibrate_over_a_folder_that_is_not_there_says_that_and_not_empty(cfg, tmp_path):
    code, envelope = drive(["analyze", "calibrate", str(tmp_path / "nowhere")])
    assert code == int(ExitCode.OK), envelope
    (check,) = envelope["data"]["checks"]
    assert check["key"] == "calibrate.folder" and check["status"] == "failed"
    assert "is not a folder on this machine" in check["detail"]


def test_calibrate_without_the_extra_refuses_rather_than_fitting_over_nothing(
    cfg, folder, silence, monkeypatch
):
    place(folder, silence, "a")
    monkeypatch.setattr(detect, "heavy_available", lambda: False)
    code, envelope = drive(["analyze", "calibrate", str(folder), "--accept-partial"])
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
    drive(["analyze", "restamp", "--queue-only", str(folder)])
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
    drive(["analyze", "run", "--queue-only", str(folder)])
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
    drive(["analyze", "run", "--queue-only", str(folder)])
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

    def onset_strength(**kwargs):
        raise ValueError("too short")

    fake = types.SimpleNamespace(
        load=lambda p, sr, mono: (np.ones(64, dtype=np.float32), sr),
        onset=types.SimpleNamespace(onset_strength=onset_strength),
        feature=types.SimpleNamespace(),
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
    code, queued = drive(["analyze", "run", "--queue-only", str(folder)])
    assert code == int(ExitCode.PRECONDITION), queued
    assert queued["cause"]["reason"] == "energy-calibration-unreadable"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_an_absent_calibration_still_queues_a_run(cfg, folder, silence, monkeypatch):
    place(folder, silence, "a")
    bind_scoring(monkeypatch)
    code, queued = drive(["analyze", "run", "--queue-only", str(folder)])
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
    drive(["analyze", "restamp", "--queue-only", str(folder)])
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


# ---------------------------------------------------------------------------
# U93: a recursive restamp queues a whole tree as one resumable job
# ---------------------------------------------------------------------------


def nest(folder: Path, silence: Path, relative: str, **fields) -> Path:
    """``place``, one level down or more. The item id becomes this relative path."""
    path = folder / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(silence, path)
    if fields:
        assert tags.write_tags(path, fields), f"the fixture could not tag {relative}"
    return path


def test_a_recursive_restamp_queues_every_nested_file_once_in_sorted_order(
    cfg, folder, silence, monkeypatch
):
    """R-376's shape on the restamp half: one invocation instead of one per folder."""
    energy.save_calibration(cfg, calibration_over(count=20))
    nest(folder, silence, "house/a.flac", energylevel=7)
    nest(folder, silence, "techno/deep/b.flac", energylevel=7)
    place(folder, silence, "top", energylevel=7)
    bind_measuring(monkeypatch, {"a": 0, "b": 19, "top": 10})

    code, queued = drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])
    assert code == int(ExitCode.OK), queued
    job = analysis_job("analyze.restamp")
    assert sorted(item_states(job.job_id)) == [
        "house/a.flac",
        "techno/deep/b.flac",
        "top.flac",
    ]


def test_a_recursive_restamp_freezes_the_flag_in_the_payload(cfg, folder, silence, monkeypatch):
    """The payload records what the queue meant, so a job is readable after the fact."""
    energy.save_calibration(cfg, calibration_over(count=20))
    nest(folder, silence, "house/a.flac", energylevel=7)
    bind_measuring(monkeypatch, {"a": 5})
    drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])
    assert analysis_job("analyze.restamp").payload["recursive"] is True


def test_a_restamp_without_the_flag_stays_one_level_and_says_so_in_the_payload(
    cfg, folder, silence, monkeypatch
):
    """The default is unchanged, which is what every existing job and resume assumed."""
    energy.save_calibration(cfg, calibration_over(count=20))
    place(folder, silence, "top", energylevel=7)
    nest(folder, silence, "house/a.flac", energylevel=7)
    bind_measuring(monkeypatch, {"top": 5})

    code, queued = drive(["analyze", "restamp", "--queue-only", str(folder)])
    assert code == int(ExitCode.OK), queued
    job = analysis_job("analyze.restamp")
    assert sorted(item_states(job.job_id)) == ["top.flac"]
    assert job.payload["recursive"] is False


def test_a_recursive_restamp_runs_every_nested_item_to_done_and_writes_the_right_file(
    cfg, folder, silence, monkeypatch
):
    """The item id is a path, so the worker has to resolve it against the frozen folder."""
    energy.save_calibration(cfg, calibration_over(count=20))
    low = nest(folder, silence, "house/low.flac", energylevel=7)
    high = nest(folder, silence, "techno/deep/high.flac", energylevel=7)
    bind_measuring(monkeypatch, {"low": 0, "high": 19})

    drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])
    job = analysis_job("analyze.restamp")
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert tags.read_energy_from_file(low) == energy.LEVEL_MIN
    assert tags.read_energy_from_file(high) == energy.LEVEL_MAX
    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert reports["house/low.flac"]["path"] == str(low)
    assert reports["techno/deep/high.flac"]["path"] == str(high)


def test_two_nested_folders_holding_the_same_filename_are_two_items(
    cfg, folder, silence, monkeypatch
):
    """``job_items`` is keyed ``(job_id, item_id)``, so bare names would collide.

    Every real library holds one track name in more than one genre folder. Under
    bare names the second insert raises and no recursive queue exists at all.
    """
    energy.save_calibration(cfg, calibration_over(count=20))
    nest(folder, silence, "house/track.flac", energylevel=7)
    nest(folder, silence, "techno/track.flac", energylevel=7)
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: features(3))

    code, queued = drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])
    assert code == int(ExitCode.OK), queued
    job = analysis_job("analyze.restamp")
    assert sorted(item_states(job.job_id)) == ["house/track.flac", "techno/track.flac"]


def test_a_nested_appledouble_sidecar_and_a_dot_directory_are_not_items(
    cfg, folder, silence, monkeypatch
):
    energy.save_calibration(cfg, calibration_over(count=20))
    nest(folder, silence, "house/track.flac", energylevel=7)
    nest(folder, silence, "house/._track.flac")
    nest(folder, silence, ".Trashes/deleted.flac")
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: features(3))

    drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])
    assert sorted(item_states(analysis_job("analyze.restamp").job_id)) == ["house/track.flac"]


def test_a_nested_file_deleted_after_the_queue_refuses_that_item_only(
    cfg, folder, silence, monkeypatch
):
    energy.save_calibration(cfg, calibration_over(count=20))
    kept = nest(folder, silence, "house/kept.flac", energylevel=7)
    doomed = nest(folder, silence, "techno/doomed.flac", energylevel=7)
    bind_measuring(monkeypatch, {"kept": 19, "doomed": 0})

    drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])
    job = analysis_job("analyze.restamp")
    doomed.unlink()
    code, _ = drive(resume_argv(job.job_id))

    assert code != int(ExitCode.OK), "a failed item is not a clean run"
    assert item_states(job.job_id) == {
        "house/kept.flac": jobs.ItemState.DONE,
        "techno/doomed.flac": jobs.ItemState.FAILED,
    }
    assert item_causes(job.job_id) == {"techno/doomed.flac": "source-missing"}
    assert tags.read_energy_from_file(kept) == energy.LEVEL_MAX


def test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest(
    cfg, folder, silence, monkeypatch
):
    """A real SIGINT through the engine's own checkpoint, not a hand edited store."""
    import os
    import signal

    energy.save_calibration(cfg, calibration_over(count=20))
    for relative in ("house/a.flac", "house/b.flac", "techno/c.flac", "techno/d.flac"):
        nest(folder, silence, relative, energylevel=7)

    measured: list[str] = []

    def interrupting(path):
        measured.append(Path(path).name)
        if len(measured) == 2:
            os.kill(os.getpid(), signal.SIGINT)
        return features(19)

    monkeypatch.setattr(energy, "_EXTRACTOR", interrupting)
    drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])
    job = analysis_job("analyze.restamp")
    drive(resume_argv(job.job_id))
    done_after_kill = [
        item for item, state in item_states(job.job_id).items() if state is jobs.ItemState.DONE
    ]
    assert done_after_kill, "the kill landed before any item settled"
    assert len(done_after_kill) < 4, "the kill did not stop the driver"

    # A KILL CANCELS THE JOB, which is not FAILED (R22), and a cancelled job is
    # re-armed before it is driven again. ``crate job resume`` does exactly this
    # and then spawns a detached child; the arming is taken by hand here so the
    # driving stays in this process where the bound extractor lives.
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: features(19))
    with jobs.open_store() as store:
        jobs.retry(store, job.job_id)
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert sorted(item_states(job.job_id)) == [
        "house/a.flac",
        "house/b.flac",
        "techno/c.flac",
        "techno/d.flac",
    ]


def test_a_recursive_restamp_says_which_linked_folders_it_did_not_walk(
    cfg, folder, silence, tmp_path, monkeypatch
):
    """A silent skip would be a clean report over a subtree nothing read."""
    energy.save_calibration(cfg, calibration_over(count=20))
    nest(folder, silence, "house/track.flac", energylevel=7)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    shutil.copy2(silence, elsewhere / "other.flac")
    (folder / "linked").symlink_to(elsewhere, target_is_directory=True)
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: features(3))

    code, queued = drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])
    assert code == int(ExitCode.OK), queued
    assert sorted(item_states(analysis_job("analyze.restamp").job_id)) == ["house/track.flac"]
    assert any(w["code"] == "linked-folder-skipped" for w in queued["warnings"]), queued


def test_a_tree_whose_only_folders_are_links_says_so_on_the_zero(
    cfg, folder, silence, tmp_path
):
    """The one place the omission changes the answer completely."""
    energy.save_calibration(cfg, calibration_over(count=20))
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    shutil.copy2(silence, elsewhere / "other.flac")
    (folder / "linked").symlink_to(elsewhere, target_is_directory=True)

    code, said = drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])
    assert code == int(ExitCode.OK), said
    assert said["data"]["state"] == "no-audio"
    assert any(w["code"] == "linked-folder-skipped" for w in said["warnings"]), said


def test_analyze_run_does_not_take_the_recursive_flag(cfg, folder):
    """Its last act on a track is a rename, and its resume marker is the NAME."""
    code, refused = drive(["analyze", "run", "--queue-only", str(folder), "--recursive"])
    assert code != int(ExitCode.OK), refused


def test_a_restamp_item_that_would_leave_the_frozen_folder_is_refused(cfg, folder, silence):
    """``Path("/library") / "/etc/passwd"`` is ``/etc/passwd``, silently."""

    class Escaping:
        item_id = "/etc/passwd"

    class Job:
        payload = {"folder": str(folder), "recursive": True}

    with pytest.raises(CratekitError) as raised:
        analysis_cli._folder_and_path(Job(), Escaping())
    assert raised.value.cause.reason == "internal-error"


def test_the_resume_repeats_what_the_walk_left_out_rather_than_only_the_queue(
    cfg, folder, silence, tmp_path, monkeypatch
):
    """The resume is the report a person keeps. The queue is the one they scroll past."""
    energy.save_calibration(cfg, calibration_over(count=20))
    nest(folder, silence, "house/track.flac", energylevel=7)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    shutil.copy2(silence, elsewhere / "other.flac")
    (folder / "linked").symlink_to(elsewhere, target_is_directory=True)
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: features(3))

    drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])
    job = analysis_job("analyze.restamp")
    assert job.payload["skipped_links"] == ["linked"]
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert any(w["code"] == "linked-folder-skipped" for w in resumed["warnings"]), resumed


def test_an_unreadable_nested_folder_is_named_rather_than_quietly_contributing_nothing(
    cfg, folder, silence, monkeypatch
):
    """``os.walk`` swallows the error by default, and nothing in the output shows it."""
    energy.save_calibration(cfg, calibration_over(count=20))
    nest(folder, silence, "house/track.flac", energylevel=7)
    shut = folder / "locked"
    shut.mkdir()
    shutil.copy2(silence, shut / "hidden.flac")
    shut.chmod(0o000)
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: features(3))
    try:
        code, queued = drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])
    finally:
        shut.chmod(0o755)

    assert code == int(ExitCode.OK), queued
    assert sorted(item_states(analysis_job("analyze.restamp").job_id)) == ["house/track.flac"]
    unreadable = [w for w in queued["warnings"] if w["code"] == "folder-unreadable"]
    assert unreadable, queued
    assert "locked" in unreadable[0]["message"]


def test_a_one_level_restamp_resume_says_nothing_about_a_walk_it_never_did(
    cfg, folder, silence, monkeypatch
):
    """The default mode's envelope is unchanged, which is what U93 promised."""
    energy.save_calibration(cfg, calibration_over(count=20))
    place(folder, silence, "top", energylevel=7)
    bind_measuring(monkeypatch, {"top": 5})
    drive(["analyze", "restamp", "--queue-only", str(folder)])
    code, resumed = drive(resume_argv(analysis_job("analyze.restamp").job_id))
    assert code == int(ExitCode.OK), resumed
    assert [w["code"] for w in resumed["warnings"]] == ["db-metadata-not-written"]


def test_the_restamp_resume_names_an_unreadable_folder_and_not_only_a_link(
    cfg, folder, silence, monkeypatch
):
    """Both halves of the walk's omission are frozen, so both are read back.

    Added after the U93 mutation table: D19 killed zero because every resume
    case in the suite froze declined links and never an unreadable folder.
    """
    energy.save_calibration(cfg, calibration_over(count=20))
    nest(folder, silence, "house/track.flac", energylevel=7)
    shut = folder / "locked"
    shut.mkdir()
    shutil.copy2(silence, shut / "hidden.flac")
    shut.chmod(0o000)
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: features(3))
    try:
        drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])
    finally:
        shut.chmod(0o755)

    job = analysis_job("analyze.restamp")
    assert job.payload["unreadable_folders"] == ["locked"]
    assert job.payload["skipped_links"] == []
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    unreadable = [w for w in resumed["warnings"] if w["code"] == "folder-unreadable"]
    assert unreadable, resumed
    assert "locked" in unreadable[0]["message"]


# ---------------------------------------------------------------------------
# U94: calibrate fits over a library wide sample and refuses a partial one
# ---------------------------------------------------------------------------


def genre_tree(cfg, silence, monkeypatch, per_folder: int = 8, **fields) -> tuple[Path, list[Path]]:
    """A library root holding two genre folders, measured by a recording fake.

    Returns the root and the list the extractor appends every path it is asked
    about to, in order, which is what "nothing was measured" and "the same
    sample twice" are asserted against.
    """
    root = Path(cfg.library.root)
    seen: list[Path] = []
    seeds: dict[str, int] = {}
    for genre in ("House", "Techno"):
        (root / "Music" / genre).mkdir(parents=True)
        for index in range(per_folder):
            name = f"{genre.lower()}{index:02d}"
            seeds[name] = len(seeds)
            place(root / "Music" / genre, silence, name, **fields)

    def extractor(path):
        seen.append(Path(path))
        return features(seeds[Path(path).stem])

    monkeypatch.setattr(energy, "_EXTRACTOR", extractor)
    return root, seen


def checks_of(envelope: dict) -> dict[str, dict]:
    return {check["key"]: check for check in envelope["data"]["checks"]}


def codes_of(envelope: dict) -> list[str]:
    return [warning["code"] for warning in envelope["warnings"]]


def test_a_single_genre_folder_without_the_flag_writes_nothing_and_says_why(
    cfg, silence, monkeypatch
):
    root, seen = genre_tree(cfg, silence, monkeypatch, per_folder=12, voxlevel=3)
    house = root / "Music" / "House"
    code, envelope = drive(["analyze", "calibrate", str(house)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    (check,) = envelope["data"]["checks"]
    assert check["key"] == "calibrate.sample" and check["status"] == "failed"
    assert "is not the library root" in check["detail"]
    assert "nothing was written" in check["detail"]
    assert "--accept-partial" in check["detail"] and "--recursive" in check["detail"]
    assert check["remedy"] is not None
    assert envelope["data"]["summary"]["calibrated"] is False
    assert seen == [], "a refused sample is refused BEFORE anything is measured"
    assert energy.load_calibration(cfg) is None
    assert not analysis_cli.vocal_calibration_path(cfg).exists()


def test_a_recursive_run_at_the_root_writes_a_calibration_with_the_sample_note(
    cfg, silence, monkeypatch
):
    root, seen = genre_tree(cfg, silence, monkeypatch)
    code, envelope = drive(["analyze", "calibrate", str(root), "--recursive"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    checks = checks_of(envelope)
    assert checks["calibrate.sample"]["status"] == "ok"
    assert checks["calibrate.sample"]["remedy"] is None
    assert checks["calibrate.energy"]["status"] == "ok"
    loaded = energy.load_calibration(cfg)
    assert loaded is not None
    assert loaded.note == f"fitted over 16 of 16 under {root}"
    assert {path.parent.name for path in seen} == {"House", "Techno"}
    assert envelope["data"]["summary"] == {
        "folder": str(root), "calibrated": True, "tracks": 16,
        "recursive": True, "sampled": 16,
    }
    assert analysis_cli.PARTIAL_SAMPLE not in codes_of(envelope)


def test_the_same_tree_gives_the_same_sample_twice(cfg, silence, monkeypatch):
    root, seen = genre_tree(cfg, silence, monkeypatch, per_folder=15)
    argv = ["analyze", "calibrate", str(root), "--recursive", "--sample", "10"]
    code, envelope = drive(argv)
    assert code == int(ExitCode.OK), envelope
    first = list(seen)
    seen.clear()
    drive(argv)
    assert first == seen
    assert len(first) == 10 == len(set(first))
    assert {path.parent.name for path in first} == {"House", "Techno"}, (
        "an even stride over the sorted walk takes from every folder, where the "
        "first ten items would all be House"
    )
    loaded = energy.load_calibration(cfg)
    assert loaded is not None and loaded.n_tracks == 10
    assert loaded.note == f"fitted over 10 of 30 under {root}"
    assert envelope["data"]["summary"]["sampled"] == 10
    assert envelope["data"]["summary"]["tracks"] == 30


def test_accept_partial_writes_and_warns(cfg, silence, monkeypatch):
    root, _ = genre_tree(cfg, silence, monkeypatch, per_folder=12)
    house = root / "Music" / "House"
    code, envelope = drive(["analyze", "calibrate", str(house), "--accept-partial"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    checks = checks_of(envelope)
    assert checks["calibrate.sample"]["status"] == "skipped", (
        "an accepted partial must not read as the library wide fit"
    )
    assert "--accept-partial was given" in checks["calibrate.sample"]["detail"]
    assert checks["calibrate.energy"]["status"] == "ok"
    (warning,) = [w for w in envelope["warnings"] if w["code"] == analysis_cli.PARTIAL_SAMPLE]
    assert str(house) in warning["message"]
    loaded = energy.load_calibration(cfg)
    assert loaded is not None and loaded.note == f"fitted over 12 of 12 under {house}"


def test_the_root_read_one_level_deep_is_partial_and_names_the_flag(cfg, silence, monkeypatch):
    root, seen = genre_tree(cfg, silence, monkeypatch, per_folder=12)
    for index in range(12):
        place(root, silence, f"loose{index:02d}")
    code, envelope = drive(["analyze", "calibrate", str(root)])
    assert code == int(ExitCode.OK), envelope
    (check,) = envelope["data"]["checks"]
    assert check["key"] == "calibrate.sample" and check["status"] == "failed"
    assert "one level deep" in check["detail"]
    assert "add --recursive" in check["detail"]
    assert seen == [] and energy.load_calibration(cfg) is None


def test_a_recursive_walk_of_one_genre_is_still_one_genre(cfg, silence, monkeypatch):
    root, seen = genre_tree(cfg, silence, monkeypatch, per_folder=12)
    house = root / "Music" / "House"
    code, envelope = drive(["analyze", "calibrate", str(house), "--recursive"])
    assert code == int(ExitCode.OK), envelope
    (check,) = envelope["data"]["checks"]
    assert check["status"] == "failed" and "is not the library root" in check["detail"]
    assert seen == [] and energy.load_calibration(cfg) is None


def test_the_music_folder_walked_recursively_is_the_library_too(cfg, silence, monkeypatch):
    """Every module that places a track places it under the music folder."""
    root, _ = genre_tree(cfg, silence, monkeypatch)
    music = root / cfg.library.music_dir
    code, envelope = drive(["analyze", "calibrate", str(music), "--recursive"])
    assert code == int(ExitCode.OK), envelope
    assert checks_of(envelope)["calibrate.sample"]["status"] == "ok"
    assert analysis_cli.PARTIAL_SAMPLE not in codes_of(envelope)
    loaded = energy.load_calibration(cfg)
    assert loaded is not None and loaded.note == f"fitted over 16 of 16 under {music}"


def test_the_root_with_no_loose_tracks_and_no_flag_is_told_about_the_flag(
    cfg, silence, monkeypatch
):
    """The normal layout. The first version walked one level, found nothing,
    and answered "holds no audio files" over a library of genre folders."""
    root, seen = genre_tree(cfg, silence, monkeypatch)
    code, envelope = drive(["analyze", "calibrate", str(root)])
    assert code == int(ExitCode.OK), envelope
    (check,) = envelope["data"]["checks"]
    assert check["key"] == "calibrate.sample" and check["status"] == "failed"
    assert "add --recursive" in check["detail"]
    assert seen == []


def test_a_refusal_known_before_the_walk_does_not_make_the_walk(cfg, silence, monkeypatch):
    root, _ = genre_tree(cfg, silence, monkeypatch)
    walked: list[Path] = []
    real = analysis_cli.discovery.scan_audio

    def recording(folder, **kwargs):
        walked.append(folder)
        return real(folder, **kwargs)

    monkeypatch.setattr(analysis_cli.discovery, "scan_audio", recording)
    drive(["analyze", "calibrate", str(root / "Music" / "House"), "--recursive"])
    drive(["analyze", "calibrate", str(root), "--recursive", "--sample", "3"])
    assert walked == []
    drive(["analyze", "calibrate", str(root), "--recursive"])
    assert walked == [root]


def test_the_wrong_folder_is_said_before_the_missing_extra(cfg, silence, monkeypatch):
    """Nobody should install the analysis stack to be told the folder was wrong."""
    root, _ = genre_tree(cfg, silence, monkeypatch)
    monkeypatch.setattr(energy, "_EXTRACTOR", None)
    monkeypatch.setattr(detect, "heavy_available", lambda: False)
    code, envelope = drive(["analyze", "calibrate", str(root / "Music" / "House")])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["checks"][0]["key"] == "calibrate.sample"


def test_the_root_reached_through_a_link_is_still_the_root(cfg, silence, monkeypatch, tmp_path):
    """Asked of the filesystem, not of two spellings of one folder."""
    root, _ = genre_tree(cfg, silence, monkeypatch)
    link = tmp_path / "shortcut"
    link.symlink_to(root, target_is_directory=True)
    code, envelope = drive(["analyze", "calibrate", str(link), "--recursive"])
    assert code == int(ExitCode.OK), envelope
    assert checks_of(envelope)["calibrate.sample"]["status"] == "ok"
    assert energy.load_calibration(cfg) is not None


@pytest.mark.parametrize("extra", [[], ["--accept-partial"]])
def test_a_sample_below_the_fit_floor_is_refused_before_measuring(
    cfg, silence, monkeypatch, extra
):
    """The floor is a different question from partiality, so the flag does not waive it."""
    root, seen = genre_tree(cfg, silence, monkeypatch)
    below = str(analysis_cli.MIN_CALIBRATION_TRACKS - 1)
    code, envelope = drive(
        ["analyze", "calibrate", str(root), "--recursive", "--sample", below, *extra]
    )
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    (check,) = envelope["data"]["checks"]
    assert check["key"] == "calibrate.sample" and check["status"] == "failed"
    assert f"a sample of {below} is below" in check["detail"]
    assert seen == [] and energy.load_calibration(cfg) is None


def test_a_sample_at_the_fit_floor_is_accepted(cfg, silence, monkeypatch):
    root, seen = genre_tree(cfg, silence, monkeypatch)
    at = str(analysis_cli.MIN_CALIBRATION_TRACKS)
    code, envelope = drive(["analyze", "calibrate", str(root), "--recursive", "--sample", at])
    assert code == int(ExitCode.OK), envelope
    assert checks_of(envelope)["calibrate.energy"]["status"] == "ok"
    assert len(seen) == analysis_cli.MIN_CALIBRATION_TRACKS


def test_the_vocal_cut_reads_every_tagged_file_while_energy_reads_the_sample(
    cfg, silence, monkeypatch
):
    root = Path(cfg.library.root)
    seeds: dict[str, int] = {}
    for genre, level in (("House", 2), ("Vocal House", 40)):
        (root / genre).mkdir()
        for index in range(15):
            name = f"{genre[0].lower()}{index:02d}"
            seeds[name] = len(seeds)
            place(root / genre, silence, name, voxlevel=level)
    bind_measuring(monkeypatch, seeds)
    code, envelope = drive(["analyze", "calibrate", str(root), "--recursive", "--sample", "10"])
    assert code == int(ExitCode.OK), envelope
    assert checks_of(envelope)["calibrate.vocals"]["status"] == "ok"
    record = metadata_cli.load_vocal_calibration(cfg)
    assert record["n_tracks"] == 30, "the vocal half is a tag read and is never sampled"
    assert record["note"] == f"fitted over 30 of 30 under {root}"
    loaded = energy.load_calibration(cfg)
    assert loaded is not None and loaded.n_tracks == 10


def test_the_default_sample_is_what_the_parser_hands_the_verb():
    import argparse

    parser = argparse.ArgumentParser()
    analysis_cli.build_calibrate(parser, registry.entry("analyze.calibrate"))
    args = parser.parse_args(["/library"])
    assert args.sample == analysis_cli.DEFAULT_CALIBRATION_SAMPLE == 500
    assert args.recursive is False and args.accept_partial is False


def test_a_walk_that_left_a_folder_out_is_not_the_library(cfg, silence, monkeypatch, tmp_path):
    """A genre kept as a link is declined by the walker, so the root walked
    recursively is a library missing a genre. The first version called it ok."""
    root, seen = genre_tree(cfg, silence, monkeypatch)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (root / "Music" / "Linked").symlink_to(elsewhere, target_is_directory=True)

    code, refused = drive(["analyze", "calibrate", str(root), "--recursive"])
    assert code == int(ExitCode.OK), refused
    (check,) = refused["data"]["checks"]
    assert check["key"] == "calibrate.sample" and check["status"] == "failed"
    assert "left out 1 folder " in check["detail"]
    (warning,) = [w for w in refused["warnings"] if w["code"] == "linked-folder-skipped"]
    assert "Music/Linked" in warning["message"]
    assert "was read" in warning["message"] and "queued" not in warning["message"], (
        "calibrate has no queue, so the borrowed sentence named a job that did not exist"
    )
    assert seen == [] and energy.load_calibration(cfg) is None

    code, fitted = drive(["analyze", "calibrate", str(root), "--recursive", "--accept-partial"])
    assert code == int(ExitCode.OK), fitted
    assert checks_of(fitted)["calibrate.sample"]["status"] == "skipped"
    assert {"linked-folder-skipped", analysis_cli.PARTIAL_SAMPLE} <= set(codes_of(fitted))
    loaded = energy.load_calibration(cfg)
    assert loaded is not None
    assert loaded.note == f"fitted over 16 of 16 under {root}, with 1 folder not walked", (
        "the warning scrolls away and the file is what a later restamp trusts"
    )


def test_a_folder_the_walk_could_not_list_is_not_the_library_either(
    cfg, silence, monkeypatch
):
    """The second omission, counted alone: ``os.walk`` swallows it by default."""
    root, seen = genre_tree(cfg, silence, monkeypatch)
    shut = root / "Music" / "Locked"
    shut.mkdir()
    shutil.copy2(silence, shut / "hidden.flac")
    shut.chmod(0o000)
    try:
        code, refused = drive(["analyze", "calibrate", str(root), "--recursive"])
    finally:
        shut.chmod(0o755)
    assert code == int(ExitCode.OK), refused
    (check,) = refused["data"]["checks"]
    assert check["key"] == "calibrate.sample" and check["status"] == "failed"
    (warning,) = [w for w in refused["warnings"] if w["code"] == "folder-unreadable"]
    assert "Locked" in warning["message"] and "was read" in warning["message"]
    assert seen == [] and energy.load_calibration(cfg) is None


def test_a_run_where_only_the_vocal_half_wrote_does_not_answer_no_op(
    cfg, silence, monkeypatch
):
    root, _ = genre_tree(cfg, silence, monkeypatch)
    for index, path in enumerate(sorted((root / "Music").rglob("*.flac"))):
        assert tags.write_tags(path, {"voxlevel": 2 if index < 10 else 40})
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: None)
    code, envelope = drive(["analyze", "calibrate", str(root), "--recursive"])
    assert code == int(ExitCode.OK), envelope
    checks = checks_of(envelope)
    assert checks["calibrate.energy"]["status"] == "failed"
    assert checks["calibrate.vocals"]["status"] == "ok"
    assert envelope["outcome"] == "ok", "a file was replaced, so something changed"
    assert envelope["data"]["summary"]["calibrated"] is False
    assert analysis_cli.vocal_calibration_path(cfg).exists()


def test_a_partial_fit_that_wrote_nothing_does_not_warn_about_a_calibration(
    cfg, folder, silence, monkeypatch
):
    for name in ("a", "b"):
        place(folder, silence, name)
    bind_measuring(monkeypatch, {"a": 0, "b": 1})
    code, envelope = drive(["analyze", "calibrate", str(folder), "--accept-partial"])
    assert code == int(ExitCode.OK), envelope
    assert checks_of(envelope)["calibrate.energy"]["status"] == "failed"
    assert analysis_cli.PARTIAL_SAMPLE not in codes_of(envelope)


def test_the_stride_sample_is_even_ordered_and_reaches_the_tail():
    items = [f"{index:04d}" for index in range(1003)]
    taken = analysis_cli.stride_sample(items, 100)
    assert len(taken) == 100 == len(set(taken))
    assert taken == sorted(taken) and taken[0] == items[0]
    assert items.index(taken[-1]) >= len(items) - 11, (
        "a fixed step of len // count stops 3 short per hundred and never "
        "reaches the tail, which in a sorted walk is whole folders"
    )
    gaps = {items.index(b) - items.index(a) for a, b in zip(taken, taken[1:])}
    assert gaps <= {10, 11}
    assert analysis_cli.stride_sample(items, 100) == taken


def test_the_stride_sample_takes_everything_when_there_is_less_than_asked():
    assert analysis_cli.stride_sample(["a", "b", "c"], 500) == ["a", "b", "c"]
    assert analysis_cli.stride_sample(["a", "b", "c"], 3) == ["a", "b", "c"]
    assert analysis_cli.stride_sample(["a", "b", "c"], 0) == []
    assert analysis_cli.stride_sample([], 10) == []


def test_the_restamp_refusal_names_the_library_wide_calibrate(cfg, folder, silence):
    place(folder, silence, "a")
    code, refused = drive(["analyze", "restamp", "--queue-only", str(folder)])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "energy-calibration-missing"
    steps = " ".join(refused["cause"]["remediation"]["steps"])
    assert "--recursive" in steps and "representative folder" not in steps


# ═══════════════════════════════════════════════════════════════════════════
# U192: run by hand, each verb drives the job it queues, in one command
# ═══════════════════════════════════════════════════════════════════════════


def _attempts(job_id: str) -> int:
    with jobs.open_store() as store:
        return jobs.get(store, job_id).attempts


def test_analyze_run_by_hand_queues_and_drives_its_job_to_succeeded_in_one_call(
    cfg, folder, silence, monkeypatch
):
    """The brief's first scenario: one command, every item settled, the files written."""
    place(folder, silence, "a")
    place(folder, silence, "b")
    head = detector()
    bind_scoring(monkeypatch, detect_=head)

    code, settled = drive(["analyze", "run", str(folder)])

    assert code == int(ExitCode.OK), settled
    job = analysis_job("analyze.run")
    assert settled["data"]["job_id"] == job.job_id
    assert settled["data"]["state"] == "succeeded"
    progress = settled["data"]["progress"]
    assert progress["settled"] == progress["total"] == 2
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert head.seen == ["a.flac", "b.flac"]
    assert sorted(path.name for path in folder.iterdir()) == [
        "08A - 124 - a.flac",
        "08A - 124 - b.flac",
    ]
    assert progress["analysis"]["by_status"] == {"analyzed": 2}, (
        "the settled envelope is the resume's, carrying what the pass did"
    )
    assert _attempts(job.job_id) == 1, "the job was driven more than once"


def test_analyze_restamp_by_hand_drives_its_job_and_says_the_database_note_once(
    cfg, folder, silence, monkeypatch
):
    energy.save_calibration(cfg, calibration_over(count=20))
    low = place(folder, silence, "low", energylevel=7)
    high = place(folder, silence, "high", energylevel=7)
    bind_measuring(monkeypatch, {"low": 0, "high": 19})

    code, settled = drive(["analyze", "restamp", str(folder)])

    assert code == int(ExitCode.OK), settled
    job = analysis_job("analyze.restamp")
    assert settled["data"]["state"] == "succeeded"
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert tags.read_energy_from_file(low) == energy.LEVEL_MIN
    assert tags.read_energy_from_file(high) == energy.LEVEL_MAX
    codes = [warning["code"] for warning in settled["warnings"]]
    assert codes.count("db-metadata-not-written") == 1, (
        "the queue's copy of the note rode beside the resume's"
    )


def test_a_restamp_driven_at_its_queue_names_a_linked_folder_once(
    cfg, folder, silence, tmp_path, monkeypatch
):
    """The walk's omission is read back off the frozen payload, not said twice."""
    energy.save_calibration(cfg, calibration_over(count=20))
    nest(folder, silence, "house/track.flac", energylevel=7)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    shutil.copy2(silence, elsewhere / "other.flac")
    (folder / "linked").symlink_to(elsewhere, target_is_directory=True)
    monkeypatch.setattr(energy, "_EXTRACTOR", lambda path: features(3))

    code, settled = drive(["analyze", "restamp", str(folder), "--recursive"])

    assert code == int(ExitCode.OK), settled
    queued = drive(["analyze", "restamp", "--queue-only", str(folder), "--recursive"])[1]
    said = [w for w in settled["warnings"] if w["code"] != "db-metadata-not-written"]
    expected = [w for w in queued["warnings"] if w["code"] != "db-metadata-not-written"]
    assert said, "the link the walk skipped was not named at all"
    assert said == expected, "the settled answer and the queue answer named the walk differently"


@pytest.mark.parametrize("verb", ["run", "restamp"])
def test_queue_only_returns_the_job_queued_with_nothing_driven(
    cfg, folder, silence, monkeypatch, verb
):
    energy.save_calibration(cfg, calibration_over(count=20))
    place(folder, silence, "a", energylevel=7)
    bind_scoring(monkeypatch)
    bind_measuring(monkeypatch, {"a": 3})

    code, queued = drive(["analyze", verb, "--queue-only", str(folder)])

    assert code == int(ExitCode.OK), queued
    job = analysis_job(f"analyze.{verb}")
    assert queued["data"]["state"] == "queued"
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.PENDING}
    assert _attempts(job.job_id) == 0, "a queue only call drove the job"


@pytest.mark.parametrize("verb", ["run", "restamp"])
def test_queue_only_beside_job_is_refused_before_anything_is_queued(cfg, folder, silence, verb):
    place(folder, silence, "a", energylevel=7)

    code, refused = drive(["analyze", verb, str(folder), "--job", "j-1", "--queue-only"])

    assert code == 2, "argparse's own refusal, before the verb runs"
    assert refused == {}, "the verb ran and answered with an envelope"
    with jobs.open_store() as store:
        assert list(jobs.list_jobs(store)) == []


def test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it(
    cfg, folder, silence, monkeypatch
):
    """A real SIGINT through the engine's checkpoint, in the call that queued the job.

    The engine records the stop as cancelled, which is closed, and a closed job's
    ``--job`` command reports rather than drives. So the job must come back
    queued, the refusal must name that command, and the command must finish the
    work without measuring a settled file again.
    """
    import os
    import shlex
    import signal

    energy.save_calibration(cfg, calibration_over(count=20))
    for name in ("a", "b", "c", "d"):
        place(folder, silence, name, energylevel=7)
    measured: list[str] = []

    def interrupting(path):
        measured.append(Path(path).name)
        if len(measured) == 2:
            os.kill(os.getpid(), signal.SIGINT)
        return features(19)

    monkeypatch.setattr(energy, "_EXTRACTOR", interrupting)
    code, stopped = drive(["analyze", "restamp", str(folder)])

    assert code == int(ExitCode.INTERRUPTED), stopped
    assert stopped["outcome"] == "cancelled"
    job = analysis_job("analyze.restamp")
    assert job.state is jobs.JobState.QUEUED, "the interrupted job was left closed"
    command = shlex.join(["crate", *resume_argv(job.job_id)])
    assert stopped["cause"]["remediation"]["steps"][0] == f"resume it with: {command}"
    assert stopped["cause"]["remediation"]["remedy"] is None, (
        "the detached job resume token rode ahead of the foreground command"
    )
    assert stopped["cause"]["detail"]["job_id"] == job.job_id
    done = sorted(i for i, s in item_states(job.job_id).items() if s is jobs.ItemState.DONE)
    assert done and len(done) < 4, done

    code, resumed = drive(resume_argv(job.job_id))

    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert not set(done) & set(measured[2:]), "the resume measured a settled file again"


def test_the_shared_tail_step_queues_only_and_drives_its_job_once(
    cfg, folder, silence, monkeypatch
):
    """``sync land`` and ``label sync --go`` drive each tail job themselves through
    one shared step, so it must queue with the flag."""
    from cratekit.cli import sync_land, tail

    place(folder, silence, "a")
    bind_scoring(monkeypatch)
    report = sync_land._report(None)

    tail.tail_step(report, "analyze", "analyze.run", ("analyze", "run"), folder, cfg)

    job = analysis_job("analyze.run")
    assert job.state is jobs.JobState.SUCCEEDED
    assert _attempts(job.job_id) == 1, "the pass drove the tail job twice"
    assert report.summary["commands"] == [
        ["crate", "analyze", "run", "--queue-only", str(folder)],
        ["crate", *resume_argv(job.job_id)],
    ]
