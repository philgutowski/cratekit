"""R-837: a set becomes a private playlist on the account, and is archived.

Every scenario the brief names is here, driven through the real dispatcher with
the two provider seams faked: the catalogue, whose text search names a typed
row's track, and the streaming account, which records every call. The set
written and archived on the author's account is owed to an attended sitting and
is not claimed here.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from cratekit.cli import registry
from cratekit.core.exit_codes import ExitCode
from cratekit.export import set_cli
from cratekit.label import catalogue
from cratekit.label.catalogue import AccountPlaylist
from cratekit.modules.outbound import ledger, sets
from cratekit.sync import mark_record
from cratekit.sync import playlists as sync_playlists
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, UnreadableCatalogue, catalogue_factory
from tests.test_intake_missing_search import Hit
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture
from tests.test_outbound_workers import bind as bind_account

BUILD = "export.set.confirm"
ARCHIVE = "export.archive.confirm"
NAME = "Warehouse Night"

#: Five rows. The provider's search names four exactly and nothing for the fifth.
ROWS = (
    ("Artist One", "Title One"),
    ("Artist Two", "Title Two"),
    ("Artist Three", "Title Three"),
    ("Artist Four", "Title Four"),
    ("Artist Five", "Title Five"),
)
SEARCHES = {
    (artist, title): [Hit(f"tid-{index}", artist, title)]
    for index, (artist, title) in enumerate(ROWS[:4], start=1)
}


@pytest.fixture
def account(installed, monkeypatch):
    """A catalogue that can search, and an account that records every call."""
    fake = FakeCatalogue(searches=dict(SEARCHES))
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(fake))
    held = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, held)
    return installed, fake, held


def _tracklist(cfg, rows=ROWS, name: str = f"{NAME}.txt") -> Path:
    folder = cfg.library.root.parent / "lists"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    path.write_text("".join(f"{a} - {t}\n" for a, t in rows), encoding="utf-8")
    return path


def _two_acts(argv: list[str], gate: str, option: str = "apply") -> tuple[int, dict]:
    """R34's two acts on an explicit gate, then the run that carries them out."""
    code, refused = drive(argv)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["detail"]["gate"] == gate
    run_id = refused["run_id"]
    code, decided = drive(["run", "decide", run_id, gate, option, "--actor", "a-person"])
    assert code == int(ExitCode.OK), decided
    return drive(["--run", run_id, *argv])


def _build(path: Path, option: str = "apply", *extra: str) -> tuple[int, dict]:
    return _two_acts(["export", "set", str(path), *extra], BUILD, option)


def _landed(cfg, name: str = "set-batch") -> Path:
    folder = cfg.library.root / "landed"
    folder.mkdir(parents=True, exist_ok=True)
    xml = folder / f"{name}_inboxed.xml"
    xml.write_bytes(b"<DJ_PLAYLISTS Version='1.0.0'></DJ_PLAYLISTS>\n")
    return xml


def _archive(xml: Path, option: str = "apply", name: str = NAME) -> tuple[int, dict]:
    return _two_acts(["export", "archive", name, "--xml", str(xml)], ARCHIVE, option)


def _tracks(done: dict) -> list[dict]:
    return [item for item in done["data"]["items"] if item["kind"] == "track"]


# ═══════════════════════════════════════════════════════════════════════════
# 1. The declaration
# ═══════════════════════════════════════════════════════════════════════════


def test_both_verbs_write_only_the_account_behind_an_explicit_gate():
    for name, gate in (("export.set", BUILD), ("export.archive", ARCHIVE)):
        entry = registry.entry(name)
        assert entry.writes == frozenset({"remote"}), name
        assert entry.module_id == "export" and entry.feature_rows == (36,)
        (spec,) = entry.gates
        assert (spec.name, spec.options, spec.explicit) == (gate, ("apply", "abort"), True)
        assert spec.digest_source == "plan"
    assert registry.entry("export.archive").destructive
    assert not registry.entry("export.set").destructive


def test_a_tracklist_name_gives_the_playlist_name_without_its_digest_or_slash():
    assert set_cli.name_of(Path("Night a/b-0123456789ab.tracklist.txt")) == "b"
    assert set_cli.name_of(Path("Club-Night-0123456789ab.tracklist.txt")) == "Club-Night"
    assert set_cli.name_of(Path("typed set.txt")) == "typed set"


# ═══════════════════════════════════════════════════════════════════════════
# 2. The set playlist
# ═══════════════════════════════════════════════════════════════════════════


