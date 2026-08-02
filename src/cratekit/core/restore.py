"""Spending the capture: the restore, its retention bounds, and its one held session.

A capture nobody can spend is a directory of files. This module is the spend, and
it is the most destructive thing this product does: it replaces a live rekordbox
database and the state coupled to it with an earlier copy, and there is no undo
for the undo. Four properties carry that weight.

**A RESTORE REPLACES EXACTLY THE DERIVED COUPLED SET, AND NOTHING ELSE.** Every
target comes from the state inventory, through ``config.snapshot_sources`` and
``config.sidecar_paths``, which is the same declaration the capture side reads. A
set even slightly different from the captured one is the plan's top-ranked risk
arriving from the restore end: the registry rolling back while the database does
not, or the reverse. Nothing declared NEVER_RESTORED or SURVIVES_ROLLBACK can be
reached from here, and that is asserted rather than assumed, because two of those
entries are locks whose inodes this very process is holding.

**THE STORAGE ENGINE'S COMPANION FILES ARE ASYMMETRIC, AND THE ASYMMETRY IS
DECLARED RATHER THAN RETYPED.** Both live companions are cleared first, so the
engine cannot replay a log belonging to the database that was just replaced; then
only the companions the inventory marks as restored are written back. Which those
are is ``Sidecar.restored``'s answer, not a suffix spelled here, because a
literal in this module is precisely the companion list the schema exists to
abolish.

**ONE SESSION SPANS THE WHOLE VERB.** The destructive-session gates are entered
once, by :func:`recovery_session`, and everything the verb does happens inside
that one guard: the listing, the plan, the write, and the composition with the
off-machine backup restore, which takes the already-open guard as its ``gates``
seam rather than acquiring its own. The shape being avoided is specific and was
found by review: a plan that takes the lock and gives it back, followed by a run
that takes it again, leaves a window in which a second process passes the same
gates and commits, after which the run copies a snapshot over a commit its plan
was built before.

**A DRY RUN AND A REAL RUN WALK ONE LIST.** :func:`plan` produces an ordered
tuple of :class:`Step` values and :func:`run` iterates it, performing each step or
not. There is no second code path for the preview, because a preview built by a
second code path is a report about a different program.

WHAT A RESTORE CANNOT DO is undo anything that left the coupled set: audio on the
music volume, a playlist renamed at the provider, a file already in the Trash.
Those are enumerated, recorded, and refused over by ``core.reconcile``, and the
enumeration happens BEFORE anything is replaced, because afterwards the live
state IS the captured state and every comparison reports that nothing happened.

LAYER: write, and the same exception the tree registry already takes. It lives
under ``core/`` because the pending register and the state inventory name it
there, and it is ranked with the write layer because it reads the tree registry
to decide which trees a pre-cutover restore leaves unconverged. Nothing below it
imports it.
"""

from __future__ import annotations

