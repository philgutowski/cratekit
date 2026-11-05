"""U201: an edit made on the account to a mirrored genre playlist changes the library.

Driven end to end on a disposable database holding an adopted BY GENRE + ENERGY
tree of two genre folders and two tagged files, with the account faked by the
strict recording account: the mirror's own step (``account_mirror.add_steps``)
and the rekordbox area's ``mirror-edits`` step, both off one shared reading as
``crate organize`` builds them, each pass a new organize run. What is asserted
is what the account, the files and the database hold afterwards, never a step's
own report alone.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import json
import shutil
import sqlite3
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import active_taxonomy, config, rb_writer, tags, taxonomy, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.modules.outbound import ledger, mirror
from cratekit.modules.outbound import mirror_edits as edits
from cratekit.organize import account_mirror, mirror_edits, rekordbox
from cratekit.organize.steps import LISTED, NOTHING, PLANNED, REFUSED, Area
from cratekit.write import routing_cli
from tests import outbound_fakes
from tests._containers import synth_container
from tests.test_active_taxonomy import write_active
from tests.test_label_workers import installed as installed  # noqa: PLC0414
from tests.test_rb_writer_db import _build_disposable_database
from tests.test_routing_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_routing_workers import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_routing_workers import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_routing_workers import configured as configured  # noqa: PLC0414
from tests.test_routing_workers import library as library  # noqa: PLC0414

ROOT = "BY GENRE + ENERGY"
BANDS = ("Low", "Med", "High", "Unsorted", "with vox")
GENRES = {"Deep House": "100", "Tech House": "101"}
#: Two library tracks, each its collection row, its file and where it starts.
TRACKS = {"1": ("Deep House", "Low", 2), "2": ("Deep House", "Med", 5)}


class Machine:
    """The disposable library and the faked account, and one organize run at a time."""

    def __init__(self, cfg: config.Config, scratch: Path) -> None:
        self.cfg = cfg
        self.account = outbound_fakes.StrictAccount(catalog={"1": "r1", "2": "r2"})
        self.runs = 0
        write_active(cfg, taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME))
        self.db = Path(cfg.library.db_path)
        _build_disposable_database(self.db)
        silence = synth_container(scratch, ".flac")
        conn = sqlite3.connect(self.db)
        for name, genre_id in GENRES.items():
            conn.execute(
                "INSERT INTO djmdGenre (ID, Name, rb_local_deleted, created_at, updated_at) "
                "VALUES (?, ?, 0, '2026-01-01', '2026-01-01')",
                (genre_id, name),
            )
        self.files: dict[str, Path] = {}
        for content_id, (genre, _band, energy) in TRACKS.items():
            path = Path(cfg.library.root) / "Music" / f"Track {content_id}.flac"
            shutil.copyfile(silence, path)
            assert tags.write_tags(
                path,
                {"title": f"Track {content_id}", "artist": "Probe", "genre": genre, "energylevel": energy},
            )
            self.files[content_id] = path
            conn.execute(
                f"UPDATE djmdContent SET FolderPath = ?, GenreID = ?, {rb_writer.ISRC_COLUMN} = ? "
                f"WHERE ID = ?",
                (str(path), GENRES[genre], f"ISRC0000000{content_id}", content_id),
            )
        conn.commit()
        conn.close()
        handle = rb_writer.open_db(self.db, unlock=False, cfg=cfg)
        try:
            root = rb_writer.ensure_folder(handle, ROOT)
            self.playlists: dict[tuple[str, str], str] = {}
            for genre in GENRES:
                folder = rb_writer.ensure_folder(handle, genre, root)
                for band in BANDS:
                    self.playlists[(genre, band)] = str(
                        rb_writer.ensure_playlist(handle, band, folder).ID
                    )
            for content_id, (genre, band, _energy) in TRACKS.items():
                rb_writer.add_memberships(
                    handle, handle.get_playlist(ID=self.playlists[(genre, band)]), [content_id]
                )
            handle.session.commit()
            root_id = str(root.ID)
        finally:
            rb_writer.close_db(handle)
        tree_registry.write(
            cfg,
            tree_registry.Registry(
                (
                    tree_registry.TreeRecord(
                        tree_id=taxonomy.default_taxonomy().tree.id,
                        mode=tree_registry.Mode.DATABASE,
                        cutover_on=date(2026, 8, 1),
                        root_id=root_id,
                        source=tree_registry.DerivationSource.TAXONOMY,
                    ),
                )
            ),
        )

    # ── one organize run ─────────────────────────────────────────────────

    def shared(self) -> account_mirror.Shared:
        self.runs += 1
        run = account_mirror.Run(run_id=f"run-{self.runs}", record=True)
        return account_mirror.Shared(self.cfg, lambda: self.account, run)

    def plan(self) -> tuple[Area, object, account_mirror.Shared]:
        shared = self.shared()
        declared = active_taxonomy.load(self.cfg)
        registry = tree_registry.read(self.cfg)
        step = mirror_edits.add_step(self.cfg, declared, registry, shared)
        area = Area(name="account")
        account_mirror.add_steps(self.cfg, area, shared.account, shared._run, shared=shared)
        return area, step, shared

    def run(self) -> tuple[Area, object]:
        """Plan both, then write the rekordbox step first and the mirror after, as organize does."""
        area, step, _shared = self.plan()
        if step.apply is not None:
            step.applied = step.apply()
        for one in area.steps:
            if one.apply is not None:
                one.applied = one.apply()
        return area, step

    # ── the account ──────────────────────────────────────────────────────

    def remote(self, title: str) -> str:
        (found,) = [pid for pid, name in self.account.titles.items() if name == title]
        return found

    def held(self, title: str) -> list[str]:
        return list(self.account.playlists[self.remote(title)])

    def take_off(self, title: str, track: str) -> None:
        self.account.playlists[self.remote(title)].remove(track)

    def put_in(self, title: str, track: str, *, at: str = "") -> None:
        self.account.playlists[self.remote(title)].append(track)
        if at:
            self.account.added_at[(self.remote(title), track)] = at

    # ── the library ──────────────────────────────────────────────────────

    def places(self, content_id: str) -> set[tuple[str, str]]:
        conn = sqlite3.connect(self.db)
        try:
            found = conn.execute(
                "SELECT PlaylistID FROM djmdSongPlaylist WHERE ContentID = ? "
                "AND COALESCE(rb_local_deleted, 0) = 0",
                (content_id,),
            ).fetchall()
        finally:
            conn.close()
        by_id = {pid: names for names, pid in self.playlists.items()}
        return {by_id[str(one[0])] for one in found if str(one[0]) in by_id}

    def genre_row(self, content_id: str) -> str:
        conn = sqlite3.connect(self.db)
        try:
            (found,) = conn.execute(
                "SELECT GenreID FROM djmdContent WHERE ID = ?", (content_id,)
            ).fetchone()
        finally:
            conn.close()
        return str(found)

    def move_in_rekordbox(self, content_id: str, to: tuple[str, str], at: str) -> None:
        """A person's move in rekordbox: out of every band, into one, at a time."""
        conn = sqlite3.connect(self.db)
        try:
            conn.execute(
                "UPDATE djmdSongPlaylist SET rb_local_deleted = 1 WHERE ContentID = ?",
                (content_id,),
            )
            conn.execute(
                "INSERT INTO djmdSongPlaylist (ID, PlaylistID, ContentID, TrackNo, "
                "rb_local_deleted, created_at, updated_at) VALUES (?, ?, ?, 1, 0, ?, ?)",
                (f"moved-{content_id}", self.playlists[to], content_id, at, at),
            )
            conn.commit()
        finally:
            conn.close()

    def forget_snapshots(self) -> None:
        path = config.state_path("outbound_writes", self.cfg)
        document = json.loads(path.read_text(encoding="utf-8"))
        for record in document["mirrors"].values():
            for entry in record["playlists"].values():
                entry.pop("agreed", None)
        path.write_text(json.dumps(document), encoding="utf-8")


