"""U69 and U73: ``crate intake missing --job JOB`` and ``--run RUN``, driven
through the real dispatcher: only missing rows are written, a job that has not
resolved every track is refused, and the file downloads against the fake adapter.
Every expected value is a literal from the fixture hearts. D1 applies.
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
from cratekit.core import config, jobs
from cratekit.core.cause import Cause, Remediation
from cratekit.core.exit_codes import ExitCode
from cratekit.deletion import stores
from cratekit.deletion.library import RemovedRow
from cratekit.intake import cli as intake_cli
from cratekit.intake import missing_cli
from cratekit.label import catalogue
from tests._containers import tagged_container
from tests.acquire_fakes import FAKE_ADAPTER, FAKE_DECLARATION, FakeAdapter, Landing, Script
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, FakePagedPlaylist, StrictCatalogue, catalogue_factory
from tests.test_config import valid_data

# Fixtures


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


def ok(job_id: str, *extra: str) -> tuple[dict, dict]:
    code, envelope = missing(job_id, *extra)
    assert code == int(ExitCode.OK), envelope
    return envelope, envelope["data"]["summary"]


def refused(job_id: str, *extra: str) -> dict:
    code, envelope = missing(job_id, *extra)
    assert code == int(ExitCode.PRECONDITION), envelope
    return envelope


def ids(summary: dict) -> list[str]:
    return [t["id"] for t in json.loads(Path(summary["list"]).read_text())["tracks"]]


def mixed_job(library: Path, monkeypatch) -> str:
    mixed_library(library)
    return finished(monkeypatch, hearts())


def edit_report(job_id: str, index: int, change) -> None:
    """Rewrite one committed report of the job through ``change``."""
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        item = jobs.items(store, job_id)[index]
    path = intake_cli.ARTIFACTS.final_path(jobs.frozen_config(job), job_id, item.ordinal)
    report = json.loads(path.read_text())
    change(report)
    path.write_text(json.dumps(report))


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
        RemovedRow(content_id="9001", recorded="2026-09-18", sequence=1, size=None, artist=artist, title=title),
        actor="deletion",
    )


# What is listed


def test_a_mixed_job_writes_only_the_missing_rows(cfg, library, monkeypatch, tmp_path):
    """One job read every way it is listed: refused, elsewhere, here, again, and downloaded."""
    job_id = mixed_job(library, monkeypatch)
    expected = lists_dir(library) / f"intake-{job_id}.list.json"
    # AN UNMOUNTED LIBRARY refuses rather than reading every row missing.
    (library / "Music").rename(library / "Music-away")
    code, envelope = missing(job_id)
    assert envelope["cause"]["reason"] == "library-volume-unmounted", (code, envelope)
    (library / "Music-away").rename(library / "Music")
    # --skip-failed means nothing for one job and is refused rather than ignored.
    envelope = refused(job_id, "--skip-failed")
    assert "--skip-failed" in envelope["cause"]["message"]
    (tmp_path / "afile").write_text("x")
    envelope = refused(job_id, "--out", str(tmp_path / "afile"))
    assert "is not a folder" in envelope["cause"]["message"]
    assert not lists_dir(library).exists()
    envelope = ok(job_id, "--out", str(tmp_path / "mine"))[0]
    assert envelope["data"]["summary"]["list"] == str(tmp_path / "mine" / expected.name)
    assert not lists_dir(library).exists()
    # A FILE THAT IS NOT A LIST at the path is refused, left alone, and given no reason.
    expected.parent.mkdir(parents=True)
    expected.write_text("not a list\n")
    envelope = refused(job_id)
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    steps = " ".join(envelope["cause"]["remediation"]["steps"])
    assert "earlier copy" not in steps
    assert "move the file aside" in steps
    assert expected.read_text() == "not a list\n"
    expected.unlink()
    envelope = ok(job_id)[0]
    assert envelope["outcome"] == "ok"
    summary = envelope["data"]["summary"]
    assert summary["list"] == str(expected)
    assert (summary["written"], summary["owned"], summary["offered"]) == (2, 2, 1)
    assert (summary["suppressed"], summary["unlisted"]) == (0, 0)
    body = json.loads(expected.read_text())
    assert body["origin"] == "tidal"
    assert [(t["id"], t["artist"], t["title"]) for t in body["tracks"]] == [
        ("204", "Lumen Drift", "Salt Road"), ("205", "Kite Harbor", "Low Tide Signal"),
    ]
    sidecar = json.loads(Path(summary["manifest"]).read_text())
    assert set(sidecar["rows"]) == {"204", "205"}
    assert {row["source"] for row in sidecar["rows"].values()} == {"playlist"}
    assert {row["source_ref"] for row in sidecar["rows"].values()} == {"favorites"}
    # A SECOND RUN writes the same BYTES, so the emitter recognises it (R-476).
    paths = [Path(summary[key]) for key in ("list", "manifest")]
    before = [path.read_bytes() for path in paths]
    again, summary = ok(job_id)
    assert summary["list"] == str(expected)
    assert [path.read_bytes() for path in paths] == before
    assert (summary["written"], summary["missing"]) == (2, 2)
    assert (summary["owned_since"], summary["suppressed_since"], summary["offered_since"]) == (0, 0, 0)
    # THE DEFAULT OUTPUT a person reads names the list and the next command.
    code, text = human(["intake", "missing", "--job", job_id])
    assert code == int(ExitCode.OK), text
    assert f"[ok  ] intake.missing.written: 2 missing track(s) written to {expected}" in text
    assert f"next: crate acquire download {expected}" in text
    assert "intake.missing.offered: 1 offered for review" in text
    # AND THE FILE IS ACCEPTED AND DOWNLOADED by acquire.
    script = Script(landings={"204": Landing(), "205": Landing()})
    monkeypatch.setitem(acquire.ADAPTERS, FAKE_ADAPTER, FAKE_DECLARATION)
    monkeypatch.setattr(FakeAdapter, "script", script)
    monkeypatch.setattr(acquire_cli, "_SLEEP", lambda _seconds: None)
    code, queued_download = drive(["acquire", "download", str(expected)])
    assert code == int(ExitCode.OK), queued_download
    download_id = queued_download["data"]["job_id"]
    with jobs.open_store() as store:
        assert [item.item_id for item in jobs.items(store, download_id)] == ["204", "205"]
    code, ran = drive(resume_argv(download_id))
    assert code == int(ExitCode.OK), ran
    assert ran["data"]["state"] == "succeeded"
    assert sorted(request.key for request in script.fetched) == ["204", "205"]


@pytest.mark.parametrize(
    ("name", "tags", "row"),
    [
        # R-664: the title tag carries the ``KEY - BPM - `` head as well as the filename.
        (
            "08A - 124 - Aurora Bloom - Sun Path.flac",
            {"artist": "Aurora Bloom", "title": "08A - 124 - Sun Path"},
            ("201", "Aurora Bloom", "Sun Path", ""),
        ),
        # R-667: the artist tag lists every credit, the row names one, both carry the ISRC.
        (
            "04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac",
            {
                "artist": "Malive, Tito Azevedo, MRQZ",
                "title": "04A - 126 - Burning (Extended Mix)",
                "isrc": "USNRS2644532",
            },
            ("301", "Malive", "Burning (Extended Mix)", "USNRS2644532"),
        ),
        # R-667's second rule: no ISRC tag, held by the primary artist in the credited list.
        (
            "07A - 128 - Traumer, antraum, Anton - Hyaku.flac",
            {"artist": "Traumer, antraum, Anton", "title": "07A - 128 - Hyaku"},
            ("302", "antraum", "Hyaku", "USNRS2644599"),
        ),
    ],
)
def test_a_held_track_is_owned_and_nothing_is_listed(
    cfg, library, tmp_path, monkeypatch, name, tags, row
):
    tagged_container(tmp_path, library / "Music" / name, **tags)
    heart = Track(*row[:3])
    heart.isrc = row[3]
    job_id = finished(monkeypatch, [heart])
    (report,) = intake_cli.ARTIFACTS.committed(cfg, job_id)
    assert report["state"] == "owned", report
    envelope, summary = ok(job_id)
    assert envelope["outcome"] == "no_op"
    assert (summary["written"], summary["owned"], summary["offered"]) == (0, 1, 0)
    assert (summary["list"], summary["next"]) == (None, None)
    assert not (lists_dir(library) / f"intake-{job_id}.list.json").exists()


# R-502: a missing row is asked again at listing time


def test_rows_acquired_since_the_job_are_not_listed_and_name_no_download(
    cfg, library, monkeypatch, tmp_path
):
    """R-502: rows acquired since are asked again; the list's name is fixed by the job."""
    job_id = mixed_job(library, monkeypatch)
    _code, first = missing(job_id)
    listed = Path(first["data"]["summary"]["list"])
    before = listed.read_bytes()
    owned(library, "Lumen Drift - Salt Road.flac")
    # A SHORTER RERUN over the job's earlier list refuses and says why.
    envelope = refused(job_id)
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    steps = " ".join(envelope["cause"]["remediation"]["steps"])
    assert (
        "1 track(s) it names are not in this one, no longer missing since it was "
        "written: Lumen Drift - Salt Road"
    ) in steps
    assert "this one names are not in it" not in steps
    assert listed.read_bytes() == before
    # ONE ROW ACQUIRED leaves the other listed, in a folder of its own.
    envelope, summary = ok(job_id, "--out", str(tmp_path / "fresh"))
    assert (summary["written"], summary["missing"], summary["owned_since"]) == (1, 1, 1)
    assert ids(summary) == ["205"]
    assert set(json.loads(Path(summary["manifest"]).read_text())["rows"]) == {"205"}
    owned(library, "Kite Harbor - Low Tide Signal.flac")
    envelope, summary = ok(job_id)
    assert envelope["outcome"] == "no_op"
    assert (summary["written"], summary["missing"], summary["owned_since"]) == (0, 0, 2)
    assert (summary["owned"], summary["offered"]) == (2, 1), "the job's own answers are kept"
    assert (summary["list"], summary["next"]) == (None, None)
    checks = checks_of(envelope)
    assert "crate acquire download" not in checks["written"]["detail"]
    assert "found missing is in the library" in checks["written"]["detail"], (
        "not the sentence for a job that never had a missing track"
    )
    assert "2 in the library since" in checks["since"]["detail"]
    assert listed.read_bytes() == before, "the earlier list is not this verb's to remove"


