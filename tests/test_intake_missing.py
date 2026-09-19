"""U69 and U73: ``crate intake missing --job JOB`` and ``--run RUN``, driven
through the real dispatcher.

A finished playlist intake leaves one committed report per track saying owned,
offered, suppressed or missing. This verb turns the missing ones into the list
document ``acquire download`` reads, through the one emitter U68 landed. The
proofs here are that only missing rows are written, that a job which has not
resolved every track is refused rather than half listed, that a person reading
the DEFAULT output sees the path and the next command, and that the file really
is accepted by the download verb and downloads against the fake adapter.

Every expected value is a literal taken from the fixture hearts, never a value
the verb or the emitter produced. D1 applies: nothing here names a real volume,
a real person or a real track.
"""

from __future__ import annotations

import dataclasses
import io
import json
from pathlib import Path

import pytest

from cratekit import acquire, cli
from cratekit.acquire import cli as acquire_cli
from cratekit.acquire import match_cli
from cratekit.cli import jobs as cli_jobs
from cratekit.cli import registry
from cratekit.core import artifacts, config, jobs
from cratekit.core.cause import Cause, Remediation
from cratekit.core.exit_codes import ExitCode
from cratekit.deletion import stores
from cratekit.deletion.library import RemovedRow
from cratekit.intake import cli as intake_cli
from cratekit.intake import missing_cli
from cratekit.label import catalogue
from tests.acquire_fakes import FAKE_ADAPTER, FAKE_DECLARATION, FakeAdapter, Landing, Script
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedPlaylist, StrictCatalogue, catalogue_factory
from tests.test_config import valid_data

# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library) -> config.Config:
    """A configured machine naming the fake adapter with pacing off, so the
    same configuration serves the intake job and the download that follows."""
    built = config.from_dict(
        valid_data(
            library,
            profile={"name": "full"},
            acquisition={"adapter": FAKE_ADAPTER, "pacing_delay_s": 0.0},
        )
    )
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture(autouse=True)
def fresh_cache():
    intake_cli.reset_cache()
    yield
    intake_cli.reset_cache()


class Track:
    """A provider row in the shape the provider reader reads."""

    def __init__(self, track_id: str, artist: str, name: str, *, version: str = "") -> None:
        self.id = track_id
        self.name = name
        self.artist = {"name": artist}
        self.isrc = ""
        if version:
            self.version = version


def hearts() -> list[Track]:
    return [
        Track("201", "Aurora Bloom", "Sun Path"),
        Track("202", "Nova Reef", "Tide"),
        Track("203", "Mira Vale", "Glass Hour"),
        Track("204", "Lumen Drift", "Salt Road"),
        Track("205", "Kite Harbor", "Low Tide Signal"),
    ]


def owned(library: Path, name: str) -> None:
    (library / "Music" / name).write_bytes(b"")


def mixed_library(library: Path) -> None:
    """Two owned, one offered (a different version is held), two missing."""
    owned(library, "Aurora Bloom - Sun Path.flac")
    owned(library, "Mira Vale - Glass Hour.flac")
    owned(library, "Nova Reef - Tide (Someone Remix).flac")


def queued(monkeypatch, rows: list[Track]) -> str:
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(StrictCatalogue(hearts=rows)))
    code, envelope = drive(["intake", "playlist", "favorites"])
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]["job_id"]


def resume_argv(job_id: str) -> list[str]:
    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def finished(monkeypatch, rows: list[Track]) -> str:
    job_id = queued(monkeypatch, rows)
    code, envelope = drive(resume_argv(job_id))
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "succeeded"
    return job_id


def missing(job_id: str, *extra: str) -> tuple[int, dict]:
    return drive(["intake", "missing", "--job", job_id, *extra])