@pytest.fixture(autouse=True)
def _field_policies():
    """The genre operation the write registers is the process's, so it is undone after each test."""
    yield
    rb_writer.reset_field_policies()


@pytest.fixture
def machine(acknowledged, tmp_path) -> Machine:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    built = Machine(acknowledged, scratch)
    built.run()
    return built


def _writes(account) -> tuple:
    return (list(account.created), list(account.chunks), list(account.taken))


# ═══════════════════════════════════════════════════════════════════════════
# 1. The snapshot and the first run
# ═══════════════════════════════════════════════════════════════════════════


def test_the_first_run_mirrors_one_way_and_records_every_playlists_snapshot(machine):
    assert machine.held("Deep House Low") == ["r1"]
    assert machine.held("Deep House Med") == ["r2"]
    recorded = ledger.mirror_folders(machine.cfg)
    agreed = {
        title: entry.agreed
        for folder in recorded.values()
        for title, entry in folder.playlists.items()
    }
    assert agreed["Deep House Low"] == {"r1"}
    assert agreed["Tech House Med"] == frozenset()
    assert all(value is not None for value in agreed.values())


def test_a_second_run_with_nothing_changed_plans_nothing_on_either_side(machine):
    area, step, _shared = machine.plan()
    assert step.state == NOTHING
    assert {one.state for one in area.steps} <= {NOTHING, LISTED}


