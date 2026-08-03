"""U36: the tree rebuild, the convergence check, and the record between them.

WHAT THIS UNIT IS. A tree that has cut over lives only in the database. If
anything puts that database back to an earlier state, the tree is short and
nothing notices: the export it used to be written from is gone, and an
incremental sync's scope is a watermark plus deduplication against what is
already owned, so the files the old database no longer places are still on disk
and still read as owned. This file covers the three joints: noticing, reporting,
and repairing.

THE FIVE SCENARIOS THE PLAN NAMES, and where each is proved:

1. a tree with membership deliberately removed is rebuilt to match a
   never-damaged control exactly
   -> ``test_a_tree_stripped_of_its_membership_rebuilds_to_match_the_control``
2. a rebuild run twice changes nothing on the second pass
   -> ``test_a_second_rebuild_writes_nothing``
3. the check reports a difference in BOTH directions
   -> ``test_the_check_reports_a_difference_in_both_directions``
4. an unconverged flag cannot be cleared while a difference stands
   -> ``test_a_flag_cannot_be_cleared_while_the_check_still_differs``
5. a rebuild refuses without the acknowledgment and without the lock
   -> ``test_a_rebuild_refuses_without_the_acknowledgment``
   and ``test_a_rebuild_refuses_while_the_lock_is_held_elsewhere``

WHAT IS SUPPLEMENTED, because those five leave the sharpest shapes uncovered.
The rename, which is the one that doubles a library rather than merely failing:
the previous unit's re-run refused rather than converging precisely because
nothing persisted which node a destination meant, and the whole point of this
unit's record is that a rebuild after a rename writes into the tree the library
has. The reader, which must be able to tell a wrong document from an empty one,
because reading a damaged record as "nothing is unconverged" is the one
misreading that admits every write it exists to refuse. The lock, because a
read-modify-write over a JSON document is not made atomic by an atomic rename.
And the latch, which must not condemn its own remedy.

D1 APPLIES TO EVERY NAME HERE. Nothing below names a real volume, a real person,
or a real track.
"""

from __future__ import annotations

import json
import os
import sqlite3
import unicodedata
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from cratekit.cli import converge as converge_cli
from cratekit.cli import registry
from cratekit.core import (
    config,
    convergence,
    preflight,
    rb_writer,
    routing,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import REASONS, CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.write import rebuild, routing_pass, trees
from tests._pending import requires
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database

# ── synthesized names (D1) ───────────────────────────────────────────────────

TREE_ID = "shelf_stack"
TREE_DISPLAY = "Shelf & Stack"
ADOPTED_ROOT = "root-row-7788"

#: One file name in each composition form, because that pair is what the shared
#: identity primitives exist for and a check that normalized only one side would
#: report a track missing that is sitting right there.
COMPOSED = "Café One.flac"
DECOMPOSED = unicodedata.normalize("NFD", COMPOSED)
PLAIN = "Second Track.flac"

#: A folder name a person might rename a bucket folder to. It carries a space
#: and an exclamation mark, which is the character coverage the locate needs.
RENAMED_FOLDER = "Loud! Room"

#: A playlist nobody declared, sitting under the governed root. Its contents must
#: never be reported as a difference: a guard that fires on somebody's own
#: playlist is a guard people learn to route around (P7).
CURATED_PLAYLIST = "Quiet? Corner"


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library, monkeypatch):
    """Configuration with the application pin RECORDED, since an unset one refuses."""
    resolved = config.from_dict(
        valid_data(
            library,
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
        )
    )
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    monkeypatch.setattr(
        rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION
    )
    return resolved


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """Everything about THIS machine a temporary library cannot speak for.

    The same four seams the sibling write suites patch, for the same reason: that
    these guards refuse is proved directly in ``tests/test_rb_writer_db.py``, and
    re-proving it here would only prove the fixture.
    """
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )


@pytest.fixture(autouse=True)
def _release_process_locks():
    """No test may leave this process believing it still holds a session lock."""
    yield
    session._HELD.clear()


@pytest.fixture
def gates_pass(cfg, monkeypatch):
    """The volume identity agrees and the acknowledgment is recorded."""
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: cfg.library.volume_id),
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    session.record_acknowledgment(cfg, terminal=lambda: True)
    return cfg


@pytest.fixture
def declared():
    return taxonomy.default_taxonomy()


def _music(cfg, name: str) -> str:
    return f"{cfg.library.root}/Music/{name}"


def _record_locations(db_path: Path, recorded: dict[str, str]) -> None:
    """Give the disposable database's rows the paths this run decided on.

    Written straight into the file BEFORE the guarded writer opens it, because
    creating a collection row is exactly what the additive whitelist forbids:
    intake makes those rows and this unit only ever places rows that exist.
    """
    conn = sqlite3.connect(db_path)
    try:
        for content_id, path in recorded.items():
            conn.execute(
                "UPDATE djmdContent SET FolderPath = ?, rb_local_deleted = 0 WHERE ID = ?",
                (path, content_id),
            )
        conn.commit()
    finally:
        conn.close()


@pytest.fixture
def db(cfg, monkeypatch):
    """A disposable database in a temporary directory, opened through the gate."""
    path = Path(cfg.library.db_path)
    _build_disposable_database(path)
    _record_locations(path, {"1": _music(cfg, COMPOSED), "2": _music(cfg, PLAIN)})
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


@pytest.fixture
def adopted_root(db):
    """The tree folder a cutover adopted, as a REAL row with a real identifier."""
    folder = rb_writer.ensure_folder(db, TREE_DISPLAY)
    db.session.commit()
    return folder


def _registry(root_id: str, *, source=tree_registry.DerivationSource.TAXONOMY):
    return tree_registry.Registry(
        (
            tree_registry.TreeRecord(
                tree_id=TREE_ID,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=date(2026, 8, 1),
                root_id=root_id,
                source=source,
            ),
        )
    )


def _destination(declared_taxonomy):
    """Where the declared rules actually put an untagged, top-energy file.

    DERIVED by asking the rules rather than by naming a bucket, because a test
    that spells a bucket identifier is a test somebody has to edit when the
    shipped default changes, and R19 puts that name in configuration precisely so
    nothing spells it. Asking the rules is also what makes this agree with the
    rebuild by construction: both go through one resolver.
    """
    bucket_id = routing.resolve_bucket(declared_taxonomy, None).bucket_id
    sub = routing.energy_sub(
        declared_taxonomy, bucket_id, declared_taxonomy.energy.scale_max
    )
    assert sub is not None, "the shipped template declares no sub for the fallback"
    return bucket_id, sub.id


def _truth(cfg, declared_taxonomy, *names, voxlevel=None):
    """The tag readings for files the rules route to one destination.

    Readings rather than placements, because the rebuild derives its own
    placements from the source the registry records and will not take a list.
    Supplying the readings is the seam; supplying the destinations would be
    supplying the answer.
    """
    return [
        rebuild.Truth(
            location=_music(cfg, name),
            genre=None,
            energy=declared_taxonomy.energy.scale_max,
            voxlevel=voxlevel,
        )
        for name in names
    ]


def _placements(cfg, declared_taxonomy, *names):
    bucket_id, sub_id = _destination(declared_taxonomy)
    return [
        rebuild.DeclaredPlacement(_music(cfg, name), bucket_id, sub_id)
        for name in names
    ]


def _rows(cfg):
    return [
        trees.ContentRow("1", _music(cfg, COMPOSED), deleted=False),
        trees.ContentRow("2", _music(cfg, PLAIN), deleted=False),
    ]


def _rebuild(cfg, db, adopted, declared_taxonomy, names, **kwargs):
    return rebuild.rebuild_tree(
        cfg,
        db,
        tree_id=TREE_ID,
        registry=kwargs.pop("registry", _registry(str(adopted.ID))),
        declared=declared_taxonomy,
        truth=kwargs.pop("truth", _truth(cfg, declared_taxonomy, *names)),
        vocal_threshold=kwargs.pop("vocal_threshold", None),
        rows=kwargs.pop("rows", _rows(cfg)),
        root_exists=lambda _root: True,
        analysis_roots=[Path(cfg.library.root) / "Music"],
        **kwargs,
    )


def _check(cfg, db, adopted, declared_taxonomy, placements, **kwargs):
    return rebuild.check(
        cfg,
        db,
        tree_id=TREE_ID,
        registry=kwargs.pop("registry", _registry(str(adopted.ID))),
        declared=declared_taxonomy,
        placements=placements,
        rows=_rows(cfg),
        root_exists=lambda _root: True,
        **kwargs,
    )


def _membership_ids(db, playlist_id: str) -> set[str]:
    return {
        str(row.ContentID)
        for row in db.get_playlist_songs(PlaylistID=str(playlist_id))
    }


def _state_fingerprint(*roots) -> dict[str, tuple[int, int]]:
    """Size and modification time of every file under each root.

    The defect class here is a refusal that already wrote something before it
    decided to refuse, and only a fingerprint either side of the call can see it.
    """
    found: dict[str, tuple[int, int]] = {}
    for root in roots:
        base = Path(root)
        if not base.is_dir():
            continue
        for current, _directories, files in os.walk(base):
            for name in files:
                path = Path(current) / name
                try:
                    stats = path.stat()
                except OSError:  # pragma: no cover - a file that vanished mid-walk
                    continue
                found[str(path)] = (stats.st_size, stats.st_mtime_ns)
    return found


# ═══════════════════════════════════════════════════════════════════════════
# Part 1: rebuildability is a precondition of cutover (approach 5)
# ═══════════════════════════════════════════════════════════════════════════


def test_a_tree_may_not_flip_on_a_source_no_rebuild_can_reproduce(cfg):
    """R39's precondition, at the one moment it can be enforced.

    A cutover is a one-way door: a tree that has taken a native write is
    permanently unsafe to import over, so a tree whose membership no declared
    source can reproduce has no repair path at all once a restore leaves it
    short. Asked before the flip, never after the damage.
    """
    for source in sorted(tree_registry.NOT_REBUILDABLE):
        with pytest.raises(tree_registry.TreeModeRefused) as excinfo:
            tree_registry.record_cutover(
                cfg, TREE_ID, root_id=ADOPTED_ROOT, on=date(2026, 8, 1), source=source
            )
        assert excinfo.value.tree_id == TREE_ID
        assert tree_registry.read(cfg).is_on_the_bridge(TREE_ID)


