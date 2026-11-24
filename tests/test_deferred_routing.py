"""Deferred routing, from the decision to the mark to the run that closes (U19).

Decided before the library holds a row, a placement can lose its decision, mark before
the commit, or close the run early. Paths keep a space and an accent (D1).
"""

from __future__ import annotations

import ast
import inspect
import json
import os
import sqlite3
import stat
import subprocess
import sys
import tomllib
import unicodedata
from dataclasses import replace
from datetime import date
from importlib import resources
from pathlib import Path
from typing import Iterator

import pytest
from pyrekordbox.db6 import tables

from cratekit.cli import registry as cli_registry
from cratekit.core import (
    config,
    convergence,
    locations,
    preflight,
    rb_writer,
    routing,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import REASONS, CratekitError
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.write import routing_pass, trees
from tests import _pending
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

TREE_ID = "shelf_stack"
TREE_DISPLAY = "Shelf & Stack"
ADOPTED_ROOT = "root-row-7788"
SESSION_ID = "s-0001"
#: The shipped template, which every test here routes by; read-only, so one is shared.
DECLARED = taxonomy.default_taxonomy()

#: One file name in each composition form; a ledger keyed on the raw string holds two records.
COMPOSED = "Café One.flac"
DECOMPOSED = unicodedata.normalize("NFD", COMPOSED)
PLAIN = "Second Track.flac"
THIRD = "Third Track.flac"


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
    pins = {"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"}
    resolved = config.from_dict(valid_data(library, rekordbox=pins))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    return resolved


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """Everything about THIS machine a temporary library cannot speak for."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer, "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )


@pytest.fixture(autouse=True)
def _release_process_locks():
    """No test may leave this process believing it still holds a session lock."""
    yield
    session._HELD.clear()


def _volume_agrees(cfg, monkeypatch):
    monkeypatch.setattr(preflight, "default_identity_provider", lambda: (lambda _path: cfg.library.volume_id))
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())


def _unlocked_integrity(monkeypatch):
    """An unencrypted fixture is asked unlocked, never via a verifier that could lie."""
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(rb_writer, "integrity_ok", lambda target, **kwargs: real_integrity_ok(target, unlock=False))


@pytest.fixture
def gates_pass(cfg, monkeypatch):
    """The volume identity agrees and the acknowledgment is recorded."""
    _volume_agrees(cfg, monkeypatch)
    session.record_acknowledgment(cfg, terminal=lambda: True)
    return cfg


def _refused_by(act, *positional, **keyword):
    """The cause ``act`` refuses with, failing when it does not."""
    with pytest.raises(CratekitError) as caught:
        act(*positional, **keyword)
    return caught.value.cause


def _music(cfg, name: str) -> str:
    return f"{cfg.library.root}/Music/{name}"


def _destination(declared_taxonomy, index: int = 0):
    """A bucket the shipped template declares, DERIVED rather than named, and a sub it has (R19)."""
    bucket = declared_taxonomy.buckets[index]
    sub = routing.energy_sub(declared_taxonomy, bucket.id, declared_taxonomy.energy.scale_max)
    assert sub is not None, f"the shipped template's bucket {index} declares no sub"
    return bucket.id, sub.id


def _intent(cfg, declared_taxonomy, name: str, *, session_id: str = SESSION_ID):
    bucket_id, sub_id = _destination(declared_taxonomy)
    location = _music(cfg, name)
    return routing_pass.RoutingIntent(
        track=routing_pass.track_id(location), session_id=session_id, location=location,
        tree=TREE_ID, bucket=bucket_id, sub=sub_id, decided="2026-08-02T00:00:00+00:00",
    )


def _not_yet_there(cfg, declared_taxonomy):
    """An intent for a file the library has no row for yet."""
    intent = replace(_intent(cfg, declared_taxonomy, PLAIN), location=_music(cfg, "Not Yet There.flac"))
    return replace(intent, track=routing_pass.track_id(intent.location))


def _filed_under(db, content_id: str):
    """The playlist and the folder above the row's membership, walked UP, never down by name."""
    membership = db.get_playlist_songs(ContentID=content_id).first()
    assert membership is not None, "the track reached no playlist"
    playlist = db.session.query(tables.DjmdPlaylist).filter_by(ID=membership.PlaylistID).one()
    return playlist, db.session.query(tables.DjmdPlaylist).filter_by(ID=playlist.ParentID).one()


def test_an_intent_is_readable_by_the_next_process_the_moment_it_is_decided(cfg):
    """A restarted process must be able to read what it believed."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    reloaded = routing_pass.read(cfg)
    assert [entry.location for entry in reloaded.for_session(SESSION_ID)] == [_music(cfg, PLAIN)]
    assert reloaded.for_session(SESSION_ID)[0].state is routing_pass.TrackState.INTENDED


def test_two_spellings_of_one_filename_are_one_record(cfg):
    """The 144-file loss, one layer up."""
    composed = _intent(cfg, DECLARED, COMPOSED)
    decomposed = _intent(cfg, DECLARED, DECOMPOSED)
    assert composed.track == decomposed.track
    routing_pass.record_intents(cfg, [composed])
    routing_pass.record_intents(cfg, [decomposed])
    assert len(routing_pass.read(cfg).for_session(SESSION_ID)) == 1


def test_outstanding_is_derived_from_status_rather_than_from_a_stored_flag(cfg):
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    track = routing_pass.read(cfg).for_session(SESSION_ID)[0].track
    assert [entry.track for entry in routing_pass.read(cfg).outstanding(SESSION_ID)] == [track]
    routing_pass.mark(cfg, [track], routing_pass.TrackState.ROUTED, session_id=SESSION_ID)
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()
    document = json.loads(routing_pass.path_for(cfg).read_text())
    record = document["intents"][0]
    assert "state" in record
    flags = [key for key, value in record.items() if isinstance(value, bool)]
    assert not flags, f"a stored flag {flags} would be a second answer to the state"


def test_every_status_is_either_settled_or_outstanding():
    """Derived by walking the enum, so the next state cannot fall between them (P3)."""
    for member in routing_pass.TrackState:
        assert (member in routing_pass.SETTLED) != (member in routing_pass.OUTSTANDING)
    assert routing_pass.OUTSTANDING == frozenset(routing_pass.TrackState) - routing_pass.SETTLED
    assert routing_pass.TrackState.INTENDED in routing_pass.OUTSTANDING


def test_no_taxonomy_display_name_reaches_the_persisted_record(cfg):
    """D5 and R19, asserted over the BYTES rather than over the shape."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    text = routing_pass.path_for(cfg).read_text()
    displays = {DECLARED.tree.display, DECLARED.intake.display}
    displays |= {bucket.display for bucket in DECLARED.buckets}
    displays |= {band.display for band in DECLARED.energy.bands}
    displays |= {entry.display for entry in DECLARED.sub_classes}
    for bucket in DECLARED.buckets:
        displays |= {sub.display for sub in bucket.subs}
    leaked = sorted(display for display in displays if display and display in text)
    assert not leaked, f"display names persisted into the routing ledger: {leaked}"


def test_the_ledger_and_every_directory_above_it_are_private_under_any_umask(cfg, monkeypatch):
    """P1. A file mode is meaningless without the directory mode."""
    previous = os.umask(0o000)
    try:
        routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    finally:
        os.umask(previous)
    path = routing_pass.path_for(cfg)
    assert stat.S_IMODE(path.stat().st_mode) == config.PRIVATE_FILE_MODE
    root = config.library_state_dir(cfg)
    current = path.parent
    while True:
        assert stat.S_IMODE(current.stat().st_mode) == config.PRIVATE_DIR_MODE, current
        if current == root:
            break
        current = current.parent


def test_an_absent_ledger_is_the_empty_one(cfg):
    """A library that has never deferred a routing decision is not a failure."""
    assert routing_pass.read(cfg) == routing_pass.EMPTY
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()


def test_acknowledging_without_a_named_actor_is_refused(cfg):
    """R34's shape, one layer up: somebody says a track is gone, not something."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    track = routing_pass.read(cfg).for_session(SESSION_ID)[0].track
    with pytest.raises(ValueError):
        routing_pass.acknowledge(cfg, [track], session_id=SESSION_ID, actor="   ")


def _row(cfg, name: str, content_id: str, *, deleted: bool = False):
    return trees.ContentRow(content_id, _music(cfg, name), deleted=deleted)


def _index(cfg, rows, *, prefix_map=()):
    return routing_pass.index_rows(rows, root=cfg.library.root, prefix_map=prefix_map)


def _placements(cfg, declared_taxonomy, intents, rows, *, prefix_map=()):
    index = _index(cfg, rows, prefix_map=prefix_map)
    return routing_pass.resolve_placements(
        intents, index, declared_taxonomy, root=cfg.library.root, prefix_map=prefix_map
    )


def test_every_sub_the_taxonomy_can_route_to_resolves_to_a_display_name():
    """P4. A derivation that replaces a list is checked against the real set."""
    produced = set()
    for bucket in DECLARED.buckets:
        for level in [None, *range(0, DECLARED.energy.scale_max + 1)]:
            sub = routing.energy_sub(DECLARED, bucket.id, level)
            if sub is not None:
                produced.add((bucket.id, sub.id))
    produced |= {
        (bucket.id, entry.id) for bucket in DECLARED.buckets for entry in DECLARED.sub_classes
    }
    assert produced, "the shipped template routes nowhere; the derivation is broken"
    for bucket_id, sub_id in sorted(produced):
        folder, sub = routing_pass.destination(DECLARED, bucket_id, sub_id)
        assert folder and sub


def test_a_sub_the_taxonomy_does_not_declare_refuses_rather_than_inventing_a_name():
    """An unresolvable identifier is a ledger and a template that disagree."""
    with pytest.raises(KeyError):
        routing_pass.destination(DECLARED, DECLARED.buckets[0].id, "a-sub-nobody-DECLARED")


def test_the_pass_matches_every_intent_against_rows_supplied_as_a_cursor(cfg):
    """The iterable consumed once, which is how the natural database read arrives."""
    intents = [_intent(cfg, DECLARED, PLAIN), _intent(cfg, DECLARED, THIRD)]
    rows = (row for row in (_row(cfg, PLAIN, "1"), _row(cfg, THIRD, "2")))
    placed = _placements(cfg, DECLARED, intents, rows)
    assert [item.placement for item in placed] == [routing_pass.Placement.RESOLVED] * 2


def test_a_track_with_no_row_at_all_is_not_imported_rather_than_withdrawn(cfg):
    intents = [_intent(cfg, DECLARED, PLAIN)]
    placed = _placements(cfg, DECLARED, intents, [])
    assert placed[0].placement is routing_pass.Placement.NOT_IMPORTED
    assert routing_pass.readiness(placed) is routing_pass.Readiness.NOT_READY


def test_a_location_reaching_only_soft_deleted_rows_is_withdrawn(cfg):
    intents = [_intent(cfg, DECLARED, PLAIN)]
    placed = _placements(cfg, DECLARED, intents, [_row(cfg, PLAIN, "1", deleted=True)])
    assert placed[0].placement is routing_pass.Placement.WITHDRAWN
    assert routing_pass.readiness(placed) is routing_pass.Readiness.READY


def test_a_tombstone_beside_a_live_row_resolves_cleanly(cfg):
    """The active-row rule, inherited rather than re-implemented."""
    intents = [_intent(cfg, DECLARED, PLAIN)]
    placed = _placements(cfg, DECLARED, intents, [_row(cfg, PLAIN, "1", deleted=True), _row(cfg, PLAIN, "2")])
    assert placed[0].placement is routing_pass.Placement.RESOLVED
    assert placed[0].content_id == "2"


def test_two_active_rows_on_one_location_are_ambiguous_and_never_written(cfg):
    intents = [_intent(cfg, DECLARED, PLAIN)]
    placed = _placements(cfg, DECLARED, intents, [_row(cfg, PLAIN, "1"), _row(cfg, PLAIN, "2")])
    assert placed[0].placement is routing_pass.Placement.AMBIGUOUS
    assert placed[0].content_ids == ("1", "2")
    assert placed[0].placement not in routing_pass.WRITABLE


def test_a_recorded_prefix_the_map_covers_resolves_to_its_row(cfg):
    """Both sides through one resolver, with the volume prefix map applied."""
    older = "/an/older/mount"
    intent = replace(_intent(cfg, DECLARED, PLAIN), location=f"{older}/Music/{PLAIN}")
    rules = [locations.PrefixRule(older, str(cfg.library.root))]
    placed = _placements(cfg, DECLARED, [intent], [_row(cfg, PLAIN, "1")], prefix_map=rules)
    assert placed[0].placement is routing_pass.Placement.RESOLVED
    assert placed[0].content_id == "1"


def test_a_composition_form_mismatch_between_the_ledger_and_the_row_resolves(cfg):
    intent = _intent(cfg, DECLARED, DECOMPOSED)
    placed = _placements(cfg, DECLARED, [intent], [_row(cfg, COMPOSED, "1")])
    assert placed[0].placement is routing_pass.Placement.RESOLVED


def test_readiness_over_nothing_pending_is_ready_rather_than_not_ready(cfg):
    """A run with nothing to route is not a run waiting for an import."""
    assert routing_pass.readiness(()) is routing_pass.Readiness.READY


def test_a_partly_imported_run_is_ready_and_places_only_what_arrived(cfg):
    """The real shape of a run somebody imported in two goes."""
    intents = [_intent(cfg, DECLARED, PLAIN), _intent(cfg, DECLARED, THIRD)]
    placed = _placements(cfg, DECLARED, intents, [_row(cfg, PLAIN, "1")])
    assert routing_pass.readiness(placed) is routing_pass.Readiness.READY
    assert [item.placement for item in placed] == [
        routing_pass.Placement.RESOLVED, routing_pass.Placement.NOT_IMPORTED
    ]


def _registry(mode: tree_registry.Mode, *, root_id: str | None = ADOPTED_ROOT):
    if mode is tree_registry.Mode.DATABASE:
        record = tree_registry.TreeRecord(
            tree_id=TREE_ID, mode=mode, cutover_on=date(2026, 8, 1), root_id=root_id,
            source=tree_registry.DerivationSource.TAXONOMY,
        )
        return tree_registry.Registry((record,))
    return tree_registry.Registry((tree_registry.TreeRecord(tree_id=TREE_ID, mode=mode),))


def _record_locations(db_path: Path, recorded: dict[str, str], *, removed=frozenset()):
    """Give the disposable database's collection rows the paths this run decided on."""
    conn = sqlite3.connect(db_path)
    try:
        for content_id, path in recorded.items():
            conn.execute(
                "UPDATE djmdContent SET FolderPath = ?, rb_local_deleted = ? WHERE ID = ?",
                (path, 1 if content_id in removed else 0, content_id),
            )
        conn.commit()
    finally:
        conn.close()


def _state_fingerprint(*roots) -> dict[str, tuple[int, int]]:
    """Size and modification time of every file under each root."""
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


@pytest.fixture
def db(cfg, monkeypatch):
    """A disposable database in a temporary directory, opened through the gate."""
    path = Path(cfg.library.db_path)
    _build_disposable_database(path)
    _record_locations(path, {"1": _music(cfg, COMPOSED), "2": _music(cfg, PLAIN)})
    _unlocked_integrity(monkeypatch)
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


@pytest.fixture
def gated_root(gates_pass, adopted_root):
    """The adopted root, on a library whose volume agrees and whose acknowledgment is recorded."""
    return adopted_root


def _route(cfg, db, adopted, declared_taxonomy, *, rows=None, registry=None, session_id=SESSION_ID, **kwargs):
    if registry is None:
        registry = _registry(tree_registry.Mode.DATABASE, root_id=str(adopted.ID))
    return routing_pass.route(
        cfg, db, session_id=session_id, registry=registry, declared=declared_taxonomy,
        rows=routing_pass.content_rows(db) if rows is None else rows,
        root_exists=lambda _root: True, analysis_roots=[Path(cfg.library.root) / "Music"], **kwargs,
    )


def _memberships(db, content_id: str) -> int:
    return db.get_playlist_songs(ContentID=str(content_id)).count()


def test_the_pass_places_a_track_and_marks_it_only_after_the_commit(cfg, db, gated_root):
    """The happy path, end to end: decide, import, route, and the mark follows."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    report = _route(cfg, db, gated_root, DECLARED)
    assert report.readiness is routing_pass.Readiness.READY
    assert len(report.routed) == 1
    assert report.memberships[0].added == 1
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()
    assert routing_pass.read(cfg).for_session(SESSION_ID)[0].state is routing_pass.TrackState.ROUTED
    assert _memberships(db, "2") == 1


def test_the_track_lands_inside_the_tree_the_cutover_adopted(cfg, db, gated_root):
    """Proved by walking UP from the membership row, never down by name."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    _route(cfg, db, gated_root, DECLARED)
    folder_display, sub_display = routing_pass.destination(DECLARED, *_destination(DECLARED))
    playlist, folder = _filed_under(db, "2")
    assert playlist.Name == sub_display
    assert folder.Name == folder_display
    assert str(folder.ParentID) == str(gated_root.ID)


def test_the_pass_run_before_the_import_is_read_only(cfg, db, gated_root):
    """Asserted against the FILESYSTEM."""
    routing_pass.record_intents(cfg, [_not_yet_there(cfg, DECLARED)])
    # The state tree is all a pass could write; a WAL read touches the database's index.
    roots = (config.library_state_dir(cfg), config.installation_state_dir(), config.config_dir())
    before = _state_fingerprint(*roots)
    report = _route(cfg, db, gated_root, DECLARED)
    assert _state_fingerprint(*roots) == before, "the pass wrote before deciding it was ready"
    assert report.readiness is routing_pass.Readiness.NOT_READY
    assert report.routed == ()
    assert report.memberships == ()
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1


def test_a_crash_between_the_commit_and_the_mark_converges(cfg, db, gated_root, monkeypatch):
    """Driven by an ACTUAL crash in the window."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    real_mark = routing_pass.mark

    def die(*args, **kwargs):
        raise RuntimeError("the process was killed between the commit and the mark")

    monkeypatch.setattr(routing_pass, "mark", die)
    with pytest.raises(RuntimeError, match="between the commit and the mark"):
        _route(cfg, db, gated_root, DECLARED)
    # The commit landed and the ledger did not move: what a kill in the window leaves.
    assert _memberships(db, "2") == 1
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1
    # The restart puts back only the mark, keeping the platform seams.
    monkeypatch.setattr(routing_pass, "mark", real_mark)
    report = _route(cfg, db, gated_root, DECLARED)
    assert report.memberships[0].added == 0
    assert report.memberships[0].already_present == 1
    assert _memberships(db, "2") == 1, "the recovery run duplicated the membership"
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()


def test_a_second_pass_over_a_settled_run_writes_nothing(cfg, db, gated_root):
    """Re-running is the recovery procedure, so re-running must be free."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    _route(cfg, db, gated_root, DECLARED)
    second = _route(cfg, db, gated_root, DECLARED)
    assert second.placed == ()
    assert second.memberships == ()
    assert _memberships(db, "2") == 1


def test_a_track_whose_membership_cannot_be_proved_is_not_marked(cfg, db, gated_root, monkeypatch):
    """The fail-safe direction on the read-back."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    monkeypatch.setattr(routing_pass, "membership_proven", lambda *args, **kwargs: False)
    report = _route(cfg, db, gated_root, DECLARED)
    assert report.routed == ()
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1


def test_a_tree_still_on_the_bridge_refuses_and_marks_nothing(cfg, db, gated_root):
    """U18's inverse guard reaches the caller with its remedy, and the ledger is untouched."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    with pytest.raises(tree_registry.TreeModeRefused) as excinfo:
        _route(cfg, db, gated_root, DECLARED, registry=_registry(tree_registry.Mode.XML))
    assert isinstance(excinfo.value, CratekitError)
    assert excinfo.value.cause.remediation.remedy is excinfo.value.remedy
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1
    assert _memberships(db, "2") == 0


def test_a_missing_acknowledgment_refuses_before_the_database_is_touched(
    cfg, monkeypatch, db, adopted_root
):
    """The session gates are the writer's, and the pass does not route around them."""
    _volume_agrees(cfg, monkeypatch)
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    assert _refused_by(_route, cfg, db, adopted_root, DECLARED).code is ExitCode.ACK_REQUIRED
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1


def test_content_rows_reads_the_soft_delete_marker_off_the_row(cfg, monkeypatch, tmp_path):
    """The withdrawn answer is only as good as the column it comes from."""
    path = tmp_path / "removed" / "master.db"
    _build_disposable_database(path)
    _record_locations(path, {"1": _music(cfg, COMPOSED), "2": _music(cfg, PLAIN)}, removed={"2"})
    _unlocked_integrity(monkeypatch)
    handle = rb_writer.open_db(path, unlock=False, cfg=cfg)
    try:
        rows = {row.content_id: row for row in routing_pass.content_rows(handle)}
    finally:
        rb_writer.close_db(handle)
    assert rows["2"].deleted is True
    assert rows["1"].deleted is False
    assert rows["2"].recorded == _music(cfg, PLAIN)


def _open_run(cfg):
    return session.open_session(cfg, workflow=routing_pass.ROUTING_WORKFLOW, session_id=SESSION_ID)


def test_a_run_with_nothing_to_route_closes(cfg, gates_pass):
    """A run that deferred nothing is not held up."""
    record = _open_run(cfg)
    closed = routing_pass.close_run(record, cfg)
    assert closed.state is session.SessionState.CLOSED
    assert closed.terminal


def test_a_run_with_a_pending_track_refuses_to_close(cfg, gates_pass):
    record = _open_run(cfg)
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    cause = _refused_by(routing_pass.close_run, record, cfg)
    assert cause.reason == "routing-outstanding"
    assert cause.code is ExitCode.PENDING_HUMAN
    assert session.read_record(SESSION_ID, cfg).state is session.SessionState.OPEN


def test_a_run_closes_once_the_routing_pass_has_placed_its_track(cfg, db, gated_root):
    record = _open_run(cfg)
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    _refused_by(routing_pass.close_run, record, cfg)
    _route(cfg, db, gated_root, DECLARED)
    closed = routing_pass.close_run(record, cfg)
    assert closed.state is session.SessionState.CLOSED


def test_a_run_whose_track_has_not_been_imported_still_refuses_to_close(cfg, db, gated_root):
    """The pass ran, said not-ready, and settled nothing. The run stays open."""
    record = _open_run(cfg)
    routing_pass.record_intents(cfg, [_not_yet_there(cfg, DECLARED)])
    assert _route(cfg, db, gated_root, DECLARED).readiness is routing_pass.Readiness.NOT_READY
    _refused_by(routing_pass.close_run, record, cfg)


def test_a_track_deleted_after_import_is_surfaced(cfg, db, gated_root):
    """Surfaced, never auto-skipped."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    report = _route(cfg, db, gated_root, DECLARED, rows=[_row(cfg, PLAIN, "2", deleted=True)])
    assert report.readiness is routing_pass.Readiness.READY
    assert [item.placement for item in report.withdrawn] == [routing_pass.Placement.WITHDRAWN]
    assert report.routed == ()
    assert report.memberships == ()


def test_the_routing_pass_never_acknowledges_a_track_by_itself(cfg, db, gated_root):
    """The separation that makes surfacing mean anything."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    _route(cfg, db, gated_root, DECLARED, rows=[_row(cfg, PLAIN, "2", deleted=True)])
    states = {entry.state for entry in routing_pass.read(cfg).for_session(SESSION_ID)}
    assert states == {routing_pass.TrackState.INTENDED}


def test_a_surfaced_track_closes_the_run_only_after_it_is_acknowledged(cfg, db, gated_root):
    """Acknowledgment is the ONLY way out of a surfaced track."""
    record = _open_run(cfg)
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    removed = [_row(cfg, PLAIN, "2", deleted=True)]
    for _ in range(2):
        _route(cfg, db, gated_root, DECLARED, rows=removed)
        _refused_by(routing_pass.close_run, record, cfg)
    track = routing_pass.read(cfg).for_session(SESSION_ID)[0].track
    routing_pass.acknowledge(cfg, [track], session_id=SESSION_ID, actor="a-person", note="removed in rekordbox")
    closed = routing_pass.close_run(record, cfg)
    assert closed.state is session.SessionState.CLOSED
    settled = routing_pass.read(cfg).for_session(SESSION_ID)[0]
    assert settled.state is routing_pass.TrackState.ACKNOWLEDGED
    assert settled.actor == "a-person"


def test_abandoning_a_run_is_not_gated_on_routing(cfg, gates_pass):
    """The escape is not gated, because a gate on the escape is a trap."""
    record = _open_run(cfg)
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    abandoned = routing_pass.close_run(record, cfg, state=session.SessionState.ABANDONED)
    assert abandoned.state is session.SessionState.ABANDONED


def test_one_run_of_another_session_does_not_hold_this_one_open(cfg, gates_pass):
    """Outstanding is asked per run, so one stalled run does not freeze the rest."""
    record = _open_run(cfg)
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN, session_id="another-run")])
    assert routing_pass.close_run(record, cfg).state is session.SessionState.CLOSED


