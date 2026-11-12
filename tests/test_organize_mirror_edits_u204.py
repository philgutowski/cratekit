"""U204: an edit made on the account to the Favorites folder or INBOX changes the library.

Driven end to end on U201's disposable library, grown a Favorites folder (All
Favorites and one month) and a database native INBOX holding two live batches,
with the account faked by the strict recording account and the catalogue by the
label fakes. Each pass is a new organize run: the rekordbox area's
``mirror-edits`` and ``mirror-downloads`` steps and the account mirror, all off
one shared reading as ``crate organize`` builds them, written in organize's
order. What is asserted is what the account, the database and the job queue
hold afterwards, never a step's own report alone.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import shutil
import sqlite3
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import config, jobs, rb_writer, tags, taxonomy, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound import mirror_edits as edits
from cratekit.organize import mirror_downloads, mirror_edits, rekordbox
from cratekit.organize.steps import LISTED, NOTHING, PLANNED
from tests._containers import synth_container
from tests.label_fakes import FakeCatalogue, catalogue_factory
from tests.test_inbox_rotate import _record_landing
from tests.test_label_workers import installed as installed  # noqa: PLC0414
from tests.test_organize_mirror_edits import Machine
from tests.test_organize_mirror_edits import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_routing_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_routing_workers import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_routing_workers import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_routing_workers import configured as configured  # noqa: PLC0414
from tests.test_routing_workers import library as library  # noqa: PLC0414

DECLARED = taxonomy.default_taxonomy()
SOURCE = "All Favorites"
MONTH = "2026-10"
BATCH_A = "2026-10-20 Tidal playlists"
BATCH_B = "2026-10-31 Defected"
PINK = "1"


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
    def num_tracks(self) -> int:
        return len(self.world.account.playlists[self.playlist_id])

    def tracks(self, limit=None, offset=0):
        size = self.page_size if limit is None else limit
        members = self.world.account.playlists[self.playlist_id][offset : offset + size]
        listed = [Listed(one, self.world.codes.get(one, "")) for one in members]
        for one in listed:
            if one.id in self.world.untitled:
                # R-1289: a row the account lists with no title.
                one.name = ""
        return listed


class World(Machine):
    """U201's library grown a Favorites folder and INBOX, with a catalogue over the account."""

    def __init__(self, cfg: config.Config, scratch: Path, monkeypatch) -> None:
        super().__init__(cfg, scratch)
        self.scratch = scratch
        self.codes = {"r1": "ISRC00000001", "r2": "ISRC00000002", "r3": "ISRC00000003"}
        #: Account tracks the catalogue lists with no title (R-1289).
        self.untitled: set[str] = set()
        handle = rb_writer.open_db(self.db, unlock=False, cfg=cfg)
        try:
            from pyrekordbox.db6 import tables

            from tests.test_rb_writer_db import _row

            handle.session.add(
                _row(tables.DjmdColor, ID=PINK, ColorCode=1, SortKey=1, Commnt="Pink")
            )
            favorites = rb_writer.ensure_folder(handle, "Favorites")
            source = handle.create_playlist(SOURCE, parent=favorites)
            month = handle.create_playlist(MONTH, parent=favorites)
            inbox = rb_writer.ensure_folder(handle, DECLARED.intake.display)
            self.old = str(rb_writer.ensure_folder(handle, DECLARED.intake_old.display, inbox).ID)
            batch_a = handle.create_playlist(BATCH_A, parent=inbox)
            batch_b = handle.create_playlist(BATCH_B, parent=inbox)
            handle.session.flush()
            rb_writer.add_memberships(handle, source, ["1"])
            rb_writer.add_memberships(handle, month, ["1"])
            rb_writer.add_memberships(handle, batch_a, ["1"])
            rb_writer.add_memberships(handle, batch_b, ["2"])
            handle.session.commit()
            self.favorites = str(favorites.ID)
            self.source, self.month = str(source.ID), str(month.ID)
            self.inbox = str(inbox.ID)
            self.batch_a, self.batch_b = str(batch_a.ID), str(batch_b.ID)
        finally:
            rb_writer.close_db(handle)
        tree_registry.write(
            cfg,
            tree_registry.read(cfg).with_record(
                tree_registry.TreeRecord(
                    tree_id=DECLARED.intake.id,
                    mode=tree_registry.Mode.DATABASE,
                    cutover_on=date(2026, 8, 1),
                    root_id=self.inbox,
                    source=tree_registry.DerivationSource.TAXONOMY,
                )
            ),
        )
        _record_landing(cfg, self.batch_a, BATCH_A, date(2026, 10, 20))
        _record_landing(cfg, self.batch_b, BATCH_B, date(2026, 10, 31))
        self.catalogue = FakeCatalogue(playlists={})
        real = self.catalogue.playlists

        class Every(dict):
            def get(inner, key, default=None):  # noqa: N805
                if key in self.account.playlists:
                    return LivePlaylist(self, key)
                return real.get(key, default)

            def __contains__(inner, key):  # noqa: N805
                return key in self.account.playlists

            def __getitem__(inner, key):  # noqa: N805
                return LivePlaylist(self, key)

        self.catalogue.playlists = Every()
        monkeypatch.setattr(catalogue, "resolve", catalogue_factory(self.catalogue))

    # ── one organize run, with the downloads step ─────────────────────────

    def plan_all(self):
        area, step, shared = self.plan()
        queue = mirror_downloads.add_step(self.cfg, shared)
        return area, step, queue, shared

    def run_all(self):
        area, step, queue, _shared = self.plan_all()
        for one in (step, queue, *area.steps):
            if one.apply is not None:
                one.applied = one.apply()
        return area, step, queue

    # ── the library ──────────────────────────────────────────────────────

    def members(self, playlist_id: str) -> set[str]:
        conn = sqlite3.connect(self.db)
        try:
            found = conn.execute(
                "SELECT ContentID FROM djmdSongPlaylist WHERE PlaylistID = ? "
                "AND COALESCE(rb_local_deleted, 0) = 0",
                (playlist_id,),
            ).fetchall()
        finally:
            conn.close()
        return {str(one[0]) for one in found}

    def under_favorites(self, name: str) -> str:
        conn = sqlite3.connect(self.db)
        try:
            found = conn.execute(
                "SELECT ID FROM djmdPlaylist WHERE ParentID = ? AND Name = ? "
                "AND COALESCE(rb_local_deleted, 0) = 0",
                (self.favorites, name),
            ).fetchall()
        finally:
            conn.close()
        assert len(found) == 1, found
        return str(found[0][0])

    def colour(self, content_id: str) -> str:
        conn = sqlite3.connect(self.db)
        try:
            (found,) = conn.execute(
                "SELECT ColorID FROM djmdContent WHERE ID = ?", (content_id,)
            ).fetchone()
        finally:
            conn.close()
        return str(found or "")

    def land(self, content_id: str, *, code: str, batch: str = "2026-11-02 Landed") -> str:
        """A download landed: its file, its row and its batch in INBOX, named by its record."""
        silence = synth_container(self.scratch, ".flac")
        path = Path(self.cfg.library.root) / "Music" / f"Track {content_id}.flac"
        shutil.copyfile(silence, path)
        assert tags.write_tags(path, {"title": f"Track {content_id}", "artist": "Probe"})
        conn = sqlite3.connect(self.db)
        try:
            conn.execute(
                f"INSERT INTO djmdContent (ID, Title, FolderPath, {rb_writer.ISRC_COLUMN}, "
                f"rb_local_deleted) VALUES (?, ?, ?, ?, 0)",
                (content_id, f"Track {content_id}", str(path), code),
            )
            conn.commit()
        finally:
            conn.close()
        handle = rb_writer.open_db(self.db, unlock=False, cfg=self.cfg)
        try:
            made = handle.create_playlist(batch, parent=handle.get_playlist(ID=self.inbox))
            handle.session.flush()
            rb_writer.add_memberships(handle, made, [content_id])
            handle.session.commit()
            batch_id = str(made.ID)
        finally:
            rb_writer.close_db(handle)
        _record_landing(self.cfg, batch_id, batch, date(2026, 11, 2))
        self.files[content_id] = path
        return batch_id


