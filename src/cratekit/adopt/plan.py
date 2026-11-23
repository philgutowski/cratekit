"""The adoption plan, and the review items it becomes.

THE PLAN IS NOT A FILE (R26). Verdicts have to outlive the process that
collected them, and a file a person edits cannot tell an answer from a typo, so
the plan is a value in memory and its OPEN QUESTIONS are persisted review items
in the queue U11 declared (R12). The applied half is a separate ledger, because
"somebody decided this" and "the library has this" are different facts.

TWO QUESTIONS ARE ASKED, and neither is "is this plan ok":

1. **A track whose genre cannot place it.** The options are the declared
   buckets, so a user's own template produces its own menu, and nothing is sent
   into the fallback folder in bulk.
2. **A declared folder that already exists holding tracks this plan does not
   name.** It is surfaced rather than merged, because a merge cannot be undone
   by re-running anything. The ANSWER BINDS, through
   :func:`with_collision_verdicts`.

WHERE A TRACK ALREADY SITS IS READ (R-731). :class:`Placements` is what the tree
holds, handed in as data, and an entry whose track holds a different competing
sub in the same bucket is WITHHELD and listed, because the membership writer
only adds. Nothing is moved or removed; which reading is right is a person's.

A VOX TAGGED TRACK IS FILED UNDER ITS BUCKET'S VOCAL SUB TOO (R-788).
:class:`Vocals` is which tracks carry the tag and which vocal subs hold them,
handed in as data. The tag is the recorded outcome of the one rule that decides
what is vocal, so no score is read here, and a library with no calibrated cut
files nothing vocal.

THE IDENTITY OF A COLLISION IS THE NODE, NEVER ITS NAME (U19). A record keyed on
the display name is a different collision once the folder is renamed, and the
person who answered is asked again. The review item's identity is the tree, the
bucket and the library node; the display name rides in the payload as a label.

Layer: modules.
"""

from __future__ import annotations

import functools
import hashlib
from collections import Counter
from dataclasses import dataclass, field, replace
from typing import Any, Callable, Mapping, Sequence

from cratekit.adopt.scan import Disposition, Readability, ScannedTrack, classify_genre
from cratekit.cli.output import canonical_json, digest_of
from cratekit.core import routing, taxonomy
from cratekit.core.review import Option, Queue, ReviewStore, offer
from cratekit.write import genre_favorites
from cratekit.write.trees import VOX_SUB_CLASS

#: The prefix every plan entry identifier carries. It differs from the review
#: queue's and the decision stores', so an identifier pasted into the wrong verb
#: fails to resolve rather than silently missing.
ENTRY_ID_PREFIX = "ap"

#: The kinds the two questions are filed under in the review queue.
KIND_GENRE = "adoption-genre"
KIND_COLLISION = "adoption-collision"

#: The two answers to a collision, a closed set: merge or do not merge.
COLLISION_ADOPT = "adopt-existing"
COLLISION_SEPARATE = "keep-separate"

#: Why an entry is withheld when a collision verdict is the reason. The other
#: reasons are the members of :class:`cratekit.core.routing.Competing`.
WITHHELD_BY_VERDICT = "verdict"

#: The two states of :attr:`Placements.read`, as the plan document spells them.
PLACEMENTS_READ = "read"
PLACEMENTS_UNREAD = "unread"


@dataclass(frozen=True, slots=True)
class Placements:
    """The competing subs each track already holds, by bucket. Supplied, not read.

    Built by :mod:`cratekit.adopt.placements`, the layer holding a database open.

    ``read`` IS A FACT OF ITS OWN, not the emptiness of ``held``: an unreadable
    tree and an empty one both hold nothing. An unread tree withholds nothing,
    says ``unread`` on the plan and moves the digest.

    ``held`` maps a bucket identifier to a content identifier to the sub
    identifiers that track holds there, never display names (R19, D5).
    ``unnamed`` is the part held ONLY through a playlist that no longer carries
    the declared names: the writer finds a playlist by name, so it would make a
    second one beside it. ``doubled`` is the part held through more than one
    active row in one playlist (R-781), which a set cannot say.

    ``alongside`` maps a bucket to a track to the places filed beside its band
    it sits in there, :func:`alongside_places`, never a competing sub, and
    ``alongside_unnamed`` the part held under another name only. ``others``
    maps a bucket to a track to the names of the other playlists of that
    bucket's own folder holding it, a manual class or one made by hand: what
    keeps a track in the folder, which the genre Favorites mirror files by.
    All three are read for the move across genre folders alone (R-1965).
    """

    read: bool = False
    held: Mapping[str, Mapping[str, tuple[str, ...]]] = field(default_factory=dict)
    unnamed: Mapping[str, Mapping[str, tuple[str, ...]]] = field(default_factory=dict)
    doubled: Mapping[str, Mapping[str, tuple[str, ...]]] = field(default_factory=dict)
    alongside: Mapping[str, Mapping[str, tuple[str, ...]]] = field(default_factory=dict)
    alongside_unnamed: Mapping[str, Mapping[str, tuple[str, ...]]] = field(default_factory=dict)
    others: Mapping[str, Mapping[str, tuple[str, ...]]] = field(default_factory=dict)

    def holds(self, bucket: str, content_id: str) -> tuple[str, ...]:
        """The subs of ``bucket`` this track sits in, or none."""
        return tuple(self.held.get(bucket, {}).get(content_id, ()))

    def holds_unnamed(self, bucket: str, content_id: str) -> tuple[str, ...]:
        """The subs of ``bucket`` this track holds under another name only."""
        return tuple(self.unnamed.get(bucket, {}).get(content_id, ()))

    def holds_doubled(self, bucket: str, content_id: str) -> tuple[str, ...]:
        """The subs of ``bucket`` this track holds through two or more rows."""
        return tuple(self.doubled.get(bucket, {}).get(content_id, ()))

    def holds_alongside(self, bucket: str, content_id: str) -> tuple[str, ...]:
        """The places filed beside the band of ``bucket`` this track sits in, or none."""
        return tuple(self.alongside.get(bucket, {}).get(content_id, ()))

    def holds_alongside_unnamed(self, bucket: str, content_id: str) -> tuple[str, ...]:
        """The places beside the band of ``bucket`` it holds under another name only."""
        return tuple(self.alongside_unnamed.get(bucket, {}).get(content_id, ()))

    def holds_others(self, bucket: str, content_id: str) -> tuple[str, ...]:
        """The other playlists of ``bucket``'s own folder this track sits in, by name."""
        return tuple(self.others.get(bucket, {}).get(content_id, ()))

    @property
    def state(self) -> str:
        return PLACEMENTS_READ if self.read else PLACEMENTS_UNREAD


