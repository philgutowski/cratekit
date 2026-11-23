"""What a restore could not undo, and the refusal that stands until somebody says.

A KTD21b restore makes the database and its coupled state agree with each
other, not with the world: downloaded audio stays on the volume, a playlist
renamed at the provider stays renamed, and a tombstoned file stays in the
Trash. This module names each one and refuses every further destructive
session until a person disposes of it, surviving process, machine and restore.

The marker set is DERIVED from ``config.RollbackEffect`` on the inventory
(P4). Every read then write cycle holds a sibling lock in its own
NEVER_RESTORED entry, so a restore cannot swap its inode. The reader
recognizes the document positively and refuses everything else, since an
empty store would read as "nothing outstanding".

Tree shortness is owned by ``core.convergence``, and ``core.restore`` hands
trees there, but a tree marker found here still latches (see
:func:`assert_converged`).

LAYER: infrastructure, carrying remediation TOKENS and steps (D2). It imports
neither the tree registry nor ``core.convergence``, both ranked above it.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence

from cratekit.cli.output import timestamp
from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy

logger = logging.getLogger(__name__)

#: The state entry holding the record.
STATE_KEY = "restore_reconciliation"

#: Its sibling lock, in an entry of its own.
LOCK_KEY = "restore_reconciliation_lock"

#: Bumped only on an incompatible change; a later document is refused, not guessed.
SCHEMA_VERSION = 1


class Kind(StrEnum):
    """The three things a restore leaves behind, which are not the same thing.

    An EFFECT happened outside the coupled set and a person disposes of it. An
    IN-FLIGHT RESTORE is written before the first destructive step and retracted
    on completion, so a killed restore still refuses. An UNCONVERGED TREE is
    closed only by a rebuild, never a sentence (R39); its owner is now
    ``core.convergence``, and an old marker still latches.
    """

    EFFECT = "effect"
    IN_FLIGHT_RESTORE = "in-flight-restore"
    UNCONVERGED_TREE = "unconverged-tree"


class Disposition(StrEnum):
    """What a person decided about one marker.

    ``ACCEPTED`` and ``REPAIRED`` both close it and are kept apart for later
    readers. Not ``Verdict``, which ``core.review`` already exports with a
    clashing member spelling.
    """

    ACCEPTED = "accepted"
    REPAIRED = "repaired"


@dataclass(frozen=True, slots=True)
class Marker:
    """One thing a restore could not undo, addressable and persisted.

    ``identity`` is a stable identifier, never a display name (R19, D5).
    ``marker_id`` is composed from kind, identity, effect AND THE RESTORE THAT
    OBSERVED IT, so recording twice for one restore is idempotent while a later
    restore is never swallowed by an earlier closed record. An unattributed
    marker keys on ``-`` and still collapses.
    """

    kind: Kind
    identity: str
    effect: config.RollbackEffect | None = None
    session_id: str | None = None
    capture_stamp: str | None = None
    detail: str = ""
    observed: str = ""

    @property
    def marker_id(self) -> str:
        effect = str(self.effect) if self.effect is not None else "-"
        session_id = self.session_id or "-"
        stamp = self.capture_stamp or "-"
        return f"{self.kind}:{self.identity}:{effect}:{session_id}:{stamp}"

    def to_json(self) -> dict[str, Any]:
        return {
            "marker_id": self.marker_id,
            "kind": str(self.kind),
            "identity": self.identity,
            "effect": str(self.effect) if self.effect is not None else None,
            "session_id": self.session_id,
            "capture_stamp": self.capture_stamp,
            "detail": self.detail,
            "observed": self.observed,
        }


@dataclass(frozen=True, slots=True)
class Record:
    """One marker plus the disposition closing it, or no disposition at all."""

    marker: Marker
    disposition: Disposition | None = None
    actor: str | None = None
    decided: str | None = None
    note: str = ""

    @property
    def outstanding(self) -> bool:
        return self.disposition is None

    def to_json(self) -> dict[str, Any]:
        return {
            **self.marker.to_json(),
            "disposition": str(self.disposition) if self.disposition is not None else None,
            "actor": self.actor,
            "decided": self.decided,
            "note": self.note,
        }


def path_for(cfg: config.Config) -> Path:
    """Where the record lives, resolved through the declared state inventory."""
    return config.state_path(STATE_KEY, cfg)


def lock_path(cfg: config.Config) -> Path:
    """The sibling lock, resolved the same way and living somewhere else.

    It is NEVER_RESTORED and the record SURVIVES_ROLLBACK, so they land in
    different directories and a restore cannot swap the lock's inode (U11).
    """
    return config.state_path(LOCK_KEY, cfg)


def _unusable(cfg: config.Config, what: str) -> CratekitError:
    """One refusal for every way this document is not this document."""
    return refuse(
        "restore-record-unusable",
        f"the restore reconciliation record at {path_for(cfg).name} could not be "
        f"read ({what}), so what a restore left outstanding is unknown; treating "
        f"it as empty would report this library converged on the strength of a "
        f"file nobody could parse",
        steps=(
            "repair or restore the reconciliation record before running anything "
            "that writes to this library",
        ),
        scope=Scope.RUN,
        origin=("reconcile",),
        detail={"path": str(path_for(cfg)), "problem": what},
    )


def _assert_library_is_readable(cfg: config.Config) -> None:
    """Refuse a READ when the library this record belongs to is not there at all.

    A missing file on a missing volume is not an empty store. An empty mount
    point cannot be told from a fresh install here (P7), so the volume is
    asserted upstream by ``session.assert_gates`` and ``session.close_session``.
    """
    root = Path(cfg.library.root)
    if not root.is_dir():
        raise _unusable(
            cfg, f"the library at {root} is not there, so its state cannot be read"
        )


def _assert_library_is_writable(cfg: config.Config) -> None:
    """Refuse a WRITE when the library is the husk an unmounted volume leaves.

    Stricter than the read, because a write creates its directory. It needs the
    state directory or the configured database; a husk has neither.
    """
    _assert_library_is_readable(cfg)
    if config.library_state_dir(cfg).is_dir():
        return
    if Path(cfg.library.db_path).exists():
        return
    raise _unusable(
        cfg,
        f"the directory at {cfg.library.root} holds neither this installation's "
        f"state nor the database the configuration names, so it is the empty folder "
        f"an unmounted volume leaves behind rather than a library with nothing "
        f"recorded yet; writing here would rebuild the state tree on whichever disk "
        f"that path now sits on",
    )


def _own_only(target: Path) -> None:
    """Set the lock file's mode, passing over a filesystem that will not take one."""
    if hasattr(os, "chmod"):
        try:
            os.chmod(target, config.PRIVATE_FILE_MODE)
        except OSError as exc:
            logger.debug("could not set the mode on %s: %s", target, exc)