@pytest.fixture
def world(acknowledged, tmp_path, monkeypatch) -> World:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    built = World(acknowledged, scratch, monkeypatch)
    built.run_all()
    return built


def _items(step) -> list[dict]:
    return [one for one in step.items if one.get("edit")]


def _named(step) -> list[dict]:
    return [one for one in step.items if not one.get("edit")]


def _queued(cfg) -> list[jobs.Job]:
    with jobs.open_store() as store:
        return [
            job
            for job in jobs.list_jobs(store)
            if (job.payload or {}).get("source_id") == mirror_downloads.SOURCE_ID
        ]


# ═══════════════════════════════════════════════════════════════════════════
# 1. The first run, and a run with nothing changed
# ═══════════════════════════════════════════════════════════════════════════


def test_the_first_run_mirrors_favorites_and_inbox_and_records_their_snapshots(world):
    assert world.held(SOURCE) == ["r1"]
    assert world.held(f"Favorites {MONTH}") == ["r1"]
    assert world.held(f"INBOX {BATCH_A}") == ["r1"]
    assert world.held(f"INBOX {BATCH_B}") == ["r2"]
    recorded = ledger.mirror_folders(world.cfg)
    assert recorded["Favorites"].playlists[SOURCE].agreed == {"r1"}
    assert recorded["INBOX"].playlists[f"INBOX {BATCH_B}"].agreed == {"r2"}