def test_one_real_run_imports_routes_and_closes(cfg, gates_pass, monkeypatch):
    """The unit's verification: import, route, tracks appear in native trees, run closes."""
    path = Path(cfg.library.db_path)
    _build_disposable_database(path)
    _record_locations(path, {"1": "", "2": ""})  # nothing imported yet
    _unlocked_integrity(monkeypatch)
    record = _open_run(cfg)
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])

    def drive(handle):
        adopted = rb_writer.ensure_folder(handle, TREE_DISPLAY)
        handle.session.commit()
        return _route(cfg, handle, adopted, DECLARED), adopted

    # Before the import nothing resolves or is marked, and the run refuses to close.
    handle = rb_writer.open_db(path, unlock=False, cfg=cfg)
    try:
        early, _ = drive(handle)
    finally:
        rb_writer.close_db(handle)
    assert early.readiness is routing_pass.Readiness.NOT_READY
    assert early.routed == ()
    assert _refused_by(routing_pass.close_run, record, cfg).reason == "routing-outstanding"
    # The person imports while this process holds nothing; the pass then places and marks.
    _record_locations(path, {"2": _music(cfg, PLAIN)})
    handle = rb_writer.open_db(path, unlock=False, cfg=cfg)
    try:
        late, adopted = drive(handle)
        assert late.readiness is routing_pass.Readiness.READY
        assert len(late.routed) == 1
        assert late.memberships[0].added == 1
        folder_display, sub_display = routing_pass.destination(DECLARED, *_destination(DECLARED))
        playlist, folder = _filed_under(handle, "2")
        assert (playlist.Name, folder.Name) == (sub_display, folder_display)
        assert str(folder.ParentID) == str(adopted.ID)
    finally:
        rb_writer.close_db(handle)
    closed = routing_pass.close_run(record, cfg)
    assert closed.state is session.SessionState.CLOSED
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()