def test_a_native_record_naming_no_derivation_source_cannot_be_constructed():
    """The same rule structurally, so nothing can build the record by hand.

    Enforcing it only inside ``record_cutover`` would leave every other
    construction path free to make a native record nothing can rebuild, and the
    record is what every later write reads.
    """
    with pytest.raises(ValueError, match="derivation source"):
        tree_registry.TreeRecord(
            tree_id=TREE_ID,
            mode=tree_registry.Mode.DATABASE,
            cutover_on=date(2026, 8, 1),
            root_id=ADOPTED_ROOT,
        )


def test_every_rebuildable_source_has_a_derivation_and_no_other_source_does():
    """The two halves are derived from each other, so neither can drift (P3, P4).

    A source declared rebuildable with no derivation behind it lets a tree flip
    and then fails at the one moment the rebuild is needed. A derivation for a
    source nothing may flip on is dead code claiming coverage it can never be
    asked for.
    """
    assert set(rebuild.DERIVATIONS) == set(tree_registry.REBUILDABLE)
    assert tree_registry.REBUILDABLE | tree_registry.NOT_REBUILDABLE == set(
        tree_registry.DerivationSource
    )
    assert not (tree_registry.REBUILDABLE & tree_registry.NOT_REBUILDABLE)


def test_a_rebuild_of_a_tree_with_a_non_derivable_source_refuses(
    cfg, gates_pass, db, adopted_root, declared
):
    """Asked again at the rebuild, because a registry can be edited by hand."""
    registry = tree_registry.Registry(
        (
            tree_registry.TreeRecord(
                tree_id=TREE_ID,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=date(2026, 8, 1),
                root_id=str(adopted_root.ID),
                source=tree_registry.DerivationSource.CURATED,
            ),
        )
    )
    with pytest.raises(tree_registry.TreeModeRefused):
        _rebuild(
            cfg,
            db,
            adopted_root,
            declared,
            [PLAIN],
            registry=registry,
        )


# ═══════════════════════════════════════════════════════════════════════════
# Part 2: the derivation. Declared taxonomy plus what is on disk, no watermark.
# ═══════════════════════════════════════════════════════════════════════════


def test_the_derivation_routes_a_file_through_the_declared_rules(declared):
    """The rules are CALLED rather than restated, so there is one answer.

    A second implementation of "where does this track go" agrees with the first
    until the day it does not, and on that day a rebuild moves a library's worth
    of tracks.
    """
    truth = [rebuild.Truth(location="/x/one.flac", genre=None, energy=None)]
    placements, gaps = rebuild.derive_from_taxonomy(
        declared, truth, vocal_threshold=None
    )
    expected_bucket = routing.resolve_bucket(declared, None).bucket_id
    assert [entry.bucket for entry in placements] == [expected_bucket]
    assert rebuild.VOCAL_DIMENSION in gaps


def test_a_vocal_track_lands_in_its_energy_sub_AND_the_additive_one(declared):
    """Additive means two placements, not one carrying a list.

    The pair is what the check compares and the write plans on, and folding them
    would make "this track is missing from one of its two playlists"
    inexpressible.
    """
    truth = [rebuild.Truth(location="/x/one.flac", genre=None, energy=9, voxlevel=90)]
    placements, gaps = rebuild.derive_from_taxonomy(
        declared, truth, vocal_threshold=5.0
    )
    subs = {entry.sub for entry in placements}
    assert trees.VOX_SUB_CLASS in subs
    assert len(subs) == 2
    assert gaps == ()


def test_an_additive_sub_playlist_with_no_signal_refuses_rather_than_being_skipped(
    declared,
):
    """P4: a derivation that is 90 percent complete is worse than an honest refusal.

    Silently skipping an additive sub-playlist would write a tree missing a whole
    dimension and then report it converged, because a playlist no declared
    destination names is not compared at all.
    """
    invented = taxonomy.SubClass(
        id="second_additive",
        display="Second Additive",
        policy=taxonomy.SubPolicy.DERIVED,
        additive=True,
    )
    widened = replace(declared, sub_classes=(*declared.sub_classes, invented))
    with pytest.raises(CratekitError) as excinfo:
        rebuild.derive_from_taxonomy(widened, [], vocal_threshold=5.0)
    assert excinfo.value.cause.reason == "rebuild-derivation-incomplete"
    assert excinfo.value.cause.code is ExitCode.LIBRARY_PREREQUISITE


def test_the_walk_reads_every_container_the_tag_module_supports(cfg, tmp_path):
    """The suffix set is DERIVED from the tag module rather than listed (P3).

    A hand-kept copy misses the next container that module learns, and the
    symptom is a whole format silently absent from a rebuild while the rebuild
    reports the tree converged.
    """
    from cratekit.core import tags

    music = Path(cfg.library.root) / "Music"
    for suffix in tags.SUPPORTED_SUFFIXES:
        (music / f"track{suffix}").write_bytes(b"")
    (music / "notes.txt").write_bytes(b"")

    seen = [
        entry.location
        for entry in rebuild.library_truth(
            music, reader=lambda path: rebuild.Truth(location=str(path))
        )
    ]
    assert len(seen) == len(tags.SUPPORTED_SUFFIXES)
    assert not any(name.endswith(".txt") for name in seen)


def test_the_walk_is_sorted_so_two_runs_over_one_library_agree(cfg):
    """A plan that depended on filesystem order would differ run to run."""
    music = Path(cfg.library.root) / "Music"
    for name in ("z.flac", "a.flac", "m.flac"):
        (music / name).write_bytes(b"")
    reader = lambda path: rebuild.Truth(location=str(path))  # noqa: E731
    first = [entry.location for entry in rebuild.library_truth(music, reader=reader)]
    second = [entry.location for entry in rebuild.library_truth(music, reader=reader)]
    assert first == second == sorted(first)


# ═══════════════════════════════════════════════════════════════════════════
# Part 3: the convergence check
# ═══════════════════════════════════════════════════════════════════════════


def test_the_check_reports_a_difference_in_both_directions(
    cfg, gates_pass, db, adopted_root, declared
):
    """The plan's third scenario. R39 asks for both directions and means it.

    One track the taxonomy places and the database lacks, one the database holds
    in a declared destination that the taxonomy does not place there. Reporting
    only the first would make the check blind to a track filed somewhere the
    declaration disagrees with.
    """
    both = _placements(cfg, declared, COMPOSED, PLAIN)
    _rebuild(cfg, db, adopted_root, declared, [COMPOSED, PLAIN])

    # The declaration now names only one of the two. The other is still in the
    # playlist, which is the second direction.
    report = _check(cfg, db, adopted_root, declared, _placements(cfg, declared, COMPOSED))
    assert report.missing == ()
    assert [entry.content_id for entry in report.unexpected] == ["2"]

    # And the first direction, from a tree the declaration outgrew: everything
    # the write placed is still there, so widening the declaration is what makes
    # the database short rather than the tree changing underneath it.
    assert _check(cfg, db, adopted_root, declared, both).converged
    third = rebuild.DeclaredPlacement(
        _music(cfg, "Third Track.flac"), *_destination(declared)
    )
    widened = rebuild.check(
        cfg,
        db,
        tree_id=TREE_ID,
        registry=_registry(str(adopted_root.ID)),
        declared=declared,
        placements=[*both, third],
        rows=[*_rows(cfg), trees.ContentRow("3", third.location, deleted=False)],
        root_exists=lambda _root: True,
    )
    assert [entry.content_id for entry in widened.missing] == ["3"]


def test_a_declared_file_the_library_has_no_row_for_is_surfaced_and_is_not_a_difference(
    cfg, gates_pass, db, adopted_root, declared
):
    """A playlist cannot hold a row the library does not have.

    Counting those as differences would make convergence unreachable for every
    library that has ever downloaded a track it has not yet imported, and an
    unreachable convergence is a flag that can never be cleared. The membership
    writer already skips and surfaces exactly this set.
    """
    absent = rebuild.DeclaredPlacement(
        _music(cfg, "Never Imported.flac"), *_destination(declared)
    )
    report = _check(cfg, db, adopted_root, declared, [absent])
    assert report.converged
    assert [match.outcome for match in report.unmatched] == [trees.MatchOutcome.ABSENT]


def test_a_membership_pointing_at_a_soft_deleted_row_is_not_a_difference_either(
    cfg, gates_pass, db, adopted_root, declared
):
    """The active-row rule, applied from the other end.

    A membership row left pointing at a track the user deleted in rekordbox is a
    leftover the declaration cannot place and an additive rebuild cannot remove.
    Calling it a difference would hold the flag shut over something nobody can
    act on, which is the shape that makes a safety flag permanent.
    """
    _rebuild(cfg, db, adopted_root, declared, [COMPOSED, PLAIN])

    tombstoned = [
        trees.ContentRow("1", _music(cfg, COMPOSED), deleted=True),
        trees.ContentRow("2", _music(cfg, PLAIN), deleted=False),
    ]
    report = rebuild.check(
        cfg,
        db,
        tree_id=TREE_ID,
        registry=_registry(str(adopted_root.ID)),
        declared=declared,
        placements=_placements(cfg, declared, PLAIN),
        rows=tombstoned,
        root_exists=lambda _root: True,
    )
    assert report.converged, "a tombstone's leftover membership was called a difference"