def test_a_second_run_with_nothing_changed_plans_nothing_anywhere(world):
    area, step, queue, _shared = world.plan_all()
    assert step.state == NOTHING
    assert queue.state == NOTHING
    assert {one.state for one in area.steps} <= {NOTHING, LISTED}


def test_edits_on_playlists_never_agreed_change_nothing_in_the_library(world):
    world.forget_snapshots()
    world.put_in(SOURCE, "r2")
    world.take_off(f"INBOX {BATCH_A}", "r1")

    _area, step, queue = world.run_all()

    assert step.state == NOTHING and queue.state == NOTHING
    assert world.members(world.source) == {"1"}
    assert world.members(world.batch_a) == {"1"}
    # The mirror wrote rekordbox's side back, as before U201.
    assert world.held(SOURCE) == ["r1"]
    assert world.held(f"INBOX {BATCH_A}") == ["r1"]


# ═══════════════════════════════════════════════════════════════════════════
# 2. Favorites
# ═══════════════════════════════════════════════════════════════════════════


def test_a_track_added_to_all_favorites_is_favourited_in_its_month_and_coloured(world):
    world.put_in(SOURCE, "r2", at="2026-09-14T10:00:00+00:00")
    before = list(world.account.chunks), list(world.account.taken)

    _area, step, _queue = world.run_all()

    (change,) = _items(step)
    assert change["edit"] == edits.FAVOURITE
    assert change["joins"] == [f"Favorites / {SOURCE}"]
    assert change["makes"] == "2026-09"
    assert change["colour"] == "Pink"
    assert world.members(world.source) == {"1", "2"}
    assert world.members(world.under_favorites("2026-09")) == {"2"}
    assert world.members(world.month) == {"1"}
    assert world.colour("2") == PINK
    # THE ACCOUNT KEPT THE EDIT, nothing taken off or added back over it.
    assert world.held(SOURCE) == ["r1", "r2"]
    assert (list(world.account.chunks), list(world.account.taken)) == before
    # The next run mirrors the month it made, and the one after plans nothing.
    world.run_all()
    assert world.held("Favorites 2026-09") == ["r2"]
    area, step, queue, shared = world.plan_all()
    assert step.state == NOTHING and queue.state == NOTHING
    assert {one.state for one in area.steps} <= {NOTHING, LISTED}
    assert shared.reading().decided.decisions == ()


def test_a_track_added_to_all_favorites_with_no_time_goes_to_undated(world):
    world.put_in(SOURCE, "r2")

    _area, step, _queue = world.run_all()

    (change,) = _items(step)
    assert change["makes"] == "Undated"
    assert world.members(world.under_favorites("Undated")) == {"2"}


def test_a_track_added_to_a_month_is_favourited_there(world):
    world.put_in(f"Favorites {MONTH}", "r2")

    _area, step, _queue = world.run_all()

    (change,) = _items(step)
    assert change["edit"] == edits.FAVOURITE
    assert sorted(change["joins"]) == [f"Favorites / {MONTH}", f"Favorites / {SOURCE}"]
    assert world.members(world.source) == {"1", "2"}
    assert world.members(world.month) == {"1", "2"}
    assert world.held(f"Favorites {MONTH}") == ["r1", "r2"]


def test_a_track_removed_from_all_favorites_leaves_the_favorites_folder(world):
    world.take_off(SOURCE, "r1")

    area, step, _queue = world.run_all()

    (change,) = _items(step)
    assert change["edit"] == edits.UNFAVOURITE
    assert sorted(change["leaves"]) == [f"Favorites / {MONTH}", f"Favorites / {SOURCE}"]
    assert "stays hearted" in change["note"]
    assert world.members(world.source) == set()
    assert world.members(world.month) == set()
    # It stays in the collection and in every other playlist it sits in.
    assert world.members(world.batch_a) == {"1"}
    assert world.places("1") == {("Deep House", "Low")}
    # The gate names the removal and the heart's second step.
    deletes = mirror_edits.deletes(step.items)
    assert len(deletes) == 1 and "un-hearted" in deletes[0]
    # The account kept it off All Favorites, and the next run takes it off the month.
    assert world.held(SOURCE) == []
    world.run_all()
    assert world.held(f"Favorites {MONTH}") == []
    _area, step, queue, _shared = world.plan_all()
    assert step.state == NOTHING and queue.state == NOTHING


