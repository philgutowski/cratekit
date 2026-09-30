"""The move plan: a track sits in one competing sub and its file reads another.

WHY THIS EXISTS (R-758). Adoption withholds an entry whose track already holds
a competing sub, lists it, and moves nothing, because every membership writer
adds and none removes. On the live library that list is 585 long, and sitting
16 scored 59 sampled tracks and found 59 equal to the energy tag their file
carries, so the placement is the stale side. The author decided on 2026-09-29
that the tag is the current reading. This module turns adoption's own plan
into the list of what to add and what to remove.

IT WRITES NO SECOND RULE FOR WHAT COMPETES. The sub a track belongs in is the
one :func:`cratekit.adopt.plan.build_adoption_plan` already resolved, through
the resolver routing uses. What it holds is the
:class:`cratekit.adopt.plan.Placements` that plan was built over. Which of
those compete is :func:`cratekit.core.routing.competing_subs`, asked of the
taxonomy. A sub class, manual or derived, is never in that set, so it is never
a source and never removed from.

WHAT IS LEFT WHERE IT IS, AND LISTED. A move is made on a reading, so a track
with none is not moved: a file with no energy tag in a bucket split by energy,
a bucket that reads neither energy nor genre and so has nothing of the file's
to decide by, and a genre that names no style in a bucket split by style,
where the resolver would fall back to a default nobody's file asked for. A
track held through a playlist that no longer carries the declared name is left
as well, since the writer finds a playlist by that name.

Layer: modules. It performs no input. Everything it reads is handed in.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from cratekit.adopt.plan import AdoptionPlan, Placements, PlanEntry
from cratekit.adopt.scan import Disposition
from cratekit.cli.output import canonical_json, digest_of
from cratekit.core import routing, taxonomy

#: The prefix a move identifier carries. Its own, for the reason
#: :data:`cratekit.adopt.plan.ENTRY_ID_PREFIX` gives.
MOVE_ID_PREFIX = "mv"

#: Why a track that holds a stale sub is left where it is.
LEFT_NO_READING = "no-reading"
LEFT_NO_STYLE = "genre-names-no-style"
LEFT_UNNAMED = "held-under-another-name"

#: Every reason, in the order a report lists them.
LEFT_REASONS: tuple[str, ...] = (LEFT_NO_READING, LEFT_NO_STYLE, LEFT_UNNAMED)

#: What decided a move, as the gate names it.
DECIDED_BY_ENERGY = "energy"
DECIDED_BY_GENRE = "genre"


@dataclass(frozen=True, slots=True)
class Move:
    """One track's move: the sub to add, the subs to remove, and the reading.

    ``target`` is the sub the file's reading names. ``add`` is ``target`` when
    the track does not hold it yet and empty when it does, which is the track
    already in the right sub and also in a stale one. ``remove`` is every
    competing sub of the bucket the track holds other than ``target``, and is
    never empty. Stable identifiers throughout (R19, D5).
    """

    move_id: str
    content_id: str
    location: str
    bucket: str
    kind: str
    target: str
    add: str
    remove: tuple[str, ...]
    holds: tuple[str, ...]
    energy: int | None
    genre: str

    @property
    def decided_by(self) -> str:
        return DECIDED_BY_ENERGY if self.kind == routing.Competing.BAND.value else DECIDED_BY_GENRE


@dataclass(frozen=True, slots=True)
class Left:
    """One track that holds a stale sub and is not moved, and why."""

    content_id: str
    location: str
    bucket: str
    kind: str
    reason: str
    target: str
    holds: tuple[str, ...]
    holds_unnamed: tuple[str, ...]
    energy: int | None
    genre: str


def move_id_for(tree: str, content_id: str, bucket: str, target: str, remove: tuple[str, ...]) -> str:
    """The stable identifier of one move. A function of the work, as an entry's is."""
    digest = hashlib.sha256(
        canonical_json(
            {
                "tree": tree,
                "content": content_id,
                "bucket": bucket,
                "target": target,
                "remove": list(remove),
            }
        ).encode()
    ).hexdigest()
    return f"{MOVE_ID_PREFIX}_{digest[:24]}"


