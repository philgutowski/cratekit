"""U959: what the account mirror reads under rekordbox's top level WIP folder, on a disposable database. D1 applies."""

from __future__ import annotations

from cratekit.core import config, rb_writer
from cratekit.modules.outbound import mirror, pairs
from cratekit.modules.outbound import mirror_edits as edits
from cratekit.organize import account_mirror
from cratekit.organize.steps import LISTED, PLANNED, REFUSED, Area
from tests import outbound_fakes
from tests.test_genre_favorites import AFRO, DEEP, Tree
from tests.test_genre_favorites import db as db  # noqa: PLC0414 - fixture
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414

SET = "deep and soulful"


class Wip:
    """The top level WIP folder on the handle, its subfolders and their playlists."""

    def __init__(self, db, name: str = "WIP ") -> None:
        self.db = db
        self.root = db.create_playlist_folder(name)
        self.subs: dict[str, object] = {}
        db.session.commit()

    def sub(self, name: str, parent=None):
        key = (name, None if parent is None else str(parent.ID))
        if key not in self.subs:
            self.subs[key] = self.db.create_playlist_folder(name, parent=parent if parent is not None else self.root)
            self.db.session.commit()
        return self.subs[key]

    def playlist(self, name: str, *members: str, under=None, smart: bool = False):
        made = self.db.create_playlist(name, parent=under if under is not None else self.root)
        for content_id in members:
            self.db.add_to_playlist(made, content_id)
        if smart:
            made.Attribute = 4
        self.db.session.commit()
        return made


def _read(cfg, db, monkeypatch) -> account_mirror.Library:
    monkeypatch.setattr(rb_writer, "open_db", lambda *args, **kwargs: db)
    monkeypatch.setattr(rb_writer, "close_db", lambda _db: None)
    return account_mirror.read_library(cfg)


def _wip(library: account_mirror.Library) -> mirror.Folder:
    (found,) = [folder for folder in library.folders if folder.name == account_mirror.WIP]
    return found


def _shape(folder: mirror.Folder) -> dict[str, list[str]]:
    return {source.name: [one.content_id for one in source.rows] for source in folder.playlists}


# 1. What the library holds under WIP


def test_two_subfolders_and_a_playlist_directly_under_wip_read_as_one_folder_of_titles(cfg, db, monkeypatch):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Low", "1")
    wip = Wip(db)
    wip.playlist(SET, "1", "2", under=wip.sub("Phil"))
    lisa = wip.sub("Lisa")
    wip.playlist("lisa_sandbox", "3", under=lisa)
    wip.playlist("lisa sandbox", "4", under=lisa)
    wip.playlist("warmup", "5")
    read = _read(cfg, db, monkeypatch)
    assert read.refused == {} and read.wip == ""
    folder = _wip(read)
    # THE TRAILING SPACE NAME IS FOUND, and the account folder takes it stripped.
    assert folder.name == "WIP" and folder.edits == edits.WIP
    assert folder.retire is False and folder.unmirrored == ()
    # mirror.title KEEPS lisa_sandbox AND lisa sandbox APART: two titles, two playlists.
    assert _shape(folder) == {
        mirror.title("Lisa", "lisa sandbox"): ["4"],
        mirror.title("Lisa", "lisa_sandbox"): ["3"],
        mirror.title("Phil", SET): ["1", "2"],
        mirror.title("WIP", "warmup"): ["5"],
    }
    assert mirror.title("Phil", SET) == f"Phil {SET}"
    # The genre tree is read beside it as before.
    assert DEEP.display in [one.name for one in read.folders]


def test_a_library_with_no_wip_folder_mirrors_nothing_for_it_and_refuses_nothing(cfg, db, monkeypatch):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Low", "1")
    # A folder named WIP that is not at the top level is not the WIP folder.
    nested = db.create_playlist_folder("WIP", parent=tree.folder(AFRO))
    db.add_to_playlist(db.create_playlist("inside", parent=nested), "2")
    db.session.commit()
    read = _read(cfg, db, monkeypatch)
    assert read.refused == {}
    assert [one.name for one in read.folders if one.name == "WIP"] == []
    assert read.wip == "the library holds no top level folder named 'WIP', so nothing is mirrored for it"


def test_a_smart_playlist_and_a_folder_two_levels_down_are_named_with_their_reasons(cfg, db, monkeypatch):
    Tree(cfg, db)
    wip = Wip(db)
    phil = wip.sub("Phil")
    wip.playlist(SET, "1", under=phil)
    wip.playlist("Fresh this week", under=phil, smart=True)
    wip.playlist("Smart at the top", smart=True)
    older = wip.sub("Older", parent=phil)
    wip.playlist("buried", "2", under=older)
    folder = _wip(_read(cfg, db, monkeypatch))
    assert _shape(folder) == {f"Phil {SET}": ["1"]}
    named = dict(folder.unmirrored)
    assert set(named) == {
        "Phil / Fresh this week, a smart playlist",
        "Smart at the top, a smart playlist",
        "Phil / Older, a folder two levels down",
    }
    assert "holds no membership" in named["Phil / Fresh this week, a smart playlist"]
    assert "one level of subfolder" in named["Phil / Older, a folder two levels down"]
    # Nothing inside the deeper folder is named or mirrored on its own.
    assert not any("buried" in label for label in named)


