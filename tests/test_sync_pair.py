"""U130, ``crate sync pair``, driven through the dispatcher on a disposable database.

One account playlist and one rekordbox playlist, the account a fake that both
the catalogue (which lists) and the account seam (which writes) read, so a write
on one is what the next listing serves. Every scenario the brief names is driven
here end to end, two explicit gates and their recorded answers included.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from cratekit.core import config, jobs, rb_writer, session
from cratekit.core.exit_codes import ExitCode
from cratekit.label import catalogue
from cratekit.label.catalogue import AccountPlaylist
from cratekit.modules.outbound import account as account_module
from cratekit.modules.outbound import ledger, pairs
from cratekit.sync import pair_cli
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.label_fakes import FakeCatalogue, catalogue_factory
from tests.test_rb_writer_db import _build_disposable_database
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414

ACCOUNT = "acc-sunset"
NAME = "Sunset Warmup"
VERB = ["sync", "pair"]
#: Content rows one through nine, each carrying the ISRC its account track has.
ROWS = tuple(str(index) for index in range(1, 10))


def isrc(index: str) -> str:
    return f"USAAA26{int(index):05d}"


def remote(index: str) -> str:
    return f"t{index}"


class Listed:
    """A provider track in the shape the playlist reader reads."""

    def __init__(self, track_id: str, artist: str, name: str, code: str) -> None:
        self.id = track_id
        self.name = name
        self.artist = {"name": artist}
        self.isrc = code


class LivePlaylist:
    """The account playlist as the catalogue lists it, read off the fake account now.

    ``declared`` is a count the provider publishes beside the listing; None
    publishes none, so the listing is never short.
    """

    page_size = 100

    def __init__(self, world: World, playlist_id: str = ACCOUNT) -> None:
        self.world = world
        self.playlist_id = playlist_id

    @property
    def num_tracks(self):
        if self.world.withheld:
            return len(self.world.account.playlists[self.playlist_id])
        return self.world.declared

    def tracks(self, limit=None, offset=0):
        size = self.page_size if limit is None else limit
        members = [
            one
            for one in self.world.account.playlists[self.playlist_id]
            if one not in self.world.withheld
        ]
        return [
            Listed(one, f"Artist {one}", f"Title {one}", self.world.codes.get(one, ""))
            for one in members[offset : offset + size]
        ]


class World:
    """The account, its catalogue and the rekordbox playlist, wired together."""

    def __init__(self, cfg, monkeypatch, *, account=(), rekordbox=()) -> None:
        self.cfg = cfg
        self.account = outbound_fakes.FakeAccount(
            {content_id: remote(content_id) for content_id in ROWS}
        )
        self.account.playlists[ACCOUNT] = [remote(one) for one in account]
        self.codes = {remote(one): isrc(one) for one in ROWS}
        self.declared: int | None = None
        #: Tracks the account holds and the provider serves to nobody: counted,
        #: never listed, and never read back.
        self.withheld: set[str] = set()
        self.catalogue = FakeCatalogue(
            playlists={ACCOUNT: LivePlaylist(self)},
            account=[AccountPlaylist(playlist_id=ACCOUNT, name=NAME)],
        )
        monkeypatch.setattr(catalogue, "resolve", catalogue_factory(self.catalogue))
        real_tracks = self.account.playlist_tracks
        self.account.playlist_tracks = lambda playlist_id: tuple(
            one for one in real_tracks(playlist_id) if one not in self.withheld
        )
        monkeypatch.setattr(account_module, "resolve", outbound_fakes.account_factory(self.account))
        handle = self.open()
        try:
            made = handle.create_playlist("My Sunset")
            for content_id in rekordbox:
                handle.add_to_playlist(made, content_id)
            handle.session.commit()
            self.rekordbox_id = str(made.ID)
        finally:
            rb_writer.close_db(handle)

    def open(self):
        return rb_writer.open_db(Path(self.cfg.library.db_path), unlock=False, cfg=self.cfg)

    def held(self) -> list[str]:
        """The rekordbox playlist's live tracks, in track order, from SQL."""
        conn = sqlite3.connect(self.cfg.library.db_path)
        try:
            return [
                str(row[0])
                for row in conn.execute(
                    "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? "
                    "AND COALESCE(rb_local_deleted, 0) = 0 ORDER BY TrackNo, ID",
                    (self.rekordbox_id,),
                ).fetchall()
            ]
        finally:
            conn.close()

    def on_account(self) -> list[str]:
        return list(self.account.playlists[ACCOUNT])

    def rekordbox_add(self, *content_ids: str) -> None:
        handle = self.open()
        try:
            made = handle.get_playlist(ID=self.rekordbox_id)
            for content_id in content_ids:
                handle.add_to_playlist(made, content_id)
            handle.session.commit()
        finally:
            rb_writer.close_db(handle)

    def rekordbox_remove(self, *content_ids: str) -> None:
        conn = sqlite3.connect(self.cfg.library.db_path)
        try:
            for content_id in content_ids:
                conn.execute(
                    "UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE PlaylistID = ? "
                    "AND ContentID = ?",
                    (self.rekordbox_id, content_id),
                )
            conn.commit()
        finally:
            conn.close()

    def rekordbox_order(self, *content_ids: str) -> None:
        conn = sqlite3.connect(self.cfg.library.db_path)
        try:
            for number, content_id in enumerate(content_ids, start=1):
                conn.execute(
                    "UPDATE djmdSongPlaylist SET TrackNo = ? WHERE PlaylistID = ? "
                    "AND ContentID = ? AND COALESCE(rb_local_deleted, 0) = 0",
                    (number, self.rekordbox_id, content_id),
                )
            conn.commit()
        finally:
            conn.close()

    def args(self, *, mark: bool = True) -> list[str]:
        return [*VERB, ACCOUNT, *(["--rekordbox", self.rekordbox_id] if mark else [])]