@contextmanager
def _locked(cfg: config.Config) -> Iterator[None]:
    """Hold the sibling lock across one read then write cycle.

    Blocking. The lock file persists after release, since unlinking it lets
    two processes hold locks on different inodes. A platform with no advisory
    locking refuses.
    """
    # Before the directory is created, or a gone volume's state tree is rebuilt.
    _assert_library_is_writable(cfg)
    target = lock_path(cfg)
    config.mkdir_private(target.parent)
    try:
        handle = config.flock_exclusive(target, _own_only)
    except (ImportError, OSError) as exc:
        raise refuse(
            "restore-record-unusable",
            f"the restore reconciliation record could not be locked ({exc}), and "
            f"writing it unlocked loses whatever a second process is writing at "
            f"the same time, silently, while reporting success",
            steps=("make the library's state directory writable by this account",),
            scope=Scope.RUN,
            origin=("reconcile",),
            detail={"lock": str(target)},
        ) from exc
    try:
        yield
    finally:
        handle.close()


def _recognize(cfg: config.Config, raw: Any) -> dict[str, Record]:
    """Turn a parsed document into records, or refuse. Positively, field by field.

    An empty result for good JSON that is not this record would be written back
    and delete every prior marker.
    """
    if not isinstance(raw, Mapping):
        raise _unusable(cfg, f"the document is a {type(raw).__name__}, not a record")
    version = raw.get("schema_version")
    if version != SCHEMA_VERSION:
        raise _unusable(
            cfg, f"it says schema version {version!r} and this build writes {SCHEMA_VERSION}"
        )
    entries = raw.get("markers")
    if not isinstance(entries, list):
        raise _unusable(
            cfg, f"its markers are a {type(entries).__name__} rather than a list"
        )
    found: dict[str, Record] = {}
    for position, entry in enumerate(entries):
        if not isinstance(entry, Mapping):
            raise _unusable(cfg, f"marker {position} is a {type(entry).__name__}")
        identity = entry.get("identity")
        if not isinstance(identity, str) or not identity.strip():
            raise _unusable(cfg, f"marker {position} names no identity")
        raw_kind = entry.get("kind")
        raw_effect = entry.get("effect")
        raw_disposition = entry.get("disposition")
        try:
            kind = Kind(str(raw_kind))
            effect = None if raw_effect is None else config.RollbackEffect(str(raw_effect))
            closed = None if raw_disposition is None else Disposition(str(raw_disposition))
        except ValueError as exc:
            # Refused, not dropped, since a dropped marker reads as closed.
            raise _unusable(cfg, f"marker {position} carries a value this build cannot read") from exc
        record = Record(
            marker=Marker(
                kind=kind,
                identity=identity,
                effect=effect,
                session_id=_optional_str(entry.get("session_id")),
                capture_stamp=_optional_str(entry.get("capture_stamp")),
                detail=str(entry.get("detail") or ""),
                observed=str(entry.get("observed") or ""),
            ),
            disposition=closed,
            actor=_optional_str(entry.get("actor")),
            decided=_optional_str(entry.get("decided")),
            note=str(entry.get("note") or ""),
        )
        found[record.marker.marker_id] = record
    return found


