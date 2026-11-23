"""U135: a set landed in several INBOX batches is one playlist under the set's name.

A set landed in two parts on two days: the second landing adds to the INBOX
playlist the first recorded, under its first name. D1 applies.
"""

from __future__ import annotations

import json
from datetime import date
from types import SimpleNamespace

import pytest

from cratekit.core import config, rb_writer, session
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name, native
from tests import cutover_fixtures
from tests import test_intake_land_native as land_native
from tests import test_set_inspiration_playlist as inspiration
from tests.test_intake_land_native import _query, _two_acts
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414
from tests.test_set_inspiration_playlist import (
    BATCH,
    FOLDER,
    NAME,
    WORDS,
    _land,
    _make_playlist,
    _members,
    _playlists_named,
    _row_ids_by_name,
    _soft_delete_playlist,
    _stage,
    set_job,
)

# The native landing suite's fixtures, on the set suite's machine and seams.
_platform_seams = land_native._platform_seams
_release_process_locks = land_native._release_process_locks
acknowledged, library = land_native.acknowledged, land_native.library
native_library, silence = inspiration.native_library, inspiration.silence
fresh_cache, machine, pinned_day = inspiration.fresh_cache, inspiration.machine, inspiration.pinned_day

SECOND = ["intake", "land", "--name", "2026-10-10 Set"]


def _inbox_under(cfg: config.Config, root_id: str) -> dict[str, list[str]]:
    """Each live child playlist of the intake root, its member titles in order.

    All but INBOX / Analyze (U166), whose own suite is ``tests/test_inbox_analyzed.py``.
    """
    rows = _query(
        cfg,
        "SELECT ID, Name FROM djmdPlaylist WHERE ParentID = ? AND Attribute = 0 "
        "AND rb_local_deleted = 0 AND Name != ? ORDER BY Name",
        root_id,
        native.ANALYZE,
    )
    out: dict[str, list[str]] = {}
    for playlist_id, name in rows:
        out[str(name)] = [
            str(title)
            for (title,) in _query(
                cfg,
                "SELECT c.Title FROM djmdSongPlaylist sp JOIN djmdContent c ON c.ID = sp.ContentID "
                "WHERE sp.PlaylistID = ? AND (sp.rb_local_deleted = 0 OR sp.rb_local_deleted IS NULL) "
                "ORDER BY sp.TrackNo",
                playlist_id,
            )
        ]
    return out


def _batch_records(cfg: config.Config) -> list[dict]:
    records, _ = session.scan_log(cfg)
    return [
        dict(record.detail[native.BATCH_PLAYLIST_KEY])
        for record in records
        if isinstance(record.detail.get(native.BATCH_PLAYLIST_KEY), dict)
    ]


def _inbox_rows(cfg: config.Config, root_id: str) -> list[tuple]:
    return [row for row in _playlists_named(cfg, NAME) if str(row[1]) == root_id]


def _inspiration_rows(cfg: config.Config, root_id: str):
    return [row for row in _playlists_named(cfg, NAME) if str(row[1]) != root_id]


def _set(cfg: config.Config, silence, titles: tuple[str, ...], *staged: str) -> str:
    """The INSPIRATION folder, a set job over ``titles``, and ``staged`` in staging."""
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, titles)
    for title in staged:
        _stage(cfg, silence, title)
    return job_id


def _shown(verb: list[str]) -> dict:
    """The landing's two acts, applied: what its gate showed."""
    code, acted, refused = _two_acts(verb)
    assert code == int(ExitCode.OK), acted
    return refused["cause"]["detail"]["shown"]


def _next_day(monkeypatch, cfg: config.Config, silence, job_id: str, title: str) -> dict:
    """The set's next part, landed the next day under that day's batch name."""
    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 10))
    _stage(cfg, silence, title)
    return _shown([*SECOND, "--set", job_id, *WORDS])


def test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order(
    native_library, silence
):
    """Both tracks staged in one landing, the set's order the opposite of their
    names'. The landing sorts its files by name, so only the set's positions
    put Zebra first; a landing of one file per part cannot tell the two orders
    apart. The one INBOX playlist is named for the set and recorded for its job."""
    cfg, root_id = native_library
    job_id = _set(cfg, silence, ("Zebra", "Apple"), "Apple", "Zebra")
    shown = _shown(_land("--set", job_id, *WORDS))
    assert shown["inbox playlist"] == NAME
    assert shown["inbox"] == "made"
    assert "inbox leftovers" not in shown
    inbox = _inbox_under(cfg, root_id)
    assert inbox[NAME] == ["Zebra", "Apple"]
    assert BATCH not in inbox
    rows = _row_ids_by_name(cfg)
    ((playlist_id, *_rest),) = _inbox_rows(cfg, root_id)
    assert _members(cfg, str(playlist_id)) == [rows["Zebra"], rows["Apple"]]
    (kept,) = _batch_records(cfg)
    assert kept["name"] == NAME and kept[native.INBOX_JOB_KEY] == job_id