def test_a_row_held_in_another_version_since_is_offered_not_listed(
    cfg, library, monkeypatch, tmp_path
):
    job_id = mixed_job(library, monkeypatch)
    remix = library / "Music" / "Lumen Drift - Salt Road (Someone Remix).flac"
    remix.write_bytes(b"")
    envelope, summary = ok(job_id, "--out", str(tmp_path / "remix"))
    assert (summary["written"], summary["offered_since"]) == (1, 1)
    assert ids(summary) == ["205"]
    # A ROW TOMBSTONED SINCE is not listed and is counted suppressed.
    remix.unlink()
    tombstone(cfg, "Kite Harbor", "Low Tide Signal")
    envelope, summary = ok(job_id, "--out", str(tmp_path / "tombstoned"))
    assert (summary["written"], summary["suppressed_since"], summary["suppressed"]) == (1, 1, 0)
    assert ids(summary) == ["204"]


def test_a_row_a_person_answered_as_another_track_stays_listed(cfg, library, monkeypatch):
    """THE ANSWER DECIDES, or the row would drop out of every later list for good."""
    mixed_library(library)
    asked = finished(monkeypatch, [Track("202", "Nova Reef", "Tide")])
    with jobs.open_store() as store:
        (report,) = missing_cli.job_reports(store, jobs.get(store, asked))
    assert report["state"] == "offered"
    code, answered = drive(["review", "resolve", report["review_item"], "--verdict", "rejected"])
    assert code == int(ExitCode.OK), answered
    job_id = finished(monkeypatch, [Track("202", "Nova Reef", "Tide")])
    envelope, summary = ok(job_id)
    assert (summary["written"], summary["missing"], summary["offered_since"]) == (1, 1, 0)
    assert ids(summary) == ["202"]


