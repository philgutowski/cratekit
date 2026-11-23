"""The move plan: a track sits in one competing sub and its file reads another.

Every membership writer adds and none removes, so adoption withholds a track
already holding a competing sub (R-758). The file's tag is the current reading,
by the author's decision of 2026-09-29, so this module turns adoption's own
plan into what to add and what to remove.

IT WRITES NO SECOND RULE FOR WHAT COMPETES. The sub a track belongs in is the
one :func:`cratekit.adopt.plan.build_adoption_plan` resolved, what it holds is
the :class:`cratekit.adopt.plan.Placements` that plan was built over, and which
of those compete is :func:`cratekit.core.routing.competing_subs`, which never
holds a sub class.

IT PLANS FROM THE TREE AS IT STANDS (R-780). An entry speaks only for the
bucket its genre names, so every band bucket holding the track twice or more is
asked too, by the census's reading through
:func:`cratekit.core.routing.energy_sub`. There the move only removes: adding
in a bucket the genre does not name is adoption's decision.

WHAT IS LEFT IS LISTED, each track under its reason: a move needs a reading, a
playlist the writer can find by its declared name, and a folder no verdict
refused. One sub held through two rows is listed and never thinned (R-781).

A FORMER PLACE (R-797) competes in the bucket that declares it and in the
folder that holds it, and a SPLIT PLACE (U118), a band a genre was split out
of, in the declaring bucket alone. A track leaves either like any other place;
nothing is ever moved INTO one, and a track sitting in one that no entry moves
it out of is listed, so the old playlist is never read as empty.

A GENRE A PERSON MOVED (U339) is the one move across buckets. ``tag set``
records, in :mod:`cratekit.adopt.genre_moves`, the bucket a row's old genre
filed it in, and that bucket is asked for that row even when the track holds
it once: the move adds the track to its new bucket's sub when adoption has not,
and takes it out of every sub of the old one. Nothing else is moved across
buckets, so a track a person put in a second genre folder by hand stays.

Layer: modules. It performs no input. Everything it reads is handed in.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields
from typing import Any, Mapping, Sequence

from cratekit.adopt.plan import (
    WITHHELD_BY_VERDICT,
    AdoptionPlan,
    Placements,
    PlanEntry,
    kept_beside,
)
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
    the track does not hold it yet and empty when it does. ``remove`` is every
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
    #: The bucket ``target`` is a sub of when it is not ``bucket``: a genre a
    #: person moved (U339), whose ``remove`` and ``holds`` are the old bucket's.
    #: Empty for every other move.
    target_bucket: str = ""

    @property
    def into(self) -> str:
        """The bucket the track is filed into: ``target_bucket``, else ``bucket``."""
        return self.target_bucket or self.bucket

    @property
    def decided_by(self) -> str:
        """What decided the move, as the gate names it.

        A move with no reading leaves a former place for the no reading sub,
        and what sent it there is its genre, never energy (R-797), as a move
        across buckets is decided by the genre a person gave (U339).
        """
        if self.target_bucket:
            return DECIDED_BY_GENRE
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


def move_id_for(
    tree: str,
    content_id: str,
    bucket: str,
    target: str,
    remove: tuple[str, ...],
    target_bucket: str = "",
) -> str:
    """The stable identifier of one move. A function of the work, as an entry's is.
    A move within one bucket is identified as it was before U339."""
    work = {"tree": tree, "content": content_id, "bucket": bucket, "target": target}
    if target_bucket:
        work["into"] = target_bucket
    digest = hashlib.sha256(canonical_json({**work, "remove": list(remove)}).encode()).hexdigest()
    return f"{MOVE_ID_PREFIX}_{digest[:24]}"


#: A move row's fields after its ``id``, in the order the gate shows them.
_MOVE_ROW = (
    "content_id", "location", "bucket", "kind", "add", "remove", "holds", "target",
    "decided_by", "energy", "genre", "target_bucket",
)  # fmt: skip


def _plain(value: Any) -> Any:
    return list(value) if isinstance(value, tuple) else value


def move_row(move: Move) -> dict[str, Any]:
    """One move as the gate shows it and the digest covers it. ONE BODY for both."""
    return {"id": move.move_id, **{name: _plain(getattr(move, name)) for name in _MOVE_ROW}}


def left_row(left: Left) -> dict[str, Any]:
    """One track left where it is, as the gate lists it and the digest covers it."""
    renamed = {"holds_unnamed": "holds_under_another_name"}
    return {renamed.get(f.name, f.name): _plain(getattr(left, f.name)) for f in fields(Left)}


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
        """What an approval is recorded against: ALL of what is shown, every
        row whole, so a track moved by hand since the approval changes it."""
        return to_json(self)["digest"]


def document_digest(document: Mapping[str, Any]) -> str:
    """The digest of a plan document, taken over the five things it shows.

    ONE BODY for a plan in memory and a document a job froze, so the worker can
    prove the rows it acts on are the rows approved. The document's own
    ``digest`` field is not read.
    """
    return digest_of(
        {key: document[key] for key in ("tree", "placements", "counts")}
        | {key: list(document[key]) for key in ("moves", "left")}
    )


def _left_reason(
    declared: taxonomy.Taxonomy,
    entry: PlanEntry,
    kind: routing.Competing,
    unnamed: tuple[str, ...],
    stale: tuple[str, ...],
) -> str:
    """Why a track holding a stale sub is left where it is, or nothing.

    A bucket reading neither energy nor genre declares one place for
    everything, so nothing about a file decides there: ``no-reading``. A genre
    the resolver's map does not hold gets a default, which is no reading.

    Leaving a former place or a split place for the no reading sub needs no
    reading (R-797, U118): nothing has to decide whether a track belongs in a
    playlist the taxonomy stopped declaring as its place. A track holding a
    stale BAND as well is still left, since which band is right is what a
    reading answers. A default STYLE is never treated this way.
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
    elsewhere: frozenset[str] = frozenset(),
) -> Move | Left | None:
    """What one entry comes to in the bucket it claims: a move, a track left, or neither.

    ONE BODY FOR THE PLAN AND FOR THE WORKER'S CHECK OF IT, so every condition
    that leaves a track alone at planning time leaves it alone at write time.
    Over the entries adoption routes, which include a track already in its sub
    and in a stale one as well (R-734), and the ones it withholds over a place.
    An entry a verdict withheld is not moved: a person refused that folder.
    A split place whose holder the track's other entry claims (``elsewhere``,
    U340) is that entry's band, never a stale place here.
    """
    if not placements.read or not entry.bucket or not claims(entry, entry.bucket):
        return None
    kind, competing = routing.competing_subs(declared, entry.bucket)
    if entry.sub not in competing:
        return None
    # A FORMER PLACE OR A SPLIT PLACE IS NEVER A TARGET (R-797, U118). No
    # resolver answers with one, so this entry was built by hand, and a move on
    # it would file a track into a playlist the taxonomy does not declare.
    if (
        routing.former_place(declared, entry.bucket, entry.sub) is not None
        or routing.split_place(declared, entry.bucket, entry.sub) is not None
    ):
        return None
    held = tuple(
        sorted(held_in(placements, declared, entry.bucket, entry.content_id, elsewhere=elsewhere))
    )
    stale = tuple(sub for sub in held if sub != entry.sub)
    if not stale:
        return None
    unnamed = _unnamed(placements, entry, entry.bucket, held)
    reason = _left_reason(declared, entry, kind, unnamed, stale)
    if reason:
        return _left(entry, entry.bucket, kind, reason, entry.sub, held, unnamed)
    return _move(entry, entry.bucket, kind, entry.sub, held, tree=tree)


