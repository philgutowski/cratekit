"""Spending the capture: the restore, its retention bounds, and its one held session.

The most destructive thing this product does, with no undo for the undo.

**A RESTORE REPLACES EXACTLY THE DERIVED COUPLED SET.** Every target comes from
``config.snapshot_sources`` and ``config.sidecar_paths``, the declaration the
capture reads, so the registry and the database cannot roll back apart. Nothing
NEVER_RESTORED or SURVIVES_ROLLBACK is reachable, asserted because two are locks
this process holds.

**COMPANION FILES ARE ASYMMETRIC, AND DECLARED.** Both live companions are cleared
so the engine cannot replay a stale log, then only those ``Sidecar.restored``
names are written back; no suffix is spelled here.

**ONE SESSION SPANS THE WHOLE VERB.** :func:`recovery_session` enters the gates
once and the off-machine restore takes that guard as ``gates``, because a plan
that releases the lock lets a second process commit before the run.

**A DRY RUN AND A REAL RUN WALK ONE LIST.** :func:`plan` yields :class:`Step`
values and :func:`run` checks each against the disk before acting; a preview on a
second path reports on a different program.

**NOTHING IS DELETED THAT NOTHING ELSE HOLDS A COPY OF.** The live write-ahead log
is moved aside, a replaced directory is removed only after its replacement lands,
and a previous attempt's only copy is adopted.

**A RESTORE THAT DID NOT FINISH SAYS SO.** A latch written before the first
destructive step and retracted by the last makes a killed restore refuse writes.

What left the coupled set (audio, provider renames, the Trash) is enumerated by
``core.reconcile`` BEFORE anything is replaced, since afterwards every comparison
reports nothing. A pre-cutover tree is handed to ``core.convergence``
(:func:`_hand_tree_shortness_over`).

LAYER: write, the tree registry's exception, because it reads that registry; it
imports no ``cratekit.write.*`` module, which ``tests/test_layering.py`` asserts.
"""

from __future__ import annotations

import logging
import os
import shutil
import tempfile
from contextlib import AbstractContextManager, contextmanager, nullcontext
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pathlib import Path
from typing import Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.core import (
    config,
    convergence,
    preflight,
    processes,
    rb_writer,
    reconcile,
    session,
    snapshot,
    tree_registry,
)
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy

logger = logging.getLogger(__name__)

#: The session log's label for a restore of this product's own capture (D2). Not
#: ``RESTORE_WORKFLOW``, which ``modules.tools.backup`` uses for the off-machine
#: restore in the same log field.
CAPTURE_RESTORE_WORKFLOW = "capture-restore"

#: The label for a lost library volume, separate because it passes weaker gates.
BARE_METAL_WORKFLOW = "bare-metal-recovery"

#: The installation-scoped lock a bare-metal recovery takes in place of the library one.
RECOVERY_LOCK_KEY = "recovery_lock"

#: Where live companion files are moved aside. Declared by no inventory entry on
#: purpose, because no capture holds these bytes.
PRE_RESTORE_DIR = ".cratekit-pre-restore"


# ---------------------------------------------------------------------------
# The residual findings this module's prose points at
# ---------------------------------------------------------------------------
#
# Named by title, not number, because a merge renumbers entries and a number in
# source repoints silently; ``tests/test_restore.py`` asserts the titles resolve.

#: The R30 sentence this unit computes and never renders. Owner U27.
RESIDUAL_CAPTURE_VOLUME_UNREPORTED = (
    "R30's second sentence is computed and never reported"
)

#: The bare-metal write path U95 put back by deriving every path from the session.
RESIDUAL_BARE_METAL_HAS_NO_WRITE_PATH = (
    "Closing the bare-metal bypass removed the bare-metal write path"
)


# ---------------------------------------------------------------------------
# What is restorable
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Restorable:
    """One session, its capture, and whether that capture can be spent.

    ``unusable`` is a sentence, and an unusable entry is still listed, because it
    is the session a person goes looking for.
    """

    record: session.SessionRecord
    capture_root: Path | None = None
    capture: snapshot.Capture | None = None
    unusable: str = ""

    @property
    def session_id(self) -> str:
        return self.record.session_id

    @property
    def started(self) -> str:
        return self.record.started

    @property
    def workflow(self) -> str:
        return self.record.workflow

    @property
    def change(self) -> session.ChangeSummary:
        return self.record.change

    @property
    def restorable(self) -> bool:
        return not self.unusable and self.capture is not None and self.capture.verified


def capture_root_of(recorded: str | Path) -> Path:
    """The capture DIRECTORY named by a session record.

    A record may name the directory or the database inside it; both are honoured,
    as ``rb_writer.default_protected_snapshot_paths`` does, so no consumer reads
    one value two ways.
    """
    path = Path(recorded)
    return path if path.is_dir() else path.parent


def list_sessions(cfg: config.Config) -> tuple[Restorable, ...]:
    """Every recorded session, newest first, with its change summary and capture.

    Ordered by recorded start, not modification time, so a backup tool touching a
    capture does not reorder the history.
    """
    listed: list[Restorable] = []
    for record in session.records(cfg):
        if not record.snapshot_path:
            listed.append(
                Restorable(
                    record=record,
                    unusable="this session recorded no capture, so there is nothing to restore",
                )
            )
            continue
        root = capture_root_of(record.snapshot_path)
        try:
            manifest = snapshot.read_manifest(root)
        except CratekitError as exc:
            listed.append(
                Restorable(record=record, capture_root=root, unusable=exc.cause.message)
            )
            continue
        listed.append(Restorable(record=record, capture_root=root, capture=manifest))
    return tuple(sorted(listed, key=lambda entry: entry.started, reverse=True))


# ---------------------------------------------------------------------------
# The one held session
# ---------------------------------------------------------------------------


class Guard(StrEnum):
    """WHICH gate produced a :class:`Held`.

    Both guards declare ``Intent.RECOVERY`` and hold a real lock, so only this
    tells the library gates from the bare-metal substitutes.
    """

    #: All three library gates, against the configured library.
    LIBRARY_SESSION = "library-session"

    #: The substitutes, against a named replacement target (:func:`bare_metal_session`).
    BARE_METAL = "bare-metal-recovery"


#: What each live token was issued FOR: guard, authorised directory, and lock.
#: Compared on use, because a caller could rebuild a ``Held`` around a live token
#: claiming another guard and directory.
_ISSUED: dict[int, tuple[Guard, str, str]] = {}


@dataclass(frozen=True, slots=True)
class Held:
    """An OPEN destructive session, handed to everything the verb then does.

    ``guard`` is the off-machine restore's ``gates`` seam, so both halves run in
    one acquisition; it does nothing, since retaking the gates would report this
    process as a foreign holder.

    ``issued_by`` and ``authorises`` let :func:`plan` and :func:`run` refuse a
    session that does not authorise the path they write, because a bare-metal
    lock once let a restore rewrite the library on a refused volume.
    ``authorises`` is the validated target or the library root, and is also
    where the paths come from (:func:`_rooted`).
    """

    workflow: str
    lock: Path
    intent: session.Intent
    issued_by: Guard
    authorises: Path
    gates: session.Gates | None = None
    record: session.SessionRecord | None = None
    token: object | None = None

    def guard(self) -> AbstractContextManager[Held]:
        return nullcontext(self)

    @property
    def still_open(self) -> bool:
        """Whether the gates this value describes are held BY THIS PROCESS, NOW.

        A ``Held`` outlives its block, so this is asked at use. The token says a
        guard is still inside its block, its recorded terms say this value claims
        what that guard issued, and ``session._HELD`` says the lock is held.
        """
        if self.token is None:
            return False
        terms = _ISSUED.get(id(self.token))
        if terms is None:
            return False
        if terms != (self.issued_by, str(self.authorises), str(self.lock.absolute())):
            return False
        return str(self.lock.absolute()) in session._HELD

    def authorises_path(self, path: Path | str) -> bool:
        """Whether this session authorises writing at ``path``.

        Compared on RESOLVED paths, so a symlink, a relative spelling or an
        unmounted volume's empty mount point cannot pass for the target.
        """
        try:
            where = Path(path).resolve()
            root = self.authorises.resolve()
        except OSError:  # pragma: no cover - resolve does not touch the disk
            return False
        return where == root or root in where.parents