#: The placements of a tree nobody read, the default everywhere one is taken.
UNREAD = Placements()

#: The states of :attr:`PlanEntry.vocal` for a vox tagged track; empty otherwise.
#: Not in the bucket's vocal sub, and an apply adds it.
VOCAL_ADD = "add"
#: Already in the sub under the declared name.
VOCAL_PRESENT = "present"
#: The sub answers under another name only, for the track or for the bucket, so
#: nothing is added: the writer would make a second playlist beside it.
VOCAL_RENAMED = "under-another-name"
#: The bucket has no vocal sub.
VOCAL_NO_SUB = "no-sub"
#: The track has no bucket: unanswered genre, unadoptable file, or no place
#: declared for its reading.
VOCAL_NO_BUCKET = "no-bucket"
#: Not in the sub and its entry is withheld, so nothing is added.
VOCAL_WITHHELD = "withheld"

#: Every state, in summary order. Every tagged track is in exactly one.
VOCAL_STATES = (
    VOCAL_ADD,
    VOCAL_PRESENT,
    VOCAL_RENAMED,
    VOCAL_NO_SUB,
    VOCAL_NO_BUCKET,
    VOCAL_WITHHELD,
)

#: The states whose membership an apply may write; see :meth:`AdoptionPlan.digest`
#: for why ``present`` is one.
VOCAL_PLANNED = frozenset({VOCAL_ADD, VOCAL_PRESENT})

#: The five states of :attr:`Vocals.state`. The first four each say why no vocal
#: membership is planned at all.
VOCALS_UNREAD = "unread"
VOCALS_NO_SUB = VOCAL_NO_SUB
VOCALS_UNCALIBRATED = "uncalibrated"
VOCALS_NO_TAG = "no-tag"
VOCALS_READ = "read"


@dataclass(frozen=True, slots=True)
class Vocals:
    """Which tracks carry the vox tag, and which vocal subs hold them. Supplied.

    ``read`` is a fact of its own: an unread tree plans no vocal membership,
    since an add planned blind is a second row wherever the first one was.
    ``has_sub`` is whether any bucket has a vocal sub; without one neither the
    calibration nor the tag is read. ``calibrated`` is whether the library has a
    with vox cut on record (R-276), a condition on the library and not on the
    tags. ``tag_found`` is not the emptiness of ``tagged``: no tag and no tagged
    track are different facts the plan names.

    ``filed`` maps a bucket to the tracks in its vocal sub by either name, and
    ``unnamed`` is the part held only under another name. ``renamed`` is the
    buckets whose vocal sub has no playlist of the declared names and one the
    record knows under another; they gain no vocal membership at all.
    """

    read: bool = False
    has_sub: bool = False
    calibrated: bool = False
    tag_found: bool = False
    tagged: frozenset[str] = frozenset()
    filed: Mapping[str, frozenset[str]] = field(default_factory=dict)
    unnamed: Mapping[str, frozenset[str]] = field(default_factory=dict)
    renamed: frozenset[str] = frozenset()

    def carries(self, content_id: str) -> bool:
        """Whether this track carries the vox tag."""
        return content_id in self.tagged

    def sits(self, bucket: str, content_id: str) -> bool:
        """Whether this track is in the vocal sub of ``bucket``, by either name."""
        return content_id in self.filed.get(bucket, ())

    def sits_unnamed(self, bucket: str, content_id: str) -> bool:
        """Whether this track is in that sub under another name only."""
        return content_id in self.unnamed.get(bucket, ())

    @property
    def filing(self) -> bool:
        """Whether a vocal membership may be planned from this at all."""
        return self.read and self.has_sub and self.calibrated

    @property
    def state(self) -> str:
        if not self.read:
            return VOCALS_UNREAD
        if not self.has_sub:
            return VOCALS_NO_SUB
        if not self.calibrated:
            return VOCALS_UNCALIBRATED
        return VOCALS_READ if self.tag_found else VOCALS_NO_TAG


#: The vocals of a library nobody read, the default everywhere one is taken.
NO_VOCALS = Vocals()