def held_in(
    placements: Placements,
    declared: taxonomy.Taxonomy,
    bucket: str,
    content_id: str,
    *,
    elsewhere: frozenset[str] = frozenset(),
) -> frozenset[str]:
    """The competing subs of ``bucket`` a track holds, less a split place its
    other entry keeps (U340). ONE BODY for the plan, the worker's check of it
    and the worker's read back, so all three agree a split pair's other band
    is never a place it is leaving."""
    _kind, competing = routing.competing_subs(declared, bucket)
    held = set(placements.holds(bucket, content_id)) & competing
    return frozenset(held - kept_beside(declared, bucket, elsewhere))


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
    """One track left where it is. ONE BUILDER for every path."""
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


def _listed(
    entry: PlanEntry,
    bucket: str,
    kind: routing.Competing,
    placements: Placements,
    held: tuple[str, ...],
    refused: bool,
    otherwise: str,
) -> Left:
    """A track listed and never moved, under the most specific reason that is
    true: a renamed playlist, then a refused folder, then ``otherwise``."""
    unnamed = _unnamed(placements, entry, bucket, held)
    if unnamed:
        reason = LEFT_UNNAMED
    elif refused:
        reason = LEFT_VERDICT
    else:
        reason = otherwise
    return _left(entry, bucket, kind, reason, "", held, unnamed)


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
    """Whether adoption's entry speaks for this bucket: the genre routed the
    track there and adoption placed it or withheld it over a place it holds."""
    if entry.bucket != bucket or not entry.sub:
        return False
    if entry.disposition is Disposition.ROUTE:
        return True
    return entry.disposition is Disposition.WITHHELD and entry.held_elsewhere


