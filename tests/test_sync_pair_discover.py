"""U198, ``crate sync pair`` with no argument: every playlist the author made, paired by itself.

Driven through the dispatcher on a disposable database and a fake account that
both the catalogue (which lists) and the account seam (which writes) read, so a
playlist the sync makes is one the next sync lists. Every scenario the brief
keeps after its split (U202 takes the rest) is driven here end to end, both
explicit gates and their recorded answers included.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from cratekit.core import config, rb_writer
from cratekit.core.exit_codes import ExitCode
from cratekit.label import catalogue
from cratekit.label.catalogue import AccountPlaylist
from cratekit.modules.outbound import account as account_module
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_cli, pair_discover
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, catalogue_factory
from tests.test_rb_writer_db import _build_disposable_database
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414

VERB = ["sync", "pair"]
#: Content rows one through nine, each carrying the ISRC its account track has.
ROWS = tuple(str(index) for index in range(1, 10))


def isrc(index: str) -> str:
    return f"USBBB26{int(index):05d}"


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
    num_tracks = None

    def __init__(self, world: World, playlist_id: str) -> None:
        self.world = world
        self.playlist_id = playlist_id

    def tracks(self, limit=None, offset=0):
        size = self.page_size if limit is None else limit
        members = self.world.account.playlists.get(self.playlist_id, [])
        return [
            Listed(one, self.world.codes.get(one, "")) for one in members[offset : offset + size]
        ]


class LiveCatalogue(FakeCatalogue):
    """The catalogue reading the fake account's own playlists live, as the provider does."""

    def __init__(self, world: World) -> None:
        super().__init__()
        self.world = world

    def account_playlists(self):
        self.account_listings += 1
        return tuple(
            AccountPlaylist(playlist_id=pid, name=name)
            for pid, name in self.world.account.titles.items()
        )

    def playlist_for(self, reference: str):
        self.playlists_asked_for.append(reference)
        if reference not in self.world.account.titles:
            raise LookupError(f"no catalogue playlist for {reference!r}")
        return LivePlaylist(self.world, reference)


class World:
    """The account, its catalogue and the rekordbox tree, wired together."""

    def __init__(self, cfg, monkeypatch) -> None:
        self.cfg = cfg
        self.account = outbound_fakes.FakeAccount(
            {content_id: remote(content_id) for content_id in ROWS}
        )
        self.codes = {remote(one): isrc(one) for one in ROWS}
        self.catalogue = LiveCatalogue(self)
        monkeypatch.setattr(catalogue, "resolve", catalogue_factory(self.catalogue))
        monkeypatch.setattr(account_module, "resolve", outbound_fakes.account_factory(self.account))

    def open(self):
        return rb_writer.open_db(Path(self.cfg.library.db_path), unlock=False, cfg=self.cfg)

    def folder(self, name: str, under: str | None = None) -> str:
        handle = self.open()
        try:
            parent = None if under is None else handle.get_playlist(ID=under)
            row = handle.create_playlist_folder(name, parent=parent)
            handle.session.commit()
            return str(row.ID)
        finally:
            rb_writer.close_db(handle)

    def playlist(self, name: str, *content_ids: str, under: str | None = None) -> str:
        handle = self.open()
        try:
            parent = None if under is None else handle.get_playlist(ID=under)
            row = handle.create_playlist(name, parent=parent)
            for content_id in content_ids:
                handle.add_to_playlist(row, content_id)
            handle.session.commit()
            return str(row.ID)
        finally:
            rb_writer.close_db(handle)

    def sql(self, statement: str, *args) -> list[tuple]:
        conn = sqlite3.connect(self.cfg.library.db_path)
        try:
            rows = conn.execute(statement, args).fetchall()
            conn.commit()
            return rows
        finally:
            conn.close()

    def held(self, playlist_id: str) -> list[str]:
        return [
            str(row[0])
            for row in self.sql(
                "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? "
                "AND COALESCE(rb_local_deleted, 0) = 0 ORDER BY TrackNo, ID",
                playlist_id,
            )
        ]

    def rekordbox_add(self, playlist_id: str, *content_ids: str) -> None:
        handle = self.open()
        try:
            row = handle.get_playlist(ID=playlist_id)
            for content_id in content_ids:
                handle.add_to_playlist(row, content_id)
            handle.session.commit()
        finally:
            rb_writer.close_db(handle)

    def rekordbox_remove(self, playlist_id: str, *content_ids: str) -> None:
        for content_id in content_ids:
            self.sql(
                "UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE PlaylistID = ? "
                "AND ContentID = ?",
                playlist_id,
                content_id,
            )

    def delete_rekordbox(self, playlist_id: str) -> None:
        self.sql("UPDATE djmdPlaylist SET rb_local_deleted = 1 WHERE ID = ?", playlist_id)

    def titled(self, title: str) -> str:
        """The account playlist of this title, the one and only."""
        found = [pid for pid, name in self.account.titles.items() if name == title]
        assert len(found) == 1, (title, self.account.titles)
        return found[0]

    def in_folder(self, folder: str) -> dict[str, str]:
        """Each account playlist in the root folder of this name, title to identifier."""
        ids = [fid for fid, name in self.account.folders().items() if name == folder]
        assert len(ids) == 1, (folder, self.account.folder_names)
        return {name: pid for pid, name in self.account.folder_playlists(ids[0]).items()}