def human(argv: list[str]) -> tuple[int, str]:
    """The DEFAULT output a person reads. ``drive`` always asks for json, and a
    json only driver has already hidden one blank renderer in this product."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue() + err.getvalue()


def lists_dir(library: Path) -> Path:
    return library.parent / "staging" / missing_cli.LISTS_DIR


def tombstone(cfg: config.Config, artist: str, title: str) -> None:
    """A deletion recorded by the REAL recorder, not an imitation of it."""
    stores.record_tombstone(
        cfg,
        RemovedRow(
            content_id="9001", recorded="2026-09-18", sequence=1, size=None,
            artist=artist, title=title,
        ),
        actor="deletion",
    )


# ═══════════════════════════════════════════════════════════════════════════
# What is listed
# ═══════════════════════════════════════════════════════════════════════════


def test_a_mixed_job_writes_only_the_missing_rows(cfg, library, monkeypatch):
    mixed_library(library)
    job_id = finished(monkeypatch, hearts())

    code, envelope = missing(job_id)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    summary = envelope["data"]["summary"]
    expected = lists_dir(library) / f"intake-{job_id}.list.json"
    assert summary["list"] == str(expected)
    assert (summary["written"], summary["owned"], summary["offered"]) == (2, 2, 1)
    assert (summary["suppressed"], summary["unlisted"]) == (0, 0)
    body = json.loads(expected.read_text())
    assert body["origin"] == "tidal"
    assert [(t["id"], t["artist"], t["title"]) for t in body["tracks"]] == [
        ("204", "Lumen Drift", "Salt Road"),
        ("205", "Kite Harbor", "Low Tide Signal"),
    ]
    sidecar = json.loads(Path(summary["manifest"]).read_text())
    assert set(sidecar["rows"]) == {"204", "205"}
    assert {row["source"] for row in sidecar["rows"].values()} == {"playlist"}
    assert {row["source_ref"] for row in sidecar["rows"].values()} == {"favorites"}


def test_the_default_human_output_names_the_list_and_the_next_command(cfg, library, monkeypatch):
    mixed_library(library)
    job_id = finished(monkeypatch, hearts())

    code, text = human(["intake", "missing", "--job", job_id])

    assert code == int(ExitCode.OK), text
    path = lists_dir(library) / f"intake-{job_id}.list.json"
    assert f"[ok  ] intake.missing.written: 2 missing track(s) written to {path}" in text
    assert f"next: crate acquire download {path}" in text
    assert "intake.missing.offered: 1 offered for review" in text


def test_the_written_list_is_accepted_and_downloaded_by_acquire(cfg, library, monkeypatch):
    mixed_library(library)
    job_id = finished(monkeypatch, hearts())
    _code, envelope = missing(job_id)
    script = Script(landings={"204": Landing(), "205": Landing()})
    monkeypatch.setitem(acquire.ADAPTERS, FAKE_ADAPTER, FAKE_DECLARATION)
    monkeypatch.setattr(FakeAdapter, "script", script)
    monkeypatch.setattr(acquire_cli, "_SLEEP", lambda _seconds: None)

    code, queued_download = drive(["acquire", "download", envelope["data"]["summary"]["list"]])
    assert code == int(ExitCode.OK), queued_download
    download_id = queued_download["data"]["job_id"]
    with jobs.open_store() as store:
        assert [item.item_id for item in jobs.items(store, download_id)] == ["204", "205"]
    code, ran = drive(resume_argv(download_id))

    assert code == int(ExitCode.OK), ran
    assert ran["data"]["state"] == "succeeded"
    assert sorted(request.key for request in script.fetched) == ["204", "205"]


def test_a_second_run_is_the_same_list_and_not_a_refusal(cfg, library, monkeypatch):
    mixed_library(library)
    job_id = finished(monkeypatch, hearts())
    _code, first = missing(job_id)

    code, again = missing(job_id)

    assert code == int(ExitCode.OK), again
    assert again["data"]["summary"]["list"] == first["data"]["summary"]["list"]


def test_out_overrides_the_folder(cfg, library, monkeypatch, tmp_path):
    mixed_library(library)
    job_id = finished(monkeypatch, hearts())

    code, envelope = missing(job_id, "--out", str(tmp_path / "mine"))

    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["list"] == str(tmp_path / "mine" / f"intake-{job_id}.list.json")
    assert not lists_dir(library).exists()


def test_a_job_with_nothing_missing_is_no_op_and_writes_nothing(cfg, library, monkeypatch):
    owned(library, "Aurora Bloom - Sun Path.flac")
    job_id = finished(monkeypatch, [Track("201", "Aurora Bloom", "Sun Path")])

    code, envelope = missing(job_id)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["list"] is None
    assert envelope["data"]["summary"]["next"] is None
    assert not lists_dir(library).exists()


# ═══════════════════════════════════════════════════════════════════════════
# R-504: hearts the provider counts and does not serve
# ═══════════════════════════════════════════════════════════════════════════


class Withholding(StrictCatalogue):
    """The seam answering as the adapter does when its listing came back
    short of the account's declared count: the rows it served, and the count."""

    def __init__(self, rows: list[Track], *, declared: int) -> None:
        super().__init__(hearts=rows)
        self.declared = declared

    def favourite_tracks(self):
        self.heart_listings += 1
        raise catalogue.HeartsShortfall(self.hearts, self.declared)


