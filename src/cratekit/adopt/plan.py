"""The adoption plan, and the review items it becomes.

WHY THE PLAN IS NOT A FILE. R26 says adoption presents its whole plan for review
and applies it incrementally and resumably. "Resumably across sessions" is
exactly what a plan file cannot give: the verdicts have to outlive the process
that collected them, and a file a person edits gives back whatever they typed,
with no way to tell an answer from a typo and no way for a second process to see
either. So the plan is a value in memory and its OPEN QUESTIONS are persisted
review items in the queue U11 declared for them (R12, R26). The applied half is a
separate ledger, because "somebody decided this" and "the library has this" are
different facts with different lifetimes.

THE TWO QUESTIONS A PLAN ASKS A PERSON, and neither is "is this plan ok".

1. **A track whose genre cannot place it.** Approach point 2, and the defect it
   comes from: a smaller version of this migration silently sent every
   unrecognised genre into the fallback folder, in bulk, on approval given for a
   plan that looked complete. The options are the declared buckets, derived from
   the active taxonomy, so a user's own template produces its own menu.

2. **A declared folder that already exists with different contents.** Adopting a
   library means writing into a tree somebody already curated. A folder named
   like a declared bucket that already holds tracks this plan does not name is
   surfaced rather than merged, because merging is the one outcome that cannot be
   undone by re-running anything. The ANSWER BINDS, through
   :func:`with_collision_verdicts`: asking the question and then applying into
   the folder regardless is worse than never asking, because it puts the person's
   name on a merge they refused.

WHERE A TRACK ALREADY SITS IS READ, AND IT WAS NOT (R-731). The plan placed
each track by its genre and its file's energy reading and asked nothing of the
tree it was about to write, and the membership writer is add only. So a track
the library files under one energy band whose file reads another was added to
the second and stayed in the first: 569 of 700 additions on a copy of a real
library. :class:`Placements` is what the tree holds, handed in as data the way
``existing`` is, and an entry whose track holds a different competing sub in
the same bucket is WITHHELD, counted under its own name, and listed. Nothing is
moved and nothing is removed. Which reading is right is a person's to say.

THE IDENTITY OF A COLLISION IS THE NODE, NEVER ITS NAME. This is the shape U19
shipped as a blocking defect and it is worth stating twice. Its membership dedup
targeted a destination's DISPLAY name, so a re-run after somebody renamed the
folder in rekordbox found nothing by the new name, created the destination a
second time, and filed one track in both. Here the same trap is one step
earlier: a collision recorded against "the folder called X" is a different
collision the moment X is renamed, so the person who already answered it is asked
again and the second answer proposes a second folder. The review item's IDENTITY
is therefore the tree, the bucket identifier, and the library node's own
identifier. The display name rides in the payload, where it is a label on a
screen and nothing keys on it.

Layer: modules.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, replace
from typing import Any, Mapping, Sequence

from cratekit.adopt.scan import Disposition, Readability, ScannedTrack
from cratekit.cli.output import canonical_json, digest_of
from cratekit.core import routing, taxonomy
from cratekit.core.review import Option, Queue, ReviewStore, offer

#: The prefix every plan entry identifier carries, so one is recognizable in a
#: log or a bug report without a lookup. Different from the review queue's and
#: from the decision stores', for the reason those two differ from each other:
#: three identifier spaces addressed by different verbs, and one pasted into
#: another must fail to resolve rather than silently miss.
ENTRY_ID_PREFIX = "ap"

#: The kind a per-track genre question is filed under in the review queue.
KIND_GENRE = "adoption-genre"

#: The kind a folder collision is filed under.
KIND_COLLISION = "adoption-collision"

#: The two named answers to a collision. A closed set, because "merge" and "do
#: not merge" are the whole question and a third option would be a way of not
#: answering it.
COLLISION_ADOPT = "adopt-existing"
COLLISION_SEPARATE = "keep-separate"

#: Why an entry is withheld, when a person's collision verdict is the reason.
#: The other reasons are the members of :class:`cratekit.core.routing.Competing`,
#: so the set of reasons is this value and that enumeration and nothing else.
WITHHELD_BY_VERDICT = "verdict"

#: The two states of :attr:`Placements.read`, as the plan document spells them.
PLACEMENTS_READ = "read"
PLACEMENTS_UNREAD = "unread"


@dataclass(frozen=True, slots=True)
class Placements:
    """The competing subs each track already holds, by bucket. Supplied, not read.

    Built by :mod:`cratekit.adopt.placements`, which is the layer holding a
    database open. This module performs no library input, for the reason
    :class:`ExistingFolder` gives.

    ``read`` IS A FACT OF ITS OWN AND NOT THE EMPTINESS OF ``held``. A tree
    nobody could read and a tree holding nothing both produce no held subs, and
    folding them is the absence read as evidence this repository has paid for
    more than once. An unread tree withholds nothing, says ``unread`` on the
    plan document, and moves the digest, so an approval given over a plan that
    could not see the tree is not honoured once it can.

    ``held`` maps a bucket identifier to a content identifier to the sub
    identifiers that track holds there. Stable identifiers throughout, never
    display names (R19, D5).

    ``unnamed`` is the part of ``held`` the membership writer cannot see: the
    subs a track holds ONLY through a playlist that no longer carries the
    names the taxonomy declares, recognised through the node a previous write
    recorded. The writer finds a playlist by its declared name, so for these
    it would make a second playlist beside the renamed one and file the track
    in both. A sub a track holds under both names is not in here.

    ``doubled`` is the part of ``held`` a track holds through MORE THAN ONE
    active row in one playlist (R-781). rekordbox made such rows; no verb here
    writes a pair twice. ``held`` is a set of subs and cannot say it, and the
    move plan lists what it cannot reach by name, so the multiplicity the tree
    walk counts is carried here rather than lost in the set.
    """

    read: bool = False
    held: Mapping[str, Mapping[str, tuple[str, ...]]] = field(default_factory=dict)
    unnamed: Mapping[str, Mapping[str, tuple[str, ...]]] = field(default_factory=dict)
    doubled: Mapping[str, Mapping[str, tuple[str, ...]]] = field(default_factory=dict)

    def holds(self, bucket: str, content_id: str) -> tuple[str, ...]:
        """The subs of ``bucket`` this track sits in, or none."""
        return tuple(self.held.get(bucket, {}).get(content_id, ()))

    def holds_unnamed(self, bucket: str, content_id: str) -> tuple[str, ...]:
        """The subs of ``bucket`` this track holds under another name only."""
        return tuple(self.unnamed.get(bucket, {}).get(content_id, ()))

    def holds_doubled(self, bucket: str, content_id: str) -> tuple[str, ...]:
        """The subs of ``bucket`` this track holds through two or more rows."""
        return tuple(self.doubled.get(bucket, {}).get(content_id, ()))

    @property
    def state(self) -> str:
        return PLACEMENTS_READ if self.read else PLACEMENTS_UNREAD


#: The placements of a tree nobody read. The default everywhere one is taken,
#: and it is visible on the plan rather than silent. See :class:`Placements`.
UNREAD = Placements()


@dataclass(frozen=True, slots=True)
class ExistingFolder:
    """A folder the library already has directly under the tree being adopted.

    Supplied by the caller, which is the layer that has a database or an export
    open. This module performs no library input, for the same reason
    :func:`cratekit.core.tree_registry.anchored_root` takes a ``root_exists``
    callable: the decision it makes is testable without a rekordbox database,
    and the live database is off limits.

    ``node_id`` is the library's own identifier for the folder and is what a
    record keys on. ``display`` is what rekordbox shows and is a label.
    """

    node_id: str
    display: str
    content_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Collision:
    """A declared bucket whose folder already exists holding something else.

    ``strangers`` is the count of rows already under that folder which this plan
    does not name. Zero strangers is not a collision at all and never reaches
    here: a folder holding exactly what the plan is about to put in it is the
    adoption working, not a conflict.
    """

    tree: str
    bucket: str
    node_id: str
    display: str
    strangers: int

    def identity(self) -> dict[str, str]:
        """What the decision about this collision is addressed by.

        The NODE, not the name. See the module docstring: a record keyed on the
        display name is orphaned by a rename in rekordbox, and an orphaned record
        reads as "nobody has answered this", which is how a second folder gets
        proposed for a place somebody already decided about.
        """
        return {"tree": self.tree, "bucket": self.bucket, "node": self.node_id}


@dataclass(frozen=True, slots=True)
class PlanEntry:
    """One track's place in the plan. Every scanned track has exactly one.

    ``entry_id`` IS A FUNCTION OF THE WORK, not of the track. It hashes the tree,
    the row, and the destination together, so changing where a track is going
    produces a different entry and the applied ledger does not report the new
    work as already done. That is the property that makes resume safe across a
    taxonomy edit: the entries that did not move keep their identifiers and stay
    skipped, and the ones that moved come back as work.

    ``bucket`` and ``sub`` are stable taxonomy identifiers and are empty for
    anything that is not routing. The folder and sub-playlist names rekordbox
    shows are resolved from the active taxonomy at write time and are never
    stored here (R19, D5).
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
    #: The census's energy reading, carried so a genre answered later resolves
    #: its sub from the same level the census read. See :class:`ScannedTrack`.
    energy: int | None = None
    energy_unreadable: bool = False
    #: The competing subs of this entry's bucket the track already holds, when
    #: that is why it is withheld. Identifiers, in sorted order. Empty for every
    #: entry withheld for another reason or not withheld at all.
    holds: tuple[str, ...] = ()
    #: The part of ``holds`` the track holds through a renamed playlist only,
    #: which is the part the membership writer cannot see.
    holds_unnamed: tuple[str, ...] = ()
    #: Why a withheld entry is withheld: :data:`WITHHELD_BY_VERDICT`, or the
    #: kind of competing place the track holds. Empty when it is not withheld.
    withheld_by: str = ""

    @property
    def held_elsewhere(self) -> bool:
        """Withheld because the track already holds a competing place."""
        return self.disposition is Disposition.WITHHELD and bool(self.holds)

    @property
    def applicable(self) -> bool:
        return self.disposition is Disposition.ROUTE