def move_row(move: Move) -> dict[str, Any]:
    """One move as the gate shows it and the digest covers it. ONE BODY for both."""
    return {
        "id": move.move_id,
        "content_id": move.content_id,
        "location": move.location,
        "bucket": move.bucket,
        "kind": move.kind,
        "add": move.add,
        "remove": list(move.remove),
        "holds": list(move.holds),
        "target": move.target,
        "decided_by": move.decided_by,
        "energy": move.energy,
        "genre": move.genre,
    }


def left_row(left: Left) -> dict[str, Any]:
    """One track left where it is, as the gate lists it and the digest covers it."""
    return {
        "content_id": left.content_id,
        "location": left.location,
        "bucket": left.bucket,
        "kind": left.kind,
        "reason": left.reason,
        "target": left.target,
        "holds": list(left.holds),
        "holds_under_another_name": list(left.holds_unnamed),
        "energy": left.energy,
        "genre": left.genre,
    }


@dataclass(frozen=True, slots=True)
class MovePlan:
    """Every move and every track left, over one tree as it was read."""

    tree: str
    placements: str
    moves: tuple[Move, ...] = ()
    left: tuple[Left, ...] = ()

    def counts(self) -> dict[str, Any]:
        """The counts by kind, zeroes included, derived over both enumerations."""
        by_kind = {str(member.value): 0 for member in routing.Competing}
        for move in self.moves:
            by_kind[move.kind] += 1
        by_reason = {reason: 0 for reason in LEFT_REASONS}
        for left in self.left:
            by_reason[left.reason] += 1
        return {
            "moves": len(self.moves),
            **by_kind,
            "memberships_added": sum(1 for move in self.moves if move.add),
            "memberships_removed": sum(len(move.remove) for move in self.moves),
            "left": {"total": len(self.left), **by_reason},
        }

    def digest(self) -> str:
        """What an approval is recorded against. It covers ALL of what is shown.

        Every move and every track left, each as its whole row, with the counts
        and whether the tree was read. A track somebody moved by hand between
        the approval and the write is a different row and a different digest.
        """
        return document_digest(
            {
                "tree": self.tree,
                "placements": self.placements,
                "counts": self.counts(),
                "moves": [move_row(move) for move in self.moves],
                "left": [left_row(left) for left in self.left],
            }
        )


def document_digest(document: Mapping[str, Any]) -> str:
    """The digest of a plan document, taken over the five things it shows.

    ONE BODY for a plan in memory and a document a job froze, so the worker
    can prove the rows it is about to act on are the rows the approval was
    recorded against. The document's own ``digest`` field is not read.
    """
    return digest_of(
        {
            "tree": document["tree"],
            "placements": document["placements"],
            "counts": document["counts"],
            "moves": list(document["moves"]),
            "left": list(document["left"]),
        }
    )


def _left_reason(
    declared: taxonomy.Taxonomy, entry: PlanEntry, kind: routing.Competing, unnamed: tuple[str, ...]
) -> str:
    """Why a track holding a stale sub is left where it is, or nothing.

    A BUCKET THAT READS NEITHER ENERGY NOR GENRE HAS NO READING TO MOVE ON. It
    declares one place for everything, so nothing about a file says a track
    belongs there rather than where it sits, and ``no-reading`` is the true
    name for that. It was first filed under the genre reason, which says a
    genre was read and named nothing, and no genre is read there at all.

    THE RESOLVER ANSWERS A DEFAULT FOR A GENRE ITS MAP DOES NOT HOLD. That
    default is a place to put a track nobody has filed, and is no reading.
    """
    if unnamed:
        return LEFT_UNNAMED
    if kind is routing.Competing.BAND:
        return LEFT_NO_READING if entry.energy is None else ""
    by_source = declared.bucket(entry.bucket).sub_by_source
    if by_source is None:
        return LEFT_NO_READING
    return "" if entry.genre in by_source.map else LEFT_NO_STYLE


