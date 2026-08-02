"""U19: deferred routing, from the decision to the mark to the run that closes.

WHAT THIS UNIT IS. New tracks arrive through the XML intake bridge, which means
a person imports them and only then does the library hold a row for them. The
placement was decided long before that, during acquisition, so it has to be
written down and picked up again later. This file covers the three joints where
that goes wrong: the decision that was never persisted, the mark that was written
before the commit, and the run that closed while a track was still nowhere.

THE FIVE SCENARIOS THE PLAN NAMES, and where each is proved:

1. a run with a pending track refuses to close and closes after the routing verb
   runs -> ``test_a_run_with_a_pending_track_refuses_to_close``
   and ``test_a_run_closes_once_the_routing_pass_has_placed_its_track``
2. a crash between commit and mark converges on restart with zero duplicate
   memberships -> ``test_a_crash_between_the_commit_and_the_mark_converges``
3. the routing verb run before import resolves nothing, marks nothing, and
   reports not-ready -> ``test_the_pass_run_before_the_import_is_read_only``
4. a track deleted by the user after import is surfaced and closeable only via
   explicit acknowledgment -> ``test_a_track_deleted_after_import_is_surfaced``
   and ``test_a_surfaced_track_closes_the_run_only_after_it_is_acknowledged``
5. a run with nothing to route closes normally
   -> ``test_a_run_with_nothing_to_route_closes``

WHAT IS SUPPLEMENTED, because the five above leave four shapes uncovered. A
partial import, where some rows arrived and some did not. An ambiguous location,
which U18 refuses to write and this unit must therefore refuse to mark. A
location that resolves to no path at all, which is a configuration failure rather
than a missing import and must not be reported as one. And the fail-safe
direction on the read-back: a track whose membership cannot be proved after the
commit stays outstanding rather than being marked on the writer's word.

D1 APPLIES TO EVERY NAME HERE. Nothing below names a real volume, a real person,
or a real track. The synthetic paths still carry the character classes that
matter, a space and an accented character, because those are what the identity
primitives exist for.
"""

from __future__ import annotations

import ast
import json
import os
import stat
import unicodedata
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from cratekit.core import (
    config,
    locations,
    preflight,
    rb_writer,
    routing,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.write import routing_pass, trees
from tests._pending import requires
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

# ── synthesized names (D1) ───────────────────────────────────────────────────

TREE_ID = "shelf_stack"
TREE_DISPLAY = "Shelf & Stack"
ADOPTED_ROOT = "root-row-7788"
SESSION_ID = "s-0001"

#: One file name in each composition form, because the pair is the whole reason
#: the identity primitives exist and a ledger keyed on the raw string would
#: silently hold two records for one file.
COMPOSED = "Café One.flac"
DECOMPOSED = unicodedata.normalize("NFD", COMPOSED)
PLAIN = "Second Track.flac"
THIRD = "Third Track.flac"


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

    The same four seams ``tests/test_tree_writer.py`` patches, for the same
    reason: that these guards refuse is proved directly in
    ``tests/test_rb_writer_db.py``, and re-proving it here would only prove the
    fixture.
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


def _destination(declared_taxonomy):
    """The first bucket the shipped template declares, and a sub it really has.

    DERIVED from the template rather than named, because a test that spells a
    bucket identifier is a test that has to be edited when the shipped default
    changes, and R19 puts that name in configuration precisely so nothing spells
    it.
    """
    bucket = declared_taxonomy.buckets[0]
    sub = routing.energy_sub(declared_taxonomy, bucket.id, declared_taxonomy.energy.scale_max)
    assert sub is not None, "the shipped template's first bucket declares no sub"
    return bucket.id, sub.id


def _intent(cfg, declared_taxonomy, name: str, *, session_id: str = SESSION_ID):
    bucket_id, sub_id = _destination(declared_taxonomy)
    location = _music(cfg, name)
    return routing_pass.RoutingIntent(
        track=routing_pass.track_id(location),
        session_id=session_id,
        location=location,
        tree=TREE_ID,
        bucket=bucket_id,
        sub=sub_id,
        decided="2026-08-02T00:00:00+00:00",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Part 1: the ledger. Persisted at the decision, derived on the way out.
# ═══════════════════════════════════════════════════════════════════════════


def test_an_intent_is_readable_by_the_next_process_the_moment_it_is_decided(
    cfg, declared
):
    """Approach 1. A restarted process must be able to read what it believed.

    Written at the DECISION rather than at the end of the run, so the read below
    goes through a fresh load off the disk rather than through the object the
    writer returned. A ledger held in memory until the run finishes is a ledger
    that is empty for exactly the runs somebody needs to recover.
    """
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])

    reloaded = routing_pass.read(cfg)
    assert [entry.location for entry in reloaded.for_session(SESSION_ID)] == [
        _music(cfg, PLAIN)
    ]
    assert reloaded.for_session(SESSION_ID)[0].state is routing_pass.TrackState.INTENDED


