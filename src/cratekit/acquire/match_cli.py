"""``crate match run``: resolve a list against the library, in three states.

The verb is thin on purpose. ``cratekit.acquire.match`` decides what each track
is; this file is where the decision meets persistence, and it owns exactly three
things the engine must not: configuration, the review queue, and the envelope.

**THE SPLIT U11 SETTLED, IMPLEMENTED HERE.** R11 has three states and only one
of them is a question. The needs-review state becomes a persisted review item in
the version-match queue; matched and missing are results, and neither ever
reaches the queue. That is not a detail of wording. A missing track is a fact,
not a question, and offering one into the queue would ask a person to confirm
that a track they put on a list should be acquired, once per run, forever, which
is precisely the unconditional re-prompting the queue exists to end. When
acquisition later cannot serve a missing track from the configured provider,
THAT is a question, and U11 declared a different queue for it.

The unit's own brief says missing items "become review items with acquisition
options". The half of that sentence which matters is its negative: not a file.
Both readings agree that the source system's ``missing.csv`` is gone. Where they
differ, U11's is the one with a countdown registered against this unit, and it
is also the one that survives contact with a person who runs the verb twice. So
a missing row carries its acquisition options as DATA in the match result, where
the next verb reads them, and it does not become a question nobody asked.

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

#: The verb that shows a person the questions this run left open.
REVIEW_VERB = "review.list"

#: A URL scheme at the start of an argument, matched against the form a path
#: leaves it in. ``Path`` COLLAPSES the double slash, so "https://host/x" is
#: "https:/host/x" by the time it is text again and a check for "://" finds
#: nothing. That is how a web address arrives as "no such file or directory".
#: Two or more characters before the colon, so a Windows drive letter is not a
#: scheme.
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
        return _text("\n".join(str(row) for row in rows))
    for position, row in enumerate(rows, start=1):
        if not isinstance(row, Mapping):
            raise _refuse(
                f"track {position} of a {origin} list is not a track record",
                position=position,
            )
    return match.READERS[origin](rows)


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
    if _URL_SCHEME.match(name):
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
) -> match.MatchResult:
    """Turn the needs-review state into queue items, and read back the answers.

    Matched and missing pass through untouched. They are results, and a result
    pushed into the queue asks a person to confirm an answer (R12, and the split
    U11 recorded when it declared these surfaces).
    """
    settled: list[match.TrackMatch] = []
    for found in result.matches:
        if found.state is not match.MatchState.NEEDS_REVIEW:
            settled.append(found)
            continue
        identity = found.identity
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
                found, accepted=accepted, option=held.option, item_id=held.item_id
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
            }
        )
    for track in result.of(match.MatchState.MATCHED):
        identity = track.identity
        if not suppresses(match.TOMBSTONE_KIND, identity):
            continue
        found.append(
            {
                "code": TOMBSTONE_OVER_OWNED,
                "message": (
                    f"{track.wanted.artist} / {track.wanted.title} is held on disk "
                    f"and a tombstone stands over it; the disk is the truth and the "
                    f"tombstone is stale"
                ),
                "suppression": identify(match.TOMBSTONE_KIND, identity),
                "match": track.match_id,
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
    """
    open_questions = result.of(match.MatchState.NEEDS_REVIEW)
    if not open_questions:
        return None
    return PendingHumanAction(
        kind="review",
        id=output.new_pending_id(run_id),
        summary=(
            f"{len(open_questions)} tracks resolved to a version this library does "
            f"not hold under that name, and need a person"
        ),
        verify_verb=REVIEW_VERB,
        steps=(
            "list the version-match queue and record a verdict on each item",
            "accept a candidate to call it the same record, or reject to acquire "
            "the version the list asked for",
        ),
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
        result = adjudicate(items, result, handler_key=ctx.entry.handler_key)
    pending = _pending(result, run_id=ctx.run.run_id)
    return ctx.envelope(
        data=result.payload(),
        outcome=Outcome.PENDING if pending is not None else Outcome.OK,
        code=ExitCode.PENDING_HUMAN if pending is not None else ExitCode.OK,
        pending=pending,
        warnings=_warnings(result, suppresses=suppresses, identify=identify),
    )


__all__ = [
    "LIST_KEYS",
    "LIST_VERSION",
    "QUEUE",
    "REVIEW_VERB",
    "SUPPRESSED_WARNING",
    "TOMBSTONE_OVER_OWNED",
    "TOMBSTONE_STORE",
    "adjudicate",
    "build",
    "library_template",
    "match_list",
    "read_list",
    "suppression_view",
]
