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

A FORMER PLACE IS LEFT THROUGH THE SAME RULE (R-797). A bucket promoted to a
folder of its own declares the playlist its tracks sat in before, and that
playlist is one of its competing subs. So a track there whose reading names a
band is a move like any other, the band added and the old playlist left, across
two folders. The playlist competes in the folder that holds it as well, as it
did before the promotion, so a track there whose genre names another style of
that folder moves to that style. A place the entry's own bucket settles is not
asked about again in the other. A track with no reading leaves the old
playlist for the no reading sub, since nothing has to be read to know a
playlist the taxonomy stopped declaring is not its place. Nothing is ever
moved INTO a former place. A track sitting only in one, claimed by neither
bucket, is listed once and not moved, so the old playlist is never read as
empty while it still holds tracks.

A SPLIT PLACE IS LEFT THROUGH THE SAME RULE TOO (U118). A genre split out of
a folder that keeps its bands, Soul out of R&B, declares those bands as split
places, and each is a competing sub of the declaring bucket alone. So a track
whose genre names Soul and that sits in ``R&B / Med`` is a move like any
other, ``Soul / Med`` added and ``R&B / Med`` left, while a track whose genre
names R&B is never asked about it. Only an entry that claims the declaring
bucket decides on one; the tree path in either bucket does not.

Layer: modules. It performs no input. Everything it reads is handed in.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from cratekit.adopt.plan import WITHHELD_BY_VERDICT, AdoptionPlan, Placements, PlanEntry
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

#: The track sits only in a former place, and its genre names neither the
#: bucket that took the place over nor the one whose folder holds it (R-797).
#: A person filed it there by hand or its genre has changed since.
LEFT_FORMER = "former-place-not-named-by-genre"

#: Every reason, in the order a report lists them.
LEFT_REASONS: tuple[str, ...] = (
    LEFT_NO_READING,
    LEFT_NO_STYLE,
    LEFT_UNNAMED,
    LEFT_NAMES_NEITHER,
    LEFT_VERDICT,
    LEFT_DOUBLED_ROWS,
    LEFT_FORMER,
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
        """What decided the move, as the gate names it.

        A MOVE WITH NO READING WAS NOT DECIDED BY ENERGY (R-797). The one move
        made without a reading leaves a former place for the no reading sub,
        and what sends the track to that bucket is its genre. Saying energy
        beside a reading of nothing would name a decision nobody took.
        """
        if self.kind == routing.Competing.BAND.value and self.energy is not None:
            return DECIDED_BY_ENERGY
        return DECIDED_BY_GENRE


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
    declared: taxonomy.Taxonomy,
    entry: PlanEntry,
    kind: routing.Competing,
    unnamed: tuple[str, ...],
    stale: tuple[str, ...],
) -> str:
    """Why a track holding a stale sub is left where it is, or nothing.

    A BUCKET THAT READS NEITHER ENERGY NOR GENRE HAS NO READING TO MOVE ON. It
    declares one place for everything, so nothing about a file says a track
    belongs there rather than where it sits, and ``no-reading`` is the true
    name for that. It was first filed under the genre reason, which says a
    genre was read and named nothing, and no genre is read there at all.

    THE RESOLVER ANSWERS A DEFAULT FOR A GENRE ITS MAP DOES NOT HOLD. That
    default is a place to put a track nobody has filed, and is no reading.

    LEAVING A FORMER PLACE FOR THE NO READING SUB NEEDS NO READING (R-797). A
    reading decides between two bands, and nothing has to decide whether a
    track belongs in a playlist the taxonomy stopped declaring. Its target is
    the sub the resolver names for a file with no reading, which says nothing
    false about the track. Found by the second review: such a track sitting in
    the former place and in the no reading sub was left in both for good. A
    track that holds a stale BAND as well is still left, since which band is
    right is the question a reading answers. A default STYLE is not treated
    this way: it would file a track as a style nobody said it was.

    A SPLIT PLACE IS LEFT THE SAME WAY (U118). What sends a track out of the
    holder's band is its genre naming the declaring bucket, so a track there
    with no reading goes to this bucket's no reading sub.
    """
    if unnamed:
        return LEFT_UNNAMED
    if kind is routing.Competing.BAND:
        if entry.energy is not None:
            return ""
        return "" if set(stale) <= routing.left_only(declared, entry.bucket) else LEFT_NO_READING
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
    # A FORMER PLACE IS NEVER A TARGET (R-797). No resolver answers with one,
    # so this is an entry somebody built by hand, and a move made on it would
    # file a track into a playlist the taxonomy stopped declaring. A split
    # place is never one either (U118): it is another bucket's band.
    if (
        routing.former_place(declared, entry.bucket, entry.sub) is not None
        or routing.split_place(declared, entry.bucket, entry.sub) is not None
    ):
        return None
    held = tuple(sorted(set(placements.holds(entry.bucket, entry.content_id)) & competing))
    stale = tuple(sub for sub in held if sub != entry.sub)
    if not stale:
        return None
    unnamed = _unnamed(placements, entry, entry.bucket, held)
    reason = _left_reason(declared, entry, kind, unnamed, stale)
    if reason:
        return _left(entry, entry.bucket, kind, reason, entry.sub, held, unnamed)
    return _move(entry, entry.bucket, kind, entry.sub, held, tree=tree)


