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
second path reports on a different program. The files' half is the one write not
in that list: a dry run checks each of its files is there and readable, and a
write a file then refuses is found only by the real run.

**NOTHING IS DELETED THAT NOTHING ELSE HOLDS A COPY OF.** The live write-ahead log
is moved aside, a replaced directory is removed only after its replacement lands,
and a previous attempt's only copy is adopted.

**A RESTORE THAT DID NOT FINISH SAYS SO.** A latch written before the first
destructive step and retracted by the last makes a killed restore refuse writes.

What left the coupled set (audio, provider renames, the Trash) is enumerated by
``core.reconcile`` BEFORE anything is replaced, since afterwards every comparison
reports nothing. A pre-cutover tree is handed to ``core.convergence``
(:func:`_hand_tree_shortness_over`).

Three parts hold the rest, each name a caller reads re-exported here (U300): the
performing steps (``restore_perform``), retention and the prune (``restore_retention``, which cites
:data:`RESIDUAL_CAPTURE_VOLUME_UNREPORTED`), and bare-metal recovery
(``restore_recovery``, which cites :data:`RESIDUAL_BARE_METAL_HAS_NO_WRITE_PATH`).
A fourth, ``restore_tags``, is the files' half (R-1924): the title tag and key
tag a session kept before it wrote them, read at the plan and put back by
:func:`run` after the database half lands and before the latch is retracted.
It is the one write outside the coupled set, and the plan's ``file_tags``.

