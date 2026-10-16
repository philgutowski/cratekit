"""U146 on the native medium: a heart on an owned track joins All Favorites and its month.

R4 and R6's landing half, driven through the real dispatcher against the
disposable database the native landing suite builds. A track the library
holds, filed deep where the source system put it and never landed by this
product, is hearted on the account; the pass's hearts job reports it owned,
with the file it resolved to; ``crate intake land --pass`` then places it,
with a file to land beside it or with download staging empty, under the
landing's own gate. Nothing is downloaded and nothing is removed.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from cratekit.core import config, rb_writer, session, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import backfill
from cratekit.intake import land_cli
from tests.cli_drive import drive
from tests.test_intake_land_account_playlists_native import PASS, _stage
from tests.test_intake_land_account_playlists_native import (
    pinned_day as pinned_day,  # noqa: PLC0414
)
from tests.test_intake_land_hearts_native import (
    NOV,
    SEP,
    SOURCE,
    UNKNOWN,
    _favorites,
    _home,
    hearts_swept,
)
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import _query, _two_acts
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414

LAND = ["intake", "land", "--pass", PASS]


def _owned(cfg: config.Config, silence: Path, title: str) -> str:
    """A track the library holds, two folders deep with its row, as the source system filed it."""
    path = Path(cfg.library.root) / cfg.library.music_dir / "Processed_Tracks" / "2025" / f"{title}.flac"
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": title, "artist": "Probe", "genre": "Deep House"})
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        row = handle.add_content(path, Title=title)
        handle.session.commit()
        return str(row.ID)
    finally:
        rb_writer.close_db(handle)


def _content_count(cfg: config.Config) -> int:
    return int(_query(cfg, "SELECT COUNT(*) FROM djmdContent")[0][0])


def _live(cfg: config.Config, playlist_id: str) -> list[str]:
    """The members a person sees, the removed rows left out, which ``_favorites`` keeps."""
    return [
        str(row[0])
        for row in _query(
            cfg,
            "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? AND rb_local_deleted = 0",
            playlist_id,
        )
    ]


def _mark_removed(cfg: config.Config, playlist_id: str, content_id: str) -> None:
    """A person takes the track out of the playlist in rekordbox: the row stays, marked removed."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        (entry,) = [
            row
            for row in handle.get_playlist_songs(PlaylistID=playlist_id)
            if str(row.ContentID) == content_id
        ]
        entry.rb_local_deleted = 1
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)


# ---------------------------------------------------------------------------
# AE4: an owned heart, nothing downloaded, joins at the next sync
# ---------------------------------------------------------------------------


def test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded(
    native_library, silence
):
    cfg, _root_id = native_library
    folder_id, source_id = _home(cfg)
    row = _owned(cfg, silence, "Owned")
    hearts_swept(cfg, {"Owned": NOV})
    rows_before = _content_count(cfg)

    code, acted, refused = _two_acts(LAND)

    assert code == int(ExitCode.OK), acted
    assert _favorites(cfg, folder_id) == {SOURCE: ["Owned"], "2026-11": ["Owned"]}
    # Nothing was downloaded or landed: no row made, staging untouched, no INBOX batch.
    assert _content_count(cfg) == rows_before
    assert list(Path(cfg.paths.download_staging).iterdir()) == []
    shown = refused["cause"]["detail"]["shown"]
    assert shown["hearts to place"] == 1 and shown["by month"] == ["2026-11: 1"]
    (item,) = shown["items"]
    assert (item["row"], item["month"], item["dated_by"]) == (row, "2026-11", "job")
    assert refused["cause"]["detail"]["gate"] == land_cli.NATIVE_GATE
    assert acted["data"]["totals"]["hearts placed"] == 2
    (note,) = [w for w in acted["warnings"] if w["code"] == land_cli.FAVORITES_PLACED]
    assert "2 membership(s) placed: 1 into" in note["message"]
    assert "for 1 owned heart(s)" in note["message"]
    # The landing's own screen: no account listing, no backfill count.
    assert shown["files to land"] == 0
    assert "already placed" not in shown and "dates asked of the account" not in shown
    assert "no file was landed" in note["message"]
    # The backfill's guarded session wrote it, recorded under the favourites key.
    (record,) = [r for r in session.records(cfg) if r.workflow == backfill.WORKFLOW]
    assert record.state is session.SessionState.CLOSED
    assert source_id