@contextmanager
def recovery_session(
    cfg: config.Config,
    *,
    workflow: str = CAPTURE_RESTORE_WORKFLOW,
    now: datetime | None = None,
    lock: Path | str | None = None,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
    analysis_roots: Iterable[Path | str] = (),
) -> Iterator[Held]:
    """Hold the destructive-session gates and an open record for one whole restore.

    IT DECLARES ITSELF A RECOVERY, which exempts it from the committed-unverified
    and unreconciled-restore latches and from nothing else; volume identity, the
    backup acknowledgment and the lock all apply.

    THE RECORD IS THE GATES' OWN (``keep``), so it closes after the analysis watch
    has judged the restore: ABANDONED on failure, CLOSED on success.
    """
    with session.assert_gates(
        cfg,
        workflow=workflow,
        intent=session.Intent.RECOVERY,
        now=now,
        lock=lock,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
        analysis_roots=analysis_roots,
        keep=session.Keep.RECORD,
    ) as gates:
        with _issued(
            workflow=workflow,
            lock=gates.lock,
            issued_by=Guard.LIBRARY_SESSION,
            authorises=Path(cfg.library.root),
            gates=gates,
            record=gates.record,
        ) as held:
            yield held


@contextmanager
def _issued(
    *,
    workflow: str,
    lock: Path,
    issued_by: Guard,
    authorises: Path,
    gates: session.Gates | None = None,
    record: session.SessionRecord | None = None,
) -> Iterator[Held]:
    """Mint one :class:`Held`, register its token, and withdraw it on the way out.

    One mint site, so none forgets the registration; withdrawn in ``finally`` so a
    raising guard cannot leave the gates reported open.
    """
    token = object()
    held = Held(
        workflow=workflow,
        lock=lock,
        intent=session.Intent.RECOVERY,
        issued_by=issued_by,
        authorises=authorises,
        gates=gates,
        record=record,
        token=token,
    )
    _ISSUED[id(token)] = (issued_by, str(authorises), str(lock.absolute()))
    try:
        yield held
    finally:
        _ISSUED.pop(id(token), None)


# ---------------------------------------------------------------------------
# Where a session's paths come from
# ---------------------------------------------------------------------------


def _rooted(cfg: config.Config, held: Held) -> config.Config:
    """The configuration :func:`plan` and :func:`run` resolve every path from.

    The ``Held``'s authorised directory is where paths are derived from, with no
    ``target=`` parameter that could drift from the session. This is the only
    place that asks which guard issued the session.

    A library session gets ``cfg`` back unchanged, so a mismatched configuration
    is still refused. A bare-metal session gets a copy rooted at its target, and
    a relocated root carries its database, as ``config._apply_env_overrides``
    does. A database never under the configured root refuses here, since it has
    no position on the target.

    Built with ``dataclasses.replace``, not ``config.from_dict``, which would apply
    the environment's relocation override.
    """
    if held.issued_by is not Guard.BARE_METAL:
        return cfg
    target = Path(held.authorises)
    database = _rebased(cfg.library.db_path, Path(cfg.library.root), target)
    if not held.authorises_path(database):
        raise _refuse_target(
            f"this installation keeps its rekordbox database at "
            f"{cfg.library.db_path}, outside the library at {cfg.library.root}, so "
            f"it has no position on {target} to be recovered to and is outside "
            f"the one directory this recovery was accepted for",
            steps=(
                "a bare-metal recovery rebuilds what was ON the library volume; a "
                "database kept elsewhere did not die with that volume and is not "
                "this recovery's to replace",
            ),
            target=str(target),
            database=str(cfg.library.db_path),
            configured_root=str(cfg.library.root),
        )
    return replace(cfg, library=replace(cfg.library, root=target, db_path=database))


def _rebased(path: Path | str, recorded_root: Path, root: Path) -> Path:
    """One recorded path, moved from the root it was recorded under onto ``root``.

    Manifests and records hold absolute paths under the dead root, which a
    bare-metal plan must not read as written.

    Textual, by ``config``'s rule (``normpath``, no ``resolve()``), so a stub of
    the dead root cannot change the answer. Left as it came when the roots are
    equal, when already under ``root`` (idempotent), or when under neither.
    """
    recorded = Path(path)
    if recorded_root == root:
        return recorded
    parts = Path(os.path.normpath(str(recorded))).parts
    here = Path(os.path.normpath(str(root))).parts
    there = Path(os.path.normpath(str(recorded_root))).parts
    if parts[: len(here)] == here or parts[: len(there)] != there:
        return recorded
    return Path(root).joinpath(*parts[len(there) :])


def _rebased_capture(
    captured: snapshot.Capture, recorded_root: Path, root: Path
) -> snapshot.Capture:
    """A manifest as read from disk, with every path it names re-based.

    All four fields or none, or reads and writes would name different volumes.
    """
    if recorded_root == root:
        return captured

    def moved(path: Path | None) -> Path | None:
        return _rebased(path, recorded_root, root) if path is not None else None

    return replace(
        captured,
        root=_rebased(captured.root, recorded_root, root),
        database=moved(captured.database),
        sources=tuple(
            replace(
                entry,
                source=_rebased(entry.source, recorded_root, root),
                captured=moved(entry.captured),
            )
            for entry in captured.sources
        ),
    )


def _assert_plan_is_authorised(
    steps: Iterable[Step], pre_restore_root: Path, cfg: config.Config, held: Held
) -> None:
    """Refuse a plan that writes anywhere the session and the inventory did not name.

    ``cfg`` is the ROOTED configuration. Every step target must be authorised and
    a member of :func:`restorable_targets`, derived again, since the authorised
    directory itself passes authorisation. The staging directory must be an
    attempt directory directly under the one derived store, because the closing
    step prunes its parent.

    Asked in :func:`plan`, so a preview is refused too, and again in
    :func:`_preflight`, because a plan is a value that can reach another session.
    """
    allowed = restorable_targets(cfg)
    for step in steps:
        if step.target is None:
            continue
        assert_gates_are_open(held, writing=step.target)
        if step.target not in allowed:
            raise refuse(
                "internal-error",
                f"the plan would {step.act} at {step.target}, which is not a path "
                f"any restore of {cfg.library.root} may replace",
                remedy=Remedy.REPORT_DEFECT,
                detail={"act": str(step.act), "target": str(step.target)},
            )
    assert_gates_are_open(held, writing=pre_restore_root)
    store = _pre_restore_root(cfg).parent
    if pre_restore_root.parent != store:
        raise refuse(
            "internal-error",
            f"the plan stages live companion files under {pre_restore_root}, which "
            f"is not an attempt directory under {store}; the restore prunes the "
            f"directory above its staging, so that has to be the one store this "
            f"library derives",
            remedy=Remedy.REPORT_DEFECT,
            detail={"staging": str(pre_restore_root), "store": str(store)},
        )


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


class Act(StrEnum):
    """One kind of thing a restore does. The set is closed and the ORDER matters.

    ``RECORD`` first, so the evidence and the latch precede any replacement.
    ``CLEAR`` before ``REPLACE``, or the engine replays a stale log.
    ``MARK_TREES`` after the replacement, because the record it writes is itself
    coupled and would be overwritten. ``RESOLVE`` after the work it claims, and
    ``RELEASE`` last, as the claim that the restore finished.
    """

    RECORD = "record-reconciliation"
    CLEAR = "clear-companion"
    REPLACE = "replace-file"
    REPLACE_TREE = "replace-directory"
    REMOVE = "remove-absent"
    MARK_TREES = "mark-trees-unconverged"
    RESOLVE = "resolve-session"
    RELEASE = "release-restore-latch"


@dataclass(frozen=True, slots=True)
class Step:
    """One action, as data, so a plan can be shown before it is performed."""

    act: Act
    target: Path | None = None
    source: Path | None = None
    detail: str = ""

    def describe(self) -> str:
        where = f" {self.target}" if self.target is not None else ""
        return f"{self.act}{where}: {self.detail}"


@dataclass(frozen=True, slots=True)
class Plan:
    """A whole restore, decided and not yet performed.

    ``latch`` is written before the first destructive step and retracted by the
    last; ``pre_restore_root`` is where live companions are moved (:func:`_perform`).
    """

    session_id: str
    capture_root: Path
    steps: tuple[Step, ...]
    latch: reconcile.Marker
    pre_restore_root: Path
    discarded_sessions: tuple[str, ...] = ()
    discarded_change: session.ChangeSummary = field(default_factory=session.ChangeSummary)
    markers: tuple[reconcile.Marker, ...] = ()
    tree_markers: tuple[reconcile.Marker, ...] = ()
    unconverged: tuple[str, ...] = ()
    unverified_sessions: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RestoreOutcome:
    """What a restore did, or would have done.

    Not ``Outcome``, which ``core.cause`` already exports.
    """

    plan: Plan
    performed: tuple[Step, ...]
    dry_run: bool
    resolved: tuple[str, ...] = ()
    outstanding: tuple[str, ...] = ()
    outstanding_unreadable: str = ""

    @property
    def converged(self) -> bool:
        """Whether nothing is left open; an unreadable record counts as open."""
        return not self.outstanding and not self.outstanding_unreadable


