"""The stamp rekordbox puts on each membership row its Remove from Collection renumbers (U955).

A202 at sitting 104 read rekordbox 7.2.19's own removal column by column: the
row after the removed one moved ``TrackNo``, ``rb_local_usn`` to the final
``localUpdateCount`` and ``updated_at`` to the removal's time, and nothing else.
These read the confinement's rule as pure readings; ``tests/test_sync_removed.py``
drives it on a disposable library.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from cratekit.core import rb_removal, rb_writer
from cratekit.core.rb_removal import RenumberingStamp

STAMP = RenumberingStamp(3047665, "2026-11-23 18:40:01.250 +00:00")
OLD = (3047562, "2026-11-20 09:00:00.000 +00:00")


#: When the plan was read, a little before :data:`STAMP`'s time.
PLANNED = "2026-11-23 18:40:01.000 +00:00"


def _reading(rows, *, moved=None, stamps=None, rest=None, gone=("x",), counter=5, read_at=PLANNED):
    """One membership table: ``rows`` as ``(id, playlist, content, TrackNo)``, the ``gone`` rows out."""
    positions = {key: (playlist, content, number, True, f"rest-{key}") for key, playlist, content, number in rows}
    held = {key: OLD for key, *_ in rows}
    if gone is not None:
        positions = {key: value for key, value in positions.items() if value[1] not in gone}
        held = {key: value for key, value in held.items() if key in positions}
    for key, number in (moved or {}).items():
        playlist, content, _was, live, digest = positions[key]
        positions[key] = (playlist, content, number, live, digest)
    for key, digest in (rest or {}).items():
        playlist, content, number, live, _digest = positions[key]
        positions[key] = (playlist, content, number, live, digest)
    held.update(stamps or {})
    members = {key: f"{value[2]}-{value[4]}-{held[key]}" for key, value in positions.items()}
    contents = {"a": "a", "b": "b"} | ({} if gone is not None else {"x": "x"})
    return rb_writer.DatabaseReading(
        rows={rb_writer.MEMBERSHIP_TABLE: members, rb_writer.CONTENT_TABLE: contents},
        named={
            rb_writer.MEMBERSHIP_TABLE: {key: value[1] for key, value in positions.items()},
            rb_writer.CONTENT_TABLE: dict(contents),
        },
        counter=counter,
        positions=positions,
        stamps=held,
        read_at=read_at,
    )


#: A202's playlist: a real track, the removed throwaway, a second real track.
ROWS = [("p1", "p", "a", 1), ("p2", "p", "x", 2), ("p3", "p", "b", 3), ("s1", "s", "a", 1)]
BEFORE = _reading(ROWS, gone=None)


def _violations(after, stamp=STAMP, **kwargs):
    return rb_writer.collection_removal_violations(BEFORE, after, removed=["x"], stamp=stamp, **kwargs)


def test_the_three_columns_moved_as_rekordbox_moves_them_are_admitted():
    after = _reading(ROWS, moved={"p3": 2}, stamps={"p3": (STAMP.counter, STAMP.at)})
    assert _violations(after) == []


@pytest.mark.parametrize(
    ("stamps", "moved", "found"),
    [
        ({"p3": (OLD[0], STAMP.at)}, {"p3": 2}, "to be stamped rb_local_usn 3047665 from 3047562 and holds 3047562"),
        ({"p3": (STAMP.counter + 1, STAMP.at)}, {"p3": 2}, "holds 3047666"),
        ({"p3": (STAMP.counter, OLD[1])}, {"p3": 2}, "to be stamped updated_at"),
        ({"p3": (STAMP.counter, "2026-11-23 18:40:01.251 +00:00")}, {"p3": 2}, "to be stamped updated_at"),
        ({"p3": (STAMP.counter, STAMP.at)}, {}, "renumbered from 3 to 2 and holds 3"),
        ({"p3": (STAMP.counter, STAMP.at)}, {"p3": 1}, "holds 1"),
    ],
    ids=["usn-unmoved", "usn-wrong", "time-unmoved", "time-wrong", "trackno-unmoved", "trackno-wrong"],
)
def test_a_planned_row_with_any_of_the_three_wrong_or_unmoved_is_refused(stamps, moved, found):
    violations = _violations(_reading(ROWS, moved=moved, stamps=stamps))
    assert any(found in line for line in violations), violations


def test_a_fourth_column_moving_on_a_planned_row_is_refused():
    after = _reading(ROWS, moved={"p3": 2}, stamps={"p3": (STAMP.counter, STAMP.at)}, rest={"p3": "UUID moved"})
    violations = _violations(after)
    assert any("other than TrackNo, rb_local_usn and updated_at" in line for line in violations), violations


@pytest.mark.parametrize("key", ["p1", "s1"])
def test_an_unplanned_row_whose_count_moves_is_refused(key):
    """The row before the removed one, and a row of a playlist it was never on."""
    after = _reading(ROWS, moved={"p3": 2}, stamps={"p3": (STAMP.counter, STAMP.at), key: (STAMP.counter, OLD[1])})
    violations = _violations(after)
    assert any(f"{key!r} changed" in line for line in violations), violations


def _planned_at(read_at):
    """BEFORE, its plan read at ``read_at``."""
    return _reading(ROWS, gone=None, read_at=read_at)


STAMPED = {"p3": (STAMP.counter, STAMP.at)}


def test_a_stamp_earlier_than_the_plan_is_refused():
    after = _reading(ROWS, moved={"p3": 2}, stamps=STAMPED)
    later = _planned_at("2026-11-23 18:40:01.251 +00:00")
    violations = rb_writer.collection_removal_violations(later, after, removed=["x"], stamp=STAMP)
    assert any("is earlier than the plan" in line for line in violations), violations


def test_a_stamp_at_the_plan_s_own_instant_is_forward():
    """A held clock, as the behaviour scenarios hold it, reads the plan and the stamp at one instant."""
    after = _reading(ROWS, moved={"p3": 2}, stamps=STAMPED)
    same = _planned_at(STAMP.at)
    assert rb_writer.collection_removal_violations(same, after, removed=["x"], stamp=STAMP) == []


@pytest.mark.parametrize(
    "held",
    [None, "2026-11-23 18:40:01 +00:00", "2031-01-01 00:00:00.000 +00:00", "not a time", "2026-11-20 09:00"],
    ids=["null", "the-stamp-s-moment", "a-later-clock", "garbage", "no-offset"],
)
def test_the_time_a_row_held_is_never_read_against_another_clock_only_left_unmoved(held):
    """A row's old ``updated_at`` may come from another machine; only an unmoved text refuses."""
    before = _reading(ROWS, gone=None)
    before = rb_writer.DatabaseReading(
        before.rows, before.named, before.counter, before.positions, {**before.stamps, "p3": (OLD[0], held)}, PLANNED
    )
    after = _reading(ROWS, moved={"p3": 2}, stamps=STAMPED)
    assert rb_writer.collection_removal_violations(before, after, removed=["x"], stamp=STAMP) == []
    unmoved = _reading(ROWS, moved={"p3": 2}, stamps={"p3": (STAMP.counter, STAMP.at)})
    unmoved_before = rb_writer.DatabaseReading(
        before.rows, before.named, before.counter, before.positions, {**before.stamps, "p3": (OLD[0], STAMP.at)}, PLANNED
    )
    violations = rb_writer.collection_removal_violations(unmoved_before, unmoved, removed=["x"], stamp=STAMP)
    assert any("was to be stamped updated_at" in line for line in violations), violations