def test_a_playlist_nobody_declared_is_reported_and_is_not_a_difference(
    cfg, gates_pass, db, adopted_root, declared
):
    """P7, on the shape that would fire on ordinary correct libraries.

    A person's own playlist under a governed tree, and every sub-playlist the
    taxonomy marks curated rather than derived, are theirs. A check that called
    them damage would demand a disposition after every manual edit.
    """
    folder = rb_writer.ensure_folder(db, RENAMED_FOLDER, parent=adopted_root)
    playlist = rb_writer.ensure_playlist(db, CURATED_PLAYLIST, folder)
    rb_writer.add_membership(db, playlist, "1")
    db.session.commit()

    report = _check(cfg, db, adopted_root, declared, _placements(cfg, declared, PLAIN))
    assert f"{RENAMED_FOLDER}/{CURATED_PLAYLIST}" in report.foreign
    assert all(entry.content_id != "1" for entry in report.unexpected)


def test_the_check_walks_down_from_the_adopted_root_and_ignores_a_namesake(
    cfg, gates_pass, db, adopted_root, declared
):
    """A walk that resolved the tree by display name would report on a namesake.

    That is the silent parallel tree arriving through the check meant to detect
    it: a second folder of the same name elsewhere in the library, holding the
    same track, would make a short tree read as complete.
    """
    elsewhere = rb_writer.ensure_folder(db, TREE_DISPLAY + " Copy")
    folder_display, sub_display = routing_pass.destination(declared, *_destination(declared))
    decoy_folder = rb_writer.ensure_folder(db, folder_display, parent=elsewhere)
    decoy = rb_writer.ensure_playlist(db, sub_display, decoy_folder)
    rb_writer.add_membership(db, decoy, "2")
    db.session.commit()

    report = _check(cfg, db, adopted_root, declared, _placements(cfg, declared, PLAIN))
    assert [entry.content_id for entry in report.missing] == ["2"]
    assert not report.converged


# ═══════════════════════════════════════════════════════════════════════════
# Part 4: the rebuild
# ═══════════════════════════════════════════════════════════════════════════


def test_a_tree_stripped_of_its_membership_rebuilds_to_match_the_control(
    cfg, gates_pass, db, adopted_root, declared
):
    """The plan's first scenario, asserted against a CONTROL rather than a count.

    The control is the membership a never-damaged tree holds. Deleting the rows
    and rebuilding has to reproduce it exactly, and comparing sets rather than
    lengths is what makes "exactly" mean something.
    """
    names = [COMPOSED, PLAIN]
    _rebuild(cfg, db, adopted_root, declared, names)

    nodes = rebuild.read_tree(db, str(adopted_root.ID))
    assert len(nodes) == 1
    control = dict(nodes[0].content_ids and {nodes[0].playlist_id: nodes[0].content_ids})
    assert control[nodes[0].playlist_id] == frozenset({"1", "2"})

    # The damage: every membership row under the tree, removed out of band.
    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        conn.execute(
            "DELETE FROM djmdSongPlaylist WHERE PlaylistID = ?", (nodes[0].playlist_id,)
        )
        conn.commit()
    finally:
        conn.close()
    db.session.expire_all()
    assert _membership_ids(db, nodes[0].playlist_id) == set()

    report = _rebuild(cfg, db, adopted_root, declared, names)
    assert report.before.missing != ()
    assert report.after.converged
    assert _membership_ids(db, nodes[0].playlist_id) == control[nodes[0].playlist_id]


def test_the_rebuild_derives_its_own_placements_and_will_not_take_a_list(
    cfg, gates_pass, db, adopted_root, declared
):
    """The softening path, closed rather than documented.

    The one thing this function guarantees is that the membership it writes comes
    from the source the registry records. A ``placements`` parameter would be
    exactly the thing that lets a caller supply the answer, so there is not one:
    the seam is the tag READINGS, and the rules, the identifiers and the display
    names all still come from the declaration.
    """
    import inspect

    accepted = set(inspect.signature(rebuild.rebuild_tree).parameters)
    assert "placements" not in accepted
    assert {"truth", "vocal_threshold"} <= accepted

    _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    folder_display, sub_display = routing_pass.destination(declared, *_destination(declared))
    node = rebuild.read_tree(db, str(adopted_root.ID))[0]
    assert (node.folder_display, node.playlist_display) == (folder_display, sub_display)


def test_a_vocal_track_reaches_both_of_its_playlists_through_a_rebuild(
    cfg, gates_pass, db, adopted_root, declared
):
    """The additive dimension, end to end rather than only in the derivation.

    rekordbox has no import path that creates an empty playlist, so the vocal
    sub-playlist is the one destination a rebuild routinely has to create, and a
    derivation that produced it without the write reaching it would look correct
    and place nothing.
    """
    _rebuild(
        cfg,
        db,
        adopted_root,
        declared,
        [PLAIN],
        truth=_truth(cfg, declared, PLAIN, voxlevel=90),
        vocal_threshold=5.0,
    )
    landed = {node.playlist_display for node in rebuild.read_tree(db, str(adopted_root.ID))}
    assert declared.sub_class(trees.VOX_SUB_CLASS).display in landed
    assert len(landed) == 2


def test_a_library_with_no_vocal_calibration_reports_what_it_did_not_compare(
    cfg, gates_pass, db, adopted_root, declared
):
    """A converged answer that quietly skipped a dimension is worse than a gap.

    The threshold is passed in and never imported (D7), and None is a real
    answer: a slim install has no vocals module and no calibration. Naming the
    dimension is what stops "converged" meaning "converged on everything".
    """
    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN], vocal_threshold=None)
    assert report.after.converged
    assert rebuild.VOCAL_DIMENSION in report.after.not_compared


def test_the_read_only_report_derives_through_the_registrys_recorded_source(
    cfg, gates_pass, db, adopted_root, declared
):
    """The diagnostic and the repair must derive the same way or they disagree.

    A report built from one derivation and a rebuild from another would let the
    check say a tree is short that the rebuild has just finished repairing.
    """
    _rebuild(cfg, db, adopted_root, declared, [COMPOSED, PLAIN])
    report = rebuild.report_convergence(
        cfg,
        db,
        tree_id=TREE_ID,
        registry=_registry(str(adopted_root.ID)),
        declared=declared,
        rows=_rows(cfg),
        root_exists=lambda _root: True,
        vocal_threshold=None,
        truth=_truth(cfg, declared, COMPOSED, PLAIN),
    )
    assert report.converged
    assert report.root_id == str(adopted_root.ID)


def test_a_second_rebuild_writes_nothing(cfg, gates_pass, db, adopted_root, declared):
    """The plan's second scenario. Re-running is the recovery procedure.

    A second pass that inserted again would turn "run it again" into a second
    failure, and the duplicate is one the user cannot remove by removing it once.
    """
    names = [COMPOSED, PLAIN]
    first = _rebuild(cfg, db, adopted_root, declared, names)
    second = _rebuild(cfg, db, adopted_root, declared, names)

    assert first.repaired == 2
    assert second.repaired == 0
    assert second.membership is not None and second.membership.already_present == 2
    assert second.after.converged


def test_a_rebuild_after_a_rename_converges_rather_than_doubling_the_tree(
    cfg, gates_pass, db, adopted_root, declared
):
    """THE ONE THAT DOUBLES A LIBRARY, and the reason this unit persists node ids.

    Every find-or-create in the guarded writer targets a playlist by the name
    rekordbox shows. A rebuild that resolved its destinations from the taxonomy's
    display names would, after a rename, find nothing under the new name, create
    the destination a second time, and file every track twice. Asserted by
    COUNTING nodes under the root, because looking the name up again finds the
    first one and reports success either way.
    """
    names = [COMPOSED, PLAIN]
    _rebuild(cfg, db, adopted_root, declared, names)
    before = rebuild.read_tree(db, str(adopted_root.ID))
    assert len(before) == 1

    # Somebody renames the bucket folder in rekordbox. The taxonomy still says
    # what it always said; the library no longer agrees.
    folder = db.get_playlist(ID=before[0].folder_id)
    folder.Name = RENAMED_FOLDER
    db.session.commit()

    report = _rebuild(cfg, db, adopted_root, declared, names)
    after = rebuild.read_tree(db, str(adopted_root.ID))

    assert len(after) == 1, "the rebuild created a second copy of the destination"
    assert after[0].playlist_id == before[0].playlist_id
    assert after[0].content_ids == frozenset({"1", "2"})
    assert report.repaired == 0
    assert report.after.converged
    assert report.after.renamed != (), "the rename is reported rather than silent"


def test_a_destination_with_no_recorded_node_falls_back_to_the_declared_name(
    cfg, gates_pass, db, adopted_root, declared
):
    """The first rebuild after a cutover has nothing recorded, and must adopt.

    Resolving by the declared display name is exactly right when no rename has
    happened, which is the ordinary adoption path the membership writer already
    relies on. Refusing without a record would make the first rebuild impossible.
    """
    folder_display, sub_display = routing_pass.destination(declared, *_destination(declared))
    folder = rb_writer.ensure_folder(db, folder_display, parent=adopted_root)
    existing = rb_writer.ensure_playlist(db, sub_display, folder)
    db.session.commit()

    assert convergence.read(cfg).tree(TREE_ID) is None
    _rebuild(cfg, db, adopted_root, declared, [PLAIN])

    nodes = rebuild.read_tree(db, str(adopted_root.ID))
    assert len(nodes) == 1 and nodes[0].playlist_id == str(existing.ID)
    recorded = convergence.read(cfg).tree(TREE_ID)
    assert recorded is not None
    assert recorded.node(*_destination(declared)).playlist_id == str(existing.ID)


def test_a_recorded_node_that_no_longer_exists_falls_back_rather_than_refusing(
    cfg, gates_pass, db, adopted_root, declared
):
    """Turning the one operation that repairs a damaged tree into another thing
    the damage breaks would leave a library with no way out at all."""
    bucket_id, sub_id = _destination(declared)
    convergence.record_nodes(
        cfg,
        TREE_ID,
        [
            convergence.DestinationNode(
                bucket=bucket_id, sub=sub_id, folder_id="gone-1", playlist_id="gone-2"
            )
        ],
    )
    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert report.after.converged
    assert rebuild.read_tree(db, str(adopted_root.ID))[0].content_ids == frozenset({"2"})


