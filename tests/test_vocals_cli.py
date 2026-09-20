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


def test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags(
    cfg, folder, silence, monkeypatch
):
    """U92, closing R-408, on the second of the two verbs sharing ``analyse``.

    The cap comes down to a byte so a real container stands in for a live set.
    The shipped value of ``VOCAL_MAX_BYTES`` is pinned in
    ``tests/test_analysis_workers.py``, because a suite that only ever lowers
    the cap proves the comparison and never the number.
    """
    track = place(folder, silence, "a live set", voxlevel=7, voxgender="F")
    bind_scoring(monkeypatch)
    monkeypatch.setattr(vocals, "VOCAL_MAX_BYTES", 1)

    code, queued = drive(["analyze", "vocals", str(folder)])
    assert code == int(ExitCode.OK), queued
    job = vocals_job()
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}

    report = artifacts.committed(cfg, job.job_id)[0]
    assert report["status"] == "inactive"
    assert report["vocal_reason"] == vocals.REASON_AUDIO_TOO_LARGE
    assert report["written"] is False
    assert report["voxlevel"] is None, "a track the model never heard is not a zero"
    assert resumed["data"]["progress"]["analysis"]["by_vocal_reason"] == {
        vocals.REASON_AUDIO_TOO_LARGE: 1
    }
    assert resumed["warnings"] == [], "no install makes this file decodable"
    assert tags.read_vox_from_file(track) == 7, "the tag already on the file was kept"
    assert tags.read_voxgender_from_file(track) == "F"


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


# ---------------------------------------------------------------------------
# U93: a recursive vocals pass queues a whole tree as one resumable job
# ---------------------------------------------------------------------------


def nest(folder: Path, silence: Path, relative: str, **fields) -> Path:
    """``place``, one level down or more. The item id becomes this relative path."""
    path = folder / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(silence, path)
    if fields:
        assert tags.write_tags(path, fields), f"the fixture could not tag {relative}"
    return path


def item_causes(job_id: str) -> dict[str, str]:
    with jobs.open_store() as store:
        return {
            item.item_id: item.cause.reason
            for item in jobs.items(store, job_id)
            if item.cause is not None
        }


def test_a_recursive_vocals_pass_queues_every_nested_file_once_in_sorted_order(
    cfg, folder, silence, monkeypatch
):
    """R-376 itself: 343 leaf folders and about 7.7 hours become one invocation."""
    bind_scoring(monkeypatch)
    nest(folder, silence, "house/a.flac")
    nest(folder, silence, "techno/deep/b.flac")
    place(folder, silence, "top")

    code, queued = drive(["analyze", "vocals", str(folder), "--recursive"])
    assert code == int(ExitCode.OK), queued
    job = vocals_job()
    assert sorted(item_states(job.job_id)) == [
        "house/a.flac",
        "techno/deep/b.flac",
        "top.flac",
    ]
    assert job.payload["recursive"] is True


def test_a_vocals_pass_without_the_flag_stays_one_level(cfg, folder, silence, monkeypatch):
    """The default is unchanged, so an existing job and an existing resume are too."""
    bind_scoring(monkeypatch)
    place(folder, silence, "top")
    nest(folder, silence, "house/a.flac")

    code, queued = drive(["analyze", "vocals", str(folder)])
    assert code == int(ExitCode.OK), queued
    job = vocals_job()
    assert sorted(item_states(job.job_id)) == ["top.flac"]
    assert job.payload["recursive"] is False


def test_a_recursive_vocals_pass_scores_the_nested_file_the_item_names(
    cfg, folder, silence, monkeypatch
):
    bind_scoring(monkeypatch)
    nested = nest(folder, silence, "house/deep/a.flac")

    drive(["analyze", "vocals", str(folder), "--recursive"])
    job = vocals_job()
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert set(item_states(job.job_id).values()) == {jobs.ItemState.DONE}
    assert tags.read_vox_from_file(nested) is not None
    reports = {report["item"]: report for report in artifacts.committed(cfg, job.job_id)}
    assert reports["house/deep/a.flac"]["path"] == str(nested)


def test_two_nested_folders_holding_the_same_filename_are_two_vocals_items(
    cfg, folder, silence, monkeypatch
):
    """``job_items`` is keyed ``(job_id, item_id)``, so bare names would collide."""
    bind_scoring(monkeypatch)
    nest(folder, silence, "house/track.flac")
    nest(folder, silence, "techno/track.flac")

    code, queued = drive(["analyze", "vocals", str(folder), "--recursive"])
    assert code == int(ExitCode.OK), queued
    assert sorted(item_states(vocals_job().job_id)) == [
        "house/track.flac",
        "techno/track.flac",
    ]