def reading_target(entry: PlanEntry, bucket: str, declared: taxonomy.Taxonomy) -> str:
    """The sub of ``bucket`` the file's reading names, or nothing.

    ONE READING, TWO WAYS OF ASKING FOR IT: in the bucket the entry claims, the
    sub adoption resolved; in any other, the same resolver asked directly with
    the same reading. A bucket the taxonomy no longer declares names nothing.
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
    entries :func:`cratekit.adopt.plan.with_collision_verdicts` withheld. So a
    bucket no entry routes to cannot be known refused here, a gap recorded
    rather than hidden.
    """
    return frozenset(entry.bucket for entry in entries if entry.withheld_by == WITHHELD_BY_VERDICT)


def tree_path_decides(kind: routing.Competing) -> bool:
    """Whether the tree path decides in a bucket whose competing subs are ``kind``.

    BAND BUCKETS ONLY: a genre that does not name a bucket says nothing about
    which of its styles is right. One predicate for every tree path question.
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
    """What one track comes to in a bucket adoption's entry does not claim.

    Only where it holds two or more competing subs of a bucket
    :func:`tree_path_decides` admits, or a split or former place alone, which
    is listed and never moved. NOTHING IS ADDED HERE. An excluded track has no
    reading whatever its row carries.
    """
    kind, competing = routing.competing_subs(declared, bucket)
    split = held_in_split_place(entry, bucket, placements, declared)
    if split:
        return _listed(entry, bucket, kind, placements, split, bucket in refused, LEFT_NO_READING)
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


def in_former_place_only(declared: taxonomy.Taxonomy, bucket: str, held: Sequence[str]) -> bool:
    """Whether everything a track holds in ``bucket`` is a former place of it.

    Of the bucket that DECLARES the place, so the track is listed once, under
    the bucket that took the place over. ONE PREDICATE for the buckets the plan
    asks about and for what it finds there.
    """
    former = {place.id for place in declared.bucket(bucket).formerly}
    return bool(held) and set(held) <= former


def settled_in_the_other_bucket(
    entry: PlanEntry, bucket: str, declared: taxonomy.Taxonomy
) -> frozenset[str]:
    """The places of ``bucket`` the tree path must not read as held.

    A FORMER PLACE COMPETES IN TWO BUCKETS AND IS SETTLED IN ONE. When the
    entry claims the other of the two, :func:`standing` decides the place
    there, so here it is not held at all; otherwise both buckets would plan
    leaving the one membership.

    A SPLIT PLACE IS NEVER THE TREE PATH'S IN EITHER BUCKET (U118). In the
    declarer every track in the holder's band reads as holding it, the
    holder's own tracks included, so only :func:`standing` decides on it. In
    the holder the band is settled by the declarer when the entry claims it or
    its genre names it, so the holder does not move a track between its bands
    while the declarer moves it out of both.
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

    THE FALLBACK TIER NAMES NOTHING, as adoption's census reads it: a taxonomy
    whose fallback is this bucket would otherwise read every unrecognised genre
    as naming it. Asked where no entry claims the bucket, since an unreadable
    file or a refused folder still carries the genre its row was read with.
    """
    resolution = routing.resolve_bucket(declared, entry.genre)
    return resolution.match is not routing.Match.FALLBACK and resolution.bucket_id == bucket


def held_in_split_place(
    entry: PlanEntry, bucket: str, placements: Placements, declared: taxonomy.Taxonomy
) -> tuple[str, ...]:
    """The split places of ``bucket`` a track sits in that no entry moves it out of.

    ONLY WHEN ITS GENRE NAMES ``bucket`` AND ITS ENTRY DOES NOT CLAIM IT (U118),
    an unreadable file or a refused folder. Such a track is LISTED, never
    moved, so the gate names every one still in the holder's places before the
    split's declaration is deleted. A track whose genre names the holder, or
    nothing, is the holder's and is never asked about here.
    """
    split = {place.id for place in declared.bucket(bucket).split_from}
    if not split or claims(entry, bucket) or not genre_names(entry, bucket, declared):
        return ()
    return tuple(sorted(set(placements.holds(bucket, entry.content_id)) & split))


def held_in_tree(
    entry: PlanEntry,
    bucket: str,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    competing: frozenset[str],
) -> tuple[str, ...]:
    """The competing subs of ``bucket`` the tree path reads a track as holding.
    ONE BODY for every tree path question, so all agree about a settled place."""
    settled = settled_in_the_other_bucket(entry, bucket, declared)
    return tuple(sorted((set(placements.holds(bucket, entry.content_id)) & competing) - settled))


def _doubled(
    entry: PlanEntry,
    bucket: str,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    competing: frozenset[str],
) -> set[str]:
    """The competing subs the track holds through two rows, settled places aside."""
    settled = settled_in_the_other_bucket(entry, bucket, declared)
    return (set(placements.holds_doubled(bucket, entry.content_id)) & competing) - settled


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

    ``no-reading`` when its genre names this bucket or the one whose folder
    holds the place, so only the census failed to read it; otherwise the genre
    names another bucket or none.
    """
    named_by_genre = {
        bucket,
        *(place.bucket for place in declared.bucket(bucket).formerly if place.id in held),
    }
    genre_names_it = any(genre_names(entry, named, declared) for named in named_by_genre)
    otherwise = LEFT_NO_READING if genre_names_it else LEFT_FORMER
    return _listed(entry, bucket, kind, placements, held, bool(named_by_genre & refused), otherwise)