def _module_string_constants(tree: ast.AST) -> frozenset[str]:
    """Every module-level name bound to a plain string in this source."""
    named: set[str] = set()
    for node in tree.body if isinstance(tree, ast.Module) else []:
        targets: list[ast.expr] = []
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        value = getattr(node, "value", None)
        if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                named.add(target.id)
    return frozenset(named)


def _is_invented(node: ast.expr | None, constants: frozenset[str]) -> bool:
    """True when this expression's value was chosen by the code, not by a person."""
    if node is None:
        return False
    if isinstance(node, ast.Constant):
        return isinstance(node.value, str)
    if isinstance(node, ast.JoinedStr):
        # An f-string with no substitution is a literal; one with a substitution carries a value.
        return not any(isinstance(part, ast.FormattedValue) for part in node.values)
    if isinstance(node, ast.IfExp):
        return _is_invented(node.body, constants) and _is_invented(node.orelse, constants)
    if isinstance(node, ast.BinOp):
        return _is_invented(node.left, constants) and _is_invented(node.right, constants)
    if isinstance(node, ast.Name):
        return node.id in constants
    return False


def _called_name(func: ast.expr) -> str:
    """The name a call is made by, attribute or bare, or empty."""
    if isinstance(func, ast.Attribute):
        return func.attr
    return func.id if isinstance(func, ast.Name) else ""


