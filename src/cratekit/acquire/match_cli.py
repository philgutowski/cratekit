"""``crate match run``: resolve a list against the library, in three states.

``cratekit.acquire.match`` decides what each track is; this verb owns the
configuration, the review queue and the envelope. Only needs-review becomes a
review item; matched and missing are results, a missing row carrying its
acquisition options. Whether missing should be a review item is open: **Two
briefs disagree about whether a missing track is a review item**. Residuals are
cited by title, since numbers collide across branches. A tombstoned version is
reported as a warning rather than in the arrays (R36).
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from cratekit.acquire import match
from cratekit.cli import output
from cratekit.cli.output import Envelope, PendingHumanAction, load_config
from cratekit.core import config, naming, review
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import ExitCode

#: The one adjudication surface this verb produces.
QUEUE = review.Queue.VERSION_MATCH

#: The decision store R36's tombstones live in; an undeclared key is refused.
TOMBSTONE_STORE = "tombstones"

#: The list document version this verb reads, and refuses any other, so a newer
#: build's file is never read as an empty list.
LIST_VERSION = 1

#: Every key a list document may carry. Anything else is refused, since a
#: misspelled ``tracks`` would otherwise read as an empty list.
LIST_KEYS = frozenset({"list", "origin", "tracks"})

#: The word a settled row is counted under by the verbs that list what a
#: resolve left missing. A missing row has no entry; each verb decides.
SETTLED_WORDS = {
    match.MatchState.MATCHED: "owned", match.MatchState.NEEDS_REVIEW: "offered",
    match.MatchState.SUPPRESSED: "suppressed",
}

#: Warning codes, identifiers a consumer switches on. Not named ``SUPPRESSED``,
#: which is a match state.
SUPPRESSED_WARNING = "acquisition-suppressed"
TOMBSTONE_OVER_OWNED = "tombstone-over-owned"

#: A stored verdict that could not be applied. The item is resolved, so it is
#: absent from the open listing, and only this warning names it.
VERDICT_UNAPPLICABLE = "verdict-unapplicable"

#: An approximate offer that was truncated, so a rejection does not pass for
#: a rejection of everything the library resembles.
CANDIDATES_WITHHELD = "candidates-withheld"

#: A list line that reads two ways, queued as a question and not gating the run.
READING_UNSETTLED = "reading-unsettled"

#: The whys queued as questions that do not make a run PENDING_HUMAN. A reading
#: question is about the list's own spelling (``Sun Path - Live``), common enough
#: that gating would exit 12 on almost every run; it stays NEEDS_REVIEW, offered,
#: and reported on :data:`READING_UNSETTLED`. A stalled why (:data:`match.STALLED`)
#: still gates.
UNGATED: frozenset[match.Why] = frozenset({match.Why.READING_AMBIGUOUS})

#: The verb that shows a person the questions this run left open.
REVIEW_VERB = "review.list"

#: The verb that puts a stalled item back in front of a person, the only
#: escape from a verdict that cannot be applied.
CLEAR_VERB = "review.clear"

#: A URL scheme at the start of an argument, matched against the stripped form a
#: ``Path`` leaves it in, which collapses ``://`` to ``:/``. Two or more
#: characters before the colon, so a Windows drive letter is not a scheme.
_URL_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]+:/")


# ---------------------------------------------------------------------------
# Refusals
# ---------------------------------------------------------------------------


#: What a person does about a list this verb will not read. Steps, not a
#: command, since nothing this product runs repairs a tracklist.
_LIST_STEPS: tuple[str, ...] = (
    "point at a tracklist of 'Artist - Title' lines, or at a list document this "
    "product wrote",
)


def _refuse(message: str, *steps: str, **detail: Any) -> CratekitError:
    """One refusal slug for every unreadable list; what differs rides on the steps."""
    return refuse(
        "intake-list-unusable", message, steps=(*steps, *_LIST_STEPS), scope=Scope.RUN,
        origin=("acquire.match",), detail=detail,
    )


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause."""
    return load_config(("acquire.match",))


# ---------------------------------------------------------------------------
# Reading a list
# ---------------------------------------------------------------------------