def test_an_edit_on_a_playlist_never_agreed_is_put_back_and_nothing_in_the_library_changes(
    machine,
):
    machine.forget_snapshots()
    machine.take_off("Deep House Low", "r1")
    machine.put_in("Tech House Med", "r1")

    area, step = machine.run()

    assert step.state == NOTHING
    assert machine.places("1") == {("Deep House", "Low")}
    assert machine.held("Deep House Low") == ["r1"]
    assert machine.held("Tech House Med") == []
    assert tags.read_genre_from_file(machine.files["1"]) == "Deep House"


# ═══════════════════════════════════════════════════════════════════════════
# 2. A move, an unfile, carried into the library
# ═══════════════════════════════════════════════════════════════════════════


def test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing(
    machine,
):
    machine.take_off("Deep House Low", "r1")
    machine.put_in("Tech House Med", "r1")
    before = _writes(machine.account)

    area, step = machine.run()

    assert step.state == PLANNED
    (change,) = [one for one in step.items if one.get("edit")]
    assert change["genre"] == ["Deep House", "Tech House"]
    assert change["energy"] == [2, 4]
    assert change["leaves"] == ["Deep House / Low"]
    assert change["joins"] == ["Tech House / Med"]
    # THE FILE, THE ROW AND THE TREE, read back from each.
    assert tags.read_genre_from_file(machine.files["1"]) == "Tech House"
    assert tags.read_energy_from_file(machine.files["1"]) == 4
    assert machine.genre_row("1") == GENRES["Tech House"]
    assert machine.places("1") == {("Tech House", "Med")}
    # THE ACCOUNT KEPT THE EDIT: nothing written back over it.
    assert machine.held("Tech House Med") == ["r1"]
    assert machine.held("Deep House Low") == []
    assert _writes(machine.account) == before
    # AND THE NEXT RUN PLANS NOTHING ON EITHER SIDE.
    area, step, shared = machine.plan()
    assert step.state == NOTHING
    assert {one.state for one in area.steps} <= {NOTHING, LISTED}
    assert shared.reading().decided.decisions == ()