def _calls(source: str) -> Iterator[tuple[str, ast.Call]]:
    """Every call in ``source`` with the name it is called by."""
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call):
            yield _called_name(node.func), node


def _made_up_actors(source: str) -> list[str]:
    """Every ``acknowledge`` call whose actor is a value the caller invented (P7, R34)."""
    constants = _module_string_constants(ast.parse(source))
    found: list[str] = []
    for name, node in _calls(source):
        if name != "acknowledge":
            continue
        for keyword in node.keywords:
            if keyword.arg == "actor":
                if _is_invented(keyword.value, constants):
                    found.append(ast.unparse(node))
                continue
            if keyword.arg is None and isinstance(keyword.value, ast.Dict):
                # ``**{"actor": ...}`` hides the argument from a check on keyword names.
                for key, value in zip(keyword.value.keys, keyword.value.values):
                    if isinstance(key, ast.Constant) and key.value == "actor" and _is_invented(value, constants):
                        found.append(ast.unparse(node))
    return found


def test_no_caller_acknowledges_a_track_with_an_actor_it_invented():
    """R34's shape, one layer up, ARMED NOW rather than when the first caller lands."""
    offenders: dict[str, list[str]] = {}
    for path in sorted(SRC_ROOT.rglob("*.py")):
        if "_vendor" in path.parts:
            continue
        source = path.read_text()
        # A file that never spells the name holds no call of it.
        if "acknowledge" in source and (found := _made_up_actors(source)):
            offenders[path.relative_to(SRC_ROOT).as_posix()] = found
    # The actor is the person who decided, from a decision recorded against the run.
    assert not offenders, f"acknowledgments recorded against an actor the code made up: {offenders}"


