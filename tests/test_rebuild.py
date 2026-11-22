"""The tree rebuild, the convergence check, and the record between them (U36).

A tree that has cut over lives only in the database, so a restore leaves it
short and nothing else notices; these tests cover noticing, reporting and
repairing. D1: nothing below names a real volume, person or track.
"""

from __future__ import annotations

import contextlib
import importlib
import importlib.util
import inspect
import json
import os
import sqlite3
import subprocess
import sys
import textwrap
import unicodedata
import unittest.mock
from dataclasses import dataclass, replace
from datetime import date
from enum import StrEnum
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
    tags,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import REASONS, CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.write import metadata_cli, rebuild, routing_pass, trees
from tests import deadca7_fixtures
from tests.test_active_taxonomy import write_active
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database

TREE_ID = "shelf_stack"
TREE_DISPLAY = "Shelf & Stack"
ADOPTED_ROOT = "root-row-7788"

#: One file name in each composition form, which the identity primitives exist for.
COMPOSED = "Café One.flac"
DECOMPOSED = unicodedata.normalize("NFD", COMPOSED)
PLAIN = "Second Track.flac"

#: A folder a person might rename a bucket to, with the space and "!" the locate must cover.
RENAMED_FOLDER = "Loud! Room"

#: A playlist nobody declared under the governed root: never a difference (P7).
CURATED_PLAYLIST = "Quiet? Corner"


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
    """Everything about THIS machine a temporary library cannot speak for."""
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


def _volume_agrees(cfg, monkeypatch):
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())


@pytest.fixture
def gates_pass(cfg, monkeypatch):
    """The volume identity agrees and the acknowledgment is recorded."""
    _volume_agrees(cfg, monkeypatch)
    session.record_acknowledgment(cfg, terminal=lambda: True)
    return cfg


@pytest.fixture
def declared():
    return taxonomy.default_taxonomy()


def _music(cfg, name: str) -> str:
    return f"{cfg.library.root}/Music/{name}"


def _record_locations(db_path: Path, recorded: dict[str, str]) -> None:
    """Give the rows this run's paths, before the guarded writer opens the file."""
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


def _disposable(cfg) -> Path:
    path = Path(cfg.library.db_path)
    _build_disposable_database(path)
    _record_locations(path, {"1": _music(cfg, COMPOSED), "2": _music(cfg, PLAIN)})
    return path


@contextlib.contextmanager
def _opened(cfg, monkeypatch, path):
    """The database at ``path``, opened through the gate, closed after."""
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer, "integrity_ok", lambda target, **kwargs: real_integrity_ok(target, unlock=False)
    )
    handle = rb_writer.open_db(path, unlock=False, cfg=cfg)
    try:
        yield handle
    finally:
        rb_writer.close_db(handle)


@pytest.fixture
def db(cfg, monkeypatch):
    """A disposable database in a temporary directory, opened through the gate."""
    with _opened(cfg, monkeypatch, _disposable(cfg)) as handle:
        yield handle


@pytest.fixture
def adopted_root(db):
    """The tree folder a cutover adopted, as a REAL row with a real identifier."""
    folder = rb_writer.ensure_folder(db, TREE_DISPLAY)
    db.session.commit()
    return folder


def _registry(root_id: str, *others, source=tree_registry.DerivationSource.TAXONOMY):
    """TREE_ID native under ``root_id``, and each ``(tree, root)`` of ``others`` beside it."""
    return tree_registry.Registry(
        tuple(
            tree_registry.TreeRecord(
                tree_id=tree_id,
                mode=tree_registry.Mode.DATABASE,
                cutover_on=date(2026, 8, 1),
                root_id=root,
                source=source,
            )
            for tree_id, root in ((TREE_ID, root_id), *others)
        )
    )


def _destination(declared_taxonomy):
    """Where the declared rules put an untagged, top-energy file, asked of the rules (R19)."""
    bucket_id = routing.resolve_bucket(declared_taxonomy, None).bucket_id
    sub = routing.energy_sub(declared_taxonomy, bucket_id, declared_taxonomy.energy.scale_max)
    assert sub is not None, "the shipped template declares no sub for the fallback"
    return bucket_id, sub.id


def _truth(cfg, declared_taxonomy, *names, voxlevel=None):
    """The tag readings for files the rules route to one destination."""
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
    return [rebuild.DeclaredPlacement(_music(cfg, name), bucket_id, sub_id) for name in names]


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
        rows=kwargs.pop("rows", _rows(cfg)),
        root_exists=lambda _root: True,
        **kwargs,
    )


def _report(cfg, db, adopted, declared_taxonomy, truth, vocal_threshold=None):
    return rebuild.report_convergence(
        cfg,
        db,
        tree_id=TREE_ID,
        registry=_registry(str(adopted.ID)),
        declared=declared_taxonomy,
        rows=_rows(cfg),
        root_exists=lambda _root: True,
        vocal_threshold=vocal_threshold,
        truth=truth,
    )


def _write_nothing(cfg, db, adopted):
    """A governed membership write with an empty plan, to meet its gates."""
    return trees.write_tree_membership(
        cfg,
        db,
        tree_id=TREE_ID,
        registry=_registry(str(adopted.ID)),
        plan={},
        rows=_rows(cfg),
        root_exists=lambda _root: True,
        analysis_roots=[Path(cfg.library.root) / "Music"],
    )


def _out_of_band(cfg, db, statement: str, *params) -> None:
    """Change the database file behind the open handle, as something else would."""
    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        conn.execute(statement, params)
        conn.commit()
    finally:
        conn.close()
    db.session.expire_all()


def _membership_ids(db, playlist_id: str) -> set[str]:
    return {str(row.ContentID) for row in db.get_playlist_songs(PlaylistID=str(playlist_id))}


def _state_fingerprint(*roots) -> dict[str, tuple[int, int]]:
    """Size and modification time of every file under each root, to see a refusal that wrote."""
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


def test_a_tree_may_not_flip_on_a_source_no_rebuild_can_reproduce(cfg):
    """R39: a native tree cannot be imported over, so one no source reproduces has no repair."""
    for source in sorted(tree_registry.NOT_REBUILDABLE):
        with pytest.raises(tree_registry.TreeModeRefused) as excinfo:
            tree_registry.record_cutover(
                cfg, TREE_ID, root_id=ADOPTED_ROOT, on=date(2026, 8, 1), source=source
            )
        assert excinfo.value.tree_id == TREE_ID
        assert tree_registry.read(cfg).is_on_the_bridge(TREE_ID)


def test_a_native_record_naming_no_derivation_source_cannot_be_constructed():
    """The same rule structurally, so no construction path can skip it."""
    with pytest.raises(ValueError, match="derivation source"):
        tree_registry.TreeRecord(
            tree_id=TREE_ID,
            mode=tree_registry.Mode.DATABASE,
            cutover_on=date(2026, 8, 1),
            root_id=ADOPTED_ROOT,
        )