# R-503: an offered row is listable once a person answers it


def offered_item(job_id: str) -> str:
    """The review item the worker named on the job's one offered report."""
    with jobs.open_store() as store:
        reports = missing_cli.job_reports(store, jobs.get(store, job_id))
    (report,) = [one for one in reports if one["state"] == "offered"]
    return report["review_item"]


def answer(job_id: str, verdict: str) -> None:
    code, answered = drive(["review", "resolve", offered_item(job_id), "--verdict", verdict])
    assert code == int(ExitCode.OK), answered


def checks_of(envelope: dict) -> dict[str, dict]:
    return {check["title"]: check for check in envelope["data"]["checks"]}


def test_an_offered_row_rejected_since_is_listed_and_no_longer_offered(
    cfg, library, monkeypatch, tmp_path
):
    """R-503: a rejection lists the row, and every refusal over an earlier copy says why."""
    job_id = mixed_job(library, monkeypatch)
    _code, first = missing(job_id)
    listed = Path(first["data"]["summary"]["list"])
    before = listed.read_bytes()
    answer(job_id, "rejected")
    # THE NAME IS FIXED BY THE JOB, so a row answered since meets the first bytes.
    envelope = refused(job_id)
    steps = " ".join(envelope["cause"]["remediation"]["steps"])
    assert (
        "1 track(s) this one names are not in it, missing since it was written: Nova Reef - Tide"
    ) in steps
    assert "it names are not in this one" not in steps
    assert listed.read_bytes() == before
    fresh = str(tmp_path / "fresh")
    envelope, summary = ok(job_id, "--out", fresh)
    assert (summary["written"], summary["missing"], summary["offered"]) == (3, 3, 0)
    assert (summary["answered_missing"], summary["answered_owned"]) == (1, 0)
    assert summary["owned"] == 2
    assert ids(summary) == ["202", "204", "205"], "in the playlist's order, not answered rows last"
    checks = checks_of(envelope)
    assert checks["offered"]["detail"].startswith("0 offered for review")
    assert checks["answered"]["detail"].startswith("1 track(s) offered for review")
    assert "asked again now: 1 missing, 0 in the library" in checks["answered"]["detail"]
    # READ FROM THE EARLIER FILE: it names a track this one does not, whatever the job says.
    held = library / "Music" / "Nova Reef - Tide.flac"
    held.write_bytes(b"")
    steps = " ".join(refused(job_id, "--out", fresh)["cause"]["remediation"]["steps"])
    assert (
        "1 track(s) it names are not in this one, no longer missing since it was "
        "written: Nova Reef - Tide"
    ) in steps
    assert "this one names are not in it" not in steps
    held.unlink()
    # A REJECTED ROW UNDER A TOMBSTONE is suppressed, not listed.
    tombstone(cfg, "Nova Reef", "Tide")
    envelope, summary = ok(job_id, "--out", str(tmp_path / "tombstoned"))
    assert (summary["suppressed"], summary["answered_suppressed"], summary["offered"]) == (1, 1, 0)
    assert ids(summary) == ["204", "205"]


