"""U135: a set landed in several INBOX batches is one playlist under the set's name.

Driven against the disposable database the native landing suite builds. A set
job is queued and landed in two parts on two days; the second landing adds to
the INBOX playlist the first recorded, under its first name, beside the
INSPIRATION join U121 already pins.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

from datetime import date

from cratekit.core import config, rb_writer, session
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import batch_name, native
from tests import cutover_fixtures
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import _query, _two_acts
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_set_inspiration_playlist import (
    BATCH,
    FOLDER,
    NAME,
    WORDS,
    _land,
    _members,
    _playlists_named,
    _row_ids_by_name,
    _stage,
    set_job,
)
from tests.test_set_inspiration_playlist import fresh_cache as fresh_cache  # noqa: PLC0414
from tests.test_set_inspiration_playlist import machine as machine  # noqa: PLC0414
from tests.test_set_inspiration_playlist import pinned_day as pinned_day  # noqa: PLC0414


def _inbox_under(cfg: config.Config, root_id: str) -> dict[str, list[str]]:
    """Each live child playlist of the intake root, its member titles in order."""
    rows = _query(
        cfg,
        "SELECT ID, Name FROM djmdPlaylist WHERE ParentID = ? AND Attribute = 0 "
        "AND rb_local_deleted = 0 ORDER BY Name",
        root_id,
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


def _inspiration_rows(cfg: config.Config, root_id: str):
    return [row for row in _playlists_named(cfg, NAME) if str(row[1]) != root_id]


def test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set(native_library, silence):
    cfg, root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One", "Two"))
    _stage(cfg, silence, "One")
    _stage(cfg, silence, "Two")

    code, acted, refused = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["inbox playlist"] == NAME
    assert shown["inbox"] == "made"
    assert "inbox leftovers" not in shown
    inbox = _inbox_under(cfg, root_id)
    assert inbox[NAME] == ["One", "Two"]
    assert BATCH not in inbox
    (kept,) = _batch_records(cfg)
    assert kept["name"] == NAME and kept[native.INBOX_JOB_KEY] == job_id


def test_two_landings_of_one_set_make_one_inbox_playlist_in_set_order(
    native_library, silence, monkeypatch
):
    """The second landing reads the first's batch playlist record, adds to it,
    and keeps its name, so a set landed in two parts is one INBOX playlist.

    Track titles are Zebra then Apple so set order differs from name order; the
    joined INBOX playlist must follow set order, not the landing's file sort.
    """
    cfg, root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("Zebra", "Apple"))
    _stage(cfg, silence, "Zebra")
    code, first, refused = _two_acts(_land("--set", job_id, *WORDS))
    assert code == int(ExitCode.OK), first
    ((playlist_id, *_rest),) = [
        row for row in _playlists_named(cfg, NAME) if str(row[1]) == root_id
    ]
    assert refused["cause"]["detail"]["shown"]["inbox playlist"] == NAME

    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 10))
    _stage(cfg, silence, "Apple")
    verb = ["intake", "land", "--name", "2026-10-10 Set", "--set", job_id, *WORDS]
    code, second, refused = _two_acts(verb)

    assert code == int(ExitCode.OK), second
    shown = refused["cause"]["detail"]["shown"]
    assert shown["inbox"].startswith("adds to the playlist an earlier landing")
    assert shown["inbox playlist"] == NAME
    assert str(playlist_id) in shown["inbox"]
    assert len([row for row in _playlists_named(cfg, NAME) if str(row[1]) == root_id]) == 1
    assert _playlists_named(cfg, "2026-10-10 Set") == []
    assert _playlists_named(cfg, BATCH) == []
    rows = _row_ids_by_name(cfg)
    assert _members(cfg, str(playlist_id)) == [rows["Zebra"], rows["Apple"]]
    assert _inbox_under(cfg, root_id)[NAME] == ["Zebra", "Apple"]
    records = _batch_records(cfg)
    assert all(one.get(native.INBOX_JOB_KEY) == job_id for one in records)
    assert {one["id"] for one in records} == {str(playlist_id)}


def test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order(
    native_library, silence
):
    """Both tracks staged in one landing, the set's order the opposite of their
    names'. The landing sorts its files by name, so only the set's positions
    put Zebra first; the two landing test above stages one file per landing
    and cannot tell the two orders apart."""
    cfg, root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("Zebra", "Apple"))
    _stage(cfg, silence, "Apple")
    _stage(cfg, silence, "Zebra")

    code, acted, _refused = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    assert _inbox_under(cfg, root_id)[NAME] == ["Zebra", "Apple"]
    rows = _row_ids_by_name(cfg)
    ((playlist_id, *_rest),) = [
        row for row in _playlists_named(cfg, NAME) if str(row[1]) == root_id
    ]
    assert _members(cfg, str(playlist_id)) == [rows["Zebra"], rows["Apple"]]


def test_a_landing_without_set_keeps_todays_dated_name(native_library, silence):
    cfg, root_id = native_library
    _stage(cfg, silence, "Loose")

    code, acted, refused = _two_acts(["intake", "land"])

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert "inbox playlist" not in shown
    inbox = _inbox_under(cfg, root_id)
    assert any(batch_name.is_default_shape(name) for name in inbox)
    (kept,) = _batch_records(cfg)
    assert native.INBOX_JOB_KEY not in kept


def test_inspiration_join_stays_pinned_beside_the_inbox_join(
    native_library, silence, monkeypatch
):
    """U121's INSPIRATION join already holds across two landings; this unit
    only adds the INBOX join beside it and does not rebuild that path."""
    cfg, root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One", "Two"))
    _stage(cfg, silence, "One")
    code, first, _ = _two_acts(_land("--set", job_id, *WORDS))
    assert code == int(ExitCode.OK), first
    ((insp_id, *_),) = _inspiration_rows(cfg, root_id)

    monkeypatch.setattr(batch_name, "today", lambda: date(2026, 10, 10))
    _stage(cfg, silence, "Two")
    code, second, refused = _two_acts(
        ["intake", "land", "--name", "2026-10-10 Set", "--set", job_id, *WORDS]
    )
    assert code == int(ExitCode.OK), second
    shown = refused["cause"]["detail"]["shown"]
    assert shown["playlist"].startswith("adds to the playlist an earlier write made")
    assert shown["set playlist"] == NAME
    assert len(_inspiration_rows(cfg, root_id)) == 1
    rows = _row_ids_by_name(cfg)
    assert _members(cfg, str(insp_id)) == [rows["One"], rows["Two"]]


def test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined(
    native_library, silence
):
    cfg, root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    twin = f"{NAME} 2"
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        handle.create_playlist(twin, parent=handle.get_playlist(ID=root_id))
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)

    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")
    code, acted, refused = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert twin in shown["inbox leftovers"]
    inbox = _inbox_under(cfg, root_id)
    assert inbox[NAME] == ["One"]
    assert inbox[twin] == []


def test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined(
    native_library, silence
):
    """An earlier --set landing wrote a dated INBOX playlist and the set under
    INSPIRATION, with no job key on the batch record. A later landing names it
    and makes the set-named INBOX playlist beside it rather than joining."""
    import json

    cfg, root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    job_id = set_job(cfg, ("One", "Two"))
    _stage(cfg, silence, "One")
    code, first, _ = _two_acts(_land("--set", job_id, *WORDS))
    assert code == int(ExitCode.OK), first

    records, _ = session.scan_log(cfg)
    closed = [
        record
        for record in records
        if isinstance(record.detail.get(native.BATCH_PLAYLIST_KEY), dict)
    ]
    assert closed
    kept = closed[-1]
    playlist_id = str(kept.detail[native.BATCH_PLAYLIST_KEY]["id"])
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        row = handle.get_playlist(ID=playlist_id)
        row.Name = BATCH
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    path = session.log_path(kept.session_id, cfg)
    raw = json.loads(path.read_text())
    batch = raw["detail"][native.BATCH_PLAYLIST_KEY]
    batch.pop(native.INBOX_JOB_KEY, None)
    batch["name"] = BATCH
    path.write_text(json.dumps(raw, indent=2, sort_keys=True) + '\n')

    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        assert native.recorded_inbox_playlist(cfg, handle, job_id, root_id) is None
        leftovers = native.leftover_set_inbox(
            cfg, handle, job_id, root_id, NAME, keep_id=""
        )
    finally:
        rb_writer.close_db(handle)
    assert BATCH in leftovers

    _stage(cfg, silence, "Two")
    code, second, refused = _two_acts(
        ["intake", "land", "--name", "2026-10-10 Set", "--set", job_id, *WORDS]
    )

    assert code == int(ExitCode.OK), second
    shown = refused["cause"]["detail"]["shown"]
    assert BATCH in shown["inbox leftovers"]
    assert shown["inbox"] == "made"
    assert shown["inbox playlist"] == NAME
    inbox = _inbox_under(cfg, root_id)
    assert inbox[BATCH] == ["One"]
    assert inbox[NAME] == ["Two"]


def test_a_removed_set_named_inbox_playlist_is_not_written_into(native_library, silence):
    """A soft-deleted INBOX playlist of the set's name must not receive members.

    Before U135 the dated batch name made this collision unlikely; the set name
    now recurs by design, so the write skips removed namesakes the way the
    INSPIRATION path already does.
    """
    from tests.test_set_inspiration_playlist import _make_playlist, _soft_delete_playlist

    cfg, root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    removed_id = _make_playlist(cfg, NAME, under=root_id)
    _soft_delete_playlist(cfg, removed_id)
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")

    code, acted, refused = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    assert refused["cause"]["detail"]["shown"]["inbox"] == "made"
    assert _members(cfg, removed_id) == []
    live = [row for row in _playlists_named(cfg, NAME) if str(row[1]) == root_id and not row[3]]
    ((live_id, *_r),) = live
    assert str(live_id) != removed_id
    assert _inbox_under(cfg, root_id)[NAME] == ["One"]
    (kept,) = _batch_records(cfg)
    assert kept["id"] == str(live_id) and kept[native.INBOX_JOB_KEY] == job_id


def test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded(
    native_library, silence
):
    """A live INBOX playlist of the set's name with no job record is joined, and
    the screen says so apart from making one, then the job key is stamped."""
    from tests.test_set_inspiration_playlist import _make_playlist

    cfg, root_id = native_library
    cutover_fixtures.add_folder(cfg, FOLDER)
    handmade_id = _make_playlist(cfg, NAME, under=root_id)
    job_id = set_job(cfg, ("One",))
    _stage(cfg, silence, "One")

    code, acted, refused = _two_acts(_land("--set", job_id, *WORDS))

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["inbox"] == "found live by name, not recorded"
    assert shown["inbox playlist"] == NAME
    assert _members(cfg, handmade_id) == [_row_ids_by_name(cfg)["One"]]
    (kept,) = _batch_records(cfg)
    assert kept["id"] == handmade_id and kept[native.INBOX_JOB_KEY] == job_id