def _document_tracks(document: Mapping[str, Any]) -> tuple[match.Wanted, ...]:
    """Recognize a list document field by field, and refuse everything else.

    Positive recognition, since many wrong shapes parse as JSON and would
    otherwise read as a list with no tracks, indistinguishable from all owned.
    """
    unknown = sorted(set(document) - LIST_KEYS)
    if unknown:
        raise _refuse(
            f"this list document carries keys this build does not read: "
            f"{', '.join(unknown)}",
            unknown=unknown,
        )
    version = document.get("list")
    if isinstance(version, bool) or not isinstance(version, int):
        raise _refuse(
            "this document does not declare which list format it is; a document "
            f"this verb reads carries 'list': {LIST_VERSION}",
            declared=repr(version),
        )
    if version != LIST_VERSION:
        raise _refuse(
            f"this list document is format {version} and this build reads "
            f"{LIST_VERSION}; reading it anyway would report a clean match over "
            f"tracks it could not see",
            declared=version, expected=LIST_VERSION,
        )
    origin = document.get("origin", match.TEXT)
    if not isinstance(origin, str) or (origin not in match.READERS and origin != match.TEXT):
        raise _refuse(
            f"{origin!r} is not a list origin this build reads; it reads "
            f"{', '.join(sorted({*match.READERS, match.TEXT}))}",
            origin=repr(origin),
        )
    rows = document.get("tracks")
    if not isinstance(rows, list):
        raise _refuse(
            "this document declares no 'tracks' array; an absent one and an "
            "empty one are different facts and only the second is a list",
            tracks=type(rows).__name__,
        )
    if origin == match.TEXT:
        for position, row in enumerate(rows, start=1):
            if not isinstance(row, str):
                raise _refuse(
                    f"track {position} of a text list is not a line of text", position=position,
                )
        # Row by row, so one array entry is one track. An empty array is allowed
        # here: a document declaring zero tracks has said something.
        try:
            return match.read_text_rows(rows)
        except match.UnreadableList as exc:
            raise _refuse(str(exc), position=exc.line) from exc
    for position, row in enumerate(rows, start=1):
        if not isinstance(row, Mapping):
            raise _refuse(
                f"track {position} of a {origin} list is not a track record", position=position,
            )
    # Each row is recognized too; a mapping alone is not a track record.
    try:
        return match.READERS[origin](rows)
    except match.UnreadableList as exc:
        raise _refuse(str(exc), position=exc.line) from exc


def _text(raw: str) -> tuple[match.Wanted, ...]:
    try:
        return match.read_text_lines(raw)
    except match.UnreadableList as exc:
        raise _refuse(str(exc), line=exc.line) from exc


def read_list(path: Path) -> tuple[match.Wanted, ...]:
    """One list, from a text tracklist or from a list document.

    A URL is refused with its own sentence: fetching belongs to the intake verbs,
    and this verb matches a list somebody already has.
    """
    name = str(path)
    if _URL_SCHEME.match(name.strip()):
        raise _refuse(
            f"{name} is a web address rather than a list on this machine; fetch "
            f"the playlist into a list document first, then match that",
            source=name,
        )
    try:
        # utf-8-sig, so an editor's byte order mark stays out of the first identity.
        raw = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise _refuse(f"{name} could not be read: {exc.strerror}", source=name) from exc
    except ValueError as exc:
        raise _refuse(f"{name} is not readable as text: {exc}", source=name) from exc
    # A leading bracket counts as JSON too, so a top level array is refused
    # rather than read as one track by the line reader.
    if raw.lstrip()[:1] in {"{", "["}:
        try:
            document = json.loads(raw)
        except ValueError as exc:
            raise _refuse(f"{name} is not readable as JSON: {exc}", source=name) from exc
        if not isinstance(document, Mapping):
            raise _refuse(
                f"{name} holds a {type(document).__name__} where a list document "
                f"belongs",
                source=name,
            )
        return _document_tracks(document)
    return _text(raw)


# ---------------------------------------------------------------------------
# Tombstones
# ---------------------------------------------------------------------------