def test_the_intake_pipeline_records_its_routing_intents_at_the_decision():
    """P5's countdown, armed the moment the pipeline that owes it lands."""
    package = SRC_ROOT / "cratekit" / "intake"
    called = any(
        name == "record_intents"
        for path in sorted(package.rglob("*.py"))
        for name, _node in _calls(path.read_text())
    )
    assert called, "the intake pipeline never records a routing intent"


def _elsewhere(cfg, declared_taxonomy, session_id: str):
    """PLAIN's intent for ``session_id``, sent to the second destination."""
    other_bucket, other_sub = _destination(declared_taxonomy, 1)
    return replace(_intent(cfg, declared_taxonomy, PLAIN, session_id=session_id), bucket=other_bucket, sub=other_sub)


def _where(db, content_id: str) -> list[tuple[str | None, str]]:
    """Every (folder, playlist) pair this content row actually sits in."""
    found: list[tuple[str | None, str]] = []
    for membership in db.get_playlist_songs(ContentID=str(content_id)):
        playlist = db.get_playlist(ID=str(membership.PlaylistID))
        if playlist is None:
            continue
        folder = db.get_playlist(ID=str(playlist.ParentID))
        found.append((folder.Name if folder is not None else None, playlist.Name))
    return found


def test_a_second_run_deferring_one_file_does_not_take_over_the_first_runs_record(cfg, gates_pass):
    """One record per RUN and file, never one record per file."""
    first = session.open_session(cfg, workflow=routing_pass.ROUTING_WORKFLOW, session_id="run-one")
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN, session_id="run-one")])
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN, session_id="run-two")])
    ledger = routing_pass.read(cfg)
    owners = sorted(entry.session_id for entry in ledger.intents)
    assert owners == ["run-one", "run-two"], f"one run's decision replaced the other's: {owners}"
    assert len(ledger.outstanding("run-one")) == 1
    assert len(ledger.outstanding("run-two")) == 1
    assert _refused_by(routing_pass.close_run, first, cfg).reason == "routing-outstanding"


