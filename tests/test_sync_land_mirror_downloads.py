"""U227: a sync pass takes the download ``crate organize`` queued for an account edit.

Sitting 85: ``crate organize``'s ``mirror-downloads`` step queued a track put
on a mirrored genre playlist on the account, under no run, and the next
``crate sync land`` left that job open ("1 open intake job(s) outside this
pass"), landing the track only because another playlist listed it too. The
pass now takes such a job into a run it started, and drives, lists, downloads
and lands it with its own.

The machine, the account and the stand ins are ``tests/test_sync_land.py``'s:
the pass, its intake jobs, the missing list and the download run through the
real dispatcher and workers, the tail and the landing stand in through the
verb's one seam.
"""

from __future__ import annotations

import pytest

from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from cratekit.organize import mirror_downloads
from tests.acquire_fakes import Landing
from tests.cli_drive import drive
from tests.test_sync_all import _playlist, _tracks, bind_playlists
from tests.test_sync_land import (
    _account,
    _all_jobs,
    _summary,
)
from tests.test_sync_land import (
    machine as machine,  # noqa: PLC0414
)
from tests.test_sync_land import (
    tail as tail,  # noqa: PLC0414
)
from tests.test_sync_land import (
    vocal_model as vocal_model,  # noqa: PLC0414
)

MIRRORED = "pl-jazz-med"


def _mirror_job(monkeypatch, cfg: config.Config, *ids: str) -> jobs.Job:
    """The job ``mirror-downloads`` queues: the account playlist's tracks, frozen, under no run."""
    bind_playlists(monkeypatch, (_playlist(MIRRORED, "Jazz Med"), _tracks(*ids)))
    listing = intake_cli.list_playlist_readable(catalogue.resolve(cfg), MIRRORED)
    with jobs.open_store() as store:
        return intake_cli.queue_playlist(
            store,
            cfg,
            handler_key=mirror_downloads.HANDLER,
            reference=MIRRORED,
            tracks={one: dict(listing.tracks[one]) for one in ids},
            source_id=mirror_downloads.SOURCE_ID,
        )


def _job(job_id: str) -> jobs.Job:
    with jobs.open_store() as store:
        return jobs.get(store, job_id)


def _left_open(envelope: dict) -> list[str]:
    return list(_summary(envelope).get("left_open") or [])


def _said(envelope: dict, step: str) -> list[str]:
    """Every detail the pass gave on one step's rows."""
    cause = envelope.get("cause") or {}
    data = (cause.get("detail") or {}).get("sync_land") or envelope["data"]
    return [row["detail"] for row in data["checks"] if row["key"] == f"sync.land.{step}"]


# ═══════════════════════════════════════════════════════════════════════════
# 1. The pass takes it
# ═══════════════════════════════════════════════════════════════════════════


def test_a_pass_takes_the_open_mirror_download_and_lands_its_track(machine, monkeypatch, tail):
    cfg, script = machine
    script.landings["301"] = Landing()
    queued = _mirror_job(monkeypatch, cfg, "301")
    _account(monkeypatch, script, "101")

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    summary = _summary(envelope)
    taken = _job(queued.job_id)
    assert taken.payload["run_id"] == summary["pass_run"]
    assert taken.payload["source_id"] == mirror_downloads.SOURCE_ID
    assert taken.state is jobs.JobState.SUCCEEDED, "the pass did not drive the mirror job"
    assert summary["mirror_downloads_taken"] == [queued.job_id]
    assert queued.job_id not in _left_open(envelope)
    assert any("took 1 download(s)" in said for said in _said(envelope, "sync"))
    staged = sorted(p.name for p in cfg.paths.download_staging.expanduser().iterdir() if p.is_file())
    assert staged == ["101.wav", "301.wav"]
    assert ("intake", "land") in tail.verbs()


def test_a_track_the_mirror_job_and_another_playlist_both_list_lands_once(
    machine, monkeypatch, tail
):
    cfg, script = machine
    queued = _mirror_job(monkeypatch, cfg, "101")
    _account(monkeypatch, script, "101", "102")

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert _job(queued.job_id).payload["run_id"] == _summary(envelope)["pass_run"]
    staged = sorted(p.name for p in cfg.paths.download_staging.expanduser().iterdir() if p.is_file())
    assert staged == ["101.wav", "102.wav"]
    assert len(script.fetched) == 2, "the track two jobs list was downloaded twice"


def test_a_pass_whose_sync_all_queued_nothing_takes_the_mirror_download(
    machine, monkeypatch, tail
):
    """No new playlist and no earlier pass: the run sync all named is the pass."""
    cfg, script = machine
    script.landings["301"] = Landing()
    queued = _mirror_job(monkeypatch, cfg, "301")
    bind_playlists(monkeypatch)

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    summary = _summary(envelope)
    assert summary["pass_run"] and _job(queued.job_id).payload["run_id"] == summary["pass_run"]
    assert _job(queued.job_id).state is jobs.JobState.SUCCEEDED
    assert _left_open(envelope) == []


# ═══════════════════════════════════════════════════════════════════════════
# 2. What the pass leaves alone
# ═══════════════════════════════════════════════════════════════════════════


def test_a_continued_pass_takes_no_mirror_download_and_names_it(machine, monkeypatch, tail):
    cfg, script = machine
    _account(monkeypatch, script, "101")
    code, earlier = drive(["sync", "all"])
    assert code == int(ExitCode.OK), earlier
    queued = _mirror_job(monkeypatch, cfg, "301")
    _account(monkeypatch, script, "101")

    code, envelope = drive(["sync", "land", "--pass-run", earlier["run_id"]])

    assert "run_id" not in _job(queued.job_id).payload
    assert _job(queued.job_id).state is jobs.JobState.QUEUED
    assert queued.job_id in _left_open(envelope)
    assert "mirror_downloads_taken" not in _summary(envelope)


