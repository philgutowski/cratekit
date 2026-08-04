"""``crate match run``: resolve a list against the library, in three states.

The verb is thin on purpose. ``cratekit.acquire.match`` decides what each track
is; this file is where the decision meets persistence, and it owns exactly three
things the engine must not: configuration, the review queue, and the envelope.

**THE SPLIT U11 SETTLED, IMPLEMENTED HERE.** R11 has three states and only one
of them is a question. The needs-review state becomes a persisted review item in
the version-match queue; matched and missing are results, and neither ever
reaches the queue.

**THE JUSTIFICATION THAT USED TO BE HERE WAS FALSE, and deleting it is part of
the record.** It argued that queueing a missing row would ask a person to confirm
the same track once per run forever. It would not: ``review.offer`` is
idempotent, so the same identity finds the same item, keeps its verdict, and
writes no second row. A review proved that against the real store. What is
actually true is narrower and is a matter of authority rather than mechanics.
Issue #16 says twice that missing items become review items with acquisition
options, and plan line 271 AE11 agrees; U11 declared matched and missing as
OUTPUTS and registered a countdown against this unit for that reading. Two
briefs disagree, the disagreement is a product decision, and it belongs to
Phillip rather than to whoever writes this file. It is recorded in
``docs/residual-findings.md`` under the title **Two briefs disagree about
whether a missing track is a review item** and needs its own issue.

**EVERY RESIDUAL THIS UNIT CITES IS CITED BY TITLE.** Six residual numbers are
claimed by two branches at once with different content on each side, so a
citation by number points at a different subject the moment either side
renumbers, and that has already caused one silent break on this wave.
``test_every_residual_this_unit_cites_is_a_heading_that_exists`` checks each
cited title against the headings in that file, so a citation that stops
resolving fails a test rather than reading plausibly.

What this file owes either way is that the sentence it prints be true. A missing
row now genuinely carries its acquisition options as DATA in the match result,
under ``acquisition``, where the next verb reads them. It used to carry an empty
candidate list, an empty path list, and nothing else, while the docstring claimed
otherwise.

**ONE CLASS OF QUESTION IS QUEUED WITHOUT GATING THE RUN**, which is a product
decision and is argued at ``UNGATED``. A list line whose dash tail is a bare
one-word qualifier reads two ways and no rule over the string decides it, so it
becomes a question; but ``- Edit``, ``- Mix`` and ``- Live`` are three of the
commonest spellings a public playlist ships, and gating on them exits 12 on
almost every run of almost every list. The row stays in ``needs_review``, the
item stays answerable, the warning channel says so, and the caller's pipeline is
not stopped by an ambiguity in somebody else's spelling.

**WHY THE QUEUE IS READ BEFORE IT IS WRITTEN.** An item that already carries a
verdict is not offered again. ``offer`` is idempotent and would leave a resolved
item alone anyway, so this is not about correctness of the store; it is about
the sentence being literally true. A run whose every question was answered last
week writes nothing to the queue at all.

**THE SUPPRESSED CHANNEL.** A tombstoned version appears in none of the three
arrays and is reported as a warning naming its suppression identifier, so it is
skipped by anything reading ``missing`` to decide what to acquire, and is still
visible and revocable (R36). The reverse disagreement is reported too: a
tombstone standing over a version the library actually holds is a stale record,
and saying so is cheaper than letting somebody discover it during a deletion.
"""

from __future__ import annotations

import argparse
import json
import re
from functools import partial
from pathlib import Path
from typing import Any, Callable, Mapping

from cratekit.acquire import match
from cratekit.cli import output
from cratekit.cli.output import Envelope, PendingHumanAction
from cratekit.core import config, naming, review
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy

#: The one adjudication surface this verb produces. Assigned once at module
#: scope so the offer below reads as one idea rather than as a queue name typed
#: at a call site, which is how a producer ends up inventing a second surface.
QUEUE = review.Queue.VERSION_MATCH

#: The decision store R36's tombstones live in. A declared inventory key, and
#: the store refuses an undeclared one by name, so a typo here fails loudly
#: rather than writing a file nobody chose a root for.
TOMBSTONE_STORE = "tombstones"