def standing_in(
    entry: PlanEntry,
    bucket: str,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    *,
    tree: str,
    refused: frozenset[str] = frozenset(),
    elsewhere: frozenset[str] = frozenset(),
    moved: Mapping[str, frozenset[str]] | None = None,
) -> Move | Left | None:
    """What one track comes to in one bucket: a move, a track left, or neither.

    ONE BODY FOR THE PLAN AND FOR THE WORKER'S CHECK OF IT, over every bucket a
    move can name. The bucket the entry claims goes to :func:`standing`, R-758's
    rule; a bucket a person moved the track's genre out of to
    :func:`moved_out_of` (U339); every other to the tree path R-780 added.
    ``refused`` is :func:`refused_buckets` over the plan the entry came from,
    ``moved`` :func:`cratekit.adopt.genre_moves.read`.
    """
    if not placements.read:
        return None
    if claims(entry, bucket):
        return standing(entry, placements, declared, tree=tree, elsewhere=elsewhere)
    if genre_moved_out_of(entry, bucket, declared, moved):
        return moved_out_of(entry, bucket, placements, declared, tree=tree, refused=refused)
    return _standing_in_tree(entry, bucket, placements, declared, tree=tree, refused=refused)


def still_moved(
    entries: Sequence[PlanEntry],
    declared: taxonomy.Taxonomy,
    moved: Mapping[str, frozenset[str]] | None,
) -> Mapping[str, frozenset[str]]:
    """``moved`` less every bucket ANY of a track's entries claims or whose genre
    names it: asked per content identifier, never per entry, so a bucket a
    second entry of the same track files it in (U340) is never left."""
    if not moved:
        return {}
    kept: dict[str, set[str]] = {key: set(value) for key, value in moved.items()}
    for entry in entries:
        held = kept.get(entry.content_id)
        if not held:
            continue
        held -= {bucket for bucket in held if claims(entry, bucket)}
        held -= {bucket for bucket in held if genre_names(entry, bucket, declared)}
    return {key: frozenset(value) for key, value in kept.items() if value}


def genre_moved_out_of(
    entry: PlanEntry,
    bucket: str,
    declared: taxonomy.Taxonomy,
    moved: Mapping[str, frozenset[str]] | None,
) -> bool:
    """Whether a person moved this track's genre out of ``bucket`` (U339) and it
    still does not name it: a genre moved back is the tree path's again."""
    return (
        bool(moved)
        and bucket in (moved or {}).get(entry.content_id, frozenset())
        # THE ENTRY OF THE GENRE A PERSON GAVE, never a second genre's (U340),
        # so one track leaves its old folder by one move.
        and not entry.second
        and not claims(entry, bucket)
        and not genre_names(entry, bucket, declared)
    )