@dataclass(frozen=True, slots=True)
class ExistingFolder:
    """A folder the library already has directly under the tree being adopted.

    Supplied by the caller, so the decision is testable without a database.
    ``node_id`` is the library's own identifier and what a record keys on;
    ``display`` is a label.
    """

    node_id: str
    display: str
    content_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Collision:
    """A declared bucket whose folder already exists holding something else.

    ``strangers`` counts the rows under the folder this plan does not name, and
    is never zero: a folder holding exactly what the plan puts there is no
    conflict.
    """

    tree: str
    bucket: str
    node_id: str
    display: str
    strangers: int

    def identity(self) -> dict[str, str]:
        """What the decision is addressed by: the node, never the name."""
        return {"tree": self.tree, "bucket": self.bucket, "node": self.node_id}


@dataclass(frozen=True, slots=True)
class PlanEntry:
    """One track's place in the plan. Every scanned track has exactly one, and a
    track filed into a second genre's folder too has a second, ``second`` set (U340).

    ``entry_id`` HASHES THE WORK, the tree, row and destination, so a track whose
    destination changes is new work the applied ledger does not report as done,
    and an unmoved entry keeps its identifier across a taxonomy edit.

    ``bucket`` and ``sub`` are stable taxonomy identifiers, empty for anything not
    routing; display names are resolved at write time (R19, D5).
    """

    entry_id: str
    content_id: str
    recorded: str
    disposition: Disposition
    category: Readability
    genre: str
    tree: str
    bucket: str = ""
    sub: str = ""
    ordinal: int = 0
    path: str | None = None
    #: The census's energy reading, so a genre answered later resolves its sub
    #: from the same level.
    energy: int | None = None
    energy_unreadable: bool = False
    #: The competing subs of this bucket the track holds, when that is why it is
    #: withheld, sorted. Empty otherwise.
    holds: tuple[str, ...] = ()
    #: The part of ``holds`` held through a renamed playlist only.
    holds_unnamed: tuple[str, ...] = ()
    #: Why a withheld entry is withheld: :data:`WITHHELD_BY_VERDICT` or the kind
    #: of competing place. Empty when it is not withheld.
    withheld_by: str = ""
    #: One of :data:`VOCAL_STATES`, or empty when no vocal question applies.
    vocal: str = ""
    #: The vocal sub the bucket declares, empty when ``vocal`` is or there is none.
    vocal_sub: str = ""
    #: The entry for the track's second genre folder (U340), its ``genre`` the
    #: second genre's word. A track has at most one, beside its first entry.
    second: bool = False

    @property
    def vocal_planned(self) -> bool:
        """Whether an apply may write this track's vocal membership."""
        return self.applicable and self.vocal in VOCAL_PLANNED

    @property
    def held_elsewhere(self) -> bool:
        """Withheld because the track already holds a competing place."""
        return self.disposition is Disposition.WITHHELD and bool(self.holds)

    @property
    def applicable(self) -> bool:
        return self.disposition is Disposition.ROUTE


def entry_id_for(tree: str, content_id: str, bucket: str, sub: str) -> str:
    """The stable identifier for one piece of adoption work.

    Content addressed, so a re-scan and a second process agree on it without a
    lookup, and serialized canonically so key order cannot make a second one.
    """
    digest = hashlib.sha256(
        canonical_json({"tree": tree, "content": content_id, "bucket": bucket, "sub": sub}).encode()
    ).hexdigest()
    return f"{ENTRY_ID_PREFIX}_{digest[:24]}"