def test_a_move_in_rekordbox_after_an_edit_was_taken_is_rekordboxs(machine):
    machine.take_off("Deep House Low", "r1")
    machine.put_in("Tech House Med", "r1")
    machine.run()
    machine.move_in_rekordbox("1", ("Deep House", "Low"), "2026-11-05 10:00:00.000 +00:00")

    _area, step = machine.run()

    assert step.state == NOTHING
    assert machine.places("1") == {("Deep House", "Low")}
    assert machine.held("Deep House Low") == ["r1"]
    assert machine.held("Tech House Med") == []


def test_a_move_within_a_genre_keeps_the_genre_and_moves_the_energy_to_the_nearest(machine):
    machine.take_off("Deep House Low", "r1")
    machine.put_in("Deep House High", "r1")

    _area, step = machine.run()

    (change,) = [one for one in step.items if one.get("edit")]
    assert change["genre"] == ["Deep House", "Deep House"]
    assert change["energy"] == [2, 7]
    assert machine.places("1") == {("Deep House", "High")}
    assert machine.genre_row("1") == GENRES["Deep House"]


def test_a_move_to_unsorted_clears_the_energy(machine):
    machine.take_off("Deep House Med", "r2")
    machine.put_in("Deep House Unsorted", "r2")

    machine.run()

    assert tags.read_energy_from_file(machine.files["2"]) is None
    assert tags.read_genre_from_file(machine.files["2"]) == "Deep House"
    assert machine.places("2") == {("Deep House", "Unsorted")}


def test_a_track_removed_on_the_account_and_added_nowhere_is_unfiled_and_listed(machine):
    machine.take_off("Deep House Low", "r1")

    _area, step = machine.run()

    (change,) = [one for one in step.items if one.get("edit")]
    assert change["edit"] == edits.UNFILE and change["genre"] == ["Deep House", None]
    assert tags.read_genre_from_file(machine.files["1"]) is None
    assert tags.read_energy_from_file(machine.files["1"]) is None
    assert machine.places("1") == set()
    unplaced, totals = routing_cli.unplaced_items(machine.cfg)
    assert totals["compared"] is True
    assert "1" in {one.get("content_id") or one.get("id") for one in unplaced}
    # IT STAYS IN THE COLLECTION.
    conn = sqlite3.connect(machine.db)
    assert conn.execute("SELECT rb_local_deleted FROM djmdContent WHERE ID = '1'").fetchone() == (0,)
    conn.close()
    area, step, _shared = machine.plan()
    assert step.state == NOTHING
    assert {one.state for one in area.steps} <= {NOTHING, LISTED}


def test_the_gate_names_every_membership_the_step_takes_away(machine):
    machine.take_off("Deep House Low", "r1")
    _area, step, _shared = machine.plan()
    lines = mirror_edits.deletes(step.items)
    assert lines == [
        "a track leaves Deep House / Low, and its genre and energy tags are cleared"
    ]


# ═══════════════════════════════════════════════════════════════════════════
# 3. Held, and the most recent change
# ═══════════════════════════════════════════════════════════════════════════


def test_a_short_listing_changes_nothing_in_the_library_and_undoes_nothing(machine):
    machine.take_off("Deep House Low", "r1")
    machine.put_in("Tech House Med", "r1")
    machine.account.hidden[machine.remote("Deep House Low")] = ("r9",)
    machine.account.playlists[machine.remote("Deep House Low")].append("r9")

    area, step = machine.run()

    assert step.state == NOTHING
    assert machine.places("1") == {("Deep House", "Low")}
    assert "r1" not in machine.held("Deep House Low")
    assert machine.held("Tech House Med") == ["r1"]


def test_a_track_the_library_lacks_added_on_the_account_is_held_there(machine):
    machine.put_in("Tech House Med", "r9")

    _area, step = machine.run()

    assert step.state == NOTHING
    (named,) = step.items
    assert named["outcome"] == edits.HELD and "U204" in named["why"]
    assert machine.held("Tech House Med") == ["r9"]