def moved_out_of(
    entry: PlanEntry,
    bucket: str,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    *,
    tree: str,
    refused: frozenset[str] = frozenset(),
) -> Move | Left | None:
    """What a track comes to in a bucket a person moved its genre out of (U339).

    EVERY COMPETING SUB IT HOLDS THERE IS LEFT, ONE MEMBERSHIP AS MUCH AS TWO,
    for the sub its new genre's entry resolved in the bucket that entry claims,
    added when the track is not in it yet. Listed and never moved: a playlist
    held under another name, an entry that claims no bucket (no reading), and a
    new bucket a person's verdict refused or that names a former or split place.
    """
    kind, competing = routing.competing_subs(declared, bucket)
    held = held_in_tree(entry, bucket, placements, declared, competing)
    if not held:
        return None
    into = entry.bucket
    unnamed = _unnamed(placements, entry, bucket, held)
    target = entry.sub if claims(entry, into) else ""
    if target and (
        routing.former_place(declared, into, target) is not None
        or routing.split_place(declared, into, target) is not None
        or target not in routing.competing_subs(declared, into)[1]
    ):
        target = ""
    if unnamed:
        reason = LEFT_UNNAMED
    elif into in refused or entry.withheld_by == WITHHELD_BY_VERDICT:
        reason = LEFT_VERDICT
    elif not target:
        reason = LEFT_NO_READING
    else:
        reason = ""
    if reason:
        return _left(entry, bucket, kind, reason, target, held, unnamed)
    return Move(
        move_id=move_id_for(tree, entry.content_id, bucket, target, held, into),
        content_id=entry.content_id,
        location=entry.recorded,
        bucket=bucket,
        kind=str(kind.value),
        target=target,
        add="" if target in placements.holds(into, entry.content_id) else target,
        remove=held,
        holds=held,
        energy=entry.energy,
        genre=entry.genre,
        target_bucket=into,
    )


def buckets_asked(
    entry: PlanEntry,
    placements: Placements,
    declared: taxonomy.Taxonomy,
    competing: Mapping[str, tuple[routing.Competing, frozenset[str]]],
    moved: Mapping[str, frozenset[str]] | None = None,
    *,
    elsewhere: frozenset[str] = frozenset(),
) -> tuple[str, ...]:
    """Every bucket the plan asks about one track, in the taxonomy's order.

    The bucket the entry claims, every bucket the track holds nothing in but a
    former place (R-797) or holds a split place no entry moves it out of
    (U118), every bucket a person moved its genre out of that holds it at all
    (U339), and every band bucket that holds the track twice or more, through
    two subs or two rows of one. Declared order, so two plans over one tree
    list the same rows in the same order and digest the same.

    A BUCKET IN ``elsewhere`` IS NEVER ASKED (U340): the track's other entry
    claims it, a second genre's folder beside the first's, and that entry's
    own question decides it, so no tree path question plans a move or a
    listing there from this one.
    """
    asked: list[str] = []
    for bucket in declared.buckets:
        if claims(entry, bucket.id):
            asked.append(bucket.id)
            continue
        if bucket.id in elsewhere:
            continue
        kind, subs = competing[bucket.id]
        # ONLY A BUCKET THAT DECLARES A FORMER PLACE CAN MATCH, whatever its kind.
        if bucket.formerly and in_former_place_only(
            declared, bucket.id, held_in_tree(entry, bucket.id, placements, declared, subs)
        ):
            asked.append(bucket.id)
            continue
        if held_in_split_place(entry, bucket.id, placements, declared):
            asked.append(bucket.id)
            continue
        if genre_moved_out_of(entry, bucket.id, declared, moved) and held_in_tree(
            entry, bucket.id, placements, declared, subs
        ):
            asked.append(bucket.id)
            continue
        if not tree_path_decides(kind):
            continue
        held = held_in_tree(entry, bucket.id, placements, declared, subs)
        if len(held) >= 2 or _doubled(entry, bucket.id, placements, declared, subs):
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

    LISTED, NOT A STANDING, so the worker never reads the double as a reason to
    leave a track. Omitted beside a move, whose next plan lists it.
    """
    if not _doubled(entry, bucket, placements, declared, competing):
        return None
    target = reading_target(entry, bucket, declared)
    held = held_in_tree(entry, bucket, placements, declared, competing)
    return _left(entry, bucket, routing.Competing.BAND, LEFT_DOUBLED_ROWS, target, held, ())


def claimed_buckets(entries: Sequence[PlanEntry]) -> dict[str, frozenset[str]]:
    """Each track's buckets claimed by any of its entries (U340).

    A track with a second genre has two entries, each claiming its own bucket,
    and both are the track's: what one claims is never another's tree path.
    """
    found: dict[str, set[str]] = {}
    for entry in entries:
        found.setdefault(entry.content_id, set()).update(_own(entry))
    return {content_id: frozenset(buckets) for content_id, buckets in found.items()}


def elsewhere_of(claimed: Mapping[str, frozenset[str]], entry: PlanEntry) -> frozenset[str]:
    """The buckets the track's other entries claim, from :func:`claimed_buckets`.
    ONE ANSWER for the plan and for the worker's check of it."""
    return claimed.get(entry.content_id, frozenset()) - _own(entry)