def suppression_view(
    tombstones: review.DecisionStore,
) -> tuple[Callable[[str, Mapping[str, Any]], bool], Callable[..., str]]:
    """One snapshot of what the store suppresses, plus the identifier rule.

    Taken once so a run sees one world, and tested with the store's own
    identifier function so the identity rule has one implementation.
    """
    identify = partial(review.suppression_id_for, tombstones.key)
    live = {record.suppression_id for record in tombstones.suppressions()}

    def suppresses(kind: str, identity: Mapping[str, Any]) -> bool:
        return identify(kind, identity) in live

    return suppresses, identify


# ---------------------------------------------------------------------------
# The queue
# ---------------------------------------------------------------------------


def _options(found: match.TrackMatch) -> tuple[review.Option, ...]:
    """The owned versions a person may say yes to.

    No "none of these" option: that answer is the REJECTED verdict, and one
    answer must not have two representations.
    """
    return tuple(
        review.Option(
            option_id=candidate.candidate_id,
            summary=(
                f"{candidate.artist} / {candidate.title}"
                f"{' [' + candidate.version + ']' if candidate.version else ''}"
                f" ({candidate.difference})"
            ),
            detail=candidate.to_json(),
        )
        for candidate in found.candidates
    )


def _item(items: review.ReviewStore, item_id: str) -> review.Item | None:
    """The stored item, or None when nobody has ever been asked this."""
    return review.find(items, item_id)


def owned_by_a_rule(found: match.TrackMatch) -> bool:
    """Whether resolution owned this row on its own evidence, consulting no
    queue and no person. A matched row under a person's applied acceptance is
    not one, and ``OWNING_RULES`` is the positive list."""
    return found.state is match.MatchState.MATCHED and found.why in match.OWNING_RULES


def touches_the_queue(found: match.TrackMatch) -> bool:
    """Whether ``adjudicate`` has anything to do with this row.

    A question is offered or read back, and a row a rule owns retires an earlier
    question. Every caller gates on this rather than on needs-review alone, or
    the retirement is unreachable from it.
    """
    return found.state is match.MatchState.NEEDS_REVIEW or owned_by_a_rule(found)


def retire_questions(items: review.ReviewStore, found: match.TrackMatch) -> tuple[review.Item, ...]:
    """Supersede every open question about a row resolution now owns.

    Every question shape is asked about, since the retiring side has no why. A
    question a person already answered is left as they left it.
    """
    return review.supersede(
        items,
        tuple(
            review.item_id_for(QUEUE, match.QUESTION_KIND, identity)
            for identity in found.wanted.questions()
        ),
        rule=str(found.why),
    )


def adjudicate(
    items: review.ReviewStore, result: match.MatchResult, *, handler_key: str,
    suppresses: Callable[[str, Mapping[str, Any]], bool], suppression_id: Callable[..., str],
) -> match.MatchResult:
    """Turn the needs-review state into queue items, and read back the answers.

    Matched and missing pass through as results (R12). The match's own tombstone
    snapshot is passed in, since a rejection reaches missing here and must see
    the same world.
    """
    settled: list[match.TrackMatch] = []
    for found in result.matches:
        if owned_by_a_rule(found):
            # A rule owns this row, so an earlier question about it is retired,
            # naming the rule. See the residual "A review item outlives its
            # question: a later resolution that owns the row leaves the
            # version-match item open, and no verdict or predicate can retire it
            # honestly".
            retire_questions(items, found)
            settled.append(found)
            continue
        if found.state is not match.MatchState.NEEDS_REVIEW:
            settled.append(found)
            continue
        # The question's identity, not the tombstone's: a review item answers
        # what was asked, which for two whys is about the key.
        identity = found.question_identity
        held = _item(items, review.item_id_for(QUEUE, match.QUESTION_KIND, identity))
        if held is not None and held.verdict is review.Verdict.SUPERSEDED:
            # The rule that retired this question no longer owns the row, so the
            # machine's verdict is cleared and re-offered; left standing it would
            # read as a rejection nobody made.
            held = review.clear(items, held.item_id, actor=handler_key)
        if held is None or not held.resolved:
            held = review.offer(
                items, queue=QUEUE, kind=match.QUESTION_KIND, identity=identity,
                payload=found.to_json(), options=_options(found), handler_key=handler_key,
            )
        # Only a person's verdict is an answer; anything else reads as None and
        # leaves the track a question.
        titles = {one.option_id: (one.detail or {}).get("title") for one in held.options}
        accepted = (
            None
            if held.verdict not in review.PERSON_VERDICTS
            else held.verdict is review.Verdict.ACCEPTED
        )
        settled.append(
            match.apply_verdict(
                found,
                accepted=accepted,
                # An older answer's identifier is carried to its file by title.
                option=(
                    None if held.option is None
                    else match.current_option(found, held.option, titles.get(held.option))
                ),
                # The candidates on screen when the person answered, so an
                # unspecific yes binds to what they saw.
                offered=tuple(
                    match.current_option(found, one.option_id, titles.get(one.option_id))
                    for one in held.options
                ),
                item_id=held.item_id,
                suppresses=suppresses,
                suppression_id=suppression_id,
            )
        )
    return match.MatchResult(matches=tuple(settled))