@pytest.mark.parametrize("read_at", [None, "not a time"], ids=["unread", "garbage"])
def test_a_plan_with_no_readable_time_cannot_say_forward_and_refuses(read_at):
    after = _reading(ROWS, moved={"p3": 2}, stamps=STAMPED)
    violations = rb_writer.collection_removal_violations(_planned_at(read_at), after, removed=["x"], stamp=STAMP)
    assert any("cannot be read as a time" in line for line in violations), violations


@pytest.mark.parametrize(
    "text",
    ["2026-11-20 09:00:00.000 -05:00 (Eastern Standard Time)", "2026-11-20T14:00:00Z", "2026-11-20 14:00 +00:00"],
    ids=["named-zone", "zulu", "whole-minute"],
)
def test_a_time_in_the_forms_a_library_holds_reads_as_one_moment(text):
    assert rb_removal.stamp_moment(text) == datetime(2026, 11, 20, 14, 0, tzinfo=timezone.utc)


def test_a_reading_carries_the_time_it_was_read(monkeypatch):
    """``database_reading`` stamps its own time, which the stamp is held after."""
    import sqlite3

    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    monkeypatch.setattr(rb_removal, "_now", lambda: datetime(2026, 11, 23, 18, 40, 1, 7000, tzinfo=timezone.utc))
    engine = create_engine("sqlite://", creator=lambda: sqlite3.connect(":memory:"))

    class Handle:
        session = Session(engine)

    assert rb_removal.database_reading(Handle()).read_at == "2026-11-23 18:40:01.007 +00:00"


