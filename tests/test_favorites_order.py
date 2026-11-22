"""U180: the Favorites folder reads newest first, and a new month lands in its place."""

from __future__ import annotations

import pytest

from cratekit.core import rb_writer, session
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import order, order_cli, placement
from tests.cli_drive import drive
from tests.test_favorites_backfill import _account, _db, _landed_hearts, _note, _sql
from tests.test_favorites_backfill import _acts as _backfill_acts
from tests.test_favorites_backfill import _approved as _backfill_approved
from tests.test_favorites_backfill import _silent as _silent  # noqa: PLC0414
from tests.test_favorites_backfill import home as home  # noqa: PLC0414
from tests.test_favorites_backfill import silence as silence  # noqa: PLC0414
from tests.test_favorites_split import _approved as _split_approved
from tests.test_favorites_split import _quarter
from tests.test_intake_land_account_playlists_native import _stage
from tests.test_intake_land_hearts_native import NOV, SOURCE, _home, _landed, hearts_swept
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import _query
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_label_workers import one_parser as one_parser  # noqa: PLC0414 - fixture

VERB = ["favorites", "order"]
GATE = order_cli.APPROVE_GATE
OCT = "2026-10-{day:02d}T12:00:00+00:00"


def _make(cfg, folder_id: str, *names: str, kind: str = "plain") -> dict[str, str]:
    """Playlists made under the folder in this order, plain unless ``kind`` says a folder."""
    with _db(cfg) as handle:
        parent = handle.get_playlist(ID=folder_id) if folder_id else None
        create = handle.create_playlist_folder if kind == "folder" else handle.create_playlist
        made = {name: str(create(name, parent=parent).ID) for name in names}
    return made


def _fill(cfg, playlist_id: str, count: int = 2) -> None:
    """Some of the library's rows put in a playlist, so a membership is there to be left alone."""
    rows = [str(row) for (row,) in _query(cfg, "SELECT ID FROM djmdContent ORDER BY ID")][:count]
    with _db(cfg) as handle:
        for row in rows:
            handle.add_to_playlist(handle.get_playlist(ID=playlist_id), row)


def _order(cfg, folder_id: str) -> list[str]:
    """The live children of the folder by name, in the order rekordbox shows them."""
    return [str(name) for (name,) in _query(
        cfg,
        "SELECT Name FROM djmdPlaylist WHERE ParentID = ? AND rb_local_deleted = 0 ORDER BY Seq, Name, ID",
        folder_id,
    )]


def _playlist_rows(cfg) -> list[tuple]:
    return _query(cfg, "SELECT * FROM djmdPlaylist ORDER BY ID")


def _memberships(cfg) -> list[tuple]:
    return _query(cfg, "SELECT * FROM djmdSongPlaylist ORDER BY ID")


def _content(cfg) -> list[tuple]:
    return _query(cfg, "SELECT * FROM djmdContent ORDER BY ID")


def _seq(cfg, playlist_id: str) -> int:
    ((value,),) = _query(cfg, "SELECT Seq FROM djmdPlaylist WHERE ID = ?", playlist_id)
    return int(value)


def _set(cfg, column: str, **values) -> None:
    """``column`` of each playlist row set by hand, as rekordbox or a person left it."""
    rows = [(value, playlist_id) for playlist_id, value in values.items()]
    _sql(cfg, f"UPDATE djmdPlaylist SET {column} = ? WHERE ID = ?", *rows)


def _mark_removed(cfg, playlist_id: str) -> None:
    """A playlist rekordbox removed: its row kept, the marker on, its position kept."""
    _set(cfg, "rb_local_deleted", **{playlist_id: 1})


def _acts() -> tuple[int, dict, dict]:
    return _backfill_acts(VERB, GATE)


def _approved() -> tuple[dict, dict]:
    return _backfill_approved(VERB, GATE)


