"""U129: a set intake is saved as an account playlist and archived when it lands.

Driven through the real dispatcher with the catalogue and account faked. No
live account write is claimed here; the attended backfill over the two October
sets is owed to a sitting.
"""

from __future__ import annotations

import json
import time
from datetime import date
from pathlib import Path

import pytest

from cratekit.acquire import match
from cratekit.cli import registry
from cratekit.core import jobs, secrets
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.export import set_cli
from cratekit.intake import cli as intake_cli
from cratekit.intake import fetch, land_cli, set_playlist
from cratekit.label import catalogue
from cratekit.modules.outbound import ledger
from cratekit.sync import mark_record
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.intake import test_workers as workers
from tests.intake.test_set_fetch import URL, PageWritingFetcher, nothing_left
from tests.intake.test_workers import job_of, recording, three_tracks
from tests.label_fakes import FakeCatalogue, catalogue_factory
from tests.test_intake_missing_search import Hit
from tests.test_label_workers import installed as installed  # noqa: PLC0414
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414
from tests.test_outbound_workers import bind as bind_account

# Fixture aliases so pytest finds them from this module.
cfg = workers.cfg
recognised = workers.recognised

ACCOUNT_GATE = intake_cli.ACCOUNT_GATE
BUILD = "export.set.confirm"
ARCHIVE = "export.archive.confirm"
NAME = "5_03_26 Probe Friday Night Mix 5-26"
BACKFILL = [
    "10_09_26 Public Service NYC Live at Vonking 5-26",
    "10_10_26 Public Service NYC Live at Signal 5-26",
]

# Matches ``three_tracks`` in the worker suite.
ROWS = (("Aurora Bloom", "Sun Path"), ("Nova Reef", "Tide"), ("Mira Vale", "Glass Hour"))
SEARCHES = {
    (artist, title): [Hit(f"tid-{index}", artist, title)]
    for index, (artist, title) in enumerate(ROWS, start=1)
}


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
    return {"title": "Probe - Friday Night Mix", "uploader": "Probe", "upload_date": "20260503"}


def _tracklist(cfg, rows=ROWS, name: str = "set.txt") -> Path:
    folder = cfg.library.root.parent / "lists"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    path.write_text("".join(f"{a} - {t}\n" for a, t in rows), encoding="utf-8")
    return path


def _paged(monkeypatch, recognised, on: date = date(2026, 10, 10)) -> None:
    """A recognised mix whose fetch writes the page, identified on ``on``."""
    three_tracks(recognised)
    monkeypatch.setattr(fetch, "fetcher", lambda: PageWritingFetcher(_page()))
    monkeypatch.setattr(set_playlist, "today", lambda: on)


def _built(cfg, name: str = NAME, list_name: str = "set.txt") -> None:
    """``export set`` over the tracklist under ``name``, approved and applied."""
    path = _tracklist(cfg, name=list_name)
    assert _two_acts(["export", "set", str(path), "--name", name], BUILD)[0] == int(ExitCode.OK)


def _proof(cfg) -> Path:
    """An intake file for the archive to read as the set's proof."""
    xml = cfg.library.root / "landed" / "set-batch_inboxed.xml"
    xml.parent.mkdir(parents=True, exist_ok=True)
    xml.write_bytes(b"<DJ_PLAYLISTS Version='1.0.0'></DJ_PLAYLISTS>\n")
    return xml


def _account_plan(envelope: dict) -> dict:
    return (envelope["data"].get("progress") or {}).get("account_playlist") or {}


def _jobs() -> tuple:
    with jobs.open_store() as store:
        return jobs.list_jobs(store)


def _transient(message: str):
    return refuse("unavailable-transient", message, remedy=Remedy.RETRY_LATER, origin=("test",))


def test_intake_set_declares_the_account_gate_and_remote_write():
    entry = registry.entry("intake.set")
    assert "remote" in entry.writes
    assert "credential.provider" in entry.doctor_checks
    (spec,) = entry.gates
    assert (spec.name, spec.options, spec.explicit) == (ACCOUNT_GATE, ("apply", "abort"), True)
    entry = registry.entry("intake.land")
    assert "remote" in entry.writes
    assert "credential.provider" in entry.doctor_checks
    for name in ("export.set", "export.archive"):
        assert "library.mounted" in registry.entry(name).doctor_checks, name


