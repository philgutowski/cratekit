"""U119: every genre folder has a Favorites playlist that mirrors All Favorites.

Driven against a disposable database with a routing tree cut over, built the
way the rebuild suite builds one, with genre folders, band playlists and the
one source playlist made on the handle. The engine is driven directly for the
plan and the two commits, and the verb through the command line for its gate,
its acknowledgment and its refusals.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import sqlite3
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from cratekit.adopt import apply_cli
from cratekit.core import active_taxonomy, convergence, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.favorites import refresh_cli
from cratekit.write import genre_favorites, rebuild, trees
from tests.cli_drive import drive
from tests.test_rb_writer_db import _build_disposable_database
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414

DECLARED = taxonomy.default_taxonomy()
TREE = DECLARED.tree.id
FAVORITES = DECLARED.sub_class("favorites")
SOURCE = FAVORITES.signal_playlist
#: Three genre folders of the shipped template, by their display names.
DEEP = DECLARED.bucket("deep_house")
AFRO = DECLARED.bucket("afro_house")
OTHER = DECLARED.bucket("electronica_other")
VERB = ["favorites", "refresh"]
APPROVE = refresh_cli.APPROVE_GATE
ROWS = ("1", "2", "3", "4", "5", "6")


# ---------------------------------------------------------------------------
# Fixtures: a tree cut over, folders and playlists made on the handle
# ---------------------------------------------------------------------------


@pytest.fixture
def db(cfg, monkeypatch):
    """A disposable database holding six content rows, opened through the gate."""
    path = Path(cfg.library.db_path)
    _build_disposable_database(path)
    conn = sqlite3.connect(path)
    try:
        for content_id in ROWS:
            conn.execute(
                "INSERT OR IGNORE INTO djmdContent (ID, Title, rb_local_deleted, created_at, "
                "updated_at) VALUES (?, ?, 0, '2026-01-01', '2026-01-01')",
                (content_id, f"track {content_id}"),
            )
            conn.execute(
                "UPDATE djmdContent SET FolderPath = ?, rb_local_deleted = 0 WHERE ID = ?",
                (f"{cfg.library.root}/Music/track {content_id}.flac", content_id),
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
    handle = rb_writer.open_db(path, unlock=False, cfg=cfg)
    try:
        yield handle
    finally:
        rb_writer.close_db(handle)


class Tree:
    """The routing tree on the handle: its root, its folders and its playlists."""

    def __init__(self, cfg, db) -> None:
        self.cfg = cfg
        self.db = db
        self.root = rb_writer.ensure_folder(db, DECLARED.tree.display)
        db.session.commit()
        self.registry = tree_registry.Registry(
            (
                tree_registry.TreeRecord(
                    tree_id=TREE,
                    mode=tree_registry.Mode.DATABASE,
                    cutover_on=date(2026, 10, 9),
                    root_id=str(self.root.ID),
                    source=tree_registry.DerivationSource.TAXONOMY,
                ),
            )
        )
        tree_registry.write(cfg, self.registry)
        self.folders: dict[str, object] = {}

    def folder(self, bucket: taxonomy.Bucket):
        if bucket.id not in self.folders:
            self.folders[bucket.id] = self.db.create_playlist_folder(bucket.display, parent=self.root)
            self.db.session.commit()
        return self.folders[bucket.id]

    def playlist(self, bucket: taxonomy.Bucket, name: str, *members: str, parent=None):
        row = self.db.create_playlist(name, parent=parent if parent is not None else self.folder(bucket))
        for content_id in members:
            self.db.add_to_playlist(row, content_id)
        self.db.session.commit()
        return row

    def source(self, *members: str):
        folder = self.db.create_playlist_folder("Favorites")
        row = self.db.create_playlist(SOURCE, parent=folder)
        for content_id in members:
            self.db.add_to_playlist(row, content_id)
        self.db.session.commit()
        return row


def _members(db, playlist_id: str) -> set[str]:
    return {
        str(row.ContentID)
        for row in db.get_playlist_songs(PlaylistID=str(playlist_id))
        if not rb_writer.membership_removed(row)
    }


def _favorites_of(db, tree: Tree, bucket: taxonomy.Bucket):
    folder = tree.folder(bucket)
    rows = [
        row
        for row in db.get_playlist(Name=FAVORITES.display)
        if str(row.ParentID) == str(folder.ID) and not rb_writer.node_removed(row)
    ]
    assert len(rows) <= 1, "two live Favorites under one folder"
    return rows[0] if rows else None


def _plan(cfg, db, tree: Tree, declared=DECLARED):
    return genre_favorites.plan_refresh(cfg, db, declared, tree.registry)


def _apply(cfg, db, tree: Tree, plan, *, remove=True, declared=DECLARED):
    return genre_favorites.apply_refresh(
        cfg,
        db,
        plan,
        declared=declared,
        registry=tree.registry,
        analysis_roots=[Path(cfg.library.root)],
        remove=remove,
    )


def _refresh(cfg, db, tree: Tree, *, remove=True):
    return _apply(cfg, db, tree, _plan(cfg, db, tree), remove=remove)


def _content_table(cfg) -> list[tuple]:
    conn = sqlite3.connect(cfg.library.db_path)
    try:
        return conn.execute("SELECT * FROM djmdContent ORDER BY ID").fetchall()
    finally:
        conn.close()


def _unmember(db, playlist, content_id: str) -> None:
    rb_writer.remove_memberships(db, playlist, [content_id])
    db.session.commit()


def _two_acts(verb: list[str]) -> tuple[int, dict, dict]:
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    detail = refused["cause"]["detail"]
    assert detail["gate"] == APPROVE and detail["explicit"] is True
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, APPROVE, "approve", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    code, acted = drive(["--run", run_id, *verb])
    return code, acted, refused


# ---------------------------------------------------------------------------
# The engine: what each folder's Favorites comes to hold
# ---------------------------------------------------------------------------


def test_a_vocal_favourite_is_in_its_band_with_vox_and_favorites_under_one_genre(
    cfg, gates_pass, db
):
    """AE1. Favorites and "with vox" are independent memberships."""
    tree = Tree(cfg, db)
    med = tree.playlist(DEEP, "Med", "1", "2")
    vox = tree.playlist(DEEP, DECLARED.sub_class("with_vox").display, "1")
    tree.source("1")

    plan = _plan(cfg, db, tree)
    (folder,) = plan.folders
    assert folder.bucket == DEEP.id and folder.members == ("1", "2")
    assert folder.wanted == ("1",) and folder.adds == ("1",) and folder.removes == ()
    assert plan.creates == 1

    refreshed = _refresh(cfg, db, tree)

    assert (refreshed.added, refreshed.removed, refreshed.created) == (1, 0, (DEEP.display,))
    favorites = _favorites_of(db, tree, DEEP)
    assert favorites is not None and _members(db, favorites.ID) == {"1"}
    assert _members(db, med.ID) == {"1", "2"} and _members(db, vox.ID) == {"1"}
    assert refreshed.disagreements == ()
    # The node is recorded under the class's own id, so the rebuild and the
    # check resolve this Favorites through it after a rename.
    recorded = convergence.read(cfg).tree(TREE)
    assert recorded is not None
    node = recorded.node(DEEP.id, FAVORITES.id)
    assert node is not None and node.playlist_id == str(favorites.ID)


def test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band(
    cfg, gates_pass, db
):
    """AE2."""
    tree = Tree(cfg, db)
    high = tree.playlist(AFRO, "High", "3", "4")
    source = tree.source("3", "4")
    _refresh(cfg, db, tree)
    assert _members(db, _favorites_of(db, tree, AFRO).ID) == {"3", "4"}

    _unmember(db, source, "3")
    refreshed = _refresh(cfg, db, tree)

    assert (refreshed.added, refreshed.removed) == (0, 1)
    assert _members(db, _favorites_of(db, tree, AFRO).ID) == {"4"}
    assert _members(db, high.ID) == {"3", "4"}


def test_a_favourite_with_no_genre_lands_only_in_the_folder_it_already_sits_in(
    cfg, gates_pass, db
):
    """AE3. By the folder, never by re-reading the tag."""
    tree = Tree(cfg, db)
    tree.playlist(OTHER, "Low", "5")
    tree.playlist(DEEP, "Med", "1")
    tree.source("5", "1")

    refreshed = _refresh(cfg, db, tree)

    assert refreshed.added == 2
    assert _members(db, _favorites_of(db, tree, OTHER).ID) == {"5"}
    assert _members(db, _favorites_of(db, tree, DEEP).ID) == {"1"}


def test_a_favourite_in_two_folders_is_in_both_folders_favorites(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "2")
    tree.playlist(AFRO, "High", "2")
    tree.source("2")

    _refresh(cfg, db, tree)

    assert _members(db, _favorites_of(db, tree, DEEP).ID) == {"2"}
    assert _members(db, _favorites_of(db, tree, AFRO).ID) == {"2"}


def test_a_hand_added_track_not_in_all_favorites_is_removed_at_the_refresh(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1", "2")
    tree.playlist(DEEP, FAVORITES.display, "2")
    tree.source("1")

    plan = _plan(cfg, db, tree)
    (folder,) = plan.folders
    assert folder.present == ("2",) and folder.adds == ("1",) and folder.removes == ("2",)

    refreshed = _refresh(cfg, db, tree)

    assert (refreshed.added, refreshed.removed, refreshed.created) == (1, 1, ())
    assert _members(db, _favorites_of(db, tree, DEEP).ID) == {"1"}


def test_the_additive_half_adds_and_counts_what_it_leaves_owed(cfg, gates_pass, db):
    """What the end of an adoption runs: nothing taken out, the removals counted."""
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1", "2")
    tree.playlist(DEEP, FAVORITES.display, "2")
    tree.source("1")

    refreshed = _refresh(cfg, db, tree, remove=False)

    assert (refreshed.added, refreshed.removed, refreshed.removals_owed) == (1, 0, 1)
    assert _members(db, _favorites_of(db, tree, DEEP).ID) == {"1", "2"}
    assert refreshed.disagreements == ()


def test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply(
    cfg, gates_pass, db
):
    """The lesson of R-788: a plan whose apply changes what it reads digests what stays put."""
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1", "2")
    tree.playlist(DEEP, FAVORITES.display, "2")
    tree.source("1")
    before = _plan(cfg, db, tree)
    _apply(cfg, db, tree, before, remove=False)
    after = _plan(cfg, db, tree)
    assert after.digest == before.digest
    assert after.adds == 0 and after.removes == 1
    # And it moves when the target moves.
    source = next(row for row in db.get_playlist(Name=SOURCE) if not rb_writer.is_folder(row))
    db.add_to_playlist(source, "2")
    db.session.commit()
    assert _plan(cfg, db, tree).digest != before.digest


def test_a_plan_that_moved_between_the_approval_and_the_write_is_refused(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1", "2")
    source = tree.source("1")
    plan = _plan(cfg, db, tree)
    db.add_to_playlist(source, "2")
    db.session.commit()
    with pytest.raises(CratekitError) as caught:
        _apply(cfg, db, tree, plan)
    assert caught.value.cause.reason == "decision-stale"
    assert _favorites_of(db, tree, DEEP) is None


def test_a_library_with_no_source_playlist_refuses_by_name_and_empties_nothing(
    cfg, gates_pass, db
):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1")
    kept = tree.playlist(DEEP, FAVORITES.display, "1")
    with pytest.raises(CratekitError) as caught:
        _plan(cfg, db, tree)
    assert caught.value.cause.reason == genre_favorites.SOURCE_MISSING
    assert _members(db, kept.ID) == {"1"}


def test_two_source_playlists_are_refused_rather_than_one_chosen(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1")
    tree.source("1")
    db.create_playlist(SOURCE)
    db.session.commit()
    with pytest.raises(CratekitError) as caught:
        _plan(cfg, db, tree)
    assert caught.value.cause.reason == genre_favorites.SOURCE_MISSING
    assert caught.value.cause.detail["count"] == 2


def test_a_folder_of_the_source_name_is_not_the_source(cfg, gates_pass, db):
    """The live library's Favorites is a FOLDER; its child All Favorites is the playlist."""
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1")
    db.create_playlist_folder(SOURCE)
    db.session.commit()
    with pytest.raises(CratekitError) as caught:
        _plan(cfg, db, tree)
    assert caught.value.cause.reason == genre_favorites.SOURCE_MISSING