def _unnamed(
    placements: Placements, entry: PlanEntry, bucket: str, held: tuple[str, ...]
) -> tuple[str, ...]:
    """The part of ``held`` the track holds under another name only."""
    return tuple(sorted(set(placements.holds_unnamed(bucket, entry.content_id)) & set(held)))


def _left(
    entry: PlanEntry,
    bucket: str,
    kind: routing.Competing,
    reason: str,
    target: str,
    held: tuple[str, ...],
    unnamed: tuple[str, ...],
) -> Left:
    """One track left where it is. ONE BUILDER for both paths."""
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


def _move(
    entry: PlanEntry,
    bucket: str,
    kind: routing.Competing,
    target: str,
    held: tuple[str, ...],
    *,
    tree: str,
) -> Move:
    """One move. ONE BUILDER for both paths: ``add`` is empty when the target
    is held, and ``remove`` is every other held sub."""
    stale = tuple(sub for sub in held if sub != target)
    return Move(
        move_id=move_id_for(tree, entry.content_id, bucket, target, stale),
        content_id=entry.content_id,
        location=entry.recorded,
        bucket=bucket,
        kind=str(kind.value),
        target=target,
        add="" if target in held else target,
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


def refused_buckets(entries: Sequence[PlanEntry]) -> frozenset[str]:
    """Every bucket a person's collision verdict kept adoption out of.

    READ OFF THE ENTRIES, because the plan carries a verdict only as the
    entries it withheld: :func:`cratekit.adopt.plan.with_collision_verdicts`
    flips the entries routed to the refused bucket and records nothing else.
    So a bucket no entry routes to cannot be known refused here, and that gap
    is recorded rather than hidden. Found by the review: the first version
    honoured a verdict only when it fell on the entry's own bucket, and would
    have planned a removal inside a folder the person refused when the track
    sat there under another genre.
    """
    return frozenset(
        entry.bucket for entry in entries if entry.withheld_by == WITHHELD_BY_VERDICT
    )


def tree_path_decides(kind: routing.Competing) -> bool:
    """Whether the tree path decides in a bucket whose competing subs are ``kind``.

    BAND BUCKETS ONLY, in one place. Style subs are decided by genre, and a
    genre that does not name the bucket has nothing to say about which of its
    styles is right, so a style double in such a bucket is out of this verb's
    scope and its pairs held twice are not listed either. The selection of
    buckets, the decision, and the doubled listing all ask this one predicate,
    so there is one guard and not three copies of it.
    """
    return kind is routing.Competing.BAND


def _standing_in_tree(
    entry: PlanEntry,
    bucket: str,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    *,
    tree: str,
    refused: frozenset[str],
) -> Move | Left | None:
    """What one track comes to in a band bucket adoption's entry does not claim.

    ONLY WHERE THE TRACK HOLDS TWO OR MORE COMPETING SUBS, and only in a
    bucket :func:`tree_path_decides` admits. A track in one sub of a bucket
    its genre does not name is not this verb's: whether it belongs there at
    all is adoption's question. THE ONE EXCEPTION IS A FORMER PLACE (R-797):
    a track holding nothing here but one is listed, whatever the kind, and is
    still not moved.

    NOTHING IS ADDED HERE. The reading picks one of the subs the track holds
    and the rest are removed, or it names none of them and the track is left,
    under its own reason. A move that added a band in a bucket the genre does
    not name would be filing the track by a rule adoption does not use.

    A FILE THE CENSUS COULD NOT READ HAS NO READING, whatever its row carries.
    An excluded track, missing, unreadable, online only or unmapped, is listed
    under ``no-reading`` and never moved, because the reading a move is made
    on was never taken off the file.
    """
    kind, competing = routing.competing_subs(declared, bucket)
    split = held_in_split_place(entry, bucket, placements, declared)
    if split:
        return _left_in_split_place(entry, bucket, kind, placements, split, refused)
    held = held_in_tree(entry, bucket, placements, declared, competing)
    if in_former_place_only(declared, bucket, held):
        return _left_in_former_place(entry, bucket, kind, placements, declared, held, refused)
    if not tree_path_decides(kind):
        return None
    if len(held) < 2:
        return None
    unnamed = _unnamed(placements, entry, bucket, held)
    target = reading_target(entry, bucket, declared)
    if unnamed:
        reason = LEFT_UNNAMED
    elif bucket in refused:
        reason = LEFT_VERDICT
    elif entry.disposition is Disposition.EXCLUDED or entry.energy is None or not target:
        reason = LEFT_NO_READING
    elif target not in held:
        reason = LEFT_NAMES_NEITHER
    else:
        reason = ""
    if reason:
        return _left(entry, bucket, kind, reason, target, held, unnamed)
    return _move(entry, bucket, kind, target, held, tree=tree)


def in_former_place_only(
    declared: taxonomy.Taxonomy, bucket: str, held: Sequence[str]
) -> bool:
    """Whether everything a track holds in ``bucket`` is a former place of it.

    OF THE BUCKET THAT DECLARES THE PLACE, and not of the bucket whose folder
    holds it, though the place competes in both. The track is listed once,
    under the bucket that took the place over.

    ONE PREDICATE for the buckets the plan asks about and for what it finds
    there, so a track the first selects is a track the second lists.
    """
    former = {place.id for place in declared.bucket(bucket).formerly}
    return bool(held) and set(held) <= former


def settled_in_the_other_bucket(
    entry: PlanEntry, bucket: str, declared: taxonomy.Taxonomy
) -> frozenset[str]:
    """The former places of ``bucket`` that the entry's own bucket settles.

    A FORMER PLACE COMPETES IN TWO BUCKETS AND IS SETTLED IN ONE. When the
    entry claims the other of the two, :func:`standing` decides the place
    there: the track leaves it for the sub its reading names, or is left under
    that path's own reason. So in this bucket the place is not held at all, as
    far as the tree path is concerned. Found by the second review, which drove
    a track in the old playlist and in a band whose genre names a style of the
    old folder: both buckets planned leaving the one membership, or one moved
    the track while the other listed it as left.

    A SPLIT PLACE IS NEVER THE TREE PATH'S IN EITHER BUCKET (U118). In the
    bucket that declares it, every track in the holder's band reads as holding
    it, R&B's own tracks included, so the tree path there would plan over
    tracks the genre never sent; only :func:`standing` decides on it, for an
    entry claiming the declarer. In the holder, the band is settled by the
    declaring bucket when the entry claims that bucket, so a track in two of
    the holder's bands is not moved between them by the holder while the
    declaring bucket moves it out of both.
    """
    settled = {
        place.id
        for declarer, place in routing.former_places(declared, bucket)
        if claims(entry, place.bucket if declarer == bucket else declarer)
    }
    for declarer, place in routing.split_places(declared, bucket):
        if declarer == bucket:
            settled.add(place.id)
        elif claims(entry, declarer) or genre_names(entry, declarer, declared):
            settled.add(place.sub)
    return frozenset(settled)


def genre_names(entry: PlanEntry, bucket: str, declared: taxonomy.Taxonomy) -> bool:
    """Whether the entry's genre names ``bucket``, by any tier but the fallback.

    THE FALLBACK TIER NAMES NOTHING, as :func:`_left_in_former_place` reads it.
    Asked where no entry claims a bucket, since a file adoption could not read
    or a folder a verdict refused still carries the genre its row was read
    with.
    """
    resolution = routing.resolve_bucket(declared, entry.genre)
    return resolution.match is not routing.Match.FALLBACK and resolution.bucket_id == bucket


def held_in_split_place(
    entry: PlanEntry, bucket: str, placements: Placements, declared: taxonomy.Taxonomy
) -> tuple[str, ...]:
    """The split places of ``bucket`` a track sits in that no entry moves it out of.

    ONLY WHEN ITS GENRE NAMES ``bucket`` AND ITS ENTRY DOES NOT CLAIM IT (U118):
    a file the census could not read, or a folder a person's verdict refused.
    Such a track is LISTED, never moved, so the gate names every one still in
    the holder's places and the split can be seen to be finished before its
    declaration is deleted. Found by the review: it was in no row at all, and
    the holder's own tree path moved it between the holder's bands. A track
    whose genre names the holder, or nothing, is the holder's and is never
    asked about here.
    """
    split = {place.id for place in declared.bucket(bucket).split_from}
    if not split or claims(entry, bucket) or not genre_names(entry, bucket, declared):
        return ()
    return tuple(sorted(set(placements.holds(bucket, entry.content_id)) & split))


def _left_in_split_place(
    entry: PlanEntry,
    bucket: str,
    kind: routing.Competing,
    placements: Placements,
    held: tuple[str, ...],
    refused: frozenset[str],
) -> Left:
    """The listing for a track :func:`held_in_split_place` found. The most
    specific true reason: a renamed playlist, a refused folder, and otherwise
    a file the census could not read, which is no reading."""
    unnamed = _unnamed(placements, entry, bucket, held)
    if unnamed:
        reason = LEFT_UNNAMED
    elif bucket in refused:
        reason = LEFT_VERDICT
    else:
        reason = LEFT_NO_READING
    return _left(entry, bucket, kind, reason, "", held, unnamed)


def held_in_tree(
    entry: PlanEntry,
    bucket: str,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    competing: frozenset[str],
) -> tuple[str, ...]:
    """The competing subs of ``bucket`` the tree path reads a track as holding.

    ONE BODY for the buckets the plan asks about, for what it finds there and
    for the rows it lists as held twice, so the three cannot disagree about a
    place the entry's own bucket settles.
    """
    settled = settled_in_the_other_bucket(entry, bucket, declared)
    return tuple(
        sorted((set(placements.holds(bucket, entry.content_id)) & competing) - settled)
    )


def _left_in_former_place(
    entry: PlanEntry,
    bucket: str,
    kind: routing.Competing,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    held: tuple[str, ...],
    refused: frozenset[str],
) -> Left:
    """The listing for a track in a former place its entry does not claim (R-797).

    LISTED, NEVER MOVED. The entry does not claim the bucket, so no reading
    adoption took sends the track to it, and a move would be filing the track
    by a rule adoption does not use. The row is what stops the old playlist
    being read as empty: the gate names every track still in it and why.

    THE REASON IS THE MOST SPECIFIC ONE THAT IS TRUE. A playlist renamed since
    it was recorded, a folder a person's verdict refused, a file the census
    could not read although its genre names this bucket or the one whose
    folder holds the place, and last a genre that names another bucket or
    none.
    """
    unnamed = _unnamed(placements, entry, bucket, held)
    named_by_genre = {
        bucket,
        *(place.bucket for place in declared.bucket(bucket).formerly if place.id in held),
    }
    # THE FALLBACK TIER NAMES NOTHING, as adoption's own census reads it. A
    # taxonomy whose fallback is one of these two buckets would otherwise have
    # every unrecognised genre read as naming it.
    resolution = routing.resolve_bucket(declared, entry.genre)
    genre_names_it = (
        resolution.match is not routing.Match.FALLBACK
        and resolution.bucket_id in named_by_genre
    )
    if unnamed:
        reason = LEFT_UNNAMED
    elif named_by_genre & refused:
        reason = LEFT_VERDICT
    elif genre_names_it:
        reason = LEFT_NO_READING
    else:
        reason = LEFT_FORMER
    return _left(entry, bucket, kind, reason, "", held, unnamed)


def standing_in(
    entry: PlanEntry,
    bucket: str,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    *,
    tree: str,
    refused: frozenset[str] = frozenset(),
) -> Move | Left | None:
    """What one track comes to in one bucket: a move, a track left, or neither.

    ONE BODY FOR THE PLAN AND FOR THE WORKER'S CHECK OF IT, over every bucket a
    move can name. The bucket adoption's entry claims goes to :func:`standing`
    unchanged, so R-758's rule is untouched there. Every other bucket goes to
    the tree path, which R-780 added. ``refused`` is :func:`refused_buckets`
    over the plan the entry came from.
    """
    if not placements.read:
        return None
    if claims(entry, bucket):
        return standing(entry, placements, declared, tree=tree)
    return _standing_in_tree(entry, bucket, placements, declared, tree=tree, refused=refused)


def buckets_asked(
    entry: PlanEntry,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    competing: Mapping[str, tuple[routing.Competing, frozenset[str]]],
) -> tuple[str, ...]:
    """Every bucket the plan asks about one track, in the taxonomy's order.

    The bucket adoption's entry claims, every band bucket the tree holds
    the track in twice or more, whether through two subs or through two rows
    of one, and every bucket the track holds nothing in but a former place
    (R-797). Declared order, so two plans over one tree list the same rows in
    the same order and digest the same.
    """
    asked: list[str] = []
    for bucket in declared.buckets:
        if claims(entry, bucket.id):
            asked.append(bucket.id)
            continue
        kind, subs = competing[bucket.id]
        # ONLY A BUCKET THAT DECLARES A FORMER PLACE CAN MATCH (R-797), and
        # then whatever its kind: a track still in one is listed in a bucket
        # split by style as well as one split by energy.
        if bucket.formerly and in_former_place_only(
            declared,
            bucket.id,
            held_in_tree(entry, bucket.id, placements, declared, subs),
        ):
            asked.append(bucket.id)
            continue
        # A SPLIT PLACE NO ENTRY MOVES THE TRACK OUT OF IS LISTED (U118).
        if held_in_split_place(entry, bucket.id, placements, declared):
            asked.append(bucket.id)
            continue
        if not tree_path_decides(kind):
            continue
        held = held_in_tree(entry, bucket.id, placements, declared, subs)
        settled = settled_in_the_other_bucket(entry, bucket.id, declared)
        doubled = (set(placements.holds_doubled(bucket.id, entry.content_id)) & subs) - settled
        if len(held) >= 2 or doubled:
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
    the worker compares against. It rides beside a track left for another
    reason as well, so the double is named whatever else is said about the
    track, and is omitted only beside a move, whose next plan lists it.
    """
    settled = settled_in_the_other_bucket(entry, bucket, declared)
    doubled = tuple(
        sorted((set(placements.holds_doubled(bucket, entry.content_id)) & competing) - settled)
    )
    if not doubled:
        return None
    return Left(
        content_id=entry.content_id,
        location=entry.recorded,
        bucket=bucket,
        kind=str(routing.Competing.BAND.value),
        reason=LEFT_DOUBLED_ROWS,
        target=reading_target(entry, bucket, declared),
        holds=held_in_tree(entry, bucket, placements, declared, competing),
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
        refused = refused_buckets(plan.entries)
        for entry in plan.entries:
            for bucket in buckets_asked(entry, plan.placements, declared, competing):
                found = standing_in(
                    entry, bucket, plan.placements, declared, tree=plan.tree, refused=refused
                )
                if isinstance(found, Move):
                    moves.append(found)
                    continue
                if isinstance(found, Left):
                    left.append(found)
                if tree_path_decides(competing[bucket][0]):
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
    "LEFT_FORMER",
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
    "genre_names",
    "held_in_split_place",
    "held_in_tree",
    "in_former_place_only",
    "left_row",
    "move_id_for",
    "move_row",
    "reading_target",
    "refused_buckets",
    "settled_in_the_other_bucket",
    "standing",
    "standing_in",
    "to_json",
    "tree_path_decides",
]