def test_every_rebuildable_source_has_a_derivation_and_no_other_source_does():
    """The two halves are derived from each other, so neither can drift (P3, P4)."""
    assert set(rebuild.DERIVATIONS) == set(tree_registry.REBUILDABLE)
    assert tree_registry.REBUILDABLE | tree_registry.NOT_REBUILDABLE == set(
        tree_registry.DerivationSource
    )
    assert not (tree_registry.REBUILDABLE & tree_registry.NOT_REBUILDABLE)


def test_a_rebuild_of_a_tree_with_a_non_derivable_source_refuses(
    cfg, gates_pass, db, adopted_root, declared
):
    """Asked again at the rebuild, because a registry can be edited by hand."""
    registry = _registry(str(adopted_root.ID), source=tree_registry.DerivationSource.CURATED)
    with pytest.raises(tree_registry.TreeModeRefused):
        _rebuild(cfg, db, adopted_root, declared, [PLAIN], registry=registry)


def test_the_derivation_routes_a_file_through_the_declared_rules(declared):
    """The rules are CALLED rather than restated, so there is one answer."""
    truth = [rebuild.Truth(location="/x/one.flac", genre=None, energy=None)]
    placements, gaps = rebuild.derive_from_taxonomy(declared, truth, vocal_threshold=None)
    expected_bucket = routing.resolve_bucket(declared, None).bucket_id
    assert [entry.bucket for entry in placements] == [expected_bucket]
    assert rebuild.VOCAL_DIMENSION in gaps


def test_a_vocal_track_lands_in_its_energy_sub_AND_the_additive_one(declared):
    """Additive means two placements, so "missing from one of its two" stays expressible."""
    truth = [rebuild.Truth(location="/x/one.flac", genre=None, energy=9, voxlevel=90)]
    placements, gaps = rebuild.derive_from_taxonomy(declared, truth, vocal_threshold=5.0)
    subs = {entry.sub for entry in placements}
    assert trees.VOX_SUB_CLASS in subs
    assert len(subs) == 2
    assert gaps == ()


def test_an_additive_sub_playlist_with_no_signal_refuses_rather_than_being_skipped(
    declared,
):
    """P4: skipping it would write a tree missing a dimension and report it converged."""
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
    """The suffix set comes from the tag module, so no format is silently absent (P3)."""
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


def test_the_check_reports_a_difference_in_both_directions(
    cfg, gates_pass, db, adopted_root, declared
):
    """R39: one track placed and not held, one held and not placed there."""
    both = _placements(cfg, declared, COMPOSED, PLAIN)
    _rebuild(cfg, db, adopted_root, declared, [COMPOSED, PLAIN])

    # The declaration now names one of the two; the other still held is the second direction.
    report = _check(cfg, db, adopted_root, declared, _placements(cfg, declared, COMPOSED))
    assert report.missing == ()
    assert [entry.content_id for entry in report.unexpected] == ["2"]
    # Named by its file as well (R-312): a person finds a track by its file, not its row.
    (leftover,) = report.unexpected
    assert leftover.location is not None and leftover.location.endswith(PLAIN), leftover

    # And the first direction: a widened declaration makes the database short.
    assert _check(cfg, db, adopted_root, declared, both).converged
    third = rebuild.DeclaredPlacement(_music(cfg, "Third Track.flac"), *_destination(declared))
    rows = [*_rows(cfg), trees.ContentRow("3", third.location, deleted=False)]
    widened = _check(cfg, db, adopted_root, declared, [*both, third], rows=rows)
    assert [entry.content_id for entry in widened.missing] == ["3"]


def test_a_declared_file_the_library_has_no_row_for_is_surfaced_and_is_not_a_difference(
    cfg, gates_pass, db, adopted_root, declared
):
    """Counting a row the library lacks would make convergence unreachable before an import."""
    absent = rebuild.DeclaredPlacement(_music(cfg, "Never Imported.flac"), *_destination(declared))
    report = _check(cfg, db, adopted_root, declared, [absent])
    assert report.converged
    assert [match.outcome for match in report.unmatched] == [trees.MatchOutcome.ABSENT]


def test_a_membership_pointing_at_a_soft_deleted_row_is_not_a_difference_either(
    cfg, gates_pass, db, adopted_root, declared
):
    """A membership on a deleted track is a leftover nobody can act on; counting it latches forever."""
    _rebuild(cfg, db, adopted_root, declared, [COMPOSED, PLAIN])

    tombstoned = [
        trees.ContentRow("1", _music(cfg, COMPOSED), deleted=True),
        trees.ContentRow("2", _music(cfg, PLAIN), deleted=False),
    ]
    report = _check(
        cfg, db, adopted_root, declared, _placements(cfg, declared, PLAIN), rows=tombstoned
    )
    assert report.converged, "a tombstone's leftover membership was called a difference"


def test_a_playlist_nobody_declared_is_reported_and_is_not_a_difference(
    cfg, gates_pass, db, adopted_root, declared
):
    """P7: a person's own playlist under a governed tree is theirs, not damage."""
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
    """A walk by display name would read a namesake and call a short tree complete."""
    elsewhere = rb_writer.ensure_folder(db, TREE_DISPLAY + " Copy")
    folder_display, sub_display = routing_pass.destination(declared, *_destination(declared))
    decoy_folder = rb_writer.ensure_folder(db, folder_display, parent=elsewhere)
    decoy = rb_writer.ensure_playlist(db, sub_display, decoy_folder)
    rb_writer.add_membership(db, decoy, "2")
    db.session.commit()

    report = _check(cfg, db, adopted_root, declared, _placements(cfg, declared, PLAIN))
    assert [entry.content_id for entry in report.missing] == ["2"]
    assert not report.converged


def test_a_tree_stripped_of_its_membership_rebuilds_to_match_the_control(
    cfg, gates_pass, db, adopted_root, declared
):
    """The plan's first scenario, asserted against a CONTROL set rather than a count."""
    names = [COMPOSED, PLAIN]
    _rebuild(cfg, db, adopted_root, declared, names)

    nodes = rebuild.read_tree(db, str(adopted_root.ID))
    assert len(nodes) == 1
    control = dict(nodes[0].content_ids and {nodes[0].playlist_id: nodes[0].content_ids})
    assert control[nodes[0].playlist_id] == frozenset({"1", "2"})

    # The damage: every membership row under the tree, removed out of band.
    _out_of_band(cfg, db, "DELETE FROM djmdSongPlaylist WHERE PlaylistID = ?", nodes[0].playlist_id)
    assert _membership_ids(db, nodes[0].playlist_id) == set()

    report = _rebuild(cfg, db, adopted_root, declared, names)
    assert report.before.missing != ()
    assert report.after.converged
    assert _membership_ids(db, nodes[0].playlist_id) == control[nodes[0].playlist_id]


