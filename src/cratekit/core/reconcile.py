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

WHAT THIS MODULE DOES NOT OWN: WHETHER A TREE IS SHORT. ``core.convergence``
owns that fact. It holds the same condition arriving from the other direction, a
database recovered out of band, gates it per tree at the writer, and clears it
only on a convergence check that found no difference. ``core.restore`` hands the
trees to that module whenever it is present, so on a complete build this store
holds no tree markers at all. It still LATCHES on one if it finds one, because a
marker written by a build that had this record and not that one outlives the
merge, and a fact recorded in a store nothing reads is worse than no record.
See :func:`assert_converged` for why latching on it does not condemn its remedy.

LAYER: infrastructure. It reads configuration, does input and output, names no
verb, and carries remediation TOKENS and steps rather than any text a user types
(D2). It deliberately does NOT import the tree registry, and for the same reason
it does not import ``core.convergence``: both are ranked write, this one is
imported by the session boundary below them, and a marker carries a tree's stable
identifier rather than anything either has to resolve. The handoff to the module
that owns the gate is therefore made by ``core.restore``, which is ranked write
and may name it.
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
    """The three things a restore leaves behind, which are not the same thing.

    An EFFECT is something that happened outside the coupled set and did not roll
    back with it. A person dispositions it: they either accept it as it stands or
    they go and repair it by hand, and either way the answer is a sentence about
    one fact.

    An IN-FLIGHT RESTORE is the record that one started and has not been seen to
    finish. It is written before the first destructive step and retracted by the
    step that completes, so a process killed in the middle leaves it standing, and
    a library whose database and coupled state are at different generations
    refuses every ordinary destructive session instead of looking finished. Seven
    of the twelve coupled entries declare ``RollbackEffect.NONE``, so a restore
    whose window touched only those produces no effect markers at all, and without
    this latch such a restore could be interrupted half way and leave no trace
    anywhere that anything reads.

    An UNCONVERGED TREE is not a fact about the outside world at all. It is a
    tree whose membership the database can no longer be trusted to hold, because
    the restore landed on the far side of that tree's cutover. Nothing a person
    says repairs it; only a full-scope rebuild does. Collapsing it with an effect
    would let somebody disposition a tree away with a sentence, which is exactly
    the escape R39 refuses.

    THE TREE KIND IS TRANSITIONAL AND ITS OWNER IS ELSEWHERE. ``core.convergence``
    owns tree shortness: it holds the same fact for an out-of-band recovery, gates
    it per tree at the writer, and clears it only on a convergence check.
    ``core.restore`` hands the trees to that module whenever it is present, so on
    a complete build no marker of this kind is ever written. What remains here is
    a marker written before that module existed, which outlives the merge and is
    closed by the first rebuild of that tree. It is latched all the same, because
    a fact recorded in a store nothing reads is worse than no record at all.
    """

    EFFECT = "effect"
    IN_FLIGHT_RESTORE = "in-flight-restore"
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

    ``marker_id`` is composed from the kind, the identity, the effect AND THE
    RESTORE THAT OBSERVED IT rather than minted randomly, so recording the same
    marker twice for ONE restore is idempotent rather than a second row somebody
    has to close twice, while two different restores that happen to produce the
    same triple stay two rows.

    THE RESTORE HAS TO BE PART OF THE IDENTIFIER, and leaving it out was a defect
    with two shapes, both verified. Restore 1 marks ``label_watermarks`` and a
    person accepts it; weeks later restore 2 discards an entirely different window
    over an entirely different set of orphaned files and produces the same triple.
    Without the session and the capture in the key, :func:`record_markers` sees a
    row already there, leaves the CLOSED record alone, and reports nothing
    outstanding: the audio restore 2 discarded is owned by nobody and nobody is
    told. The second shape is worse, because it survives the correct remedy. A
    pre-cutover restore marks a tree, somebody rebuilds it and closes it REPAIRED,
    the tree cuts over again, and a second pre-cutover restore of the same tree is
    swallowed by the closed record of the first. One rebuild would pay for every
    later restore of that tree, and an incremental sync structurally cannot see
    the gap it leaves.

    A marker with no session and no capture, which is what a caller building one
    by hand gets, keys on ``-`` in both positions and therefore still collapses.
    That is the right default: an unattributed marker is a marker nobody can date,
    and two of them are not distinguishable by anything this module can read.
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