def test_intake_set_with_all_three_words_freezes_the_page_upload_date(
    account, recognised, monkeypatch
):
    """U136: --dj --set-name --set-date alone must not freeze today's date when
    the page carries upload_date. The Signal set run hit this: early named
    before the fetch, kept early, and landed under 10_12_26."""
    cfg, _fake, held = account
    _paged(monkeypatch, recognised, date(2026, 10, 12))
    words = ["--dj", "Probe", "--set-name", "Friday Night Mix", "--set-date", "2026-05"]
    code, done = _two_acts(["intake", "set", URL, *words], ACCOUNT_GATE)
    assert code == int(ExitCode.OK), done
    job = job_of(done["data"]["job_id"])
    assert job.payload[intake_cli.PLAYLIST_NAME] == NAME
    assert "10_12_26" not in job.payload[intake_cli.PLAYLIST_NAME]
    assert not any(w["code"] == set_playlist.POSTED_FALLBACK for w in done["warnings"])
    assert held.created == [NAME]


def test_a_set_intake_plans_and_makes_the_account_playlist(account, recognised, monkeypatch):
    """And a second identification of the same set plans nothing on it."""
    cfg, _fake, held = account
    _paged(monkeypatch, recognised)
    code, refused = drive(["intake", "set", URL])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == ACCOUNT_GATE
    assert held.created == []
    assert _jobs() == (), "the gate must fire before any set is queued"
    code, done = _two_acts(["intake", "set", URL], ACCOUNT_GATE)
    assert code == int(ExitCode.OK), done
    assert nothing_left()
    queued = _jobs()
    assert len(queued) == 1, "plan, approve and resume must queue exactly one set"
    job = job_of(done["data"]["job_id"])
    assert job.job_id == queued[0].job_id
    assert job.payload[intake_cli.PLAYLIST_NAME] == NAME
    assert ledger.set_playlist(cfg, NAME) is not None
    assert held.created == [NAME]
    assert len(held.added) == 3
    # The account playlist already holds every matched track, so the plan writes nothing.
    code, again = _two_acts(["intake", "set", URL], ACCOUNT_GATE)
    assert code == int(ExitCode.OK), again
    assert held.created == [NAME]
    assert _account_plan(again).get("totals", {}).get("writes") is False
    assert len(_jobs()) == 2


def test_a_set_with_no_matches_makes_nothing_and_says_so(account, recognised, monkeypatch):
    cfg, fake, held = account
    fake.searches.clear()
    _paged(monkeypatch, recognised)
    code, done = _two_acts(["intake", "set", URL], ACCOUNT_GATE)
    assert code == int(ExitCode.OK), done
    assert held.created == []
    assert ledger.set_playlist(cfg, NAME) is None
    plan = _account_plan(done)
    assert plan.get("totals", {}).get("writes") is False
    assert plan.get("totals", {}).get("unmatched") == 3
    assert any(w["code"] == "export-tracks-unmatched" for w in done["warnings"])


def test_a_local_set_without_name_words_queues_and_skips_the_account_playlist(account, recognised):
    """No page and no name flags means the account step was never expected, so
    the skip is silent rather than a ``set-account-unnamed`` warning."""
    cfg, _fake, held = account
    three_tracks(recognised)
    code, done = drive(["intake", "set", str(recording(cfg.library.root))])
    assert code == int(ExitCode.OK), done
    assert held.created == []
    assert intake_cli.ACCOUNT_UNNAMED not in [w["code"] for w in done["warnings"]], (
        "a local set that never asked for a name must not warn set-account-unnamed; "
        "the account playlist step was not expected"
    )
    assert intake_cli.PLAYLIST_NAME not in job_of(done["data"]["job_id"]).payload


def test_a_rerun_of_export_set_plans_nothing_when_every_matched_track_is_on_it(account):
    cfg, _fake, held = account
    path = _tracklist(cfg)
    code, first = _two_acts(["export", "set", str(path), "--name", NAME], BUILD)
    assert code == int(ExitCode.OK), first
    assert held.created == [NAME]
    code, again = _two_acts(["export", "set", str(path), "--name", NAME], BUILD)
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"
    assert held.created == [NAME]
    assert again["data"]["totals"]["writes"] is False


def test_export_archive_takes_the_set_in_its_year_folder(account):
    cfg, _fake, held = account
    _built(cfg)
    code, done = _two_acts(["export", "archive", NAME, "--xml", str(_proof(cfg))], ARCHIVE)
    assert code == int(ExitCode.OK), done
    remote_id = ledger.set_playlist(cfg, NAME).remote_id
    # U242: held as taken, no title written.
    assert held.renamed == [] and remote_id in mark_record.MarkRecord(cfg).taken_ids()


def test_frozen_name_agrees_with_inspiration_form():
    words = set_playlist.words_from_page(_page())
    day, warn = set_playlist.naming_day(page_upload_date=_page()["upload_date"])
    assert warn is None and day == date(2026, 5, 3)
    assert set_cli.set_name(set_playlist.playlist_name(words, on=day)) == NAME


def test_plan_archive_named_skips_the_intake_file_check(account):
    """And the archive it plans folds into the landing's digest."""
    cfg, _fake, _held = account
    _built(cfg)
    archived = set_cli.plan_archive_named(cfg, NAME, pass_name="set-batch")
    assert archived.writes
    assert archived.planned is not None
    assert archived.planned.mark and not archived.planned.taken
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