def test_two_spellings_of_one_filename_are_one_record(cfg, declared):
    """The 144-file loss, one layer up.

    A ledger keyed on the raw recorded string holds two records for one file when
    the two sides were spelled in different composition forms, and the second run
    then routes a track the first run already routed.
    """
    composed = _intent(cfg, declared, COMPOSED)
    decomposed = _intent(cfg, declared, DECOMPOSED)
    assert composed.track == decomposed.track

    routing_pass.record_intents(cfg, [composed])
    routing_pass.record_intents(cfg, [decomposed])
    assert len(routing_pass.read(cfg).for_session(SESSION_ID)) == 1


def test_outstanding_is_derived_from_status_rather_than_from_a_stored_flag(
    cfg, declared
):
    """Approach 3, asserted in both directions.

    The state is the only thing that moves, and what is outstanding changes with
    it. A stored flag beside the state is a second answer to one question, and
    the two disagree the first time a crash lands between the two writes.
    """
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    track = routing_pass.read(cfg).for_session(SESSION_ID)[0].track

    assert [entry.track for entry in routing_pass.read(cfg).outstanding(SESSION_ID)] == [track]
    routing_pass.mark(cfg, [track], routing_pass.TrackState.ROUTED)
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()

    document = json.loads(routing_pass.path_for(cfg).read_text())
    record = document["intents"][0]
    assert "state" in record
    flags = [key for key, value in record.items() if isinstance(value, bool)]
    assert not flags, (
        f"the persisted record carries the boolean field(s) {flags}; outstanding "
        f"is derived from the state and a stored flag is a second answer to the "
        f"same question"
    )


def test_every_status_is_either_settled_or_outstanding(declared):
    """Derived by walking the enum, so the next state cannot fall between them (P3).

    The DIRECTION is the property. A member nobody classified must land in the
    outstanding half, because a state that settles a run by omission is a run
    that closes over a track nobody looked at.
    """
    for member in routing_pass.TrackState:
        assert (member in routing_pass.SETTLED) != (member in routing_pass.OUTSTANDING)
    assert routing_pass.OUTSTANDING == frozenset(routing_pass.TrackState) - routing_pass.SETTLED
    assert routing_pass.TrackState.INTENDED in routing_pass.OUTSTANDING


def test_no_taxonomy_display_name_reaches_the_persisted_record(cfg, declared):
    """D5 and R19, asserted over the BYTES rather than over the shape.

    Every display name the shipped template declares is searched for in the file,
    so a future field that persists one fails here rather than at the rename that
    orphans it. Derived from the template, never listed.
    """
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    text = routing_pass.path_for(cfg).read_text()

    displays = {declared.tree.display, declared.intake.display}
    displays |= {bucket.display for bucket in declared.buckets}
    displays |= {band.display for band in declared.energy.bands}
    displays |= {entry.display for entry in declared.sub_classes}
    for bucket in declared.buckets:
        displays |= {sub.display for sub in bucket.subs}
    leaked = sorted(display for display in displays if display and display in text)
    assert not leaked, f"display names persisted into the routing ledger: {leaked}"


def test_the_ledger_and_every_directory_above_it_are_private_under_any_umask(
    cfg, declared, monkeypatch
):
    """P1. A file mode is meaningless without the directory mode.

    Walked from the library state root DOWN to the file rather than asserted on
    the file alone, because a 0600 record inside a world-writable directory can
    be unlinked and replaced by any local account, and this record decides
    whether a run may close.
    """
    previous = os.umask(0o000)
    try:
        routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
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