def _assert_library_is_readable(cfg: config.Config) -> None:
    """Refuse a READ when the library this record belongs to is not there at all.

    A MISSING FILE ON A MISSING VOLUME IS NOT AN EMPTY STORE, and the empty
    reading is the permissive answer to the one question this module exists to
    answer conservatively.

    THIS IS THE WEAK HALF AND ITS LIMIT IS STATED RATHER THAN IMPLIED. The
    directory a volume was mounted at survives the unmount on every platform, so a
    library root can exist with everything under it gone, and from inside this
    function that state is INDISTINGUISHABLE from a library this installation has
    been pointed at and has not yet written to. Both are "the root is there and
    the document is not". A stricter rule here was tried and refused the fresh
    install, which is a guard firing on correct behaviour and therefore a guard
    people route around (P7).

    WHAT ACTUALLY CLOSES THE GAP is upstream, at the two gates that have both the
    recorded volume identity and the seams to ask about it:
    ``session.assert_gates`` asserts the volume before it reaches this module at
    all, and ``session.close_session`` now does the same before its convergence
    gate, which was the one caller that did not. The write half below is separately
    strict, because a write is proof that something is being recorded and has no
    fresh-install reading.
    """
    root = Path(cfg.library.root)
    if not root.is_dir():
        raise _unusable(
            cfg, f"the library at {root} is not there, so its state cannot be read"
        )


def _assert_library_is_writable(cfg: config.Config) -> None:
    """Refuse a WRITE when the library is the husk an unmounted volume leaves.

    STRICTER THAN THE READ, and the asymmetry is the point rather than an
    inconsistency. A read against a library with nothing recorded yet is an
    ordinary thing that happens on the first run of every install, so it cannot
    refuse. A write is different in two ways: it is proof that something is being
    recorded right now, and it CREATES the directory it writes into. Against a
    library whose volume has gone, that meant rebuilding this installation's whole
    state tree on whatever disk the mount point happens to sit on and recording
    into it, so the record landed somewhere no library will ever read it and
    nothing refused.

    So a write asks for the two things a configured library cannot be without:
    this installation's state directory, or the database the configuration names.
    A library that has been written to has the first, one that has only been
    pointed at has the second, and a husk has neither.
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
    # BEFORE the directory is created, not after. Creating the lock's parent first
    # meant a write against a library whose volume had gone rebuilt the state tree
    # on whatever disk the mount point happens to sit on, and then recorded into
    # it, so the refusal below never fired and the record landed somewhere no
    # library will ever see it.
    _assert_library_is_writable(cfg)
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
    """Load the record, treating anything it cannot RECOGNIZE as a refusal.

    Absence is checked through :func:`_assert_library_is_readable`, which is where
    the argument for what "absent" means, and what this cannot see, lives. It is
    asked HERE rather than at each of the four readers, so all four keep answering
    identically, which they are separately asserted to do.
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
    unchanged while every file inside it had moved.

    IT HASHES THE CONTENTS, not the names and lengths. Names and lengths look
    sufficient for "did this entry change across the window" and are not: a
    document edited in place to the same length reads as unchanged, and
    ``label_outcomes`` is a directory of small documents AND the one COUPLED
    directory entry carrying a declared out-of-band effect. So the one entry where
    a same-length edit is most likely is the one entry where missing it means an
    effect goes unmarked. The failure direction of the cheaper comparison is
    under-marking, which is the direction this module exists to avoid.

    The cost is bounded by what is being compared: these are state documents, not
    audio, and the walk already had to stat every one of them.
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
                # Unreadable is its own state and must not compare equal to
                # readable-and-empty, so it contributes a token no file's bytes
                # can produce.
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