def test_marking_one_runs_track_leaves_another_runs_record_alone(cfg):
    """A mark is scoped to the run that made the decision it settles."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN, session_id="run-one")])
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN, session_id="run-two")])
    track = routing_pass.read(cfg).for_session("run-two")[0].track
    routing_pass.mark(cfg, [track], routing_pass.TrackState.ROUTED, session_id="run-two")
    assert routing_pass.read(cfg).outstanding("run-two") == ()
    assert len(routing_pass.read(cfg).outstanding("run-one")) == 1


def test_two_overlapping_runs_over_one_file_each_reach_their_own_destination(cfg, db, gated_root):
    """Both runs driven to completion, and neither closes while it still owes work."""
    first = session.open_session(cfg, workflow=routing_pass.ROUTING_WORKFLOW, session_id="run-one")
    second = session.open_session(cfg, workflow=routing_pass.ROUTING_WORKFLOW, session_id="run-two")
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN, session_id="run-one")])
    routing_pass.record_intents(cfg, [_elsewhere(cfg, DECLARED, "run-two")])
    first_destination = routing_pass.destination(DECLARED, *_destination(DECLARED))
    second_destination = routing_pass.destination(DECLARED, *_destination(DECLARED, 1))
    assert first_destination != second_destination
    # Run one places its track while run two still owes its own.
    _route(cfg, db, gated_root, DECLARED, session_id="run-one")
    assert routing_pass.close_run(first, cfg).state is session.SessionState.CLOSED
    assert _refused_by(routing_pass.close_run, second, cfg).reason == "routing-outstanding"
    _route(cfg, db, gated_root, DECLARED, session_id="run-two")
    assert routing_pass.close_run(second, cfg).state is session.SessionState.CLOSED
    landed = sorted(_where(db, "2"))
    assert landed == sorted([first_destination, second_destination]), f"the library holds {landed}"


@pytest.mark.parametrize("marker", ["absent", None], ids=["column-absent", "column-empty"])
def test_a_row_that_cannot_report_the_soft_delete_marker_refuses(cfg, marker):
    """U18 gave ``ContentRow.deleted`` no default, so no producer may supply one, empty or absent."""

    class Row:
        ID = "9"
        FolderPath = "/somewhere/nothing.flac"

    if marker is None:
        Row.rb_local_deleted = None

    class Blind:
        def get_content(self):
            return [Row()]

    assert _refused_by(list, routing_pass.content_rows(Blind())).code is ExitCode.LIBRARY_UNREADABLE


def test_a_destination_the_taxonomy_no_longer_declares_is_its_own_placement(cfg):
    """An undeclared destination is its own placement, never written, and not a missing import."""
    stale = replace(_intent(cfg, DECLARED, PLAIN), sub="a-sub-this-library-dropped")
    placed = _placements(cfg, DECLARED, [stale], [_row(cfg, PLAIN, "1")])
    assert placed[0].placement is routing_pass.Placement.UNDECLARED
    assert placed[0].placement not in routing_pass.WRITABLE
    assert routing_pass.readiness(placed) is routing_pass.Readiness.UNANSWERABLE


def test_one_stale_destination_does_not_stop_the_other_tracks_in_the_run(cfg, db, gated_root):
    """The good track is placed, and the bad one is reported rather than raised."""
    good = _intent(cfg, DECLARED, PLAIN)
    stale = replace(_intent(cfg, DECLARED, COMPOSED), sub="a-sub-this-library-dropped")
    routing_pass.record_intents(cfg, [good, stale])
    report = _route(cfg, db, gated_root, DECLARED)
    assert _memberships(db, "2") == 1, "the good track was blocked by the stale one"
    assert report.routed == (good.track,)
    reasons = {item.intent.track: item.placement for item in report.placed}
    assert reasons[stale.track] is routing_pass.Placement.UNDECLARED
    outstanding = routing_pass.read(cfg).outstanding(SESSION_ID)
    assert [entry.track for entry in outstanding] == [stale.track]


class _CrashOnce:
    """A mark that dies the first time and works afterwards."""

    def __init__(self, real):
        self.real = real
        self.armed = True

    def __call__(self, *args, **kwargs):
        if self.armed:
            self.armed = False
            raise RuntimeError("the process was killed between the commit and the mark")
        return self.real(*args, **kwargs)


def _crash_between_the_commit_and_the_mark(cfg, db, adopted, declared_taxonomy, monkeypatch):
    routing_pass.record_intents(cfg, [_intent(cfg, declared_taxonomy, PLAIN)])
    monkeypatch.setattr(routing_pass, "mark", _CrashOnce(routing_pass.mark))
    with pytest.raises(RuntimeError, match="between the commit and the mark"):
        _route(cfg, db, adopted, declared_taxonomy)
    assert _memberships(db, "2") == 1
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1


def _rename_bucket_folder(db, declared_taxonomy) -> None:
    """A person renames the first bucket's folder in rekordbox."""
    folder_display, _sub_display = routing_pass.destination(declared_taxonomy, *_destination(declared_taxonomy))
    db.session.query(tables.DjmdPlaylist).filter_by(Name=folder_display).one().Name = "A Name Of Their Own"
    db.session.commit()


def test_a_recovery_run_after_a_rekordbox_rename_refuses_rather_than_duplicating(
    cfg, db, gated_root, monkeypatch
):
    """With no recorded node map a rename refuses, rather than duplicating (R19, D5)."""
    _crash_between_the_commit_and_the_mark(cfg, db, gated_root, DECLARED, monkeypatch)
    # The node map the pass wrote is what makes a rename converge; wiped, the refusal stands.
    convergence.record_nodes(cfg, TREE_ID, (), replace_all=True)
    _rename_bucket_folder(db, DECLARED)
    cause = _refused_by(_route, cfg, db, gated_root, DECLARED)
    assert cause.reason == "routing-destination-renamed"
    assert _memberships(db, "2") == 1, "the recovery run duplicated the membership"
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1


def _taxonomy_with_the_first_bucket_renamed(new_display: str):
    """The shipped template, REBUILT, with one bucket's display name changed."""
    source = resources.files("cratekit") / "templates" / taxonomy.DEFAULT_TEMPLATE
    data = tomllib.loads(source.read_text(encoding="utf-8"))
    data["bucket"][0]["display"] = new_display
    return taxonomy.build_taxonomy(data)


def test_a_recovery_run_after_a_taxonomy_rename_converges_rather_than_duplicating(
    cfg, db, gated_root, monkeypatch
):
    """The template moved, not the library. The node map still names the folder."""
    _crash_between_the_commit_and_the_mark(cfg, db, gated_root, DECLARED, monkeypatch)
    renamed = _taxonomy_with_the_first_bucket_renamed("A Bucket Renamed")
    assert renamed.buckets[0].id == DECLARED.buckets[0].id
    report = _route(cfg, db, gated_root, renamed)
    assert len(report.routed) == 1
    assert _memberships(db, "2") == 1
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()


def test_a_recovery_run_after_a_rename_converges_once_the_tree_layer_can(
    cfg, db, gated_root, monkeypatch
):
    """P5's countdown for the refusal above, so it cannot become permanent."""
    _crash_between_the_commit_and_the_mark(cfg, db, gated_root, DECLARED, monkeypatch)
    _rename_bucket_folder(db, DECLARED)
    report = _route(cfg, db, gated_root, DECLARED)
    assert len(report.routed) == 1
    assert _memberships(db, "2") == 1, "the recovery run duplicated the membership"
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()