def test_an_unreadable_ledger_refuses_rather_than_reading_as_nothing_outstanding(cfg):
    """The gate that reads its own state through a tolerant reader fails open.

    An unreadable ledger collapsed into "no records" is read as "nothing is
    outstanding", which admits the one close this unit exists to refuse. It has
    to be its own answer.
    """
    path = routing_pass.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{ not json")
    with pytest.raises(routing_pass.RoutingLedgerUnreadable):
        routing_pass.read(cfg)


def test_an_absent_ledger_is_the_empty_one(cfg):
    """A library that has never deferred a routing decision is not a failure."""
    assert routing_pass.read(cfg) == routing_pass.EMPTY
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()


def test_acknowledging_without_a_named_actor_is_refused(cfg, declared):
    """R34's shape, one layer up: somebody says a track is gone, not something."""
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    track = routing_pass.read(cfg).for_session(SESSION_ID)[0].track
    with pytest.raises(ValueError):
        routing_pass.acknowledge(cfg, [track], actor="   ")


# ═══════════════════════════════════════════════════════════════════════════
# Part 2: resolution and readiness. Read-only, and no session anywhere.
# ═══════════════════════════════════════════════════════════════════════════


def _row(cfg, name: str, content_id: str, *, deleted: bool = False):
    return trees.ContentRow(content_id, _music(cfg, name), deleted=deleted)


def _index(cfg, rows, *, prefix_map=()):
    return routing_pass.index_rows(rows, root=cfg.library.root, prefix_map=prefix_map)


def _placements(cfg, declared_taxonomy, intents, rows, *, prefix_map=()):
    return routing_pass.resolve_placements(
        intents,
        _index(cfg, rows, prefix_map=prefix_map),
        declared_taxonomy,
        root=cfg.library.root,
        prefix_map=prefix_map,
    )


def test_every_sub_the_taxonomy_can_route_to_resolves_to_a_display_name(declared):
    """P4. A derivation that replaces a list is checked against the real set.

    The set is built by asking the routing rules what they can RETURN, over every
    bucket and every level on the scale, rather than by listing the sub shapes
    somebody remembered. A resolver that covered four of the five shapes would
    look complete right up until a library used the fifth, and the failure would
    be a run that cannot place a track it already decided on.
    """
    produced = set()
    for bucket in declared.buckets:
        for level in [None, *range(0, declared.energy.scale_max + 1)]:
            sub = routing.energy_sub(declared, bucket.id, level)
            if sub is not None:
                produced.add((bucket.id, sub.id))
    produced |= {
        (bucket.id, entry.id) for bucket in declared.buckets for entry in declared.sub_classes
    }
    assert produced, "the shipped template routes nowhere; the derivation is broken"

    for bucket_id, sub_id in sorted(produced):
        folder, sub = routing_pass.destination(declared, bucket_id, sub_id)
        assert folder and sub


def test_a_sub_the_taxonomy_does_not_declare_refuses_rather_than_inventing_a_name(
    declared,
):
    """An unresolvable identifier is a ledger and a template that disagree.

    Falling back to the identifier itself would write a folder into somebody's
    library named after an internal key, which is both wrong and invisible.
    """
    with pytest.raises(KeyError):
        routing_pass.destination(declared, declared.buckets[0].id, "a-sub-nobody-declared")


def test_the_pass_matches_every_intent_against_rows_supplied_as_a_cursor(cfg, declared):
    """The iterable consumed once, which is how the natural database read arrives.

    A row set rebuilt or re-walked per intent silently matches nothing after the
    first one when the caller's rows are a cursor, and the run reports clean. The
    generator here is consumable exactly once, so an implementation that walks it
    twice reports the second track absent.
    """
    intents = [_intent(cfg, declared, PLAIN), _intent(cfg, declared, THIRD)]
    rows = (row for row in (_row(cfg, PLAIN, "1"), _row(cfg, THIRD, "2")))
    placed = _placements(cfg, declared, intents, rows)
    assert [item.placement for item in placed] == [
        routing_pass.Placement.RESOLVED,
        routing_pass.Placement.RESOLVED,
    ]


def test_a_track_with_no_row_at_all_is_not_imported_rather_than_withdrawn(cfg, declared):
    intents = [_intent(cfg, declared, PLAIN)]
    placed = _placements(cfg, declared, intents, [])
    assert placed[0].placement is routing_pass.Placement.NOT_IMPORTED
    assert routing_pass.readiness(placed) is routing_pass.Readiness.NOT_READY


def test_a_location_reaching_only_soft_deleted_rows_is_withdrawn(cfg, declared):
    """The plan's fifth approach point, at the level the distinction is made.

    rekordbox soft-deletes, so the row for a track the user removed is still
    there wearing the marker. Reading that as "not imported" would tell somebody
    to import a track they imported and then deliberately deleted.
    """
    intents = [_intent(cfg, declared, PLAIN)]
    placed = _placements(cfg, declared, intents, [_row(cfg, PLAIN, "1", deleted=True)])
    assert placed[0].placement is routing_pass.Placement.WITHDRAWN
    assert routing_pass.readiness(placed) is routing_pass.Readiness.READY


def test_a_tombstone_beside_a_live_row_resolves_cleanly(cfg, declared):
    """The active-row rule, inherited rather than re-implemented.

    A re-import leaves the old row soft-deleted beside the new one, and a matcher
    that counted both would call one file ambiguous and refuse to place it.
    """
    intents = [_intent(cfg, declared, PLAIN)]
    placed = _placements(
        cfg,
        declared,
        intents,
        [_row(cfg, PLAIN, "1", deleted=True), _row(cfg, PLAIN, "2")],
    )
    assert placed[0].placement is routing_pass.Placement.RESOLVED
    assert placed[0].content_id == "2"


def test_two_active_rows_on_one_location_are_ambiguous_and_never_written(cfg, declared):
    intents = [_intent(cfg, declared, PLAIN)]
    placed = _placements(cfg, declared, intents, [_row(cfg, PLAIN, "1"), _row(cfg, PLAIN, "2")])
    assert placed[0].placement is routing_pass.Placement.AMBIGUOUS
    assert placed[0].content_ids == ("1", "2")
    assert placed[0].placement not in routing_pass.WRITABLE


def test_a_location_that_resolves_to_no_path_is_not_reported_as_a_missing_import(
    cfg, declared
):
    """A configuration failure and a missing import have opposite answers.

    An unmapped volume prefix reaches no row for a reason importing cannot fix,
    so counting it as evidence that the import has not happened would send a
    person round the same loop forever.
    """
    intent = replace(
        _intent(cfg, declared, PLAIN), location="/somewhere/nothing/maps/onto/x.flac"
    )
    placed = _placements(cfg, declared, [intent], [_row(cfg, PLAIN, "1")])
    assert placed[0].placement is routing_pass.Placement.UNRESOLVED
    assert routing_pass.readiness(placed) is routing_pass.Readiness.NOT_READY


def test_a_recorded_prefix_the_map_covers_resolves_to_its_row(cfg, declared):
    """Both sides through one resolver, with the volume prefix map applied.

    Most active rows in a real library record a volume name the drive stopped
    using years ago. A pass that did not consult the map would report every one
    of them absent and tell the user the import never happened.
    """
    older = "/an/older/mount"
    intent = replace(_intent(cfg, declared, PLAIN), location=f"{older}/Music/{PLAIN}")
    rules = [locations.PrefixRule(older, str(cfg.library.root))]
    placed = _placements(cfg, declared, [intent], [_row(cfg, PLAIN, "1")], prefix_map=rules)
    assert placed[0].placement is routing_pass.Placement.RESOLVED
    assert placed[0].content_id == "1"


def test_a_composition_form_mismatch_between_the_ledger_and_the_row_resolves(
    cfg, declared
):
    intent = _intent(cfg, declared, DECOMPOSED)
    placed = _placements(cfg, declared, [intent], [_row(cfg, COMPOSED, "1")])
    assert placed[0].placement is routing_pass.Placement.RESOLVED


def test_readiness_over_nothing_pending_is_ready_rather_than_not_ready(cfg, declared):
    """A run with nothing to route is not a run waiting for an import.

    Reporting not-ready here would make the empty case indistinguishable from the
    before-the-import case, and the refusal a caller built on it would refuse a
    run that has nothing left to do.
    """
    assert routing_pass.readiness(()) is routing_pass.Readiness.READY


def test_a_partly_imported_run_is_ready_and_places_only_what_arrived(cfg, declared):
    """Supplementary. The real shape of a run somebody imported in two goes."""
    intents = [_intent(cfg, declared, PLAIN), _intent(cfg, declared, THIRD)]
    placed = _placements(cfg, declared, intents, [_row(cfg, PLAIN, "1")])
    assert routing_pass.readiness(placed) is routing_pass.Readiness.READY
    assert [item.placement for item in placed] == [
        routing_pass.Placement.RESOLVED,
        routing_pass.Placement.NOT_IMPORTED,
    ]


# ═══════════════════════════════════════════════════════════════════════════
# Part 3: the pass, against a real database and the real session spine
# ═══════════════════════════════════════════════════════════════════════════


def _registry(mode: tree_registry.Mode, *, root_id: str | None = ADOPTED_ROOT):
    if mode is tree_registry.Mode.DATABASE:
        return tree_registry.Registry(
            (
                tree_registry.TreeRecord(
                    tree_id=TREE_ID,
                    mode=mode,
                    cutover_on=date(2026, 8, 1),
                    root_id=root_id,
                ),
            )
        )
    return tree_registry.Registry((tree_registry.TreeRecord(tree_id=TREE_ID, mode=mode),))


def _record_locations(db_path: Path, recorded: dict[str, str], *, removed=frozenset()):
    """Give the disposable database's collection rows the paths this run decided on.

    Written straight into the file BEFORE the guarded writer ever opens it,
    because creating a collection row is exactly what the additive whitelist
    forbids: intake creates those rows, and this unit only ever places rows
    somebody else's import already made.
    """
    import sqlite3

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
    """Size and modification time of every file under each root.

    The same shape ``tests/test_cli_contract.py`` uses for the same question, and
    for the same reason: the defect class is a path that wrote something before
    it decided not to, and only a fingerprint either side can see that.
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


@pytest.fixture
def db(cfg, monkeypatch):
    """A disposable database in a temporary directory, opened through the gate.

    Built rather than substituted from a supplied snapshot, and that is a
    deliberate departure from the sibling suites. What this file proves end to
    end is that a track whose placement was decided BEFORE its row existed
    reaches the tree once the row arrives, which needs rows whose recorded
    locations this test chose. A supplied library's rows record somebody else's
    paths, so substituting one would replace the proof with a different one.
    """
    path = Path(cfg.library.db_path)
    _build_disposable_database(path)
    _record_locations(path, {"1": _music(cfg, COMPOSED), "2": _music(cfg, PLAIN)})
    # The capture's integrity check reaches for the encryption key by default and
    # an unencrypted fixture fails it, which would report every session here as
    # having no verified recovery point. Compensated at the FIXTURE, never by
    # giving the writer a verifier argument it could be handed a lie through.
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


def _route(cfg, db, adopted, declared_taxonomy, *, rows=None, registry=None, **kwargs):
    return routing_pass.route(
        cfg,
        db,
        session_id=SESSION_ID,
        registry=registry
        if registry is not None
        else _registry(tree_registry.Mode.DATABASE, root_id=str(adopted.ID)),
        declared=declared_taxonomy,
        rows=routing_pass.content_rows(db) if rows is None else rows,
        root_exists=lambda _root: True,
        analysis_roots=[Path(cfg.library.root) / "Music"],
        **kwargs,
    )


def _memberships(db, content_id: str) -> int:
    return db.get_playlist_songs(ContentID=str(content_id)).count()


def test_the_pass_places_a_track_and_marks_it_only_after_the_commit(
    cfg, gates_pass, db, adopted_root, declared
):
    """The happy path, end to end: decide, import, route, and the mark follows.

    The mark is asserted against the RELOADED ledger rather than against the
    report, because what a later process reads is the only thing that decides
    whether the work is repeated.
    """
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    report = _route(cfg, db, adopted_root, declared)

    assert report.readiness is routing_pass.Readiness.READY
    assert len(report.routed) == 1
    assert report.memberships[0].added == 1
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()
    assert routing_pass.read(cfg).for_session(SESSION_ID)[0].state is routing_pass.TrackState.ROUTED
    assert _memberships(db, "2") == 1


def test_the_track_lands_inside_the_tree_the_cutover_adopted(
    cfg, gates_pass, db, adopted_root, declared
):
    """Proved by walking UP from the membership row, never down by name.

    A lookup by name finds a namesake anywhere in the library and reports
    success, which is the silent parallel tree wearing the check meant to prevent
    it. Starting from the membership row that actually exists cannot do that.
    """
    from pyrekordbox.db6 import tables

    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    _route(cfg, db, adopted_root, declared)

    folder_display, sub_display = routing_pass.destination(declared, *_destination(declared))
    membership = db.get_playlist_songs(ContentID="2").first()
    playlist = db.session.query(tables.DjmdPlaylist).filter_by(ID=membership.PlaylistID).one()
    assert playlist.Name == sub_display
    folder = db.session.query(tables.DjmdPlaylist).filter_by(ID=playlist.ParentID).one()
    assert folder.Name == folder_display
    assert str(folder.ParentID) == str(adopted_root.ID)


def test_the_pass_run_before_the_import_is_read_only(
    cfg, gates_pass, db, adopted_root, declared
):
    """The plan's third scenario, asserted against the FILESYSTEM.

    "Resolves nothing and marks nothing" is not a claim about the return value. A
    pass that took a session, wrote a lock, and then decided it had nothing to do
    would satisfy every assertion about its report while leaving a trace, so the
    whole state tree is fingerprinted either side of the call.
    """
    intent = replace(
        _intent(cfg, declared, PLAIN), location=_music(cfg, "Not Yet There.flac")
    )
    intent = replace(intent, track=routing_pass.track_id(intent.location))
    routing_pass.record_intents(cfg, [intent])

    # The STATE tree, which is everything a pass could write: the lock, the
    # acknowledgment, the session log, the snapshot store and the ledger itself.
    # The database file is deliberately outside it, because opening one in
    # write-ahead-log mode touches its shared-memory index on a pure read and
    # that would make this assert on the wrong thing.
    roots = (
        config.library_state_dir(cfg),
        config.installation_state_dir(),
        config.config_dir(),
    )
    before = _state_fingerprint(*roots)
    report = _route(cfg, db, adopted_root, declared)
    assert _state_fingerprint(*roots) == before, (
        "the pass wrote to the state tree before deciding the library was ready; "
        "a read-only path that leaves a trace has already done something"
    )

    assert report.readiness is routing_pass.Readiness.NOT_READY
    assert report.routed == ()
    assert report.memberships == ()
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1


def test_a_crash_between_the_commit_and_the_mark_converges(
    cfg, gates_pass, db, adopted_root, declared, monkeypatch
):
    """The plan's second scenario, driven by an ACTUAL crash in the window.

    Not a test that the code contains the two calls in that order: an assertion
    over source text cannot tell a correct order from a coincidental one, and the
    property being claimed is about what survives a process that stopped. So the
    mark is made to raise, the pass is re-driven for real, and the membership
    rows are counted in the database afterwards.

    THE ORDER IS THE WHOLE PROPERTY. Marked first and committed second, this
    crash would leave a track recorded as placed and a playlist that never got
    it, with nothing left that knows to try again. Committed first, the cost is a
    re-run and the re-run deduplicates.
    """
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    real_mark = routing_pass.mark

    def die(*args, **kwargs):
        raise RuntimeError("the process was killed between the commit and the mark")

    monkeypatch.setattr(routing_pass, "mark", die)
    with pytest.raises(RuntimeError, match="between the commit and the mark"):
        _route(cfg, db, adopted_root, declared)

    # The commit landed and the ledger did not move, which is exactly the state a
    # kill in that window leaves behind.
    assert _memberships(db, "2") == 1
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1

    # The restart. Only the mark is put back: undoing every patch would also undo
    # the platform seams this whole file runs behind, and the run would then fail
    # on the machine rather than on the property under test.
    monkeypatch.setattr(routing_pass, "mark", real_mark)
    report = _route(cfg, db, adopted_root, declared)
    assert report.memberships[0].added == 0
    assert report.memberships[0].already_present == 1
    assert _memberships(db, "2") == 1, "the recovery run duplicated the membership"
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()


def test_a_second_pass_over_a_settled_run_writes_nothing(
    cfg, gates_pass, db, adopted_root, declared
):
    """Re-running is the recovery procedure, so re-running must be free."""
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    _route(cfg, db, adopted_root, declared)
    second = _route(cfg, db, adopted_root, declared)
    assert second.placed == ()
    assert second.memberships == ()
    assert _memberships(db, "2") == 1


def test_a_track_whose_membership_cannot_be_proved_is_not_marked(
    cfg, gates_pass, db, adopted_root, declared, monkeypatch
):
    """The fail-safe direction on the read-back.

    The mark follows the commit AND the proof, so a proof that cannot be made
    leaves the track outstanding and a later pass tries again. Marking on the
    writer's own accounting would make the read-back decoration: the one thing it
    can catch is a commit that reported success and placed nothing.
    """
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    monkeypatch.setattr(routing_pass, "membership_proven", lambda *args, **kwargs: False)
    report = _route(cfg, db, adopted_root, declared)

    assert report.routed == ()
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1


def test_a_tree_still_on_the_bridge_refuses_and_marks_nothing(
    cfg, gates_pass, db, adopted_root, declared
):
    """U18's inverse guard reaches the caller, and the ledger is untouched.

    A pass that swallowed the refusal and marked the track anyway would record a
    placement into a medium that does not own the tree.
    """
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    with pytest.raises(tree_registry.TreeModeRefused):
        _route(cfg, db, adopted_root, declared, registry=_registry(tree_registry.Mode.XML))
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1
    assert _memberships(db, "2") == 0


def test_a_missing_acknowledgment_refuses_before_the_database_is_touched(
    cfg, monkeypatch, db, adopted_root, declared
):
    """The session gates are the writer's, and the pass does not route around them."""
    monkeypatch.setattr(
        preflight,
        "default_identity_provider",
        lambda: (lambda _path: cfg.library.volume_id),
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    with pytest.raises(CratekitError) as excinfo:
        _route(cfg, db, adopted_root, declared)
    assert excinfo.value.cause.code is ExitCode.ACK_REQUIRED
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1


def test_content_rows_reads_the_soft_delete_marker_off_the_row(cfg, monkeypatch, tmp_path):
    """The withdrawn answer is only as good as the column it comes from.

    Every test above supplies its own row values, which proves the RULE and
    proves nothing about where the marker is read. This one opens a real database
    with one row removed and asks the reader.
    """
    path = tmp_path / "removed" / "master.db"
    _build_disposable_database(path)
    _record_locations(
        path, {"1": _music(cfg, COMPOSED), "2": _music(cfg, PLAIN)}, removed={"2"}
    )
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer,
        "integrity_ok",
        lambda target, **kwargs: real_integrity_ok(target, unlock=False),
    )
    handle = rb_writer.open_db(path, unlock=False, cfg=cfg)
    try:
        rows = {row.content_id: row for row in routing_pass.content_rows(handle)}
    finally:
        rb_writer.close_db(handle)

    assert rows["2"].deleted is True
    assert rows["1"].deleted is False
    assert rows["2"].recorded == _music(cfg, PLAIN)


# ═══════════════════════════════════════════════════════════════════════════
# Part 4: the run that will not close while anything is still nowhere
# ═══════════════════════════════════════════════════════════════════════════


def _open_run(cfg):
    return session.open_session(
        cfg, workflow=routing_pass.ROUTING_WORKFLOW, session_id=SESSION_ID
    )


def test_a_run_with_nothing_to_route_closes(cfg, gates_pass):
    """The plan's fifth scenario. A run that deferred nothing is not held up."""
    record = _open_run(cfg)
    closed = routing_pass.close_run(record, cfg)
    assert closed.state is session.SessionState.CLOSED
    assert closed.terminal


def test_a_run_with_a_pending_track_refuses_to_close(cfg, gates_pass, declared):
    """The plan's first scenario, first half.

    The refusal names the class of answer rather than a failure: nothing is
    broken, the tool has done its half and the placement has not landed yet.
    """
    record = _open_run(cfg)
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])

    with pytest.raises(CratekitError) as excinfo:
        routing_pass.close_run(record, cfg)
    assert excinfo.value.cause.reason == "routing-outstanding"
    assert excinfo.value.cause.code is ExitCode.PENDING_HUMAN
    assert session.read_record(SESSION_ID, cfg).state is session.SessionState.OPEN


