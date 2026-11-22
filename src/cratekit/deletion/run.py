"""The deletion pass: review what was removed, then trash exactly what was confirmed.

THE ORDER IS THE UNIT. Each step is where it is for a reason:

1. **The volume identity is asserted before anything is resolved (R38).** A
   restored clone mounted where the real library belongs is consistent all the
   way down, and the files trashed would be the backup recovery depends on.
   Every other check is evaluated against whatever is mounted.
2. **rekordbox is refused, application and background agent both.** A library
   open in rekordbox has rows in memory the file does not show, and which rows
   are active decides whether a file is somebody's music.
3. **The reference set is completed before any candidate is judged.** See
   ``candidates``: a proof built from the rows that answered is a different claim.
4. **The review is offered, and the move is a separate act** (R34, R35).
5. **Every precondition is re-asserted immediately before the move (R37).** A
   review item is durable and may be confirmed days later, so ``apply`` re-reads
   the library and re-runs the same categoriser rather than trusting a plan.

**NOTHING HERE WRITES A DATABASE ROW (KTD15).** Removals are read off rekordbox's
soft delete marker, off the session records of ``crate sync removed`` (U288),
and off a native landing's records of the rows it made while the database shows
that landing was not rolled back (R-1037, R-1844). The database is opened, read
and closed, so the session takes no capture: a snapshot protects rows, and the
files at risk are protected by the backup acknowledgment the gates require and by
the only move being into the Trash, which a rename reverses.

**NOTHING HERE TOUCHES A STREAMING SERVICE (R36).** A deletion is a fact about
this disk.

``analysis_roots`` defaults to empty because this pass opens no analysis file and
writes no tag; a caller may still name roots and the watch arms.

``Plan``, ``Report`` and ``apply`` also exist in ``write.metadata`` and
``core.profiles`` with other fields; every call site spells the module.

Layer note: MODULES. It names its own workflow string for the session log.
"""

from __future__ import annotations

import dataclasses
import functools
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from cratekit.cli.output import timestamp
from cratekit.core import config, locations, preflight, rb_writer, review, session, tombstone
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.deletion import candidates as candidate_rules
from cratekit.deletion import library, stores, trash
from cratekit.deletion import watermark as watermark_store
from cratekit.deletion.candidates import Candidate, Category

logger = logging.getLogger(__name__)

#: The operation this pass records in the session log; not a verb name.
DELETION_WORKFLOW = "track-deletion"

#: The kind every deletion review item carries, spelled once in ``core.tombstone``.
REVIEW_KIND = tombstone.KIND_REMOVED_FILE

#: The one option a deletion item offers. ACCEPTED trashes the file, REJECTED
#: keeps it until the decline is revoked (R35).
TRASH_OPTION = "move-to-trash"


