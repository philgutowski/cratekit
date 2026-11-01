"""Another app's folder at the top of rekordbox's tree is left exactly as it is (U185).

DEADCA7 pushes its playlists into a folder named ``DEADCA7`` at the top of the
playlist tree. The predicate that names that folder, the commit guard every
write in the product passes through, and the taxonomy's refusal of a tree of
that name are driven here against a disposable database carrying a push
written the way the push writes it (``tests/deadca7_fixtures.py``).
"""

from __future__ import annotations

import sqlite3

import pytest

from cratekit.cli import setup as setup_verb
from cratekit.core import foreign_tree, taxonomy
from cratekit.core import rb_writer as W
from tests import deadca7_fixtures as dc7
from tests.test_rb_writer_db import (  # noqa: F401 - fixtures
    _build_disposable_database,
    cloud_sync_off,
    library,
)


@pytest.fixture(autouse=True)
def _rekordbox_closed(monkeypatch):
    """No rekordbox on a disposable database, patched where the guards read it."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)


@pytest.fixture
def pushed_db(library):  # noqa: F811 - the imported fixture
    """A disposable database holding two tracks and one DEADCA7 push of both."""
    path = library / "db" / "master.db"
    _build_disposable_database(path)
    return path, dc7.push(path, ("1", "2"))


@pytest.fixture
def handle(pushed_db, cloud_sync_off):  # noqa: F811 - the imported fixture
    path, pushed = pushed_db
    db = W.open_db(path, unlock=False)
    try:
        yield db, path, pushed
    finally:
        W.close_db(db)


def _refused(db) -> str:
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.commit_guarded(db)
    assert excinfo.value.cause.reason == "whitelist-violation"
    return str(excinfo.value)


# ---------------------------------------------------------------------------
# The predicate
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("parent", W.ROOT_PARENT_SENTINELS + (None,))
def test_a_folder_named_deadca7_at_the_top_is_foreign_under_every_root_spelling(parent):
    assert foreign_tree.is_foreign_root("DEADCA7", parent, 1)


@pytest.mark.parametrize(
    ("name", "parent", "attribute", "why"),
    [
        ("DEADCA7", "root", 0, "a plain playlist of the name is not the shape the push writes"),
        ("DEADCA7", "root", 4, "a smart playlist of the name is not either"),
        ("DEADCA7", "12", 1, "a folder of the name below the top is a namesake"),
        ("deadca7", "root", 1, "the name is matched with its case"),
        ("DEADCA7 sets", "root", 1, "the name is matched whole"),
        ("DEADCA7", "root", None, "a row that cannot say it is a folder is not one"),
        ("DEADCA7", "root", "x", "nor one whose kind is not a number"),
    ],
)
def test_nothing_else_is_a_foreign_root(name, parent, attribute, why):
    assert not foreign_tree.is_foreign_root(name, parent, attribute), why


def test_every_node_under_the_root_is_foreign_at_any_depth_and_nothing_beside_it():
    roots, ids = foreign_tree.ids_of(
        [
            ("1", "DEADCA7", "root", 1),
            ("2", "sets", "1", 1),
            ("3", "peak", "2", 0),
            ("4", "warm up", "1", 0),
            ("5", "Mine", "root", 1),
            ("6", "DEADCA7", "5", 1),
            ("7", "inside the namesake", "6", 0),
        ]
    )
    assert roots == {"1"}
    assert ids == {"1", "2", "3", "4"}


def test_a_cycle_ends_the_walk_rather_than_looping():
    _roots, ids = foreign_tree.ids_of(
        [("1", "DEADCA7", "root", 1), ("2", "a", "3", 1), ("3", "b", "2", 1), ("4", "c", "1", 0)]
    )
    assert ids == {"1", "4"}


def test_the_reading_at_open_names_the_push_and_not_a_namesake_below_the_top(
    pushed_db, cloud_sync_off  # noqa: F811 - the imported fixture
):
    path, pushed = pushed_db
    conn = sqlite3.connect(path)
    conn.execute(
        "INSERT INTO djmdPlaylist (ID, Seq, Name, Attribute, ParentID, rb_local_deleted) "
        "VALUES ('88950', 1, 'Mine', 1, 'root', 0)"
    )
    conn.commit()
    conn.close()
    dc7.nested_namesake(path, "88950", node_id="88900")
    db = W.open_db(path, unlock=False)
    try:
        reading = foreign_tree.reading_at_open(db)
    finally:
        W.close_db(db)
    assert reading is not None
    assert reading.roots == {pushed.folder_id}
    assert reading.ids == {pushed.folder_id, *pushed.playlist_ids}
    assert set(reading.memberships) == {
        f"{playlist}{n:02d}" for playlist in pushed.playlist_ids for n in (1, 2)
    }


# ---------------------------------------------------------------------------
# The commit guard
# ---------------------------------------------------------------------------


def test_renaming_the_folder_is_refused_and_rolled_back(handle):
    db, path, pushed = handle
    before = dc7.written(path, pushed)
    db.get_playlist(ID=pushed.folder_id).Name = "renamed"
    assert "DEADCA7's folder" in _refused(db)
    assert dc7.written(path, pushed) == before


def test_a_membership_added_to_a_pushed_playlist_is_refused(handle):
    db, path, pushed = handle
    before = dc7.written(path, pushed)
    db.add_to_playlist(db.get_playlist(ID=pushed.playlist_ids[0]), "1")
    assert "membership" in _refused(db)
    assert dc7.written(path, pushed) == before


def test_a_pushed_membership_rewritten_to_another_owner_is_refused(handle):
    """Read by its new owner alone, the row would leave the push's playlist unseen."""
    db, path, pushed = handle
    before = dc7.written(path, pushed)
    mine = db.create_playlist("mine at the top")
    W.commit_guarded(db)
    member = db.get_playlist_songs(PlaylistID=pushed.playlist_ids[0]).first()
    member.PlaylistID = mine.ID
    assert "membership" in _refused(db)
    assert dc7.written(path, pushed) == before