def test_five_rows_with_one_unmatched_plan_four_and_name_the_fifth(account):
    cfg, _fake, held = account
    code, refused = drive(["export", "set", str(_tracklist(cfg))])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    assert held.created == [] and held.added == []
    code, done = _build(_tracklist(cfg), "abort")
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op" and held.created == []
    rows = _tracks(done)
    assert [row["action"] for row in rows] == ["add"] * 4 + ["unmatched"]
    fifth = rows[4]
    assert (fifth["artist"], fifth["title"]) == ("Artist Five", "Title Five")
    assert fifth["why"] == "the provider's search returned nothing for it"
    assert done["data"]["totals"]["add"] == 4 and done["data"]["totals"]["unmatched"] == 1
    (warning,) = [w for w in done["warnings"] if w["code"] == "export-tracks-unmatched"]
    assert "Artist Five - Title Five: the provider's search returned nothing" in warning["message"]


def test_approved_the_account_holds_a_private_playlist_of_four_in_order(account):
    cfg, _fake, held = account
    code, done = _build(_tracklist(cfg))
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "ok"
    assert held.created == [NAME]
    (playlist,) = held.playlists
    assert playlist in held.private
    assert held.playlists[playlist] == ["tid-1", "tid-2", "tid-3", "tid-4"]
    recorded = ledger.set_playlist(cfg, NAME)
    assert recorded is not None and recorded.remote_id == playlist
    assert recorded.added == frozenset({"tid-1", "tid-2", "tid-3", "tid-4"})
    # The answer names the fifth on the run that wrote, too (R-850).
    assert any(w["code"] == "export-tracks-unmatched" for w in done["warnings"])


def test_a_second_run_onto_the_same_set_plans_nothing(account):
    cfg, _fake, held = account
    path = _tracklist(cfg)
    assert _build(path)[0] == int(ExitCode.OK)
    held.chunks.clear()
    code, done = _build(path)
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert done["data"]["totals"]["writes"] is False
    assert held.created == [NAME] and held.chunks == []
    assert [row["action"] for row in _tracks(done)] == ["already"] * 4 + ["unmatched"]


def test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist(account):
    cfg, fake, held = account
    assert _build(_tracklist(cfg))[0] == int(ExitCode.OK)
    fake.searches[("Artist Five", "Title Five")] = [Hit("tid-5", "Artist Five", "Title Five")]
    code, done = _build(_tracklist(cfg))
    assert code == int(ExitCode.OK), done
    assert held.created == [NAME]
    (playlist,) = held.playlists
    assert held.playlists[playlist][-1] == "tid-5"


def test_a_set_with_nothing_matched_makes_no_empty_playlist(account):
    cfg, _fake, held = account
    path = _tracklist(cfg, rows=(("Nobody", "Nothing"),), name="empty.txt")
    code, done = _build(path)
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op" and held.created == []
    assert ledger.set_playlist(cfg, "empty") is None


def test_a_search_the_provider_cannot_answer_refuses_before_the_gate(installed, monkeypatch):
    monkeypatch.setattr(catalogue, "resolve", catalogue_factory(UnreadableCatalogue()))
    held = outbound_fakes.StrictAccount()
    bind_account(monkeypatch, held)
    code, refused = drive(["export", "set", str(_tracklist(installed))])
    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == "unavailable-transient"
    assert held.created == []


def test_two_exact_candidates_are_not_chosen_between(account):
    cfg, fake, held = account
    fake.searches[("Artist Five", "Title Five")] = [
        Hit("tid-5a", "Artist Five", "Title Five"),
        Hit("tid-5b", "Artist Five", "Title Five"),
    ]
    code, done = _build(_tracklist(cfg), "abort")
    assert code == int(ExitCode.OK), done
    fifth = _tracks(done)[4]
    assert fifth["action"] == "unmatched" and "no single exact match" in fifth["why"]


def test_the_sweep_never_reads_a_set_playlist_as_intake(account, monkeypatch):
    from types import SimpleNamespace

    from cratekit.sync import cli as sync_cli

    cfg, _fake, _held = account
    assert _build(_tracklist(cfg))[0] == int(ExitCode.OK)
    built = ledger.set_playlist_ids(cfg)
    assert len(built) == 1
    (playlist_id,) = built
    listed = AccountPlaylist(playlist_id=playlist_id, name=NAME, tracks=4)
    assert (
        sync_playlists.exclusion(listed, recorded=set(), in_flight=set(), set_built=built)
        is sync_playlists.Excluded.SET_PLAYLIST
    )
    handed: list[frozenset[str]] = []

    class Stop(Exception):
        pass

    def plan(store, cfg_, found, *, handler_key, label_built=frozenset(), set_built=frozenset()):
        handed.append(set_built)
        raise Stop

    monkeypatch.setattr(sync_playlists, "plan", plan)
    with pytest.raises(Stop):
        sync_cli._plan_playlists(SimpleNamespace(handler_key="intake.playlist"), None)
    assert handed == [built]


# ═══════════════════════════════════════════════════════════════════════════
# 3. The archive
# ═══════════════════════════════════════════════════════════════════════════