@dataclass(frozen=True, slots=True)
class Plan:
    """What this run found, before anybody has decided anything.

    ``baselined`` is True on the run that recorded a first watermark: R35 wants
    "prior removals accepted as history" said on a first run, not "nothing to
    delete".
    """

    database_identity: str
    watermark: watermark_store.Watermark
    baselined: bool
    candidates: tuple[Candidate, ...] = ()
    references: candidate_rules.ReferenceSet | None = None
    baselined_over: int = 0
    #: Rows whose version identity is shared with a removed row of a DIFFERENT
    #: ISRC, computed over the whole walk (the twin may be one an earlier run
    #: retired) and carried so ``apply`` re-checks under the same answer.
    ambiguous: frozenset[str] = frozenset()
    #: Landings read as rolled back (R-1844) holding an absent row no run has
    #: numbered, so none is offered; said on the gate's screen.
    rolled_back: int = 0

    @property
    def deletable(self) -> tuple[Candidate, ...]:
        return tuple(item for item in self.candidates if item.deletable)


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
    """The volume prefix map, resolved once per run for the reference set, the
    candidates and the re-check, so one resolver answers all three.

    Each rule carries the identity recorded for its target: this pass follows a
    rule to move a file, so where it points has to be provable.
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
    """Volume identity first, then rekordbox closed, then the cloud canary.

    The identity is asked of EVERY volume a rule reaches, not only the root's:
    the reference set reads there and the move writes there. ``rules`` is
    required, because an empty default reads a forgetful caller as no rules.
    """
    session.assert_volume_identity(
        cfg, identity_provider=identity_provider, mount_enumerator=mount_enumerator
    )
    session.assert_mapped_volume_identities(
        cfg, rules, identity_provider=identity_provider, mount_enumerator=mount_enumerator
    )
    rb_writer.assert_rekordbox_closed("reviewing tracks removed from the collection")
    rb_writer.canary(db)


def _recorded_details(cfg: config.Config) -> tuple[session.SessionRecord, ...]:
    """Each readable session record (U288's removals, R-1037's landed rows).

    An unreadable record offers nothing, so its files stay; the pass says so.
    """
    found, unreadable = session.scan_log(cfg)
    if unreadable:
        logger.warning(
            "%d session record(s) could not be read, so a row a recorded removal took out of the "
            "collection, or a landed row removed in rekordbox, may not be offered this run",
            len(unreadable),
        )
    return found


def _playlists_held(db: Any) -> Callable[[str], bool]:
    """Whether the database holds a playlist row of an id, live or marked.

    Read once, and only when a landing record names a playlist.
    """
    read: list[frozenset[str]] = []

    def held(playlist_id: str) -> bool:
        if not read:
            read.append(library.playlist_ids(db.get_playlist()))
        return playlist_id in read[0]

    return held


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
    """Read the library and answer every removal since the watermark. Moves no file.

    The one write is the watermark's document: on the run that BASELINES (R35,
    so the next run does not decide again), and on a run that first sees a
    landed row gone or live again, since the number it is given must be read
    back rather than made again (R-1037).
    """
    rules = _rules(cfg, prefix_map)
    _assert_library_is_still(
        cfg, db, rules=rules, identity_provider=identity_provider, mount_enumerator=mount_enumerator
    )
    identity = library.database_identity(db)
    counter = library.current_sequence(db)
    marks = watermark_store.WatermarkStore(cfg)

    # ONE walk, unfiltered: the baseline needs the highest sequence and the
    # filter needs the baseline, and a second walk of a cursor returns nothing.
    seen = library.read_collection(db.get_content())
    # A row deleted outright carries no marker (R-1037, U288): the recorded
    # removals join the marked ones before the baseline and the watermark.
    records = _recorded_details(cfg)
    held = {row.content_id for row in seen.active} | {row.content_id for row in seen.removed}
    recorded = library.recorded_removals(
        [one.detail for one in records], database_identity=identity, present=held
    )
    # And a row a native landing made that the database no longer holds; one a
    # recorded removal names is that removal. Rolled back landings are counted
    # for the gate's screen (R-1844).
    landings = library.landed_absences(
        [one.detail for one in records],
        database_identity=identity,
        present=held | {row.content_id for row in recorded},
        uuids=seen.uuids,
        playlist_held=_playlists_held(db),
    )
    absent = landings.absent
    seen = dataclasses.replace(seen, removed=seen.removed + recorded)
    highest = max((row.sequence for row in seen.removed), default=counter)

    mark, baselined = marks.baseline(
        database_identity=identity,
        sequence=max(counter, highest),
        actor=actor,
        now=None if now is None else timestamp(now),
    )
    # Numbered AFTER the baseline: an absent row is given the count at its first
    # sighting, which on the baselining run is at or under the baseline, so it
    # is history (R35) with no rule of its own.
    mark = marks.sight(database_identity=identity, absent=absent, present=held, counter=counter)
    seen = dataclasses.replace(
        seen, removed=seen.removed + tuple(one.row(mark.absent[key]) for key, one in absent.items())
    )
    if baselined:
        return Plan(
            database_identity=identity,
            watermark=mark,
            baselined=True,
            baselined_over=len(seen.removed),
            rolled_back=landings.unasked(mark.absent),
        )

    # STRICTLY GREATER, and the only place the rule is applied: a row ON the
    # watermark is finished, and >= would re-offer every run's last row forever.
    removed = tuple(row for row in seen.removed if row.sequence > mark.sequence)
    references = candidate_rules.reference_set(
        seen.active, root=cfg.library.root, prefix_map=rules, stat=stat
    )
    candidate_rules.assert_complete(references)
    # The counts are said even when the run proceeds: a tally nobody reports is
    # indistinguishable from one nobody computes.
    logger.info("deletion reference set: %s", dict(references.counts))
    for anchor in references.suspect_anchors:
        # Per anchor, not per run: one healthy anchor elsewhere must not silence
        # a rule pointing at an existing but wrong directory.
        logger.warning(
            "every active row that resolves through %s points at a file that is not there, so "
            "nothing under it was indexed and no candidate can be shown to collide with any of "
            "those rows; if that is not the directory those rows actually live in, this run "
            "cannot prove anything about the files it is about to offer",
            anchor,
        )
    referenced = library.playlist_referenced(db.get_playlist_songs())

    # Over the whole walk, not the filtered removals: the colliding twin is often
    # a row an earlier run retired (see ``stores.ambiguous_versions``).
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
        rolled_back=landings.unasked(mark.absent),
    )


def present(cfg: config.Config, found: Plan, *, handler_key: str = "") -> tuple[review.Item, ...]:
    """Put every deletable candidate in front of a person, idempotently (R12, R35).

    Only the deletable ones: no other category has a question a decision could
    answer. Re-offering returns the item already there, verdict and all.
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
    """Every decided deletion item by identifier, from one walk of the queue."""
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
    return review.item_id_for(review.Queue.DELETION, REVIEW_KIND, stores.row_identity(item.row))


