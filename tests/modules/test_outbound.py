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
            "album": "",
        }
    ]


def test_the_export_plan_hands_the_account_the_files_album_tag():
    """R-572. The album rides with the ISRC so releases spelled alike can be told apart."""
    account = FakeAccount(catalog={"7": "tid-7"})
    planned = export.plan(
        [
            export.LocalTrack(
                identity="7",
                title="08A - 124 - Sun Path",
                artist="Nova Reef",
                isrc="AA0000000001",
                release_title="Sun Path",
                album="Tidal Lines",
            )
        ],
        playlist_key="crate-one",
        name="Crate One",
        account=account,
    )
    assert planned.matched == (("7", "tid-7"),)
    assert account.matches == [
        {
            "identity": "7",
            "isrc": "AA0000000001",
            "title": "Sun Path",
            "artist": "Nova Reef",
            "album": "Tidal Lines",
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
        "album": "",
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


_CRATE = ("1", "2", "3", "4")


def _recognise(cfg, key="New", *, name="New", tracks=_CRATE, live=None):
    living = {key: tracks} if live is None else live
    return ledger.recognise(cfg, key, name=name, track_ids=tracks, live=living)


def _nothing(crate: int = len(_CRATE)) -> ledger.Recognition:
    return ledger.Recognition(crate=crate)


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
        assert found.shared == len(set(recorded) & set(_CRATE))
        assert found.crate == len(_CRATE)
    else:
        assert found == _nothing()


@pytest.mark.parametrize(
    "size, adopted",
    [(8, True), (9, False), (3000, False)],
    ids=["quadrupled", "one-past-quadrupled", "a-crate-that-merely-contains-it"],
)
def test_a_crate_the_record_is_a_sliver_of_is_not_that_crate(cfg, size, adopted):
    """Two of two recorded tracks is not evidence when the crate holds thousands."""
    _write_ledger(cfg, {"Old": {"remote_id": "pl-9", "tracks": ["1", "2"]}})
    crate = tuple(str(index) for index in range(1, size + 1))
    assert (_recognise(cfg, tracks=crate).adopts == "Old") is adopted


def test_a_record_that_holds_nothing_is_carried_by_nothing():
    """Half of nothing is nothing, and nothing must not read as a match."""
    assert ledger._still_carries(frozenset(), frozenset({"1"})) is False
    assert ledger._still_carries(frozenset(), frozenset()) is False


def test_a_key_the_export_still_carries_is_not_a_candidate(cfg):
    _write_ledger(cfg, {"Old": {"remote_id": "pl-9", "tracks": list(_CRATE)}})
    assert _recognise(cfg, live={"New": _CRATE, "Old": _CRATE}) == _nothing()


def test_a_path_reused_for_a_different_crate_frees_its_record(cfg):
    """B was renamed to C and A was renamed to B. C still adopts what B wrote."""
    _write_ledger(cfg, {"B": {"remote_id": "pl-2", "tracks": ["1", "2", "3", "4"]}})
    found = _recognise(cfg, "C", name="C", live={"C": _CRATE, "B": ("7", "8", "9")})
    assert found.adopts == "B"


def test_a_legacy_record_under_a_living_path_is_never_freed(cfg):
    """With no contents recorded, nothing says the path was reused."""
    _write_ledger(cfg, {"Sets/New": {"remote_id": "pl-2", "added": []}})
    found = _recognise(cfg, live={"New": _CRATE, "Sets/New": ("7",)})
    assert found == _nothing()


def test_a_crate_with_its_own_record_recognises_nothing(cfg):
    _write_ledger(
        cfg,
        {
            "Old": {"remote_id": "pl-9", "tracks": list(_CRATE)},
            "New": {"remote_id": "pl-1", "tracks": ["1", "2"]},
        },
    )
    assert _recognise(cfg) == ledger.Recognition(own_remote_id="pl-1", crate=4)


def test_a_record_under_the_crates_own_path_written_from_other_music_is_said(cfg):
    """The other half of the rename chain: this path now holds a different crate."""
    _write_ledger(
        cfg,
        {
            "B": {"remote_id": "pl-2", "tracks": ["7", "8", "9"]},
            # F CARRIES THE SAME MUSIC AND HAS ITS OWN REMOTE PLAYLIST, so it is
            # not a crate waiting to claim this one.
            "F": {"remote_id": "pl-3", "tracks": ["7", "8", "9"]},
        },
    )
    found = _recognise(
        cfg,
        "B",
        name="B",
        live={
            "B": _CRATE,
            "C": ("7", "8", "9"),
            "D": ("7",),
            "E": ("1", "2"),
            "F": ("7", "8", "9"),
        },
    )
    assert found.own_remote_id == "pl-2"
    assert found.mismatched is True
    assert found.claimed_by == ("C",)
    assert found.adopts == ""


def test_a_legacy_record_under_the_crates_own_path_is_never_a_mismatch(cfg):
    _write_ledger(cfg, {"New": {"remote_id": "pl-1", "added": ["tid-9"]}})
    assert _recognise(cfg).mismatched is False


def test_declining_keeps_everything_but_the_offer(cfg):
    _write_ledger(cfg, {"Old": {"remote_id": "pl-9", "tracks": list(_CRATE)}})
    found = _recognise(cfg)
    assert found.adopts == "Old"
    assert found.without_offer() == _nothing()
    mismatched = ledger.Recognition(
        own_remote_id="pl-1", crate=4, mismatched=True, claimed_by=("C",)
    )
    assert mismatched.without_offer() == mismatched


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
    _write_ledger(cfg, {"Old": {"remote_id": "", "tracks": list(_CRATE)}})
    assert _recognise(cfg) == _nothing()


@pytest.mark.parametrize(
    "recorded_key, name, adopted",
    [
        ("Crate", "Crate", True),
        ("2024/Crate", "Crate", True),
        ("2024/Other", "Crate", False),
        ("2024/Big Crate", "Crate", False),
        ("2024/A/B", "A/B", True),
        ("Crate", "", False),
        # A PLAYLIST WITH NO NAME under a folder joins to a key ending in the
        # separator, which an empty name would match by suffix.
        ("2024/", "", False),
    ],
)
def test_a_record_written_before_tracks_were_kept_is_recognised_by_name(
    cfg, recorded_key, name, adopted
):
    """The legacy rule: a crate dragged into a folder keeps its display name."""
    _write_ledger(cfg, {recorded_key: {"remote_id": "pl-9", "added": ["tid-1"]}})
    found = _recognise(cfg, f"Sets/{name}", name=name)
    assert (found.adopts == recorded_key) is adopted
    assert (found.shared, found.recorded) == (0, 0)


def test_a_record_that_holds_tracks_is_never_recognised_by_name(cfg):
    """An old name reused for different music is a different crate."""
    _write_ledger(cfg, {"Crate": {"remote_id": "pl-9", "tracks": ["7", "8"]}})
    assert _recognise(cfg, "Sets/Crate", name="Crate") == _nothing()


def test_a_record_this_build_wrote_with_no_tracks_is_not_a_legacy_record(cfg):
    """An empty list is no evidence. Only the field's absence is a legacy record."""
    _write_ledger(cfg, {"Crate": {"remote_id": "pl-9", "tracks": []}})
    assert _recognise(cfg, "Sets/Crate", name="Crate") == _nothing()


def test_a_tracks_field_that_is_not_a_list_reads_as_a_legacy_record(cfg):
    _write_ledger(cfg, {"Crate": {"remote_id": "pl-9", "tracks": "1,2"}})
    assert _recognise(cfg, "Sets/Crate", name="Crate").adopts == "Crate"


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


def _plan(account, key, *identities, adopts="", expected="", contents=None):
    return export.plan(
        [export.LocalTrack(identity=i, title=i.upper()) for i in identities],
        playlist_key=key,
        name=key,
        account=account,
        adopts=adopts,
        expected=expected,
        contents=contents,
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
            # R-836. The row each written track came from, moved with the record.
            "rows": {"a": "tid-a", "b": "tid-b"},
        }
    }


def test_the_move_is_reported_once_under_the_per_item_shape(cfg):
    account = FakeAccount(catalog={"a": "tid-a", "b": "tid-b"})
    export.apply(cfg, account, _plan(account, "Old", "a"))
    reports = [
        export.apply(
            cfg, account, _plan(account, "New", item, adopts="Old", contents=["a", "b"])
        )
        for item in ("a", "b")
    ]
    assert [report.adopted_from for report in reports] == ["Old", ""]
    assert account.created == ["Old"]
    assert _read_ledger(cfg)["New"]["formerly"] == ["Old"]
    assert _read_ledger(cfg)["New"]["tracks"] == ["a", "b"]


def test_a_confirmed_adoption_whose_record_is_gone_refuses_rather_than_creating(cfg):
    """Two crates can be offered one orphan. The second to run confirmed an update."""
    account = FakeAccount(catalog={"a": "tid-a"})
    with pytest.raises(CratekitError) as raised:
        export.apply(cfg, account, _plan(account, "New", "a", adopts="Gone"))
    assert raised.value.cause.reason == "outbound-record-moved"
    assert raised.value.cause.detail["adopts"] == "Gone"
    assert account.created == []
    assert account.added == []


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
            "New": {"remote_id": "", "added": ["tid-z"]},
        },
    )
    reserved = ledger.reserve_playlist(cfg, "New", lambda: "never", adopts="Old")
    assert reserved == ledger.Reserved(
        "pl-9", adopted_from="Old", key="New", added=frozenset({"tid-a", "tid-z"})
    )
    assert _read_ledger(cfg)["New"]["added"] == ["tid-a", "tid-z"]


