"""U33: outbound service writes share one add-only discipline, and deletion never reaches them.
"""

from __future__ import annotations

import ast
import functools
import json
import subprocess
import sys
from pathlib import Path

import pytest

from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import export, hearts, ledger, pairs, shell
from cratekit.modules.outbound.hearts import REMOVE_FLAGS
from tests import outbound_fakes
from tests.outbound_fakes import FakeAccount, FakeColors
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414

SRC_ROOT = Path(__file__).resolve().parent.parent.parent / "src" / "cratekit"
OUTBOUND_ROOT = SRC_ROOT / "modules" / "outbound"
WRITERS = (OUTBOUND_ROOT, SRC_ROOT / "export", SRC_ROOT / "favorites")

FORBIDDEN_WRITE_NAMES = frozenset({
    "remove_heart", "unheart", "unlike", "uncolor", "clear_heart", "clear_color",
    "delete_playlist", "remove_from_playlist", "remove_track", "un_heart", "un_color",
})


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A library configuration, saved only by the tests that drive the CLI."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (tmp_path / "install").mkdir()
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(tmp_path / "install"))
    monkeypatch.setenv("CRATEKIT_CONFIG_DIR", str(tmp_path / "cfgdir"))
    built = config.from_dict({
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(root), "volume_id": "F1E2-D3C4", "db_path": str(root / "db" / "master.db")
        },
        "paths": {"download_staging": str(tmp_path / "staging")},
        "profile": {"name": "full"},
    })
    config.reset_cache()
    return built


def _trees(root: Path):
    for path in sorted(root.rglob("*.py")):
        yield path.name, ast.parse(path.read_text(encoding="utf-8"))


@functools.cache
def _defined_where(root: Path) -> tuple[tuple[str, str], ...]:
    """Every function defined under ``root`` and the file it is in, read once."""
    return tuple(
        (where, node.name)
        for where, tree in _trees(root)
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    )


def _plan(account, key, *identities, name="", adopts="", expected="", contents=None):
    return export.plan(
        [export.LocalTrack(identity=i, title=i.upper()) for i in identities],
        playlist_key=key, name=name or key, account=account, adopts=adopts, expected=expected,
        contents=contents,
    )


def _match(account, **track) -> export.Plan:
    """One row through the export plan, so the account's ``matches`` say what it was handed."""
    return export.plan(
        [export.LocalTrack(identity="7", title="08A - 124 - Sun Path", **track)],
        playlist_key="crate-one", name="Crate One", account=account,
    )


# ── 1. Unmatched tracks are reported; export has its own confirmation ──────

def test_playlist_export_reports_unmatched_tracks_rather_than_dropping_them(cfg):
    account = FakeAccount(catalog={"owned": "tid-1"})
    report = export.apply(cfg, account, _plan(account, "crate-one", "owned", "missing"))
    assert [item.identity for item in report.unmatched] == ["missing"]
    assert report.added == ("tid-1",)
    assert account.playlist_tracks(report.remote_id) == ("tid-1",)


def test_the_export_plan_hands_the_account_the_release_title_and_not_the_display_one():
    """R-356. The display title carries the naming head and agrees with no provider."""
    account = FakeAccount()
    _match(account, artist="Nova Reef", isrc="AA0000000001", release_title="Sun Path")
    assert account.matches == [{
        "identity": "7", "isrc": "AA0000000001", "title": "Sun Path", "artist": "Nova Reef",
        "album": "",
    }]


def test_the_export_plan_hands_the_account_the_files_album_tag():
    """R-572. The album rides with the ISRC so releases spelled alike can be told apart."""
    account = FakeAccount(catalog={"7": "tid-7"})
    planned = _match(
        account, artist="Nova Reef", isrc="AA0000000001", release_title="Sun Path",
        album="Tidal Lines",
    )
    assert planned.matched == (("7", "tid-7"),)
    assert account.matches == [{
        "identity": "7", "isrc": "AA0000000001", "title": "Sun Path", "artist": "Nova Reef",
        "album": "Tidal Lines",
    }]


def test_an_unmatched_export_row_carries_what_the_account_said_about_it():
    account = FakeAccount()
    account.reasons["several"] = "the ISRC X names 3 provider tracks"
    rows = [export.LocalTrack(identity="several", title="08A - 124 - Sun Path"),
            export.LocalTrack(identity="unknown", title="08A - 124 - Moon Road")]
    planned = export.plan(rows, playlist_key="crate-one", name="Crate One", account=account)
    assert [(row.identity, row.title, row.reason) for row in planned.unmatched] == [
        ("several", "08A - 124 - Sun Path", "the ISRC X names 3 provider tracks"),
        ("unknown", "08A - 124 - Moon Road", "unmatched"),
    ]