@dataclass(frozen=True, slots=True)
class AdoptionPlan:
    """Every scanned track, what adoption proposes, and what it cannot answer.

    THE PLAN HOLDS EVERY TRACK, including the ones it will not touch, so "nothing
    falls out" is the set comparison :func:`covers` makes.
    """

    tree: str
    entries: tuple[PlanEntry, ...] = ()
    collisions: tuple[Collision, ...] = ()
    #: What the tree holds, and which tracks carry the vox tag, kept so a genre
    #: answered later is checked against the same tree.
    placements: Placements = UNREAD
    vocals: Vocals = NO_VOCALS

    def applicable(self) -> tuple[PlanEntry, ...]:
        """The entries an apply may write, in plan order."""
        return tuple(entry for entry in self.entries if entry.applicable)

    def content_ids(self) -> frozenset[str]:
        return frozenset(entry.content_id for entry in self.entries)

    def firsts(self) -> tuple[PlanEntry, ...]:
        """One entry per track, its first genre's: what a per track count counts (U340)."""
        return tuple(entry for entry in self.entries if not entry.second)

    def seconds(self) -> tuple[PlanEntry, ...]:
        """Every entry for a second genre's folder (U340), in plan order."""
        return tuple(entry for entry in self.entries if entry.second)

    def counts(self) -> dict[str, int]:
        """One count per disposition and one per category, zeroes included.

        Derived over both enumerations, so "none here" and "not looked for" differ
        (AE12). The two share one mapping, so ``tests/test_adoption.py`` asserts
        their value sets are disjoint.
        """
        counts = {str(member): 0 for member in (*Disposition, *Readability)}
        for entry in self.firsts():
            counts[str(entry.disposition)] += 1
            counts[str(entry.category)] += 1
        return counts

    def energy_readings(self) -> dict[str, int]:
        """How many adoptable files held a reading, held none, or could not be read.

        Over the readable entries only: an excluded file was never opened, and
        counting it as holding no reading would read absence as evidence.
        """
        readings = {"read": 0, "absent": 0, "unreadable": 0}
        for entry in self.firsts():
            if entry.category is not Readability.READABLE:
                continue
            if entry.energy_unreadable:
                readings["unreadable"] += 1
            elif entry.energy is None:
                readings["absent"] += 1
            else:
                readings["read"] += 1
        return readings

    def withheld_by_placement(self) -> dict[str, int]:
        """How many entries are withheld over a place the track holds, by kind.

        Apart from :meth:`counts`, whose ``withheld`` mixes in verdicts. Every kind
        reads, zero included, with the total.
        """
        found = {str(member.value): 0 for member in routing.Competing}
        for entry in self.entries:
            if entry.held_elsewhere and entry.withheld_by in found:
                found[entry.withheld_by] += 1
        return {"total": sum(found.values()), **found}

    def held_elsewhere(self) -> tuple[PlanEntry, ...]:
        """Every entry withheld over a place its track holds, unbounded, in order."""
        return tuple(entry for entry in self.entries if entry.held_elsewhere)

    def outside_root(self) -> tuple[PlanEntry, ...]:
        """Every track left out because its file is outside the library root
        (U956), unbounded, in plan order: what the gate names."""
        return tuple(
            entry for entry in self.firsts() if entry.category is Readability.OUTSIDE_ROOT
        )

    def vocal_counts(self) -> dict[str, int]:
        """How many vox tagged tracks are in each vocal state, zeroes included."""
        found = {state: 0 for state in VOCAL_STATES}
        found.update(Counter(entry.vocal for entry in self.entries if entry.vocal in found))
        return found

    def vocal_memberships(self) -> tuple[PlanEntry, ...]:
        """Every entry whose vocal membership an apply may write, unbounded.

        The ones already present beside the ones to add: this is what the digest
        covers and the gate lists.
        """
        return tuple(entry for entry in self.entries if entry.vocal_planned)

    def vocal_additions(self) -> tuple[PlanEntry, ...]:
        """The part of :meth:`vocal_memberships` the tree does not hold yet."""
        return tuple(entry for entry in self.vocal_memberships() if entry.vocal == VOCAL_ADD)

    def digest(self) -> str:
        """What an approval is recorded AGAINST, so a stale one is refused.

        A canonical projection: the applicable identifiers (each hashes its sub,
        so an energy reading that moves a track moves the digest), the counts,
        the reading tally, the collisions by node, whether the tree was read, and
        the withheld rows exactly as the review list shows them (R-731).

        THE VOCAL MEMBERSHIPS ARE COVERED BY IDENTIFIER (R-788), WITHOUT SAYING
        WHICH ARE PRESENT. The apply's own write turns an addition into a
        presence, so a digest that told them apart would be moved by the apply it
        approved and a stopped run would refuse its own work. The gate therefore
        lists every one, present or not.
        """
        return digest_of(
            {
                "tree": self.tree,
                "entries": [entry.entry_id for entry in self.applicable()],
                "vocals": self.vocals.state,
                "vocal": [vocal_id(entry) for entry in self.vocal_memberships()],
                "counts": self.counts(),
                "energy": self.energy_readings(),
                "placements": self.placements.state,
                "held_elsewhere": [
                    {"id": entry.entry_id, **review_row(entry)} for entry in self.held_elsewhere()
                ],
                "collisions": sorted(f"{item.bucket}:{item.node_id}" for item in self.collisions),
                # NAMED, NOT ONLY COUNTED (U956): the gate lists them, so the same
                # count over other rows is another screen.
                "outside_root": [outside_row(entry) for entry in self.outside_root()],
            }
        )


def outside_row(entry: PlanEntry) -> dict[str, Any]:
    """One track the plan leaves outside the root, as the gate names it."""
    return {"content_id": entry.content_id, "location": entry.recorded, "path": entry.path}


def covers(plan: AdoptionPlan, scanned: Sequence[ScannedTrack]) -> frozenset[str]:
    """Rows the census produced that the plan does not carry. Empty is correct."""
    return frozenset(track.content_id for track in scanned) - plan.content_ids()


def _sub_for(
    declared: taxonomy.Taxonomy, bucket_id: str, genre: str, level: int | None
) -> str | None:
    """The sub-playlist a track lands in, from its file's energy level.

    Through :func:`cratekit.core.routing.energy_sub` with the level the census
    read, so adoption files a track where routing would. None is a real answer:
    the taxonomy declares no place for this track below the bucket.
    """
    sub = routing.energy_sub(declared, bucket_id, level, source_genre=genre)
    return None if sub is None else sub.id


@dataclass(frozen=True, slots=True)
class Predicted:
    """Where the plan would file a track that is not in the library yet (U165).

    What a native landing shows and digests before its rows exist.
    """

    disposition: Disposition
    bucket: str = ""
    sub: str = ""
    #: The bucket's vocal sub when the track will carry the vox tag, else empty.
    vocal_sub: str = ""

    def identity(self) -> list[str]:
        return [str(self.disposition), self.bucket, self.sub, self.vocal_sub]

    @classmethod
    def of(cls, entry: PlanEntry) -> Predicted:
        """What a built entry answers, in the prediction's own shape."""
        vocal_sub = entry.vocal_sub if entry.vocal == VOCAL_ADD else ""
        return cls(entry.disposition, entry.bucket, entry.sub, vocal_sub)