def test_two_landings_of_one_set_make_one_inbox_playlist_in_set_order(
    native_library, silence, monkeypatch
):
    """The second landing reads the first's batch playlist record, adds to it,
    and keeps its name, so a set landed in two parts is one INBOX playlist.

    Track titles are Zebra then Apple so set order differs from name order; the
    joined INBOX playlist must follow set order, not the landing's file sort.
    U121's INSPIRATION join holds beside it, and is not rebuilt.
    """
    cfg, root_id = native_library
    job_id = _set(cfg, silence, ("Zebra", "Apple"), "Zebra")
    assert _shown(_land("--set", job_id, *WORDS))["inbox playlist"] == NAME
    ((playlist_id, *_rest),) = _inbox_rows(cfg, root_id)
    ((insp_id, *_),) = _inspiration_rows(cfg, root_id)
    shown = _next_day(monkeypatch, cfg, silence, job_id, "Apple")
    assert shown["inbox"].startswith("adds to the playlist an earlier landing")
    assert shown["inbox playlist"] == NAME
    assert str(playlist_id) in shown["inbox"]
    assert shown["playlist"].startswith("adds to the playlist an earlier write made")
    assert shown["set playlist"] == NAME
    assert len(_inbox_rows(cfg, root_id)) == 1
    assert len(_inspiration_rows(cfg, root_id)) == 1
    assert _playlists_named(cfg, "2026-10-10 Set") == []
    assert _playlists_named(cfg, BATCH) == []
    rows = _row_ids_by_name(cfg)
    assert _members(cfg, str(playlist_id)) == [rows["Zebra"], rows["Apple"]]
    assert _members(cfg, str(insp_id)) == [rows["Zebra"], rows["Apple"]]
    assert _inbox_under(cfg, root_id)[NAME] == ["Zebra", "Apple"]
    records = _batch_records(cfg)
    assert all(one.get(native.INBOX_JOB_KEY) == job_id for one in records)
    assert {one["id"] for one in records} == {str(playlist_id)}


def test_a_landing_without_set_keeps_todays_dated_name(native_library, silence):
    cfg, root_id = native_library
    _stage(cfg, silence, "Loose")
    assert "inbox playlist" not in _shown(["intake", "land"])
    assert any(batch_name.is_default_shape(name) for name in _inbox_under(cfg, root_id))
    (kept,) = _batch_records(cfg)
    assert native.INBOX_JOB_KEY not in kept


def test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined(
    native_library, silence
):
    """And a folder under INBOX of the set's name is never taken as its playlist
    (A15): the landing makes the playlist beside both and files nothing into either."""
    cfg, root_id = native_library
    twin = f"{NAME} 2"
    _make_playlist(cfg, twin, under=root_id)
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        folder = rb_writer.ensure_folder(handle, NAME, parent=handle.get_playlist(ID=root_id))
        handle.session.commit()
        folder_id = str(folder.ID)
    finally:
        rb_writer.close_db(handle)
    job_id = _set(cfg, silence, ("One",), "One")
    shown = _shown(_land("--set", job_id, *WORDS))
    assert twin in shown["inbox leftovers"]
    assert shown["inbox"] == "made"
    assert _members(cfg, folder_id) == []
    inbox = _inbox_under(cfg, root_id)
    assert inbox[NAME] == ["One"]
    assert inbox[twin] == []


def test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined(
    native_library, silence, monkeypatch
):
    """An earlier --set landing wrote a dated INBOX playlist and the set under
    INSPIRATION, with no job key on the batch record. A later landing names it
    and makes the set-named INBOX playlist beside it rather than joining."""
    cfg, root_id = native_library
    job_id = _set(cfg, silence, ("One", "Two"), "One")
    _shown(_land("--set", job_id, *WORDS))
    records, _ = session.scan_log(cfg)
    closed = [r for r in records if isinstance(r.detail.get(native.BATCH_PLAYLIST_KEY), dict)]
    assert closed
    kept = closed[-1]
    playlist_id = str(kept.detail[native.BATCH_PLAYLIST_KEY]["id"])
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        handle.get_playlist(ID=playlist_id).Name = BATCH
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    path = session.log_path(kept.session_id, cfg)
    raw = json.loads(path.read_text())
    batch = raw["detail"][native.BATCH_PLAYLIST_KEY]
    batch.pop(native.INBOX_JOB_KEY, None)
    batch["name"] = BATCH
    path.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        assert native.recorded_inbox_playlist(cfg, handle, job_id, root_id) is None
        leftovers = native.leftover_set_inbox(cfg, handle, job_id, root_id, NAME, keep_id="")
    finally:
        rb_writer.close_db(handle)
    assert BATCH in leftovers
    _stage(cfg, silence, "Two")
    shown = _shown([*SECOND, "--set", job_id, *WORDS])
    assert BATCH in shown["inbox leftovers"]
    assert shown["inbox"] == "made"
    assert shown["inbox playlist"] == NAME
    inbox = _inbox_under(cfg, root_id)
    assert inbox[BATCH] == ["One"]
    assert inbox[NAME] == ["Two"]