#: The version of the list document this verb reads AND the version it refuses
#: anything else at. Reading a document without checking its version is how a
#: newer build's file is read as an empty list and the run reports a clean
#: match over nothing.
LIST_VERSION = 1

#: Every key a list document may carry. Anything else is refused rather than
#: ignored: a misspelled ``tracks`` would otherwise parse as a valid document
#: holding no tracks, and an empty list and a typo look identical afterwards.
LIST_KEYS = frozenset({"list", "origin", "tracks"})

#: Warning codes this verb emits. Identifiers a consumer can switch on, never
#: sentences.
#:
#: NOT called ``SUPPRESSED``. ``match.MatchState.SUPPRESSED`` is a state and this
#: is a warning code, and one name meaning two things in two modules of one unit
#: is a defect no passing test can see.
SUPPRESSED_WARNING = "acquisition-suppressed"
TOMBSTONE_OVER_OWNED = "tombstone-over-owned"

#: A stored verdict that could not be applied, on the channel that can carry the
#: item identifier. Without it the only sign is an exit status: the item is
#: RESOLVED in the queue, so a listing of open items shows nothing and resolving
#: it again is refused, and a caller reading the exit code and then the verify
#: verb is told "blocked" and "nothing to do" in the same breath.
VERDICT_UNAPPLICABLE = "verdict-unapplicable"

#: An approximate offer that was truncated. A silently truncated offer looks
#: exactly like an offer of everything the library resembles, so a person who
#: rejects it has rejected answers they were never shown, and the run then
#: acquires a track the library already holds, which is what the approximate pass
#: exists to prevent.
CANDIDATES_WITHHELD = "candidates-withheld"

#: A list line this module could not read one way, queued as a question and NOT
#: gating the run. See :data:`UNGATED` for the whole argument.
READING_UNSETTLED = "reading-unsettled"

#: The whys that are queued as questions but do not by themselves make a run
#: PENDING_HUMAN. Exactly one, and the reason it is not simply "every question"
#: is the point.
#:
#: A key question and a version question are about the LIBRARY: the person holds
#: a different record from the one the list names, and until somebody says
#: whether it is the same record, this run genuinely cannot say what is owned. A
#: READING question is about the LIST'S OWN SPELLING. ``Sun Path - Live`` is
#: either a live cut of "Sun Path" or a record called "Sun Path - Live", no rule
#: over the string decides it, and ``- Edit``, ``- Mix`` and ``- Live`` are three
#: of the commonest spellings a public playlist ships. Gating on them costs a
#: measured 14 of 68 cells in the library-state table, all in one direction, so a
#: 40,000 track library run against public playlists exits 12 on almost every
#: run: a gate that fires every time is a gate nobody reads, and a queue nobody
#: empties is worse than the wrong guess this class exists to avoid making.
#:
#: WHAT IS NOT GIVEN UP. The row is still NEEDS_REVIEW, so nothing counts it
#: owned and nothing acquires it; the item is still offered, so the question is
#: still answerable and the answer still persists; and the run still says so out
#: loud on :data:`READING_UNSETTLED`. R11's silence is a question nobody is told
#: about, not a question that did not stop the pipeline. A row of this class that
#: later carries a verdict this build cannot apply leaves this set on its own,
#: because ``apply_verdict`` rewrites the why into one of :data:`match.STALLED`,
#: and those gate: a stalled item is invisible to the open listing and needs an
#: act nobody will perform unless told.
UNGATED: frozenset[match.Why] = frozenset({match.Why.READING_AMBIGUOUS})

#: The verb that shows a person the questions this run left open.
REVIEW_VERB = "review.list"

#: The verb that puts a stalled item back in front of a person. Named because it
#: is the ONLY escape from a verdict that cannot be applied, and a pending action
#: naming a remedy nobody can execute is the printed instruction this field
#: exists to replace.
CLEAR_VERB = "review.clear"

