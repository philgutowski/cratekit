"""A date the binding cannot place in local time reads as a bound, never a failure (U285).

DEADCA7 0.2.3 stamps every row it pushes ``0001-01-01T00:00:00Z``. The pinned
binding converts each stamp to local time, which west of UTC falls before year
1 and raised ``OverflowError``, so a verb walking the playlist tree failed over
a real push. ``core/rb_dates.py`` wraps that conversion once, at the open seam.
Driven here on the conversion itself and through a real handle on a disposable
database carrying the producer's own value.
"""

from __future__ import annotations

from datetime import datetime

import pytest
from pyrekordbox.db6 import tables

from cratekit.core import rb_dates
from cratekit.core import rb_writer as W
from tests import deadca7_fixtures as dc7
from tests.test_rb_writer_db import (  # noqa: F401 - fixtures
    _build_disposable_database,
    cloud_sync_off,
    library,
)

#: Zones as POSIX rules, which need no zone database: US Eastern, Japan, UTC,
#: and the two furthest offsets in use, twelve hours west and fourteen east.
WEST = dc7.EASTERN
EAST = "JST-9"
ZONES = (WEST, EAST, "UTC0", "AOE+12", "LINT-14")

#: rekordbox's own stamp, as its rows read, and what it is in US Eastern
#: (four hours behind in March, after the change to summer time).
OWN = "2026-03-09 21:06:07.516 +00:00"
OWN_EASTERN = datetime(2026, 3, 9, 17, 6, 7, 516000)
#: A playlist of the library's own, stamped as rekordbox stamps.
OWN_ID = "4242"


def _binding() -> object:
    """The binding's own conversion, unwrapped whatever state the process is in."""
    current = tables.string_to_datetime
    return getattr(current, "__wrapped__", current)


@pytest.fixture
def unwrapped(monkeypatch):
    """The binding's conversion and XML update as shipped, put back after the test."""
    from pyrekordbox.db6 import aux_files

    monkeypatch.setattr(tables, "string_to_datetime", _binding())
    update = aux_files.MasterPlaylistXml.update
    monkeypatch.setattr(
        aux_files.MasterPlaylistXml, "update", getattr(update, "__wrapped__", update)
    )
    return tables.string_to_datetime


@pytest.fixture(autouse=True)
def _rekordbox_closed(monkeypatch):
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)


# ---------------------------------------------------------------------------
# The conversion
# ---------------------------------------------------------------------------


def test_the_binding_alone_cannot_place_the_zero_date_west_of_utc(unwrapped):
    """The defect, so the tests below are known to reach it."""
    with dc7.west_of_utc(WEST), pytest.raises(OverflowError):
        unwrapped(dc7.ZERO_STAMP)


@pytest.mark.parametrize("zone", ZONES)
def test_the_zero_date_reads_as_the_floor_in_every_zone(unwrapped, zone):
    read = rb_dates.placeable(unwrapped)
    with dc7.west_of_utc(zone):
        assert read(dc7.ZERO_STAMP) == rb_dates.FLOOR == datetime(1, 1, 2)


@pytest.mark.parametrize("zone", ZONES)
def test_the_calendars_last_moment_reads_as_the_ceiling(unwrapped, zone):
    read = rb_dates.placeable(unwrapped)
    with dc7.west_of_utc(zone):
        assert read("9999-12-31T23:59:59Z") == rb_dates.CEILING == datetime(9999, 12, 30)


@pytest.mark.parametrize("zone", ZONES)
@pytest.mark.parametrize(
    ("text", "bound"),
    [
        ("0001-01-01 00:00:00", "FLOOR"),
        ("0001-01-01 00:00:00.000", "FLOOR"),
        ("9999-12-31 23:00:00", "CEILING"),
    ],
)
def test_an_edge_stamp_with_no_offset_reads_as_its_bound(unwrapped, zone, text, bound):
    """With no offset the binding fails with ValueError rather than OverflowError,
    in every zone, and the brief asks for any value the conversion cannot place."""
    read = rb_dates.placeable(unwrapped)
    with dc7.west_of_utc(zone):
        with pytest.raises(ValueError, match="out of range"):
            unwrapped(text)
        assert read(text) == getattr(rb_dates, bound)


def test_an_ordinary_stamp_reads_exactly_as_the_binding_reads_it(unwrapped):
    read = rb_dates.placeable(unwrapped)
    with dc7.west_of_utc(WEST):
        assert read(OWN) == unwrapped(OWN) == OWN_EASTERN
        assert read(dc7.STAMP) == datetime(2026, 10, 30, 8, 0)


@pytest.mark.parametrize("zone", ZONES)
def test_each_bound_converts_back_in_every_zone(zone):
    """A reader that converts a bound again cannot overflow where the binding did."""
    with dc7.west_of_utc(zone):
        for bound in (rb_dates.FLOOR, rb_dates.CEILING):
            assert bound.astimezone().replace(tzinfo=None) == bound
            assert isinstance(bound.timestamp(), float)