def test_a_run_closes_once_the_routing_pass_has_placed_its_track(
    cfg, gates_pass, db, adopted_root, declared
):
    """The plan's first scenario, second half. The same run, after the pass."""
    record = _open_run(cfg)
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    with pytest.raises(CratekitError):
        routing_pass.close_run(record, cfg)

    _route(cfg, db, adopted_root, declared)
    closed = routing_pass.close_run(record, cfg)
    assert closed.state is session.SessionState.CLOSED


def test_a_run_whose_track_has_not_been_imported_still_refuses_to_close(
    cfg, gates_pass, db, adopted_root, declared
):
    """The pass ran, said not-ready, and settled nothing. The run stays open.

    A pass that returned cleanly because there was nothing it could do must not
    be mistaken for a pass that finished the work.
    """
    record = _open_run(cfg)
    intent = replace(
        _intent(cfg, declared, PLAIN), location=_music(cfg, "Not Yet There.flac")
    )
    routing_pass.record_intents(
        cfg, [replace(intent, track=routing_pass.track_id(intent.location))]
    )

    assert _route(cfg, db, adopted_root, declared).readiness is routing_pass.Readiness.NOT_READY
    with pytest.raises(CratekitError):
        routing_pass.close_run(record, cfg)


def test_a_track_deleted_after_import_is_surfaced(
    cfg, gates_pass, db, adopted_root, declared
):
    """The plan's fourth scenario, first half. Surfaced, never auto-skipped."""
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    report = _route(
        cfg,
        db,
        adopted_root,
        declared,
        rows=[_row(cfg, PLAIN, "2", deleted=True)],
    )

    assert report.readiness is routing_pass.Readiness.READY
    assert [item.placement for item in report.withdrawn] == [routing_pass.Placement.WITHDRAWN]
    assert report.routed == ()
    assert report.memberships == ()