#: A URL scheme at the start of an argument, matched against the form a path
#: leaves it in. ``Path`` COLLAPSES the double slash, so "https://host/x" is
#: "https:/host/x" by the time it is text again and a check for "://" finds
#: nothing. That is how a web address arrives as "no such file or directory".
#: Two or more characters before the colon, so a Windows drive letter is not a
#: scheme. Matched against a STRIPPED name: a leading space survives a copy and
#: paste, is legal in a filename and therefore cannot be refused on its own, and
#: anchoring at the first character sent " https://host/x" back out as "no such
#: file or directory", which is the exact failure this pattern exists to stop.
_URL_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]+:/")


# ---------------------------------------------------------------------------
# Refusals
# ---------------------------------------------------------------------------


#: What a person does about a list this verb will not read. Carried as steps
#: rather than as a token because the fix is not a command: nothing this product
#: runs repairs somebody's tracklist, and rendering a command here would send
#: them to a verb that cannot help.
_LIST_STEPS: tuple[str, ...] = (
    "point at a tracklist of 'Artist - Title' lines, or at a list document this "
    "product wrote",
)


def _refuse(message: str, *steps: str, **detail: Any) -> CratekitError:
    """One refusal for every way a list is not a list this verb can read.

    One slug, in the same shape the configuration layer uses for five ways a
    config can be unusable: what differs between them is what a person does
    next, and that travels on the steps rather than on the code.
    """
    return refuse(
        "intake-list-unusable",
        message,
        steps=(*steps, *_LIST_STEPS),
        scope=Scope.RUN,
        origin=("acquire.match",),
        detail=detail,
    )


def _load() -> config.Config:
    """Read config, carrying the configuration failure's own remedy through."""
    try:
        return config.load()
    except config.ConfigError as exc:
        raise refuse(
            "config-unusable",
            str(exc),
            remedy=Remedy(str(exc.remedy)),
            origin=("acquire.match",),
            detail={"kind": type(exc).__name__},
        ) from exc


# ---------------------------------------------------------------------------
# Reading a list
# ---------------------------------------------------------------------------


def _document_tracks(document: Mapping[str, Any]) -> tuple[match.Wanted, ...]:
    """Recognize a list document field by field, and refuse everything else.

    POSITIVE RECOGNITION, not "did the parse raise". A top level array, a bare
    number, a null ``tracks``, or rows under a key a newer build introduced all
    parse as JSON perfectly well, and a reader that only catches a decoding
    error reads every one of them as a list with no tracks. The match then
    reports nothing missing and nothing to review, which is indistinguishable
    from a list that was genuinely all owned.
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
            declared=version,
            expected=LIST_VERSION,
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
                    f"track {position} of a text list is not a line of text",
                    position=position,
                )
        # ROW BY ROW rather than joined and re-split. Joining made a refusal cite
        # a line number in a string nobody has, let a row carrying a newline
        # become two tracks, and stopped the array's length being the number of
        # tracks read. An explicitly empty array is allowed here and refused on
        # the plain-text path, because a document that declares zero tracks has
        # said something and a file with no readable line in it has not.
        try:
            return match.read_text_rows(rows)
        except match.UnreadableList as exc:
            raise _refuse(str(exc), position=exc.line) from exc
    for position, row in enumerate(rows, start=1):
        if not isinstance(row, Mapping):
            raise _refuse(
                f"track {position} of a {origin} list is not a track record",
                position=position,
            )
    # POSITIVE RECOGNITION OF THE ROW ITSELF, not only of its container. A
    # mapping is not a track record: two rows carrying nothing but an identifier
    # used to fold to one match identifier, and an anonymous row resolved
    # "matched" against any file in the library whose name folded to nothing.
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

    A URL is refused with its own sentence rather than as an unreadable file.
    Fetching a playlist needs a provider session and pagination, both of which
    belong to the intake verbs; this verb matches a list somebody already has,
    which is what keeps the whole unit provable without an account.
    """
    name = str(path)
    if _URL_SCHEME.match(name.strip()):
        raise _refuse(
            f"{name} is a web address rather than a list on this machine; fetch "
            f"the playlist into a list document first, then match that",
            source=name,
        )
    try:
        # utf-8-sig, so a byte order mark left by an editor comes off the first
        # artist's name rather than travelling into the identity it is hashed
        # into. Folding happens to remove it too, and relying on that would be
        # relying on a coincidence in a function that exists for another reason.
        raw = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise _refuse(f"{name} could not be read: {exc.strerror}", source=name) from exc
    except ValueError as exc:
        raise _refuse(f"{name} is not readable as text: {exc}", source=name) from exc
    # A LEADING BRACKET COUNTS AS JSON, not only a leading brace. A top level
    # array falls through to the line reader otherwise, and ``["Artist - Title"]``
    # splits on the separator perfectly happily, so a JSON document of the wrong
    # shape is read as one track with punctuation in its name. That is the same
    # defect as reading a wrong document as an empty one, wearing a different hat.
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

    The store answers ``suppresses`` by reading its whole document, which is
    right for a caller asking once and wrong for a caller asking per track in a
    three hundred track list. The snapshot is taken once so a run sees one
    consistent world, and membership is tested against identifiers built by the
    store's OWN identifier function, so there is no second implementation of the
    identity rule to drift from the first.
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

    There is deliberately no "none of these" option. Saying no to every
    candidate is a REJECTED verdict, which the queue already models and which
    suppresses the item until somebody clears it; an option meaning the same
    thing would give one answer two representations and the store would have to
    guess which one a later reader meant.
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
    try:
        return review.get(items, item_id)
    except CratekitError as exc:
        if exc.cause.reason == "review-item-unknown":
            return None
        raise