def withheld(envelope: dict) -> list[dict]:
    return [w for w in envelope["warnings"] if w["code"] == "intake-hearts-withheld"]


def test_a_short_hearts_listing_is_queued_and_says_by_how_much(cfg, library, monkeypatch):
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(Withholding(hearts(), declared=7)))
    code, envelope = drive(["intake", "playlist", "favorites"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert envelope["data"]["progress"]["shortfall"] == {
        "declared": 7,
        "listed": 5,
        "withheld": 2,
    }
    (warning,) = withheld(envelope)
    assert "7 declared, 5 listed, 2 withheld by the provider" in warning["message"]
    with jobs.open_store() as store:
        items = jobs.items(store, envelope["data"]["job_id"])
    assert [item.item_id for item in items] == ["201", "202", "203", "204", "205"]

    # WHAT CAME BACK IS STILL LISTED, through to the missing list.
    mixed_library(library)
    code, done = drive(resume_argv(envelope["data"]["job_id"]))
    assert code == int(ExitCode.OK), done
    code, listed = missing(envelope["data"]["job_id"])
    assert code == int(ExitCode.OK), listed
    assert listed["data"]["summary"]["written"] == 2


def test_the_default_human_output_names_the_shortfall(cfg, library, monkeypatch):
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(Withholding(hearts(), declared=7)))
    code, text = human(["intake", "playlist", "favorites"])
    assert code == int(ExitCode.OK), text
    assert "warning [intake-hearts-withheld]:" in text
    assert "7 declared, 5 listed, 2 withheld by the provider" in text


def test_a_complete_hearts_listing_says_nothing_of_a_shortfall(cfg, library, monkeypatch):
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(StrictCatalogue(hearts=hearts())))
    code, envelope = drive(["intake", "playlist", "favorites"])
    assert code == int(ExitCode.OK), envelope
    assert withheld(envelope) == []
    assert "shortfall" not in envelope["data"]["progress"]


