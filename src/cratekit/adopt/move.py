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

IT PLANS FROM THE TREE AS IT STANDS, NOT FROM ADOPTION'S LIST ALONE (R-780).
Adoption resolves one bucket per track, the one its genre names, and its
entries can only ever speak for that bucket. A track sitting in two band subs
of a bucket its genre does not name, or of any bucket when it has no genre at
all, held both before adoption ran and is in no entry's bucket, so the first
version of this plan never saw it: two such tracks were read back off the
author's library after the pass that was meant to end the shape. So the plan
asks, for every entry, every band bucket the tree holds the track in twice or
more, and decides by the reading the census took off the file, through the
resolver routing uses, :func:`cratekit.core.routing.energy_sub`. In a bucket
the genre does not name the move only ever removes: the reading picks one of
the subs the track holds and the others go, or it names none of them and the
track is left and listed. Adding a sub in a bucket the genre does not name is
adoption's decision and not this verb's.

WHAT IS LEFT WHERE IT IS, AND LISTED. A move is made on a reading, so a track
with none is not moved: a file with no energy tag in a bucket split by energy,
a bucket that reads neither energy nor genre and so has nothing of the file's
to decide by, and a genre that names no style in a bucket split by style,
where the resolver would fall back to a default nobody's file asked for. A
track held through a playlist that no longer carries the declared name is left
as well, since the writer finds a playlist by that name. A track in two band
subs whose reading names a third, in a bucket its genre does not name, is
left. A track a person's verdict withheld from a bucket is left. And a track
holding one sub through two rows (R-781) is listed so that the doubles the
verb cannot reach are named, though nothing here removes a row of a pair the
reading names.

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
#: In a bucket the genre does not name, the reading names none of the subs the
#: track holds there, and this verb adds nothing in such a bucket (R-780).
LEFT_NAMES_NEITHER = "reading-names-neither-held"
#: A person's collision verdict kept adoption out of this bucket's folder.
LEFT_VERDICT = "withheld-by-verdict"
#: One sub held through two or more active rows, and nothing else to move
#: (R-781). Listed so the double is named; no row of it is removed.
LEFT_DOUBLED_ROWS = "one-sub-held-by-two-rows"

#: Every reason, in the order a report lists them.
LEFT_REASONS: tuple[str, ...] = (
    LEFT_NO_READING,
    LEFT_NO_STYLE,
    LEFT_UNNAMED,
    LEFT_NAMES_NEITHER,
    LEFT_VERDICT,
    LEFT_DOUBLED_ROWS,
)

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


def claims(entry: PlanEntry, bucket: str) -> bool:
    """Whether adoption's entry speaks for this bucket.

    It does when the genre routed the track there and adoption either placed
    it or withheld it over a place it holds. Those are the entries
    :func:`standing` was written over, and the sub adoption resolved is the
    reading there. Every other bucket a track sits in is asked of the tree.
    """
    if entry.bucket != bucket or not entry.sub:
        return False
    if entry.disposition is Disposition.ROUTE:
        return True
    return entry.disposition is Disposition.WITHHELD and entry.held_elsewhere


def reading_target(entry: PlanEntry, bucket: str, declared: taxonomy.Taxonomy) -> str:
    """The sub of ``bucket`` the file's reading names, or nothing.

    ONE READING, TWO WAYS OF ASKING FOR IT. In the bucket adoption's entry
    claims, the answer is the sub adoption resolved, which is the resolver's
    answer to the census's reading. In any other bucket it is the same
    resolver asked directly with the same reading, so no second opinion on
    what a level means can grow here. A bucket the taxonomy no longer
    declares names nothing.
    """
    if claims(entry, bucket):
        return entry.sub
    try:
        sub = routing.energy_sub(declared, bucket, entry.energy, source_genre=entry.genre)
    except KeyError:
        return ""
    return "" if sub is None else sub.id


def _standing_in_tree(
    entry: PlanEntry,
    bucket: str,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    *,
    tree: str,
) -> Move | Left | None:
    """What one track comes to in a band bucket adoption's entry does not claim.

    BAND SUBS ONLY, and only where the track holds two or more of them.
    Style subs are decided by genre, and a genre that does not name the bucket
    has nothing to say about which of its styles is right. A track in one sub
    of a bucket its genre does not name is not this verb's either: whether it
    belongs there at all is adoption's question.

    NOTHING IS ADDED HERE. The reading picks one of the subs the track holds
    and the rest are removed, or it names none of them and the track is left,
    under its own reason. A move that added a band in a bucket the genre does
    not name would be filing the track by a rule adoption does not use.
    """
    kind, competing = routing.competing_subs(declared, bucket)
    if kind is not routing.Competing.BAND:
        return None
    held = tuple(sorted(set(placements.holds(bucket, entry.content_id)) & competing))
    if len(held) < 2:
        return None
    unnamed = tuple(
        sorted(set(placements.holds_unnamed(bucket, entry.content_id)) & set(held))
    )
    target = reading_target(entry, bucket, declared)
    if unnamed:
        reason = LEFT_UNNAMED
    elif entry.disposition is Disposition.WITHHELD and entry.bucket == bucket:
        reason = LEFT_VERDICT
    elif entry.energy is None or not target:
        reason = LEFT_NO_READING
    elif target not in held:
        reason = LEFT_NAMES_NEITHER
    else:
        reason = ""
    if reason:
        return Left(
            content_id=entry.content_id,
            location=entry.recorded,
            bucket=bucket,
            kind=str(kind.value),
            reason=reason,
            target=target,
            holds=held,
            holds_unnamed=unnamed,
            energy=entry.energy,
            genre=entry.genre,
        )
    stale = tuple(sub for sub in held if sub != target)
    return Move(
        move_id=move_id_for(tree, entry.content_id, bucket, target, stale),
        content_id=entry.content_id,
        location=entry.recorded,
        bucket=bucket,
        kind=str(kind.value),
        target=target,
        add="",
        remove=stale,
        holds=held,
        energy=entry.energy,
        genre=entry.genre,
    )