def restorable_targets(cfg: config.Config) -> frozenset[Path]:
    """Every path a restore is allowed to touch, DERIVED, never listed.

    The database and companions, the legacy playlist file, and everything
    ``config.snapshot_sources`` declares. A manifest path outside it is refused,
    not skipped. No lock or session record can be a member, and :func:`plan`
    asserts membership rather than trusting the layout.
    """
    targets = {
        *snapshot.database_paths(cfg),
        *config.snapshot_sources(cfg),
        config.state_path(snapshot.DATABASE_KEY, cfg).parent / rb_writer.MASTER_PLAYLIST_XML,
    }
    return frozenset(targets)


def _captured_by_key(
    cfg: config.Config, captured: snapshot.Capture
) -> dict[str, Path | None]:
    """Where each coupled inventory entry sits INSIDE a capture, or None if absent.

    Entries inside the coupled directory are composed from that directory's
    position in the capture; others are looked up in the manifest. No per-entry
    literal, so a new inventory entry is found automatically.
    """
    coupled_dir = config.library_coupled_dir(cfg)
    by_source = {entry.source: entry.captured for entry in captured.sources}
    resolved: dict[str, Path | None] = {}
    for entry in config.coupled_state_files():
        if entry.medium is config.Medium.KEYCHAIN:
            continue
        live = config.state_path(entry.key, cfg)
        if coupled_dir in live.parents:
            landed = captured.root / coupled_dir.name / live.relative_to(coupled_dir)
            resolved[entry.key] = landed if landed.exists() else None
            continue
        resolved[entry.key] = by_source.get(live)
    return resolved


def _committed(record: session.SessionRecord) -> bool:
    """Whether this session put anything into the library.

    A committed source counts, and so does committed-unverified, whose rows landed.
    """
    return bool(record.committed_sources()) or (
        record.state is session.SessionState.COMMITTED_UNVERIFIED
    )


def plan(
    cfg: config.Config,
    session_id: str,
    *,
    held: Held,
    discarding: Sequence[str] = (),
    process_lister: Callable[[], Sequence[str]] | None = None,
    now: datetime | None = None,
) -> Plan:
    """Decide a restore, or refuse. Nothing here writes.

    ``held`` is required, so the plan and the run share one acquisition.

    ``discarding`` is a list of session identifiers, not a flag: a restore past a
    later committed session must name exactly those sessions, or it is refused.

    Every target resolves from :func:`_rooted`; the caller's ``configured`` root
    is only what recorded paths are re-based from.
    :func:`_assert_plan_is_authorised` checks every location the plan writes.

    Rekordbox is asserted closed, because planning reads live coupled state.
    """
    configured = cfg
    cfg = _rooted(configured, held)
    assert_gates_are_open(held, writing=cfg.library.root)
    _assert_rekordbox_closed(process_lister)
    record = session.read_record(session_id, cfg)
    if not record.snapshot_path:
        raise refuse(
            "internal-error",
            f"session {session_id} recorded no capture, so there is nothing to "
            f"restore it from",
            remedy=Remedy.REPORT_DEFECT,
            detail={"session_id": session_id},
        )
    recorded_root, rooted_at = Path(configured.library.root), Path(cfg.library.root)
    root = capture_root_of(_rebased(record.snapshot_path, recorded_root, rooted_at))
    captured = _rebased_capture(snapshot.read_manifest(root), recorded_root, rooted_at)
    # An unverified capture is no recovery point. Both the verdict and the bytes'
    # presence are asked, since a file can vanish after the verdict.
    snapshot.assert_verified(captured)
    snapshot.assert_sources_present(captured)

    later = _later_committed(cfg, record)
    _assert_override_names_them(record, later, discarding)

    allowed = restorable_targets(cfg)
    steps: list[Step] = []

    by_key = _captured_by_key(cfg, captured)
    effects = reconcile.effect_markers(
        cfg,
        captured=by_key,
        session_id=session_id,
        capture_stamp=captured.stamp,
        now=now,
    )
    unconverged = _trees_the_capture_predates(cfg, captured, by_key)
    trees = reconcile.tree_markers(
        unconverged, session_id=session_id, capture_stamp=captured.stamp, now=now
    )
    latch = reconcile.in_flight_marker(capture_stamp=captured.stamp, now=now)

    # ALWAYS, never `if markers:`, or a restore with no markers writes no latch
    # before replacing files and a kill leaves the library writable.
    steps.append(
        Step(
            act=Act.RECORD,
            detail=(
                "latch this restore as in flight and record "
                + (
                    "nothing else, because its window touched nothing that leaves "
                    "the coupled set"
                    if not effects
                    else f"{len(effects)} "
                    + ("thing" if len(effects) == 1 else "things")
                    + " it cannot undo"
                )
                + ", before the evidence for any of it is replaced"
            ),
        )
    )

    steps.extend(_file_steps(cfg, captured, allowed))

    if unconverged:
        steps.append(
            Step(
                act=Act.MARK_TREES,
                detail=(
                    "record that "
                    + ", ".join(unconverged)
                    + (" needs" if len(unconverged) == 1 else " need")
                    + " a full rebuild, AFTER the replacement, because the record "
                    "that holds it is itself part of the coupled set"
                ),
            )
        )

    unverified = tuple(
        entry.session_id
        for entry in session.records(cfg)
        if entry.state is session.SessionState.COMMITTED_UNVERIFIED
    )
    if unverified:
        # One step for all, since the action is a single sweep.
        steps.append(
            Step(
                act=Act.RESOLVE,
                detail=(
                    "resolve "
                    + ", ".join(unverified)
                    + ", whose condemning records live in the log and therefore "
                    "outlive the restore that answers them"
                ),
            )
        )

    steps.append(
        Step(
            act=Act.RELEASE,
            detail=(
                "retract every in-flight restore latch, which is the only claim in "
                "this plan that a restore finished, and is therefore last"
            ),
        )
    )

    pre_restore_root = _pre_restore_root(cfg, now=now)
    _assert_plan_is_authorised(steps, pre_restore_root, cfg, held)

    return Plan(
        session_id=session_id,
        capture_root=root,
        steps=tuple(steps),
        latch=latch,
        pre_restore_root=pre_restore_root,
        discarded_sessions=tuple(entry.session_id for entry in later),
        discarded_change=_merged_change(later),
        # EFFECTS ONLY. Tree markers go to ``core.convergence`` on
        # ``tree_markers``, so one fact lives in one store (R-21 item 3).
        markers=tuple(effects),
        tree_markers=trees,
        unconverged=unconverged,
        unverified_sessions=unverified,
    )


def _pre_restore_root(cfg: config.Config, *, now: datetime | None = None) -> Path:
    """Where a restore puts the live companion files it takes out of the way.

    Beside the database, so the move is a rename, under a dotted directory no
    inventory entry declares. One directory per ATTEMPT, not per latch, so a
    second attempt's log never overwrites the first's.
    """
    return (
        config.state_path(snapshot.DATABASE_KEY, cfg).parent
        / PRE_RESTORE_DIR
        / snapshot.new_stamp(now)
    )


def _later_committed(
    cfg: config.Config, target: session.SessionRecord
) -> tuple[session.SessionRecord, ...]:
    """Every session that committed after the one being restored to, by recorded start."""
    return tuple(
        sorted(
            (
                entry
                for entry in session.records(cfg)
                if entry.session_id != target.session_id
                and entry.started > target.started
                and _committed(entry)
            ),
            key=lambda entry: entry.started,
        )
    )


def _merged_change(records: Sequence[session.SessionRecord]) -> session.ChangeSummary:
    """Everything the given sessions did, PER TREE, so a person can judge it."""
    total = session.ChangeSummary()
    for record in records:
        total = total.merged(record.change)
    return total


