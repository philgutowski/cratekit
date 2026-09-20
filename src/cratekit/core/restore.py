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

**A DRY RUN AND A REAL RUN WALK ONE LIST, AND BOTH EVALUATE THE SAME
PREDICATES.** :func:`plan` produces an ordered tuple of :class:`Step` values,
:func:`run` checks every one of them against the disk, and only then does it
perform each step or not. There is no second code path for the preview, because a
preview built by a second code path is a report about a different program; and
there is no third mode in which the checks are skipped, because a rehearsal that
evaluated nothing its steps depend on was reporting on the loop rather than on the
restore.

**NOTHING IS DELETED THAT NOTHING ELSE HOLDS A COPY OF.** The live write-ahead log
holds transactions committed since the last checkpoint, which are in no capture
because every capture predates them, so it is moved aside rather than unlinked. A
directory being replaced is not removed until its replacement has landed, and the
copy a previous attempt left behind is adopted rather than deleted when it is the
only one left.

**A RESTORE THAT DID NOT FINISH SAYS SO.** A latch is written before the first
destructive step and retracted by the last one, so a process killed anywhere
between them leaves a library that refuses ordinary writes rather than one that
looks finished. It is written on every restore, including the ones whose window
produced nothing else to record, which is most of them.

WHAT A RESTORE CANNOT DO is undo anything that left the coupled set: audio on the
music volume, a playlist renamed at the provider, a file already in the Trash.
Those are enumerated, recorded, and refused over by ``core.reconcile``, and the
enumeration happens BEFORE anything is replaced, because afterwards the live
state IS the captured state and every comparison reports that nothing happened.

WHAT IT LEAVES SHORT, as opposed to what it cannot undo, is a database-native
tree whose cutover the capture predates, and that fact belongs to
``core.convergence`` rather than here. See :func:`_hand_tree_shortness_over` for
the argument. This module decides which trees, and hands them to the module that
gates them and that a rebuild clears.

LAYER: write, and the same exception the tree registry already takes. It lives
under ``core/`` because the pending register and the state inventory name it
there, and it is ranked with the write layer because it reads the tree registry
to decide which trees a pre-cutover restore leaves unconverged. Nothing below it
imports it. THE RANK IS BROADER THAN THE EXCEPTION IT IMPLEMENTS: it also grants
permission to import every ``cratekit.write.*`` module, and this one imports none
of them, which ``tests/test_layering.py`` asserts rather than leaves to good
intentions.
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

#: Where the live storage-engine companion files go when a restore takes them out
#: of the way. Beside the database, dotted, and declared by nothing in the state
#: inventory on purpose: these bytes are the ones no capture holds, so a directory
#: any capture or restore could reach is the wrong place for them.
PRE_RESTORE_DIR = ".cratekit-pre-restore"


# ---------------------------------------------------------------------------
# The residual findings this module's prose points at
# ---------------------------------------------------------------------------
#
# NAMED BY TITLE RATHER THAN BY NUMBER, and the number is deliberately absent.
# ``docs/residual-findings.md`` is a file every branch appends to, and the
# standing rule renumbers an entry when two of them reach for one number at a
# merge. A number written into source is therefore a reference that repoints
# SILENTLY: it still resolves, it still reads as a citation, and it now names
# somebody else's finding. That has already happened once in this repository,
# where ``core/convergence.py`` said "See R-15" and R-15 on the merged tree was a
# different finding entirely.
#
# Titles do not move under a renumber. ``tests/test_restore.py`` asserts that each
# of these still names a heading in that file, so a retitle goes red here rather
# than becoming a dangling citation, and the number lives in exactly one place.

#: The R30 sentence this unit computes and never renders. Owner U27.
RESIDUAL_CAPTURE_VOLUME_UNREPORTED = (
    "R30's second sentence is computed and never reported"
)

#: The bare-metal write path that closing the bypass removed, and that U95 put
#: back by deriving every path from the session. The entry is closed in place and
#: still cited, because it is where "what must NOT close it" is written down.
RESIDUAL_BARE_METAL_HAS_NO_WRITE_PATH = (
    "Closing the bare-metal bypass removed the bare-metal write path"
)


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


class Guard(StrEnum):
    """WHICH gate produced a :class:`Held`. Two guards, two different gate sets.

    The two are not interchangeable and a value carrying no answer to "which one
    made me" is a value nothing can tell apart. :func:`recovery_session` passes
    all three library-scoped gates against the configured library.
    :func:`bare_metal_session` passes SUBSTITUTES for those gates against a
    replacement drive, and its lock is installation-scoped. Both declare
    ``Intent.RECOVERY`` and both hold a lock this process really holds, so intent
    and lock membership cannot separate them.
    """

    #: All three library gates, against the configured library.
    LIBRARY_SESSION = "library-session"

    #: The substitutes, against a named replacement target. See
    #: :func:`bare_metal_session` for what each substitute is worth.
    BARE_METAL = "bare-metal-recovery"


#: What each live token was issued FOR: the guard that minted it, the directory it
#: authorises, and the lock it was taken against.
#:
#: A MEMBERSHIP TEST WAS NOT ENOUGH, and the gap it left is the original bypass one
#: line longer. ``Held`` is exported, is a plain frozen dataclass, and carries its
#: token in a public field, so inside a ``bare_metal_session`` a caller could read
#: the real token off the value the guard yielded and rebuild a ``Held`` around it
#: claiming a different guard and a different authorised directory. Every check
#: passed, because the only question being asked was whether that token was live.
#: Measured: the library database on the volume the identity gate had just refused
#: was rewritten with no acknowledgment. What the guard minted is therefore
#: recorded beside the token and compared, so a value may carry a live token and
#: still be refused for claiming something the guard never issued.
_ISSUED: dict[int, tuple[Guard, str, str]] = {}


