"""Deferred routing: what a run meant to place, and whether it ever landed (U19).

A new track's placement is decided during acquisition, when the library holds
no row for it; the row appears only when a person imports the intake export.
Everything here follows from that gap, through four properties.

**The decision is persisted when it is MADE**, so the process that picks the
work up after a crash reads what its predecessor believed.

**The mark comes AFTER the commit, never before.** A track becomes routed only
once its membership is committed and a read-back proves it. A crash in between
costs a re-run, cheap because membership deduplicates; a mark before a commit
that never happens strands the track for good.

**Outstanding is DERIVED from per-track state.** There is no completion flag,
since a flag beside the states is a second answer that a crash makes disagree.

**Readiness is row presence, read-only, and fail-safe.** Before the import the
pass resolves nothing, marks nothing and opens nothing. A pass that cannot tell
whether the import happened BEHAVES like one that knows it has not, but
REPORTS differently: a location no prefix maps, or a destination no longer
declared, is fixed by configuration and never by importing, so the question
has three answers rather than two.

rekordbox soft-deletes, so a track imported then removed still has a row with
the removal marker. It is surfaced as withdrawn, never skipped: a skip looks
like a placement that worked.

LAYER: write. It calls the session spine rather than rebuilding it, and NAMES
NO VERB (D2): the CLI layer renders commands from a remediation token.
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

#: The state entry this module owns, named once.
STATE_KEY = "routing_intents"

#: The lock that serializes every read-modify-write of the entry above, a
#: declared entry so the inventory knows the file.
LOCK_KEY = "routing_intents_lock"

#: Bumped only when the on-disk shape changes incompatibly. A newer build's
#: file is refused rather than guessed at, since a misread could close a run.
SCHEMA_VERSION = 1

#: The workflow name the membership write records in the session log, an
#: operation and not a verb (D2).
ROUTING_WORKFLOW = "deferred-routing"


class TrackState(StrEnum):
    """Where one track's deferred placement got to.

    ``ACKNOWLEDGED`` is not a flavour of routed: it records a person saying a track
    this pass could not place is gone, and fusing the two would falsify the report.
    """

    INTENDED = "intended"
    ROUTED = "routed"
    ACKNOWLEDGED = "acknowledged"


#: The states that settle a track. Listed, with OUTSTANDING derived, so a
#: state added later lands outstanding and cannot close a run by omission.
SETTLED: frozenset[TrackState] = frozenset({TrackState.ROUTED, TrackState.ACKNOWLEDGED})

#: Everything else, derived from the enum so the two halves cannot both miss a
#: member (P3).
OUTSTANDING: frozenset[TrackState] = frozenset(TrackState) - SETTLED


class Placement(StrEnum):
    """Why one intent did or did not reach a single active row this pass.

    Six answers, since fusing any two reports one problem as another; above all
    ``NOT_IMPORTED``, answered by importing, against ``WITHDRAWN``, which never is.
    """

    #: Exactly one active row. This is the only placement that gets written.
    RESOLVED = "resolved"
    #: No row at all, of any kind. The import has not happened for this track.
    NOT_IMPORTED = "not-imported"
    #: Every row carries the soft-delete marker: imported, then removed.
    WITHDRAWN = "withdrawn"
    #: Two or more active rows claim the location; U18 writes neither.
    AMBIGUOUS = "ambiguous"
    #: The recorded location resolves to no path on this machine: a
    #: configuration failure, never a missing import.
    UNRESOLVED = "unresolved"
    #: The destination this ledger names is no longer declared by the active
    #: taxonomy. PER TRACK, so one stale record cannot abort the whole pass.
    UNDECLARED = "undeclared"


#: The placements a membership write may be built from, named so widening it
#: is one deliberate edit.
WRITABLE: frozenset[Placement] = frozenset({Placement.RESOLVED})

#: The placements that count as evidence the import HAPPENED: the location
#: reached a row of some kind. ``UNRESOLVED`` is not, since importing cannot fix it.
IMPORTED: frozenset[Placement] = frozenset(
    {Placement.RESOLVED, Placement.WITHDRAWN, Placement.AMBIGUOUS}
)

#: The placements that say NOTHING about whether the import happened, derived
#: so a member added later lands here, neither evidence nor a missing import (P3).
ANSWERLESS: frozenset[Placement] = (
    frozenset(Placement) - IMPORTED - {Placement.NOT_IMPORTED}
)


class Readiness(StrEnum):
    """Whether the library holds rows for the tracks this run is waiting on.

    ``NOT_READY`` says the rows are not there yet and importing puts them there.
    ``UNANSWERABLE`` says nothing reached a row and some intent could not be asked,
    its location mapping to no path or its destination undeclared. Both write
    nothing; only one is answered by importing.
    """

    READY = "ready"
    NOT_READY = "not-ready"
    UNANSWERABLE = "unanswerable"


class RoutingLedgerUnreadable(CratekitError):
    """The ledger exists and cannot be understood.

    Never collapsed into "no records", which would read as nothing outstanding and
    admit the close this module refuses. A ``CratekitError`` (S4), so the remedy
    survives the command-line boundary: one slug, and the remedy differs, an
    upgrade for a newer build's file and the doctor for a corrupt one.
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

    A digest of the DECODED, composition-normalized path: not a display name (D5),
    and the same whichever composition form the caller holds, so one accented
    filename never gets two records.
    """
    return hashlib.sha256(
        locations.location_to_path(str(location)).encode("utf-8")
    ).hexdigest()


@dataclass(frozen=True, slots=True)
class RoutingIntent:
    """One track's decided placement, as the ledger holds it.

    Not ``Intent``, which :class:`cratekit.core.session.Intent` already means.
    Every field naming a place is a STABLE IDENTIFIER, never a display name (R19,
    D5), so renaming a folder orphans nothing; display names resolve at write time.
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

    Two runs owing one file is ordinary, and keyed on the track alone the second
    would take over the first's obligation, letting the first close over a track
    in no playlist, or one run's mark settle another's record.
    """
    return (intent.session_id, intent.track)


@dataclass(frozen=True, slots=True)
class Ledger:
    """Every deferred placement this library holds, settled or not.

    A TUPLE rather than a mapping, as the tree registry keeps it, so no identifier
    sits in a key position for the R19 guard to interpret.
    """

    intents: tuple[RoutingIntent, ...] = ()

    def intent(self, session_id: str, track: str) -> RoutingIntent | None:
        """One run's record for one track. BOTH halves of the key are required."""
        for entry in self.intents:
            if entry.session_id == session_id and entry.track == track:
                return entry
        return None

    def for_session(self, session_id: str) -> tuple[RoutingIntent, ...]:
        return tuple(entry for entry in self.intents if entry.session_id == session_id)

    def outstanding(self, session_id: str | None = None) -> tuple[RoutingIntent, ...]:
        """Every intent that has not settled. DERIVED from state, always.

        ``session_id`` of None asks of the whole library, as a doctor check does.
        """
        return tuple(
            entry
            for entry in self.intents
            if entry.state in OUTSTANDING
            and (session_id is None or entry.session_id == session_id)
        )

    def with_intents(self, intents: Iterable[RoutingIntent]) -> Ledger:
        """This ledger plus ``intents``, replacing any record for the same run and track.

        Pure, so a change can be inspected before it reaches disk. Replacing on
        :func:`_key` makes recording one decision twice a no-op.
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

        Ignored, since another process may have removed one. ``session_id`` IS
        REQUIRED: a mark matched on the track alone settled every run's record for
        that file, including one whose destination was never written.
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
EMPTY = Ledger()


def path_for(cfg: config.Config) -> Path:
    """Where the ledger lives, resolved through the state inventory.

    Declared rather than composed, so the inventory snapshots it, and COUPLED so a
    restore rolls it back with the memberships it describes.
    """
    return config.state_path(STATE_KEY, cfg)


def read(cfg: config.Config) -> Ledger:
    """The effective ledger for this library. An absent file is the empty one."""
    path = path_for(cfg)

    def unusable(message: str) -> RoutingLedgerUnreadable:
        return RoutingLedgerUnreadable(message, path=path, remedy=Remedy.RUN_DOCTOR)

    try:
        raw = config.read_bytes_if_present(path)
    except OSError as exc:
        raise unusable(f"{path} exists and could not be read: {exc}") from exc
    if raw is None:
        return EMPTY

    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise unusable(f"{path} is not readable as JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise unusable(f"{path} does not hold an object at its top level")

    version = data.get("schema_version")
    if not isinstance(version, int):
        raise unusable(
            f"{path} carries no integer schema_version, so nothing can be said "
            f"about the shape of what follows it"
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
        raise unusable(f"{path} has no intents array")

    records: list[RoutingIntent] = []
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise unusable(f"{path} holds an intent that is not an object")
        try:
            record = RoutingIntent.from_json(entry)
        except (KeyError, ValueError) as exc:
            # Refused rather than dropped: a dropped record reads as never deferred.
            raise unusable(f"{path} holds an unusable intent: {exc}") from exc
        if _key(record) in seen:
            raise unusable(
                f"{path} holds two records for the track {record.track!r} in the "
                f"run {record.session_id!r}; a ledger that gives two answers for "
                f"one run's track cannot say whether it settled, and resolving "
                f"that by line order decides whether a run closes"
            )
        seen.add(_key(record))
        records.append(record)
    return Ledger(tuple(sorted(records, key=_key)))


def write(cfg: config.Config, ledger: Ledger) -> Path:
    """Persist ``ledger`` for this library, atomically and owner only.

    ``config.atomic_write_bytes`` applies the file mode AND the directory mode
    (P1): a 0600 record in a world-writable directory can be replaced.
    """
    payload = {
        "schema_version": SCHEMA_VERSION,
        # Sorted so the bytes are a function of the content alone.
        "intents": [entry.to_json() for entry in sorted(ledger.intents, key=_key)],
    }
    path = path_for(cfg)
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


def lock_path(cfg: config.Config) -> Path:
    """Where the ledger's exclusive lock lives, resolved through the inventory.

    Declared, in the never-restored half beside the other locks, since a restore
    that swapped its directory would swap the inode a live lock is held on.
    """
    return config.state_path(LOCK_KEY, cfg)


def record_intents(cfg: config.Config, intents: Iterable[RoutingIntent]) -> Ledger:
    """Write down what this run means to place, AT THE MOMENT IT IS DECIDED.

    Read, modify, write, since many runs share one ledger, and UNDER AN EXCLUSIVE
    LOCK, since interleaved writers would erase a recorded decision and let its run
    close clean over a track in no ledger.
    """
    with config.exclusive_lock(lock_path(cfg)):
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

    Re-reads under the lock ``record_intents`` takes, so a mark never carries a
    stale view forward. ``session_id`` is required: see :meth:`Ledger.marked`.
    """
    with config.exclusive_lock(lock_path(cfg)):
        updated = read(cfg).marked(
            tracks, state, session_id=session_id, when=output.timestamp(now), actor=actor,
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

    The only way an unplaceable track leaves the outstanding set, never reached
    from the pass, so surfacing and auto-skipping stay different. Scoped to one
    run, so a person never settles a run they were not shown.
    """
    if not str(actor).strip():
        raise ValueError(
            "acknowledging a track that cannot be placed records WHO decided it "
            "is gone; an acknowledgment with no actor is the product asserting "
            "something about itself, which is what it must never do here"
        )
    return mark(
        cfg, tracks, TrackState.ACKNOWLEDGED, session_id=session_id, now=now, actor=actor,
        note=note,
    )


# ---------------------------------------------------------------------------
# Reading the library: one walk, partitioned by the soft-delete marker
# ---------------------------------------------------------------------------


def content_rows(db: Any) -> Iterator[trees.ContentRow]:
    """Every collection row, as the three columns the matcher compares.

    A GENERATOR, consumed once by :func:`index_rows`; a re-reader must materialize
    it. A row with no path drops out later, in the module that owns paths.

    THE SOFT-DELETE MARKER IS READ, NEVER DEFAULTED, AND A ROW THAT CANNOT REPORT
    IT REFUSES: a default of active hands every tombstone to the matcher as live,
    and the pass would place and mark a deleted track. The read is
    :func:`cratekit.write.trees.soft_delete_marker`, the one copy of the rule (U24).
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

    BOTH halves are indexed by :func:`cratekit.write.trees.index_active_rows`, the
    writer's own single locate, so one location never resolves to two rows. The
    rows are kept too, since the writer builds its own index from them.
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

    Once, since the rows are a database cursor and a second walk sees nothing.
    """
    active: list[trees.ContentRow] = []
    tombstoned: list[trees.ContentRow] = []
    for row in rows:
        if row.deleted:
            # The marker is cleared so the SHARED index function, which skips
            # tombstones, indexes this half too.
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

    Resolved at WRITE time from the active taxonomy, never persisted, so a rename
    orphans nothing (R19, D5). The shapes a sub identifier takes: a bucket's own
    sub, its single sub, the shared no energy sink, an energy BAND with the
    bucket's label, an additive sub-class, and a genre sub (U155), each checked
    against what the rules return (P4). An identifier none declares REFUSES rather
    than naming a folder after an internal key.
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
    # A genre sub (U155): its identifier is apart from all the others.
    for genre in bucket.genre_subs:
        if genre.id == sub_id:
            return bucket.display, genre.display
    raise KeyError(
        f"the bucket {bucket_id!r} declares no sub-playlist {sub_id!r}; the "
        f"ledger and this library's taxonomy disagree about where a track was "
        f"going, and inventing a name for it would create a folder nobody chose"
    )


@dataclass(frozen=True, slots=True)
class Placed:
    """One intent, where it was going, and what the library says about it now.

    ``folder`` and ``sub`` are display names for the write, never written back.
    """

    intent: RoutingIntent
    placement: Placement
    folder: str
    sub: str
    content_id: str | None = None
    content_ids: tuple[str, ...] = ()


def row_placement(alive: trees.RowMatch, removed: trees.RowMatch) -> Placement:
    """Which placement one location's two row answers amount to.

    ``alive`` matches the live rows and ``removed`` the tombstoned ones. The one
    rule every surface reports with, so the deferred pass and the inbox apply name
    one state alike (R-318). An undeclared destination is the caller's to decide.
    """
    if alive.outcome is trees.MatchOutcome.MATCHED:
        return Placement.RESOLVED
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.AMBIGUOUS
    if alive.outcome is trees.MatchOutcome.UNRESOLVED:
        return Placement.UNRESOLVED
    if removed.outcome in (trees.MatchOutcome.MATCHED, trees.MatchOutcome.AMBIGUOUS):
        # A row exists and every one of them is a tombstone: imported once, then
        # removed in rekordbox.
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

    Read-only and pure, so readiness is answered before any session. Both halves go
    through :func:`cratekit.write.trees.match_indexed_rows` once each, ONE locate.
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
            # PER TRACK, never out of the pass: the close gate promises one
            # reason per track it could not place.
            out.append(Placed(intent=intent, placement=Placement.UNDECLARED, folder="", sub=""))
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
        out.append(Placed(intent, placement, folder, sub, content_id, ids))
    return tuple(out)


def readiness(placed: Sequence[Placed]) -> Readiness:
    """Whether the library holds rows for the tracks this run is waiting on.

    THE SIGNAL IS ROW PRESENCE, fail-safe: before the import nothing reaches a row
    and the answer is not-ready. Nothing pending is READY, so a run with nothing to
    place is not refused. A run that reached no row and could not ask for one of
    its tracks is UNANSWERABLE, since telling that person to import sends them
    round the same act for ever.
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

    Climbing from a membership row, as :func:`membership_proven` does, so a
    namesake elsewhere cannot fool it.
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

    Recovery is a re-run, deduplicated by display name, so a renamed folder would
    be created a second time and the track filed in both (R19, D5). The node map
    :func:`cratekit.write.rebuild.resolve_destinations` reads names a rename
    first; this fires only where it cannot.

    NARROW ON PURPOSE (P7): only when the destination folder is not under the root
    AND the track already sits there in a folder the taxonomy declares no bucket
    for. A track placed into a second, new bucket is untouched.
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

    :mod:`cratekit.write.rebuild` is imported lazily, since it imports this module.
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

    Merged, not replaced: the pass sees only the destinations it placed.
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

    ``routed`` is the tracks this pass MARKED, narrower than those it wrote: a
    write whose read-back cannot be proved stays outstanding on purpose.
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
        """The tracks somebody deleted, which only a person can settle."""
        return tuple(item for item in self.placed if item.placement is Placement.WITHDRAWN)


def membership_proven(db: Any, placed: Placed, *, root_id: str) -> bool:
    """Read the library back and say whether this track really is where it belongs.

    THE WALK GOES UP, from the membership row to the root, never down by name, so
    a namesake cannot pass it, and it never calls the find-or-create helpers, which
    would make true what they were asked. A BOOLEAN, never raising for an absent
    row: unproven tries again. A membership marked removed proves nothing (R-758),
    and nor does one that cannot say.
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

    THE ORDER IS THE UNIT: resolve, commit, prove, mark. A crash before the mark
    leaves the intent outstanding and a re-run is free.

    READ-ONLY UNTIL THE LIBRARY IS READY, answered from rows before any session.
    The session is :func:`cratekit.write.trees.write_tree_membership`'s, one tree
    at a time in sorted order (R29), so a refusal on the second leaves the first
    committed and marked.

    ``rows`` is walked EXACTLY ONCE, here. Plans are rewritten through the recorded
    node map before any find-or-create, so a rename converges, and
    :func:`assert_destinations_are_not_renamed` is the leftover. It places what it
    can and reports the rest, one reason per track.
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
        # Nothing is opened, locked or marked. WRITTEN AS "not READY", so an
        # answer added later cannot acquire the writing behaviour.
        return RoutingReport(session_id=session_id, readiness=state, placed=placed)

    by_tree: dict[str, list[Placed]] = {}
    for item in placed:
        if item.placement in WRITABLE:
            by_tree.setdefault(item.intent.tree, []).append(item)

    # READ-ONLY, AND BEFORE THE FIRST WRITE OF THE FIRST TREE, so a refusal on
    # the second tree never stands beside a first already committed. The node
    # map remaps first, so a rename it can name never reaches the refusal.
    anchored = {
        tree_id: tree_registry.anchored_root(tree_id, registry, root_exists=root_exists)
        for tree_id in sorted(by_tree)
    }
    for tree_id, root_id in anchored.items():
        by_tree[tree_id] = _converge_destinations(
            cfg, db, by_tree[tree_id], declared, tree_id=tree_id, root_id=root_id
        )
        assert_destinations_are_not_renamed(
            db, by_tree[tree_id], declared, tree_id=tree_id, root_id=root_id
        )

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
            # ONE prefix map for both sides, so the pass and the write cannot
            # disagree about which row a location names.
            prefix_map=rules,
            analysis_roots=watched,
            workflow=workflow,
        )
        reports.append(report)
        _record_routed_nodes(cfg, db, group, tree_id=tree_id, root_id=report.root_id)

        proven = [
            item for item in group if membership_proven(db, item, root_id=report.root_id)
        ]
        if proven:
            mark(
                cfg, [item.intent.track for item in proven], TrackState.ROUTED,
                session_id=session_id, now=now,
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

    A run closed here would report placed tracks that sit in no tree, with nothing
    left to place them. Read from the LEDGER alone, since the library may be
    unmounted at close. Pending-human rather than failure: nothing is broken.
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

    ``awaiting-import`` is a run whose XML half is written and whose import has
    not happened, and ``close_session`` asked only whether the target state is
    terminal, so such a run closed while the spine still refused it. It reuses the
    slug :func:`cratekit.core.session.assert_database_surface_allowed` reports.
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

    TWO GATES, for an unlanded placement and an unimported export. Closing is
    gated and abandoning is not: a run nobody can finish or give up on is how
    people edit state files by hand. The close is
    :func:`cratekit.core.session.close_session`, which releases the capture.
    """
    if state is session.SessionState.CLOSED:
        assert_import_settled(record)
        assert_settled(cfg, record.session_id)
    return session.close_session(record, cfg, state=state, now=now)


__all__ = [
    "ANSWERLESS", "EMPTY", "IMPORTED", "LOCK_KEY", "OUTSTANDING", "ROUTING_WORKFLOW",
    "SCHEMA_VERSION", "SETTLED", "STATE_KEY", "WRITABLE", "Ledger", "Placed", "Placement",
    "Readiness", "RoutingIntent", "RoutingLedgerUnreadable", "RoutingReport", "RowIndex",
    "TrackState", "acknowledge", "assert_destinations_are_not_renamed", "assert_import_settled",
    "assert_settled", "close_run", "lock_path", "content_rows", "destination", "index_rows",
    "mark", "membership_proven", "route", "path_for", "read", "readiness", "record_intents",
    "resolve_placements", "row_placement", "track_id", "write",
]
