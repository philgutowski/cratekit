"""Whether a database-native tree still matches what this library declares (U36).

WHAT THIS MODULE IS FOR. Once a tree cuts over, the database is the only copy of
its membership. There is no export to re-import and, under U9's A2 verdict, no
safe way to import one, so anything that puts the database back to an earlier
state leaves that tree short with nothing to notice it. Incremental sync cannot
close the gap either: its scope is a watermark plus deduplication against what is
already owned, and the files an old database no longer places are still on disk
and therefore still read as owned. This module is the record of which trees are
in that condition, plus the two questions that put a tree into it and the one act
that takes it out.

THE CASE IT ACTUALLY COVERS, WHICH IS NARROWER THAN IT FIRST LOOKS. Cratekit's
own restore is not it. KTD21b makes a capture atomic over the database and every
COUPLED state entry, and this document is one of them, so a Cratekit restore puts
the database and this record back together and they agree by construction. What
remains is the case that mechanism cannot see: a database recovered OUT OF BAND,
from the rclone mirror after a drive failure, or from a hand copy somebody made
before a rekordbox upgrade. Nothing Cratekit wrote is involved, so nothing
Cratekit wrote can be trusted to have noticed.

HOW A RECOVERY THAT LEFT NO TRACE IS DETECTED ANYWAY. The database itself keeps
a monotonically increasing local update count: rekordbox bumps it on every change
to its own tables. A fingerprint of that number, taken at the close of each
governed write and compared at the start of the next, is what makes an
out-of-band recovery visible. A count that went BACKWARD is a database that went
backward. A row count that moved while the sequence stood still is the same fact
from the other side, because rekordbox cannot add or remove a row without
bumping the number. Neither is ordinary use, and ordinary use is exactly what a
mismatch check has to stay quiet about (P7): a person importing forty tracks in
rekordbox moves both numbers forward together, every day, and a guard that
demanded a rebuild after that would be a guard people learn to route around.

THE HONEST LIMIT, STATED RATHER THAN IMPLIED. This detects a database that went
backward. It cannot detect a SIDEWAYS one: a copy from another machine whose
update count happens to be higher reads as ordinary progress. Closing that would
need a durable per-install identity the schema does not expose, and claiming this
covers it would be worse than the gap, because it invites trust the mechanism
cannot repay (P4).

WHY THE FLAG IS NOT A JUDGEMENT ABOUT THE PRODUCT. An unconverged tree refuses
that tree's writes and nothing else. A library may hold one governed tree and
five playlists a person curates, and the fact that a restore damaged the first
says nothing about the rest. The escape hatch has the same shape: a difference
nothing can derive is disposed of BY TREE, by a named person, in the record,
because the alternative is a refusal with no way past it, and a refusal with no
way past it is how people learn to edit state files by hand.

LAYER: infrastructure. It reads and writes state and reads the database through
the guarded writer. It names no verb (D2) and no display name (R19): the
destinations it records are the taxonomy's stable identifiers and the database's
own row identifiers, which is what lets a rebuild converge across a folder
somebody renamed in rekordbox rather than filing every track twice.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from cratekit.cli import output
from cratekit.core import config, rb_writer, tree_registry
from cratekit.core.cause import Cause, CratekitError, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy

#: The state entry this module owns. Named once, so the resolver and every caller
#: cannot disagree about which file is meant.
STATE_KEY = "tree_convergence"

#: The lock that serializes every read-modify-write of the entry above. A second
#: DECLARED entry rather than a suffix composed from the first, because a path
#: built under a state root is a file the inventory does not know about, and
#: nothing walks, captures or clears a file the inventory has never heard of.
LOCK_KEY = "tree_convergence_lock"

#: Bumped only when the on-disk shape changes incompatibly. A file written by a
#: newer build is refused rather than guessed at: a misread here decides whether
#: a governed write runs against a tree a restore already left short.
SCHEMA_VERSION = 1

#: The column rekordbox soft-deletes with. Named once here because the row count
#: below filters on it AT THE DATABASE rather than in Python, which is the whole
#: reason the count cannot silently default: a column the schema no longer has
#: makes the query raise instead of counting every tombstone as a live track.
#:
#: THIS IS A THIRD SPELLING OF ONE COLUMN AND IT IS NOT SHARED, which is a cost
#: recorded rather than hidden. ``cratekit.write.routing_pass`` reads the same
#: column off a row, ``cratekit.core.rb_writer`` names it in the additive
#: whitelist, and U24 consolidates the row-reading half behind
#: ``cratekit.write.trees.soft_delete_marker``. This module cannot import that
#: one: KTD23 ranks ``cratekit.write.trees`` at the write layer and this module
#: is imported BY it, so sharing the constant in that direction is the upward
#: dependency the ladder exists to refuse. The spellings are held together by
#: this comment and by the fact that all three fail loudly rather than silently:
#: a filter on a column the schema moved raises, and a reader with no default
#: refuses. If a fourth appears, hoist the constant into the foundation rather
#: than adding another comment.
SOFT_DELETE_COLUMN = "rb_local_deleted"


class Purpose(StrEnum):
    """What a governed database write is FOR. Two answers, one pair of gates apart.

    NOT A FLAG AND NOT AN OVERRIDE, and the distinction is the same one
    :class:`cratekit.core.session.Intent` draws for the unresolved-session latch.
    A ``REBUILD`` write still asserts the volume, still needs the acknowledgment,
    still takes the lock, still passes the medium check and the anchored root,
    still arms the analysis watch, and still may not write a grid. What it is not
    held by is the pair of latches whose own stated remedy is a rebuild.

    Without this declaration the product would refuse the rebuild it just told
    somebody to run, and the only way past would be editing a state file by hand.
    That failure has already been shipped once in this repository, by a
    committed-unverified session whose refusal named a restore and whose latch
    then refused the restore, and the lesson is cheap to apply a second time.

    NAMED ``Purpose`` RATHER THAN ``Intent`` deliberately. ``Intent`` already
    means a session's declared purpose one package away, and anything performing
    a governed write imports both modules. The repository carries several
    collisions of that shape, recorded rather than resolved because outside code
    holds the names; this one had never been seen by anything, so it cost a word.

    The default everywhere is ``ROUTINE``, which is the RESTRICTIVE answer. A
    caller that forgets to declare its purpose gets both latches, and the only
    way to shed them is to say so.
    """

    ROUTINE = "routine"
    REBUILD = "tree-rebuild"


class Regression(StrEnum):
    """How the database went backward. Two shapes, and they are not the same.

    Both mean "something replaced this database with an earlier state", and both
    are recorded rather than collapsed into one, because the second one is the
    case a reader will not believe without being told which number moved.
    """

    #: The local update count is lower than the one recorded at the last close.
    SEQUENCE_WENT_BACKWARD = "sequence-went-backward"

    #: The active row count moved while the update count did not. rekordbox
    #: cannot add or remove a row without bumping the sequence, so a standstill
    #: sequence beside a moved count is two databases, not one.
    ROWS_MOVED_AT_A_STANDSTILL = "rows-moved-at-a-standstill"


class ConvergenceStateUnreadable(CratekitError):
    """The convergence record exists and cannot be understood.

    Deliberately NOT collapsed into "nothing is unconverged". That reading is the
    permissive one: it admits every governed write over a tree a restore may have
    emptied, and it does it silently. An unreadable record is a record whose
    flags have not been cleared, so it has to be its own answer.

    A ``CratekitError`` for the reason its siblings in the tree registry and the
    routing ledger give (S4). One slug covers every way the file can be unusable
    and the REMEDY is what differs between them: a record from a newer build asks
    for an upgrade and a corrupt one asks for the doctor, and flattening the two
    at the command-line boundary would replace both with "report a defect".
    """

    def __init__(self, message: str, *, path: Path, remedy: Remedy) -> None:
        super().__init__(
            Cause(
                reason="tree-convergence-unusable",
                message=message,
                remediation=Remediation(remedy=remedy),
                scope=Scope.RUN,
                origin=("convergence",),
                detail={"path": str(path)},
            )
        )
        self.path = path
        self.remedy = remedy


# ---------------------------------------------------------------------------
# The fingerprint: what the database looked like when Cratekit last left it
# ---------------------------------------------------------------------------


def _is_whole_number(value: Any) -> bool:
    """True for a real integer, and FALSE FOR A BOOLEAN.

    ``isinstance(True, int)`` is True in Python, so a document carrying
    ``"local_usn": true`` passes a bare integer check and then reads as usn 1. A
    fingerprint at usn 1 compares lower than every real database, so the next
    routine assertion sees no regression, silently, on the one number that says
    whether a library went backward. The bool exclusion is spelled here once and
    used by every reader of these two counts.
    """
    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(frozen=True, slots=True)
class Fingerprint:
    """Three readings that together say which database this is and when.

    ``schema_version`` is RECORDED AND IS NOT A TRIGGER, deliberately. A
    rekordbox upgrade migrates the schema, which is an ordinary act, and the
    version pin in the guarded writer already refuses on any drift from the
    recorded pin before a governed verb gets this far. Carrying it here gives a
    person reading a refusal the one fact that explains a jump in the other two
    numbers; treating it as evidence of a restore would fire on every upgrade.
    """

    schema_version: str | None
    active_rows: int
    local_usn: int
    taken: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "active_rows": self.active_rows,
            "local_usn": self.local_usn,
            "taken": self.taken,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Fingerprint:
        version = data.get("schema_version")
        rows = data.get("active_rows")
        usn = data.get("local_usn")
        if not _is_whole_number(rows) or not _is_whole_number(usn):
            raise ValueError(
                "a fingerprint needs an integer active row count and an integer "
                "local update count; without both there is no comparison to make "
                "and no way to say a database went backward"
            )
        return cls(
            schema_version=None if version is None else str(version),
            active_rows=rows,
            local_usn=usn,
            taken=str(data.get("taken") or ""),
        )


def probe(db: Any) -> Fingerprint:
    """Read the three numbers straight out of the database.

    THE ROW COUNT IS FILTERED AT THE DATABASE, NOT IN PYTHON, and that is the
    soft-delete rule arriving by construction rather than by discipline. A Python
    side walk would read the marker off each row through an accessor, and an
    accessor with a default hands back "not deleted" for every tombstone the
    moment the binding stops exposing the column, which is the exact defect a
    previous unit shipped and a review caught. A filter on the column either
    filters or raises. There is no third answer for a default to occupy.

    UNDER THE AUTOFLUSH GUARD, because this runs a query through the caller's
    session and a query flushes pending work out of the collections every write
    guard downstream reads. The probe that first exposed that hazard is gone and
    the containment travels with the guard path rather than with whichever probe
    currently occupies it.

    A DATABASE THAT CANNOT ANSWER REFUSES WITH A STRUCTURED CAUSE rather than
    with a traceback (S4). A column the schema moved, or a registry row a
    rekordbox version stopped writing, means the question "is this the database
    we last wrote to" has no answer at all, and the command-line boundary turns
    anything that is not a structured cause into an internal defect with "report
    a defect" attached, which is not what a person whose schema has moved should
    be told to do.

    THE THREE READINGS ARE TAKEN AND REFUSED SEPARATELY. One try block around all
    three produced one slug for three different failures, so a schema that moved
    the soft-delete column and a rekordbox version that stopped writing the
    update-count row arrived at the reader as the same sentence. They are
    different problems with different answers, and the reading that failed rides
    on the detail where the answer can be worked out.

    THE HANDLE MUST EXPOSE A SESSION, and an absent one refuses rather than
    reading on. ``_no_autoflush`` degrades to a no-op when handed something with
    no ``no_autoflush``, deliberately, so a stand-in can drive the probe. Handing
    it ``getattr(db, "session", None)`` turned that documented degradation into a
    silent one for a whole class of handle: the guard's own docstring calls this
    the one place a read can defeat a guard, and a probe that quietly ran outside
    it would flush the pending collections every downstream write guard reads.
    """
    session = getattr(db, "session", _NO_SESSION)
    if session is _NO_SESSION:
        raise refuse(
            "library-fingerprint-unreadable",
            "this database handle exposes no session, so the autoflush guard "
            "this probe has to run under cannot be armed; a query issued outside "
            "it flushes the pending collections that every downstream write "
            "guard reads to decide what a commit would do, and the guard then "
            "passes a forbidden write it can no longer see",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.RUN,
            origin=("convergence",),
            detail={"handle": type(db).__name__},
        )
    with rb_writer._no_autoflush(session):
        version = _reading(
            "schema version", lambda: rb_writer.db_schema_version(db)
        )
        active = _reading(
            "active row count", lambda: db.get_content(**{SOFT_DELETE_COLUMN: 0}).count()
        )
        usn = _reading("local update count", lambda: db.get_local_usn())
    return Fingerprint(
        schema_version=version,
        active_rows=_counted("active row count", active),
        local_usn=_counted("local update count", usn),
    )


#: Distinguishes "this handle has no session attribute at all" from "its session
#: is None", which are different mistakes and only one of them is a stand-in.
_NO_SESSION = object()


def _reading(what: str, read: Callable[[], Any]) -> Any:
    """One reading off the database, or a refusal that NAMES which one failed."""
    try:
        return read()
    except CratekitError:
        raise
    except Exception as exc:  # noqa: BLE001 - a database that cannot answer IS the answer
        raise refuse(
            "library-fingerprint-unreadable",
            f"the database's {what} could not be read ({exc}), so whether this "
            f"is the database Cratekit last wrote to cannot be decided in either "
            f"direction",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("convergence",),
            detail={"reading": what, "column": SOFT_DELETE_COLUMN},
        ) from exc


def _counted(what: str, value: Any) -> int:
    """A reading that must already BE a whole number, never one coerced into being.

    ``int(value)`` here would accept the string ``"7"`` and the boolean ``True``
    without comment, which is the defaulting-accessor shape this module's own
    docstring argues against for the row count: a binding that started handing
    back a formatted string would have its answer quietly converted, and the two
    numbers that decide whether a library went backward would be built out of
    whatever happened to parse.
    """
    if not _is_whole_number(value):
        raise refuse(
            "library-fingerprint-unreadable",
            f"the database answered its {what} with {value!r}, which is not a "
            f"whole number; coercing it would build the comparison that decides "
            f"whether this library went backward out of a value nobody checked",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.RUN,
            origin=("convergence",),
            detail={"reading": what, "found": type(value).__name__},
        )
    return value


def regression(previous: Fingerprint | None, current: Fingerprint) -> Regression | None:
    """Whether the database went backward between the two readings. Pure.

    NO PREVIOUS READING IS NOT A REGRESSION, and this is the one defaulting
    answer in the module that is correct. A library that has never taken a
    governed write has nothing recorded, and calling that a restore would mark
    every tree unconverged on the first run of a fresh install, which is a
    refusal on a library where nothing has happened at all.

    ORDINARY USE MOVES BOTH NUMBERS FORWARD TOGETHER and is silent here. That is
    the property the narrowness buys (P7): importing forty tracks in rekordbox
    raises the row count and raises the sequence, and a guard that fired on it
    would be one people learn to route around, which is the failure the guard
    exists to prevent arriving through the guard.
    """
    if previous is None:
        return None
    if current.local_usn < previous.local_usn:
        return Regression.SEQUENCE_WENT_BACKWARD
    if (
        current.local_usn == previous.local_usn
        and current.active_rows != previous.active_rows
    ):
        return Regression.ROWS_MOVED_AT_A_STANDSTILL
    return None


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Disposition:
    """A named person saying a difference this tree carries is not damage.

    THE ONE ESCAPE FROM A REFUSAL THAT WOULD OTHERWISE BE PERMANENT. A tree can
    hold a difference nothing derives: a playlist somebody curated by hand under
    a governed root, a track they filed themselves. Without a way past it the
    flag stands forever and every sync refuses, which is not a safety property,
    it is a product nobody can use.

    ``actor`` is required and is never defaulted. A disposition is a person
    taking responsibility for a difference, and a record that cannot say who took
    it is the product asserting something about the user's library on their
    behalf, which is precisely what it must never do.
    """

    actor: str
    note: str = ""
    on: str = ""

    def __post_init__(self) -> None:
        if not str(self.actor).strip():
            raise ValueError(
                "disposing of a convergence difference records WHO decided it is "
                "not damage; a disposition with no actor is the product deciding "
                "on the user's behalf that their library is fine"
            )

    def to_json(self) -> dict[str, Any]:
        return {"actor": self.actor, "note": self.note, "on": self.on}

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Disposition:
        return cls(
            actor=str(data["actor"]),
            note=str(data.get("note") or ""),
            on=str(data.get("on") or ""),
        )


@dataclass(frozen=True, slots=True)
class DestinationNode:
    """One declared destination and the two playlist rows a write put it in.

    THE RECORD THAT MAKES A REBUILD CONVERGE ACROSS A RENAME, which is the whole
    reason it exists. Every find-or-create in the guarded writer targets a
    playlist by the name rekordbox shows, so a rebuild that resolved its
    destinations from the taxonomy's display names would, after somebody renamed
    a folder in rekordbox, find nothing by the new name, create the destination a
    second time, and file every track twice. The tree registry already keeps this
    shape for the root a cutover adopted; this is the same idea one level down,
    and the previous unit registered the obligation rather than inventing a
    second answer to "which node is this destination".

    ``bucket`` and ``sub`` are STABLE IDENTIFIERS, never display names (R19, D5).
    That is what survives the rename; the node identifiers are what survive the
    template being edited.
    """

    bucket: str
    sub: str
    folder_id: str
    playlist_id: str

    def __post_init__(self) -> None:
        for name in ("bucket", "sub", "folder_id", "playlist_id"):
            if not str(getattr(self, name)).strip():
                raise ValueError(
                    f"a recorded destination needs a {name}; a half-recorded node "
                    f"cannot be resolved and would send the next rebuild back to "
                    f"resolving by display name, which is what it exists to avoid"
                )

    def to_json(self) -> dict[str, Any]:
        return {
            "bucket": self.bucket,
            "sub": self.sub,
            "folder": self.folder_id,
            "playlist": self.playlist_id,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> DestinationNode:
        return cls(
            bucket=str(data["bucket"]),
            sub=str(data["sub"]),
            folder_id=str(data["folder"]),
            playlist_id=str(data["playlist"]),
        )


def assert_injective(tree_id: str, nodes: Sequence[DestinationNode]) -> None:
    """Refuse a node map that is not one-to-one, in either direction.

    THE MAP IS A BIJECTION OR IT IS DAMAGE, and nothing was checking either half.

    Two records for ONE declared destination cannot both be right, and resolving
    that by position means the destination a rebuild writes into is decided by
    line order in a JSON file.

    Two declared destinations pointing at ONE node is the sharper half and it is
    what a real defect produced: a rebuild whose plan was keyed on display names
    merged two destinations into one write, then wrote the colliding node
    identifier back for both. Every later rebuild then resolves both declared
    destinations to one playlist, files both sets of tracks into it, and reports
    the other one short forever. The rebuild is additive, so it cannot undo that,
    and the flag can never be cleared by a rebuild again.

    THERE IS NO AUTOMATIC FALLBACK, AND AN EARLIER VERSION OF THIS DOCSTRING SAID
    THERE WAS. It claimed that refusing the record "keeps a tree recoverable: the
    map is rebuilt from scratch by falling back to display-name resolution, which
    is exactly what an absent record already does". Nothing does that.
    :func:`read` turns this ``ValueError`` into ``ConvergenceStateUnreadable`` and
    raises, so a record in this shape stops every reader of the file. The claim
    was load bearing and false, which is worse than the gap it described.

    THE FALLBACK IS NOT IMPLEMENTED BECAUSE IT WOULD CONTRADICT THE READER'S OWN
    RULE. Dropping the nodes and continuing means the next rebuild reads "nothing
    was ever recorded", and that is precisely the misreading
    :meth:`TreeConvergence.from_json` refuses an absent ``nodes`` key for: after a
    rename it resolves by display name and files the whole tree a second time.
    Falling back is the permissive answer wearing a recovery's clothes.

    SO THE HONEST POSITION IS THAT A CORRUPT MAP IS A CORRUPT STATE FILE, with
    the same answers every other corrupt state file in this product has: the
    doctor, or a restore of the coupled set, which carries this document back
    with the database it describes. What stays reachable meanwhile is the
    read-only convergence check, which reports an unreadable record as a finding
    rather than dying with it, because the diagnostic somebody is told to run
    must not be the second thing that breaks.

    A ``ValueError`` rather than a structured cause, because it is the
    dataclass's own construction guard and :func:`read` turns every one of those
    into ``ConvergenceStateUnreadable`` with the doctor remedy attached.
    """
    by_destination: dict[tuple[str, str], DestinationNode] = {}
    by_node: dict[tuple[str, str], DestinationNode] = {}
    for entry in nodes:
        destination = (entry.bucket, entry.sub)
        if destination in by_destination:
            raise ValueError(
                f"the tree {tree_id!r} records two nodes for the destination "
                f"{entry.bucket}/{entry.sub}; a destination that resolves to two "
                f"playlists is resolved by line order, which decides where a "
                f"rebuild writes a library's worth of tracks"
            )
        node = (entry.folder_id, entry.playlist_id)
        clash = by_node.get(node)
        if clash is not None:
            raise ValueError(
                f"the tree {tree_id!r} records the destinations "
                f"{clash.bucket}/{clash.sub} and {entry.bucket}/{entry.sub} "
                f"against one playlist row ({entry.folder_id}/"
                f"{entry.playlist_id}); two declared destinations sharing one "
                f"node means every rebuild files both sets of tracks into it and "
                f"reports the other destination short, and an additive rebuild "
                f"cannot undo that, so the tree could never converge again"
            )
        by_destination[destination] = entry
        by_node[node] = entry


@dataclass(frozen=True, slots=True)
class TreeConvergence:
    """One tree's convergence standing, and where its destinations landed.

    ``unconverged`` is a persisted FACT rather than something derived on demand,
    and the difference matters: the condition it records is that the database no
    longer holds what it should, so a reader that re-derived it would be asking
    the damaged database to report its own damage.
    """

    tree_id: str
    unconverged: bool = False
    reason: str | None = None
    since: str | None = None
    disposition: Disposition | None = None
    nodes: tuple[DestinationNode, ...] = ()

    def __post_init__(self) -> None:
        if not str(self.tree_id).strip():
            raise ValueError(
                "a convergence record needs the identifier of the tree it "
                "describes; a record that cannot say which tree it is about "
                "still refuses writes and names nothing for anyone to repair"
            )
        assert_injective(self.tree_id, self.nodes)

    @property
    def blocking(self) -> bool:
        """Whether this record refuses a governed write today.

        A disposed tree is unconverged AND does not block, and keeping both
        halves rather than clearing the flag is deliberate: the difference is
        still there, a report should still say so, and only the refusal was
        answered for.
        """
        return self.unconverged and self.disposition is None

    def node(self, bucket: str, sub: str) -> DestinationNode | None:
        for entry in self.nodes:
            if entry.bucket == bucket and entry.sub == sub:
                return entry
        return None

    def with_nodes(self, nodes: Iterable[DestinationNode]) -> TreeConvergence:
        """This record with ``nodes`` replacing any entry for the same destination."""
        merged = {(entry.bucket, entry.sub): entry for entry in self.nodes}
        for entry in nodes:
            merged[(entry.bucket, entry.sub)] = entry
        return replace(
            self,
            nodes=tuple(sorted(merged.values(), key=lambda e: (e.bucket, e.sub))),
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "tree": self.tree_id,
            "unconverged": self.unconverged,
            "reason": self.reason,
            "since": self.since,
            "disposition": None if self.disposition is None else self.disposition.to_json(),
            "nodes": [entry.to_json() for entry in self.nodes],
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> TreeConvergence:
        flag = data.get("unconverged")
        if not isinstance(flag, bool):
            # NO DEFAULT, for the reason ``trees.ContentRow.deleted`` has none:
            # the value this would default to means "converged", which is the
            # permissive answer, so a record missing the field would read as a
            # healthy tree and admit every write. A string or a number is refused
            # for the same reason rather than being read for its truthiness.
            raise ValueError(
                "a convergence record needs an explicit boolean unconverged "
                "field; the value it would otherwise default to is the one that "
                "admits a write to a tree a restore may have left short"
            )
        raw_nodes = data.get("nodes")
        if not isinstance(raw_nodes, list):
            # NO DEFAULT, and the inconsistency this closes is the whole reason.
            # ``data.get("nodes", [])`` refused a NULL and accepted an ABSENT
            # key, so one shape of damaged record was caught and the other read
            # as "no nodes were ever recorded". That reading is not harmless: it
            # sends the next rebuild back to resolving destinations by display
            # name, which is the exact resolution this record exists to replace,
            # and after a rename it files the whole tree a second time. Every
            # record this build writes carries the key, so an absent one is a
            # file that was edited or truncated.
            raise ValueError(
                "a convergence record's nodes field is an array and is required; "
                "an absent one would read as 'nothing was ever recorded' and "
                "send the next rebuild back to resolving by display name, which "
                "doubles the tree after a rename"
            )
        raw_disposition = data.get("disposition")
        if raw_disposition is not None and not isinstance(raw_disposition, dict):
            raise ValueError("a convergence record's disposition is an object or null")
        return cls(
            tree_id=str(data["tree"]),
            unconverged=flag,
            reason=None if data.get("reason") is None else str(data["reason"]),
            since=None if data.get("since") is None else str(data["since"]),
            disposition=(
                None if raw_disposition is None else Disposition.from_json(raw_disposition)
            ),
            nodes=tuple(DestinationNode.from_json(entry) for entry in raw_nodes),
        )


@dataclass(frozen=True, slots=True)
class ConvergenceState:
    """Everything this library records about its governed trees.

    Records are a TUPLE rather than a mapping keyed by tree, for the reason the
    tree registry gives for the same choice: it keeps the identifier out of every
    key position, so the R19 guard has nothing to interpret and no future reader
    is tempted to key it on something a user can rename.
    """

    fingerprint: Fingerprint | None = None
    trees: tuple[TreeConvergence, ...] = ()

    def tree(self, tree_id: str) -> TreeConvergence | None:
        for entry in self.trees:
            if entry.tree_id == tree_id:
                return entry
        return None

    def blocking_trees(self) -> tuple[str, ...]:
        return tuple(entry.tree_id for entry in self.trees if entry.blocking)

    def with_tree(self, record: TreeConvergence) -> ConvergenceState:
        kept = tuple(e for e in self.trees if e.tree_id != record.tree_id)
        return replace(
            self, trees=tuple(sorted((*kept, record), key=lambda e: e.tree_id))
        )

    def with_fingerprint(self, taken: Fingerprint) -> ConvergenceState:
        return replace(self, fingerprint=taken)


#: What a library with no record resolves to. Named, because "nothing recorded
#: yet" is a real answer here rather than a missing one.
EMPTY = ConvergenceState()


# ---------------------------------------------------------------------------
# Reading and writing it
# ---------------------------------------------------------------------------


def path_for(cfg: config.Config) -> Path:
    """Where the record lives, resolved through the state inventory.

    Through ``state_path`` rather than composed here. A module that builds its
    own path under a state root has invented a state file the inventory does not
    know about, and this entry is COUPLED precisely so a restore rolls it back
    with the database it describes.
    """
    return config.state_path(STATE_KEY, cfg)


def lock_path(cfg: config.Config) -> Path:
    """Where the record's exclusive lock lives, resolved through the inventory."""
    return config.state_path(LOCK_KEY, cfg)


