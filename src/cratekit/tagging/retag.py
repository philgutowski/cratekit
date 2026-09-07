"""Correct a genre that is already wrong (U40, Feature Inventory row 18).

WHY THIS IS A SECOND VERB AND NOT A FLAG ON THE FIRST.
:func:`cratekit.tagging.tag.tag_folder` is fill-if-empty BY CONSTRUCTION: it
reads the file's genre and skips any file that already carries one. That is the
right policy for a file with no genre, and it is precisely why a vendor's
catch-all survives for ever. The file HAS a genre, so no verb ever looks a better
one up, routing parks the track in the fallback bucket, and that bucket only
grows. Two policies over one field is not a flag, it is two verbs: one fills,
this one corrects, and the ownership each claims over the genre is different.

THE SELECTION IS THE TAXONOMY'S OWN AND NEVER A LIST WRITTEN HERE.
:meth:`cratekit.core.taxonomy.Taxonomy.is_too_coarse_as_source` reads the user's
declared ``too_coarse_as_source``, so the capability is general rather than one
person's catch-all. R19 forbids a display name in code below the modules layer
and this is the reason that rule exists: a name hardcoded here would work for one
library and quietly do nothing in the next.

A BLANK GENRE IS NOT SELECTED, AND THE TAXONOMY SAYS IT IS TOO COARSE.
``is_too_coarse_as_source("")`` is True, because the declared list carries the
empty string. Selecting on that predicate alone would put this verb and
``tag.folder`` on the same state under DIFFERENT ownership: fill-if-empty there,
OWNED here. One field owned by two operations with two policies is how a value a
person set by hand eventually loses to whichever ran last. So the selection is
"carries a genre AND that genre is too coarse", and a file with no genre is
skipped by name with the verb that owns it in the reason.

AN ANSWER THAT IS ITSELF TOO COARSE IS REFUSED, NEVER WRITTEN. The same
predicate, at the other end. Without it a lookup returning the same catch-all
launders it into a value this verb would never select again, because writing
counts as progress and re-reading the write does not.

A DECLINE IS A QUESTION, NOT A FAILURE. A searcher that returns nothing and an
answer refused above both leave the file unfixed, and both are things a person
can settle. They go into the GENRE review queue as ONE item per file, offered
with the declared buckets as its candidates, and :func:`cratekit.core.review.offer`
is idempotent on the identity, so a verdict survives every later run and the
question is asked once.

THE DATABASE HALF IS PLANNED, NEVER WRITTEN HERE. :func:`plan_library` builds a
:class:`cratekit.write.metadata.Plan` under the ``RETAG_GENRE`` policy and
:func:`apply_library` registers that policy before applying it. Registering is
not optional and not a convenience: an unregistered operation decides
``SKIP_UNOWNED`` for every change, which writes nothing and reports success, and
a sweep that silently wrote nothing looks exactly like a sweep with nothing to do.

LAYER: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.core import locations, review, tags, taxonomy
from cratekit.core.naming import AUDIO_EXTS
from cratekit.core.review import Queue
from cratekit.tagging.tag import Searcher
from cratekit.write import metadata, trees

#: The producing verb, in the registry's own vocabulary. Carried onto every review
#: item as a VALUE, exactly as the job engine carries the command line it
#: re-invokes, so this module never names the CLI layer.
HANDLER_KEY = "tag.retag"

#: ONE kind for BOTH unanswered shapes, deliberately. A searcher that declined and
#: a searcher whose answer was refused are two reasons for one question, "what
#: genre is this really". Two kinds would hash to two item identifiers on one file,
#: so a run whose searcher flipped from one shape to the other would put the same
#: question in front of the same person twice under two identities, and answering
#: one would leave the other asking.
KIND = "coarse-genre"

#: Why a file was passed over during selection.
NO_GENRE = "no-genre"
GENRE_SPECIFIC = "genre-specific"

#: Why a selected file was not written.
NO_ANSWER = "no-answer"
ANSWER_TOO_COARSE = "answer-too-coarse"
DECLINED_IN_REVIEW = "declined-in-review"


@dataclass(frozen=True, slots=True)
class Candidate:
    """One file this pass may correct, and the value it currently carries."""

    path: Path
    current: str


@dataclass(frozen=True, slots=True)
class Passed:
    """One file the selection did not take, and why.

    Surfaced rather than dropped. "Nothing was selected" and "nothing was looked
    at" are different answers and a person's next move after each is different.
    """

    path: Path
    reason: str


@dataclass(frozen=True, slots=True)
class Selection:
    """What one walk of a folder decided about every audio file under it."""

    candidates: tuple[Candidate, ...] = ()
    passed: tuple[Passed, ...] = ()


@dataclass(frozen=True, slots=True)
class RetagResult:
    """What happened to one candidate.

    ``written`` is the genre now on the file, or None. ``reason`` is empty exactly
    when ``written`` is set, so the two can never both describe the same file.
    """

    path: Path
    current: str
    written: str | None = None
    reason: str = ""
    proposed: str = ""
    item_id: str = ""


@dataclass(frozen=True, slots=True)
class RetagOutcome:
    """Every candidate's result and every file the selection passed over."""

    results: tuple[RetagResult, ...] = ()
    passed: tuple[Passed, ...] = ()

    @property
    def written(self) -> tuple[RetagResult, ...]:
        return tuple(result for result in self.results if result.written)

    @property
    def asked(self) -> tuple[RetagResult, ...]:
        """Results that put a question in the review queue on THIS run.

        A file settled against every candidate carries an item id too, because the
        item is what settled it, so "has an id and was not written" would count a
        decision as an open question and a report would tell a person there is
        work waiting for them that they already did. The reason is what separates
        the two, not the presence of an identifier.
        """
        return tuple(
            result
            for result in self.results
            if result.item_id and result.reason in {NO_ANSWER, ANSWER_TOO_COARSE}
        )