def test_a_rebuild_never_removes_a_membership_the_declaration_does_not_place(
    cfg, gates_pass, db, adopted_root, declared
):
    """Additive on purpose. A membership somebody made by hand is their data.

    A rebuild that made the tree match by deleting would be the one operation in
    this product that destroys work nobody can get back, so the other direction
    is reported and settled by a person instead.
    """
    _rebuild(cfg, db, adopted_root, declared, [COMPOSED, PLAIN])
    report = _rebuild(cfg, db, adopted_root, declared, [COMPOSED])

    nodes = rebuild.read_tree(db, str(adopted_root.ID))
    assert nodes[0].content_ids == frozenset({"1", "2"}), "a rebuild deleted a membership"
    assert [entry.content_id for entry in report.after.unexpected] == ["2"]
    assert not report.cleared


# ═══════════════════════════════════════════════════════════════════════════
# Part 5: the destructive-session gates (approach 3, scenario 5)
# ═══════════════════════════════════════════════════════════════════════════


def test_a_rebuild_refuses_without_the_acknowledgment(
    cfg, db, adopted_root, declared, monkeypatch
):
    """A rebuild is a destructive session and passes the same three gates.

    Driven with the volume agreeing and nothing acknowledged, which is the state
    of every library before a person answers, and asserted against the state tree
    either side: a refusal that leaves a trace has already done something.
    """
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: cfg.library.volume_id),
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    roots = (cfg.library.root, config.installation_state_dir(), config.config_dir())
    before = _state_fingerprint(*roots)

    with pytest.raises(CratekitError) as excinfo:
        _rebuild(cfg, db, adopted_root, declared, [PLAIN])

    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED
    assert _state_fingerprint(*roots) == before


def test_a_rebuild_refuses_while_the_lock_is_held_elsewhere(
    cfg, gates_pass, db, adopted_root, declared
):
    """The lock looks exactly like another process holding it, because it is."""
    lock = session.lock_path(cfg)
    lock.parent.mkdir(parents=True, exist_ok=True)
    contender = open(lock, "a+")
    try:
        rb_writer._acquire_exclusive(contender)
        with pytest.raises(CratekitError) as excinfo:
            _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    finally:
        contender.close()
    assert excinfo.value.cause.code is ExitCode.LIBRARY_BUSY


def test_a_rebuild_refuses_on_a_volume_whose_identity_does_not_match(
    cfg, gates_pass, db, adopted_root, declared, monkeypatch
):
    """The one gate that must fire before any path is resolved."""
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: "0000-0000")
    )
    with pytest.raises(CratekitError) as excinfo:
        _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE


# ═══════════════════════════════════════════════════════════════════════════
# Part 6: detecting a database that came back from somewhere else (approach 4)
# ═══════════════════════════════════════════════════════════════════════════


def _fingerprint(*, rows: int, usn: int) -> convergence.Fingerprint:
    return convergence.Fingerprint(schema_version="6000", active_rows=rows, local_usn=usn)


def test_ordinary_rekordbox_use_is_not_a_regression():
    """P7, stated as the property the whole detector turns on.

    Importing forty tracks moves the row count and the update count forward
    together, every day. A guard that demanded a rebuild after that would be a
    guard people learn to route around, which is the failure it exists to prevent
    arriving through the guard.
    """
    previous = _fingerprint(rows=100, usn=500)
    assert convergence.regression(previous, _fingerprint(rows=140, usn=560)) is None
    assert convergence.regression(previous, _fingerprint(rows=90, usn=560)) is None
    assert convergence.regression(previous, previous) is None


def test_nothing_recorded_yet_is_not_a_regression():
    """A fresh install has taken no governed write, so it has nothing to compare.

    Calling that a restore would mark every tree unconverged on the first run of
    a library where nothing has happened at all.
    """
    assert convergence.regression(None, _fingerprint(rows=1, usn=1)) is None


@pytest.mark.parametrize(
    "current, expected",
    [
        (_fingerprint(rows=100, usn=400), convergence.Regression.SEQUENCE_WENT_BACKWARD),
        (_fingerprint(rows=90, usn=500), convergence.Regression.ROWS_MOVED_AT_A_STANDSTILL),
    ],
)
def test_a_database_that_went_backward_is_detected(current, expected):
    """Two shapes, and the second is the one a reader will not believe untold.

    rekordbox cannot add or remove a row without bumping the sequence, so a
    standstill sequence beside a moved row count is two databases, not one.
    """
    assert convergence.regression(_fingerprint(rows=100, usn=500), current) is expected


def test_the_probe_reads_the_three_numbers_out_of_a_real_database(cfg, db):
    """The row count is filtered AT THE DATABASE rather than in Python.

    A Python side walk would read the soft-delete marker off each row through an
    accessor, and an accessor with a default hands back "not deleted" for every
    tombstone the moment the binding stops exposing the column. A filter either
    filters or raises.
    """
    taken = convergence.probe(db)
    assert taken.active_rows == 2
    assert taken.local_usn == db.get_local_usn()
    assert taken.schema_version == rb_writer.db_schema_version(db)

    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        conn.execute("UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = '1'")
        conn.commit()
    finally:
        conn.close()
    db.session.expire_all()
    assert convergence.probe(db).active_rows == 1


def test_a_database_that_cannot_answer_refuses_with_a_structured_cause(cfg, db):
    """S4. A traceback at the boundary becomes "report a defect", which is wrong.

    A column the schema moved, or a registry row a rekordbox version stopped
    writing, means the question has no answer in either direction. Telling
    somebody whose schema has moved to file a bug is not the remedy.
    """

    class _Mute:
        session = db.session

        def get_content(self, **_kwargs):
            raise RuntimeError("no such column")

    with pytest.raises(CratekitError) as excinfo:
        convergence.probe(_Mute())
    assert excinfo.value.cause.reason == "library-fingerprint-unreadable"
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNREADABLE


def test_a_governed_write_records_the_fingerprint_at_its_close(
    cfg, gates_pass, db, adopted_root, declared
):
    """Taken AFTER the commit, or the next run reads its own write as a restore.

    Asserted through the membership writer rather than by calling the recorder,
    because the point is that the one call every database membership write goes
    through is what arms it.
    """
    assert convergence.read(cfg).fingerprint is None
    _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    recorded = convergence.read(cfg).fingerprint
    assert recorded is not None
    assert recorded.local_usn == db.get_local_usn()
    assert recorded.taken


def test_an_out_of_band_restore_marks_every_native_tree_and_refuses_the_next_write(
    cfg, gates_pass, db, adopted_root, declared
):
    """The case atomic snapshots cannot see, end to end.

    Nothing Cratekit wrote is involved in a recovery from the rclone mirror, so
    nothing Cratekit wrote can be trusted to have noticed. What is left is the
    number inside the database itself.
    """
    _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    recorded = convergence.read(cfg).fingerprint
    assert recorded is not None

    # The recovery: the same library, from an older copy. Written straight into
    # the file, because that is what a restore outside this product looks like.
    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        conn.execute(
            "UPDATE AgentRegistry SET int_1 = ? WHERE registry_id = 'localUpdateCount'",
            (recorded.local_usn - 5,),
        )
        conn.commit()
    finally:
        conn.close()
    db.session.expire_all()

    with pytest.raises(CratekitError) as excinfo:
        trees.write_tree_membership(
            cfg,
            db,
            tree_id=TREE_ID,
            registry=_registry(str(adopted_root.ID)),
            plan={},
            rows=_rows(cfg),
            root_exists=lambda _root: True,
            analysis_roots=[Path(cfg.library.root) / "Music"],
        )
    assert excinfo.value.cause.reason == "tree-unconverged"
    assert excinfo.value.cause.code is ExitCode.UNCONVERGED

    record = convergence.read(cfg).tree(TREE_ID)
    assert record is not None and record.blocking
    assert record.reason == str(convergence.Regression.SEQUENCE_WENT_BACKWARD)


def test_a_library_with_nothing_flipped_never_probes_at_all(cfg, declared):
    """Every library until the first cutover. The mechanism stays off its path.

    Driven with a handle that raises on any read, which is the only assertion
    that can tell "did not probe" from "probed and found nothing".
    """

    class _Exploding:
        def __getattr__(self, name):  # pragma: no cover - the point is it is unused
            raise AssertionError(f"the convergence check touched the database ({name})")

    convergence.assert_no_out_of_band_restore(cfg, _Exploding(), tree_registry.EMPTY)


def test_a_rebuild_is_not_refused_by_the_flag_it_exists_to_clear(
    cfg, gates_pass, db, adopted_root, declared
):
    """A latch that condemned its own remedy would be a library with no exit.

    This repository has shipped that shape once already, with a
    committed-unverified session whose refusal named a restore and whose latch
    then refused the restore. The rebuild purpose is the same declaration U8
    made, scoped to this pair of latches and to nothing else.
    """
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    assert convergence.read(cfg).tree(TREE_ID).blocking

    with pytest.raises(CratekitError):
        trees.write_tree_membership(
            cfg,
            db,
            tree_id=TREE_ID,
            registry=_registry(str(adopted_root.ID)),
            plan={},
            rows=_rows(cfg),
            root_exists=lambda _root: True,
            analysis_roots=[Path(cfg.library.root) / "Music"],
        )

    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert report.cleared
    assert not convergence.read(cfg).tree(TREE_ID).blocking


def test_the_rebuild_purpose_sheds_the_convergence_latches_and_nothing_else(
    cfg, db, adopted_root, declared, monkeypatch
):
    """The exemption is one pair of gates wide. The session spine still applies.

    Named explicitly because an exemption nobody bounds is an override, and the
    difference is only visible if somebody asserts what a rebuild is still held
    by.
    """
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: cfg.library.volume_id),
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")

    with pytest.raises(CratekitError) as excinfo:
        _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED


# ═══════════════════════════════════════════════════════════════════════════
# Part 7: clearing the flag, and the one escape from a permanent refusal
# ═══════════════════════════════════════════════════════════════════════════