import logging
import os
import shutil
import tempfile
from contextlib import AbstractContextManager, contextmanager, nullcontext
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pathlib import Path
from typing import Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.core import (
    config,
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

#: What the session log calls a restore of one of this product's own captures. A
#: workflow LABEL rather than a verb name: this layer does not decide what the
#: command line calls itself, and the log records what happened rather than what
#: somebody typed (D2).
#:
#: NOT called ``RESTORE_WORKFLOW``. ``modules.tools.backup`` already exports that
#: name for the OFF-MACHINE restore, with a different value, and the two land in
#: the same log field. A caller importing the wrong one would record an rclone
#: pull as a capture restore, and nothing would raise, because both are strings
#: and the field takes either.
CAPTURE_RESTORE_WORKFLOW = "capture-restore"

#: What the log calls the case where the library volume itself is gone. Its own
#: label because it passes a DIFFERENT set of gates, and a log that called both
#: by one name would make the weaker gates invisible afterwards.
BARE_METAL_WORKFLOW = "bare-metal-recovery"

#: The installation-scoped lock a bare-metal recovery takes in place of the
#: library one. Named once, so this module and the inventory cannot disagree.
RECOVERY_LOCK_KEY = "recovery_lock"


# ---------------------------------------------------------------------------
# What is restorable
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Restorable:
    """One session, its capture, and whether that capture can be spent.

    ``unusable`` is a sentence rather than a flag, and an unusable entry is still
    LISTED. A session whose capture directory was deleted by hand, or whose
    manifest a later build wrote, is exactly the session a person is about to go
    looking for, and dropping it from the list answers their question with
    silence.
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

    A record may name either the directory or the database file inside it,
    because the capture function returns the file path while the composing layer
    records the root. Both spellings are honoured here for the same reason
    ``rb_writer.default_protected_snapshot_paths`` honours both: two readings of
    one recorded value is how a capture ends up protected by one consumer and
    prunable by the next.
    """
    path = Path(recorded)
    return path if path.is_dir() else path.parent


def list_sessions(cfg: config.Config) -> tuple[Restorable, ...]:
    """Every recorded session, newest first, with its change summary and capture.

    Newest FIRST, unlike the log's own ordering, because the question a person
    asks of this list is "what did I just do" far more often than "what did I do
    in June". The ordering key is the recorded start rather than a directory
    modification time, so a capture touched by a backup tool does not reorder the
    history.
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


@dataclass(frozen=True, slots=True)
class Held:
    """An OPEN destructive session, handed to everything the verb then does.

    ``guard`` is the whole reason this type exists. The off-machine backup
    restore takes a zero-argument callable returning a context manager as its
    ``gates`` seam, and handing it this method rather than letting it default is
    what makes both halves of that restore run inside ONE acquisition. The
    context manager it returns does nothing, deliberately: the gates are already
    held by the block this value was yielded into, and taking them again in this
    process would be reported as a foreign holder, which is to say the caller
    would be told to wait for itself.
    """

    workflow: str
    lock: Path
    intent: session.Intent
    gates: session.Gates | None = None
    record: session.SessionRecord | None = None

    def guard(self) -> AbstractContextManager[Held]:
        return nullcontext(self)

    @property
    def still_open(self) -> bool:
        """Whether the gates this value describes are held BY THIS PROCESS, NOW.

        The distinction is the whole reason this is a property rather than a
        field. A ``Held`` is an ordinary value: it outlives the block that
        yielded it, and a caller who kept one and used it afterwards would be
        writing with no lock at all while every signature said otherwise.
        Asking the session module's own record of what this process holds is the
        only answer that cannot be stale, because it is the same set the lock
        acquisition maintains.
        """
        return str(self.lock.absolute()) in session._HELD


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

    IT DECLARES ITSELF A RECOVERY, and that declaration buys exactly two things,
    both of which are latches whose own remedy is a recovery. A library latched
    by a session that ended committed-unverified does not refuse this, and a
    library holding an unreconciled restore does not either. All three gates
    apply unchanged: the volume identity assertion, the backup acknowledgment,
    and the library lock. A recovery is exempt from the latches and from nothing
    else.

    THE RECORD IS OPENED INSIDE THE GATES AND CLOSED ON BOTH PATHS. A restore
    that raised part way through would otherwise leave a record open forever,
    protecting a capture from retention and refusing every later close. It closes
    ABANDONED on a failure and CLOSED on success, which is the same split
    ``close_run`` makes for the same reason: closing is the claim that the work
    finished and abandoning is the opposite claim.
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
    ) as gates:
        record = session.open_session(cfg, workflow=workflow, now=now)
        held = Held(
            workflow=workflow,
            lock=gates.lock,
            intent=session.Intent.RECOVERY,
            gates=gates,
            record=record,
        )
        try:
            yield held
        except BaseException:
            session.close_session(
                record, cfg, state=session.SessionState.ABANDONED, now=now
            )
            raise
        session.close_session(
            record,
            cfg,
            state=session.SessionState.CLOSED,
            intent=session.Intent.RECOVERY,
            now=now,
        )


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


class Act(StrEnum):
    """One kind of thing a restore does. The set is closed and the ORDER matters.

    ``RECORD`` first, because what a restore cannot undo has to be written down
    before the evidence for it is overwritten. ``CLEAR`` before ``REPLACE``,
    because a companion log left beside a database that has started to change is
    a log the engine will replay onto the wrong file. ``RESOLVE`` last, because
    it is the claim that the condemning record has been answered, and a claim
    made before the work is a claim that can be wrong.
    """

    RECORD = "record-reconciliation"
    CLEAR = "clear-companion"
    REPLACE = "replace-file"
    REPLACE_TREE = "replace-directory"
    REMOVE = "remove-absent"
    RESOLVE = "resolve-session"


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
    """A whole restore, decided and not yet performed."""

    session_id: str
    capture_root: Path
    steps: tuple[Step, ...]
    discarded_sessions: tuple[str, ...] = ()
    discarded_change: session.ChangeSummary = field(default_factory=session.ChangeSummary)
    markers: tuple[reconcile.Marker, ...] = ()
    unconverged: tuple[str, ...] = ()
    unverified_sessions: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RestoreOutcome:
    """What a restore did, or would have done.

    NOT called ``Outcome``. ``core.cause`` exports one already, a string enum of
    how a run ended, and this module imports from that same module. It follows
    the shape ``backup.BackupOutcome`` set for the same reason.
    """

    plan: Plan
    performed: tuple[Step, ...]
    dry_run: bool
    resolved: tuple[str, ...] = ()
    outstanding: tuple[str, ...] = ()

    @property
    def converged(self) -> bool:
        return not self.outstanding


def restorable_targets(cfg: config.Config) -> frozenset[Path]:
    """Every path a restore is allowed to touch, DERIVED, never listed.

    The union of what the capture side takes: the database and its companion
    files, rekordbox's own legacy playlist file beside it, and everything
    ``config.snapshot_sources`` declares. Anything else in a manifest is refused
    rather than skipped, because a manifest naming a path outside this set is
    either a build this one does not understand or a file somebody edited, and
    both of those are reasons to stop rather than to proceed with the subset that
    happens to be recognised.

    This is also what makes "a restore never touches a lock" true rather than
    intended. The declared roles resolve NEVER_RESTORED and SURVIVES_ROLLBACK
    entries into different directories, so no lock and no session record can be a
    member of this set, and :func:`plan` asserts the membership rather than
    trusting the layout.
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

    Two resolutions, because the capture has two shapes. Entries living inside the
    coupled directory travel as part of one directory copy, so their captured path
    is composed from that directory's position in the capture. Everything else was
    copied individually and the manifest names where it landed.

    Composed from the entry's own declared position rather than from a per-entry
    literal, so an entry added to the inventory is found without anybody
    remembering this function exists.
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

    Two ways, and both count. A source marked committed is the ordinary one. A
    session that ended committed-unverified is the sharp one: the commit landed
    and only the read-back disagreed, so the rows are there and discarding them
    is discarding real work.
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
    now: datetime | None = None,
) -> Plan:
    """Decide a restore, or refuse. Nothing here writes.

    ``held`` is the open recovery session, required rather than optional so there
    is no call shape that reaches this function without the gates, and so the
    plan and the run provably share one acquisition.

    ``discarding`` is the override, and it is a LIST OF SESSION IDENTIFIERS
    rather than a boolean. A restore that reaches back past a later session which
    committed is destroying work somebody did on purpose, and a flag saying "yes"
    is an answer to a question nobody read. Naming them means the refusal shows
    the trees and the counts, the caller repeats the identifiers back, and the two
    have to agree exactly; a set that does not match is refused again rather than
    interpreted generously.
    """
    assert_gates_are_open(held)
    record = session.read_record(session_id, cfg)
    if not record.snapshot_path:
        raise refuse(
            "internal-error",
            f"session {session_id} recorded no capture, so there is nothing to "
            f"restore it from",
            remedy=Remedy.REPORT_DEFECT,
            detail={"session_id": session_id},
        )
    root = capture_root_of(record.snapshot_path)
    captured = snapshot.read_manifest(root)
    # A capture that did not pass its integrity check is not a smaller recovery
    # point, it is the absence of one, and restoring FROM one would put a live
    # library behind a file nobody has established can be opened.
    snapshot.assert_verified(captured)

    later = _later_committed(cfg, record)
    _assert_override_names_them(record, later, discarding)

    allowed = restorable_targets(cfg)
    steps: list[Step] = []

    by_key = _captured_by_key(cfg, captured)
    markers = list(
        reconcile.effect_markers(
            cfg,
            captured=by_key,
            session_id=session_id,
            capture_stamp=captured.stamp,
            now=now,
        )
    )
    unconverged = _trees_the_capture_predates(cfg, captured, by_key)
    markers.extend(
        reconcile.tree_markers(
            unconverged, session_id=session_id, capture_stamp=captured.stamp, now=now
        )
    )
    if markers:
        steps.append(
            Step(
                act=Act.RECORD,
                detail=(
                    f"record {len(markers)} "
                    + ("thing" if len(markers) == 1 else "things")
                    + " this restore cannot undo, before the evidence for them is "
                    "replaced"
                ),
            )
        )

    steps.extend(_file_steps(cfg, captured, allowed))

    unverified = tuple(
        entry.session_id
        for entry in session.records(cfg)
        if entry.state is session.SessionState.COMMITTED_UNVERIFIED
    )
    if unverified:
        # ONE step for all of them rather than one each. The action is a single
        # sweep over the record, so emitting it per session would make the second
        # and later steps no-ops that a reader of the preview would count as work.
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

    return Plan(
        session_id=session_id,
        capture_root=root,
        steps=tuple(steps),
        discarded_sessions=tuple(entry.session_id for entry in later),
        discarded_change=_merged_change(later),
        markers=tuple(markers),
        unconverged=unconverged,
        unverified_sessions=unverified,
    )