def test_a_track_removed_from_a_month_alone_is_listed_and_not_carried(world):
    world.take_off(f"Favorites {MONTH}", "r1")

    for _ in range(2):
        _area, step, _queue = world.run_all()
        assert step.state == NOTHING
        (named,) = _named(step)
        assert named["outcome"] == edits.HELD and "listed and not carried" in named["why"]
        # Neither carried nor undone.
        assert world.members(world.month) == {"1"}
        assert world.held(f"Favorites {MONTH}") == []


def test_a_short_favorites_listing_changes_nothing(world):
    world.take_off(SOURCE, "r1")
    world.account.hidden[world.remote(SOURCE)] = ("r1",)
    world.account.playlists[world.remote(SOURCE)].append("r1")

    _area, step, _queue = world.run_all()

    assert step.state == NOTHING
    assert world.members(world.source) == {"1"}
    assert world.members(world.month) == {"1"}


def test_an_unfavourite_against_a_rekordbox_addition_keeps_the_addition(world):
    world.take_off(SOURCE, "r1")
    world.take_off(f"Favorites {MONTH}", "r1")
    handle = rb_writer.open_db(world.db, unlock=False, cfg=world.cfg)
    try:
        made = handle.create_playlist("2026-11", parent=handle.get_playlist(ID=world.favorites))
        handle.session.flush()
        rb_writer.add_memberships(handle, made, ["1"])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    world.run_all()  # the new month is mirrored and agreed first

    _area, step, _queue = world.run_all()

    assert step.state == NOTHING
    assert world.members(world.source) == {"1"}


# ═══════════════════════════════════════════════════════════════════════════
# 3. INBOX
# ═══════════════════════════════════════════════════════════════════════════


def test_a_track_added_to_an_inbox_batch_joins_it_and_one_taken_off_leaves_it(world):
    world.put_in(f"INBOX {BATCH_A}", "r2")
    world.take_off(f"INBOX {BATCH_B}", "r2")

    _area, step, _queue = world.run_all()

    found = {one["edit"]: one for one in _items(step)}
    assert found[edits.JOIN]["joins"] == [f"INBOX / {BATCH_A}"]
    assert found[edits.LEAVE]["leaves"] == [f"INBOX / {BATCH_B}"]
    assert world.members(world.batch_a) == {"1", "2"}
    assert world.members(world.batch_b) == set()
    # Nothing left the collection or the genre tree.
    assert world.places("2") == {("Deep House", "Med")}
    assert world.held(f"INBOX {BATCH_A}") == ["r1", "r2"]
    assert world.held(f"INBOX {BATCH_B}") == []
    _area, step, queue, _shared = world.plan_all()
    assert step.state == NOTHING and queue.state == NOTHING


def test_a_batch_moved_into_old_since_the_plan_is_never_touched(world):
    world.put_in(f"INBOX {BATCH_A}", "r2")
    _area, step, _queue, _shared = world.plan_all()
    assert step.state == PLANNED
    conn = sqlite3.connect(world.db)
    try:
        conn.execute(
            "UPDATE djmdPlaylist SET ParentID = ? WHERE ID = ?", (world.old, world.batch_a)
        )
        conn.commit()
    finally:
        conn.close()

    with pytest.raises(CratekitError) as raised:
        step.apply()

    assert raised.value.cause.reason == "decision-stale"
    assert world.members(world.batch_a) == {"1"}


def test_a_batch_in_old_is_not_read_and_not_written(world):
    conn = sqlite3.connect(world.db)
    try:
        conn.execute(
            "UPDATE djmdPlaylist SET ParentID = ? WHERE ID = ?", (world.old, world.batch_a)
        )
        conn.commit()
    finally:
        conn.close()
    world.account.playlists[world.remote(f"INBOX {BATCH_A}")].append("r2")

    area, step, _queue = world.run_all()

    assert step.state == NOTHING
    assert world.members(world.batch_a) == {"1"}
    # The mirror retires the playlist of the batch that left INBOX, as U150 does.
    assert any("left INBOX" in line for line in area.deletes)


# ═══════════════════════════════════════════════════════════════════════════
# 4. A track the library lacks: queued once, held, filed when it lands
# ═══════════════════════════════════════════════════════════════════════════


def _land_and_file(world, *, matched_as: str) -> None:
    world.account.catalog["3"] = matched_as
    world.land("3", code="ISRC00000003")