def test_an_offered_row_accepted_since_is_owned_and_not_listed(cfg, library, monkeypatch, tmp_path):
    job_id = mixed_job(library, monkeypatch)
    answer(job_id, "accepted")
    envelope, summary = ok(job_id)
    assert (summary["written"], summary["owned"], summary["offered"]) == (2, 3, 0)
    assert (summary["answered_owned"], summary["answered_missing"]) == (1, 0)
    assert ids(summary) == ["204", "205"]
    assert "0 missing, 1 in the library" in checks_of(envelope)["answered"]["detail"]
    # A YES ABOUT A COPY THAT IS GONE stays a question: it does not own another copy.
    held = library / "Music" / "Nova Reef - Tide (Someone Remix).flac"
    held.rename(held.with_name("Nova Reef - Tide (Another Remix).flac"))
    envelope, summary = ok(job_id, "--out", str(tmp_path / "gone"))
    assert (summary["offered"], summary["answered_offered"], summary["written"]) == (1, 1, 2)
    assert summary["owned"] == 2


def test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing(cfg, library, monkeypatch):
    """Nothing is asked again, so the library is not needed and the item is left alone."""
    owned(library, "Nova Reef - Tide (Someone Remix).flac")
    job_id = finished(monkeypatch, [Track("202", "Nova Reef", "Tide")])
    _code, shown = drive(["review", "show", offered_item(job_id)])
    (library / "Music").rename(library / "Music-away")
    envelope = ok(job_id)[0]
    assert envelope["outcome"] == "no_op"
    summary = envelope["data"]["summary"]
    assert (summary["offered"], summary["missing"], summary["written"]) == (1, 0, 0)
    assert sum(summary[key] for key in summary if key.startswith("answered_")) == 0
    assert "then list this again" in checks_of(envelope)["offered"]["detail"]
    assert drive(["review", "show", offered_item(job_id)])[1]["data"] == shown["data"]


def test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it(
    cfg, library, monkeypatch, tmp_path
):
    """A job freezes the configuration it was queued against, and the library's root may move after
    it."""
    job_id = mixed_job(library, monkeypatch)
    moved = tmp_path / "moved"
    library.rename(moved)
    # THE FILE MOVES THE ROOT, NOT THE ENVIRONMENT. The override re-bases a
    # frozen configuration as well as the current one, so a move made through
    # it cannot tell the two apart, which the mutation table measured.
    monkeypatch.delenv(config.ENV_LIBRARY_ROOT)
    config.save(
        config.from_dict(
            valid_data(
                moved,
                profile={"name": "full"},
                acquisition={"adapter": FAKE_ADAPTER, "pacing_delay_s": 0.0},
            )
        )
    )
    config.reset_cache()
    owned(moved, "Lumen Drift - Salt Road.flac")
    owned(moved, "Kite Harbor - Low Tide Signal.flac")
    envelope = ok(job_id)[0]
    assert (envelope["outcome"], envelope["data"]["summary"]["owned_since"]) == ("no_op", 2)


def test_a_job_with_nothing_missing_is_no_op_and_writes_nothing(cfg, library, monkeypatch):
    owned(library, "Aurora Bloom - Sun Path.flac")
    job_id = finished(monkeypatch, [Track("201", "Aurora Bloom", "Sun Path")])
    envelope, summary = ok(job_id)
    assert envelope["outcome"] == "no_op"
    assert (summary["list"], summary["next"]) == (None, None)
    assert not lists_dir(library).exists()
    # AND DOES NOT NEED THE LIBRARY: nothing is asked again.
    (library / "Music").rename(library / "Music-away")
    assert ok(job_id)[0]["outcome"] == "no_op"


# R-504: hearts the provider counts and does not serve


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
    assert envelope["data"]["progress"]["shortfall"] == {"declared": 7, "listed": 5, "withheld": 2}
    (warning,) = withheld(envelope)
    assert "7 declared, 5 listed, 2 withheld by the provider" in warning["message"]
    with jobs.open_store() as store:
        items = jobs.items(store, envelope["data"]["job_id"])
    assert [item.item_id for item in items] == ["201", "202", "203", "204", "205"]
    # WHAT CAME BACK IS STILL LISTED, through to the missing list.
    mixed_library(library)
    code, done = drive(resume_argv(envelope["data"]["job_id"]))
    assert code == int(ExitCode.OK), done
    listed = ok(envelope["data"]["job_id"])[0]
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
    assert envelope["data"]["progress"]["shortfall"] == {"declared": 3, "listed": 0, "withheld": 3}
    (warning,) = withheld(envelope)
    assert "3 declared, 0 listed, 3 withheld by the provider" in warning["message"]
    with jobs.open_store() as store:
        assert list(jobs.list_jobs(store)) == []