@dataclass(frozen=True, slots=True)
class Held:
    """An OPEN destructive session, handed to everything the verb then does.

    ``guard`` (the METHOD) is one of the two reasons this type exists. The
    off-machine backup restore takes a zero-argument callable returning a context
    manager as its ``gates`` seam, and handing it that method rather than letting
    it default is what makes both halves of that restore run inside ONE
    acquisition. The context manager it returns does nothing, deliberately: the
    gates are already held by the block this value was yielded into, and taking
    them again in this process would be reported as a foreign holder, which is to
    say the caller would be told to wait for itself.

    ``issued_by`` and ``authorises`` are the other reason, and they were missing.
    A ``Held`` used to say only "some lock is held and the intent is recovery",
    which three separate compositions satisfied without any of the gates a person
    would assume. Measured end to end: with a configured library present and
    readable and an identity provider reporting a foreign volume,
    :func:`recovery_session` correctly refuses with ``library-volume-mismatch``;
    but :func:`bare_metal_session` against a replacement drive yields a ``Held``
    whose installation-scoped ``recovery.lock`` satisfies the same check, and
    :func:`plan` and :func:`run` then performed every step against
    ``cfg.library.root``, rewriting the database and the whole coupled tree on the
    volume the identity gate had just refused, with no acknowledgment, with the
    library lock held by a second process, while the target that
    :func:`assert_recovery_target` had validated received nothing. A ``Held``
    naming any unrelated lock this process happened to hold passed too.

    So a ``Held`` now says which guard issued it and WHAT IT AUTHORISES, and
    :func:`plan` and :func:`run` refuse one that does not authorise the path they
    are about to write. ``authorises`` is a directory: a bare-metal recovery
    authorises its validated target and nothing else, and a library session
    authorises the configured library root and nothing else.

    ``authorises`` IS ALSO WHERE THE PATHS COME FROM, which is what lets a
    bare-metal session be spent at all. See :func:`_rooted`.
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

        The distinction is the whole reason this is a property rather than a
        field. A ``Held`` is an ordinary value: it outlives the block that
        yielded it, and a caller who kept one and used it afterwards would be
        writing with no lock at all while every signature said otherwise.

        THREE QUESTIONS, because each alone is answerable by an accident. The
        session module's own record of what this process holds is the only
        non-stale answer about the LOCK, and it is the same set the lock
        acquisition maintains; but it is a set of paths, so any lock this process
        happens to hold satisfies it, including one taken for something else
        entirely. The token answers whether a guard in this module is still inside
        its own block. And the token's RECORDED TERMS answer the question a
        membership test cannot: whether this value claims what that guard actually
        issued, or whether somebody read a live token off a legitimate value and
        rebuilt a different claim around it.
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

        Compared on RESOLVED paths, because the hazard is a target that looks
        different and is the same directory, or looks the same and is not: a
        symlink, a relative spelling, or the empty folder an unmounted volume
        leaves behind at its own mount point.
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
        with _issued(
            workflow=workflow,
            lock=gates.lock,
            issued_by=Guard.LIBRARY_SESSION,
            authorises=Path(cfg.library.root),
            gates=gates,
            record=record,
        ) as held:
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
                # NO PLATFORM SEAMS ARE PASSED, and their absence is the point
                # rather than an omission. ``close_session`` asserts the volume
                # only on the path it gates, and a RECOVERY is exempt from that
                # gate for the reason it is exempt from every other latch here.
                # Forwarding them anyway said "this close is volume-asserted" to a
                # reader, which was not true on this path, and a seam that is
                # threaded but never reached is a seam somebody later trusts.
                intent=session.Intent.RECOVERY,
                now=now,
            )


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

    ONE PLACE MINTS THEM, so there is no second construction site that could
    forget the registration and hand back a value every assertion then treats as
    forged. The withdrawal is in a ``finally`` because the failure path is the one
    that matters: a guard that raised on its way out and left the token standing
    would leave a value that reports the gates open for the rest of the process.
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

    ONE SOURCE FOR ONE ANSWER. Both functions used to resolve every path from
    ``cfg.library.root`` and then ask whether the session authorised that root,
    which left a bare-metal session, whose whole point is that it authorises
    somewhere else, with no composition that reached a plan at all. The repair
    that was refused in advance is a ``target=`` parameter, because the two
    functions would then have to agree with the session about it, and a validated
    target that was then dropped is how the original bypass was built. So nothing
    is passed: the directory the guard minted into the ``Held`` is the directory
    the paths are derived from, and the authorisation check reads that same field.

    THIS IS THE ONLY PLACE THAT ASKS WHICH GUARD ISSUED THE SESSION. Everything
    downstream compares two roots, the configured one and the one this returns,
    and does nothing when they are equal, so there is one decision rather than
    one per helper that a later guard would have to be taught to each of.

    A LIBRARY SESSION GETS ``cfg`` BACK UNCHANGED, the same object. Its gates were
    passed against the configured library, so a configuration naming a different
    one is refused by the caller's assertion exactly as before rather than
    quietly re-aimed at the directory the session happens to authorise.

    A BARE-METAL SESSION GETS A COPY ROOTED AT ITS TARGET, and A RELOCATED ROOT
    CARRIES ITS DATABASE, which is the rule ``config._apply_env_overrides``
    already states for the same reason: what the configuration records is where
    the database sits RELATIVE to the library.

    A DATABASE THAT WAS NEVER UNDER THE CONFIGURED ROOT REFUSES HERE, by name and
    before anything is read. It is a supported layout, acknowledged at setup, so
    the refusal is this recovery's own rather than the defect-flavoured one the
    authorisation check would raise a few lines later: there is no relative
    position to carry that database to, and it sits outside the one directory
    this session authorises.

    Built with ``dataclasses.replace`` and never through ``config.from_dict``,
    which applies the environment's relocation override and would hand back a
    root that is neither the configured one nor the authorised one.
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

    A capture manifest and a session record both hold ABSOLUTE paths, written
    while the library sat at the configured root. After that disk has died and
    its contents have been brought back onto a replacement, every one of those
    paths still names the dead root, so a bare-metal plan that read them as
    written would either refuse every file as outside the restorable set or, far
    worse, write at the configured root after all. Same relative position, under
    the root :func:`_rooted` chose.

    TEXTUAL, AND BY THE RULE ``config`` ALREADY USES for the same question:
    ``normpath`` on both sides and a comparison of parts, with no ``resolve()``.
    Both spellings come from one configuration, resolving would make the answer
    depend on whether the dead root still exists as a stub, and a second rule
    here would disagree with validation about which databases are inside the
    library.

    THREE ANSWERS LEAVE THE PATH AS IT CAME. Equal roots, which is every library
    session. A path already under ``root``, so that re-basing is idempotent when
    the target is mounted inside the configured root and a path naming the target
    is lexically under both. And a path under neither, which on the write side
    then fails the restorable-set membership test and the authorisation check,
    and on the read side is a capture store somebody placed outside the library,
    which is still where it says it is.
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

    ALL FOUR FIELDS OR NONE. Re-basing the sources alone would aim the writes at
    the target while the reads still named the dead volume, and re-basing the
    captured paths alone would do the reverse, which is the original bypass with
    the capture pulled from the replacement.
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

    ``cfg`` is the ROOTED configuration. Three questions, and the first alone was
    all that used to be asked:

    * does the session AUTHORISE every step target;
    * is every step target a member of :func:`restorable_targets`, DERIVED again
      rather than trusted from plan time. Authorisation is a question about a
      directory, and the authorised directory ITSELF passes it, while replacing
      it would stage beside it, one level above anything the session was asked
      about;
    * is the staging directory an attempt directory directly under the ONE store
      the rooted configuration derives. It is not a step target, so the per-step
      check never covered it, and it is a write location twice over: every live
      companion is renamed into it, and the closing step PRUNES ITS PARENT. A
      staging directory that was merely somewhere inside the library would hand
      that prune the library's own parent, and it deletes directories.

    ASKED TWICE, in :func:`plan` and again in :func:`_preflight`. At plan time it
    makes "a plan cannot name a path outside its session" a property of every
    ``Plan`` value rather than of the run that may never happen, so a preview is
    refused as loudly as a write. At run time it is asked again because a plan is
    a value: one built under a session for one directory can be handed to ``run``
    under a session for another, and the rooted configuration is no defence there
    because the targets were fixed when the plan was built.
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

    ``RECORD`` first, because what a restore cannot undo has to be written down
    before the evidence for it is overwritten, and because the latch saying a
    restore is in flight is worth nothing if it is written after the first file is
    replaced. ``CLEAR`` before ``REPLACE``, because a companion log left beside a
    database that has started to change is a log the engine will replay onto the
    wrong file. ``MARK_TREES`` after the replacement rather than with the other
    recording, because the record that holds tree shortness is itself a COUPLED
    entry and is therefore one of the things being replaced: marking first would
    write the mark and then overwrite it. ``RESOLVE`` after that, because it is the
    claim that the condemning record has been answered, and a claim made before
    the work is a claim that can be wrong. ``RELEASE`` last of all, because it is
    the claim that the restore finished, and nothing else may outrank it.
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

    ``latch`` is the marker written before the first destructive step and
    retracted by the last one, so an interruption anywhere between them leaves a
    library that refuses ordinary writes instead of one that looks finished.

    ``pre_restore_root`` is where the live storage-engine companions are moved to
    rather than deleted. See :func:`_perform`.
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

    NOT called ``Outcome``. ``core.cause`` exports one already, a string enum of
    how a run ended, and this module imports from that same module. It follows
    the shape ``backup.BackupOutcome`` set for the same reason.
    """

    plan: Plan
    performed: tuple[Step, ...]
    dry_run: bool
    resolved: tuple[str, ...] = ()
    outstanding: tuple[str, ...] = ()
    outstanding_unreadable: str = ""

    @property
    def converged(self) -> bool:
        """Whether nothing is left open, which an UNKNOWN answer is not.

        A reconciliation record that could not be read after the restore landed
        reports False here, because "nobody could tell" and "nothing is
        outstanding" are the same value only if the permissive reading wins, and
        this is the one question this unit answers conservatively everywhere else.
        """
        return not self.outstanding and not self.outstanding_unreadable


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
    process_lister: Callable[[], Sequence[str]] | None = None,
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

    IT NAMES THE PATH IT IS PLANNING AGAINST. Every target below resolves from
    the configuration :func:`_rooted` returns and from nothing else, so ``cfg`` is
    rebound on the first line. The caller's spelling survives only as
    ``configured``, and only for its root, which is what recorded paths are
    re-based FROM. For a library session the rooted configuration is the
    caller's own, so a session opened against a different library is still
    refused here rather than discovered at the copy. For a bare-metal session it
    is a copy rooted at the validated target, which is what lets that session
    reach a plan at all, and every recorded path it reads is re-based the same
    way.

    AND IT CHECKS ITS OWN ANSWER. The assertion on the root is, for a bare-metal
    session, a statement about a value derived from the session, so it cannot be
    the check that catches a path escaping. :func:`_assert_plan_is_authorised`
    is: it asks the session about every location the finished plan writes at.

    REKORDBOX IS ASSERTED CLOSED HERE TOO, and the docstring on :func:`run` used
    to claim it while this function did not do it. Planning reads the live coupled
    state to decide what a restore cannot undo, so a library changing underneath
    the read produces a marker set about a library that no longer exists.
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
    # A capture that did not pass its integrity check is not a smaller recovery
    # point, it is the absence of one, and restoring FROM one would put a live
    # library behind a file nobody has established can be opened. Both halves are
    # asked: the recorded verdict AND whether the bytes it was about are still
    # there, because a store that lost a file after the verdict was written plans
    # and rehearses perfectly clean without the second question.
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

    # ALWAYS, never `if markers:`. Seven of the twelve coupled entries declare
    # RollbackEffect.NONE, so a restore whose window touched only those derives no
    # effect markers at all, and a capture taken after every cutover derives no
    # tree markers either. Emitting this step conditionally meant precisely those
    # restores wrote nothing anywhere before they began replacing files, so a hard
    # kill part way through left the database at one generation, the coupled state
    # at another, and the next ordinary destructive session allowed.
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
        # EFFECTS ONLY. The tree markers ride on ``tree_markers`` and are handed to
        # ``core.convergence``, which owns tree shortness; putting them here as
        # well would record one fact in two stores, and a rebuild clearing one
        # would leave the other standing. That is the duplication R-21 item 3
        # existed to close.
        markers=tuple(effects),
        tree_markers=trees,
        unconverged=unconverged,
        unverified_sessions=unverified,
    )


