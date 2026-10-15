"""U147: what the account mirror reads from the library, on a disposable database.

The routing tree is cut over and its folders and playlists made on the handle,
as the genre Favorites suite makes them, and the Favorites folder beside it.
:func:`account_mirror.read_library` is handed that handle in place of the live
database's, so the walk, the titles and the refusals are read off a real
schema rather than a stand in.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

from cratekit.core import rb_writer
from cratekit.organize import account_mirror
from tests.test_genre_favorites import AFRO, DEEP, Tree
from tests.test_genre_favorites import db as db  # noqa: PLC0414 - fixture
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414


def _read(cfg, db, monkeypatch) -> account_mirror.Library:
    monkeypatch.setattr(rb_writer, "open_db", lambda *args, **kwargs: db)
    monkeypatch.setattr(rb_writer, "close_db", lambda _db: None)
    return account_mirror.read_library(cfg)


def _shape(library: account_mirror.Library) -> dict[str, dict[str, list[str]]]:
    return {
        folder.name: {
            source.name: [row.content_id for row in source.rows] for source in folder.playlists
        }
        for folder in library.folders
    }


def test_every_genre_folder_and_the_favorites_folder_is_read_under_its_account_titles(
    cfg, db, monkeypatch
):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Low", "1", "2")
    tree.playlist(DEEP, "with vox", "2")
    tree.playlist(AFRO, "High", "3")
    source = tree.source("1", "3")
    favorites = db.get_playlist(ID=str(source.ParentID))
    month = db.create_playlist("2026-10", parent=favorites)
    db.add_to_playlist(month, "1")
    undated = db.create_playlist("Undated", parent=favorites)
    db.add_to_playlist(undated, "3")
    # A folder inside a genre folder is no shape the mirror copies, nor its playlists.
    nested = db.create_playlist_folder("Nested", parent=tree.folder(DEEP))
    db.add_to_playlist(db.create_playlist("Deeper", parent=nested), "4")
    db.session.commit()

    read = _read(cfg, db, monkeypatch)

    assert read.refused == {} and read.favorites == ""
    assert _shape(read) == {
        AFRO.display: {f"{AFRO.display} High": ["3"]},
        DEEP.display: {f"{DEEP.display} Low": ["1", "2"], f"{DEEP.display} with vox": ["2"]},
        "Favorites": {
            "All Favorites": ["1", "3"],
            "Favorites 2026-10": ["1"],
            "Favorites Undated": ["3"],
        },
    }


def test_two_tree_folders_of_one_name_refuse_that_name_and_read_the_rest(cfg, db, monkeypatch):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Low", "1")
    twin = db.create_playlist_folder(AFRO.display, parent=tree.root)
    db.create_playlist("Low", parent=twin)
    tree.playlist(AFRO, "High", "3")
    db.session.commit()

    read = _read(cfg, db, monkeypatch)

    assert list(read.refused) == [AFRO.display]
    assert read.refused[AFRO.display].reason == "account-mirror-ambiguous"
    assert [folder.name for folder in read.folders] == [DEEP.display]


def test_a_library_with_no_favourites_playlist_mirrors_the_tree_and_says_why_not_favorites(
    cfg, db, monkeypatch
):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Low", "1")

    read = _read(cfg, db, monkeypatch)

    assert [folder.name for folder in read.folders] == [DEEP.display]
    assert "All Favorites" in read.favorites