def _assert_override_names_them(
    target: session.SessionRecord,
    later: Sequence[session.SessionRecord],
    discarding: Sequence[str],
) -> None:
    """Refuse unless the caller named exactly the sessions they are discarding."""
    if not later:
        return
    expected = {entry.session_id for entry in later}
    named = set(discarding)
    if named == expected:
        return
    summary = _merged_change(later)
    raise refuse(
        "restore-discards-committed-work",
        f"restoring session {target.session_id} reaches back past "
        + (
            f"{len(later)} later session that committed"
            if len(later) == 1
            else f"{len(later)} later sessions that committed"
        )
        + ", and everything they wrote goes with it:\n"
        + "\n".join(
            f"  - {entry.tree}: {entry.created} created, {entry.updated} updated"
            + (f", {entry.removed} removed" if entry.removed else "")
            for entry in summary.trees
        )
        + ("\n  - no tree-level changes were recorded" if not summary.trees else "")
        + "\nName every one of those sessions to proceed; naming none, or naming a "
        "different set, is refused rather than interpreted",
        remedy=Remedy.ANSWER_DECISION,
        scope=Scope.RUN,
        origin=("restore",),
        detail={
            "session_id": target.session_id,
            "discards": sorted(expected),
            "named": sorted(named),
            "change": summary.to_json(),
        },
    )


def _trees_the_capture_predates(
    cfg: config.Config, captured: snapshot.Capture, by_key: Mapping[str, Path | None]
) -> tuple[str, ...]:
    """Trees the database owns now and did not own when this capture was taken.

    Read from the captured registry, not cutover dates, which are off by a day in
    both directions and would fire on correct restores (P7). An absent or
    unreadable captured registry marks every native tree, the conservative way.
    ``by_key`` comes from :func:`_captured_by_key`, so the registry is looked for
    where the capture put it.
    """
    try:
        live = tree_registry.read(cfg)
    except tree_registry.TreeRegistryUnreadable:
        # Nothing can be said, so nothing is marked; the registry refuses at the
        # next governed verb.
        logger.warning("the tree registry could not be read, so no tree was marked")
        return ()
    native = {entry.tree_id for entry in live.trees if entry.mode is tree_registry.Mode.DATABASE}
    if not native:
        return ()
    inside = by_key.get(tree_registry.STATE_KEY)
    if inside is None or not inside.exists():
        return tuple(sorted(native))
    try:
        was = tree_registry.read_path(inside)
    except tree_registry.TreeRegistryUnreadable:
        return tuple(sorted(native))
    already = {
        entry.tree_id for entry in was.trees if entry.mode is tree_registry.Mode.DATABASE
    }
    return tuple(sorted(native - already))


def _file_steps(
    cfg: config.Config, captured: snapshot.Capture, allowed: frozenset[Path]
) -> tuple[Step, ...]:
    """The replacement half of the plan, in the order that makes it safe.

    COMPANIONS ARE CLEARED BEFORE ANY COPY, so no stale log ever sits beside a
    changing database; which come back is ``config.sidecar_paths`` asked with
    ``restored_only``.

    ABSENCE IN THE CAPTURE IS AN INSTRUCTION: a source recorded absent is removed.
    """
    database = config.state_path(snapshot.DATABASE_KEY, cfg)
    steps: list[Step] = [
        Step(
            act=Act.CLEAR,
            target=companion,
            detail=(
                "clear the live companion file before anything is copied, so the "
                "engine cannot replay a log belonging to the database that is "
                "about to be replaced"
            ),
        )
        for companion in config.sidecar_paths(snapshot.DATABASE_KEY, cfg)
    ]
    all_companions = set(config.sidecar_paths(snapshot.DATABASE_KEY, cfg))
    restored_companions = set(
        config.sidecar_paths(snapshot.DATABASE_KEY, cfg, restored_only=True)
    )

    for entry in captured.sources:
        if entry.source not in allowed:
            raise refuse(
                "internal-error",
                f"the capture manifest names {entry.source}, which is not a path "
                f"any restore may replace; refusing rather than restoring the "
                f"subset this build happens to recognise",
                remedy=Remedy.REPORT_DEFECT,
                detail={"source": str(entry.source), "capture": str(captured.root)},
            )
        if entry.source in restored_companions:
            if entry.captured is not None:
                steps.append(
                    Step(
                        act=Act.REPLACE,
                        target=entry.source,
                        source=entry.captured,
                        detail="write back the companion the inventory declares restored",
                    )
                )
            continue
        if entry.source in all_companions:
            # Never written back, since a stale index beside a fresh log gives the
            # engine two views; cleared above and stays cleared.
            continue
        if entry.captured is None:
            steps.append(
                Step(
                    act=Act.REMOVE,
                    target=entry.source,
                    detail=(
                        "the capture records this as absent, so returning to the "
                        "pre-session state means removing it"
                    ),
                )
            )
            continue
        steps.append(
            Step(
                act=Act.REPLACE_TREE if entry.directory else Act.REPLACE,
                target=entry.source,
                source=entry.captured,
                detail=(
                    "restore the database"
                    if entry.source == database
                    else "restore the coupled state captured with the database"
                ),
            )
        )
    return tuple(steps)


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------


def run(
    decided: Plan,
    cfg: config.Config,
    *,
    held: Held,
    dry_run: bool = False,
    process_lister: Callable[[], Sequence[str]] | None = None,
    now: datetime | None = None,
) -> RestoreOutcome:
    """Perform a plan, or walk it without performing it. ONE list, one order.

    The modes differ only inside the loop, so the preview is evidence about the
    write. A DRY RUN PERFORMS NOTHING, the clearing included.

    Rekordbox is re-asserted closed, even for a rehearsal. The whole plan is
    checked (:func:`_preflight`) before any step runs, so a passing rehearsal
    means the real run reaches its work. Every path comes from :func:`_rooted`.
    """
    configured = cfg
    cfg = _rooted(configured, held)
    assert_gates_are_open(held, writing=cfg.library.root)
    _assert_rekordbox_closed(process_lister)
    _preflight(decided, cfg, held=held, recorded_root=Path(configured.library.root))
    performed: list[Step] = []
    resolved: list[str] = []
    for step in decided.steps:
        performed.append(step)
        if dry_run:
            continue
        resolved.extend(_perform(step, decided, cfg, now=now))
    # Read on both paths, since outstanding is a fact about the library. Read
    # defensively, because raising after the work would close a finished
    # restore ABANDONED.
    unreadable = ""
    try:
        outstanding = tuple(
            record.marker.marker_id for record in reconcile.outstanding(cfg)
        )
    except CratekitError as exc:
        outstanding = ()
        unreadable = exc.cause.message
        logger.warning(
            "the restore landed and the reconciliation record could not then be "
            "read, so what is outstanding is unknown: %s",
            unreadable,
        )
    return RestoreOutcome(
        plan=decided,
        performed=tuple(performed),
        dry_run=dry_run,
        resolved=tuple(resolved),
        outstanding=outstanding,
        outstanding_unreadable=unreadable,
    )


def _preflight(
    decided: Plan, cfg: config.Config, *, held: Held, recorded_root: Path
) -> None:
    """Evaluate every predicate the plan's steps depend on. Writes nothing.

    * the session authorises every write location, staging included;
    * the capture is still whole;
    * every replacement source exists and is the expected kind;
    * every destination is writable;
    * every companion's staging name is free, asked here because
      :func:`_stage_companion_aside` runs per companion and a late refusal would
      leave the log moved and the database unreplaced;
    * the library volume has room for the whole copy.

    ``cfg`` is ROOTED; ``recorded_root`` is what the manifest is re-based from.
    What the restore discards is derived again, since a session can commit
    between plan and run.
    """
    _assert_plan_is_authorised(decided.steps, decided.pre_restore_root, cfg, held)

    record = session.read_record(decided.session_id, cfg)
    later = _later_committed(cfg, record)
    _assert_override_names_them(record, later, decided.discarded_sessions)

    captured = _rebased_capture(
        snapshot.read_manifest(decided.capture_root),
        recorded_root,
        Path(cfg.library.root),
    )
    snapshot.assert_verified(captured)
    snapshot.assert_sources_present(captured)

    for step in decided.steps:
        if step.act in (Act.REPLACE, Act.REPLACE_TREE):
            _assert_source_usable(step)
        if step.act is Act.CLEAR and step.target is not None:
            _assert_staging_is_free(step.target, decided.pre_restore_root)
        if step.target is not None:
            _assert_writable(step)

    snapshot.assert_room_for(
        space_peak_bytes(decided),
        config.state_path(snapshot.DATABASE_KEY, cfg).parent,
        what="the high-water mark of putting this capture back",
        steps=(
            "free space on the LIBRARY volume, which is the one being written to "
            "here; pruning captures helps only if the capture store is on it, and "
            "the retention plan reports whether it is",
        ),
    )