def test_a_flag_cannot_be_cleared_while_the_check_still_differs(cfg):
    """The plan's fourth scenario. The refusal repeats what is still wrong.

    Clearing on request would be the flag's off switch wearing the flag's
    clothes, and the differences travel as the check's own list rather than as a
    count so the refusal can name them.
    """
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    with pytest.raises(CratekitError) as excinfo:
        convergence.clear_unconverged(cfg, TREE_ID, differences=["missing:a/b:7"])
    assert excinfo.value.cause.reason == "tree-unconverged"
    assert excinfo.value.cause.detail["differences"] == ["missing:a/b:7"]
    assert convergence.read(cfg).tree(TREE_ID).blocking


def test_a_named_person_can_dispose_of_a_difference_nothing_derives(cfg):
    """The one escape, because a refusal with no way past it is not a safety
    property, it is a product nobody can use.

    The flag STAYS SET and stops refusing, so a report still says the difference
    is there and only the refusal was answered for.
    """
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    convergence.clear_unconverged(
        cfg,
        TREE_ID,
        differences=["unexpected:a/b:7"],
        disposition=convergence.Disposition(actor="an operator", note="filed by hand"),
    )
    record = convergence.read(cfg).tree(TREE_ID)
    assert record.unconverged and not record.blocking
    assert record.disposition.actor == "an operator"
    assert record.disposition.on, "a disposition records when it was taken"


def test_a_disposition_with_no_actor_is_refused():
    """A disposition is a person taking responsibility for a difference.

    A record that cannot say who took it is the product deciding on the user's
    behalf that their library is fine.
    """
    with pytest.raises(ValueError, match="WHO decided"):
        convergence.Disposition(actor="  ")


def test_a_disposition_is_scoped_to_one_tree(cfg):
    """A library may hold one governed tree beside five somebody curates.

    Answering for a difference in the first says nothing about the second, and a
    disposition that widened would wave through the next restore.
    """
    convergence.mark_unconverged(cfg, [TREE_ID, "other_tree"], reason="a restore")
    convergence.clear_unconverged(
        cfg,
        TREE_ID,
        differences=["unexpected:a/b:7"],
        disposition=convergence.Disposition(actor="an operator"),
    )
    state = convergence.read(cfg)
    assert not state.tree(TREE_ID).blocking
    assert state.tree("other_tree").blocking
    assert state.blocking_trees() == ("other_tree",)


def test_a_new_refusal_clears_an_old_disposition(cfg):
    """Somebody accepted a difference they were SHOWN.

    A later restore is a different difference they have not seen, and carrying
    the old answer forward would let one judgement about a curated playlist wave
    through every restore after it.
    """
    convergence.mark_unconverged(cfg, [TREE_ID], reason="first")
    convergence.clear_unconverged(
        cfg,
        TREE_ID,
        differences=["unexpected:a/b:7"],
        disposition=convergence.Disposition(actor="an operator"),
    )
    convergence.mark_unconverged(cfg, [TREE_ID], reason="second")
    record = convergence.read(cfg).tree(TREE_ID)
    assert record.disposition is None and record.blocking


def test_marking_twice_for_one_reason_keeps_the_date_the_damage_was_first_seen(cfg):
    """Re-running the detection must not keep moving the date forward to now."""
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    first = convergence.read(cfg).tree(TREE_ID).since
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    assert convergence.read(cfg).tree(TREE_ID).since == first


# ═══════════════════════════════════════════════════════════════════════════
# Part 8: the record itself. A wrong document is not an empty one.
# ═══════════════════════════════════════════════════════════════════════════


def test_an_absent_record_is_the_empty_one(cfg):
    assert convergence.read(cfg) is convergence.EMPTY
    assert convergence.read(cfg).blocking_trees() == ()


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param("[]", id="a top-level list"),
        pytest.param('"unconverged"', id="a scalar"),
        pytest.param("{}", id="no schema version"),
        pytest.param('{"schema_version": "1", "trees": []}', id="a string version"),
        pytest.param('{"schema_version": 1}', id="no trees array"),
        pytest.param('{"schema_version": 1, "trees": {}}', id="trees as an object"),
        pytest.param('{"schema_version": 1, "trees": [1]}', id="a record that is not an object"),
        pytest.param(
            '{"schema_version": 1, "trees": [{"tree": "a"}, {"tree": "a"}]}',
            id="two records for one tree",
        ),
        pytest.param(
            '{"schema_version": 1, "trees": [{"tree": "a", "unconverged": "yes"}]}',
            id="a flag read for its truthiness",
        ),
        pytest.param(
            '{"schema_version": 1, "trees": [{"tree": "a"}]}',
            id="a record with no flag at all, which would default to converged",
        ),
        pytest.param(
            '{"schema_version": 1, "trees": [{"tree": " "}]}',
            id="a record naming no tree",
        ),
        pytest.param(
            '{"schema_version": 1, "trees": [], "fingerprint": {"active_rows": 1}}',
            id="a fingerprint missing a number",
        ),
        pytest.param(
            '{"schema_version": 1, "trees": [], "fingerprint": []}',
            id="a fingerprint that is not an object",
        ),
        pytest.param(
            '{"schema_version": 1, "trees": [{"tree": "a", "nodes": [{"bucket": "b"}]}]}',
            id="a half-recorded destination node",
        ),
        pytest.param("not json at all", id="not JSON"),
    ],
)
def test_a_wrong_document_is_refused_rather_than_read_as_nothing_unconverged(cfg, payload):
    """The misreading that admits every write this record exists to refuse.

    Catching only a JSON parse error is what let a previous unit read a top-level
    list, a scalar, a null field and records under a newer version's key all as
    an empty store, after which the next write persisted that emptiness. Here the
    same misreading would report a damaged tree as fine and then write it down.
    """
    path = convergence.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")
    with pytest.raises(convergence.ConvergenceStateUnreadable):
        convergence.read(cfg)


def test_a_record_from_a_newer_build_asks_for_an_upgrade_rather_than_the_doctor(cfg):
    """One slug covers every way the file is unusable; the REMEDY is what differs."""
    path = convergence.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"schema_version": convergence.SCHEMA_VERSION + 1, "trees": []}),
        encoding="utf-8",
    )
    with pytest.raises(convergence.ConvergenceStateUnreadable) as excinfo:
        convergence.read(cfg)
    assert excinfo.value.remedy is not None
    assert excinfo.value.cause.reason == "tree-convergence-unusable"
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNREADABLE


def test_the_version_this_build_writes_is_the_version_it_reads_back(cfg):
    """A version stamped and never read is the shape that let a wrong document in."""
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    parsed = json.loads(convergence.path_for(cfg).read_text(encoding="utf-8"))
    assert parsed["schema_version"] == convergence.SCHEMA_VERSION


def test_the_record_is_keyed_on_the_identifier_and_never_on_a_display_name(cfg):
    """R19 and D5, asserted against the BYTES rather than against the API.

    A record keyed on a display name is orphaned the moment somebody renames the
    folder, and an orphaned record reads as "this tree is fine".
    """
    convergence.record_nodes(
        cfg,
        TREE_ID,
        [
            convergence.DestinationNode(
                bucket="a_bucket", sub="a_sub", folder_id="f-1", playlist_id="p-1"
            )
        ],
    )
    raw = convergence.path_for(cfg).read_text(encoding="utf-8")
    assert TREE_ID in raw and "a_bucket" in raw
    assert TREE_DISPLAY not in raw and RENAMED_FOLDER not in raw


def test_the_record_and_its_lock_are_declared_state_with_the_right_roles():
    """The three failures the roles prevent, one assertion each.

    A fingerprint that survived a rollback would make Cratekit's own restore look
    like somebody else's. A node map that survived would point a rebuild at rows
    the restore removed. A lock inside the coupled set would have its inode
    swapped under every process holding it.
    """
    entry = config.state_file(convergence.STATE_KEY)
    assert entry.snapshot is config.SnapshotRole.COUPLED
    assert entry.root is config.StateRoot.LIBRARY
    assert entry in config.coupled_state_files()

    lock = config.state_file(convergence.LOCK_KEY)
    assert lock.snapshot is config.SnapshotRole.NEVER_RESTORED
    assert lock not in config.coupled_state_files()


def test_the_lock_serializes_a_read_modify_write_across_processes(cfg):
    """A rename is atomic. The read-modify-write CYCLE around it is not.

    Two units in this repository shipped an unlocked cycle over a JSON document
    and both were caught by review rather than by a suite: every losing call
    returns a record reporting success. Driven with a real second process,
    because a lock this one already holds proves nothing.
    """
    import subprocess
    import sys
    import textwrap

    workers, per_worker = 4, 25
    convergence.mark_unconverged(cfg, ["tree_seed"], reason="a restore")
    source = textwrap.dedent(
        f"""
        import os, sys
        sys.path.insert(0, {str(Path(__file__).resolve().parent.parent / "src")!r})
        os.environ["CRATEKIT_LIBRARY_ROOT"] = {str(cfg.library.root)!r}
        from cratekit.core import config, convergence
        cfg = config.from_dict({_config_payload(cfg)!r})
        worker = sys.argv[1]
        for index in range({per_worker}):
            convergence.mark_unconverged(
                cfg, ["tree_%s_%d" % (worker, index)], reason="a restore"
            )
        """
    )
    # EVERY WORKER WRITES NAMES NO OTHER WORKER WRITES, which is the whole design
    # of this test. Four processes recording the SAME set would still end with
    # every name on disk after an interleave discarded half the writes, because
    # somebody else wrote each one too; the test would pass with the lock deleted.
    running = [
        subprocess.Popen([sys.executable, "-c", source, str(index)])
        for index in range(workers)
    ]
    for worker in running:
        assert worker.wait() == 0

    recorded = convergence.read(cfg).blocking_trees()
    assert len(recorded) == workers * per_worker + 1, (
        f"{workers * per_worker + 1 - len(recorded)} record(s) were lost to an "
        f"interleaved read-modify-write, and every losing call returned a record "
        f"reporting success"
    )