def _later_committed(
    cfg: config.Config, target: session.SessionRecord
) -> tuple[session.SessionRecord, ...]:
    """Every session that committed after the one being restored to.

    Compared on the RECORDED START rather than on a capture directory's timestamp
    or on identifier order alone. The identifier is derived from the start, so in
    practice the two agree; comparing the field that is actually persisted means
    they cannot come apart if the identifier scheme ever changes.
    """
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
    """Everything the given sessions did, per tree, as one summary.

    PER TREE, because that is the only form in which a person can judge the
    question being asked. One aggregate number says nothing about whether the
    forty changes were in the tree they care about, which is exactly why the
    change summary was built per tree in the first place.
    """
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

    DERIVED FROM THE CAPTURED REGISTRY RATHER THAN FROM DATE ARITHMETIC, and the
    difference is not cosmetic. A cutover carries a date, and comparing that date
    against the capture's own is off by a whole day in both directions: a
    same-day cutover before a capture reads as after it, and the fix for that
    reads every same-day restore as unconverged, which is a guard that fires on
    correct behaviour and therefore a guard people route around (P7). The
    registry inside the capture is the exact record of which trees had cut over
    at that moment, and it is right there in the capture.

    A registry that is absent or unreadable inside the capture is treated as
    declaring nothing, which marks every currently-native tree. That is the
    conservative direction: over-marking costs a rebuild, and under-marking
    leaves a tree silently short with an incremental sync that structurally
    cannot see the gap.

    ``by_key`` is where the capture actually put each coupled entry, composed
    once by :func:`_captured_by_key`. Composing a second answer here is how a
    reader ends up looking at the top of the capture for a file that travelled
    inside the coupled directory, which reads as "the registry was empty" and
    marks every tree on every restore.
    """
    try:
        live = tree_registry.read(cfg)
    except tree_registry.TreeRegistryUnreadable:
        # Nothing can be said about which trees are native, so nothing is marked
        # here. The registry itself refuses at the next governed verb, which is a
        # louder and more accurate refusal than a marker would be.
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

    THE COMPANION FILES ARE CLEARED BEFORE ANY COPY, including before the coupled
    directories, and that is the strongest form of the invariant rather than the
    cheapest: at no point during a restore does a stale log sit beside a database
    that has started to change. Which companions exist is
    ``config.sidecar_paths``; which of them come back is the same declaration
    asked with ``restored_only``, so the two answers cannot drift into a stale
    shared-memory index being written back beside a fresh log.

    ABSENCE IN THE CAPTURE IS AN INSTRUCTION, NOT A GAP. The manifest records the
    difference between a source that was captured and one that was legitimately
    not there, and returning the library to its pre-session state means removing
    what the capture says did not exist. Skipping that would leave a file the
    session created standing behind a database that has never heard of it.
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
            # Captured for completeness, never written back: it is derived from
            # the log, and putting a stale one beside a fresh log hands the engine
            # two disagreeing views of one database. It was cleared above and
            # stays cleared.
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

    The dry run and the real run differ in exactly one expression, and it is
    inside the loop rather than around it. Every step is described, in the same
    sequence, by the same code, whichever mode this is in; the preview is
    therefore evidence about the write rather than a second program's opinion of
    it.

    A DRY RUN PERFORMS NOTHING AT ALL, including the clearing. Deleting the live
    companion files is itself destructive, so a rehearsal that cleared them and
    then copied nothing would leave the user's database without the log it needs:
    a preview that did the damage and skipped the repair.

    REKORDBOX IS RE-ASSERTED CLOSED HERE, even though the plan asserted it, and
    even for a rehearsal. Restoring underneath a live application replaces the
    file it holds open, which leaves the application and the disk describing two
    different libraries; and a rehearsal run while the application is writing
    describes a library that is changing underneath it.
    """
    assert_gates_are_open(held)
    _assert_rekordbox_closed(process_lister)
    performed: list[Step] = []
    resolved: list[str] = []
    for step in decided.steps:
        performed.append(step)
        if dry_run:
            continue
        resolved.extend(_perform(step, decided, cfg, now=now))
    # Read on BOTH paths. What is outstanding is a fact about the library rather
    # than about this call, and a rehearsal that reported convergence because it
    # recorded nothing itself would be the preview lying about the world.
    outstanding = tuple(record.marker.marker_id for record in reconcile.outstanding(cfg))
    return RestoreOutcome(
        plan=decided,
        performed=tuple(performed),
        dry_run=dry_run,
        resolved=tuple(resolved),
        outstanding=outstanding,
    )