def space_peak_bytes(decided: Plan) -> int:
    """The most this plan will ever occupy beyond what the library holds now.

    Not the largest single step. A ``CLEAR`` is a rename, so the staged log stays
    and the companion written back frees nothing, and a target missing live frees
    nothing; both raise the floor for every later step. So the peak is the running
    total plus the step in flight, over the plan in its order.
    """
    staged_aside = {
        step.target for step in decided.steps if step.act is Act.CLEAR
    }
    occupied = 0
    peak = 0
    for step in decided.steps:
        if step.target is None:
            continue
        if step.act is Act.REMOVE:
            occupied -= snapshot.freed_bytes(step.target)
            continue
        if step.act not in (Act.REPLACE, Act.REPLACE_TREE) or step.source is None:
            continue
        incoming = snapshot.incoming_bytes(step.source)
        # A target that was staged aside is still on the volume under another
        # name, so replacing it gives nothing back.
        outgoing = (
            0 if step.target in staged_aside else snapshot.freed_bytes(step.target)
        )
        # Both copies exist at once, which is what makes the swap atomic.
        peak = max(peak, occupied + incoming)
        occupied += incoming - outgoing
    return max(peak, occupied)


def _assert_source_usable(step: Step) -> None:
    """Refuse a replacement whose source is gone or is the wrong kind of thing."""
    source = step.source
    if source is None:  # pragma: no cover - a replacement always has a source
        raise refuse(
            "internal-error",
            f"the step {step.act} on {step.target} carries no source",
            remedy=Remedy.REPORT_DEFECT,
            detail={"act": str(step.act), "target": str(step.target)},
        )
    wanted_directory = step.act is Act.REPLACE_TREE
    if source.is_dir() if wanted_directory else source.is_file():
        return
    raise refuse(
        "snapshot-integrity-failed",
        f"the restore would put {source} at {step.target} and that source is "
        + ("not a directory" if wanted_directory else "not a file that exists")
        + "; refusing before anything is replaced rather than part way through",
        remedy=Remedy.REPORT_DEFECT,
        scope=Scope.RUN,
        origin=("restore",),
        detail={"act": str(step.act), "source": str(source), "target": str(step.target)},
    )


def _assert_writable(step: Step) -> None:
    """Refuse when this account cannot write where the step has to write.

    A directory replacement needs BOTH its parent, where
    :func:`_replace_directory` stages, and itself, for the first rename. The
    target probe is needed on darwin and stricter than Linux needs, asked
    everywhere so a rehearsal means the same thing on every platform. Each is
    asked of the nearest EXISTING ancestor, since a restore creates directories.
    """
    target = step.target
    assert target is not None
    wanted = [target.parent] if step.act is Act.REPLACE_TREE else []
    wanted.append(target)
    for candidate in wanted:
        _assert_directory_writable(step, candidate)


def _assert_directory_writable(step: Step, wanted: Path) -> None:
    probe = wanted
    while not probe.exists() and probe.parent != probe:
        probe = probe.parent
    writable = probe if probe.is_dir() else probe.parent
    if os.access(writable, os.W_OK):
        return
    raise refuse(
        "restore-step-failed",
        f"{writable} is not writable by this account, so the restore would stop "
        f"at {step.target} after having already replaced everything before it",
        steps=(
            "make the library's directories writable by this account, then run "
            "this again",
        ),
        scope=Scope.RUN,
        origin=("restore",),
        detail={
            "act": str(step.act),
            "target": str(step.target),
            "unwritable": str(writable),
        },
    )


def assert_gates_are_open(held: Held, *, writing: Path | str | None = None) -> None:
    """Refuse unless the gates are held by this process AT THIS MOMENT, for THIS path.

    A ``Held`` can outlive its block, so this is asked at each use. The intent must
    be a recovery, since the latches would refuse an ordinary write. The written
    path must be authorised, because the other checks cannot tell a library
    session from a bare-metal one.
    """
    if held.intent is not session.Intent.RECOVERY:
        raise refuse(
            "internal-error",
            f"a restore was handed a {held.intent} session; a restore declares "
            f"itself a recovery, because the latches it answers would otherwise "
            f"refuse it",
            remedy=Remedy.REPORT_DEFECT,
            detail={"workflow": held.workflow, "intent": str(held.intent)},
        )
    if not held.still_open:
        raise refuse(
            "internal-error",
            f"the destructive-session gates for {held.workflow} are not held by "
            f"this process, so this call would plan or write with the library lock "
            f"released and every other process free to commit underneath it; a "
            f"session value that was never issued by one of this module's own "
            f"guards reports the same thing, and for the same reason",
            remedy=Remedy.REPORT_DEFECT,
            detail={"workflow": held.workflow, "lock": str(held.lock)},
        )
    if writing is None or held.authorises_path(writing):
        return
    raise refuse(
        "internal-error",
        f"the {held.issued_by} session open here authorises {held.authorises} and "
        f"this call would write at {writing}; the gates a session passed are gates "
        f"about a particular library, so spending one against a different one "
        f"would replace a database behind checks that were never asked of it",
        remedy=Remedy.REPORT_DEFECT,
        detail={
            "workflow": held.workflow,
            "issued_by": str(held.issued_by),
            "authorises": str(held.authorises),
            "writing": str(writing),
        },
    )


def _assert_rekordbox_closed(process_lister: processes.ProcessLister | None = None) -> None:
    """Refuse while the application or its background agent holds the database.

    Through ``core.processes``, which returns a tuple, not the guarded writer's
    same-named probe, which returns a joined string.
    """
    running = processes.rekordbox_processes_running(lister=process_lister)
    if not running:
        return
    raise refuse(
        "rekordbox-running",
        f"{', '.join(running)} is running, and restoring underneath a live "
        f"rekordbox replaces the file it holds open, which leaves the application "
        f"and the disk describing two different libraries",
        remedy=Remedy.QUIT_REKORDBOX,
        scope=Scope.SESSION,
        origin=("restore",),
        detail={"running": list(running)},
    )


def _perform(
    step: Step, decided: Plan, cfg: config.Config, *, now: datetime | None = None
) -> tuple[str, ...]:
    """Do one step. Returns the session identifiers it resolved, usually none.

    The parameter is ``decided``, not ``plan``, so it never shadows :func:`plan`.
    """
    if step.act is Act.RECORD:
        # The latch FIRST, in the same call as the effect markers. Tree markers
        # are not here; MARK_TREES hands them to ``core.convergence``.
        reconcile.record_markers(cfg, (decided.latch, *decided.markers))
        return ()
    if step.act is Act.MARK_TREES:
        _hand_tree_shortness_over(cfg, decided, now=now)
        return ()
    if step.act is Act.RESOLVE:
        return _resolve_unverified(decided, cfg, now=now)
    if step.act is Act.RELEASE:
        # EVERY latch, not this plan's own, so a restore after an interrupted one
        # discharges both (reconcile.retract_in_flight).
        discharged = reconcile.retract_in_flight(cfg)
        if len(discharged) > 1:
            logger.info(
                "this restore discharged %d in-flight latches, including %d left "
                "by earlier attempts",
                len(discharged),
                len(discharged) - 1,
            )
        _prune_staged_companions(decided.pre_restore_root.parent)
        return ()
    if step.target is None:  # pragma: no cover - every other act carries a target
        raise refuse(
            "internal-error",
            f"the step {step.act} carries no target",
            remedy=Remedy.REPORT_DEFECT,
            detail={"act": str(step.act)},
        )
    try:
        if step.act is Act.CLEAR:
            _stage_companion_aside(step.target, decided.pre_restore_root)
            return ()
        if step.act is Act.REMOVE:
            _remove(step.target)
            return ()
        if step.source is None:  # pragma: no cover - a replacement always has a source
            raise refuse(
                "internal-error",
                f"the step {step.act} on {step.target} carries no source",
                remedy=Remedy.REPORT_DEFECT,
                detail={"act": str(step.act), "target": str(step.target)},
            )
        if step.act is Act.REPLACE_TREE:
            _replace_directory(step.source, step.target)
        else:
            _replace_file(step.source, step.target)
    except OSError as exc:
        # A raw OSError carries no reason or remedy. The latch stays standing.
        raise refuse(
            "restore-step-failed",
            f"the restore could not {step.act} at {step.target}: {exc}. The "
            f"in-flight latch stays recorded, so this library refuses ordinary "
            f"writes until a restore completes",
            steps=(
                "read the error above, put right what it names, and run the "
                "restore again; it is safe to repeat",
                f"the live storage-engine companion files this restore moved out "
                f"of the way are under {decided.pre_restore_root}",
            ),
            scope=Scope.RUN,
            origin=("restore",),
            detail={
                "act": str(step.act),
                "target": str(step.target),
                "source": str(step.source) if step.source is not None else None,
                "staged": str(decided.pre_restore_root),
            },
        ) from exc
    return ()