def _own(entry: PlanEntry) -> frozenset[str]:
    """The bucket one entry claims, or nothing."""
    return frozenset({entry.bucket}) if claims(entry, entry.bucket) else frozenset()


def entry_for(
    entries: Mapping[str, Sequence[PlanEntry]], content_id: str, bucket: str
) -> PlanEntry | None:
    """The entry of a track that speaks for ``bucket``: the one claiming it, else its first.

    THE WORKER'S LOOKUP (U340), so a move approved in a second genre's folder
    is checked against the entry that planned it. None when the plan has no
    entry for the track at all.
    """
    found = entries.get(content_id, ())
    for entry in found:
        if claims(entry, bucket):
            return entry
    return next((entry for entry in found if not entry.second), found[0] if found else None)


def entries_by_track(entries: Sequence[PlanEntry]) -> dict[str, tuple[PlanEntry, ...]]:
    """Every entry of a plan, by track, in plan order."""
    found: dict[str, list[PlanEntry]] = {}
    for entry in entries:
        found.setdefault(entry.content_id, []).append(entry)
    return {content_id: tuple(group) for content_id, group in found.items()}


def build_move_plan(
    plan: AdoptionPlan,
    declared: taxonomy.Taxonomy,
    moved: Mapping[str, frozenset[str]] | None = None,
) -> MovePlan:
    """Every track holding a competing sub its reading does not name.

    OVER EVERY BUCKET THE TREE HOLDS EACH TRACK IN (R-780): the entry's own
    bucket first, as R-758 asked it, then every band bucket the track doubles
    in, and every bucket ``moved`` says a person moved its genre out of (U339).
    A TREE NOBODY READ PLANS NOTHING and the plan says ``unread``, so an
    approval given over it is not honoured once the tree can be read.
    """
    moves: list[Move] = []
    left: list[Left] = []
    moved = still_moved(plan.entries, declared, moved)
    if plan.placements.read:
        competing = {
            bucket.id: routing.competing_subs(declared, bucket.id) for bucket in declared.buckets
        }
        refused = refused_buckets(plan.entries)
        claimed = claimed_buckets(plan.entries)
        for entry in plan.entries:
            elsewhere = elsewhere_of(claimed, entry)
            for bucket in buckets_asked(
                entry, plan.placements, declared, competing, moved, elsewhere=elsewhere
            ):
                found = standing_in(
                    entry, bucket, plan.placements, declared, tree=plan.tree, refused=refused,
                    elsewhere=elsewhere, moved=moved,
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
        tree=plan.tree, placements=plan.placements.state, moves=tuple(moves), left=tuple(left)
    )


def to_json(plan: MovePlan) -> dict[str, Any]:
    """The plan as a structured document. A transport, never an editing surface."""
    body = {
        "placements": plan.placements,
        "counts": plan.counts(),
        "moves": [move_row(move) for move in plan.moves],
        "left": [left_row(left) for left in plan.left],
    }
    return {"tree": plan.tree, "digest": document_digest({"tree": plan.tree, **body}), **body}


def from_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[Move, ...]:
    """The moves an approval froze, read back out of a job's payload.

    Every field is read by name and none is defaulted, so a payload short of
    one raises here rather than moving a track on half a row, BUT
    ``target_bucket``, which a job frozen before U339 does not carry and which
    is empty for every move within one bucket.
    """
    return tuple(
        Move(
            move_id=str(row["id"]),
            **{key: str(row[key]) for key in ("content_id", "location", "bucket", "kind")},
            target=str(row["target"]),
            add=str(row["add"]),
            remove=tuple(str(sub) for sub in row["remove"]),
            holds=tuple(str(sub) for sub in row["holds"]),
            energy=None if row["energy"] is None else int(row["energy"]),
            genre=str(row["genre"]),
            target_bucket=str(row.get("target_bucket") or ""),
        )
        for row in rows
    )