def test_hearts_all_withheld_are_not_read_as_an_account_with_none(cfg, library, monkeypatch):
    """Nothing to queue, and still not the quiet no-op an empty account gets."""
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(Withholding([], declared=3)))
    code, envelope = drive(["intake", "playlist", "favorites"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["progress"]["shortfall"] == {
        "declared": 3,
        "listed": 0,
        "withheld": 3,
    }
    (warning,) = withheld(envelope)
    assert "3 declared, 0 listed, 3 withheld by the provider" in warning["message"]
    with jobs.open_store() as store:
        assert list(jobs.list_jobs(store)) == []


# ═══════════════════════════════════════════════════════════════════════════
# What is refused
# ═══════════════════════════════════════════════════════════════════════════


def test_an_open_job_is_refused_and_nothing_is_written(cfg, library, monkeypatch):
    job_id = queued(monkeypatch, hearts())

    code, envelope = missing(job_id)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "not succeeded" in envelope["cause"]["message"]
    assert "--job" in " ".join(envelope["cause"]["remediation"]["steps"])
    assert not lists_dir(library).exists()


def test_a_failed_job_is_refused_carrying_its_own_cause(cfg, library, monkeypatch):
    job_id = queued(monkeypatch, hearts())
    cause = Cause(
        reason="internal-error", message="stopped for the test",
        remediation=Remediation(steps=("nothing",)), origin=("test",),
    )
    with jobs.open_store() as store:
        jobs.transition(store, job_id, jobs.JobState.FAILED, cause=cause)

    code, envelope = missing(job_id)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["inner"]["message"] == "stopped for the test"
    assert not lists_dir(library).exists()


def test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset(
    cfg, library, monkeypatch
):
    job_id = finished(monkeypatch, hearts())
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        item = jobs.items(store, job_id)[4]
    artifacts.final_path(intake_cli.ARTIFACTS, jobs.frozen_config(job), job_id, item.ordinal).write_text("{")

    code, envelope = missing(job_id)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert "5 item(s) and 4 readable report(s)" in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["unreported"] == ["205"]
    assert not lists_dir(library).exists()


def test_a_report_for_the_wrong_item_refuses_even_when_the_count_matches(cfg, library, monkeypatch):
    """By identifier, not by count: a stray report and a skipped one cancel out."""
    job_id = finished(monkeypatch, hearts())
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        item = jobs.items(store, job_id)[4]
    path = artifacts.final_path(intake_cli.ARTIFACTS, jobs.frozen_config(job), job_id, item.ordinal)
    report = json.loads(path.read_text())
    report["item_id"] = "999"
    path.write_text(json.dumps(report))

    code, envelope = missing(job_id)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["detail"]["unreported"] == ["205"]


def test_a_report_with_a_state_this_verb_cannot_read_refuses(cfg, library, monkeypatch):
    job_id = finished(monkeypatch, hearts())
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        item = jobs.items(store, job_id)[0]
    path = artifacts.final_path(intake_cli.ARTIFACTS, jobs.frozen_config(job), job_id, item.ordinal)
    report = json.loads(path.read_text())
    report["state"] = "needs_review"
    path.write_text(json.dumps(report))

    code, envelope = missing(job_id)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert "'201'" in envelope["cause"]["message"]


def test_a_job_of_another_verb_is_refused(cfg, library):
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key="acquire.download", payload={"list": "x"}, cfg=cfg, item_ids=("1",)
        )

    code, envelope = missing(job.job_id)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "job-unknown"


def test_an_unknown_job_is_refused_by_name(cfg):
    code, envelope = missing("j_nothing")
    assert envelope["cause"]["reason"] == "job-unknown"
    assert code == int(ExitCode.PRECONDITION)


def test_a_file_where_the_folder_should_be_is_refused(cfg, library, monkeypatch, tmp_path):
    mixed_library(library)
    job_id = finished(monkeypatch, hearts())
    (tmp_path / "afile").write_text("x")

    code, envelope = missing(job_id, "--out", str(tmp_path / "afile"))

    assert code == int(ExitCode.PRECONDITION), envelope
    assert "is not a folder" in envelope["cause"]["message"]


def test_a_different_list_already_at_the_path_is_refused_and_left_alone(cfg, library, monkeypatch):
    mixed_library(library)
    job_id = finished(monkeypatch, hearts())
    target = lists_dir(library) / f"intake-{job_id}.list.json"
    target.parent.mkdir(parents=True)
    target.write_text("somebody else's list\n")

    code, envelope = missing(job_id)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert target.read_text() == "somebody else's list\n"


def test_a_missing_row_from_no_provider_is_reported_unlisted_as_a_failing_check(
    cfg, library, monkeypatch
):
    """A recognised track carries no provider id. Its report is edited here to
    stand for any missing row the provider cannot be asked for."""
    job_id = finished(monkeypatch, hearts())
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        item = jobs.items(store, job_id)[4]
    path = artifacts.final_path(intake_cli.ARTIFACTS, jobs.frozen_config(job), job_id, item.ordinal)
    report = json.loads(path.read_text())
    report["track"] = {**report["track"], "origin": "text", "ref": ""}
    path.write_text(json.dumps(report))

    code, text = human(["intake", "missing", "--job", job_id])

    assert code == int(ExitCode.OK), text
    assert "[FAIL] intake.missing.unlisted: 1 missing track(s)" in text
    _code, envelope = missing(job_id)
    assert envelope["data"]["summary"]["unlisted_tracks"] == [
        {
            "artist": "Kite Harbor",
            "title": "Low Tide Signal",
            "isrc": None,
            "why": missing_cli.NO_ISRC,
            "reason": "it carries no ISRC, so the provider cannot be asked for it exactly",
            "in_file": True,
        }
    ]


def test_a_succeeded_job_with_no_items_is_refused_not_listed_empty(cfg, library):
    """The review's first finding, driven: a pre U57 build queued intake jobs with
    no items, and zero reports against zero items passes a comparison by id."""
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key="intake.playlist", payload={"source": "pl-1"}, cfg=cfg, item_ids=()
        )
        jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)

    code, envelope = missing(job.job_id)

    assert code == int(ExitCode.PRECONDITION), envelope
    assert "has no items" in envelope["cause"]["message"]