def _prune_staged_companions(store: Path) -> None:
    """Bound the staged-companion store, oldest first, AFTER a restore completed.

    Each attempt stages a fresh copy that its restore never deletes, so the store
    grows without this. Pruned only on success, since a failed attempt's log is
    the one most wanted.

    IT NEVER RAISES. It runs from RELEASE, outside :func:`_perform`'s ``try`` and
    after the latch is discharged, so an escaping error would close a finished
    restore ABANDONED.
    """
    # By modification time, since a stamp's random tail makes names unordered
    # within one second.
    try:
        attempts = sorted(
            (entry for entry in store.iterdir() if entry.is_dir()),
            key=lambda entry: (entry.stat().st_mtime, entry.name),
        )
    except OSError:
        return
    for stale in attempts[: max(len(attempts) - KEEP_STAGED_ATTEMPTS, 0)]:
        try:
            shutil.rmtree(stale)
            logger.info("pruned the staged companion files from %s", stale.name)
        except OSError as exc:
            logger.warning("could not prune the staged companions at %s: %s", stale, exc)


def _stage_companion_aside(target: Path, staging: Path) -> None:
    """Move a live companion out of the way instead of deleting it.

    A write-ahead log holds transactions in no capture, so unlinking it before a
    failing copy loses them for good. A rename costs nothing and still takes the
    log off the name the engine reads. The restore that staged it never deletes it.

    A collision is refused rather than overwritten (:func:`_assert_staging_is_free`),
    per file since one attempt stages several companions. :func:`_preflight` asks
    first; this is the backstop for the window between.

    The early return asks ``lexists``, since the engine follows a dangling symlink.
    """
    if not os.path.lexists(target):
        return
    _assert_staging_is_free(target, staging)
    config.mkdir_private(staging)
    os.replace(target, staging / target.name)


def _assert_staging_is_free(target: Path, staging: Path) -> None:
    """Refuse when an earlier attempt's companion already rests under this name.

    Asked with ``lexists`` on both sides, since a dangling link is a taken name.
    The refusal names what the staging directory already holds, so a person can
    find a log this run has already moved.
    """
    if not os.path.lexists(target):
        return
    resting = staging / target.name
    if not os.path.lexists(resting):
        return
    occupied = _staged_names(staging)
    raise refuse(
        "restore-staging-occupied",
        f"the staging directory {staging} already holds "
        f"{', '.join(occupied) or resting.name}, and this restore would move the "
        f"live {target} onto {resting}. Those bytes are in no capture, so "
        f"overwriting them destroys the only copy of them that exists anywhere",
        steps=(
            "run the restore again; it is safe to repeat, and a fresh attempt "
            "takes a staging directory of its own that nothing occupies",
            f"the live storage-engine companion files already moved out of the "
            f"way are under {staging}",
        ),
        scope=Scope.RUN,
        origin=("restore",),
        retryable=True,
        detail={
            "target": str(target),
            "staged": str(resting),
            "staging_root": str(staging),
            "already_staged": list(occupied),
        },
    )


def _staged_names(staging: Path) -> tuple[str, ...]:
    """What the staging directory holds right now, or nothing if it cannot be read.

    Never raises, so it cannot replace the refusal it describes.
    """
    try:
        return tuple(sorted(entry.name for entry in staging.iterdir()))
    except OSError:
        return ()


#: Why a tree this restore left short is short, in ``core.convergence``'s vocabulary.
PRE_CUTOVER_RESTORE = "restore-predates-cutover"


def _hand_tree_shortness_over(
    cfg: config.Config, decided: Plan, *, now: datetime | None = None
) -> None:
    """Record that these trees need a rebuild, in the record that GATES that fact.

    ``core.convergence`` OWNS TREE SHORTNESS (U36). Its fingerprint travels with
    the database in a capture, so it cannot see a pre-cutover restore; only this
    module holds both registries. So this module decides which trees, and that
    module holds and gates the answer, per tree, exempting ``Purpose.REBUILD``
    and cleared only by a rebuild. One fact in one store, so a rebuild cannot
    clear one flag and leave another (R-21 item 3).
    """
    if not decided.tree_markers:
        return
    tree_ids = tuple(sorted({marker.identity for marker in decided.tree_markers}))
    convergence.mark_unconverged(cfg, tree_ids, reason=PRE_CUTOVER_RESTORE, now=now)
    logger.info(
        "handed %d unconverged tree(s) to the convergence record, which is "
        "what a rebuild clears",
        len(tree_ids),
    )


def _resolve_unverified(
    decided: Plan, cfg: config.Config, *, now: datetime | None = None
) -> tuple[str, ...]:
    """Answer every condemning record this restore has now made false.

    A step, because the session log SURVIVES_ROLLBACK and a committed-unverified
    record would otherwise outlive the restore that answers it. Every such record
    is resolved, since the library now holds a verified capture.
    """
    answered: list[str] = []
    for session_id in decided.unverified_sessions:
        try:
            session.resolve_unverified_session(session_id, cfg, now=now)
        except CratekitError as exc:
            # Already resolved or moved on; not fatal once the restore has landed.
            logger.info("session %s was not resolved: %s", session_id, exc)
            continue
        answered.append(session_id)
    return tuple(answered)


def _remove(target: Path) -> None:
    if target.is_dir() and not target.is_symlink():
        shutil.rmtree(target)
        return
    target.unlink(missing_ok=True)


def _replace_file(source: Path, target: Path) -> None:
    """Copy into place through a temporary name in the TARGET's directory.

    Beside the target so the rename is atomic on one filesystem and an
    interruption never leaves a half-written database.
    """
    config.mkdir_private(target.parent)
    descriptor, temporary = tempfile.mkstemp(dir=str(target.parent), suffix=".tmp")
    os.close(descriptor)
    staged = Path(temporary)
    try:
        shutil.copyfile(source, staged)
        shutil.copystat(source, staged)
        os.replace(staged, target)
    except BaseException:
        staged.unlink(missing_ok=True)
        raise


def _replace_directory(source: Path, target: Path) -> None:
    """Swap a whole directory in, rather than emptying the live one first.

    Staging beside the target and renaming leaves the old directory findable if a
    crash falls between the two renames.

    ``.replaced`` IS ADOPTED, NOT DELETED, when it is the only copy left, and is
    removed only after the new directory lands, since a second attempt once
    deleted the only pre-restore state. A partial ``.restoring`` is removed up front.
    """
    config.mkdir_private(target.parent)
    staged = target.with_name(f"{target.name}.restoring")
    previous = target.with_name(f"{target.name}.replaced")
    if previous.exists() and not target.exists():
        logger.warning(
            "%s is missing and %s holds the only copy of the state a previous "
            "restore took out of the way; adopting it back rather than deleting it",
            target,
            previous,
        )
        os.replace(previous, target)
    _remove(staged)
    try:
        shutil.copytree(source, staged)
    except BaseException:
        _remove(staged)
        raise
    if target.exists():
        _remove(previous)
        os.replace(target, previous)
    os.replace(staged, target)
    # THE SWAP HAS LANDED, SO NOTHING AFTER THIS MAY FAIL THE RESTORE, or a correct
    # restore never retracts its latch. A leftover directory is only logged.
    try:
        _remove(previous)
    except OSError as exc:
        logger.warning(
            "the restore of %s landed and the previous copy at %s could not be "
            "removed (%s); it is left in place and can be deleted by hand",
            target,
            previous,
            exc,
        )


# ---------------------------------------------------------------------------
# Retention (R30)
# ---------------------------------------------------------------------------

#: How many captures survive on count alone, the guarded writer's default.
DEFAULT_KEEP = 5

#: How old a capture may be before count stops protecting it.
DEFAULT_MAX_AGE = timedelta(days=30)