# ---------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------


def select(root: Path, *, declared: taxonomy.Taxonomy) -> Selection:
    """Every audio file under ``root`` whose genre is too coarse to be final.

    Sorted, so a plan digest over the result is stable across two runs on one
    unchanged folder. An unsorted walk would make the digest depend on directory
    order, and a gate answered against one digest would then be stale against a
    second run that changed nothing.
    """
    candidates: list[Candidate] = []
    passed: list[Passed] = []
    if not root.is_dir():
        return Selection()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in AUDIO_EXTS:
            continue
        # NOT STRIPPED HERE, and the missing call is deliberate. ``tags.read_tag``
        # already trims every value it returns, at ``core/tags.py:489``, so a
        # strip here was dead code: a mutation removing it killed nothing because
        # no input can reach it padded. A second normalization beside the one that
        # owns it is two opinions that agree until one of them moves.
        current = tags.read_genre_from_file(path) or ""
        if not current:
            # tag.folder's, under fill-if-empty. See the module docstring.
            passed.append(Passed(path=path, reason=NO_GENRE))
            continue
        if not declared.is_too_coarse_as_source(current):
            passed.append(Passed(path=path, reason=GENRE_SPECIFIC))
            continue
        candidates.append(Candidate(path=path, current=current))
    return Selection(candidates=tuple(candidates), passed=tuple(passed))


def plan_items(selection: Selection) -> list[dict[str, str]]:
    """The selection as plan rows, which is what the confirm gate digests."""
    return [
        {"path": str(candidate.path), "current": candidate.current}
        for candidate in selection.candidates
    ]


# ---------------------------------------------------------------------------
# The review queue: one item per file, asked once
# ---------------------------------------------------------------------------


def identity_for(path: Path | str) -> dict[str, str]:
    """What a review item about one file is addressed by.

    THE PATH, and the cost of that is stated rather than left to be discovered: a
    library that moves orphans every open item, because the identity hashes into
    the item id. A bare audio file carries no identifier this pass could use
    instead. The database half has content ids and this half runs before any row
    is matched, on purpose, so that a folder with no library rows at all can still
    be corrected.
    """
    return {"path": str(path)}