def _succeeded_set_job(
    cfg, name: str | None, *, created: str = "2026-10-09T12:00:00+00:00", tracks=None
):
    """One succeeded set job with the INSPIRATION name frozen on its payload when given."""
    tracks = tracks or {
        f"rc-{index}": {
            "artist": artist,
            "title": title,
            "origin": "text",
            "spelled": f"{artist} - {title}",
        }
        for index, (artist, title) in enumerate(ROWS, start=1)
    }
    payload = {
        intake_cli.SOURCE: "https://example.invalid/a-set",
        intake_cli.TRACKS: tracks,
        intake_cli.CALLS: len(tracks),
        intake_cli.UNREACHED: 0,
        intake_cli.PARTS: 1,
        intake_cli.PAGE: _page(),
    }
    if name is not None:
        payload[intake_cli.PLAYLIST_NAME] = name
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=set_playlist.SET_KEY,
            payload=payload,
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


@pytest.mark.parametrize("failure", ["transient", "changed"])
def test_landing_archive_failure_after_write_is_a_warning(account, monkeypatch, failure):
    """A raise after the landing wrote is a warning, and so is a not-renamed return."""
    cfg, _fake, _held = account
    _built(cfg)
    archived = set_cli.plan_archive_named(cfg, NAME, pass_name="set-batch")
    assert archived.writes

    def boom(_cfg, _archived):
        raise _transient("the account could not be reached")

    def soft(_cfg, _archived):
        said = f"{NAME} was retitled by somebody, so it was not renamed"
        return archived.payload, [{"code": "export-archive-changed-since-plan", "message": said}], False
    monkeypatch.setattr(set_cli, "apply_archive", boom if failure == "transient" else soft)
    notes = land_cli._apply_landing_archive(cfg, archived)
    if failure == "transient":
        assert len(notes) == 1
        assert notes[0]["code"] == land_cli.LAND_ARCHIVE_FAILED
        assert "could not finish after the landing wrote" in notes[0]["message"]
    else:
        assert [n["code"] for n in notes] == ["export-archive-changed-since-plan"]
        assert "not renamed" in notes[0]["message"]