def test_the_routing_pass_never_acknowledges_a_track_by_itself(
    cfg, gates_pass, db, adopted_root, declared
):
    """The separation that makes surfacing mean anything.

    A pass that could settle what it failed to place would make "surfaced for a
    person to answer" and "quietly skipped" the same thing, which is the failure
    the fifth approach point names.
    """
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    _route(cfg, db, adopted_root, declared, rows=[_row(cfg, PLAIN, "2", deleted=True)])

    states = {entry.state for entry in routing_pass.read(cfg).for_session(SESSION_ID)}
    assert states == {routing_pass.TrackState.INTENDED}


def test_a_surfaced_track_closes_the_run_only_after_it_is_acknowledged(
    cfg, gates_pass, db, adopted_root, declared
):
    """The plan's fourth scenario, second half, and the ONLY way out of it.

    Re-running the pass is asserted not to help, because a track somebody deleted
    is never coming back and a remedy that has already been spent is what sends a
    person round a loop.
    """
    record = _open_run(cfg)
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    removed = [_row(cfg, PLAIN, "2", deleted=True)]

    _route(cfg, db, adopted_root, declared, rows=removed)
    with pytest.raises(CratekitError):
        routing_pass.close_run(record, cfg)

    _route(cfg, db, adopted_root, declared, rows=removed)
    with pytest.raises(CratekitError):
        routing_pass.close_run(record, cfg)

    track = routing_pass.read(cfg).for_session(SESSION_ID)[0].track
    routing_pass.acknowledge(cfg, [track], actor="a-person", note="removed in rekordbox")

    closed = routing_pass.close_run(record, cfg)
    assert closed.state is session.SessionState.CLOSED
    settled = routing_pass.read(cfg).for_session(SESSION_ID)[0]
    assert settled.state is routing_pass.TrackState.ACKNOWLEDGED
    assert settled.actor == "a-person"


