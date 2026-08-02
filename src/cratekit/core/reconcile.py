"""What a restore could not undo, and the refusal that stands until somebody says.

A KTD21b restore is a state transition rather than a file copy. It returns the
database and the state coupled to it to one matched earlier point, so the
registry, the watermarks, the tombstones and the declines all agree with the rows
they describe. That agreement is real and it is not convergence, because agreeing
with each other is not the same as agreeing with the world:

* the audio a discarded run downloaded is still on the music volume, and the next
  acquisition pass reads those files as owned by nobody;
* the playlist that run renamed at the provider is still renamed, so the marker
  saying "already taken" lives on somebody else's server and did not roll back;
* the file a discarded tombstone recorded is still in the Trash, and the library
  now holds a row for a file nobody can open.

None of those is repairable from here. What IS possible is to name every one of
them, to refuse every further destructive session until a person has said what
they want done about each, and to make that refusal survive the process, the
machine, and the next restore. That is this module.

THREE PROPERTIES, AND EACH ONE IS A DEFECT THIS REPOSITORY HAS ALREADY PAID FOR.

**The marker set is DERIVED from the state inventory** (P4). Each COUPLED entry
declares what its records caused outside the coupled set, in
``config.RollbackEffect``, and this module asks the inventory rather than
carrying a list. A list here would be right on the day it was written and silent
about every entry added afterwards, which is the failure mode that makes a
derivation worth building in the first place.

**Every read then write cycle is under a sibling lock.** ``atomic_write_bytes``
makes the rename atomic and does nothing for the cycle around it, so two
processes both read the same set, both add their own record, and the second
rename discards the first one's while the losing call returns a record reporting
success. Two separate units shipped exactly that bug. The lock is its own
NEVER_RESTORED inventory entry rather than a file beside the document, because
the process replacing directories during a restore is the process holding this
lock, and a lock whose inode gets swapped underneath its holder is exclusion
disappearing mid-session with nothing raised.

**The reader recognizes the document positively, field by field**, and refuses
everything else. Catching only ``json.loads`` raising leaves a top-level list, a
scalar, a null field, or records under a version this build does not know all
reading as an empty store, and an empty store here means "nothing is
outstanding", which is the permissive answer to the one question this module
exists to answer conservatively.

LAYER: infrastructure. It reads configuration, does input and output, names no
verb, and carries remediation TOKENS and steps rather than any text a user types
(D2). It deliberately does NOT import the tree registry: that module is ranked
write, this one is imported by the session boundary below it, and a marker
carries a tree's stable identifier rather than anything the registry has to
resolve.
"""

from __future__ import annotations

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

#: The state entry holding the record. Named once so this module and every
#: consumer cannot disagree about which file is meant.
STATE_KEY = "restore_reconciliation"

#: Its sibling lock, in an entry of its own. See the module docstring.
LOCK_KEY = "restore_reconciliation_lock"

#: Bumped only when the record's on-disk shape changes incompatibly. A document
#: written by a later build is refused rather than guessed at: a wrong reading
#: here reports a library as converged when it is not.
SCHEMA_VERSION = 1


class Kind(StrEnum):
    """The two things a restore leaves behind, which are not the same thing.

    An EFFECT is something that happened outside the coupled set and did not roll
    back with it. A person dispositions it: they either accept it as it stands or
    they go and repair it by hand, and either way the answer is a sentence about
    one fact.

    An UNCONVERGED TREE is not a fact about the outside world at all. It is a
    tree whose membership the database can no longer be trusted to hold, because
    the restore landed on the far side of that tree's cutover. Nothing a person
    says repairs it; only a full-scope rebuild does. Collapsing the two would let
    somebody disposition a tree away with a sentence, which is exactly the escape
    R39 refuses.
    """

    EFFECT = "effect"
    UNCONVERGED_TREE = "unconverged-tree"


