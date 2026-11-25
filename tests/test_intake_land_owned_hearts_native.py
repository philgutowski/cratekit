"""U146 on the native medium: a heart on an owned track joins All Favorites and its month.

``crate intake land --pass`` places a held hearted track under the landing's gate, with or
without a file to land; nothing is downloaded or removed. D1."""

from __future__ import annotations

import shutil
from pathlib import Path

from cratekit.core import config, rb_writer, session, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import backfill
from cratekit.intake import land_cli
from tests import test_intake_land_hearts_native as hearts
from tests.cli_drive import drive
from tests.test_intake_land_account_playlists_native import PASS, _opened, _stage
from tests.test_intake_land_account_playlists_native import pinned_day as pinned_day
from tests.test_intake_land_hearts_native import NOV, PINK_ID, RED_ID, SEP, SOURCE, UNKNOWN
from tests.test_intake_land_hearts_native import cfg as cfg  # noqa: PLC0414 - the fixture
from tests.test_intake_land_native import _answered, _execute, _lands, _query
from tests.test_intake_land_native import _platform_seams as _platform_seams
from tests.test_intake_land_native import _release_process_locks as _release_process_locks
from tests.test_intake_land_native import acknowledged as acknowledged
from tests.test_intake_land_native import library as library
from tests.test_intake_land_native import machine as machine
from tests.test_intake_land_native import native_library as native_library
from tests.test_intake_land_native import silence as silence

LAND = ["intake", "land", "--pass", PASS]


def _owned_path(cfg: config.Config, title: str) -> Path:
    return Path(cfg.library.root) / cfg.library.music_dir / "Processed_Tracks" / "2025" / f"{title}.flac"


def _owned(cfg: config.Config, silence: Path, title: str) -> str:
    """A track the library holds, two folders deep with its row, as the source system filed it."""
    path = _owned_path(cfg, title)
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(silence, path)
    assert tags.write_tags(path, {"title": title, "artist": "Probe", "genre": "Deep House"})
    with _opened(cfg) as handle:
        row = handle.add_content(path, Title=title)
        handle.session.commit()
        return str(row.ID)


def _content_count(cfg: config.Config) -> int:
    return int(_query(cfg, "SELECT COUNT(*) FROM djmdContent")[0][0])


def _live(cfg: config.Config, playlist_id: str) -> list[str]:
    """The members a person sees, the removed rows left out, which ``_favorites`` keeps."""
    live = "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? AND rb_local_deleted = 0"
    return [str(row[0]) for row in _query(cfg, live, playlist_id)]


def _no_op() -> dict:
    """One run of the landing, which must succeed having done nothing."""
    code, acted = drive(LAND)
    assert code == int(ExitCode.OK), acted
    assert acted["outcome"] == "no_op"
    return acted


def _hold(cfg: config.Config, source_id: str, row: str) -> None:
    """All Favorites already holds ``row``."""
    with _opened(cfg) as handle:
        handle.add_to_playlist(handle.get_playlist(ID=source_id), row)
        handle.session.commit()


def _colour_red(cfg: config.Config, row: str) -> None:
    """A person coloured ``row`` Red."""
    _execute(cfg, "UPDATE djmdContent SET ColorID = ? WHERE ID = ?", RED_ID, row)


def _mark_removed(cfg: config.Config, playlist_id: str, content_id: str) -> None:
    """A person takes the track out of the playlist in rekordbox: the row stays, marked removed."""
    with _opened(cfg) as handle:
        songs = handle.get_playlist_songs(PlaylistID=playlist_id)
        (entry,) = [row for row in songs if str(row.ContentID) == content_id]
        entry.rb_local_deleted = 1
        handle.session.commit()


def test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded(
        cfg, silence):
    folder_id, source_id = hearts._home(cfg)
    row = _owned(cfg, silence, "Owned")
    hearts.hearts_swept(cfg, {"Owned": NOV})
    rows_before = _content_count(cfg)
    acted, refused = _lands(verb=LAND)
    assert hearts._favorites(cfg, folder_id) == {SOURCE: ["Owned"], "2026-11": ["Owned"]}
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
    # Run again, every owned heart is placed, so it asks nothing and ends no-op.
    assert _no_op()["data"]["totals"] == {"count": 0}
    assert hearts._favorites(cfg, folder_id) == {SOURCE: ["Owned"], "2026-11": ["Owned"]}
    # Removed from All Favorites by hand and still hearted, it joins again.
    _mark_removed(cfg, source_id, row)
    assert _live(cfg, source_id) == []
    hearts.hearts_swept(cfg, {"Owned": NOV})
    acted, _refused = _lands(verb=LAND)
    assert _live(cfg, source_id) == [row]
    assert hearts._favorites(cfg, folder_id)["2026-11"] == ["Owned"]
    assert acted["data"]["totals"]["hearts placed"] == 1, "the month already held it"