def test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op(
    native_library, silence
):
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _owned(cfg, silence, "Owned")
    hearts_swept(cfg, {"Owned": NOV})
    code, _acted, _refused = _two_acts(LAND)
    assert code == int(ExitCode.OK)

    code, acted = drive(LAND)

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert acted["data"]["totals"] == {"count": 0}
    assert _favorites(cfg, folder_id) == {SOURCE: ["Owned"], "2026-11": ["Owned"]}


def test_a_pass_with_no_hearts_job_opens_nothing_and_ends_no_op(native_library, monkeypatch):
    """The empty landing as it always was: no owned heart, no database opened."""
    cfg, _root_id = native_library
    _home(cfg)
    opened: list[object] = []
    real = rb_writer.open_db

    def counting(*args, **kwargs):
        opened.append(args)
        return real(*args, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", counting)

    code, acted = drive(LAND)

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert opened == []


# ---------------------------------------------------------------------------
# R6: taken out of All Favorites by hand and still hearted, it joins again
# ---------------------------------------------------------------------------


def test_a_track_removed_from_all_favorites_by_hand_and_still_hearted_joins_again(
    native_library, silence
):
    cfg, _root_id = native_library
    folder_id, source_id = _home(cfg)
    row = _owned(cfg, silence, "Owned")
    hearts_swept(cfg, {"Owned": NOV})
    code, _acted, _refused = _two_acts(LAND)
    assert code == int(ExitCode.OK)
    _mark_removed(cfg, source_id, row)
    assert _live(cfg, source_id) == []
    hearts_swept(cfg, {"Owned": NOV})

    code, acted, _refused = _two_acts(LAND)

    assert code == int(ExitCode.OK), acted
    assert _live(cfg, source_id) == [row]
    assert _favorites(cfg, folder_id)["2026-11"] == ["Owned"]
    assert acted["data"]["totals"]["hearts placed"] == 1, "the month already held it"


# ---------------------------------------------------------------------------
# With a file to land: one commit places both kinds of heart
# ---------------------------------------------------------------------------


def test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one(native_library, silence):
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _owned(cfg, silence, "Owned")
    hearts_swept(cfg, {"Owned": SEP, "Fresh": NOV})
    _stage(cfg, silence, "Fresh")

    code, acted, refused = _two_acts(LAND)

    assert code == int(ExitCode.OK), acted
    placed = _favorites(cfg, folder_id)
    assert sorted(placed[SOURCE]) == ["Fresh", "Owned"]
    assert (placed["2026-09"], placed["2026-11"]) == (["Owned"], ["Fresh"])
    shown = refused["cause"]["detail"]["shown"]
    assert shown["owned hearts"] == ["Probe - Owned, 2026-09"]
    assert shown["hearts"].startswith("1 file(s) the account hearts and 1 owned track(s), into")
    assert shown["month playlists"] == ["2026-09 (0 file(s), 1 owned), made", "2026-11 (1 file(s)), made"]
    assert acted["data"]["totals"]["hearts placed"] == 4
    # One session wrote the batch and both hearts.
    (record,) = [r for r in session.records(cfg) if "favorites_placed" in r.detail]
    assert record.detail["favorites_placed"]["added_source"] == 2


def test_an_owned_heart_all_favorites_holds_is_no_write_beside_a_landing(native_library, silence):
    cfg, _root_id = native_library
    folder_id, source_id = _home(cfg)
    row = _owned(cfg, silence, "Owned")
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        handle.add_to_playlist(handle.get_playlist(ID=source_id), row)
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    hearts_swept(cfg, {"Owned": SEP, "Fresh": NOV})
    _stage(cfg, silence, "Fresh")

    code, acted, refused = _two_acts(LAND)

    assert code == int(ExitCode.OK), acted
    assert "owned hearts" not in refused["cause"]["detail"]["shown"]
    assert sorted(_favorites(cfg, folder_id)[SOURCE]) == ["Fresh", "Owned"]
    assert "2026-09" not in _favorites(cfg, folder_id)


# ---------------------------------------------------------------------------
# What the landing leaves alone
# ---------------------------------------------------------------------------


def test_an_owned_heart_whose_job_froze_no_date_key_is_left_to_the_backfill(
    native_library, silence
):
    """The landing has no listing to date it from, and Undated is a placement nothing undoes."""
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _owned(cfg, silence, "Old")
    hearts_swept(cfg, {"Old": UNKNOWN})

    code, acted = drive(LAND)

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert _favorites(cfg, folder_id) == {SOURCE: []}


def test_an_owned_heart_the_account_dates_nowhere_goes_to_undated(native_library, silence):
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _owned(cfg, silence, "Dateless")
    hearts_swept(cfg, {"Dateless": None})

    code, acted, _refused = _two_acts(LAND)

    assert code == int(ExitCode.OK), acted
    assert _favorites(cfg, folder_id) == {SOURCE: ["Dateless"], "Undated": ["Dateless"]}


def test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why(native_library, silence):
    cfg, _root_id = native_library
    _owned(cfg, silence, "Owned")
    hearts_swept(cfg, {"Owned": NOV})

    code, acted = drive(LAND)

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    (note,) = [w for w in acted["warnings"] if w["code"] == land_cli.FAVORITES_SKIPPED]
    assert "no owned heart was placed" in note["message"]
    assert _query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name = '2026-11'") == []


def test_an_owned_only_pass_refuses_before_the_gate_with_no_acknowledgment(native_library, silence):
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _owned(cfg, silence, "Owned")
    hearts_swept(cfg, {"Owned": NOV})
    session.ack_path(cfg).unlink()

    code, refused = drive(LAND)

    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert _favorites(cfg, folder_id) == {SOURCE: []}


# ---------------------------------------------------------------------------
# What the review added
# ---------------------------------------------------------------------------


def test_an_owned_heart_whose_file_two_rows_claim_is_not_placed_by_a_guess(native_library, silence):
    """U128's rule for an owned member: a file two active rows claim answers
    nothing, so the landing never files whichever duplicate came first."""
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _owned(cfg, silence, "Twice Imported")
    path = Path(cfg.library.root) / cfg.library.music_dir / "Processed_Tracks" / "2025" / "Twice Imported.flac"
    # A second import of the same file: a row made elsewhere and pointed at it.
    elsewhere = path.with_name("Twice Imported copy.flac")
    shutil.copyfile(silence, elsewhere)
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        second = handle.add_content(elsewhere, Title="Twice Imported")
        second.FolderPath = str(path)
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    elsewhere.unlink()
    assert len(_query(cfg, "SELECT ID FROM djmdContent WHERE FolderPath = ?", str(path))) == 2
    hearts_swept(cfg, {"Twice Imported": NOV})

    code, acted = drive(LAND)

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert _favorites(cfg, folder_id) == {SOURCE: []}


def test_landing_an_older_pass_places_no_owned_heart_once_a_later_hearts_job_ran(
    native_library, silence
):
    """The pass's job is a snapshot of the account; a later hearts job is the
    account's later word, so an older pass cannot put back a heart the author
    dropped since, un-hearted and taken out of All Favorites."""
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _owned(cfg, silence, "Dropped")
    hearts_swept(cfg, {"Dropped": NOV})
    hearts_swept(cfg, {"Other": NOV}, run_id="2026-10-04T101500Z-ef56")

    code, acted = drive(LAND)

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert _favorites(cfg, folder_id) == {SOURCE: []}


def test_an_owned_heart_all_favorites_holds_without_a_month_is_no_write_for_an_empty_landing(
    native_library, silence
):
    """The landing places what All Favorites lacks and nothing else: a month
    for a heart it already holds is the backfill's to give."""
    cfg, _root_id = native_library
    folder_id, source_id = _home(cfg)
    row = _owned(cfg, silence, "Held")
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        handle.add_to_playlist(handle.get_playlist(ID=source_id), row)
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    hearts_swept(cfg, {"Held": NOV})

    code, acted = drive(LAND)

    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    assert _favorites(cfg, folder_id) == {SOURCE: ["Held"]}


def test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart(native_library, silence):
    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _owned(cfg, silence, "Owned")
    hearts_swept(cfg, {"Owned": NOV})
    _stage(cfg, silence, "Loose")

    code, acted, _refused = _two_acts(LAND)

    assert code == int(ExitCode.OK), acted
    assert _favorites(cfg, folder_id) == {SOURCE: ["Owned"], "2026-11": ["Owned"]}
    assert acted["data"]["totals"]["landed"] == 1


def test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale(
    native_library, silence
):
    """The digest covers the owned hearts, so an answer given while one was
    missing is stale once it is in All Favorites. A downloaded heart lands
    beside it, so the placement is planned in both acts and only the owned
    hearts differ between them."""
    cfg, _root_id = native_library
    folder_id, source_id = _home(cfg)
    row = _owned(cfg, silence, "Owned")
    hearts_swept(cfg, {"Owned": NOV, "Fresh": NOV})
    _stage(cfg, silence, "Fresh")
    code, refused = drive(LAND)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(
        ["run", "decide", run_id, land_cli.NATIVE_GATE, "apply", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
    try:
        handle.add_to_playlist(handle.get_playlist(ID=source_id), row)
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)

    code, acted = drive(["--run", run_id, *LAND])

    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "decision-stale", acted["cause"]
    assert _favorites(cfg, folder_id) == {SOURCE: ["Owned"]}, "nothing was written"


# ---------------------------------------------------------------------------
# U153: an owned heart takes Pink, one a person coloured keeps it
# ---------------------------------------------------------------------------

from tests.test_intake_land_hearts_native import PINK_ID, RED_ID, _colour_of  # noqa: E402


def test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held(native_library, silence):
    import sqlite3

    cfg, _root_id = native_library
    folder_id, _source_id = _home(cfg)
    _owned(cfg, silence, "Owned")
    chosen = _owned(cfg, silence, "Chosen")
    conn = sqlite3.connect(cfg.library.db_path)
    conn.execute("UPDATE djmdContent SET ColorID = ? WHERE ID = ?", (RED_ID, chosen))
    conn.commit()
    conn.close()
    hearts_swept(cfg, {"Owned": NOV, "Chosen": NOV})

    code, acted, refused = _two_acts(LAND)

    assert code == int(ExitCode.OK), acted
    assert sorted(_favorites(cfg, folder_id)[SOURCE]) == ["Chosen", "Owned"]
    assert (_colour_of(cfg, "Owned"), _colour_of(cfg, "Chosen")) == (PINK_ID, RED_ID)
    shown = refused["cause"]["detail"]["shown"]
    assert shown["rows to colour Pink"] == 1
    # The held line reads the row's own title, which is the bare tag here.
    assert shown["colour held"] == ["Chosen (Red)"]
    (note,) = [w for w in acted["warnings"] if w["code"] == land_cli.FAVORITES_PLACED]
    assert "1 row(s) coloured Pink" in note["message"]
    (held,) = [w for w in acted["warnings"] if w["code"] == land_cli.FAVORITES_COLOUR_HELD]
    assert held["message"].endswith("keep it: Chosen (Red)")


def test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit(native_library, silence):
    cfg, _root_id = native_library
    _home(cfg)
    _owned(cfg, silence, "Owned")
    hearts_swept(cfg, {"Owned": SEP, "Fresh": NOV})
    _stage(cfg, silence, "Fresh")

    code, acted, refused = _two_acts(LAND)

    assert code == int(ExitCode.OK), acted
    assert (_colour_of(cfg, "Owned"), _colour_of(cfg, "Fresh")) == (PINK_ID, PINK_ID)
    shown = refused["cause"]["detail"]["shown"]
    assert shown["rows to colour Pink"] == 2
    (record,) = [r for r in session.records(cfg) if "favorites_placed" in r.detail]
    assert sorted(record.detail["favorites_placed"]["coloured"]) == sorted(
        str(row) for (row,) in _query(cfg, "SELECT ID FROM djmdContent WHERE Title IN ('Probe - Owned', 'Fresh', 'Owned')")
    )
