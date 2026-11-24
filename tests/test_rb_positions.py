"""Every playlist this product writes stays numbered 1 to N (U958).

rekordbox's Remove from Playlist takes the row whose ``TrackNo`` equals the shown
position (sitting 107, A218), so a membership removal closes up the playlist it
touched at the commit: the live rows 1 to N in their order, the marked rows at 0,
stamped as U955 stamps a renumbered row and proven from SQL. The rule is read as
pure readings first, then driven through ``commit_guarded`` on a disposable library.
"""

from __future__ import annotations

import sqlite3
from contextlib import closing

import pytest

from cratekit.core import rb_positions, rb_writer
from cratekit.core.rb_removal import RenumberingStamp
from tests.test_rb_writer_db import _build_disposable_database
from tests.test_rb_writer_db import _rekordbox_closed as _rekordbox_closed  # noqa: PLC0414
from tests.test_rb_writer_db import cloud_sync_off as cloud_sync_off  # noqa: PLC0414
from tests.test_rb_writer_db import library as library  # noqa: PLC0414

W = rb_writer
TRACKS = tuple(str(n) for n in range(1, 9))


# ── the rule, pure ────────────────────────────────────────────────────────────


def _rows(*held, playlist="p"):
    """``(id, TrackNo, live)`` triples as the rule's rows, all in one playlist."""
    return [(key, playlist, number, live) for key, number, live in held]


def test_a_playlist_already_numbered_one_to_n_moves_nothing():
    rows = _rows(("a", 1, True), ("b", 2, True), ("c", 3, True), ("m", 0, False), ("n", None, False))
    assert W.contiguous_positions(rows) == {}
    assert W.numbering(rows)["p"].contiguous


def test_a_gap_in_the_middle_closes_up_in_order():
    rows = _rows(("a", 1, True), ("b", 2, True), ("d", 4, True), ("e", 5, True))
    assert W.contiguous_positions(rows) == {"d": ("p", 4, 3), "e": ("p", 5, 4)}


def test_a_marked_row_goes_to_zero_and_is_never_counted_as_a_place():
    rows = _rows(("a", 1, True), ("x", 2, False), ("c", 3, True), ("y", 9, False))
    assert W.contiguous_positions(rows) == {
        "c": ("p", 3, 2),
        "x": ("p", 2, W.MARKED_PLACE),
        "y": ("p", 9, W.MARKED_PLACE),
    }


def test_a_gap_and_an_old_marked_row_in_one_playlist_come_out_one_to_n_in_order():
    """Sitting 107's shape: live rows run 1 to 557 with 548 missing, a marked row at 55."""
    live = [(f"r{n:03d}", n, True) for n in range(1, 558) if n != 548]
    rows = _rows(*live, ("m055", 55, False))
    moved = W.contiguous_positions(rows)
    assert moved["m055"] == ("p", 55, 0)
    assert moved["r557"] == ("p", 557, 556) and moved["r549"] == ("p", 549, 548)
    assert "r547" not in moved and len(moved) == 10
    after = {key: moved.get(key, ("p", number, number))[2] for key, number, _live in [*live, ("m055", 55, False)]}
    assert sorted(after[key] for key, _n, _l in live) == list(range(1, 557))


def test_two_live_rows_tied_on_one_place_come_out_apart_the_lower_row_id_first():
    """R-1852: a tie is read in row id order, as every reader here orders it."""
    rows = _rows(("a", 1, True), ("c2", 2, True), ("c1", 2, True), ("d", 3, True))
    assert W.contiguous_positions(rows) == {"c2": ("p", 2, 3), "d": ("p", 3, 4)}


def test_each_playlist_is_numbered_on_its_own():
    rows = [*_rows(("a", 2, True), ("b", 3, True)), *_rows(("c", 1, True), ("d", 5, True), playlist="q")]
    assert W.contiguous_positions(rows) == {
        "a": ("p", 2, 1), "b": ("p", 3, 2), "d": ("q", 5, 2),
    }