def test_the_rebuild_derives_its_own_placements_and_will_not_take_a_list(
    cfg, gates_pass, db, adopted_root, declared
):
    """No ``placements`` parameter: the seam is the tag READINGS, never the answer."""
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
    """The additive dimension end to end: the vocal sub is a destination a rebuild creates."""
    truth = _truth(cfg, declared, PLAIN, voxlevel=90)
    _rebuild(cfg, db, adopted_root, declared, [PLAIN], truth=truth, vocal_threshold=5.0)
    landed = {node.playlist_display for node in rebuild.read_tree(db, str(adopted_root.ID))}
    assert declared.sub_class(trees.VOX_SUB_CLASS).display in landed
    assert len(landed) == 2


def test_a_genre_sub_is_created_once_beside_the_band_and_a_second_rebuild_plans_nothing(
    cfg, gates_pass, db, adopted_root, declared
):
    """U155: a Rominimal track lands in its band and genre sub, a Minimal one in the band alone."""
    truth = [
        rebuild.Truth(location=_music(cfg, COMPOSED), genre="Rominimal", energy=3, voxlevel=None),
        rebuild.Truth(location=_music(cfg, PLAIN), genre="Minimal", energy=3, voxlevel=None),
    ]
    first = _rebuild(cfg, db, adopted_root, declared, [], truth=truth)
    second = _rebuild(cfg, db, adopted_root, declared, [], truth=truth)

    nodes = {
        (node.folder_display, node.playlist_display): node.content_ids
        for node in rebuild.read_tree(db, str(adopted_root.ID))
    }
    assert nodes == {
        ("Minimal / Deep Tech", "Low Energy"): frozenset({"1", "2"}),
        ("Minimal / Deep Tech", "Rominimal"): frozenset({"1"}),
    }
    assert first.repaired == 3
    assert second.repaired == 0
    assert second.after.converged


def test_a_library_with_no_vocal_calibration_reports_what_it_did_not_compare(
    cfg, gates_pass, db, adopted_root, declared
):
    """None is a real threshold (D7); naming the dimension keeps "converged" honest."""
    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN], vocal_threshold=None)
    assert report.after.converged
    assert rebuild.VOCAL_DIMENSION in report.after.not_compared


def test_a_vocal_playlist_nothing_compared_is_not_named_as_left_behind(
    cfg, gates_pass, db, adopted_root, declared
):
    """"I could not observe" must not reach a person as "take this out" (R-312)."""
    truth = _truth(cfg, declared, PLAIN, voxlevel=90)
    _rebuild(cfg, db, adopted_root, declared, [PLAIN], truth=truth, vocal_threshold=5.0)
    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN], truth=truth, vocal_threshold=None)
    assert [entry.sub for entry in report.after.unexpected] == [trees.VOX_SUB_CLASS]
    assert rebuild.left_behind(report.after, declared) == ()

    # Calibrated again and below the cut, it is a leftover somebody can act on, and named.
    quiet = _truth(cfg, declared, PLAIN, voxlevel=0)
    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN], truth=quiet, vocal_threshold=5.0)
    assert [entry.sub for entry in rebuild.left_behind(report.after, declared)] == [
        trees.VOX_SUB_CLASS
    ]


def test_the_read_only_report_derives_through_the_registrys_recorded_source(
    cfg, gates_pass, db, adopted_root, declared
):
    """The diagnostic and the repair derive the same way, or they disagree."""
    _rebuild(cfg, db, adopted_root, declared, [COMPOSED, PLAIN])
    report = _report(cfg, db, adopted_root, declared, _truth(cfg, declared, COMPOSED, PLAIN))
    assert report.converged
    assert report.root_id == str(adopted_root.ID)


def test_a_second_rebuild_writes_nothing(cfg, gates_pass, db, adopted_root, declared):
    """Re-running is the recovery procedure."""
    names = [COMPOSED, PLAIN]
    first = _rebuild(cfg, db, adopted_root, declared, names)
    second = _rebuild(cfg, db, adopted_root, declared, names)

    assert first.repaired == 2
    assert second.repaired == 0
    assert second.membership is not None and second.membership.already_present == 2
    assert second.after.converged


@pytest.fixture(params=["ordinary", "zero-date-west-of-utc"])
def pushed(request, cfg, monkeypatch):
    """The database with a DEADCA7 push of both tracks, ordinary or zero dated west of UTC (U285)."""
    zero = request.param != "ordinary"
    stamp = deadca7_fixtures.ZERO_STAMP if zero else deadca7_fixtures.STAMP
    with deadca7_fixtures.west_of_utc() if zero else contextlib.nullcontext():
        path = _disposable(cfg)
        push = deadca7_fixtures.push(path, ("1", "2"), stamp=stamp)
        with _opened(cfg, monkeypatch, path) as handle:
            yield handle, path, push


def test_a_rebuild_and_its_check_beside_deadca7s_folder_leave_it_and_report_no_drift(
    cfg, gates_pass, pushed, declared
):
    """U185: beside the push's own folder, rebuilds converge and leave all it wrote byte for byte."""
    db, path, push = pushed
    before = deadca7_fixtures.written(path, push)
    # The push's grid and waveform files, under the root the rebuild watches.
    files = deadca7_fixtures.push_analysis_files(Path(cfg.library.root) / "Music")
    # The pushed track, its analysis path changed by the push, is not a moved file.
    for name in (COMPOSED, PLAIN):
        Path(_music(cfg, name)).parent.mkdir(parents=True, exist_ok=True)
        Path(_music(cfg, name)).write_bytes(b"audio")
    assert metadata_cli.resolution_totals(cfg, db).unresolved == 0
    adopted = rb_writer.ensure_folder(db, TREE_DISPLAY)
    db.session.commit()
    names = [COMPOSED, PLAIN]
    first = _rebuild(cfg, db, adopted, declared, names)
    second = _rebuild(cfg, db, adopted, declared, names)
    assert first.repaired == 2 and second.repaired == 0
    report = _check(cfg, db, adopted, declared, _placements(cfg, declared, *names))
    assert report.converged
    assert not report.missing and not report.unexpected and not report.foreign
    assert deadca7_fixtures.written(path, push) == before
    assert deadca7_fixtures.analysis_files_now(files) == files