def predicted_place(
    declared: taxonomy.Taxonomy, genre: str, energy: int | None, *, vox: bool
) -> Predicted:
    """Where :func:`build_adoption_plan` would file a new track, by its own rule (U165).

    A new track holds no place yet, so nothing withholds it; a later plan that
    reads one answers differently and the caller says so.
    """
    disposition, bucket, _match = classify_genre(declared, genre)
    if disposition is not Disposition.ROUTE:
        return Predicted(disposition=disposition)
    sub = _sub_for(declared, bucket, genre, energy)
    if sub is None:
        return Predicted(disposition=Disposition.UNDECLARED)
    vocal = (vocal_sub(declared, bucket) or "") if vox else ""
    return Predicted(disposition=disposition, bucket=bucket, sub=sub, vocal_sub=vocal)


def review_row(entry: PlanEntry) -> dict[str, Any]:
    """One withheld entry as the review list shows it and the digest covers it.

    ONE BODY for both, so a field added to the screen is a field the approval
    binds to.
    """
    return {
        "content_id": entry.content_id,
        "location": entry.recorded,
        "bucket": entry.bucket,
        "kind": entry.withheld_by,
        "holds": list(entry.holds),
        "holds_under_another_name": list(entry.holds_unnamed),
        "planned": entry.sub,
        "energy": entry.energy,
        "energy_unreadable": entry.energy_unreadable,
        # Only on a second genre's entry (U340), so a one genre row reads as before.
        **({"second_genre": entry.genre} if entry.second else {}),
    }


def vocal_sub(declared: taxonomy.Taxonomy, bucket_id: str) -> str | None:
    """The identifier of the vocal sub one bucket has, or None.

    The additive sub class :data:`cratekit.write.trees.VOX_SUB_CLASS`, which sits
    under every bucket and is where the routing pass files a vocal track. A
    bucket has it when :func:`derived_classes` names it there.
    """
    return VOX_SUB_CLASS if VOX_SUB_CLASS in derived_classes(declared, bucket_id) else None


def derived_classes(declared: taxonomy.Taxonomy, bucket_id: str) -> tuple[str, ...]:
    """The derived sub classes one bucket's folder holds beside its band, in declared order.

    Every additive class, which automation files beside the sub a track is
    in: the vocal sub and the genre Favorites in the shipped template. A
    manual class is never one, so nothing reading this ever removes it.

    A BUCKET WHOSE OWN PLACES TAKE A CLASS'S IDENTIFIER OR NAME HAS NOT THAT
    CLASS: there the class and the bucket's own playlist are one playlist, and
    neither the reader nor the writer could tell them apart. ONE RULE for the
    vocal sub and for the move that leaves a folder (R-1965).
    """
    found: list[str] = []
    for entry in declared.sub_classes:
        if not entry.additive:
            continue
        others = tuple(other for other in declared.sub_classes if other is not entry)
        # The loader's own list of what a bucket's folder holds, without this class.
        ids, displays = taxonomy.live_places(declared.bucket(bucket_id), declared.energy, others)
        if entry.id not in ids and entry.display not in displays:
            found.append(entry.id)
    return tuple(found)


def alongside_places(declared: taxonomy.Taxonomy, bucket_id: str) -> tuple[str, ...]:
    """The places one bucket's folder files a track in beside its band, in declared order.

    The derived sub classes, :func:`derived_classes`, and the genre subs
    (U155), which the source genre picks. Every one is filed by what the track
    is, its tag, its genre or a playlist, so a track whose genre a person moved
    out of the bucket belongs in none of them there (R-1965). A manual class is
    never one.
    """
    genre = tuple(sub.id for sub in declared.bucket(bucket_id).genre_subs)
    return (*derived_classes(declared, bucket_id), *genre)


def mirrored_classes(declared: taxonomy.Taxonomy) -> frozenset[str]:
    """The derived classes that mirror a playlist, the genre Favorites (U119).

    A folder's Favorites holds every favourite sitting in ANY other playlist of
    that folder, so a track that stays in the folder keeps it (R-1965). Asked
    of :func:`cratekit.write.genre_favorites.favorites_class`, the class the
    refresh mirrors, so the two never name different classes.
    """
    found = genre_favorites.favorites_class(declared)
    return frozenset() if found is None else frozenset({found.id})


def in_own_folder(declared: taxonomy.Taxonomy, bucket_id: str, sub_id: str) -> bool:
    """Whether one competing sub of a bucket is a playlist of that bucket's own folder.

    A split place is the holder's band and a former place sits in the folder of
    the bucket that held it (R-797, U118), so in the declaring bucket neither
    is; in the holding bucket a former place is its own.
    """
    if routing.split_place(declared, bucket_id, sub_id) is not None:
        return False
    former = routing.former_place(declared, bucket_id, sub_id)
    return former is None or former.bucket == bucket_id


#: What :func:`vocal_place` answers for an entry with no vocal question.
NO_VOCAL_PLACE: tuple[str, str] = ("", "")