# ---------------------------------------------------------------------------
# The verb
# ---------------------------------------------------------------------------


def build(parser: argparse.ArgumentParser, entry: Any) -> None:
    """Declare the command line. ``entry`` is untyped (KTD23): naming it would be
    an upward import from the modules layer to the CLI layer."""
    parser.add_argument("list", help="a tracklist of 'Artist - Title' lines, or a list document")
    parser.set_defaults(_handler=match_list)


def _warnings(
    result: match.MatchResult, *, suppresses: Callable[[str, Mapping[str, Any]], bool],
    identify: Callable[..., str],
) -> tuple[dict[str, str], ...]:
    """What the three arrays cannot say, on the warning channel (R36). Every
    value is text."""
    found: list[dict[str, str]] = []
    for track in result.suppressed:
        found.append(
            {
                "code": SUPPRESSED_WARNING,
                "message": (
                    f"{track.wanted.artist} / {track.wanted.title} is suppressed by "
                    f"a tombstone and was not counted missing"
                ),
                "suppression": track.suppression_id or "", "match": track.match_id, "item": "",
                "remedy": "",
            }
        )
    # A tombstone that did not suppress is still reported: over a held file it is
    # stale, over a question it still stands and acquisition must skip it.
    seen: set[tuple[str, str]] = set()
    for state in match.PAYLOAD_STATES:
        for track in result.of(state):
            # Asked under every spelling the suppression itself is asked under.
            held = state is match.MatchState.MATCHED
            standing = match.standing_tombstone(
                track.wanted,
                suppresses=suppresses,
                suppression_id=identify,
                # A held file cannot call a companion stale.
                companions=not held,
            )
            if standing is None or (track.match_id, standing) in seen:
                continue
            seen.add((track.match_id, standing))
            found.append(
                {
                    "code": TOMBSTONE_OVER_OWNED if held else SUPPRESSED_WARNING,
                    "message": (
                        f"{track.wanted.artist} / {track.wanted.title} is held on "
                        f"disk and a tombstone stands over it; the disk is the "
                        f"truth and the tombstone is stale"
                        if held
                        else f"a tombstone stands over "
                        f"{track.wanted.artist} / {track.wanted.title}, which "
                        f"resolved to {state} rather than being suppressed; "
                        f"acquisition must skip it whatever this row says"
                    ),
                    "suppression": standing, "match": track.match_id, "item": track.item_id or "",
                    "remedy": "",
                }
            )
    # A tombstone over an offered candidate, a version the list did not spell, is
    # stale in every state, since the candidate was read off the disk. The pair
    # (row, suppression) dedupes against the loop above.
    for track in result.matches:
        for candidate in track.candidates:
            offered = match.Wanted(
                artist=candidate.artist, title=candidate.title, version=candidate.version,
            )
            standing = match.standing_tombstone(
                offered, suppresses=suppresses, suppression_id=identify
            )
            if standing is None or (track.match_id, standing) in seen:
                continue
            seen.add((track.match_id, standing))
            found.append(
                {
                    "code": TOMBSTONE_OVER_OWNED,
                    "message": (
                        f"{track.wanted.artist} / {track.wanted.title} is offered "
                        f"the held file {candidate.artist} / {offered.listed} as "
                        f"an answer, and a tombstone stands over that file; the "
                        f"disk is the truth and the tombstone is stale"
                    ),
                    "suppression": standing, "match": track.match_id, "item": track.item_id or "",
                    "remedy": "",
                }
            )
    named: set[str] = set()
    for track in result.of(match.MatchState.NEEDS_REVIEW):
        if track.why not in match.STALLED:
            continue
        # One warning per item, since two rows can resolve to one question.
        if track.item_id and track.item_id in named:
            continue
        named.add(track.item_id or "")
        found.append(
            {
                "code": VERDICT_UNAPPLICABLE,
                "message": (
                    f"{track.wanted.artist} / {track.wanted.title} carries a "
                    f"recorded verdict this run could not apply ({track.why}); the "
                    f"item stays resolved, so it is not in the open queue and "
                    f"cannot be resolved again"
                ),
                "suppression": "", "match": track.match_id, "item": track.item_id or "",
                "remedy": CLEAR_VERB,
            }
        )
    # The questions that do not gate, said out loud, one per item, since this is
    # all that stands between an exit zero and R11's silence.
    asked: set[str] = set()
    for track in result.of(match.MatchState.NEEDS_REVIEW):
        if track.why not in UNGATED:
            continue
        marker = track.item_id or track.match_id
        if marker in asked:
            continue
        asked.add(marker)
        found.append(
            {
                "code": READING_UNSETTLED,
                "message": (
                    f"{track.wanted.artist} / {track.wanted.title} reads two ways "
                    f"and this library holds the other one; it is queued as a "
                    f"question rather than counted owned, and the run was not "
                    f"blocked on it"
                ),
                "suppression": "", "match": track.match_id, "item": track.item_id or "",
                "remedy": REVIEW_VERB,
            }
        )
    # Every state, since the run that acquires is the one after the rejection.
    for track in result.matches:
        if not track.withheld:
            continue
        found.append(
            {
                "code": CANDIDATES_WITHHELD,
                "message": (
                    f"{track.wanted.artist} / {track.wanted.title} resembles more "
                    f"of this library than one offer can hold; "
                    f"{track.withheld} further candidates were never shown, so "
                    f"any answer here answers only what was, and this row "
                    f"resolved to {track.state}"
                ),
                "suppression": "", "match": track.match_id, "item": track.item_id or "",
                "remedy": "",
            }
        )
    return tuple(found)