def adjudicate(
    items: review.ReviewStore,
    result: match.MatchResult,
    *,
    handler_key: str,
    suppresses: Callable[[str, Mapping[str, Any]], bool],
    suppression_id: Callable[..., str],
) -> match.MatchResult:
    """Turn the needs-review state into queue items, and read back the answers.

    Matched and missing pass through untouched. They are results, and a result
    pushed into the queue asks a person to confirm an answer (R12, and the split
    U11 recorded when it declared these surfaces).

    The tombstone view is threaded through because a REJECTION reaches "missing"
    by a road resolution never walks, and the row it produces is the one that
    tells acquisition what to go and get. Passing the same snapshot the match
    used, rather than re-reading the store, is what keeps one run seeing one
    world.
    """
    settled: list[match.TrackMatch] = []
    for found in result.matches:
        if found.state is not match.MatchState.NEEDS_REVIEW:
            settled.append(found)
            continue
        # THE QUESTION'S identity, not the tombstone's. They address different
        # things and they are two functions for that reason: a tombstone is a
        # fact about a version that outlives every list, and a review item is the
        # answer to something somebody was asked, which for two of these whys is
        # a question about the key.
        identity = found.question_identity
        held = _item(items, review.item_id_for(QUEUE, match.QUESTION_KIND, identity))
        if held is None or not held.resolved:
            held = review.offer(
                items,
                queue=QUEUE,
                kind=match.QUESTION_KIND,
                identity=identity,
                payload=found.to_json(),
                options=_options(found),
                handler_key=handler_key,
            )
        # THREE ANSWERS. A verdict this build cannot read coerces to None, which
        # leaves the track a question rather than freezing it into a state
        # nobody can reach to correct.
        accepted = (
            None if held.verdict is None else held.verdict is review.Verdict.ACCEPTED
        )
        settled.append(
            match.apply_verdict(
                found,
                accepted=accepted,
                option=held.option,
                # WHAT THE ANSWER WAS ABOUT. The store keeps the options an item
                # was offered with and ``offer`` leaves a RESOLVED item's row
                # alone, so this is the candidate list that was on the screen
                # when somebody answered, not the one this run just built. An
                # unspecific yes is bound to it, which is the only thing that
                # tells "yes, that copy" apart from "yes, whatever you hold now".
                offered=tuple(one.option_id for one in held.options),
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
    """Declare the command line. ``entry`` is untyped, and that is KTD23.

    A verb whose module lives in the acquisition package sits at the modules
    layer, and the registry that defines ``Entry`` sits at the CLI layer above
    it. Naming the type would be an upward import, including under
    ``TYPE_CHECKING``, which the layering guard reads because a lazy import is
    exactly the shape it exists to catch. The verbs that DO name it are the ones
    that live in the CLI package.
    """
    parser.add_argument(
        "list",
        help="a tracklist of 'Artist - Title' lines, or a list document",
    )
    parser.set_defaults(_handler=match_list)


def _warnings(
    result: match.MatchResult,
    *,
    suppresses: Callable[[str, Mapping[str, Any]], bool],
    identify: Callable[..., str],
) -> tuple[dict[str, str], ...]:
    """What the three arrays cannot say, said on the envelope's own channel.

    R36 requires the suppression to be REPORTED rather than omitted silently,
    and the payload surface is closed at three arrays. Every value is text
    because a warning is declared as a mapping of text and a consumer reading
    one should not have to ask which fields are.
    """
    found: list[dict[str, str]] = []
    for track in result.suppressed:
        found.append(
            {
                "code": SUPPRESSED_WARNING,
                "message": (
                    f"{track.wanted.artist} / {track.wanted.title} is suppressed by "
                    f"a tombstone and was not counted missing"
                ),
                "suppression": track.suppression_id or "",
                "match": track.match_id,
                "item": "",
                "remedy": "",
            }
        )
    # A TOMBSTONE THAT DID NOT SUPPRESS IS STILL REPORTED. The match consults the
    # store last, so a version the library can say something about becomes a
    # matched row or a question rather than a suppression, and the tombstone
    # would otherwise leave no trace at all. The two cases are different facts
    # and get different codes: over a held file the record is STALE and the disk
    # wins, while over a question the record still stands and whatever the person
    # answers, acquisition must not go and fetch it.
    seen: set[tuple[str, str]] = set()
    for state in match.PAYLOAD_STATES:
        for track in result.of(state):
            # ASKED UNDER EVERY SPELLING, the same set the suppression itself is
            # asked under. Reporting on ``track.identity`` alone asked under ONE
            # of them, so a tombstone recorded from the row ``Sun Path (Live)``
            # left no trace at all against a list line spelling it ``Aurora Bloom
            # - Sun Path [Live]``, which is the case the extra spellings exist
            # for: a report narrower than the rule it reports on is silent on
            # exactly the rows the rule was widened to catch.
            standing = match.standing_tombstone(
                track.wanted, suppresses=suppresses, suppression_id=identify
            )
            if standing is None or (track.match_id, standing) in seen:
                continue
            seen.add((track.match_id, standing))
            held = state is match.MatchState.MATCHED
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
                    "suppression": standing,
                    "match": track.match_id,
                    "item": track.item_id or "",
                    "remedy": "",
                }
            )
    # AND THE FILE BEING OFFERED AS THE ANSWER IS A SECOND PLACE A TOMBSTONE CAN
    # STAND, which the loop above cannot see and which went unreported in every
    # state. It asks under the addresses of the reading the LIST spelled, and a
    # candidate is by construction a version the list did NOT spell: that is what
    # makes it a question. So with a tombstone under ``Sun Path (Live)`` and the
    # library still holding that file, the list line ``Aurora Bloom - Sun Path -
    # Live`` reported the candidate, said nothing about the tombstone, and after
    # somebody accepted it came back MATCHED with an empty warning array. This
    # file's own docstring promises the opposite in as many words, that a
    # tombstone over a version the library actually holds is a stale record and
    # saying so is cheaper than letting somebody find out during a deletion.
    #
    # ALWAYS ``TOMBSTONE_OVER_OWNED``, never the suppression code, and in every
    # state including SUPPRESSED. A candidate is a file this run read off the
    # disk, so the disk has already won: the record is stale whatever the row
    # around it resolved to. The pair (row, suppression) is the dedupe key, so a
    # candidate standing under the same tombstone the row already reported is one
    # warning rather than two.
    for track in result.matches:
        for candidate in track.candidates:
            offered = match.Wanted(
                artist=candidate.artist,
                title=candidate.title,
                version=candidate.version,
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
                    "suppression": standing,
                    "match": track.match_id,
                    "item": track.item_id or "",
                    "remedy": "",
                }
            )
    named: set[str] = set()
    for track in result.of(match.MatchState.NEEDS_REVIEW):
        if track.why not in match.STALLED:
            continue
        # ONE WARNING PER ITEM. Two rows of one list can resolve to one question,
        # and a second warning about it is a second thing to clear that is not
        # there.
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
                "suppression": "",
                "match": track.match_id,
                "item": track.item_id or "",
                "remedy": CLEAR_VERB,
            }
        )
    # THE QUESTIONS THAT DO NOT GATE, SAID OUT LOUD, and this is the whole price
    # of not gating. A row of this class leaves the run at exit zero, so the only
    # thing standing between it and R11's silence is this warning and the
    # needs-review array. One per ITEM, for the reason the stalled loop above
    # gives: two rows of one list can resolve to one question, and two warnings
    # about one question is one thing to answer wearing two hats.
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
                "suppression": "",
                "match": track.match_id,
                "item": track.item_id or "",
                "remedy": REVIEW_VERB,
            }
        )
    # EVERY STATE, not only the one where nothing is acquired. This warning's own
    # reason for existing is that "the run then acquires a track the library
    # already holds", and the run that acquires is the one AFTER the rejection:
    # ``apply_verdict`` carries the withheld count onto the rejected MISSING row,
    # so run one exited 12 saying candidates were kept back and run two exited 0
    # with an acquisition option, no pending action and no warning at all. Silent
    # on the only run the sentence is about.
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
                "suppression": "",
                "match": track.match_id,
                "item": track.item_id or "",
                "remedy": "",
            }
        )
    return tuple(found)