def test_a_removed_set_named_inbox_playlist_is_not_written_into(native_library, silence):
    """A soft-deleted INBOX playlist of the set's name must not receive members.

    The set name recurs by design, so the write skips removed namesakes the way
    the INSPIRATION path already does.
    """
    cfg, root_id = native_library
    removed_id = _make_playlist(cfg, NAME, under=root_id)
    _soft_delete_playlist(cfg, removed_id)
    job_id = _set(cfg, silence, ("One",), "One")
    assert _shown(_land("--set", job_id, *WORDS))["inbox"] == "made"
    assert _members(cfg, removed_id) == []
    ((live_id, *_r),) = [row for row in _inbox_rows(cfg, root_id) if not row[3]]
    assert str(live_id) != removed_id
    assert _inbox_under(cfg, root_id)[NAME] == ["One"]
    (kept,) = _batch_records(cfg)
    assert kept["id"] == str(live_id) and kept[native.INBOX_JOB_KEY] == job_id


def test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded(
    native_library, silence
):
    """A live INBOX playlist of the set's name with no job record is joined, and
    the screen says so apart from making one, then the job key is stamped."""
    cfg, root_id = native_library
    handmade_id = _make_playlist(cfg, NAME, under=root_id)
    job_id = _set(cfg, silence, ("One",), "One")
    shown = _shown(_land("--set", job_id, *WORDS))
    assert shown["inbox"] == "found live by name, not recorded"
    assert shown["inbox playlist"] == NAME
    assert _members(cfg, handmade_id) == [_row_ids_by_name(cfg)["One"]]
    (kept,) = _batch_records(cfg)
    assert kept["id"] == handmade_id and kept[native.INBOX_JOB_KEY] == job_id


# ---------------------------------------------------------------------------
# U139: the U135 guards no test reached (rows A6 and A11; A15 is above)
# ---------------------------------------------------------------------------


def test_a_recorded_inbox_playlist_removed_before_the_next_landing_is_not_joined(
    native_library, silence, monkeypatch
):
    """A6. The first landing records its INBOX playlist; a person removes it in
    rekordbox; the second landing reads the record, sees the row is soft
    deleted, and makes the set's playlist afresh rather than joining it."""
    cfg, root_id = native_library
    job_id = _set(cfg, silence, ("One", "Two"), "One")
    _shown(_land("--set", job_id, *WORDS))
    ((removed_id, *_rest),) = _inbox_rows(cfg, root_id)
    _soft_delete_playlist(cfg, str(removed_id))
    before = _members(cfg, str(removed_id))
    shown = _next_day(monkeypatch, cfg, silence, job_id, "Two")
    assert shown["inbox"] == "made"
    assert _members(cfg, str(removed_id)) == before
    # Made afresh, so named for the set on this landing's day.
    assert _inbox_under(cfg, root_id) == {shown["inbox playlist"]: ["Two"]}


def test_a_recorded_inbox_playlist_removed_after_the_plan_is_refused_at_the_write(native_library):
    """A11. The plan named a recorded playlist live; by the write it was removed.
    Asked of the write's own row lookup, since between two drives the landing
    plans again and refuses on the digest before the write is reached."""
    cfg, root_id = native_library
    removed_id = _make_playlist(cfg, NAME, under=root_id)
    _soft_delete_playlist(cfg, removed_id)
    planned = SimpleNamespace(batch_playlist_id=removed_id, playlist=NAME)
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        with pytest.raises(CratekitError) as refused:
            native._batch_playlist_row(handle, planned, handle.get_playlist(ID=root_id))
    finally:
        rb_writer.close_db(handle)
    assert refused.value.cause.reason == "decision-stale"
    assert removed_id in refused.value.cause.message
    assert _members(cfg, removed_id) == []