@pytest.mark.parametrize(
    "bad", [("u", 2, None), ("v", None, True)], ids=["unreadable-marker", "live-with-no-number"]
)
def test_a_playlist_whose_order_cannot_be_said_is_left_whole_and_named(bad):
    rows = [*_rows(("a", 1, True), ("c", 3, True), bad), *_rows(("d", 2, True), playlist="q")]
    assert W.unplaceable(rows) == {"p": [bad[0]]}
    assert W.contiguous_positions(rows) == {"d": ("q", 2, 1)}
    assert not W.numbering(rows)["p"].contiguous


def test_the_numbering_reads_count_and_reach_for_the_plan_and_the_doctor():
    rows = _rows(("a", 1, True), ("c", 3, True), ("x", 2, False), ("y", 0, False))
    read = W.numbering(rows)["p"]
    assert (read.rows, read.lowest, read.highest, read.marked_placed, read.contiguous) == (2, 1, 3, 1, False)
    empty = W.numbering(_rows(("x", 4, False)))["p"]
    assert (empty.rows, empty.lowest, empty.highest, empty.contiguous) == (0, None, None, True)


# ── the proof, pure ───────────────────────────────────────────────────────────

COLUMNS = ("ID", "PlaylistID", "ContentID", "TrackNo", "rb_local_deleted", "rb_local_usn", "updated_at", "UUID")
STAMP = RenumberingStamp(120, "2026-11-24 18:00:00.000 +00:00")
OLD = (101, "2026-11-01 09:00:00")


def _reading(rows, counter=100):
    return rb_positions.GapReading(
        COLUMNS,
        {key: (key, playlist, content, number, marker, *stamped, f"u-{key}") for key, playlist, content, number, marker, *stamped in rows},
        counter,
    )


BEFORE_ROWS = [
    ("a", "p", "1", 1, 0, *OLD),
    ("x", "p", "2", 2, 1, *OLD),
    ("c", "p", "3", 3, 0, *OLD),
]
PLANNED = {"c": ("p", 3, 2), "x": ("p", 2, 0)}


def _after(**changes):
    rows = {row[0]: list(row) for row in BEFORE_ROWS}
    rows["c"][3:4] = [2]
    rows["c"][5:7] = [STAMP.counter, STAMP.at]
    rows["x"][3:4] = [0]
    for key, values in changes.items():
        for at, value in values.items():
            rows[key][at] = value
    return _reading([tuple(row) for row in rows.values()])


def _violations(after):
    return W.gap_violations(_reading(BEFORE_ROWS), after, planned=PLANNED, stamp=STAMP)


def test_the_planned_closing_up_reads_clean():
    assert _violations(_after()) == []


@pytest.mark.parametrize(
    ("changes", "found"),
    [
        ({"c": {3: 3}}, "was to move from 3 to 2 and holds 3"),
        ({"c": {5: OLD[0]}}, "stamped rb_local_usn 120 and holds 101"),
        ({"c": {6: OLD[1]}}, "stamped updated_at"),
        ({"c": {2: "8"}}, "in a column other than TrackNo"),
        ({"a": {6: STAMP.at}}, "'a' changed, and the closing up planned no move of it"),
        ({"x": {3: 2}}, "was to move from 2 to 0 and holds 2"),
        # Review round one, B1: a marked row's removal time is what sync pair reads.
        ({"x": {6: STAMP.at}}, "marked djmdSongPlaylist row 'x' changed in a column other than TrackNo"),
        ({"x": {5: STAMP.counter}}, "marked djmdSongPlaylist row 'x' changed in a column other than TrackNo"),
    ],
    ids=[
        "unmoved", "count-unstamped", "time-unstamped", "fourth-column", "unplanned-row",
        "marked-left", "marked-time-restamped", "marked-count-restamped",
    ],
)
def test_every_move_the_plan_does_not_explain_is_named(changes, found):
    violations = _violations(_after(**changes))
    assert any(found in line for line in violations), violations