def test_two_moves_follow_the_later_rekordbox_move(machine):
    machine.take_off("Deep House Low", "r1")
    machine.put_in("Tech House Med", "r1", at="2026-11-04T09:00:00+00:00")
    machine.move_in_rekordbox("1", ("Deep House", "High"), "2026-11-04 10:00:00.000 +00:00")

    _area, step = machine.run()

    assert step.state == NOTHING
    assert machine.places("1") == {("Deep House", "High")}
    assert tags.read_genre_from_file(machine.files["1"]) == "Deep House"
    assert machine.held("Deep House High") == ["r1"]
    assert machine.held("Tech House Med") == []


def test_two_moves_follow_the_later_account_move(machine):
    machine.take_off("Deep House Low", "r1")
    machine.put_in("Tech House Med", "r1", at="2026-11-04T11:00:00+00:00")
    machine.move_in_rekordbox("1", ("Deep House", "High"), "2026-11-04 10:00:00.000 +00:00")

    _area, step = machine.run()

    assert step.state == PLANNED
    assert machine.places("1") == {("Tech House", "Med")}
    assert machine.held("Tech House Med") == ["r1"]
    area, step, _shared = machine.plan()
    assert step.state == NOTHING and {one.state for one in area.steps} <= {NOTHING, LISTED}


def test_two_moves_with_the_account_time_unknown_keep_rekordboxs(machine):
    machine.take_off("Deep House Low", "r1")
    machine.put_in("Tech House Med", "r1")
    machine.move_in_rekordbox("1", ("Deep House", "High"), "2026-11-04 10:00:00.000 +00:00")

    _area, step = machine.run()

    assert step.state == NOTHING
    (named,) = step.items
    assert named["outcome"] == edits.REKORDBOX and "unknown" in named["why"]
    assert machine.places("1") == {("Deep House", "High")}


# ═══════════════════════════════════════════════════════════════════════════
# 4. The write's own guards
# ═══════════════════════════════════════════════════════════════════════════


def test_a_library_moved_since_the_plan_writes_nothing(machine):
    machine.take_off("Deep House Low", "r1")
    machine.put_in("Tech House Med", "r1")
    _area, step, _shared = machine.plan()
    conn = sqlite3.connect(machine.db)
    conn.execute(
        "INSERT INTO djmdSongPlaylist (ID, PlaylistID, ContentID, TrackNo, rb_local_deleted, "
        "created_at, updated_at) VALUES ('late', ?, '1', 2, 0, '2026-11-04', '2026-11-04')",
        (machine.playlists[("Tech House", "High")],),
    )
    conn.commit()
    conn.close()

    with pytest.raises(CratekitError) as caught:
        step.apply()

    assert caught.value.cause.reason == "decision-stale"
    assert tags.read_genre_from_file(machine.files["1"]) == "Deep House"


def test_without_the_backup_acknowledgment_the_rekordbox_area_is_not_planned(machine, monkeypatch):
    from cratekit.core.cause import refuse

    monkeypatch.setattr(
        rekordbox,
        "acknowledgment",
        lambda _cfg: refuse("backup-acknowledgment-missing", "no backup", origin=("test",)),
    )
    machine.take_off("Deep House Low", "r1")
    area = rekordbox.plan_area(
        machine.cfg,
        None,
        gate="organize.rekordbox.approve",
        today=date(2026, 11, 4),
        labels=(),
        report=False,
        only=frozenset({rekordbox.MIRROR_EDITS}),
        shared=machine.shared(),
    )
    assert area.cause is not None and area.steps == []
    assert tags.read_genre_from_file(machine.files["1"]) == "Deep House"