def test_a_rebuild_after_a_rename_converges_rather_than_doubling_the_tree(
    cfg, gates_pass, db, adopted_root, declared
):
    """The one that doubles a library, so node identifiers persist; counted, since a name lookup hides it."""
    names = [COMPOSED, PLAIN]
    _rebuild(cfg, db, adopted_root, declared, names)
    before = rebuild.read_tree(db, str(adopted_root.ID))
    assert len(before) == 1

    # Somebody renames the bucket folder in rekordbox; the taxonomy does not change.
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
    """The first rebuild after a cutover has nothing recorded, and must adopt."""
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
    """The operation that repairs a damaged tree must not be broken by the damage."""
    bucket_id, sub_id = _destination(declared)
    gone = convergence.DestinationNode(
        bucket=bucket_id, sub=sub_id, folder_id="gone-1", playlist_id="gone-2"
    )
    convergence.record_nodes(cfg, TREE_ID, [gone])
    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert report.after.converged
    assert rebuild.read_tree(db, str(adopted_root.ID))[0].content_ids == frozenset({"2"})


def test_a_rebuild_never_removes_a_membership_the_declaration_does_not_place(
    cfg, gates_pass, db, adopted_root, declared
):
    """Additive on purpose: a membership made by hand is somebody's data."""
    _rebuild(cfg, db, adopted_root, declared, [COMPOSED, PLAIN])
    report = _rebuild(cfg, db, adopted_root, declared, [COMPOSED])

    nodes = rebuild.read_tree(db, str(adopted_root.ID))
    assert nodes[0].content_ids == frozenset({"1", "2"}), "a rebuild deleted a membership"
    assert [entry.content_id for entry in report.after.unexpected] == ["2"]
    assert not report.cleared


def test_a_rebuild_refuses_without_the_acknowledgment(
    cfg, db, adopted_root, declared, monkeypatch
):
    """A rebuild is a destructive session, and its refusal leaves no trace in the state tree."""
    _volume_agrees(cfg, monkeypatch)
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
    monkeypatch.setattr(preflight, "default_identity_provider", lambda: (lambda _path: "0000-0000"))
    with pytest.raises(CratekitError) as excinfo:
        _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE


#: What a restore outside this product does to the database's update count.
_SET_USN = "UPDATE AgentRegistry SET int_1 = ? WHERE registry_id = 'localUpdateCount'"


def _fingerprint(*, rows: int, usn: int) -> convergence.Fingerprint:
    return convergence.Fingerprint(schema_version="6000", active_rows=rows, local_usn=usn)


def test_ordinary_rekordbox_use_is_not_a_regression():
    """P7: an import moves the row count and the update count forward together."""
    previous = _fingerprint(rows=100, usn=500)
    assert convergence.regression(previous, _fingerprint(rows=140, usn=560)) is None
    assert convergence.regression(previous, _fingerprint(rows=90, usn=560)) is None
    assert convergence.regression(previous, previous) is None


def test_nothing_recorded_yet_is_not_a_regression():
    """A fresh install has nothing to compare, so nothing is marked."""
    assert convergence.regression(None, _fingerprint(rows=1, usn=1)) is None


@pytest.mark.parametrize(
    "current, expected",
    [
        (_fingerprint(rows=100, usn=400), convergence.Regression.SEQUENCE_WENT_BACKWARD),
        (_fingerprint(rows=90, usn=500), convergence.Regression.ROWS_MOVED_AT_A_STANDSTILL),
    ],
)
def test_a_database_that_went_backward_is_detected(current, expected):
    """Two shapes; a standstill sequence beside a moved row count is two databases."""
    assert convergence.regression(_fingerprint(rows=100, usn=500), current) is expected


def test_the_probe_reads_the_three_numbers_out_of_a_real_database(cfg, db):
    """The row count is filtered at the database, never defaulting a tombstone to "not deleted"."""
    taken = convergence.probe(db)
    assert taken.active_rows == 2
    assert taken.local_usn == db.get_local_usn()
    assert taken.schema_version == rb_writer.db_schema_version(db)

    _out_of_band(cfg, db, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = '1'")
    assert convergence.probe(db).active_rows == 1


def test_a_database_that_cannot_answer_refuses_with_a_structured_cause(cfg, db):
    """S4: a moved schema is not a defect to report, so it carries a structured cause."""

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
    """Taken AFTER the commit, through the one writer every membership write uses."""
    assert convergence.read(cfg).fingerprint is None
    _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    recorded = convergence.read(cfg).fingerprint
    assert recorded is not None
    assert recorded.local_usn == db.get_local_usn()
    assert recorded.taken


def test_an_out_of_band_restore_marks_every_native_tree_and_refuses_the_next_write(
    cfg, gates_pass, db, adopted_root, declared
):
    """The case atomic snapshots cannot see: only the number inside the database."""
    _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    recorded = convergence.read(cfg).fingerprint
    assert recorded is not None

    _out_of_band(cfg, db, _SET_USN, recorded.local_usn - 5)

    with pytest.raises(CratekitError) as excinfo:
        _write_nothing(cfg, db, adopted_root)
    assert excinfo.value.cause.reason == "tree-unconverged"
    assert excinfo.value.cause.code is ExitCode.UNCONVERGED

    record = convergence.read(cfg).tree(TREE_ID)
    assert record is not None and record.blocking
    assert record.reason == str(convergence.Regression.SEQUENCE_WENT_BACKWARD)


def test_a_library_with_nothing_flipped_never_probes_at_all(cfg, declared):
    """A handle that raises on any read tells "did not probe" from "probed and found nothing"."""

    class _Exploding:
        def __getattr__(self, name):  # pragma: no cover - the point is it is unused
            raise AssertionError(f"the convergence check touched the database ({name})")

    convergence.assert_no_out_of_band_restore(cfg, _Exploding(), tree_registry.EMPTY)


def test_a_rebuild_is_not_refused_by_the_flag_it_exists_to_clear(
    cfg, gates_pass, db, adopted_root, declared
):
    """A latch that condemned its own remedy would leave a library with no exit."""
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    assert convergence.read(cfg).tree(TREE_ID).blocking

    with pytest.raises(CratekitError):
        _write_nothing(cfg, db, adopted_root)

    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert report.cleared
    assert not convergence.read(cfg).tree(TREE_ID).blocking


def test_the_rebuild_purpose_sheds_the_convergence_latches_and_nothing_else(
    cfg, db, adopted_root, declared, monkeypatch
):
    """The exemption is one pair of gates wide; the session spine still applies."""
    _volume_agrees(cfg, monkeypatch)
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")

    with pytest.raises(CratekitError) as excinfo:
        _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED


def _dispose(cfg, actor="an operator", **note) -> None:
    """A named person disposes of TREE_ID's one unexpected difference."""
    disposition = convergence.Disposition(actor=actor, **note)
    convergence.clear_unconverged(
        cfg, TREE_ID, differences=["unexpected:a/b:7"], disposition=disposition
    )


def test_a_flag_cannot_be_cleared_while_the_check_still_differs(cfg):
    """The refusal repeats the check's own list."""
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    with pytest.raises(CratekitError) as excinfo:
        convergence.clear_unconverged(cfg, TREE_ID, differences=["missing:a/b:7"])
    assert excinfo.value.cause.reason == "tree-unconverged"
    assert excinfo.value.cause.detail["differences"] == ["missing:a/b:7"]
    assert convergence.read(cfg).tree(TREE_ID).blocking


def test_a_named_person_can_dispose_of_a_difference_nothing_derives(cfg):
    """The one escape: the flag stays set and stops refusing, so a report still shows it."""
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    _dispose(cfg, note="filed by hand")
    record = convergence.read(cfg).tree(TREE_ID)
    assert record.unconverged and not record.blocking
    assert record.disposition.actor == "an operator"
    assert record.disposition.on, "a disposition records when it was taken"


def test_a_disposition_with_no_actor_is_refused():
    """A disposition is a person taking responsibility, so it names who."""
    with pytest.raises(ValueError, match="WHO decided"):
        convergence.Disposition(actor="  ")


def test_a_disposition_is_scoped_to_one_tree(cfg):
    """Answering for one tree must not wave through the next restore of another."""
    convergence.mark_unconverged(cfg, [TREE_ID, "other_tree"], reason="a restore")
    _dispose(cfg)
    state = convergence.read(cfg)
    assert not state.tree(TREE_ID).blocking
    assert state.tree("other_tree").blocking
    assert state.blocking_trees() == ("other_tree",)


def test_a_new_refusal_clears_an_old_disposition(cfg):
    """An acceptance covers the difference shown, never a later restore."""
    convergence.mark_unconverged(cfg, [TREE_ID], reason="first")
    _dispose(cfg)
    convergence.mark_unconverged(cfg, [TREE_ID], reason="second")
    record = convergence.read(cfg).tree(TREE_ID)
    assert record.disposition is None and record.blocking


def test_marking_twice_for_one_reason_keeps_the_date_the_damage_was_first_seen(cfg):
    """Re-running the detection must not keep moving the date forward to now."""
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    first = convergence.read(cfg).tree(TREE_ID).since
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    assert convergence.read(cfg).tree(TREE_ID).since == first


def _write_record(cfg, payload) -> None:
    """Write the convergence record by hand, as text or as data to serialise."""
    path = convergence.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload if isinstance(payload, str) else json.dumps(payload), encoding="utf-8")


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
    """A damaged record read as empty would report a damaged tree as fine and write that down."""
    _write_record(cfg, payload)
    with pytest.raises(convergence.ConvergenceStateUnreadable):
        convergence.read(cfg)