# What is refused


def test_an_open_job_is_refused_and_nothing_is_written(cfg, library, monkeypatch):
    job_id = queued(monkeypatch, hearts())
    envelope = refused(job_id)
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
    envelope = refused(job_id)
    assert envelope["cause"]["inner"]["message"] == "stopped for the test"
    assert not lists_dir(library).exists()


def test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset(
    cfg, library, monkeypatch
):
    """Damaged reports refuse the job, by identifier and not by count; a row nothing names is
    reported unlisted as a failing check."""
    job_id = finished(monkeypatch, hearts())
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        found = jobs.items(store, job_id)
    paths = [intake_cli.ARTIFACTS.final_path(jobs.frozen_config(job), job_id, one.ordinal)
             for one in found]
    kept = [path.read_text() for path in paths]
    paths[4].write_text("{")
    envelope = refused(job_id)
    assert "5 item(s) and 4 readable report(s)" in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["unreported"] == ["205"]
    assert not lists_dir(library).exists()
    # A REPORT FOR THE WRONG ITEM: a stray report and a skipped one cancel out by count.
    paths[4].write_text(kept[4])
    edit_report(job_id, 4, lambda report: report.update({"item_id": "999"}))
    assert refused(job_id)["cause"]["detail"]["unreported"] == ["205"]
    paths[4].write_text(kept[4])
    edit_report(job_id, 0, lambda report: report.update({"state": "needs_review"}))
    assert "'201'" in refused(job_id)["cause"]["message"]
    paths[0].write_text(kept[0])
    # A MISSING ROW FROM NO PROVIDER stands for any row the provider cannot be asked for.
    edit_report(job_id, 4, lambda report: report.update(
        {"track": {**report["track"], "origin": "text", "ref": ""}}))
    code, text = human(["intake", "missing", "--job", job_id])
    assert code == int(ExitCode.OK), text
    assert "[FAIL] intake.missing.unlisted: 1 missing track(s)" in text
    _code, envelope = missing(job_id)
    assert envelope["data"]["summary"]["unlisted_tracks"] == [
        {"artist": "Kite Harbor", "title": "Low Tide Signal", "isrc": None, "why": missing_cli.NO_ISRC, "reason": "it carries no ISRC, so the provider cannot be asked for it exactly", "in_file": True}
    ]


def test_a_job_of_another_verb_is_refused(cfg, library):
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key="acquire.download", payload={"list": "x"}, cfg=cfg, item_ids=("1",)
        )
    envelope = refused(job.job_id)
    assert envelope["cause"]["reason"] == "job-unknown"


def test_an_unknown_job_is_refused_by_name(cfg):
    code, envelope = missing("j_nothing")
    assert envelope["cause"]["reason"] == "job-unknown"
    assert code == int(ExitCode.PRECONDITION)


def test_a_succeeded_job_with_no_items_is_refused_not_listed_empty(cfg, library):
    """The review's first finding, driven: a pre U57 build queued intake jobs with
    no items, and zero reports against zero items passes a comparison by id."""
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key="intake.playlist", payload={"source": "pl-1"}, cfg=cfg, item_ids=()
        )
        jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)
    envelope = refused(job.job_id)
    assert "has no items" in envelope["cause"]["message"]


def test_missing_tracks_none_of_which_can_be_listed_write_the_unlisted_list_not_a_no_op(
    cfg, library, monkeypatch
):
    """Nothing nameable is not a no-op: the track is handed on to a text list and said so."""
    job_id = finished(monkeypatch, [Track("205", "Kite Harbor", "Low Tide Signal")])
    edit_report(
        job_id,
        0,
        lambda report: report.update({"track": {**report["track"], "origin": "text", "ref": ""}}),
    )
    envelope = ok(job_id)[0]
    assert envelope["outcome"] == "ok"
    summary = envelope["data"]["summary"]
    assert (summary["list"], summary["written"], summary["unlisted"]) == (None, 0, 1)
    handed = lists_dir(library) / f"intake-{job_id}.unlisted.json"
    assert summary["unlisted_list"] == str(handed)
    assert summary["unlisted_next"] == f"crate intake missing --list {handed}"
    assert not (lists_dir(library) / f"intake-{job_id}.list.json").exists()
    read = match_cli.read_list(handed)
    assert [(one.artist, one.title) for one in read] == [("Kite Harbor", "Low Tide Signal")]


# Tombstones: a deliberately deleted track and the download it would cost