def test_a_folder_oldest_first_reads_newest_first_with_all_favorites_first_and_undated_last(home):
    cfg, folder_id, source_id = home
    made = _make(cfg, folder_id, "Undated", "2026-08", "2026-09", "2026-10")
    _fill(cfg, source_id)
    _fill(cfg, made["2026-09"])
    memberships, content = _memberships(cfg), _content(cfg)
    assert _order(cfg, folder_id) == [SOURCE, "Undated", "2026-08", "2026-09", "2026-10"]
    acted, shown = _approved()
    after = [SOURCE, "2026-10", "2026-09", "2026-08", "Undated"]
    assert _order(cfg, folder_id) == after
    assert shown["order now"] == [SOURCE, "Undated", "2026-08", "2026-09", "2026-10"]
    assert shown["order after"] == after
    assert shown["playlists to move"] == 4
    items = {item["playlist"]: item for item in acted["data"]["items"]}
    assert (items["Undated"]["from"], items["Undated"]["to"]) == (2, 5)
    assert (items["2026-10"]["from"], items["2026-10"]["to"]) == (5, 2)
    assert items[SOURCE]["action"] == "stay" and items["2026-10"]["action"] == "move"
    assert acted["data"]["totals"]["moved"] == 4
    note = _note(acted, order_cli.ORDERED)
    assert "4 playlist(s) moved in 'Favorites'" in note and ", ".join(after) in note
    # Positions and nothing else.
    assert _memberships(cfg) == memberships
    assert _content(cfg) == content


def test_a_folder_already_in_order_plans_no_writes_and_opens_no_gate(home):
    cfg, folder_id, _source_id = home
    _make(cfg, folder_id, "2026-10", "2026-09", "Undated")
    before = _playlist_rows(cfg)
    code, acted = drive(VERB)
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert "nothing was written" in _note(acted, order_cli.IN_ORDER)
    assert acted["data"]["totals"]["moves"] == 0
    assert {item["action"] for item in acted["data"]["items"]} == {"stay"}
    assert _playlist_rows(cfg) == before


def test_a_second_run_after_the_order_asks_nothing(home):
    cfg, folder_id, _source_id = home
    _make(cfg, folder_id, "2026-08", "2026-10")
    acted, _shown = _approved()
    code, again = drive(VERB)
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"


def test_a_non_month_playlist_keeps_its_relative_place_after_the_months(home):
    cfg, folder_id, _source_id = home
    _make(cfg, folder_id, "Zeta", "2026-08")
    _make(cfg, folder_id, "Crates", kind="folder")
    _make(cfg, folder_id, "2026-Q2", "Undated", "Alpha", "2026-10")
    acted, _shown = _approved()
    assert _order(cfg, folder_id) == [
        SOURCE, "2026-10", "2026-08", "Undated", "Zeta", "Crates", "2026-Q2", "Alpha"
    ]


def test_a_folder_named_as_a_month_is_not_a_month(home):
    cfg, folder_id, _source_id = home
    _make(cfg, folder_id, "2026-12", kind="folder")
    _make(cfg, folder_id, "2026-09")
    planned = order_cli.planned(cfg, source=SOURCE)
    assert [(one.name, one.kind) for one in planned.children] == [
        (SOURCE, "source"), ("2026-09", "month"), ("2026-12", "other"),
    ]


def test_a_soft_deleted_month_is_neither_moved_nor_counted(home):
    cfg, folder_id, _source_id = home
    made = _make(cfg, folder_id, "2026-07", "2026-08", "2026-09")
    _mark_removed(cfg, made["2026-07"])
    removed_row = [row for row in _playlist_rows(cfg) if str(row[0]) == made["2026-07"]]
    planned = order_cli.planned(cfg, source=SOURCE)
    assert [one.name for one in planned.children] == [SOURCE, "2026-09", "2026-08"]
    assert made["2026-07"] not in {one.row for one in planned.children}
    acted, _shown = _approved()
    assert _order(cfg, folder_id) == [SOURCE, "2026-09", "2026-08"]
    assert [row for row in _playlist_rows(cfg) if str(row[0]) == made["2026-07"]] == removed_row
    assert acted["data"]["totals"]["count"] == 3