def test_a_job_confirmed_before_its_record_moved_goes_on_writing_to_it(cfg):
    """The remote id is the stable identifier. A half driven job must not create."""
    account = FakeAccount(catalog={"a": "tid-a", "b": "tid-b", "c": "tid-c"})
    export.apply(cfg, account, _plan(account, "House", "a", contents=["a", "b"]))
    export.apply(
        cfg, account, _plan(account, "Deep/House", "c", adopts="House", contents=["a", "c"])
    )

    late = export.apply(
        cfg, account, _plan(account, "House", "b", expected="pl-1", contents=["a", "b"])
    )

    assert account.created == ["House"]
    assert late.remote_id == "pl-1"
    assert late.added == ("tid-b",)
    recorded = _read_ledger(cfg)
    assert list(recorded) == ["Deep/House"]
    assert recorded["Deep/House"]["added"] == ["tid-a", "tid-c", "tid-b"]
    # THE LATE JOB DESCRIBES THE CRATE AS IT WAS, so it does not get to say what
    # the crate holds now.
    assert recorded["Deep/House"]["tracks"] == ["a", "c"]


def test_a_job_whose_confirmed_remote_playlist_nothing_records_refuses(cfg):
    account = FakeAccount(catalog={"a": "tid-a"})
    with pytest.raises(CratekitError) as raised:
        export.apply(cfg, account, _plan(account, "House", "a", expected="pl-7"))
    assert raised.value.cause.reason == "outbound-record-moved"
    assert raised.value.cause.detail["remote_id"] == "pl-7"
    assert account.created == []


