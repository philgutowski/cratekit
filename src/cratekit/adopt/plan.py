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
from dataclasses import dataclass, replace
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

    def digest(self) -> str:
        """What an approval is recorded AGAINST, so a stale one is detectable.

        A canonical projection rather than the rendered plan: the identifiers of
        the work, the counts per disposition, and the collisions by node. It
        moves when the plan moves and stays put when only the wording does, which
        is the property :func:`cratekit.cli.output.digest_of` was ported for. An
        approval whose digest no longer matches is refused rather than applied,
        because the person approved a different plan.
        """
        return digest_of(
            {
                "tree": self.tree,
                "entries": [entry.entry_id for entry in self.applicable()],
                "counts": self.counts(),
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


def _sub_for(declared: taxonomy.Taxonomy, bucket_id: str, genre: str) -> str | None:
    """The sub-playlist identifier a track lands in with no energy reading.

    Through :func:`cratekit.core.routing.energy_sub` with a level of None, which
    is the honest input: adoption reads an existing library and has no analysis
    of its own, and the analysis backfill R26 mentions is a separate module that
    may not be installed. The three per-bucket exceptions that decision has to
    respect are already encoded there, in the one order that gets them right, and
    a second resolution here would be a second opinion that eventually disagrees.

    None is a real answer and is passed straight back: the taxonomy declares no
    place below this bucket for a track with no reading, and a caller that
    treated None as an error would reintroduce the crash the declaration exists
    to avoid.
    """
    sub = routing.energy_sub(declared, bucket_id, None, source_genre=genre)
    return None if sub is None else sub.id


def build_adoption_plan(
    scanned: Sequence[ScannedTrack],
    declared: taxonomy.Taxonomy,
    *,
    tree: str,
    existing: Sequence[ExistingFolder] = (),
) -> AdoptionPlan:
    """Turn a census into a plan, resolving destinations and finding collisions.

    ``scanned`` IS A SEQUENCE RATHER THAN AN ITERABLE, deliberately. It is walked
    more than once here, and the census is a generator over a database cursor in
    the only shape that matters. Taking an iterable and walking it twice is how
    U18's row index reported an empty library while the run reported clean, so
    the type says what it needs and the caller materializes once.
    """
    entries: list[PlanEntry] = []
    for ordinal, track in enumerate(scanned, start=1):
        disposition = track.disposition
        bucket = track.bucket
        sub = ""
        if disposition is Disposition.ROUTE:
            resolved = _sub_for(declared, bucket, track.genre)
            if resolved is None:
                disposition = Disposition.UNDECLARED
            else:
                sub = resolved
        # THE IDENTIFIER IS DERIVED FROM WHAT THE RECORD WILL HOLD, not from
        # what was resolved on the way to it. An identifier a reader cannot
        # recompute from the record it identifies is an identifier nobody can
        # audit, and the first version of this hashed a bucket that the
        # undeclared entries then did not carry.
        if disposition is not Disposition.ROUTE:
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
            )
        )
    return AdoptionPlan(
        tree=tree,
        entries=tuple(entries),
        collisions=find_collisions(entries, declared, tree=tree, existing=existing),
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
    for entry in entries:
        if entry.applicable:
            planned_by_bucket.setdefault(entry.bucket, set()).add(entry.content_id)
    by_display = {folder.display: folder for folder in existing}

    found: list[Collision] = []
    for bucket_id in sorted(planned_by_bucket):
        folder = by_display.get(declared.bucket(bucket_id).display)
        if folder is None:
            continue
        strangers = set(folder.content_ids) - planned_by_bucket[bucket_id]
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
        sub = _sub_for(declared, chosen, entry.genre)
        if sub is None:
            updated.append(replace(entry, disposition=Disposition.UNDECLARED))
            continue
        updated.append(
            replace(
                entry,
                disposition=Disposition.ROUTE,
                bucket=chosen,
                sub=sub,
                entry_id=entry_id_for(entry.tree, entry.content_id, chosen, sub),
            )
        )
    return AdoptionPlan(tree=plan.tree, entries=tuple(updated), collisions=plan.collisions)


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
        replace(entry, disposition=Disposition.WITHHELD)
        if entry.applicable and entry.bucket in withheld
        else entry
        for entry in plan.entries
    )
    return AdoptionPlan(tree=plan.tree, entries=updated, collisions=plan.collisions)


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
    "Collision",
    "ExistingFolder",
    "AdoptionPlan",
    "PlanEntry",
    "bucket_options",
    "build_adoption_plan",
    "covers",
    "entry_id_for",
    "find_collisions",
    "offer_plan",
    "to_json",
    "with_collision_verdicts",
    "with_verdicts",
]