def test_the_archive_prefixes_records_and_files_it_in_a_year_folder_made_once(account):
    cfg, _fake, held = account
    assert _build(_tracklist(cfg))[0] == int(ExitCode.OK)
    other = "Second Night"
    assert _build(_tracklist(cfg, name=f"{other}.txt"))[0] == int(ExitCode.OK)
    year = ledger.set_playlist(cfg, NAME).year
    xml = _landed(cfg)
    code, done = _archive(xml)
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "ok"
    first = ledger.set_playlist(cfg, NAME).remote_id
    assert held.folders_created == [year]
    (folder_id,) = held.folder_names
    assert held.placed[first] == folder_id
    assert held.titles[first] == f"DOWNLOADED {NAME}"
    marks = mark_record.MarkRecord(cfg).of_pass("set-batch")
    assert [(m.playlist_id, m.name, m.to) for m in marks] == [
        (first, NAME, f"DOWNLOADED {NAME}")
    ]
    code, done = _archive(xml, name=other)
    assert code == int(ExitCode.OK), done
    second = ledger.set_playlist(cfg, other).remote_id
    assert held.folders_created == [year] and held.placed[second] == folder_id


def test_a_playlist_already_in_its_folder_is_left(account):
    cfg, _fake, held = account
    assert _build(_tracklist(cfg))[0] == int(ExitCode.OK)
    xml = _landed(cfg)
    assert _archive(xml)[0] == int(ExitCode.OK)
    held.moves.clear()
    held.renamed.clear()
    code, done = _archive(xml)
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert held.moves == [] and held.renamed == [] and len(held.folders_created) == 1


def test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled(account):
    cfg, _fake, held = account
    assert _build(_tracklist(cfg))[0] == int(ExitCode.OK)
    year = ledger.set_playlist(cfg, NAME).year
    held.folder_names["by-hand"] = year
    assert _archive(_landed(cfg))[0] == int(ExitCode.OK)
    assert held.folders_created == []
    assert held.placed[ledger.set_playlist(cfg, NAME).remote_id] == "by-hand"


def test_two_folders_named_as_the_year_refuse_and_write_nothing(account):
    cfg, _fake, held = account
    assert _build(_tracklist(cfg))[0] == int(ExitCode.OK)
    year = ledger.set_playlist(cfg, NAME).year
    held.folder_names.update({"one": year, "two": year})
    code, refused = drive(["export", "archive", NAME, "--xml", str(_landed(cfg))])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "export-set-ambiguous"
    assert held.moves == [] and held.renamed == []


def test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left(account):
    cfg, _fake, held = account
    assert _build(_tracklist(cfg))[0] == int(ExitCode.OK)
    playlist = ledger.set_playlist(cfg, NAME).remote_id
    held.titles[playlist] = "My Own Title"
    code, done = _archive(_landed(cfg))
    assert code == int(ExitCode.OK), done
    assert held.placed.get(playlist) and held.renamed == []
    assert any(w["code"] == "export-archive-changed-since-plan" for w in done["warnings"])
    assert mark_record.MarkRecord(cfg).of_pass("set-batch") == ()


def test_an_archive_with_no_landed_file_refuses_before_anything(account):
    cfg, _fake, held = account
    assert _build(_tracklist(cfg))[0] == int(ExitCode.OK)
    missing = cfg.library.root / "landed" / "never_inboxed.xml"
    code, refused = drive(["export", "archive", NAME, "--xml", str(missing)])
    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "sync-marks-blocked"
    assert held.moves == [] and held.folders_created == []


def test_an_archive_of_a_set_never_made_says_so(account):
    cfg, _fake, held = account
    code, done = _archive(_landed(cfg), name="Never Made")
    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op"
    assert [w["code"] for w in done["warnings"]] == ["export-archive-nothing-built"]


def test_sync_unmark_takes_the_archive_mark_off_again(account):
    cfg, fake, held = account
    assert _build(_tracklist(cfg))[0] == int(ExitCode.OK)
    assert _archive(_landed(cfg))[0] == int(ExitCode.OK)
    fake.account = [
        AccountPlaylist(playlist_id=pid, name=title, tracks=None)
        for pid, title in held.titles.items()
    ]
    held.renamed.clear()
    code, done = _two_acts(["sync", "unmark", "--pass", "set-batch"], "sync.unmark.confirm")
    assert code == int(ExitCode.OK), done
    assert held.renamed == [(ledger.set_playlist(cfg, NAME).remote_id, NAME)]


# ═══════════════════════════════════════════════════════════════════════════
# 4. Add only, by the suite's own scan
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("source", (Path(sets.__file__), Path(set_cli.__file__)))
def test_no_removal_shape_appears_in_the_set_path(source):
    called = {
        node.func.attr
        for node in ast.walk(ast.parse(source.read_text(encoding="utf-8")))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert not {
        name
        for name in called
        if any(word in name for word in ("remove", "delete", "unheart", "clear"))
    }