def options_for(declared: taxonomy.Taxonomy) -> tuple[review.Option, ...]:
    """The declared buckets, as the candidates a person may choose from.

    ``review.resolve`` refuses an option the item does not offer, so a person
    cannot answer with a genre nobody showed them. That makes the OFFER the place
    the answer set is decided, and the declared taxonomy is the only defensible
    source for it: these are exactly the genres this library routes by.

    The too-coarse ones are filtered out here as well as at the write. Filtering
    only here would let an item offered by an older build carry one; checking only
    at the write would put an answer in front of a person that the verb is going
    to refuse.
    """
    return tuple(
        review.Option(
            option_id=bucket.id,
            summary=bucket.display,
            detail={"genre": bucket.display},
        )
        for bucket in declared.buckets
        if not declared.is_too_coarse_as_source(bucket.display)
    )


def accepted_genre(item: review.Item) -> str:
    """The genre a resolved item settled on, or empty.

    Reads the OPTION the person chose out of the item's own option list rather
    than trusting the option id to be a genre name. The id is a bucket identifier
    and the genre is its display name (R19), and an id that happened to read like
    a display name is how the two silently become one thing.
    """
    if item.verdict is not review.Verdict.ACCEPTED or not item.option:
        return ""
    for option in item.options:
        if option.option_id != item.option:
            continue
        detail = option.detail or {}
        return str(detail.get("genre") or option.summary or "").strip()
    return ""


def decided_index(store: review.ReviewStore | None) -> dict[str, review.Item]:
    """Every item this pass has ever offered, read ONCE.

    A per-file lookup would be one query per candidate over a folder that can hold
    thousands. The whole queue for one kind is small enough to hold, and reading it
    once is the same reasoning ``trees.index_active_rows`` states for the library.

    PUBLIC BECAUSE THE JOB WORKER NEEDS IT TOO. A worker runs one candidate per
    call and builds this index per call, which is one read of a small queue per
    item rather than one per folder. The queue holds only unanswered coarse-genre
    questions, so it is bounded by the size of that backlog rather than by the
    library, and the cost is recorded as a residual rather than assumed away.
    """
    if store is None:
        return {}
    predicate = review.Predicate(queue=str(Queue.GENRE), kind=KIND)
    return {
        item.item_id: item
        for item in review.iter_items(store, predicate=predicate, include_resolved=True)
    }


def _ask(
    store: review.ReviewStore | None,
    candidate: Candidate,
    *,
    reason: str,
    proposed: str,
    declared: taxonomy.Taxonomy,
    handler_key: str,
) -> RetagResult:
    """Put the question in the queue and report the file as unwritten.

    With no store this still returns a result carrying the reason. A pass driven
    without a queue is a pass that reports what it could not settle, not a pass
    that pretends it settled it.
    """
    item_id = ""
    if store is not None:
        item = review.offer(
            store,
            queue=Queue.GENRE,
            kind=KIND,
            identity=identity_for(candidate.path),
            payload={
                "path": str(candidate.path),
                "current": candidate.current,
                "proposed": proposed,
                "reason": reason,
            },
            options=options_for(declared),
            handler_key=handler_key,
        )
        item_id = item.item_id
    return RetagResult(
        path=candidate.path,
        current=candidate.current,
        reason=reason,
        proposed=proposed,
        item_id=item_id,
    )


# ---------------------------------------------------------------------------
# The pass over the files
# ---------------------------------------------------------------------------