def test_missing_tracks_none_of_which_can_be_listed_write_the_unlisted_list_not_a_no_op(
    cfg, library, monkeypatch
):
    """The review's second finding of U69, restated by U78. A no-op here would
    read, to a person and to a script, exactly like a job where everything was
    owned. Before U78 it refused; now the track is handed on to a text list, so
    the verb has written something to act on and says so."""
    job_id = finished(monkeypatch, [Track("205", "Kite Harbor", "Low Tide Signal")])
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        item = jobs.items(store, job_id)[0]
    path = artifacts.final_path(intake_cli.ARTIFACTS, jobs.frozen_config(job), job_id, item.ordinal)
    report = json.loads(path.read_text())
    report["track"] = {**report["track"], "origin": "text", "ref": ""}
    path.write_text(json.dumps(report))

    code, envelope = missing(job_id)

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    summary = envelope["data"]["summary"]
    assert (summary["list"], summary["written"], summary["unlisted"]) == (None, 0, 1)
    handed = lists_dir(library) / f"intake-{job_id}.unlisted.json"
    assert summary["unlisted_list"] == str(handed)
    assert summary["unlisted_next"] == f"crate intake missing --list {handed}"
    assert not (lists_dir(library) / f"intake-{job_id}.list.json").exists()
    read = match_cli.read_list(handed)
    assert [(one.artist, one.title) for one in read] == [("Kite Harbor", "Low Tide Signal")]


# ═══════════════════════════════════════════════════════════════════════════
# Tombstones: a deliberately deleted track and the download it would cost
# ═══════════════════════════════════════════════════════════════════════════