def _pending(result: match.MatchResult, *, run_id: str) -> PendingHumanAction | None:
    """The outstanding questions, as a state rather than as a printed sentence.

    A run that produced version questions and exited zero is exactly the silence
    R11 exists to remove: the caller's next step reads ``missing``, acquires it,
    and never learns that four more tracks were a remix away from being right.
    Nothing is put in ``blocks``: an open version question stops nobody from
    working, it only stops the run from claiming it is finished.

    TWO KINDS OF OUTSTANDING, and conflating them parked a run at
    ``PENDING_HUMAN`` forever naming a remedy nobody could execute. An ANSWERABLE
    question is in the open queue and ``review list`` shows it. A STALLED one
    carries a verdict this run could not apply, which leaves the item RESOLVED:
    it is absent from the open listing, resolving it again is refused, and the
    only way forward is to clear it. That was reachable by deleting or retagging
    one file, and every later run repeated the same exit status while the verb it
    named reported nothing to do. So the verb the action names is the verb that
    can act, and the item identifiers ride in the steps.

    COUNTED BY QUESTION, not by row, IN BOTH HALVES OF THE SENTENCE. The first
    version of this counted the total by question and the stalled part by row, so
    one line pasted twice produced "1 tracks ... need a person; 2 of them carry a
    verdict that could not be applied", which is arithmetic nobody can follow, and
    then printed one identifier for the two.

    ONE CLASS OF QUESTION DOES NOT GATE, and it is a decision rather than an
    oversight: see :data:`UNGATED`, which also says what is not given up. It is
    filtered here rather than left out of the queue, so the question is still
    asked and still answerable; what changes is only whether one common public
    playlist spelling stops the caller's pipeline.

    IT IS FILTERED OUT OF THE GATE AND NOT OUT OF THE SENTENCE, and for one round
    it was filtered out of both. Measured on a 200 line list: 4 rows gate, 20
    more queue ungated, ``needs_review`` holds 24, and the summary a caller reads
    said "4 tracks ... need a person". Undercounting the outstanding questions
    six fold is the same silence R11 exists to remove wearing this unit's own fix
    as a costume, since the caller who reads the summary is exactly the caller
    who does not read every warning. So the ungated rows are counted in the
    sentence and named in a step, and what they do not do is change the exit
    status.
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
        # ONE STEP PER ITEM, each a command that runs. Joining the identifiers
        # into one line rendered "crate review clear a, b", and the verb takes a
        # single positional, so the shell answered "unrecognized arguments" and
        # exit 2. A pending action naming a remedy nobody can execute is the
        # printed instruction this field exists to replace, so rendering one here
        # was the same defect wearing this unit's own fix as a costume.
        steps.extend(f"crate review clear {item_id}" for item_id in stalled)
    if ungated:
        steps.append(
            f"{len(ungated)} further questions are queued and did not block this "
            f"run, because this list spells a version after a dash and no rule "
            f"over that string decides it; they are answered the same way"
        )
    return PendingHumanAction(
        kind="review",
        id=output.new_pending_id(run_id),
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
        verify_verb=REVIEW_VERB if answerable else CLEAR_VERB,
        steps=tuple(steps),
    )


def library_template(cfg: config.Config) -> naming.NameTemplate:
    """The shape the library's own filenames are written in.

    THE MARKER IS THE POINT. R21 makes a lossy copy carry a marker inside its
    name, and a template that does not declare the marker cannot strip it, so
    the marked copy and its lossless twin fold to two different recordings. The
    source system's two strippers disagreed about exactly this and the result
    was a pair of duplicates sitting in one playlist. Config owns the marker
    text (S3) and this is where it is handed to the engine.
    """
    marker = (cfg.naming.lossy_marker or "").strip()
    if not marker:
        # A marker rule with an empty literal is refused at construction, and a
        # configuration with no marker text is a configuration where no file
        # carries one. Refusing the whole run over it would turn a naming policy
        # into a reason the match cannot happen at all.
        return naming.NameTemplate()
    return naming.NameTemplate(
        markers=(naming.MarkerRule(field="lossy", literal=marker),)
    )


def match_list(ctx: Any) -> Envelope:
    """The handler. NOT called ``run``: ``cli.run`` is the dispatcher.

    Two things called ``run`` in one call path is the collision the repository
    already records three times over, and here the two would sit one frame apart
    in every traceback this verb ever produces.
    """
    cfg = _load()
    wanted = read_list(Path(ctx.args.list))
    # THE TOMBSTONE SNAPSHOT COMES BEFORE THE LIBRARY WALK. A store that cannot
    # be read refuses, and a refusal that arrives after a scan of every file on
    # the music volume is a refusal the user waited minutes for. The order costs
    # nothing and is the same argument U8 makes for its three gates.
    suppresses, identify = suppression_view(review.DecisionStore(TOMBSTONE_STORE, cfg))
    index = match.index_library(
        cfg.library.root / cfg.library.music_dir, template=library_template(cfg)
    )
    result = match.resolve_all(
        wanted, index, suppresses=suppresses, suppression_id=identify
    )
    with review.open_store(cfg) as items:
        result = adjudicate(
            items,
            result,
            handler_key=ctx.entry.handler_key,
            suppresses=suppresses,
            suppression_id=identify,
        )
    pending = _pending(result, run_id=ctx.run.run_id)
    return ctx.envelope(
        data=result.payload(),
        outcome=Outcome.PENDING if pending is not None else Outcome.OK,
        code=ExitCode.PENDING_HUMAN if pending is not None else ExitCode.OK,
        pending=pending,
        warnings=_warnings(result, suppresses=suppresses, identify=identify),
    )


__all__ = [
    "CANDIDATES_WITHHELD",
    "CLEAR_VERB",
    "LIST_KEYS",
    "LIST_VERSION",
    "QUEUE",
    "READING_UNSETTLED",
    "REVIEW_VERB",
    "SUPPRESSED_WARNING",
    "TOMBSTONE_OVER_OWNED",
    "TOMBSTONE_STORE",
    "UNGATED",
    "VERDICT_UNAPPLICABLE",
    "adjudicate",
    "build",
    "library_template",
    "match_list",
    "read_list",
    "suppression_view",
]
