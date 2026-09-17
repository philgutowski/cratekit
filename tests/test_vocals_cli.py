"""U25: ``analyze.vocals`` scores Camelot-prefixed files. ``analyze.run`` still skips them."""

from __future__ import annotations

import contextlib
import io
import shutil
from pathlib import Path

import numpy as np
import pytest

from cratekit import cli
from cratekit.analysis import artifacts, vocals
from cratekit.cli import handlers, registry
from cratekit.core import config, jobs, profiles, tags
from cratekit.core.exit_codes import ExitCode
from tests._containers import synth_container
from tests.cli_drive import drive
from tests.test_analysis import _FakeModel
from tests.test_config import valid_data


@pytest.fixture
def cfg(tmp_path, monkeypatch) -> config.Config:
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
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
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", None)
    monkeypatch.setattr(vocals, "_VOCAL_MODEL", None)
    monkeypatch.setattr(vocals, "_VOCAL_FAILED", False)
    monkeypatch.setattr(vocals, "_DECODER", None)


def place(folder: Path, silence: Path, name: str, **fields) -> Path:
    path = folder / f"{name}.flac"
    shutil.copy2(silence, path)
    if fields:
        assert tags.write_tags(path, fields), f"the fixture could not tag {name}"
    return path


def voiced(samples: int = 16000, level: float = 0.2):
    return lambda path: np.full(samples, level, dtype=np.float32)


def bind_scoring(monkeypatch, *, decoder=None, loader=None):
    monkeypatch.setattr(vocals, "_VOCAL_LOADER", loader if loader is not None else _FakeModel)
    monkeypatch.setattr(vocals, "_DECODER", decoder if decoder is not None else voiced())


def vocals_job():
    with jobs.open_store() as store:
        held = [
            job
            for job in jobs.list_jobs(store)
            if job.handler_key == registry.entry("analyze.vocals").handler_key
        ]
    assert len(held) == 1, f"expected exactly one analyze.vocals job, found {len(held)}"
    return held[0]


def resume_argv(job_id: str) -> list[str]:
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def item_states(job_id: str) -> dict[str, jobs.ItemState]:
    with jobs.open_store() as store:
        return {item.item_id: item.state for item in jobs.items(store, job_id)}


def test_the_vocals_key_resolves_to_a_worker_that_is_not_the_run_worker():
    assert handlers.is_known("analyze.vocals")
    assert handlers.resolve("analyze.vocals") is not handlers.resolve("analyze.run")
    assert handlers.resolve("analyze.vocals") is not handlers.resolve("analyze.restamp")


def test_a_prefixed_file_is_scored_by_analyze_vocals_and_not_skipped(
    cfg, folder, silence, monkeypatch
):
    """R-277. The head is the resume marker for ``analyze.run``, not for this verb."""
    prefixed = place(folder, silence, "08A - 124 - done")
    bind_scoring(monkeypatch)

    code, queued = drive(["analyze", "vocals", str(folder)])
    assert code == int(ExitCode.OK), queued
    job = vocals_job()
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}

    assert prefixed.name == "08A - 124 - done.flac", "a vocals restamp renames nothing"
    assert tags.read_vox_from_file(prefixed) is not None
    assert tags.read_vox_from_file(prefixed) > 0
    assert tags.read_voxgender_from_file(prefixed) == "M"
    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert reports["08A - 124 - done.flac"]["status"] == "scored"
    assert reports["08A - 124 - done.flac"]["written"] is True


def test_a_file_finalized_with_no_voxlevel_is_scored_once_the_model_is_bound(
    cfg, folder, silence, monkeypatch
):
    """The R-277 cost: analyzed without the model, then scored by this verb."""
    finalized = place(folder, silence, "08A - 124 - a")
    assert tags.read_vox_from_file(finalized) is None
    bind_scoring(monkeypatch)

    drive(["analyze", "vocals", str(folder)])
    job = vocals_job()
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert tags.read_vox_from_file(finalized) is not None
    assert tags.read_vox_from_file(finalized) > 0
    assert tags.read_tag(finalized, "initialkey") is None, (
        "this verb writes vocal tags only, never a key or a rename"
    )


def test_analyze_run_still_skips_a_prefixed_file(cfg, folder, silence, monkeypatch):
    """Resume is not broken: the run worker still treats the head as finished."""
    from tests.test_analysis_workers import bind_scoring as bind_run
    from tests.test_analysis_workers import detector

    place(folder, silence, "08A - 124 - done")
    head = detector()
    bind_run(monkeypatch, detect_=head)

    drive(["analyze", "run", str(folder)])
    with jobs.open_store() as store:
        held = [job for job in jobs.list_jobs(store) if job.handler_key == "analyze.run"]
    assert len(held) == 1
    code, resumed = drive(resume_argv(held[0].job_id))
    assert code == int(ExitCode.OK), resumed
    assert head.seen == []
    reports = {report["item"]: report for report in artifacts.committed(cfg, held[0].job_id)}
    assert reports["08A - 124 - done.flac"]["status"] == "skipped-prefixed"