def test_a_track_deleted_on_purpose_is_suppressed_and_not_listed(cfg, library, monkeypatch):
    mixed_library(library)
    tombstone(cfg, "Lumen Drift", "Salt Road")
    job_id = finished(monkeypatch, hearts())

    _code, envelope = missing(job_id)

    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["suppressed"]) == (1, 1)
    body = json.loads(Path(summary["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["205"]


def test_a_deleted_track_the_tombstone_consult_cannot_reach_is_listed_as_recorded(
    cfg, library, monkeypatch
):
    """R-431, PINNED SO IT IS SEEN TO CLOSE. The library row kept a featured
    credit the provider never spells, the shape ``UNRECONCILED`` names in
    ``tests/test_match_states.py`` and R-69 records. Before this unit a miss
    here reported plain missing and led nowhere. Now it leads to a download of
    a track somebody deleted. This test failing is the residual closing."""
    tombstone(cfg, "Aurora Bloom", "Sun Path (feat. Mira) (Nightwave Remix)")
    job_id = finished(monkeypatch, [Track("201", "Aurora Bloom", "Sun Path", version="Nightwave Remix")])

    _code, envelope = missing(job_id)

    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["suppressed"]) == (1, 0)
    assert match_cli.TOMBSTONE_STORE == "tombstones"


# ═══════════════════════════════════════════════════════════════════════════
# One sync pass, one list (U73)
#
# ``crate sync all`` queues one intake job per new playlist under one run. The
# jobs here are queued through the same ``queue_playlist`` the pass calls, with
# the run and the source it stamps, and driven through the real worker. The run
# identifier is shaped like a real one, colons and all, because the list's name
# is derived from it and a colon cannot be in a name on an exFAT volume.
# ═══════════════════════════════════════════════════════════════════════════

RUN = "2026-09-18T10:00:00Z-ab12"
RUN_LIST = "2026-09-18T100000Z-ab12_synced.list.json"


def in_run(cfg, reference: str, rows: list[Track], *, run_id: str = RUN) -> str:
    """Queue one playlist job exactly as a sync pass does, and leave it open."""
    tracks = intake_cli.list_playlist(
        FakeCatalogue(playlists={reference: FakePagedPlaylist(rows)}), reference
    )
    with jobs.open_store() as store:
        job = intake_cli.queue_playlist(
            store, cfg, handler_key="intake.playlist", reference=reference,
            tracks=tracks, run_id=run_id, source_id="playlists",
        )
    return job.job_id


def finished_in_run(cfg, reference: str, rows: list[Track], *, run_id: str = RUN) -> str:
    job_id = in_run(cfg, reference, rows, run_id=run_id)
    code, envelope = drive(resume_argv(job_id))
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["state"] == "succeeded"
    return job_id


def fail(job_id: str) -> None:
    cause = Cause(
        reason="internal-error", message="stopped for the test",
        remediation=Remediation(steps=("nothing",)), origin=("test",),
    )
    with jobs.open_store() as store:
        jobs.transition(store, job_id, jobs.JobState.FAILED, cause=cause)


def run_missing(*extra: str, run_id: str = RUN) -> tuple[int, dict]:
    return drive(["intake", "missing", "--run", run_id, *extra])


def test_two_playlists_sharing_a_track_list_it_once_with_both_provenances(cfg, library):
    shared = Track("204", "Lumen Drift", "Salt Road")
    first = finished_in_run(cfg, "pl-a", [Track("205", "Kite Harbor", "Low Tide Signal"), shared])
    second = finished_in_run(cfg, "pl-b", [shared, Track("206", "Sable Cove", "Quiet Pier")])

    code, envelope = run_missing()

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert summary["list"] == str(lists_dir(library) / RUN_LIST)
    assert (summary["run_id"], summary["jobs"], summary["skipped"]) == (RUN, [first, second], [])
    assert summary["land_name"] == "2026-09-18T100000Z-ab12_synced"
    assert (summary["written"], summary["missing"]) == (3, 4)
    body = json.loads(Path(summary["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["205", "204", "206"]
    rows = json.loads(Path(summary["manifest"]).read_text())["rows"]
    assert rows["204"]["source_ref"] == "pl-a"
    assert rows["204"]["source_refs"] == ["pl-a", "pl-b"]
    assert (rows["205"]["source_ref"], rows["206"]["source_ref"]) == ("pl-a", "pl-b")
    assert "source_refs" not in rows["205"] and "source_refs" not in rows["206"]


def test_a_run_list_is_one_file_a_second_listing_reproduces(cfg, library):
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    finished_in_run(cfg, "pl-b", [Track("205", "Kite Harbor", "Low Tide Signal")])
    _code, first = run_missing()

    code, again = run_missing()

    assert code == int(ExitCode.OK), again
    assert again["data"]["summary"]["list"] == first["data"]["summary"]["list"]
    assert sorted(p.name for p in lists_dir(library).iterdir()) == [
        RUN_LIST, RUN_LIST.replace(".list.json", ".manifest.json"),
    ]


def test_the_default_human_output_names_the_list_the_download_and_the_landing(cfg, library):
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])

    code, text = human(["intake", "missing", "--run", RUN])

    assert code == int(ExitCode.OK), text
    path = lists_dir(library) / RUN_LIST
    assert f"next: crate acquire download {path}" in text
    assert "crate intake land --export XML --name 2026-09-18T100000Z-ab12_synced" in text


def test_an_open_job_refuses_the_whole_run_and_names_it(cfg, library):
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    still = in_run(cfg, "pl-b", [Track("205", "Kite Harbor", "Low Tide Signal")])

    code, envelope = run_missing("--skip-failed")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "still open" in envelope["cause"]["message"]
    assert still in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["open"] == [still]
    assert still in " ".join(envelope["cause"]["remediation"]["steps"])
    assert not lists_dir(library).exists()


def test_a_failed_job_is_named_and_refuses_the_run_without_skip_failed(cfg, library):
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    broken = in_run(cfg, "pl-b", [Track("205", "Kite Harbor", "Low Tide Signal")])
    fail(broken)

    code, envelope = run_missing()

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert broken in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["failed"] == [broken]
    assert envelope["cause"]["inner"]["message"] == "stopped for the test"
    assert "--skip-failed" in " ".join(envelope["cause"]["remediation"]["steps"])
    assert not lists_dir(library).exists()


def test_skip_failed_lists_the_rest_and_names_what_it_left_out(cfg, library):
    kept = finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    broken = in_run(cfg, "pl-b", [Track("205", "Kite Harbor", "Low Tide Signal")])
    fail(broken)

    code, envelope = run_missing("--skip-failed")

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["jobs"], summary["skipped"]) == ([kept], [broken])
    body = json.loads(Path(summary["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["204"]
    (skipped,) = [c for c in envelope["data"]["checks"] if c["title"] == "skipped"]
    assert skipped["status"] == "fail"
    assert broken in skipped["detail"] and "pl-b" in skipped["detail"]


def test_skip_failed_over_nothing_missing_refuses_rather_than_a_clean_no_op(cfg, library):
    """The finished job owns everything and the skipped one resolved nothing, so
    a no-op would say the pass needs no download when half of it was never read."""
    owned(library, "Lumen Drift - Salt Road.flac")
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    broken = in_run(cfg, "pl-b", [Track("205", "Kite Harbor", "Low Tide Signal")])
    fail(broken)

    code, envelope = run_missing("--skip-failed")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert broken in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["failed"] == [broken]
    assert not lists_dir(library).exists()


def test_skip_failed_over_tracks_only_handed_on_writes_them_rather_than_refusing(cfg, library):
    """U78's mutation row B4. The finished job's one missing track has no
    provider id and no ISRC, so it is handed on to the text list. That is a file
    to act on, and the pass must not be refused as though nothing was missing."""
    kept = finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    broken = in_run(cfg, "pl-b", [Track("205", "Kite Harbor", "Low Tide Signal")])
    fail(broken)
    with jobs.open_store() as store:
        job = jobs.get(store, kept)
        item = jobs.items(store, kept)[0]
    path = artifacts.final_path(intake_cli.ARTIFACTS, jobs.frozen_config(job), kept, item.ordinal)
    report = json.loads(path.read_text())
    report["track"] = {**report["track"], "origin": "text", "ref": ""}
    path.write_text(json.dumps(report))

    code, envelope = run_missing("--skip-failed")

    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["unlisted"], summary["skipped"]) == (0, 1, [broken])
    assert Path(summary["unlisted_list"]).is_file()


def test_a_run_with_nothing_missing_and_nothing_skipped_is_a_no_op(cfg, library):
    owned(library, "Lumen Drift - Salt Road.flac")
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])

    code, envelope = run_missing()

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["next"] is None
    assert not lists_dir(library).exists()


def test_a_run_whose_every_job_failed_refuses_even_with_skip_failed(cfg, library):
    broken = in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    fail(broken)

    code, envelope = run_missing("--skip-failed")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "nothing to list" in envelope["cause"]["message"]
    assert not lists_dir(library).exists()


def test_an_unknown_run_is_refused_by_name(cfg, library):
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])

    code, envelope = run_missing(run_id="2026-01-01T00:00:00Z-0000")

    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "job-unknown"
    assert "2026-01-01T00:00:00Z-0000" in envelope["cause"]["message"]
    assert not lists_dir(library).exists()


