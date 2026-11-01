"""U149, the custom playlist twins: ``crate sync twins`` and the twin pairs, on a disposable database.

The account is a fake that the catalogue (which lists) and the account seam
(which lists folders and writes) both read, so an edit on one is what the next
listing serves. Every scenario the brief names for the backfill, the merge
after it and the unpair is driven here end to end through the dispatcher, the
explicit gates and their recorded answers included. The landing's twins are
driven in tests/test_intake_land_twins.py.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from cratekit.core import jobs, rb_writer, session, taxonomy
from cratekit.core.exit_codes import ExitCode
from cratekit.label import catalogue
from cratekit.label.catalogue import AccountPlaylist
from cratekit.modules.outbound import account as account_module
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_cli, twins, twins_cli
from cratekit.write import playlist_pair
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, catalogue_factory
from tests.test_rb_writer_db import _build_disposable_database
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414

PHIL = "acc-phil"
PHIL_NAME = "DOWNLOADED Phil 9-30-26"
YEAR_FOLDER = "fold-2026"
VERB = ["sync", "twins"]
#: Content rows one through nine, each carrying the ISRC its account track has.
ROWS = tuple(str(index) for index in range(1, 10))


def isrc(index: str) -> str:
    return f"USAAA26{int(index):05d}"


def remote(index: str) -> str:
    return f"t{index}"


class Listed:
    """A provider track in the shape the playlist reader reads."""

    def __init__(self, track_id: str, code: str) -> None:
        self.id = track_id
        self.name = f"Title {track_id}"
        self.artist = {"name": f"Artist {track_id}"}
        self.isrc = code


class LivePlaylist:
    """One account playlist as the catalogue lists it, read off the fake account now."""

    page_size = 100

    def __init__(self, world: World, playlist_id: str) -> None:
        self.world = world
        self.playlist_id = playlist_id

    @property
    def num_tracks(self):
        if self.playlist_id in self.world.short:
            return len(self.world.account.playlists[self.playlist_id]) + 1
        return None

    def tracks(self, limit=None, offset=0):
        size = self.page_size if limit is None else limit
        members = self.world.account.playlists[self.playlist_id]
        return [
            Listed(one, self.world.codes.get(one, ""))
            for one in members[offset : offset + size]
        ]


class World:
    """The account, its year folder and the library, wired together."""

    def __init__(self, cfg, monkeypatch) -> None:
        self.cfg = cfg
        self.account = outbound_fakes.FakeAccount(
            {content_id: remote(content_id) for content_id in ROWS}
        )
        self.codes = {remote(one): isrc(one) for one in ROWS}
        #: Account tracks the library lacks, with ISRCs no row carries.
        self.codes.update({"t20": "USZZZ2600020", "t21": "USZZZ2600021"})
        self.short: set[str] = set()
        self.catalogue = FakeCatalogue(playlists={}, account=[])
        self.account.folder_names[YEAR_FOLDER] = "2026"
        monkeypatch.setattr(catalogue, "resolve", catalogue_factory(self.catalogue))
        monkeypatch.setattr(account_module, "resolve", outbound_fakes.account_factory(self.account))

    def playlist(self, playlist_id: str, name: str, tracks, *, folder: str = YEAR_FOLDER) -> None:
        self.account.playlists[playlist_id] = list(tracks)
        self.account.titles[playlist_id] = name
        if folder:
            self.account.placed[playlist_id] = folder
        self.catalogue.playlists[playlist_id] = LivePlaylist(self, playlist_id)
        self.catalogue.account.append(AccountPlaylist(playlist_id=playlist_id, name=name))

    def delete(self, playlist_id: str) -> None:
        self.account.playlists.pop(playlist_id, None)
        self.account.placed.pop(playlist_id, None)
        self.catalogue.account = [
            one for one in self.catalogue.account if one.playlist_id != playlist_id
        ]

    def open(self):
        return rb_writer.open_db(Path(self.cfg.library.db_path), unlock=False, cfg=self.cfg)

    def sql(self, statement: str, *args) -> list[tuple]:
        conn = sqlite3.connect(self.cfg.library.db_path)
        try:
            return list(conn.execute(statement, args).fetchall())
        finally:
            conn.close()

    def folder(self, year: str = "2026") -> list[str]:
        """Every live top level folder named for the year, by id."""
        return [
            str(row[0])
            for row in self.sql(
                "SELECT ID FROM djmdPlaylist WHERE Name = ? AND Attribute = 1 "
                "AND COALESCE(ParentID, '') IN ('', '0', 'root', 'None') "
                "AND COALESCE(rb_local_deleted, 0) = 0",
                twins.folder_name(year),
            )
        ]

    def twin(self, name: str, year: str = "2026") -> str:
        (folder,) = self.folder(year)
        found = self.sql(
            "SELECT ID FROM djmdPlaylist WHERE Name = ? AND ParentID = ? "
            "AND COALESCE(rb_local_deleted, 0) = 0",
            name,
            folder,
        )
        assert len(found) == 1, found
        return str(found[0][0])

    def held(self, playlist_id: str) -> list[str]:
        return [
            str(row[0])
            for row in self.sql(
                "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? "
                "AND COALESCE(rb_local_deleted, 0) = 0 ORDER BY TrackNo, ID",
                playlist_id,
            )
        ]

    def make(self, name: str, *, parent: str = "", folder: bool = False) -> str:
        handle = self.open()
        try:
            above = handle.get_playlist(ID=parent) if parent else None
            made = (
                handle.create_playlist_folder(name, parent=above)
                if folder
                else handle.create_playlist(name, parent=above)
            )
            handle.session.commit()
            return str(made.ID)
        finally:
            rb_writer.close_db(handle)

    def rekordbox_remove(self, playlist_id: str, *content_ids: str) -> None:
        conn = sqlite3.connect(self.cfg.library.db_path)
        try:
            for content_id in content_ids:
                conn.execute(
                    "UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE PlaylistID = ? "
                    "AND ContentID = ?",
                    (playlist_id, content_id),
                )
            conn.commit()
        finally:
            conn.close()


def backfill(answer: str = "approve"):
    """Drive the verb through its explicit gate, answering as asked."""
    code, envelope = drive(VERB)
    if code != int(ExitCode.DECISION_REQUIRED):
        return code, envelope
    run_id = envelope["run_id"]
    gate = envelope["cause"]["detail"]["gate"]
    assert gate == twins_cli.APPROVE_GATE, envelope
    decided, said = drive(["run", "decide", run_id, gate, answer, "--actor", "a-person"])
    assert decided == int(ExitCode.OK), said
    return drive(["--run", run_id, *VERB])


def sync_pair(*args: str):
    """Drive ``sync pair`` through both explicit gates, applying each."""
    run_id = None
    for _ in range(3):
        resume = ["--run", run_id] if run_id else []
        code, envelope = drive([*resume, "sync", "pair", *args])
        if code != int(ExitCode.DECISION_REQUIRED):
            return code, envelope
        run_id = envelope["run_id"]
        gate = envelope["cause"]["detail"]["gate"]
        decided, said = drive(["run", "decide", run_id, gate, "apply", "--actor", "a-person"])
        assert decided == int(ExitCode.OK), said
    raise AssertionError("sync pair kept asking after both gates were answered")


@pytest.fixture
def db(cfg, monkeypatch):
    """A disposable database holding nine content rows, each with its ISRC."""
    path = Path(cfg.library.db_path)
    _build_disposable_database(path)
    conn = sqlite3.connect(path)
    try:
        for content_id in ROWS:
            conn.execute(
                "INSERT OR IGNORE INTO djmdContent (ID, Title, rb_local_deleted, created_at, "
                "updated_at) VALUES (?, ?, 0, '2026-01-01', '2026-01-01')",
                (content_id, f"Title {remote(content_id)}"),
            )
            conn.execute(
                "UPDATE djmdContent SET FolderPath = ?, ISRC = ?, rb_local_deleted = 0 "
                "WHERE ID = ?",
                (f"{cfg.library.root}/Music/{content_id}.flac", isrc(content_id), content_id),
            )
        conn.commit()
    finally:
        conn.close()
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer,
        "integrity_ok",
        lambda target, **kwargs: real_integrity_ok(target, unlock=False),
    )
    return path


@pytest.fixture
def world(cfg, gates_pass, db, monkeypatch) -> World:
    return World(cfg, monkeypatch)


def _codes(envelope) -> set[str]:
    return {warning["code"] for warning in envelope.get("warnings") or ()}


def _phil(w: World) -> None:
    """``DOWNLOADED Phil 9-30-26`` in ``2026``: three owned tracks, one the library lacks."""
    w.playlist(PHIL, PHIL_NAME, ["t3", "t1", "t20", "t2"])


# ═══════════════════════════════════════════════════════════════════════════
# The brief's scenarios
# ═══════════════════════════════════════════════════════════════════════════


def test_a_downloaded_playlist_plans_its_twin_with_the_owned_rows_and_names_the_rest(world):
    _phil(world)
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["twins"] == "Custom Playlists 2026 / Phil 9-30-26: 3 track(s), 1 missing"
    code, envelope = backfill("abort")
    assert code == int(ExitCode.OK), envelope
    rows = envelope["data"]["items"]
    made = [one for one in rows if one["action"] == twins.CREATE]
    assert [(one["folder"], one["playlist"], one["tracks"]) for one in made] == [
        ("Custom Playlists 2026", "Phil 9-30-26", 3)
    ]
    missing = [one for one in rows if one["action"] == "missing"]
    assert [(one["remote_id"], one["why"]) for one in missing] == [("t20", twins.NOT_OWNED)]


def test_the_backfill_makes_the_folder_and_twin_in_the_accounts_order_and_pairs_it(world, cfg):
    _phil(world)
    code, envelope = backfill()
    assert code == int(ExitCode.OK), envelope
    assert len(world.folder()) == 1
    twin_id = world.twin("Phil 9-30-26")
    assert world.held(twin_id) == ["3", "1", "2"]
    held = pairs.PairStore(cfg).get(PHIL)
    assert held is not None and held.twin and held.rekordbox_id == twin_id
    assert held.account == ("t3", "t1", "t20", "t2")
    assert [one.content_id for one in held.rekordbox] == ["3", "1", "2"]
    assert dict(held.links) == {"t3": "3", "t1": "1", "t2": "2"}
    assert twins_cli.MISSING in _codes(envelope)
    assert envelope["data"]["totals"]["made"] == 1


def test_a_second_backfill_plans_nothing_and_asks_nothing(world):
    _phil(world)
    assert backfill()[0] == int(ExitCode.OK)
    code, envelope = drive(VERB)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op" or twins_cli.NOTHING in _codes(envelope)
    assert twins_cli.NOTHING in _codes(envelope)
    assert len(world.folder()) == 1


def test_an_abort_writes_nothing_and_pairs_nothing(world, cfg):
    _phil(world)
    code, envelope = backfill("abort")
    assert code == int(ExitCode.OK), envelope
    assert world.folder() == []
    assert pairs.PairStore(cfg).all() == {}


def test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once(world, cfg):
    _phil(world)
    assert backfill()[0] == int(ExitCode.OK)
    twin_id = world.twin("Phil 9-30-26")
    world.account.playlists[PHIL].append("t4")
    world.account.playlists[PHIL].append("t21")
    world.rekordbox_remove(twin_id, "1")
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.held(twin_id) == ["3", "2", "4"]
    assert world.account.playlists[PHIL] == ["t3", "t20", "t2", "t4", "t21"]
    queued = envelope["data"]["totals"]["queued_jobs"]
    assert len(queued) == 1
    with jobs.open_store() as store:
        job = jobs.get(store, queued[0])
    assert sorted((job.payload or {}).get("tracks") or {}) == ["t20", "t21"]
    code, again = sync_pair()
    assert code == int(ExitCode.OK), again
    assert again["data"]["totals"]["queued_jobs"] == []


def test_a_twin_whose_account_playlist_is_deleted_is_unpaired_and_left_named(world, cfg):
    _phil(world)
    assert backfill()[0] == int(ExitCode.OK)
    twin_id = world.twin("Phil 9-30-26")
    world.delete(PHIL)
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert pairs.PairStore(cfg).get(PHIL) is None
    assert world.held(twin_id) == ["3", "1", "2"], "the twin lost a track"
    assert pair_cli.UNPAIRED in _codes(envelope)
    said = next(w["message"] for w in envelope["warnings"] if w["code"] == pair_cli.UNPAIRED)
    assert "Phil 9-30-26" in said
    assert world.account.taken == [] and world.account.deleted == []


def test_a_pair_made_by_hand_whose_account_playlist_is_gone_is_left_out_not_unpaired(world, cfg):
    _phil(world)
    mine = world.make("My Own")
    pairs.PairStore(cfg).mark(PHIL, mine, name=PHIL_NAME)
    world.delete(PHIL)
    code, envelope = sync_pair()
    assert pairs.PairStore(cfg).get(PHIL) is not None
    assert pair_cli.UNPAIRED not in _codes(envelope)


def test_a_name_the_folder_already_holds_is_refused_by_name_never_counted(world, cfg):
    _phil(world)
    folder = world.make(twins.folder_name("2026"), folder=True)
    world.make("Phil 9-30-26", parent=folder)
    code, envelope = drive(VERB)
    assert code == int(ExitCode.OK), envelope
    assert twins_cli.LEFT in _codes(envelope)
    left = [one for one in envelope["data"]["items"] if one["action"] == twins.LEFT]
    assert [one["playlist"] for one in left] == ["Phil 9-30-26"]
    assert "already holds a playlist named 'Phil 9-30-26'" in left[0]["why"]
    assert pairs.PairStore(cfg).all() == {}
    names = [
        row[0]
        for row in world.sql("SELECT Name FROM djmdPlaylist WHERE ParentID = ?", folder)
    ]
    assert names == ["Phil 9-30-26"], "a counted second twin was made"


def test_an_existing_folder_is_reused_and_two_of_one_year_place_nothing(world, cfg):
    _phil(world)
    first = world.make(twins.folder_name("2026"), folder=True)
    code, envelope = backfill()
    assert code == int(ExitCode.OK), envelope
    assert world.folder() == [first]
    world.playlist("acc-two", "DOWNLOADED Two", ["t5"])
    world.make(twins.folder_name("2026"), folder=True)
    code, envelope = drive(VERB)
    assert code == int(ExitCode.OK), envelope
    left = [one for one in envelope["data"]["items"] if one["action"] == twins.LEFT]
    assert [one["account_id"] for one in left] == ["acc-two"]
    assert "2 top level folders" in left[0]["why"]


def test_only_downloaded_own_playlists_in_a_year_folder_are_read(world, cfg):
    world.playlist(PHIL, PHIL_NAME, ["t1"])
    world.playlist("acc-working", "Still Building", ["t2"])
    world.playlist("acc-root", "DOWNLOADED At The Root", ["t3"], folder="")
    world.account.folder_names["fold-exports"] = "Exports"
    world.playlist("acc-exported", "DOWNLOADED Exported", ["t4"], folder="fold-exports")
    code, envelope = backfill("abort")
    assert code == int(ExitCode.OK), envelope
    rows = envelope["data"]["items"]
    assert [one["account_id"] for one in rows if one["action"] == twins.CREATE] == [PHIL]


def test_a_short_listing_pairs_the_twin_with_no_snapshot(world, cfg):
    _phil(world)
    world.short.add(PHIL)
    code, envelope = backfill()
    assert code == int(ExitCode.OK), envelope
    held = pairs.PairStore(cfg).get(PHIL)
    assert held is not None and held.first and held.twin
    assert twins_cli.SHORT in _codes(envelope)


def test_a_folder_made_after_the_approval_refuses_as_stale(world, cfg):
    _phil(world)
    code, envelope = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED)
    run_id = envelope["run_id"]
    drive(["run", "decide", run_id, twins_cli.APPROVE_GATE, "approve", "--actor", "a-person"])
    world.make(twins.folder_name("2026"), folder=True)
    code, refused = drive(["--run", run_id, *VERB])
    assert code != int(ExitCode.OK)
    assert refused["cause"]["reason"] == "decision-stale", refused
    assert pairs.PairStore(cfg).all() == {}


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(world, cfg):
    _phil(world)
    session.ack_path(cfg).unlink()
    code, refused = drive(VERB)
    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert "gate" not in (refused.get("cause") or {}).get("detail", {})


# ═══════════════════════════════════════════════════════════════════════════
# The pair rule, the name, and the confinement
# ═══════════════════════════════════════════════════════════════════════════


def _registry_free():
    class Empty:
        trees = ()

    return Empty()


@pytest.mark.parametrize("top", ["BY GENRE + ENERGY", "INBOX", "INSPIRATION"])
def test_the_pair_rule_still_refuses_a_playlist_under_cratekits_own_trees(top):
    from cratekit.core.cause import CratekitError

    tops = pair_cli.generated_tops(taxonomy.default_taxonomy(), _registry_free())
    assert top in tops[1]
    found = playlist_pair.Playlist(
        playlist_id="p1", name="x", attribute=0, removed=False, ancestors=(("f1", top),)
    )
    with pytest.raises(CratekitError) as refused:
        pair_cli._scope_rekordbox("p1", found, tops)
    assert refused.value.cause.reason == "sync-pair-out-of-scope"


def test_the_pair_rule_lets_a_twin_pair():
    tops = pair_cli.generated_tops(taxonomy.default_taxonomy(), _registry_free())
    found = playlist_pair.Playlist(
        playlist_id="p1",
        name="Phil 9-30-26",
        attribute=0,
        removed=False,
        ancestors=(("f1", twins.folder_name("2026")),),
    )
    assert pair_cli._scope_rekordbox("p1", found, tops) is found


@pytest.mark.parametrize(
    ("account", "twin"),
    [
        ("DOWNLOADED Phil 9-30-26", "Phil 9-30-26"),
        ("Phil 9-30-26", "Phil 9-30-26"),
        ("DOWNLOADED ", ""),
        ("downloaded lower", "downloaded lower"),
    ],
)
def test_the_twins_name_is_the_accounts_less_the_prefix(account, twin):
    assert twins.twin_name(account) == twin


def test_place_refuses_a_held_name_a_taken_name_an_empty_name_and_an_unplaced_year():
    folder = twins.Folder(year="2026", name="Custom Playlists 2026", held=frozenset({"A"}))
    taken: set[str] = set()
    assert twins.place("A", folder, taken)
    assert twins.place("", folder, taken)
    assert twins.place("B", folder, taken) == ""
    assert "also named 'B'" in twins.place("B", folder, taken)
    unplaced = twins.Folder(year="2026", name="Custom Playlists 2026", why="two of them")
    assert twins.place("C", unplaced, set()) == "two of them"


def _tables(playlists, memberships, content=None) -> rb_writer.NodeTables:
    return rb_writer.NodeTables(
        playlist_columns=("ID", "Name", "ParentID", "Attribute", "Seq", rb_writer.SOFT_DELETE_COLUMN),
        playlists=playlists,
        membership_columns=("ID", "PlaylistID", "ContentID", rb_writer.SOFT_DELETE_COLUMN),
        memberships=memberships,
        content=content or {"1": "a", "2": "b"},
    )


BEFORE = _tables({"10": ("10", "INBOX", "root", 1, 1, 0)}, {})


def _after(**changes) -> rb_writer.NodeTables:
    playlists = {
        "10": ("10", "INBOX", "root", 1, 1, 0),
        "20": ("20", "Custom Playlists 2026", "root", 1, 2, 0),
        "21": ("21", "Phil", "20", 0, 1, 0),
    }
    memberships = {"m1": ("m1", "21", "1", 0)}
    playlists.update(changes.get("playlists", {}))
    memberships.update(changes.get("memberships", {}))
    return _tables(playlists, memberships, changes.get("content"))


PLANNED = {"folders": {"20": "Custom Playlists 2026"}, "playlists": {"21": ("Phil", "20", frozenset({"1"}))}}


def test_the_confinement_admits_exactly_the_twins_made():
    assert twins.addition_violations(BEFORE, _after(), **PLANNED) == []


@pytest.mark.parametrize(
    "changes",
    [
        {"playlists": {"22": ("22", "Stray", "root", 0, 3, 0)}},
        {"playlists": {"21": ("21", "Phil", "10", 0, 1, 0)}},
        {"playlists": {"20": ("20", "Custom Playlists 2026", "10", 1, 2, 0)}},
        {"playlists": {"10": ("10", "INBOX renamed", "root", 1, 1, 0)}},
        {"memberships": {"m2": ("m2", "21", "2", 0)}},
        {"memberships": {"m2": ("m2", "10", "1", 0)}},
        {"content": {"1": "changed", "2": "b"}},
    ],
)
def test_the_confinement_refuses_what_no_twin_explains(changes):
    assert twins.addition_violations(BEFORE, _after(**changes), **PLANNED)


def test_the_pair_store_reads_a_pair_written_before_u149_as_no_twin(cfg):
    store = pairs.PairStore(cfg)
    store.mark("a", "1", name="x")
    raw = store.path.read_text(encoding="utf-8")
    assert '"twin"' not in raw
    assert store.get("a").twin is False
    store.mark("b", "2", name="y", twin=True)
    assert store.get("b").twin is True
    assert store.unmark("b", "9") is None and store.get("b") is not None
    assert store.unmark("b", "2") is not None and store.get("b") is None