def _config_payload(cfg) -> dict:
    """The configuration a helper process rebuilds from, as plain data."""
    return {
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(cfg.library.root),
            "volume_id": cfg.library.volume_id,
            "db_path": str(cfg.library.db_path),
        },
        "paths": {"download_staging": str(Path(cfg.library.root).parent / "staging")},
        "profile": {"name": "slim"},
    }


def test_the_two_new_reasons_are_declared_in_the_one_vocabulary():
    """S4: a refusal with no reserved code collapses to a bare status at the
    process boundary and cannot be recovered downstream."""
    assert REASONS["tree-convergence-unusable"] is ExitCode.LIBRARY_UNREADABLE
    assert REASONS["rebuild-derivation-incomplete"] is ExitCode.LIBRARY_PREREQUISITE
    assert REASONS["library-fingerprint-unreadable"] is ExitCode.LIBRARY_UNREADABLE


def test_the_two_composition_forms_of_one_filename_are_one_track(
    cfg, gates_pass, db, adopted_root, declared
):
    """The 144-file loss, arriving at the check.

    macOS stores filenames decomposed and rekordbox stores them precomposed, so
    the two forms turn up in one library routinely. A check that normalized one
    side and not the other would report a track missing that is sitting there.
    """
    bucket_id, sub_id = _destination(declared)
    _rebuild(cfg, db, adopted_root, declared, [COMPOSED])
    report = _check(
        cfg,
        db,
        adopted_root,
        declared,
        [rebuild.DeclaredPlacement(_music(cfg, DECOMPOSED), bucket_id, sub_id)],
    )
    assert report.converged
    assert report.unmatched == ()


# ═══════════════════════════════════════════════════════════════════════════
# Part 9: what an EMPTY answer means, and what a NAME COLLISION costs
#
# Every test below is a reviewer's reproduction, kept in the shape it was
# executed in. The shared defect is one sentence: absence read as evidence of
# absence. A derivation that placed nothing, a destination that lost every
# track, a playlist holding one track twice and a folder whose name now belongs
# to two nodes all produced NO DIFFERENCE, and no difference read as converged.
# ═══════════════════════════════════════════════════════════════════════════


def _energy_truth(cfg, declared_taxonomy, pairs):
    """Readings that place named files at named energies, so two subs are used."""
    return [
        rebuild.Truth(location=_music(cfg, name), genre=None, energy=energy)
        for name, energy in pairs
    ]


def _two_destinations(declared_taxonomy):
    """Two declared destinations under one bucket, by energy band. Derived."""
    bucket_id = routing.resolve_bucket(declared_taxonomy, None).bucket_id
    low = routing.energy_sub(declared_taxonomy, bucket_id, 1)
    high = routing.energy_sub(declared_taxonomy, bucket_id, declared_taxonomy.energy.scale_max)
    assert low is not None and high is not None and low.id != high.id
    return bucket_id, low.id, high.id


def test_a_rebuild_that_derived_nothing_refuses_instead_of_reporting_converged(
    cfg, gates_pass, db, adopted_root, declared
):
    """THE DOMINANT DEFECT SHAPE, reproduced exactly as it was executed.

    A governed tree holding two placed tracks, flagged for a restore, rebuilt
    with the music directory mounted and EMPTY. Every question downstream is
    scoped to the destinations the derivation produced, so zero placements gave
    zero destinations, every node fell into ``foreign``, ``differences`` was
    empty, ``converged`` was True, and the flag was cleared. Worse, the plan was
    empty too, so the acknowledgment, the volume assertion, the session lock, the
    verified capture and the analysis watch were all skipped on the exact path
    that cleared the safety flag.
    """
    _rebuild(cfg, db, adopted_root, declared, [COMPOSED, PLAIN])
    convergence.mark_unconverged(
        cfg, [TREE_ID], reason=str(convergence.Regression.SEQUENCE_WENT_BACKWARD)
    )
    assert convergence.read(cfg).tree(TREE_ID).blocking

    with pytest.raises(CratekitError) as excinfo:
        # An empty music directory, read live rather than supplied. The seam is
        # the readings, and here there are none to read.
        _rebuild(cfg, db, adopted_root, declared, [], truth=None)

    assert excinfo.value.cause.reason == "rebuild-derivation-empty"
    assert excinfo.value.cause.code is ExitCode.LIBRARY_PREREQUISITE
    assert convergence.read(cfg).tree(TREE_ID).blocking, "the flag was cleared"


def test_a_music_directory_that_is_not_there_refuses_rather_than_walking_nothing(
    cfg, gates_pass, db, adopted_root, declared
):
    """The unmounted volume, which used to be indistinguishable from an empty one.

    ``library_truth`` returned on a directory it could not find, so "the volume
    is not mounted" and "the library holds no music" reached the derivation as
    one answer. Only one of them is a fact about the library.
    """
    music = Path(cfg.library.root) / cfg.library.music_dir
    for entry in sorted(music.rglob("*"), reverse=True):
        entry.unlink() if entry.is_file() else entry.rmdir()
    music.rmdir()

    with pytest.raises(CratekitError) as excinfo:
        list(rebuild.library_truth(music))
    assert excinfo.value.cause.reason == "rebuild-derivation-empty"

    with pytest.raises(CratekitError):
        _rebuild(cfg, db, adopted_root, declared, [], truth=None)


def test_a_destination_that_lost_every_track_is_still_compared(
    cfg, gates_pass, db, adopted_root, declared
):
    """THE PARTIAL SHRINK, which is the same defect at one destination's scale.

    A destination whose declared placements all go away stopped being a
    destination at all: nothing resolved to its node, the node fell into
    ``foreign``, which is the set reserved for playlists a person curated and
    which is deliberately not a difference, and its whole contents left the
    comparison in silence. The tree then reported converged with a playlist full
    of tracks nothing declares.

    Carrying the RECORDED destinations forward is the fix, and it is the record
    this unit already keeps being used for the second thing it is good for.
    """
    bucket_id, low_id, high_id = _two_destinations(declared)
    both = _energy_truth(cfg, declared, [(COMPOSED, 1), (PLAIN, declared.energy.scale_max)])
    first = _rebuild(cfg, db, adopted_root, declared, [], truth=both)
    assert first.after.converged
    assert len(rebuild.read_tree(db, str(adopted_root.ID))) == 2

    recorded = convergence.read(cfg).tree(TREE_ID)
    assert recorded.node(bucket_id, low_id) is not None
    assert recorded.node(bucket_id, high_id) is not None

    # The library shrinks: the low-energy track is gone from the derivation
    # entirely, so that destination has no declared placements this run.
    shrunk = _energy_truth(cfg, declared, [(PLAIN, declared.energy.scale_max)])
    report = _rebuild(cfg, db, adopted_root, declared, [], truth=shrunk)

    assert not report.after.converged, "a destination that emptied reported converged"
    assert not report.cleared
    assert [entry.content_id for entry in report.after.unexpected] == ["1"]
    assert f"{bucket_id}/{low_id}" not in " ".join(report.after.foreign)


def test_two_declared_destinations_on_one_display_pair_refuse(
    cfg, gates_pass, db, adopted_root, declared
):
    """THE COLLISION THAT CORRUPTS A TREE PERMANENTLY, reproduced.

    An ordinary bucket consolidation produces it: two destinations end up
    carrying one folder and playlist name. The plan was keyed on that pair, so
    both sets of tracks went into whichever node the name lookup reached first,
    every track in one bucket ended up in two playlists at once, and the node
    record was then rewritten from the same lookup so BOTH destinations named one
    node. Every later rebuild reported the other destination short, and an
    additive rebuild cannot undo what it did, so the flag could never be cleared
    again.

    The XML half of this repository has refused exactly this since U18, in
    ``trees.DuplicateFolders``. The database half now refuses it too.
    """
    both = _energy_truth(cfg, declared, [(COMPOSED, 1), (PLAIN, declared.energy.scale_max)])
    _rebuild(cfg, db, adopted_root, declared, [], truth=both)
    nodes = rebuild.read_tree(db, str(adopted_root.ID))
    assert len(nodes) == 2

    # The consolidation: one playlist is renamed to the other one's name, so two
    # declared destinations now resolve to one display pair.
    victim = db.get_playlist(ID=nodes[0].playlist_id)
    victim.Name = nodes[1].playlist_display
    db.session.commit()

    with pytest.raises(CratekitError) as excinfo:
        _rebuild(cfg, db, adopted_root, declared, [], truth=both)
    assert excinfo.value.cause.reason == "tree-unconverged"
    assert "one folder and playlist named" in excinfo.value.cause.message

    after = rebuild.read_tree(db, str(adopted_root.ID))
    assert {node.playlist_id for node in after} == {n.playlist_id for n in nodes}
    for node in after:
        assert len(node.content_ids) == 1, "a track was filed into two playlists"

    # And the read-only check refuses the same condition, so somebody can see it
    # without writing anything.
    with pytest.raises(CratekitError):
        rebuild.report_convergence(
            cfg,
            db,
            tree_id=TREE_ID,
            registry=_registry(str(adopted_root.ID)),
            declared=declared,
            rows=_rows(cfg),
            root_exists=lambda _root: True,
            vocal_threshold=None,
            truth=both,
        )


def test_two_nodes_under_one_display_pair_refuse_the_way_the_xml_half_does(
    cfg, gates_pass, db, adopted_root, declared
):
    """``DuplicateFolders``' own sentence, applied to the database writer.

    "A writer that targets a folder by name cannot tell them apart, so it would
    write to the first one twice and to the second one never."
    """
    _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    node = rebuild.read_tree(db, str(adopted_root.ID))[0]
    twin_folder = rb_writer.ensure_folder(db, RENAMED_FOLDER, parent=adopted_root)
    twin = rb_writer.ensure_playlist(db, node.playlist_display, twin_folder)
    twin_folder.Name = node.folder_display
    db.session.commit()
    assert twin is not None

    with pytest.raises(CratekitError) as excinfo:
        _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert "cannot tell them apart" in excinfo.value.cause.message