def entry_id_for(tree: str, content_id: str, bucket: str, sub: str) -> str:
    """The stable identifier for one piece of adoption work.

    Content addressed rather than allocated, exactly as a review item is, and for
    the same two reasons: a re-scan produces the same identifiers for the same
    work without a lookup table, and two processes agree on them without
    coordinating. Serialized canonically so a different key order cannot
    manufacture a second identifier for one piece of work.
    """
    digest = hashlib.sha256(
        canonical_json(
            {"tree": tree, "content": content_id, "bucket": bucket, "sub": sub}
        ).encode()
    ).hexdigest()
    return f"{ENTRY_ID_PREFIX}_{digest[:24]}"


@dataclass(frozen=True, slots=True)
class AdoptionPlan:
    """Every scanned track, what adoption proposes, and what it cannot answer.

    THE PLAN HOLDS EVERY TRACK, INCLUDING THE ONES IT WILL NOT TOUCH. That is
    what makes "nothing falls out of the plan" a set comparison rather than a
    promise: :func:`covers` compares the plan's rows against the census's rows,
    and an omission anywhere shows up as a difference rather than as a smaller
    number nobody was counting.
    """

    tree: str
    entries: tuple[PlanEntry, ...] = ()
    collisions: tuple[Collision, ...] = ()
    #: What the tree already holds, kept on the plan so a genre answered later
    #: is checked against the same tree the first build was.
    placements: Placements = UNREAD

    def applicable(self) -> tuple[PlanEntry, ...]:
        """The entries an apply may write, in plan order."""
        return tuple(entry for entry in self.entries if entry.applicable)

    def content_ids(self) -> frozenset[str]:
        return frozenset(entry.content_id for entry in self.entries)

    def counts(self) -> dict[str, int]:
        """One count per disposition and one per category, zeroes included.

        DERIVED over the members of both enumerations rather than over what this
        plan happens to contain. A summary that listed only the categories it saw
        makes "no online-only files here" and "this build does not look for them"
        the same output, which is the distinction AE12 is about.

        TWO ENUMERATIONS IN ONE MAPPING, which is the shape this repository has
        shipped a silent duplicate into before. A member added to one with the
        same VALUE as a member of the other would collapse the two counts onto
        one key, and every test over this mapping iterates the runtime object and
        would be blind to it. ``tests/test_adoption.py`` asserts the two value
        sets are disjoint, which is the only check that can see it coming.
        """
        counts = {str(member): 0 for member in Disposition}
        counts.update({str(member): 0 for member in Readability})
        for entry in self.entries:
            counts[str(entry.disposition)] += 1
            counts[str(entry.category)] += 1
        return counts

    def energy_readings(self) -> dict[str, int]:
        """How many adoptable files held a reading, held none, or could not be read.

        OVER THE READABLE ENTRIES ONLY, because those are the files the census
        opened. An excluded file was never read, and counting it as holding no
        reading would be the absence read as evidence this module exists to
        refuse. Its own mapping rather than keys in :meth:`counts`, whose two
        enumerations already share one namespace and whose ``unreadable`` key
        means something else.
        """
        readings = {"read": 0, "absent": 0, "unreadable": 0}
        for entry in self.entries:
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
        """How many entries are withheld over a place the track already holds.

        A NAME OF ITS OWN, beside :meth:`counts` rather than inside it. The
        ``withheld`` count there is every withheld entry whatever the reason,
        and a person reading the gate needs the ones the tree caused apart from
        the ones a verdict caused. Split by kind, derived over the members of
        the enumeration so a kind with nothing in it reads zero rather than
        being absent, and totalled so nobody adds them up by eye.
        """
        found = {str(member.value): 0 for member in routing.Competing}
        for entry in self.entries:
            if entry.held_elsewhere and entry.withheld_by in found:
                found[entry.withheld_by] += 1
        return {"total": sum(found.values()), **found}

    def held_elsewhere(self) -> tuple[PlanEntry, ...]:
        """Every entry withheld over a place its track already holds, in plan order.

        THE WHOLE LIST, with no bound, because the list is what a person
        decides from and a first page would leave the rest decided by nobody.
        """
        return tuple(entry for entry in self.entries if entry.held_elsewhere)

    def digest(self) -> str:
        """What an approval is recorded AGAINST, so a stale one is detectable.

        A canonical projection rather than the rendered plan: the identifiers of
        the work, the counts per disposition, and the collisions by node. It
        moves when the plan moves and stays put when only the wording does, which
        is the property :func:`cratekit.cli.output.digest_of` was ported for.
        Each entry's identifier hashes its sub, so a track the energy reading
        moves moves the digest, and the reading tally is covered too, because
        an unreadable file lands where an untagged one does and a screen that
        counts them differently is a different plan. An
        approval whose digest no longer matches is refused rather than applied,
        because the person approved a different plan.

        THE WITHHELD ENTRIES ARE COVERED BY WHAT THEY HOLD (R-731). An entry
        withheld over a place its track already sits in is on the screen with
        that place named, so a track somebody moved between the approval and
        the apply is a different screen and a different digest. Whether the
        tree was read at all is covered for the reason :class:`Placements`
        gives. The rows are digested as they are shown, every field of them,
        so nothing on the review list can change under a recorded answer.
        """
        return digest_of(
            {
                "tree": self.tree,
                "entries": [entry.entry_id for entry in self.applicable()],
                "counts": self.counts(),
                "energy": self.energy_readings(),
                "placements": self.placements.state,
                "held_elsewhere": [
                    {"id": entry.entry_id, **review_row(entry)}
                    for entry in self.held_elsewhere()
                ],
                "collisions": sorted(
                    f"{item.bucket}:{item.node_id}" for item in self.collisions
                ),
            }
        )