def test_two_all_favorites_refuses_by_name_and_writes_nothing(home):
    cfg, folder_id, _source_id = home
    _make(cfg, folder_id, "2026-08", "2026-10")
    _make(cfg, "", SOURCE)
    before = _playlist_rows(cfg)
    code, refused = drive(VERB)
    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == placement.SOURCE_MISSING
    assert "2 live playlists" in refused["cause"]["message"]
    assert _playlist_rows(cfg) == before


def test_no_favorites_folder_refuses_by_name_and_writes_nothing(native_library):
    cfg, _root_id = native_library
    _folder_id, source_id = _home(cfg, folder=False)
    _make(cfg, "", "2026-08", "2026-10")
    before = _playlist_rows(cfg)
    code, refused = drive(VERB)
    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == placement.SOURCE_MISSING
    assert "playlist root" in refused["cause"]["message"]
    assert refused["cause"]["detail"]["row"] == source_id
    assert _playlist_rows(cfg) == before


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(home):
    cfg, folder_id, _source_id = home
    _make(cfg, folder_id, "2026-08", "2026-10")
    session.ack_path(cfg).unlink()
    code, refused = drive(VERB)
    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert "gate" not in (refused.get("cause") or {}).get("detail", {})


def test_a_folder_that_changed_after_the_approval_is_refused_and_nothing_is_written(home):
    cfg, folder_id, _source_id = home
    _make(cfg, folder_id, "2026-08", "2026-10")
    approved = order_cli.planned(cfg, source=SOURCE)
    _make(cfg, folder_id, "2026-09")
    before = _playlist_rows(cfg)
    with pytest.raises(CratekitError) as caught:
        order_cli.written(cfg, approved, source=SOURCE)
    assert caught.value.cause.reason == "decision-stale"
    assert _playlist_rows(cfg) == before


def test_the_digest_moves_when_the_target_order_moves_and_not_otherwise(home):
    cfg, folder_id, _source_id = home
    made = _make(cfg, folder_id, "2026-08", "2026-10", "Zeta")
    first = order_cli.planned(cfg, source=SOURCE)
    # Shuffled by hand, the same target: the same digest.
    eight, ten = made["2026-08"], made["2026-10"]
    _set(cfg, "Seq", **{eight: _seq(cfg, ten), ten: _seq(cfg, eight)})
    shuffled = order_cli.planned(cfg, source=SOURCE)
    assert [one.name for one in shuffled.now] == [SOURCE, "2026-10", "2026-08", "Zeta"]
    assert shuffled.digest == first.digest
    # A month made: another target, another digest.
    _make(cfg, folder_id, "2026-09")
    grown = order_cli.planned(cfg, source=SOURCE)
    assert grown.digest != first.digest
    # Two others swapped: their relative order is the target's, so another digest.
    other = _make(cfg, folder_id, "Alpha")
    with_alpha = order_cli.planned(cfg, source=SOURCE)
    zeta, alpha = made["Zeta"], other["Alpha"]
    _set(cfg, "Seq", **{zeta: _seq(cfg, alpha), alpha: _seq(cfg, zeta)})
    assert order_cli.planned(cfg, source=SOURCE).digest != with_alpha.digest


def test_the_order_takes_the_positions_the_live_children_hold_and_no_other(home):
    """Gaps kept, a shared position lifted, a removed row's position untouched."""
    cfg, folder_id, source_id = home
    made = _make(cfg, folder_id, "2026-08", "Gone", "2026-09", "2026-10")
    _mark_removed(cfg, made["Gone"])
    seqs = {source_id: 1, made["2026-08"]: 4, made["Gone"]: 7, made["2026-09"]: 9, made["2026-10"]: 9}
    _set(cfg, "Seq", **seqs)
    acted, _shown = _approved()
    assert _order(cfg, folder_id) == [SOURCE, "2026-10", "2026-09", "2026-08"]
    assert [_seq(cfg, made[name]) for name in ("2026-10", "2026-09", "2026-08")] == [4, 9, 10]
    assert _seq(cfg, source_id) == 1
    assert _seq(cfg, made["Gone"]) == 7