def test_a_blank_run_is_refused_and_does_not_match_a_job_queued_with_no_run(cfg, library):
    code, envelope = run_missing(run_id=" ")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "intake-list-unusable"


def test_another_librarys_job_in_the_same_run_is_not_this_librarys_to_list(cfg, library):
    """The hazard the brief names: the run alone would merge two libraries. The
    other library's job is left OPEN, so a filter on the run alone refuses."""
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    elsewhere = dataclasses.replace(
        cfg, library=dataclasses.replace(cfg.library, volume_id="0000-0000")
    )
    in_run(elsewhere, "pl-b", [Track("205", "Kite Harbor", "Low Tide Signal")])

    code, envelope = run_missing()

    assert code == int(ExitCode.OK), envelope
    body = json.loads(Path(envelope["data"]["summary"]["list"]).read_text())
    assert [t["id"] for t in body["tracks"]] == ["204"]


def test_a_job_of_another_verb_in_the_same_run_is_not_listed(cfg, library):
    """A full pass queues a labels and a favourites job under the same run. Left
    OPEN here, so a selection that took every job in the run refuses the run."""
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    with jobs.open_store() as store:
        jobs.enqueue(
            store, handler_key="sync.labels", payload={"run_id": RUN}, cfg=cfg,
            item_ids=("some-label",),
        )

    code, envelope = run_missing()

    assert code == int(ExitCode.OK), envelope
    assert len(envelope["data"]["summary"]["jobs"]) == 1