def vocal_place(
    vocals: Vocals,
    *,
    disposition: Disposition,
    bucket: str,
    content_id: str,
    sub_of: Callable[[str], str | None],
) -> tuple[str, str]:
    """What the plan does about one track's vocal sub, and which sub that is.

    One of :data:`VOCAL_STATES` and the sub, or :data:`NO_VOCAL_PLACE` for an
    untagged track, an unread tree, no vocal sub anywhere, or no cut on record.
    ``sub_of`` answers :func:`vocal_sub` per bucket, asked once per bucket.

    THE TAG DECIDES, and nothing here removes. A tagged track with no bucket is
    named as one. What is already there is asked before what is withheld, so a
    withheld track in its sub reads ``present``; a withheld track gains nothing.
    A track or a bucket whose sub answers under another name only gains nothing,
    because the writer would make a second playlist of the declared name.
    """
    if not vocals.filing or not vocals.carries(content_id):
        return NO_VOCAL_PLACE
    if not bucket or disposition not in (Disposition.ROUTE, Disposition.WITHHELD):
        return VOCAL_NO_BUCKET, ""
    sub = sub_of(bucket)
    if sub is None:
        return VOCAL_NO_SUB, ""
    if vocals.sits_unnamed(bucket, content_id):
        return VOCAL_RENAMED, sub
    if vocals.sits(bucket, content_id):
        return VOCAL_PRESENT, sub
    if bucket in vocals.renamed:
        return VOCAL_RENAMED, sub
    if disposition is Disposition.WITHHELD:
        return VOCAL_WITHHELD, sub
    return VOCAL_ADD, sub


def vocal_id(entry: PlanEntry) -> str:
    """The identifier of one entry's vocal membership: the entry's addressing
    over the vocal sub in place of the band."""
    return entry_id_for(entry.tree, entry.content_id, entry.bucket, entry.vocal_sub)


def vocal_row(entry: PlanEntry) -> dict[str, Any]:
    """One vocal membership an apply may write, as the plan document lists it.

    ``present`` is shown and not digested, for the reason
    :meth:`AdoptionPlan.digest` gives.
    """
    return {
        "id": vocal_id(entry),
        "content_id": entry.content_id,
        "location": entry.recorded,
        "bucket": entry.bucket,
        "sub": entry.vocal_sub,
        "present": entry.vocal == VOCAL_PRESENT,
    }


#: What :func:`competing_place` answers for an entry that may be placed.
NO_COMPETING_PLACE: tuple[str, tuple[str, ...], tuple[str, ...]] = ("", (), ())


def kept_beside(
    declared: taxonomy.Taxonomy, bucket: str, beside: frozenset[str]
) -> frozenset[str]:
    """The split places of ``bucket`` that are the track's own other folder (U340).

    A split place is a band of its holder, so a track whose other genre files
    it into that holder sits there by right: its entry there keeps it, and the
    declaring bucket neither withholds over it nor moves the track out of it.
    ``beside`` is the buckets the track's other entries claim. ONE ANSWER for
    adoption and for the move.
    """
    if not beside:
        return frozenset()
    return frozenset(
        place.id for place in declared.bucket(bucket).split_from if place.bucket in beside
    )


def competing_place(
    declared: taxonomy.Taxonomy,
    placements: Placements,
    *,
    bucket: str,
    sub: str,
    content_id: str,
    beside: frozenset[str] = frozenset(),
) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
    """Why a routed entry must be withheld and what its track holds, or nothing.

    The kind of competing place, the subs held, and those held under another name
    only; :data:`NO_COMPETING_PLACE` when the entry may be placed. What competes
    is :func:`cratekit.core.routing.competing_subs`, asked of both the planned sub
    and the held ones.

    A TRACK ALREADY IN THE PLANNED SUB IS NOT WITHHELD, since the writer adds
    nothing there, UNLESS it sits there only through a renamed playlist the
    writer cannot see, where it would be filed a second time.
    """
    if not placements.read:
        return NO_COMPETING_PLACE
    kind, competing = routing.competing_subs(declared, bucket)
    if sub not in competing:
        return NO_COMPETING_PLACE
    kept = kept_beside(declared, bucket, beside)
    held = tuple(sorted((set(placements.holds(bucket, content_id)) & competing) - kept))
    unnamed = tuple(sorted(set(placements.holds_unnamed(bucket, content_id)) & set(held)))
    if not held or (sub in held and sub not in unnamed):
        return NO_COMPETING_PLACE
    return str(kind.value), held, unnamed


def build_adoption_plan(
    scanned: Sequence[ScannedTrack],
    declared: taxonomy.Taxonomy,
    *,
    tree: str,
    existing: Sequence[ExistingFolder] = (),
    placements: Placements = UNREAD,
    vocals: Vocals = NO_VOCALS,
) -> AdoptionPlan:
    """Turn a census into a plan, resolving destinations and finding collisions.

    ``scanned`` IS A SEQUENCE because it is walked more than once (U18).
    ``placements`` and ``vocals`` default to a tree nobody read, which withholds
    nothing, plans no vocal membership, and says ``unread``.
    """
    sub_of = functools.cache(functools.partial(vocal_sub, declared))
    entries: list[PlanEntry] = []
    for ordinal, track in enumerate(scanned, start=1):
        unplaced = PlanEntry(
            entry_id="",
            content_id=track.content_id,
            recorded=track.recorded,
            disposition=track.disposition,
            category=track.readability,
            genre=track.genre,
            tree=tree,
            ordinal=ordinal,
            path=track.path,
            energy=track.energy,
            energy_unreadable=track.energy_unreadable,
        )
        bucket, sub = track.bucket, ""
        if track.disposition is Disposition.ROUTE:
            sub = _sub_for(declared, bucket, track.genre, track.energy)
        elif track.disposition is not Disposition.WITHHELD:
            bucket = ""
        second_sub = _second_sub(declared, track)
        beside = frozenset({track.second_bucket}) if second_sub else frozenset()
        entries.append(
            _destined(declared, placements, vocals, sub_of, unplaced, bucket, sub, beside=beside)
        )
        if second_sub:
            entry = replace(unplaced, genre=track.second_genre, second=True)
            entries.append(
                _destined(
                    declared, placements, vocals, sub_of, entry, track.second_bucket, second_sub,
                    beside=frozenset({bucket}) if sub else frozenset(),
                )
            )
    collisions = find_collisions(entries, declared, tree=tree, existing=existing)
    return AdoptionPlan(tree, tuple(entries), collisions, placements, vocals)