def test_only_a_row_whose_position_changes_is_written(home):
    cfg, folder_id, _source_id = home
    made = _make(cfg, folder_id, "2026-10", "2026-08", "2026-09", "Undated")
    rows = {str(row[0]): row for row in _playlist_rows(cfg)}
    acted, _shown = _approved()
    after = {str(row[0]): row for row in _playlist_rows(cfg)}
    assert after[made["2026-10"]] == rows[made["2026-10"]]
    assert after[made["Undated"]] == rows[made["Undated"]]
    assert after[made["2026-08"]] != rows[made["2026-08"]]
    assert after[made["2026-09"]] != rows[made["2026-09"]]
    assert acted["data"]["totals"]["moved"] == 2


def test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites(home, silence):
    cfg, folder_id, _source_id = home
    _make(cfg, folder_id, "2026-10", "2026-09", "Undated", "Zeta")
    hearts_swept(cfg, {"Hearted": NOV})
    _stage(cfg, silence, "Hearted")
    _landed()
    assert _order(cfg, folder_id) == [SOURCE, "2026-11", "2026-10", "2026-09", "Undated", "Zeta"]
    code, again = drive(VERB)
    assert code == int(ExitCode.OK) and again["outcome"] == "no_op", again


def test_the_splits_months_land_in_order(home, silence, monkeypatch):
    cfg, folder_id, _source_id = home
    _make(cfg, folder_id, "2026-09")
    _landed_hearts(cfg, silence, {"One": OCT.format(day=1), "Two": NOV})
    _quarter(cfg, folder_id, "2026-Q4", "One", "Two")
    _account(monkeypatch, {})
    acted, _shown = _split_approved()
    assert _order(cfg, folder_id) == [SOURCE, "2026-11", "2026-10", "2026-09"]


_P_COLS = ("ID", "Seq", "Name", "Attribute", "ParentID", rb_writer.SOFT_DELETE_COLUMN, "updated_at")
_M_COLS = ("ID", "PlaylistID", "ContentID", "TrackNo", rb_writer.SOFT_DELETE_COLUMN)


def _tables(playlists: dict, memberships: dict | None = None, content: dict | None = None):
    return rb_writer.NodeTables(
        content=content or {"c1": "x"}, playlists=playlists,
        memberships=memberships if memberships is not None else {"m1": ("m1", "a", "c1", 1, 0)},
        playlist_columns=_P_COLS, membership_columns=_M_COLS,
    )


_BEFORE = {
    "f": ("f", 1, "Favorites", 1, "root", 0, "t0"), "a": ("a", 1, SOURCE, 0, "f", 0, "t0"),
    "x": ("x", 2, "2026-08", 0, "f", 0, "t0"), "y": ("y", 3, "2026-09", 0, "f", 0, "t0"),
}
_AFTER = {
    **_BEFORE, "x": ("x", 3, "2026-08", 0, "f", 0, "t1"), "y": ("y", 2, "2026-09", 0, "f", 0, "t1"),
}


def test_the_planned_order_is_confined():
    assert order.order_violations(
        _tables(_BEFORE), _tables(_AFTER), folder_id="f", seated={"x": 3, "y": 2}
    ) == []