def _optional_str(value: Any) -> str | None:
    return None if value is None else str(value)


def _read(cfg: config.Config) -> dict[str, Record]:
    """Load the record, treating anything it cannot RECOGNIZE as a refusal.

    Absence is checked once here, so all four readers answer alike.
    """
    path = path_for(cfg)
    if not path.exists():
        _assert_library_is_readable(cfg)
        return {}
    try:
        text = path.read_text()
    except OSError as exc:
        raise _unusable(cfg, "it could not be opened") from exc
    try:
        raw = json.loads(text)
    except ValueError as exc:
        raise _unusable(cfg, "it is not JSON") from exc
    return _recognize(cfg, raw)


def _write(cfg: config.Config, recorded: Mapping[str, Record]) -> None:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "markers": [recorded[key].to_json() for key in sorted(recorded)],
    }
    config.atomic_write_bytes(
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"), path_for(cfg)
    )


# Deriving the markers a restore leaves behind


def _document_bytes(path: Path) -> bytes | None:
    """The bytes at ``path``, or None when there is nothing there, kept apart from empty."""
    try:
        if path.is_dir():
            return _directory_digest(path)
        return path.read_bytes()
    except OSError:
        return None


def _directory_digest(root: Path) -> bytes:
    """A stable summary of a directory's contents, for comparison only.

    Derived by walking (P3), and it hashes contents, because a same-length edit
    in ``label_outcomes`` would otherwise go unmarked.
    """
    digest = hashlib.sha256()
    for current, directories, files in os.walk(root):
        directories.sort()
        here = Path(current)
        for name in sorted(files):
            path = here / name
            digest.update(path.relative_to(root).as_posix().encode("utf-8"))
            digest.update(b"\0")
            try:
                with path.open("rb") as handle:
                    while chunk := handle.read(1 << 20):
                        digest.update(chunk)
            except OSError:
                # A token no file's bytes can produce, so unreadable never equals empty.
                digest.update(b"\0unreadable\0")
            digest.update(b"\n")
    return digest.digest()


def effect_markers(
    cfg: config.Config,
    *,
    captured: Mapping[str, Path | None],
    session_id: str | None = None,
    capture_stamp: str | None = None,
    now: datetime | None = None,
) -> tuple[Marker, ...]:
    """Every out-of-band effect inside the window this restore is about to discard.

    ``captured`` maps an inventory key to its captured copy, or None when it was
    absent. The caller must run this BEFORE anything is replaced. One marker per
    declared effect, since each is disposed of separately.
    """
    observed = timestamp(now)
    markers: list[Marker] = []
    for entry, effect in config.out_of_band_effects():
        if entry.medium is config.Medium.KEYCHAIN:
            continue
        live = _document_bytes(config.state_path(entry.key, cfg))
        capture_path = captured.get(entry.key)
        held = _document_bytes(capture_path) if capture_path is not None else None
        if live == held:
            continue
        markers.append(
            Marker(
                kind=Kind.EFFECT,
                identity=entry.key,
                effect=effect,
                session_id=session_id,
                capture_stamp=capture_stamp,
                detail=(
                    f"{entry.key} changed after this capture was taken, and the "
                    f"{effect} it caused does not roll back with it"
                ),
                observed=observed,
            )
        )
    return tuple(markers)