def covers(plan: AdoptionPlan, scanned: Sequence[ScannedTrack]) -> frozenset[str]:
    """Rows the census produced that the plan does not carry. Empty is correct.

    Written as a function returning the DIFFERENCE rather than a boolean, so a
    failure names the rows that went missing instead of asserting that some did.
    """
    return frozenset(track.content_id for track in scanned) - plan.content_ids()


def _sub_for(
    declared: taxonomy.Taxonomy, bucket_id: str, genre: str, level: int | None
) -> str | None:
    """The sub-playlist identifier a track lands in, from its file's energy level.

    Through :func:`cratekit.core.routing.energy_sub` with the level the census
    read off the file, which is the level the routing pass reads, so adoption
    files a track where routing would. It once passed None for every track,
    which filed 7,401 of 7,773 tracks as unsorted over a library where 7,726
    carried a reading. The three per-bucket exceptions that decision has to
    respect are already encoded there, in the one order that gets them right, and
    a second resolution here would be a second opinion that eventually disagrees.

    None is a real answer and is passed straight back: the taxonomy declares no
    place below this bucket for a track with no reading, and a caller that
    treated None as an error would reintroduce the crash the declaration exists
    to avoid.
    """
    sub = routing.energy_sub(declared, bucket_id, level, source_genre=genre)
    return None if sub is None else sub.id