def test_a_playlist_made_inside_the_folder_is_refused(handle):
    db, path, pushed = handle
    before = dc7.written(path, pushed)
    W.ensure_playlist(db, "a new one", db.get_playlist(ID=pushed.folder_id))
    assert "inside DEADCA7's folder" in _refused(db)
    assert dc7.written(path, pushed) == before


def test_a_pushed_playlist_moved_out_of_the_folder_is_refused(handle):
    db, path, pushed = handle
    before = dc7.written(path, pushed)
    mine = db.create_playlist_folder("Mine")
    W.commit_guarded(db)
    db.move_playlist(db.get_playlist(ID=pushed.playlist_ids[1]), mine)
    assert "DEADCA7's folder" in _refused(db)
    assert dc7.written(path, pushed)["djmdSongPlaylist"] == before["djmdSongPlaylist"]
    assert [row[5] for row in dc7.written(path, pushed)["djmdPlaylist"]][1:] == [
        pushed.folder_id
    ] * 2


def test_a_playlist_of_ones_own_moved_into_the_folder_is_refused(handle):
    db, path, pushed = handle
    mine = db.create_playlist("mine")
    W.commit_guarded(db)
    db.move_playlist(mine, db.get_playlist(ID=pushed.folder_id))
    assert "into DEADCA7's folder" in _refused(db) or "DEADCA7's folder" in _refused(db)


def test_a_soft_delete_of_a_pushed_playlist_is_refused_even_where_the_commit_admits_removals(
    handle,
):
    """The removal a few writers may ask for by name is still not one of these."""
    db, path, pushed = handle
    before = dc7.written(path, pushed)
    row = db.get_playlist(ID=pushed.playlist_ids[0])
    setattr(row, W.SOFT_DELETE_COLUMN, 1)
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.commit_guarded(db, removals=(W.PLAYLIST_TABLE, W.MEMBERSHIP_TABLE))
    assert "DEADCA7's folder" in str(excinfo.value)
    assert dc7.written(path, pushed) == before


def test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql(handle):
    """No pending object carries this one: only the second reading can see it."""
    from sqlalchemy import text

    db, path, pushed = handle
    membership = f"{pushed.playlist_ids[0]}01"
    db.session.execute(
        text("UPDATE djmdSongPlaylist SET TrackNo = 9 WHERE ID = :id"), {"id": membership}
    )
    message = _refused(db)
    assert membership in message and "changed" in message