def test_a_heart_back_hands_the_account_the_names_and_reports_its_reasons(cfg):
    account = FakeAccount(catalog={"held": "tid-1"})
    account.reasons["several"] = "the ISRC X names 2 provider tracks"
    report = hearts.heart_back(cfg, account, [
        hearts.HeartCandidate(row_id="several", isrc="X", release_title="Sun Path", artist="Nova Reef"),
        hearts.HeartCandidate(row_id="unknown"),
        hearts.HeartCandidate(row_id="held"),
    ])
    assert account.matches[0] == {
        "identity": "several", "isrc": "X", "title": "Sun Path", "artist": "Nova Reef", "album": "",
    }
    assert report.unmatched == ("several", "unknown")
    assert report.reasons == (("several", "the ISRC X names 2 provider tracks"),)
    assert report.hearted == ("tid-1",)


@pytest.mark.parametrize(
    "verb, gate",
    [
        (["export", "playlist", outbound_fakes.CRATE], "export.playlist.confirm"),
        (["sync", "favorites"], "sync.favorites.confirm"),
    ],
    ids=["export", "favorites"],
)
def test_playlist_export_requires_its_own_confirmation(cfg, tmp_path, verb, gate):
    """Each verb meets its own explicit gate, the export handed a real document (U51)."""
    from tests.test_cli_contract import drive
    assert cfg.profile.name == "full"
    config.save(cfg)
    config.reset_cache()
    exported = outbound_fakes.write_export(tmp_path / "outbound")
    code, out, _err = drive(["--output", "json", *verb, "--export", str(exported)])
    assert code == int(ExitCode.DECISION_REQUIRED)
    detail = json.loads(out)["cause"]["detail"]
    assert (detail["gate"], detail["explicit"]) == (gate, True)


# ── 2. Re-export updates rather than creating a duplicate ──────────────────

def test_reexporting_the_same_playlist_updates_rather_than_creating_a_duplicate(cfg):
    """A job frozen before R-229 carries no confirmed remote and is looked up by key."""
    account = FakeAccount(catalog={"a": "tid-a", "b": "tid-b"})
    first = export.apply(cfg, account, _plan(account, "crate-one", "a", name="Crate One"))
    second = export.apply(cfg, account, _plan(account, "crate-one", "a", "b", name="Crate One"))
    assert first.remote_id == second.remote_id
    assert (first.created, second.created) == (True, False)
    assert account.created == ["Crate One"]
    assert account.playlist_tracks(first.remote_id) == ("tid-a", "tid-b")
    assert (second.added, second.already) == (("tid-b",), ("tid-a",))


# ── 2b. R-229. A crate under a new path is recognised, and the record moves ─

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
        assert (found.remote_id, found.recorded, found.crate) == ("pl-9", len(recorded), 4)
        assert found.shared == len(set(recorded) & set(_CRATE))
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
    assert _recognise(cfg, live={"New": _CRATE, "Sets/New": ("7",)}) == _nothing()


@pytest.mark.parametrize(
    "records, key, expected",
    [
        pytest.param(
            {"Old": {"remote_id": "pl-9", "tracks": list(_CRATE)},
             "New": {"remote_id": "pl-1", "tracks": ["1", "2"]}},
            "New", ledger.Recognition(own_remote_id="pl-1", crate=4),
            id="a-crate-with-its-own-record-recognises-nothing",
        ),
        pytest.param(
            {"New": {"remote_id": "pl-1", "added": ["tid-9"]}},
            "New", ledger.Recognition(own_remote_id="pl-1", crate=4),
            id="a-legacy-record-under-its-own-path-is-never-a-mismatch",
        ),
        pytest.param(
            # ``record_playlist_track`` can leave a record with no remote id.
            {"Old": {"remote_id": "pl-9", "tracks": ["1", "2"]},
             "New": {"remote_id": "", "added": []}},
            "New", ledger.Recognition(
                adopts="Old", remote_id="pl-9", shared=2, recorded=2, crate=4,
                candidates=("Old",),
            ),
            id="a-stub-under-its-own-key-does-not-hide-the-orphan",
        ),
        pytest.param(
            {"Old": {"remote_id": "", "tracks": list(_CRATE)}}, "New", _nothing(),
            id="a-record-with-no-remote-playlist-is-never-offered",
        ),
        pytest.param(
            # An old name reused for different music is a different crate.
            {"Crate": {"remote_id": "pl-9", "tracks": ["7", "8"]}}, "Sets/Crate", _nothing(),
            id="a-record-that-holds-tracks-is-never-recognised-by-name",
        ),
        pytest.param(
            {"Crate": {"remote_id": "pl-9", "tracks": "1,2"}},
            "Sets/Crate", ledger.Recognition(
                adopts="Crate", remote_id="pl-9", crate=4, candidates=("Crate",)
            ),
            id="a-tracks-field-that-is-not-a-list-reads-as-a-legacy-record",
        ),
    ],
)
def test_what_a_crate_is_recognised_as(cfg, records, key, expected):
    _write_ledger(cfg, records)
    assert _recognise(cfg, key, name=key.rpartition("/")[2]) == expected