def test_a_node_map_naming_one_playlist_for_two_destinations_is_refused(
    cfg, gates_pass, db, adopted_root, declared
):
    """The injectivity nothing was checking, in both directions.

    Two destinations against one node is the collision above seen from the
    record's side, and it is what made the damage permanent: the map is read
    FIRST on every later rebuild, so a single wrong entry misfiles a library with
    no rename involved at all.
    """
    bucket_id, low_id, high_id = _two_destinations(declared)
    with pytest.raises(ValueError, match="one playlist row"):
        convergence.TreeConvergence(
            tree_id=TREE_ID,
            nodes=(
                convergence.DestinationNode(
                    bucket=bucket_id, sub=low_id, folder_id="f1", playlist_id="p1"
                ),
                convergence.DestinationNode(
                    bucket=bucket_id, sub=high_id, folder_id="f1", playlist_id="p1"
                ),
            ),
        )

    with pytest.raises(ValueError, match="two nodes for the destination"):
        convergence.TreeConvergence(
            tree_id=TREE_ID,
            nodes=(
                convergence.DestinationNode(
                    bucket=bucket_id, sub=low_id, folder_id="f1", playlist_id="p1"
                ),
                convergence.DestinationNode(
                    bucket=bucket_id, sub=low_id, folder_id="f2", playlist_id="p2"
                ),
            ),
        )


def test_the_recorded_node_is_the_one_the_destination_resolved_to(
    cfg, gates_pass, db, adopted_root, declared
):
    """The identifier this unit exists to preserve is never re-derived and lost.

    The record used to be rebuilt from a display-name lookup over the freshly
    read tree, which threw away the resolved answer and replaced it with a weaker
    one. Asserted through a RENAME, because that is the case where the two
    answers differ.
    """
    _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    before = rebuild.read_tree(db, str(adopted_root.ID))[0]
    folder = db.get_playlist(ID=before.folder_id)
    folder.Name = RENAMED_FOLDER
    db.session.commit()

    _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    recorded = convergence.read(cfg).tree(TREE_ID).node(*_destination(declared))
    assert recorded.folder_id == before.folder_id
    assert recorded.playlist_id == before.playlist_id


def test_a_track_held_twice_in_one_playlist_is_a_difference_the_flag_stays_shut_on(
    cfg, gates_pass, db, adopted_root, declared
):
    """The doubling the check could not see, because it compared SETS.

    Two ``djmdSongPlaylist`` rows for one pair is a doubled tree one level below
    the level the doubling check looked at. rekordbox shows the track twice,
    removing it once leaves the other, and the additive write cannot take either
    away, so it has to hold the flag shut rather than being repaired.
    """
    _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    node = rebuild.read_tree(db, str(adopted_root.ID))[0]

    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        rows = conn.execute(
            "SELECT * FROM djmdSongPlaylist WHERE PlaylistID = ?", (node.playlist_id,)
        ).fetchall()
        columns = [description[0] for description in conn.execute(
            "SELECT * FROM djmdSongPlaylist LIMIT 1"
        ).description]
        duplicate = dict(zip(columns, rows[0]))
        duplicate["ID"] = f"{duplicate['ID']}-again"
        conn.execute(
            f"INSERT INTO djmdSongPlaylist ({','.join(columns)}) "
            f"VALUES ({','.join('?' * len(columns))})",
            [duplicate[name] for name in columns],
        )
        conn.commit()
    finally:
        conn.close()
    db.session.expire_all()

    walked = rebuild.read_tree(db, str(adopted_root.ID))[0]
    assert walked.doubled == frozenset({"2"})

    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert report.after.doubled != ()
    assert not report.after.converged
    assert not report.cleared


def test_a_rebuild_runs_the_restore_detection_it_is_merely_not_refused_by(
    cfg, gates_pass, db, adopted_root, declared
):
    """BLOCKING 3, reproduced: the rebuild-first flow after an out-of-band restore.

    ``assert_tree_writable`` returned immediately for a rebuild purpose, so a
    rebuild never ran the detection, while the fingerprint at the close of the
    membership write was recorded unconditionally. The rebuild was therefore the
    one governed write that UPDATED the evidence without ever checking it. The
    operator's first act is a rebuild, because that is what the product's own
    refusal text and the read-only check both tell them to do, and that act
    blessed the recovered fingerprint as canonical. A second native tree, emptied
    by the same restore, was then never flagged at all.
    """
    second_tree = "second_shelf"
    registry = tree_registry.Registry(
        (
            *_registry(str(adopted_root.ID)).trees,
            tree_registry.TreeRecord(
                tree_id=second_tree,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=date(2026, 8, 1),
                root_id="root-row-other",
                source=tree_registry.DerivationSource.TAXONOMY,
            ),
        )
    )
    _rebuild(cfg, db, adopted_root, declared, [PLAIN], registry=registry)
    recorded = convergence.read(cfg).fingerprint
    assert recorded is not None

    # The out-of-band recovery, written straight into the file.
    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        conn.execute(
            "UPDATE AgentRegistry SET int_1 = ? WHERE registry_id = 'localUpdateCount'",
            (recorded.local_usn - 40,),
        )
        conn.commit()
    finally:
        conn.close()
    db.session.expire_all()

    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN], registry=registry)

    # The tree that was rebuilt converged on a real check, so its own flag is
    # cleared. Every OTHER native tree the same database owns stays flagged.
    assert report.after.converged and report.cleared
    assert convergence.read(cfg).blocking_trees() == (second_tree,)
    assert convergence.read(cfg).tree(second_tree).reason == str(
        convergence.Regression.SEQUENCE_WENT_BACKWARD
    )


def test_the_detection_marks_every_native_tree_on_disk_not_only_the_argument(
    cfg, gates_pass, db, adopted_root, declared
):
    """"EVERY DATABASE-NATIVE TREE IS MARKED" was true only if the caller obliged.

    Nothing in ``src`` reads the registry from disk; it always arrives as an
    argument, so a caller passing the one record it cared about would have marked
    one tree and left the others in the same damaged database reporting
    themselves fine. Driven with a registry that names ONE tree while the file on
    disk names two.
    """
    on_disk = tree_registry.Registry(
        (
            *_registry(str(adopted_root.ID)).trees,
            tree_registry.TreeRecord(
                tree_id="third_shelf",
                mode=tree_registry.Mode.DATABASE,
                cutover_on=date(2026, 8, 1),
                root_id="root-row-third",
                source=tree_registry.DerivationSource.TAXONOMY,
            ),
        )
    )
    tree_registry.write(cfg, on_disk)
    convergence.record_fingerprint(cfg, db)

    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        conn.execute(
            "UPDATE AgentRegistry SET int_1 = 1 WHERE registry_id = 'localUpdateCount'"
        )
        conn.commit()
    finally:
        conn.close()
    db.session.expire_all()

    with pytest.raises(CratekitError):
        convergence.assert_no_out_of_band_restore(
            cfg, db, _registry(str(adopted_root.ID))
        )
    assert set(convergence.read(cfg).blocking_trees()) == {TREE_ID, "third_shelf"}


def test_the_rebuild_reports_that_the_other_record_was_not_reached(
    cfg, gates_pass, db, adopted_root, declared
):
    """TWO RECORDS FOR ONE FACT, and the honest third answer.

    ``cratekit.core.reconcile`` is U32's and is not part of this build, so the
    rebuild cannot close the marker it keeps. That absence is REPORTED rather
    than swallowed: None means the question could not be asked, which is a
    different fact from False, and reading one as the other is the defect shape
    this whole part is about.
    """
    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert report.cleared
    assert report.restore_marker_closed is None
    assert rebuild.close_restore_marker(cfg, TREE_ID) is None


def test_the_rebuild_declares_a_recovery_intent_so_the_restore_latch_lets_it_past(
    cfg, gates_pass, db, adopted_root, declared, monkeypatch
):
    """The second deadlock: a latch refusing the rebuild its own refusal names.

    ``reconcile.assert_converged`` sits inside ``session.assert_gates`` and
    refuses every ordinary destructive session while a restore marker is open,
    and the markers it refuses over include "this tree needs rebuilding". The
    membership write therefore declares ``RECOVERY``, exactly as a restore does.
    """
    seen: list[session.Intent] = []
    real = session.assert_gates

    def _record(*args, **kwargs):
        seen.append(kwargs.get("intent", session.Intent.WRITE))
        return real(*args, **kwargs)

    monkeypatch.setattr(session, "assert_gates", _record)
    _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert seen == [session.Intent.RECOVERY]


def test_a_rebuild_is_still_held_by_the_unresolved_session_latch(
    cfg, gates_pass, db, adopted_root, declared, monkeypatch
):
    """``RECOVERY`` lifts two latches and only one of them belongs to a rebuild.

    The unresolved-session latch names a RESTORE as its remedy, not a rebuild, so
    the rebuild asserts it by name rather than shedding it as a side effect of
    the intent it needs for the other one. A rebuild over a library whose last
    commit could not be read back would be adding to something nobody can vouch
    for.
    """
    def _refuse(_cfg):
        raise CratekitError(
            convergence.Cause(
                reason="session-committed-unverified",
                message="a session ended committed-unverified",
                remediation=convergence.Remediation(
                    remedy=convergence.Remedy.RESTORE_FROM_SNAPSHOT
                ),
                origin=("test",),
            )
        )

    monkeypatch.setattr(session, "assert_no_unresolved_session", _refuse)
    with pytest.raises(CratekitError) as excinfo:
        _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert excinfo.value.cause.reason == "session-committed-unverified"


# ── the readers that were reading too generously ─────────────────────────────


def test_a_boolean_update_count_is_not_a_number(cfg):
    """``isinstance(True, int)`` is True, so ``"local_usn": true`` read as usn 1.

    A fingerprint at usn 1 compares lower than every real database, so the next
    routine assertion saw no regression at all, silently, on the one number that
    says whether a library went backward.
    """
    with pytest.raises(ValueError):
        convergence.Fingerprint.from_json(
            {"schema_version": "6000", "active_rows": 10, "local_usn": True}
        )