def in_flight_marker(
    *,
    capture_stamp: str,
    now: datetime | None = None,
) -> Marker:
    """The latch a restore writes before its first destructive step.

    Keyed on the capture with no session, so a repeated attempt is idempotent.
    The stamp is taken verbatim; validation belongs to the manifest reader. It
    is written even when nothing else is, so a killed restore refuses rather
    than leaving mismatched generations allowed. Its remedy, a recovery, is exempt.
    """
    return Marker(
        kind=Kind.IN_FLIGHT_RESTORE,
        identity=capture_stamp,
        effect=None,
        session_id=None,
        capture_stamp=capture_stamp,
        detail=(
            f"a restore of this library from the capture {capture_stamp} started "
            f"and was not seen to finish, so the database and the state coupled to "
            f"it may be at different generations; until a restore completes, "
            f"anything written now is written against a library whose halves do "
            f"not agree"
        ),
        observed=timestamp(now),
    )


def tree_markers(
    tree_ids: Iterable[str],
    *,
    session_id: str | None = None,
    capture_stamp: str | None = None,
    detail: str = "",
    now: datetime | None = None,
) -> tuple[Marker, ...]:
    """One marker per tree a restore left unconverged.

    Pure, taking identifiers, so this module stays below the registry.
    """
    observed = timestamp(now)
    return tuple(
        Marker(
            kind=Kind.UNCONVERGED_TREE,
            identity=tree_id,
            effect=None,
            session_id=session_id,
            capture_stamp=capture_stamp,
            detail=detail
            or (
                "the restored capture predates this tree's recorded cutover, so "
                "the membership written natively since then is gone from the "
                "database while the files it referenced are still on disk and "
                "still read as owned; an incremental sync cannot see that gap"
            ),
            observed=observed,
        )
        for tree_id in sorted(set(tree_ids))
    )


# The record


def record_markers(cfg: config.Config, markers: Sequence[Marker]) -> tuple[Record, ...]:
    """Persist markers, idempotently, and return every record afterwards.

    The whole cycle is under the lock. A marker already recorded is left alone,
    so a disposition is never reopened.
    """
    with _locked(cfg):
        recorded = _read(cfg)
        for marker in markers:
            recorded.setdefault(marker.marker_id, Record(marker=marker))
        _write(cfg, recorded)
        return tuple(recorded[key] for key in sorted(recorded))


def retract_in_flight(cfg: config.Config) -> tuple[str, ...]:
    """Discharge EVERY in-flight latch. Returns the identifiers that were there.

    Deletion, not a disposition, since the fact is true only during a restore;
    restricted to this kind so no refusal can be deleted away. Every latch,
    because restores do not overlap and a completed one leaves the library whole.
    """
    with _locked(cfg):
        recorded = _read(cfg)
        discharged = tuple(
            sorted(
                key
                for key, record in recorded.items()
                if record.marker.kind is Kind.IN_FLIGHT_RESTORE
            )
        )
        if not discharged:
            return ()
        for key in discharged:
            del recorded[key]
        _write(cfg, recorded)
        return discharged


def records(cfg: config.Config) -> tuple[Record, ...]:
    """Every recorded marker, closed and open alike, in identifier order."""
    recorded = _read(cfg)
    return tuple(recorded[key] for key in sorted(recorded))


def outstanding(cfg: config.Config) -> tuple[Record, ...]:
    """Every marker nobody has closed yet."""
    return tuple(record for record in records(cfg) if record.outstanding)


def unconverged_trees(cfg: config.Config) -> tuple[str, ...]:
    """The stable identifiers of trees whose rebuild is still owed, deduplicated.

    A tree may carry one open marker per restore that observed it.
    """
    return tuple(
        sorted(
            {
                record.marker.identity
                for record in outstanding(cfg)
                if record.marker.kind is Kind.UNCONVERGED_TREE
            }
        )
    )