def test_abandoning_a_run_is_not_gated_on_routing(cfg, gates_pass, declared):
    """The escape is not gated, because a gate on the escape is a trap.

    Closing claims a run finished, and that claim is what routing has to back up.
    Abandoning claims the opposite, so refusing it would leave a user with a run
    they can neither finish nor give up on.
    """
    record = _open_run(cfg)
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    abandoned = routing_pass.close_run(
        record, cfg, state=session.SessionState.ABANDONED
    )
    assert abandoned.state is session.SessionState.ABANDONED


def test_one_run_of_another_session_does_not_hold_this_one_open(
    cfg, gates_pass, declared
):
    """Outstanding is asked per run, so one stalled run does not freeze the rest."""
    record = _open_run(cfg)
    routing_pass.record_intents(
        cfg, [_intent(cfg, declared, PLAIN, session_id="another-run")]
    )
    assert routing_pass.close_run(record, cfg).state is session.SessionState.CLOSED


# ═══════════════════════════════════════════════════════════════════════════
# The unit's verification: one real run, imported, routed, closed
# ═══════════════════════════════════════════════════════════════════════════


def test_one_real_run_imports_routes_and_closes(cfg, gates_pass, declared, monkeypatch):
    """Import, route, tracks appear in database-native trees, run closes.

    Against a DISPOSABLE database in a temporary directory, never the live
    library. The import is modelled the way it really happens: the database is
    CLOSED, the row appears while this process is not holding it, and the pass
    opens it again afterwards. Doing it that way is not ceremony; it is the only
    shape in which "run the pass before importing" and "run it after" are two
    different states of the same run rather than two different tests.
    """
    from pyrekordbox.db6 import tables

    path = Path(cfg.library.db_path)
    _build_disposable_database(path)
    # Nothing recorded against either row yet: this library has not been imported.
    _record_locations(path, {"1": "", "2": ""})
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer,
        "integrity_ok",
        lambda target, **kwargs: real_integrity_ok(target, unlock=False),
    )

    record = _open_run(cfg)
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])

    def drive(handle):
        adopted = rb_writer.ensure_folder(handle, TREE_DISPLAY)
        handle.session.commit()
        return routing_pass.route(
            cfg,
            handle,
            session_id=SESSION_ID,
            registry=_registry(tree_registry.Mode.DATABASE, root_id=str(adopted.ID)),
            declared=declared,
            rows=routing_pass.content_rows(handle),
            root_exists=lambda _root: True,
            analysis_roots=[Path(cfg.library.root) / "Music"],
        ), adopted

    # 1. Before the import. Nothing resolves, nothing is marked, the run refuses
    #    to close.
    handle = rb_writer.open_db(path, unlock=False, cfg=cfg)
    try:
        early, _ = drive(handle)
    finally:
        rb_writer.close_db(handle)
    assert early.readiness is routing_pass.Readiness.NOT_READY
    assert early.routed == ()
    with pytest.raises(CratekitError) as excinfo:
        routing_pass.close_run(record, cfg)
    assert excinfo.value.cause.reason == "routing-outstanding"

    # 2. The person imports. The row exists now, and this process was not holding
    #    the database while that happened.
    _record_locations(path, {"2": _music(cfg, PLAIN)})

    # 3. The pass runs again, places the track, and marks it.
    handle = rb_writer.open_db(path, unlock=False, cfg=cfg)
    try:
        late, adopted = drive(handle)
        assert late.readiness is routing_pass.Readiness.READY
        assert len(late.routed) == 1
        assert late.memberships[0].added == 1

        folder_display, sub_display = routing_pass.destination(
            declared, *_destination(declared)
        )
        membership = handle.get_playlist_songs(ContentID="2").first()
        assert membership is not None, "the track reached no playlist"
        playlist = (
            handle.session.query(tables.DjmdPlaylist).filter_by(ID=membership.PlaylistID).one()
        )
        folder = (
            handle.session.query(tables.DjmdPlaylist).filter_by(ID=playlist.ParentID).one()
        )
        assert (playlist.Name, folder.Name) == (sub_display, folder_display)
        assert str(folder.ParentID) == str(adopted.ID)
    finally:
        rb_writer.close_db(handle)

    # 4. The run closes.
    closed = routing_pass.close_run(record, cfg)
    assert closed.state is session.SessionState.CLOSED
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()