def test_a_row_added_or_gone_and_a_playlist_left_gapped_are_named():
    after = _after()
    gone = rb_positions.GapReading(after.columns, {k: v for k, v in after.rows.items() if k != "a"}, 100)
    assert any("'a' was added or disappeared" in line for line in _violations(gone))
    gapped = _reading([("a", "p", "1", 1, 0, *OLD), ("c", "p", "3", 3, 0, *OLD)])
    violations = W.gap_violations(gapped, gapped, planned={}, stamp=STAMP)
    assert any("does not read 1 to N" in line for line in violations), violations


# ── driven through the commit, on a disposable library ────────────────────────


@pytest.fixture
def db(library, cloud_sync_off):
    """A disposable library holding eight tracks, opened through the gate."""
    path = library / "db" / "master.db"
    _build_disposable_database(path)
    with closing(sqlite3.connect(path)) as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO djmdContent (ID, Title, rb_local_deleted) VALUES (?, ?, 0)",
            [(key, f"track {key}") for key in TRACKS],
        )
        conn.commit()
    handle = W.open_db(path, unlock=False)
    try:
        yield handle
    finally:
        W.close_db(handle)


def _playlist(db, *tracks, name="a playlist"):
    folder = W.ensure_folder(db, "a folder")
    playlist = W.ensure_playlist(db, name, folder)
    W.add_memberships(db, playlist, tracks)
    W.commit_guarded(db)
    return playlist


def _sql(db, statement, *params):
    db.session.expire_all()
    return db.session.execute(__import__("sqlalchemy").text(statement), dict(enumerate(params))).fetchall()


def _members(db, playlist):
    """``{content id: (TrackNo, marked, rb_local_usn, updated_at)}`` read from SQL."""
    from sqlalchemy import text

    db.session.expire_all()
    rows = db.session.execute(
        text(
            "SELECT ContentID, TrackNo, rb_local_deleted, rb_local_usn, updated_at "
            "FROM djmdSongPlaylist WHERE PlaylistID = :p"
        ),
        {"p": str(playlist.ID)},
    ).fetchall()
    return {str(row[0]): (row[1], row[2], row[3], row[4]) for row in rows}


def _live_order(db, playlist):
    held = _members(db, playlist)
    return [key for key, value in sorted(held.items(), key=lambda kv: kv[1][0]) if not value[1]]


def _count(db):
    from sqlalchemy import text

    return db.session.execute(
        text("SELECT int_1 FROM agentRegistry WHERE registry_id = 'localUpdateCount'")
    ).scalar()


def _set(db, playlist, **numbers):
    """Put tracks at numbers by SQL, committed, as an earlier writer left them."""
    from sqlalchemy import text

    for content, number in numbers.items():
        db.session.execute(
            text("UPDATE djmdSongPlaylist SET TrackNo = :n WHERE PlaylistID = :p AND ContentID = :c"),
            {"n": number, "p": str(playlist.ID), "c": content.lstrip("t")},
        )
    db.session.commit()


def _remove(db, playlist, *tracks):
    marked = W.remove_memberships(db, playlist, tracks)
    W.commit_guarded(db, removals=(W.MEMBERSHIP_TABLE,))
    return marked


@pytest.mark.parametrize(
    ("removed", "left"),
    [
        (("3",), ["1", "2", "4", "5"]),
        (("5",), ["1", "2", "3", "4"]),
        (("2", "4"), ["1", "3", "5"]),
    ],
    ids=["the-middle", "the-end", "two-rows"],
)
def test_a_removal_leaves_the_playlist_one_to_n_in_its_old_order(db, removed, left):
    playlist = _playlist(db, "1", "2", "3", "4", "5")
    assert _remove(db, playlist, *removed) == list(removed)
    held = _members(db, playlist)
    assert _live_order(db, playlist) == left
    assert sorted(held[key][0] for key in left) == list(range(1, len(left) + 1))
    for key in removed:
        assert held[key][:2] == (W.MARKED_PLACE, 1), key


def test_a_moved_row_is_stamped_with_the_count_the_commit_left_and_an_unmoved_one_is_not(db):
    playlist = _playlist(db, "1", "2", "3", "4")
    before = _members(db, playlist)
    _remove(db, playlist, "2")
    after, count = _members(db, playlist), _count(db)
    for key in ("3", "4"):
        assert after[key][2] == count and after[key][3] != before[key][3], key
        assert rb_writer.stamp_moment(after[key][3]) is not None
    assert after["1"] == before["1"]