def sync(args: list[str], *, rekordbox: str = "apply", account: str = "apply"):
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
def world(cfg, gates_pass, db, monkeypatch):
    def made(**kwargs) -> World:
        return World(cfg, monkeypatch, **kwargs)

    return made


def _codes(envelope) -> set[str]:
    return {warning["code"] for warning in envelope.get("warnings") or ()}


def _pair(cfg) -> pairs.Pair:
    held = pairs.PairStore(cfg).get(ACCOUNT)
    assert held is not None
    return held


# ═══════════════════════════════════════════════════════════════════════════
# The brief's scenarios
# ═══════════════════════════════════════════════════════════════════════════


def test_the_first_sync_marks_the_pair_and_adds_only(world, cfg):
    w = world(account=("1", "2"), rekordbox=("2", "3"))
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "2", "3"]
    assert w.on_account() == ["t1", "t2", "t3"]
    held = _pair(cfg)
    assert held.rekordbox_id == w.rekordbox_id
    assert held.account == ("t1", "t2", "t3")
    assert [member.content_id for member in held.rekordbox] == ["1", "2", "3"]
    assert w.account.taken == []


def test_the_first_sync_removes_nothing_on_either_side(world):
    w = world(account=("1",), rekordbox=("2",))
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert set(w.held()) == {"1", "2"} and set(w.on_account()) == {"t1", "t2"}
    assert envelope["data"]["totals"]["rekordbox_removes"] == 0
    assert envelope["data"]["totals"]["account_removes"] == 0