def assert_gates_are_open(held: Held) -> None:
    """Refuse unless the gates are held by this process AT THIS MOMENT.

    A ``Held`` parameter on :func:`plan` and :func:`run` makes it impossible to
    reach either without having entered the guard once. That is not the same as
    being inside it, and the difference is a whole restore: a caller can keep the
    value, leave the block, and call ``run`` afterwards, at which point every
    signature still says the gates were passed and the library lock is on the
    floor. Nothing about the types can catch that, so it is asked rather than
    assumed, and it is asked in the two places that matter rather than once at
    construction.

    THE INTENT IS ASSERTED TOO. A restore that ran as an ordinary write would be
    refused by the very latches its own success is the remedy for, so a ``Held``
    that is not a recovery is a defect in the caller rather than a shape to
    accommodate.
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
    if held.still_open:
        return
    raise refuse(
        "internal-error",
        f"the destructive-session gates for {held.workflow} are no longer held by "
        f"this process, so this call would plan or write with the library lock "
        f"released and every other process free to commit underneath it",
        remedy=Remedy.REPORT_DEFECT,
        detail={"workflow": held.workflow, "lock": str(held.lock)},
    )


def _assert_rekordbox_closed(process_lister: processes.ProcessLister | None = None) -> None:
    """Refuse while the application or its background agent holds the database.

    Through ``core.processes``, which returns a TUPLE and takes an injectable
    lister, rather than through the guarded writer's same-named probe, which
    returns a comma-joined string and takes none. The two are deliberately
    different and the divergence is asserted elsewhere; naming the wrong one here
    would produce a refusal message spelled one character at a time.
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

    The plan arrives as ``decided`` rather than as ``plan`` here and in
    :func:`run`, because ``plan`` is a module-level function in this file and a
    parameter of that name shadows it. Nothing calls it from inside these two
    today, which is exactly the condition under which the next person adds a call
    and gets the parameter with nothing raised.
    """
    if step.act is Act.RECORD:
        reconcile.record_markers(cfg, decided.markers)
        return ()
    if step.act is Act.RESOLVE:
        return _resolve_unverified(decided, cfg, now=now)
    if step.target is None:  # pragma: no cover - every other act carries a target
        raise refuse(
            "internal-error",
            f"the step {step.act} carries no target",
            remedy=Remedy.REPORT_DEFECT,
            detail={"act": str(step.act)},
        )
    if step.act is Act.CLEAR:
        step.target.unlink(missing_ok=True)
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
    return ()


def _resolve_unverified(
    decided: Plan, cfg: config.Config, *, now: datetime | None = None
) -> tuple[str, ...]:
    """Answer every condemning record this restore has now made false.

    THE LATCH SURVIVES ITS OWN REMEDY, which is why this is a step rather than a
    side effect of the copy. The session log is declared SURVIVES_ROLLBACK on
    purpose, because rolling it back would erase the record of which sessions are
    restorable, and that is exactly what somebody needs in order to restore
    again. The consequence is that a committed-unverified record outlives the
    restore that answers it, and without this a user who did precisely what the
    refusal asked would find the next write still refused with the remedy already
    spent.

    EVERY such record is resolved, not only the one being restored to. The
    library now holds a capture that passed its integrity check, so no earlier
    unverified commit condemns these bytes either; leaving one standing would
    refuse the next write over a commit that no longer exists.
    """
    answered: list[str] = []
    for session_id in decided.unverified_sessions:
        try:
            session.resolve_unverified_session(session_id, cfg, now=now)
        except CratekitError as exc:
            # Already resolved by somebody else, or moved on since the plan was
            # built. Not fatal: the restore itself has landed, and refusing here
            # would report a failed restore over a bookkeeping race.
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

    The rename is what makes it atomic, and it is only a rename when both names
    are on one filesystem, which is why the temporary file is created beside the
    target rather than in the platform's temporary directory. Copying straight
    onto the target would leave a half-written database if anything interrupted
    it, and a half-written database is the state this whole module exists to get
    somebody out of.
    """
    config._mkdir_private(target.parent)
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

    Copying into a live directory after deleting it leaves a window in which the
    coupled state does not exist at all, and a crash in that window loses the
    old contents without having landed the new ones. Staging beside the target
    and then renaming reduces the window to two renames, and the failure between
    them leaves the old directory under a name a person can find rather than
    nowhere.
    """
    config._mkdir_private(target.parent)
    staged = target.with_name(f"{target.name}.restoring")
    previous = target.with_name(f"{target.name}.replaced")
    _remove(staged)
    _remove(previous)
    shutil.copytree(source, staged)
    if target.exists():
        os.replace(target, previous)
    os.replace(staged, target)
    _remove(previous)


# ---------------------------------------------------------------------------
# Retention (R30)
# ---------------------------------------------------------------------------

#: How many captures survive on count alone. Five is what the guarded writer
#: already defaults to, carried rather than re-chosen so two answers to one
#: question cannot exist.
DEFAULT_KEEP = 5

#: How old a capture may be before count stops protecting it. A month is long
#: enough to cover a person who works in bursts and short enough that a library
#: does not silently accumulate a year of database copies.
DEFAULT_MAX_AGE = timedelta(days=30)


@dataclass(frozen=True, slots=True)
class RetentionPolicy:
    """Three bounds, and a capture survives only if it clears all of them.

    THREE RATHER THAN ONE, because each answers a question the others cannot. A
    count alone keeps five captures of a library that has not been written to
    since March, which is five copies of one database. An age alone keeps nothing
    at all on a machine that was idle for a month, which is the machine most
    likely to need one. A byte bound alone lets a run of tiny captures fill a
    volume with directories.

    ``max_bytes`` is None by default because the right number depends on the
    volume, and a default that guessed would either do nothing or delete somebody's
    recovery point on the first run.
    """

    keep: int = DEFAULT_KEEP
    max_age: timedelta | None = DEFAULT_MAX_AGE
    max_bytes: int | None = None


@dataclass(frozen=True, slots=True)
class StoredCapture:
    """One capture directory on disk, with what retention needs to judge it.

    NOT called ``Capture``. ``snapshot.Capture`` is the manifest record saying
    what a capture holds and whether it verified, and this module holds both in
    one namespace. Two ideas under one name in modules that import each other is
    the collision this repository keeps finding after the fact, and here the two
    would be one import line apart.
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

    R30 asks that it does not, so that one volume failure cannot take both the
    library and every undo for it. The default layout puts the capture store
    beside the library and the containment rule pulls the database inside the
    library root, so the preferred install has them on one volume and this
    answers True.

    REPORTED RATHER THAN REFUSED, deliberately. Refusing would make the product
    unusable in the layout it recommends, which is the shape of a guard people
    switch off; and the honest fix is a second location the user chooses, which is
    configuration this unit does not add. It is compared on the filesystem
    identifier rather than on path prefixes, because a bind mount, a symlink or a
    nested mount point all make a prefix comparison confidently wrong.
    """
    store = root if root is not None else snapshot.store_root(cfg)
    database = config.state_path(snapshot.DATABASE_KEY, cfg)
    left = _device_of(store)
    right = _device_of(database)
    return left is not None and left == right


def _device_of(path: Path) -> int | None:
    probe = path
    while True:
        try:
            return probe.stat().st_dev
        except OSError:
            if probe.parent == probe:
                return None
            probe = probe.parent


def retention_plan(
    cfg: config.Config,
    *,
    policy: RetentionPolicy | None = None,
    root: Path | str | None = None,
    protected_provider: Callable[[], set[Path]] | None = None,
    now: datetime | None = None,
) -> RetentionPlan:
    """Decide what retention would delete. Reads only.

    A capture an OPEN session references is spared whatever else is true of it,
    which is R30 in one sentence: a snapshot an unfinished run may restore from is
    not old, whatever its position in the retention order. The protected set comes
    from the guarded writer's own provider, called rather than reimplemented,
    because two derivations of "which captures are in use" is how one of them ends
    up sparing the wrong ones.

    A PROVIDER THAT RAISES DELETES NOTHING. A transient failure in an unrelated
    module must not cost somebody their recovery point, and a capture kept one run
    too long costs disk.
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
        # Oldest first, because the byte bound is the least specific of the three
        # and should give up the least useful capture first.
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

    ``owning`` is the session this prune belongs to, and passing a session that
    has not reached a terminal state REFUSES. The source system pruned from
    inside the snapshot function, which put retention before the commit the
    snapshot exists to protect; the fix was to make pruning a separate step the
    caller places afterwards, and this is the assertion that stops the separate
    step being placed in the same wrong position by hand.

    The plan is built and then performed, so what is deleted is exactly what a
    caller could have been shown.
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

