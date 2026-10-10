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

    def __init__(self, world: World) -> None:
        self.world = world

    @property
    def num_tracks(self):
        return self.world.declared

    def tracks(self, limit=None, offset=0):
        size = self.page_size if limit is None else limit
        members = self.world.account.playlists[ACCOUNT]
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
        self.catalogue = FakeCatalogue(
            playlists={ACCOUNT: LivePlaylist(self)},
            account=[AccountPlaylist(playlist_id=ACCOUNT, name=NAME)],
        )
        monkeypatch.setattr(catalogue, "resolve", catalogue_factory(self.catalogue))
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


def test_a_landed_track_another_account_playlist_landed_is_not_taken(world, cfg, tmp_path):
    from cratekit.cli import output
    from cratekit.intake import ingest

    w = world(account=("1",), rekordbox=("1",))
    assert sync(w.args())[0] == int(ExitCode.OK)
    _untagged_row(cfg, "8", tmp_path, file_isrc=isrc("8"))
    handle = w.open()
    try:
        mirror = handle.create_playlist("Another (INBOX)")
        handle.add_to_playlist(mirror, "8")
        handle.session.commit()
        mirror_id = str(mirror.ID)
    finally:
        rb_writer.close_db(handle)
    session.write_record(
        session.SessionRecord(
            session_id="s-other",
            workflow=ingest.INTAKE_WORKFLOW,
            started=output.timestamp(),
            state=session.SessionState.CLOSED,
            detail={
                ingest.INBOX_PLAYLISTS_KEY: [
                    {"id": mirror_id, "name": "Another", ingest.INBOX_ACCOUNT_KEY: "acc-other"}
                ]
            },
        ),
        cfg,
    )
    w.account.playlists[ACCOUNT].append("t8")
    code, envelope = sync([*VERB, ACCOUNT])
    assert code == int(ExitCode.OK), envelope
    assert w.held() == ["1"]
    assert len(envelope["data"]["totals"]["queued_jobs"]) == 1


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
