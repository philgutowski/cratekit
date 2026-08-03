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
from typing import Any, Iterable, Mapping, Sequence

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
    """
    if prefix_map is not None:
        return list(prefix_map)
    return [locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]


def _assert_library_is_still(
    cfg: config.Config,
    db: Any,
    *,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> None:
    """The three assertions that make every later answer mean anything.

    Volume identity first, because it is the one that decides whether the other
    two are being asked about the right disk at all. Then the refusal while
    rekordbox or its background agent is running, then the cloud canary, because
    both of those are asking the same question from two directions: is anything
    else changing this library while this run reads it.
    """
    session.assert_volume_identity(
        cfg, identity_provider=identity_provider, mount_enumerator=mount_enumerator
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
    _assert_library_is_still(
        cfg, db, identity_provider=identity_provider, mount_enumerator=mount_enumerator
    )
    identity = library.database_identity(db)
    counter = library.current_sequence(db)
    marks = watermark_store.WatermarkStore(cfg)

    # ONE walk of the collection, with no filter, because the baseline needs the
    # highest sequence any removal carries and the filter needs the baseline. A
    # second walk would return nothing at all against a database cursor, which is
    # the shape that reports an empty library while the run reports clean.
    seen = library.read_collection(db.get_content(), since=watermark_store.UNBASELINED)
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

    removed = tuple(row for row in seen.removed if row.sequence > mark.sequence)
    rules = _rules(cfg, prefix_map)
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
    if references.missing and not references.by_identity:
        logger.warning(
            "every active row that named a path (%d) points at a file that is "
            "not there, so nothing was indexed and no candidate can collide with "
            "anything; check the volume prefix map before acting on this run",
            len(references.missing),
        )
    referenced = library.playlist_referenced(db.get_playlist_songs())

    answered = candidate_rules.categorize(
        removed,
        references,
        root=cfg.library.root,
        prefix_map=rules,
        referenced=referenced,
        declined=stores.decline_predicate(cfg),
        identifiable=stores.identifiable,
        stat=stat,
    )
    return Plan(
        database_identity=identity,
        watermark=mark,
        baselined=False,
        candidates=answered,
        references=references,
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
        stores.list_tombstones(cfg, include_revoked=True)

        decided = _verdicts(cfg)
        rules = _rules(cfg, prefix_map)
        referenced = library.playlist_referenced(db.get_playlist_songs())
        handled: list[tuple[int, bool]] = []

        for item in found.candidates:
            verdict = decided.get(_item_id(item))
            if verdict is None:
                handled.append((item.row.sequence, item.handled))
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
                handled.append((item.row.sequence, item.handled))
                continue

            # RE-ASSERTED IMMEDIATELY BEFORE THE MOVE, through the same
            # categoriser that produced the answer in the first place. A second,
            # smaller re-check written here would be a second opinion, and the
            # two would eventually disagree about what a collision is.
            fresh = candidate_rules.recheck(
                item,
                found.references,
                root=cfg.library.root,
                prefix_map=rules,
                referenced=referenced,
                identifiable=stores.identifiable,
                stat=stat,
            )
            if not fresh.deletable or fresh.resolved is None:
                logger.warning(
                    "confirmed file %s is %s now and was not moved: %s",
                    fresh.resolved or item.row.recorded,
                    fresh.category,
                    fresh.problem,
                )
                refused.append(fresh)
                handled.append((item.row.sequence, fresh.handled))
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
            shown = str(verdict.payload.get("path") or "")
            if shown and locations.norm_for_compare(shown) != locations.norm_for_compare(
                fresh.resolved
            ):
                logger.warning(
                    "confirmed removal %s was accepted for %s and now resolves to "
                    "%s, so nothing was moved: the decision was made about a "
                    "different file",
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
            record = stores.record_tombstone(
                cfg, fresh.row, actor=actor, trashed_to=str(target)
            )
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


def _reopen_review_item(cfg: config.Config, record: review.Suppression, *, actor: str) -> None:
    """Clear the verdict that produced a decline, so the file is asked about again.

    THE SECOND HALF OF REVOKING A DECLINE, and without it the first half does
    nothing a person can see. Lifting the decline lets the row be categorised as
    deletable again, and ``present`` then re-offers it, but ``review.offer`` is
    idempotent by design and hands back the item that is already there WITH THE
    REJECTION STILL ON IT. The next apply reads that verdict and records the
    decline again, so a run that revoked would end exactly where it started, and
    the only trace would be a revocation in a store nothing consults.

    The item is addressed by derivation rather than by search: the decline and
    the review item are built from the same kind and the same identity, so the
    identifier is a function of the record. A record written before identities
    were kept has nothing to derive from and is left alone, which costs that one
    record a re-offer rather than costing the revocation its meaning.
    """
    if not record.identity:
        return  # pragma: no cover - a record predating the identity field
    with review.open_store(cfg) as store:
        review.clear(
            store,
            review.item_id_for(review.Queue.DELETION, record.kind, record.identity),
            actor=actor,
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
    """
    for held in (stores.tombstones(cfg), stores.declines(cfg)):
        for record in held.suppressions(include_revoked=True):
            if record.suppression_id == suppression_id:
                lifted = held.revoke(suppression_id, actor=actor)
                if held.key == tombstone.DECLINE_STORE_KEY:
                    _reopen_review_item(cfg, lifted, actor=actor)
                return lifted
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