# ═══════════════════════════════════════════════════════════════════════════
# The softening paths this unit creates, closed in the commit that creates them
# ═══════════════════════════════════════════════════════════════════════════


def _made_up_actors(source: str) -> list[str]:
    """Every ``acknowledge`` call whose actor is a literal the caller invented.

    An AST walk rather than a text search. The rule is about the ARGUMENT, and a
    text search cannot tell a call from the word appearing in a docstring, which
    is the shape that gets a guard muted rather than obeyed (P7).
    """
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue
        name = node.func.attr if isinstance(node.func, ast.Attribute) else (
            node.func.id if isinstance(node.func, ast.Name) else ""
        )
        if name != "acknowledge":
            continue
        for keyword in node.keywords:
            if keyword.arg == "actor" and isinstance(keyword.value, ast.Constant):
                found.append(ast.unparse(node))
    return found


def test_the_made_up_actor_guard_bites():
    """The fixture half. A guard that has never fired is a guard nobody has run."""
    assert _made_up_actors('routing_pass.acknowledge(cfg, t, actor="cli")')
    assert _made_up_actors("acknowledge(cfg, t, actor='cli')")
    assert _made_up_actors("routing_pass.acknowledge(cfg, t, actor=decision.actor)") == []
    assert _made_up_actors('"acknowledge with actor=... somewhere in prose"') == []