def standing_in(
    entry: PlanEntry,
    bucket: str,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    *,
    tree: str,
) -> Move | Left | None:
    """What one track comes to in one bucket: a move, a track left, or neither.

    ONE BODY FOR THE PLAN AND FOR THE WORKER'S CHECK OF IT, over every bucket a
    move can name. The bucket adoption's entry claims goes to :func:`standing`
    unchanged, so R-758's rule is untouched there. Every other bucket goes to
    the tree path, which R-780 added.
    """
    if not placements.read:
        return None
    if claims(entry, bucket):
        return standing(entry, placements, declared, tree=tree)
    return _standing_in_tree(entry, bucket, placements, declared, tree=tree)


def buckets_asked(
    entry: PlanEntry,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    competing: Mapping[str, tuple[routing.Competing, frozenset[str]]],
) -> tuple[str, ...]:
    """Every bucket the plan asks about one track, in the taxonomy's order.

    The bucket adoption's entry claims, and every band bucket the tree holds
    the track in twice or more, whether through two subs or through two rows
    of one. Declared order, so two plans over one tree list the same rows in
    the same order and digest the same.
    """
    asked: list[str] = []
    for bucket in declared.buckets:
        if claims(entry, bucket.id):
            asked.append(bucket.id)
            continue
        kind, subs = competing[bucket.id]
        if kind is not routing.Competing.BAND:
            continue
        held = set(placements.holds(bucket.id, entry.content_id)) & subs
        if len(held) >= 2 or (set(placements.holds_doubled(bucket.id, entry.content_id)) & subs):
            asked.append(bucket.id)
    return tuple(asked)


def _doubled_rows(
    entry: PlanEntry,
    bucket: str,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    competing: frozenset[str],
) -> Left | None:
    """The listing for a track that holds a sub through two rows, or nothing.

    LISTED, NOT A STANDING. The worker asks :func:`standing_in` of every
    approved row, and a move whose target is doubled is done once the stale
    sub is gone, so the double must not read as a reason the plan as it stands
    leaves the track. It is a row on the screen and in the digest and nothing
    the worker compares against.
    """
    doubled = tuple(sorted(set(placements.holds_doubled(bucket, entry.content_id)) & competing))
    if not doubled:
        return None
    return Left(
        content_id=entry.content_id,
        location=entry.recorded,
        bucket=bucket,
        kind=str(routing.Competing.BAND.value),
        reason=LEFT_DOUBLED_ROWS,
        target=reading_target(entry, bucket, declared),
        holds=tuple(sorted(set(placements.holds(bucket, entry.content_id)) & competing)),
        holds_unnamed=(),
        energy=entry.energy,
        genre=entry.genre,
    )


def build_move_plan(plan: AdoptionPlan, declared: taxonomy.Taxonomy) -> MovePlan:
    """Every track holding a competing sub its reading does not name.

    OVER EVERY BUCKET THE TREE HOLDS EACH TRACK IN, not only the one its genre
    names (R-780). The entry's own bucket is asked first, as R-758 asked it,
    then every band bucket the track doubles in.

    A TREE NOBODY READ PLANS NOTHING and the plan says ``unread``, so an
    approval given over it is not honoured once the tree can be read.
    """
    moves: list[Move] = []
    left: list[Left] = []
    if plan.placements.read:
        competing = {
            bucket.id: routing.competing_subs(declared, bucket.id) for bucket in declared.buckets
        }
        for entry in plan.entries:
            for bucket in buckets_asked(entry, plan.placements, declared, competing):
                found = standing_in(entry, bucket, plan.placements, declared, tree=plan.tree)
                if isinstance(found, Move):
                    moves.append(found)
                elif isinstance(found, Left):
                    left.append(found)
                elif competing[bucket][0] is routing.Competing.BAND:
                    doubled = _doubled_rows(
                        entry, bucket, plan.placements, declared, competing[bucket][1]
                    )
                    if doubled is not None:
                        left.append(doubled)
    return MovePlan(
        tree=plan.tree,
        placements=plan.placements.state,
        moves=tuple(moves),
        left=tuple(left),
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
    "LEFT_DOUBLED_ROWS",
    "LEFT_NAMES_NEITHER",
    "LEFT_NO_READING",
    "LEFT_NO_STYLE",
    "LEFT_REASONS",
    "LEFT_UNNAMED",
    "LEFT_VERDICT",
    "MOVE_ID_PREFIX",
    "Left",
    "Move",
    "MovePlan",
    "buckets_asked",
    "build_move_plan",
    "claims",
    "document_digest",
    "from_rows",
    "left_row",
    "move_id_for",
    "move_row",
    "reading_target",
    "standing",
    "standing_in",
    "to_json",
]
