"""Which stored captures to keep, and the prune that deletes the rest (R30).

Part of :mod:`cratekit.core.restore`, which re-exports every name here; read them there. A
name of restore outside this file, every seam a test patches, and ``os`` and ``shutil``,
which a test patches on restore to sample the disk, are read through ``restore`` at call
time so a patch on restore bites here too (U300).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

from cratekit.core import (
    config,
    preflight,
    rb_writer,
    session,
    snapshot,
)
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import Remedy

#: The restore logger, so a record reads as it did before the split.
logger = logging.getLogger("cratekit.core.restore")


def _restore():
    """``restore`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import restore

    return restore


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
    for current, _directories, files in _restore().os.walk(root):
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
        _restore().shutil.rmtree(entry.root, ignore_errors=False)
        removed.append(entry.root)
        logger.info("pruned capture %s", entry.root.name)
    return tuple(removed)