def test_no_caller_acknowledges_a_track_with_an_actor_it_invented():
    """R34's shape, one layer up, ARMED NOW rather than when the first caller lands.

    ``acknowledge`` refuses an empty actor, and that is all a function can do: it
    cannot tell a name a person gave from a constant the calling code supplied.
    A caller passing a literal would satisfy the check while recording that the
    product acknowledged the track to itself, which is precisely what R34 forbids
    for a decision of this class. Armed over the whole package today, so the
    first caller to try it fails rather than the guard being written after the
    fact and only ever confirming what already shipped.
    """
    offenders: dict[str, list[str]] = {}
    for path in sorted(SRC_ROOT.rglob("*.py")):
        if "_vendor" in path.parts:
            continue
        found = _made_up_actors(path.read_text())
        if found:
            offenders[path.relative_to(SRC_ROOT).as_posix()] = found
    assert not offenders, (
        f"acknowledgments recorded against an actor the code made up: {offenders}. "
        f"The actor is the person who decided, and it reaches this layer from a "
        f"decision the CLI recorded against the run, never from a literal."
    )


@requires("cratekit.intake.collection_xml")
def test_the_intake_pipeline_records_its_routing_intents_at_the_decision():
    """P5's countdown, armed the moment the pipeline that owes it lands.

    Everything in this file is a mechanism with no subject until something writes
    an intent, and the only place that can is intake, at the point it decides
    where a new track goes. A pipeline that skipped the call would leave every
    run closing cleanly with nothing outstanding, because nothing was ever
    recorded, and this whole suite would stay green over a feature that never
    runs.

    It walks the SYNTAX TREE for the call rather than searching the text, because
    a module's own docstring explaining why it defers routing would satisfy a text
    search with every call deleted. That is the softening path wearing the
    guard's clothes, and this repository has already shipped it once.
    """
    package = SRC_ROOT / "cratekit" / "intake"
    called = False
    for path in sorted(package.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Call):
                name = (
                    node.func.attr
                    if isinstance(node.func, ast.Attribute)
                    else (node.func.id if isinstance(node.func, ast.Name) else "")
                )
                if name == "record_intents":
                    called = True
    assert called, (
        "the intake pipeline never records a routing intent, so no run ever has "
        "anything deferred and the deferred-routing mechanism has no subject"
    )