def sync(args: list[str] = VERB, *, rekordbox: str = "apply", account: str = "apply"):
    """Drive the verb through both explicit gates, answering each as asked."""
    answers = {pair_cli.REKORDBOX_GATE: rekordbox, pair_cli.ACCOUNT_GATE: account}
    run_id = None
    for _ in range(3):
        resume = ["--run", run_id] if run_id else []
        code, envelope = drive([*resume, *args])
        if code != int(ExitCode.DECISION_REQUIRED):
            return code, envelope
        run_id = envelope["run_id"]
        gate = envelope["cause"]["detail"]["gate"]
        decided, said = drive(["run", "decide", run_id, gate, answers[gate], "--actor", "a-person"])
        assert decided == int(ExitCode.OK), said
    raise AssertionError("the verb kept asking after both gates were answered")


def plan_only(args: list[str] = VERB):
    """The plan both gates show, both answered skip, so nothing is written."""
    code, envelope = sync(args, rekordbox="skip", account="skip")
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]


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


def _said(envelope, code: str) -> str:
    return next(w["message"] for w in envelope["warnings"] if w["code"] == code)


def _items(plan, side: str, action: str) -> list[dict]:
    return [item for item in plan["items"] if item["side"] == side and item["action"] == action]


# ═══════════════════════════════════════════════════════════════════════════
# Discovery and the account side made
# ═══════════════════════════════════════════════════════════════════════════


def test_a_gig_ready_playlist_is_made_on_the_account_in_its_folder_and_filled(world, cfg):
    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    inside = world.in_folder("GIG READY")
    assert list(inside) == ["GIG READY Opener"]
    made = inside["GIG READY Opener"]
    assert world.account.playlists[made] == ["t1", "t2", "t3"]
    assert made in world.account.private
    held = pairs.PairStore(cfg).get(made)
    assert held is not None and held.rekordbox_id == opener
    assert held.made and held.folder == "GIG READY"
    assert held.account == ("t1", "t2", "t3")
    assert envelope["data"]["totals"]["created_playlists"] == [made]


def test_a_second_run_plans_nothing(world):
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", "2", under=gig)
    assert sync()[0] == int(ExitCode.OK)
    created = list(world.account.created)
    asked = len(world.account.matches)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert world.account.created == created
    assert len(world.account.matches) == asked


def test_a_playlist_in_a_subfolder_takes_its_path_and_one_at_the_root_goes_in_playlists(world):
    gig = world.folder("GIG READY")
    halloween = world.folder("Halloween", under=gig)
    world.playlist("Opener", "1", under=halloween)
    world.playlist("Loose", "2")
    assert sync()[0] == int(ExitCode.OK)
    assert list(world.in_folder("GIG READY")) == ["GIG READY Halloween Opener"]
    assert list(world.in_folder("Playlists")) == ["Playlists Loose"]


