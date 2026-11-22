"""Correct a genre that is already wrong (U40, Feature Inventory row 18).

A SECOND VERB, NOT A FLAG: ``tag folder`` fills if empty, this one corrects.
The selection is the taxonomy's own ``is_too_coarse_as_source``, never a list
here (R19); A BLANK GENRE IS NOT SELECTED, being ``tag folder``'s, and AN ANSWER
ITSELF TOO COARSE IS REFUSED. A decline is a question: ONE GENRE review item
per file, offered once. :func:`apply_library` registers the ``RETAG_GENRE``
policy, since an unregistered one skips every change; its one caller is
``cratekit.tagging.rows``, and :func:`plan_library` has none (R-185, R-246).

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
from cratekit.tagging import titles
from cratekit.tagging.tag import Searcher
from cratekit.write import metadata, trees

#: The producing verb, carried onto every review item as a VALUE, so this module
#: never names the CLI layer.
HANDLER_KEY = "tag.retag"

#: ONE kind for BOTH unanswered shapes, which are two reasons for one question;
#: two kinds would ask it twice under two item identifiers.
KIND = "coarse-genre"

#: Why a file was passed over during selection.
NO_GENRE = "no-genre"
GENRE_SPECIFIC = "genre-specific"

#: Why a selected file was not written.
NO_ANSWER = "no-answer"
ANSWER_TOO_COARSE = "answer-too-coarse"
DECLINED_IN_REVIEW = "declined-in-review"

#: The file would not take the answer, ``tags.write_genre`` answering False
#: (R-1103). Also the refusal's slug, so the reason and the cause are one name.
UNWRITTEN_REASON = "tag-retag-unwritten"


@dataclass(frozen=True, slots=True)
class Candidate:
    """One file this pass may correct, and the value it currently carries."""

    path: Path
    current: str


@dataclass(frozen=True, slots=True)
class Passed:
    """One file the selection did not take, and why. Surfaced, since "nothing
    selected" and "nothing looked at" are different answers."""

    path: Path
    reason: str


@dataclass(frozen=True, slots=True)
class Selection:
    """What one walk of a folder decided about every audio file under it."""

    candidates: tuple[Candidate, ...] = ()
    passed: tuple[Passed, ...] = ()


@dataclass(frozen=True, slots=True)
class RetagResult:
    """What happened to one candidate. ``written`` is the genre now on the file,
    or None; ``reason`` is empty exactly when it is set."""

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
        """Results that put a question in the review queue on THIS run, told by
        the reason, since a file a verdict settled carries an item id too."""
        return tuple(
            result
            for result in self.results
            if result.item_id and result.reason in {NO_ANSWER, ANSWER_TOO_COARSE}
        )


def select(root: Path, *, declared: taxonomy.Taxonomy) -> Selection:
    """Every audio file under ``root`` whose genre is too coarse to be final,
    sorted so a plan's digest is stable across two runs."""
    candidates: list[Candidate] = []
    passed: list[Passed] = []
    if not root.is_dir():
        return Selection()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in AUDIO_EXTS:
            continue
        # NOT STRIPPED HERE: ``tags.read_tag`` already trims every value.
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


def identity_for(path: Path | str) -> dict[str, str]:
    """What a review item about one file is addressed by: THE PATH, so a library
    that moves orphans every open item. A bare file carries no better identifier,
    and this runs before any row is matched, so a folder with no rows is corrected."""
    return {"path": str(path)}


def options_for(declared: taxonomy.Taxonomy) -> tuple[review.Option, ...]:
    """The declared buckets, the only answers a person may give, since
    ``review.resolve`` refuses an option not offered. Too coarse ones are left out
    here as well as refused at the write, for items an older build offered."""
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
    """The genre a resolved item settled on, or empty, read off the chosen
    OPTION: its id is a bucket identifier and the genre its display name (R19)."""
    if item.verdict is not review.Verdict.ACCEPTED or not item.option:
        return ""
    for option in item.options:
        if option.option_id != item.option:
            continue
        detail = option.detail or {}
        return str(detail.get("genre") or option.summary or "").strip()
    return ""


def decided_index(store: review.ReviewStore | None) -> dict[str, review.Item]:
    """Every item this pass has ever offered, read ONCE rather than per file.
    Public for the job worker, which reads this small queue once per item."""
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
    """Put the question in the queue and report the file as unwritten; with no
    store the result still carries the reason."""
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

    The per candidate work, shared by :func:`retag_folder` and the job worker so
    they hold one policy. A VERDICT ALREADY RECORDED IS READ BEFORE THE SEARCHER
    IS ASKED, so an answered question is not looked up again; a REJECTED one
    leaves the file alone and offers nothing. ``decided`` is read once by the
    caller.
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
        # A NAME IS READ PAST THE OLDER NAMING'S TAIL (R-1724), as ``tag
        # folder`` reads the title of one; its artist is not read (R-1727).
        title = tags.read_tag(candidate.path, "title") or titles.name_title(candidate.path.stem)
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
    if not tags.write_genre(candidate.path, answer):
        # THE WRITER'S FALSE IS AN UNWRITTEN FILE, NEVER A CORRECTION (R-1103).
        # ``written`` stays None, so :attr:`RetagOutcome.written` leaves the file
        # out and :func:`plan_library` plans no row for it, and the answer it
        # could not take rides as ``proposed`` so the report can name it. A
        # verdict the answer came from stays as it is: the next run reads it
        # again and tries the write again, rather than asking a person twice.
        return RetagResult(
            path=candidate.path,
            current=candidate.current,
            reason=UNWRITTEN_REASON,
            proposed=answer,
            item_id=item_id,
        )
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
    """Correct every too coarse genre under ``root`` that can be corrected: the
    selection, one queue read, and :func:`retag_one` per candidate."""
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

    THE WRITTEN RESULTS, NOT THE SELECTION, so no row is planned for a refused
    write. Rows are matched through :func:`cratekit.write.trees.match_active_rows`,
    which drops tombstones. A file resolving to no row, to several, or to nothing
    visible is SURFACED, and TWO FILES RESOLVING TO ONE ROW are both surfaced and
    neither written, rather than letting the last decide.
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

    An unregistered operation answers ``SKIP_UNOWNED``, writing nothing and
    reporting clean. DOES NOT COMMIT: one session is judged once, by the caller.
    """
    metadata.enable((metadata.RETAG_GENRE,))
    metadata.assert_within_policy(library_plan.plan)
    return metadata.write_plan(library_plan.plan, mapped)


__all__ = [
    "ANSWER_TOO_COARSE", "DECLINED_IN_REVIEW", "GENRE_SPECIFIC", "HANDLER_KEY", "KIND", "NO_ANSWER",
    "NO_GENRE", "UNWRITTEN_REASON", "Candidate", "LibraryPlan", "Passed", "RetagOutcome",
    "RetagResult", "Selection", "Unmatched", "accepted_genre", "apply_library", "decided_index",
    "identity_for", "options_for", "plan_items", "plan_library", "retag_folder", "retag_one",
    "select",
]
