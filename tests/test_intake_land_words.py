"""U163: a native landing writes artist, album, genre and year on each row from the file (R-921).

On the native suite's disposable database. Nothing here is real (D1)."""

from __future__ import annotations

import shutil
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.adopt import collection
from cratekit.core import config, rb_writer, tags, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import native
from tests import test_intake_land_native as land
from tests._containers import synth_container
from tests.test_intake_land_hearts_native import cfg as cfg  # noqa: PLC0414 - the fixture
from tests.test_intake_land_native import _platform_seams as _platform_seams
from tests.test_intake_land_native import _release_process_locks as _release_process_locks
from tests.test_intake_land_native import acknowledged as acknowledged
from tests.test_intake_land_native import library as library
from tests.test_intake_land_native import machine as machine
from tests.test_intake_land_native import native_library as native_library
from tests.test_intake_land_native import silence as silence
from tests.test_rb_writer_db import _row


def _tag(path: Path, **fields: object) -> Path:
    assert tags.write_tags(path, fields)
    return path


def _strip(path: Path, *fields: str) -> Path:
    assert tags.clear_tags(path, fields)
    return path


def _seed(cfg: config.Config, table: str, *rows: dict) -> None:
    """Lookup rows the library already holds, each active unless it says otherwise."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    kind = {rb_writer.ARTIST_TABLE: tables.DjmdArtist, rb_writer.ALBUM_TABLE: tables.DjmdAlbum,
            rb_writer.GENRE_TABLE: tables.DjmdGenre}[table]
    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        for values in rows:
            db_session.add(_row(kind, **{rb_writer.SOFT_DELETE_COLUMN: 0, **values}))
        db_session.commit()
    engine.dispose()


def _words(cfg: config.Config, content_id: str) -> tuple:
    """(ArtistID, AlbumID, GenreID, KeyID, ReleaseYear) of one row."""
    ((*found,),) = land._query(cfg, "SELECT ArtistID, AlbumID, GenreID, KeyID, ReleaseYear FROM "
                          "djmdContent WHERE ID = ?", content_id)
    return tuple(found)


def _names(cfg: config.Config, table: str) -> list[tuple]:
    return land._query(cfg, f"SELECT ID, Name, rb_local_deleted FROM {table} ORDER BY ID")


def _landed_ok() -> dict:
    """Land the staged folder through both acts, and the refusal that showed the gate."""
    code, acted, refused = land._two_acts(land._land())
    assert code == int(ExitCode.OK), acted
    return refused


def _only_id(cfg: config.Config) -> str:
    ((content_id, _title, _path),) = land._landed_rows(cfg)
    return str(content_id)


def _by_name(cfg: config.Config) -> dict[str, str]:
    return {Path(row[2]).name: str(row[0]) for row in land._landed_rows(cfg)}


def _shown_row(refused: dict, index: int = 0) -> dict:
    return refused["cause"]["detail"]["shown"]["items"][index]["row"]


def test_a_word_the_library_holds_links_its_active_row_and_mints_nothing(cfg, silence):
    """A file with no artist leaves the column empty."""
    _seed(cfg, rb_writer.ARTIST_TABLE, {"ID": "501", "Name": "Probe"})
    _seed(cfg, rb_writer.GENRE_TABLE, {"ID": "601", "Name": "Deep House"})
    land._stage(cfg, silence, "One.flac")
    _strip(land._stage(cfg, silence, "Two.flac"), "artist")
    refused = _landed_ok()
    items = refused["cause"]["detail"]["shown"]["items"]
    shown = {Path(item["to"]).name: item["row"] for item in items}
    assert shown["One.flac"][native.ARTIST_COLUMN] == {"name": "Probe", "row": "501"}
    assert shown["One.flac"][native.GENRE_COLUMN] == {"name": "Deep House", "row": "601"}
    assert native.ARTIST_COLUMN not in shown["Two.flac"]
    by_name = _by_name(cfg)
    artist, album, genre, _key, _year = _words(cfg, by_name["One.flac"])
    assert (str(artist), album, str(genre)) == ("501", None, "601")
    artist, album, genre, _key, year = _words(cfg, by_name["Two.flac"])
    assert (artist, album, year) == (None, None, None)
    assert genre is not None
    assert [row[1] for row in _names(cfg, rb_writer.ARTIST_TABLE)] == ["Probe"]
    assert [row[1] for row in _names(cfg, rb_writer.GENRE_TABLE)] == ["Deep House"]


def test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit(cfg, silence):
    """A second file with the same new artist mints it once."""
    _tag(land._stage(cfg, silence, "One.flac"), album="Probe Album", albumartist="Probe Various",
         date="2021-03-05")
    land._stage(cfg, silence, "Two.flac")
    assert _names(cfg, rb_writer.ARTIST_TABLE) == []
    refused = _landed_ok()
    shown = _shown_row(refused)
    # THE SCREEN SAYS MINT, with what the mint stores, per word.
    assert shown[native.ARTIST_COLUMN] == {"name": "Probe", "row": "mint", "SearchStr": None}
    assert shown[native.GENRE_COLUMN] == {"name": "Deep House", "row": "mint"}
    assert shown[native.ALBUM_COLUMN] == {
        "name": "Probe Album", "row": "mint", "SearchStr": None,
        "album artist": {"name": "Probe Various", "row": "mint", "SearchStr": None},
    }
    assert shown[native.YEAR_COLUMN] == 2021
    by_name = _by_name(cfg)
    artist, album, genre, key, year = _words(cfg, by_name["One.flac"])
    assert str(_words(cfg, by_name["Two.flac"])[0]) == str(artist)
    artists = {name: row_id for row_id, name, _deleted in _names(cfg, rb_writer.ARTIST_TABLE)}
    assert sorted(row[1] for row in _names(cfg, rb_writer.ARTIST_TABLE)) == ["Probe", "Probe Various"]
    assert str(artist) == str(artists["Probe"])
    ((album_id, album_name, deleted),) = _names(cfg, rb_writer.ALBUM_TABLE)
    assert (str(album), album_name, deleted) == (str(album_id), "Probe Album", 0)
    ((album_artist,),) = land._query(cfg, "SELECT AlbumArtistID FROM djmdAlbum")
    assert str(album_artist) == str(artists["Probe Various"])
    ((genre_id, genre_name, _),) = _names(cfg, rb_writer.GENRE_TABLE)
    assert (str(genre), genre_name) == (str(genre_id), "Deep House")
    # NEVER THE KEY, though the title head carries one; and the date's year.
    assert key is None
    assert year == 2021


def test_a_tombstoned_namesake_is_skipped_for_the_active_row_after_it_or_else_minted(cfg, silence):
    """``add_artist`` refuses a name whose only namesake is a tombstone, so the mint is by hand."""
    gone = {rb_writer.SOFT_DELETE_COLUMN: 1}
    _seed(cfg, rb_writer.ARTIST_TABLE, {"ID": "501", "Name": "Probe", **gone},
          {"ID": "502", "Name": "Other", **gone}, {"ID": "503", "Name": "Other"})
    land._stage(cfg, silence, "One.flac")
    _tag(land._stage(cfg, silence, "Two.flac"), artist="Other")
    _landed_ok()
    by_name = _by_name(cfg)
    assert str(_words(cfg, by_name["Two.flac"])[0]) == "503"
    linked = str(_words(cfg, by_name["One.flac"])[0])
    assert linked != "501"
    named = _names(cfg, rb_writer.ARTIST_TABLE)
    assert ("Probe", 0) in [(name, gone) for row_id, name, gone in named if str(row_id) == linked]


def test_an_album_links_the_one_its_album_artist_holds(cfg, silence):
    """Two albums of one name stay two, found by name and album artist; a new album artist
    holds no album yet, so a namesake with none is not linked."""
    _seed(cfg, rb_writer.ARTIST_TABLE, {"ID": "501", "Name": "Probe"},
          {"ID": "502", "Name": "Other"})
    _seed(cfg, rb_writer.ALBUM_TABLE, {"ID": "701", "Name": "Probe Album", "AlbumArtistID": "502"},
          {"ID": "702", "Name": "Probe Album", "AlbumArtistID": "501"},
          {"ID": "703", "Name": "Probe Album"})
    _tag(land._stage(cfg, silence, "One.flac"), album="Probe Album", albumartist="Probe")
    _tag(land._stage(cfg, silence, "Two.flac"), album="Probe Album")
    _tag(land._stage(cfg, silence, "Three.flac"), album="Probe Album", albumartist="Probe Various")
    _landed_ok()
    by_name = _by_name(cfg)
    assert str(_words(cfg, by_name["One.flac"])[1]) == "702"
    assert str(_words(cfg, by_name["Two.flac"])[1]) == "703"
    album = str(_words(cfg, by_name["Three.flac"])[1])
    assert album not in ("701", "702", "703")
    assert len(_names(cfg, rb_writer.ALBUM_TABLE)) == 4
    ((album_artist,),) = land._query(cfg, "SELECT AlbumArtistID FROM djmdAlbum WHERE ID = ?", album)
    ((various,),) = land._query(cfg, "SELECT ID FROM djmdArtist WHERE Name = 'Probe Various'")
    assert str(album_artist) == str(various)


def test_a_mint_follows_the_librarys_searchstr_convention(cfg, silence):
    _seed(cfg, rb_writer.ARTIST_TABLE, {"ID": "501", "Name": "Alpha", "SearchStr": "Alpha"},
          {"ID": "502", "Name": "Beta", "SearchStr": "Beta"}, {"ID": "503", "Name": "Gamma"})
    land._stage(cfg, silence, "One.flac")
    refused = _landed_ok()
    assert _shown_row(refused)[native.ARTIST_COLUMN]["SearchStr"] == "Probe"
    ((stored,),) = land._query(cfg, "SELECT SearchStr FROM djmdArtist WHERE Name = 'Probe'")
    assert stored == "Probe"


def test_a_multi_value_id3_frame_lands_its_first_value_as_the_word(cfg, tmp_path):
    """A NUL joined name would mint a lookup row nothing shares, so the first value."""
    from mutagen.id3 import ID3, TCON, TPE1
    scratch = tmp_path / "mp3"
    scratch.mkdir()
    path = land._staging(cfg) / "One.mp3"
    shutil.copyfile(synth_container(scratch, ".mp3"), path)
    assert tags.write_tags(path, {"title": "01A - 124 - One"})
    frames = ID3(path)
    frames.add(TPE1(encoding=3, text=["Alpha", "Beta"]))
    frames.add(TCON(encoding=3, text=["House", "Techno"]))
    frames.save(path)
    _landed_ok()
    assert [row[1] for row in _names(cfg, rb_writer.ARTIST_TABLE)] == ["Alpha"]
    assert [row[1] for row in _names(cfg, rb_writer.GENRE_TABLE)] == ["House"]


@pytest.mark.parametrize(
    ("date", "year"),
    [("2021", 2021), ("2021-03-05", 2021), ("2021-03-05T10:00:00", 2021), ("0000", None),
     ("21", None), ("circa 2021", None), ("", None), (None, None)])
def test_the_year_is_the_four_digits_the_date_tag_opens_with(date, year):
    assert native.year_of(date) == year


def _engine_plan(cfg: config.Config, silence: Path, db) -> native.NativePlan:
    folder = land._music(cfg)
    folder.mkdir(parents=True)
    path = land._stage(cfg, silence, "One.flac")
    landed = folder / "One.flac"
    path.rename(landed)
    registry = tree_registry.read(cfg)
    return native.plan_rows(
        cfg, db, tree_id=land.INTAKE, registry=registry, batch=land.BATCH, files=[(landed, landed)])


def test_a_word_minted_by_another_hand_since_the_plan_refuses_and_writes_nothing(cfg, silence):
    with land._opened(cfg) as db:
        plan = _engine_plan(cfg, silence, db)
        (row,) = plan.to_add()
        assert row.artist is not None and row.artist.row_id == ""
        _seed(cfg, rb_writer.ARTIST_TABLE, {"ID": "501", "Name": "Probe"})
        db.session.expire_all()
        with pytest.raises(CratekitError) as caught:
            native.apply_rows(cfg, db, plan, analysis_roots=[Path(cfg.library.root)])
    assert caught.value.cause.reason == "decision-stale"
    assert "Probe" in caught.value.cause.message
    assert land._landed_rows(cfg) == []
    assert [row[1] for row in _names(cfg, rb_writer.ARTIST_TABLE)] == ["Probe"]


def test_a_landed_row_whose_word_reads_back_wrong_is_refused():
    right = native.AddedRow(
        target=Path(__file__), content_id="9", title="t", folder_path="f", empty={},
        file_id=str(native.file_id_of(Path(__file__))), content_link=1,
        words={native.ARTIST_COLUMN: "Probe"}, planned={native.ARTIST_COLUMN: "Probe"})
    landed = native.NativeLanded(
        tree_id="t", playlist="p", playlist_id="1", added=(right,), present=(), memberships_added=0,
        session_id="s", content_link=1)
    native.assert_rows_identified(landed)
    wrong = replace(landed, added=(replace(right, words={native.ARTIST_COLUMN: ""}),))
    with pytest.raises(CratekitError) as caught:
        native.assert_rows_identified(wrong)
    assert native.ARTIST_COLUMN in caught.value.cause.message


def test_a_tied_searchstr_convention_mints_null(cfg, silence):
    _seed(cfg, rb_writer.ARTIST_TABLE, {"ID": "501", "Name": "Alpha", "SearchStr": "Alpha"},
          {"ID": "502", "Name": "Beta"})
    land._stage(cfg, silence, "One.flac")
    refused = _landed_ok()
    assert _shown_row(refused)[native.ARTIST_COLUMN]["SearchStr"] is None
    ((stored,),) = land._query(cfg, "SELECT SearchStr FROM djmdArtist WHERE Name = 'Probe'")
    assert stored is None


def test_the_read_back_takes_no_word_through_a_tombstoned_lookup_row(cfg, silence):
    """A link to a retired row reads as no word, as rekordbox shows it, after adoption read it."""
    land._stage(cfg, silence, "One.flac")
    _landed_ok()
    content_id = _only_id(cfg)
    collection.reset_cache()
    (row,) = [one for one in collection.read_collection(cfg) if one.content_id == content_id]
    assert row.genre == "Deep House"
    land._execute(cfg, "UPDATE djmdArtist SET rb_local_deleted = 1")
    with land._opened(cfg) as db:
        words = native._words_back(db, content_id)
    assert words[native.ARTIST_COLUMN] == ""
    assert words[native.GENRE_COLUMN] == "Deep House"
