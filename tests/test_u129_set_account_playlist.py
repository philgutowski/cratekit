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
from cratekit.core.exit_codes import ExitCode
from cratekit.export import set_cli
from cratekit.intake import cli as intake_cli
from cratekit.intake import fetch, set_playlist
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

    code, done = _two_acts(["intake", "set", URL], ACCOUNT_GATE)
    assert code == int(ExitCode.OK), done
    assert nothing_left()
    job = job_of(done["data"]["job_id"])
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


def test_backfill_lists_inspiration_playlists_without_an_account_playlist(
    account, monkeypatch
):
    cfg, _fake, held = account
    # Two inspiration names, neither on the account ledger yet.
    names = [
        "10_09_26 Public Service NYC Live at Vonking 5-26",
        "10_10_26 Public Service NYC Live at Signal 5-26",
    ]
    monkeypatch.setattr(
        set_cli, "_inspiration_playlists", lambda _cfg: [(name, f"id-{i}") for i, name in enumerate(names)]
    )
    monkeypatch.setattr(set_cli, "_job_for_inspiration_name", lambda _cfg, _name: None)
    code, refused = drive(["export", "set"])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == BUILD
    # The gate screen names both October sets.
    message = json.dumps(refused)
    assert names[0] in message and names[1] in message
    assert held.created == []