def test_a_track_added_on_the_account_only_lands_in_rekordbox_in_place(world):
    w = world(account=("1", "2"), rekordbox=("1", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.account.playlists[ACCOUNT] = ["t1", "t4", "t2"]
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "4", "2"]
    assert w.on_account() == ["t1", "t4", "t2"]


def test_a_track_added_in_rekordbox_only_lands_on_the_account(world):
    w = world(account=("1", "2"), rekordbox=("1", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.rekordbox_add("5")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.on_account() == ["t1", "t2", "t5"]
    assert w.held() == ["1", "2", "5"]


def test_a_track_removed_on_the_account_leaves_the_playlist_and_stays_in_the_collection(
    world, cfg
):
    w = world(account=("1", "2", "3"), rekordbox=("1", "2", "3"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.account.playlists[ACCOUNT] = ["t1", "t3"]
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "3"]
    removed = [item for item in envelope["data"]["items"] if item["action"] == "remove"]
    assert [(item["side"], item["content_id"]) for item in removed] == [("rekordbox", "2")]
    assert all(item["title"] for item in removed), "a removal on the gate names no track"
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        live = conn.execute(
            "SELECT COALESCE(rb_local_deleted, 0) FROM djmdContent WHERE ID = '2'"
        ).fetchone()
    finally:
        conn.close()
    assert live == (0,), "a removal took the track out of the collection"


def test_a_track_removed_in_rekordbox_is_taken_off_the_account(world):
    w = world(account=("1", "2", "3"), rekordbox=("1", "2", "3"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.rekordbox_remove("2")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.on_account() == ["t1", "t3"]
    assert w.account.taken == [(ACCOUNT, ("t2",))]


def test_a_track_removed_on_the_account_and_put_back_in_rekordbox_is_kept(world):
    w = world(account=("1", "2", "3"), rekordbox=("1", "2", "3"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.account.playlists[ACCOUNT] = ["t1", "t3"]
    w.rekordbox_remove("2")
    w.rekordbox_add("2")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert "2" in w.held()
    assert "t2" in w.on_account()
    assert w.account.taken == []


def test_when_both_sides_reorder_the_account_order_wins(world):
    w = world(account=("1", "2", "3"), rekordbox=("1", "2", "3"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.account.playlists[ACCOUNT] = ["t3", "t2", "t1"]
    w.rekordbox_order("2", "1", "3")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["3", "2", "1"]
    assert w.on_account() == ["t3", "t2", "t1"]


def test_when_rekordbox_alone_reorders_the_account_follows(world):
    w = world(account=("1", "2", "3"), rekordbox=("1", "2", "3"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.rekordbox_order("3", "1", "2")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.on_account() == ["t3", "t1", "t2"]
    assert w.held() == ["3", "1", "2"]


def test_an_unmatched_rekordbox_track_is_named_and_stays_in_rekordbox(world):
    w = world(account=("1",), rekordbox=("1", "6"))
    del w.account.catalog["6"]
    w.account.reasons["6"] = "three releases share its ISRC"
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert w.on_account() == ["t1"]
    assert w.held() == ["1", "6"]
    warning = next(
        one for one in envelope["warnings"] if one["code"] == pair_cli.UNMATCHED
    )
    assert "Title t6" in warning["message"]
    assert "three releases share its ISRC" in warning["message"]
    unmatched = [item for item in envelope["data"]["items"] if item["action"] == "unmatched"]
    assert [item["content_id"] for item in unmatched] == ["6"]


def test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row(world, cfg):
    w = world(account=("1",), rekordbox=("1",))
    w.account.playlists[ACCOUNT].append("t-missing")
    w.codes["t-missing"] = "GBZZZ2600099"
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1"]
    queued = envelope["data"]["totals"]["queued_jobs"]
    assert len(queued) == 1
    with jobs.open_store() as store:
        job = jobs.get(store, queued[0])
    assert job.handler_key == pair_cli.INTAKE_HANDLER
    assert job.payload["source_id"] == pair_cli.PAIR_SOURCE
    assert list(job.payload["tracks"]) == ["t-missing"]

    code, again = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), again
    assert again["data"]["totals"]["queued_jobs"] == []
    assert pair_cli.AWAITING in _codes(again)
    assert w.held() == ["1"]


def test_an_account_track_found_by_isrc_is_linked_and_the_link_is_kept(world, cfg):
    w = world(account=("1", "4"), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    assert w.held() == ["1", "4"]
    assert _pair(cfg).links.get("t4") == "4"


# ═══════════════════════════════════════════════════════════════════════════
# The gates, the snapshot, and what a skipped side owes
# ═══════════════════════════════════════════════════════════════════════════


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(world, cfg):
    w = world(account=("1",), rekordbox=("1",))
    session.ack_path(cfg).unlink()
    code, refused = drive(w.args())
    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert "gate" not in (refused.get("cause") or {}).get("detail", {})


def test_both_gates_are_asked_before_anything_is_written(world, cfg):
    w = world(account=("1",), rekordbox=("2",))
    code, first = drive(w.args())
    assert code == int(ExitCode.DECISION_REQUIRED)
    assert first["cause"]["detail"]["gate"] == pair_cli.REKORDBOX_GATE
    run_id = first["run_id"]
    drive(["run", "decide", run_id, pair_cli.REKORDBOX_GATE, "apply", "--actor", "a-person"])
    code, second = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_REQUIRED)
    assert second["cause"]["detail"]["gate"] == pair_cli.ACCOUNT_GATE
    assert w.held() == ["2"] and w.on_account() == ["t1"]
    assert pairs.PairStore(cfg).get(ACCOUNT) is None


def test_a_skipped_account_side_is_finished_by_the_next_sync(world, cfg):
    w = world(account=("1", "2"), rekordbox=("1", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.rekordbox_remove("2")
    w.rekordbox_add("5")
    code, envelope = sync([*VERB, ACCOUNT], account="skip")
    assert code == int(ExitCode.OK), envelope
    assert w.on_account() == ["t1", "t2"], "a skipped side was written"
    assert w.held() == ["1", "5"]

    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.on_account() == ["t1", "t5"]
    assert w.held() == ["1", "5"], "the owed removal came back as an addition"


def test_a_skipped_rekordbox_side_is_finished_by_the_next_sync(world):
    w = world(account=("1", "2"), rekordbox=("1", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.account.playlists[ACCOUNT] = ["t1"]
    code, envelope = sync([*VERB, ACCOUNT], rekordbox="skip")
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "2"]

    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1"]
    assert w.on_account() == ["t1"]


def test_both_sides_skipped_writes_nothing_and_marks_nothing(world, cfg):
    w = world(account=("1",), rekordbox=("2",))
    code, envelope = sync(w.args(), rekordbox="skip", account="skip")
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert pairs.PairStore(cfg).get(ACCOUNT) is None
    assert w.held() == ["2"]


def test_a_short_account_listing_reads_nothing_as_removed(world):
    w = world(account=("1", "2"), rekordbox=("1", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.account.playlists[ACCOUNT] = ["t1"]
    w.declared = 2
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "2"], "a withheld track was read as a removal"
    assert pair_cli.WITHHELD in _codes(envelope)


def test_a_short_listing_removes_nothing_from_the_account(world):
    w = world(account=("1", "2"), rekordbox=("1", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.rekordbox_remove("2")
    w.declared = 5
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.account.taken == []
    assert w.on_account() == ["t1", "t2"]


def test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale(world, cfg):
    w = world(account=("1",), rekordbox=("1",))
    code, first = drive(w.args())
    run_id = first["run_id"]
    drive(["run", "decide", run_id, pair_cli.REKORDBOX_GATE, "apply", "--actor", "a-person"])
    drive(["--run", run_id, *w.args()])
    drive(["run", "decide", run_id, pair_cli.ACCOUNT_GATE, "apply", "--actor", "a-person"])
    w.rekordbox_add("3")
    code, refused = drive(["--run", run_id, *w.args()])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert w.on_account() == ["t1"]


# ═══════════════════════════════════════════════════════════════════════════
# What a pair may hold
# ═══════════════════════════════════════════════════════════════════════════


def test_the_hearts_are_not_a_pair(world):
    w = world(account=("1",), rekordbox=("1",))
    code, refused = drive([*VERB, "favorites", "--rekordbox", w.rekordbox_id])
    assert refused["cause"]["reason"] == "sync-pair-out-of-scope", refused


def test_a_label_playlist_is_not_a_pair(world, cfg):
    w = world(account=("1",), rekordbox=("1",))
    ledger.reserve_set_playlist(cfg, "a set", "2026", lambda: ACCOUNT)
    code, refused = drive(w.args())
    assert refused["cause"]["reason"] == "sync-pair-out-of-scope", refused


def test_a_playlist_under_one_of_cratekits_trees_is_not_a_pair(world, cfg):
    from cratekit.core import taxonomy

    w = world(account=("1",), rekordbox=())
    handle = w.open()
    try:
        inbox = rb_writer.ensure_folder(handle, taxonomy.default_taxonomy().intake.display)
        made = handle.create_playlist("batch", parent=inbox)
        handle.session.commit()
        inside = str(made.ID)
    finally:
        rb_writer.close_db(handle)
    code, refused = drive([*VERB, ACCOUNT, "--rekordbox", inside])
    assert refused["cause"]["reason"] == "sync-pair-out-of-scope", refused


def test_a_folder_is_not_a_pair(world):
    w = world(account=("1",), rekordbox=())
    handle = w.open()
    try:
        folder = handle.create_playlist_folder("Mine")
        handle.session.commit()
        folder_id = str(folder.ID)
    finally:
        rb_writer.close_db(handle)
    code, refused = drive([*VERB, ACCOUNT, "--rekordbox", folder_id])
    assert refused["cause"]["reason"] == "sync-pair-out-of-scope", refused


def test_an_unmarked_account_playlist_with_no_rekordbox_playlist_is_refused(world):
    world(account=("1",), rekordbox=())
    code, refused = drive([*VERB, ACCOUNT])
    assert refused["cause"]["reason"] == "sync-pair-unknown", refused


def test_a_second_rekordbox_playlist_for_a_paired_account_playlist_is_refused(world):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    handle = w.open()
    try:
        other = handle.create_playlist("Another")
        handle.session.commit()
        other_id = str(other.ID)
    finally:
        rb_writer.close_db(handle)
    code, refused = drive([*VERB, ACCOUNT, "--rekordbox", other_id])
    assert refused["cause"]["reason"] == "sync-pair-conflict", refused


def test_with_no_argument_every_marked_pair_is_synced(world):
    w = world(account=("1", "2"), rekordbox=("1", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.account.playlists[ACCOUNT].append("t3")
    code, envelope = sync(VERB)
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "2", "3"]


def test_the_pairs_document_names_both_identifiers_and_no_path(world, cfg):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    document = json.loads(config.state_path("playlist_pairs", cfg).read_text())
    assert document["library_id"] == cfg.library.volume_id
    assert document["pairs"][ACCOUNT]["rekordbox_id"] == w.rekordbox_id
    assert str(cfg.library.root) not in json.dumps(document)


# ═══════════════════════════════════════════════════════════════════════════
# Where a match comes from when the row's own column is empty
# ═══════════════════════════════════════════════════════════════════════════


def _untagged_row(cfg, content_id: str, tmp_path: Path, *, file_isrc: str) -> None:
    """Give a row no ISRC of its own and a real audio file carrying ``file_isrc``."""
    from tests._containers import tagged_container

    target = Path(cfg.library.root) / "Music" / f"{content_id}.flac"
    tagged_container(tmp_path, target, isrc=file_isrc)
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        conn.execute("UPDATE djmdContent SET ISRC = '' WHERE ID = ?", (content_id,))
        conn.commit()
    finally:
        conn.close()


def test_a_rekordbox_row_with_no_isrc_column_is_matched_on_its_files_isrc(world, cfg, tmp_path):
    w = world(account=(), rekordbox=("7",))
    _untagged_row(cfg, "7", tmp_path, file_isrc=isrc("7"))
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    asked = [one for one in w.account.matches if one["identity"] == "7"]
    assert asked and asked[0]["isrc"] == isrc("7")
    assert w.on_account() == ["t7"]


def test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account(
    world, cfg, tmp_path
):
    from cratekit.cli import output
    from cratekit.intake import ingest

    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _untagged_row(cfg, "8", tmp_path, file_isrc=isrc("8"))
    handle = w.open()
    try:
        mirror = handle.create_playlist("Sunset Warmup (INBOX)")
        handle.add_to_playlist(mirror, "8")
        handle.session.commit()
        mirror_id = str(mirror.ID)
    finally:
        rb_writer.close_db(handle)
    session.write_record(
        session.SessionRecord(
            session_id="s-landed",
            workflow=ingest.INTAKE_WORKFLOW,
            started=output.timestamp(),
            state=session.SessionState.CLOSED,
            detail={
                ingest.INBOX_PLAYLISTS_KEY: [
                    {"id": mirror_id, "name": NAME, ingest.INBOX_ACCOUNT_KEY: ACCOUNT}
                ]
            },
        ),
        cfg,
    )
    w.account.playlists[ACCOUNT].append("t8")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "8"]
    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert _pair(cfg).links.get("t8") == "8"


def _landed_for(w, cfg, account_id: str, content_ids, *, session_id: str, name: str) -> str:
    """Record a landing that made one INBOX playlist for ``account_id``, holding the rows named."""
    from cratekit.cli import output
    from cratekit.intake import ingest

    handle = w.open()
    try:
        mirror = handle.create_playlist(f"{name} (INBOX)")
        for content_id in content_ids:
            handle.add_to_playlist(mirror, content_id)
        handle.session.commit()
        mirror_id = str(mirror.ID)
    finally:
        rb_writer.close_db(handle)
    session.write_record(
        session.SessionRecord(
            session_id=session_id,
            workflow=ingest.INTAKE_WORKFLOW,
            started=output.timestamp(),
            state=session.SessionState.CLOSED,
            detail={
                ingest.INBOX_PLAYLISTS_KEY: [
                    {"id": mirror_id, "name": name, ingest.INBOX_ACCOUNT_KEY: account_id}
                ]
            },
        ),
        cfg,
    )
    return mirror_id


def _acquired(envelope) -> list[str]:
    found: list[str] = []
    with jobs.open_store() as store:
        for job_id in envelope["data"]["totals"]["queued_jobs"]:
            found.extend(sorted((jobs.get(store, job_id).payload or {}).get("tracks") or {}))
    return sorted(found)


# U229. A track the library holds because a landing through ANOTHER account
# playlist brought it in is that row, never a track to download again.


def test_a_track_another_account_playlist_landed_is_added_and_never_queued(world, cfg, tmp_path):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _untagged_row(cfg, "8", tmp_path, file_isrc=isrc("8"))
    _landed_for(w, cfg, "acc-other", ("8",), session_id="s-other", name="Another")
    w.account.playlists[ACCOUNT].append("t8")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "8"]
    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert envelope["data"]["totals"]["acquire"] == 0
    assert _pair(cfg).links.get("t8") == "8"


def test_a_track_another_account_playlist_landed_with_its_isrc_in_the_row_is_added(world, cfg):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _landed_for(w, cfg, "acc-other", ("8",), session_id="s-other", name="Another")
    w.account.playlists[ACCOUNT].append("t8")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "8"]
    assert envelope["data"]["totals"]["queued_jobs"] == []


def test_a_track_no_landing_brought_in_is_still_queued(world, cfg, tmp_path):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    # Another account playlist's landing holds row eight, whose file carries
    # its own code, and the account lists a track nobody landed.
    _untagged_row(cfg, "8", tmp_path, file_isrc=isrc("8"))
    _landed_for(w, cfg, "acc-other", ("8",), session_id="s-other", name="Another")
    w.codes["t40"] = "USZZZ2600040"
    w.account.playlists[ACCOUNT].append("t40")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1"]
    assert _acquired(envelope) == ["t40"]


def test_two_landed_rows_carrying_the_code_are_ambiguous_and_queue_nothing(world, cfg, tmp_path):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _untagged_row(cfg, "8", tmp_path, file_isrc=isrc("8"))
    _untagged_row(cfg, "9", tmp_path, file_isrc=isrc("8"))
    _landed_for(w, cfg, "acc-other", ("8",), session_id="s-other", name="Another")
    _landed_for(w, cfg, "acc-third", ("9",), session_id="s-third", name="Third")
    w.account.playlists[ACCOUNT].append("t8")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1"]
    assert pair_cli.AMBIGUOUS in _codes(envelope)
    assert envelope["data"]["totals"]["queued_jobs"] == []


def test_this_account_playlists_own_landing_wins_over_anothers(world, cfg, tmp_path):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _untagged_row(cfg, "8", tmp_path, file_isrc=isrc("8"))
    _untagged_row(cfg, "9", tmp_path, file_isrc=isrc("8"))
    _landed_for(w, cfg, ACCOUNT, ("8",), session_id="s-own", name=NAME)
    _landed_for(w, cfg, "acc-other", ("9",), session_id="s-other", name="Another")
    # A track nobody landed keeps the widened step asked, which must answer
    # only what the earlier steps left lacking, never t8 again.
    w.codes["t40"] = "USZZZ2600040"
    w.account.playlists[ACCOUNT].extend(["t8", "t40"])
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "8"]
    assert pair_cli.AMBIGUOUS not in _codes(envelope)
    assert _acquired(envelope) == ["t40"]


def test_a_track_another_pairs_intake_job_found_owned_is_added(world, cfg, tmp_path, monkeypatch):
    from cratekit.intake import missing_cli

    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    # Row eight carries no code anywhere the plan reads by ISRC: only the
    # other pair's intake job, which found it owned by its path, names it.
    _untagged_row(cfg, "8", tmp_path, file_isrc="USZZZ2600099")
    _other_pairs_job(cfg, state=str(jobs.JobState.SUCCEEDED))
    owned = str(Path(cfg.library.root) / "Music" / "8.flac")
    monkeypatch.setattr(
        missing_cli,
        "job_reports",
        lambda _store, _job: ({"item_id": "t8", "state": pair_cli.OWNED_STATE, "paths": [owned]},),
    )
    w.account.playlists[ACCOUNT].append("t8")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "8"]
    assert envelope["data"]["totals"]["queued_jobs"] == []


def _other_pairs_job(
    cfg,
    *,
    state: str,
    config_toml: str | None = None,
    tracks: dict[str, str] | None = None,
) -> str:
    """Queue a ``sync pair`` intake job for another account playlist, holding t8 unless told."""
    from cratekit.intake import cli as intake_cli

    held = tracks if tracks is not None else {"t8": isrc("8")}
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=pair_cli.INTAKE_HANDLER,
            payload={
                "source_id": pair_cli.PAIR_SOURCE,
                intake_cli.SOURCE: "acc-other",
                intake_cli.TRACKS: {one: {"isrc": code} for one, code in held.items()},
                intake_cli.PLAYLIST_NAME: "Another",
            },
            cfg=cfg,
            item_ids=tuple(held),
        )
        store.conn.execute("UPDATE jobs SET state = ? WHERE job_id = ?", (state, job.job_id))
        if config_toml is not None:
            store.conn.execute(
                "UPDATE jobs SET config_toml = ? WHERE job_id = ?", (config_toml, job.job_id)
            )
        store.conn.commit()
    return job.job_id


def test_another_pairs_job_that_no_longer_reads_stops_no_plan(world, cfg):
    """U229. One pair's old job is passed over by every other pair's plan, never a refusal."""
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _other_pairs_job(cfg, state=str(jobs.JobState.SUCCEEDED), config_toml="[library]\nroot = 1\n")
    w.codes["t40"] = "USZZZ2600040"
    w.account.playlists[ACCOUNT].append("t40")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert _acquired(envelope) == ["t40"]


# R-1385. A TRACK NO LANDING BROUGHT IN IS QUEUED ONCE FOR THE LIBRARY: once
# for every pair of one plan listing it, and never again beside another
# pair's job still holding it.

SECOND = "acc-second"
SECOND_NAME = "Second Set"
LACKING = {"t40": "USZZZ2600040"}


def _second_pair(w, cfg, tracks) -> str:
    """Mark and sync a second pair, ``Second Set`` and a rekordbox playlist of its own."""
    w.account.playlists[SECOND] = [remote(one) for one in tracks]
    w.catalogue.playlists[SECOND] = LivePlaylist(w, SECOND)
    w.catalogue.account.append(AccountPlaylist(playlist_id=SECOND, name=SECOND_NAME))
    handle = w.open()
    try:
        made = handle.create_playlist("Second")
        for content_id in tracks:
            handle.add_to_playlist(made, content_id)
        handle.session.commit()
        second_id = str(made.ID)
    finally:
        rb_writer.close_db(handle)
    code, envelope = sync([*VERB, SECOND, "--rekordbox", second_id])
    assert code == int(ExitCode.OK), envelope
    return second_id


def _awaiting(envelope) -> list[tuple[str, str, str]]:
    return [
        (item["pair"], item["remote_id"], item.get("reason", ""))
        for item in envelope["data"]["items"]
        if item["side"] == "library" and item["action"] == "awaiting"
    ]


def _acquiring(envelope) -> list[tuple[str, str]]:
    return [
        (item["pair"], item["remote_id"])
        for item in envelope["data"]["items"]
        if item["side"] == "library" and item["action"] == "acquire"
    ]


def test_two_pairs_listing_one_lacking_track_queue_it_once(world, cfg):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _second_pair(w, cfg, ("2",))
    w.codes.update(LACKING)
    w.account.playlists[ACCOUNT].append("t40")
    w.account.playlists[SECOND].append("t40")
    code, envelope = sync(VERB)
    assert code == int(ExitCode.OK), envelope
    assert len(envelope["data"]["totals"]["queued_jobs"]) == 1
    assert _acquired(envelope) == ["t40"]
    assert envelope["data"]["totals"]["acquire"] == 1
    ((first, _),) = _acquiring(envelope)
    ((later, track, why),) = _awaiting(envelope)
    assert track == "t40" and later != first
    assert "this sync" in why
    assert pair_cli.AWAITING in _codes(envelope)
    # THE NEXT SYNC QUEUES NOTHING: the one job holds t40 for both pairs.
    code, again = sync(VERB)
    assert code == int(ExitCode.OK), again
    assert again["data"]["totals"]["queued_jobs"] == []
    assert sorted(track for _pair, track, _why in _awaiting(again)) == ["t40", "t40"]


@pytest.mark.parametrize(
    "state", [jobs.JobState.QUEUED, jobs.JobState.RUNNING, jobs.JobState.SUCCEEDED]
)
def test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued(world, cfg, state):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _other_pairs_job(cfg, state=str(state), tracks=LACKING)
    w.codes.update(LACKING)
    w.account.playlists[ACCOUNT].append("t40")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["queued_jobs"] == []
    ((pair, track, why),) = _awaiting(envelope)
    assert (pair, track) == (ACCOUNT, "t40")
    assert "Another" in why
    assert pair_cli.AWAITING in _codes(envelope)


@pytest.mark.parametrize("state", [jobs.JobState.FAILED, jobs.JobState.CANCELLED])
def test_a_track_only_a_failed_or_cancelled_job_held_is_queued(world, cfg, state):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _other_pairs_job(cfg, state=str(state), tracks=LACKING)
    w.codes.update(LACKING)
    w.account.playlists[ACCOUNT].append("t40")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert _acquired(envelope) == ["t40"]
    assert _awaiting(envelope) == []


def test_a_track_this_pair_alone_lists_is_queued_once_beside_anothers_job(world, cfg):
    """Another pair's job holding another track holds nothing of this pair's."""
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _other_pairs_job(cfg, state=str(jobs.JobState.QUEUED), tracks={"t41": "USZZZ2600041"})
    w.codes.update(LACKING)
    w.account.playlists[ACCOUNT].append("t40")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert _acquired(envelope) == ["t40"]
    assert _awaiting(envelope) == []


def _held_at_its_gate(w):
    """Drive a sync of every pair to its first gate, answering nothing: the run id."""
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    return first["run_id"], first["cause"]["detail"]["gate"]


def _finished(run_id: str, gate: str):
    """Answer each gate the run asks and resume it, until it answers."""
    for _ in range(3):
        decided, said = drive(["run", "decide", run_id, gate, "apply", "--actor", "a-person"])
        assert decided == int(ExitCode.OK), said
        code, envelope = drive(["--run", run_id, *VERB])
        if code != int(ExitCode.DECISION_REQUIRED):
            return code, envelope
        gate = envelope["cause"]["detail"]["gate"]
    raise AssertionError("the verb kept asking after both gates were answered")


def test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale(world, cfg):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.codes.update(LACKING)
    w.account.playlists[ACCOUNT].append("t40")
    run_id, gate = _held_at_its_gate(w)
    _other_pairs_job(cfg, state=str(jobs.JobState.QUEUED), tracks=LACKING)
    code, refused = _finished(run_id, gate)
    assert code == int(ExitCode.DECISION_STALE), refused
    assert "another sync queued since the plan" in json.dumps(refused)


def test_the_runs_own_job_for_an_earlier_pair_stops_no_later_command(world, cfg):
    """The write held across its gates finishes beside the job its first pair queued."""
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _second_pair(w, cfg, ("2",))
    w.codes.update(LACKING)
    w.account.playlists[ACCOUNT].append("t40")
    w.account.playlists[SECOND].append("t40")
    run_id, gate = _held_at_its_gate(w)
    code, envelope = _finished(run_id, gate)
    assert code == int(ExitCode.OK), envelope
    assert _acquired(envelope) == ["t40"]


def test_one_row_landed_in_two_inbox_playlists_is_one_row(world, cfg, tmp_path):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _untagged_row(cfg, "8", tmp_path, file_isrc=isrc("8"))
    _landed_for(w, cfg, "acc-other", ("8",), session_id="s-other", name="Another")
    _landed_for(w, cfg, "acc-third", ("8",), session_id="s-third", name="Third")
    w.account.playlists[ACCOUNT].append("t8")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "8"]
    assert pair_cli.AMBIGUOUS not in _codes(envelope)


def test_each_landed_file_is_read_once_per_plan(world, cfg, tmp_path, monkeypatch):
    """U229. This pair's own landing and every landing are one read of each file."""
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _untagged_row(cfg, "8", tmp_path, file_isrc=isrc("8"))
    _landed_for(w, cfg, ACCOUNT, ("8",), session_id="s-own", name=NAME)
    # A track nobody landed reaches every step, so both landed reads are asked.
    w.codes["t40"] = "USZZZ2600040"
    w.account.playlists[ACCOUNT].append("t40")
    read: list[str] = []
    real = pair_cli.file_identity

    def counted(config_read, recorded):
        read.append(recorded)
        return real(config_read, recorded)

    monkeypatch.setattr(pair_cli, "file_identity", counted)
    code, envelope = drive([*VERB, ACCOUNT])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert [one for one in read if one.endswith("/8.flac")] == [
        f"{cfg.library.root}/Music/8.flac"
    ]


def test_two_rows_carrying_one_isrc_add_neither_and_say_so(world, cfg):
    w = world(account=("1",), rekordbox=("1",))
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        conn.execute("UPDATE djmdContent SET ISRC = ? WHERE ID = '9'", (isrc("4"),))
        conn.commit()
    finally:
        conn.close()
    w.account.playlists[ACCOUNT].append("t4")
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1"]
    assert pair_cli.AMBIGUOUS in _codes(envelope)
    assert envelope["data"]["totals"]["queued_jobs"] == []


# ═══════════════════════════════════════════════════════════════════════════
# The playlists sweep leaves a pair alone
# ═══════════════════════════════════════════════════════════════════════════


def test_the_sweep_excludes_a_paired_playlist():
    from cratekit.sync import playlists

    listed = AccountPlaylist(playlist_id=ACCOUNT, name=NAME, tracks=3)
    assert (
        playlists.exclusion(listed, recorded=set(), in_flight=set(), paired={ACCOUNT})
        == playlists.Excluded.PAIRED
    )
    assert playlists.exclusion(listed, recorded=set(), in_flight=set()) is None


def test_the_sync_pass_hands_the_pairs_to_the_sweep(world, cfg, monkeypatch):
    from cratekit.sync import playlists

    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    seen: list[frozenset[str]] = []
    real = playlists.plan

    def spy(*args, **kwargs):
        seen.append(kwargs.get("paired", frozenset()))
        return real(*args, **kwargs)

    monkeypatch.setattr(playlists, "plan", spy)
    from cratekit.sync import cli as sync_cli
    from cratekit.sync import sources

    spec = next(one for one in sources.SPECS if one.source_id == "playlists")
    planned = sync_cli._plan_playlists(spec, None)
    assert seen and ACCOUNT in seen[0]
    excluded = planned.detail["excluded"]
    assert excluded[ACCOUNT]["reason"] == str(playlists.Excluded.PAIRED)


# ═══════════════════════════════════════════════════════════════════════════
# The review's findings, each driven
# ═══════════════════════════════════════════════════════════════════════════


def test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first(world, cfg):
    """With one side's snapshot alone, the other side would read every track as added."""
    w = world(account=("1", "2"), rekordbox=("1", "2"))
    code, envelope = sync(w.args(), account="skip")
    assert code == int(ExitCode.OK), envelope
    held = _pair(cfg)
    assert held.first is True and held.account is None and held.rekordbox is None


def test_a_whole_sync_after_a_skipped_one_finishes_both_sides_from_the_old_base(world):
    w = world(account=("1", "2", "3"), rekordbox=("1", "2", "3"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.rekordbox_remove("2")
    assert sync([*VERB, ACCOUNT], account="skip")[0] == int(ExitCode.OK)
    w.rekordbox_order("3", "1")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.on_account() == ["t3", "t1"]
    assert w.held() == ["3", "1"]


def test_a_track_the_account_already_holds_by_isrc_is_linked_without_asking_the_provider(world, cfg):
    w = world(account=("1", "2"), rekordbox=("1", "2"))
    # The provider would name another release of row 2's recording.
    w.account.catalog["2"] = "t2-album"
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert [one["identity"] for one in w.account.matches] == []
    assert w.on_account() == ["t1", "t2"]
    assert _pair(cfg).links.get("t2") == "2"


def test_a_row_with_no_isrc_anywhere_is_named_and_the_provider_is_not_asked(world, cfg):
    w = world(account=("1",), rekordbox=("1", "6"))
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        conn.execute("UPDATE djmdContent SET ISRC = '' WHERE ID = '6'")
        conn.commit()
    finally:
        conn.close()
    code, envelope = sync(w.args())
    assert code == int(ExitCode.OK), envelope
    assert "6" not in [one["identity"] for one in w.account.matches]
    warning = next(one for one in envelope["warnings"] if one["code"] == pair_cli.UNMATCHED)
    assert pair_cli.NO_ISRC in warning["message"]
    assert w.on_account() == ["t1"]


def test_a_short_listing_leaves_the_snapshot_so_a_withheld_track_is_not_read_as_added(world, cfg):
    w = world(account=("1", "2"), rekordbox=("1", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    before = _pair(cfg)
    w.withheld = {"t2"}
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert _pair(cfg).account == before.account
    assert envelope["data"]["totals"]["account_adds"] == 0, "a withheld track was offered back"
    # The provider serves t2 again, and the author took it out of rekordbox.
    w.withheld = set()
    w.rekordbox_remove("2")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1"]
    assert w.on_account() == ["t1"]


def test_the_writer_refuses_a_playlist_whose_memberships_moved_since_the_plan(world, cfg):
    """The gate's digest catches this first; the writer's own check is held alone here."""
    from cratekit.core import analysis_store
    from cratekit.core.cause import CratekitError
    from cratekit.write import playlist_pair

    w = world(account=(), rekordbox=("1", "2"))
    handle = w.open()
    try:
        planned = playlist_pair.read_playlist(handle, w.rekordbox_id)
    finally:
        rb_writer.close_db(handle)
    w.rekordbox_add("3")
    change = playlist_pair.Change(
        playlist_id=w.rekordbox_id,
        before=planned.memberships(),
        adds=("4",),
        order=("1", "2", "4"),
    )
    handle = rb_writer.open_db(Path(cfg.library.db_path), require_closed=True, unlock=False, cfg=cfg)
    try:
        with pytest.raises(CratekitError) as refused:
            playlist_pair.apply(
                cfg,
                handle,
                change,
                source="playlist-pair:test",
                analysis_roots=analysis_store.watch_roots(cfg),
            )
    finally:
        rb_writer.close_db(handle)
    assert refused.value.cause.reason == "decision-stale"
    assert w.held() == ["1", "2", "3"]


def test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair(world, cfg, monkeypatch):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    pairs.PairStore(cfg).mark("acc-gone", "no-such-rekordbox-playlist", name="Gone")
    w.catalogue.account.append(AccountPlaylist(playlist_id="acc-gone", name="Gone"))
    w.account.playlists[ACCOUNT].append("t2")
    code, envelope = sync(VERB)
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1", "2"]
    assert pair_cli.LEFT_OUT in _codes(envelope)
    code, refused = drive([*VERB, "acc-gone"])
    assert refused["cause"]["reason"] == "sync-pair-unknown", refused


def test_a_track_held_twice_that_lost_one_copy_is_not_read_as_put_back(world):
    w = world(account=("1", "2"), rekordbox=("1", "2", "2"))
    assert sync(w.args())[0] == int(ExitCode.OK)
    conn = sqlite3.connect(w.cfg.library.db_path)
    try:
        first = conn.execute(
            "SELECT ID FROM djmdSongPlaylist WHERE PlaylistID = ? AND ContentID = '2' "
            "AND COALESCE(rb_local_deleted, 0) = 0 ORDER BY TrackNo LIMIT 1",
            (w.rekordbox_id,),
        ).fetchone()[0]
        conn.execute("UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE ID = ?", (first,))
        conn.commit()
    finally:
        conn.close()
    w.account.playlists[ACCOUNT] = ["t1"]
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1"]
    assert w.on_account() == ["t1"]


def test_skipping_the_only_side_with_changes_answers_no_op(world):
    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    w.account.playlists[ACCOUNT].append("t2")
    code, envelope = sync([*VERB, ACCOUNT], rekordbox="skip")
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert w.held() == ["1"]


# ═══════════════════════════════════════════════════════════════════════════
# U206: a rehearsal and its live run pay for their ISRC lookups once
# ═══════════════════════════════════════════════════════════════════════════


class _Named:
    def __init__(self, name: str) -> None:
        self.name = name


class _ProviderTrack:
    """A provider track in the client's own shape, the one answer to its ISRC."""

    def __init__(self, track_id: str) -> None:
        self.id = track_id
        self.name = self.title = f"Title {track_id}"
        self.version = None
        self.artists = [_Named(f"Artist {track_id}")]
        self.artist = self.artists[0]
        self.album = None
        self.available = True


class _IsrcClient:
    """The provider client the real account adapter asks, counting every ISRC."""

    country_code = "GB"

    def __init__(self) -> None:
        self.asked: list[str] = []

    def get_tracks_by_isrc(self, code: str) -> list[_ProviderTrack]:
        self.asked.append(code)
        index = str(int(code[-5:]))
        return [_ProviderTrack(remote(index))]


def _through_the_shipped_lookup(w: World, client: _IsrcClient) -> None:
    """The fake account's match goes through the shipped adapter's, ISRC cache
    and all, built afresh for every row as a new process would build it, over
    the configuration the run itself loaded."""
    from cratekit.modules.outbound import tidal_account

    def match_track(**kwargs):
        made = tidal_account.TidalAccount(client, sleep=lambda _: None, cfg=config.load())
        return made.match_track(**kwargs)

    w.account.match_track = match_track


def _loading(monkeypatch, loaded) -> None:
    """Every load in the run answers ``loaded``, as the suite's fixture does."""
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: loaded)


@pytest.mark.parametrize("days", [30, 0], ids=["kept", "cache-off"])
def test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again(
    world, cfg, monkeypatch, days
):
    """The sitting's rule for a copy run: the library's state directory copied to
    a scratch name and ``state_dirname`` naming it. The rehearsal's own state is
    thrown away with it, and the ISRC answers are not."""
    import dataclasses
    import shutil

    from cratekit.cli import ISRC_LOOKUPS

    live_cfg = dataclasses.replace(
        cfg, provider=dataclasses.replace(cfg.provider, isrc_cache_days=days)
    )
    scratch = ".cratekit-rehearsal"
    rehearsal = dataclasses.replace(
        live_cfg, library=dataclasses.replace(live_cfg.library, state_dirname=scratch)
    )
    w = world(account=("1",), rekordbox=("1", "2", "3"))
    client = _IsrcClient()
    _through_the_shipped_lookup(w, client)
    root = Path(cfg.library.root)
    shutil.copytree(root / cfg.library.state_dirname, root / scratch)
    _loading(monkeypatch, rehearsal)

    code, rehearsed = drive(w.args())
    assert code == int(ExitCode.DECISION_REQUIRED), rehearsed
    assert sorted(client.asked) == [isrc("2"), isrc("3")]
    assert (root / scratch) in config.state_path("playlist_pairs", rehearsal).parents
    _loading(monkeypatch, live_cfg)

    code, live = drive(w.args())

    assert code == int(ExitCode.DECISION_REQUIRED), live
    assert live["cause"]["detail"]["shown"]["digest"] == rehearsed["cause"]["detail"]["shown"]["digest"]
    said = [one["message"] for one in live["warnings"] if one["code"] == ISRC_LOOKUPS]
    if days:
        assert sorted(client.asked) == [isrc("2"), isrc("3")], "the live plan asked again"
        assert said == ["2 ISRC lookups answered from the cache, 0 asked of the streaming provider"]
    else:
        assert sorted(client.asked) == sorted([isrc("2"), isrc("3")] * 2)
        assert said == ["0 ISRC lookups answered from the cache, 2 asked of the streaming provider"]