def in_flight_marker(
    *,
    capture_stamp: str,
    now: datetime | None = None,
) -> Marker:
    """The latch a restore writes before its first destructive step.

    IT IS KEYED ON THE CAPTURE AND CARRIES NO SESSION, which is the opposite of
    every other marker here and is deliberate. The first version keyed it on the
    restore's own recovery session, which mints a new identifier every attempt, so
    the product's own printed advice, "run the restore again, it is safe to
    repeat", produced a second permanent row on every repeat. Two attempts of one
    restore are one restore, and what identifies a restore is the capture it is
    putting back, which is stable across every attempt. So a repeat collides with
    the row already there and is idempotent, which is what the advice promises.

    The run that started it is not lost: the session log holds a record for every
    restore, and the detail below names the capture, which is the field a person
    matches against the listing.

    IT IS WRITTEN EVEN WHEN THERE IS NOTHING ELSE TO WRITE, which is the whole
    point. Seven of the twelve coupled entries declare ``RollbackEffect.NONE``, so
    a restore whose window touched only those derives no effect markers, and a
    restore of a capture taken after every cutover derives no tree markers either.
    Such a restore used to write nothing anywhere before it began replacing files,
    and a hard kill part way through left the database at one generation, the
    coupled state at another, an empty reconciliation store, and the next ordinary
    destructive session ALLOWED. The only trace was a non-terminal session record
    that nothing consults except the prune-protection scan.

    The concrete loss that shape produces: a ``label_watermarks`` at the later
    generation against a database at the earlier one means the next label sweep
    believes it consumed releases whose rows are gone, so those tracks are never
    re-imported and nothing demands the rebuild that would find them.

    ITS REMEDY IS A RECOVERY, WHICH IS EXEMPT, so this latch does not condemn its
    own remedy: finishing the interrupted restore, or running another one, is an
    ``Intent.RECOVERY`` session and passes. A person who would rather accept the
    half-restored state closes it with a disposition like any other marker.
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


def retract_in_flight(cfg: config.Config) -> tuple[str, ...]:
    """Discharge EVERY in-flight latch. Returns the identifiers that were there.

    DELETION RATHER THAN A DISPOSITION, because the two operations mean different
    things. A disposition is a person's answer about something that happened and
    will always have happened, so it is kept forever and never restamped. "A
    restore is in flight" is not that kind of fact: it is true for the length of
    one restore and false afterwards, and recording a decision about it would put
    a permanent row in the store for something nobody decided. It is restricted to
    that one kind rather than offered generally, because a general delete is the
    softening path in its purest form: every refusal this module raises could be
    answered by removing the marker that raised it, with no record that anything
    was ever outstanding.

    EVERY LATCH, NOT THE CALLER'S OWN, and that is the correction rather than a
    convenience. The refusal these markers raise says an unfinished restore is
    closed by finishing one. When only the caller's own row was retracted that
    sentence was false: restore 1 interrupted and restore 2 run to completion
    SUCCESSFULLY left restore 1's latch standing, the outcome reported itself
    unconverged, and the next ordinary session refused with a remedy that had
    already been carried out. The claim in the refusal is what decides the scope
    here, and the claim is right: the library lock is exclusive, so restores do
    not overlap, and one that ran to the end left this library whole whatever was
    in flight before it. A latch is a claim that the halves may not agree, and a
    completed restore is evidence that they do.
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

    Deduplicated because a tree can now carry several open markers: the identifier
    includes the restore that observed it, on purpose, so two pre-cutover restores
    of one tree are two rows rather than one swallowing the other. What a caller
    wants from this is the SET of trees, and a tree named twice is one tree.
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


#: The kinds this module LATCHES on at the session boundary.
#:
#: EVERY KIND, and it is written as a set rather than left implicit so that the
#: question "which kinds does this hold" has one answer somewhere a reader can
#: find, and so that a kind added later has to be placed deliberately.
LATCHING_KINDS: frozenset[Kind] = frozenset(Kind)


def converged(cfg: config.Config) -> bool:
    """True when nothing this module LATCHES on is still open."""
    return not [
        record for record in outstanding(cfg) if record.marker.kind in LATCHING_KINDS
    ]


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

    AN UNCONVERGED TREE IS LATCHED HERE, AND THE ARGUMENT FOR THAT WAS RE-DERIVED
    ONCE FROM A FALSE PREMISE. The first fix round removed it, reasoning that the
    refusal names a rebuild as its remedy, that a rebuild writes through
    ``write.trees.write_tree_membership``, and that ``write_tree_membership`` has
    no ``intent`` parameter and therefore cannot enter these gates as anything but
    an ordinary write. The last clause was true of this branch alone and is false
    of the product: the unit that builds the rebuild gives that function both a
    ``purpose`` and an ``intent``, and its rebuild declares
    ``session.Intent.RECOVERY`` precisely so this latch cannot refuse it. So the
    remedy CAN declare itself, the latch does not condemn it, and the rule that
    was invoked to remove this does not apply. Removing it cost more than it
    saved: with the latch gone, a pre-cutover restore recorded a tree marker that
    nothing anywhere read, and both the next destructive session and the next run
    close were allowed over a library holding a tree that is provably short.

    THE EXEMPTION IS WIDER THAN THE REBUILD NEEDS AND THE REBUILD NARROWS IT BACK.
    ``RECOVERY`` sheds this whole latch, including the EFFECT markers, which are
    facts about the world outside this library that no rebuild repairs. That is
    the rebuild's to put back by name, and it does.

    WHERE THE FACT LIVES ON A COMPLETE BUILD. ``core.convergence`` owns tree
    shortness: it holds the same condition arriving from an out-of-band recovery,
    gates it per tree at the writer, and clears it only on a convergence check
    reporting no difference. ``core.restore`` hands the trees to that module when
    it is present, so on a complete build this store holds no tree markers at all
    and this branch of the refusal is unreachable. What it covers is the window in
    which this record exists and that one does not, and a marker written before
    the merge that outlives it.

    The kinds are reported SEPARATELY inside one refusal, because their remedies
    are three different acts: an effect is closed by a person saying what they
    want done about it, an unfinished restore by finishing one, and a tree only by
    a full rebuild, never by a decision.
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