def test_a_handle_with_no_session_cannot_defeat_the_autoflush_guard(cfg):
    """The one place a read can defeat a guard, closed rather than degraded.

    ``_no_autoflush`` degrades to a no-op deliberately, so a stand-in can drive
    a probe. Handing it ``getattr(db, "session", None)`` turned that documented
    degradation into a silent one for a whole class of handle.
    """

    class _NoSession:
        def get_content(self, **_kwargs):  # pragma: no cover - never reached
            raise AssertionError("the probe read the database outside the guard")

    with pytest.raises(CratekitError) as excinfo:
        convergence.probe(_NoSession())
    assert excinfo.value.cause.reason == "library-fingerprint-unreadable"


def test_a_count_answered_as_a_string_is_refused_rather_than_coerced(cfg, db):
    """``int(value)`` accepted ``"7"`` and ``True`` without comment.

    That is the defaulting-accessor shape this module's own docstring argues
    against for the row count, arriving one line below it.
    """

    class _Stringly:
        session = db.session

        def __init__(self, inner):
            self._inner = inner

        def get_content(self, **kwargs):
            return self._inner.get_content(**kwargs)

        def get_local_usn(self):
            return str(self._inner.get_local_usn())

    with pytest.raises(CratekitError) as excinfo:
        convergence.probe(_Stringly(db))
    assert excinfo.value.cause.detail["reading"] == "local update count"


def test_each_unreadable_reading_names_which_one_failed(cfg, db):
    """One try block around three reads produced one slug for three problems."""

    class _NoVersion:
        session = db.session

        def __init__(self, inner):
            self._inner = inner

        def get_content(self, **kwargs):
            return self._inner.get_content(**kwargs)

        def get_local_usn(self):
            return self._inner.get_local_usn()

    def _boom(_db):
        raise RuntimeError("the property table moved")

    import unittest.mock

    with unittest.mock.patch.object(rb_writer, "db_schema_version", _boom):
        with pytest.raises(CratekitError) as excinfo:
            convergence.probe(_NoVersion(db))
    assert excinfo.value.cause.detail["reading"] == "schema version"


def test_a_record_with_no_nodes_key_is_refused_like_one_with_a_null_nodes_key(cfg):
    """The two shapes were treated differently and neither reading is harmless.

    An absent key read as "nothing was ever recorded", which sends the next
    rebuild back to resolving destinations by display name. That is the exact
    resolution this record exists to replace, and after a rename it files the
    whole tree a second time.
    """
    with pytest.raises(ValueError, match="required"):
        convergence.TreeConvergence.from_json({"tree": TREE_ID, "unconverged": False})


def test_a_disposition_for_a_tree_that_is_not_refusing_anything_is_refused(cfg):
    """A signed acceptance of a difference nobody was ever shown.

    Worse than useless: it sits in the record as a standing answer, so the next
    restore that empties this tree is waved through by a judgement made before it
    happened. ``mark_unconverged`` clears an old disposition for the same reason.
    """
    with pytest.raises(CratekitError) as excinfo:
        convergence.clear_unconverged(
            cfg,
            TREE_ID,
            differences=(),
            disposition=convergence.Disposition(actor="a person"),
        )
    assert excinfo.value.cause.reason == "tree-unconverged"
    assert convergence.read(cfg).tree(TREE_ID) is None


def test_a_registry_record_with_no_mode_is_refused_rather_than_read_as_the_bridge(cfg):
    """One missing key switched the restore detector off for the whole library.

    A record keeping ``cutover_on``, ``root`` and ``source`` while losing
    ``mode`` read as ``Mode.XML``: ``is_on_the_bridge`` answered True, so the
    bridge writer would splice an export for a tree the database owns, and
    ``database_native_trees`` answered empty, which is the restore detector's
    whole input.
    """
    tree_registry.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    tree_registry.path_for(cfg).write_text(
        json.dumps(
            {
                "schema_version": tree_registry.SCHEMA_VERSION,
                "trees": [
                    {
                        "tree": TREE_ID,
                        "cutover_on": "2026-08-01",
                        "root": ADOPTED_ROOT,
                        "source": "taxonomy",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(CratekitError) as excinfo:
        tree_registry.read(cfg)
    assert excinfo.value.cause.reason == "tree-registry-unusable"


def test_a_bridge_record_carrying_a_cutover_contradicts_itself_and_is_refused():
    """The same contradiction from the other end, refused at construction."""
    with pytest.raises(ValueError, match="contradicts itself"):
        tree_registry.TreeRecord(
            tree_id=TREE_ID,
            mode=tree_registry.Mode.XML,
            cutover_on=date(2026, 8, 1),
            root_id=ADOPTED_ROOT,
            source=tree_registry.DerivationSource.TAXONOMY,
        )


def test_an_undeclared_destination_refuses_structurally_rather_than_by_key_error(
    cfg, gates_pass, db, adopted_root, declared
):
    """A bare ``KeyError`` reaches the boundary as "report a defect" (S4).

    A recorded destination outliving a template edit that removed the sub it
    named is ordinary, and the person holding it has a taxonomy to repair rather
    than a bug to file.
    """
    convergence.record_nodes(
        cfg,
        TREE_ID,
        [
            convergence.DestinationNode(
                bucket=_destination(declared)[0],
                sub="a_sub_this_taxonomy_never_declared",
                folder_id="f",
                playlist_id="p",
            )
        ],
    )
    with pytest.raises(CratekitError) as excinfo:
        _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert excinfo.value.cause.reason == "routing-destination-renamed"


def test_the_empty_derivation_reason_is_declared_in_the_one_vocabulary():
    """S4, for the slug this round adds."""
    assert REASONS["rebuild-derivation-empty"] is ExitCode.LIBRARY_PREREQUISITE


# ═══════════════════════════════════════════════════════════════════════════
# Part 10: the two surfaces, one landed and one still owed
# ═══════════════════════════════════════════════════════════════════════════


def test_the_read_only_verb_is_landed_and_the_destructive_one_is_not():
    """The wall has three independent parts and only ONE of them is the database.

    A verb is behind it if it declares an explicit gate, if it needs the
    one-gate-per-drive shape, or if it is a destructive database verb that cannot
    exit OK where no database exists. ``converge`` is none of the three: no
    gates, nothing destructive, nothing written. It was parked only because both
    convergence verbs named one module and the countdown keys on the module, and
    parking it parked the remedy both of this unit's refusals name.
    """
    converge_entry = registry.entry("converge")
    rebuild_entry = registry.entry("rebuild")
    assert converge_entry.landed and converge_entry.module == "cratekit.cli.converge"
    assert converge_entry.gates == () and not converge_entry.destructive
    assert converge_entry.writes == frozenset()
    assert not rebuild_entry.landed
    assert rebuild_entry.destructive and "db_tree" in rebuild_entry.writes
    assert rebuild_entry.module != converge_entry.module, (
        "one module for two verbs is what parked the read-only one"
    )


def test_the_landed_verb_opens_no_session_and_writes_no_state(cfg, db, adopted_root):
    """READ ONLY BY CONTRACT, asserted by driving it with every gate unanswered.

    The person reaching for this verb is by definition somebody whose library is
    refusing writes, so a diagnostic that took the acknowledgment, the lock or
    the session would be one they cannot reach at the only moment they need it.
    Asserted twice over: nothing in the module's source calls the session spine,
    and a real drive against a library with no acknowledgment recorded still
    answers.
    """
    source = Path(converge_cli.__file__).read_text(encoding="utf-8")
    for forbidden in ("assert_gates", "record_acknowledgment", "session_lock"):
        assert forbidden not in source, f"the read-only verb reaches for {forbidden}"

    tree_registry.write(cfg, _registry(str(adopted_root.ID)))
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    roots = (cfg.library.root, config.installation_state_dir(), config.config_dir())
    before = _state_fingerprint(*roots)

    class _Args:
        tree = None

    class _Ctx:
        args = _Args()

        @staticmethod
        def envelope(*, data, **kwargs):
            return {"data": data, **kwargs}

    result = converge_cli.converge(_Ctx())
    assert result["data"]["summary"]["blocking"] == [TREE_ID]
    assert _state_fingerprint(*roots) == before


def test_the_landed_verb_never_calls_an_uncompared_tree_converged(cfg, adopted_root):
    """The unit's own sentence, said at the surface.

    A tree whose database this build cannot open has NOT been compared, and the
    report says so with the reason attached. Reporting an empty comparison as a
    clean one is how a run tells somebody their damaged tree is fine.
    """
    tree_registry.write(cfg, _registry("root-row-nowhere"))
    Path(cfg.library.db_path).unlink(missing_ok=True)

    class _Args:
        tree = None

    class _Ctx:
        args = _Args()

        @staticmethod
        def envelope(*, data, **kwargs):
            return {"data": data, **kwargs}

    checks = converge_cli.converge(_Ctx())["data"]["checks"]
    assert [entry["status"] for entry in checks] == [converge_cli.NOT_COMPARED]
    assert converge_cli.MATCHING not in {entry["status"] for entry in checks}


@requires("cratekit.cli.rebuild")
def test_the_rebuild_verb_records_a_named_person_for_a_disposition():
    """The guard behind this unit's remaining register entry (P5).

    R39's escape hatch is an EXPLICIT, LOGGED operator disposition scoped to one
    tree. The engine already refuses an empty actor; what a surface can still do
    wrong is invent one, from the process owner or from the environment, which
    turns a person taking responsibility into the product deciding on their
    behalf. Driven against the module the moment it lands.
    """
    import importlib

    module = importlib.import_module("cratekit.cli.rebuild")
    source = Path(module.__file__).read_text(encoding="utf-8")
    for invented in ("getuser", "getlogin", "geteuid", "environ"):
        assert invented not in source, (
            f"the rebuild surface derives a disposition actor from {invented!r}; "
            f"an actor nobody typed is the product answering for the user"
        )
    assert "clear_unconverged" not in source, (
        "the surface clears a tree's flag directly rather than through the "
        "rebuild, whose clearing call is handed the check's own difference list"
    )
