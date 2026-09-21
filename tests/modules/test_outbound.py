"""U33: outbound service writes share one add-only discipline.

The brief names five scenarios. Each one has a test below:

1. playlist export reports unmatched tracks and requires its own confirmation
2. re-exporting the same playlist updates rather than creating a duplicate
3. hearts sync never removes a heart or a colour under any flag or config key
4. a deletion run triggers no outbound call
5. an outbound write interrupted partway is re-runnable without duplicating
   remote state

Scope is add-only. Deletion never reaches this package (R36). The brief
Files line was src/cratekit/modules/outbound/; the verbs land at the
registry strings cratekit.export.cli and cratekit.favorites.cli.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import export, hearts, ledger
from cratekit.modules.outbound.hearts import REMOVE_FLAGS
from tests import outbound_fakes
from tests.outbound_fakes import FakeAccount, FakeColors

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_ROOT = REPO_ROOT / "src"
OUTBOUND_ROOT = SRC_ROOT / "cratekit" / "modules" / "outbound"
DELETION_ROOT = SRC_ROOT / "cratekit" / "deletion"
EXPORT_ROOT = SRC_ROOT / "cratekit" / "export"
FAVORITES_ROOT = SRC_ROOT / "cratekit" / "favorites"

FORBIDDEN_WRITE_NAMES = frozenset(
    {
        "remove_heart",
        "unheart",
        "unlike",
        "uncolor",
        "clear_heart",
        "clear_color",
        "delete_playlist",
        "remove_from_playlist",
        "remove_track",
        "un_heart",
        "un_color",
    }
)


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    install = tmp_path / "install"
    install.mkdir()
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(install))
    monkeypatch.setenv("CRATEKIT_CONFIG_DIR", str(tmp_path / "cfgdir"))
    built = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(built)
    config.reset_cache()
    return built


def _defined_functions(root: Path) -> set[str]:
    found: set[str] = set()
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found.add(node.name)
    return found


def _imported_modules(root: Path) -> set[str]:
    found: set[str] = set()
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found.add(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                found.add(node.module)
    return found


# ═══════════════════════════════════════════════════════════════════════════
# 1. Unmatched tracks are reported; export has its own confirmation
# ═══════════════════════════════════════════════════════════════════════════


def test_playlist_export_reports_unmatched_tracks_rather_than_dropping_them(cfg):
    account = FakeAccount(catalog={"owned": "tid-1"})
    planned = export.plan(
        [
            export.LocalTrack(identity="owned", title="Held", artist="Act"),
            export.LocalTrack(identity="missing", title="Gone", artist="Act"),
        ],
        playlist_key="crate-one",
        name="Crate One",
        account=account,
    )
    report = export.apply(cfg, account, planned)
    assert [item.identity for item in report.unmatched] == ["missing"]
    assert report.added == ("tid-1",)
    assert account.playlist_tracks(report.remote_id) == ("tid-1",)


def test_the_export_plan_hands_the_account_the_release_title_and_not_the_display_one():
    """R-356. The display title carries the naming head and agrees with no provider."""
    account = FakeAccount()
    export.plan(
        [
            export.LocalTrack(
                identity="7",
                title="08A - 124 - Sun Path",
                artist="Nova Reef",
                isrc="AA0000000001",
                release_title="Sun Path",
            )
        ],
        playlist_key="crate-one",
        name="Crate One",
        account=account,
    )
    assert account.matches == [
        {
            "identity": "7",
            "isrc": "AA0000000001",
            "title": "Sun Path",
            "artist": "Nova Reef",
        }
    ]


def test_an_unmatched_export_row_carries_what_the_account_said_about_it():
    account = FakeAccount()
    account.reasons["several"] = "the ISRC X names 3 provider tracks"
    planned = export.plan(
        [
            export.LocalTrack(identity="several", title="08A - 124 - Sun Path"),
            export.LocalTrack(identity="unknown", title="08A - 124 - Moon Road"),
        ],
        playlist_key="crate-one",
        name="Crate One",
        account=account,
    )
    assert [(row.identity, row.title, row.reason) for row in planned.unmatched] == [
        ("several", "08A - 124 - Sun Path", "the ISRC X names 3 provider tracks"),
        ("unknown", "08A - 124 - Moon Road", "unmatched"),
    ]


def test_a_heart_back_hands_the_account_the_names_and_reports_its_reasons(cfg):
    account = FakeAccount(catalog={"held": "tid-1"})
    account.reasons["several"] = "the ISRC X names 2 provider tracks"
    report = hearts.heart_back(
        cfg,
        account,
        [
            hearts.HeartCandidate(
                row_id="several", isrc="X", release_title="Sun Path", artist="Nova Reef"
            ),
            hearts.HeartCandidate(row_id="unknown"),
            hearts.HeartCandidate(row_id="held"),
        ],
    )
    assert account.matches[0] == {
        "identity": "several",
        "isrc": "X",
        "title": "Sun Path",
        "artist": "Nova Reef",
    }
    assert report.unmatched == ("several", "unknown")
    assert report.reasons == (("several", "the ISRC X names 2 provider tracks"),)
    assert report.hearted == ("tid-1",)


def test_playlist_export_requires_its_own_confirmation(cfg, tmp_path):
    from tests.test_cli_contract import drive

    assert cfg.profile.name == "full"
    # THE EXPORT IS REAL RATHER THAN OMITTED, since U51. This verb now decides
    # its job items from a collection document, and an absent one refuses
    # BEFORE the gate. Handing it a real document keeps the claim this test
    # makes, that the confirmation is reached and is explicit, rather than
    # letting an earlier refusal stand in for it.
    exported = outbound_fakes.write_export(tmp_path / "outbound")
    code, out, _err = drive(
        [
            "--output",
            "json",
            "export",
            "playlist",
            outbound_fakes.CRATE,
            "--export",
            str(exported),
        ]
    )
    assert code == int(ExitCode.DECISION_REQUIRED)
    envelope = json.loads(out)
    assert envelope["cause"]["detail"]["gate"] == "export.playlist.confirm"
    assert envelope["cause"]["detail"]["explicit"] is True


# ═══════════════════════════════════════════════════════════════════════════
# 2. Re-export updates rather than creating a duplicate
# ═══════════════════════════════════════════════════════════════════════════


def test_reexporting_the_same_playlist_updates_rather_than_creating_a_duplicate(cfg):
    account = FakeAccount(catalog={"a": "tid-a", "b": "tid-b"})
    first = export.apply(
        cfg,
        account,
        export.plan(
            [export.LocalTrack(identity="a", title="A")],
            playlist_key="crate-one",
            name="Crate One",
            account=account,
        ),
    )
    second = export.apply(
        cfg,
        account,
        export.plan(
            [
                export.LocalTrack(identity="a", title="A"),
                export.LocalTrack(identity="b", title="B"),
            ],
            playlist_key="crate-one",
            name="Crate One",
            account=account,
        ),
    )
    assert first.remote_id == second.remote_id
    assert first.created is True
    assert second.created is False
    assert account.created == ["Crate One"]
    assert account.playlist_tracks(first.remote_id) == ("tid-a", "tid-b")
    assert second.added == ("tid-b",)
    assert second.already == ("tid-a",)


# ═══════════════════════════════════════════════════════════════════════════
# 2b. R-229. A crate under a new path is recognised, and the record moves
# ═══════════════════════════════════════════════════════════════════════════


def _write_ledger(cfg, playlists: dict) -> None:
    path = config.state_path("outbound_writes", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"version": 1, "playlists": playlists, "hearts": {}}))


def _read_ledger(cfg) -> dict:
    return json.loads(config.state_path("outbound_writes", cfg).read_text())["playlists"]


def _recognise(cfg, key="New", *, name="New", tracks=("1", "2", "3", "4"), live=("New",)):
    return ledger.recognise(cfg, key, name=name, track_ids=tracks, live_keys=live)


@pytest.mark.parametrize(
    "recorded, adopted",
    [
        (["1", "2", "3", "4"], True),
        (["1", "2", "8", "9"], True),
        (["1", "7", "8", "9"], False),
        (["1", "2", "7", "8", "9"], False),
        (["7", "8", "9"], False),
    ],
    ids=["all", "exactly-half", "a-quarter", "two-of-five", "none"],
)
def test_a_record_is_recognised_when_the_crate_still_carries_half_its_tracks(
    cfg, recorded, adopted
):
    _write_ledger(cfg, {"Old": {"remote_id": "pl-9", "added": [], "tracks": recorded}})
    found = _recognise(cfg)
    assert (found.adopts == "Old") is adopted
    if adopted:
        assert found.remote_id == "pl-9"
        assert found.recorded == len(recorded)
        assert found.shared == len(set(recorded) & {"1", "2", "3", "4"})
    else:
        assert found == ledger.Recognition()


def test_a_key_the_export_still_carries_is_not_a_candidate(cfg):
    _write_ledger(cfg, {"Old": {"remote_id": "pl-9", "tracks": ["1", "2", "3", "4"]}})
    assert _recognise(cfg, live=("New", "Old")) == ledger.Recognition()


def test_a_crate_with_its_own_record_recognises_nothing(cfg):
    _write_ledger(
        cfg,
        {
            "Old": {"remote_id": "pl-9", "tracks": ["1", "2", "3", "4"]},
            "New": {"remote_id": "pl-1", "tracks": ["1"]},
        },
    )
    assert _recognise(cfg) == ledger.Recognition()


def test_a_stub_under_the_crates_own_key_does_not_hide_the_orphan(cfg):
    """``record_playlist_track`` can leave a record with no remote id."""
    _write_ledger(
        cfg,
        {
            "Old": {"remote_id": "pl-9", "tracks": ["1", "2"]},
            "New": {"remote_id": "", "added": []},
        },
    )
    assert _recognise(cfg).adopts == "Old"


def test_a_record_with_no_remote_playlist_is_never_offered(cfg):
    _write_ledger(cfg, {"Old": {"remote_id": "", "tracks": ["1", "2", "3", "4"]}})
    assert _recognise(cfg) == ledger.Recognition()


@pytest.mark.parametrize(
    "recorded_key, name, adopted",
    [
        ("Crate", "Crate", True),
        ("2024/Crate", "Crate", True),
        ("2024/Other", "Crate", False),
        ("2024/Big Crate", "Crate", False),
        ("2024/A/B", "A/B", True),
        ("Crate", "", False),
    ],
)
def test_a_record_written_before_tracks_were_kept_is_recognised_by_name(
    cfg, recorded_key, name, adopted
):
    """The legacy rule: a crate dragged into a folder keeps its display name."""
    _write_ledger(cfg, {recorded_key: {"remote_id": "pl-9", "added": ["tid-1"]}})
    found = _recognise(cfg, f"Sets/{name}", name=name, live=(f"Sets/{name}",))
    assert (found.adopts == recorded_key) is adopted
    assert (found.shared, found.recorded) == (0, 0)


def test_a_record_that_holds_tracks_is_never_recognised_by_name(cfg):
    """An old name reused for different music is a different crate."""
    _write_ledger(cfg, {"Crate": {"remote_id": "pl-9", "tracks": ["7", "8"]}})
    found = _recognise(cfg, "Sets/Crate", name="Crate", live=("Sets/Crate",))
    assert found == ledger.Recognition()


def test_a_tracks_field_that_is_not_a_list_reads_as_a_legacy_record(cfg):
    _write_ledger(cfg, {"Crate": {"remote_id": "pl-9", "tracks": "1,2"}})
    found = _recognise(cfg, "Sets/Crate", name="Crate", live=("Sets/Crate",))
    assert found.adopts == "Crate"


def test_two_candidates_are_both_named_and_neither_is_adopted(cfg):
    _write_ledger(
        cfg,
        {
            "B": {"remote_id": "pl-2", "tracks": ["1", "2"]},
            "A": {"remote_id": "pl-1", "tracks": ["3", "4"]},
        },
    )
    found = _recognise(cfg)
    assert found.adopts == ""
    assert found.remote_id == ""
    assert found.candidates == ("A", "B")
    assert found.ambiguous is True


def _plan(account, key, *identities, adopts=""):
    return export.plan(
        [export.LocalTrack(identity=i, title=i.upper()) for i in identities],
        playlist_key=key,
        name=key,
        account=account,
        adopts=adopts,
    )


def test_an_adopted_record_moves_and_no_playlist_is_created(cfg):
    account = FakeAccount(catalog={"a": "tid-a", "b": "tid-b"})
    first = export.apply(cfg, account, _plan(account, "Old", "a"))

    moved = export.apply(cfg, account, _plan(account, "New", "a", "b", adopts="Old"))

    assert account.created == ["Old"]
    assert moved.remote_id == first.remote_id
    assert moved.created is False
    assert moved.adopted_from == "Old"
    assert moved.added == ("tid-b",)
    assert moved.already == ("tid-a",)
    assert _read_ledger(cfg) == {
        "New": {
            "remote_id": first.remote_id,
            "added": ["tid-a", "tid-b"],
            "tracks": ["a", "b"],
            "formerly": ["Old"],
        }
    }


def test_the_move_is_reported_once_under_the_per_item_shape(cfg):
    account = FakeAccount(catalog={"a": "tid-a", "b": "tid-b"})
    export.apply(cfg, account, _plan(account, "Old", "a"))
    reports = [
        export.apply(cfg, account, _plan(account, "New", item, adopts="Old"))
        for item in ("a", "b")
    ]
    assert [report.adopted_from for report in reports] == ["Old", ""]
    assert account.created == ["Old"]
    assert _read_ledger(cfg)["New"]["formerly"] == ["Old"]


def test_an_adoption_naming_a_record_that_is_gone_creates(cfg):
    account = FakeAccount(catalog={"a": "tid-a"})
    report = export.apply(cfg, account, _plan(account, "New", "a", adopts="Gone"))
    assert report.created is True
    assert report.adopted_from == ""
    assert account.created == ["New"]


def test_a_crate_with_its_own_record_ignores_a_frozen_adoption(cfg):
    account = FakeAccount(catalog={"a": "tid-a"})
    export.apply(cfg, account, _plan(account, "Old", "a"))
    export.apply(cfg, account, _plan(account, "New", "a"))
    report = export.apply(cfg, account, _plan(account, "New", "a", adopts="Old"))
    assert report.adopted_from == ""
    assert report.remote_id == "pl-2"
    assert sorted(_read_ledger(cfg)) == ["New", "Old"]


def test_a_move_keeps_what_a_stub_under_the_new_key_already_held(cfg):
    _write_ledger(
        cfg,
        {
            "Old": {"remote_id": "pl-9", "added": ["tid-a"], "tracks": ["a"]},
            "New": {"remote_id": "", "added": ["tid-z"], "tracks": ["z"]},
        },
    )
    reserved = ledger.reserve_playlist(cfg, "New", lambda: "never", adopts="Old")
    assert reserved == ledger.Reserved("pl-9", adopted_from="Old")
    assert _read_ledger(cfg)["New"]["added"] == ["tid-a", "tid-z"]
    assert _read_ledger(cfg)["New"]["tracks"] == ["a", "z"]


def test_a_legacy_record_gains_its_tracks_on_the_next_export_under_its_key(cfg):
    """Every row is already there, nothing is added, and the rows are recorded."""
    account = FakeAccount(catalog={"a": "tid-a", "b": "tid-b"})
    account.playlists["pl-9"] = ["tid-a", "tid-b"]
    _write_ledger(cfg, {"Crate": {"remote_id": "pl-9", "added": ["tid-a", "tid-b"]}})

    report = export.apply(cfg, account, _plan(account, "Crate", "a", "b"))

    assert report.added == ()
    assert _read_ledger(cfg)["Crate"]["tracks"] == ["a", "b"]
    assert _read_ledger(cfg)["Crate"]["added"] == ["tid-a", "tid-b"]


def test_a_settled_crate_costs_no_ledger_writes(cfg, monkeypatch):
    account = FakeAccount(catalog={"a": "tid-a"})
    export.apply(cfg, account, _plan(account, "Crate", "a"))
    writes: list[object] = []
    monkeypatch.setattr(ledger, "_write", lambda *args: writes.append(args))
    export.apply(cfg, account, _plan(account, "Crate", "a"))
    assert writes == []


# ═══════════════════════════════════════════════════════════════════════════
# 3. Hearts sync never removes a heart or a colour
# ═══════════════════════════════════════════════════════════════════════════


def test_hearts_sync_never_removes_a_heart_or_a_color_under_any_flag(cfg):
    account = FakeAccount(catalog={"row-1": "tid-1", "row-2": "tid-2"})
    account.hearts.add("tid-keep")
    colors = FakeColors()
    colors.pink.add("already-pink")
    flags = {name: True for name in REMOVE_FLAGS}
    flags["remove_missing"] = True
    flags["mirror"] = True
    report = hearts.heart_back(
        cfg,
        account,
        [
            hearts.HeartCandidate(row_id="row-1", remote_id="tid-1"),
            hearts.HeartCandidate(row_id="already-pink", remote_id="tid-keep"),
        ],
        colors=colors,
        flags=flags,
    )
    assert "tid-keep" in account.hearts
    assert "already-pink" in colors.pink
    assert account.removed == []
    assert colors.cleared == []
    assert "tid-1" in account.hearts
    assert report.hearted == ("tid-1",)
    assert hearts.remove_requested(flags) is True


def test_the_outbound_package_defines_no_remove_write():
    defined = _defined_functions(OUTBOUND_ROOT) | _defined_functions(EXPORT_ROOT) | _defined_functions(
        FAVORITES_ROOT
    )
    clash = sorted(defined & FORBIDDEN_WRITE_NAMES)
    assert clash == []


# ═══════════════════════════════════════════════════════════════════════════
# 4. A deletion run triggers no outbound call
# ═══════════════════════════════════════════════════════════════════════════


def test_a_deletion_run_triggers_no_outbound_call():
    imported = _imported_modules(DELETION_ROOT)
    banned = {
        name
        for name in imported
        if name == "cratekit.modules.outbound"
        or name.startswith("cratekit.modules.outbound.")
        or name == "cratekit.export"
        or name.startswith("cratekit.export.")
        or name == "cratekit.favorites"
        or name.startswith("cratekit.favorites.")
    }
    assert not banned, sorted(banned)


# ═══════════════════════════════════════════════════════════════════════════
# 5. An interrupted write is re-runnable without duplicating remote state
# ═══════════════════════════════════════════════════════════════════════════


def test_an_interrupted_outbound_write_is_rerunnable_without_duplicating(cfg):
    account = FakeAccount(catalog={"a": "tid-a", "b": "tid-b"}, fail_after=2)
    planned = export.plan(
        [
            export.LocalTrack(identity="a", title="A"),
            export.LocalTrack(identity="b", title="B"),
        ],
        playlist_key="crate-one",
        name="Crate One",
        account=account,
    )
    with pytest.raises(RuntimeError, match="interrupted"):
        export.apply(cfg, account, planned)
    assert account.created == ["Crate One"]
    remote_id = ledger.playlist_remote_id(cfg, "crate-one")
    assert remote_id is not None
    account.fail_after = None
    report = export.apply(cfg, account, planned)
    assert report.remote_id == remote_id
    assert report.created is False
    assert account.created == ["Crate One"]
    assert account.playlist_tracks(remote_id) == ("tid-a", "tid-b")
    assert account.added.count((remote_id, "tid-a")) == 1
    assert account.added.count((remote_id, "tid-b")) == 1


def test_an_interrupted_heart_is_rerunnable_without_duplicating(cfg):
    account = FakeAccount(fail_after=1)
    first = [
        hearts.HeartCandidate(row_id="r1", remote_id="tid-1"),
        hearts.HeartCandidate(row_id="r2", remote_id="tid-2"),
    ]
    with pytest.raises(RuntimeError, match="interrupted"):
        hearts.heart_back(cfg, account, first)
    assert account.hearted == ["tid-1"]
    account.fail_after = None
    report = hearts.heart_back(cfg, account, first)
    assert account.hearted == ["tid-1", "tid-2"]
    assert report.hearted == ("tid-2",)
    assert report.already == ("tid-1",)


# ═══════════════════════════════════════════════════════════════════════════
# Ledger and landing
# ═══════════════════════════════════════════════════════════════════════════


def test_an_unreadable_outbound_ledger_refuses_rather_than_going_empty(cfg):
    path = config.state_path("outbound_writes", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(CratekitError) as excinfo:
        ledger.playlist_remote_id(cfg, "crate-one")
    assert excinfo.value.cause.reason == "outbound-ledger-unusable"


def test_the_outbound_ledger_survives_a_rollback():
    entry = config.state_file("outbound_writes")
    assert entry.snapshot is config.SnapshotRole.SURVIVES_ROLLBACK
    assert entry.root is config.StateRoot.LIBRARY


def test_favorites_confirm_is_separate_from_the_export_confirm(cfg, tmp_path):
    from tests.test_cli_contract import drive

    assert cfg.profile.name == "full"
    exported = outbound_fakes.write_export(tmp_path / "outbound")
    code, out, _err = drive(
        ["--output", "json", "sync", "favorites", "--export", str(exported)]
    )
    assert code == int(ExitCode.DECISION_REQUIRED)
    envelope = json.loads(out)
    assert envelope["cause"]["detail"]["gate"] == "sync.favorites.confirm"
    assert envelope["cause"]["detail"]["gate"] != "export.playlist.confirm"