def test_a_track_deleted_on_purpose_is_suppressed_and_not_listed(cfg, library, monkeypatch):
    mixed_library(library)
    tombstone(cfg, "Lumen Drift", "Salt Road")
    job_id = finished(monkeypatch, hearts())
    _code, envelope = missing(job_id)
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["suppressed"]) == (1, 1)
    assert ids(summary) == ["205"]


def test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed(
    cfg, library, monkeypatch
):
    """R-431: a deletion whose row kept a featured credit still suppresses the heart."""
    tombstone(cfg, "Aurora Bloom", "Sun Path (feat. Mira) (Nightwave Remix)")
    job_id = finished(monkeypatch, [Track("201", "Aurora Bloom", "Sun Path", version="Nightwave Remix")])
    _code, envelope = missing(job_id)
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["suppressed"]) == (0, 1)
    assert summary["list"] is None
    assert not (lists_dir(library) / f"intake-{job_id}.list.json").exists()


def test_a_billed_guest_survives_the_freeze_the_worker_resolves_from():
    """THE WORKER DECIDES SUPPRESSED FROM THE THAWED TRACK, not from the row the reader saw."""
    from cratekit.acquire import match
    solo, billed = match.read_tidal_tracks(
        [
            {"id": "1", "title": "Sun Path", "version": "Nightwave Remix",
             "artists": [{"name": "Aurora Bloom"}]},
            {"id": "2", "title": "Sun Path", "version": "Nightwave Remix",
             "artists": [{"name": "Aurora Bloom"}, {"name": "Zed"}]},
        ]
    )
    assert intake_cli.thawed(intake_cli.frozen(solo)).uncredited_spellings
    assert intake_cli.thawed(intake_cli.frozen(billed)).uncredited_spellings == ()
    older = {k: v for k, v in intake_cli.frozen(solo).items() if k != "several_artists"}
    assert intake_cli.thawed(older).uncredited_spellings == ()


def test_a_deleted_credited_row_never_withholds_another_remix_of_the_recording(
    cfg, library, monkeypatch
):
    """The companion names one VERSION. A heart for a different remix of the
    same recording is still missing and still listed, because nobody deleted it."""
    tombstone(cfg, "Aurora Bloom", "Sun Path (feat. Mira) (Nightwave Remix)")
    job_id = finished(monkeypatch, [Track("202", "Aurora Bloom", "Sun Path", version="Daybreak Remix")])
    _code, envelope = missing(job_id)
    summary = envelope["data"]["summary"]
    assert (summary["written"], summary["suppressed"]) == (1, 0)


# One sync pass, one list (U73)
#
# ``crate sync all`` queues one intake job per new playlist under one run. The
# jobs here are queued through the same ``queue_playlist`` the pass calls, with
# the run and the source it stamps, and driven through the real worker. The run
# identifier is shaped like a real one, colons and all, because the list's name
# is derived from it and a colon cannot be in a name on an exFAT volume.

RUN = "2026-09-18T10:00:00Z-ab12"
RUN_LIST = "2026-09-18T100000Z-ab12_synced.list.json"


def in_run(cfg, reference: str, rows: list[Track], *, run_id: str = RUN) -> str:
    """Queue one playlist job exactly as a sync pass does, and leave it open."""
    tracks = intake_cli.list_playlist(
        FakeCatalogue(playlists={reference: FakePagedPlaylist(rows)}), reference
    )
    with jobs.open_store() as store:
        job = intake_cli.queue_playlist(store, cfg, handler_key="intake.playlist", reference=reference, tracks=tracks, run_id=run_id, source_id="playlists")
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


def run_ok(*extra: str, run_id: str = RUN) -> tuple[dict, dict]:
    code, envelope = run_missing(*extra, run_id=run_id)
    assert code == int(ExitCode.OK), envelope
    return envelope, envelope["data"]["summary"]


def run_refused(*extra: str, run_id: str = RUN) -> dict:
    code, envelope = run_missing(*extra, run_id=run_id)
    assert code == int(ExitCode.PRECONDITION), envelope
    return envelope