def test_a_bucket_folder_that_does_not_exist_yet_is_not_mistaken_for_a_rename(cfg, db, gated_root):
    """P7, the other direction. A guard that fires on correct code gets routed around."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN, session_id="run-one")])
    _route(cfg, db, gated_root, DECLARED, session_id="run-one")
    routing_pass.record_intents(cfg, [_elsewhere(cfg, DECLARED, "run-two")])
    report = _route(cfg, db, gated_root, DECLARED, session_id="run-two")
    assert len(report.routed) == 1
    assert _memberships(db, "2") == 2


def test_two_playlists_of_the_destinations_name_leave_its_node_unrecorded(cfg, db, gated_root):
    """The node map never binds a destination to whichever of two namesakes came first."""
    bucket_id, sub_id = _destination(DECLARED)
    folder_display, sub_display = routing_pass.destination(DECLARED, bucket_id, sub_id)
    folder = db.create_playlist_folder(folder_display, parent=gated_root)
    db.create_playlist(sub_display, parent=folder)
    db.create_playlist(sub_display, parent=folder)
    db.session.commit()
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    report = _route(cfg, db, gated_root, DECLARED)
    assert report.memberships[0].added == 1
    record = convergence.read(cfg).tree(TREE_ID)
    assert record is None or record.node(bucket_id, sub_id) is None


_CONCURRENT_WRITER = '''
import sys
from pathlib import Path

from cratekit.core import config
from cratekit.write import routing_pass
from tests.test_config import valid_data

root = Path(sys.argv[1])
run = sys.argv[2]
count = int(sys.argv[3])
cfg = config.from_dict(valid_data(root))
for index in range(count):
    location = f"{root}/Music/{run}-{index}.flac"
    intent = routing_pass.RoutingIntent(
        track=routing_pass.track_id(location), session_id=run, location=location, tree="a_tree",
        bucket="a_bucket", sub="a_sub", decided="2026-08-02T00:00:00+00:00",
    )
    routing_pass.record_intents(cfg, [intent])
'''


def test_two_processes_recording_intents_lose_none_of_them(cfg, library, tmp_path):
    """REAL PROCESSES, not threads, because the hazard is a real process boundary."""
    script = tmp_path / "concurrent_writer.py"
    script.write_text(_CONCURRENT_WRITER)
    each = 60
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join([str(SRC_ROOT), str(REPO_ROOT)])
    processes = [
        subprocess.Popen(
            [sys.executable, str(script), str(library), run, str(each)], env=environment,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        for run in ("run-one", "run-two")
    ]
    for process in processes:
        _out, errors = process.communicate(timeout=300)
        assert process.returncode == 0, errors.decode()
    recorded = routing_pass.read(cfg).intents
    assert len(recorded) == 2 * each, f"{len(recorded)} of {2 * each} decisions survived"


def test_the_lock_is_a_declared_state_entry_that_a_restore_never_replaces(cfg):
    """A path composed under a state root is a file nothing walks or backs up."""
    entry = config.state_file(routing_pass.LOCK_KEY)
    assert entry.root is config.StateRoot.LIBRARY
    assert entry.snapshot is config.SnapshotRole.NEVER_RESTORED
    assert config.library_coupled_dir(cfg) not in routing_pass.lock_path(cfg).parents


def test_everything_this_module_creates_is_private_under_any_umask(cfg):
    """P1 and P3 together: walk the tree, do not name the files in it."""
    previous = os.umask(0o000)
    try:
        routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
        track = routing_pass.read(cfg).for_session(SESSION_ID)[0].track
        routing_pass.mark(cfg, [track], routing_pass.TrackState.ROUTED, session_id=SESSION_ID)
    finally:
        os.umask(previous)
    root = config.library_state_dir(cfg)
    permissive: list[str] = []
    for current, directories, files in os.walk(root):
        expected = [(name, config.PRIVATE_DIR_MODE) for name in directories]
        for name, mode in [*expected, *((name, config.PRIVATE_FILE_MODE) for name in files)]:
            path = Path(current) / name
            if stat.S_IMODE(path.stat().st_mode) != mode:
                permissive.append(f"{path} is {oct(stat.S_IMODE(path.stat().st_mode))}")
    assert stat.S_IMODE(root.stat().st_mode) == config.PRIVATE_DIR_MODE
    assert not permissive, f"created under umask 000 at a permissive mode: {permissive}"


def _awaiting_import(cfg) -> None:
    """An intake run left waiting on an import of its export."""
    record = session.open_session(cfg, workflow="an-intake-workflow", session_id=SESSION_ID)
    pending = session.pending_import(
        record, artifact=cfg.library.root / "an-export.xml",
        summary="import this export into rekordbox", verify_verb="a-verify-verb",
    )
    session.mark_awaiting_import(record, pending, cfg)


def test_a_run_whose_export_was_never_imported_refuses_to_close(cfg, gates_pass):
    """The other state in which somebody still owes an act."""
    _awaiting_import(cfg)
    cause = _refused_by(routing_pass.close_run, session.read_record(SESSION_ID, cfg), cfg)
    assert cause.reason == "awaiting-import"
    assert cause.code is ExitCode.PENDING_HUMAN
    assert session.read_record(SESSION_ID, cfg).state is session.SessionState.AWAITING_IMPORT


def test_abandoning_a_run_whose_export_was_never_imported_is_still_allowed(cfg, gates_pass):
    """The escape stays open, for the reason the routing gate leaves it open."""
    _awaiting_import(cfg)
    held = session.read_record(SESSION_ID, cfg)
    abandoned = routing_pass.close_run(held, cfg, state=session.SessionState.ABANDONED)
    assert abandoned.state is session.SessionState.ABANDONED


def _write_ledger(cfg, text: str) -> None:
    path = routing_pass.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_an_unreadable_ledger_carries_its_remedy_to_the_boundary(cfg):
    """Read through a tolerant reader the gate fails open, and a non-structured refusal is a defect (S4)."""
    _write_ledger(cfg, "{ not json")
    with pytest.raises(routing_pass.RoutingLedgerUnreadable) as excinfo:
        routing_pass.read(cfg)
    assert isinstance(excinfo.value, CratekitError)
    assert excinfo.value.cause.remediation.remedy is Remedy.RUN_DOCTOR
    assert excinfo.value.cause.reason in REASONS


def test_a_ledger_from_a_newer_build_carries_the_upgrade_remedy(cfg):
    """The same slug, a different remedy, which is why the remedy travels on the cause."""
    _write_ledger(cfg, json.dumps({"schema_version": routing_pass.SCHEMA_VERSION + 1, "intents": []}))
    assert _refused_by(routing_pass.read, cfg).remediation.remedy is Remedy.UPGRADE_CRATEKIT


def test_every_refusal_this_module_raises_is_a_structured_cause():
    """P3. The set is DERIVED by walking the module rather than listed."""
    raised: set[str] = set()
    for node in ast.walk(ast.parse(inspect.getsource(routing_pass))):
        if not isinstance(node, ast.Raise) or node.exc is None:
            continue
        thrown = node.exc
        name = _called_name(thrown.func if isinstance(thrown, ast.Call) else thrown)
        if name:
            raised.add(name)
    # ``ValueError`` guards a constructor; ``refuse`` already returns a structured cause.
    exempt = {"refuse", "ValueError"}
    checked = 0
    for name in sorted(raised - exempt):
        candidate = getattr(routing_pass, name, None)
        if not isinstance(candidate, type) or not issubclass(candidate, BaseException):
            continue
        checked += 1
        assert issubclass(candidate, CratekitError), f"{name} is not a CratekitError (S4)"
    assert checked, "the walk found no raised exception type, so it proves nothing"


def test_every_refusal_the_pass_propagates_carries_its_remedy_too():
    """The same rule, over the module this pass RAISES THROUGH rather than from (P5)."""
    checked = 0
    for _name, candidate in inspect.getmembers(tree_registry, inspect.isclass):
        if not issubclass(candidate, BaseException):
            continue
        if candidate.__module__ != tree_registry.__name__:
            continue
        signature = inspect.signature(candidate.__init__)
        holds_a_remedy = "remedy" in signature.parameters or "Remedy" in inspect.getsource(candidate)
        if not holds_a_remedy:
            continue
        checked += 1
        assert issubclass(candidate, CratekitError), f"{candidate.__name__} is not a CratekitError (S4)"
    assert checked >= 2, "the walk found nothing carrying a remedy, so it proves nothing"


def test_a_run_whose_locations_all_resolve_to_nothing_is_not_told_to_import(cfg):
    """A configuration failure and a missing import have opposite answers."""
    intent = replace(_intent(cfg, DECLARED, PLAIN), location="/somewhere/nothing/maps/onto/x.flac")
    placed = _placements(cfg, DECLARED, [intent], [_row(cfg, PLAIN, "1")])
    assert placed[0].placement is routing_pass.Placement.UNRESOLVED
    assert routing_pass.readiness(placed) is routing_pass.Readiness.UNANSWERABLE
    assert routing_pass.readiness(placed) is not routing_pass.Readiness.NOT_READY


def test_every_readiness_answer_except_ready_writes_nothing(cfg, db, gated_root, monkeypatch):
    """DERIVED over the enum, so a member added later cannot acquire the writing answer."""
    routing_pass.record_intents(cfg, [_intent(cfg, DECLARED, PLAIN)])
    for answer in routing_pass.Readiness:
        if answer is routing_pass.Readiness.READY:
            continue
        monkeypatch.setattr(routing_pass, "readiness", lambda _placed, _held=answer: _held)
        report = _route(cfg, db, gated_root, DECLARED)
        assert report.readiness is answer
        assert report.routed == ()
        assert report.memberships == ()
        assert _memberships(db, "2") == 0, f"{answer} wrote to the library"


def test_the_readiness_answers_are_three_rather_than_two():
    """One file cannot argue both sides of the same question."""
    assert len(routing_pass.Readiness) >= 3
    assert routing_pass.Readiness.UNANSWERABLE not in (routing_pass.Readiness.READY, routing_pass.Readiness.NOT_READY)


def test_the_routing_verbs_have_landed():
    """U20 discharged the countdown: the four verbs are no longer planned."""
    named = [entry for entry in cli_registry.ENTRIES if entry.module == "cratekit.write.routing_cli"]
    assert named, "no entry names the routing command-line module any more"
    still_planned = [entry.name for entry in named if not entry.landed]
    assert not still_planned, f"routing verbs still carry a planned_in marker: {still_planned}"


def test_the_routing_command_line_module_is_no_longer_owed_in_the_register():
    """The countdown fired and was discharged, not left as a comment (P5, U59)."""
    assert "cratekit.write.routing_cli" not in _pending.PENDING


def test_the_routing_verbs_close_their_runs_through_the_gated_close():
    """P5's countdown for the close gate, armed when the surface that spends it lands."""
    write = SRC_ROOT / "cratekit" / "write"
    # The verbs' module and the export path it imports since U302.
    sources = [write / "routing_cli.py", write / "routing_export.py"]
    bypassed: list[str] = []
    gated = False
    for path in sources:
        for name, node in _calls(path.read_text()):
            if name == "close_session":
                bypassed.append(ast.unparse(node))
            if name == "close_run":
                gated = True
    assert gated, "the routing verbs never close a run through the gated close"
    # A direct close releases the capture without asking whether a track reached no playlist.
    assert not bypassed, f"the routing verbs close through the session spine directly: {bypassed}"