def test_a_playlist_with_an_old_gap_and_an_old_marked_row_comes_out_one_to_n(db):
    playlist = _playlist(db, "1", "2", "3", "4", "5", "6")
    _set(db, playlist, t4=7, t5=9, t6=12)
    from sqlalchemy import text

    db.session.execute(
        text(
            "UPDATE djmdSongPlaylist SET rb_local_deleted = 1, updated_at = '2026-11-01 09:00:00', "
            "rb_local_usn = 7 WHERE PlaylistID = :p AND ContentID = '3'"
        ),
        {"p": str(playlist.ID)},
    )
    db.session.commit()
    _remove(db, playlist, "5")
    held = _members(db, playlist)
    assert _live_order(db, playlist) == ["1", "2", "4", "6"]
    assert [held[key][0] for key in ("1", "2", "4", "6")] == [1, 2, 3, 4]
    assert held["3"][:2] == (0, 1) and held["5"][:2] == (0, 1)
    # Review round one, B1: the older removal keeps its own moment and count,
    # which sync pair reads against the account's changes.
    assert held["3"][2:] == (7, "2026-11-01 09:00:00")


def test_a_closing_up_that_moved_a_row_other_than_planned_refuses_and_writes_nothing(db, monkeypatch):
    """The proof from SQL is what refuses, not the write's own row count."""
    playlist = _playlist(db, "1", "2", "3", "4")
    before = _members(db, playlist)
    real = rb_writer.renumber_memberships

    def and_one_more(handle, moved, **kwargs):
        real(handle, moved, **kwargs)
        from sqlalchemy import text

        handle.session.execute(
            text("UPDATE djmdSongPlaylist SET TrackNo = 9 WHERE PlaylistID = :p AND ContentID = '1'"),
            {"p": str(playlist.ID)},
        )

    monkeypatch.setattr(rb_writer, "renumber_memberships", and_one_more)
    W.remove_memberships(db, playlist, ["2"])
    with pytest.raises(W.RekordboxUnavailable, match="closing up the numbers"):
        W.commit_guarded(db, removals=(W.MEMBERSHIP_TABLE,))
    assert _members(db, playlist) == before
    assert W.touched(db) == frozenset()


def test_two_live_rows_tied_on_one_place_come_out_apart_in_row_id_order(db):
    playlist = _playlist(db, "1", "2", "3", "4")
    _set(db, playlist, t3=2, t4=5)
    ids = {
        str(row[1]): str(row[0])
        for row in _sql(db, "SELECT ID, ContentID FROM djmdSongPlaylist")
    }
    _remove(db, playlist, "1")
    held = _members(db, playlist)
    first, second = sorted(("2", "3"), key=lambda key: ids[key])
    assert (held[first][0], held[second][0], held["4"][0]) == (1, 2, 3)


def test_a_playlist_already_one_to_n_after_the_removal_moves_no_live_row(db):
    playlist = _playlist(db, "1", "2", "3")
    before = _members(db, playlist)
    _remove(db, playlist, "3")
    after = _members(db, playlist)
    assert after["1"] == before["1"] and after["2"] == before["2"]


def test_a_rolled_back_removal_leaves_nothing_for_a_later_commit_to_close_up(db):
    playlist = _playlist(db, "1", "2", "3")
    _set(db, playlist, t3=7)
    W.remove_memberships(db, playlist, ["1"])
    assert W.touched(db) == {str(playlist.ID)}
    db.rollback()
    assert W.touched(db) == frozenset()
    W.commit_guarded(db)
    held = _members(db, playlist)
    assert [held[key][0] for key in ("1", "2", "3")] == [1, 2, 7]