def test_a_track_the_library_lacks_is_queued_once_held_and_filed_when_it_lands(world):
    world.put_in("Tech House Med", "r3")

    _area, step, queue = world.run_all()

    assert queue.state == PLANNED
    (job,) = _queued(world.cfg)
    assert job.handler_key == mirror_downloads.HANDLER == "intake.playlist"
    assert job.payload[intake_cli.SOURCE] == world.remote("Tech House Med")
    assert list(job.payload[intake_cli.TRACKS]) == ["r3"]
    assert job.payload[intake_cli.TRACKS]["r3"]["isrc"] == "ISRC00000003"
    assert world.held("Tech House Med") == ["r3"]
    # QUEUED ONCE: the next run names it as awaiting and queues nothing.
    _area, step, queue = world.run_all()
    assert queue.state == NOTHING
    assert [one["outcome"] for one in queue.items] == ["awaiting its landing"]
    assert len(_queued(world.cfg)) == 1
    assert world.held("Tech House Med") == ["r3"]
    # IT LANDS, and the next run files it where the account put it.
    _land_and_file(world, matched_as="r3")
    _area, step, queue = world.run_all()
    (change,) = _items(step)
    assert change["edit"] == edits.MOVE and change["joins"] == ["Tech House / Med"]
    assert world.places("3") == {("Tech House", "Med")}
    assert tags.read_genre_from_file(world.files["3"]) == "Tech House"
    assert len(_queued(world.cfg)) == 1
    assert world.held("Tech House Med") == ["r3"]


def test_a_landed_track_the_provider_ties_to_another_release_is_still_filed(world):
    world.put_in("Tech House Med", "r3")
    world.run_all()
    _land_and_file(world, matched_as="r3-other-release")

    _area, step, _queue = world.run_all()

    (change,) = _items(step)
    assert change["edit"] == edits.MOVE
    assert world.places("3") == {("Tech House", "Med")}
    # The row is answered as the track the account holds, so the mirror never
    # swaps it for the other release.
    world.run_all()
    assert world.held("Tech House Med") == ["r3"]
    assert "r3-other-release" not in world.held("INBOX 2026-11-02 Landed")


def test_a_track_added_to_inbox_or_favorites_that_the_library_lacks_is_queued(world):
    world.put_in(f"INBOX {BATCH_A}", "r3")
    world.put_in(SOURCE, "r3")

    _area, _step, queue = world.run_all()

    assert queue.state == PLANNED
    queued = {
        job.payload[intake_cli.SOURCE]: list(job.payload[intake_cli.TRACKS])
        for job in _queued(world.cfg)
    }
    # One job, the first playlist it was added to: a track is queued once.
    assert list(queued.values()) == [["r3"]]
    assert set(queued) <= {world.remote(f"INBOX {BATCH_A}"), world.remote(SOURCE)}
    assert world.held(SOURCE) == ["r1", "r3"]
    assert world.held(f"INBOX {BATCH_A}") == ["r1", "r3"]


def test_a_track_a_snapshot_once_held_is_never_queued_again(world):
    decided = edits.decide(
        [
            edits.Mirrored(
                place=edits.Place(SOURCE, "Favorites", SOURCE, True, edits.FAVORITES),
                account=frozenset({"r9"}),
                agreed=frozenset(),
            ),
            edits.Mirrored(
                place=edits.Place(f"INBOX {BATCH_A}", "INBOX", BATCH_A, True, edits.INBOX),
                account=frozenset({"r9"}),
                agreed=frozenset({"r9"}),
            ),
        ],
        {},
    )
    assert decided.wanted == ()


def test_the_steps_are_kinds_the_rekordbox_area_names():
    assert rekordbox.MIRROR_DOWNLOADS in rekordbox.STEPS
    assert rekordbox.STEPS.index(rekordbox.MIRROR_EDITS) < rekordbox.STEPS.index(
        rekordbox.MIRROR_DOWNLOADS
    )


def test_never_a_beat_grid(world):
    world.put_in(SOURCE, "r2")
    world.put_in(f"INBOX {BATCH_A}", "r2")

    world.run_all()

    conn = sqlite3.connect(world.db)
    try:
        (grids,) = conn.execute(
            "SELECT COUNT(*) FROM djmdContent WHERE BPM IS NOT NULL AND BPM != 0"
        ).fetchone()
    finally:
        conn.close()
    assert grids == 0


def test_without_a_reading_the_downloads_step_is_listed(acknowledged):
    from datetime import date as day

    area = rekordbox.plan_area(
        acknowledged,
        None,
        gate="organize.rekordbox",
        today=day(2026, 11, 5),
        labels=(),
        report=True,
        only=frozenset({rekordbox.MIRROR_DOWNLOADS}),
    )
    (step,) = area.steps
    assert step.state == LISTED and step.key == rekordbox.MIRROR_DOWNLOADS