#: How many attempts' worth of staged companion files survive. Shares only the
#: default with :data:`DEFAULT_KEEP`: the prune runs at RELEASE with no policy in
#: scope, so a retention argument must not decide how much log a restore discards.
#: ``tests/test_restore.py`` pins both with literal values.
KEEP_STAGED_ATTEMPTS = DEFAULT_KEEP


@dataclass(frozen=True, slots=True)
class RetentionPolicy:
    """Three bounds, and a capture survives only if it clears all of them.

    Count, age and bytes each catch what the others miss. ``max_bytes`` defaults
    to None because the right number depends on the volume.
    """

    keep: int = DEFAULT_KEEP
    max_age: timedelta | None = DEFAULT_MAX_AGE
    max_bytes: int | None = None


@dataclass(frozen=True, slots=True)
class StoredCapture:
    """One capture directory on disk, with what retention needs to judge it.

    Not ``Capture``, which ``snapshot.Capture`` already names.
    """

    root: Path
    modified: float
    size: int
    protected: bool


@dataclass(frozen=True, slots=True)
class RetentionPlan:
    """What retention would delete, what it would keep, and why."""

    root: Path
    policy: RetentionPolicy
    keeping: tuple[StoredCapture, ...] = ()
    deleting: tuple[StoredCapture, ...] = ()
    total_bytes: int = 0
    shares_the_database_volume: bool = False

    @property
    def reclaimed_bytes(self) -> int:
        return sum(entry.size for entry in self.deleting)


def _directory_size(root: Path) -> int:
    total = 0
    for current, _directories, files in os.walk(root):
        here = Path(current)
        for name in files:
            try:
                total += (here / name).stat().st_size
            except OSError:
                continue
    return total


def shares_the_database_volume(cfg: config.Config, *, root: Path | None = None) -> bool:
    """Whether the capture store sits on the same filesystem as the database.

    R30 asks that it does not; the default layout answers True. Reported rather
    than refused, since refusing would break the recommended layout. Compared on
    the filesystem identifier, since bind mounts and symlinks fool prefixes.
    Computed but rendered nowhere yet, recorded under
    :data:`RESIDUAL_CAPTURE_VOLUME_UNREPORTED`.
    """
    store = root if root is not None else snapshot.store_root(cfg)
    database = config.state_path(snapshot.DATABASE_KEY, cfg)
    left = preflight.device_of(store)
    right = preflight.device_of(database)
    return left is not None and left == right


def retention_plan(
    cfg: config.Config,
    *,
    policy: RetentionPolicy | None = None,
    root: Path | str | None = None,
    protected_provider: Callable[[], set[Path]] | None = None,
    now: datetime | None = None,
) -> RetentionPlan:
    """Decide what retention would delete. Reads only.

    A capture an OPEN session references is spared whatever else holds (R30),
    using the guarded writer's own provider. A provider that raises deletes
    nothing, since a kept capture costs only disk.
    """
    rules = policy or RetentionPolicy()
    store = Path(root) if root is not None else snapshot.store_root(cfg)
    moment = now or datetime.now(timezone.utc)
    plan_shares = shares_the_database_volume(cfg, root=store)
    if not store.is_dir():
        return RetentionPlan(
            root=store, policy=rules, shares_the_database_volume=plan_shares
        )

    provider = protected_provider
    if provider is None:
        provider = lambda: rb_writer.default_protected_snapshot_paths(cfg)  # noqa: E731
    try:
        spared = provider()
    except Exception as exc:  # noqa: BLE001 - see the docstring
        logger.warning(
            "the protected-capture provider failed, so every capture is kept: %s", exc
        )
        spared = None

    found: list[StoredCapture] = []
    for directory in sorted(store.iterdir()):
        if not directory.is_dir():
            continue
        database = rb_writer.snapshot_database_in(directory)
        if database is None:
            continue
        try:
            modified = directory.stat().st_mtime
        except OSError:
            continue
        found.append(
            StoredCapture(
                root=directory,
                modified=modified,
                size=_directory_size(directory),
                protected=spared is None
                or _is_protected(directory, database, spared),
            )
        )
    found.sort(key=lambda entry: entry.modified, reverse=True)

    keeping: list[StoredCapture] = []
    candidates: list[StoredCapture] = []
    for position, entry in enumerate(found):
        if entry.protected or position < max(rules.keep, 0):
            keeping.append(entry)
        else:
            candidates.append(entry)

    deleting: list[StoredCapture] = []
    if rules.max_age is not None:
        cutoff = (moment - rules.max_age).timestamp()
        for entry in list(candidates):
            if entry.modified < cutoff:
                candidates.remove(entry)
                deleting.append(entry)
    if rules.max_bytes is not None:
        # Oldest first, the least useful capture going first.
        for entry in sorted(candidates, key=lambda e: e.modified):
            held = sum(e.size for e in keeping) + sum(e.size for e in candidates)
            if held <= rules.max_bytes:
                break
            candidates.remove(entry)
            deleting.append(entry)
    keeping.extend(candidates)
    keeping.sort(key=lambda entry: entry.modified, reverse=True)
    deleting.sort(key=lambda entry: entry.modified, reverse=True)
    return RetentionPlan(
        root=store,
        policy=rules,
        keeping=tuple(keeping),
        deleting=tuple(deleting),
        total_bytes=sum(entry.size for entry in found),
        shares_the_database_volume=plan_shares,
    )


def _is_protected(directory: Path, database: Path, spared: set[Path]) -> bool:
    """Whether either spelling of this capture appears in the protected set."""
    for candidate in (directory, database):
        try:
            if candidate.resolve() in spared:
                return True
        except (OSError, ValueError):
            continue
    return False


def prune(
    cfg: config.Config,
    *,
    policy: RetentionPolicy | None = None,
    owning: session.SessionRecord | None = None,
    root: Path | str | None = None,
    protected_provider: Callable[[], set[Path]] | None = None,
    now: datetime | None = None,
) -> tuple[Path, ...]:
    """Delete what :func:`retention_plan` decided, and refuse before a commit.

    A non-terminal ``owning`` session refuses, so pruning never precedes the commit
    its snapshot protects. ``owning=None`` widens the check to every session in
    the log. What is deleted is exactly the plan a caller could have been shown.
    """
    if owning is not None and not owning.terminal:
        raise refuse(
            "internal-error",
            f"session {owning.session_id} is {str(owning.state)!r} and has not "
            f"committed, so pruning now would delete recovery points the run "
            f"still behind them may need",
            remedy=Remedy.REPORT_DEFECT,
            detail={"session_id": owning.session_id, "state": str(owning.state)},
        )
    if owning is None:
        open_runs = [entry for entry in session.records(cfg) if not entry.terminal]
        if open_runs:
            raise refuse(
                "internal-error",
                "pruning was asked for with no session named, and "
                + (
                    f"{len(open_runs)} session has not reached a terminal state"
                    if len(open_runs) == 1
                    else f"{len(open_runs)} sessions have not reached a terminal state"
                )
                + ": "
                + ", ".join(entry.session_id for entry in open_runs[:20])
                + ". Pruning now would delete recovery points a run still behind "
                "them may need",
                remedy=Remedy.REPORT_DEFECT,
                detail={"open_sessions": [entry.session_id for entry in open_runs[:20]]},
            )
    decided = retention_plan(
        cfg, policy=policy, root=root, protected_provider=protected_provider, now=now
    )
    removed: list[Path] = []
    for entry in decided.deleting:
        shutil.rmtree(entry.root, ignore_errors=False)
        removed.append(entry.root)
        logger.info("pruned capture %s", entry.root.name)
    return tuple(removed)


# ---------------------------------------------------------------------------
# Bare-metal recovery: the library volume itself is gone
# ---------------------------------------------------------------------------

#: The mount verdicts that mean the configured library is NOT THERE, as opposed
#: to present or unknown.
_VOLUME_IS_GONE: frozenset[preflight.MountState] = frozenset(
    {
        preflight.MountState.NOT_MOUNTED,
        preflight.MountState.LIBRARY_PATH_MISSING,
        preflight.MountState.FOREIGN_VOLUME,
    }
)


def recovery_lock_path() -> Path:
    """The installation-scoped lock a bare-metal recovery takes.

    Needs no configuration, since every KTD21 gate lives beside the lost library.
    """
    return config.state_path(RECOVERY_LOCK_KEY)


def _refuse_target(message: str, steps: Sequence[str], **detail: object) -> CratekitError:
    return refuse(
        "recovery-target-refused",
        message,
        steps=tuple(steps),
        scope=Scope.RUN,
        origin=("restore",),
        detail=dict(detail),
    )