def _record_or_put_it_back(
    cfg: config.Config, moved: Candidate, target: Path, *, actor: str
) -> review.Suppression:
    """Write the tombstone the move owes, or undo the move. Never neither (R36).

    The one window where failing has already destroyed something. A store proved
    readable may still refuse a write, and a file in the Trash with no tombstone
    reads GONE next run, the watermark passes it, and nothing records it. So the
    move is undone with ``trash.recover`` and the store's own refusal propagates.

    If the undo fails too, the refusal is REPLACED with one naming both paths,
    the original riding inside. Both handlers take ``BaseException``, as
    ``trash.move_to_trash`` does: Ctrl-C and a SIGTERM's ``SystemExit`` land in
    the store's lock wait. The outer one re-raises what arrived after the undo;
    the inner one converts, so the person is told both paths.
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
                f"{original} was moved to {target} and the tombstone R36 requires could not be "
                f"written ({exc}), so the deletion is half done; putting the file back failed too "
                f"({undo}), which leaves it in the Trash with nothing recording that this library "
                "deliberately stopped holding it",
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
            "the tombstone for %s could not be written (%s), so the file was moved back out of "
            "the Trash and this deletion did not happen; nothing further was attempted",
            original,
            exc,
        )
        raise


def _the_anchor_proved_nothing(
    answered: Candidate, references: candidate_rules.ReferenceSet
) -> bool:
    """Whether this row's missing file is a statement about a DIRECTORY, not a file.

    An unclean eject leaves the mount point standing EMPTY, so every row through
    it reads ``GONE``. ``reference_set`` already walked the active rows through
    the same anchors: an anchor in ``suspect_anchors`` exists, indexed nothing
    and had rows go missing, which separates an empty mount point from one file
    deleted in the Finder with no threshold.

    An anchor no active row goes through is never suspect; for that case
    ``_assert_the_volume_this_file_is_on`` refuses first, since an empty mount
    point is on the wrong disk. This signal stays for the right disk with the
    wrong directory named.
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

    Retiring it without a tombstone loses R36's record, and holding it open
    forever wedges the contiguous watermark behind one Finder delete. So the
    deletion is RECORDED: the person confirmed it, rekordbox no longer holds the
    row and the file is not at its path. If the file was moved rather than
    deleted, the suppression is listable and revocable, and the caller names it.

    Only for a confirmed row, and only where the absence is evidence about the
    file: where :func:`_the_anchor_proved_nothing`, the row stays open, because
    tombstones for an unmounted drive are not recoverable and a held queue is.
    """
    if answered.category is not Category.GONE:
        return answered.handled
    if recorded(answered.row):
        return True
    if _the_anchor_proved_nothing(answered, references):
        logger.warning(
            "confirmed removal %s is not at %s and NOTHING WAS RECORDED, because every active row "
            "under %s is missing too: an anchor no active row found a file under says the volume "
            "is not really there, and this pass will not write a deletion off a directory that is "
            "empty. Mount the volume and run this again; the removal is still open and every "
            "removal after it is waiting behind it",
            answered.row.content_id,
            answered.resolved or answered.row.recorded,
            answered.anchor,
        )
        return False
    record = stores.record_tombstone(cfg, answered.row, actor=actor, trashed_to="")
    logger.warning(
        "confirmed removal %s is not at %s, so nothing was moved to the Trash; the deletion has "
        "been RECORDED anyway, because you confirmed it and the collection no longer holds the "
        "row, and R36 says a completed deletion is recorded. If you moved the file rather than "
        "deleting it, it is still on this disk outside the collection and this library will not "
        "acquire that version again until suppression %s is revoked",
        answered.row.content_id,
        answered.resolved or answered.row.recorded,
        record.suppression_id,
    )
    return True


def _warn_that_an_unanswered_removal_is_being_retired(
    answered: Candidate, *, recorded: Callable[[library.RemovedRow], bool], held: bool = False
) -> None:
    """Say what became of an unanswered removal whose file is elsewhere.

    Retiring it without a tombstone is deliberate (nobody asked this pass for
    anything), but a MOVED file is then reachable from nowhere, so it is said.
    ``held`` is the caller's answer from :func:`_the_anchor_proved_nothing`: the
    row is not retired, and the sentence says so instead.
    """
    if answered.category is not Category.GONE or recorded(answered.row):
        return
    if held:
        logger.warning(
            "removal %s was NOT retired: the file is not at %s, but no active row under %s found "
            "a file there either, so the volume rather than the file is what this run has proved "
            "absent. Mount it and run this again; nothing about this removal has been decided",
            answered.row.content_id,
            answered.resolved or answered.row.recorded,
            answered.anchor,
        )
        return
    logger.warning(
        "removal %s was retired without being offered: the file is not at %s and no tombstone "
        "records this library ever deleting it, so there is nothing to move and nothing to "
        "record. If you deleted it yourself that is the end of it; if you MOVED it, the file is "
        "still on this disk outside the collection and nothing will offer it again",
        answered.row.content_id,
        answered.resolved or answered.row.recorded,
    )


def _reopen_for_the_path_it_now_resolves_to(
    cfg: config.Config, item_id: str, *, actor: str
) -> None:
    """Withdraw a verdict made about a different file, so it is asked again.

    ``review.offer`` leaves a resolved item's payload alone, so without this a
    corrected prefix rule would compare the new path with the stale one and
    refuse forever. Clearing it lets ``present`` re-offer the item under the
    path the row resolves to now; the row is not handled, so nothing moves first.
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
    """Re-assert the volume under one answer before anything permanent rests on it.

    The move, a settlement's tombstone and an unanswered row's retirement all
    rest on a stat through a rule, and a drive ejected mid-queue leaves its
    mount point answering "gone". Asked after the evidence and before the act,
    through the rule that produced the path; a row under the library root is
    the session's to assert.
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

    The session is this function's own (R29: one source per run), and the plan
    is REBUILT inside the gates rather than handed in, so the preview and the
    write are one function over one library (R37).

    A re-check that no longer holds costs that one file and is reported; a move
    the filesystem refuses stops the run. Every file moved has its tombstone and
    the watermark advances only at the end, so a re-run picks up the rest.
    """
    seams = {"identity_provider": identity_provider, "mount_enumerator": mount_enumerator}
    watched = [Path(root) for root in analysis_roots]
    trashed: list[Trashed] = []
    declined: list[Candidate] = []
    refused: list[Candidate] = []

    with session.assert_gates(cfg, workflow=DELETION_WORKFLOW, analysis_roots=watched, **seams):
        found = plan(cfg, db, actor=actor, prefix_map=prefix_map, stat=stat, now=now, **seams)
        if found.baselined:
            return Report(plan=found, watermark=found.watermark)
        if found.references is None:  # pragma: no cover - the branch above owns this case
            # Not defaulted to an empty set, which would prove every candidate
            # unreferenced.
            raise refuse(
                "internal-error",
                "the plan carried no reference set, so nothing proves a candidate is "
                "unreferenced; refusing rather than treating the absence of evidence as evidence",
                remedy=Remedy.REPORT_DEFECT,
                scope=Scope.RUN,
                origin=("deletion.run",),
                detail={},
            )
        references = found.references

        # The tombstones are proved readable before the first move, by the same
        # eager read that answers whether a GONE row's deletion was recorded.
        recorded_now = stores.tombstone_predicate(cfg)
        decided = _verdicts(cfg)
        rules = _rules(cfg, prefix_map)
        referenced = library.playlist_referenced(db.get_playlist_songs())
        # The re-check gets a FRESH decline snapshot taken after the plan: a
        # decline recorded in that window is a file that must not move.
        declined_now = stores.decline_predicate(cfg)
        look = functools.partial(_assert_the_volume_this_file_is_on, cfg, rules=rules, **seams)
        settle = functools.partial(
            _settle_a_confirmed_absence,
            cfg,
            actor=actor,
            recorded=recorded_now,
            references=references,
        )

        def decide(item: Candidate) -> bool:
            """Act on one answer; returns whether the watermark may pass its row."""
            # The plan's answer is about to be acted on, and it is as old as the
            # queue is long: the volume is asserted first.
            look(item)
            verdict = decided.get(_item_id(item))
            if verdict is None:
                # A retirement is permanent too, so an anchor that proved nothing
                # retires nothing.
                held = _the_anchor_proved_nothing(item, references)
                _warn_that_an_unanswered_removal_is_being_retired(
                    item, recorded=recorded_now, held=held
                )
                return item.handled and not held
            if verdict.verdict is review.Verdict.REJECTED:
                # NOT handled: passing a declined sequence would retire the row,
                # and the revocation R35 promises would reach nothing.
                stores.record_decline(cfg, item.row, actor=actor, resolved=item.resolved)
                declined.append(item)
                return False
            if not item.deletable:
                logger.warning(
                    "confirmed removal %s is %s now and was not moved: %s",
                    item.row.content_id,
                    item.category,
                    item.problem,
                )
                refused.append(item)
                return settle(item)

            # Re-asserted immediately before the move through the same categoriser.
            # ``identifiable`` and ``ambiguous`` are functions of the plan just
            # rebuilt, which called this row deletable, so they could never differ;
            # ``declined`` is a fresh read and can.
            fresh = candidate_rules.recheck(
                item,
                references,
                root=cfg.library.root,
                prefix_map=rules,
                referenced=referenced,
                declined=declined_now,
                stat=stat,
            )
            # And again for the re-check's fresh stat, before both branches: an
            # ejected drive takes the settling branch, not the move.
            look(fresh)
            if not fresh.deletable or fresh.resolved is None:
                logger.warning(
                    "confirmed file %s is %s now and was not moved: %s",
                    fresh.resolved or item.row.recorded,
                    fresh.category,
                    fresh.problem,
                )
                refused.append(fresh)
                return settle(fresh)

            # The path the person was shown is part of what they answered, though
            # not of the item's identity: a changed prefix map would otherwise move
            # a DIFFERENT file. A decision that cannot be honoured is withdrawn so
            # it is asked again under the new path.
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
                return False

            layout = trash.assert_usable(fresh.resolved, home=home)
            try:
                target = trash.move_to_trash(fresh.resolved, layout=layout)
            except CratekitError as exc:
                # A refusal the Trash declares Scope.ITEM is about one name and
                # costs one file; any wider scope is the volume and stops the run.
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
                return False
            except OSError as exc:
                # Structured, so the remedy reaches the person (S4); the run stops,
                # since the next rename will fail too.
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
            return True

        handled = [(item.row.sequence, decide(item)) for item in found.candidates]
        reached = watermark_store.contiguous_sequence(handled, floor=found.watermark.sequence)
        advanced = watermark_store.WatermarkStore(cfg).advance(
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


#: The key set ``tombstone.removed_file_identity`` produces; a decline addressed
#: by anything else did not come out of ``stores.record_decline``.
_DECLINE_IDENTITY_FIELDS: frozenset[str] = frozenset({"content_id", "recorded"})


def _assert_addressable(record: review.Suppression) -> None:
    """Refuse a decline whose review identifier cannot be DERIVED, before deriving it.

    ``review-item-unknown`` is read below as "the queue does not hold it". A
    wrongly derived identifier produces the same reason while the REJECTED
    verdict stays armed and the next apply re-records the decline. The
    derivation reads exactly these two fields, so checking them positively
    leaves only the first meaning; anything else is a build mismatch or a
    corrupt document, REPORT_DEFECT.
    """
    if record.kind == REVIEW_KIND and frozenset(record.identity or {}) == _DECLINE_IDENTITY_FIELDS:
        return
    raise refuse(
        "internal-error",
        f"the decline {record.suppression_id} is addressed by {sorted(record.identity or {})} "
        f"under kind {record.kind!r}, and a deletion review item is addressed by "
        f"{sorted(_DECLINE_IDENTITY_FIELDS)} under {REVIEW_KIND!r}; the identifier that would "
        "reopen the review item cannot be derived from it, and clearing a derived-wrong "
        "identifier would report the file released while the verdict that holds it shut is still "
        "there",
        remedy=Remedy.REPORT_DEFECT,
        scope=Scope.ITEM,
        origin=("deletion.run",),
        detail={"suppression_id": record.suppression_id, "kind": record.kind},
    )


def _reopen_review_item(cfg: config.Config, record: review.Suppression, *, actor: str) -> None:
    """Clear the verdict that produced a decline, so the file is asked about again.

    Without it ``review.offer`` hands back the item WITH THE REJECTION on it and
    the next apply records the decline again.

    IT RUNS BEFORE THE STORE WRITE. Two files, no transaction: queue first
    leaves the harmless partial state (decline standing, item open, re-run
    completes it); store first left the decline lifted and the rejection armed.

    A missing item (export and re-import, a hand ``review.clear``, pruning) is
    a revoke already done, read off the declared reason, never the message. The
    identifier is derived from the record, and asserted derivable first
    (:func:`_assert_addressable`); a record predating identities is left alone.
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

    The identifier is derived from the store key, so it cannot resolve in the
    wrong store. A decline also reopens its review item, queue first (see
    ``_reopen_review_item``); a tombstone answers no question this queue asked.
    """
    for held in (stores.tombstones(cfg), stores.declines(cfg)):
        for record in held.suppressions(include_revoked=True):
            if record.suppression_id == suppression_id:
                if held.key == tombstone.DECLINE_STORE_KEY:
                    _reopen_review_item(cfg, record, actor=actor)
                    return held.revoke(suppression_id, actor=actor)
                # Through ``stores``, so a credited tombstone's companion goes too
                # (R-431); tombstones are read first, never needing the declines.
                return stores.revoke_tombstone(cfg, suppression_id, actor=actor)
    # Neither store holds it: the store refuses, in one sentence however reached.
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