def test_a_missing_vocals_extra_names_the_install_command():
    def importer(name: str):
        raise ImportError("torch is not installed", name="torch")

    entry = registry.entry("analyze.vocals")
    parser = cli.build_parser(
        [entry], membership=profiles.resolve("full"), importer=importer
    )
    help_text = io.StringIO()
    with contextlib.redirect_stdout(help_text), pytest.raises(SystemExit):
        parser.parse_args(["analyze", "--help"])
    listed = " ".join(help_text.getvalue().split())
    assert "requires the 'vocals' extra" in listed

    args = parser.parse_args(["analyze", "vocals"])
    assert args._stub is not None
    cause = cli._stub_cause(args._entry, args._stub)
    assert cause.code is ExitCode.MODULE_UNAVAILABLE
    assert cause.detail["install"] == "pip install 'cratekit[vocals]'"


def test_help_still_lists_other_verbs_when_the_vocals_extra_is_blocked(
    cfg, monkeypatch
):
    del cfg

    class Blocker:
        def find_spec(self, name, path=None, target=None):
            if name.split(".")[0] in {"torch", "panns_inference"}:
                raise ImportError(f"blocked: {name}", name=name)
            return None

    import sys

    monkeypatch.setattr(sys, "meta_path", [Blocker(), *sys.meta_path])
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        code, _, _ = _drive_help(["--help"])
    assert code == 0
    assert "crate" in printed.getvalue()
    assert "analyze" in printed.getvalue()


def _drive_help(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def test_a_slim_worker_refuses_at_the_queue_rather_than_reporting_done(
    cfg, folder, silence, monkeypatch
):
    """Nothing bound and no extra is the state of a real slim process.

    The availability check is patched rather than relied on, because the
    suite runs in a venv that may carry the extra (R-370).
    """
    monkeypatch.setattr(
        vocals, "missing_requirement", lambda: "the 'vocals' extra is not installed here"
    )
    place(folder, silence, "track")
    code, refused = drive(["analyze", "vocals", str(folder)])
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "module-extras-missing"
    assert refused["cause"]["detail"]["install"] == "pip install 'cratekit[vocals]'"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_missing_checkpoint_is_refused_at_the_queue_and_named(
    cfg, folder, silence, monkeypatch, tmp_path
):
    """A job that could score nothing is not filed, and the message names the file."""
    import sys
    import types

    labels = tmp_path / "class_labels_indices.csv"
    labels.write_text("index,mid,display_name\n", encoding="utf-8")
    monkeypatch.setattr(vocals, "LABELS", labels)
    monkeypatch.setattr(vocals, "CHECKPOINT", tmp_path / "absent.pth")
    monkeypatch.setitem(sys.modules, "torch", types.ModuleType("torch"))
    monkeypatch.setitem(sys.modules, "panns_inference", types.ModuleType("panns_inference"))
    place(folder, silence, "track")
    code, refused = drive(["analyze", "vocals", str(folder)])
    assert code != int(ExitCode.OK), refused
    assert refused["cause"]["reason"] == "module-extras-missing"
    assert "absent.pth" in refused["cause"]["detail"]["missing"]
    assert "absent.pth" in refused["cause"]["message"]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_an_unchanged_score_is_not_rewritten(cfg, folder, silence, monkeypatch):
    bind_scoring(monkeypatch)
    track = place(folder, silence, "08A - 124 - steady")
    drive(["analyze", "vocals", str(folder)])
    job = vocals_job()
    drive(resume_argv(job.job_id))
    before = track.stat().st_mtime_ns
    drive(["analyze", "vocals", str(folder)])
    with jobs.open_store() as store:
        second = max(
            (job for job in jobs.list_jobs(store) if job.handler_key == "analyze.vocals"),
            key=lambda job: job.created,
        )
    code, _ = drive(resume_argv(second.job_id))
    assert code == int(ExitCode.OK)
    report = artifacts.committed(cfg, second.job_id)[0]
    assert report["status"] == "unchanged" and report["written"] is False
    assert track.stat().st_mtime_ns == before


def test_a_folder_with_no_audio_queues_nothing(cfg, folder):
    code, envelope = drive(["analyze", "vocals", str(folder)])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "no-audio"
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_owed_by_unit_no_longer_lists_25():
    import importlib.util

    path = Path(__file__).resolve().parent.parent / "scripts" / "board.py"
    spec = importlib.util.spec_from_file_location("board_under_test_u25", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    owed = module.owed_by_unit()
    assert 25 not in owed
    assert registry.entry("analyze.vocals").planned_in is None
    assert registry.entry("metadata.mytags-vocals").planned_in is None