def test_a_record_from_a_newer_build_asks_for_an_upgrade_rather_than_the_doctor(cfg):
    """One slug covers every way the file is unusable; the REMEDY is what differs."""
    _write_record(cfg, {"schema_version": convergence.SCHEMA_VERSION + 1, "trees": []})
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
    """R19 and D5, against the BYTES: a record keyed on a name is orphaned by a rename."""
    node = convergence.DestinationNode(
        bucket="a_bucket", sub="a_sub", folder_id="f-1", playlist_id="p-1"
    )
    convergence.record_nodes(cfg, TREE_ID, [node])
    raw = convergence.path_for(cfg).read_text(encoding="utf-8")
    assert TREE_ID in raw and "a_bucket" in raw
    assert TREE_DISPLAY not in raw and RENAMED_FOLDER not in raw


def test_the_record_and_its_lock_are_declared_state_with_the_right_roles():
    """A record surviving a rollback would mislead; a lock in the coupled set would swap inodes."""
    entry = config.state_file(convergence.STATE_KEY)
    assert entry.snapshot is config.SnapshotRole.COUPLED
    assert entry.root is config.StateRoot.LIBRARY
    assert entry in config.coupled_state_files()

    lock = config.state_file(convergence.LOCK_KEY)
    assert lock.snapshot is config.SnapshotRole.NEVER_RESTORED
    assert lock not in config.coupled_state_files()


def test_the_lock_serializes_a_read_modify_write_across_processes(cfg):
    """A rename is atomic and the cycle around it is not; real processes, as a held lock proves nothing."""
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
    # Disjoint names per worker: over one shared set a lost write would hide behind another's.
    running = [subprocess.Popen([sys.executable, "-c", source, str(index)]) for index in range(workers)]
    for worker in running:
        assert worker.wait() == 0

    recorded = convergence.read(cfg).blocking_trees()
    lost = workers * per_worker + 1 - len(recorded)
    assert lost == 0, f"{lost} record(s) were lost to an interleaved read-modify-write"


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
    """S4: a refusal with no reserved code collapses to a bare status."""
    assert REASONS["tree-convergence-unusable"] is ExitCode.LIBRARY_UNREADABLE
    assert REASONS["rebuild-derivation-incomplete"] is ExitCode.LIBRARY_PREREQUISITE
    assert REASONS["library-fingerprint-unreadable"] is ExitCode.LIBRARY_UNREADABLE


def test_the_two_composition_forms_of_one_filename_are_one_track(
    cfg, gates_pass, db, adopted_root, declared
):
    """The 144-file loss at the check: macOS decomposes, rekordbox precomposes."""
    bucket_id, sub_id = _destination(declared)
    _rebuild(cfg, db, adopted_root, declared, [COMPOSED])
    decomposed = rebuild.DeclaredPlacement(_music(cfg, DECOMPOSED), bucket_id, sub_id)
    report = _check(cfg, db, adopted_root, declared, [decomposed])
    assert report.converged
    assert report.unmatched == ()


def _energy_truth(cfg, declared_taxonomy, pairs):
    """Readings that place named files at named energies, so two subs are used."""
    return [rebuild.Truth(location=_music(cfg, name), genre=None, energy=energy) for name, energy in pairs]


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
    """An empty music directory once gave zero placements, CONVERGED and a cleared flag."""
    _rebuild(cfg, db, adopted_root, declared, [COMPOSED, PLAIN])
    convergence.mark_unconverged(cfg, [TREE_ID], reason=str(convergence.Regression.SEQUENCE_WENT_BACKWARD))
    assert convergence.read(cfg).tree(TREE_ID).blocking

    with pytest.raises(CratekitError) as excinfo:
        # The empty music directory is read live rather than supplied.
        _rebuild(cfg, db, adopted_root, declared, [], truth=None)

    assert excinfo.value.cause.reason == "rebuild-derivation-empty"
    assert excinfo.value.cause.code is ExitCode.LIBRARY_PREREQUISITE
    assert convergence.read(cfg).tree(TREE_ID).blocking, "the flag was cleared"