# ═══════════════════════════════════════════════════════════════════════════
# 5. Review round one (Fable): driven, then pinned
# ═══════════════════════════════════════════════════════════════════════════


def _second_month(world) -> str:
    handle = rb_writer.open_db(world.db, unlock=False, cfg=world.cfg)
    try:
        made = handle.create_playlist("2026-09", parent=handle.get_playlist(ID=world.favorites))
        handle.session.commit()
        pid = str(made.ID)
    finally:
        rb_writer.close_db(handle)
    world.run_all()
    return pid


def test_a_track_moved_between_months_leaves_the_old_month(world):
    """Finding 1: a month move was carried as a second month and listed for ever."""
    september = _second_month(world)
    world.take_off(f"Favorites {MONTH}", "r1")
    world.put_in("Favorites 2026-09", "r1")

    _area, step, _queue = world.run_all()

    (change,) = _items(step)
    assert change["edit"] == edits.FAVOURITE
    assert change["joins"] == ["Favorites / 2026-09"]
    assert change["leaves"] == [f"Favorites / {MONTH}"]
    assert world.members(september) == {"1"}
    assert world.members(world.month) == set()
    assert world.members(world.source) == {"1"}
    assert world.held(f"Favorites {MONTH}") == []
    _area, step, queue, shared = world.plan_all()
    assert step.state == NOTHING and queue.state == NOTHING
    assert shared.reading().decided.decisions == ()


def test_another_release_of_an_owned_recording_is_never_queued_nor_swapped(world):
    """Finding 2: r9 carries row 1's ISRC; nothing is queued, row 1 keeps its track."""
    world.codes["r9"] = "ISRC00000001"
    world.put_in("Tech House Med", "r9")

    for _ in range(2):
        _area, _step, queue = world.run_all()
        assert queue.state == NOTHING
        (named,) = queue.items
        assert named["outcome"] == "not queued" and "already holds its recording" in named["why"]
    assert _queued(world.cfg) == []
    assert ledger.mirror_links(world.cfg)["1"][0] == "r1"
    assert world.held("Deep House Low") == ["r1"]
    assert world.held(SOURCE) == ["r1"]
    assert world.held("Tech House Med") == ["r9"]


def test_a_recording_the_library_holds_in_no_playlist_is_never_queued(world):
    """Finding 3: a row in no mirrored playlist is found by the database's code."""
    conn = sqlite3.connect(world.db)
    try:
        conn.execute(
            f"INSERT INTO djmdContent (ID, Title, {rb_writer.ISRC_COLUMN}, rb_local_deleted) "
            f"VALUES ('4', 'Track 4', 'ISRC00000004', 0)"
        )
        conn.commit()
    finally:
        conn.close()
    world.codes["r4"] = "ISRC00000004"
    world.put_in("Tech House Med", "r4")

    _area, _step, queue = world.run_all()

    assert queue.state == NOTHING
    assert "row 4" in queue.items[0]["why"]
    assert _queued(world.cfg) == []


def test_an_inbox_edit_over_a_latched_intake_tree_writes_nothing(world, monkeypatch):
    from cratekit.core import convergence
    from cratekit.core.cause import refuse

    asked: list[str] = []

    def latched(_cfg, _db, tree_id, _registry, **_kwargs):
        asked.append(tree_id)
        raise refuse("tree-unconverged", "the tree is latched", origin=("test",))

    monkeypatch.setattr(convergence, "assert_tree_writable", latched)
    world.put_in(f"INBOX {BATCH_A}", "r2")
    _area, step, _queue, _shared = world.plan_all()

    with pytest.raises(CratekitError) as caught:
        step.apply()

    assert caught.value.cause.reason == "tree-unconverged"
    assert asked == [DECLARED.intake.id]
    assert world.members(world.batch_a) == {"1"}


def test_a_favourites_only_write_detects_an_out_of_band_restore_and_asks_no_tree_latch(
    world, monkeypatch
):
    from cratekit.core import convergence

    detected: list[str] = []
    real = convergence.detect_out_of_band_restore

    def watched(cfg, db, registry, **kwargs):
        detected.append("asked")
        return real(cfg, db, registry, **kwargs)

    def never(*_args, **_kwargs):
        raise AssertionError("no tree is written by a favourite")

    monkeypatch.setattr(convergence, "detect_out_of_band_restore", watched)
    monkeypatch.setattr(convergence, "assert_tree_writable", never)
    world.put_in(SOURCE, "r2")

    world.run_all()

    assert detected == ["asked"]
    assert world.members(world.source) == {"1", "2"}