def test_an_archive_playlist_is_listed_and_never_written(world):
    archive = world.folder("ARCHIVE")
    world.playlist("Old", "1", under=archive)
    gig = world.folder("GIG READY")
    world.playlist("Opener", "2", under=gig)
    plan = plan_only()
    skipped = _items(plan, "discovery", pair_discover.SKIPPED)
    assert [item["where"] for item in skipped] == ["ARCHIVE / Old"]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert "ARCHIVE" not in world.account.folder_names.values()
    assert not any("Old" in name for name in world.account.titles.values())
    assert "ARCHIVE" in _said(envelope, pair_cli.NOT_DISCOVERED)


def test_the_skip_list_is_the_configurations(world, cfg, monkeypatch):
    from dataclasses import replace

    moved = replace(cfg, outbound=replace(cfg.outbound, pair_skip_folders=("WIP",)))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: moved)
    archive = world.folder("ARCHIVE")
    world.playlist("Old", "1", under=archive)
    wip = world.folder("WIP")
    world.playlist("Draft", "2", under=wip)
    assert sync()[0] == int(ExitCode.OK)
    assert list(world.in_folder("ARCHIVE")) == ["ARCHIVE Old"]
    assert "WIP" not in world.account.folder_names.values()


def test_cratekits_own_trees_and_the_favorites_folder_are_never_discovered(world):
    for top in ("BY GENRE + ENERGY", "INBOX", "Record Labels"):
        under = world.folder(top)
        world.playlist(f"{top} list", "1", under=under)
    favorites = world.folder("Favorites")
    world.playlist("All Favorites", "2", under=favorites)
    world.playlist("Favorites 2026-10", "3", under=favorites)
    twins = world.folder("Custom Playlists 2026")
    world.playlist("A twin", "4", under=twins)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert world.account.created == []
    assert world.account.folders_created == []


def test_a_favourites_playlist_at_the_root_is_not_discovered(world):
    world.playlist("All Favorites", "1")
    world.playlist("Mine", "2")
    assert sync()[0] == int(ExitCode.OK)
    assert list(world.in_folder("Playlists")) == ["Playlists Mine"]