def test_two_playlists_sharing_a_track_list_it_once_with_both_provenances(cfg, library, tmp_path):
    """One list per pass, reproduced by a second listing, and asked again row by row."""
    shared = Track("204", "Lumen Drift", "Salt Road")
    first = finished_in_run(cfg, "pl-a", [Track("205", "Kite Harbor", "Low Tide Signal"), shared])
    second = finished_in_run(cfg, "pl-b", [shared, Track("206", "Sable Cove", "Quiet Pier")])
    _code, earlier = run_missing()
    envelope, summary = run_ok()
    assert summary["list"] == earlier["data"]["summary"]["list"] == str(lists_dir(library) / RUN_LIST)
    assert sorted(p.name for p in lists_dir(library).iterdir()) == [
        RUN_LIST, RUN_LIST.replace(".list.json", ".manifest.json"),
    ]
    assert (summary["run_id"], summary["jobs"], summary["skipped"]) == (RUN, [first, second], [])
    assert summary["land_name"] == "2026-09-18T100000Z-ab12_synced"
    assert (summary["written"], summary["missing"]) == (3, 4)
    assert ids(summary) == ["205", "204", "206"]
    rows = json.loads(Path(summary["manifest"]).read_text())["rows"]
    assert rows["204"]["source_ref"] == "pl-a"
    assert rows["204"]["source_refs"] == ["pl-a", "pl-b"]
    assert (rows["205"]["source_ref"], rows["206"]["source_ref"]) == ("pl-a", "pl-b")
    assert "source_refs" not in rows["205"] and "source_refs" not in rows["206"]
    code, text = human(["intake", "missing", "--run", RUN])
    assert code == int(ExitCode.OK), text
    assert f"next: crate acquire download {lists_dir(library) / RUN_LIST}" in text
    # R-770: the hint names the batch and which medium wants the export. ``--pass``,
    # never ``--name`` (U110): the run names the intake file sync mark reads.
    assert "crate intake land --pass 2026-09-18T100000Z-ab12_synced" in text
    assert "--name" not in text
    assert "adding --export XML" in text and "while the intake tree is on the xml bridge" in text
    assert "no export once the intake tree is database native" in text
    assert "crate intake land --export" not in text
    # R-502 over ``--run``: the shared track was acquired, so it drops from both.
    owned(library, "Lumen Drift - Salt Road.flac")
    tombstone(cfg, "Sable Cove", "Quiet Pier")
    envelope, summary = run_ok("--out", str(tmp_path / "later"))
    assert (summary["written"], summary["missing"]) == (1, 1)
    assert (summary["owned_since"], summary["suppressed_since"]) == (2, 1)
    assert ids(summary) == ["205"]
    assert "land what it downloads" in checks_of(envelope)["written"]["detail"]


def test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does(cfg, library):
    """R-503 over ``--run``: the same lookup, per row, across every job."""
    mixed_library(library)
    asked = finished_in_run(cfg, "pl-a", [Track("202", "Nova Reef", "Tide")])
    finished_in_run(cfg, "pl-b", [Track("205", "Kite Harbor", "Low Tide Signal")])
    answer(asked, "rejected")
    envelope, summary = run_ok()
    assert (summary["written"], summary["offered"], summary["answered_missing"]) == (2, 0, 1)
    assert ids(summary) == ["202", "205"]


def test_a_run_whose_rows_were_all_acquired_since_names_no_download(cfg, library):
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    owned(library, "Lumen Drift - Salt Road.flac")
    envelope = run_ok()[0]
    assert envelope["outcome"] == "no_op"
    assert (envelope["data"]["summary"]["next"], envelope["data"]["summary"]["owned_since"]) == (None, 1)


def test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest(
    cfg, library, monkeypatch, tmp_path
):
    """An unknown run, an open job, a failed one, --skip-failed, and the jobs no run owns."""
    kept = finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    code, envelope = run_missing(run_id="2026-01-01T00:00:00Z-0000")
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "job-unknown"
    assert "2026-01-01T00:00:00Z-0000" in envelope["cause"]["message"]
    # ONE OPEN JOB REFUSES THE WHOLE RUN, --skip-failed or not.
    broken = in_run(cfg, "pl-b", [Track("205", "Kite Harbor", "Low Tide Signal")])
    envelope = run_refused("--skip-failed")
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "still open" in envelope["cause"]["message"]
    assert broken in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["open"] == [broken]
    assert broken in " ".join(envelope["cause"]["remediation"]["steps"])
    # A FAILED JOB is named and refuses the run without --skip-failed.
    fail(broken)
    envelope = run_refused()
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert broken in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["failed"] == [broken]
    assert envelope["cause"]["inner"]["message"] == "stopped for the test"
    assert "--skip-failed" in " ".join(envelope["cause"]["remediation"]["steps"])
    assert not lists_dir(library).exists()
    envelope, summary = run_ok("--skip-failed")
    assert (summary["jobs"], summary["skipped"]) == ([kept], [broken])
    assert ids(summary) == ["204"]
    (skipped,) = [c for c in envelope["data"]["checks"] if c["title"] == "skipped"]
    assert skipped["status"] == "fail"
    assert broken in skipped["detail"] and "pl-b" in skipped["detail"]
    # JOBS NO RUN OF THIS LIBRARY OWNS are left OPEN, so a selection that took one refuses:
    # another library's job in the run, another verb's, and one queued by hand.
    elsewhere = dataclasses.replace(
        cfg, library=dataclasses.replace(cfg.library, volume_id="0000-0000")
    )
    in_run(elsewhere, "pl-c", [Track("206", "Sable Cove", "Quiet Pier")])
    with jobs.open_store() as store:
        jobs.enqueue(
            store, handler_key="sync.labels", payload={"run_id": RUN}, cfg=cfg,
            item_ids=("some-label",),
        )
    queued(monkeypatch, hearts())
    envelope, summary = run_ok("--skip-failed")
    assert (summary["jobs"], ids(summary)) == ([kept], ["204"])
    # TRACKS ONLY HANDED ON are written to the text list rather than refused.
    edit_report(kept, 0, lambda report: report.update(
        {"track": {**report["track"], "origin": "text", "ref": ""}}))
    envelope, summary = run_ok("--skip-failed", "--out", str(tmp_path / "handed"))
    assert (summary["written"], summary["unlisted"], summary["skipped"]) == (0, 1, [broken])
    assert Path(summary["unlisted_list"]).is_file()