def test_an_abort_on_the_account_gate_queues_the_set_and_writes_no_playlist(
    account, recognised, monkeypatch
):
    cfg, _fake, held = account
    _paged(monkeypatch, recognised)
    code, refused = drive(["intake", "set", URL])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    assert _jobs() == ()
    code, decided = drive(["run", "decide", run_id, ACCOUNT_GATE, "abort", "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    code, done = drive(["--run", run_id, "intake", "set", URL])
    assert code == int(ExitCode.OK), done
    assert len(_jobs()) == 1
    assert held.created == []
    assert ledger.set_playlist(cfg, NAME) is None
    assert _account_plan(done).get("digest")


ONE_TRACK = {"rc-1": {"artist": "A", "title": "B", "origin": "text"}}


def test_job_for_inspiration_name_matches_a_set_from_another_day(account, monkeypatch):
    cfg, _fake, _held = account
    # Pre-freeze job: no PLAYLIST_NAME, only the page. Posted day is May 3 from
    # upload_date; today is patched to Oct 10 so a today() fallback would miss.
    monkeypatch.setattr(set_playlist, "today", lambda: date(2026, 10, 10))
    job = _succeeded_set_job(cfg, None, tracks=ONE_TRACK)
    found = set_cli._job_for_inspiration_name(cfg, "5_03_26 Probe Friday Night Mix 5-26")
    assert found is not None
    assert found.job_id == job.job_id


def _failing_once(monkeypatch, name: str, raised) -> None:
    """``set_cli.name`` writes its first playlist and raises ``raised`` on the second."""
    applied = []
    real_apply = getattr(set_cli, name)

    def once(cfg_arg, built):
        if applied:
            raise raised
        data, more, wrote = real_apply(cfg_arg, built)
        if wrote:
            applied.append(built.name)
        return data, more, wrote
    monkeypatch.setattr(set_cli, name, once)


def _backfill_refused(verb: str, gate: str) -> tuple[dict, str]:
    """The backfill's two acts, its acting drive refused: the envelope and its text."""
    code, refused = drive(["export", verb])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    assert drive(["run", "decide", run_id, gate, "apply", "--actor", "a-person"])[0] == int(
        ExitCode.OK
    )
    code, done = drive(["--run", run_id, "export", verb])
    assert code != int(ExitCode.OK), done
    return done, json.dumps(done)


def _assert_sign_in_refusal(done: dict, message: str) -> None:
    assert done["cause"]["reason"] == "credential-missing"
    assert done["cause"]["remediation"]["remedy"] == "set-credential"
    assert "internal-error" not in message
    assert "report a defect" not in message.lower()


@pytest.mark.parametrize("credential", [False, True], ids=["transient", "credential"])
def test_export_set_backfill_names_playlists_already_made_when_one_fails(
    account, monkeypatch, credential
):
    """A credential error mid backfill is a sign-in refuse, naming what was made."""
    cfg, _fake, held = account
    for name, created in zip(
        BACKFILL, ("2026-10-09T12:00:00+00:00", "2026-10-10T12:00:00+00:00"), strict=True
    ):
        _succeeded_set_job(cfg, name, created=created)
    monkeypatch.setattr(
        set_cli,
        "_inspiration_playlists",
        lambda _cfg: [(name, f"id-{i}") for i, name in enumerate(BACKFILL)],
    )
    wanted = tuple(match.Wanted(artist=a, title=t, origin=match.TEXT) for a, t in ROWS)
    monkeypatch.setattr(set_cli, "_wanted_from_job", lambda _cfg, _job: wanted)
    raised = (
        secrets.CredentialError("the provider session expired mid backfill")
        if credential
        else _transient("the account dropped the second write")
    )
    _failing_once(monkeypatch, "apply_planned", raised)
    done, message = _backfill_refused("set", BUILD)
    assert BACKFILL[0] in message
    assert "already made" in message
    if credential:
        _assert_sign_in_refusal(done, message)
    assert held.created == [BACKFILL[0]]


def test_export_archive_backfill_soft_skips_cratekit_errors(account, monkeypatch):
    cfg, _fake, held = account
    _built(cfg)
    xml = _proof(cfg)

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


def test_export_archive_backfill_refuses_a_credential_error(account, monkeypatch):
    cfg, _fake, held = account
    _built(cfg)
    xml = _proof(cfg)

    def boom(_cfg, _name, _xml):
        raise secrets.CredentialError("no provider session is recorded")
    monkeypatch.setattr(set_cli, "plan_archive", boom)
    monkeypatch.setattr(set_cli, "_proof_for_set", lambda _cfg, _name: xml)
    # CredentialError is raised while planning, before the gate: the first drive
    # refuses the verb rather than asking for a decision.
    code, done = drive(["export", "archive"])
    assert code != int(ExitCode.OK), done
    message = json.dumps(done)
    assert "CredentialError" in message or "no provider session" in message
    assert "export-archive-backfill-refused" not in message
    assert held.renamed == []


@pytest.mark.parametrize("credential", [False, True], ids=["transient", "credential"])
def test_export_archive_backfill_names_playlists_already_archived_when_one_fails(
    account, monkeypatch, credential
):
    """A CredentialError mid archive backfill is a sign-in refuse, naming what archived."""
    cfg, _fake, held = account
    # Ledger names are sorted: Other comes before Probe under the same day prefix.
    names = ["10_10_26 Other Friday Night Mix 5-26", NAME]
    for name in names:
        _built(cfg, name, f"{name}.txt")
    xml = _proof(cfg)
    monkeypatch.setattr(set_cli, "_proof_for_set", lambda _cfg, _name: xml)
    raised = (
        secrets.CredentialError("the provider session expired mid archive")
        if credential
        else _transient("the account dropped the second archive")
    )
    _failing_once(monkeypatch, "apply_archive", raised)
    done, message = _backfill_refused("archive", ARCHIVE)
    assert names[0] in message
    assert "already archived" in message
    if credential:
        _assert_sign_in_refusal(done, message)
    assert held.renamed == [] and mark_record.MarkRecord(cfg).taken_ids()


def test_job_for_inspiration_name_uses_the_local_day_at_half_past_eleven(account, monkeypatch):
    """A set queued at 23:30 Eastern is that local day, not the next UTC day."""
    cfg, _fake, _held = account
    # MonkeyPatch.context restores TZ, then the outer finally calls tzset so the
    # worker is not left on America/New_York (R-658).
    try:
        with pytest.MonkeyPatch.context() as zone:
            zone.setenv("TZ", "America/New_York")
            time.tzset()
            monkeypatch.setattr(set_playlist, "today", lambda: date(2026, 10, 10))
            # 23:30 Eastern on Oct 9 is 03:30 UTC on Oct 10.
            job = _succeeded_set_job(
                cfg, None, created="2026-10-10T03:30:00+00:00", tracks=ONE_TRACK
            )
            found = set_cli._job_for_inspiration_name(cfg, "10_09_26 Probe Friday Night Mix 5-26")
            assert found is not None
            assert found.job_id == job.job_id
            # A UTC .date() would have looked for 10_10_26 and missed.
            assert set_cli._job_for_inspiration_name(
                cfg, "10_10_26 Probe Friday Night Mix 5-26"
            ) is None
    finally:
        time.tzset()
