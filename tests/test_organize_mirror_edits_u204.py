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
        return [Listed(one, self.world.codes.get(one, "")) for one in members]


class World(Machine):
    """U201's library grown a Favorites folder and INBOX, with a catalogue over the account."""

    def __init__(self, cfg: config.Config, scratch: Path, monkeypatch) -> None:
        super().__init__(cfg, scratch)
        self.scratch = scratch
        self.codes = {"r1": "ISRC00000001", "r2": "ISRC00000002", "r3": "ISRC00000003"}
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