def test_the_step_is_a_kind_the_rekordbox_area_names_and_listed_with_no_reading(machine):
    assert rekordbox.MIRROR_EDITS in rekordbox.STEPS
    area = rekordbox.plan_area(
        machine.cfg,
        None,
        gate="organize.rekordbox.approve",
        today=date(2026, 11, 4),
        labels=(),
        report=False,
        only=frozenset({rekordbox.MIRROR_EDITS}),
    )
    (step,) = area.steps
    assert (step.key, step.state) == (mirror_edits.KIND, LISTED)


def test_an_account_that_cannot_be_read_refuses_the_step_alone(machine):
    from cratekit.core.cause import refuse

    def unreachable():
        raise refuse("credential-missing", "no account", origin=("test",))

    shared = account_mirror.Shared(machine.cfg, unreachable, None)
    step = mirror_edits.add_step(
        machine.cfg, active_taxonomy.load(machine.cfg), tree_registry.read(machine.cfg), shared
    )
    assert step.state == REFUSED and step.cause.reason == "credential-missing"


# ═══════════════════════════════════════════════════════════════════════════
# 5. The tags routing reads, chosen by routing
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "folder, playlist, genre, energy, expected",
    [
        ("Tech House", "Med", "Deep House", 2, ("Tech House", 4)),
        ("Deep House", "Med", "Deep House", 5, ("Deep House", 5)),
        ("Deep House", "High", "Deep House", None, ("Deep House", 7)),
        ("Deep House", "Unsorted", "Deep House", 5, ("Deep House", None)),
        ("Tech House", None, "Deep House", 5, ("Tech House", 5)),
        ("No Such Genre", "Low", "Deep House", 5, None),
        ("Minimal / Deep Tech", "Low Energy", "Deep House", 9, ("Minimal / Deep Tech", 3)),
    ],
)
def test_the_tags_are_the_nearest_pair_routing_files_into_the_place(
    folder, playlist, genre, energy, expected
):
    declared = taxonomy.default_taxonomy()
    assert mirror_edits.target_tags(declared, folder, playlist, genre, energy) == expected