def test_a_job_with_no_confirmed_remote_is_looked_up_by_key_as_it_always_was(cfg):
    """A payload frozen before this build carries no remote id and still runs."""
    account = FakeAccount(catalog={"a": "tid-a"})
    first = export.apply(cfg, account, _plan(account, "House", "a"))
    again = export.apply(cfg, account, _plan(account, "House", "a"))
    assert (first.created, again.created) == (True, False)
    assert account.created == ["House"]


def test_the_recorded_contents_are_replaced_and_not_grown(cfg):
    """A crate whose music rotates is measured against what it last held."""
    account = FakeAccount(catalog={str(i): f"tid-{i}" for i in range(1, 7)})
    export.apply(cfg, account, _plan(account, "Current", "1", "2"))
    export.apply(cfg, account, _plan(account, "Current", "3", "4"))
    export.apply(cfg, account, _plan(account, "Current", "5", "6"))
    assert _read_ledger(cfg)["Current"]["tracks"] == ["5", "6"]

    found = ledger.recognise(
        cfg, "Peak", name="Peak", track_ids=("5", "6"), live={"Peak": ("5", "6")}
    )
    assert found.adopts == "Current"


def test_the_whole_crate_is_recorded_by_the_first_item_even_unmatched_rows(cfg):
    """An export interrupted after one item must not leave one row as the crate."""
    account = FakeAccount(catalog={"a": "tid-a"})
    export.apply(cfg, account, _plan(account, "Crate", "a", contents=["a", "b", "c"]))
    assert _read_ledger(cfg)["Crate"]["tracks"] == ["a", "b", "c"]