def test_a_music_directory_that_is_not_there_refuses_rather_than_walking_nothing(
    cfg, gates_pass, db, adopted_root, declared
):
    """An unmounted volume is not an empty library."""
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
    """A destination that lost every placement once fell into ``foreign`` and read converged."""
    bucket_id, low_id, high_id = _two_destinations(declared)
    both = _energy_truth(cfg, declared, [(COMPOSED, 1), (PLAIN, declared.energy.scale_max)])
    first = _rebuild(cfg, db, adopted_root, declared, [], truth=both)
    assert first.after.converged
    assert len(rebuild.read_tree(db, str(adopted_root.ID))) == 2

    recorded = convergence.read(cfg).tree(TREE_ID)
    assert recorded.node(bucket_id, low_id) is not None
    assert recorded.node(bucket_id, high_id) is not None

    # The low-energy track leaves the derivation, so its destination has no placements.
    shrunk = _energy_truth(cfg, declared, [(PLAIN, declared.energy.scale_max)])
    report = _rebuild(cfg, db, adopted_root, declared, [], truth=shrunk)

    assert not report.after.converged, "a destination that emptied reported converged"
    assert not report.cleared
    assert [entry.content_id for entry in report.after.unexpected] == ["1"]
    assert f"{bucket_id}/{low_id}" not in " ".join(report.after.foreign)


def test_two_declared_destinations_on_one_display_pair_refuse(
    cfg, gates_pass, db, adopted_root, declared
):
    """Two destinations on one display pair would file into one playlist for good; refused as
    the XML side refuses it (U18), by the rebuild and by the read-only check."""
    both = _energy_truth(cfg, declared, [(COMPOSED, 1), (PLAIN, declared.energy.scale_max)])
    _rebuild(cfg, db, adopted_root, declared, [], truth=both)
    nodes = rebuild.read_tree(db, str(adopted_root.ID))
    assert len(nodes) == 2

    # One playlist renamed to the other's name: two destinations, one display pair.
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

    with pytest.raises(CratekitError):
        _report(cfg, db, adopted_root, declared, both)


def test_two_nodes_under_one_display_pair_refuse_the_way_the_xml_half_does(
    cfg, gates_pass, db, adopted_root, declared
):
    """A writer targeting by name would write the first twice and the second never."""
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
    """Injectivity in both directions: the map is read first on every rebuild."""
    bucket_id, low_id, high_id = _two_destinations(declared)

    def node(sub, folder_id, playlist_id):
        return convergence.DestinationNode(
            bucket=bucket_id, sub=sub, folder_id=folder_id, playlist_id=playlist_id
        )

    with pytest.raises(ValueError, match="one playlist row"):
        convergence.TreeConvergence(
            tree_id=TREE_ID, nodes=(node(low_id, "f1", "p1"), node(high_id, "f1", "p1"))
        )
    with pytest.raises(ValueError, match="two nodes for the destination"):
        convergence.TreeConvergence(
            tree_id=TREE_ID, nodes=(node(low_id, "f1", "p1"), node(low_id, "f2", "p2"))
        )


def test_the_recorded_node_is_the_one_the_destination_resolved_to(
    cfg, gates_pass, db, adopted_root, declared
):
    """The resolved identifier is never re-derived by name, asserted through a rename."""
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
    """A doubled row is invisible to set comparison and beyond an additive repair."""
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
    """A fingerprint recorded without the detection would bless a recovered database."""
    second_tree = "second_shelf"
    registry = _registry(str(adopted_root.ID), (second_tree, "root-row-other"))
    _rebuild(cfg, db, adopted_root, declared, [PLAIN], registry=registry)
    recorded = convergence.read(cfg).fingerprint
    assert recorded is not None

    _out_of_band(cfg, db, _SET_USN, recorded.local_usn - 40)

    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN], registry=registry)

    # The rebuilt tree's flag is cleared on a real check; every other native tree stays flagged.
    assert report.after.converged and report.cleared
    assert convergence.read(cfg).blocking_trees() == (second_tree,)
    assert convergence.read(cfg).tree(second_tree).reason == str(
        convergence.Regression.SEQUENCE_WENT_BACKWARD
    )


def test_the_detection_marks_every_native_tree_on_disk_not_only_the_argument(
    cfg, gates_pass, db, adopted_root, declared
):
    """Every native tree on disk is marked, whatever registry the caller passes."""
    on_disk = _registry(str(adopted_root.ID), ("third_shelf", "root-row-third"))
    tree_registry.write(cfg, on_disk)
    convergence.record_fingerprint(cfg, db)

    _out_of_band(cfg, db, _SET_USN, 1)

    with pytest.raises(CratekitError):
        convergence.assert_no_out_of_band_restore(cfg, db, _registry(str(adopted_root.ID)))
    assert set(convergence.read(cfg).blocking_trees()) == {TREE_ID, "third_shelf"}


def test_the_rebuild_reports_that_the_other_record_was_not_reached(
    cfg, gates_pass, db, adopted_root, declared
):
    """None where ``cratekit.core.reconcile`` is absent, False where nothing was marked to close."""
    present = importlib.util.find_spec("cratekit.core.reconcile") is not None
    report = _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert report.cleared
    expected = False if present else None
    assert report.restore_marker_closed is expected
    assert rebuild.close_restore_marker(cfg, TREE_ID) is expected


def test_the_rebuild_declares_a_recovery_intent_so_the_restore_latch_lets_it_past(
    cfg, gates_pass, db, adopted_root, declared, monkeypatch
):
    """The latch must not refuse the rebuild its refusal names, so the write declares ``RECOVERY``."""
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
    """``RECOVERY`` lifts two latches; this one names a restore, so it is put back."""
    def _refuse(_cfg):
        raise CratekitError(
            convergence.Cause(
                reason="session-committed-unverified",
                message="a session ended committed-unverified",
                remediation=convergence.Remediation(remedy=convergence.Remedy.RESTORE_FROM_SNAPSHOT),
                origin=("test",),
            )
        )

    monkeypatch.setattr(session, "assert_no_unresolved_session", _refuse)
    with pytest.raises(CratekitError) as excinfo:
        _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert excinfo.value.cause.reason == "session-committed-unverified"


def test_a_boolean_update_count_is_not_a_number(cfg):
    """``isinstance(True, int)``: a usn of 1 hides every regression."""
    with pytest.raises(ValueError):
        convergence.Fingerprint.from_json({"schema_version": "6000", "active_rows": 10, "local_usn": True})


def test_a_handle_with_no_session_cannot_defeat_the_autoflush_guard(cfg):
    """A handle with no session is refused rather than read outside the guard."""

    class _NoSession:
        def get_content(self, **_kwargs):  # pragma: no cover - never reached
            raise AssertionError("the probe read the database outside the guard")

    with pytest.raises(CratekitError) as excinfo:
        convergence.probe(_NoSession())
    assert excinfo.value.cause.reason == "library-fingerprint-unreadable"


class _Wrapped:
    """A probe handle that reads through to the real one."""

    def __init__(self, inner):
        self._inner = inner
        self.session = inner.session

    def get_content(self, **kwargs):
        return self._inner.get_content(**kwargs)

    def get_local_usn(self):
        return self._inner.get_local_usn()