@pytest.mark.parametrize(
    ("after", "memberships", "content", "seated", "expected"),
    [
        ({**_AFTER, "y": ("y", 2, "renamed", 0, "f", 0, "t1")}, None, None, {"x": 3, "y": 2}, "['Name']"),
        ({**_AFTER, "y": ("y", 2, "2026-09", 0, "g", 0, "t1")}, None, None, {"x": 3, "y": 2}, "not live under"),
        ({**_AFTER, "y": ("y", 2, "2026-09", 0, "f", 1, "t1")}, None, None, {"x": 3, "y": 2}, "not live under"),
        (_BEFORE, None, None, {"x": 3, "y": 2}, "at the planned position 3"),
        (_AFTER, None, None, {"x": 3}, "row 'y' changed ['Seq', 'updated_at']"),
        ({**_AFTER, "a": ("a", 4, SOURCE, 0, "f", 0, "t0")}, None, None, {"x": 3, "y": 2}, "row 'a' changed ['Seq']"),
        ({**_AFTER, "z": ("z", 9, "new", 0, "f", 0, "t1")}, None, None, {"x": 3, "y": 2}, "unplanned"),
        ({k: v for k, v in _AFTER.items() if k != "a"}, None, None, {"x": 3, "y": 2}, "disappeared"),
        (_AFTER, {"m1": ("m1", "a", "c1", 1, 1)}, None, {"x": 3, "y": 2}, "changes no membership"),
        (_AFTER, {}, None, {"x": 3, "y": 2}, "added or disappeared"),
        (_AFTER, None, {"c1": "y"}, {"x": 3, "y": 2}, "touches no track"),
    ],
    ids=[
        "renamed", "reparented", "removed", "not-made", "unplanned-move", "source-moved",
        "row-added", "row-gone", "membership-changed", "membership-gone", "content-changed",
    ],
)
def test_an_order_reaching_what_it_did_not_plan_is_a_violation(after, memberships, content, seated, expected):
    violations = order.order_violations(
        _tables(_BEFORE), _tables(after, memberships, content), folder_id="f", seated=seated,
    )
    assert any(expected in one for one in violations), violations


def test_the_writer_refuses_an_order_that_reached_a_name(home, monkeypatch):
    cfg, folder_id, _source_id = home
    _make(cfg, folder_id, "2026-08", "2026-10")
    approved = order_cli.planned(cfg, source=SOURCE)
    before = _playlist_rows(cfg)
    real_seat = placement.seat
    def seat_and_rename(db, rows, **kwargs):
        moved = real_seat(db, rows, **kwargs)
        rows[-1].Name = "renamed"
        return moved
    monkeypatch.setattr(placement, "seat", seat_and_rename)
    with pytest.raises(CratekitError) as caught:
        order_cli.written(cfg, approved, source=SOURCE)
    assert caught.value.cause.reason == "whitelist-violation"
    assert "['Name']" in caught.value.cause.message
    assert _playlist_rows(cfg) == before


def test_the_read_back_names_a_folder_that_does_not_read_in_the_planned_order(home):
    cfg, folder_id, _source_id = home
    made = _make(cfg, folder_id, "2026-10", "2026-08")
    with _db(cfg) as handle:
        planned = order.plan(handle, source=SOURCE)
        assert order._read_back(handle, planned) == ()
    _set(cfg, "Seq", **{made["2026-08"]: 2, made["2026-10"]: 3})
    with _db(cfg) as handle:
        (said,) = order._read_back(handle, planned)
    assert said == (
        f"the folder reads {SOURCE}, 2026-08, 2026-10 and the plan was {SOURCE}, 2026-10, 2026-08"
    )
    done = order.Ordered(moved=(), order=(), session_id="s1", disagreements=(said,))
    with pytest.raises(CratekitError) as caught:
        order.assert_read_back(done)
    assert caught.value.cause.reason == "session-committed-unverified"
    assert said in caught.value.cause.message


def test_the_verb_refuses_an_answer_the_read_back_does_not_hold(home, monkeypatch):
    """The verb's own refusal of a disagreeing read back, driven through the gate (M25)."""
    cfg, folder_id, _source_id = home
    _make(cfg, folder_id, "2026-08", "2026-10")
    monkeypatch.setattr(order, "_read_back", lambda _db, _planned: ("the folder reads otherwise",))
    code, acted, _refused = _acts()
    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "session-committed-unverified"
    assert "the folder reads otherwise" in acted["cause"]["message"]