@pytest.mark.parametrize(
    "text",
    [
        "not a date",
        "0001-13-01T00:00:00Z",
        "0001-13-01 00:00:00",
        "9999-02-30 00:00:00",
        "2026-02-30 00:00:00.000 +00:00",
        "0000-01-01T00:00:00Z",
        "0000-01-01 00:00:00",
    ],
)
def test_text_the_binding_cannot_parse_still_fails_as_it_did(unwrapped, text):
    """Never a hidden error: only the calendar's edge reads as a bound, and text
    the binding refuses is refused with the binding's own error."""
    read = rb_dates.placeable(unwrapped)
    with dc7.west_of_utc(WEST):
        with pytest.raises(Exception) as by_binding:
            unwrapped(text)
        with pytest.raises(Exception) as by_wrapper:
            read(text)
    assert not isinstance(by_binding.value, OverflowError)
    assert type(by_wrapper.value) is type(by_binding.value)
    assert str(by_wrapper.value) == str(by_binding.value)


def test_an_overflow_away_from_the_calendars_edge_is_raised_as_it_came():
    def overflowing(value: str) -> datetime:
        raise OverflowError(f"cannot place {value}")

    read = rb_dates.placeable(overflowing)
    with pytest.raises(OverflowError, match="cannot place 2026"):
        read(OWN)
    assert read(dc7.ZERO_STAMP) == rb_dates.FLOOR


def test_an_aware_answer_is_handed_on_as_it_came():
    from datetime import timezone

    aware = datetime(1, 1, 1, tzinfo=timezone.utc)
    assert rb_dates.placeable(lambda value: aware)(dc7.ZERO_STAMP) is aware


def test_installing_twice_wraps_once(unwrapped):
    from pyrekordbox.db6 import aux_files

    shipped_update = aux_files.MasterPlaylistXml.update
    rb_dates.install()
    first = tables.string_to_datetime
    first_update = aux_files.MasterPlaylistXml.update
    rb_dates.install()
    assert tables.string_to_datetime is first
    assert aux_files.MasterPlaylistXml.update is first_update
    assert first.__wrapped__ is unwrapped
    assert first_update.__wrapped__ is shipped_update
    assert rb_dates.installed()


def test_a_bound_is_never_handed_to_the_xml_update():
    calls = []

    def update(self, playlist_id, parent_id=None, attribute=None, updated_at=None,
               lib_type=None, check_type=None):
        calls.append((playlist_id, parent_id, attribute, updated_at, lib_type, check_type))

    kept = rb_dates.keeps_bounds(update)
    kept(None, "1", updated_at=rb_dates.FLOOR)
    kept(None, "2", updated_at=rb_dates.CEILING)
    assert calls == []
    kept(None, "3", parent_id="9", updated_at=rb_dates.FLOOR)
    ordinary = datetime(2026, 11, 13, 12, 0)
    kept(None, "4", updated_at=ordinary)
    assert calls == [("3", "9", None, None, None, None), ("4", None, None, ordinary, None, None)]


# ---------------------------------------------------------------------------
# Through a real handle
# ---------------------------------------------------------------------------


@pytest.fixture
def zero_pushed(library):  # noqa: F811 - the imported fixture
    """A disposable database holding two tracks and a push stamped as the app stamps."""
    import sqlite3

    path = library / "db" / "master.db"
    _build_disposable_database(path)
    conn = sqlite3.connect(path)
    try:
        conn.execute(
            "INSERT INTO djmdPlaylist (ID, Seq, Name, Attribute, ParentID, UUID, "
            "rb_local_deleted, created_at, updated_at) "
            "VALUES (?, 1, 'my own', 0, 'root', 'own-uuid', 0, ?, ?)",
            (OWN_ID, OWN, OWN),
        )
        conn.commit()
    finally:
        conn.close()
    return path, dc7.push(path, ("1", "2"), stamp=dc7.ZERO_STAMP)


def test_the_open_seam_installs_the_wrapper(unwrapped, zero_pushed, cloud_sync_off):  # noqa: F811
    path, _pushed = zero_pushed
    assert not rb_dates.installed()
    db = W.open_db(path, unlock=False)
    try:
        assert rb_dates.installed()
    finally:
        W.close_db(db)


def test_a_handle_reads_the_whole_tree_over_a_zero_dated_push_and_writes_nothing(
    unwrapped, zero_pushed, cloud_sync_off  # noqa: F811
):
    """Every playlist and membership row loads; the push's read as the floor, the
    library's own exactly as the binding reads them; the file is not written."""
    import sqlite3

    path, pushed = zero_pushed
    before = dc7.written(path, pushed)
    conn = sqlite3.connect(path)
    try:
        own = dict(
            conn.execute(
                "SELECT ID, created_at FROM djmdPlaylist WHERE ID NOT IN (?, ?, ?)",
                (pushed.folder_id, *pushed.playlist_ids),
            ).fetchall()
        )
    finally:
        conn.close()
    with dc7.west_of_utc(WEST):
        expected_own = {str(key): unwrapped(text) for key, text in own.items() if text}
        db = W.open_db(path, unlock=False)
        try:
            rows = {str(row.ID): row for row in db.get_playlist()}
            songs = list(db.get_playlist_songs())
            for node in (pushed.folder_id, *pushed.playlist_ids):
                assert rows[node].created_at == rows[node].updated_at == rb_dates.FLOOR
            pushed_songs = [song for song in songs if str(song.PlaylistID) in pushed.playlist_ids]
            assert len(pushed_songs) == 2 * len(pushed.content_ids)
            assert {song.created_at for song in pushed_songs} == {rb_dates.FLOOR}
            assert OWN_ID in expected_own
            assert {key: rows[key].created_at for key in expected_own} == expected_own
            assert rows[OWN_ID].created_at == rows[OWN_ID].updated_at == OWN_EASTERN
            assert not db.session.dirty and not db.session.new
            W.commit_guarded(db)
        finally:
            W.close_db(db)
    assert dc7.written(path, pushed) == before