def test_a_pass_continuing_an_earlier_one_over_nothing_new_takes_none(
    machine, monkeypatch, tail
):
    """Sync all queued nothing and one earlier pass is open: that pass is continued.

    The left open row names the mirror job as the next new pass's, never as
    one queued by hand to drive outside a pass (the review of U227, S12).
    """
    cfg, script = machine
    _account(monkeypatch, script, "101")
    code, earlier = drive(["sync", "all"])
    assert code == int(ExitCode.OK), earlier
    queued = _mirror_job(monkeypatch, cfg, "301")
    _account(monkeypatch, script, "101")

    code, envelope = drive(["sync", "land"])

    assert _summary(envelope)["pass_run"] == earlier["run_id"]
    assert "run_id" not in _job(queued.job_id).payload
    assert queued.job_id in _left_open(envelope)
    (row,) = [said for said in _said(envelope, "left-open") if queued.job_id in said]
    assert "the next new pass takes it: crate sync land" in row
    assert "queued by hand" not in row.split(queued.job_id, 1)[1].split(" | ")[0]


def test_a_hand_queued_playlist_job_and_a_cancelled_mirror_job_are_not_taken(
    machine, monkeypatch, tail
):
    cfg, script = machine
    cancelled = _mirror_job(monkeypatch, cfg, "301")
    with jobs.open_store() as store:
        jobs.cancel(store, cancelled.job_id)
    _account(monkeypatch, script, "101")
    code, by_hand = drive(["intake", "playlist", "pl-a"])
    assert code == int(ExitCode.OK), by_hand
    script.landings["201"] = Landing()
    bind_playlists(
        monkeypatch,
        (_playlist("pl-a", "Warmup"), _tracks("101")),
        (_playlist("pl-b", "Peak"), _tracks("201")),
    )

    code, envelope = drive(["sync", "land"])

    assert "run_id" not in _job(cancelled.job_id).payload
    assert "run_id" not in _job(by_hand["data"]["job_id"]).payload
    assert "mirror_downloads_taken" not in _summary(envelope)


# ═══════════════════════════════════════════════════════════════════════════
# 3. The queue's one write
# ═══════════════════════════════════════════════════════════════════════════


def test_join_run_gives_a_queued_job_with_no_run_the_run_and_nothing_else(machine, monkeypatch):
    cfg, _script = machine
    queued = _mirror_job(monkeypatch, cfg, "301")
    with jobs.open_store() as store:
        joined = jobs.join_run(store, queued.job_id, "run-1")
    assert joined.payload == {**queued.payload, "run_id": "run-1"}
    assert joined.state is jobs.JobState.QUEUED


@pytest.mark.parametrize(
    "why",
    ["has-a-run", "blank"]
    + [str(state) for state in jobs.JobState if state is not jobs.JobState.QUEUED],
)
def test_join_run_refuses_every_other_job(machine, monkeypatch, why):
    """Every state but QUEUED, read off the enum, and a job that carries a run."""
    cfg, _script = machine
    queued = _mirror_job(monkeypatch, cfg, "301")
    run_id = "run-2"
    with jobs.open_store() as store:
        if why == "has-a-run":
            jobs.join_run(store, queued.job_id, "run-1")
        elif why == "blank":
            run_id = "  "
        else:
            store.conn.execute("UPDATE jobs SET state = ? WHERE job_id = ?", (why, queued.job_id))
        before = jobs.get(store, queued.job_id).payload
        with pytest.raises(CratekitError):
            jobs.join_run(store, queued.job_id, run_id)
        assert jobs.get(store, queued.job_id).payload == before


def test_join_run_refuses_a_job_the_queue_does_not_hold(machine):
    with jobs.open_store() as store:
        with pytest.raises(CratekitError) as refused:
            jobs.join_run(store, "no-such-job", "run-1")
    assert refused.value.cause.reason == "job-unknown"
    assert _all_jobs() == []


def test_a_mirror_download_another_library_queued_is_not_taken(machine, monkeypatch, tail):
    """The queue is installation wide: a job of another library is never given this pass's run."""
    import dataclasses

    cfg, script = machine
    elsewhere = dataclasses.replace(
        cfg, library=dataclasses.replace(cfg.library, volume_id="another-library-volume")
    )
    queued = _mirror_job(monkeypatch, elsewhere, "301")
    assert queued.library_id != cfg.library.volume_id
    _account(monkeypatch, script, "101")

    code, envelope = drive(["sync", "land"])

    assert code == int(ExitCode.PENDING_HUMAN), envelope
    assert "run_id" not in _job(queued.job_id).payload
    assert "mirror_downloads_taken" not in _summary(envelope)


def test_a_mirror_download_a_pass_cannot_take_keeps_the_command_that_settles_it(
    machine, monkeypatch, tail
):
    """A blocked mirror job is not the next pass's, so the row names its own command."""
    cfg, script = machine
    queued = _mirror_job(monkeypatch, cfg, "301")
    with jobs.open_store() as store:
        store.conn.execute(
            "UPDATE jobs SET state = ? WHERE job_id = ?", (str(jobs.JobState.BLOCKED), queued.job_id)
        )
    _account(monkeypatch, script, "101")

    code, envelope = drive(["sync", "land"])

    (row,) = [said for said in _said(envelope, "left-open") if queued.job_id in said]
    mine = row.split(queued.job_id, 1)[1].split(" | ")[0]
    assert "queued by hand, drive it with: crate intake playlist" in mine
    assert "the next new pass takes it" not in mine