def read(cfg: config.Config) -> ConvergenceState:
    """The effective record for this library. An absent file is the empty one.

    EVERY FIELD IS RECOGNISED POSITIVELY AND EVERYTHING ELSE IS REFUSED. Catching
    only a JSON parse error is what let a previous unit read a top-level list, a
    scalar, a null field and records filed under a newer version's key all as an
    empty store, after which the next write persisted that emptiness and deleted
    the real records for good. Here the same misreading would report a damaged
    tree as fine and then write that answer down.
    """
    path = path_for(cfg)
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return EMPTY
    except OSError as exc:
        raise ConvergenceStateUnreadable(
            f"{path} exists and could not be read: {exc}",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        ) from exc

    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ConvergenceStateUnreadable(
            f"{path} is not readable as JSON: {exc}", path=path, remedy=Remedy.RUN_DOCTOR
        ) from exc
    if not isinstance(data, dict):
        raise ConvergenceStateUnreadable(
            f"{path} does not hold an object at its top level",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )

    version = data.get("schema_version")
    if not isinstance(version, int):
        raise ConvergenceStateUnreadable(
            f"{path} carries no integer schema_version, so nothing can be said "
            f"about the shape of what follows it",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    if version > SCHEMA_VERSION:
        raise ConvergenceStateUnreadable(
            f"{path} was written at schema version {version}; this build "
            f"understands {SCHEMA_VERSION}",
            path=path,
            remedy=Remedy.UPGRADE_CRATEKIT,
        )

    raw_fingerprint = data.get("fingerprint")
    if raw_fingerprint is not None and not isinstance(raw_fingerprint, dict):
        raise ConvergenceStateUnreadable(
            f"{path} holds a fingerprint that is not an object",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        )
    entries = data.get("trees")
    if not isinstance(entries, list):
        raise ConvergenceStateUnreadable(
            f"{path} has no trees array", path=path, remedy=Remedy.RUN_DOCTOR
        )

    records: list[TreeConvergence] = []
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ConvergenceStateUnreadable(
                f"{path} holds a tree record that is not an object",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        try:
            record = TreeConvergence.from_json(entry)
        except (KeyError, TypeError, ValueError) as exc:
            # Refused rather than dropped. A dropped record reads as "that tree
            # is fine", which is the one misreading that admits a write over a
            # tree a restore left short.
            raise ConvergenceStateUnreadable(
                f"{path} holds an unusable tree record: {exc}",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            ) from exc
        if record.tree_id in seen:
            raise ConvergenceStateUnreadable(
                f"{path} holds two records for the tree {record.tree_id!r}; a "
                f"record that gives two answers for one tree cannot say whether "
                f"it is converged, and resolving that by line order decides "
                f"whether a write runs against a damaged library",
                path=path,
                remedy=Remedy.RUN_DOCTOR,
            )
        seen.add(record.tree_id)
        records.append(record)

    try:
        taken = None if raw_fingerprint is None else Fingerprint.from_json(raw_fingerprint)
    except (KeyError, TypeError, ValueError) as exc:
        raise ConvergenceStateUnreadable(
            f"{path} holds an unusable fingerprint: {exc}",
            path=path,
            remedy=Remedy.RUN_DOCTOR,
        ) from exc

    return ConvergenceState(
        fingerprint=taken, trees=tuple(sorted(records, key=lambda e: e.tree_id))
    )


def write(cfg: config.Config, state: ConvergenceState) -> Path:
    """Persist ``state`` for this library, atomically and owner only.

    Through ``config.atomic_write_bytes``, which applies the explicit file mode
    AND creates the enclosing directories at the explicit directory mode. Both
    halves matter (P1): a 0600 record inside a world-writable directory can be
    unlinked and replaced by any local account, and this record decides whether a
    write runs against a tree a restore may have emptied.
    """
    payload = {
        "schema_version": SCHEMA_VERSION,
        "fingerprint": None if state.fingerprint is None else state.fingerprint.to_json(),
        # Sorted so the bytes are a function of the content alone. An unordered
        # dump makes every write a difference even when nothing changed.
        "trees": [entry.to_json() for entry in sorted(state.trees, key=lambda e: e.tree_id)],
    }
    path = path_for(cfg)
    config.atomic_write_bytes(
        json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


# ---------------------------------------------------------------------------
# The mutators. Every one of them holds the lock across read and write.
# ---------------------------------------------------------------------------
#
# A read-modify-write over a JSON document is not made atomic by an atomic
# rename: the rename is atomic and the CYCLE is not, so two processes that both
# read, both modify and both rename leave one edit on the floor while the call
# that lost it returns a record reporting success. Two separate units in this
# repository shipped exactly that and both were caught by review rather than by
# a suite. The primitive is the one the config migration already takes, not a
# third implementation of one idea.


def record_fingerprint(
    cfg: config.Config, db: Any, *, now: datetime | None = None
) -> Fingerprint:
    """Write down what the database looks like as this session leaves it.

    CALLED AFTER THE COMMIT, NEVER BEFORE. A fingerprint recorded before the
    write describes a database the session then changed, so the next run reads a
    difference it caused itself and reports the library as restored.

    WHAT A CRASH IN THE WINDOW COSTS, stated plainly, because "idempotent in the
    happy path" says nothing about this one. A crash between the guarded commit
    and this call leaves the PREVIOUS fingerprint standing. The next run then
    compares a database that has moved forward against a reading from before it
    moved, and forward is not a regression in either direction the rule tests:
    the update count is higher or equal, and the active row count cannot have
    changed at all, because a membership write creates no collection rows. So the
    cost is a stale reading that the next successful write replaces, and not a
    false refusal. The reverse order has no such answer: a fingerprint taken
    first and a commit that then fails records a database that never existed, and
    the regression it hides is a real one.
    """
    taken = replace(probe(db), taken=output.timestamp(now))
    with config._exclusive_lock(lock_path(cfg)):
        write(cfg, read(cfg).with_fingerprint(taken))
    return taken


def mark_unconverged(
    cfg: config.Config,
    tree_ids: Iterable[str],
    *,
    reason: str,
    now: datetime | None = None,
) -> ConvergenceState:
    """Flag trees as no longer matching what this library declares.

    Idempotent on the reason and the timestamp: a tree already flagged for the
    same reason keeps its original ``since``, so re-running the detection does
    not keep moving the date the damage was first seen forward to now.
    """
    stamp = output.timestamp(now)
    with config._exclusive_lock(lock_path(cfg)):
        state = read(cfg)
        for tree_id in tree_ids:
            current = state.tree(tree_id) or TreeConvergence(tree_id=tree_id)
            if current.unconverged and current.reason == reason:
                continue
            state = state.with_tree(
                replace(
                    current,
                    unconverged=True,
                    reason=reason,
                    since=stamp,
                    # A NEW REFUSAL CLEARS AN OLD DISPOSITION. Somebody accepted
                    # a difference they were shown; this is a different one they
                    # have not seen, and carrying the old answer forward would
                    # let one person's judgement about a curated playlist wave
                    # through the next restore that empties the tree.
                    disposition=None,
                )
            )
        write(cfg, state)
    return state


def record_nodes(
    cfg: config.Config,
    tree_id: str,
    nodes: Iterable[DestinationNode],
    *,
    replace_all: bool = False,
) -> ConvergenceState:
    """Write down which playlist rows a write put each declared destination in.

    ``replace_all`` is for the caller that considered EVERY destination the
    record knows about, which is the rebuild: it resolves the union of what it
    derived and what was recorded, so a recorded destination it did not write
    back is one whose node no longer resolves. Merging would keep that dangling
    entry, and a dangling entry is not inert: it can hold the identifier a
    destination resolved to this run, which makes the merged map name one node
    for two destinations, which is the shape :func:`assert_injective` refuses.
    Every other caller merges, because it has only looked at part of the tree.
    """
    with config._exclusive_lock(lock_path(cfg)):
        state = read(cfg)
        current = state.tree(tree_id) or TreeConvergence(tree_id=tree_id)
        updated = (
            replace(current, nodes=tuple(sorted(nodes, key=lambda e: (e.bucket, e.sub))))
            if replace_all
            else current.with_nodes(nodes)
        )
        state = state.with_tree(updated)
        write(cfg, state)
    return state


def clear_unconverged(
    cfg: config.Config,
    tree_id: str,
    *,
    differences: Sequence[str],
    now: datetime | None = None,
    disposition: Disposition | None = None,
) -> ConvergenceState:
    """Take a tree out of the refusing state, on evidence or on a named decision.

    TWO WAYS THROUGH AND ONLY TWO. Either a convergence check just ran and found
    no difference at all, in which case ``differences`` is empty and the flag is
    cleared outright; or a person is answering for a difference nothing can
    derive, in which case they are recorded by name and the flag stays set while
    ceasing to refuse. There is no third way, and in particular there is no
    "clear it anyway" argument, because an argument that clears a safety flag on
    request is the flag's off switch wearing the flag's clothes.

    ``differences`` is the CHECK'S OWN LIST rather than a count, so the refusal
    can name what is still wrong. A caller that has to fabricate the list to get
    past this is a caller that has noticed it is lying.
    """
    outstanding = [str(entry) for entry in differences]
    if outstanding and disposition is None:
        raise refuse(
            "tree-unconverged",
            f"the tree {tree_id!r} still differs from what this library declares "
            f"in {len(outstanding)} place(s), so its unconverged flag stays set; "
            f"clearing it now would report the tree as repaired while the "
            f"membership it is missing is still missing",
            remedy=Remedy.REBUILD_TREE,
            steps=(
                "run the rebuild for this tree, which derives its whole "
                "membership from the declared taxonomy and what is on disk and "
                "writes back everything the database lacks",
                "a difference the rebuild cannot derive, such as a playlist "
                "somebody curated by hand under this tree, is answered by a "
                "named person disposing of it for this tree alone",
            ),
            scope=Scope.RUN,
            origin=("convergence",),
            detail={"tree_id": tree_id, "differences": outstanding[:20]},
        )

    stamp = output.timestamp(now)
    with config._exclusive_lock(lock_path(cfg)):
        state = read(cfg)
        current = state.tree(tree_id) or TreeConvergence(tree_id=tree_id)
        if disposition is not None:
            if not current.blocking:
                # A DISPOSITION ANSWERS A REFUSAL AND THERE IS NONE HERE. Writing
                # one anyway records a named person accepting a difference on a
                # tree that is not refusing anything, which is a signed statement
                # about a library nobody was shown. Worse, it sits in the record
                # as a standing answer: the next restore that empties this tree
                # would be waved through by a judgement made before it happened.
                # ``mark_unconverged`` clears an old disposition for the same
                # reason, and this is that rule applied from the other end.
                raise refuse(
                    "tree-unconverged",
                    f"the tree {tree_id!r} is not refusing anything, so there is "
                    f"no difference for anybody to dispose of; recording one now "
                    f"would leave a named person's acceptance standing over a "
                    f"library they were never shown",
                    remedy=Remedy.COMPLETE_PENDING_ACTION,
                    steps=(
                        "run the convergence check for this tree and dispose of "
                        "what it actually reports",
                    ),
                    scope=Scope.RUN,
                    origin=("convergence",),
                    detail={"tree_id": tree_id, "actor": disposition.actor},
                )
            settled = replace(
                current, disposition=replace(disposition, on=disposition.on or stamp)
            )
        else:
            settled = replace(
                current, unconverged=False, reason=None, since=None, disposition=None
            )
        state = state.with_tree(settled)
        write(cfg, state)
    return state


# ---------------------------------------------------------------------------
# The two assertions every governed write makes
# ---------------------------------------------------------------------------


def native_trees(cfg: config.Config, registry: tree_registry.Registry) -> tuple[str, ...]:
    """Every database-native tree in this library, from the record AND from disk.

    THE UNION, because the docstring below promises "every database-native tree
    is marked" and a caller-supplied registry cannot make that promise true. The
    registry is a parameter at every call site, so the guarantee held only as
    long as every future caller happened to pass the WHOLE registry rather than
    the one record it cared about. A caller that passed a filtered registry would
    have marked one tree and left every other native tree in the same damaged
    database reporting itself fine, which is precisely the failure the promise
    names. Reading the file removes the condition rather than documenting it.

    AN EARLIER VERSION OF THIS ARGUED THE UNION WAS FREE because "nothing in src
    calls tree_registry.read". That was false in the commit that wrote it:
    ``cratekit.cli.converge`` reads the registry, and a rebuild's caller reads it
    to build the argument in the first place. The union is justified by what it
    GUARANTEES, not by being free, and the extra read costs one small JSON file
    on a path that is about to open a database.

    Read from disk IN ADDITION TO the argument rather than instead of it, so a
    caller that has already loaded the registry keeps deciding which root it
    writes under, while the SET this marks is derived from the file that actually
    says which trees have cut over. An unreadable registry raises here, which is
    correct: a build that cannot say which trees are native cannot say which ones
    a restore endangered.

    A TREE ON DISK THAT NO CALLER EVER WRITES TO IS MARKED AND NEVER CLEARED, and
    that is recorded rather than solved. It is fail-closed, so nothing is written
    against a tree that may be short, but the flags accumulate. See R-17.
    """
    return tuple(
        sorted(
            set(registry.database_native_trees())
            | set(tree_registry.read(cfg).database_native_trees())
        )
    )


@dataclass(frozen=True, slots=True)
class RestoreCheck:
    """What the detection found, and the two readings it decided from.

    A value rather than a bare ``Regression | None`` so the refusal one layer up
    can name both numbers without probing the database a second time. Probing
    twice would read a database the first probe's own marking has since been
    written beside, and the two readings in one refusal would then be from
    different moments.
    """

    regression: Regression | None
    previous: Fingerprint | None
    current: Fingerprint | None
    trees: tuple[str, ...] = ()

    def __bool__(self) -> bool:
        return self.regression is not None


def detect_out_of_band_restore(
    cfg: config.Config,
    db: Any,
    registry: tree_registry.Registry,
    *,
    now: datetime | None = None,
) -> RestoreCheck:
    """Compare the database against the fingerprint, MARK, and report. Never refuses.

    THE DETECTION AND THE REFUSAL ARE SEPARATE CALLS, and separating them is what
    closes the hole a rebuild drove through. ``assert_tree_writable`` returned
    immediately for a rebuild purpose, so a rebuild never ran this at all, while
    the fingerprint at the close of the membership write was recorded
    unconditionally. The rebuild was therefore the one governed write that
    UPDATED the evidence without ever checking it: an operator whose database had
    been recovered out of band, doing exactly what the product's own refusal text
    tells them to do, blessed the recovered fingerprint as canonical with their
    first action, and every tree the same restore emptied went unmarked forever
    because the routine assertion that would have caught it was now silent.

    IT MARKS BEFORE IT RETURNS, and the write on this path is the point rather
    than an oversight. The evidence is a number inside the database, and the very
    next thing anybody does is open that database again; a detection that left
    nothing behind would have to re-derive the same conclusion from a reading
    that has since moved on, and after one more rekordbox session it no longer
    can. So the conclusion is persisted once, and every later verb reads the flag
    rather than re-deciding.

    EVERY DATABASE-NATIVE TREE IS MARKED, not the one this caller was about to
    write, and :func:`native_trees` is what makes that sentence true rather than
    conditional on the caller. The evidence is about the whole database, so
    scoping the mark to the tree that happened to be asked first would leave the
    others reporting themselves fine until somebody wrote to each of them in turn.
    """
    native = native_trees(cfg, registry)
    if not native:
        # Nothing has cut over, so nothing here can be damaged by a restore and
        # nothing needs a fingerprint yet. Returning before the probe also keeps
        # the whole mechanism off the path of a library that has never flipped a
        # tree, which is every library until the first cutover.
        return RestoreCheck(regression=None, previous=None, current=None)
    current = probe(db)
    previous = read(cfg).fingerprint
    found = regression(previous, current)
    if found is not None:
        mark_unconverged(cfg, native, reason=str(found), now=now)
    return RestoreCheck(
        regression=found, previous=previous, current=current, trees=native
    )


def assert_no_out_of_band_restore(
    cfg: config.Config,
    db: Any,
    registry: tree_registry.Registry,
    *,
    now: datetime | None = None,
) -> None:
    """Detect, and then refuse if the database went backward.

    The refusing half. It adds nothing to :func:`detect_out_of_band_restore`
    except the refusal, so a caller that must not be refused by this latch runs
    the detection directly and is still held to its findings by the flag it
    leaves behind.
    """
    checked = detect_out_of_band_restore(cfg, db, registry, now=now)
    found = checked.regression
    if found is None:
        return
    raise refuse(
        "tree-unconverged",
        f"this library's database went backward since Cratekit last wrote to it "
        f"({str(found)}), which no snapshot restore of ours explains, so every "
        f"tree the database owns is treated as short until it is rebuilt; the "
        f"membership a recovered database no longer holds is not something an "
        f"incremental sync can put back, because the files it lost are still on "
        f"disk and still read as already owned",
        remedy=Remedy.REBUILD_TREE,
        steps=(
            "run the convergence check, which reports per tree what the database "
            "is missing and what it holds that nothing declares",
            "run the rebuild for each tree it reports short",
        ),
        scope=Scope.RUN,
        origin=("convergence",),
        detail={
            "regression": str(found),
            "trees": list(checked.trees),
            "recorded_usn": (
                None if checked.previous is None else checked.previous.local_usn
            ),
            "found_usn": None if checked.current is None else checked.current.local_usn,
        },
    )


def assert_converged(cfg: config.Config, tree_id: str) -> None:
    """Refuse a governed write to a tree that is recorded as short.

    Read from the RECORD alone, so this needs no database. That matters because
    the record is what survives the process that discovered the damage, and
    because a refusal that had to open the library to decide would fail for the
    wrong reason on a machine where the volume is not mounted.
    """
    record = read(cfg).tree(tree_id)
    if record is None or not record.blocking:
        return
    raise refuse(
        "tree-unconverged",
        f"the tree {tree_id!r} has been unconverged since {record.since} "
        f"({record.reason}), so writing to it now would add to a tree that is "
        f"already missing membership and report the run as clean",
        remedy=Remedy.REBUILD_TREE,
        steps=(
            "run the rebuild for this tree, which derives its whole membership "
            "from the declared taxonomy and what is on disk",
            "a difference the rebuild cannot derive is answered by a named "
            "person disposing of it for this tree alone",
        ),
        scope=Scope.RUN,
        origin=("convergence",),
        detail={"tree_id": tree_id, "reason": record.reason, "since": record.since},
    )


def assert_tree_writable(
    cfg: config.Config,
    db: Any,
    tree_id: str,
    registry: tree_registry.Registry,
    *,
    purpose: Purpose = Purpose.ROUTINE,
    now: datetime | None = None,
) -> None:
    """Both questions, in the order that makes the second one's answer current.

    The restore check runs FIRST because it is what SETS the flag the second one
    reads. Reversed, a database recovered out of band would pass the flag check,
    which is still clear, and the write would land in a short tree while the
    detection that would have caught it ran afterwards or not at all.

    ONE CALL, so a later writer cannot arm half of this. Two exported assertions
    with a documented ordering is a docstring asking to be obeyed; a caller that
    makes one call cannot make it in the wrong order.

    A ``REBUILD`` purpose is exempt from the two REFUSALS and is NOT exempt from
    the detection behind the first one, which is the distinction that was missing
    and which cost a whole database's worth of evidence. See :class:`Purpose` for
    why a latch may not condemn its own remedy, and note what a rebuild is still
    held by: everything in the session spine, the medium check, the anchored
    root, the grid rules, and now the restore detection.

    WHY THE DETECTION RUNS FOR A REBUILD TOO. The membership write records a
    fingerprint at its close, unconditionally, because that is what makes the
    NEXT run's comparison possible. A rebuild that skipped the detection
    therefore overwrote the evidence without ever reading it, and the concrete
    sequence is the ordinary one: a database is recovered out of band, the
    operator does what the product's own refusal text and the read-only check
    both tell them to do, and their first act is a rebuild for the tree they were
    told about. Skipping detection meant that rebuild silently blessed the
    recovered fingerprint, after which the routine assertion had nothing to
    compare against and every OTHER tree the same restore emptied reported itself
    fine forever. Running the detection marks all of them first, and the rebuild
    then clears its own tree on the evidence of a real check.

    The exemption is written as "only ROUTINE is refused" rather than as "REBUILD
    is exempt" for the same reason the settled and outstanding sets are derived
    in the direction they are: a purpose added later must inherit the checking
    behaviour, not the exemption.
    """
    if purpose is Purpose.ROUTINE:
        assert_no_out_of_band_restore(cfg, db, registry, now=now)
        assert_converged(cfg, tree_id)
        return
    detect_out_of_band_restore(cfg, db, registry, now=now)


__all__ = [
    "EMPTY",
    "LOCK_KEY",
    "SCHEMA_VERSION",
    "SOFT_DELETE_COLUMN",
    "STATE_KEY",
    "ConvergenceState",
    "ConvergenceStateUnreadable",
    "DestinationNode",
    "Disposition",
    "Fingerprint",
    "Purpose",
    "Regression",
    "RestoreCheck",
    "TreeConvergence",
    "assert_converged",
    "assert_injective",
    "assert_no_out_of_band_restore",
    "assert_tree_writable",
    "clear_unconverged",
    "detect_out_of_band_restore",
    "lock_path",
    "mark_unconverged",
    "native_trees",
    "path_for",
    "probe",
    "read",
    "record_fingerprint",
    "record_nodes",
    "regression",
    "write",
]