LAYER: write, the tree registry's exception, because it reads that registry; it
imports no ``cratekit.write.*`` module, which ``tests/test_layering.py`` asserts.
"""

from __future__ import annotations

import logging
import os
import shutil  # noqa: F401 - its parts read restore.shutil at call time, which a test patches
from contextlib import AbstractContextManager, contextmanager, nullcontext
from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.core import (
    config,
    preflight,
    processes,
    reconcile,
    restore_tags,
    session,
    snapshot,
    tree_registry,
)
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.restore_perform import PRE_CUTOVER_RESTORE as PRE_CUTOVER_RESTORE
from cratekit.core.restore_perform import _assert_staging_is_free as _assert_staging_is_free
from cratekit.core.restore_perform import _perform as _perform
from cratekit.core.restore_perform import _replace_directory as _replace_directory
from cratekit.core.restore_perform import _replace_file as _replace_file
from cratekit.core.restore_perform import _stage_companion_aside as _stage_companion_aside
from cratekit.core.restore_recovery import _is_mount_point as _is_mount_point
from cratekit.core.restore_recovery import _refuse_target as _refuse_target
from cratekit.core.restore_recovery import bare_metal_session as bare_metal_session
from cratekit.core.restore_recovery import recovered_database_fileset as recovered_database_fileset
from cratekit.core.restore_recovery import recovery_lock_path as recovery_lock_path
from cratekit.core.restore_retention import KEEP_STAGED_ATTEMPTS as KEEP_STAGED_ATTEMPTS
from cratekit.core.restore_retention import RetentionPolicy as RetentionPolicy
from cratekit.core.restore_retention import prune as prune
from cratekit.core.restore_retention import retention_plan as retention_plan

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


def _defect(message: str, *, detail: Mapping[str, object]) -> CratekitError:
    """A refusal that only a defect in this build can reach, reported as one."""
    return refuse("internal-error", message, remedy=Remedy.REPORT_DEFECT, detail=detail)


def _refuse_run(reason: str, message: str, **terms: object) -> CratekitError:
    """A refusal scoped to this restore's run, as every restore step's refusal is."""
    return refuse(reason, message, scope=Scope.RUN, origin=("restore",), **terms)


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
        else:
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


def _spendable_capture(root: Path, recorded_root: Path, rooted_at: Path) -> snapshot.Capture:
    """The capture at ``root``, re-based onto ``rooted_at``, or a refusal to spend it.

    An unverified capture is no recovery point. Both the verdict and the bytes'
    presence are asked, since a file can vanish after the verdict.
    """
    captured = _rebased_capture(snapshot.read_manifest(root), recorded_root, rooted_at)
    snapshot.assert_verified(captured)
    snapshot.assert_sources_present(captured)
    return captured


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
            raise _defect(
                f"the plan would {step.act} at {step.target}, which is not a path "
                f"any restore of {cfg.library.root} may replace",
                detail={"act": str(step.act), "target": str(step.target)},
            )
    assert_gates_are_open(held, writing=pre_restore_root)
    store = _pre_restore_root(cfg).parent
    if pre_restore_root.parent != store:
        raise _defect(
            f"the plan stages live companion files under {pre_restore_root}, which "
            f"is not an attempt directory under {store}; the restore prunes the "
            f"directory above its staging, so that has to be the one store this "
            f"library derives",
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
    #: Each file's title tag and key tag before the restored session and every
    #: session it discards wrote them, put back after the database (R-1924).
    file_tags: tuple[restore_tags.FileBefore, ...] = ()


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
    #: What the files' half did; a dry run plans its files and writes none.
    file_tags: restore_tags.TagsPutBack = field(default_factory=restore_tags.TagsPutBack)

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
    return snapshot.captured_paths(cfg)


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
        raise _defect(
            f"session {session_id} recorded no capture, so there is nothing to "
            f"restore it from",
            detail={"session_id": session_id},
        )
    recorded_root, rooted_at = Path(configured.library.root), Path(cfg.library.root)
    root = capture_root_of(_rebased(record.snapshot_path, recorded_root, rooted_at))
    captured = _spendable_capture(root, recorded_root, rooted_at)

    later = _later_committed(cfg, record)
    _assert_override_names_them(record, later, discarding)
    # READ BEFORE ANYTHING IS REPLACED, so a record kept in a form this build
    # cannot read refuses here and never after the rows went back (R-1924). The
    # restored session first: the files go back to before the earliest it undoes.
    # EVERY LATER SESSION, NOT ONLY THOSE THAT COMMITTED: a session that wrote
    # files and no rows, or stopped between the two, holds the only true before
    # values, and a commit is no evidence about files (review round one, B1).
    file_tags = restore_tags.befores(
        (record, *_later_started(cfg, record)),
        rebased=lambda path: _rebased(path, recorded_root, rooted_at),
    )

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
        file_tags=file_tags,
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


def _later_started(
    cfg: config.Config, target: session.SessionRecord
) -> tuple[session.SessionRecord, ...]:
    """Every session that started after the one being restored to, whatever its
    state, by recorded start: what the files' half reads (R-1924)."""
    return tuple(
        sorted(
            (
                entry
                for entry in session.records(cfg)
                if entry.session_id != target.session_id and entry.started > target.started
            ),
            key=lambda entry: (entry.started, entry.session_id),
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
    raise _refuse_run(
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
            raise _defect(
                f"the capture manifest names {entry.source}, which is not a path "
                f"any restore may replace; refusing rather than restoring the "
                f"subset this build happens to recognise",
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
    files = restore_tags.TagsPutBack(planned=len(decided.file_tags))
    for step in decided.steps:
        if step.act is Act.RELEASE:
            # THE FILES AFTER THE DATABASE HALF LANDED AND BEFORE THE LATCH IS
            # RETRACTED (R-1924), so a restore stopped among the files still says
            # it did not finish. Nothing in the put back raises for one file, so a
            # finished restore is never closed abandoned for it. A dry run checks
            # each file is there and readable, and writes none.
            files = restore_tags.put_back(decided.file_tags, dry_run=dry_run)
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
        file_tags=files,
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

    _spendable_capture(decided.capture_root, recorded_root, Path(cfg.library.root))

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
        raise _no_source(step)
    wanted_directory = step.act is Act.REPLACE_TREE
    if source.is_dir() if wanted_directory else source.is_file():
        return
    raise _refuse_run(
        "snapshot-integrity-failed",
        f"the restore would put {source} at {step.target} and that source is "
        + ("not a directory" if wanted_directory else "not a file that exists")
        + "; refusing before anything is replaced rather than part way through",
        remedy=Remedy.REPORT_DEFECT,
        detail={"act": str(step.act), "source": str(source), "target": str(step.target)},
    )


def _no_source(step: Step) -> CratekitError:
    """The refusal for a replacement step that carries no source, a defect."""
    return _defect(
        f"the step {step.act} on {step.target} carries no source",
        detail={"act": str(step.act), "target": str(step.target)},
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
    probe = snapshot.nearest_existing(wanted)
    writable = probe if probe.is_dir() else probe.parent
    if os.access(writable, os.W_OK):
        return
    raise _refuse_run(
        "restore-step-failed",
        f"{writable} is not writable by this account, so the restore would stop "
        f"at {step.target} after having already replaced everything before it",
        steps=(
            "make the library's directories writable by this account, then run "
            "this again",
        ),
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
        raise _defect(
            f"a restore was handed a {held.intent} session; a restore declares "
            f"itself a recovery, because the latches it answers would otherwise "
            f"refuse it",
            detail={"workflow": held.workflow, "intent": str(held.intent)},
        )
    if not held.still_open:
        raise _defect(
            f"the destructive-session gates for {held.workflow} are not held by "
            f"this process, so this call would plan or write with the library lock "
            f"released and every other process free to commit underneath it; a "
            f"session value that was never issued by one of this module's own "
            f"guards reports the same thing, and for the same reason",
            detail={"workflow": held.workflow, "lock": str(held.lock)},
        )
    if writing is None or held.authorises_path(writing):
        return
    raise _defect(
        f"the {held.issued_by} session open here authorises {held.authorises} and "
        f"this call would write at {writing}; the gates a session passed are gates "
        f"about a particular library, so spending one against a different one "
        f"would replace a database behind checks that were never asked of it",
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