def test_a_pass_with_no_hearts_job_opens_nothing_and_ends_no_op(cfg, monkeypatch):
    """The empty landing as it always was: no owned heart, no database opened."""
    hearts._home(cfg)
    opened: list[object] = []
    real = rb_writer.open_db

    def counting(*args, **kwargs):
        opened.append(args)
        return real(*args, **kwargs)
    monkeypatch.setattr(rb_writer, "open_db", counting)
    _no_op()
    assert opened == []


def test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one(cfg, silence):
    folder_id, _source_id = hearts._home(cfg)
    _owned(cfg, silence, "Owned")
    hearts.hearts_swept(cfg, {"Owned": SEP, "Fresh": NOV})
    _stage(cfg, silence, "Fresh")
    acted, refused = _lands(verb=LAND)
    placed = hearts._favorites(cfg, folder_id)
    assert sorted(placed[SOURCE]) == ["Fresh", "Owned"]
    assert (placed["2026-09"], placed["2026-11"]) == (["Owned"], ["Fresh"])
    shown = refused["cause"]["detail"]["shown"]
    assert shown["owned hearts"] == ["Probe - Owned, 2026-09"]
    assert shown["hearts"].startswith("1 file(s) the account hearts and 1 owned track(s), into")
    assert shown["month playlists"] == ["2026-09 (0 file(s), 1 owned), made", "2026-11 (1 file(s)), made"]
    assert acted["data"]["totals"]["hearts placed"] == 4
    # One session wrote the batch and both hearts, each row coloured Pink (U153).
    (record,) = [r for r in session.records(cfg) if "favorites_placed" in r.detail]
    assert record.detail["favorites_placed"]["added_source"] == 2
    assert (hearts._colour_of(cfg, "Owned"), hearts._colour_of(cfg, "Fresh")) == (PINK_ID, PINK_ID)
    assert shown["rows to colour Pink"] == 2
    both = _query(cfg, "SELECT ID FROM djmdContent WHERE Title IN ('Fresh', 'Owned')")
    coloured = record.detail["favorites_placed"]["coloured"]
    assert sorted(coloured) == sorted(str(row) for (row,) in both)


def test_an_owned_heart_all_favorites_holds_is_no_write_beside_a_landing(cfg, silence):
    folder_id, source_id = hearts._home(cfg)
    row = _owned(cfg, silence, "Owned")
    _hold(cfg, source_id, row)
    hearts.hearts_swept(cfg, {"Owned": SEP, "Fresh": NOV})
    _stage(cfg, silence, "Fresh")
    acted, refused = _lands(verb=LAND)
    assert "owned hearts" not in refused["cause"]["detail"]["shown"]
    assert sorted(hearts._favorites(cfg, folder_id)[SOURCE]) == ["Fresh", "Owned"]
    assert "2026-09" not in hearts._favorites(cfg, folder_id)


def test_an_owned_heart_the_account_dates_nowhere_goes_to_undated(cfg, silence):
    """Once acknowledged: an owned only pass refuses before the gate without it."""
    folder_id, _source_id = hearts._home(cfg)
    _owned(cfg, silence, "Dateless")
    hearts.hearts_swept(cfg, {"Dateless": None})
    session.ack_path(cfg).unlink()
    code, refused = drive(LAND)
    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert hearts._favorites(cfg, folder_id) == {SOURCE: []}
    session.record_acknowledgment(cfg, terminal=lambda: True)
    acted, _refused = _lands(verb=LAND)
    assert hearts._favorites(cfg, folder_id) == {SOURCE: ["Dateless"], "Undated": ["Dateless"]}


def test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why(cfg, silence):
    _owned(cfg, silence, "Owned")
    hearts.hearts_swept(cfg, {"Owned": NOV})
    acted = _no_op()
    (note,) = [w for w in acted["warnings"] if w["code"] == land_cli.FAVORITES_SKIPPED]
    assert "no owned heart was placed" in note["message"]
    assert _query(cfg, "SELECT ID FROM djmdPlaylist WHERE Name = '2026-11'") == []


def test_owned_hearts_an_empty_landing_cannot_place_alone_are_no_write(cfg, silence):
    """No listing dates a job that froze no date key, and Undated is undone by nothing; a file
    two active rows claim answers nothing (U128); a held heart's month is the backfill's."""
    folder_id, source_id = hearts._home(cfg)
    _owned(cfg, silence, "Old")
    _hold(cfg, source_id, _owned(cfg, silence, "Held"))
    _owned(cfg, silence, "Twice Imported")
    path = _owned_path(cfg, "Twice Imported")
    # A second import of the same file: a row made elsewhere and pointed at it.
    elsewhere = path.with_name("Twice Imported copy.flac")
    shutil.copyfile(silence, elsewhere)
    with _opened(cfg) as handle:
        second = handle.add_content(elsewhere, Title="Twice Imported")
        second.FolderPath = str(path)
        handle.session.commit()
    elsewhere.unlink()
    assert len(_query(cfg, "SELECT ID FROM djmdContent WHERE FolderPath = ?", str(path))) == 2
    hearts.hearts_swept(cfg, {"Old": UNKNOWN, "Held": NOV, "Twice Imported": NOV})
    _no_op()
    assert hearts._favorites(cfg, folder_id) == {SOURCE: ["Held"]}