def test_without_a_stamp_the_planned_row_moves_trackno_alone():
    """The rule before U955, kept for a caller that plans no stamp; the removal always plans one."""
    assert _violations(_reading(ROWS, moved={"p3": 2}), stamp=None) == []
    stamped = _reading(ROWS, moved={"p3": 2}, stamps={"p3": (STAMP.counter, STAMP.at)})
    violations = _violations(stamped, stamp=None)
    assert any("other than TrackNo, and a renumbering" in line for line in violations), violations


def test_a_read_back_refuses_a_count_other_than_the_stamp():
    after = _reading(ROWS, moved={"p3": 2}, stamps={"p3": (STAMP.counter, STAMP.at)}, counter=STAMP.counter)
    assert _violations(after, committed=True) == []
    past = _reading(ROWS, moved={"p3": 2}, stamps={"p3": (STAMP.counter, STAMP.at)}, counter=STAMP.counter + 1)
    violations = _violations(past, committed=True)
    assert any("reads 3047666 after the commit" in line for line in violations), violations
    # A removal that renumbered nothing has no stamp to read the count against.
    lone = [("q1", "q", "a", 1), ("q2", "q", "x", 2)]
    before = _reading(lone, gone=None)
    after = _reading(lone, counter=STAMP.counter + 9)
    assert rb_writer.collection_removal_violations(before, after, removed=["x"], stamp=STAMP, committed=True) == []


@pytest.mark.parametrize(
    ("moment", "text"),
    [
        (datetime(2026, 11, 23, 18, 40, 1, 250999, tzinfo=timezone.utc), "2026-11-23 18:40:01.250 +00:00"),
        (datetime(2026, 11, 23, 18, 40, 1, 0, tzinfo=timezone.utc), "2026-11-23 18:40:01.000 +00:00"),
        (
            datetime(2026, 11, 23, 13, 40, 1, 7000, tzinfo=timezone(timedelta(hours=-5))),
            "2026-11-23 18:40:01.007 +00:00",
        ),
    ],
    ids=["milliseconds-cut", "whole-second", "other-zone"],
)
def test_a_stamp_s_time_is_rekordbox_s_text_form_in_utc(moment, text):
    assert rb_removal.stamp_time(moment) == text
    assert rb_removal.stamp_moment(text) == moment.replace(microsecond=moment.microsecond // 1000 * 1000)


def test_a_stamp_s_time_refuses_a_moment_with_no_zone():
    with pytest.raises(ValueError, match="time zone"):
        rb_removal.stamp_time(datetime(2026, 11, 23, 18, 40, 1))


def test_the_removal_stamp_takes_the_clock_and_the_count_the_commit_will_leave(monkeypatch):
    from pyrekordbox.db6.registry import RekordboxAgentRegistry

    class Handle:
        def get_local_usn(self):
            return 100

    monkeypatch.setattr(RekordboxAgentRegistry, "__update_sequence__", [object(), object(), object()])
    monkeypatch.setattr(rb_removal, "_now", lambda: datetime(2026, 11, 23, 18, 40, 1, 250000, tzinfo=timezone.utc))
    assert rb_removal.removal_stamp(Handle()) == RenumberingStamp(103, "2026-11-23 18:40:01.250 +00:00")


def test_a_count_that_cannot_be_read_refuses_and_rolls_back(monkeypatch):
    from pyrekordbox.db6.registry import RekordboxAgentRegistry

    rolled: list[bool] = []

    class Handle:
        def get_local_usn(self):
            return None

        def rollback(self):
            rolled.append(True)

    monkeypatch.setattr(RekordboxAgentRegistry, "__update_sequence__", [])
    with pytest.raises(rb_writer.RekordboxUnavailable, match="cannot be said"):
        rb_removal.counter_at_commit(Handle())
    assert rolled == [True]