class Disposition(StrEnum):
    """What a person decided about one marker.

    ``ACCEPTED`` means "leave it as it is, I know". ``REPAIRED`` means "I went and
    put it right". Both close the marker, and they are kept apart because the
    difference is the only thing a later reader can use to tell a library that
    was tidied from one that was merely acknowledged.

    DELIBERATELY NOT CALLED ``Verdict``. ``core.review`` already exports a
    ``Verdict`` whose members are ACCEPTED and REJECTED, and the two enums share
    a member spelling while meaning different things about different objects.
    Both are string enums, so one passed where the other belongs compares equal
    to a stored value and nothing raises. One name for two ideas is the shape
    this repository keeps finding after the fact, so it is spelled apart here
    rather than recorded as a known collision.
    """

    ACCEPTED = "accepted"
    REPAIRED = "repaired"


@dataclass(frozen=True, slots=True)
class Marker:
    """One thing a restore could not undo, addressable and persisted.

    ``identity`` is a STABLE IDENTIFIER and never a derived display name (R19,
    D5). For an effect it is the state entry's inventory key, which is chosen by
    this product and cannot be renamed by a user; for an unconverged tree it is
    the taxonomy's tree identifier. A marker keyed on anything a person can
    rename diverges after the rename instead of converging, and the divergence is
    invisible: the code simply finds no entry and reports convergence.

    ``marker_id`` is composed from the kind, the identity and the effect rather
    than minted randomly, so recording the same marker twice for one restore is
    idempotent rather than a second row somebody has to close twice.
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
        return f"{self.kind}:{self.identity}:{effect}"

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
    """Where the record lives, resolved through the declared state inventory.

    Through ``state_path`` and never composed here. A module that builds its own
    path under a state root has invented a state file the inventory does not know
    about, so nothing walking the inventory can see it, back it up, or reason
    about whether a restore replaces it.
    """
    return config.state_path(STATE_KEY, cfg)


def lock_path(cfg: config.Config) -> Path:
    """The sibling lock, resolved the same way and living somewhere else.

    Somewhere else is not an accident of naming. The lock entry is declared
    NEVER_RESTORED and the record entry SURVIVES_ROLLBACK, and ``state_path``
    derives each entry's directory from that answer, so the two land in different
    directories by construction. A lock beside the document it guards is one a
    restore can swap the inode of, which is the shape U11 paid for.
    """
    return config.state_path(LOCK_KEY, cfg)


def _unusable(cfg: config.Config, what: str) -> CratekitError:
    """One refusal for every way this document is not this document.

    The same sentence in each case, deliberately: what a person does about it
    does not depend on WHICH way the file is wrong, and the specific shape rides
    on the detail where a bug report can read it.
    """
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


@contextmanager
def _locked(cfg: config.Config) -> Iterator[None]:
    """Hold the sibling lock across one read then write cycle.

    BLOCKING, like the decision stores next door: two processes recording
    markers should serialize rather than raise at a person. The lock file
    persists after release, deliberately, for the reason every lock in this
    repository states at length: unlinking the name lets a second process take a
    lock on a fresh inode while the first still holds the old one, and both then
    believe they hold the only lock with nothing raised.

    A PLATFORM WITH NO ADVISORY LOCKING REFUSES. Proceeding unlocked is the
    behaviour being prevented, so degrading to it on the platform where the fix
    cannot be applied would leave exactly the defect, reachable by anybody on
    that platform.
    """
    target = lock_path(cfg)
    config._mkdir_private(target.parent)
    handle = None
    try:
        import fcntl

        # os.open with an explicit mode rather than the builtin open(), which
        # creates at 0666 masked by the umask (P1).
        descriptor = os.open(target, os.O_CREAT | os.O_RDWR, config.PRIVATE_FILE_MODE)
        handle = os.fdopen(descriptor, "r+b")
        if hasattr(os, "chmod"):
            try:
                # O_CREAT applies the mode only when it CREATES the file, so a
                # lock left behind at another mode would keep it without this.
                os.chmod(target, config.PRIVATE_FILE_MODE)
            except OSError as exc:
                logger.debug("could not set the mode on %s: %s", target, exc)
        fcntl.flock(handle, fcntl.LOCK_EX)
    except BaseException as exc:
        if handle is not None:
            handle.close()
        if not isinstance(exc, (ImportError, OSError)):
            raise
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

    REFUSAL IS THE ONLY ALTERNATIVE TO A CORRECT READ. A guard that covers only
    the case where ``json.loads`` itself raises lets every document that is good
    JSON and is not this record fall through to an empty mapping: a top-level
    list, a scalar, a version this build does not know, ``markers`` present and
    null, a record whose identifier key was renamed. Each of those reports that
    nothing is outstanding, and the empty result is then handed to the writer, so
    one further record deletes every prior marker from the disk.
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
            # A member this build does not know is refused rather than dropped. A
            # dropped marker reads as "already closed", which is the one
            # misreading that lets a library report convergence it never reached.
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
    """Load the record, treating anything it cannot RECOGNIZE as a refusal."""
    path = path_for(cfg)
    if not path.exists():
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


# ---------------------------------------------------------------------------
# Deriving the markers a restore leaves behind
# ---------------------------------------------------------------------------


def _document_bytes(path: Path) -> bytes | None:
    """The bytes at ``path``, or None when there is nothing there.

    None and empty are kept apart. A coupled entry that did not exist at capture
    time and exists now is a change; a file that exists at both ends and holds
    the same bytes is not.
    """
    try:
        if path.is_dir():
            return _directory_digest(path)
        return path.read_bytes()
    except OSError:
        return None


def _directory_digest(root: Path) -> bytes:
    """A stable summary of a directory's contents, for comparison only.

    DERIVED BY WALKING (P3). Several coupled entries are directories, and a
    comparison that looked only at the top level would report a directory
    unchanged while every file inside it had moved. Names and sizes are enough
    for the question being asked, which is "did this entry change across the
    window", not "what changed".
    """
    parts: list[str] = []
    for current, directories, files in os.walk(root):
        directories.sort()
        here = Path(current)
        for name in sorted(files):
            try:
                size = (here / name).stat().st_size
            except OSError:
                size = -1
            parts.append(f"{(here / name).relative_to(root).as_posix()}:{size}")
    return "\n".join(parts).encode("utf-8")


def effect_markers(
    cfg: config.Config,
    *,
    captured: Mapping[str, Path | None],
    session_id: str | None = None,
    capture_stamp: str | None = None,
    now: datetime | None = None,
) -> tuple[Marker, ...]:
    """Every out-of-band effect inside the window this restore is about to discard.

    ``captured`` maps a state entry's inventory key to the copy of it inside the
    capture, or to None when the capture recorded that entry as legitimately
    absent. Both answers are used: an entry present now and absent then changed,
    and so did one whose bytes differ.

    THE COMPARISON RUNS BEFORE ANYTHING IS REPLACED, and the caller is
    responsible for that ordering. Afterwards the live document IS the captured
    one, every comparison is equal, and the report says nothing happened.

    ONE MARKER PER DECLARED EFFECT rather than one per changed file, because the
    effects are what a person dispositions and they are dispositioned separately:
    a label watermark that advanced means both that audio landed on the volume
    and that a playlist was renamed at the provider, and putting one of those
    right does not put the other right.
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