def test_a_paired_playlist_and_a_twin_are_left_with_their_reasons(cfg, db, monkeypatch):
    Tree(cfg, db)
    wip = Wip(db)
    phil = wip.sub("Phil")
    wip.playlist(SET, "1", under=phil)
    paired = wip.playlist("paired set", "2", under=phil)
    twin = wip.playlist("a twin", "3")
    store = pairs.PairStore(cfg)
    store.mark("acc-paired", str(paired.ID), name="paired set")
    store.mark("acc-twin", str(twin.ID), name="a twin", twin=True)
    folder = _wip(_read(cfg, db, monkeypatch))
    assert _shape(folder) == {f"Phil {SET}": ["1"]}
    named = dict(folder.unmirrored)
    assert named == {
        "Phil / paired set, paired by sync pair": (
            "it is one side of a sync pair with the account playlist acc-paired, which "
            "sync pair keeps the same list, so the mirror does not copy it a second time"
        ),
        "a twin, a custom playlist twin": (
            "it is a custom playlist twin of the account playlist acc-twin, which sync "
            "pair keeps the same list, so the mirror does not copy it a second time"
        ),
    }


def test_two_playlists_taking_one_title_refuse_wip_alone_and_the_genre_folders_still_read(cfg, db, monkeypatch):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Low", "1")
    wip = Wip(db)
    phil = wip.sub("Phil")
    wip.playlist(SET, "1", under=phil)
    wip.playlist(SET, "2", under=phil)
    read = _read(cfg, db, monkeypatch)
    assert list(read.refused) == ["WIP"]
    assert read.refused["WIP"].reason == mirror.AMBIGUOUS_REASON
    assert f"Phil {SET}" in read.refused["WIP"].message
    assert [one.name for one in read.folders] == [DEEP.display]


def test_a_title_a_subfolder_and_a_top_playlist_both_take_is_refused(cfg, db, monkeypatch):
    """``WIP / Phil a / b`` and ``WIP / Phil / a b`` both title as ``Phil a b``."""
    Tree(cfg, db)
    wip = Wip(db)
    wip.playlist("b", "1", under=wip.sub("Phil a"))
    wip.playlist("a b", "2", under=wip.sub("Phil"))
    read = _read(cfg, db, monkeypatch)
    assert list(read.refused) == ["WIP"] and read.refused["WIP"].reason == mirror.AMBIGUOUS_REASON


def test_two_top_level_wip_folders_refuse_wip_alone(cfg, db, monkeypatch):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Low", "1")
    Wip(db, "WIP").playlist("one", "1")
    Wip(db, "WIP ").playlist("two", "2")
    read = _read(cfg, db, monkeypatch)
    assert list(read.refused) == ["WIP"]
    assert read.refused["WIP"].reason == mirror.AMBIGUOUS_REASON
    assert "top level folders" in read.refused["WIP"].message
    assert [one.name for one in read.folders] == [DEEP.display]


def test_unreadable_pairs_refuse_wip_alone(cfg, db, monkeypatch):
    """UNREAD IS NOT NONE: a pair the mirror cannot see would be copied a second time."""
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Low", "1")
    Wip(db).playlist("warmup", "1")
    path = config.state_path("playlist_pairs", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{ not json", encoding="utf-8")
    read = _read(cfg, db, monkeypatch)
    assert list(read.refused) == ["WIP"]
    assert read.refused["WIP"].reason == "sync-pair-store-unusable"
    assert [one.name for one in read.folders] == [DEEP.display]


def test_the_step_over_the_library_refuses_wip_alone_and_plans_the_genre_folder(cfg, db, monkeypatch):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Low", "1")
    wip = Wip(db)
    wip.playlist(SET, "1", under=wip.sub("Phil"))
    wip.playlist(SET, "2", under=wip.sub("Phil"))
    monkeypatch.setattr(rb_writer, "open_db", lambda *args, **kwargs: db)
    monkeypatch.setattr(rb_writer, "close_db", lambda _db: None)
    area = Area(name="account")
    account = outbound_fakes.StrictAccount(catalog={"1": "r1", "2": "r2"})
    account_mirror.add_steps(cfg, area, lambda: account)
    states = {step.key: step.state for step in area.steps if step.state != LISTED}
    assert states == {f"mirror:{DEEP.display}": PLANNED, "mirror:WIP": REFUSED}
    (wip,) = [step for step in area.steps if step.key == "mirror:WIP"]
    assert wip.cause.reason == mirror.AMBIGUOUS_REASON