def test_a_second_folder_of_the_name_at_the_top_is_refused(handle):
    db, _path, _pushed = handle
    db.create_playlist_folder("DEADCA7")
    assert "second DEADCA7 folder" in _refused(db)


def test_a_write_beside_the_folder_commits_and_leaves_every_row_the_push_wrote(handle):
    """A root playlist and folder of one's own, and a playlist in that folder.

    Appended at the top, as every writer here makes them, so no sibling is
    renumbered and the push's rows are byte for byte what they were.
    """
    db, path, pushed = handle
    before = dc7.written(path, pushed)
    db.create_playlist("mine at the top")
    W.ensure_playlist(db, "in mine", W.ensure_folder(db, "Mine"))
    W.commit_guarded(db)
    assert {str(row.Name) for row in db.get_playlist()} >= {"mine at the top", "Mine", "in mine"}
    assert dc7.written(path, pushed) == before


def test_a_position_named_at_the_top_moves_the_folder_and_is_refused(handle):
    """The one write that renumbers root siblings, which nothing in the product makes."""
    db, path, pushed = handle
    before = dc7.written(path, pushed)
    db.create_playlist("first at the top", seq=1)
    assert "Seq" in _refused(db)
    assert dc7.written(path, pushed) == before


def test_a_handle_with_no_reading_at_open_refuses_rather_than_assuming_nothing_is_there(handle):
    db, _path, _pushed = handle
    delattr(db, foreign_tree.ATTRIBUTE)
    db.create_playlist("mine at the top")
    assert "was not read when this database handle opened" in _refused(db)


def test_a_reading_that_failed_at_open_is_kept_as_unread_and_refuses(handle):
    db, _path, _pushed = handle

    class _Broken:
        def execute(self, *_args, **_kwargs):
            raise RuntimeError("the table could not be read")

    class _Handle:
        session = _Broken()

    held = _Handle()
    foreign_tree.remember(held)
    assert getattr(held, foreign_tree.ATTRIBUTE) == foreign_tree.UNREAD
    assert foreign_tree.reading_at_open(held) is None
    setattr(db, foreign_tree.ATTRIBUTE, foreign_tree.UNREAD)
    db.create_playlist("mine at the top")
    assert "was not read when this database handle opened" in _refused(db)


def test_a_cue_write_on_a_pushed_track_is_refused_by_the_whitelist(handle):
    """Nothing in the product writes a cue row, and the whitelist holds it so."""
    db, path, pushed = handle
    before = dc7.written(path, pushed)
    cue = db.get_cue(ContentID=pushed.pushed_track).first()
    cue.InMsec = 5
    message = _refused(db)
    assert "djmdCue" in message
    assert dc7.written(path, pushed) == before


# ---------------------------------------------------------------------------
# The taxonomy
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("section", "display"),
    [("tree", "BY GENRE + ENERGY")],
)
def test_a_tree_declared_with_the_folders_name_is_refused_so_none_adopts_it(section, display):
    text = setup_verb.template_text("default")
    assert f'display = "{display}"' in text
    taxonomy.load_taxonomy(text)
    with pytest.raises(taxonomy.TaxonomyError) as excinfo:
        taxonomy.load_taxonomy(text.replace(f'display = "{display}"', 'display = "DEADCA7"', 1))
    assert f"[{section}] display 'DEADCA7'" in str(excinfo.value)


def test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit(
    library, cloud_sync_off  # noqa: F811 - the imported fixtures
):
    """Two writers on one library, serialised by refusal rather than interleaved.

    The push happens after this handle read the subtree, so its next commit
    finds rows that were not there at open, and is refused rather than landing
    over a library it no longer describes. A handle opened after the push
    commits the same write.
    """
    path = library / "db" / "master.db"
    _build_disposable_database(path)
    db = W.open_db(path, unlock=False)
    try:
        dc7.push(path, ("1", "2"))
        db.create_playlist("mine at the top")
        assert "appeared under DEADCA7's folder" in _refused(db)
    finally:
        W.close_db(db)
    db = W.open_db(path, unlock=False)
    try:
        db.create_playlist("mine at the top")
        W.commit_guarded(db)
    finally:
        W.close_db(db)