def test_a_favourite_the_placement_did_not_write_is_refused_at_the_read_back(world, monkeypatch):
    from cratekit.favorites import placement

    real = placement.place

    def short(db, home, pairs, **kwargs):
        return real(db, home, [], **kwargs)

    monkeypatch.setattr(placement, "place", short)
    world.put_in(f"Favorites {MONTH}", "r2")
    _area, step, _queue, _shared = world.plan_all()

    with pytest.raises(CratekitError) as caught:
        step.apply()

    assert caught.value.cause.reason == "session-committed-unverified"


def test_a_track_put_in_a_quarter_is_named_and_not_filed(world):
    handle = rb_writer.open_db(world.db, unlock=False, cfg=world.cfg)
    try:
        handle.create_playlist("2026-Q3", parent=handle.get_playlist(ID=world.favorites))
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    world.run_all()
    world.put_in("Favorites 2026-Q3", "r2")

    _area, step, _queue = world.run_all()

    assert step.state == NOTHING
    (named,) = _named(step)
    assert named["outcome"] == "not taken" and "quarter" in named["why"]
    assert world.members(world.source) == {"1"}


def test_two_plans_approved_one_after_the_other_queue_a_track_once(world):
    world.put_in("Tech House Med", "r3")
    _area, _step, first, _shared = world.plan_all()
    _area, _step, second, _shared = world.plan_all()

    first.apply()
    second.apply()

    assert len(_queued(world.cfg)) == 1


def test_a_failed_download_frees_its_track_to_be_queued_again(world):
    world.put_in("Tech House Med", "r3")
    world.run_all()
    (job,) = _queued(world.cfg)
    with jobs.open_store() as store:
        store.conn.execute(
            "UPDATE jobs SET state = ? WHERE job_id = ?", (str(jobs.JobState.FAILED), job.job_id)
        )
        store.conn.commit()

    _area, _step, queue = world.run_all()

    assert queue.state == PLANNED
    assert len(_queued(world.cfg)) == 2


def test_an_untitled_track_on_a_mirrored_playlist_is_named_and_the_others_queue(world):
    """R-1289: one row the account lists with no title no longer stops the playlist."""
    world.codes["r9"] = "ISRC00000009"
    world.untitled.add("r9")
    world.put_in("Tech House Med", "r9")
    world.put_in("Tech House Med", "r3")

    _area, _step, queue = world.run_all()

    assert queue.state == PLANNED
    (job,) = _queued(world.cfg)
    assert list(job.payload[intake_cli.TRACKS]) == ["r3"]
    (named,) = [one for one in queue.items if one.get("track") == "r9"]
    assert named["outcome"] == "not queued"
    assert "the account lists it with no title" in named["why"]
    assert named["playlist"] == "Tech House Med"


def test_a_playlist_the_provider_cannot_list_is_named_and_the_others_queue():
    from types import SimpleNamespace

    from cratekit.core.cause import refuse

    one = edits.Place("Tech House Med", "Tech House", "Med", True)
    two = edits.Place("Deep House Low", "Deep House", "Low", True)
    decided = edits.decide(
        [
            edits.Mirrored(place=one, account=frozenset({"r7"}), agreed=frozenset()),
            edits.Mirrored(place=two, account=frozenset({"r8"}), agreed=frozenset()),
        ],
        {},
    )
    recorded = {
        folder: SimpleNamespace(playlists={title: SimpleNamespace(remote_id=pid)})
        for folder, title, pid in (
            ("Tech House", "Tech House Med", "p1"),
            ("Deep House", "Deep House Low", "p2"),
        )
    }
    reading = SimpleNamespace(decided=decided, recorded=recorded)

    def listed(pid):
        if pid == "p1":
            raise refuse("label-playlist-unreadable", "down", origin=("test",))
        return intake_cli.Readable(
            tracks={"r8": {"isrc": "ISRC00000008", "artist": "A", "title": "T"}},
            short=None,
            unread={},
            order=("r8",),
        )

    cfg = SimpleNamespace(library=SimpleNamespace(volume_id="v"))
    from unittest import mock

    with mock.patch.object(mirror_downloads, "queued", return_value={}):
        planned = mirror_downloads.plan(cfg, reading, listed=listed, owned=lambda _code: ())

    assert list(planned.queue) == ["p2"]
    assert [one["track"] for one in planned.named] == ["r7"]


# ═══════════════════════════════════════════════════════════════════════════
# 6. Review round two (Fable): driven, then pinned
# ═══════════════════════════════════════════════════════════════════════════


