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
from cratekit.core.cause import REASONS, CratekitError
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.write import routing_pass, trees
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
    routing_pass.mark(cfg, [track], routing_pass.TrackState.ROUTED, session_id=SESSION_ID)
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
        routing_pass.acknowledge(cfg, [track], session_id=SESSION_ID, actor="   ")


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

    THE READINESS ASSERTION HERE USED TO SAY ``NOT_READY``, which is the sentence
    this docstring forbids, written one line below it. That is finding eight, and
    the answer is now its own member: the pass still writes nothing, and it no
    longer tells anybody to import a track whose location maps nowhere.
    """
    intent = replace(
        _intent(cfg, declared, PLAIN), location="/somewhere/nothing/maps/onto/x.flac"
    )
    placed = _placements(cfg, declared, [intent], [_row(cfg, PLAIN, "1")])
    assert placed[0].placement is routing_pass.Placement.UNRESOLVED
    assert routing_pass.readiness(placed) is routing_pass.Readiness.UNANSWERABLE


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
                    source=tree_registry.DerivationSource.TAXONOMY,
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


def _route(
    cfg,
    db,
    adopted,
    declared_taxonomy,
    *,
    rows=None,
    registry=None,
    session_id=SESSION_ID,
    **kwargs,
):
    return routing_pass.route(
        cfg,
        db,
        session_id=session_id,
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
    routing_pass.acknowledge(
        cfg, [track], session_id=SESSION_ID, actor="a-person", note="removed in rekordbox"
    )

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


def _module_string_constants(tree: ast.AST) -> frozenset[str]:
    """Every module-level name bound to a plain string in this source.

    ``actor=ACTOR`` reads like a value and is a literal with a name on it, which
    is the cheapest way past a guard that only looks at the argument node.
    """
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
    """True when this expression's value was chosen by the code, not by a person.

    RECURSIVE, because every bypass found in review was one wrapper away from a
    literal: an f-string with no substitution, a conditional between two
    literals, two literals concatenated, a module constant. An expression
    carrying a runtime value is not invented, which is why an f-string WITH a
    substitution and a plain parameter both pass.
    """
    if node is None:
        return False
    if isinstance(node, ast.Constant):
        return isinstance(node.value, str)
    if isinstance(node, ast.JoinedStr):
        # An f-string with nothing substituted into it is a literal wearing a
        # prefix. One with a substitution carries a value from somewhere.
        return not any(isinstance(part, ast.FormattedValue) for part in node.values)
    if isinstance(node, ast.IfExp):
        return _is_invented(node.body, constants) and _is_invented(node.orelse, constants)
    if isinstance(node, ast.BinOp):
        return _is_invented(node.left, constants) and _is_invented(node.right, constants)
    if isinstance(node, ast.Name):
        return node.id in constants
    return False


def _made_up_actors(source: str) -> list[str]:
    """Every ``acknowledge`` call whose actor is a value the caller invented.

    An AST walk rather than a text search. The rule is about the ARGUMENT, and a
    text search cannot tell a call from the word appearing in a docstring, which
    is the shape that gets a guard muted rather than obeyed (P7).

    IT LOOKS THROUGH FOUR WRAPPERS AND ONE UNPACKING, because matching only a
    bare constant left the guard passable by ``actor=f"cli"``, ``actor=ACTOR``,
    ``actor="cli" if x else "cli"`` and ``**{"actor": "cli"}``. Every one of those
    records the product acknowledging a track to itself, which is what R34
    forbids for a decision of this class. The other direction is asserted too:
    a caller passing a parameter, an attribute, an f-string with a substitution,
    or a mapping this walk cannot see is left alone, because a guard that fires
    on correct code gets routed around and then protects nothing.
    """
    tree = ast.parse(source)
    constants = _module_string_constants(tree)
    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = (
            node.func.attr
            if isinstance(node.func, ast.Attribute)
            else (node.func.id if isinstance(node.func, ast.Name) else "")
        )
        if name != "acknowledge":
            continue
        for keyword in node.keywords:
            if keyword.arg == "actor":
                if _is_invented(keyword.value, constants):
                    found.append(ast.unparse(node))
                continue
            if keyword.arg is None and isinstance(keyword.value, ast.Dict):
                # ``**{"actor": ...}``: the same argument, spelled so a check on
                # keyword names never sees it.
                for key, value in zip(keyword.value.keys, keyword.value.values):
                    if (
                        isinstance(key, ast.Constant)
                        and key.value == "actor"
                        and _is_invented(value, constants)
                    ):
                        found.append(ast.unparse(node))
    return found


# The fixture half of this guard, in both directions, is at the end of this file
# under finding 11. It was four assertions in one test and is now two
# parametrized sets, because a bypass that a reviewer found has to be a named
# case somebody can read rather than one more line in a list.


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


# ═══════════════════════════════════════════════════════════════════════════
# Part 5: the defects an adversarial review found in the shape above
#
# Every test below was written against the DEFECT and observed failing before
# the fix beside it existed. They are grouped by the finding they close rather
# than by the part of the module they touch, because what has to stay true is
# the property, and the property is what the finding named.
# ═══════════════════════════════════════════════════════════════════════════


def _second_destination(declared_taxonomy):
    """A second bucket the shipped template declares, DERIVED rather than named.

    The pair of destinations is what makes "two runs, one file" a real test: two
    runs that happened to decide the same folder prove nothing about whose record
    is whose.
    """
    bucket = declared_taxonomy.buckets[1]
    sub = routing.energy_sub(declared_taxonomy, bucket.id, declared_taxonomy.energy.scale_max)
    assert sub is not None, "the shipped template's second bucket declares no sub"
    return bucket.id, sub.id


def _where(db, content_id: str) -> list[tuple[str | None, str]]:
    """Every (folder, playlist) pair this content row actually sits in.

    Walked UP from the membership rows, never down by name, for the reason
    ``membership_proven`` gives: a lookup by name finds a namesake anywhere.
    """
    found: list[tuple[str | None, str]] = []
    for membership in db.get_playlist_songs(ContentID=str(content_id)):
        playlist = db.get_playlist(ID=str(membership.PlaylistID))
        if playlist is None:
            continue
        folder = db.get_playlist(ID=str(playlist.ParentID))
        found.append((folder.Name if folder is not None else None, playlist.Name))
    return found


# ── Finding 1: the ledger is keyed per file, the close gate asks per run ─────


def test_a_second_run_deferring_one_file_does_not_take_over_the_first_runs_record(
    cfg, gates_pass, declared
):
    """One record per RUN and file, never one record per file.

    Two runs touching one path is ordinary: a re-download to the same location, a
    resumed intake, one track acquired twice from two sources. A ledger that can
    hold only one record for the path lets the second run take ownership of the
    first run's obligation, and the first run then closes reporting a placed
    track that is in no playlist at all.
    """
    first = session.open_session(
        cfg, workflow=routing_pass.ROUTING_WORKFLOW, session_id="run-one"
    )
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN, session_id="run-one")])
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN, session_id="run-two")])

    ledger = routing_pass.read(cfg)
    owners = sorted(entry.session_id for entry in ledger.intents)
    assert owners == ["run-one", "run-two"], (
        f"the ledger holds {owners}; one run's decision replaced the other's"
    )
    assert len(ledger.outstanding("run-one")) == 1
    assert len(ledger.outstanding("run-two")) == 1
    with pytest.raises(CratekitError) as excinfo:
        routing_pass.close_run(first, cfg)
    assert excinfo.value.cause.reason == "routing-outstanding"


def test_marking_one_runs_track_leaves_another_runs_record_alone(cfg, declared):
    """A mark is scoped to the run that made the decision it settles.

    Matching on the track alone lets one run's pass report a placement into ITS
    destination and settle a different run's record, whose destination was never
    written. The two records name the same file and mean different playlists.
    """
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN, session_id="run-one")])
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN, session_id="run-two")])
    track = routing_pass.read(cfg).for_session("run-two")[0].track

    routing_pass.mark(cfg, [track], routing_pass.TrackState.ROUTED, session_id="run-two")
    assert routing_pass.read(cfg).outstanding("run-two") == ()
    assert len(routing_pass.read(cfg).outstanding("run-one")) == 1


def test_two_overlapping_runs_over_one_file_each_reach_their_own_destination(
    cfg, gates_pass, db, adopted_root, declared
):
    """Both runs driven to completion, and neither closes while it still owes work.

    This is the whole of finding one in one drive: two runs decide two different
    destinations for one file, each pass writes ITS destination, each run refuses
    to close until its own record settles, and both destinations are in the
    library at the end.
    """
    first = session.open_session(
        cfg, workflow=routing_pass.ROUTING_WORKFLOW, session_id="run-one"
    )
    second = session.open_session(
        cfg, workflow=routing_pass.ROUTING_WORKFLOW, session_id="run-two"
    )
    other_bucket, other_sub = _second_destination(declared)
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN, session_id="run-one")])
    routing_pass.record_intents(
        cfg,
        [
            replace(
                _intent(cfg, declared, PLAIN, session_id="run-two"),
                bucket=other_bucket,
                sub=other_sub,
            )
        ],
    )
    first_destination = routing_pass.destination(declared, *_destination(declared))
    second_destination = routing_pass.destination(declared, other_bucket, other_sub)
    assert first_destination != second_destination

    # Run one places its track. Run two still owes its own.
    _route(cfg, db, adopted_root, declared, session_id="run-one")
    assert routing_pass.close_run(first, cfg).state is session.SessionState.CLOSED
    with pytest.raises(CratekitError) as excinfo:
        routing_pass.close_run(second, cfg)
    assert excinfo.value.cause.reason == "routing-outstanding"

    _route(cfg, db, adopted_root, declared, session_id="run-two")
    assert routing_pass.close_run(second, cfg).state is session.SessionState.CLOSED

    landed = sorted(_where(db, "2"))
    assert landed == sorted([first_destination, second_destination]), (
        f"the library holds {landed}; each run's own destination has to be written"
    )


# ── Finding 2: the soft-delete marker must never default to "active" ─────────


def test_a_row_that_cannot_report_the_soft_delete_marker_refuses(cfg):
    """U18 gave ``ContentRow.deleted`` no default. The producer must not supply one.

    A default of False means active, which is the permissive answer, so a binding
    that stops exposing the column hands every tombstone to the matcher as a live
    row. The pass then places a track the user deleted on purpose, marks it
    routed, and the run closes over it.
    """

    class Row:
        ID = "9"
        FolderPath = "/somewhere/nothing.flac"

    class Blind:
        def get_content(self):
            return [Row()]

    with pytest.raises(CratekitError) as excinfo:
        list(routing_pass.content_rows(Blind()))
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNREADABLE


def test_a_soft_delete_marker_that_reads_as_nothing_refuses(cfg):
    """An exposed column holding no value is the same hazard wearing a value.

    ``bool(None)`` is False, which is the permissive answer again, so a column
    that is present and null must refuse exactly as a missing one does.
    """

    class Row:
        ID = "9"
        FolderPath = "/somewhere/nothing.flac"
        rb_local_deleted = None

    class Blind:
        def get_content(self):
            return [Row()]

    with pytest.raises(CratekitError):
        list(routing_pass.content_rows(Blind()))


# ── Finding 3: one stale destination must not abort the whole pass ───────────


def test_a_destination_the_taxonomy_no_longer_declares_is_its_own_placement(
    cfg, declared
):
    """``Placement`` had five members and none of them meant this.

    A ledger naming a sub the active template dropped is a real state: somebody
    edited the taxonomy between the decision and the import. It is not a missing
    row and it is not a defect, and reporting it as either sends a person to the
    wrong remedy.
    """
    stale = replace(_intent(cfg, declared, PLAIN), sub="a-sub-this-library-dropped")
    placed = _placements(cfg, declared, [stale], [_row(cfg, PLAIN, "1")])
    assert placed[0].placement is routing_pass.Placement.UNDECLARED
    assert placed[0].placement not in routing_pass.WRITABLE


def test_one_stale_destination_does_not_stop_the_other_tracks_in_the_run(
    cfg, gates_pass, db, adopted_root, declared
):
    """The good track is placed, and the bad one is reported rather than raised.

    ``assert_settled`` promises the pass "places every track the library now holds
    a row for, and reports one reason per track it could not place". A bare
    ``KeyError`` out of the whole pass places none and reports no reason, so the
    documented remedy is spent and the run can never close.
    """
    good = _intent(cfg, declared, PLAIN)
    stale = replace(_intent(cfg, declared, COMPOSED), sub="a-sub-this-library-dropped")
    routing_pass.record_intents(cfg, [good, stale])

    report = _route(cfg, db, adopted_root, declared)

    assert _memberships(db, "2") == 1, "the good track was blocked by the stale one"
    assert report.routed == (good.track,)
    reasons = {item.intent.track: item.placement for item in report.placed}
    assert reasons[stale.track] is routing_pass.Placement.UNDECLARED
    outstanding = routing_pass.read(cfg).outstanding(SESSION_ID)
    assert [entry.track for entry in outstanding] == [stale.track]


# ── Finding 4: the recovery primitive is keyed on a mutable display name ─────


class _CrashOnce:
    """A mark that dies the first time and works afterwards.

    Replacing the mark outright would also undo the platform seams this whole
    file runs behind, and the run would then fail on the machine rather than on
    the property under test.
    """

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


def test_a_recovery_run_after_a_rekordbox_rename_refuses_rather_than_duplicating(
    cfg, gates_pass, db, adopted_root, declared, monkeypatch
):
    """R19 claims renaming a folder in rekordbox changes nothing, and re-running is the remedy.

    The module rests on "a re-run is cheap because membership deduplicates", and
    the dedup targets by DISPLAY NAME. Rename the folder between the crash and the
    recovery and the recovery re-creates the folder under the taxonomy name, adds
    the track a second time, and marks it routed. D5 forbids keying a persisted
    record by a display name; this is the same lesson on the recovery path.
    """
    from pyrekordbox.db6 import tables

    _crash_between_the_commit_and_the_mark(cfg, db, adopted_root, declared, monkeypatch)
    from cratekit.core import convergence

    # THE MAP THIS PASS JUST WROTE IS THE THING THAT MAKES A RENAME CONVERGE.
    # Wiping it is what leaves the leftover refusal standing: no recorded
    # identifier, a missing declared folder, and a track sitting under a name
    # the taxonomy does not know.
    convergence.record_nodes(cfg, TREE_ID, (), replace_all=True)
    folder_display, _sub_display = routing_pass.destination(declared, *_destination(declared))
    row = db.session.query(tables.DjmdPlaylist).filter_by(Name=folder_display).one()
    row.Name = "A Name Of Their Own"
    db.session.commit()

    with pytest.raises(CratekitError) as excinfo:
        _route(cfg, db, adopted_root, declared)
    assert excinfo.value.cause.reason == "routing-destination-renamed"
    assert _memberships(db, "2") == 1, "the recovery run duplicated the membership"
    assert len(routing_pass.read(cfg).outstanding(SESSION_ID)) == 1


def _taxonomy_with_the_first_bucket_renamed(new_display: str):
    """The shipped template, REBUILT, with one bucket's display name changed.

    Rebuilt through the real parser rather than patched onto the frozen object,
    because ``Taxonomy`` carries derived lookups beside its fields and a
    dataclass replacement leaves them describing the template that was there
    before. A test that edited the object in place would prove that the guard
    reads a stale index, which is not the property under test.
    """
    import tomllib
    from importlib import resources

    source = resources.files("cratekit") / "templates" / taxonomy.DEFAULT_TEMPLATE
    data = tomllib.loads(source.read_text(encoding="utf-8"))
    data["bucket"][0]["display"] = new_display
    return taxonomy.build_taxonomy(data)


def test_a_recovery_run_after_a_taxonomy_rename_converges_rather_than_duplicating(
    cfg, gates_pass, db, adopted_root, declared, monkeypatch
):
    """The template moved, not the library. The node map still names the folder."""
    _crash_between_the_commit_and_the_mark(cfg, db, adopted_root, declared, monkeypatch)
    renamed = _taxonomy_with_the_first_bucket_renamed("A Bucket Renamed")
    assert renamed.buckets[0].id == declared.buckets[0].id

    report = _route(cfg, db, adopted_root, renamed)
    assert len(report.routed) == 1
    assert _memberships(db, "2") == 1
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()


def test_a_recovery_run_after_a_rename_converges_once_the_tree_layer_can(
    cfg, gates_pass, db, adopted_root, declared, monkeypatch
):
    """P5's countdown for the refusal above, so it cannot become permanent.

    Refusing is correct and it is not service. What makes the re-run converge is
    a persisted map from the stable destination identifiers to the node
    identifiers a previous write used, which is the tree layer's record to own
    and the reason this obligation is registered against the unit that owns it
    rather than asserted in a docstring. When that lands, this file's rename
    scenario must end with one membership and no refusal.
    """
    from pyrekordbox.db6 import tables

    _crash_between_the_commit_and_the_mark(cfg, db, adopted_root, declared, monkeypatch)
    folder_display, _sub_display = routing_pass.destination(declared, *_destination(declared))
    row = db.session.query(tables.DjmdPlaylist).filter_by(Name=folder_display).one()
    row.Name = "A Name Of Their Own"
    db.session.commit()

    report = _route(cfg, db, adopted_root, declared)
    assert len(report.routed) == 1
    assert _memberships(db, "2") == 1, "the recovery run duplicated the membership"
    assert routing_pass.read(cfg).outstanding(SESSION_ID) == ()


def test_a_bucket_folder_that_does_not_exist_yet_is_not_mistaken_for_a_rename(
    cfg, gates_pass, db, adopted_root, declared
):
    """P7, the other direction. A guard that fires on correct code gets routed around.

    A track already filed in one declared bucket, being placed into a second
    declared bucket whose folder this library has never held, is the ordinary
    case. The refusal above must not touch it.
    """
    other_bucket, other_sub = _second_destination(declared)
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN, session_id="run-one")])
    _route(cfg, db, adopted_root, declared, session_id="run-one")
    routing_pass.record_intents(
        cfg,
        [
            replace(
                _intent(cfg, declared, PLAIN, session_id="run-two"),
                bucket=other_bucket,
                sub=other_sub,
            )
        ],
    )

    report = _route(cfg, db, adopted_root, declared, session_id="run-two")
    assert len(report.routed) == 1
    assert _memberships(db, "2") == 2


# ── Finding 5: the ledger's read-modify-write takes no lock ──────────────────


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
    routing_pass.record_intents(
        cfg,
        [
            routing_pass.RoutingIntent(
                track=routing_pass.track_id(location),
                session_id=run,
                location=location,
                tree="a_tree",
                bucket="a_bucket",
                sub="a_sub",
                decided="2026-08-02T00:00:00+00:00",
            )
        ],
    )
'''


def test_two_processes_recording_intents_lose_none_of_them(cfg, library, tmp_path):
    """REAL PROCESSES, not threads, because the hazard is a real process boundary.

    Two writers interleaving an unlocked read-modify-write erases a fully recorded
    decision. Nothing is then outstanding for it, the run closes clean, and a
    track that was decided sits in no ledger at all: the one shape this whole
    module exists to prevent, arriving through the writer rather than the reader.
    A thread test would prove something about one interpreter's scheduler; the
    ledger is documented as accumulating several runs from several sources.
    """
    import subprocess
    import sys

    script = tmp_path / "concurrent_writer.py"
    script.write_text(_CONCURRENT_WRITER)
    each = 60
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join([str(SRC_ROOT), str(REPO_ROOT)])

    processes = [
        subprocess.Popen(
            [sys.executable, str(script), str(library), run, str(each)],
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        for run in ("run-one", "run-two")
    ]
    for process in processes:
        _out, errors = process.communicate(timeout=300)
        assert process.returncode == 0, errors.decode()

    recorded = routing_pass.read(cfg).intents
    assert len(recorded) == 2 * each, (
        f"{2 * each} decisions were recorded and {len(recorded)} survived; an "
        f"unlocked read-modify-write erased the rest"
    )


def test_the_lock_is_a_declared_state_entry_that_a_restore_never_replaces(cfg):
    """A path composed under a state root is a file nothing walks or backs up.

    And the role is not a detail: a restore that replaced the directory holding
    this file would swap the inode a live lock is held on, and both holders would
    go on believing they had exclusive access with nothing raised. That is the
    argument the write lock and the session lock already record.
    """
    entry = config.state_file(routing_pass.LOCK_KEY)
    assert entry.root is config.StateRoot.LIBRARY
    assert entry.snapshot is config.SnapshotRole.NEVER_RESTORED
    assert config.library_coupled_dir(cfg) not in routing_pass.lock_path(cfg).parents


def test_everything_this_module_creates_is_private_under_any_umask(cfg, declared):
    """P1 and P3 together: walk the tree, do not name the files in it.

    The version of this test that named the ledger was already blind to the lock
    beside it on the day the lock landed, which is the shape P3 exists to stop. A
    walk covers whatever the next writer adds without anybody remembering, and
    both halves are asserted because a 0600 record inside a world-writable
    directory can be unlinked and replaced by any local account.
    """
    previous = os.umask(0o000)
    try:
        routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
        track = routing_pass.read(cfg).for_session(SESSION_ID)[0].track
        routing_pass.mark(
            cfg, [track], routing_pass.TrackState.ROUTED, session_id=SESSION_ID
        )
    finally:
        os.umask(previous)

    root = config.library_state_dir(cfg)
    permissive: list[str] = []
    for current, directories, files in os.walk(root):
        for name in directories:
            path = Path(current) / name
            if stat.S_IMODE(path.stat().st_mode) != config.PRIVATE_DIR_MODE:
                permissive.append(f"{path} is {oct(stat.S_IMODE(path.stat().st_mode))}")
        for name in files:
            path = Path(current) / name
            if stat.S_IMODE(path.stat().st_mode) != config.PRIVATE_FILE_MODE:
                permissive.append(f"{path} is {oct(stat.S_IMODE(path.stat().st_mode))}")
    assert stat.S_IMODE(root.stat().st_mode) == config.PRIVATE_DIR_MODE
    assert not permissive, f"created under umask 000 at a permissive mode: {permissive}"


# ── Finding 6: a run whose export was never imported must not close ──────────


def test_a_run_whose_export_was_never_imported_refuses_to_close(cfg, gates_pass):
    """The other state in which somebody still owes an act.

    The unit's thesis is that a run cannot close while somebody still owes an
    act. It enforced that for the routing half and not for the import half, so a
    run sitting in ``awaiting-import`` with its pending action still attached
    closed and released its capture, while the session spine went on refusing a
    database surface for that same record.
    """
    record = session.open_session(cfg, workflow="an-intake-workflow", session_id=SESSION_ID)
    pending = session.pending_import(
        record,
        artifact=cfg.library.root / "an-export.xml",
        summary="import this export into rekordbox",
        verify_verb="a-verify-verb",
    )
    session.mark_awaiting_import(record, pending, cfg)

    with pytest.raises(CratekitError) as excinfo:
        routing_pass.close_run(session.read_record(SESSION_ID, cfg), cfg)
    assert excinfo.value.cause.reason == "awaiting-import"
    assert excinfo.value.cause.code is ExitCode.PENDING_HUMAN
    assert session.read_record(SESSION_ID, cfg).state is session.SessionState.AWAITING_IMPORT


def test_abandoning_a_run_whose_export_was_never_imported_is_still_allowed(cfg, gates_pass):
    """The escape stays open, for the reason the routing gate leaves it open.

    A refusal with no way past it is how people learn to edit state files by
    hand, and abandoning is the claim that the run did NOT finish.
    """
    record = session.open_session(cfg, workflow="an-intake-workflow", session_id=SESSION_ID)
    pending = session.pending_import(
        record,
        artifact=cfg.library.root / "an-export.xml",
        summary="import this export into rekordbox",
        verify_verb="a-verify-verb",
    )
    session.mark_awaiting_import(record, pending, cfg)

    abandoned = routing_pass.close_run(
        session.read_record(SESSION_ID, cfg), cfg, state=session.SessionState.ABANDONED
    )
    assert abandoned.state is session.SessionState.ABANDONED


# ── Finding 7: every refusal has to carry its remedy to the boundary ─────────


def test_an_unreadable_ledger_carries_its_remedy_to_the_boundary(cfg):
    """S4. A refusal that is not a ``CratekitError`` reaches the user as a defect report.

    The command-line boundary converts anything that is not a structured cause
    into ``internal-error`` with ``report-defect``, discarding the remedy the
    exception was carrying. ``session.py`` already converts an unreadable backup
    fact file correctly, and this follows that precedent.
    """
    path = routing_pass.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{ not json")

    with pytest.raises(routing_pass.RoutingLedgerUnreadable) as excinfo:
        routing_pass.read(cfg)
    assert isinstance(excinfo.value, CratekitError)
    assert excinfo.value.cause.remediation.remedy is Remedy.RUN_DOCTOR
    assert excinfo.value.cause.reason in REASONS


def test_a_ledger_from_a_newer_build_carries_the_upgrade_remedy(cfg):
    """The same slug, a different remedy, which is why the remedy travels on the cause."""
    path = routing_pass.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"schema_version": routing_pass.SCHEMA_VERSION + 1, "intents": []})
    )
    with pytest.raises(CratekitError) as excinfo:
        routing_pass.read(cfg)
    assert excinfo.value.cause.remediation.remedy is Remedy.UPGRADE_CRATEKIT


def test_a_tree_still_on_the_bridge_carries_its_remedy_to_the_boundary(
    cfg, gates_pass, db, adopted_root, declared
):
    """The other refusal this unit can raise, and it came from the same shape."""
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    with pytest.raises(tree_registry.TreeModeRefused) as excinfo:
        _route(cfg, db, adopted_root, declared, registry=_registry(tree_registry.Mode.XML))
    assert isinstance(excinfo.value, CratekitError)
    assert excinfo.value.cause.remediation.remedy is excinfo.value.remedy


def test_every_refusal_this_module_raises_is_a_structured_cause():
    """P3. The set is DERIVED by walking the module rather than listed.

    A guard that names today's two exception types stops covering the third the
    day it is added, which is the same shape as a test that enumerates the files
    it claims to quantify over.
    """
    import inspect

    raised: set[str] = set()
    for node in ast.walk(ast.parse(inspect.getsource(routing_pass))):
        if not isinstance(node, ast.Raise) or node.exc is None:
            continue
        thrown = node.exc
        name = ""
        if isinstance(thrown, ast.Call):
            name = (
                thrown.func.attr
                if isinstance(thrown.func, ast.Attribute)
                else (thrown.func.id if isinstance(thrown.func, ast.Name) else "")
            )
        elif isinstance(thrown, ast.Name):
            name = thrown.id
        if name:
            raised.add(name)

    # ``ValueError`` is a programming-error guard on a constructor, not a refusal
    # a user can act on, and ``refuse`` already returns a structured cause.
    exempt = {"refuse", "ValueError"}
    checked = 0
    for name in sorted(raised - exempt):
        candidate = getattr(routing_pass, name, None)
        if not isinstance(candidate, type) or not issubclass(candidate, BaseException):
            continue
        checked += 1
        assert issubclass(candidate, CratekitError), (
            f"{name} is raised as a refusal and is not a CratekitError, so the "
            f"command-line boundary will flatten it to a defect report and throw "
            f"away the remedy it carries (S4)"
        )
    assert checked, "the walk found no raised exception type, so it proves nothing"


def test_every_refusal_the_pass_propagates_carries_its_remedy_too():
    """The same rule, over the module this pass RAISES THROUGH rather than from.

    DERIVED, by asking which exception types carry a remedy at all rather than by
    naming the two the review found. A type that goes to the trouble of holding a
    ``Remedy`` is a refusal somebody is meant to act on, and the only way that
    remedy survives the command-line boundary is a structured cause. Fixing the
    two named types and leaving a third beside them is precisely the shape P5
    calls out: the same lesson applied in one place and not the other, and the
    third one is invisible until somebody hits it.
    """
    import inspect

    checked = 0
    for _name, candidate in inspect.getmembers(tree_registry, inspect.isclass):
        if not issubclass(candidate, BaseException):
            continue
        if candidate.__module__ != tree_registry.__name__:
            continue
        signature = inspect.signature(candidate.__init__)
        holds_a_remedy = "remedy" in signature.parameters or "Remedy" in (
            inspect.getsource(candidate)
        )
        if not holds_a_remedy:
            continue
        checked += 1
        assert issubclass(candidate, CratekitError), (
            f"{candidate.__name__} carries a remedy and is not a CratekitError, "
            f"so the command-line boundary flattens it to a defect report and "
            f"the remedy it holds never reaches the person who needs it (S4)"
        )
    assert checked >= 2, "the walk found nothing carrying a remedy, so it proves nothing"


# ── Finding 8: readiness had two answers where the module argues for three ───


def test_a_run_whose_locations_all_resolve_to_nothing_is_not_told_to_import(
    cfg, declared
):
    """``readiness`` forbids the conflation the module docstring endorsed.

    An unresolvable location reaches no row for a configuration reason importing
    cannot fix. Answering "the import has not happened" sends a person round the
    same loop forever, and the file said both things at once.
    """
    intent = replace(
        _intent(cfg, declared, PLAIN), location="/somewhere/nothing/maps/onto/x.flac"
    )
    placed = _placements(cfg, declared, [intent], [_row(cfg, PLAIN, "1")])
    assert placed[0].placement is routing_pass.Placement.UNRESOLVED
    assert routing_pass.readiness(placed) is routing_pass.Readiness.UNANSWERABLE
    assert routing_pass.readiness(placed) is not routing_pass.Readiness.NOT_READY


def test_a_run_whose_destinations_are_all_undeclared_is_not_told_to_import(cfg, declared):
    """The second answerless placement, and it must not read as a missing import either."""
    stale = replace(_intent(cfg, declared, PLAIN), sub="a-sub-this-library-dropped")
    placed = _placements(cfg, declared, [stale], [_row(cfg, PLAIN, "1")])
    assert routing_pass.readiness(placed) is routing_pass.Readiness.UNANSWERABLE


def test_every_readiness_answer_except_ready_writes_nothing(
    cfg, gates_pass, db, adopted_root, declared, monkeypatch
):
    """DERIVED over the enum, so a member added later cannot acquire the writing answer.

    The direction is the property, exactly as it is for the settled and
    outstanding halves: only ``READY`` may write, and everything else, including a
    member nobody has classified yet, must leave the library alone.
    """
    routing_pass.record_intents(cfg, [_intent(cfg, declared, PLAIN)])
    for answer in routing_pass.Readiness:
        if answer is routing_pass.Readiness.READY:
            continue
        monkeypatch.setattr(routing_pass, "readiness", lambda _placed, _held=answer: _held)
        report = _route(cfg, db, adopted_root, declared)
        assert report.readiness is answer
        assert report.routed == ()
        assert report.memberships == ()
        assert _memberships(db, "2") == 0, f"{answer} wrote to the library"


def test_the_readiness_answers_are_three_rather_than_two():
    """One file cannot argue both sides of the same question.

    The module docstring endorsed the conflation and ``readiness`` forbade it. The
    contradiction is resolved in the direction the function argued for, which
    needs an answer that is neither ready nor not-ready to exist at all.
    """
    assert len(routing_pass.Readiness) >= 3
    assert routing_pass.Readiness.UNANSWERABLE not in (
        routing_pass.Readiness.READY,
        routing_pass.Readiness.NOT_READY,
    )


# ── Findings 9 and 10: the obligations a later unit owes ─────────────────────


def test_the_routing_verbs_have_landed():
    """U20 discharged the countdown: the four verbs are no longer planned.

    Derived from the registry, so a fifth entry added with a leftover marker
    fails here rather than shipping as a declared-but-absent verb.
    """
    from cratekit.cli import registry as cli_registry

    named = [
        entry
        for entry in cli_registry.ENTRIES
        if entry.module == "cratekit.write.routing_cli"
    ]
    assert named, "no entry names the routing command-line module any more"
    still_planned = [entry.name for entry in named if not entry.landed]
    assert not still_planned, (
        f"routing verbs still carry a planned_in marker: {still_planned}"
    )


def test_the_routing_command_line_module_is_no_longer_owed_in_the_register():
    """The countdown fired and was discharged, not left as a comment."""
    from tests import _pending

    assert "cratekit.write.routing_cli" not in _pending.PENDING


def test_the_routing_verbs_close_their_runs_through_the_gated_close():
    """P5's countdown for the close gate, armed when the surface that spends it lands.

    ``session.close_session`` is exported and bypasses the routing gate entirely.
    This unit has zero production callers, so nothing today obliges the first one
    to close through ``routing_pass.close_run``, and a verb that closed through
    the session spine would release its capture over a track sitting nowhere.
    """
    module = SRC_ROOT / "cratekit" / "write" / "routing_cli.py"
    sources = (
        [module]
        if module.exists()
        else sorted((SRC_ROOT / "cratekit" / "write" / "routing_cli").rglob("*.py"))
    )
    bypassed: list[str] = []
    gated = False
    for path in sources:
        for node in ast.walk(ast.parse(path.read_text())):
            if not isinstance(node, ast.Call):
                continue
            name = (
                node.func.attr
                if isinstance(node.func, ast.Attribute)
                else (node.func.id if isinstance(node.func, ast.Name) else "")
            )
            if name == "close_session":
                bypassed.append(ast.unparse(node))
            if name == "close_run":
                gated = True
    assert gated, "the routing verbs never close a run through the gated close"
    assert not bypassed, (
        f"the routing verbs close through the session spine directly: {bypassed}. "
        f"That releases the capture without asking whether the run still holds a "
        f"track that reached no playlist."
    )


def test_the_intake_pipeline_closes_its_runs_through_the_gated_close():
    """The same obligation against the unit that CREATES the deferred work."""
    package = SRC_ROOT / "cratekit" / "intake"
    bypassed: list[str] = []
    for path in sorted(package.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text())):
            if not isinstance(node, ast.Call):
                continue
            name = (
                node.func.attr
                if isinstance(node.func, ast.Attribute)
                else (node.func.id if isinstance(node.func, ast.Name) else "")
            )
            if name == "close_session":
                bypassed.append(f"{path.name}: {ast.unparse(node)}")
    assert not bypassed, (
        f"intake closes runs through the session spine directly: {bypassed}. A run "
        f"that deferred a placement must close through routing_pass.close_run."
    )


# ── Finding 11: the made-up-actor guard was bypassable four ways ─────────────


@pytest.mark.parametrize(
    "source",
    [
        'routing_pass.acknowledge(cfg, t, actor="cli")',
        "acknowledge(cfg, t, actor='cli')",
        'routing_pass.acknowledge(cfg, t, actor=f"cli")',
        'ACTOR = "cli"\nrouting_pass.acknowledge(cfg, t, actor=ACTOR)',
        'routing_pass.acknowledge(cfg, t, actor="cli" if x else "cli")',
        'routing_pass.acknowledge(cfg, t, **{"actor": "cli"})',
        'routing_pass.acknowledge(cfg, t, actor="cl" + "i")',
    ],
)
def test_the_made_up_actor_guard_bites_each_evasion(source):
    """P7's first half. Four documented bypasses, and each one has to fail.

    A guard that only matched a bare literal was satisfied by an f-string, a
    module constant, a conditional between two literals, and a dictionary
    unpacked into the call. All of them record the product acknowledging a track
    to itself, which is exactly what the guard exists to forbid.
    """
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
    """P7's second half, and the half that decides whether the guard survives.

    A guard with false positives gets suppressed, and a suppressed guard protects
    nothing. Every line here is a caller doing exactly the right thing.
    """
    assert _made_up_actors(source) == [], f"the guard fired on correct code: {source}"