def test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items(
    cfg, folder, silence, monkeypatch
):
    bind_scoring(monkeypatch)
    nest(folder, silence, "house/track.flac")
    nest(folder, silence, "house/._track.flac")
    nest(folder, silence, ".Trashes/deleted.flac")

    drive(["analyze", "vocals", str(folder), "--recursive"])
    assert sorted(item_states(vocals_job().job_id)) == ["house/track.flac"]


def test_a_nested_file_deleted_after_the_vocals_queue_refuses_that_item_only(
    cfg, folder, silence, monkeypatch
):
    bind_scoring(monkeypatch)
    kept = nest(folder, silence, "house/kept.flac")
    doomed = nest(folder, silence, "techno/doomed.flac")

    drive(["analyze", "vocals", str(folder), "--recursive"])
    job = vocals_job()
    doomed.unlink()
    code, _ = drive(resume_argv(job.job_id))

    assert code != int(ExitCode.OK), "a failed item is not a clean run"
    assert item_states(job.job_id) == {
        "house/kept.flac": jobs.ItemState.DONE,
        "techno/doomed.flac": jobs.ItemState.FAILED,
    }
    assert item_causes(job.job_id) == {"techno/doomed.flac": "source-missing"}
    assert tags.read_vox_from_file(kept) is not None


def test_a_recursive_vocals_pass_says_which_linked_folders_it_did_not_walk(
    cfg, folder, silence, tmp_path, monkeypatch
):
    bind_scoring(monkeypatch)
    nest(folder, silence, "house/track.flac")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    shutil.copy2(silence, elsewhere / "other.flac")
    (folder / "linked").symlink_to(elsewhere, target_is_directory=True)

    code, queued = drive(["analyze", "vocals", str(folder), "--recursive"])
    assert code == int(ExitCode.OK), queued
    assert sorted(item_states(vocals_job().job_id)) == ["house/track.flac"]
    assert any(w["code"] == "linked-folder-skipped" for w in queued["warnings"]), queued


def test_a_vocals_item_that_would_leave_the_frozen_folder_is_refused(cfg, folder):
    """``Path("/library") / "/etc/passwd"`` is ``/etc/passwd``, silently."""
    from cratekit.core.cause import CratekitError
    from cratekit.vocals import cli as vocals_cli

    class Escaping:
        item_id = "../../etc/passwd"

    class Job:
        payload = {"folder": str(folder), "recursive": True}

    with pytest.raises(CratekitError) as raised:
        vocals_cli._folder_and_path(Job(), Escaping())
    assert raised.value.cause.reason == "internal-error"


def test_the_two_queued_verbs_share_one_walker(cfg):
    """The second copy of the scan is gone, which is why it cannot drift again."""
    from cratekit.analysis import cli as analysis_cli
    from cratekit.core import discovery
    from cratekit.vocals import cli as vocals_cli

    assert not hasattr(vocals_cli, "_audio_in"), (
        "the vocals module grew its own scan back; there is one walker and it is "
        "cratekit.core.discovery"
    )
    assert analysis_cli.discovery is discovery
    assert vocals_cli.discovery is discovery


def test_the_vocals_resume_repeats_what_the_walk_left_out(
    cfg, folder, silence, tmp_path, monkeypatch
):
    bind_scoring(monkeypatch)
    nest(folder, silence, "house/track.flac")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    shutil.copy2(silence, elsewhere / "other.flac")
    (folder / "linked").symlink_to(elsewhere, target_is_directory=True)

    drive(["analyze", "vocals", str(folder), "--recursive"])
    job = vocals_job()
    assert job.payload["skipped_links"] == ["linked"]
    code, resumed = drive(resume_argv(job.job_id))
    assert code == int(ExitCode.OK), resumed
    assert any(w["code"] == "linked-folder-skipped" for w in resumed["warnings"]), resumed


def test_a_one_level_vocals_resume_says_nothing_about_a_walk_it_never_did(
    cfg, folder, silence, monkeypatch
):
    bind_scoring(monkeypatch)
    place(folder, silence, "top")
    drive(["analyze", "vocals", str(folder)])
    code, resumed = drive(resume_argv(vocals_job().job_id))
    assert code == int(ExitCode.OK), resumed
    assert [w["code"] for w in resumed["warnings"]] == []