def retag_one(
    candidate: Candidate,
    *,
    searcher: Searcher,
    declared: taxonomy.Taxonomy,
    decided: Mapping[str, review.Item],
    store: review.ReviewStore | None = None,
    handler_key: str = HANDLER_KEY,
) -> RetagResult:
    """Correct ONE candidate's genre, or record why it was not corrected.

    THE PER CANDIDATE WORK, split out so a job worker can run exactly one of
    them. :func:`retag_folder` is this function applied to every candidate the
    selection took, so the sweep and the queued worker cannot come to hold two
    different policies about one field.

    A VERDICT ALREADY RECORDED IS READ BEFORE THE SEARCHER IS ASKED. That ordering
    is the whole of "a resolved verdict is not re-asked": asking first and reading
    afterwards would spend a lookup per run on a question a person has already
    answered, and would let a fresh answer overwrite the recorded one.

    A REJECTED item is settled AGAINST every candidate, so the file is left alone
    and nothing is re-offered. ``review.offer`` would not reopen it, but calling it
    would refresh nothing and would say in the code that this pass is still asking.

    ``decided`` is passed in rather than read here, because the folder sweep reads
    the queue once for the whole walk and a worker reads it once for its one item.
    Reading it inside would make the sweep one query per candidate.
    """
    item_id = review.item_id_for(Queue.GENRE, KIND, identity_for(candidate.path))
    item = decided.get(item_id)
    answer = ""
    if item is not None and item.resolved:
        if item.suppressed:
            return RetagResult(
                path=candidate.path,
                current=candidate.current,
                reason=DECLINED_IN_REVIEW,
                item_id=item_id,
            )
        answer = accepted_genre(item)
    if not answer:
        artist = tags.read_tag(candidate.path, "artist") or ""
        title = tags.read_tag(candidate.path, "title") or candidate.path.stem
        hit = searcher(artist, title)
        answer = (hit.genre or "").strip() if hit is not None and hit.genre else ""
    if not answer:
        return _ask(
            store,
            candidate,
            reason=NO_ANSWER,
            proposed="",
            declared=declared,
            handler_key=handler_key,
        )
    if declared.is_too_coarse_as_source(answer):
        return _ask(
            store,
            candidate,
            reason=ANSWER_TOO_COARSE,
            proposed=answer,
            declared=declared,
            handler_key=handler_key,
        )
    tags.write_genre(candidate.path, answer)
    return RetagResult(
        path=candidate.path,
        current=candidate.current,
        written=answer,
        item_id=item_id,
    )


def retag_folder(
    root: Path,
    *,
    searcher: Searcher,
    declared: taxonomy.Taxonomy,
    store: review.ReviewStore | None = None,
    handler_key: str = HANDLER_KEY,
) -> RetagOutcome:
    """Correct every too-coarse genre under ``root`` that can be corrected.

    The selection, the queue read, and :func:`retag_one` per candidate. Every
    policy decision lives one function down, where the job worker reaches it too.
    """
    selection = select(root, declared=declared)
    decided = decided_index(store)
    results = [
        retag_one(
            candidate,
            searcher=searcher,
            declared=declared,
            decided=decided,
            store=store,
            handler_key=handler_key,
        )
        for candidate in selection.candidates
    ]
    return RetagOutcome(results=tuple(results), passed=selection.passed)


# ---------------------------------------------------------------------------
# The database half: plan under the RETAG_GENRE policy, then apply it
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Unmatched:
    """A written file the library could not resolve to exactly one live row."""

    path: str
    outcome: str
    content_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class LibraryPlan:
    """The metadata plan and every written file that never reached a row."""

    plan: metadata.Plan
    unmatched: tuple[Unmatched, ...] = ()


