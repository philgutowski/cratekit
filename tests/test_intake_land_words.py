"""U163: a native landing writes artist, album, genre and year on each row from the file.

R-921 asked why a landed row read empty in rekordbox until Reload Tags ran by
hand. These tests drive the real dispatcher and the engine over real FLAC
containers against the disposable database ``tests/test_intake_land_native.py``
builds, and pin what the brief asks: a word with an active lookup row links
it, a word with none mints one and links it in the same commit, a tombstoned
namesake is skipped, a file with no artist leaves the column empty, the key is
never written, the year comes off the date tag, and adoption reads the genre
off the landed row with nothing reloaded.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path

import pytest

from cratekit.adopt import collection
from cratekit.core import config, rb_writer, tags, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import native
from tests._containers import synth_container
from tests.test_intake_land_native import (
    BATCH,
    INTAKE,
    _land,
    _landed_rows,
    _music,
    _query,
    _stage,
    _staging,
    _two_acts,
)
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
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

    kind = {
        rb_writer.ARTIST_TABLE: tables.DjmdArtist,
        rb_writer.ALBUM_TABLE: tables.DjmdAlbum,
        rb_writer.GENRE_TABLE: tables.DjmdGenre,
    }[table]
    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        for values in rows:
            db_session.add(_row(kind, **{rb_writer.SOFT_DELETE_COLUMN: 0, **values}))
        db_session.commit()
    engine.dispose()


def _words(cfg: config.Config, content_id: str) -> tuple:
    """(ArtistID, AlbumID, GenreID, KeyID, ReleaseYear) of one row."""
    ((*found,),) = _query(
        cfg,
        "SELECT ArtistID, AlbumID, GenreID, KeyID, ReleaseYear FROM djmdContent WHERE ID = ?",
        content_id,
    )
    return tuple(found)


def _names(cfg: config.Config, table: str) -> list[tuple]:
    return _query(cfg, f"SELECT ID, Name, rb_local_deleted FROM {table} ORDER BY ID")


def _shown_row(refused: dict, index: int = 0) -> dict:
    return refused["cause"]["detail"]["shown"]["items"][index]["row"]


# ---------------------------------------------------------------------------
# A word with an active row links it; a word with none is minted and linked
# ---------------------------------------------------------------------------


def test_a_word_the_library_holds_links_its_active_row_and_mints_nothing(
    native_library, silence
):
    cfg, _root = native_library
    _seed(cfg, rb_writer.ARTIST_TABLE, {"ID": "501", "Name": "Probe"})
    _seed(cfg, rb_writer.GENRE_TABLE, {"ID": "601", "Name": "Deep House"})
    _stage(cfg, silence, "One.flac")

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    shown = _shown_row(refused)
    assert shown[native.ARTIST_COLUMN] == {"name": "Probe", "row": "501"}
    assert shown[native.GENRE_COLUMN] == {"name": "Deep House", "row": "601"}
    ((content_id, _title, _path),) = _landed_rows(cfg)
    artist, album, genre, _key, _year = _words(cfg, str(content_id))
    assert (str(artist), album, str(genre)) == ("501", None, "601")
    assert [row[1] for row in _names(cfg, rb_writer.ARTIST_TABLE)] == ["Probe"]
    assert [row[1] for row in _names(cfg, rb_writer.GENRE_TABLE)] == ["Deep House"]


def test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit(
    native_library, silence
):
    cfg, _root = native_library
    _tag(
        _stage(cfg, silence, "One.flac"),
        album="Probe Album",
        albumartist="Probe Various",
        date="2021-03-05",
    )
    assert _names(cfg, rb_writer.ARTIST_TABLE) == []

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    shown = _shown_row(refused)
    # THE SCREEN SAYS MINT, with what the mint stores, per word.
    assert shown[native.ARTIST_COLUMN] == {"name": "Probe", "row": "mint", "SearchStr": None}
    assert shown[native.GENRE_COLUMN] == {"name": "Deep House", "row": "mint"}
    assert shown[native.ALBUM_COLUMN] == {
        "name": "Probe Album",
        "row": "mint",
        "album artist": {"name": "Probe Various", "row": "mint", "SearchStr": None},
        "SearchStr": None,
    }
    assert shown[native.YEAR_COLUMN] == 2021
    ((content_id, _title, _path),) = _landed_rows(cfg)
    artist, album, genre, key, year = _words(cfg, str(content_id))
    artists = {name: row_id for row_id, name, _deleted in _names(cfg, rb_writer.ARTIST_TABLE)}
    assert set(artists) == {"Probe", "Probe Various"}
    assert str(artist) == str(artists["Probe"])
    ((album_id, album_name, deleted),) = _names(cfg, rb_writer.ALBUM_TABLE)
    assert (str(album), album_name, deleted) == (str(album_id), "Probe Album", 0)
    ((album_artist,),) = _query(cfg, "SELECT AlbumArtistID FROM djmdAlbum")
    assert str(album_artist) == str(artists["Probe Various"])
    ((genre_id, genre_name, _),) = _names(cfg, rb_writer.GENRE_TABLE)
    assert (str(genre), genre_name) == (str(genre_id), "Deep House")
    # NEVER THE KEY, though the title head carries one; and the date's year.
    assert key is None
    assert year == 2021


def test_two_files_with_one_new_artist_mint_it_once(native_library, silence):
    cfg, _root = native_library
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert [row[1] for row in _names(cfg, rb_writer.ARTIST_TABLE)] == ["Probe"]
    assert [row[1] for row in _names(cfg, rb_writer.GENRE_TABLE)] == ["Deep House"]
    linked = {_words(cfg, str(row[0]))[0] for row in _landed_rows(cfg)}
    assert len(linked) == 1


# ---------------------------------------------------------------------------
# Tombstones, absences and the album's artist
# ---------------------------------------------------------------------------


def test_a_tombstoned_namesake_is_skipped_for_the_active_row_after_it(native_library, silence):
    cfg, _root = native_library
    _seed(
        cfg,
        rb_writer.ARTIST_TABLE,
        {"ID": "501", "Name": "Probe", rb_writer.SOFT_DELETE_COLUMN: 1},
        {"ID": "502", "Name": "Probe"},
    )
    _stage(cfg, silence, "One.flac")

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    ((content_id, _title, _path),) = _landed_rows(cfg)
    assert str(_words(cfg, str(content_id))[0]) == "502"


def test_a_word_whose_only_namesake_is_a_tombstone_is_minted(native_library, silence):
    """The binding's ``add_artist`` refuses this name, which is why the mint is by hand."""
    cfg, _root = native_library
    _seed(
        cfg,
        rb_writer.ARTIST_TABLE,
        {"ID": "501", "Name": "Probe", rb_writer.SOFT_DELETE_COLUMN: 1},
    )
    _stage(cfg, silence, "One.flac")

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    ((content_id, _title, _path),) = _landed_rows(cfg)
    linked = str(_words(cfg, str(content_id))[0])
    assert linked != "501"
    assert ("Probe", 0) in [(name, deleted) for row_id, name, deleted in _names(
        cfg, rb_writer.ARTIST_TABLE
    ) if str(row_id) == linked]