def test_a_count_answered_as_a_string_is_refused_rather_than_coerced(cfg, db):
    """``int(value)`` accepted ``"7"`` and ``True`` without comment."""

    class _Stringly(_Wrapped):
        def get_local_usn(self):
            return str(self._inner.get_local_usn())

    with pytest.raises(CratekitError) as excinfo:
        convergence.probe(_Stringly(db))
    assert excinfo.value.cause.detail["reading"] == "local update count"


def test_each_unreadable_reading_names_which_one_failed(cfg, db):
    """One try block around three reads produced one slug for three problems."""

    def _boom(_db):
        raise RuntimeError("the property table moved")

    with unittest.mock.patch.object(rb_writer, "db_schema_version", _boom):
        with pytest.raises(CratekitError) as excinfo:
            convergence.probe(_Wrapped(db))
    assert excinfo.value.cause.detail["reading"] == "schema version"


def test_a_record_with_no_nodes_key_is_refused_like_one_with_a_null_nodes_key(cfg):
    """An absent key read as "nothing recorded" doubles the tree after a rename."""
    with pytest.raises(ValueError, match="required"):
        convergence.TreeConvergence.from_json({"tree": TREE_ID, "unconverged": False})


def test_a_disposition_for_a_tree_that_is_not_refusing_anything_is_refused(cfg):
    """An acceptance of nothing shown would wave the next restore through."""
    with pytest.raises(CratekitError) as excinfo:
        disposition = convergence.Disposition(actor="a person")
        convergence.clear_unconverged(cfg, TREE_ID, differences=(), disposition=disposition)
    assert excinfo.value.cause.reason == "tree-unconverged"
    assert convergence.read(cfg).tree(TREE_ID) is None


def test_a_registry_record_with_no_mode_is_refused_rather_than_read_as_the_bridge(cfg):
    """One missing ``mode`` read as XML and switched the restore detector off."""
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


def test_a_recorded_destination_the_taxonomy_dropped_is_reported_not_refused(
    cfg, gates_pass, db, adopted_root, declared
):
    """An ordinary taxonomy edit is not a one-way door: the rebuild and its check still answer."""
    bucket_id = _destination(declared)[0]
    dropped = convergence.DestinationNode(
        bucket=bucket_id, sub="a_sub_this_taxonomy_never_declared", folder_id="f", playlist_id="p"
    )
    convergence.record_nodes(cfg, TREE_ID, [dropped])
    report = _report(cfg, db, adopted_root, declared, _truth(cfg, declared, PLAIN))
    assert f"{bucket_id}/a_sub_this_taxonomy_never_declared" in report.undeclared

    rebuilt = _rebuild(cfg, db, adopted_root, declared, [PLAIN])
    assert rebuilt.after.converged and rebuilt.cleared
    assert rebuilt.after.undeclared != ()

    # The record keeps it, since a taxonomy edit is reversible.
    kept = convergence.read(cfg).tree(TREE_ID)
    assert kept.node(bucket_id, "a_sub_this_taxonomy_never_declared") is not None


def test_dropping_the_additive_sub_class_leaves_both_verbs_working(
    cfg, gates_pass, db, adopted_root, declared
):
    """Removing a recorded additive sub-class is curation; both verbs still answer."""
    def vocal(declared_taxonomy):
        return _truth(cfg, declared_taxonomy, PLAIN, voxlevel=90)

    _rebuild(cfg, db, adopted_root, declared, [PLAIN], truth=vocal(declared), vocal_threshold=5.0)
    bucket_id = _destination(declared)[0]
    assert convergence.read(cfg).tree(TREE_ID).node(bucket_id, trees.VOX_SUB_CLASS)

    trimmed = replace(declared, sub_classes=tuple(s for s in declared.sub_classes if not s.additive))

    report = _report(cfg, db, adopted_root, trimmed, vocal(trimmed), vocal_threshold=5.0)
    assert f"{bucket_id}/{trees.VOX_SUB_CLASS}" in report.undeclared

    again = _rebuild(cfg, db, adopted_root, trimmed, [PLAIN], truth=vocal(trimmed), vocal_threshold=5.0)
    assert again.after.converged
    # Re-declared, the kept record resolves again.
    restored = _rebuild(cfg, db, adopted_root, declared, [PLAIN], truth=vocal(declared), vocal_threshold=5.0)
    assert restored.after.converged
    assert len(rebuild.read_tree(db, str(adopted_root.ID))) == 2


def test_a_derived_placement_the_taxonomy_cannot_name_is_still_a_defect(declared):
    """One document contradicting itself keeps its refusal and its sentence."""
    assert rebuild._declared_display(declared, "no_such_bucket_at_all", "high", derived=False) is None
    with pytest.raises(CratekitError) as excinfo:
        rebuild._declared_display(declared, "no_such_bucket_at_all", "high", derived=True)
    assert excinfo.value.cause.reason == "routing-destination-renamed"


def test_the_empty_derivation_reason_is_declared_in_the_one_vocabulary():
    """S4, for the slug this round adds."""
    assert REASONS["rebuild-derivation-empty"] is ExitCode.LIBRARY_PREREQUISITE


class _Args:
    tree = None


class _Ctx:
    """The handler context the read-only verb reads: no tree named, a plain envelope."""

    args = _Args()

    @staticmethod
    def envelope(*, data, **kwargs):
        return {"data": data, **kwargs}


def _converge():
    return converge_cli.converge(_Ctx())


def test_the_read_only_verb_and_the_destructive_one_stay_in_separate_modules():
    """``converge`` has no gates and writes nothing; sharing ``rebuild``'s module parked it (U20)."""
    converge_entry = registry.entry("converge")
    rebuild_entry = registry.entry("rebuild")
    assert converge_entry.landed and converge_entry.module == "cratekit.cli.converge"
    assert converge_entry.gates == () and not converge_entry.destructive
    assert converge_entry.writes == frozenset()
    assert rebuild_entry.landed
    assert rebuild_entry.destructive and "db_tree" in rebuild_entry.writes
    assert rebuild_entry.module != converge_entry.module


def test_the_landed_verb_opens_no_session_and_writes_no_state(cfg, db, adopted_root):
    """Read only by contract, so it is driven with every gate unanswered."""
    source = Path(converge_cli.__file__).read_text(encoding="utf-8")
    for forbidden in ("assert_gates", "record_acknowledgment", "session_lock"):
        assert forbidden not in source, f"the read-only verb reaches for {forbidden}"

    tree_registry.write(cfg, _registry(str(adopted_root.ID)))
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    roots = (cfg.library.root, config.installation_state_dir(), config.config_dir())
    before = _state_fingerprint(*roots)

    result = _converge()
    assert result["data"]["summary"]["blocking"] == [TREE_ID]
    assert _state_fingerprint(*roots) == before