def _second_sub(declared: taxonomy.Taxonomy, track: ScannedTrack) -> str | None:
    """The sub of a routed track's second genre folder, or nothing (U340).

    By the same rules as its first entry, with the second genre's word: its
    own band from the one energy reading. EMPTY when the census named no
    second bucket or the track does not route by its first genre, and None
    when the second bucket declares no place for the reading; the one caller
    reads both as no second entry, since such an entry would file nothing
    (R-1950 removed an ``or ""`` that changed nothing any input reaches). The
    entry built on it has its own competing place and its own vocal place, and
    each of the two entries keeps a split place the other's bucket holds
    (:func:`kept_beside`).
    """
    if track.disposition is not Disposition.ROUTE or not track.second_bucket:
        return ""
    return _sub_for(declared, track.second_bucket, track.second_genre, track.energy)


def _destined(
    declared: taxonomy.Taxonomy,
    placements: Placements,
    vocals: Vocals,
    sub_of: Callable[[str], str | None],
    entry: PlanEntry,
    bucket: str,
    sub: str | None,
    *,
    beside: frozenset[str] = frozenset(),
) -> PlanEntry:
    """``entry`` routed to ``bucket`` and ``sub``, or left as it is when ``sub`` is empty.

    A ``sub`` of None is a bucket that declares no place for the track's reading,
    and the entry is UNDECLARED with no bucket. A routed entry whose track holds
    a competing place is WITHHELD and KEEPS ITS BUCKET AND SUB, as an entry a
    verdict withheld does. Its vocal place is asked of the bucket it ends with,
    and its identifier is derived from what the record holds, so a reader can
    recompute it from the record.
    """
    disposition, (withheld_by, holds, holds_unnamed) = entry.disposition, NO_COMPETING_PLACE
    if sub is None:
        disposition, bucket = Disposition.UNDECLARED, ""
    elif sub:
        withheld_by, holds, holds_unnamed = competing_place(
            declared, placements, bucket=bucket, sub=sub, content_id=entry.content_id,
            beside=beside,
        )
        disposition = Disposition.WITHHELD if withheld_by else Disposition.ROUTE
    vocal, vocal_in = vocal_place(
        vocals, disposition=disposition, bucket=bucket, content_id=entry.content_id, sub_of=sub_of
    )
    return replace(
        entry,
        entry_id=entry_id_for(entry.tree, entry.content_id, bucket, sub or ""),
        disposition=disposition,
        bucket=bucket,
        sub=sub or "",
        holds=holds,
        holds_unnamed=holds_unnamed,
        withheld_by=withheld_by,
        vocal=vocal,
        vocal_sub=vocal_in,
    )


def find_collisions(
    entries: Sequence[PlanEntry],
    declared: taxonomy.Taxonomy,
    *,
    tree: str,
    existing: Sequence[ExistingFolder],
) -> tuple[Collision, ...]:
    """Declared folders that already exist in the library holding other tracks.

    FOUND BY DISPLAY NAME, RECORDED BY NODE: the name is all a foreign library
    shares with the taxonomy, and the node is what a rename cannot change. A
    folder holding only tracks this plan names, applicable or withheld over a
    place they hold, is not a collision (P7).

    A folder renamed so it matches no bucket is not found, and adoption writes
    into a new folder beside it. Finding it needs a node map the routing pass may
    not invent a second copy of, so the gap is left visible rather than closed.
    """
    planned_by_bucket: dict[str, set[str]] = {}
    named_by_bucket: dict[str, set[str]] = {}
    for entry in entries:
        if entry.applicable or entry.held_elsewhere:
            into = planned_by_bucket if entry.applicable else named_by_bucket
            into.setdefault(entry.bucket, set()).add(entry.content_id)
    by_display = {folder.display: folder for folder in existing}
    found: list[Collision] = []
    for bucket_id in sorted(planned_by_bucket):
        folder = by_display.get(declared.bucket(bucket_id).display)
        if folder is None:
            continue
        strangers = (
            set(folder.content_ids)
            - planned_by_bucket[bucket_id]
            - named_by_bucket.get(bucket_id, set())
        )
        if strangers:
            found.append(Collision(tree, bucket_id, folder.node_id, folder.display, len(strangers)))
    return tuple(found)


def bucket_options(declared: taxonomy.Taxonomy) -> tuple[Option, ...]:
    """Every declared bucket as a candidate, addressed by its stable identifier."""
    return tuple(Option(option_id=bucket.id, summary=bucket.display) for bucket in declared.buckets)


def collision_row(collision: Collision) -> dict[str, Any]:
    """One collision as the review item's payload and the plan document carry it."""
    return {key: getattr(collision, key) for key in ("bucket", "node_id", "display", "strangers")}


#: The two answers a collision is offered.
_COLLISION_OPTIONS = (
    Option(option_id=COLLISION_ADOPT, summary="write into the folder that is already there"),
    Option(option_id=COLLISION_SEPARATE, summary="leave that folder alone and place nothing in it"),
)