def close_marker(
    cfg: config.Config,
    marker_id: str,
    *,
    disposition: Disposition,
    actor: str,
    note: str = "",
    now: datetime | None = None,
) -> Record:
    """Close one marker, naming who closed it and how.

    Under the lock, since a dropped disposition refuses forever. Closing a
    closed marker returns it unchanged.
    """
    with _locked(cfg):
        recorded = _read(cfg)
        existing = recorded.get(marker_id)
        if existing is None:
            raise refuse(
                "restore-record-unusable",
                f"no reconciliation marker has the identifier {marker_id!r}",
                steps=("list the outstanding markers and take the identifier from one",),
                scope=Scope.RUN,
                origin=("reconcile",),
                detail={"marker_id": marker_id},
            )
        if not existing.outstanding:
            return existing
        closed = Record(
            marker=existing.marker,
            disposition=disposition,
            actor=actor,
            decided=timestamp(now),
            note=note,
        )
        recorded[marker_id] = closed
        _write(cfg, recorded)
        return closed


# The refusal


#: The kinds this module LATCHES on at the session boundary: every kind, named
#: so a later kind is placed deliberately.
LATCHING_KINDS: frozenset[Kind] = frozenset(Kind)


def converged(cfg: config.Config) -> bool:
    """True when nothing this module LATCHES on is still open."""
    return not [
        record for record in outstanding(cfg) if record.marker.kind in LATCHING_KINDS
    ]


def assert_converged(cfg: config.Config) -> None:
    """Refuse every further destructive session while a restore is unreconciled.

    Enforced at the gate every destructive session passes. A RECOVERY is exempt
    so the latch never condemns its own remedy (U8); the rebuild declares
    ``session.Intent.RECOVERY`` and puts the effect latch back by name. Tree
    markers still latch for builds or records predating ``core.convergence``.
    The kinds are reported separately, since their remedies differ.
    """
    open_records = [
        record for record in outstanding(cfg) if record.marker.kind in LATCHING_KINDS
    ]
    if not open_records:
        return
    effects = [r for r in open_records if r.marker.kind is Kind.EFFECT]
    in_flight = [r for r in open_records if r.marker.kind is Kind.IN_FLIGHT_RESTORE]
    trees = sorted({r.marker.identity for r in open_records if r.marker.kind is Kind.UNCONVERGED_TREE})
    lines = [f"  - {r.marker.marker_id}: {r.marker.detail}" for r in open_records]
    raise refuse(
        "restore-reconciliation-outstanding",
        "a restore of this library left "
        + ", ".join(
            part
            for part in (
                f"{len(effects)} effect(s) it could not undo" if effects else "",
                f"{len(in_flight)} restore(s) never seen to finish" if in_flight else "",
                f"{len(trees)} tree(s) that need rebuilding" if trees else "",
            )
            if part
        )
        + ", and every further write is refused until each one is closed. An "
        "effect is closed by a person deciding what to do about it; an "
        "unfinished restore is closed by finishing one; a tree is closed only by "
        "a full rebuild, never by a decision. Each of those declares itself a "
        "recovery and is not held by this:\n"
        + "\n".join(lines),
        remedy=(
            Remedy.REBUILD_TREE
            if trees
            else Remedy.RESTORE_FROM_SNAPSHOT
            if in_flight
            else Remedy.COMPLETE_PENDING_ACTION
        ),
        scope=Scope.RUN,
        origin=("reconcile",),
        detail={
            "markers": [r.marker.marker_id for r in open_records],
            "effects": [r.marker.marker_id for r in effects],
            "in_flight_restores": [r.marker.marker_id for r in in_flight],
            "unconverged_trees": trees,
        },
    )


__all__ = [
    "LATCHING_KINDS",
    "LOCK_KEY",
    "SCHEMA_VERSION",
    "STATE_KEY",
    "Disposition",
    "Kind",
    "Marker",
    "Record",
    "assert_converged",
    "close_marker",
    "converged",
    "effect_markers",
    "in_flight_marker",
    "lock_path",
    "outstanding",
    "path_for",
    "record_markers",
    "records",
    "retract_in_flight",
    "tree_markers",
    "unconverged_trees",
]