def _pending(result: match.MatchResult, *, run_id: str) -> PendingHumanAction | None:
    """The outstanding questions, as a state rather than as a printed sentence.

    A run with open version questions must not exit zero (R11). Nothing goes in
    ``blocks``: an open question stops nobody working. An answerable question is
    in the open queue; a stalled one carries a verdict this run could not apply,
    is resolved and absent from the listing, and is only cleared, so the verb
    named is the one that can act and each stalled item gets its own step.
    Counted by question, not by row, throughout. :data:`UNGATED` questions are
    left out of the gate but counted in the sentence and named in a step, since
    the summary is what a caller reads.
    """
    open_questions = [
        found
        for found in result.of(match.MatchState.NEEDS_REVIEW)
        if found.why not in UNGATED
    ]
    ungated = {
        found.item_id or found.match_id
        for found in result.of(match.MatchState.NEEDS_REVIEW)
        if found.why in UNGATED
    }
    if not open_questions:
        return None
    stalled = sorted(
        {found.item_id for found in open_questions if found.why in match.STALLED and found.item_id}
    )
    answerable = {
        found.item_id or found.match_id
        for found in open_questions
        if found.why not in match.STALLED
    }
    questions = {found.item_id or found.match_id for found in open_questions}
    steps: list[str] = []
    if answerable:
        steps.append("list the version-match queue and record a verdict on each item")
        steps.append(
            "accept a candidate to call it the same record, or reject to acquire "
            "the version the list asked for"
        )
    if stalled:
        steps.append(
            f"{len(stalled)} of these carry a verdict this run could not apply, so "
            f"they are resolved, invisible to the open listing, and refused by "
            f"review resolve; clear each one to put it back in front of a person"
        )
        # One step per item, each a command that runs: the verb takes one id.
        steps.extend(f"crate review clear {item_id}" for item_id in stalled)
    if ungated:
        steps.append(
            f"{len(ungated)} further questions are queued and did not block this "
            f"run, because this list spells a version after a dash and no rule "
            f"over that string decides it; they are answered the same way"
        )
    return PendingHumanAction(
        kind="review", id=output.new_pending_id(run_id),
        summary=(
            f"{len(questions)} tracks resolved to a version this library does "
            f"not hold under that name, and need a person"
            + (
                f"; {len(stalled)} of them carry a verdict that could not be "
                f"applied and have to be cleared first"
                if stalled
                else ""
            )
            + (
                f"; {len(ungated)} further questions are queued and did not "
                f"block this run, for {len(questions) + len(ungated)} outstanding "
                f"in all"
                if ungated
                else ""
            )
        ),
        verify_verb=REVIEW_VERB if answerable else CLEAR_VERB, steps=tuple(steps),
    )