def test_a_job_queued_by_hand_is_not_part_of_any_run(cfg, library, monkeypatch):
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    queued(monkeypatch, hearts())

    code, envelope = run_missing()

    assert code == int(ExitCode.OK), envelope
    assert len(envelope["data"]["summary"]["jobs"]) == 1


def test_skip_failed_with_one_job_is_refused_rather_than_ignored(cfg, library, monkeypatch):
    mixed_library(library)
    job_id = finished(monkeypatch, hearts())

    code, envelope = missing(job_id, "--skip-failed")

    assert code == int(ExitCode.PRECONDITION), envelope
    assert "--skip-failed" in envelope["cause"]["message"]
    assert not lists_dir(library).exists()


def test_job_and_run_together_are_refused_by_the_parser(cfg):
    code, _envelope = drive(["intake", "missing", "--job", "j", "--run", RUN])
    assert code != int(ExitCode.OK)


# ═══════════════════════════════════════════════════════════════════════════
# The registry
# ═══════════════════════════════════════════════════════════════════════════


def test_the_entry_is_landed_diagnostic_and_declares_no_write():
    entry = registry.entry("intake.missing")
    assert entry.landed
    assert entry.module == "cratekit.intake.missing_cli"
    assert entry.output_schema == "diagnostic/1"
    assert entry.writes == frozenset()
    assert entry.destructive is False
    assert entry.gates == ()
    assert entry.long_running is False