def test_a_file_with_no_artist_leaves_the_column_empty(native_library, silence):
    cfg, _root = native_library
    _strip(_stage(cfg, silence, "One.flac"), "artist")

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert native.ARTIST_COLUMN not in _shown_row(refused)
    ((content_id, _title, _path),) = _landed_rows(cfg)
    artist, album, genre, _key, year = _words(cfg, str(content_id))
    assert (artist, album, year) == (None, None, None)
    assert genre is not None
    assert _names(cfg, rb_writer.ARTIST_TABLE) == []


def test_an_album_links_the_one_its_album_artist_holds(native_library, silence):
    """Two albums of one name stay two: the album is found by name and album artist."""
    cfg, _root = native_library
    _seed(
        cfg,
        rb_writer.ARTIST_TABLE,
        {"ID": "501", "Name": "Probe"},
        {"ID": "502", "Name": "Other"},
    )
    _seed(
        cfg,
        rb_writer.ALBUM_TABLE,
        {"ID": "701", "Name": "Probe Album", "AlbumArtistID": "502"},
        {"ID": "702", "Name": "Probe Album", "AlbumArtistID": "501"},
        {"ID": "703", "Name": "Probe Album"},
    )
    _tag(_stage(cfg, silence, "One.flac"), album="Probe Album", albumartist="Probe")
    _tag(_stage(cfg, silence, "Two.flac"), album="Probe Album")

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    by_name = {Path(row[2]).name: str(row[0]) for row in _landed_rows(cfg)}
    assert str(_words(cfg, by_name["One.flac"])[1]) == "702"
    assert str(_words(cfg, by_name["Two.flac"])[1]) == "703"
    assert len(_names(cfg, rb_writer.ALBUM_TABLE)) == 3