def _pre_restore_root(cfg: config.Config, *, now: datetime | None = None) -> Path:
    """Where a restore puts the live companion files it takes out of the way.

    Beside the database, so the move is a rename on one filesystem rather than a
    copy that can itself run out of room. Under a dotted directory that nothing in
    the state inventory declares, so no capture takes it and no restore replaces
    it: these bytes exist precisely because they are outside every capture.

    ONE DIRECTORY PER ATTEMPT, NOT PER LATCH, and the two are now different things.
    The latch keys on the capture so that repeating a restore collides with the
    row already there; the staged bytes must do the OPPOSITE, because the second
    attempt's log is not the first attempt's log and writing it over the top would
    destroy the very bytes this staging exists to keep. So it takes a fresh stamp,
    whose random tail makes two attempts inside one second distinct.
    """
    return (
        config.state_path(snapshot.DATABASE_KEY, cfg).parent
        / PRE_RESTORE_DIR
        / snapshot.new_stamp(now)
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

    THE WHOLE PLAN IS CHECKED BEFORE ANY OF IT IS PERFORMED, and that is what
    makes the rehearsal mean something. The previous shape evaluated three
    expressions and skipped everything a step depends on, because every dependency
    lived inside :func:`_perform`, which a rehearsal skips wholesale: a replacement
    whose source had been deleted rehearsed as every step performed with no
    refusal, and so did a target directory nobody could write to. The two modes now
    differ only in whether the loop that follows the checks does anything, so a
    rehearsal that passes is evidence the real run reaches its work. On the real
    run the same checks are the reason the first destructive step is not taken
    until the last one is known to be possible.

    EVERY PATH COMES FROM THE SESSION, as in :func:`plan` and through the same
    :func:`_rooted`. The latch, the tree markers, the resolved records and the
    retraction are all written through the rooted configuration, so under a
    bare-metal session they land on the target beside the files the steps put
    there, and never at the configured root.
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
    # Read on BOTH paths. What is outstanding is a fact about the library rather
    # than about this call, and a rehearsal that reported convergence because it
    # recorded nothing itself would be the preview lying about the world.
    #
    # AND READ DEFENSIVELY, because this runs AFTER everything has been performed.
    # A reconciliation document that is unreadable at this moment is a real problem
    # and it is not this restore's failure: raising here would report a completed
    # restore as failed and close its record ABANDONED, which is the opposite of
    # what happened and is the state a person then tries to recover from.
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

    Six questions, and each one is a failure the old rehearsal could not see:

    * does this session AUTHORISE every path the plan writes at, the staging
      directory included, which is the per-location half of the check
      :func:`assert_gates_are_open` makes once;
    * is the capture still whole, asked again rather than trusted from plan time,
      because a plan is a value that can be held across a store being pruned;
    * does every source a replacement reads still exist, and is it still the kind
      of thing the step expects;
    * can this account write at every destination, so a read-only directory
      refuses before the first companion is moved rather than after;
    * is every companion's resting name in the staging directory still free, so
      the attempt that would overwrite an earlier attempt's log refuses before it
      has moved any log at all;
    * is there room on the library volume for the whole copy, which nothing asked
      at all: the capacity refusal had exactly one call site, inside ``capture``.

    THE STAGING QUESTION LANDED HERE AFTER BEING ANSWERED ONLY ON THE PERFORMING
    PATH, and the round that put it there relocated the hole rather than closing
    it. :func:`_stage_companion_aside` is called once PER COMPANION, so with both
    companions live and the second one's resting name occupied, the first was
    already renamed out of the live tree when the second raised: the run aborted
    with the live write-ahead log gone and the database never replaced, which is
    exactly the half done state this staging exists to prevent. The rehearsal was
    worse than useless, because it reported all eight steps performed and refused
    nothing while the real run refused. Asked here, both modes answer the same
    way, which is the property that makes a rehearsal evidence about the run.

    ``cfg`` IS THE ROOTED CONFIGURATION and ``recorded_root`` is the library root
    the caller's configuration named, kept only because the manifest is read
    again here and its recorded paths are re-based from that root, exactly as
    :func:`plan` did.

    IT ALSO RE-DERIVES WHAT THE RESTORE DISCARDS. A plan is a value and a session
    can commit between building one and running it, so a plan built before that
    commit used to execute unchanged and destroy it, while a freshly built plan
    refused. The check that decides is the same one :func:`plan` made, asked again
    against the log as it stands now.
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

    THE MAXIMUM OF ONE STEP IS NOT THE ANSWER, AND ASSUMING IT WAS WAS A FALSE
    ACCEPTANCE. The reasoning that produced it is sound about a single
    replacement, which stages a copy beside its target and renames over it, so the
    old copy is freed before the next step begins. It is wrong about the plan,
    because two kinds of step GROW THE LIBRARY PERMANENTLY and every later step
    starts from that higher floor:

    * a ``CLEAR`` is a rename, not a delete. The live write-ahead log keeps its
      blocks under a new name forever, on purpose, because those bytes postdate
      every capture and this module is not entitled to decide they are worthless.
      The ``REPLACE`` that follows then writes the captured companion onto a
      target that no longer exists, so it frees nothing, and the captured
      companion's whole size is a permanent add;
    * any target that is not there live frees nothing when it is replaced, which
      is the ordinary shape of restoring onto a library that lost files.

    So the peak is the running total of what completed steps added, plus the
    transient of the step in flight, maximised over the plan. Four shapes were
    measured by sampling allocated bytes around every rename and copy, and the
    single-step rule was below the real peak on all four, by up to 7.4 MB; on a
    real 64 MiB volume squeezed to just above what it demanded, the preflight
    passed, the log was staged aside, the database was replaced, and the coupled
    copy died with ENOSPC, leaving the two halves at different generations.

    IT WALKS THE PLAN RATHER THAN THE MANIFEST, because the order is what makes
    the arithmetic true and only the plan has it. The plan is also what a caller
    was shown, so this is an estimate about the thing that is going to run.
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

    A DIRECTORY REPLACEMENT NEEDS BOTH ITS PARENT AND ITSELF, and each of the two
    previous versions of this check asked for exactly one of them.
    :func:`_replace_directory` stages a sibling and renames twice, so the staging
    writes all happen in the target's PARENT; that is the half the first version
    missed, and with it gone NOTHING refuses: the rehearsal reports every step
    performed, and the real run stages the log aside, replaces the database, and
    dies inside ``shutil.copytree`` into the unwritable parent, leaving the
    database at the new generation and the coupled state at the old. The other
    half is ``os.replace(target, previous)``, the first of those two renames, and
    it is the half the second version missed: the rehearsal reported all seven
    steps performed with no refusal and the real run died on that rename with the
    coupled state half replaced. So both are asked.

    NEITHER HALF IS COVERED BY ANY OTHER STEP, which is why both need their own
    test. The database's parent is ``<library>/db`` and the coupled directory's
    parent is ``<library>/<state>``; they are different directories, so the
    ordinary file steps say nothing at all about the second one.

    THE TARGET PROBE IS PLATFORM DEPENDENT, AND IS ASKED FOR THE STRICTEST
    PLATFORM. An earlier version of this docstring justified it by saying that
    renaming a directory rewrites that directory's own ``..`` entry. That is not a
    portable account of anything and it is not what was measured. What WAS
    measured: on darwin, renaming a directory whose own mode denies this account
    write fails with ``EACCES`` even though the parent is writable and the parent
    is the only thing changing; on Linux the same rename SUCCEEDS, because rename
    permission there is decided by the containing directories alone. So the probe
    is necessary on darwin and over restrictive on Linux, and asking it everywhere
    is deliberate: a rehearsal has to mean the same thing wherever it runs, the
    cost of the strict answer is a refusal that tells somebody to make their own
    library directory writable, and the cost of the loose one is a restore that
    stops with the coupled state half replaced.

    Each is asked of the nearest EXISTING ancestor, because a restore legitimately
    creates directories that are not there yet, and asking about a path that does
    not exist answers about nothing.
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

    AND SO IS WHAT THE SESSION AUTHORISES, which is the assertion that was
    missing. The three checks above are satisfied by every guard in this module,
    so they cannot tell a session that passed all three library gates against the
    configured library from one that passed weaker substitutes against a
    replacement drive. Composing the second and then planning against the first
    was a working bypass of all three library gates, verified end to end. Every
    call that is about to write therefore names the path, and a session that does
    not authorise that path refuses even though it is genuinely open.
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
        # The latch FIRST and in the same call as everything else it records, so
        # a process killed between the two would still have written the latch.
        #
        # ``decided.markers`` IS THE RECORDED SET AND NOTHING IS FILTERED OUT OF
        # IT HERE. It used to carry the tree markers too and this call subtracted
        # them by kind, because the transitional fallback wrote them into this
        # same store when ``core.convergence`` was not in the build. That module
        # is here now and owns tree shortness outright, so the plan no longer puts
        # tree markers in the recorded set at all: they live on
        # ``decided.tree_markers``, which the MARK_TREES step hands over. One fact,
        # one store, and no kind subtracted at the point of writing.
        reconcile.record_markers(cfg, (decided.latch, *decided.markers))
        return ()
    if step.act is Act.MARK_TREES:
        _hand_tree_shortness_over(cfg, decided, now=now)
        return ()
    if step.act is Act.RESOLVE:
        return _resolve_unverified(decided, cfg, now=now)
    if step.act is Act.RELEASE:
        # EVERY latch, not this plan's own. See reconcile.retract_in_flight: the
        # refusal these markers raise says an unfinished restore is closed by
        # finishing one, and retracting only this restore's row made that sentence
        # false for the restore that came after an interrupted one.
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
        # A RAW OSError CARRIES NOTHING. No reason, no remedy, no reserved exit
        # code, so a full volume, a permission error or a failing drive all arrive
        # at the process boundary as a bare traceback, at exactly the moment
        # somebody is already recovering from something. The in-flight latch is
        # still standing at this point and stays standing, which is the whole
        # point of writing it first.
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

    THE BOUND EXISTS BECAUSE THE STAGING IS DELIBERATELY UNBOUNDED IN THE OTHER
    DIRECTION. A staged log is never deleted by the restore that made it, because
    those bytes postdate every capture, and each attempt takes a fresh directory
    because the second attempt's log is not the first's. Both of those are right
    and together they grow without limit: four attempts leave four copies. That
    compounds with the capacity estimate, because every stranded log permanently
    occupies space on the volume being restored onto.

    PRUNED ONLY ON THE SUCCESS PATH, from the step that claims the restore
    finished. A failed attempt's log is the one most likely to be wanted, and
    pruning from a run that is about to fail would delete the evidence of the run
    before it.

    IT NEVER RAISES. This is housekeeping running after the work has landed, and
    nothing after the point of no return may fail a restore that succeeded.

    THAT IS A CLAIM ABOUT THE CALL SITE, and the call site is what makes it
    load bearing. :func:`_perform` calls this from the RELEASE branch, which is
    OUTSIDE the ``try`` that turns an ``OSError`` into a refusal, and by then
    ``reconcile.retract_in_flight`` has already discharged the latch. So an
    escaping error would arrive at the process boundary raw, with no reason, no
    remedy and no reserved exit code; :func:`run` would never return; and
    ``recovery_session`` would close the record ABANDONED for a restore that
    completed, which is the state a person then tries to recover from. That is
    exactly the defect fix round 2 closed one function away in
    :func:`_replace_directory`, and ``tests/test_restore.py`` covers this instance
    of it the same way that one is covered.
    """
    # ORDERED BY MODIFICATION TIME, not by name. The directory names are capture
    # stamps, whose second-resolution prefix is followed by a RANDOM tail, so
    # sorting them lexically is chronological only for attempts in different
    # seconds and is arbitrary for attempts inside one. Retention next door already
    # orders on the recorded time for the same reason.
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

    THE BYTES IN A WRITE-AHEAD LOG POSTDATE EVERY CAPTURE, WHICH IS WHY THEY ARE
    KEPT. The plan is: clear the log, clear the shared-memory index, replace the
    database. The clearing used to be ``unlink``, with no staging and no copy, and
    the log at that moment holds every transaction committed since the last
    checkpoint, none of which is in the main file and none of which is in ANY
    capture, because all of them predate it. Measured: with the capture's database
    missing, the plan built, the rehearsal reported all five steps performed and
    touched nothing, and the real run then unlinked the log and raised on the copy,
    leaving the database at its original generation with its log gone. Every
    transaction in it was unrecoverable from anywhere. The same window opens on a
    full volume, a permission error and an I/O error, which is the exact set of
    conditions under which people restore.

    A RENAME RATHER THAN A COPY, so it costs nothing and cannot itself run out of
    room, and it satisfies the ordering property just as well: what matters is that
    no log sits beside the database under the name the engine looks for while that
    database is changing, and a renamed file is not under that name.

    THE STAGED COPY IS NOT DELETED BY THE RESTORE THAT MADE IT. It is the only
    surviving record of work nobody can otherwise recover, so the restore that
    supersedes it is not entitled to decide it is worthless.

    AND A COLLISION IS REFUSED RATHER THAN LEFT TO THE STAMP'S WIDTH.
    :func:`_pre_restore_root` takes a fresh stamp per attempt with a 64-bit random
    tail, which makes two attempts landing on one directory vanishingly unlikely,
    but ``_mkdir_private`` returns silently when the directory is already there and
    ``os.replace`` overwrites, so the consequence of the unlikely event is the
    silent destruction of the one copy of transactions in no capture. The
    probability was the whole defence and the docstring used to read as though the
    rename were the whole answer. ``snapshot.capture`` refuses an occupied stamp
    for exactly this reason one module away, and the two sides now answer the same
    way: the staging side is per FILE rather than per directory, because one
    attempt legitimately stages several companions into one directory and only a
    name already taken means two attempts.

    THAT REFUSAL IS ASKED HERE AS A BACKSTOP AND IN :func:`_preflight` AS THE
    PRIMARY, and the difference is a whole restore. Asked only here, it fires
    while the loop is part way through the companions: with two companions live
    and the SECOND one's resting name occupied, the first was already renamed out
    of the live tree before this raised, which is the half done state the module
    docstring says the staging exists to prevent, and the rehearsal reported every
    step performed and refused nothing. A rehearsal that passes and a real run
    that refuses is the most misleading shape this module has. The preflight copy
    is the one that decides; this one exists because the directory can be occupied
    in the window between the two, and reaching it should be impossible.

    THE EARLY RETURN ASKS ``lexists``. A dangling symlink at the live companion's
    name is a name the storage engine will follow and create through, so it is a
    companion to be moved aside rather than an absence to skip; ``Path.exists``
    resolves the link and answers False, which read a taken name as a free one.
    """
    if not os.path.lexists(target):
        return
    _assert_staging_is_free(target, staging)
    config._mkdir_private(staging)
    os.replace(target, staging / target.name)


def _assert_staging_is_free(target: Path, staging: Path) -> None:
    """Refuse when an earlier attempt's companion already rests under this name.

    ASKED WITH ``lexists`` ON BOTH SIDES. ``Path.exists`` follows symlinks, so a
    broken link at the resting name answered False and the guard let the rename
    through, which replaced the link with the live log. The rule this enforces is
    that a name already TAKEN means two attempts, and a name holding a dangling
    link is taken. That is the absence-read-as-evidence-of-absence shape, and it
    is the same reason the caller's own early return asks ``lexists`` too.

    IT NAMES WHAT IS ALREADY IN THE STAGING DIRECTORY, not only the file it is
    refusing to move. On the performing path the occupants are what THIS run has
    already renamed out of the live tree, and a refusal that named only the file
    it declined to touch left a person with a live log missing and no sentence
    saying where it went.
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

    Never raises. This runs only to describe a refusal that is already decided, so
    an unreadable directory must not replace that refusal with a different one.
    """
    try:
        return tuple(sorted(entry.name for entry in staging.iterdir()))
    except OSError:
        return ()


#: Why a tree this restore left short is short, in the vocabulary the module that
#: OWNS tree shortness records reasons in. Named once here so the handoff and the
#: transitional fallback cannot describe the same fact two ways.
PRE_CUTOVER_RESTORE = "restore-predates-cutover"


def _hand_tree_shortness_over(
    cfg: config.Config, decided: Plan, *, now: datetime | None = None
) -> None:
    """Record that these trees need a rebuild, in the record that GATES that fact.

    ``core.convergence`` OWNS TREE SHORTNESS AND THIS MODULE DOES NOT. Both this
    unit and U36 discovered the same fact from opposite directions: a restore that
    lands on the far side of a tree's cutover leaves that tree short, and so does a
    database recovered out of band. Both wrote it down, in different stores, with
    different gates, different exemptions, different clearing calls and different
    refusal slugs, and neither module referenced the other. A rebuild cleared one
    flag and left the other standing, so every destructive session kept refusing
    after the remedy had been carried out correctly.

    WHY THE OTHER MODULE CANNOT SIMPLY DETECT THIS ITSELF, which its own docstring
    is right to say it does not. Its detection compares a fingerprint of the
    database's update count against one recorded at the last governed write, and
    that record is a COUPLED entry, so a Cratekit restore puts the database and
    the fingerprint back together and they agree by construction. That is exactly
    why it scopes itself to a database recovered out of band. The pre-cutover case
    is invisible from that side and visible from this one, because only this
    module holds both the live registry and the registry inside the capture. So
    the two halves are: this module DECIDES which trees, and that module HOLDS and
    GATES the answer. Neither can do the other's half.

    THE ARGUMENT FOR WHICH ONE OWNS IT. Not seniority and not who found it first.
    ``convergence`` has the better machinery for this specific fact on all four
    counts that matter. Its gate is PER TREE and sits inside the writer, so a short
    ``routing`` tree does not refuse a write to an unrelated one. Its exemption is
    ``Purpose.REBUILD``, declared at the call the remedy actually makes, so the
    latch cannot condemn its own remedy. Its clearing takes the convergence
    check's own list of differences and refuses a clear that is not backed by one,
    so a rebuild reporting success is the only thing that closes it, which is
    exactly the property this unit registered against U36 to protect. And its
    record is the one a rebuild already updates. Reproducing any of that here would
    be the second implementation of one rule that its own layering comment warns
    about, and the disagreement between two such implementations is a library that
    reports itself repaired while a tree is still missing membership.

    THE IMPORT IS AN ORDINARY ONE NOW, AND THE FALLBACK IT REPLACED IS GONE.
    ``core.convergence`` landed with U36 and both modules share this build, so the
    handoff is a call rather than a negotiation. While the two were apart this
    function resolved the import at call time through a private helper and, when
    the module was absent, recorded the fact in this unit's own store and latched
    it there with ``reconcile.assert_converged``, which gated rather than merely
    reporting. That was correct for a build holding one half of a handoff and is
    wrong for a build holding both: two stores holding one fact is exactly the
    disagreement the paragraph above argues against, and a rebuild clearing one of
    them would leave the other standing. The obligation to delete it was carried
    as R-21 item 3 and by an always-armed test that named the three deletions, and
    this is that deletion.
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

    THE SECOND ATTEMPT IS WHERE THIS USED TO LOSE EVERYTHING. The single failure
    is handled correctly by the shape above; what was not handled is running it
    again afterwards. This function began by removing both working names
    unconditionally, and after a crash between the two renames ``.replaced``
    holds the ONLY surviving copy of the live pre-restore state. A second run
    deleted it before copying anything, so a capture that then turned out to be
    unreadable, which is the shape a failing drive or an interrupted sync
    produces, left the live directory absent, the only copy of the old state
    gone, and a partial new one under ``.restoring``. The work the abandoned
    restore did, which is the only reason a person abandons one, existed nowhere.

    So ``.replaced`` IS ADOPTED RATHER THAN DELETED when it is the only copy left,
    and it is not deleted at all until the new directory has landed. ``.restoring``
    is still removed up front, because a partial copy from a dead attempt is
    worth nothing and its only alternative use is being mistaken for a whole one.
    """
    config._mkdir_private(target.parent)
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
    # THE SWAP HAS LANDED, SO NOTHING AFTER THIS POINT MAY FAIL THE RESTORE. The
    # old copy is tidy-up, and an unwritable subtree inside it, which is invisible
    # to a check that probes only the top of each target, used to raise here: the
    # new directory was correct on disk, every earlier step had succeeded, and the
    # restore reported ``restore-step-failed`` and never reached the step that
    # retracts its own latch. A correct restore that latches the library
    # permanently is a worse outcome than a directory left behind, so this leaves
    # the directory behind and says where it is.
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

#: How many captures survive on count alone. Five is what the guarded writer
#: already defaults to, carried rather than re-chosen so two answers to one
#: question cannot exist.
DEFAULT_KEEP = 5

#: How old a capture may be before count stops protecting it. A month is long
#: enough to cover a person who works in bursts and short enough that a library
#: does not silently accumulate a year of database copies.
DEFAULT_MAX_AGE = timedelta(days=30)

#: How many attempts' worth of staged companion files survive.
#:
#: THE DEFAULT RETENTION COUNT, carried rather than re-chosen, so the number is
#: written down in exactly one place: :data:`DEFAULT_KEEP`, which is also
#: ``RetentionPolicy.keep``'s default.
#:
#: IT IS NOT "WHATEVER THE CAPTURE STORE KEEPS ON THIS RUN", and an earlier
#: version of this comment claimed it was. :func:`retention_plan` takes a
#: ``policy`` per call, so a caller passing ``RetentionPolicy(keep=20)`` gets
#: twenty captures and still five staged attempts, and the claim that two answers
#: to one question cannot exist was simply false against that signature.
#:
#: THEY ARE TWO QUESTIONS, WHICH IS WHY THE ASYMMETRY STAYS. A policy argument
#: answers "how many captures should this run keep". The prune runs inside
#: :func:`_perform` at the RELEASE step of a restore, where there is no policy in
#: scope and no caller in a position to supply one, and threading one through
#: would mean an argument to the retention verb silently decided how much
#: unrecoverable write-ahead log a later restore throws away. What the two do
#: share is the default, and that is what this line says and all it says.
#:
#: THAT ARGUMENT WAS PUT AS A DICHOTOMY AND THERE ARE THREE OPTIONS. It offered
#: two: thread a policy down to the RELEASE step, or correct this comment. The
#: first is genuinely out of scope, confirmed rather than asserted: :func:`run`
#: takes no policy, :class:`Plan` carries no policy field, and
#: :class:`RetentionPolicy` is constructed in exactly one place and is never
#: persisted. The third option is to move the count into ``core.config`` as a
#: configured value, at which point both sides READ one persisted number and the
#: "one answer to one question" claim becomes true with no coupling at all. It is
#: not taken here because it is a configuration surface this unit did not ship,
#: and it is written down because a decline argued from an option set that is
#: missing its best member is a decline the next reader cannot check.
#:
#: ``tests/test_restore.py`` pins this and :data:`DEFAULT_KEEP` by consequence
#: with LITERAL expected values. Writing the constant into its own expected value
#: is an assertion that passes at every value the constant can take, which is how
#: a silent change from five to one used to leave four attempts' worth of
#: write-ahead log deleted with the suite green.
KEEP_STAGED_ATTEMPTS = DEFAULT_KEEP


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

    "REPORTED" IS AN OVERSTATEMENT OF WHAT LANDED, AND THE GAP IS RECORDED.
    This function computes the answer and ``RetentionPlan`` carries it, and
    nothing in ``src/`` renders it: there is no command-line surface, no doctor
    check, and no session-time warning, so a user is never told. The honest status
    is COMPUTED, NOT REPORTED, and it is written down in
    ``docs/residual-findings.md`` under the title named by
    :data:`RESIDUAL_CAPTURE_VOLUME_UNREPORTED`, with an owner, because an
    obligation carried only by a docstring on a closing unit is owned by nobody
    the moment that unit closes, which is the argument this unit makes twice in
    ``tests/_pending.py`` about somebody else's markers.
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

    ``owning=None`` DOES NOT SKIP THE CHECK, it widens it. The guard used to be
    opt-in, and the default was to opt out, so the one call shape that took no
    argument at all, which is the easy one to write, was the one that checked
    nothing. With nothing named, the log itself is asked, and any session that has
    not reached a terminal state refuses: pruning is never urgent, and a capture
    kept one run too long costs disk while a capture deleted one run too early
    costs the only undo an unfinished run has.

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


#: Answers "is this directory the root of its own filesystem". A SEAM, for the
#: same reason ``preflight.IdentityProvider`` and ``session.has_controlling_terminal``
#: are: the real answer depends on a mounted volume, and a battery that needed one
#: could not drive this refusal at all. The default is the real probe and the
#: substitute is supplied per call rather than set globally.
#:
#: IT IS A REAL SOFTENING PATH AND THE DECISION TO KEEP IT IS DELIBERATE, so it is
#: stated rather than left for somebody to find. Passing a probe that always
#: answers yes disables the strongest of the three substitutes a bare-metal
#: recovery makes, which is the check that stops a whole library being written onto
#: the internal disk. Nothing in ``src/`` passes one. The battery does, for every
#: bare-metal test, because a temporary directory is a mount point on no platform
#: and without it the refusals under test are unreachable; each stub test then
#: answers no to drive the refusal directly. What keeps the default honest is
#: ``test_round2_the_real_mount_probe_is_armed_by_default``, which supplies nothing
#: and asserts the real probe still refuses a stub. The alternative considered and
#: rejected was making the tests run against a real mount point, which needs a disk
#: image and a mount, and would make the one refusal that protects a boot disk the
#: only refusal in this unit with no coverage at all.
MountProbe = Callable[[Path], bool]


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
    cfg: config.Config,
    target: Path | str,
    *,
    replacing_existing: bool = False,
    mount_probe: MountProbe | None = None,
) -> Path:
    """Refuse a bare-metal target that is not one. Reads only; creates nothing.

    THE STUB CHECK COVERS TWO SHAPES, NOT ONE. It used to fire only when the target
    resolved EXACTLY to ``cfg.library.root``, and both of the near misses are the
    internal disk. A SUBDIRECTORY of the configured root passes an equality test
    and is the same empty folder one level down. And an operating system that finds
    a volume's mount point occupied mounts it beside the original under a
    suffixed name, so the stale stub and the live volume sit next to each other
    with names one character apart; naming the stub passes an equality test too.
    Both are answered on the filesystem identifier rather than on the path, because
    the whole hazard is a path that looks right.
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
    # RECURSIVE. The non-recursive form missed a target holding a library whose
    # database is in a subdirectory, which is the layout the containment rule
    # produces and the layout this unit's own fixtures use, so the check passed on
    # precisely the arrangement it exists to catch.
    existing = sorted(entry for entry in where.rglob("*.db") if entry.is_file())
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

    THE SESSION THIS YIELDS IS SPENT THROUGH :func:`plan` AND :func:`run`, WHICH
    DERIVE EVERY PATH FROM IT. For a while nothing could spend it at all: a
    verified bypass, in which this function's session was spent on the library the
    identity gate had just refused, was closed by having both functions refuse a
    session that did not authorise ``cfg.library.root``, and since this session
    never does, the write path went with the bypass. That history, and the two
    repairs refused in advance, are in ``docs/residual-findings.md`` under the
    title named by :data:`RESIDUAL_BARE_METAL_HAS_NO_WRITE_PATH`. Both functions
    now root their configuration at ``Held.authorises`` through :func:`_rooted`,
    so the target validated here is the only place a path can come from.

    WHAT IS STILL MISSING IS A CALLER. No shipped verb composes this session with
    a plan, and nothing here brings the dead library's contents onto the target,
    so the session log and the capture a plan reads must already be there.

    AND THE LOCK ARGUMENT ABOVE PREDATES THE WRITE PATH. "Nothing is lost" was
    written when this session could write nothing. A target that already holds a
    recovered library holds that library's own lock, which this does not take.
    The ledger records it, owned by whichever unit writes the first caller.
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
        # THE TARGET RIDES ON THE VALUE. It used to be validated here and then
        # dropped, so the ``Held`` this yielded authorised nothing in particular
        # and ``plan`` and ``run`` resolved every path from ``cfg.library.root``
        # instead: the drive this function had just refused. Carrying it is what
        # makes the validation mean something downstream.
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