def test_a_taxonomy_declaring_no_playlist_class_refuses_by_name(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1")
    tree.source("1")
    trimmed = replace(DECLARED, sub_classes=tuple(c for c in DECLARED.sub_classes if c.id != "favorites"))
    with pytest.raises(CratekitError) as caught:
        _plan(cfg, db, tree, declared=trimmed)
    assert caught.value.cause.reason == genre_favorites.CLASS_UNDECLARED
    assert genre_favorites.favorites_class(trimmed) is None


def test_a_folder_nobody_declares_and_a_name_two_folders_carry_are_left_alone(
    cfg, gates_pass, db
):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1")
    own = db.create_playlist_folder("My Crate", parent=tree.root)
    db.session.commit()
    tree.playlist(DEEP, "Med", "2", parent=own)
    twin_a = db.create_playlist_folder(AFRO.display, parent=tree.root)
    twin_b = db.create_playlist_folder(AFRO.display, parent=tree.root)
    db.session.commit()
    db.add_to_playlist(db.create_playlist("High", parent=twin_a), "3")
    db.add_to_playlist(db.create_playlist("High", parent=twin_b), "4")
    db.session.commit()
    tree.source("1", "2", "3", "4")

    plan = _plan(cfg, db, tree)

    assert [folder.bucket for folder in plan.folders] == [DEEP.id]
    assert len(plan.unclaimed) == 3
    assert any("My Crate" in name for name in plan.unclaimed)
    refreshed = _apply(cfg, db, tree, plan)
    assert refreshed.added == 1
    assert [row for row in db.get_playlist(Name=FAVORITES.display)
            if str(row.ParentID) in {str(own.ID), str(twin_a.ID), str(twin_b.ID)}] == []


def test_a_renamed_folder_is_still_its_buckets_through_the_recorded_node(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1", "2")
    tree.source("1", "2")
    _refresh(cfg, db, tree)
    folder = tree.folder(DEEP)
    folder.Name = "Deep Cuts!"
    db.session.commit()

    plan = _plan(cfg, db, tree)

    (planned,) = plan.folders
    assert planned.bucket == DEEP.id and planned.folder_display == "Deep Cuts!"
    assert planned.present == ("1", "2") and planned.adds == ()


def test_a_second_refresh_adds_and_removes_nothing(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1", "2")
    tree.source("1")
    _refresh(cfg, db, tree)
    plan = _plan(cfg, db, tree)
    assert not plan.writes
    refreshed = _apply(cfg, db, tree, plan)
    assert (refreshed.added, refreshed.removed) == (0, 0)


def test_no_content_row_tempo_or_rating_is_written(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1", "2")
    tree.playlist(DEEP, FAVORITES.display, "2")
    tree.source("1")
    before = _content_table(cfg)
    _refresh(cfg, db, tree)
    assert _content_table(cfg) == before


# ---------------------------------------------------------------------------
# The rebuild and the convergence check count Favorites as declared membership
# ---------------------------------------------------------------------------


def _rows(cfg) -> list[trees.ContentRow]:
    return [
        trees.ContentRow(content_id, f"{cfg.library.root}/Music/track {content_id}.flac", deleted=False)
        for content_id in ROWS
    ]


def test_the_favourites_become_declared_placements_and_a_missing_source_a_gap(
    cfg, gates_pass, db
):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1", "2")
    placed, gaps = genre_favorites.placements(cfg, db, DECLARED, tree.registry, _rows(cfg))
    assert placed == () and gaps == (genre_favorites.FAVORITES_DIMENSION,)

    tree.source("1")
    placed, gaps = genre_favorites.placements(cfg, db, DECLARED, tree.registry, _rows(cfg))
    assert gaps == ()
    assert [(p.bucket, p.sub, Path(p.location).name) for p in placed] == [
        (DEEP.id, FAVORITES.id, "track 1.flac")
    ]


def test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign(
    cfg, gates_pass, db
):
    """The dimension is declared to the check: a favourite the folder lacks is
    missing, a Favorites member that is no favourite is unexpected, and neither
    is somebody's own playlist."""
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1", "2")
    tree.playlist(DEEP, FAVORITES.display, "2")
    tree.source("1")
    placed, gaps = genre_favorites.placements(cfg, db, DECLARED, tree.registry, _rows(cfg))
    report = rebuild.check(
        cfg,
        db,
        tree_id=TREE,
        registry=tree.registry,
        declared=DECLARED,
        placements=placed,
        rows=_rows(cfg),
        root_exists=lambda _root: True,
        not_compared=gaps,
    )
    missing = {(d.bucket, d.sub, d.content_id) for d in report.missing}
    unexpected = {(d.bucket, d.sub, d.content_id) for d in report.unexpected}
    assert (DEEP.id, FAVORITES.id, "1") in missing
    assert (DEEP.id, FAVORITES.id, "2") in unexpected
    assert not any(FAVORITES.display in name for name in report.foreign)


def test_with_favorites_leaves_another_tree_and_an_undeclared_class_alone(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    placements, gaps = rebuild.with_favorites(
        cfg, db, DECLARED, tree.registry, _rows(cfg), (), ("vocal",), tree_id="another_tree"
    )
    assert placements == () and gaps == ("vocal",)
    trimmed = replace(DECLARED, sub_classes=tuple(c for c in DECLARED.sub_classes if c.id != "favorites"))
    placements, gaps = rebuild.with_favorites(
        cfg, db, trimmed, tree.registry, _rows(cfg), (), (), tree_id=TREE
    )
    assert placements == () and gaps == ()


# ---------------------------------------------------------------------------
# The end of an adoption
# ---------------------------------------------------------------------------


def test_the_additive_refresh_at_an_adoptions_end_skips_what_it_cannot_read_and_says_why(
    cfg, gates_pass, db
):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1")
    roots = [Path(cfg.library.root)]
    rb_writer.close_db(db)
    outcome = genre_favorites.refresh_additive(cfg, DECLARED, analysis_roots=roots)
    assert outcome.refreshed is None and "no live playlist" in outcome.skipped

    trimmed = replace(DECLARED, sub_classes=tuple(c for c in DECLARED.sub_classes if c.id != "favorites"))
    outcome = genre_favorites.refresh_additive(cfg, trimmed, analysis_roots=roots)
    assert outcome.refreshed is None and "declares no sub class" in outcome.skipped

    on_the_bridge = tree_registry.Registry()
    tree_registry.write(cfg, on_the_bridge)
    outcome = genre_favorites.refresh_additive(cfg, DECLARED, analysis_roots=roots)
    assert outcome.refreshed is None and outcome.skipped
    tree_registry.write(cfg, tree.registry)


def test_the_resume_carries_the_removals_owed_as_a_note():
    summary = {"favorites": {"added": 2, "removals_owed": 3, "created": [], "skipped": ""}}
    (note,) = apply_cli.favorites_warnings(summary)
    assert note["code"] == apply_cli.FAVORITES_REMOVALS_OWED and "3 track(s)" in note["message"]
    assert apply_cli.favorites_warnings({"favorites": {"removals_owed": 0}}) == []
    assert apply_cli.favorites_warnings({}) == []


# ---------------------------------------------------------------------------
# The verb
# ---------------------------------------------------------------------------


def _closed(db) -> None:
    """The verb opens handles of its own, so the fixture's is closed first."""
    rb_writer.close_db(db)


def test_the_verb_asks_its_explicit_gate_then_adds_and_removes_and_reads_back(
    cfg, gates_pass, db
):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1", "2")
    tree.playlist(DEEP, FAVORITES.display, "2")
    tree.playlist(AFRO, "High", "3")
    tree.source("1", "3")
    _closed(db)

    code, acted, refused = _two_acts(VERB)

    assert code == int(ExitCode.OK), acted
    shown = refused["cause"]["detail"]["shown"]
    assert shown["adds"] == 2 and shown["removes"] == 1 and shown["playlists to create"] == 1
    assert shown["digest"] == acted["data"]["digest"]
    totals = acted["data"]["totals"]
    assert (totals["added"], totals["removed"], totals["created"]) == (2, 1, 1)
    assert [w["code"] for w in acted["warnings"]] == [refresh_cli.REFRESHED]
    (record,) = [r for r in session.records(cfg) if r.workflow == genre_favorites.WORKFLOW]
    assert record.state is session.SessionState.CLOSED
    assert {c.tree: (c.created, c.updated) for c in record.change.trees} == {TREE: (2, 1)}


def test_the_verb_over_a_mirror_already_true_asks_and_then_writes_nothing(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1")
    tree.playlist(DEEP, FAVORITES.display, "1")
    tree.source("1")
    _closed(db)
    code, acted, _ = _two_acts(VERB)
    assert code == int(ExitCode.OK) and acted["outcome"] == "no_op", acted
    assert [w["code"] for w in acted["warnings"]] == [refresh_cli.NOTHING_TO_REFRESH]


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1")
    tree.source("1")
    _closed(db)
    session.ack_path(cfg).unlink()
    code, refused = drive(VERB)
    assert code == int(ExitCode.ACK_REQUIRED), refused
    assert "gate" not in (refused.get("cause") or {}).get("detail", {})


def test_a_tree_on_the_bridge_is_refused_before_the_gate(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.source("1")
    tree_registry.write(cfg, tree_registry.Registry())
    _closed(db)
    code, refused = drive(VERB)
    assert code != int(ExitCode.DECISION_REQUIRED), refused
    assert refused["cause"]["reason"] == "tree-unconverged"


def test_a_source_that_went_between_the_two_acts_is_refused_by_the_gate(cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1", "2")
    source_id = str(tree.source("1").ID)
    _closed(db)
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, _ = drive(["run", "decide", run_id, APPROVE, "approve", "--actor", "a-person"])
    assert decided == int(ExitCode.OK)
    handle = rb_writer.open_db(Path(cfg.library.db_path), unlock=False, cfg=cfg)
    try:
        handle.add_to_playlist(handle.get_playlist(ID=source_id), "2")
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    code, acted = drive(["--run", run_id, *VERB])
    assert acted["cause"]["reason"] == "decision-stale", acted


def test_the_verb_refuses_an_undeclared_class_by_name(cfg, gates_pass, db, monkeypatch):
    tree = Tree(cfg, db)
    tree.source("1")
    _closed(db)
    trimmed = replace(DECLARED, sub_classes=tuple(c for c in DECLARED.sub_classes if c.id != "favorites"))
    monkeypatch.setattr(active_taxonomy, "load", lambda _cfg: trimmed)
    code, refused = drive(VERB)
    assert refused["cause"]["reason"] == genre_favorites.CLASS_UNDECLARED, refused
    assert code != int(ExitCode.DECISION_REQUIRED)