def assert_library_volume_is_gone(
    cfg: config.Config,
    *,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> preflight.MountState:
    """Refuse unless the library this installation names is genuinely unreachable.

    Keeps the cases apart: a present library must use the three real gates, so
    the weaker substitutes are reachable only when it is gone. Absent is gone,
    mounted elsewhere is alive, and an unreported identity is not "gone".
    """
    try:
        preflight.assert_library_volume(
            cfg.library.root,
            cfg.library.volume_id,
            destructive=True,
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
        )
    except preflight.LibraryVolumeError as exc:
        if exc.status.state in _VOLUME_IS_GONE:
            return exc.status.state
        raise _refuse_target(
            f"the library volume is not absent, it is {exc.status.state.value}; a "
            f"bare-metal recovery substitutes weaker gates for the library-scoped "
            f"ones and is refused whenever the real ones could be read",
            steps=(
                "mount the library where this installation expects it and use the "
                "ordinary restore, which passes all three gates",
            ),
            state=str(exc.status.state),
            configured_root=str(cfg.library.root),
        ) from exc
    raise _refuse_target(
        f"the library at {cfg.library.root} is mounted and is the volume this "
        f"installation was set up against, so there is nothing to recover from "
        f"bare metal",
        steps=("use the ordinary restore, which passes all three gates",),
        configured_root=str(cfg.library.root),
    )


#: Answers "is this directory the root of its own filesystem". A seam, since the
#: real answer needs a mounted volume. A probe that always answers yes disables
#: the boot-disk check; nothing in ``src/`` passes one, and
#: ``test_round2_the_real_mount_probe_is_armed_by_default`` keeps the default real.
MountProbe = Callable[[Path], bool]


def _is_mount_point(path: Path) -> bool:
    """Whether a directory is the root of its own filesystem.

    Asked of the filesystem identifier, since an unmounted volume leaves an empty
    folder on the internal disk at the same path.
    """
    try:
        return path.stat().st_dev != path.parent.stat().st_dev
    except OSError:
        return False


def recovered_database_fileset(cfg: config.Config, target: Path) -> tuple[Path, ...]:
    """Where a recovery onto ``target`` lands the database, then each companion.

    Repeats ``backup.database_target_for``'s re-basing, since this layer does not
    import the backup module;
    ``test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`` holds them
    together.
    """
    database = config.state_path("rekordbox_db", cfg)
    try:
        landing = target / database.relative_to(cfg.library.root)
    except ValueError:
        landing = target / database.name
    companions = tuple(
        landing.with_name(landing.name + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    return (landing, *companions)


def assert_recovery_target(
    cfg: config.Config,
    target: Path | str,
    *,
    replacing_existing: bool = False,
    mount_probe: MountProbe | None = None,
) -> Path:
    """Refuse a bare-metal target that is not one. Reads only; creates nothing.

    The stub check covers a target at or inside the configured root and one beside
    it (a suffixed mount name), each answered by the filesystem identifier.
    """
    where = Path(target)
    if not where.is_dir():
        raise _refuse_target(
            f"the recovery target {where} is not a directory that exists",
            steps=("mount or create the volume to recover onto, then run this again",),
            target=str(where),
        )
    probe = mount_probe or _is_mount_point
    configured = Path(cfg.library.root).resolve()
    resolved = where.resolve()
    inside_configured = resolved == configured or configured in resolved.parents
    beside_configured = resolved.parent == configured.parent
    if (inside_configured or beside_configured) and not probe(where):
        raise _refuse_target(
            (
                f"{where} is at or inside the path this installation's library was "
                f"mounted at"
                if inside_configured
                else f"{where} sits in the directory this installation's library "
                f"mounts into, under a name one this system chose"
            )
            + ", and is not a mount point now, so it is the empty folder an "
            "unmounted volume leaves behind; recovering into it would write the "
            "library onto the internal disk, where the volume will hide it the "
            "moment it is plugged back in",
            steps=(
                "mount the replacement volume at this path first, or name a "
                "different target",
            ),
            target=str(where),
            configured_root=str(configured),
        )
    # Only where THIS library's database lands, since the mirror deletes nothing
    # and reruns must pass (R-592).
    existing = [entry for entry in recovered_database_fileset(cfg, where) if entry.exists()]
    if existing and not replacing_existing:
        raise _refuse_target(
            f"{where} already holds {existing[0].name}; a recovery that replaced "
            f"it would destroy a library nobody named for replacement",
            steps=("name this target for replacement explicitly, or choose another",),
            target=str(where),
            holds=[str(entry) for entry in existing[:20]],
        )
    return where


@contextmanager
def bare_metal_session(
    cfg: config.Config,
    *,
    target: Path | str,
    acknowledged: bool,
    replacing_existing: bool = False,
    terminal: Callable[[], bool] | None = None,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
    mount_probe: MountProbe | None = None,
) -> Iterator[Held]:
    """Hold the substitute gates for the case where the library volume is gone.

    Every KTD21 gate is library-scoped and died with the volume (R-8), so each is
    substituted:

    * VOLUME: the configured library is unreachable and the target is a real
      mount, not an unmounted volume's stub;
    * ACKNOWLEDGMENT: an explicit decision at a controlling terminal, by an actor
      derived from the process; WEAKER than R34's record, which is on the dead volume;
    * LOCK: installation-scoped, since no shared volume is left to contend over.

    The read-only assertions run before the lock, so a refusal changes nothing.
    :func:`plan` and :func:`run` derive every path from this session through
    :func:`_rooted` (:data:`RESIDUAL_BARE_METAL_HAS_NO_WRITE_PATH`). The caller is
    the recovery verb in ``cratekit.session.restore_cli``, which spends it on the
    off-machine restore. A target already holding a library holds a lock this does
    not take, and needs ``replacing_existing``.
    """
    assert_library_volume_is_gone(
        cfg, identity_provider=identity_provider, mount_enumerator=mount_enumerator
    )
    where = assert_recovery_target(
        cfg, target, replacing_existing=replacing_existing, mount_probe=mount_probe
    )
    probe = terminal or session.has_controlling_terminal
    if not probe():
        raise _refuse_target(
            "this invocation has no controlling terminal, so there is nobody here "
            "to accept a recovery that replaces a library; the acknowledgment this "
            "substitutes for is a person's act and its record is on the volume "
            "that died",
            steps=("run the recovery from a terminal a person is sitting at",),
            target=str(where),
        )
    if not acknowledged:
        raise _refuse_target(
            "a bare-metal recovery writes a whole library onto the target and is "
            "not performed without an explicit decision naming that target",
            steps=("name the target and accept the replacement explicitly",),
            target=str(where),
        )
    actor = session.derive_actor()
    logger.warning(
        "bare-metal recovery accepted by %s onto %s, with library-scoped gates "
        "unreachable",
        actor,
        where,
    )
    with session.session_lock(path=recovery_lock_path()) as lock:
        # THE TARGET RIDES ON THE VALUE, so the paths come from what was validated.
        with _issued(
            workflow=BARE_METAL_WORKFLOW,
            lock=lock,
            issued_by=Guard.BARE_METAL,
            authorises=where,
        ) as held:
            yield held


__all__ = [
    "BARE_METAL_WORKFLOW",
    "CAPTURE_RESTORE_WORKFLOW",
    "DEFAULT_KEEP",
    "DEFAULT_MAX_AGE",
    "KEEP_STAGED_ATTEMPTS",
    "PRE_RESTORE_DIR",
    "PRE_CUTOVER_RESTORE",
    "RECOVERY_LOCK_KEY",
    "RESIDUAL_BARE_METAL_HAS_NO_WRITE_PATH",
    "RESIDUAL_CAPTURE_VOLUME_UNREPORTED",
    "Act",
    "Guard",
    "Held",
    "Plan",
    "RetentionPlan",
    "RestoreOutcome",
    "RetentionPolicy",
    "Restorable",
    "Step",
    "StoredCapture",
    "assert_gates_are_open",
    "assert_library_volume_is_gone",
    "assert_recovery_target",
    "recovered_database_fileset",
    "bare_metal_session",
    "capture_root_of",
    "list_sessions",
    "plan",
    "prune",
    "recovery_lock_path",
    "recovery_session",
    "restorable_targets",
    "space_peak_bytes",
    "retention_plan",
    "run",
    "shares_the_database_volume",
]