def tree_markers(
    tree_ids: Iterable[str],
    *,
    session_id: str | None = None,
    capture_stamp: str | None = None,
    detail: str = "",
    now: datetime | None = None,
) -> tuple[Marker, ...]:
    """One marker per tree a restore left unconverged.

    Pure, and it takes identifiers rather than a registry, so the module that
    holds the registry stays above this one in the ladder and this one stays
    importable by the session boundary underneath it.
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


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


def record_markers(cfg: config.Config, markers: Sequence[Marker]) -> tuple[Record, ...]:
    """Persist markers, idempotently, and return every record afterwards.

    THE WHOLE CYCLE IS UNDER THE LOCK. The read decides what the write contains,
    so a lock around the write alone protects nothing: the losing process still
    writes a set it read before the winner's marker existed, and the marker it
    drops is a library reporting convergence it never reached.

    A marker already recorded is left ALONE rather than reset, including one that
    has been dispositioned. Re-recording would silently reopen a decision a
    person already made, which is the opposite of what an idempotent call should
    do, and it would do it on every subsequent restore.
    """
    with _locked(cfg):
        recorded = _read(cfg)
        for marker in markers:
            recorded.setdefault(marker.marker_id, Record(marker=marker))
        _write(cfg, recorded)
        return tuple(recorded[key] for key in sorted(recorded))


def records(cfg: config.Config) -> tuple[Record, ...]:
    """Every recorded marker, closed and open alike, in identifier order."""
    recorded = _read(cfg)
    return tuple(recorded[key] for key in sorted(recorded))


def outstanding(cfg: config.Config) -> tuple[Record, ...]:
    """Every marker nobody has closed yet."""
    return tuple(record for record in records(cfg) if record.outstanding)


def unconverged_trees(cfg: config.Config) -> tuple[str, ...]:
    """The stable identifiers of trees whose rebuild is still owed."""
    return tuple(
        record.marker.identity
        for record in outstanding(cfg)
        if record.marker.kind is Kind.UNCONVERGED_TREE
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

    Under the lock for the same reason recording is, and losing one costs more:
    a dropped disposition leaves a marker standing forever, so every further
    destructive session refuses and nobody can work out why.

    Closing an already closed marker returns the existing record unchanged rather
    than restamping it. The first answer is the one that was given.
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


# ---------------------------------------------------------------------------
# The refusal
# ---------------------------------------------------------------------------


def converged(cfg: config.Config) -> bool:
    """True when nothing a restore left behind is still open."""
    return not outstanding(cfg)


def assert_converged(cfg: config.Config) -> None:
    """Refuse every further destructive session while a restore is unreconciled.

    ENFORCED AT THE GATE EVERY DESTRUCTIVE SESSION PASSES THROUGH, rather than in
    each workflow, for the same reason the committed-unverified latch is: a
    refusal a caller can forget is a refusal that is eventually forgotten. A
    RECOVERY declares itself exempt, and it has to be, because a second restore
    is one of the things a person may legitimately do about the first one, and a
    latch that condemned its own remedy would leave a library with no exit but a
    hand-edited file. That is the lesson U8 paid for and it applies unchanged
    here.

    The two kinds are reported SEPARATELY inside one refusal, because their
    remedies are not the same act: an effect is closed by a person saying what
    they want done about it, and an unconverged tree is closed only by a rebuild.
    Collapsing them would send somebody to disposition a tree, which is exactly
    the escape a rebuild requirement exists to close.
    """
    open_records = outstanding(cfg)
    if not open_records:
        return
    trees = [r.marker.identity for r in open_records if r.marker.kind is Kind.UNCONVERGED_TREE]
    effects = [r for r in open_records if r.marker.kind is Kind.EFFECT]
    lines = [f"  - {r.marker.marker_id}: {r.marker.detail}" for r in open_records]
    raise refuse(
        "restore-reconciliation-outstanding",
        "a restore of this library left "
        + (f"{len(effects)} effect it could not undo" if len(effects) == 1 else f"{len(effects)} effects it could not undo")
        + (f" and {len(trees)} tree that needs rebuilding" if len(trees) == 1 else f" and {len(trees)} trees that need rebuilding")
        + ", and every further write is refused until each one is closed. An "
        "effect is closed by a person deciding what to do about it; a tree is "
        "closed only by a full rebuild, never by a decision:\n"
        + "\n".join(lines),
        remedy=Remedy.REBUILD_TREE if trees else Remedy.COMPLETE_PENDING_ACTION,
        scope=Scope.RUN,
        origin=("reconcile",),
        detail={
            "markers": [r.marker.marker_id for r in open_records],
            "effects": [r.marker.marker_id for r in effects],
            "unconverged_trees": trees,
        },
    )


__all__ = [
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
    "lock_path",
    "outstanding",
    "path_for",
    "record_markers",
    "records",
    "tree_markers",
    "unconverged_trees",
]