def test_a_record_under_the_crates_own_path_written_from_other_music_is_said(cfg):
    """The other half of the rename chain: this path now holds a different crate."""
    _write_ledger(cfg, {
        "B": {"remote_id": "pl-2", "tracks": ["7", "8", "9"]},
        # F carries the same music with its own remote playlist, so it claims nothing.
        "F": {"remote_id": "pl-3", "tracks": ["7", "8", "9"]},
    })
    found = _recognise(cfg, "B", name="B", live={
        "B": _CRATE, "C": ("7", "8", "9"), "D": ("7",), "E": ("1", "2"), "F": ("7", "8", "9"),
    })
    assert (found.own_remote_id, found.mismatched) == ("pl-2", True)
    assert (found.claimed_by, found.adopts) == (("C",), "")


def test_declining_keeps_everything_but_the_offer(cfg):
    _write_ledger(cfg, {"Old": {"remote_id": "pl-9", "tracks": list(_CRATE)}})
    found = _recognise(cfg)
    assert found.adopts == "Old"
    assert found.without_offer() == _nothing()
    mismatched = ledger.Recognition(own_remote_id="pl-1", crate=4, mismatched=True, claimed_by=("C",))
    assert mismatched.without_offer() == mismatched


@pytest.mark.parametrize(
    "recorded_key, name, adopted",
    [
        ("Crate", "Crate", True),
        ("2024/Crate", "Crate", True),
        ("2024/Other", "Crate", False),
        ("2024/Big Crate", "Crate", False),
        ("2024/A/B", "A/B", True),
        ("Crate", "", False),
        # A NAMELESS playlist under a folder joins to a key ending in the separator.
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


def test_a_record_this_build_wrote_with_no_tracks_is_not_a_legacy_record(cfg):
    """An empty list is no evidence. Only the field's absence is a legacy record."""
    _write_ledger(cfg, {"Crate": {"remote_id": "pl-9", "tracks": []}})
    assert _recognise(cfg, "Sets/Crate", name="Crate") == _nothing()


def test_two_candidates_are_both_named_and_neither_is_adopted(cfg):
    _write_ledger(cfg, {
        "B": {"remote_id": "pl-2", "tracks": ["1", "2"]},
        "A": {"remote_id": "pl-1", "tracks": ["3", "4"]},
    })
    found = _recognise(cfg)
    assert (found.adopts, found.remote_id) == ("", "")
    assert found.candidates == ("A", "B")
    assert found.ambiguous is True


def test_an_adopted_record_moves_and_no_playlist_is_created(cfg):
    account = FakeAccount(catalog={"a": "tid-a", "b": "tid-b"})
    first = export.apply(cfg, account, _plan(account, "Old", "a"))
    moved = export.apply(cfg, account, _plan(account, "New", "a", "b", adopts="Old"))
    assert account.created == ["Old"]
    assert (moved.remote_id, moved.created, moved.adopted_from) == (first.remote_id, False, "Old")
    assert (moved.added, moved.already) == (("tid-b",), ("tid-a",))
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
        export.apply(cfg, account, _plan(account, "New", item, adopts="Old", contents=["a", "b"]))
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
    assert (account.created, account.added) == ([], [])


def test_a_crate_with_its_own_record_ignores_a_frozen_adoption(cfg):
    account = FakeAccount(catalog={"a": "tid-a"})
    export.apply(cfg, account, _plan(account, "Old", "a"))
    export.apply(cfg, account, _plan(account, "New", "a"))
    report = export.apply(cfg, account, _plan(account, "New", "a", adopts="Old"))
    assert (report.adopted_from, report.remote_id) == ("", "pl-2")
    assert sorted(_read_ledger(cfg)) == ["New", "Old"]


def test_a_move_keeps_what_a_stub_under_the_new_key_already_held(cfg):
    _write_ledger(cfg, {
        "Old": {"remote_id": "pl-9", "added": ["tid-a"], "tracks": ["a"]},
        "New": {"remote_id": "", "added": ["tid-z"]},
    })
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
    planned = _plan(account, "House", "b", expected="pl-1", contents=["a", "b"])
    late = export.apply(cfg, account, planned)
    assert account.created == ["House"]
    assert (late.remote_id, late.added) == ("pl-1", ("tid-b",))
    recorded = _read_ledger(cfg)
    assert list(recorded) == ["Deep/House"]
    assert recorded["Deep/House"]["added"] == ["tid-a", "tid-c", "tid-b"]
    # The late job describes the crate as it was, so it does not say what it holds now.
    assert recorded["Deep/House"]["tracks"] == ["a", "c"]


def test_a_job_whose_confirmed_remote_playlist_nothing_records_refuses(cfg):
    account = FakeAccount(catalog={"a": "tid-a"})
    with pytest.raises(CratekitError) as raised:
        export.apply(cfg, account, _plan(account, "House", "a", expected="pl-7"))
    assert raised.value.cause.reason == "outbound-record-moved"
    assert raised.value.cause.detail["remote_id"] == "pl-7"
    assert account.created == []


def test_the_recorded_contents_are_replaced_and_not_grown(cfg):
    """A crate whose music rotates is measured against what it last held."""
    account = FakeAccount(catalog={str(i): f"tid-{i}" for i in range(1, 7)})
    for pair in (("1", "2"), ("3", "4"), ("5", "6")):
        export.apply(cfg, account, _plan(account, "Current", *pair))
    assert _read_ledger(cfg)["Current"]["tracks"] == ["5", "6"]
    assert _recognise(cfg, "Peak", name="Peak", tracks=("5", "6")).adopts == "Current"


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


# ── 3. Hearts sync never removes a heart or a colour ───────────────────────

def test_hearts_sync_never_removes_a_heart_or_a_color_under_any_flag(cfg):
    account = FakeAccount(catalog={"row-1": "tid-1", "row-2": "tid-2"})
    account.hearts.add("tid-keep")
    colors = FakeColors()
    colors.pink.add("already-pink")
    flags = {name: True for name in REMOVE_FLAGS}
    candidates = [hearts.HeartCandidate(row_id="row-1", remote_id="tid-1"),
                  hearts.HeartCandidate(row_id="already-pink", remote_id="tid-keep")]
    report = hearts.heart_back(cfg, account, candidates, colors=colors, flags=flags)
    assert {"tid-keep", "tid-1"} <= account.hearts
    assert "already-pink" in colors.pink
    assert (account.removed, colors.cleared) == ([], [])
    assert report.hearted == ("tid-1",)
    assert hearts.remove_requested(flags) is True


def test_a_favourite_un_hearted_on_the_account_is_hearted_again_and_nothing_is_removed(cfg):
    """U146's R6: a heart taken back while All Favorites holds the track is hearted again."""
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
    defined = {name for root in WRITERS for _where, name in _defined_where(root)}
    assert sorted(defined & FORBIDDEN_WRITE_NAMES) == []


#: R-836. The removals the protocol declares (``remove_tracks``, since U123
#: ``remove_playlist``, since U143 the account root's two), and the flag reader,
#: which names a question rather than a write.
PROTOCOL_REMOVALS = (
    "remove_tracks", "remove_playlist", "remove_root_playlist", "remove_legacy_folder"
)
ADMITTED_REMOVE_NAMES = frozenset({*PROTOCOL_REMOVALS, "remove_requested"})


def test_the_one_remove_the_outbound_package_defines_is_the_protocols_own():
    """Every ``remove`` or delete shaped name is a protocol member, where declared, or the flag reader."""
    shaped = [
        (where, name)
        for root in WRITERS
        for where, name in _defined_where(root)
        if name.lstrip("_").startswith("remove") or "delete" in name.lower()
    ]
    assert {name.lstrip("_") for _where, name in shaped} == ADMITTED_REMOVE_NAMES, shaped
    for member in PROTOCOL_REMOVALS:
        assert sorted(where for where, name in shaped if name == member) == [
            "service.py",
            "tidal_account.py",
        ], member


# ── 4. A deletion run triggers no outbound call ────────────────────────────

def test_a_deletion_run_triggers_no_outbound_call():
    imported = set()
    for _where, tree in _trees(SRC_ROOT / "deletion"):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported |= {alias.name for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
    writers = ("cratekit.modules.outbound", "cratekit.export", "cratekit.favorites")
    banned = {n for n in imported if any(n == w or n.startswith(w + ".") for w in writers)}
    assert not banned, sorted(banned)


# ── 5. An interrupted write is re-runnable without duplicating remote state ─

def test_an_interrupted_outbound_write_is_rerunnable_without_duplicating(cfg):
    # THE SECOND WRITE IS THE ADD (U270): the create, then one request for
    # both tracks, which fails whole.
    account = FakeAccount(catalog={"a": "tid-a", "b": "tid-b"}, fail_after=1)
    planned = _plan(account, "crate-one", "a", "b", name="Crate One")
    with pytest.raises(RuntimeError, match="interrupted"):
        export.apply(cfg, account, planned)
    assert account.created == ["Crate One"]
    remote_id = ledger.playlist_remote_id(cfg, "crate-one")
    assert remote_id is not None
    account.fail_after = None
    report = export.apply(cfg, account, planned)
    assert (report.remote_id, report.created) == (remote_id, False)
    assert account.created == ["Crate One"]
    assert account.playlist_tracks(remote_id) == ("tid-a", "tid-b")
    for tid in ("tid-a", "tid-b"):
        assert account.added.count((remote_id, tid)) == 1, tid


def test_an_interrupted_heart_is_rerunnable_without_duplicating(cfg):
    account = FakeAccount(fail_after=1)
    first = [hearts.HeartCandidate(row_id=f"r{n}", remote_id=f"tid-{n}") for n in (1, 2)]
    with pytest.raises(RuntimeError, match="interrupted"):
        hearts.heart_back(cfg, account, first)
    assert account.hearted == ["tid-1"]
    account.fail_after = None
    report = hearts.heart_back(cfg, account, first)
    assert account.hearted == ["tid-1", "tid-2"]
    assert (report.hearted, report.already) == (("tid-2",), ("tid-1",))


# ── The ledger ──────────────────────────────────────────────────────────────

def test_an_unreadable_outbound_ledger_refuses_rather_than_going_empty(cfg):
    path = config.state_path("outbound_writes", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(CratekitError) as excinfo:
        ledger.playlist_remote_id(cfg, "crate-one")
    assert excinfo.value.cause.reason == "outbound-ledger-unusable"



def test_a_track_settled_twice_on_a_set_playlist_is_recorded_once(cfg):
    """Settling a track the record already holds does not list it a second time."""
    ledger.reserve_set_playlist(cfg, "Set", "2026", lambda: "pl-1")
    ledger.record_set_tracks(cfg, "Set", added=["t1"])
    ledger.record_set_tracks(cfg, "Set", added=["t1", "t2"])
    sets = json.loads(config.state_path("outbound_writes", cfg).read_text())["sets"]
    assert sets["Set"]["added"] == ["t1", "t2"]


def test_a_settled_write_whose_record_is_gone_refuses(cfg):
    """Tracks just written to a playlist the ledger no longer holds refuse, never pass quietly."""
    with pytest.raises(CratekitError) as excinfo:
        ledger.record_set_tracks(cfg, "Gone", added=["t1"])
    assert excinfo.value.cause.reason == "outbound-ledger-unusable"


def test_a_pairs_record_whose_links_hold_empty_text_is_unusable(cfg):
    """Empty text is a hold's word only, so a link naming no track refuses the pairs record."""
    store = pairs.PairStore(cfg)
    store.path.parent.mkdir(parents=True, exist_ok=True)
    pair = {"rekordbox_id": "rb-1", "links": {"tid-1": ""}}
    store.path.write_text(json.dumps(
        {"version": pairs.PAIRS_VERSION, "library_id": cfg.library.volume_id, "pairs": {"p": pair}}
    ))
    with pytest.raises(CratekitError, match="links that are not ids"):
        store.all()


def test_an_unusable_config_is_refused_as_the_verb_that_met_it(monkeypatch):
    """The outbound shell's config refusal names the one origin it was asked from."""
    def broken():
        raise config.ConfigMissing("no config")

    monkeypatch.setattr(config, "load", broken)
    with pytest.raises(CratekitError) as raised:
        shell.load_config("playlist")
    assert (raised.value.cause.reason, raised.value.cause.origin) == ("config-unusable", ("playlist",))


def test_the_outbound_ledger_survives_a_rollback():
    entry = config.state_file("outbound_writes")
    assert entry.snapshot is config.SnapshotRole.SURVIVES_ROLLBACK
    assert entry.root is config.StateRoot.LIBRARY


@pytest.mark.parametrize("first", ["ledger", "ledger_reserve", "ledger_settle"])
def test_each_part_of_the_ledger_imports_first_in_a_fresh_interpreter(first):
    """The ledger re-exports its two parts, so each must import with nothing loaded before it."""
    done = subprocess.run(
        [sys.executable, "-c", f"import cratekit.modules.outbound.{first}"],
        capture_output=True, text=True, check=False,
    )
    assert done.returncode == 0, done.stderr