def test_a_genre_folder_places_only_what_routing_files_into():
    declared = taxonomy.default_taxonomy()
    folder = mirror.Folder(
        name="Deep House",
        playlists=tuple(
            mirror.Source(name=f"Deep House {one}")
            for one in ("Low", "Unsorted", "with vox", "Favorites", "Candy")
        ),
        genre=True,
    )
    found = mirror_edits.places(declared, [folder, mirror.Folder(name="Not A Genre", genre=True)])
    assert {title: place.primary for title, place in found.items()} == {
        "Deep House Low": True,
        "Deep House Unsorted": True,
        "Deep House with vox": False,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 6. Favorites and INBOX keep their one way mirror until U204
# ═══════════════════════════════════════════════════════════════════════════


def test_a_folder_that_is_not_a_genre_folder_is_mirrored_one_way(installed, monkeypatch):
    account = outbound_fakes.StrictAccount(catalog={"c1": "r1"})
    favorites = mirror.Folder(
        name="Favorites",
        playlists=(
            mirror.Source(name="All Favorites", rows=(mirror.Row(content_id="c1", isrc="ISRC00001"),)),
        ),
    )
    monkeypatch.setattr(
        account_mirror, "read_library", lambda _cfg: account_mirror.Library(folders=(favorites,))
    )

    def run() -> None:
        area = Area(name="account")
        account_mirror.add_steps(
            installed, area, lambda: account, account_mirror.Run(run_id="r", record=True)
        )
        for one in area.steps:
            if one.apply is not None:
                one.apply()

    run()
    (pid,) = [one for one, name in account.titles.items() if name == "All Favorites"]
    assert ledger.mirror_folders(installed)["Favorites"].playlists["All Favorites"].agreed == {"r1"}
    account.playlists[pid].remove("r1")
    run()
    assert account.playlists[pid] == ["r1"]



# ═══════════════════════════════════════════════════════════════════════════
# 7. The account's dated listing, and the snapshot's record
# ═══════════════════════════════════════════════════════════════════════════


def _dated_adapter(cfg, members, *, hidden=0, declared=True, times=None):
    from datetime import datetime

    from cratekit.modules.outbound import tidal_account
    from tests import test_prune

    store = test_prune._Store()
    store.members["p"] = list(members)
    store.hidden["p"] = hidden
    stamped = dict(times or {})

    class Track(test_prune._Track):
        def __init__(self, track_id: str) -> None:
            super().__init__(track_id)
            at = stamped.get(track_id)
            self.user_date_added = datetime.fromisoformat(at) if at else None

    class Playlist(test_prune._Playlist):
        def __init__(self, store, playlist_id) -> None:
            super().__init__(store, playlist_id)
            if not declared:
                self.num_tracks = None

        def tracks(self, limit=None, offset=0):
            size = 100 if limit is None else limit
            return [Track(one) for one in self.store.members[self.id][offset : offset + size]]

    class Client(test_prune._Client):
        def playlist(self, playlist_id):
            self.store.opened.append(playlist_id)
            return Playlist(self.store, playlist_id)

    return tidal_account.TidalAccount(Client(store), sleep=lambda seconds: None, cfg=cfg)


def test_the_adapter_lists_each_track_with_its_added_time_and_the_declared_count(installed):
    listing = _dated_adapter(
        installed,
        ["a", "b", "a"],
        times={"a": "2026-11-04T10:00:00+00:00", "b": "2026-11-04T11:00:00"},
    ).playlist_listing("p")
    assert listing.names == {"a": ("Artist a", "Title a"), "b": ("Artist b", "Title b")}
    # A TIME WITH NO ZONE IS UNKNOWN, never guessed.
    assert listing.added == {"a": "2026-11-04T10:00:00+00:00"}
    assert (listing.listed, listing.declared, listing.short) == (3, 3, False)


def test_a_listing_the_provider_counts_more_than_it_lists_is_short(installed):
    listing = _dated_adapter(installed, ["a"], hidden=1).playlist_listing("p")
    assert (listing.listed, listing.declared, listing.short) == (1, 2, True)


def test_a_listing_with_no_declared_count_is_short(installed):
    listing = _dated_adapter(installed, ["a"], declared=False).playlist_listing("p")
    assert listing.declared is None and listing.short


def test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist(installed):
    ledger.reserve_mirror_folder(installed, "Deep House", lambda: "f1")
    ledger.reserve_mirror_playlist(installed, "Deep House", "Deep House Low", lambda: "p1")
    ledger.reserve_mirror_playlist(installed, "Deep House", "Deep House Med", lambda: "p2")
    assert ledger.mirror_folders(installed)["Deep House"].playlists["Deep House Low"].agreed is None

    ledger.record_mirror_agreed(
        installed,
        "Deep House",
        {
            "Deep House Low": ("p1", {"r1", "r2"}, set()),
            "Deep House Med": ("another", {"r3"}, set()),
        },
    )
    held = ledger.mirror_folders(installed)["Deep House"].playlists
    assert held["Deep House Low"].agreed == {"r1", "r2"}
    assert held["Deep House Med"].agreed is None

    # A HELD TRACK KEEPS THE WORD THE RECORD HOLDS NOW, settled or not.
    ledger.settle_mirror_tracks(installed, [("Deep House", "Deep House Low", "r9", True)])
    ledger.record_mirror_agreed(installed, "Deep House", {"Deep House Low": ("p1", {"r1"}, {"r9", "r2"})})
    assert ledger.mirror_folders(installed)["Deep House"].playlists["Deep House Low"].agreed == {
        "r1",
        "r2",
        "r9",
    }
    ledger.record_mirror_agreed(installed, "Deep House", {"Deep House Low": ("p1", set(), set())})
    assert ledger.mirror_folders(installed)["Deep House"].playlists["Deep House Low"].agreed == frozenset()
