"""The deletion pass: review what was removed, then trash exactly what was confirmed.

THE ORDER IS THE UNIT, and it is the same claim the deferred-routing pass makes
about its own order. Assert the volume, read the library, prove the file, offer
it, and only then, in a second act by a person, move it. Every one of those steps
has a reason it is where it is:

1. **The volume identity is asserted before anything is resolved (R38).** A
   restored clone of the library mounted where the real one belongs is internally
   consistent all the way down: its rows resolve, its sizes match, its playlists
   agree. Everything this pass believes would be true of the clone and false of
   the disk, and the files it would trash are the backup the recovery story
   depends on. No other check in this module can catch that, because every one of
   them is evaluated against whatever is mounted.
2. **rekordbox is refused, application and background agent both.** The natural
   way to use this verb is to remove tracks in rekordbox and then run it, so
   rekordbox is the application most likely to be open, and a library open in
   rekordbox has rows in memory that the file on disk does not show. Every
   identity assertion below would then be evaluated against a stale view of which
   rows are active, which is the one input that decides whether a file is
   somebody's music or an orphan.
3. **The reference set is completed before any candidate is judged.** See
   ``candidates``: a proof of "no active row points at this" built from the rows
   that happened to answer is not a weaker proof, it is a different claim.
4. **The review is offered, and the move is a separate act.** R35 presents
   removals with resolved path and size, and R34 forbids a blanket affirmative
   for a gate in this class. Nothing here moves a file because a run started.
5. **Every precondition is re-asserted immediately before the move, not at review
   time (R37).** A review item is durable by design: a person may confirm one
   days later from another process, and in the meantime they may have re-imported
   the track, restored a backup over it, or added it to a playlist. So ``apply``
   re-reads the library from scratch and re-runs the same categoriser rather than
   trusting the plan it was handed.

**NOTHING HERE WRITES A DATABASE ROW (KTD15).** Deletion is driven by rekordbox's
own soft-delete marker precisely so the guarded writer's unconditional delete
prohibition never has to be reopened. The database is opened, read, and closed.
That is also why there is no capture: a snapshot protects database rows, this
run creates, edits and deletes none, and the thing that is actually at risk is
files, which a database snapshot does not hold. What protects those is the
backup acknowledgment the session gates require and the fact that the only move
performed is into the Trash.

**NOTHING HERE TOUCHES A STREAMING SERVICE (R36).** No import in this package
reaches an adapter, a provider session, or an HTTP client, and no streaming state
is read. A deletion is a fact about this disk.

**WHY THE SESSION TAKES NO CAPTURE, stated because its absence looks like an
omission.** Every other destructive session in this product snapshots the
database first. This one creates, edits and deletes no row, so there is nothing
in the database for a capture to protect, and a snapshot of a database does not
hold a music file. What protects the files is the backup acknowledgment the gates
require, and the fact that the only move performed is into the Trash, which is
reversible by a rename.

**WHY ``analysis_roots`` DEFAULTS TO EMPTY HERE and refuses when empty in the
membership writer.** That writer opens the database with write intent and commits,
so a grid rewritten through a handle the binding already returned is a real
possibility and the watch is the only thing that can see it. This pass opens no
analysis file, writes no tag, and moves only files a collection row names by
path, size and inode. A caller may still name roots and the watch will arm; the
default is empty because there is nothing here it could catch.

THREE NAMING DECISIONS, RECORDED because the repository hunts for one symbol
meaning two things and these are the three this module produces. ``Plan``,
``Report`` and ``apply`` each already exist elsewhere: the first two in
``write.metadata``, whose own docstring argues the same shape this one has, and
the third in ``core.profiles``. All three are one idea correctly specialised per
module, in the same class as ``Item`` in ``core.jobs`` and ``core.review``, and
every call site in this repository spells the module. The hazard, stated so the
next reader does not rediscover it: a caller importing the bare name from the
wrong module gets a dataclass with entirely different fields.

Layer note: MODULES. It names its own workflow string for the session log, which
is the value ``core.session`` takes as a parameter precisely so that no layer
below the modules names a verb.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from cratekit.cli.output import timestamp
from cratekit.core import config, locations, preflight, rb_writer, review, session, tombstone
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.deletion import candidates as candidate_rules
from cratekit.deletion import library, stores, trash
from cratekit.deletion import watermark as watermark_store
from cratekit.deletion.candidates import Candidate, Category

logger = logging.getLogger(__name__)

#: The workflow name this pass records in the session log. It is not a verb name:
#: the CLI owns those, and this string names the OPERATION so that a person
#: reading the log can tell which session did what.
DELETION_WORKFLOW = "track-deletion"

#: The kind every deletion review item carries, taken from the shared identity
#: module so the item, the decline that may follow it, and anything that later
#: looks either of them up all spell it once.
REVIEW_KIND = tombstone.KIND_REMOVED_FILE

#: The one candidate a deletion review item offers. A verdict of ACCEPTED chooses
#: it and REJECTED settles against it, which is R35's pair exactly: move the file
#: to the Trash, or keep it and never ask again until the decline is revoked.
TRASH_OPTION = "move-to-trash"


@dataclass(frozen=True, slots=True)
class Plan:
    """What this run found, in full, before anybody has decided anything.

    ``baselined`` is True on the run that recorded a first watermark. It matters
    to the person reading the report: "nothing to delete" and "the removals that
    happened before today have been accepted as history" are different sentences,
    and R35 asks for the second one on a first run rather than presenting a whole
    library's worth of old removals as if they had just happened.
    """

    database_identity: str
    watermark: watermark_store.Watermark
    baselined: bool
    candidates: tuple[Candidate, ...] = ()
    references: candidate_rules.ReferenceSet | None = None
    baselined_over: int = 0
    #: The rows whose version identity is shared with a removed row carrying a
    #: DIFFERENT ISRC. Computed over the whole collection walk rather than over
    #: the filtered removals, because the row a candidate collides with may be
    #: one an earlier run already dealt with, and carried on the plan rather than
    #: recomputed because ``apply`` re-checks each candidate through the same
    #: categoriser and has to hand it the same answer the review was made under.
    ambiguous: frozenset[str] = frozenset()

    @property
    def deletable(self) -> tuple[Candidate, ...]:
        return tuple(item for item in self.candidates if item.deletable)

    def by_category(self) -> Mapping[str, tuple[Candidate, ...]]:
        """Every candidate grouped by its answer, INCLUDING the empty groups.

        Derived by iterating the enum rather than by collecting the categories
        that turned up, so a report shows "size-mismatch: 0" rather than omitting
        the row. An absent row and a zero read the same way to a person skimming,
        and only one of them means the check ran.
        """
        return {
            str(category): tuple(
                item for item in self.candidates if item.category is category
            )
            for category in Category
        }


@dataclass(frozen=True, slots=True)
class Trashed:
    """One file that was moved, where it went, and the tombstone that followed it."""

    candidate: Candidate
    target: str
    suppression_id: str


@dataclass(frozen=True, slots=True)
class Report:
    """What one apply did. Every list is a fact about files, not about intentions."""

    plan: Plan
    trashed: tuple[Trashed, ...] = ()
    declined: tuple[Candidate, ...] = ()
    refused: tuple[Candidate, ...] = ()
    watermark: watermark_store.Watermark | None = None


def _rules(
    cfg: config.Config, prefix_map: Sequence[locations.PrefixRule] | None
) -> list[locations.PrefixRule]:
    """The volume prefix map, resolved once per run and passed everywhere.

    One map for the reference set, the candidates and the re-check. Letting any
    of the three resolve its own would be two resolvers answering one question,
    and the cost of them disagreeing is a file that looks unreferenced to the
    proof and referenced to nothing.

    EACH RULE CARRIES THE IDENTITY RECORDED FOR ITS TARGET, which is what makes
    this pass's rules differ from every reader's. A reader follows a rule to
    look; this follows one to move a file, so where the rule points has to be
    provable and not only present.
    """
    if prefix_map is not None:
        return list(prefix_map)
    return [
        locations.PrefixRule(source, target, volume_id)
        for source, target, volume_id in cfg.resolved_prefix_rules()
    ]


def _assert_library_is_still(
    cfg: config.Config,
    db: Any,
    *,
    rules: Sequence[locations.PrefixRule],
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> None:
    """The four assertions that make every later answer mean anything.

    Volume identity first, because it is the one that decides whether the other
    two are being asked about the right disk at all. Then the refusal while
    rekordbox or its background agent is running, then the cloud canary, because
    both of those are asking the same question from two directions: is anything
    else changing this library while this run reads it.

    THE IDENTITY IS ASKED OF EVERY VOLUME THIS PASS CAN REACH, not only the one
    the library root sits on. A prefix rule sends a row onto whatever is mounted
    at its target, and both halves of the pass follow it: the reference set reads
    there to prove a file unreferenced, and the move writes there. Asserting the
    root alone left the first half proving things about the wrong directory and
    the second trashing files on a disk nobody had identified. ``rules`` is
    required rather than defaulted to none, because an empty default is a caller
    who forgot being read as a library with no rules.
    """
    session.assert_volume_identity(
        cfg, identity_provider=identity_provider, mount_enumerator=mount_enumerator
    )
    session.assert_mapped_volume_identities(
        cfg, rules, identity_provider=identity_provider, mount_enumerator=mount_enumerator
    )
    rb_writer.assert_rekordbox_closed("reviewing tracks removed from the collection")
    rb_writer.canary(db)


def plan(
    cfg: config.Config,
    db: Any,
    *,
    actor: str,
    prefix_map: Sequence[locations.PrefixRule] | None = None,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
    stat: candidate_rules.Stat = os.stat,
    now: datetime | None = None,
) -> Plan:
    """Read the library and answer every removal since the watermark. Writes no file.

    Read-only against the database and against the music volume. The one thing it
    can write is the watermark, and only on the run that BASELINES: R35 says a
    first run on an existing library accepts the prior removals as history rather
    than presenting them, and accepting them is a decision that has to be
    recorded or the next run makes it again.
    """
    rules = _rules(cfg, prefix_map)
    _assert_library_is_still(
        cfg,
        db,
        rules=rules,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    )
    identity = library.database_identity(db)
    counter = library.current_sequence(db)
    marks = watermark_store.WatermarkStore(cfg)

    # ONE walk of the collection, with no filter, because the baseline needs the
    # highest sequence any removal carries and the filter needs the baseline. A
    # second walk would return nothing at all against a database cursor, which is
    # the shape that reports an empty library while the run reports clean.
    seen = library.read_collection(db.get_content())
    highest = max((row.sequence for row in seen.removed), default=counter)

    mark, baselined = marks.baseline(
        database_identity=identity,
        sequence=max(counter, highest),
        actor=actor,
        now=None if now is None else timestamp(now),
    )
    if baselined:
        return Plan(
            database_identity=identity,
            watermark=mark,
            baselined=True,
            baselined_over=len(seen.removed),
        )

    # STRICTLY GREATER, AND THIS IS THE ONLY PLACE THE RULE IS APPLIED. The
    # watermark names the highest sequence everything at or below which has been
    # handled, so a row sitting exactly on it is one this pass has already
    # finished with; greater-or-equal would re-offer the last row of every
    # previous run, forever. ``read_collection`` used to carry the same test
    # behind a parameter the only caller permanently disabled, which is one rule
    # written twice with one copy unreachable, so neither copy could be measured.
    removed = tuple(row for row in seen.removed if row.sequence > mark.sequence)
    references = candidate_rules.reference_set(
        seen.active, root=cfg.library.root, prefix_map=rules, stat=stat
    )
    candidate_rules.assert_complete(references)
    # THE COUNTS ARE SAID OUT LOUD even on the run that proceeds. ``missing`` is
    # the tally the proof deliberately does not block on, and a tally nothing
    # ever reports is indistinguishable from a tally nobody computes: the whole
    # reference set could have been empty for a configuration reason and the run
    # would have read as clean. Reported at INFO because it is the ordinary
    # state of a real library, and at WARNING when the number is the entire
    # active collection, which is not.
    logger.info("deletion reference set: %s", dict(references.counts))
    for anchor in references.suspect_anchors:
        # PER ANCHOR, NOT PER RUN. The first version of this warning fired only
        # when the WHOLE reference set was empty, which one unrelated active row
        # resolving anywhere in the library was enough to silence, and the case
        # it exists for is precisely a rule that points at an existing but wrong
        # directory, where the rest of the library resolves perfectly well.
        logger.warning(
            "every active row that resolves through %s points at a file that is "
            "not there, so nothing under it was indexed and no candidate can be "
            "shown to collide with any of those rows; if that is not the "
            "directory those rows actually live in, this run cannot prove "
            "anything about the files it is about to offer",
            anchor,
        )
    referenced = library.playlist_referenced(db.get_playlist_songs())

    # OVER THE WHOLE WALK, NOT OVER THE FILTERED REMOVALS. See
    # ``stores.ambiguous_versions``: what makes a tombstone dangerous is that a
    # SECOND row produces the same identity, and that second row is very often
    # one an earlier run already retired, which is exactly the set the watermark
    # filter has just removed. Asking the filtered set would find the collision
    # only when both halves of it happened to be removed in the same window.
    ambiguous = stores.ambiguous_versions(seen.removed)
    answered = candidate_rules.categorize(
        removed,
        references,
        root=cfg.library.root,
        prefix_map=rules,
        referenced=referenced,
        declined=stores.decline_predicate(cfg),
        identifiable=stores.identifiable,
        ambiguous=lambda row: row.content_id in ambiguous,
        stat=stat,
    )
    return Plan(
        database_identity=identity,
        watermark=mark,
        baselined=False,
        candidates=answered,
        references=references,
        ambiguous=ambiguous,
    )


def present(cfg: config.Config, found: Plan, *, handler_key: str = "") -> tuple[review.Item, ...]:
    """Put every deletable candidate in front of a person, idempotently (R12, R35).

    ONLY THE DELETABLE ONES ARE OFFERED. Every other category is reported and
    never asked about, because there is no question to ask: nobody can answer
    "this file is also an active row's file" with a decision, and offering it
    would train a person to approve things the software has already said it
    cannot prove.

    Re-offering is free. The queue addresses an item by a content-derived
    identifier, so a run that offers the same candidate again returns the item
    that is already there with the verdict somebody already recorded, rather than
    asking twice.
    """
    if found.baselined:
        return ()
    items: list[review.Item] = []
    with review.open_store(cfg) as store:
        for item in found.deletable:
            items.append(
                review.offer(
                    store,
                    queue=review.Queue.DELETION,
                    kind=REVIEW_KIND,
                    identity=stores.row_identity(item.row),
                    payload={
                        "artist": item.row.artist,
                        "title": item.row.title,
                        "path": item.resolved or "",
                        "size": item.observed_size,
                        "sequence": item.row.sequence,
                        "content_id": item.row.content_id,
                    },
                    options=(
                        review.Option(
                            option_id=TRASH_OPTION,
                            summary="move this file to the system Trash",
                            detail={"path": item.resolved or ""},
                        ),
                    ),
                    handler_key=handler_key,
                )
            )
    return tuple(items)


def _verdicts(cfg: config.Config) -> dict[str, review.Item]:
    """Every deletion item that has been decided, by identifier.

    Walked through ``iter_items`` rather than fetched per candidate, so one query
    answers for the whole run and a candidate nobody has looked at costs no
    exception. Resolved items are included deliberately, since a resolved item is
    the entire point of reading this queue at all.
    """
    with review.open_store(cfg) as store:
        return {
            item.item_id: item
            for item in review.iter_items(
                store,
                predicate=review.Predicate(queue=review.Queue.DELETION),
                include_resolved=True,
            )
            if item.resolved
        }


def _item_id(item: Candidate) -> str:
    return review.item_id_for(
        review.Queue.DELETION, REVIEW_KIND, stores.row_identity(item.row)
    )


def _record_or_put_it_back(
    cfg: config.Config, moved: Candidate, target: Path, *, actor: str
) -> review.Suppression:
    """Write the tombstone the move owes, or undo the move. Never neither (R36).

    **THE ONE WINDOW IN THIS PASS WHERE FAILING HAS ALREADY DESTROYED
    SOMETHING**, and until this function existed the pass fell through it
    silently. The pre-flight ``list_tombstones`` above proves the store
    READABLE, which is a different claim from writable: a store on a full disk,
    on a volume that went read only, or whose sibling lock cannot be taken reads
    perfectly and refuses every write. So the sequence "the file is in the Trash,
    the tombstone is not written" is reachable, and it used to end the run by
    propagating, which LOOKS safe because the watermark never advances.

    It is not safe, and the reason is the next run rather than this one. The file
    is gone from where the row named, so the categoriser answers ``GONE``,
    ``GONE`` is the one member of ``HANDLED``, and the watermark passes straight
    over the row. Net result: the file sits in the Trash forever with no
    tombstone, R36's "every completed deletion writes one" is false, the version
    is re-acquirable, and nothing anywhere records that any of it happened. It is
    the only state in this unit where the product loses an invariant with no
    trace at all.

    So the move is UNDONE instead. ``trash.recover`` renames the file back to
    where the row named, which puts the library exactly where it was before this
    candidate was touched: the row is still removed, the file is still on disk,
    the re-run categorises it deletable again, and the person's confirmation is
    still in the queue. The store's own refusal then propagates untouched,
    carrying the remedy it was built with, because the thing to fix is the store
    and it is the store that knows what is wrong with it.

    WHEN THE UNDO ITSELF FAILS the refusal is REPLACED rather than chained
    quietly, because the two states need different sentences from the person.
    A store that will not write is an errand. A file in the Trash with no
    tombstone and no way back is a fact about their music, and the only thing
    that helps is being told both paths so they can move it themselves. The
    original cause rides inside so nothing about why is lost.

    **BOTH HANDLERS TAKE ``BaseException``, WHICH IS THE SAME CHOICE
    ``trash.move_to_trash`` ALREADY MADE FOR THE IDENTICAL WINDOW**, and taking
    only ``Exception`` here left the hole this function was written to close. The
    store write takes a sibling lock, which is the slowest thing in the pass, so
    it is precisely where a Ctrl-C lands: ``KeyboardInterrupt`` and the
    ``SystemExit`` a SIGTERM handler raises are both ``BaseException`` and neither
    is an ``Exception``. Either one used to walk straight out of this function
    with the file in the Trash and no tombstone, which is the state the whole
    function exists to make unreachable. The undo runs first and the interrupt
    then propagates untouched, because the bare ``raise`` re-raises what arrived
    rather than something built here, so Ctrl-C still ends the process the way
    the person asked it to.

    THE INNER HANDLER TAKES IT TOO, and that one does convert: an interrupt
    during the recover becomes this refusal. It is worth it. The alternative is a
    bare traceback for the one state in this unit where a person must be told two
    paths and a manual step, and the interrupt is not lost, it rides in as the
    ``from`` cause.
    """
    try:
        return stores.record_tombstone(cfg, moved.row, actor=actor, trashed_to=str(target))
    except BaseException as exc:
        original = moved.resolved or moved.row.recorded
        try:
            trash.recover(target, original)
        except BaseException as undo:
            cause = exc.cause if isinstance(exc, CratekitError) else None
            raise refuse(
                "internal-error",
                f"{original} was moved to {target} and the tombstone R36 "
                f"requires could not be written ({exc}), so the deletion is "
                f"half done; putting the file back failed too ({undo}), which "
                f"leaves it in the Trash with nothing recording that this "
                f"library deliberately stopped holding it",
                steps=(
                    f"move {target} back to {original} by hand, then run this "
                    f"again once the suppression store can be written",
                ),
                scope=Scope.RUN,
                origin=("deletion.run",),
                detail={"path": original, "trashed_to": str(target)},
                inner=cause,
            ) from exc
        logger.warning(
            "the tombstone for %s could not be written (%s), so the file was "
            "moved back out of the Trash and this deletion did not happen; "
            "nothing further was attempted",
            original,
            exc,
        )
        raise


def _the_anchor_proved_nothing(
    answered: Candidate, references: candidate_rules.ReferenceSet
) -> bool:
    """Whether this row's missing file is a statement about a DIRECTORY, not a file.

    **THE WHOLE OF THE ROUND SIX DEFECT IS THAT NOBODY ASKED THIS.**
    ``candidates.categorize`` answers ``GONE`` for a row whose file will not stat
    as long as the anchor directory EXISTS, and existence is not the question. A
    volume that unmounted cleanly leaves no mount point and every row through it
    is ``UNRESOLVED``, which is right and is not the case here. What macOS leaves
    after an UNCLEAN eject, and what anything at all creates by writing to the
    path while the drive is detached, is the mount point directory standing there
    EMPTY. Every removed row through it then stats absent, reads ``GONE``, and
    the round six settlement writes each one a tombstone, marks it handled, and
    lets the watermark past. Remounting the drive brings none of them back. That
    is a whole library's removal history recorded as deleted, with the files
    untouched, off one empty directory.

    **THE COUNTER-EVIDENCE WAS ALREADY COMPUTED AND WAS NOT WIRED TO ANYTHING
    THAT DECIDES.** ``reference_set`` walks the ACTIVE rows through the same
    anchors, and ``suspect_anchors`` names every anchor that exists, produced no
    filesystem identity at all, and had at least one active row go missing under
    it. On the empty mount point that is the whole volume; on a mounted library
    where somebody deleted one track in the Finder it is nothing, because
    thousands of active rows are indexed under that same anchor. So the signal
    separates the two cases this pass most needs separated, and it does it
    without a threshold: the question is whether ANY active row found a file
    there, not how many.

    WHICH WAY THIS FAILS, AND WHAT NOW STANDS BEHIND IT. An anchor with no active
    rows through it at all is not suspect, because ``missing_under`` never
    records it, so on this signal alone a mapped volume holding only removed
    rows settles off an empty mount point. Nothing local can do better: with no
    active row through that anchor there is no evidence either way, and the
    alternative is a threshold over how many removed rows look gone, which is
    the same all-or-nothing rule ``suspect_anchors`` replaced. The evidence that
    closes it comes from outside the walk. An empty mount point is on the disk
    that holds the mount directory, not on the volume the rule recorded, so
    ``_assert_the_volume_this_file_is_on`` refuses before this is ever asked.
    This signal stays for the case identity cannot see, which is the right disk
    with the wrong directory named.
    """
    return answered.anchor is not None and answered.anchor in references.suspect_anchors


def _settle_a_confirmed_absence(
    cfg: config.Config,
    answered: Candidate,
    *,
    actor: str,
    recorded: Callable[[library.RemovedRow], bool],
    references: candidate_rules.ReferenceSet,
) -> bool:
    """Finish a CONFIRMED removal whose file is not where the row named it. Returns handled.

    **ABSENCE IS NOT EVIDENCE THAT A DELETION HAPPENED, AND HOLDING THE ROW OPEN
    FOREVER IS NOT THE ANSWER EITHER. BOTH OF THOSE HAVE SHIPPED HERE.** ``GONE``
    is the single member of :data:`candidates.HANDLED`, so a confirmed row whose
    file is absent was once retired by the watermark with no tombstone written:
    a person confirmed a deletion, moved the file by hand before the apply, and
    the run reported nothing trashed, recorded nothing, and passed over the row.
    That was closed by refusing to retire the row without a tombstone, and the
    refusal has a cost nobody measured: a person who confirmed a removal and then
    deleted that file in the Finder can never satisfy it. The file cannot come
    back. The row holds the watermark at its own sequence forever, and because
    the watermark is contiguous, EVERY REMOVAL ABOVE IT IS HELD TOO, including
    ones this pass trashed and recorded perfectly. One Finder delete wedges the
    whole queue.

    **SO THE DELETION IS COMPLETED RATHER THAN HELD.** The person confirmed this
    removal, rekordbox no longer holds the row, and the file is not at the path
    the row records. That is a deletion that happened, by their hand rather than
    by this pass's, and R36 says a completed deletion writes a tombstone. Writing
    it is what makes the row finished business honestly, rather than retiring it
    while R36 is quietly false, which is what the original defect did.

    WHAT IT COSTS WHEN THE FILE WAS MOVED RATHER THAN DELETED, stated because it
    is the case that is not certain. The bytes are still on the disk somewhere,
    outside the collection, and the version is now suppressed from future
    acquisition. No music is lost: they have the file. The suppression is
    LISTABLE and REVOCABLE by R36, which is the property that makes writing it
    the recoverable choice and holding the queue open the unrecoverable one, and
    the caller says out loud that it happened and names the identifier to revoke.

    ONLY FOR A CONFIRMED ROW. A removal nobody has answered for is not settled
    here at all: a person who deletes music in the Finder has not asked this pass
    for anything, so there is no deletion of ours to record.

    **AND ONLY WHERE THE ABSENCE IS EVIDENCE ABOUT THE FILE.** The paragraph
    above reasons from "the file is not at the path the row records", and that
    sentence is worth nothing when the DIRECTORY the path hangs off answered
    nothing either. An empty mount point left behind by an unclean eject makes
    every row on the volume read absent, and settling them writes a tombstone
    apiece for files that are all still on a drive sitting on the desk. See
    :func:`_the_anchor_proved_nothing`: where the reference set says no active
    row found a file under that anchor, this refuses to settle and the row stays
    open. Holding the queue is the recoverable state and a shelf of tombstones
    for an unmounted drive is not, which is the reverse of the trade this
    function makes when the anchor IS answering.
    """
    if answered.category is not Category.GONE:
        return answered.handled
    if recorded(answered.row):
        return True
    if _the_anchor_proved_nothing(answered, references):
        logger.warning(
            "confirmed removal %s is not at %s and NOTHING WAS RECORDED, because "
            "every active row under %s is missing too: an anchor no active row "
            "found a file under says the volume is not really there, and this "
            "pass will not write a deletion off a directory that is empty. Mount "
            "the volume and run this again; the removal is still open and every "
            "removal after it is waiting behind it",
            answered.row.content_id,
            answered.resolved or answered.row.recorded,
            answered.anchor,
        )
        return False
    record = stores.record_tombstone(cfg, answered.row, actor=actor, trashed_to="")
    logger.warning(
        "confirmed removal %s is not at %s, so nothing was moved to the Trash; "
        "the deletion has been RECORDED anyway, because you confirmed it and the "
        "collection no longer holds the row, and R36 says a completed deletion "
        "is recorded. If you moved the file rather than deleting it, it is still "
        "on this disk outside the collection and this library will not acquire "
        "that version again until suppression %s is revoked",
        answered.row.content_id,
        answered.resolved or answered.row.recorded,
        record.suppression_id,
    )
    return True


def _warn_that_an_unanswered_removal_is_being_retired(
    answered: Candidate, *, recorded: Callable[[library.RemovedRow], bool], held: bool = False
) -> None:
    """Say what became of a removal nobody answered for whose file is elsewhere.

    **THE MIRROR OF THE CONFIRMED CASE, AND IT WAS SILENT.** A removal with no
    verdict uses ``item.handled`` directly, ``GONE`` is in
    :data:`candidates.HANDLED`, so the row is retired, the watermark passes it,
    no tombstone is written, and nothing offers it again. That scoping is
    deliberate and stays: nobody asked this pass for anything, so it has no
    deletion to record and re-walking a person's whole removal history forever
    would do more harm than the defect.

    What was wrong is that it happened without a word. If the file was MOVED
    rather than deleted it is still on the disk, no longer in the collection, and
    now no longer reachable by this pass either, which is the one state where a
    person has a file they can neither see in rekordbox nor be reminded of here.
    Saying it costs one log line and is the only notice they will get.

    ``held`` IS THE ANSWER TO A DIFFERENT QUESTION AND IT CHANGES THE SENTENCE.
    Retiring is only right where the absence is evidence about the file, and
    :func:`_the_anchor_proved_nothing` is where that is decided; when it says the
    anchor answered nothing, the caller does NOT retire the row and this says so
    instead. One retirement per unanswered removal was already permanent, so an
    empty mount point would otherwise retire a whole library's removal history in
    one pass, quietly, with no tombstone and no second chance.
    """
    if answered.category is not Category.GONE or recorded(answered.row):
        return
    if held:
        logger.warning(
            "removal %s was NOT retired: the file is not at %s, but no active row "
            "under %s found a file there either, so the volume rather than the "
            "file is what this run has proved absent. Mount it and run this "
            "again; nothing about this removal has been decided",
            answered.row.content_id,
            answered.resolved or answered.row.recorded,
            answered.anchor,
        )
        return
    logger.warning(
        "removal %s was retired without being offered: the file is not at %s and "
        "no tombstone records this library ever deleting it, so there is nothing "
        "to move and nothing to record. If you deleted it yourself that is the "
        "end of it; if you MOVED it, the file is still on this disk outside the "
        "collection and nothing will offer it again",
        answered.row.content_id,
        answered.resolved or answered.row.recorded,
    )


def _reopen_for_the_path_it_now_resolves_to(
    cfg: config.Config, item_id: str, *, actor: str
) -> None:
    """Withdraw a verdict that was made about a different file, so it is re-asked.

    **THE GUARD BELOW IS RIGHT AND IT USED TO HAVE NO WAY OUT.** A verdict may
    not travel to whatever the row resolves to at apply time, so a confirmed
    removal whose resolved path no longer matches the path the person was shown
    is refused. But ``review.offer`` leaves a RESOLVED item's payload alone, by
    design, so the item kept the stale path forever: correct a volume prefix rule
    after a remount, which is a legitimate repair and the exact case
    ``core.tombstone`` says a person "would be asked again" after, and every
    later apply compared the new path against the old one and refused again.
    Nothing moved, ever, and the only way back was ``review.clear`` run out of
    band by somebody who knew it existed.

    Clearing the verdict here is what "asked again" means as an act. It discards
    a decision, which is exactly right: the decision was about a file this row no
    longer resolves to, and the whole reason for the guard is that such a
    decision must not be honoured. The next ``present`` re-offers the item, and
    because an OPEN item's payload is refreshed, it is offered under the path the
    row resolves to now.

    The row is NOT handled either way, so the watermark holds and the re-offer
    reaches a person before anything moves.
    """
    with review.open_store(cfg) as store:
        review.clear(store, item_id, actor=actor)


def _assert_the_volume_this_file_is_on(
    cfg: config.Config,
    answered: Candidate,
    rules: Sequence[locations.PrefixRule],
    *,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> None:
    """Re-assert the volume under one answer before anything permanent is built on it.

    EVERY PERMANENT ACT IN THE LOOP RESTS ON A STAT, and a stat through a rule
    is only evidence while the right disk is mounted there. The move is the
    obvious one. The other two are quieter and just as permanent: a confirmed
    removal whose file will not stat is SETTLED with a tombstone, and an
    unanswered one is RETIRED past the watermark. Eject the drive part way
    through a queue, leaving its mount point behind, and every remaining file
    stops answering, reads as gone, and is recorded as deleted while it sits on
    a disk on the desk. So this is asked AFTER the evidence was gathered and
    BEFORE it is acted on, which is the order that catches a disk that went
    away underneath the stat.

    The rule is found through the same resolver and the same rules that produced
    the path, so the rule asserted is the rule that was followed. A row under
    the library root goes through no rule and is not this function's: the
    session asserts the root when it opens and again when it closes.
    """
    if answered.resolved is None:
        return
    resolved = locations.resolve_recorded_path(
        answered.row.recorded, root=cfg.library.root, prefix_map=rules
    )
    if resolved.rule_index is None:
        return
    session.assert_mapped_file_volume(
        cfg,
        rules,
        resolved.rule_index,
        answered.resolved,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    )


def apply(
    cfg: config.Config,
    db: Any,
    *,
    actor: str,
    prefix_map: Sequence[locations.PrefixRule] | None = None,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
    analysis_roots: Iterable[Path | str] = (),
    stat: candidate_rules.Stat = os.stat,
    home: Path | None = None,
    now: datetime | None = None,
) -> Report:
    """Trash every confirmed file, record what happened, and advance the watermark.

    THE SESSION IS THIS FUNCTION'S OWN and no gates factory is accepted, which is
    the rule the membership writer already argues: R29 declares the boundary as
    one source per run, and a caller-supplied factory can supply one that names no
    analysis roots, which would undo the argument by way of the parameter meant to
    make it flexible.

    THE PLAN IS REBUILT INSIDE THE GATES rather than passed in. A plan handed in
    is a photograph of a library taken before the lock was held, possibly days
    before, and R37's last sentence exists because of exactly that. Rebuilding is
    also what makes the dry run honest: the preview and the write run the same
    function over the same inputs, so a preview is evidence about the write rather
    than a second implementation that agrees most of the time.

    A DISAGREEMENT COSTS ONE FILE AND A BROKEN FILESYSTEM COSTS THE RUN, and the
    two are deliberately not the same. A candidate whose re-check no longer holds
    is reported and skipped, because that is a fact about that one track and
    aborting on the first one would leave a person with a queue full of confirmed
    items, no files moved, and one reason for all of them. A move that the
    filesystem refuses to perform stops the pass, because it is a fact about the
    disk and the next file will meet it too. Neither loses work: every file
    already moved has its tombstone, and the watermark is only advanced at the
    end, so a re-run sees the moved files as already gone and picks up the rest.
    """
    watched = [Path(root) for root in analysis_roots]
    trashed: list[Trashed] = []
    declined: list[Candidate] = []
    refused: list[Candidate] = []

    with session.assert_gates(
        cfg,
        workflow=DELETION_WORKFLOW,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
        analysis_roots=watched,
    ):
        found = plan(
            cfg,
            db,
            actor=actor,
            prefix_map=prefix_map,
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
            stat=stat,
            now=now,
        )
        if found.baselined:
            return Report(plan=found, watermark=found.watermark)
        if found.references is None:  # pragma: no cover - the branch above owns this case
            # NOT DEFAULTED TO AN EMPTY SET. An empty reference set is the
            # permissive answer: it says no active row points at anything, so
            # every candidate would pass the proof that exists to stop exactly
            # that. A plan with no reference set is a defect, and a defect that
            # trashes files is worth one refusal.
            raise refuse(
                "internal-error",
                "the plan carried no reference set, so nothing proves a candidate "
                "is unreferenced; refusing rather than treating the absence of "
                "evidence as evidence",
                remedy=Remedy.REPORT_DEFECT,
                scope=Scope.RUN,
                origin=("deletion.run",),
                detail={},
            )

        # BOTH DECISION STORES ARE PROVED READABLE BEFORE THE FIRST MOVE. The
        # tombstone is part of the deletion rather than a consequence of it
        # (R36), and the one window in this pass where a failure has already
        # destroyed something is between the move and the record. A store that
        # cannot be read refuses here, where nothing has moved yet, rather than
        # after the first file is in the Trash. The declines store was already
        # read by the plan; this is its sibling.
        #
        # IT IS THE SAME READ THAT ANSWERS THE GONE QUESTION, and merging the two
        # is deliberate rather than a saving. The pre-flight used to be a bare
        # ``list_tombstones`` beside a second read of the same store, and two
        # statements that prove one thing are one statement plus a line nothing
        # can be measured against: delete either and the other still refuses, so
        # neither is pinned by anything. One EAGER read, taken here rather than
        # where the answer is first wanted, is both the proof and the evidence,
        # and making it lazy is a change a test can see.
        recorded_now = stores.tombstone_predicate(cfg)

        decided = _verdicts(cfg)
        rules = _rules(cfg, prefix_map)
        referenced = library.playlist_referenced(db.get_playlist_songs())
        # THE RE-CHECK GETS THE SAME PREDICATE THE PLAN GOT, and its absence was
        # the one assertion the re-check quietly dropped. ``recheck`` defaults
        # ``declined`` to a predicate that answers False for every row, so a
        # re-check built without this argument reads "no decline is recorded"
        # rather than asking, which is absence taken as evidence of absence in
        # the one function whose docstring says it re-runs EVERY assertion. The
        # window is narrow, a decline recorded between the plan this apply just
        # built and the move below, but the thing on the other side of it is a
        # file that moves.
        #
        # ONE SNAPSHOT, TAKEN AFTER THE PLAN, rather than a read per row. That is
        # ``decline_predicate``'s own argument and it holds here for the same
        # reason: a store consulted per row could change underneath one pass, so
        # two rows in one report would have been judged against two different
        # sets of declines. Reading it here rather than reusing the plan's is
        # what narrows the window to the smallest one a single read can leave.
        declined_now = stores.decline_predicate(cfg)
        handled: list[tuple[int, bool]] = []

        for item in found.candidates:
            # THE PLAN'S ANSWER ABOUT THIS ROW IS ABOUT TO BE ACTED ON, by a
            # retirement, a settlement or a move, and the plan is as old as the
            # queue is long. See the function for why this comes first.
            _assert_the_volume_this_file_is_on(
                cfg,
                item,
                rules,
                identity_provider=identity_provider,
                mount_enumerator=mount_enumerator,
            )
            verdict = decided.get(_item_id(item))
            if verdict is None:
                # THE SAME QUESTION THE CONFIRMED PATH ASKS, ASKED HERE TOO. A
                # retirement is permanent whether or not a tombstone rides with
                # it, so an anchor that proved nothing must not retire this row
                # any more than it may record one.
                held = _the_anchor_proved_nothing(item, found.references)
                _warn_that_an_unanswered_removal_is_being_retired(
                    item, recorded=recorded_now, held=held
                )
                handled.append((item.row.sequence, item.handled and not held))
                continue
            if verdict.verdict is review.Verdict.REJECTED:
                # NOT HANDLED, and this is the pair to the one-way door
                # ``candidates.HANDLED`` argues against. A decline is revocable by
                # R35, and the watermark is the thing that decides whether a row
                # is ever looked at again. Passing over a declined sequence
                # retires the row permanently, so the revocation the stores
                # faithfully record would have nothing left to reach.
                stores.record_decline(cfg, item.row, actor=actor, resolved=item.resolved)
                declined.append(item)
                handled.append((item.row.sequence, False))
                continue
            if not item.deletable:
                # CONFIRMED, AND NO LONGER DELETABLE. Reported rather than
                # dropped: this is the case where a person answered a question
                # and the answer stopped applying, and a run that silently did
                # nothing about it would leave them believing the file had been
                # trashed. The category says which assertion stopped holding.
                logger.warning(
                    "confirmed removal %s is %s now and was not moved: %s",
                    item.row.content_id,
                    item.category,
                    item.problem,
                )
                refused.append(item)
                handled.append(
                    (
                        item.row.sequence,
                        _settle_a_confirmed_absence(
                            cfg,
                            item,
                            actor=actor,
                            recorded=recorded_now,
                            references=found.references,
                        ),
                    )
                )
                continue

            # RE-ASSERTED IMMEDIATELY BEFORE THE MOVE, through the same
            # categoriser that produced the answer in the first place. A second,
            # smaller re-check written here would be a second opinion, and the
            # two would eventually disagree about what a collision is.
            # TWO PREDICATES ARE DELIBERATELY NOT RE-SUPPLIED, AND BOTH USED TO
            # BE. ``identifiable`` and ``ambiguous`` were passed here as well,
            # and deleting either killed exactly ZERO tests, measured. Neither
            # can ever measure otherwise, which is the point: both answers are
            # functions of the plan this ``apply`` has just rebuilt, the loop
            # skips every candidate that plan did not call deletable, and a row
            # failing either one is UNIDENTIFIABLE or AMBIGUOUS_VERSION and
            # therefore not deletable. So the re-check could never be handed a
            # row for which either answer differed. That is one rule written
            # twice with one copy unreachable, which is the shape the ``since``
            # parameter was deleted for, and it is deleted for the same reason
            # rather than left as a line that reads as a guard and is not.
            #
            # ``declined`` IS re-supplied, and the difference is the whole
            # distinction: ``declined_now`` is a fresh read of a store taken
            # after the plan, so it genuinely can differ, and a decline recorded
            # in that window is a file that must not move.
            fresh = candidate_rules.recheck(
                item,
                found.references,
                root=cfg.library.root,
                prefix_map=rules,
                referenced=referenced,
                declined=declined_now,
                stat=stat,
            )
            # AND AGAIN FOR THE RE-CHECK'S OWN ANSWER, which is a fresh stat and
            # therefore fresh evidence. It sits before BOTH branches below on
            # purpose: a re-check that now says the file is gone is settled with
            # a tombstone a few lines down, and that is the branch an ejected
            # drive takes, so asserting only on the way to the move would guard
            # the one branch a missing disk never reaches.
            _assert_the_volume_this_file_is_on(
                cfg,
                fresh,
                rules,
                identity_provider=identity_provider,
                mount_enumerator=mount_enumerator,
            )
            if not fresh.deletable or fresh.resolved is None:
                logger.warning(
                    "confirmed file %s is %s now and was not moved: %s",
                    fresh.resolved or item.row.recorded,
                    fresh.category,
                    fresh.problem,
                )
                refused.append(fresh)
                handled.append(
                    (
                        item.row.sequence,
                        _settle_a_confirmed_absence(
                            cfg,
                            fresh,
                            actor=actor,
                            recorded=recorded_now,
                            references=found.references,
                        ),
                    )
                )
                continue

            # THE PATH THE PERSON WAS SHOWN IS PART OF WHAT THEY ANSWERED, even
            # though it is deliberately not part of the item's IDENTITY. Keeping
            # it out of the identity is right: a remount changes the path and must
            # not throw away a decision somebody already made about that row. But
            # the argued cost of the exclusion was "asked again after a remount",
            # and the real cost is larger, because the verdict otherwise travels
            # to whatever the row resolves to at apply time. Edit the prefix map
            # between the review and the apply and a DIFFERENT file is moved while
            # the one they looked at is still on disk. Comparing here keeps the
            # decision durable and keeps it bound to the file it was made about.
            #
            # AND A DECISION THAT CANNOT BE HONOURED IS WITHDRAWN RATHER THAN
            # STOOD ON FOREVER. See ``_reopen_for_the_path_it_now_resolves_to``:
            # an offer leaves a resolved item's payload alone, so without this
            # the stale path is compared against the new one on every later run
            # and a legitimately corrected prefix rule refuses the confirmed
            # deletion permanently, with the only way out being a command
            # nothing in this pass names.
            shown = str(verdict.payload.get("path") or "")
            if shown and locations.norm_for_compare(shown) != locations.norm_for_compare(
                fresh.resolved
            ):
                _reopen_for_the_path_it_now_resolves_to(cfg, _item_id(item), actor=actor)
                logger.warning(
                    "confirmed removal %s was accepted for %s and now resolves to "
                    "%s, so nothing was moved: the decision was made about a "
                    "different file. The confirmation has been withdrawn and this "
                    "removal will be offered again for the path it resolves to now",
                    item.row.content_id,
                    shown,
                    fresh.resolved,
                )
                refused.append(fresh)
                handled.append((item.row.sequence, False))
                continue

            layout = trash.assert_usable(fresh.resolved, home=home)
            try:
                target = trash.move_to_trash(fresh.resolved, layout=layout)
            except CratekitError as exc:
                # ONE NAME IS NOT THE DISK. A refusal the Trash raises about this
                # one destination, an over-long name whose numbered alternatives
                # will not fit or a directory already holding a thousand files of
                # that name, is declared Scope.ITEM by the module that raises it,
                # and honouring that declaration is what keeps one unlucky
                # filename from aborting a pass over a thousand good ones. Any
                # wider scope is a fact about the volume and stops the run.
                if exc.cause.scope is not Scope.ITEM:
                    raise
                logger.warning(
                    "confirmed file %s could not be given a name in the Trash at "
                    "%s and was not moved: %s",
                    fresh.resolved,
                    layout.files,
                    exc.cause.message,
                )
                refused.append(fresh)
                handled.append((item.row.sequence, False))
                continue
            except OSError as exc:
                # A STRUCTURED REFUSAL RATHER THAN A BARE OSError, because an
                # unstructured exception reaches the command line as an internal
                # defect and the remedy it was carrying is discarded (S4). The
                # run stops rather than continuing: a filesystem that cannot
                # perform this rename will not perform the next one either, and
                # every file already moved has its tombstone, so a re-run resumes
                # from where this stopped rather than repeating it.
                raise refuse(
                    "trash-unavailable",
                    f"{fresh.resolved} could not be moved into the Trash at "
                    f"{layout.files} ({exc}); nothing further was attempted",
                    remedy=Remedy.RUN_DOCTOR,
                    scope=Scope.RUN,
                    origin=("deletion.run",),
                    detail={"path": fresh.resolved, "trash": str(layout.files)},
                ) from exc
            record = _record_or_put_it_back(cfg, fresh, target, actor=actor)
            trashed.append(
                Trashed(candidate=fresh, target=str(target), suppression_id=record.suppression_id)
            )
            handled.append((item.row.sequence, True))

        reached = watermark_store.contiguous_sequence(handled, floor=found.watermark.sequence)
        marks = watermark_store.WatermarkStore(cfg)
        advanced = marks.advance(
            database_identity=found.database_identity,
            sequence=reached,
            actor=actor,
            now=None if now is None else timestamp(now),
        )

    return Report(
        plan=found,
        trashed=tuple(trashed),
        declined=tuple(declined),
        refused=tuple(refused),
        watermark=advanced,
    )


#: The key set ``tombstone.removed_file_identity`` produces, spelled once so the
#: check below compares against the identity's own shape rather than against two
#: strings somebody typed here. A decline addressed by anything else did not come
#: out of ``stores.record_decline``.
_DECLINE_IDENTITY_FIELDS: frozenset[str] = frozenset({"content_id", "recorded"})


def _assert_addressable(record: review.Suppression) -> None:
    """Refuse a decline whose review identifier cannot be DERIVED, before deriving it.

    **ONE VALUE MEANING TWO THINGS, WHICH IS THIS WAVE'S RECURRING FAULT.** The
    caller below treats ``review-item-unknown`` as "the queue legitimately does
    not hold this item", which is the case it is for: after an export and
    re-import, after a ``review.clear`` a person ran themselves, after any
    pruning. But that same reason arrives for a second, opposite cause: the
    identifier was DERIVED WRONG, from a record this function cannot address at
    all. The queue then holds the item perfectly well under a different
    identifier, the clear misses it, and the caller logs that the revocation
    stands while the REJECTED verdict is still armed. The next apply reads it,
    re-records the decline, and the revoke a person asked for is undone by the
    run that was supposed to complete it, with a cheerful INFO line as the only
    trace. Round 1 raised on this shape; round 2's narrowing gave it back.

    The derivation is a function of exactly two fields, so those two are checked
    POSITIVELY here and the ambiguity is gone by construction: past this point
    ``review-item-unknown`` can only mean the queue does not hold it. It is a
    check on the RECORD rather than a threshold, so it costs nothing and cannot
    refuse a legitimate revoke. A record in the declines store always comes from
    ``stores.record_decline``, which spells both fields once, so anything else is
    a build mismatch or a corrupt document, and REPORT_DEFECT says so instead of
    a sentence claiming a file was released that was not.
    """
    if record.kind == REVIEW_KIND and frozenset(record.identity or {}) == _DECLINE_IDENTITY_FIELDS:
        return
    raise refuse(
        "internal-error",
        f"the decline {record.suppression_id} is addressed by "
        f"{sorted(record.identity or {})} under kind {record.kind!r}, and a "
        f"deletion review item is addressed by {sorted(_DECLINE_IDENTITY_FIELDS)} "
        f"under {REVIEW_KIND!r}; the identifier that would reopen the review item "
        f"cannot be derived from it, and clearing a derived-wrong identifier "
        f"would report the file released while the verdict that holds it shut is "
        f"still there",
        remedy=Remedy.REPORT_DEFECT,
        scope=Scope.ITEM,
        origin=("deletion.run",),
        detail={"suppression_id": record.suppression_id, "kind": record.kind},
    )


def _reopen_review_item(cfg: config.Config, record: review.Suppression, *, actor: str) -> None:
    """Clear the verdict that produced a decline, so the file is asked about again.

    THE FIRST HALF OF REVOKING A DECLINE, and without it the other half does
    nothing a person can see. Lifting the decline lets the row be categorised as
    deletable again, and ``present`` then re-offers it, but ``review.offer`` is
    idempotent by design and hands back the item that is already there WITH THE
    REJECTION STILL ON IT. The next apply reads that verdict and records the
    decline again, so a run that revoked would end exactly where it started, and
    the only trace would be a revocation in a store nothing consults.

    **IT RUNS BEFORE THE STORE WRITE, AND THE ORDER IS THE WHOLE DESIGN.** These
    are two writes to two files with no transaction across them, so one of the
    four intermediate states is going to be reachable and the only question is
    which. Store first left the bad one: the decline lifted, the item still
    REJECTED, and the very next apply re-recording the decline, so a failed
    revoke ended as one standing decline with no trace that anybody had tried.
    Queue first leaves the harmless one. The decline still stands, so the file is
    still not offered, which is exactly what the person asked for last time; the
    item is open, which is idempotent; and re-running the revoke completes it.
    A partial revoke must never be the state where the suppression is gone and
    the thing that re-creates it is still armed.

    **A MISSING ITEM IS A REVOKE THAT HAS ALREADY SUCCEEDED, NOT A REFUSAL.**
    ``review.clear`` goes through ``review.get``, which refuses an identifier it
    cannot resolve, and that refusal is right for somebody who typed one. Here
    nobody typed it: it is derived from the record, and the queue legitimately
    may not hold it after an export and re-import, after a ``review.clear`` a
    person ran themselves, or after any pruning. Nothing is holding the file
    shut, which is the state this function exists to reach, so it returns having
    reached it. The reason is a DECLARED field on the cause and is what a caller
    may branch on; the message is not.

    The item is addressed by derivation rather than by search: the decline and
    the review item are built from the same kind and the same identity, so the
    identifier is a function of the record. A record written before identities
    were kept has nothing to derive from and is left alone, which costs that one
    record a re-offer rather than costing the revocation its meaning.

    **AND THE DERIVATION IS ASSERTED BEFORE IT IS TRUSTED.** See
    :func:`_assert_addressable`. Reading "the queue does not hold it" off a
    reason that a wrong derivation produces just as readily is the reading that
    let this function report a revocation complete while the verdict re-creating
    the decline was still armed.
    """
    if not record.identity:
        return  # pragma: no cover - a record predating the identity field
    _assert_addressable(record)
    with review.open_store(cfg) as store:
        try:
            review.clear(
                store,
                review.item_id_for(review.Queue.DELETION, record.kind, record.identity),
                actor=actor,
            )
        except CratekitError as exc:
            if exc.cause.reason != "review-item-unknown":
                raise
            logger.info(
                "no review item held the decline being revoked, so there was "
                "nothing to reopen; the revocation stands"
            )


def revoke(cfg: config.Config, suppression_id: str, *, actor: str) -> review.Suppression:
    """Lift one suppression, whichever store holds it (R35, R36).

    ONE ENTRY POINT FOR BOTH STORES, because a person holding an identifier from
    a listing should not have to know which of two files it came out of. The
    identifier itself says: it is derived from the store key, so an identifier
    from the tombstones cannot resolve in the declines and the search below can
    never revoke the wrong record.

    A DECLINE ALSO REOPENS ITS REVIEW ITEM and a tombstone does not, because the
    two suppress different things. A decline answers a question this queue asked,
    so lifting it puts that question back. A tombstone answers a question an
    acquisition pass will ask later and no item in this queue is holding it.

    THE QUEUE IS WRITTEN BEFORE THE STORE. See ``_reopen_review_item``: there is
    no transaction across the two files, so the order chooses which half-done
    state is reachable, and only one of the two is safe to be interrupted in.
    """
    for held in (stores.tombstones(cfg), stores.declines(cfg)):
        for record in held.suppressions(include_revoked=True):
            if record.suppression_id == suppression_id:
                if held.key == tombstone.DECLINE_STORE_KEY:
                    _reopen_review_item(cfg, record, actor=actor)
                    return held.revoke(suppression_id, actor=actor)
                # THROUGH THE STORES MODULE AND NOT THE STORE, because a credited
                # tombstone has a companion and lifting one without the other
                # leaves the version suppressed (R-431). The tombstones are still
                # read FIRST, so lifting one never depends on the declines store
                # being readable.
                return stores.revoke_tombstone(cfg, suppression_id, actor=actor)
    # Neither store holds it. The refusal comes from the store rather than being
    # written here, so a person gets the same sentence whichever way they arrive
    # at an identifier that resolves nowhere.
    return stores.revoke_tombstone(cfg, suppression_id, actor=actor)


__all__ = [
    "DELETION_WORKFLOW",
    "REVIEW_KIND",
    "TRASH_OPTION",
    "Plan",
    "Report",
    "Trashed",
    "apply",
    "plan",
    "present",
    "revoke",
]