def test_landing_an_older_pass_places_no_owned_heart_once_a_later_hearts_job_ran(cfg, silence):
    """A later hearts job is the account's later word: an older pass puts back no dropped heart."""
    folder_id, _source_id = hearts._home(cfg)
    _owned(cfg, silence, "Dropped")
    hearts.hearts_swept(cfg, {"Dropped": NOV})
    hearts.hearts_swept(cfg, {"Other": NOV}, run_id="2026-10-04T101500Z-ef56")
    _no_op()
    assert hearts._favorites(cfg, folder_id) == {SOURCE: []}


def test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart(cfg, silence):
    folder_id, _source_id = hearts._home(cfg)
    _owned(cfg, silence, "Owned")
    hearts.hearts_swept(cfg, {"Owned": NOV})
    _stage(cfg, silence, "Loose")
    acted, _refused = _lands(verb=LAND)
    assert hearts._favorites(cfg, folder_id) == {SOURCE: ["Owned"], "2026-11": ["Owned"]}
    assert acted["data"]["totals"]["landed"] == 1


def test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale(cfg, silence):
    """The digest covers the owned hearts, so one placed by hand between the acts is stale."""
    folder_id, source_id = hearts._home(cfg)
    row = _owned(cfg, silence, "Owned")
    hearts.hearts_swept(cfg, {"Owned": NOV, "Fresh": NOV})
    _stage(cfg, silence, "Fresh")
    run_id = _answered(LAND, land_cli.NATIVE_GATE)[1]
    _hold(cfg, source_id, row)
    code, acted = drive(["--run", run_id, *LAND])
    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "decision-stale", acted["cause"]
    assert hearts._favorites(cfg, folder_id) == {SOURCE: ["Owned"]}, "nothing was written"


def test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held(cfg, silence):
    folder_id, _source_id = hearts._home(cfg)
    _owned(cfg, silence, "Owned")
    chosen = _owned(cfg, silence, "Chosen")
    _colour_red(cfg, chosen)
    hearts.hearts_swept(cfg, {"Owned": NOV, "Chosen": NOV})
    acted, refused = _lands(verb=LAND)
    assert sorted(hearts._favorites(cfg, folder_id)[SOURCE]) == ["Chosen", "Owned"]
    assert (hearts._colour_of(cfg, "Owned"), hearts._colour_of(cfg, "Chosen")) == (PINK_ID, RED_ID)
    shown = refused["cause"]["detail"]["shown"]
    assert shown["rows to colour Pink"] == 1
    # The held line reads the row's own title, which is the bare tag here.
    assert shown["colour held"] == ["Chosen (Red)"]
    (note,) = [w for w in acted["warnings"] if w["code"] == land_cli.FAVORITES_PLACED]
    assert "1 row(s) coloured Pink" in note["message"]
    (held,) = [w for w in acted["warnings"] if w["code"] == land_cli.FAVORITES_COLOUR_HELD]
    assert held["message"].endswith("keep it: Chosen (Red)")


def test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named(cfg, silence):
    """U153 L2: beside a landing file, the held note names an owned heart a person coloured."""
    hearts._home(cfg)
    chosen = _owned(cfg, silence, "Chosen")
    _colour_red(cfg, chosen)
    hearts.hearts_swept(cfg, {"Chosen": SEP, "Fresh": NOV})
    _stage(cfg, silence, "Fresh")
    acted, _refused = _lands(verb=LAND)
    assert hearts._colour_of(cfg, "Chosen") == RED_ID and hearts._colour_of(cfg, "Fresh") == PINK_ID
    (held,) = [w for w in acted["warnings"] if w["code"] == land_cli.FAVORITES_COLOUR_HELD]
    assert held["message"].endswith("keep it: Chosen (Red)")


def test_a_coloured_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale(
    cfg, silence
):
    """A person coloured it, so no Pink row names it: only the owned key of the digest can."""
    folder_id, source_id = hearts._home(cfg)
    row = _owned(cfg, silence, "Chosen")
    _colour_red(cfg, row)
    hearts.hearts_swept(cfg, {"Chosen": NOV, "Fresh": NOV})
    _stage(cfg, silence, "Fresh")
    run_id = _answered(LAND, land_cli.NATIVE_GATE)[1]
    _hold(cfg, source_id, row)
    code, acted = drive(["--run", run_id, *LAND])
    assert code != int(ExitCode.OK), acted
    assert acted["cause"]["reason"] == "decision-stale", acted["cause"]
    assert hearts._favorites(cfg, folder_id) == {SOURCE: ["Chosen"]}, "nothing was written"
