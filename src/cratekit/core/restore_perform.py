"""Performing a restore plan: staging companions aside and replacing files and directories.

Part of :mod:`cratekit.core.restore`, which re-exports every name here; read them there. A
name of restore outside this file, every seam a test patches, and ``os`` and ``shutil``,
which a test patches on restore to sample the disk, are read through ``restore`` at call
time so a patch on restore bites here too (U300).
"""

from __future__ import annotations

import logging
import tempfile
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from cratekit.core import (
    config,
    convergence,
    reconcile,
    session,
)
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy

if TYPE_CHECKING:
    from cratekit.core.restore import Plan, Step


#: The restore logger, so a record reads as it did before the split.
logger = logging.getLogger("cratekit.core.restore")


def _restore():
    """``restore`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import restore

    return restore


def _perform(
    step: Step, decided: Plan, cfg: config.Config, *, now: datetime | None = None
) -> tuple[str, ...]:
    """Do one step. Returns the session identifiers it resolved, usually none.

    The parameter is ``decided``, not ``plan``, so it never shadows :func:`plan`.
    """
    if step.act is _restore().Act.RECORD:
        # The latch FIRST, in the same call as the effect markers. Tree markers
        # are not here; MARK_TREES hands them to ``core.convergence``.
        reconcile.record_markers(cfg, (decided.latch, *decided.markers))
        return ()
    if step.act is _restore().Act.MARK_TREES:
        _hand_tree_shortness_over(cfg, decided, now=now)
        return ()
    if step.act is _restore().Act.RESOLVE:
        return _resolve_unverified(decided, cfg, now=now)
    if step.act is _restore().Act.RELEASE:
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
        if step.act is _restore().Act.CLEAR:
            _restore()._stage_companion_aside(step.target, decided.pre_restore_root)
            return ()
        if step.act is _restore().Act.REMOVE:
            _remove(step.target)
            return ()
        if step.source is None:  # pragma: no cover - a replacement always has a source
            raise refuse(
                "internal-error",
                f"the step {step.act} on {step.target} carries no source",
                remedy=Remedy.REPORT_DEFECT,
                detail={"act": str(step.act), "target": str(step.target)},
            )
        if step.act is _restore().Act.REPLACE_TREE:
            _replace_directory(step.source, step.target)
        else:
            _restore()._replace_file(step.source, step.target)
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
    for stale in attempts[: max(len(attempts) - _restore().KEEP_STAGED_ATTEMPTS, 0)]:
        try:
            _restore().shutil.rmtree(stale)
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
    if not _restore().os.path.lexists(target):
        return
    _assert_staging_is_free(target, staging)
    config.mkdir_private(staging)
    _restore().os.replace(target, staging / target.name)


def _assert_staging_is_free(target: Path, staging: Path) -> None:
    """Refuse when an earlier attempt's companion already rests under this name.

    Asked with ``lexists`` on both sides, since a dangling link is a taken name.
    The refusal names what the staging directory already holds, so a person can
    find a log this run has already moved.
    """
    if not _restore().os.path.lexists(target):
        return
    resting = staging / target.name
    if not _restore().os.path.lexists(resting):
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
        _restore().shutil.rmtree(target)
        return
    target.unlink(missing_ok=True)


def _replace_file(source: Path, target: Path) -> None:
    """Copy into place through a temporary name in the TARGET's directory.

    Beside the target so the rename is atomic on one filesystem and an
    interruption never leaves a half-written database.
    """
    config.mkdir_private(target.parent)
    descriptor, temporary = tempfile.mkstemp(dir=str(target.parent), suffix=".tmp")
    _restore().os.close(descriptor)
    staged = Path(temporary)
    try:
        _restore().shutil.copyfile(source, staged)
        _restore().shutil.copystat(source, staged)
        _restore().os.replace(staged, target)
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
        _restore().os.replace(previous, target)
    _remove(staged)
    try:
        _restore().shutil.copytree(source, staged)
    except BaseException:
        _remove(staged)
        raise
    if target.exists():
        _remove(previous)
        _restore().os.replace(target, previous)
    _restore().os.replace(staged, target)
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
