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
pass that cannot tell whether the import happened must behave exactly like a pass
that knows it has not.

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
from cratekit.core import config, locations, session, taxonomy, tree_registry
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.write import trees

logger = logging.getLogger(__name__)

#: The state entry this module owns. Named once, so the resolver and every caller
#: cannot disagree about which file is meant.
STATE_KEY = "routing_intents"

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

    Five answers rather than placed-or-not, because four of these are different
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


class Readiness(StrEnum):
    """Whether the library holds rows for the tracks this run is waiting on."""

    READY = "ready"
    NOT_READY = "not-ready"


class RoutingLedgerUnreadable(Exception):
    """The ledger exists and cannot be understood.

    Deliberately NOT collapsed into "no records". An empty ledger reads as
    "nothing is outstanding", which admits exactly the close this module exists
    to refuse, so an unreadable file has to be its own answer. This is the same
    shape as a gate reading its own state through a tolerant reader: an
    unreadable record is a record that has not been settled.
    """

    def __init__(self, message: str, *, path: Path, remedy: Remedy) -> None:
        super().__init__(message)
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


@dataclass(frozen=True, slots=True)
class Ledger:
    """Every deferred placement this library holds, settled or not.

    Records are a TUPLE rather than a mapping, for the reason the tree registry
    gives for the same choice: it keeps the identifier out of every key position,
    so the R19 guard has nothing to interpret and no future reader is tempted to
    key it on something a user can rename.
    """

    intents: tuple[RoutingIntent, ...] = ()

    def intent(self, track: str) -> RoutingIntent | None:
        for entry in self.intents:
            if entry.track == track:
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
        """This ledger plus ``intents``, replacing any record for the same track.

        Pure, so a caller can compose a change and inspect it before anything
        reaches the disk. Replacing rather than appending is what makes recording
        the same decision twice a no-op instead of a duplicate.
        """
        merged = {entry.track: entry for entry in self.intents}
        for entry in intents:
            merged[entry.track] = entry
        return Ledger(tuple(sorted(merged.values(), key=lambda e: e.track)))

    def marked(
        self,
        tracks: Iterable[str],
        state: TrackState,
        *,
        when: str,
        actor: str | None = None,
        note: str | None = None,
    ) -> Ledger:
        """This ledger with ``tracks`` moved to ``state``. Unknown tracks are ignored.

        Ignored rather than refused, because the caller that asks is a pass
        reporting what it just wrote, and a track that has since been removed
        from the ledger by another process is not this pass's problem to raise.
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
                if entry.track in wanted
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
    seen: set[str] = set()
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
        if record.track in seen:
            raise RoutingLedgerUnreadable(
                f"{path} holds two records for the track {record.track!r}; a "
                f"ledger that gives two answers for one track cannot say whether "
                f"it settled, and resolving that by line order decides whether a "
                f"run closes",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        seen.add(record.track)
        records.append(record)
    return Ledger(tuple(sorted(records, key=lambda e: e.track)))


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
        "intents": [entry.to_json() for entry in sorted(ledger.intents, key=lambda e: e.track)],
    }
    path = path_for(cfg)
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


def record_intents(cfg: config.Config, intents: Iterable[RoutingIntent]) -> Ledger:
    """Write down what this run means to place, AT THE MOMENT IT IS DECIDED.

    Read, modify, write, rather than a whole-file overwrite, because several runs
    and several sources accumulate in one ledger and a writer that replaced the
    file would erase every other run's outstanding work on each call.
    """
    updated = read(cfg).with_intents(intents)
    write(cfg, updated)
    return updated


def mark(
    cfg: config.Config,
    tracks: Iterable[str],
    state: TrackState,
    *,
    now: datetime | None = None,
    actor: str | None = None,
    note: str | None = None,
) -> Ledger:
    """Move tracks to ``state`` and persist immediately.

    Re-reads before it writes, so a mark never carries a stale view of the rest
    of the ledger forward over another process's work.
    """
    updated = read(cfg).marked(
        tracks, state, when=output.timestamp(now), actor=actor, note=note
    )
    write(cfg, updated)
    return updated


def acknowledge(
    cfg: config.Config,
    tracks: Iterable[str],
    *,
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
    """
    if not str(actor).strip():
        raise ValueError(
            "acknowledging a track that cannot be placed records WHO decided it "
            "is gone; an acknowledgment with no actor is the product asserting "
            "something about itself, which is what it must never do here"
        )
    return mark(cfg, tracks, TrackState.ACKNOWLEDGED, now=now, actor=actor, note=note)


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
    """
    for row in db.get_content():
        yield trees.ContentRow(
            content_id=str(row.ID),
            recorded=str(getattr(row, "FolderPath", "") or ""),
            deleted=bool(getattr(row, "rb_local_deleted", 0)),
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
        folder, sub = destination(declared, intent.bucket, intent.sub)
        if alive.outcome is trees.MatchOutcome.MATCHED:
            placement, content_id, ids = Placement.RESOLVED, alive.content_id, ()
        elif alive.outcome is trees.MatchOutcome.AMBIGUOUS:
            placement, content_id, ids = Placement.AMBIGUOUS, None, alive.content_ids
        elif alive.outcome is trees.MatchOutcome.UNRESOLVED:
            placement, content_id, ids = Placement.UNRESOLVED, None, ()
        elif removed.outcome in (trees.MatchOutcome.MATCHED, trees.MatchOutcome.AMBIGUOUS):
            # A row exists and every one of them is a tombstone: imported once,
            # then removed in rekordbox. Distinguishable from "no row at all",
            # and the distinction is the whole of the fifth approach point.
            placement = Placement.WITHDRAWN
            content_id = removed.content_id
            ids = removed.content_ids
        else:
            placement, content_id, ids = Placement.NOT_IMPORTED, None, ()
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

    An unresolvable location is deliberately NOT evidence of an import. It
    reaches no row for a configuration reason, and counting it as "the import has
    not happened" would send a person back to import something they already have.
    """
    if not placed:
        return Readiness.READY
    if any(item.placement in IMPORTED for item in placed):
        return Readiness.READY
    return Readiness.NOT_READY


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
    """
    if placed.content_id is None:
        return False
    for membership in db.get_playlist_songs(ContentID=str(placed.content_id)):
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
    if state is Readiness.NOT_READY:
        # Nothing is opened, nothing is locked, nothing is marked. Returning here
        # rather than entering the loop with an empty plan is what makes that
        # true on the disk rather than approximately true.
        return RoutingReport(session_id=session_id, readiness=state, placed=placed)

    by_tree: dict[str, list[Placed]] = {}
    for item in placed:
        if item.placement in WRITABLE:
            by_tree.setdefault(item.intent.tree, []).append(item)

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

        proven = [
            item for item in group if membership_proven(db, item, root_id=report.root_id)
        ]
        if proven:
            mark(cfg, [item.intent.track for item in proven], TrackState.ROUTED, now=now)
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


def close_run(
    record: session.SessionRecord,
    cfg: config.Config,
    *,
    state: session.SessionState = session.SessionState.CLOSED,
    now: datetime | None = None,
) -> session.SessionRecord:
    """Close a run, refusing while its routing is outstanding.

    CLOSING IS GATED AND ABANDONING IS NOT, deliberately. Closing is the claim
    that the run finished, and the routing is what has to back that claim up.
    Abandoning is the opposite claim, so gating it would leave somebody with a
    run they can neither finish nor give up on, and a refusal with no way past it
    is how people learn to edit state files by hand.

    The close itself is :func:`cratekit.core.session.close_session`, called
    rather than reimplemented: it owns the terminal-state rule and the record it
    writes is what releases the capture.
    """
    if state is session.SessionState.CLOSED:
        assert_settled(cfg, record.session_id)
    return session.close_session(record, cfg, state=state, now=now)


__all__ = [
    "EMPTY",
    "IMPORTED",
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
    "assert_settled",
    "close_run",
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
    "track_id",
    "write",
]