def standing(
    entry: PlanEntry,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    *,
    tree: str,
) -> Move | Left | None:
    """What one entry comes to over one tree: a move, a track left, or neither.

    ONE BODY FOR THE PLAN AND FOR THE WORKER'S CHECK OF IT. The plan is built
    from this, and the worker asks it again of the library as it stands, so
    every condition that leaves a track alone at planning time leaves it alone
    at write time. The first version of the worker compared the bucket and the
    sub and nothing else, and would have removed a membership of a track the
    plan as it stood listed as left.

    OVER THE ENTRIES ADOPTION ROUTES AND THE ONES IT WITHHOLDS OVER A PLACE.
    The second set is its review list. The first holds the track already in
    the sub its reading names and in a stale one as well, which adoption
    leaves applicable and off that list (R-734), and which has only the stale
    one removed.

    AN ENTRY A VERDICT WITHHELD IS NOT MOVED. A person refused that folder.
    """
    if not placements.read or not entry.bucket or not entry.sub:
        return None
    if entry.disposition is Disposition.WITHHELD:
        if not entry.held_elsewhere:
            return None
    elif entry.disposition is not Disposition.ROUTE:
        return None
    kind, competing = routing.competing_subs(declared, entry.bucket)
    if entry.sub not in competing:
        return None
    held = tuple(sorted(set(placements.holds(entry.bucket, entry.content_id)) & competing))
    stale = tuple(sub for sub in held if sub != entry.sub)
    if not stale:
        return None
    unnamed = tuple(
        sorted(set(placements.holds_unnamed(entry.bucket, entry.content_id)) & set(held))
    )
    reason = _left_reason(declared, entry, kind, unnamed)
    if reason:
        return Left(
            content_id=entry.content_id,
            location=entry.recorded,
            bucket=entry.bucket,
            kind=str(kind.value),
            reason=reason,
            target=entry.sub,
            holds=held,
            holds_unnamed=unnamed,
            energy=entry.energy,
            genre=entry.genre,
        )
    return Move(
        move_id=move_id_for(tree, entry.content_id, entry.bucket, entry.sub, stale),
        content_id=entry.content_id,
        location=entry.recorded,
        bucket=entry.bucket,
        kind=str(kind.value),
        target=entry.sub,
        add="" if entry.sub in held else entry.sub,
        remove=stale,
        holds=held,
        energy=entry.energy,
        genre=entry.genre,
    )


def build_move_plan(plan: AdoptionPlan, declared: taxonomy.Taxonomy) -> MovePlan:
    """Every track holding a competing sub its reading does not name.

    A TREE NOBODY READ PLANS NOTHING and the plan says ``unread``, so an
    approval given over it is not honoured once the tree can be read.
    """
    found = [
        standing(entry, plan.placements, declared, tree=plan.tree) for entry in plan.entries
    ]
    return MovePlan(
        tree=plan.tree,
        placements=plan.placements.state,
        moves=tuple(item for item in found if isinstance(item, Move)),
        left=tuple(item for item in found if isinstance(item, Left)),
    )


def to_json(plan: MovePlan) -> dict[str, Any]:
    """The plan as a structured document. A transport, never an editing surface."""
    return {
        "tree": plan.tree,
        "digest": plan.digest(),
        "placements": plan.placements,
        "counts": plan.counts(),
        "moves": [move_row(move) for move in plan.moves],
        "left": [left_row(left) for left in plan.left],
    }


def from_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[Move, ...]:
    """The moves an approval froze, read back out of a job's payload.

    Every field is read by name and none is defaulted, so a payload short of
    one raises here rather than moving a track on half a row.
    """
    return tuple(
        Move(
            move_id=str(row["id"]),
            content_id=str(row["content_id"]),
            location=str(row["location"]),
            bucket=str(row["bucket"]),
            kind=str(row["kind"]),
            target=str(row["target"]),
            add=str(row["add"]),
            remove=tuple(str(sub) for sub in row["remove"]),
            holds=tuple(str(sub) for sub in row["holds"]),
            energy=None if row["energy"] is None else int(row["energy"]),
            genre=str(row["genre"]),
        )
        for row in rows
    )


__all__ = [
    "DECIDED_BY_ENERGY",
    "DECIDED_BY_GENRE",
    "LEFT_NO_READING",
    "LEFT_NO_STYLE",
    "LEFT_REASONS",
    "LEFT_UNNAMED",
    "MOVE_ID_PREFIX",
    "Left",
    "Move",
    "MovePlan",
    "build_move_plan",
    "document_digest",
    "from_rows",
    "left_row",
    "move_id_for",
    "move_row",
    "standing",
    "to_json",
]