def test_skip_failed_over_nothing_missing_refuses_rather_than_a_clean_no_op(cfg, library):
    """The finished job owns everything and the skipped one resolved nothing, so
    a no-op would say the pass needs no download when half of it was never read."""
    owned(library, "Lumen Drift - Salt Road.flac")
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    broken = in_run(cfg, "pl-b", [Track("205", "Kite Harbor", "Low Tide Signal")])
    fail(broken)
    envelope = run_refused("--skip-failed")
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert broken in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["failed"] == [broken]
    assert not lists_dir(library).exists()


def test_a_run_with_nothing_missing_and_nothing_skipped_is_a_no_op(cfg, library):
    owned(library, "Lumen Drift - Salt Road.flac")
    finished_in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    envelope = run_ok()[0]
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["summary"]["next"] is None
    assert not lists_dir(library).exists()


def test_a_run_whose_every_job_failed_refuses_even_with_skip_failed(cfg, library):
    broken = in_run(cfg, "pl-a", [Track("204", "Lumen Drift", "Salt Road")])
    fail(broken)
    envelope = run_refused("--skip-failed")
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "nothing to list" in envelope["cause"]["message"]
    assert not lists_dir(library).exists()


def test_a_blank_run_is_refused_and_does_not_match_a_job_queued_with_no_run(cfg, library):
    envelope = run_refused(run_id=" ")
    assert envelope["cause"]["reason"] == "intake-list-unusable"


def test_job_and_run_together_are_refused_by_the_parser(cfg):
    code, _envelope = drive(["intake", "missing", "--job", "j", "--run", RUN])
    assert code != int(ExitCode.OK)


# The registry


def test_the_entry_is_landed_diagnostic_and_declares_no_write():
    entry = registry.entry("intake.missing")
    assert entry.landed
    assert entry.module == "cratekit.intake.missing_cli"
    assert entry.output_schema == "diagnostic/1"
    assert entry.writes == frozenset()
    assert entry.destructive is False
    assert entry.gates == ()
    assert entry.long_running is False


# R-515: a playlist the provider counts tracks on and does not serve

SHORT = "pl-short"


def eight() -> list[Track]:
    return [Track(str(300 + n), f"Act {n}", f"Title {n}") for n in range(1, 9)]


def playlist_withheld(envelope: dict) -> list[dict]:
    return [w for w in envelope["warnings"] if w["code"] == "intake-playlist-withheld"]


def bind_playlist(monkeypatch, rows: list[Track], *, declared: int | None) -> None:
    fake = FakeCatalogue(playlists={SHORT: FakePagedPlaylist(rows, declared=declared)})
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))


def test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns(
    cfg, library, monkeypatch
):
    bind_playlist(monkeypatch, eight(), declared=10)
    code, envelope = drive(["intake", "playlist", SHORT])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    with jobs.open_store() as store:
        items = jobs.items(store, envelope["data"]["job_id"])
    assert len(items) == 8
    assert envelope["data"]["progress"]["shortfall"] == {"declared": 10, "listed": 8, "withheld": 2}
    (warning,) = playlist_withheld(envelope)
    assert "10 declared, 8 listed, 2 withheld by the provider" in warning["message"]
    assert repr(SHORT) in warning["message"]


@pytest.mark.parametrize("declared", [8, None])
def test_a_full_playlist_listing_or_one_with_no_declared_count_warns_nothing(
    cfg, library, monkeypatch, declared
):
    bind_playlist(monkeypatch, eight(), declared=declared)
    code, envelope = drive(["intake", "playlist", SHORT])
    assert code == int(ExitCode.OK), envelope
    assert playlist_withheld(envelope) == []
    assert "shortfall" not in envelope["data"]["progress"]


def test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op(cfg, library, monkeypatch):
    bind_playlist(monkeypatch, [], declared=3)
    code, envelope = drive(["intake", "playlist", SHORT])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["progress"]["shortfall"] == {"declared": 3, "listed": 0, "withheld": 3}
    assert len(playlist_withheld(envelope)) == 1


def test_the_default_human_output_names_the_playlist_shortfall(cfg, library, monkeypatch):
    bind_playlist(monkeypatch, eight(), declared=10)
    code, text = human(["intake", "playlist", SHORT])
    assert code == int(ExitCode.OK), text
    assert "warning [intake-playlist-withheld]:" in text
    assert "10 declared, 8 listed, 2 withheld by the provider" in text