def test_a_wrapper_installed_after_a_handle_has_read_is_still_the_one_called(
    unwrapped, zero_pushed, cloud_sync_off  # noqa: F811
):
    """The binding's column looks the conversion up at every row, so a handle
    that has already read a date before the install reads a zero dated row
    after it."""
    from pyrekordbox import Rekordbox6Database

    path, pushed = zero_pushed
    with dc7.west_of_utc(WEST):
        db = Rekordbox6Database(path=str(path), unlock=False)
        try:
            assert isinstance(db.get_playlist(ID=OWN_ID).created_at, datetime)
            with pytest.raises(OverflowError):
                db.get_playlist(ID=pushed.folder_id)
            db.session.rollback()
            rb_dates.install()
            assert db.get_playlist(ID=pushed.folder_id).created_at == rb_dates.FLOOR
        finally:
            db.close()


def _playlist_xml(db_path, timestamps: dict[str, int]):
    """A ``masterPlaylists6.xml`` beside the database, one node per playlist id."""
    nodes = "".join(
        f'<NODE Id="{int(node):X}" ParentId="0" Attribute="0" Timestamp="{ms}" '
        'Lib_Type="0" CheckType="0"/>'
        for node, ms in timestamps.items()
    )
    xml = db_path.parent / "masterPlaylists6.xml"
    xml.write_text(
        '<?xml version="1.0" encoding="UTF-8"?><MASTER_PLAYLIST Version="1.0.0" '
        'AutomaticSync="0"><PRODUCT Name="rekordbox" Version="7.0.0" Company="AlphaTheta"/>'
        f"<PLAYLISTS>{nodes}</PLAYLISTS></MASTER_PLAYLIST>",
        encoding="utf-8",
    )
    return xml


def _node_attributes(xml, node: str) -> dict[str, str]:
    import xml.etree.ElementTree as ET

    for element in ET.parse(xml).getroot().iter("NODE"):
        if element.get("Id") == f"{int(node):X}":
            return dict(element.attrib)
    raise AssertionError(f"no node {node}")


#: DEADCA7's push time at sitting 98, in milliseconds, and a time the library's
#: own row does not hold, so the binding's sync has something to change.
PUSHED_MS = 1763050727914
STALE_MS = 1700000000000


@pytest.mark.parametrize("zone", [WEST, "UTC0", EAST])
def test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own(
    unwrapped, zero_pushed, cloud_sync_off, zone  # noqa: F811
):
    """Round two of the review: the binding's sync would write the floor's
    instant into DEADCA7's nodes. A commit now leaves those nodes exactly as
    they were, while the library's own stale node is still synced to its row."""
    path, pushed = zero_pushed
    foreign = (pushed.folder_id, *pushed.playlist_ids)
    xml = _playlist_xml(path, {**{node: PUSHED_MS for node in foreign}, OWN_ID: STALE_MS})
    before = {node: _node_attributes(xml, node) for node in foreign}
    rows = dc7.written(path, pushed)
    with dc7.west_of_utc(zone):
        db = W.open_db(path, unlock=False)
        try:
            W.ensure_folder(db, "a folder of the product's")
            W.commit_guarded(db)
        finally:
            W.close_db(db)
        own_ms = int(OWN_EASTERN.timestamp() * 1000) if zone == WEST else None
    assert {node: _node_attributes(xml, node) for node in foreign} == before
    own = int(_node_attributes(xml, OWN_ID)["Timestamp"])
    assert own != STALE_MS
    if own_ms is not None:
        assert own == own_ms == 1773090367516
    assert dc7.written(path, pushed) == rows


def test_before_the_seam_such_a_commit_failed_after_its_write(unwrapped, zero_pushed):
    """The binding alone, at UTC where the row loads: its sync cannot convert
    the year 1 value back, so the commit raised after the database write."""
    from pyrekordbox import Rekordbox6Database

    path, pushed = zero_pushed
    _playlist_xml(path, {node: PUSHED_MS for node in (pushed.folder_id, *pushed.playlist_ids)})
    with dc7.west_of_utc("UTC0"):
        db = Rekordbox6Database(path=str(path), unlock=False)
        try:
            with pytest.raises(ValueError, match="year 0 is out of range"):
                db.commit()
        finally:
            db.close()
