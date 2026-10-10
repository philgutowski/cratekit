"""U129: a set intake is saved as an account playlist and archived when it lands.

Driven through the real dispatcher with the catalogue and account faked. No
live account write is claimed here; the attended backfill over the two October
sets is owed to a sitting.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from cratekit.cli import registry
from cratekit.core import jobs
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.export import set_cli
from cratekit.intake import cli as intake_cli
from cratekit.intake import fetch, land_cli, set_playlist
from cratekit.label import catalogue
from cratekit.modules.outbound import ledger
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.intake import test_workers as workers
from tests.intake.test_set_fetch import URL, FakeFetcher, nothing_left
from tests.intake.test_workers import job_of, recording, three_tracks

# Fixture aliases so pytest finds them from this module.
cfg = workers.cfg
recognised = workers.recognised
from tests.label_fakes import FakeCatalogue, catalogue_factory
from tests.test_intake_missing_search import Hit
from tests.test_label_workers import installed as installed  # noqa: PLC0414
from tests.test_outbound_workers import bind as bind_account

ACCOUNT_GATE = intake_cli.ACCOUNT_GATE
BUILD = "export.set.confirm"
ARCHIVE = "export.archive.confirm"
NAME = "10_10_26 Probe Friday Night Mix 5-26"

# Matches ``three_tracks`` in the worker suite.
ROWS = (
    ("Aurora Bloom", "Sun Path"),
    ("Nova Reef", "Tide"),
    ("Mira Vale", "Glass Hour"),
)
SEARCHES = {
    (artist, title): [Hit(f"tid-{index}", artist, title)]
    for index, (artist, title) in enumerate(ROWS, start=1)
}


class PageWritingFetcher(FakeFetcher):
    """Lands the recording and the info document that names the set."""

    def __init__(self, page: dict) -> None:
        super().__init__()
        self.page = page

    def fetch(self, url: str, directory: Path) -> Path:
        landed = super().fetch(url, directory)
        (directory / f"{landed.stem}{fetch.INFO_SUFFIX}").write_text(
            json.dumps(self.page), encoding="utf-8"
        )
        return landed


@pytest.fixture
def account(installed, monkeypatch):
    fake = FakeCatalogue(searches=dict(SEARCHES))
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    held = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, held)
    return installed, fake, held


def _two_acts(argv: list[str], gate: str, option: str = "apply") -> tuple[int, dict]:
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == gate
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    return drive(["--run", run_id, *argv])


def _page() -> dict:
    return {
        "title": "Probe - Friday Night Mix",
        "uploader": "Probe",
        "upload_date": "20260503",
    }


def _tracklist(cfg, rows=ROWS, name: str = "set.txt") -> Path:
    folder = cfg.library.root.parent / "lists"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    path.write_text("".join(f"{a} - {t}\n" for a, t in rows), encoding="utf-8")
    return path


def test_intake_set_declares_the_account_gate_and_remote_write():
    entry = registry.entry("intake.set")
    assert "remote" in entry.writes
    assert "credential.provider" in entry.doctor_checks
    (spec,) = entry.gates
    assert (spec.name, spec.options, spec.explicit) == (
        ACCOUNT_GATE,
        ("apply", "abort"),
        True,
    )


def test_a_set_intake_plans_and_makes_the_account_playlist(account, recognised, monkeypatch):
    cfg, _fake, held = account
    three_tracks(recognised)
    monkeypatch.setattr(fetch, "fetcher", lambda: PageWritingFetcher(_page()))
    monkeypatch.setattr(set_playlist, "today", lambda: date(2026, 10, 10))

    code, refused = drive(["intake", "set", URL])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == ACCOUNT_GATE
    assert held.created == []
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == (), "the gate must fire before any set is queued"

    code, done = _two_acts(["intake", "set", URL], ACCOUNT_GATE)
    assert code == int(ExitCode.OK), done
    assert nothing_left()
    with jobs.open_store() as store:
        queued = jobs.list_jobs(store)
    assert len(queued) == 1, "plan, approve and resume must queue exactly one set"
    job = job_of(done["data"]["job_id"])
    assert job.job_id == queued[0].job_id
    assert job.payload[intake_cli.PLAYLIST_NAME] == NAME
    assert ledger.set_playlist(cfg, NAME) is not None
    assert held.created == [NAME]
    assert len(held.added) == 3


def test_a_set_with_no_matches_makes_nothing_and_says_so(account, recognised, monkeypatch):
    cfg, fake, held = account
    fake.searches.clear()
    three_tracks(recognised)
    monkeypatch.setattr(fetch, "fetcher", lambda: PageWritingFetcher(_page()))
    monkeypatch.setattr(set_playlist, "today", lambda: date(2026, 10, 10))

    code, done = _two_acts(["intake", "set", URL], ACCOUNT_GATE)
    assert code == int(ExitCode.OK), done
    assert held.created == []
    assert ledger.set_playlist(cfg, NAME) is None
    plan = (done["data"].get("progress") or {}).get("account_playlist") or {}
    assert plan.get("totals", {}).get("writes") is False
    assert plan.get("totals", {}).get("unmatched") == 3
    assert any(w["code"] == "export-tracks-unmatched" for w in done["warnings"])


def test_a_local_set_without_name_words_queues_and_skips_the_account_playlist(
    account, recognised
):
    cfg, _fake, held = account
    three_tracks(recognised)
    path = recording(cfg.library.root)
    code, done = drive(["intake", "set", str(path)])
    assert code == int(ExitCode.OK), done
    assert held.created == []
    assert any(w["code"] == intake_cli.ACCOUNT_UNNAMED for w in done["warnings"])
    assert intake_cli.PLAYLIST_NAME not in job_of(done["data"]["job_id"]).payload


def test_a_rerun_of_export_set_plans_nothing_when_every_matched_track_is_on_it(account):
    cfg, _fake, held = account
    path = _tracklist(cfg)
    code, first = _two_acts(["export", "set", str(path), "--name", NAME], BUILD)
    assert code == int(ExitCode.OK), first
    assert held.created == [NAME]
    created_at = list(held.created)
    code, again = _two_acts(["export", "set", str(path), "--name", NAME], BUILD)
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"
    assert held.created == created_at
    assert again["data"]["totals"]["writes"] is False


def test_export_archive_prefixes_the_set_in_its_year_folder(account):
    cfg, _fake, held = account
    path = _tracklist(cfg)
    assert _two_acts(["export", "set", str(path), "--name", NAME], BUILD)[0] == int(ExitCode.OK)
    xml = cfg.library.root / "landed" / "set-batch_inboxed.xml"
    xml.parent.mkdir(parents=True, exist_ok=True)
    xml.write_bytes(b"<DJ_PLAYLISTS Version='1.0.0'></DJ_PLAYLISTS>\n")
    code, done = _two_acts(["export", "archive", NAME, "--xml", str(xml)], ARCHIVE)
    assert code == int(ExitCode.OK), done
    remote_id = ledger.set_playlist(cfg, NAME).remote_id
    assert any(pid == remote_id and title.startswith("DOWNLOADED ") for pid, title in held.renamed)


def test_frozen_name_agrees_with_inspiration_form():
    words = set_playlist.words_from_page(_page())
    assert set_cli.set_name(set_playlist.playlist_name(words, on=date(2026, 10, 10))) == NAME


def test_plan_archive_named_skips_the_intake_file_check(account):
    cfg, _fake, _held = account
    path = _tracklist(cfg)
    assert _two_acts(["export", "set", str(path), "--name", NAME], BUILD)[0] == int(ExitCode.OK)
    archived = set_cli.plan_archive_named(cfg, NAME, pass_name="set-batch")
    assert archived.writes
    assert archived.planned is not None
    assert archived.planned.to.startswith("DOWNLOADED ")


def _succeeded_set_job(cfg, name: str, *, created: str = "2026-10-09T12:00:00+00:00"):
    """One succeeded set job with the INSPIRATION name frozen on its payload."""
    tracks = {
        f"rc-{index}": {
            "artist": artist,
            "title": title,
            "origin": "text",
            "spelled": f"{artist} - {title}",
        }
        for index, (artist, title) in enumerate(ROWS, start=1)
    }
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=set_playlist.SET_KEY,
            payload={
                intake_cli.SOURCE: "https://example.invalid/a-set",
                intake_cli.TRACKS: tracks,
                intake_cli.CALLS: 3,
                intake_cli.UNREACHED: 0,
                intake_cli.PARTS: 1,
                intake_cli.PAGE: _page(),
                intake_cli.PLAYLIST_NAME: name,
            },
            cfg=cfg,
            item_ids=tuple(tracks),
        )
        # Stamp the queue day so a pre-freeze fallback would still match across days.
        with store.immediate() as conn:
            conn.execute(
                "UPDATE jobs SET created = ?, updated = ? WHERE job_id = ?",
                (created, created, job.job_id),
            )
        jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)
        return jobs.get(store, job.job_id)


def test_intake_land_declares_remote_and_provider_for_the_archive():
    entry = registry.entry("intake.land")
    assert "remote" in entry.writes
    assert "credential.provider" in entry.doctor_checks


def test_export_set_and_archive_declare_library_mounted_for_backfill():
    for name in ("export.set", "export.archive"):
        entry = registry.entry(name)
        assert "library.mounted" in entry.doctor_checks, name


def test_an_abort_on_the_account_gate_queues_the_set_and_writes_no_playlist(
    account, recognised, monkeypatch
):
    cfg, _fake, held = account
    three_tracks(recognised)
    monkeypatch.setattr(fetch, "fetcher", lambda: PageWritingFetcher(_page()))
    monkeypatch.setattr(set_playlist, "today", lambda: date(2026, 10, 10))

    code, refused = drive(["intake", "set", URL])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()

    code, decided = drive(
        ["run", "decide", run_id, ACCOUNT_GATE, "abort", "--actor", "a-person"]
    )
    assert code == int(ExitCode.OK), decided
    code, done = drive(["--run", run_id, "intake", "set", URL])
    assert code == int(ExitCode.OK), done
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == 1
    assert held.created == []
    assert ledger.set_playlist(cfg, NAME) is None
    plan = (done["data"].get("progress") or {}).get("account_playlist") or {}
    assert plan.get("digest")


def test_a_rerun_of_intake_set_plans_nothing_when_the_playlist_already_holds_the_tracks(
    account, recognised, monkeypatch
):
    cfg, _fake, held = account
    three_tracks(recognised)
    monkeypatch.setattr(fetch, "fetcher", lambda: PageWritingFetcher(_page()))
    monkeypatch.setattr(set_playlist, "today", lambda: date(2026, 10, 10))

    code, first = _two_acts(["intake", "set", URL], ACCOUNT_GATE)
    assert code == int(ExitCode.OK), first
    assert held.created == [NAME]
    created_at = list(held.created)

    # A second identification of the same set: the account playlist already
    # holds every matched track, so the plan writes nothing.
    code, again = _two_acts(["intake", "set", URL], ACCOUNT_GATE)
    assert code == int(ExitCode.OK), again
    assert held.created == created_at
    plan = (again["data"].get("progress") or {}).get("account_playlist") or {}
    assert plan.get("totals", {}).get("writes") is False
    with jobs.open_store() as store:
        assert len(jobs.list_jobs(store)) == 2


def test_landing_archive_failure_after_write_is_a_warning(account, monkeypatch):
    cfg, _fake, _held = account
    path = _tracklist(cfg)
    assert _two_acts(["export", "set", str(path), "--name", NAME], BUILD)[0] == int(ExitCode.OK)
    archived = set_cli.plan_archive_named(cfg, NAME, pass_name="set-batch")
    assert archived.writes

    def boom(_cfg, _archived):
        raise refuse(
            "unavailable-transient",
            "the account could not be reached",
            remedy=Remedy.RETRY_LATER,
            origin=("test",),
        )

    monkeypatch.setattr(set_cli, "apply_archive", boom)
    notes = land_cli._apply_landing_archive(cfg, archived)
    assert len(notes) == 1
    assert notes[0]["code"] == land_cli.LAND_ARCHIVE_FAILED
    assert "could not finish after the landing wrote" in notes[0]["message"]


def test_landing_archive_surfaces_changed_since_plan_as_a_warning(account, monkeypatch):
    cfg, _fake, _held = account
    path = _tracklist(cfg)
    assert _two_acts(["export", "set", str(path), "--name", NAME], BUILD)[0] == int(ExitCode.OK)
    archived = set_cli.plan_archive_named(cfg, NAME, pass_name="set-batch")

    def soft(_cfg, _archived):
        return (
            archived.payload,
            [
                {
                    "code": "export-archive-changed-since-plan",
                    "message": f"{NAME} was retitled by somebody, so it was not renamed",
                }
            ],
            False,
        )

    monkeypatch.setattr(set_cli, "apply_archive", soft)
    notes = land_cli._apply_landing_archive(cfg, archived)
    assert [n["code"] for n in notes] == ["export-archive-changed-since-plan"]
    assert "not renamed" in notes[0]["message"]


def test_with_archive_folds_into_the_landing_digest(account):
    cfg, _fake, _held = account
    path = _tracklist(cfg)
    assert _two_acts(["export", "set", str(path), "--name", NAME], BUILD)[0] == int(ExitCode.OK)
    archived = set_cli.plan_archive_named(cfg, NAME, pass_name="set-batch")
    base = {
        "digest": "land-only",
        "items": [{"id": "row", "kind": "track", "action": "add"}],
        "totals": {"count": 1},
    }
    folded = land_cli._with_archive(base, archived)
    assert folded["digest"] != base["digest"]
    assert folded["totals"]["archive_writes"] is True
    assert any(item.get("area") == "account-archive" for item in folded["items"])
    assert land_cli._with_archive(base, None) == base


def test_backfill_lists_the_two_october_sets_from_their_jobs(account, monkeypatch):
    cfg, _fake, held = account
    names = [
        "10_09_26 Public Service NYC Live at Vonking 5-26",
        "10_10_26 Public Service NYC Live at Signal 5-26",
    ]
    _succeeded_set_job(cfg, names[0], created="2026-10-09T15:00:00+00:00")
    _succeeded_set_job(cfg, names[1], created="2026-10-10T15:00:00+00:00")
    monkeypatch.setattr(
        set_cli,
        "_inspiration_playlists",
        lambda _cfg: [(name, f"id-{i}") for i, name in enumerate(names)],
    )
    # Drive the real job lookup; only the tracklist rebuild is stubbed so the
    # gate can show both sets without running the set worker.
    from cratekit.acquire import match

    wanted = tuple(
        match.Wanted(artist=a, title=t, origin=match.TEXT) for a, t in ROWS
    )
    monkeypatch.setattr(set_cli, "_wanted_from_job", lambda _cfg, _job: wanted)

    code, refused = drive(["export", "set"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == BUILD
    message = json.dumps(refused)
    assert names[0] in message and names[1] in message
    assert held.created == []
    # Real lookup found both jobs: no "no-job" soft skips.
    assert "export-set-backfill-no-job" not in message


def test_job_for_inspiration_name_matches_a_set_from_another_day(account, monkeypatch):
    cfg, _fake, _held = account
    # Pre-freeze job: no PLAYLIST_NAME, only the page. Naming day is Oct 9; today
    # is patched to Oct 10 so a today() fallback would miss.
    monkeypatch.setattr(set_playlist, "today", lambda: date(2026, 10, 10))
    name = "10_09_26 Probe Friday Night Mix 5-26"
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=set_playlist.SET_KEY,
            payload={
                intake_cli.SOURCE: "https://example.invalid/a-set",
                intake_cli.TRACKS: {"rc-1": {"artist": "A", "title": "B", "origin": "text"}},
                intake_cli.CALLS: 1,
                intake_cli.UNREACHED: 0,
                intake_cli.PARTS: 1,
                intake_cli.PAGE: _page(),
            },
            cfg=cfg,
            item_ids=("rc-1",),
        )
        with store.immediate() as conn:
            conn.execute(
                "UPDATE jobs SET created = ?, updated = ? WHERE job_id = ?",
                ("2026-10-09T12:00:00+00:00", "2026-10-09T12:00:00+00:00", job.job_id),
            )
        jobs.transition(store, job.job_id, jobs.JobState.SUCCEEDED)
    found = set_cli._job_for_inspiration_name(cfg, name)
    assert found is not None
    assert found.job_id == job.job_id


def test_export_set_backfill_names_playlists_already_made_when_one_fails(
    account, monkeypatch
):
    cfg, _fake, held = account
    names = [
        "10_09_26 Public Service NYC Live at Vonking 5-26",
        "10_10_26 Public Service NYC Live at Signal 5-26",
    ]
    for name, created in zip(
        names, ("2026-10-09T12:00:00+00:00", "2026-10-10T12:00:00+00:00"), strict=True
    ):
        _succeeded_set_job(cfg, name, created=created)
    monkeypatch.setattr(
        set_cli,
        "_inspiration_playlists",
        lambda _cfg: [(name, f"id-{i}") for i, name in enumerate(names)],
    )
    from cratekit.acquire import match

    wanted = tuple(
        match.Wanted(artist=a, title=t, origin=match.TEXT) for a, t in ROWS
    )
    monkeypatch.setattr(set_cli, "_wanted_from_job", lambda _cfg, _job: wanted)

    applied = []
    real_apply = set_cli.apply_planned

    def once(cfg_arg, built):
        if applied:
            raise refuse(
                "unavailable-transient",
                "the account dropped the second write",
                remedy=Remedy.RETRY_LATER,
                origin=("test",),
            )
        data, more, wrote = real_apply(cfg_arg, built)
        if wrote:
            applied.append(built.name)
        return data, more, wrote

    monkeypatch.setattr(set_cli, "apply_planned", once)
    code, refused = drive(["export", "set"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    assert drive(["run", "decide", run_id, BUILD, "apply", "--actor", "a-person"])[0] == int(
        ExitCode.OK
    )
    code, done = drive(["--run", run_id, "export", "set"])
    assert code != int(ExitCode.OK), done
    message = json.dumps(done)
    assert names[0] in message
    assert "already made" in message
    assert held.created == [names[0]]


def test_export_archive_backfill_soft_skips_cratekit_errors(account, monkeypatch):
    cfg, _fake, held = account
    path = _tracklist(cfg)
    assert _two_acts(["export", "set", str(path), "--name", NAME], BUILD)[0] == int(ExitCode.OK)
    xml = cfg.library.root / "landed" / "set-batch_inboxed.xml"
    xml.parent.mkdir(parents=True, exist_ok=True)
    xml.write_bytes(b"<DJ_PLAYLISTS Version='1.0.0'></DJ_PLAYLISTS>\n")

    def boom(_cfg, _name, _xml):
        raise refuse(
            "intake-list-unusable",
            "the intake file is not usable",
            remedy=Remedy.FIX_COMMAND_LINE,
            origin=("test",),
        )

    monkeypatch.setattr(set_cli, "plan_archive", boom)
    monkeypatch.setattr(set_cli, "_proof_for_set", lambda _cfg, _name: xml)
    code, done = _two_acts(["export", "archive"], ARCHIVE)
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert any(w["code"] == "export-archive-backfill-refused" for w in done["warnings"])
    assert NAME in done["warnings"][0]["message"]
    assert held.renamed == []
