"""U69: ``crate intake missing --job JOB``, driven through the real dispatcher.

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
from tests.label_fakes import StrictCatalogue, catalogue_factory
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
        {"artist": "Kite Harbor", "title": "Low Tide Signal"}
    ]


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
