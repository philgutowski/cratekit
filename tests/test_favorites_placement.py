"""U120: where a landed heart goes, All Favorites and its month.

The engine alone, on the disposable database the genre Favorites suite builds,
with the Favorites folder and its playlists made on the handle. The landing
and the backfill that call it are driven in their own suites.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import re
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from cratekit.core import rb_writer, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.favorites import placeholders, placement
from cratekit.modules.outbound import source as outbound_source
from tests.test_genre_favorites import _members
from tests.test_genre_favorites import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_genre_favorites import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_genre_favorites import cfg as cfg  # noqa: PLC0414
from tests.test_genre_favorites import db as db  # noqa: PLC0414
from tests.test_genre_favorites import library as library  # noqa: PLC0414

DECLARED = taxonomy.default_taxonomy()
SOURCE = DECLARED.sub_class("favorites").signal_playlist
UTC = timezone.utc
NOV = datetime(2026, 11, 3, 12, 0, tzinfo=UTC)
SEP = datetime(2026, 9, 29, 22, 0, tzinfo=UTC)


def _home(db, *members: str, folder: str = "Favorites"):
    """The Favorites folder holding the source, as the source system left it."""
    parent = db.create_playlist_folder(folder) if folder else None
    row = db.create_playlist(SOURCE, parent=parent)
    for content_id in members:
        db.add_to_playlist(row, content_id)
    db.session.commit()
    return parent, row


def _month(db, parent, name: str, *members: str):
    row = db.create_playlist(name, parent=parent)
    for content_id in members:
        db.add_to_playlist(row, content_id)
    db.session.commit()
    return row


def _names_under(db, parent) -> dict[str, str]:
    def here(row) -> bool:
        held = str(getattr(row, "ParentID", "") or "")
        if parent is None:
            return held in rb_writer.ROOT_PARENT_SENTINELS
        return held == str(parent.ID)

    return {
        str(row.Name): str(row.ID)
        for row in db.get_playlist()
        if here(row) and not rb_writer.is_folder(row) and not rb_writer.node_removed(row)
    }


# ---------------------------------------------------------------------------
# The naming rule, shared with the account side
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("moment", "label"),
    [
        (datetime(2026, 1, 1, 0, 0, tzinfo=UTC), "2026-01"),
        (datetime(2026, 3, 31, 23, 59, tzinfo=UTC), "2026-03"),
        (datetime(2026, 4, 1, 0, 0, tzinfo=UTC), "2026-04"),
        (datetime(2026, 10, 20, 9, 0, tzinfo=UTC), "2026-10"),
        (datetime(2026, 12, 31, 23, 59, 59, tzinfo=UTC), "2026-12"),
        # A naive moment is UTC, the source system's rule.
        (datetime(2026, 7, 1), "2026-07"),
        # New York's evening on the last of October is November in UTC.
        (datetime(2026, 10, 31, 21, 0, tzinfo=timezone(timedelta(hours=-5))), "2026-11"),
        # And on the last of December it is the next year's January.
        (datetime(2026, 12, 31, 20, 0, tzinfo=timezone(timedelta(hours=-5))), "2027-01"),
    ],
)
def test_the_month_is_the_utc_month(moment, label):
    assert placeholders.month_of(moment) == label
    assert placeholders.month_label(moment) == label
    assert re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", label)
    assert not placeholders.QUARTER_LABEL.fullmatch(label)


def test_no_quarter_is_named_by_the_placement_any_more():
    """U145: the month rule is the only one, so no quarter playlist is written again."""
    assert not hasattr(placeholders, "quarter_label")
    assert not hasattr(placeholders, "quarter_of")
    assert placeholders.month_of(datetime(2026, 1, 9, tzinfo=UTC)) == "2026-01"
    assert placeholders.QUARTER_LABEL.fullmatch("2026-Q4")


def test_a_heart_with_no_date_goes_to_undated():
    assert placeholders.month_label(None) == placeholders.UNDATED == "Undated"


def test_a_frozen_date_reads_back_and_junk_reads_as_no_date():
    assert placeholders.parse_hearted("2026-10-01T03:00:00+00:00") == datetime(
        2026, 10, 1, 3, tzinfo=UTC
    )
    assert placeholders.parse_hearted("2026-10-01T03:00:00Z") == datetime(2026, 10, 1, 3, tzinfo=UTC)
    assert placeholders.parse_hearted(datetime(2026, 10, 1, 3)) == datetime(2026, 10, 1, 3, tzinfo=UTC)
    assert placeholders.parse_hearted("last tuesday") is None
    assert placeholders.parse_hearted("") is None
    assert placeholders.parse_hearted(None) is None
    assert placeholders.parse_hearted(1700000000) is None


def test_the_account_side_names_keep_their_prefix_and_the_library_side_has_none():
    # The account side keeps the source system's quarters (U145 leaves it).
    assert placeholders.placeholder_name("2026-Q4") == "Favorites 2026-Q4"
    assert placeholders.is_placeholder("Favorites 2026-Q4")
    assert not placeholders.is_placeholder("Favorites 2026-11")
    assert not placeholders.is_placeholder("2026-Q4")
    assert not placeholders.is_placeholder("2026-11")
    assert not placeholders.is_placeholder(placeholders.UNDATED)


# ---------------------------------------------------------------------------
# The source name, chosen once
# ---------------------------------------------------------------------------


def test_the_source_is_the_classs_playlist_else_the_outbound_default():
    assert placement.source_name(DECLARED) == "All Favorites"
    renamed = replace(
        DECLARED,
        sub_classes=tuple(
            replace(c, signal_playlist="Hearts") if c.id == "favorites" else c
            for c in DECLARED.sub_classes
        ),
    )
    assert placement.source_name(renamed) == "Hearts"
    undeclared = replace(
        DECLARED, sub_classes=tuple(c for c in DECLARED.sub_classes if c.id != "favorites")
    )
    assert placement.source_name(undeclared) == outbound_source.DEFAULT_FAVORITES_PLAYLIST


# ---------------------------------------------------------------------------
# The home
# ---------------------------------------------------------------------------


def test_the_home_is_the_one_plain_live_source_its_folder_and_the_months_there(cfg, db):
    folder, source = _home(db, "1")
    q3 = _month(db, folder, "2026-09", "1")
    # A smart playlist of a month's name and a removed one are not there.
    smart = db.create_playlist("2026-Q2", parent=folder)
    smart.Attribute = 4
    gone = db.create_playlist("2026-Q1", parent=folder)
    gone.rb_local_deleted = 1
    db.session.commit()

    home = placement.resolve_home(db, SOURCE)

    assert (home.source_id, home.folder_id, home.folder_name) == (
        str(source.ID),
        str(folder.ID),
        "Favorites",
    )
    assert dict(home.present) == {SOURCE: str(source.ID), "2026-09": str(q3.ID)}
    assert home.identity() == {"source": str(source.ID), "folder": str(folder.ID)}


def test_an_empty_source_is_a_home_here_where_the_refresh_refuses_it(cfg, db):
    _home(db)
    assert placement.resolve_home(db, SOURCE).source_name == SOURCE


def test_a_source_at_the_root_has_no_folder_and_the_months_sit_beside_it(cfg, db):
    _parent, source = _home(db, "1", folder="")
    home = placement.resolve_home(db, SOURCE)
    assert home.folder_id == "" and home.folder_name == ""
    assert home.present == {SOURCE: str(source.ID)}

    placed = placement.place(db, home, [("1", "2026-11")])
    db.session.commit()

    assert placed.created == ("2026-11",)
    assert "2026-11" in _names_under(db, None)


@pytest.mark.parametrize("shape", ["none", "two", "folder", "smart", "removed"])
def test_no_source_or_two_or_the_wrong_kind_refuses_under_u119s_reason(cfg, db, shape):
    if shape == "two":
        _home(db, "1")
        db.create_playlist(SOURCE)
    elif shape == "folder":
        db.create_playlist_folder(SOURCE)
    elif shape == "smart":
        row = db.create_playlist(SOURCE)
        row.Attribute = 4
    elif shape == "removed":
        row = db.create_playlist(SOURCE)
        row.rb_local_deleted = 1
    db.session.commit()
    with pytest.raises(CratekitError) as caught:
        placement.resolve_home(db, SOURCE)
    assert caught.value.cause.reason == placement.SOURCE_MISSING
    assert "no heart was placed" in caught.value.cause.message


# ---------------------------------------------------------------------------
# The plan over rows
# ---------------------------------------------------------------------------


def test_the_plan_reads_what_each_heart_already_has_and_what_it_would_make(cfg, db):
    folder, _source = _home(db, "1")
    _month(db, folder, "2026-09", "2")
    home = placement.resolve_home(db, SOURCE)

    plan = placement.plan_placements(
        db, home, [("1", SEP, "one"), ("2", SEP, "two"), ("3", NOV, "three"), ("4", None, "four")]
    )

    by_row = {one.content_id: one for one in plan.placements}
    assert (by_row["1"].into_source, by_row["1"].into_month) == (False, True)
    assert (by_row["2"].into_source, by_row["2"].into_month) == (True, False)
    assert (by_row["3"].month, by_row["3"].adds) == ("2026-11", 2)
    assert (by_row["4"].month, by_row["4"].adds) == ("Undated", 2)
    assert plan.adds == 6 and plan.writes
    assert plan.creates == ("2026-11", "Undated")
    assert plan.identity()["placements"][0] == {
        "row": "1",
        "month": "2026-09",
        "source": False,
        "into_month": True,
    }


def test_a_row_named_twice_folds_to_its_first_mention(cfg, db):
    _home(db)
    home = placement.resolve_home(db, SOURCE)
    plan = placement.plan_placements(db, home, [("1", SEP, "a"), ("1", NOV, "a again")])
    assert [(one.content_id, one.month) for one in plan.placements] == [("1", "2026-09")]


def test_a_plan_over_a_library_already_placed_writes_nothing(cfg, db):
    folder, _source = _home(db, "1")
    _month(db, folder, "2026-09", "1")
    home = placement.resolve_home(db, SOURCE)
    plan = placement.plan_placements(db, home, [("1", SEP, "one")])
    assert not plan.writes and plan.creates == ()


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


def test_place_adds_to_the_source_and_to_each_month_making_an_absent_one(cfg, db):
    folder, source = _home(db, "1")
    q3 = _month(db, folder, "2026-09")
    home = placement.resolve_home(db, SOURCE)

    placed = placement.place(db, home, [("1", "2026-09"), ("2", "2026-11"), ("3", "Undated")])
    db.session.commit()

    assert placed.source_id == str(source.ID)
    assert placed.added_source == 2
    assert placed.created == ("2026-11", "Undated")
    assert placed.added == 5
    names = _names_under(db, folder)
    assert set(names) == {SOURCE, "2026-09", "2026-11", "Undated"}
    assert _members(db, source.ID) == {"1", "2", "3"}
    assert _members(db, q3.ID) == {"1"}
    assert _members(db, names["2026-11"]) == {"2"}
    assert _members(db, names["Undated"]) == {"3"}
    assert [(name, count) for name, _row, count in placed.months] == [
        ("2026-09", 1),
        ("2026-11", 1),
        ("Undated", 1),
    ]
    assert placed.to_json()["months"][1] == {"name": "2026-11", "id": names["2026-11"], "added": 1}


def test_placing_the_same_heart_twice_adds_nothing_twice(cfg, db):
    folder, source = _home(db)
    home = placement.resolve_home(db, SOURCE)
    first = placement.place(db, home, [("1", "2026-11")])
    db.session.commit()
    again = placement.place(db, home, [("1", "2026-11"), ("1", "2026-11")])
    db.session.commit()

    assert first.added == 2 and again.added == 0 and again.created == ()
    assert _members(db, source.ID) == {"1"}
    (month_id,) = [row for name, row in _names_under(db, folder).items() if name == "2026-11"]
    assert _members(db, month_id) == {"1"}
    assert len([s for s in db.get_playlist_songs(PlaylistID=month_id)]) == 1


def test_a_members_marked_removedhip_in_the_month_is_added_again_live(cfg, db):
    """R-758: a soft deleted membership is not present, so the heart comes back."""
    folder, _source = _home(db, "1")
    q4 = _month(db, folder, "2026-11", "1")
    (entry,) = list(db.get_playlist_songs(PlaylistID=str(q4.ID)))
    entry.rb_local_deleted = 1
    db.session.commit()
    home = placement.resolve_home(db, SOURCE)

    placed = placement.place(db, home, [("1", "2026-11")])
    db.session.commit()

    assert placed.added == 1 and placed.added_source == 0
    assert _members(db, q4.ID) == {"1"}


def test_a_source_that_went_between_the_plan_and_the_write_is_refused(cfg, db):
    _folder, source = _home(db)
    home = placement.resolve_home(db, SOURCE)
    source.rb_local_deleted = 1
    db.session.commit()
    with pytest.raises(CratekitError) as caught:
        placement.place(db, home, [("1", "2026-11")])
    assert caught.value.cause.reason == "decision-stale"
    assert "no heart was placed" in caught.value.cause.message


def test_a_smart_playlist_of_the_months_name_is_not_written_to_and_a_plain_one_is_made(cfg, db):
    folder, _source = _home(db)
    smart = db.create_playlist("2026-11", parent=folder)
    smart.Attribute = 4
    db.session.commit()
    home = placement.resolve_home(db, SOURCE)

    placed = placement.place(db, home, [("1", "2026-11")])
    db.session.commit()

    assert placed.created == ("2026-11",)
    ((_name, row, count),) = placed.months
    assert row != str(smart.ID) and count == 1
    assert _members(db, smart.ID) == set()


def test_no_content_row_tempo_or_rating_is_written(cfg, db):
    """The standing constraint, read from SQL after the write."""
    import sqlite3

    _home(db)
    home = placement.resolve_home(db, SOURCE)
    placement.place(db, home, [("1", "2026-11"), ("2", "Undated")])
    db.session.commit()
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        rows = conn.execute(
            "SELECT ID, BPM, Rating, AnalysisDataPath FROM djmdContent ORDER BY ID"
        ).fetchall()
        assert len(rows) == 6
        assert all(bpm in (None, 0) and rating in (None, 0) and not path for _id, bpm, rating, path in rows)
        assert conn.execute("SELECT COUNT(*) FROM djmdContent").fetchone()[0] == 6
    finally:
        conn.close()


def test_members_marked_removedhips_are_read_apart_from_live_ones(cfg, db):
    folder, source = _home(db, "1", "2")
    (entry,) = [row for row in db.get_playlist_songs(PlaylistID=str(source.ID)) if str(row.ContentID) == "2"]
    entry.rb_local_deleted = 1
    db.session.commit()
    assert placement.members(db, source.ID) == {"1"}
    assert placement.members_marked_removed(db, source.ID) == {"2"}
    del folder


def test_the_plans_digest_covers_each_months_row_found_or_to_be_made(cfg, db):
    folder, _source = _home(db)
    q3 = _month(db, folder, "2026-09")
    home = placement.resolve_home(db, SOURCE)
    plan = placement.plan_placements(db, home, [("1", SEP, "one"), ("2", NOV, "two")])
    assert plan.identity()["months"] == {"2026-09": str(q3.ID), "2026-11": ""}