def test_a_mint_follows_the_librarys_searchstr_convention(native_library, silence):
    cfg, _root = native_library
    _seed(
        cfg,
        rb_writer.ARTIST_TABLE,
        {"ID": "501", "Name": "Alpha", "SearchStr": "Alpha"},
        {"ID": "502", "Name": "Beta", "SearchStr": "Beta"},
        {"ID": "503", "Name": "Gamma"},
    )
    _stage(cfg, silence, "One.flac")

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert _shown_row(refused)[native.ARTIST_COLUMN]["SearchStr"] == "Probe"
    ((stored,),) = _query(cfg, "SELECT SearchStr FROM djmdArtist WHERE Name = 'Probe'")
    assert stored == "Probe"


def test_a_multi_value_id3_frame_lands_its_first_value_as_the_word(
    native_library, tmp_path
):
    """Review round one: the ID3 reader joins a frame's values on NUL, and a
    NUL joined name minted a lookup row nothing shares and adoption files
    under no rule. Every container now answers its first value."""
    from mutagen.id3 import ID3, TCON, TPE1

    cfg, _root = native_library
    scratch = tmp_path / "mp3"
    scratch.mkdir()
    path = _staging(cfg) / "One.mp3"
    shutil.copyfile(synth_container(scratch, ".mp3"), path)
    assert tags.write_tags(path, {"title": "01A - 124 - One"})
    frames = ID3(path)
    frames.add(TPE1(encoding=3, text=["Alpha", "Beta"]))
    frames.add(TCON(encoding=3, text=["House", "Techno"]))
    frames.save(path)

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert [row[1] for row in _names(cfg, rb_writer.ARTIST_TABLE)] == ["Alpha"]
    assert [row[1] for row in _names(cfg, rb_writer.GENRE_TABLE)] == ["House"]


@pytest.mark.parametrize(
    ("date", "year"),
    [("2021", 2021), ("2021-03-05", 2021), ("2021-03-05T10:00:00", 2021), ("0000", None),
     ("21", None), ("circa 2021", None), ("", None), (None, None)],
)
def test_the_year_is_the_four_digits_the_date_tag_opens_with(date, year):
    assert native.year_of(date) == year


# ---------------------------------------------------------------------------
# Adoption reads the genre, with nothing reloaded
# ---------------------------------------------------------------------------


def test_adoption_reads_the_landed_rows_genre_with_rekordbox_closed(native_library, silence):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    ((content_id, _title, _path),) = _landed_rows(cfg)
    collection.reset_cache()
    (row,) = [one for one in collection.read_collection(cfg) if one.content_id == str(content_id)]
    assert row.genre == "Deep House"


# ---------------------------------------------------------------------------
# A lookup row that moved since the plan refuses the apply
# ---------------------------------------------------------------------------


def _engine_plan(cfg: config.Config, silence: Path, db) -> native.NativePlan:
    folder = _music(cfg)
    folder.mkdir(parents=True)
    path = _stage(cfg, silence, "One.flac")
    landed = folder / "One.flac"
    path.rename(landed)
    return native.plan_rows(
        cfg,
        db,
        tree_id=INTAKE,
        registry=tree_registry.read(cfg),
        batch=BATCH,
        files=[(landed, landed)],
    )


def test_a_word_minted_by_another_hand_since_the_plan_refuses_and_writes_nothing(
    native_library, silence
):
    cfg, _root = native_library
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        plan = _engine_plan(cfg, silence, db)
        (row,) = plan.to_add()
        assert row.artist is not None and row.artist.row_id == ""
        _seed(cfg, rb_writer.ARTIST_TABLE, {"ID": "501", "Name": "Probe"})
        db.session.expire_all()
        with pytest.raises(CratekitError) as caught:
            native.apply_rows(cfg, db, plan, analysis_roots=[Path(cfg.library.root)])
    finally:
        rb_writer.close_db(db)
    assert caught.value.cause.reason == "decision-stale"
    assert "Probe" in caught.value.cause.message
    assert _landed_rows(cfg) == []
    assert [row[1] for row in _names(cfg, rb_writer.ARTIST_TABLE)] == ["Probe"]