def review_row(entry: PlanEntry) -> dict[str, Any]:
    """One withheld entry as the review list shows it and the digest covers it.

    What a person needs to decide which reading is right: the track, where it
    sits, where the plan would have put it, and what the file reads. ONE BODY
    for the document and the digest, so a field added to the screen is a field
    the approval binds to.
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
    }


#: What :func:`competing_place` answers for an entry that may be placed.
NO_COMPETING_PLACE: tuple[str, tuple[str, ...], tuple[str, ...]] = ("", (), ())


def competing_place(
    declared: taxonomy.Taxonomy,
    placements: Placements,
    *,
    bucket: str,
    sub: str,
    content_id: str,
) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
    """Why a routed entry must be withheld and what its track holds, or nothing.

    Returns the kind of competing place, the subs held, and the ones among
    them held under another name only. :data:`NO_COMPETING_PLACE` when the
    entry may be placed.

    WHAT COMPETES IS THE TAXONOMY'S ANSWER, through
    :func:`cratekit.core.routing.competing_subs`, and both sides are asked of
    it. The sub the plan names has to be one of the bucket's competing subs,
    and only a held sub in that same set counts, so a track sitting in a
    manual or derived sub alone is placed as it always was whatever the
    placements carry.

    A TRACK ALREADY IN THE SUB THE PLAN NAMES IS NOT WITHHELD, even when it
    holds a second one as well. The writer reports that row already present
    and adds nothing, which is the outcome this function exists to guarantee,
    and withholding it would list a track for review over a write that was
    never going to happen.

    UNLESS THE WRITER CANNOT SEE THAT IT IS THERE. The writer finds a playlist
    by its declared name, so a track sitting in the planned sub through a
    renamed playlist only is a track the writer would file a second time, in a
    new playlist under the old name. That entry is withheld and its row shows
    the sub it holds and the sub planned as the same one, with the name as the
    reason. Found by the review of this unit and driven before it was fixed.
    """
    if not placements.read:
        return NO_COMPETING_PLACE
    kind, competing = routing.competing_subs(declared, bucket)
    if sub not in competing:
        return NO_COMPETING_PLACE
    held = tuple(sorted(set(placements.holds(bucket, content_id)) & competing))
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
) -> AdoptionPlan:
    """Turn a census into a plan, resolving destinations and finding collisions.

    ``scanned`` IS A SEQUENCE RATHER THAN AN ITERABLE, deliberately. It is walked
    more than once here, and the census is a generator over a database cursor in
    the only shape that matters. Taking an iterable and walking it twice is how
    U18's row index reported an empty library while the run reported clean, so
    the type says what it needs and the caller materializes once.

    ``placements`` DEFAULTS TO A TREE NOBODY READ, and the plan says so. A
    caller with a database passes what :mod:`cratekit.adopt.placements` read
    off it; a caller without one gets a plan that withholds nothing over a
    held place and carries ``unread`` on its document and in its digest.
    """
    entries: list[PlanEntry] = []
    for ordinal, track in enumerate(scanned, start=1):
        disposition = track.disposition
        bucket = track.bucket
        sub = ""
        withheld_by, holds, holds_unnamed = NO_COMPETING_PLACE
        if disposition is Disposition.ROUTE:
            resolved = _sub_for(declared, bucket, track.genre, track.energy)
            if resolved is None:
                disposition = Disposition.UNDECLARED
            else:
                sub = resolved
                withheld_by, holds, holds_unnamed = competing_place(
                    declared,
                    placements,
                    bucket=bucket,
                    sub=sub,
                    content_id=track.content_id,
                )
                if withheld_by:
                    # THE BUCKET AND THE SUB STAY, as they do for an entry a
                    # verdict withheld: the identifier is derived from the
                    # record, and the record is what the review list shows.
                    disposition = Disposition.WITHHELD
        # THE IDENTIFIER IS DERIVED FROM WHAT THE RECORD WILL HOLD, not from
        # what was resolved on the way to it. An identifier a reader cannot
        # recompute from the record it identifies is an identifier nobody can
        # audit, and the first version of this hashed a bucket that the
        # undeclared entries then did not carry.
        if disposition not in (Disposition.ROUTE, Disposition.WITHHELD):
            bucket = ""
        entries.append(
            PlanEntry(
                entry_id=entry_id_for(tree, track.content_id, bucket, sub),
                content_id=track.content_id,
                recorded=track.recorded,
                disposition=disposition,
                category=track.readability,
                genre=track.genre,
                tree=tree,
                bucket=bucket,
                sub=sub,
                ordinal=ordinal,
                path=track.path,
                energy=track.energy,
                energy_unreadable=track.energy_unreadable,
                holds=holds,
                holds_unnamed=holds_unnamed,
                withheld_by=withheld_by,
            )
        )
    return AdoptionPlan(
        tree=tree,
        entries=tuple(entries),
        collisions=find_collisions(entries, declared, tree=tree, existing=existing),
        placements=placements,
    )


def find_collisions(
    entries: Sequence[PlanEntry],
    declared: taxonomy.Taxonomy,
    *,
    tree: str,
    existing: Sequence[ExistingFolder],
) -> tuple[Collision, ...]:
    """Declared folders that already exist in the library holding other tracks.

    THE MATCH IS BY DISPLAY NAME AND THE RECORD IS BY NODE, and the split is the
    point. Finding the folder has to go through the name, because the name is the
    only thing a library that has never heard of this product shares with the
    taxonomy; that is the same reason U18's cutover adopts by matching names
    exactly. Recording the finding has to go through the node identifier, because
    the name is the one thing about it a user can change between two runs.

    A folder holding ONLY tracks this plan names is not a collision. Adoption
    writing into a folder that already contains the tracks it is about to place
    is the feature, and reporting it would train the reader to approve past this
    report, which is how the real one gets approved too (P7).

    THE LIMITATION THIS LEAVES, STATED RATHER THAN DISCOVERED. A folder renamed
    in rekordbox so that it no longer matches any declared bucket is not found,
    so no collision is reported for it and adoption would write into a folder
    created under the taxonomy's name beside it. Finding it would need a
    persisted map from the stable destination identifiers to the node
    identifiers a previous write used, which is the shape the tree registry
    already has for a tree's adopted root and which the routing pass was
    explicitly forbidden from inventing a second copy of. So this leaves it
    alone: two answers to "which node is this destination" is a worse failure
    than one honest gap, and the gap is visible because the folder shows up
    empty in the library rather than silently absorbing tracks.
    """
    planned_by_bucket: dict[str, set[str]] = {}
    # A TRACK WITHHELD OVER A PLACE IT HOLDS IS NAMED BY THIS PLAN, under this
    # bucket, and it sits in the folder by definition. Counting it a stranger
    # would raise a collision over the tracks the plan has already listed.
    named_by_bucket: dict[str, set[str]] = {}
    for entry in entries:
        if entry.applicable:
            planned_by_bucket.setdefault(entry.bucket, set()).add(entry.content_id)
        elif entry.held_elsewhere:
            named_by_bucket.setdefault(entry.bucket, set()).add(entry.content_id)
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
        if not strangers:
            continue
        found.append(
            Collision(
                tree=tree,
                bucket=bucket_id,
                node_id=folder.node_id,
                display=folder.display,
                strangers=len(strangers),
            )
        )
    return tuple(found)


def bucket_options(declared: taxonomy.Taxonomy) -> tuple[Option, ...]:
    """Every declared bucket as a candidate, addressed by its stable identifier.

    DERIVED from the active taxonomy, so a user's own template produces its own
    menu and nothing here names a folder. ``summary`` carries the display name,
    which is what a person reads; ``option_id`` is the identifier the verdict is
    recorded against, so renaming the folder afterwards does not orphan the
    decision.
    """
    return tuple(
        Option(option_id=bucket.id, summary=bucket.display)
        for bucket in declared.buckets
    )


def offer_plan(
    store: ReviewStore,
    plan: AdoptionPlan,
    declared: taxonomy.Taxonomy,
    *,
    handler_key: str,
) -> tuple[str, ...]:
    """Put the plan's open questions in the review queue. Returns the item ids.

    IDEMPOTENT because :func:`cratekit.core.review.offer` is: re-scanning a
    library re-offers the same candidates, and an item somebody already settled
    keeps its verdict, keeps its payload, and does not reopen. That is what makes
    "a plan approved thirty percent through and resumed in a later session"
    possible at all, and it is what a plan file cannot do.

    THE EXCLUDED TRACKS ARE NOT OFFERED. An unreadable or online-only file is
    not a question for a person, it is a fact about the machine, and putting a
    thousand of them in an adjudication queue would bury the two questions that
    genuinely need answering. They are carried IN THE PLAN with the category that
    names them, which is what AE12 asks for.
    """
    candidates = bucket_options(declared)
    offered: list[str] = []
    for entry in plan.entries:
        if entry.disposition is not Disposition.NEEDS_GENRE:
            continue
        item = offer(
            store,
            queue=Queue.ADOPTION,
            kind=KIND_GENRE,
            identity={"tree": entry.tree, "content": entry.content_id},
            payload={
                "content_id": entry.content_id,
                "location": entry.recorded,
                "genre": entry.genre,
                "reason": str(entry.disposition),
            },
            options=candidates,
            handler_key=handler_key,
        )
        offered.append(item.item_id)
    for collision in plan.collisions:
        item = offer(
            store,
            queue=Queue.ADOPTION,
            kind=KIND_COLLISION,
            identity=collision.identity(),
            payload={
                "bucket": collision.bucket,
                "node_id": collision.node_id,
                # The display name is a LABEL here. Nothing keys on it, and it is
                # refreshed on every re-offer precisely because it can change.
                "display": collision.display,
                "strangers": collision.strangers,
            },
            options=(
                Option(
                    option_id=COLLISION_ADOPT,
                    summary="write into the folder that is already there",
                ),
                Option(
                    option_id=COLLISION_SEPARATE,
                    summary="leave that folder alone and place nothing in it",
                ),
            ),
            handler_key=handler_key,
        )
        offered.append(item.item_id)
    return tuple(offered)


def with_verdicts(
    plan: AdoptionPlan, answers: Mapping[str, str], declared: taxonomy.Taxonomy
) -> AdoptionPlan:
    """Fold answered genre questions back into the plan as routable entries.

    ``answers`` maps a row identifier to the bucket identifier a person chose. It
    arrives as data rather than as a queue handle so that this stays pure and the
    caller owns the read; the queue is where the answers LIVE, and reading them
    out of it is one line at the call site.

    An answer naming a bucket the taxonomy does not declare is IGNORED rather
    than applied. It can only arrive from a verdict recorded against a template
    that has since changed, and inventing a folder from an identifier nobody
    declares is the failure :func:`cratekit.write.routing_pass.destination`
    refuses one layer down.
    """
    declared_ids = set(declared.bucket_ids())
    updated: list[PlanEntry] = []
    for entry in plan.entries:
        chosen = answers.get(entry.content_id)
        if entry.disposition is not Disposition.NEEDS_GENRE or chosen is None:
            updated.append(entry)
            continue
        if chosen not in declared_ids:
            updated.append(entry)
            continue
        sub = _sub_for(declared, chosen, entry.genre, entry.energy)
        if sub is None:
            updated.append(replace(entry, disposition=Disposition.UNDECLARED))
            continue
        # AN ANSWERED GENRE IS CHECKED AGAINST THE SAME TREE. A track a person
        # has just given a bucket to may already sit in that bucket under
        # another band. NOTHING UNDER ``src`` CALLS THIS FUNCTION TODAY, so
        # this holds the rule for the caller that will fold answers in and is
        # proven by this module's own tests and by nothing driven.
        withheld_by, holds, holds_unnamed = competing_place(
            declared,
            plan.placements,
            bucket=chosen,
            sub=sub,
            content_id=entry.content_id,
        )
        updated.append(
            replace(
                entry,
                disposition=Disposition.WITHHELD if withheld_by else Disposition.ROUTE,
                bucket=chosen,
                sub=sub,
                entry_id=entry_id_for(entry.tree, entry.content_id, chosen, sub),
                holds=holds,
                holds_unnamed=holds_unnamed,
                withheld_by=withheld_by,
            )
        )
    return replace(plan, entries=tuple(updated))


def with_collision_verdicts(
    plan: AdoptionPlan, answers: Mapping[str, str]
) -> AdoptionPlan:
    """Fold answered collision questions back into the plan. The answer BINDS.

    ``answers`` maps a folder's NODE identifier to one of the two declared
    verdicts, which is what the review item is addressed by (see
    :meth:`Collision.identity`) and the one thing about the folder a user cannot
    change between two runs.

    THIS IS THE FUNCTION THE QUESTION WAS MISSING. :func:`offer_plan` asked
    whether to write into a folder that already exists holding strangers, and
    nothing anywhere read the answer back: :func:`with_verdicts` handles genre
    answers only, :func:`cratekit.adopt.apply.apply_plan` takes no verdicts at
    all, and both option identifiers appeared nowhere outside their own
    definition. A plan with a real collision therefore applied into that folder
    whatever the person said, so somebody who answered "leave that folder alone"
    got precisely the merge this module says it exists to prevent, and it is the
    one outcome that cannot be undone by re-running anything.

    ``keep-separate`` withholds every entry routed to that bucket.
    ``adopt-existing`` leaves them applicable, which is what they already were,
    so an unanswered collision behaves exactly as an approved one does. That
    asymmetry is deliberate and it is the safe direction ONLY because the
    collision is surfaced and the plan cannot be approved without its digest,
    which moves the moment a verdict lands.

    THE ENTRY IDENTIFIER DOES NOT MOVE. A withheld entry is the same piece of
    work as the entry it came from, addressed to the same destination, and it
    keeps its bucket and sub so the identifier stays derivable from the record it
    names. Somebody who changes their answer gets the work back under the
    identifier the ledger already knows, rather than as a second piece of work
    that has never been done.
    """
    withheld = {
        collision.bucket
        for collision in plan.collisions
        if answers.get(collision.node_id) == COLLISION_SEPARATE
    }
    if not withheld:
        return plan
    updated = tuple(
        replace(entry, disposition=Disposition.WITHHELD, withheld_by=WITHHELD_BY_VERDICT)
        if entry.applicable and entry.bucket in withheld
        else entry
        for entry in plan.entries
    )
    return replace(plan, entries=updated)


def to_json(plan: AdoptionPlan) -> dict[str, Any]:
    """The plan as a structured document, for R32's output mode.

    A TRANSPORT, never an editing surface. The distinction is the same one
    :func:`cratekit.core.review.export_document` makes: this is what a caller
    renders or pipes, and no decision is ever read back out of it. Every verdict
    comes from the queue.
    """
    return {
        "tree": plan.tree,
        "digest": plan.digest(),
        "counts": plan.counts(),
        "energy": plan.energy_readings(),
        "placements": plan.placements.state,
        "withheld_by_placement": plan.withheld_by_placement(),
        # EVERY ONE OF THEM, for the reason ``held_elsewhere`` gives.
        "held_elsewhere": [review_row(entry) for entry in plan.held_elsewhere()],
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
            }
            for entry in plan.entries
        ],
        "collisions": [
            {
                "bucket": item.bucket,
                "node_id": item.node_id,
                "display": item.display,
                "strangers": item.strangers,
            }
            for item in plan.collisions
        ],
    }


__all__ = [
    "COLLISION_ADOPT",
    "COLLISION_SEPARATE",
    "ENTRY_ID_PREFIX",
    "KIND_COLLISION",
    "KIND_GENRE",
    "NO_COMPETING_PLACE",
    "PLACEMENTS_READ",
    "PLACEMENTS_UNREAD",
    "UNREAD",
    "WITHHELD_BY_VERDICT",
    "Collision",
    "ExistingFolder",
    "AdoptionPlan",
    "Placements",
    "PlanEntry",
    "bucket_options",
    "competing_place",
    "build_adoption_plan",
    "covers",
    "entry_id_for",
    "find_collisions",
    "offer_plan",
    "review_row",
    "to_json",
    "with_collision_verdicts",
    "with_verdicts",
]