def test_a_legacy_record_gains_its_contents_on_the_next_export_under_its_key(cfg):
    """Every row is already there, nothing is added, and the crate is recorded."""
    account = FakeAccount(catalog={"a": "tid-a", "b": "tid-b"})
    account.playlists["pl-9"] = ["tid-a", "tid-b"]
    _write_ledger(cfg, {"Crate": {"remote_id": "pl-9", "added": ["tid-a", "tid-b"]}})

    report = export.apply(cfg, account, _plan(account, "Crate", "a", "b"))

    assert report.added == ()
    assert _read_ledger(cfg)["Crate"]["tracks"] == ["a", "b"]
    assert _read_ledger(cfg)["Crate"]["added"] == ["tid-a", "tid-b"]


def test_a_settled_crate_reads_the_ledger_once_and_writes_nothing(cfg, monkeypatch):
    account = FakeAccount(catalog={"a": "tid-a"})
    export.apply(cfg, account, _plan(account, "Crate", "a"))
    writes: list[object] = []
    reads: list[object] = []
    load = ledger._load
    monkeypatch.setattr(ledger, "_write", lambda *args: writes.append(args))
    monkeypatch.setattr(ledger, "_load", lambda cfg: reads.append(cfg) or load(cfg))
    export.apply(cfg, account, _plan(account, "Crate", "a"))
    assert writes == []
    assert len(reads) == 1

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


def test_a_favourite_un_hearted_on_the_account_is_hearted_again_and_nothing_is_removed(cfg):
    """U146's R6, the outbound half: a track hearted on the account, placed
    into All Favorites by the inbound side, then un-hearted on the account
    while All Favorites still holds it, is a candidate again and is hearted
    again. The heart the author made is in no ledger, so nothing stops it."""
    account = FakeAccount(catalog={"row-owned": "tid-owned"})
    account.hearts.add("tid-other")
    assert "tid-owned" not in account.hearts, "taken back on the account"

    report = hearts.heart_back(
        cfg, account, [hearts.HeartCandidate(row_id="row-owned", remote_id="tid-owned")]
    )

    assert report.hearted == ("tid-owned",)
    assert account.hearts == {"tid-owned", "tid-other"}
    assert account.removed == []


def test_the_outbound_package_defines_no_remove_write():
    defined = _defined_functions(OUTBOUND_ROOT) | _defined_functions(EXPORT_ROOT) | _defined_functions(
        FAVORITES_ROOT
    )
    clash = sorted(defined & FORBIDDEN_WRITE_NAMES)
    assert clash == []


#: R-836. The removals the protocol declares, ``remove_tracks``, since U123
#: ``remove_playlist``, since U143 the account root's two, and the flag reader
#: that was already here and names a question rather than a write.
PROTOCOL_REMOVALS = (
    "remove_tracks",
    "remove_playlist",
    "remove_root_playlist",
    "remove_legacy_folder",
)
ADMITTED_REMOVE_NAMES = frozenset({*PROTOCOL_REMOVALS, "remove_requested"})


def _defined_where(root: Path) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found.append((path.name, node.name))
    return found


def test_the_one_remove_the_outbound_package_defines_is_the_protocols_own():
    """Narrowed on R-836 from "no remove" to exactly ``remove_tracks``, on
    U123 to that and ``remove_playlist``, and on U143 to those and the account
    root's two.

    The exact name scan above misses a plural, which ``remove_tracks`` is of
    ``remove_track``, so this one reads every function whose name opens with
    ``remove`` or names a delete, and admits only the protocol's member, in
    the two files that declare and implement it, and the flag readers.
    """
    shaped = [
        (where, name)
        for root in (OUTBOUND_ROOT, EXPORT_ROOT, FAVORITES_ROOT)
        for where, name in _defined_where(root)
        if name.lstrip("_").startswith("remove") or "delete" in name.lower()
    ]
    assert {name.lstrip("_") for _where, name in shaped} == ADMITTED_REMOVE_NAMES, shaped
    for member in PROTOCOL_REMOVALS:
        assert sorted(where for where, name in shaped if name == member) == [
            "service.py",
            "tidal_account.py",
        ], member


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
    # THE SECOND WRITE IS THE ADD (U270): the create, then one request for
    # both tracks, which fails whole.
    account = FakeAccount(catalog={"a": "tid-a", "b": "tid-b"}, fail_after=1)
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