def test_the_intake_pipeline_closes_its_runs_through_the_gated_close():
    """The same obligation against the unit that CREATES the deferred work."""
    package = SRC_ROOT / "cratekit" / "intake"
    bypassed: list[str] = []
    for path in sorted(package.rglob("*.py")):
        for name, node in _calls(path.read_text()):
            if name == "close_session":
                bypassed.append(f"{path.name}: {ast.unparse(node)}")
    assert not bypassed, f"intake closes runs through the session spine directly: {bypassed}"


@pytest.mark.parametrize(
    "source",
    [
        'routing_pass.acknowledge(cfg, t, actor="cli")', "acknowledge(cfg, t, actor='cli')",
        'routing_pass.acknowledge(cfg, t, actor=f"cli")',
        'ACTOR = "cli"\nrouting_pass.acknowledge(cfg, t, actor=ACTOR)',
        'routing_pass.acknowledge(cfg, t, actor="cli" if x else "cli")',
        'routing_pass.acknowledge(cfg, t, **{"actor": "cli"})',
        'routing_pass.acknowledge(cfg, t, actor="cl" + "i")',
    ],
)
def test_the_made_up_actor_guard_bites_each_evasion(source):
    """P7's first half. Four documented bypasses, and each one has to fail."""
    assert _made_up_actors(source), f"the guard did not bite: {source}"


@pytest.mark.parametrize(
    "source",
    [
        "routing_pass.acknowledge(cfg, t, actor=decision.actor)",
        "def f(actor):\n    routing_pass.acknowledge(cfg, t, actor=actor)",
        'routing_pass.acknowledge(cfg, t, actor=f"{decision.actor}")',
        "routing_pass.acknowledge(cfg, t, **decided)",
        "routing_pass.acknowledge(cfg, t, actor=record.actor or holder.name)",
        '"acknowledge with actor=... somewhere in prose"',
        "acknowledge_receipt(cfg, t, actor='cli')",
    ],
)
def test_the_made_up_actor_guard_does_not_fire_on_correct_code(source):
    """P7's second half, and the half that decides whether the guard survives."""
    assert _made_up_actors(source) == [], f"the guard fired on correct code: {source}"