#: The mount verdicts that mean the library this installation was set up against
#: is NOT THERE. Everything else means something is there, or that this platform
#: cannot say, and neither of those is the same question.
_VOLUME_IS_GONE: frozenset[preflight.MountState] = frozenset(
    {
        preflight.MountState.NOT_MOUNTED,
        preflight.MountState.LIBRARY_PATH_MISSING,
        preflight.MountState.FOREIGN_VOLUME,
    }
)


def recovery_lock_path() -> Path:
    """The installation-scoped lock a bare-metal recovery takes.

    Installation-scoped, and no configuration is needed to resolve it, which is
    the entire point: every gate KTD21 publishes lives beside the library, so all
    of them are unreachable in the one case this path exists for.
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

    THIS IS THE GATE THAT KEEPS THE TWO CASES APART, and keeping them apart is
    the whole reason a bare-metal path is allowed to exist at all. A library that
    is present and damaged has all three real gates available and must use them.
    A bare-metal recovery substitutes weaker ones, so it must be unreachable by
    anything that could have passed the real ones.

    THREE ANSWERS, NOT TWO, which is the lesson the liveness probe already
    records. A volume that is absent is gone. A volume mounted somewhere else is
    alive and should be used where it is. A platform that will not report an
    identity has said nothing, and reading silence as "gone" is how a recovery
    runs against a library that was there all along.
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


def _is_mount_point(path: Path) -> bool:
    """Whether a directory is the root of its own filesystem.

    Asked of the filesystem identifier rather than of the path, because the
    hazard is precisely a path that LOOKS right: when an external volume is
    unmounted, the directory it was mounted at is still there and is now an
    ordinary empty folder on the internal disk. Restoring a library into it fills
    the boot disk and puts the result somewhere the volume will hide the moment
    it is plugged back in.
    """
    try:
        return path.stat().st_dev != path.parent.stat().st_dev
    except OSError:
        return False


def assert_recovery_target(
    cfg: config.Config, target: Path | str, *, replacing_existing: bool = False
) -> Path:
    """Refuse a bare-metal target that is not one. Reads only; creates nothing."""
    where = Path(target)
    if not where.is_dir():
        raise _refuse_target(
            f"the recovery target {where} is not a directory that exists",
            steps=("mount or create the volume to recover onto, then run this again",),
            target=str(where),
        )
    if where.resolve() == Path(cfg.library.root).resolve() and not _is_mount_point(where):
        raise _refuse_target(
            f"{where} is the path this installation's library was mounted at and "
            f"is not a mount point now, so it is the empty folder an unmounted "
            f"volume leaves behind; recovering into it would write the library "
            f"onto the internal disk, where the volume will hide it the moment it "
            f"is plugged back in",
            steps=(
                "mount the replacement volume at this path first, or name a "
                "different target",
            ),
            target=str(where),
        )
    existing = sorted(where.glob("*.db"))
    if existing and not replacing_existing:
        raise _refuse_target(
            f"{where} already holds {existing[0].name}; a recovery that replaced "
            f"it would destroy a library nobody named for replacement",
            steps=("name this target for replacement explicitly, or choose another",),
            target=str(where),
            holds=[str(entry) for entry in existing],
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
) -> Iterator[Held]:
    """Hold the substitute gates for the case where the library volume is gone.

    R-8's third open item, and the reason it was open: every gate KTD21 publishes
    is library-scoped ON PURPOSE, so that a second machine contends with the first
    instead of holding an invisible lock of its own. The cost is that the lock,
    the acknowledgment and the session log all sit on the disk that died, so the
    ordinary restore refuses with "mount the library volume" and names a drive
    that no longer exists. Refusing honestly is not the same as serving the case.

    MOVING THE VOLUME ASSERTION ONTO THE TARGET DOES NOT FIX IT, and was not
    attempted. The refusal would simply move to the acknowledgment, which lives on
    the same dead volume, and the live case would lose a real check. What this
    does instead is substitute one gate at a time, and say what each substitute is
    worth:

    * the VOLUME assertion becomes two assertions, that the configured library is
      genuinely unreachable and that the target is a real filesystem rather than
      the stub an unmounted volume leaves behind. It is the strongest of the
      three substitutes and arguably stronger than the original, because it is
      the check that stops a recovery landing on the internal disk;
    * the ACKNOWLEDGMENT becomes an explicit decision by a named actor at a
      controlling terminal. It is WEAKER than the real gate and that is stated
      rather than papered over: the recorded acknowledgment R34 asks for lives on
      the dead volume, so there is no record to consult, and what remains is that
      an invocation with no terminal cannot proceed and the actor is derived from
      the process rather than supplied by it;
    * the LOCK becomes an installation-scoped one. Nothing is lost: with the
      library gone there is no shared volume for two machines to contend over, and
      the only contention that can exist is between processes here.

    THE ORDER IS THE SAME ORDER, and for the same reason. The two read-only
    assertions run before the one gate that creates a file, so a refused recovery
    leaves the disk exactly as it found it.
    """
    assert_library_volume_is_gone(
        cfg, identity_provider=identity_provider, mount_enumerator=mount_enumerator
    )
    where = assert_recovery_target(cfg, target, replacing_existing=replacing_existing)
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
        yield Held(
            workflow=BARE_METAL_WORKFLOW,
            lock=lock,
            intent=session.Intent.RECOVERY,
        )


__all__ = [
    "BARE_METAL_WORKFLOW",
    "CAPTURE_RESTORE_WORKFLOW",
    "DEFAULT_KEEP",
    "DEFAULT_MAX_AGE",
    "RECOVERY_LOCK_KEY",
    "Act",
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
    "bare_metal_session",
    "capture_root_of",
    "list_sessions",
    "plan",
    "prune",
    "recovery_lock_path",
    "recovery_session",
    "restorable_targets",
    "retention_plan",
    "run",
    "shares_the_database_volume",
]
