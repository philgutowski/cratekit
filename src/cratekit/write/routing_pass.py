"""Deferred routing: what a run meant to place, and whether it ever landed (U19).

WHAT THIS MODULE IS FOR. A new track's placement is decided during acquisition,
when there is nothing in the library to place. The row it needs comes into
existence later, when a person imports the intake export, and only after that can
membership be written. So the decision and the write are separated by an act this
product does not perform, and everything here follows from that gap.

THE FOUR PROPERTIES, each one a failure the gap produces.

**The decision is persisted when it is MADE.** A run that holds its placements in
memory until the end has nothing to say about them after a crash, which is
precisely the run somebody needs to recover. So an intent reaches disk at the
moment it is decided, and the process that picks the work up later reads what its
predecessor believed rather than re-deriving it from inputs that have since moved.

**The mark comes AFTER the commit, never before.** A track becomes routed only
once its membership row is committed and a read-back proves it. A crash in that
window costs a re-run, and a re-run is cheap because membership deduplicates.
The reverse order is not merely riskier, it is unrecoverable: a mark written
before a commit that never happens strands the membership permanently, because
the one thing that knew to place the track has already recorded that it did.

**Outstanding is DERIVED from per-track state.** There is no completion flag,
anywhere. A flag beside the states is a second answer to one question, and the
two disagree the first time a crash lands between the two writes; the shape this
whole module exists to avoid is exactly a record that says something finished
when it did not.

**Readiness is row presence, read-only, and fail-safe.** Run the pass before the
import and it resolves nothing, marks nothing, and says so. Nothing is opened,
no session is taken, and the state tree is left byte for byte as it was found. A
pass that cannot tell whether the import happened BEHAVES exactly like a pass
that knows it has not, and REPORTS something else entirely. The two halves of
that sentence used to be one, and the conflation is a loop with no exit: a
location that reaches no row because no prefix maps it, or a destination the
template no longer declares, is answered by fixing configuration and never by
importing, so telling that person the import has not happened sends them round
the same act forever. Behaving the same is the fail-safe direction; reporting
the same is a wrong answer, so the question has three answers rather than two.

WHAT IS SURFACED RATHER THAN SKIPPED. rekordbox soft-deletes, so a track the user
imported and then removed still has a row, carrying the removal marker. Its
location therefore reaches a row and reaches no ACTIVE row, and that pair is
distinguishable from a location that reaches nothing at all. The first is a track
somebody deleted on purpose and the second is a track nobody has imported yet,
and only one of them is answered by importing. Neither is skipped: a skip is
indistinguishable from a placement that worked, and a run that closes over one is
a run that reports tracks as placed while they sit nowhere.

LAYER: write. It reads and writes state, calls the session spine rather than
rebuilding it, and NAMES NO VERB (D2): every command a user types is rendered by
the CLI layer from a remediation token.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, replace
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.cli import output
from cratekit.core import (
    config,
    convergence,
    locations,
    rb_writer,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import trees

logger = logging.getLogger(__name__)

#: The state entry this module owns. Named once, so the resolver and every caller
#: cannot disagree about which file is meant.
STATE_KEY = "routing_intents"

#: The lock that serializes every read-modify-write of the entry above. A second
#: declared entry rather than a suffix computed from the first, because a path
#: composed under a state root is a file the inventory does not know about.
LOCK_KEY = "routing_intents_lock"

#: Bumped only when the on-disk shape changes incompatibly. A file written by a
#: newer build is refused rather than guessed at: a misread here decides whether
#: a run may close over a track that is in no playlist.
SCHEMA_VERSION = 1

#: The workflow name the membership write records in the session log. A name for
#: an operation, not a verb: the CLI layer owns verb names (D2).
ROUTING_WORKFLOW = "deferred-routing"


class TrackState(StrEnum):
    """Where one track's deferred placement got to.

    ``ACKNOWLEDGED`` is not a flavour of routed. It records that a person looked
    at a track this pass could not place and said out loud that it is not coming
    back. Collapsing the two would make "we placed it" and "somebody deleted it"
    the same fact, and the run's own report would then be false.
    """

    INTENDED = "intended"
    ROUTED = "routed"
    ACKNOWLEDGED = "acknowledged"


#: The states that settle a track. Listed rather than derived, and the
#: OUTSTANDING set below is the derived half. The direction is the property: a
#: state nobody has classified lands in the outstanding set, so a member added
#: later cannot close a run by omission. Deriving this half instead would give a
#: new member the settling answer, which is the fail-open direction.
SETTLED: frozenset[TrackState] = frozenset({TrackState.ROUTED, TrackState.ACKNOWLEDGED})

#: Everything else, derived from the enum so the two halves cannot both miss a
#: member (P3).
OUTSTANDING: frozenset[TrackState] = frozenset(TrackState) - SETTLED


class Placement(StrEnum):
    """Why one intent did or did not reach a single active row this pass.

    Six answers rather than placed-or-not, because five of these are different
    problems with different answers and fusing any two of them reports one as the
    other. The pair that matters most is ``NOT_IMPORTED`` against ``WITHDRAWN``:
    the first is answered by importing and the second never will be.
    """

    #: Exactly one active row. This is the only placement that gets written.
    RESOLVED = "resolved"
    #: No row at all, of any kind. The import has not happened for this track.
    NOT_IMPORTED = "not-imported"
    #: Rows exist and every one of them carries the soft-delete marker. The track
    #: was imported and then removed in rekordbox.
    WITHDRAWN = "withdrawn"
    #: Two or more active rows claim the location. U18 refuses to write both, so
    #: this unit refuses to mark it.
    AMBIGUOUS = "ambiguous"
    #: The recorded location resolves to no path on this machine. A configuration
    #: failure, never a missing import, and reporting it as one sends a person to
    #: import something they have already imported.
    UNRESOLVED = "unresolved"
    #: The destination this ledger names is not one the active taxonomy declares
    #: any more. Somebody edited the template between the decision and the
    #: import, which is an ordinary act, and it says nothing at all about rows.
    #: IT IS PER TRACK, and that is the whole reason it exists: resolving the
    #: display names used to raise out of the pass, so one stale record left
    #: every other track in the run unplaced, still outstanding, and unable to
    #: close, with no reason reported for any of them.
    UNDECLARED = "undeclared"


#: The placements a membership write may be built from. One member today, named
#: rather than spelled at the two places that ask, so widening it is one edit
#: somebody has to make deliberately.
WRITABLE: frozenset[Placement] = frozenset({Placement.RESOLVED})

#: The placements that count as evidence the import HAPPENED: the location
#: reached a row of some kind. ``UNRESOLVED`` is deliberately not among them,
#: because a location that resolves to no path reaches nothing for a reason
#: importing cannot fix.
IMPORTED: frozenset[Placement] = frozenset(
    {Placement.RESOLVED, Placement.WITHDRAWN, Placement.AMBIGUOUS}
)

#: The placements that say NOTHING about whether the import happened. Derived as
#: everything that is neither evidence of an import nor the one member that means
#: "no row exists and one could have", so a member added later lands here rather
#: than being counted as a missing import (P3). The direction is the property: a
#: new member wrongly counted as evidence would let a pass write, and a new member
#: wrongly counted as a missing import would tell a person to repeat an import
#: they have already done.
ANSWERLESS: frozenset[Placement] = (
    frozenset(Placement) - IMPORTED - {Placement.NOT_IMPORTED}
)


class Readiness(StrEnum):
    """Whether the library holds rows for the tracks this run is waiting on.

    THREE ANSWERS, because two of them collapsed a question with two different
    remedies into one. ``NOT_READY`` is a claim about the world: the rows are not
    there yet and importing is what puts them there. ``UNANSWERABLE`` is a claim
    about this pass: nothing reached a row and at least one intent could not even
    be asked the question, because its location maps to no path or its
    destination is not declared any more. Both write nothing, which is the
    fail-safe half they share; only one of them is answered by importing.
    """

    READY = "ready"
    NOT_READY = "not-ready"
    UNANSWERABLE = "unanswerable"


class RoutingLedgerUnreadable(CratekitError):
    """The ledger exists and cannot be understood.

    Deliberately NOT collapsed into "no records". An empty ledger reads as
    "nothing is outstanding", which admits exactly the close this module exists
    to refuse, so an unreadable file has to be its own answer. This is the same
    shape as a gate reading its own state through a tolerant reader: an
    unreadable record is a record that has not been settled.

    A ``CratekitError`` RATHER THAN A PLAIN EXCEPTION (S4). It has always carried
    a remedy, and the command-line boundary converts anything that is not a
    structured cause into an internal defect with "report a defect" attached, so
    the remedy it carried was being discarded at the last hop. One slug covers
    every way the file can be unusable and the REMEDY is what differs between
    them, exactly as ``config-unusable`` works: a file from a newer build asks for
    an upgrade and a corrupt one asks for the doctor.
    """

    def __init__(self, message: str, *, path: Path, remedy: Remedy) -> None:
        super().__init__(
            Cause(
                reason="routing-ledger-unusable",
                message=message,
                remediation=Remediation(remedy=remedy),
                scope=Scope.RUN,
                origin=("routing_pass",),
                detail={"path": str(path)},
            )
        )
        self.path = path
        self.remedy = remedy


# ---------------------------------------------------------------------------
# The ledger
# ---------------------------------------------------------------------------


def track_id(location: str) -> str:
    """The stable identifier for one file's deferred placement.

    A digest of the DECODED, composition-normalized path, which is the only thing
    about a not-yet-imported track that is stable. It is not a display name (D5),
    it survives the file being renamed in the library's own records, and, most
    importantly, it is the same identifier whichever composition form the caller
    happened to be handed: a ledger keyed on the raw string holds two records for
    one accented filename, and the second run then places a track the first run
    already placed.
    """
    return hashlib.sha256(
        locations.location_to_path(str(location)).encode("utf-8")
    ).hexdigest()


@dataclass(frozen=True, slots=True)
class RoutingIntent:
    """One track's decided placement, as the ledger holds it.

    NAMED ``RoutingIntent`` RATHER THAN ``Intent``, deliberately.
    :class:`cratekit.core.session.Intent` already means something else entirely,
    a session's declared purpose, and this module is imported alongside that one
    by anything that routes. The repository already carries three collisions of
    exactly this shape, recorded rather than resolved because outside code holds
    the names; this one had never been seen by anything, so it cost one word.

    Every field that names a place is a STABLE IDENTIFIER: the tree, the bucket
    and the sub are taxonomy identifiers, never the display names rekordbox
    shows. R19 and D5 both require it, and the concrete reason is that a user
    renaming a folder must not orphan the record of what was meant to go in it.
    The display names are resolved from the active taxonomy at write time.
    """

    track: str
    session_id: str
    location: str
    tree: str
    bucket: str
    sub: str
    state: TrackState = TrackState.INTENDED
    decided: str = ""
    settled: str | None = None
    actor: str | None = None
    note: str | None = None

    def __post_init__(self) -> None:
        for name in ("track", "session_id", "location", "tree", "bucket", "sub"):
            if not str(getattr(self, name)).strip():
                raise ValueError(
                    f"a routing intent needs a {name}; a record that cannot say "
                    f"which track it describes, or where it was going, is worse "
                    f"than no record because it still blocks the run from closing"
                )
        if self.state is TrackState.ACKNOWLEDGED and not (self.actor or "").strip():
            raise ValueError(
                f"the track {self.track!r} is acknowledged with no actor; "
                f"acknowledging is a person saying a track is gone, and a record "
                f"that cannot say who said it is not an acknowledgment"
            )

    def to_json(self) -> dict[str, Any]:
        return {
            "track": self.track,
            "session": self.session_id,
            "location": self.location,
            "tree": self.tree,
            "bucket": self.bucket,
            "sub": self.sub,
            "state": str(self.state),
            "decided": self.decided,
            "settled": self.settled,
            "actor": self.actor,
            "note": self.note,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> RoutingIntent:
        return cls(
            track=str(data["track"]),
            session_id=str(data["session"]),
            location=str(data["location"]),
            tree=str(data["tree"]),
            bucket=str(data["bucket"]),
            sub=str(data["sub"]),
            state=TrackState(str(data.get("state", TrackState.INTENDED))),
            decided=str(data.get("decided") or ""),
            settled=data.get("settled"),
            actor=data.get("actor"),
            note=data.get("note"),
        )


def _key(intent: RoutingIntent) -> tuple[str, str]:
    """What identifies one record: the RUN and the track, never the track alone.

    A ledger keyed on the track alone cannot represent "run A owes this file" and
    "run B owes this file" at once, and two runs touching one file is ordinary: a
    re-download to the same path, a resumed intake, one track acquired from two
    sources. With one record per file the second run takes ownership of the
    first run's obligation, so the first run's close gate sees nothing
    outstanding and closes over a track that is in no playlist. The same key is
    what stops one run's mark from settling another run's record, whose
    destination was never written.
    """
    return (intent.session_id, intent.track)


@dataclass(frozen=True, slots=True)
class Ledger:
    """Every deferred placement this library holds, settled or not.

    Records are a TUPLE rather than a mapping, for the reason the tree registry
    gives for the same choice: it keeps the identifier out of every key position,
    so the R19 guard has nothing to interpret and no future reader is tempted to
    key it on something a user can rename.
    """

    intents: tuple[RoutingIntent, ...] = ()

    def intent(self, session_id: str, track: str) -> RoutingIntent | None:
        """One run's record for one track. BOTH halves of the key are required.

        A lookup by track alone would return whichever run's record happened to
        be first, and the two records mean different destinations.
        """
        for entry in self.intents:
            if entry.session_id == session_id and entry.track == track:
                return entry
        return None

    def for_session(self, session_id: str) -> tuple[RoutingIntent, ...]:
        return tuple(entry for entry in self.intents if entry.session_id == session_id)

    def outstanding(self, session_id: str | None = None) -> tuple[RoutingIntent, ...]:
        """Every intent that has not settled. DERIVED from state, always.

        ``session_id`` of None asks the question of the whole library, which is
        what a doctor check wants; a run asks it of itself.
        """
        return tuple(
            entry
            for entry in self.intents
            if entry.state in OUTSTANDING
            and (session_id is None or entry.session_id == session_id)
        )

    def with_intents(self, intents: Iterable[RoutingIntent]) -> Ledger:
        """This ledger plus ``intents``, replacing any record for the same run and track.

        Pure, so a caller can compose a change and inspect it before anything
        reaches the disk. Replacing rather than appending is what makes recording
        the same decision twice a no-op instead of a duplicate, and keying the
        replacement on :func:`_key` is what stops a second run's decision from
        being a replacement at all.
        """
        merged = {_key(entry): entry for entry in self.intents}
        for entry in intents:
            merged[_key(entry)] = entry
        return Ledger(tuple(sorted(merged.values(), key=_key)))

    def marked(
        self,
        tracks: Iterable[str],
        state: TrackState,
        *,
        session_id: str,
        when: str,
        actor: str | None = None,
        note: str | None = None,
    ) -> Ledger:
        """One run's ``tracks`` moved to ``state``. Unknown tracks are ignored.

        Ignored rather than refused, because the caller that asks is a pass
        reporting what it just wrote, and a track that has since been removed
        from the ledger by another process is not this pass's problem to raise.

        ``session_id`` IS REQUIRED, not defaulted and not optional. A mark that
        matched on the track alone settled every run's record for that file,
        including a run whose destination was never written, and the settled
        record is what the close gate reads.
        """
        wanted = frozenset(str(track) for track in tracks)
        return Ledger(
            tuple(
                replace(
                    entry,
                    state=state,
                    settled=when,
                    actor=actor if actor is not None else entry.actor,
                    note=note if note is not None else entry.note,
                )
                if entry.session_id == session_id and entry.track in wanted
                else entry
                for entry in self.intents
            )
        )


#: The ledger every library starts with, and what an absent file resolves to.
#: Named, because "nothing deferred" is a real answer rather than a missing one.
EMPTY = Ledger()


def path_for(cfg: config.Config) -> Path:
    """Where the ledger lives, resolved through the state inventory.

    Through ``state_path`` rather than composed here. A module that builds its
    own path under a state root has invented a state file the inventory does not
    know about, so nothing that walks the inventory will snapshot it, and this
    entry is COUPLED precisely so a restore rolls it back with the memberships it
    describes.
    """
    return config.state_path(STATE_KEY, cfg)


def read(cfg: config.Config) -> Ledger:
    """The effective ledger for this library. An absent file is the empty one."""
    path = path_for(cfg)
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return EMPTY
    except OSError as exc:
        raise RoutingLedgerUnreadable(
            f"{path} exists and could not be read: {exc}",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        ) from exc

    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RoutingLedgerUnreadable(
            f"{path} is not readable as JSON: {exc}", path=path, remedy=Remedy.RUN_DOCTOR
        ) from exc
    if not isinstance(data, dict):
        raise RoutingLedgerUnreadable(
            f"{path} does not hold an object at its top level",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )

    version = data.get("schema_version")
    if not isinstance(version, int):
        raise RoutingLedgerUnreadable(
            f"{path} carries no integer schema_version, so nothing can be said "
            f"about the shape of what follows it",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    if version > SCHEMA_VERSION:
        raise RoutingLedgerUnreadable(
            f"{path} was written at schema version {version}; this build "
            f"understands {SCHEMA_VERSION}",
            path=path,
            remedy=Remedy.UPGRADE_CRATEKIT,
        )

    entries = data.get("intents")
    if not isinstance(entries, list):
        raise RoutingLedgerUnreadable(
            f"{path} has no intents array", path=path, remedy=Remedy.RUN_DOCTOR
        )

    records: list[RoutingIntent] = []
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise RoutingLedgerUnreadable(
                f"{path} holds an intent that is not an object",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        try:
            record = RoutingIntent.from_json(entry)
        except (KeyError, ValueError) as exc:
            # Refused rather than dropped. A dropped record reads as "that track
            # was never deferred", which is the one misreading that lets a run
            # close over a track sitting in no playlist.
            raise RoutingLedgerUnreadable(
                f"{path} holds an unusable intent: {exc}",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            ) from exc
        if _key(record) in seen:
            raise RoutingLedgerUnreadable(
                f"{path} holds two records for the track {record.track!r} in the "
                f"run {record.session_id!r}; a ledger that gives two answers for "
                f"one run's track cannot say whether it settled, and resolving "
                f"that by line order decides whether a run closes",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        seen.add(_key(record))
        records.append(record)
    return Ledger(tuple(sorted(records, key=_key)))


def write(cfg: config.Config, ledger: Ledger) -> Path:
    """Persist ``ledger`` for this library, atomically and owner only.

    Through ``config.atomic_write_bytes``, which applies the explicit file mode
    AND creates the enclosing directories at the explicit directory mode. Both
    halves matter (P1): a 0600 record inside a world-writable directory can be
    unlinked and replaced by any local account, and this record decides whether a
    run may report itself finished.
    """
    payload = {
        "schema_version": SCHEMA_VERSION,
        # Sorted so the bytes are a function of the content alone. An unordered
        # dump makes every write a difference even when nothing changed.
        "intents": [entry.to_json() for entry in sorted(ledger.intents, key=_key)],
    }
    path = path_for(cfg)
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


def lock_path(cfg: config.Config) -> Path:
    """Where the ledger's exclusive lock lives, resolved through the inventory.

    A DECLARED entry rather than a path composed here, for the reason every other
    state file is declared: a file the inventory does not know about is a file
    nothing walks, backs up, or clears. It sits in the never-restored half
    alongside the two other locks, because a restore that replaced the directory
    holding it would swap the inode a live lock is held on and both holders would
    go on believing they had exclusive access.
    """
    return config.state_path(LOCK_KEY, cfg)


def record_intents(cfg: config.Config, intents: Iterable[RoutingIntent]) -> Ledger:
    """Write down what this run means to place, AT THE MOMENT IT IS DECIDED.

    Read, modify, write, rather than a whole-file overwrite, because several runs
    and several sources accumulate in one ledger and a writer that replaced the
    file would erase every other run's outstanding work on each call.

    UNDER AN EXCLUSIVE LOCK, because a read-modify-write is not atomic and this
    one is documented as being performed by several processes against one file.
    Two of them interleaving erases a decision that was fully recorded: nothing
    is then outstanding for it, the run that made it closes clean, and the track
    it decided on is in no ledger at all. That is the same failure this module
    exists to prevent, arriving through the writer rather than through the
    reader, and the same ``fcntl`` primitive the config migration takes is used
    rather than a third implementation of one idea.
    """
    with config._exclusive_lock(lock_path(cfg)):
        updated = read(cfg).with_intents(intents)
        write(cfg, updated)
    return updated


def mark(
    cfg: config.Config,
    tracks: Iterable[str],
    state: TrackState,
    *,
    session_id: str,
    now: datetime | None = None,
    actor: str | None = None,
    note: str | None = None,
) -> Ledger:
    """Move ONE RUN's tracks to ``state`` and persist immediately.

    Re-reads before it writes, under the same exclusive lock ``record_intents``
    takes and for the same reason, so a mark never carries a stale view of the
    rest of the ledger forward over another process's work.

    ``session_id`` is required. See :meth:`Ledger.marked`.
    """
    with config._exclusive_lock(lock_path(cfg)):
        updated = read(cfg).marked(
            tracks,
            state,
            session_id=session_id,
            when=output.timestamp(now),
            actor=actor,
            note=note,
        )
        write(cfg, updated)
    return updated


def acknowledge(
    cfg: config.Config,
    tracks: Iterable[str],
    *,
    session_id: str,
    actor: str,
    note: str = "",
    now: datetime | None = None,
) -> Ledger:
    """Settle tracks nobody can place, by a NAMED person saying so.

    The only way an unplaceable track leaves the outstanding set, and it is never
    reached from the routing pass. That separation is the requirement: a pass
    that could settle a track it failed to place would make "surfaced for
    acknowledgment" and "auto-skipped" the same thing, and the whole point of
    surfacing is that somebody is told.

    Scoped to one run, like every other mark. A person answering for the run in
    front of them must not settle a second run's obligation over the same file,
    which they were never shown and never asked about.
    """
    if not str(actor).strip():
        raise ValueError(
            "acknowledging a track that cannot be placed records WHO decided it "
            "is gone; an acknowledgment with no actor is the product asserting "
            "something about itself, which is what it must never do here"
        )
    return mark(
        cfg,
        tracks,
        TrackState.ACKNOWLEDGED,
        session_id=session_id,
        now=now,
        actor=actor,
        note=note,
    )


# ---------------------------------------------------------------------------
# Reading the library: one walk, partitioned by the soft-delete marker
# ---------------------------------------------------------------------------


def content_rows(db: Any) -> Iterator[trees.ContentRow]:
    """Every collection row, as the three columns the matcher compares.

    A GENERATOR over the binding's own query, which is the natural shape for a
    whole-library read and the shape that breaks a caller who walks it twice.
    :func:`index_rows` is the only consumer here and it consumes this exactly
    once; anything else that wants to re-read must materialize it deliberately.

    A row with no recorded path is not dropped here. It resolves to no path one
    step along and drops out of the index there, which keeps the decision about
    what a path is in the one module that owns it.

    THE SOFT-DELETE MARKER IS READ, NEVER DEFAULTED, AND A ROW THAT CANNOT
    REPORT IT REFUSES. ``trees.ContentRow.deleted`` has no default on purpose,
    and its comment gives the reason: False means active, which is the permissive
    answer, so a producer that supplies it hands every tombstone to the matcher
    as a live row. This is that producer. Supplying the default through
    ``getattr`` re-introduced exactly what U18 refused, and the cost is concrete:
    against a real database with one row genuinely soft-deleted, a binding that
    stops exposing the column makes the pass place the deleted track, mark it
    routed, and close the run over it.

    THE READ ITSELF MOVED to :func:`cratekit.write.trees.soft_delete_marker`,
    beside the field whose missing default it defends, when U24 added a second
    producer that asks the opposite question of the same column. Two copies of
    this rule would agree today and disagree eventually, and one of the two
    directions it can disagree in trashes a live file.
    """
    for row in db.get_content():
        yield trees.ContentRow(
            content_id=str(row.ID),
            recorded=str(getattr(row, "FolderPath", "") or ""),
            deleted=trees.soft_delete_marker(row),
        )


@dataclass(frozen=True, slots=True)
class RowIndex:
    """The library's rows, walked once and split by the soft-delete marker.

    BOTH halves are indexed by :func:`cratekit.write.trees.index_active_rows`,
    the same single locate the membership writer uses, with the marker cleared on
    the tombstoned half so that one function answers "which location is this"
    for both. A second normalization written here would be a second locate, and
    two locates that resolve one name differently eventually disagree about which
    row they mean, which is how a track gets placed twice under two identities.

    The materialized rows are kept, not only the indexes, because the membership
    writer builds its own index from rows and handing it the caller's exhausted
    iterator would report every track absent while the run reported clean.
    """

    active: tuple[trees.ContentRow, ...]
    tombstoned: tuple[trees.ContentRow, ...]
    by_active_location: Mapping[str, tuple[str, ...]]
    by_tombstoned_location: Mapping[str, tuple[str, ...]]


def index_rows(
    rows: Iterable[trees.ContentRow],
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule] = (),
) -> RowIndex:
    """Walk the collection ONCE and index both halves of it.

    Once, because the caller's rows are a database cursor in the only shape that
    matters, and a function that walked them twice would see an empty library the
    second time. The partition happens during that single walk and the two
    indexes are built from the two lists afterwards.
    """
    active: list[trees.ContentRow] = []
    tombstoned: list[trees.ContentRow] = []
    for row in rows:
        if row.deleted:
            # The marker is cleared so the SHARED index function, whose whole
            # rule is that a tombstone cannot claim a location, will index these
            # at all. The rule is not being weakened: it is being asked of the
            # other half of the same partition.
            tombstoned.append(replace(row, deleted=False))
        else:
            active.append(row)
    return RowIndex(
        active=tuple(active),
        tombstoned=tuple(tombstoned),
        by_active_location=trees.index_active_rows(active, root=root, prefix_map=prefix_map),
        by_tombstoned_location=trees.index_active_rows(
            tombstoned, root=root, prefix_map=prefix_map
        ),
    )


# ---------------------------------------------------------------------------
# Resolving a stable destination into the two names the writer needs
# ---------------------------------------------------------------------------


def destination(declared: taxonomy.Taxonomy, bucket_id: str, sub_id: str) -> tuple[str, str]:
    """The folder and sub-playlist display names a stable destination names.

    Resolved at WRITE time from the active taxonomy, never persisted, which is
    what lets a user rename a folder between the decision and the write without
    orphaning either the record or the tracks already in it (R19, D5).

    THE FIVE SHAPES A SUB IDENTIFIER CAN TAKE, in the order the routing rules
    themselves produce them: a bucket that routes by source genre names one of
    its own subs; a bucket with no energy dimension names its single sub; a
    bucket with energy and no reading names the shared sink; a bucket with a
    reading names an energy BAND, whose label the bucket may override; and an
    additive sub-class sits under every bucket. Missing any one of them would
    look complete until a library used it, so the set is checked against what
    the rules can actually return rather than against a reading of them (P4).

    An identifier none of them declares REFUSES. Falling back to the identifier
    itself would create a folder in somebody's library named after an internal
    key, which is both wrong and invisible until they look.
    """
    bucket = declared.bucket(bucket_id)
    for sub in bucket.subs:
        if sub.id == sub_id:
            return bucket.display, sub.display
    if bucket.single_sub is not None and bucket.single_sub.id == sub_id:
        return bucket.display, bucket.single_sub.display
    sink = declared.energy.no_energy_sub
    if sink is not None and sink.id == sub_id:
        return bucket.display, sink.display
    for band in declared.energy.bands:
        if band.id == sub_id:
            return bucket.display, bucket.energy.band_display.get(band.id, band.display)
    for entry in declared.sub_classes:
        if entry.id == sub_id:
            return bucket.display, entry.display
    raise KeyError(
        f"the bucket {bucket_id!r} declares no sub-playlist {sub_id!r}; the "
        f"ledger and this library's taxonomy disagree about where a track was "
        f"going, and inventing a name for it would create a folder nobody chose"
    )


@dataclass(frozen=True, slots=True)
class Placed:
    """One intent, where it was going, and what the library says about it now.

    ``folder`` and ``sub`` are display names, resolved here and used to build the
    write. They are never written back to the ledger: reading a display name is
    fine, keying a record on one is not.
    """

    intent: RoutingIntent
    placement: Placement
    folder: str
    sub: str
    content_id: str | None = None
    content_ids: tuple[str, ...] = ()


def row_placement(alive: trees.RowMatch, removed: trees.RowMatch) -> Placement:
    """Which placement one location's two row answers amount to.

    ``alive`` is the match against the live rows and ``removed`` the match against
    the tombstoned ones, produced by ONE locate each. The rule every surface that
    reports a placement reads, so the deferred pass and the inbox apply cannot
    come to call one state by two names (R-318). A destination the taxonomy no
    longer declares is not a row answer and is decided by the caller.
    """
    if alive.outcome is trees.MatchOutcome.MATCHED:
        return Placement.RESOLVED
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.AMBIGUOUS
    if alive.outcome is trees.MatchOutcome.UNRESOLVED:
        return Placement.UNRESOLVED
    if removed.outcome in (trees.MatchOutcome.MATCHED, trees.MatchOutcome.AMBIGUOUS):
        # A row exists and every one of them is a tombstone: imported once, then
        # removed in rekordbox. Distinguishable from "no row at all", and the
        # distinction is the whole of the fifth approach point.
        return Placement.WITHDRAWN
    return Placement.NOT_IMPORTED


def resolve_placements(
    intents: Sequence[RoutingIntent],
    index: RowIndex,
    declared: taxonomy.Taxonomy,
    *,
    root: Path | str,
    prefix_map: Sequence[locations.PrefixRule] = (),
) -> tuple[Placed, ...]:
    """Say, for each intent, whether the library now holds a row for it.

    Read-only and pure. Nothing here opens a session, takes a lock, or writes a
    byte, which is what lets the pass answer the readiness question before it
    decides whether to become a destructive session at all.

    Both questions go through :func:`cratekit.write.trees.match_indexed_rows`,
    once each over the whole list, so the live and the tombstoned answers for one
    location are produced by ONE locate rather than by two that could disagree.
    """
    requested = [entry.location for entry in intents]
    live = trees.match_indexed_rows(
        requested, index.by_active_location, root=root, prefix_map=prefix_map
    )
    dead = trees.match_indexed_rows(
        requested, index.by_tombstoned_location, root=root, prefix_map=prefix_map
    )

    out: list[Placed] = []
    for intent, alive, removed in zip(intents, live, dead):
        try:
            folder, sub = destination(declared, intent.bucket, intent.sub)
        except KeyError:
            # PER TRACK, never out of the pass. Resolving the display names used
            # to raise from here, and this loop runs over every intent including
            # the ones whose placement will never be written, so one record
            # naming a sub the template dropped aborted the whole pass: nothing
            # placed, nothing reported, every track still outstanding, and a run
            # that can never close. The refusal that gate raises promises the
            # pass "reports one reason per track it could not place", and this is
            # that reason for this track.
            out.append(
                Placed(
                    intent=intent,
                    placement=Placement.UNDECLARED,
                    folder="",
                    sub="",
                )
            )
            continue
        placement = row_placement(alive, removed)
        if placement is Placement.RESOLVED:
            content_id, ids = alive.content_id, ()
        elif placement is Placement.AMBIGUOUS:
            content_id, ids = None, alive.content_ids
        elif placement is Placement.WITHDRAWN:
            content_id, ids = removed.content_id, removed.content_ids
        else:
            content_id, ids = None, ()
        out.append(
            Placed(
                intent=intent,
                placement=placement,
                folder=folder,
                sub=sub,
                content_id=content_id,
                content_ids=ids,
            )
        )
    return tuple(out)


def readiness(placed: Sequence[Placed]) -> Readiness:
    """Whether the library holds rows for the tracks this run is waiting on.

    THE SIGNAL IS ROW PRESENCE, and it is fail-safe in the direction that costs
    nothing: run the pass before the import and every location reaches no row at
    all, so the answer is not-ready, and a not-ready pass resolves nothing and
    marks nothing.

    Nothing pending is READY rather than not-ready. The two would otherwise be
    indistinguishable, and a run with nothing left to place would be refused on
    the grounds that an import it does not need has not happened.

    AN ANSWERLESS PLACEMENT IS ITS OWN ANSWER, and this is the contradiction the
    two-member version carried. An unresolvable location reaches no row because
    no prefix maps it, and a destination the template dropped reaches no row
    because it was never asked; neither says anything about whether an import
    happened, and both are answered by fixing configuration. Returning not-ready
    for them tells a person to import a track they already imported, and they
    will be told the same thing next time. So a run that reached no row at all,
    and could not even ask the question for one of its tracks, gets the third
    answer. It writes exactly as little as not-ready does.
    """
    if not placed:
        return Readiness.READY
    if any(item.placement in IMPORTED for item in placed):
        return Readiness.READY
    if any(item.placement in ANSWERLESS for item in placed):
        return Readiness.UNANSWERABLE
    return Readiness.NOT_READY


# ---------------------------------------------------------------------------
# The recovery path, and the one thing a display name cannot survive
# ---------------------------------------------------------------------------


def _folders_holding(db: Any, content_id: str | None, *, root_id: str) -> set[str]:
    """The folders DIRECTLY under ``root_id`` whose playlists already hold this row.

    The same walk :func:`membership_proven` makes and for the same reason: it
    starts from a membership row that exists and climbs, so it cannot be fooled
    by a namesake somewhere else in the library.
    """
    found: set[str] = set()
    if content_id is None:
        return found
    for membership in db.get_playlist_songs(ContentID=str(content_id)):
        if rb_writer.membership_removed(membership):
            continue
        playlist = db.get_playlist(ID=str(membership.PlaylistID))
        if playlist is None:
            continue
        folder = db.get_playlist(ID=str(playlist.ParentID))
        if folder is None or str(folder.ParentID) != str(root_id):
            continue
        found.add(str(folder.Name))
    return found


def assert_destinations_are_not_renamed(
    db: Any,
    group: Sequence[Placed],
    declared: taxonomy.Taxonomy,
    *,
    tree_id: str,
    root_id: str,
) -> None:
    """Refuse a write that would file a track twice under two names for one place.

    THE RECOVERY PRIMITIVE IS "RE-RUN", AND IT IS KEYED ON A DISPLAY NAME. The
    whole module rests on a crash between the commit and the mark costing nothing
    because membership deduplicates, and the dedup happens in the find-or-create
    helpers, which target by the name rekordbox shows. Rename that folder, in
    rekordbox or in the template, and the next run finds nothing by the new name,
    creates the destination a second time, adds the track again, and marks it
    routed. R19 says renaming a folder changes nothing and D5 forbids keying a
    persisted record by a display name; this is the same lesson arriving on the
    recovery path.

    THE NODE MAP IS READ FIRST. A previous write records each destination's
    playlist identifiers through :func:`cratekit.core.convergence.record_nodes`,
    and :func:`cratekit.write.rebuild.resolve_destinations` resolves a rename
    through those identifiers. This refusal is the leftover: it fires only when
    that map cannot name the folder the track already sits in, so writing by
    the declared display name would create the destination a second time.

    THE CONDITION IS NARROW ON PURPOSE (P7). It fires only when the destination
    folder is not under the adopted root AND the track already sits under that
    root inside a folder the taxonomy declares no bucket for. A track being
    placed into a second, genuinely new bucket while it sits in a first, declared
    one is the ordinary case and is untouched. What remains is a person's own
    folder under a governed tree root holding this exact track at the moment its
    bucket folder is first created, and refusing there is honest rather than
    silent.
    """
    children = {str(row.Name) for row in db.get_playlist(ParentID=str(root_id))}
    for item in group:
        if item.folder in children:
            continue
        orphaned = sorted(
            name
            for name in _folders_holding(db, item.content_id, root_id=root_id)
            if declared.bucket_for_display(name) is None
        )
        if not orphaned:
            continue
        raise refuse(
            "routing-destination-renamed",
            f"the track already sits in the tree {tree_id!r} under {orphaned!r}, "
            f"which this library's taxonomy names no bucket for, and the "
            f"destination it was decided for is not there at all; writing it now "
            f"would create that destination a second time and file one track in "
            f"both, so the pass refuses rather than duplicating it",
            remedy=Remedy.REBUILD_TREE,
            steps=(
                "a folder renamed in rekordbox is renamed back, or the taxonomy "
                "is edited to declare the name the library now uses",
                "a track that belongs in the folder under its new name is moved "
                "there by hand, and the run's record is then acknowledged",
            ),
            scope=Scope.RUN,
            origin=("routing_pass",),
            detail={
                "tree_id": tree_id,
                "track": item.intent.track,
                "session_id": item.intent.session_id,
                "found_under": orphaned,
            },
        )


def _converge_destinations(
    cfg: config.Config,
    db: Any,
    group: Sequence[Placed],
    declared: taxonomy.Taxonomy,
    *,
    tree_id: str,
    root_id: str,
) -> list[Placed]:
    """Rewrite each placement through the node map a previous write recorded.

    Imported lazily because :mod:`cratekit.write.rebuild` already imports this
    module at the top. A cycle at import time would take both modules out of
    collection.
    """
    from cratekit.write import rebuild

    placements = [
        rebuild.DeclaredPlacement(item.intent.location, item.intent.bucket, item.intent.sub)
        for item in group
    ]
    standing = rebuild.read_tree(db, root_id)
    record = convergence.read(cfg).tree(tree_id)
    destinations = rebuild.resolve_destinations(declared, placements, standing, record)
    by_key = {(entry.bucket, entry.sub): entry for entry in destinations}
    remapped: list[Placed] = []
    for item in group:
        destination = by_key.get((item.intent.bucket, item.intent.sub))
        if destination is None:
            remapped.append(item)
            continue
        remapped.append(replace(item, folder=destination.folder, sub=destination.playlist))
    return remapped


def _record_routed_nodes(
    cfg: config.Config,
    db: Any,
    group: Sequence[Placed],
    *,
    tree_id: str,
    root_id: str,
) -> None:
    """Persist the playlist identifiers this pass just wrote, merging per tree.

    Merged, not replaced. This pass looks at the destinations it placed, not
    at every destination the tree has ever held, and a whole-record replace
    would drop the ones it did not touch.
    """
    from cratekit.write import rebuild

    standing = rebuild.read_tree(db, root_id)
    by_display: dict[tuple[str, str], list[Any]] = {}
    for node in standing:
        by_display.setdefault((node.folder_display, node.playlist_display), []).append(node)
    recorded: list[convergence.DestinationNode] = []
    seen: set[tuple[str, str]] = set()
    for item in group:
        key = (item.intent.bucket, item.intent.sub)
        if key in seen:
            continue
        seen.add(key)
        candidates = by_display.get((item.folder, item.sub), ())
        if len(candidates) != 1:
            continue
        node = candidates[0]
        recorded.append(
            convergence.DestinationNode(
                bucket=item.intent.bucket,
                sub=item.intent.sub,
                folder_id=node.folder_id,
                playlist_id=node.playlist_id,
            )
        )
    if recorded:
        convergence.assert_injective(tree_id, recorded)
        convergence.record_nodes(cfg, tree_id, recorded)


# ---------------------------------------------------------------------------
# The pass: commit, prove, then mark
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RoutingReport:
    """What one pass placed, and everything it could not.

    A report rather than a stream of prints, because this layer has no console
    and because the two lists below are what a CLI turns into the sentence a
    person acts on. ``routed`` is the tracks this pass MARKED, which is a
    narrower set than the tracks it wrote: a write whose read-back cannot be
    proved leaves the track outstanding on purpose.
    """

    session_id: str
    readiness: Readiness
    placed: tuple[Placed, ...] = ()
    routed: tuple[str, ...] = ()
    memberships: tuple[trees.MembershipReport, ...] = ()

    @property
    def unsettled(self) -> tuple[Placed, ...]:
        """Every placement this pass did not settle, in the order it saw them."""
        landed = frozenset(self.routed)
        return tuple(item for item in self.placed if item.intent.track not in landed)

    @property
    def withdrawn(self) -> tuple[Placed, ...]:
        """The tracks somebody deleted, which only a person can settle.

        Surfaced here rather than swallowed, because an auto-skip and a
        successful placement look identical from outside and one of them is a
        lie about the user's library.
        """
        return tuple(item for item in self.placed if item.placement is Placement.WITHDRAWN)


def membership_proven(db: Any, placed: Placed, *, root_id: str) -> bool:
    """Read the library back and say whether this track really is where it belongs.

    THE WALK GOES UP, FROM THE MEMBERSHIP ROW TO THE ROOT, never down by name.
    A lookup by name finds a namesake anywhere in the library and reports
    success, which is the silent parallel tree arriving through the check meant
    to detect it. Starting from a membership row that actually exists and
    climbing to its playlist, its folder and the adopted root cannot resolve to
    anything but the node the write really used.

    It is also the reason nothing here calls the find-or-create helpers the write
    used. Those create when they miss, so a read-back built on them would answer
    "yes" by making the thing it was asked about true, which is a guard that
    passes because it fired.

    Returns a BOOLEAN and never raises for an absent row: a proof that cannot be
    made is a track that stays outstanding and is tried again, which is the
    fail-safe direction.

    A MEMBERSHIP MARKED REMOVED PROVES NOTHING (R-758), since rekordbox shows no
    track for it. NEITHER DOES ONE THAT CANNOT SAY, and it is passed over here
    where every other reader refuses on it: this function's contract is a
    boolean, and unproven is the direction that tries again.
    """
    if placed.content_id is None:
        return False
    for membership in db.get_playlist_songs(ContentID=str(placed.content_id)):
        try:
            if rb_writer.membership_removed(membership):
                continue
        except CratekitError:
            continue
        playlist = db.get_playlist(ID=str(membership.PlaylistID))
        if playlist is None or playlist.Name != placed.sub:
            continue
        folder = db.get_playlist(ID=str(playlist.ParentID))
        if folder is None or folder.Name != placed.folder:
            continue
        if str(folder.ParentID) == str(root_id):
            return True
    return False


def route(
    cfg: config.Config,
    db: Any,
    *,
    session_id: str,
    registry: tree_registry.Registry,
    declared: taxonomy.Taxonomy,
    rows: Iterable[trees.ContentRow],
    root_exists: Callable[[str], bool],
    analysis_roots: Iterable[Path | str],
    prefix_map: Sequence[locations.PrefixRule] | None = None,
    workflow: str = ROUTING_WORKFLOW,
    now: datetime | None = None,
) -> RoutingReport:
    """Place every outstanding track this library now holds a row for.

    THE ORDER IS THE UNIT. Resolve, then commit, then prove, then mark. A crash
    anywhere before the mark leaves the intent outstanding and the next pass
    redoes it, and redoing it is free because membership deduplicates. The
    reverse order, marking before committing, has no recovery at all: the one
    record that knew the track still needed placing already says it was placed.

    IT IS READ-ONLY UNTIL IT KNOWS THE LIBRARY IS READY. The readiness question
    is answered from rows alone, before any session is opened, so running this
    before the import writes nothing whatsoever: no lock, no snapshot, no mark.

    THE SESSION IS NOT THIS FUNCTION'S TO OPEN. Each tree's write goes through
    :func:`cratekit.write.trees.write_tree_membership`, which owns its own gates
    for the reason R29 gives: one source per run, independently committed and
    independently snapshotted. Trees are written one at a time and in sorted
    order, so a refusal on the second leaves the first committed and marked.

    ``rows`` is walked EXACTLY ONCE, here, and the materialized active half is
    what the writer is handed. A caller's rows are a database cursor in the shape
    that matters, and a second walk of an exhausted one reports every track
    absent while the run reports clean.

    THE RE-RUN CONVERGES WHEN THE NODE MAP CAN NAME THE FOLDER. A previous
    write records each destination's playlist identifiers, and the plan is
    rewritten through those identifiers before any find-or-create. A folder
    renamed between the commit and the recovery is therefore the same folder,
    not a second one. :func:`assert_destinations_are_not_renamed` still runs
    over every tree's remapped plan, and it is the leftover: it fires only
    when the map cannot name the folder the track already sits in.

    IT PLACES WHAT IT CAN AND REPORTS THE REST, one reason per track. A record
    whose destination the taxonomy no longer declares is one entry in the report
    rather than an exception out of the pass: the refusal the close gate raises
    promises a person a reason per track, and a pass that aborted on the first
    such record placed none of the good ones and gave no reason for any of them.
    """
    watched = [Path(root) for root in analysis_roots]
    pending = read(cfg).outstanding(session_id)
    rules = (
        [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]
        if prefix_map is None
        else list(prefix_map)
    )

    index = index_rows(rows, root=cfg.library.root, prefix_map=rules)
    placed = resolve_placements(pending, index, declared, root=cfg.library.root, prefix_map=rules)
    state = readiness(placed)
    if state is not Readiness.READY:
        # Nothing is opened, nothing is locked, nothing is marked. Returning here
        # rather than entering the loop with an empty plan is what makes that
        # true on the disk rather than approximately true.
        #
        # WRITTEN AS "not READY" RATHER THAN AS "is NOT_READY", which is the same
        # direction the settled and outstanding halves are derived in: only the
        # one answer that means the library is ready may write, so an answer
        # added later cannot acquire the writing behaviour by nobody having
        # classified it.
        return RoutingReport(session_id=session_id, readiness=state, placed=placed)

    by_tree: dict[str, list[Placed]] = {}
    for item in placed:
        if item.placement in WRITABLE:
            by_tree.setdefault(item.intent.tree, []).append(item)

    # READ-ONLY, AND BEFORE THE FIRST WRITE OF THE FIRST TREE. Checking inside
    # the loop would leave a refusal on the second tree standing beside a first
    # tree that was already committed and marked, and the whole point of this
    # refusal is that nothing gets filed twice. Destinations are remapped
    # through the recorded node identifiers first, so a rename the map can
    # name never reaches the leftover refusal.
    anchored = {
        tree_id: tree_registry.anchored_root(tree_id, registry, root_exists=root_exists)
        for tree_id in sorted(by_tree)
    }
    remapped: dict[str, list[Placed]] = {}
    for tree_id in sorted(by_tree):
        remapped[tree_id] = _converge_destinations(
            cfg,
            db,
            by_tree[tree_id],
            declared,
            tree_id=tree_id,
            root_id=anchored[tree_id],
        )
        assert_destinations_are_not_renamed(
            db,
            remapped[tree_id],
            declared,
            tree_id=tree_id,
            root_id=anchored[tree_id],
        )
    by_tree = remapped

    routed: list[str] = []
    reports: list[trees.MembershipReport] = []
    for tree_id in sorted(by_tree):
        group = by_tree[tree_id]
        plan: dict[tuple[str, str], list[str]] = {}
        for item in group:
            plan.setdefault((item.folder, item.sub), []).append(item.intent.location)

        report = trees.write_tree_membership(
            cfg,
            db,
            tree_id=tree_id,
            registry=registry,
            plan=plan,
            rows=index.active,
            root_exists=root_exists,
            # ONE prefix map for both sides. The writer would resolve its own
            # from configuration if this were omitted, and two resolvers reading
            # one question differently is how the pass and the write come to
            # disagree about which row a location names.
            prefix_map=rules,
            analysis_roots=watched,
            workflow=workflow,
        )
        reports.append(report)
        _record_routed_nodes(
            cfg,
            db,
            group,
            tree_id=tree_id,
            root_id=report.root_id,
        )

        proven = [
            item for item in group if membership_proven(db, item, root_id=report.root_id)
        ]
        if proven:
            mark(
                cfg,
                [item.intent.track for item in proven],
                TrackState.ROUTED,
                session_id=session_id,
                now=now,
            )
            routed.extend(item.intent.track for item in proven)
        if len(proven) != len(group):
            logger.warning(
                "%d of %d tracks committed into tree %s could not be read back and "
                "stay outstanding",
                len(group) - len(proven),
                len(group),
                tree_id,
            )

    return RoutingReport(
        session_id=session_id,
        readiness=state,
        placed=placed,
        routed=tuple(routed),
        memberships=tuple(reports),
    )


# ---------------------------------------------------------------------------
# The run that will not close while anything is still nowhere
# ---------------------------------------------------------------------------


def assert_settled(cfg: config.Config, session_id: str) -> None:
    """Refuse while this run still holds a track that reached no playlist.

    THE WHOLE POINT OF THE UNIT, stated as one refusal. A run that closed here
    would report placed tracks that sit in no tree at all, and nothing left on
    disk would know to place them: the session is over, its capture is released,
    and the intents are the only record that the work was ever owed.

    Read from the LEDGER alone, so this needs no database and no session. That
    matters because closing is the one moment when the library may legitimately
    be unmounted, and a refusal that needed the library to decide would fail for
    the wrong reason.

    The refusal is in the pending-human class rather than a failure class,
    because nothing is broken. Either the pass has not been run since the import,
    or it has run and surfaced something only a person can answer for, and the
    pass itself is what tells them which.
    """
    outstanding = read(cfg).outstanding(session_id)
    if not outstanding:
        return
    raise refuse(
        "routing-outstanding",
        f"run {session_id} still holds {len(outstanding)} track(s) whose "
        f"placement was decided and never landed, so closing it would report "
        f"them as placed while they sit in no playlist",
        remedy=Remedy.COMPLETE_PENDING_ACTION,
        steps=(
            "run the deferred routing pass over this run, which places every "
            "track the library now holds a row for, and reports one reason per "
            "track it could not place",
            "a track it reports as not yet imported needs the intake export "
            "importing first",
            "a track it reports as unresolvable needs the volume prefix map "
            "fixing, and a track it reports as claimed by two rows needs one of "
            "them removing",
            "a track it reports as going somewhere this library's taxonomy no "
            "longer declares needs that destination declaring again, or the "
            "record acknowledging by a named person",
            "a track it reports as removed from the library is settled the only "
            "way it can be, by a named person acknowledging that it is gone",
        ),
        scope=Scope.RUN,
        origin=("routing_pass",),
        detail={
            "session_id": session_id,
            "outstanding": [entry.track for entry in outstanding],
        },
    )


def assert_import_settled(record: session.SessionRecord) -> None:
    """Refuse while this run's export is still sitting there un-imported.

    THE SECOND OF THE TWO STATES IN WHICH SOMEBODY STILL OWES AN ACT, and the
    gate below used to cover only the first. ``awaiting-import`` is a first-class
    session state precisely because a run whose XML half is written and whose
    import has not happened is not finished, and
    :func:`cratekit.core.session.close_session` only ever asked whether the state
    being closed into is terminal. So a run in that state closed, released its
    capture, and left its pending action attached, while the session spine went
    on refusing a database surface for the very same record. One record cannot be
    both finished and owed.

    It reuses the ``awaiting-import`` slug rather than minting one, because it is
    the same fact about the same run that
    :func:`cratekit.core.session.assert_database_surface_allowed` reports; what
    differs is which act is being refused, and the message says which.
    """
    if record.state is not session.SessionState.AWAITING_IMPORT:
        return
    pending = record.pending
    raise refuse(
        "awaiting-import",
        f"run {record.session_id} has an export that has not been imported, so "
        f"closing it would report the run as finished and release its capture "
        f"while the rows that import creates do not exist",
        remedy=Remedy.COMPLETE_PENDING_ACTION,
        steps=tuple(pending.steps) if pending is not None else (),
        scope=Scope.RUN,
        origin=("routing_pass",),
        detail={
            "session_id": record.session_id,
            "pending_id": pending.id if pending is not None else None,
            "verify_verb": pending.verify_verb if pending is not None else None,
            "artifact": pending.artifact if pending is not None else None,
        },
    )


def close_run(
    record: session.SessionRecord,
    cfg: config.Config,
    *,
    state: session.SessionState = session.SessionState.CLOSED,
    now: datetime | None = None,
) -> session.SessionRecord:
    """Close a run, refusing while anybody still owes it an act.

    TWO GATES, BECAUSE THERE ARE TWO SUCH ACTS. A track whose placement was
    decided and never landed is one; an export nobody has imported is the other.
    Enforcing one of the two would be the same defect either way round: a run
    reporting itself finished with work outstanding and its capture released.

    CLOSING IS GATED AND ABANDONING IS NOT, deliberately. Closing is the claim
    that the run finished, and both gates are what have to back that claim up.
    Abandoning is the opposite claim, so gating it would leave somebody with a
    run they can neither finish nor give up on, and a refusal with no way past it
    is how people learn to edit state files by hand.

    The close itself is :func:`cratekit.core.session.close_session`, called
    rather than reimplemented: it owns the terminal-state rule and the record it
    writes is what releases the capture.
    """
    if state is session.SessionState.CLOSED:
        assert_import_settled(record)
        assert_settled(cfg, record.session_id)
    return session.close_session(record, cfg, state=state, now=now)


__all__ = [
    "ANSWERLESS",
    "EMPTY",
    "IMPORTED",
    "LOCK_KEY",
    "OUTSTANDING",
    "ROUTING_WORKFLOW",
    "SCHEMA_VERSION",
    "SETTLED",
    "STATE_KEY",
    "WRITABLE",
    "Ledger",
    "Placed",
    "Placement",
    "Readiness",
    "RoutingIntent",
    "RoutingLedgerUnreadable",
    "RoutingReport",
    "RowIndex",
    "TrackState",
    "acknowledge",
    "assert_destinations_are_not_renamed",
    "assert_import_settled",
    "assert_settled",
    "close_run",
    "lock_path",
    "content_rows",
    "destination",
    "index_rows",
    "mark",
    "membership_proven",
    "route",
    "path_for",
    "read",
    "readiness",
    "record_intents",
    "resolve_placements",
    "row_placement",
    "track_id",
    "write",
]