def test_a_landed_row_whose_word_reads_back_wrong_is_refused():
    right = native.AddedRow(
        target=Path(__file__),
        content_id="9",
        title="t",
        folder_path="f",
        empty={},
        file_id=str(native.file_id_of(Path(__file__))),
        content_link=1,
        words={native.ARTIST_COLUMN: "Probe"},
        planned={native.ARTIST_COLUMN: "Probe"},
    )
    landed = native.NativeLanded(
        tree_id="t",
        playlist="p",
        playlist_id="1",
        added=(right,),
        present=(),
        memberships_added=0,
        session_id="s",
        content_link=1,
    )
    native.assert_rows_identified(landed)
    wrong = native.NativeLanded(
        **{
            **{name: getattr(landed, name) for name in native.NativeLanded.__dataclass_fields__},
            "added": (
                native.AddedRow(
                    **{
                        **{name: getattr(right, name) for name in native.AddedRow.__dataclass_fields__},
                        "words": {native.ARTIST_COLUMN: ""},
                    }
                ),
            ),
        }
    )
    with pytest.raises(CratekitError) as caught:
        native.assert_rows_identified(wrong)
    assert native.ARTIST_COLUMN in caught.value.cause.message


# ---------------------------------------------------------------------------
# The mutation table's zeros, each given the test that kills it
# ---------------------------------------------------------------------------


def test_an_album_whose_album_artist_is_minted_is_minted_beside_a_namesake_with_none(
    native_library, silence
):
    """A new album artist holds no album yet, so the album the library holds
    under the same name with no album artist is not the one it links."""
    cfg, _root = native_library
    _seed(cfg, rb_writer.ALBUM_TABLE, {"ID": "701", "Name": "Probe Album"})
    _tag(_stage(cfg, silence, "One.flac"), album="Probe Album", albumartist="Probe Various")

    code, acted, _refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    ((content_id, _title, _path),) = _landed_rows(cfg)
    album = str(_words(cfg, str(content_id))[1])
    assert album != "701"
    ((album_artist,),) = _query(cfg, "SELECT AlbumArtistID FROM djmdAlbum WHERE ID = ?", album)
    ((various,),) = _query(cfg, "SELECT ID FROM djmdArtist WHERE Name = 'Probe Various'")
    assert str(album_artist) == str(various)


def test_a_tied_searchstr_convention_mints_null(native_library, silence):
    cfg, _root = native_library
    _seed(
        cfg,
        rb_writer.ARTIST_TABLE,
        {"ID": "501", "Name": "Alpha", "SearchStr": "Alpha"},
        {"ID": "502", "Name": "Beta"},
    )
    _stage(cfg, silence, "One.flac")

    code, acted, refused = _two_acts(_land())

    assert code == int(ExitCode.OK), acted
    assert _shown_row(refused)[native.ARTIST_COLUMN]["SearchStr"] is None
    ((stored,),) = _query(cfg, "SELECT SearchStr FROM djmdArtist WHERE Name = 'Probe'")
    assert stored is None


def test_the_read_back_takes_no_word_through_a_tombstoned_lookup_row(native_library, silence):
    """A link to a retired row reads as no word, which is what rekordbox shows."""
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    code, acted, _refused = _two_acts(_land())
    assert code == int(ExitCode.OK), acted
    ((content_id, _title, _path),) = _landed_rows(cfg)
    connection = sqlite3.connect(cfg.library.db_path)
    try:
        connection.execute("UPDATE djmdArtist SET rb_local_deleted = 1")
        connection.commit()
    finally:
        connection.close()
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        words = native._words_back(db, str(content_id))
    finally:
        rb_writer.close_db(db)
    assert words[native.ARTIST_COLUMN] == ""
    assert words[native.GENRE_COLUMN] == "Deep House"