def offer_plan(
    store: ReviewStore, plan: AdoptionPlan, declared: taxonomy.Taxonomy, *, handler_key: str
) -> tuple[str, ...]:
    """Put the plan's open questions in the review queue. Returns the item ids.

    IDEMPOTENT through :func:`cratekit.core.review.offer`: a settled item keeps
    its verdict and does not reopen. An excluded track is not offered, since it
    is a fact about the machine and not a question; the plan carries it (AE12).
    """
    candidates = bucket_options(declared)
    questions = [
        (
            KIND_GENRE,
            {"tree": entry.tree, "content": entry.content_id},
            {
                "content_id": entry.content_id,
                "location": entry.recorded,
                "genre": entry.genre,
                "reason": str(entry.disposition),
            },
            candidates,
        )
        for entry in plan.entries
        if entry.disposition is Disposition.NEEDS_GENRE
    ]
    # A collision's display name is a LABEL, refreshed on every re-offer.
    questions += [
        (KIND_COLLISION, collision.identity(), collision_row(collision), _COLLISION_OPTIONS)
        for collision in plan.collisions
    ]
    return tuple(
        offer(
            store,
            queue=Queue.ADOPTION,
            kind=kind,
            identity=identity,
            payload=payload,
            options=options,
            handler_key=handler_key,
        ).item_id
        for kind, identity, payload, options in questions
    )


def with_verdicts(
    plan: AdoptionPlan, answers: Mapping[str, str], declared: taxonomy.Taxonomy
) -> AdoptionPlan:
    """Fold answered genre questions back into the plan as routable entries.

    ``answers`` maps a row identifier to the chosen bucket, as data, so this stays
    pure. An answer naming a bucket the taxonomy does not declare is IGNORED: it
    comes from a template that has since changed. An answered track is checked
    against the same tree and its vocal sub asked of the bucket it was given.
    Nothing under ``src`` calls this today; this module's tests hold the rule.
    """
    declared_ids = set(declared.bucket_ids())
    sub_of = functools.cache(functools.partial(vocal_sub, declared))
    updated: list[PlanEntry] = []
    for entry in plan.entries:
        chosen = answers.get(entry.content_id)
        if entry.disposition is not Disposition.NEEDS_GENRE or chosen not in declared_ids:
            updated.append(entry)
            continue
        sub = _sub_for(declared, chosen, entry.genre, entry.energy)
        if sub is None:
            updated.append(replace(entry, disposition=Disposition.UNDECLARED))
            continue
        updated.append(
            _destined(declared, plan.placements, plan.vocals, sub_of, entry, chosen, sub)
        )
    return replace(plan, entries=tuple(updated))


def with_collision_verdicts(plan: AdoptionPlan, answers: Mapping[str, str]) -> AdoptionPlan:
    """Fold answered collision questions back into the plan. The answer BINDS.

    ``answers`` maps a folder's NODE identifier to a verdict. ``keep-separate``
    withholds every entry routed to that bucket, and its vocal additions with it
    (R-788); a track already in the vocal sub stays ``present``. ``adopt-existing``
    leaves the entries as they were, which is safe only because the collision is
    surfaced and the digest moves when a verdict lands. The entry identifier does
    not move, so a changed answer gets the work back under the same identifier.
    """
    withheld = {
        collision.bucket
        for collision in plan.collisions
        if answers.get(collision.node_id) == COLLISION_SEPARATE
    }
    if not withheld:
        return plan
    updated = tuple(
        replace(
            entry,
            disposition=Disposition.WITHHELD,
            withheld_by=WITHHELD_BY_VERDICT,
            vocal=VOCAL_WITHHELD if entry.vocal == VOCAL_ADD else entry.vocal,
        )
        if entry.applicable and entry.bucket in withheld
        else entry
        for entry in plan.entries
    )
    return replace(plan, entries=updated)


def to_json(plan: AdoptionPlan) -> dict[str, Any]:
    """The plan as a structured document (R32). A transport, never read back."""
    return {
        "tree": plan.tree,
        "digest": plan.digest(),
        "counts": plan.counts(),
        "energy": plan.energy_readings(),
        "placements": plan.placements.state,
        "withheld_by_placement": plan.withheld_by_placement(),
        "held_elsewhere": [review_row(entry) for entry in plan.held_elsewhere()],
        "outside_root": [outside_row(entry) for entry in plan.outside_root()],
        "vocals": plan.vocals.state,
        "vocal": plan.vocal_counts(),
        "vocal_memberships": [vocal_row(entry) for entry in plan.vocal_memberships()],
        "entries": [
            {
                "id": entry.entry_id,
                "ordinal": entry.ordinal,
                "content_id": entry.content_id,
                "location": entry.recorded,
                "disposition": str(entry.disposition),
                "category": str(entry.category),
                "bucket": entry.bucket,
                "sub": entry.sub,
                "energy": entry.energy,
                "energy_unreadable": entry.energy_unreadable,
                "withheld_by": entry.withheld_by,
                "holds": list(entry.holds),
                "holds_under_another_name": list(entry.holds_unnamed),
                "vocal": entry.vocal,
                # Only on a second genre's entry, so a one genre plan reads as before.
                **({"second_genre": entry.genre} if entry.second else {}),
            }
            for entry in plan.entries
        ],
        "collisions": [collision_row(item) for item in plan.collisions],
    }