def test_the_landed_verb_never_calls_an_uncompared_tree_converged(cfg, adopted_root):
    """A tree whose database cannot be opened is reported NOT compared."""
    tree_registry.write(cfg, _registry("root-row-nowhere"))
    Path(cfg.library.db_path).unlink(missing_ok=True)

    checks = _converge()["data"]["checks"]
    assert [entry["status"] for entry in checks] == [converge_cli.NOT_COMPARED]
    assert converge_cli.MATCHING not in {entry["status"] for entry in checks}


def test_an_active_taxonomy_that_cannot_be_read_is_not_compared_and_opens_nothing(
    cfg, db, adopted_root, monkeypatch
):
    """R-685: an unreadable active taxonomy is not compared, asked before the database opens."""
    tree_registry.write(cfg, _registry(str(adopted_root.ID)))
    write_active(cfg, "this is = = not toml")
    opened = []
    monkeypatch.setattr(rb_writer, "open_db", lambda **kw: opened.append(kw))

    checks = _converge()["data"]["checks"]
    assert [entry["status"] for entry in checks] == [converge_cli.NOT_COMPARED]
    assert "taxonomy" in checks[0]["detail"]
    assert opened == []


def test_the_rebuild_verb_records_a_named_person_for_a_disposition():
    """P5: the surface never invents a disposition actor nobody typed."""
    module = importlib.import_module("cratekit.cli.rebuild")
    source = Path(module.__file__).read_text(encoding="utf-8")
    for invented in ("getuser", "getlogin", "geteuid", "environ"):
        assert invented not in source, f"the surface derives an actor from {invented!r}"
    # Only the rebuild clears a flag, handed the check's own difference list.
    assert "clear_unconverged" not in source


class _Kind(StrEnum):
    """U32's reconciliation kinds in a stand-in, so the rule is asserted, not U32's current answer."""

    EFFECT = "effect"
    IN_FLIGHT_RESTORE = "in-flight-restore"
    UNCONVERGED_TREE = "unconverged-tree"
    SOMETHING_LATER = "a-kind-added-after-this-was-written"


@dataclass(frozen=True)
class _Marker:
    kind: _Kind
    identity: str = "x"

    @property
    def marker_id(self) -> str:
        return f"{self.kind}:{self.identity}"


@dataclass(frozen=True)
class _Record:
    marker: _Marker


def _stand_in(monkeypatch, *kinds, latching=None):
    """Patch the guarded reconcile accessor with a module-shaped stand-in."""

    class _Module:
        Kind = _Kind

        @staticmethod
        def outstanding(_cfg):
            return tuple(_Record(_Marker(kind)) for kind in kinds)

    if latching is not None:
        _Module.LATCHING_KINDS = frozenset(latching)
    monkeypatch.setattr(rebuild, "_reconcile", lambda: _Module)
    return _Module


_E, _F, _T, _L = _Kind.EFFECT, _Kind.IN_FLIGHT_RESTORE, _Kind.UNCONVERGED_TREE, _Kind.SOMETHING_LATER


@pytest.mark.parametrize(
    "outstanding, latching, held",
    [
        # RECOVERY sheds the in-flight latch; a restore killed partway must still hold.
        pytest.param(_F, {_E, _F}, True, id="an in-flight restore holds"),
        # An effect is outside the library and no rebuild repairs it.
        pytest.param(_E, {_E, _F}, True, id="an effect holds"),
        # The one subtraction, by NAME: a tree marker's only remedy is this rebuild.
        pytest.param(_T, {_E, _F, _T}, False, id="a tree marker does not hold"),
        # Derived so a kind nobody classified lands on the side that refuses.
        pytest.param(_L, {_E, _F, _L}, True, id="a kind added later holds"),
        # An absent set is a shape this build cannot interrogate, not permission.
        pytest.param(_L, None, True, id="no latching set holds an unknown kind"),
        pytest.param(_T, None, False, id="no latching set still frees the tree kind"),
    ],
)
def test_the_latch_holds_every_kind_but_the_one_this_rebuild_answers(
    cfg, monkeypatch, outstanding, latching, held
):
    """What ``Intent.RECOVERY`` sheds, put back by derivation from the latch's own set."""
    _stand_in(monkeypatch, outstanding, latching=latching)
    if not held:
        rebuild.assert_no_latched_restore(cfg)
        return
    with pytest.raises(CratekitError) as excinfo:
        rebuild.assert_no_latched_restore(cfg)
    assert excinfo.value.cause.detail["kinds"] == [str(outstanding)]


def test_a_build_without_the_module_is_held_by_nothing_here(cfg, monkeypatch):
    """There is no latch to put back where there is no latch."""
    monkeypatch.setattr(rebuild, "_reconcile", lambda: None)
    rebuild.assert_no_latched_restore(cfg)


def test_the_rebuild_refuses_end_to_end_while_a_restore_is_in_flight(
    cfg, gates_pass, db, adopted_root, declared, monkeypatch
):
    """The whole rebuild refuses, writing no membership, fingerprint or clearing."""
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    _stand_in(monkeypatch, _Kind.IN_FLIGHT_RESTORE, latching={_Kind.EFFECT, _Kind.IN_FLIGHT_RESTORE})
    before = convergence.read(cfg).fingerprint

    with pytest.raises(CratekitError):
        _rebuild(cfg, db, adopted_root, declared, [PLAIN])

    assert convergence.read(cfg).tree(TREE_ID).blocking, "the flag was cleared"
    assert convergence.read(cfg).fingerprint == before, "a fingerprint was recorded"
    assert rebuild.read_tree(db, str(adopted_root.ID)) == ()


def test_the_diagnostic_survives_a_record_every_other_reader_refuses(cfg, adopted_root):
    """A corrupt node map refuses every reader, and the diagnostic a person is told to run answers."""
    tree_registry.write(cfg, _registry(str(adopted_root.ID)))
    tree = {
        "tree": TREE_ID,
        "unconverged": True,
        "reason": "a restore",
        "since": "2026-08-02",
        "disposition": None,
        "nodes": [
            {"bucket": "b", "sub": "one", "folder": "f", "playlist": "p"},
            {"bucket": "b", "sub": "two", "folder": "f", "playlist": "p"},
        ],
    }
    _write_record(cfg, {"schema_version": convergence.SCHEMA_VERSION, "fingerprint": None, "trees": [tree]})

    with pytest.raises(CratekitError):
        convergence.read(cfg)

    result = _converge()["data"]
    assert result["summary"]["record_readable"] is False
    assert converge_cli.MATCHING not in {entry["status"] for entry in result["checks"]}
    assert any(entry["key"] == "record.unreadable" for entry in result["checks"])