def plan_library(
    outcome: RetagOutcome,
    rows: Iterable[trees.ContentRow],
    mapped: Mapping[str, Any],
    *,
    root: Path | str,
    db: Any,
    prefix_map: Sequence[locations.PrefixRule] = (),
) -> LibraryPlan:
    """Plan the ``GenreID`` write for every file this pass actually retagged.

    THE WRITTEN RESULTS AND NOT THE SELECTION. A plan built from what was proposed
    rather than from what happened is the reporting half of the first-caller defect
    the corpus records: it would name a row for a file whose write was refused, and
    the database would then disagree with the file on disk in the direction nobody
    checks.

    ROWS ARE MATCHED THROUGH :func:`cratekit.write.trees.match_active_rows`, which
    drops tombstones before it compares. ``metadata.plan_genre_retag`` does not
    read the soft-delete marker, and it is right not to: three sibling planners in
    that module take the rows their caller chose. Choosing them is this caller's
    job, and choosing them without reading the marker would retag rows the person
    removed from the collection.

    A file that resolves to no row, to more than one, or to nothing this machine
    can see is SURFACED rather than dropped. The file is already corrected on disk,
    so silence here would report a full sweep over a library half of which never
    moved.

    TWO FILES RESOLVING TO ONE ROW ARE BOTH SURFACED AND NEITHER IS WRITTEN. The
    ambiguity above is one location claimed by two rows; this is its mirror, two
    requested locations resolving onto one row, which a prefix rule can produce
    from two paths that are different on disk. Keying a dictionary on the content
    id and moving on would silently let whichever file came last decide the row,
    and the report would name both as written. That is METHOD's second pattern,
    an identity trusted alone, in the one place this function mints one.
    """
    written = outcome.written
    matches = trees.match_active_rows(
        [result.path for result in written], rows, root=root, prefix_map=prefix_map
    )
    genres: dict[str, str] = {}
    claimed_by: dict[str, str] = {}
    unmatched: list[Unmatched] = []
    contested: set[str] = set()
    for result, match in zip(written, matches, strict=True):
        if match.outcome is not trees.MatchOutcome.MATCHED or match.content_id is None:
            unmatched.append(
                Unmatched(
                    path=str(result.path),
                    outcome=str(match.outcome.value),
                    content_ids=tuple(match.content_ids),
                )
            )
            continue
        content_id = str(match.content_id)
        if content_id in claimed_by:
            contested.add(content_id)
            unmatched.append(
                Unmatched(path=str(result.path), outcome="contested", content_ids=(content_id,))
            )
            continue
        claimed_by[content_id] = str(result.path)
        genres[content_id] = str(result.written)
    for content_id in sorted(contested):
        genres.pop(content_id, None)
        unmatched.append(
            Unmatched(path=claimed_by[content_id], outcome="contested", content_ids=(content_id,))
        )
    wanted = [mapped[content_id] for content_id in genres if content_id in mapped]
    absent = sorted(content_id for content_id in genres if content_id not in mapped)
    plan = metadata.plan_genre_retag(wanted, genres, db=db)
    if absent:
        plan = metadata.Plan(
            plan.owner,
            plan.changes,
            plan.skipped + tuple(metadata.Skipped(cid, "row-absent") for cid in absent),
        )
    return LibraryPlan(plan=plan, unmatched=tuple(unmatched))


def apply_library(library_plan: LibraryPlan, mapped: Mapping[str, Any]) -> metadata.Report:
    """Register the operation, refuse a plan outside its policy, then apply it.

    REGISTERING IS NOT A CONVENIENCE. ``metadata_decision`` answers ``SKIP_UNOWNED``
    for an operation nobody registered, so an unregistered sweep writes nothing,
    raises nothing, and reports a clean run over a library it did not touch. This
    is the first caller of that layer in ``src``, so the registration and the
    refusal that catches its absence are both this function's rather than every
    future caller's to remember.

    DOES NOT COMMIT. ``rb_writer.commit_guarded`` is the caller's, because one
    session carries several operations and is judged once.
    """
    metadata.enable((metadata.RETAG_GENRE,))
    metadata.assert_within_policy(library_plan.plan)
    return metadata.write_plan(library_plan.plan, mapped)


__all__ = [
    "ANSWER_TOO_COARSE",
    "DECLINED_IN_REVIEW",
    "GENRE_SPECIFIC",
    "HANDLER_KEY",
    "KIND",
    "NO_ANSWER",
    "NO_GENRE",
    "Candidate",
    "LibraryPlan",
    "Passed",
    "RetagOutcome",
    "RetagResult",
    "Selection",
    "Unmatched",
    "accepted_genre",
    "apply_library",
    "decided_index",
    "identity_for",
    "options_for",
    "plan_items",
    "plan_library",
    "retag_folder",
    "retag_one",
    "select",
]