def test_a_favorites_edit_planned_and_not_applied_is_taken_whole_by_the_next_run(world):
    """Round two, finding 1: the plan's snapshot of a level playlist swallowed half the edit."""
    september = _second_month(world)
    handle = rb_writer.open_db(world.db, unlock=False, cfg=world.cfg)
    try:
        rb_writer.add_memberships(handle, handle.get_playlist(ID=september), ["1"])
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    world.take_off(f"Favorites {MONTH}", "r1")
    # Later than rekordbox's own addition, so the account's move is the one carried.
    world.put_in("Favorites 2026-09", "r1", at="2099-01-01T00:00:00+00:00")
    # The run that plans records its snapshots and its account side, and the
    # edits step is never applied (rekordbox was open, say).
    area, step, _queue, _shared = world.plan_all()
    assert step.state == PLANNED
    for one in area.steps:
        if one.apply is not None:
            one.apply()

    _area, step, _queue = world.run_all()

    (change,) = _items(step)
    assert change["leaves"] == [f"Favorites / {MONTH}"]
    assert world.members(world.month) == set()
    assert world.members(september) == {"1"}
    _area, step, _queue, shared = world.plan_all()
    assert step.state == NOTHING
    assert shared.reading().decided.decisions == ()


@pytest.mark.parametrize(
    ("state", "said"),
    [("owned", "already holds it"), ("missing", "could not be fetched"), ("offered", None)],
)
def test_a_finished_download_that_never_lands_is_never_said_to_await_one(
    world, monkeypatch, state, said
):
    """Round two, finding 2: the job owned what this step's own check cannot see."""
    from cratekit.intake import missing_cli

    world.put_in("Tech House Med", "r3")
    world.run_all()
    (job,) = _queued(world.cfg)
    with jobs.open_store() as store:
        store.conn.execute(
            "UPDATE jobs SET state = ? WHERE job_id = ?",
            (str(jobs.JobState.SUCCEEDED), job.job_id),
        )
        store.conn.commit()
    monkeypatch.setattr(
        missing_cli, "job_reports", lambda _store, _job: ({"item_id": "r3", "state": state},)
    )

    _area, _step, queue = world.run_all()

    (named,) = queue.items
    if said is None:
        assert named["outcome"] == "awaiting its landing"
    else:
        assert named["outcome"] == "not queued" and said in named["why"]
        assert "awaiting" not in named["why"]
    assert len(_queued(world.cfg)) == 1
    assert world.held("Tech House Med") == ["r3"]


def test_a_playlist_of_another_name_in_the_favorites_folder_is_mirrored_one_way(world):
    """Mutation row O1: only All Favorites and a filing playlist are read as edits."""
    handle = rb_writer.open_db(world.db, unlock=False, cfg=world.cfg)
    try:
        handle.create_playlist("Warmup", parent=handle.get_playlist(ID=world.favorites))
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    world.run_all()
    world.put_in("Favorites Warmup", "r2")

    _area, step, _queue = world.run_all()

    assert step.state == NOTHING and step.items == []
    assert world.held("Favorites Warmup") == []


def test_a_month_the_placement_did_not_make_is_refused_at_the_read_back(world, monkeypatch):
    """Mutation row O8: the favourite's month is read back as well as All Favorites."""
    from cratekit.favorites import placement

    real = placement.place

    def no_month(db, home, pairs, **kwargs):
        return real(db, home, [(content_id, None) for content_id, _month in pairs], **kwargs)

    monkeypatch.setattr(placement, "place", no_month)
    world.put_in(SOURCE, "r2", at="2026-09-14T10:00:00+00:00")
    _area, step, _queue, _shared = world.plan_all()

    with pytest.raises(CratekitError) as caught:
        step.apply()

    assert caught.value.cause.reason == "session-committed-unverified"


def test_the_downloads_plan_reads_the_library_through_a_reports_one_handle(world, monkeypatch):
    """U267. ``--report`` hands its one read handle to the ISRC read, which opens none."""
    import sys

    world.put_in("Tech House Med", "r3")
    _area, _step, shared = world.plan()
    opened: list[str] = []
    real = rb_writer.open_db

    def counting(*args, **kwargs):
        opened.append(sys._getframe(1).f_code.co_name)
        return real(*args, **kwargs)

    monkeypatch.setattr(rb_writer, "open_db", counting)
    alone = mirror_downloads.add_step(world.cfg, shared)
    assert opened == ["_owned"], "the plan reads the library's codes on its own handle"
    opened.clear()
    one_read = rb_writer.SharedRead(world.cfg)
    try:
        through = mirror_downloads.add_step(world.cfg, shared, one_read=one_read)
    finally:
        one_read.close()

    assert opened == ["handle"]
    assert through.state == alone.state == PLANNED
    assert (through.digest, through.items) == (alone.digest, alone.items)