def test_a_refused_commit_leaves_nothing_recorded(db, monkeypatch):
    playlist = _playlist(db, "1", "2", "3")
    W.remove_memberships(db, playlist, ["1"])
    with pytest.raises(W.RekordboxUnavailable):
        W.commit_guarded(db)  # no removal admitted: the marker change refuses
    assert W.touched(db) == frozenset()


def test_a_removed_playlist_keeps_every_number(db):
    playlist = _playlist(db, "1", "2", "3")
    _set(db, playlist, t3=7)
    W.remove_playlist_node(db, playlist)
    assert W.touched(db) == frozenset()
    W.commit_guarded(db, removals=(W.MEMBERSHIP_TABLE, W.PLAYLIST_TABLE))
    held = _members(db, playlist)
    assert [held[key][:2] for key in ("1", "2", "3")] == [(1, 1), (2, 1), (7, 1)]


def test_a_touched_playlist_whose_marker_cannot_be_read_refuses_and_writes_nothing(db):
    playlist = _playlist(db, "1", "2", "3", "4")
    _set(db, playlist, t4=9)
    from sqlalchemy import text

    db.session.execute(
        text("UPDATE djmdSongPlaylist SET rb_local_deleted = NULL WHERE PlaylistID = :p AND ContentID = '2'"),
        {"p": str(playlist.ID)},
    )
    db.session.commit()
    before = _members(db, playlist)
    W.remove_memberships(db, playlist, ["1"])
    with pytest.raises(Exception) as raised:
        W.commit_guarded(db, removals=(W.MEMBERSHIP_TABLE,))
    assert "cannot be read" in str(raised.value)
    assert _members(db, playlist) == before


def test_a_closing_up_with_no_other_change_moves_the_count_by_one_and_stamps_it(db):
    """The repair's own commit: nothing removed, the gap closed, the count moved forward once."""
    playlist = _playlist(db, "1", "2", "3")
    _set(db, playlist, t2=4, t3=6)
    count = _count(db)
    W.record_touched(db, playlist.ID)
    W.commit_guarded(db)
    held = _members(db, playlist)
    assert [held[key][0] for key in ("1", "2", "3")] == [1, 2, 3]
    assert _count(db) == count + 1
    assert held["2"][2] == held["3"][2] == count + 1
    # A contiguous playlist recorded again writes nothing and moves no count.
    W.record_touched(db, playlist.ID)
    W.commit_guarded(db)
    assert _members(db, playlist) == held and _count(db) == count + 1


def test_an_add_into_a_playlist_holding_a_marked_row_comes_out_one_to_n(db):
    """Review round two: the binding numbers an append past every row, marked ones included."""
    playlist = _playlist(db, "1", "2", "3", "4")
    _set(db, playlist, t4=6)
    from sqlalchemy import text

    db.session.execute(
        text("UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE PlaylistID = :p AND ContentID = '2'"),
        {"p": str(playlist.ID)},
    )
    db.session.commit()
    assert W.add_memberships(db, playlist, ["5", "6"]) == ["5", "6"]
    W.commit_guarded(db)
    held = _members(db, playlist)
    assert _live_order(db, playlist) == ["1", "3", "4", "5", "6"]
    assert [held[key][0] for key in ("1", "3", "4", "5", "6")] == [1, 2, 3, 4, 5]
    assert held["2"][:2] == (0, 1)


def test_a_closing_up_that_moves_only_marked_rows_takes_no_stamp_and_moves_no_count(db):
    playlist = _playlist(db, "1", "2", "3")
    from sqlalchemy import text

    db.session.execute(
        text(
            "UPDATE djmdSongPlaylist SET rb_local_deleted = 1, rb_local_usn = 7, "
            "updated_at = '2026-11-01 09:00:00' WHERE PlaylistID = :p AND ContentID = '3'"
        ),
        {"p": str(playlist.ID)},
    )
    db.session.commit()
    count, before = _count(db), _members(db, playlist)
    W.record_touched(db, playlist.ID)
    W.commit_guarded(db)
    after = _members(db, playlist)
    assert after["3"] == (0, 1, 7, "2026-11-01 09:00:00")
    assert after["1"] == before["1"] and after["2"] == before["2"]
    assert _count(db) == count