def library_template(cfg: config.Config) -> naming.NameTemplate:
    """The shape the library's own filenames are written in, the marker with it."""
    return naming.NameTemplate.lossy_if_marked(cfg.naming.lossy_marker)


def library_view(cfg: config.Config) -> tuple[match.LibraryIndex, Callable[..., bool], Callable[..., str]]:
    """The library as the match engine sees it: the index, and the tombstone view.

    One builder for every caller. The tombstone snapshot comes before the library
    walk, so an unreadable store refuses before a long scan.
    """
    suppresses, identify = suppression_view(review.DecisionStore(TOMBSTONE_STORE, cfg))
    index = match.index_library(
        cfg.library.root / cfg.library.music_dir, template=library_template(cfg)
    )
    return index, suppresses, identify


@dataclass(frozen=True, slots=True)
class ListResolved:
    """One list resolved against the library, with what the envelope carries."""

    result: match.MatchResult
    pending: PendingHumanAction | None
    warnings: tuple[dict[str, str], ...]


def resolve_list(
    cfg: config.Config, wanted: Sequence[match.Wanted], *, handler_key: str, run_id: str,
) -> ListResolved:
    """Resolve ``wanted`` against the library and offer what needs a person.

    The one implementation shared with ``intake identify``, so the two never
    disagree about what the library holds.
    """
    index, suppresses, identify = library_view(cfg)
    result = match.resolve_all(wanted, index, suppresses=suppresses, suppression_id=identify)
    with review.open_store(cfg) as items:
        result = adjudicate(
            items, result, handler_key=handler_key, suppresses=suppresses, suppression_id=identify,
        )
    return ListResolved(
        result=result, pending=_pending(result, run_id=run_id),
        warnings=_warnings(result, suppresses=suppresses, identify=identify),
    )


def match_list(ctx: Any) -> Envelope:
    """The handler. Not called ``run``, which is the dispatcher's name."""
    cfg = _load()
    wanted = read_list(Path(ctx.args.list))
    resolved = resolve_list(cfg, wanted, handler_key=ctx.entry.handler_key, run_id=ctx.run.run_id)
    pending = resolved.pending
    return ctx.envelope(
        data=resolved.result.payload(),
        outcome=Outcome.PENDING if pending is not None else Outcome.OK,
        code=ExitCode.PENDING_HUMAN if pending is not None else ExitCode.OK, pending=pending,
        warnings=resolved.warnings,
    )


__all__ = [
    "CANDIDATES_WITHHELD", "CLEAR_VERB", "LIST_KEYS", "LIST_VERSION", "ListResolved", "QUEUE",
    "SETTLED_WORDS", "READING_UNSETTLED", "REVIEW_VERB", "SUPPRESSED_WARNING",
    "TOMBSTONE_OVER_OWNED", "TOMBSTONE_STORE", "UNGATED", "VERDICT_UNAPPLICABLE", "adjudicate",
    "build", "library_template", "library_view", "match_list", "read_list", "resolve_list",
    "suppression_view",
]