def test_two_playlists_taking_one_title_refuse_that_title_only(world):
    gig = world.folder("GIG READY")
    world.playlist("A B", "1", under=gig)
    a = world.folder("A", under=gig)
    world.playlist("B", "2", under=a)
    world.playlist("Closer", "3", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert list(world.in_folder("GIG READY")) == ["GIG READY Closer"]
    said = _said(envelope, pair_cli.NOT_DISCOVERED)
    assert "GIG READY A B" in said


def test_a_smart_playlist_is_listed_not_paired(world):
    gig = world.folder("GIG READY")
    smart = world.playlist("Smart", under=gig)
    world.sql("UPDATE djmdPlaylist SET Attribute = 4 WHERE ID = ?", smart)
    world.playlist("Opener", "1", under=gig)
    plan = plan_only()
    assert [item["name"] for item in _items(plan, "discovery", pair_discover.SMART)] == ["Smart"]
    assert sync()[0] == int(ExitCode.OK)
    assert list(world.in_folder("GIG READY")) == ["GIG READY Opener"]


def test_an_existing_root_folder_of_the_name_is_reused_and_a_persons_title_is_left(world):
    folder_id = world.account.create_folder("GIG READY")
    theirs = world.account.create_playlist("GIG READY Opener")
    world.account.move_to_folder(theirs, folder_id)
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", under=gig)
    world.playlist("Closer", "2", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.folders_created == ["GIG READY"]
    inside = world.in_folder("GIG READY")
    assert sorted(inside) == ["GIG READY Closer", "GIG READY Opener"]
    assert inside["GIG READY Opener"] == theirs
    assert world.account.playlists[theirs] == []
    assert "GIG READY Opener" in _said(envelope, pair_cli.NOT_DISCOVERED)


def test_two_root_folders_of_the_name_leave_that_folder_out(world):
    world.account.create_folder("GIG READY")
    world.account.create_folder("GIG READY")
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", under=gig)
    world.playlist("Loose", "2")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert sorted(world.account.titles.values()) == ["Playlists Loose"]
    assert "2 root folders" in _said(envelope, pair_cli.NOT_DISCOVERED)


def test_a_root_folder_another_list_of_cratekits_keeps_is_not_adopted(world, cfg):
    from cratekit.modules.outbound import ledger

    folder_id = world.account.create_folder("GIG READY")
    ledger.reserve_mirror_folder(cfg, "GIG READY", lambda: "unused", adopt=folder_id)
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.created == []
    assert "another list" in _said(envelope, pair_cli.NOT_DISCOVERED)


def test_skipping_the_account_gate_makes_and_marks_nothing(world, cfg):
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", under=gig)
    code, envelope = sync(account="skip")
    assert code == int(ExitCode.OK), envelope
    assert world.account.created == []
    assert pairs.PairStore(cfg).all() == {}


def test_skipping_rekordbox_makes_the_account_side_and_the_next_sync_finishes(world, cfg):
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", "2", under=gig)
    assert sync(rekordbox="skip")[0] == int(ExitCode.OK)
    made = world.titled("GIG READY Opener")
    assert world.account.playlists[made] == ["t1", "t2"]
    held = pairs.PairStore(cfg).get(made)
    assert held is not None and held.first
    assert sync()[0] == int(ExitCode.OK)
    assert world.titled("GIG READY Opener") == made
    assert not pairs.PairStore(cfg).get(made).first


def test_a_made_playlist_is_never_offered_by_sync_all(world, cfg):
    from cratekit.sync import playlists

    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", under=gig)
    assert sync()[0] == int(ExitCode.OK)
    made = world.titled("GIG READY Opener")
    listed = AccountPlaylist(playlist_id=made, name="GIG READY Opener", tracks=1)
    assert (
        playlists.exclusion(
            listed, recorded=set(), in_flight=set(), paired=pairs.paired_ids(cfg)
        )
        == playlists.Excluded.PAIRED
    )


# ═══════════════════════════════════════════════════════════════════════════
# Both ways, after the pair is made
# ═══════════════════════════════════════════════════════════════════════════


def _made_pair(world) -> tuple[str, str]:
    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", under=gig)
    assert sync()[0] == int(ExitCode.OK)
    return opener, world.titled("GIG READY Opener")


def test_an_owned_track_added_on_the_account_lands_in_rekordbox(world):
    opener, made = _made_pair(world)
    world.account.playlists[made].append("t3")
    assert sync()[0] == int(ExitCode.OK)
    assert world.held(opener) == ["1", "2", "3"]


def test_an_unowned_track_added_on_the_account_is_queued_once_and_then_awaiting(world):
    opener, made = _made_pair(world)
    world.account.playlists[made].append("t99")
    world.codes["t99"] = "USBBB2699999"
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert len(envelope["data"]["totals"]["queued_jobs"]) == 1
    assert world.held(opener) == ["1", "2"]
    code, again = sync()
    assert code == int(ExitCode.OK), again
    assert again["data"]["totals"]["queued_jobs"] == []
    assert pair_cli.AWAITING in _codes(again)


def test_a_removal_on_each_side_comes_off_the_other(world):
    opener, made = _made_pair(world)
    world.rekordbox_add(opener, "3")
    assert sync()[0] == int(ExitCode.OK)
    assert world.account.playlists[made] == ["t1", "t2", "t3"]
    world.rekordbox_remove(opener, "1")
    world.account.playlists[made].remove("t3")
    assert sync()[0] == int(ExitCode.OK)
    assert world.held(opener) == ["2"]
    assert world.account.playlists[made] == ["t2"]


def test_a_playlist_deleted_on_the_account_unpairs_stays_and_is_not_made_again(world, cfg):
    opener, made = _made_pair(world)
    world.account.remove_playlist(made)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.RELEASED in _codes(envelope)
    assert pairs.PairStore(cfg).get(made) is None
    assert world.held(opener) == ["1", "2"]
    assert pairs.PairStore(cfg).released().rekordbox == frozenset({opener})
    created = list(world.account.created)
    code, again = sync()
    assert code == int(ExitCode.OK), again
    assert world.account.created == created
    plan_said = _said(again, pair_cli.NOT_DISCOVERED)
    assert "Opener" in plan_said


def test_a_playlist_deleted_in_rekordbox_unpairs_and_leaves_the_account_playlist(world, cfg):
    opener, made = _made_pair(world)
    world.delete_rekordbox(opener)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.RELEASED in _codes(envelope)
    assert pairs.PairStore(cfg).get(made) is None
    assert world.account.playlists[made] == ["t1", "t2"]
    assert pairs.PairStore(cfg).released().account == frozenset({made})


def test_a_hand_named_pair_whose_rekordbox_playlist_is_gone_is_still_left_out(world, cfg):
    """The release is a made pair's; a pair a person named keeps U130's rule."""
    theirs = world.account.create_playlist("Theirs")
    pairs.PairStore(cfg).mark(theirs, "no-such-playlist", name="Theirs")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT in _codes(envelope)
    assert pairs.PairStore(cfg).get(theirs) is not None


def test_a_short_account_listing_removes_nothing(world, monkeypatch):
    opener, made = _made_pair(world)
    world.rekordbox_add(opener, "3")
    assert sync()[0] == int(ExitCode.OK)
    real = LivePlaylist.tracks

    def short(self, limit=None, offset=0):
        rows = real(self, limit, offset)
        return [one for one in rows if one.id != "t1"] if self.playlist_id == made else rows

    monkeypatch.setattr(LivePlaylist, "tracks", short)
    monkeypatch.setattr(LivePlaylist, "num_tracks", property(lambda self: 3))
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(opener) == ["1", "2", "3"]
    assert world.account.playlists[made] == ["t1", "t2", "t3"]
    assert pair_cli.WITHHELD in _codes(envelope)


# ═══════════════════════════════════════════════════════════════════════════
# A rekordbox track the account cannot carry, skipped and remembered (R-988)
# ═══════════════════════════════════════════════════════════════════════════


def test_rows_the_account_cannot_carry_are_counted_skipped_and_never_asked_again(world, cfg):
    world.sql("UPDATE djmdContent SET ISRC = '' WHERE ID = '2'")
    del world.account.catalog["3"]
    world.account.reasons["3"] = "the provider has no track under this ISRC"
    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    made = world.titled("GIG READY Opener")
    assert world.account.playlists[made] == ["t1"]
    assert world.held(opener) == ["1", "2", "3"]
    assert envelope["data"]["totals"]["unmatched"] == 2
    assert [one["identity"] for one in world.account.matches].count("3") == 1
    assert pairs.PairStore(cfg).misses()["3"] == pairs.Miss(
        isrc("3"), "the provider has no track under this ISRC"
    )
    code, again = sync()
    assert code == int(ExitCode.OK), again
    code, third = sync()
    assert code == int(ExitCode.OK), third
    assert [one["identity"] for one in world.account.matches].count("3") == 1
    assert "2" not in [one["identity"] for one in world.account.matches]
    assert third["data"]["totals"]["unmatched"] == 2


def test_a_remembered_miss_is_asked_again_when_the_rows_isrc_changes(world, cfg):
    del world.account.catalog["3"]
    gig = world.folder("GIG READY")
    world.playlist("Opener", "3", under=gig)
    assert sync()[0] == int(ExitCode.OK)
    assert [one["identity"] for one in world.account.matches].count("3") == 1
    world.sql("UPDATE djmdContent SET ISRC = 'USBBB2600333' WHERE ID = '3'")
    world.account.catalog["3"] = "t3"
    assert sync()[0] == int(ExitCode.OK)
    assert [one["identity"] for one in world.account.matches].count("3") > 1
    assert world.account.playlists[world.titled("GIG READY Opener")] == ["t3"]
    assert "3" not in pairs.PairStore(cfg).misses()


def test_an_unreadable_candidate_is_never_remembered(world, cfg):
    from cratekit.modules.outbound.service import UNREADABLE_CANDIDATE

    del world.account.catalog["3"]
    world.account.reasons["3"] = f"a candidate {UNREADABLE_CANDIDATE}"
    gig = world.folder("GIG READY")
    world.playlist("Opener", "3", under=gig)
    assert sync()[0] == int(ExitCode.OK)
    assert "3" not in pairs.PairStore(cfg).misses()


# ═══════════════════════════════════════════════════════════════════════════
# The document, organize, and the configuration
# ═══════════════════════════════════════════════════════════════════════════


def test_a_write_of_the_pairs_alone_keeps_the_folders_misses_and_released(world, cfg):
    store = pairs.PairStore(cfg)
    store.reserve_folder("GIG READY", lambda: "folder-x")
    store.remember({"7": pairs.Miss("CODE", "none")})
    store.mark("acc-1", "rb-1", name="One")
    store.release("acc-1", "rb-1", side=pairs.ACCOUNT_SIDE)
    store.mark("acc-2", "rb-2", name="Two")
    assert store.folders()["GIG READY"].folder_id == "folder-x"
    assert store.misses() == {"7": pairs.Miss("CODE", "none")}
    assert store.released().rekordbox == frozenset({"rb-1"})


def test_reserve_made_makes_one_playlist_per_rekordbox_playlist(world, cfg):
    store = pairs.PairStore(cfg)
    made = []
    first = store.reserve_made("rb-1", name="X", folder="F", create=lambda: made.append(1) or "a1")
    second = store.reserve_made("rb-1", name="X", folder="F", create=lambda: made.append(1) or "a2")
    assert first == ("a1", True) and second == ("a1", False) and made == [1]


def test_an_unusable_released_record_refuses(world, cfg):
    store = pairs.PairStore(cfg)
    store.mark("acc-1", "rb-1", name="One")
    path = config.state_path("playlist_pairs", cfg)
    text = path.read_text().replace('"pairs"', '"released": {"account": [3]}, "pairs"')
    path.write_text(text)
    with pytest.raises(Exception) as raised:
        store.all()
    assert getattr(raised.value, "cause", None) is not None
    assert raised.value.cause.reason == "sync-pair-store-unusable"


def test_organize_does_not_list_a_paired_playlist_as_yours(cfg, monkeypatch):
    from cratekit.organize import account as organize_account
    from cratekit.organize.steps import Area

    pairs.PairStore(cfg).mark("acc-paired", "rb-1", name="Paired")
    fake = outbound_fakes.FakeAccount({})
    fake.titles = {"acc-paired": "Paired", "acc-mine": "Mine"}
    listed = FakeCatalogue(
        account=[
            AccountPlaylist(playlist_id="acc-paired", name="Paired"),
            AccountPlaylist(playlist_id="acc-mine", name="Mine"),
        ]
    )
    area = Area(name="account")

    class Lazy:
        def __init__(self, value):
            self.value = value

        def get(self):
            return self.value

    organize_account._yours(cfg, area, (), Lazy(listed), Lazy(fake))
    assert [one["playlist_id"] for one in area.yours] == ["acc-mine"]


def test_the_skip_list_defaults_to_archive_and_refuses_a_list_that_is_not_names(library):
    from tests.test_rebuild import valid_data

    assert config.from_dict(valid_data(library)).outbound.pair_skip_folders == ("ARCHIVE",)
    moved = config.from_dict(valid_data(library, outbound={"pair_skip_folders": ["WIP", "X"]}))
    assert moved.outbound.pair_skip_folders == ("WIP", "X")
    assert config.from_dict(
        valid_data(library, outbound={"pair_skip_folders": []})
    ).outbound.pair_skip_folders == ()
    for value in ("ARCHIVE", ["ARCHIVE", ""], [3]):
        problems = config.validate(valid_data(library, outbound={"pair_skip_folders": value}))
        assert [p for p in problems if config.PAIR_SKIP_FOLDERS_KEY in p], (value, problems)


def test_title_of_names_each_place():
    assert pair_discover.title_of(("Loose",)) == ("Playlists", "Playlists Loose")
    assert pair_discover.title_of(("GIG READY", "Opener")) == ("GIG READY", "GIG READY Opener")
    assert pair_discover.title_of(("GIG READY", "Halloween", "Opener")) == (
        "GIG READY",
        "GIG READY Halloween Opener",
    )


# ═══════════════════════════════════════════════════════════════════════════
# The review's findings, round one
# ═══════════════════════════════════════════════════════════════════════════


def test_a_made_pair_moved_into_archive_is_let_go_and_never_written_again(world, cfg):
    opener, made = _made_pair(world)
    archive = world.folder("ARCHIVE")
    world.sql("UPDATE djmdPlaylist SET ParentID = ? WHERE ID = ?", archive, opener)
    world.account.playlists[made].append("t3")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(opener) == ["1", "2"]
    assert pairs.PairStore(cfg).get(made) is None
    assert "ARCHIVE" in _said(envelope, pair_cli.RELEASED)
    assert world.account.playlists[made] == ["t1", "t2", "t3"]
    code, again = sync()
    assert code == int(ExitCode.OK), again
    assert world.held(opener) == ["1", "2"]


def test_two_favourites_playlists_leave_both_folders_out_and_say_so(world):
    gig = world.folder("GIG READY")
    world.playlist("All Favorites", "1", under=gig)
    world.playlist("Opener", "2", under=gig)
    favorites = world.folder("Favorites")
    world.playlist("All Favorites", "3", under=favorites)
    world.playlist("Loose", "4")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert sorted(world.account.titles.values()) == ["Playlists Loose"]
    said = _said(envelope, pair_cli.NOT_DISCOVERED)
    assert "2 playlists are named 'All Favorites'" in said


def test_a_tie_is_never_remembered_and_is_asked_again(world, cfg):
    from cratekit.modules.outbound.service import AGREEING_RELEASES

    del world.account.catalog["3"]
    world.account.reasons["3"] = f"2 {AGREEING_RELEASES}"
    gig = world.folder("GIG READY")
    world.playlist("Opener", "3", under=gig)
    assert sync()[0] == int(ExitCode.OK)
    assert "3" not in pairs.PairStore(cfg).misses()
    world.account.catalog["3"] = "t3"
    assert sync()[0] == int(ExitCode.OK)
    assert world.account.playlists[world.titled("GIG READY Opener")] == ["t3"]


def test_another_apps_top_folder_is_never_discovered(world):
    from cratekit.core import foreign_tree

    theirs = world.folder(foreign_tree.OWNER)
    world.playlist("Pushed", "1", under=theirs)
    world.playlist("Loose", "2")
    assert sync()[0] == int(ExitCode.OK)
    assert sorted(world.account.titles.values()) == ["Playlists Loose"]


def test_a_paired_playlist_is_not_listed_on_a_later_run(world):
    _made_pair(world)
    plan = plan_only()
    assert [item for item in plan["items"] if item["side"] == "discovery"] == []


def test_a_recorded_folder_deleted_on_the_account_is_made_again(world, cfg):
    _made_pair(world)
    old = pairs.PairStore(cfg).folders()["GIG READY"].folder_id
    world.account.folder_names.pop(old)
    gig = [pid for pid, name in world.sql("SELECT ID, Name FROM djmdPlaylist") if name == "GIG READY"][0]
    world.playlist("Closer", "3", under=str(gig))
    assert sync()[0] == int(ExitCode.OK)
    fresh = pairs.PairStore(cfg).folders()["GIG READY"].folder_id
    assert fresh != old
    assert world.account.placed[world.titled("GIG READY Closer")] == fresh


def test_a_version_one_document_is_read_and_written_as_version_two(world, cfg):
    import json

    store = pairs.PairStore(cfg)
    store.mark("acc-1", "rb-1", name="One")
    path = config.state_path("playlist_pairs", cfg)
    document = json.loads(path.read_text())
    document["version"] = 1
    path.write_text(json.dumps(document))
    assert "acc-1" in store.all()
    store.mark("acc-2", "rb-2", name="Two")
    assert json.loads(path.read_text())["version"] == pairs.PAIRS_VERSION == 2
