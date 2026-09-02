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
