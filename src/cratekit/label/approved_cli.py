"""``label.approved``: the list document for the label releases a person accepted.

R-402's acquire half. A label sweep offers each new release into the review
queue, a person accepts or rejects it, and until this verb the answer went
nowhere: ``review resolve`` records a verdict and produces nothing acquirable.
This verb reads every ACCEPTED release on the label queue, reads its tracks
again from the provider, resolves each against the library, and hands the
missing ones to the one emitter, :func:`cratekit.acquire.listdoc.write`, with a
manifest that says which label, which year and which release each came from.

THE REVIEW ITEM'S PAYLOAD NAMES THE RELEASE AND NOTHING ELSE IS TAKEN FROM IT
ABOUT A TRACK. A payload written before R-379 carries a memory address where
the artist belongs, and 98 such rows sit on the live queue. Every artist and
title in the list comes from the provider's own track rows, read by release
identifier through :meth:`~cratekit.label.catalogue.Catalogue.release_tracks`.
The label's identifier and name do travel from the payload into the manifest,
as provenance and never as a key: R-381 records that an accented name yields a
mangled identifier, so nothing here looks anything up by one.

THERE IS NO HANDED OFF STATE, and that is what makes a second run safe.
Ownership is the record. A track downloaded and landed since the last run
resolves owned and is left out, so the verb may be run after every review
sitting and lists only what is still owed. The list's name carries a digest of
WHAT IT WRITES, the rows and their provenance and not the identifiers alone:
the same work writes the same bytes to the same name, which the emitter
recognises, and any other work, a corrected year included, takes a different
name rather than meeting the emitter's refusal to replace a file holding
something else. A list written before its tracks landed is superseded by the
next one, which holds everything the earlier one did that is still owed.

ONLY MISSING IS LISTED, on the rule ``intake missing`` states. A track the
library holds in another version is a question, offered into the match queue
the way an intake offers it, and an answer already given is read back, so a
person who said "that is not the same record" finds the track listed next run.
The same recording on two accepted releases, a single and the album it came
from, is listed once under the first.

A RELEASE THAT CANNOT BE READ IS NAMED AND THE REST STILL LIST. One withdrawn
release among ninety must not hold the other eighty nine, so it becomes a
failing check carrying its identifier and the step that settles it, and the
step differs by KIND: a release that is gone, or an item naming no release, is
settled by revoking the acceptance, and only a provider that did not answer is
settled by asking again. What is refused outright is a run that read NO release,
or listed nothing while some could not be read, because reported as a no-op
either reads exactly like a library that already holds everything. A
``CratekitError`` from the seam passes through untouched: an adapter that knows
the session expired names an act that is the person's to take once.

A PROVIDER THAT HAS STOPPED ANSWERING IS NOT ASKED NINETY TIMES. Every failed
read has already climbed the listing module's retry ladder, 31 seconds of
waiting, so :data:`OUTAGE_AFTER` failures in a row end the asking and the
releases left are reported as not asked. An answer, or a release that is gone,
which is an answer too, resets the count.

THE GENRE GATE JUDGES EVERY RELEASE READ BEFORE ANY IS LISTED. U101, R-420.
:func:`cratekit.core.routing.gate_decisions` decides against a set of
releases at once, so every accepted release is read first, the gate runs once
per label over one genre per release, and only then are the passed releases
resolved. The set is the label's releases ACCEPTED AND READ THIS RUN, not its
whole catalogue, which this verb never reads (R-462), and a label with any
release unread this run is not judged at all. A release the gate holds is
named with its family and its share and is neither listed nor offered for
review. A release whose genre is not known,
because its rows report none or report more than one, is listed with a failing
line saying the gate could not judge it: absence of a genre is not evidence of
a bad fit, and it is not evidence of a good one either. No shipped catalogue
reports a genre today, so in the shipped build that share rule judges nothing.

THE SAME GATE ALSO JUDGES KIND, WITH THE GENERAL CATALOGUE'S WORDS. R-798. The
share rule above cannot hold a release of music the label was never followed
for when that music is most of what was accepted, and it has no genre to read.
So each release read is first judged the way the sweep judges it,
:func:`cratekit.core.routing.kind_verdict` over what a general catalogue
publishes for its tracks: the words the sweep recorded on the item when it
filed it, else the lookup, asked with the ISRCs of the rows this verb already
read, so no provider call is added. A release of another kind than its label
is followed as is HELD, named with the words and the kind, and neither listed
nor offered. A release a person returned to review is passed without being
judged, and the held line names the command that returns one,
``crate label held return``, which works on a release already in review. A
release the catalogue has no word for is listed, and it joins the failing
``ungated`` line only when the share rule did not judge it either. This is
what judges a release filed before the sweep had a gate, or filed unjudged
because the catalogue could not be read that day.

THE CATALOGUE IS NOT ASKED ABOUT A RELEASE THE LIBRARY ALREADY HOLDS IN FULL.
This verb reads every accepted release on every run, the downloaded ones
included, and a hold can only keep a release out of the list and out of the
match queue. A release with every track owned reaches neither, so asking about
it would spend paced requests on every run for an answer that changes nothing.

Not a confirm gate and not destructive: it writes two new files and the
emitter refuses rather than replaces. Nothing here composes
``acquire download``, so nothing here can spend a download.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import shlex
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.acquire import listdoc, match, match_cli
from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, review, routing, taxonomy
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.review import Queue
from cratekit.intake.missing_cli import LISTS_DIR
from cratekit.label import catalogue, sweep
from cratekit.label import cli as label_cli
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.tagging import searchers

#: What the provenance sidecar says a listed row came from. ``intake land``
#: reads exactly this word to find the rows it files under the labels tree.
#: NOT NAMED ``PROVENANCE_SOURCE``: ``intake.missing_cli`` already exports that
#: name as a mapping from a job's key, and one symbol meaning two things in two
#: modules is a defect shape this repository has paid for.
LABEL_SOURCE = "label"

#: What every list this verb writes is named after, before the digest.
LIST_PREFIX = "label-approved"

#: How many provider failures IN A ROW end the asking. Three, because one is a
#: bad release and two is a coincidence, and each has already cost a full retry
#: ladder by the time it is counted.
OUTAGE_AFTER = 3

#: The four ways an accepted release yields no tracks, by what settles each.
GONE = "gone"
NO_IDENTIFIER = "no-identifier"
PROVIDER = "provider"
NOT_ASKED = "not-asked"

#: How many bytes of digest a list's name carries, as twice that many hex
#: characters. Six bytes is 48 bits, and a collision costs a refusal to replace
#: a file, never a wrong list. Asked of the hash as its size rather than sliced
#: off a longer one, so this module holds no bare integer an exit code could be
#: mistaken for, which is a population ``tests/test_reserved_causes.py`` pins.
DIGEST_BYTES = 6


def build_approved(parser, entry) -> None:
    parser.add_argument(
        "--out",
        default=None,
        metavar="DIR",
        help="folder to write the list into (default: the lists folder under download staging)",
    )
    parser.set_defaults(_handler=label_approved)


def _unusable(message: str, *steps: str, **detail: Any):
    return refuse(
        "label-list-unusable",
        message,
        steps=steps,
        origin=("label.approved",),
        detail=detail,
    )


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return {"key": f"label.approved.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


@dataclass(frozen=True, slots=True)
class _Release:
    """One accepted review item, reduced to what names and places its release."""

    item_id: str
    release_id: str
    title: str
    label_id: str | None
    label_name: str | None
    #: The general catalogue's words the sweep recorded when it filed the item,
    #: or None when it recorded none. The kind gate judges on these (R-798).
    genres: tuple[str, ...] | None = None
    #: Whether a person returned this release to review after the gate held it.
    returned: bool = False


@dataclass(frozen=True, slots=True)
class _Failed:
    release: _Release
    kind: str
    why: str

    def to_json(self) -> dict[str, Any]:
        return {
            "release_id": self.release.release_id,
            "item_id": self.release.item_id,
            "kind": self.kind,
            "gone": self.kind == GONE,
            "why": self.why,
        }


@dataclass(frozen=True, slots=True)
class _Read:
    """One release the provider answered for: its readable rows, and the rest.

    ``genre`` is the one genre its rows report, or ``None`` with ``ungated``
    saying why the gate cannot judge it.
    """

    wanted: tuple[match.Wanted, ...]
    year: int | None
    unreadable: tuple[str, ...]
    genre: str | None = None
    ungated: str | None = None
    #: The provider's rows as it returned them, which is where the kind gate
    #: reads the ISRCs it asks the general catalogue with.
    rows: tuple[Any, ...] = ()


@dataclass(frozen=True, slots=True)
class _Held:
    """One release the genre gate held, and the numbers it was held on."""

    release: _Release
    genre: str
    family: str
    of_family: int
    classified: int
    share: float

    def to_json(self) -> dict[str, Any]:
        return {
            "release_id": self.release.release_id,
            "item_id": self.release.item_id,
            "genre": self.genre,
            "family": self.family,
            "of_family": self.of_family,
            "classified": self.classified,
            "share": self.share,
        }


@dataclass(frozen=True, slots=True)
class _OutOfKind:
    """One release held because it is not the kind of music its label is followed for."""

    release: _Release
    judged: genre_gate.Judged

    def to_json(self) -> dict[str, Any]:
        return {
            "release_id": self.release.release_id,
            "item_id": self.release.item_id,
            "genres": list(self.judged.genres),
            "kind": self.judged.kind,
            "reason": self.judged.reason,
        }


def _text(value: Any) -> str | None:
    """A payload value as text, or ``None``. Only a string is believed."""
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


def _genre_of(rows: tuple[Any, ...]) -> tuple[str | None, str | None]:
    """The one genre a release's rows report, or ``None`` and why there is none.

    Read from a mapping or an attribute, the two shapes a provider row comes in.
    ROWS THAT DISAGREE ARE NOT A GENRE. An EP whose remix is filed elsewhere
    has no one answer, and choosing the first or the most common would let the
    gate hold a release on a guess. The source system kept anything uncertain,
    and so does this.
    """
    said: dict[str, str] = {}
    for row in rows:
        value = row.get("genre") if isinstance(row, Mapping) else getattr(row, "genre", None)
        text = _text(value)
        if text is not None:
            said.setdefault(text.casefold(), text)
    if not said:
        return None, "the catalogue reports no genre for it"
    if len(said) > 1:
        return None, "its tracks report " + " and ".join(repr(one) for one in said.values())
    return next(iter(said.values())), None


def _label_of(release: _Release) -> str:
    """What a release is grouped under for the gate: its label, else itself.

    A release naming no label is judged alone, and alone every family it could
    carry is the whole of its output, so it is never held. Grouping every
    unlabelled release together would judge one against releases it shares
    nothing with.
    """
    return release.label_id or release.label_name or f"release:{release.release_id}"


def _gated(
    declared: taxonomy.Taxonomy,
    read: list[tuple[_Release, _Read]],
    failures: list[_Failed],
) -> tuple[dict[str, _Held], dict[str, str]]:
    """Every read release the genre gate holds, and every one it could not judge.

    Both keyed by review item. ONE CALL PER LABEL, never one per release. The
    gate's share is a fraction of the label's accepted releases, so one judged
    alone is always the whole of it and nothing would ever be held.

    A LABEL WITH A RELEASE UNREAD THIS RUN IS NOT JUDGED AT ALL. Its share is
    unknown rather than smaller: the unread release could be of the family in
    question or of any other, so a provider that failed on some releases would
    decide which of the rest are held. Every release of that label is listed
    unjudged and says why, the timid direction, and the next run that reads
    them all judges them.
    """
    unread = {_label_of(one.release) for one in failures}
    groups: dict[str, list[tuple[_Release, _Read]]] = {}
    for release, outcome in read:
        groups.setdefault(_label_of(release), []).append((release, outcome))
    share = declared.label_gate.out_of_place_share
    held: dict[str, _Held] = {}
    unjudged: dict[str, str] = {}
    for label, members in groups.items():
        if label in unread:
            for release, outcome in members:
                unjudged[release.item_id] = outcome.ungated or (
                    "another accepted release on its label could not be read, so the "
                    "label's share of its genre is not known"
                )
            continue
        genres = [outcome.genre for _release, outcome in members]
        verdicts = routing.gate_decisions(declared, genres)
        families = [routing.gate_family(declared, genre) for genre in genres]
        classified = sum(1 for genre in genres if genre)
        for (release, outcome), verdict, family in zip(members, verdicts, families, strict=True):
            if outcome.ungated is not None:
                unjudged[release.item_id] = outcome.ungated
            elif verdict is routing.GateVerdict.DROP and family and outcome.genre:
                held[release.item_id] = _Held(
                    release, outcome.genre, family, families.count(family), classified, share
                )
    return held, unjudged


def _judged_by_kind(
    declared: taxonomy.Taxonomy,
    read: list[tuple[_Release, _Read]],
    followed: labels.Registry,
    owned: Callable[[_Release], bool],
) -> tuple[dict[str, _OutOfKind], dict[str, str]]:
    """Every read release held as another kind of music, and every one not judged.

    Both keyed by review item. ONE RELEASE AT A TIME, unlike the share rule:
    kind is a fact about a release and the label it is on, not about the set
    accepted beside it, so a release unread this run changes nothing here.

    THE WORDS THE SWEEP RECORDED ARE USED WHEN THERE ARE ANY, so a release is
    judged at acceptance on what it was judged on when it was filed and the
    catalogue is not asked twice. The lookup is asked otherwise, with the rows
    this verb already read, and it is looked up at call time, only when a
    release needs it.

    A RELEASE A PERSON RETURNED IS NOT JUDGED AND NOT REPORTED AS UNJUDGED.
    Their answer is the judgment.

    A LABEL THE REGISTRY NO LONGER HOLDS IS THE DEFAULT KIND, which is what it
    would be judged as were it followed with no kind set.

    A RELEASE THE LIBRARY HOLDS IN FULL IS NOT ASKED ABOUT, ``owned`` says
    which, and says so as its reason. See the module docstring. Words the
    sweep recorded are still judged, since that costs no request.
    """
    held: dict[str, _OutOfKind] = {}
    unjudged: dict[str, str] = {}
    # ONE ASKING FOR THE RUN, so a catalogue that cannot be reached is given up
    # on after a few releases and not paid for on every one.
    asking = genre_gate.Asking()
    for release, outcome in read:
        if release.returned:
            continue
        entry = followed.by_id(release.label_id) if release.label_id else None
        kind = entry.kind if entry is not None else None
        if release.genres is not None:
            words = genre_gate.Words(release.genres, searchers.Answer.MATCHED.value)
            judged = genre_gate.judge_words(declared, kind, words)
        elif routing.kind_settled(declared, kind) is not None:
            # NOT THIS MODULE'S ``NOT_ASKED``, which is a release the PROVIDER
            # was not asked for. The two words are spelled alike and mean
            # different catalogues.
            judged = genre_gate.judge_words(
                declared, kind, genre_gate.Words((), searchers.NOT_ASKED)
            )
        elif owned(release):
            unjudged[release.item_id] = (
                "every track of it is already in the library, so the general "
                "catalogue was not asked about it"
            )
            continue
        else:
            judged = genre_gate.judge_rows(declared, kind, outcome.rows, asking)
        if judged.held:
            held[release.item_id] = _OutOfKind(release, judged)
        elif judged.verdict is routing.KindVerdict.NOT_JUDGED:
            unjudged[release.item_id] = judged.reason
    return held, unjudged


def _release_of(items: review.ReviewStore, item: review.Item) -> _Release:
    """The release an accepted item names, from its IDENTITY before its payload.

    The identity is what the item is addressed by and is what the sweep keyed
    on. An item that arrived through ``review import`` carries none, because
    the export format does not, and then the payload's own copy of the
    identifier is all there is. An item naming no release at all is kept, with
    an empty identifier, so it is reported as a failure rather than skipped.
    """
    identity = review.identity_of(items, item.item_id) or {}
    release_id = _text(identity.get("release_id")) or _text(item.payload.get("identity")) or ""
    # RETURNED BY EITHER RECORD. The hold is the record of a return. A release
    # the gate held at a SWEEP also carries the word on its payload, written
    # when it was filed, and that copy is what survives a queue exported to
    # another machine. A release returned while it was already in review has
    # the hold alone, since a decided item's payload is never rewritten.
    # Believing either is the safe direction: a returned release held a second
    # time is music a person asked for and never gets.
    standing = review.find_hold(items, queue=str(Queue.LABEL_RELEASE), item_id=item.item_id)
    returned = (
        standing is not None and standing.state == review.HOLD_RETURNED
    ) or item.payload.get(genre_gate.GATE_FIELD) == genre_gate.RETURNED
    return _Release(
        item_id=item.item_id,
        release_id=release_id,
        title=_text(item.payload.get("title")) or "",
        label_id=_text(item.payload.get("label_id")),
        label_name=_text(item.payload.get("label_name")),
        genres=genre_gate.recorded_genres(item.payload, genre_gate.GENRES_FIELD),
        returned=returned,
    )


def _queued(items: review.ReviewStore) -> tuple[list[_Release], int, int]:
    """The accepted releases in queue order, and how many were rejected or open.

    An item whose stored verdict this build cannot read counts as OPEN, which
    is the direction ``review`` argues for everywhere: undecided rather than
    decided the wrong way.
    """
    page = review.list_items(
        items,
        queue=str(Queue.LABEL_RELEASE),
        kinds=(sweep.KIND,),
        include_resolved=True,
        limit=None,
    )
    accepted: list[_Release] = []
    rejected = still_open = 0
    for item in page.items:
        if item.verdict is review.Verdict.ACCEPTED:
            accepted.append(_release_of(items, item))
        elif item.verdict is review.Verdict.REJECTED:
            rejected += 1
        else:
            still_open += 1
    return accepted, rejected, still_open


def _tracks_or_failure(found: catalogue.Catalogue, release: _Release) -> _Read | _Failed:
    """One release's tracks as ``Wanted`` rows and its year, or why there are none.

    THE FIRST CALLER OF ``release_tracks`` OWNS ITS FAILURE PATHS. Two exception
    shapes arrive and neither is this module's to predict, the argument
    ``label_cli.playlist_tracks_or_refuse`` makes: the provider's own error once
    the retry ladder is spent, and the listing module's plain ``RuntimeError``
    for a truncated or unpageable listing. So the catch is broad, bounded by the
    ``CratekitError`` passthrough above it.

    ONLY THE SEAM'S OWN EXCEPTION MEANS GONE. ``LookupError`` would be the
    shorter catch and is the wrong one: ``KeyError`` is a ``LookupError``, a
    client that meets a payload it cannot parse raises exactly that, and a
    person would be told to revoke an acceptance over a parse failure.

    EACH ROW IS READ ALONE. The row reader refuses a whole listing over one row
    it cannot recognise, which is right for a document somebody wrote and wrong
    here, where one odd row would cost every other track on the release. A row
    it refuses is kept by what the refusal said, and reported.
    """
    if not release.release_id:
        return _Failed(release, NO_IDENTIFIER, "the review item names no release identifier")
    try:
        rows, year = found.release_tracks(release.release_id)
    except CratekitError:
        raise
    except catalogue.ReleaseUnresolvable as exc:
        return _Failed(release, GONE, str(exc))
    except Exception as exc:  # noqa: BLE001 - named per release, never swallowed
        return _Failed(release, PROVIDER, f"{type(exc).__name__}: {exc}")
    wanted: list[match.Wanted] = []
    unreadable: list[str] = []
    for row in rows:
        try:
            wanted.extend(match.read_tidal_tracks((row,)))
        except match.UnreadableList as exc:
            unreadable.append(str(exc))
    genre, ungated = _genre_of(tuple(rows))
    return _Read(tuple(wanted), year, tuple(unreadable), genre, ungated, tuple(rows))


def _out_dir(ctx, cfg) -> Path:
    given = ctx.args.out
    if given:
        out = Path(str(given)).expanduser().absolute()
    else:
        out = cfg.paths.download_staging / LISTS_DIR
    if out.exists() and not out.is_dir():
        raise _unusable(
            f"{out} exists and is not a folder, so no list can be written into it",
            "name a folder with --out",
            out=str(out),
        )
    return out


def list_name(
    body: Mapping[str, Any], provenance: Mapping[str, listdoc.Provenance]
) -> str:
    """The name a list of exactly these rows, from exactly these releases, takes.

    OVER EVERYTHING THE EMITTER COMPARES, not over the identifiers alone. The
    emitter refuses a name whose file holds any other bytes, and the manifest's
    bytes carry the year and the label. A digest of the identifiers gave the
    same name to the same tracks with a year the provider had since corrected,
    and the verb then refused on every run until somebody moved a file by hand.
    """
    said = {
        "tracks": body["tracks"],
        "provenance": [
            dataclasses.asdict(provenance[track["id"]]) for track in body["tracks"]
        ],
    }
    encoded = json.dumps(said, ensure_ascii=False, sort_keys=True).encode("utf-8")
    digest = hashlib.blake2s(encoded, digest_size=DIGEST_BYTES)
    return f"{LIST_PREFIX}-{digest.hexdigest()}"


def _named(release: _Release) -> str:
    said = f"release {release.release_id or '(no identifier)'}"
    if release.title:
        said += f" ({release.title!r}"
        said += f" on {release.label_name})" if release.label_name else ")"
    return said


def _failure_check(failed: _Failed) -> dict[str, Any]:
    """One failing line per release, ending in the act that settles ITS kind."""
    release = failed.release
    clear = f"crate review clear {release.item_id}"
    if failed.kind == GONE:
        detail = (
            f"{_named(release)} is gone from the provider and none of it is in the "
            f"list ({failed.why}); waiting will not bring it back, so revoke its "
            f"acceptance with: {clear}"
        )
    elif failed.kind == NO_IDENTIFIER:
        detail = (
            f"{_named(release)} cannot be asked for and none of it is in the list "
            f"({failed.why}); running again will not change that, so revoke its "
            f"acceptance with: {clear}"
        )
    elif failed.kind == NOT_ASKED:
        detail = (
            f"{_named(release)} was NOT ASKED FOR and none of it is in the list "
            f"({failed.why}); run this again once the provider answers"
        )
    else:
        detail = (
            f"{_named(release)} could not be read and none of it is in the list "
            f"({failed.why}); run this again once the provider answers"
        )
    return _check(f"release.{release.release_id or release.item_id}", "fail", detail)


def _held_check(held: _Held | _OutOfKind) -> dict[str, Any]:
    """One line per held release, carrying what it was held on."""
    release = held.release
    if isinstance(held, _OutOfKind):
        return _check(
            f"held.{release.release_id or release.item_id}",
            "info",
            f"{_named(release)} is HELD by the genre gate and none of it is in the "
            f"list: {held.judged.reason}; to list this one anyway: crate label held "
            f"return {release.release_id}; to pass its kind for the whole label: "
            f"crate label registry set LABEL --kind KIND",
        )
    label = release.label_name or release.label_id or "no named label"
    detail = (
        f"{_named(release)} is HELD by the genre gate and none of it is in the list: "
        f"its genre {held.genre!r} is the {held.family} family, {held.of_family} of "
        f"the {held.classified} release(s) with a genre accepted from {label}, "
        f"under the {held.share:.0%} share a family needs to belong to that label"
    )
    return _check(f"held.{release.release_id or release.item_id}", "info", detail)


def label_approved(ctx) -> Envelope:
    """List the missing tracks of every accepted label release, or say why not."""
    cfg = label_cli._load()
    with review.open_store(cfg) as items:
        accepted, rejected, still_open = _queued(items)
    queue_check = _check(
        "queue",
        "info",
        f"{len(accepted)} accepted release(s) read; {rejected} rejected and "
        f"{still_open} not yet answered were not; see: crate review list --queue "
        f"{Queue.LABEL_RELEASE}",
    )
    if not accepted:
        # ASKED BEFORE THE CATALOGUE IS RESOLVED, so a queue with nothing
        # accepted spends no login and refuses over no missing credential.
        return ctx.envelope(
            data={
                "checks": [
                    _check("written", "info", "nothing listed: no label release is accepted"),
                    queue_check,
                ],
                "summary": _summary(None, accepted=0, rejected=rejected, open=still_open),
            },
            outcome=Outcome.NO_OP,
        )

    # THE DECLARATION BEFORE THE FIRST LOGIN (R-685). An active copy that cannot
    # be read refuses here, not after every accepted release was fetched.
    declared = active_taxonomy.load(cfg)
    # THE REGISTRY BEFORE THE FIRST LOGIN TOO, for the same reason (R-798). A
    # label's kind decides what the gate holds, and judging every label as the
    # default because the registry could not be read would hold an R&B label's
    # own releases. So an unreadable registry refuses here, with its own
    # remedy, and not after every accepted release was fetched.
    followed = labels.RegistryStore().load()
    # LOOKED UP ON THE MODULE AT CALL TIME, the contract ``catalogue`` states,
    # which is what lets a suite substitute the seam.
    found = catalogue.resolve(cfg)
    index, suppresses, identify = match_cli.library_view(cfg)

    counts = {"owned": 0, "offered": 0, "suppressed": 0, "duplicate": 0, "missing": 0}
    failures: list[_Failed] = []
    undated: list[_Release] = []
    unreadable: list[tuple[_Release, str]] = []
    missing: list[match.Wanted] = []
    origins: list[tuple[_Release, int | None]] = []
    seen: set[str] = set()
    answered: list[tuple[_Release, _Read]] = []
    in_a_row = 0
    for release in accepted:
        if in_a_row >= OUTAGE_AFTER:
            failures.append(
                _Failed(
                    release,
                    NOT_ASKED,
                    f"the provider failed {OUTAGE_AFTER} releases in a row, so the "
                    f"rest were not spent on it",
                )
            )
            continue
        outcome = _tracks_or_failure(found, release)
        if isinstance(outcome, _Failed):
            failures.append(outcome)
            # ONLY A PROVIDER THAT DID NOT ANSWER COUNTS. A release that is gone
            # is the provider answering, and an item naming no release never
            # reached it.
            in_a_row = in_a_row + 1 if outcome.kind == PROVIDER else 0
            continue
        in_a_row = 0
        answered.append((release, outcome))
        unreadable.extend((release, why) for why in outcome.unreadable)
    read = len(answered)

    # THE GATE BEFORE ANY RESOLUTION, so a held release is never offered for
    # review and never listed, and every release it judges is judged against
    # the same set.
    by_share, unjudged = _gated(declared, answered, failures)
    # KIND AS WELL, and a release of another kind is held whatever its share
    # (R-798). A release is UNJUDGED only when neither rule judged it, and the
    # line says what each was missing.
    # EACH RELEASE IS RESOLVED AGAINST THE LIBRARY ONCE, HERE, before either
    # rule runs. Resolution is a read and writes nothing, the offer into the
    # match queue stays below, after the gate. The kind rule asks it whether
    # the library already holds a release in full, and the listing loop reads
    # the same answer.
    resolutions = {
        release.item_id: tuple(
            match.resolve_one(one, index, suppresses=suppresses, suppression_id=identify)
            for one in outcome.wanted
        )
        for release, outcome in answered
    }
    rows_unread = {release.item_id for release, _why in unreadable}

    def fully_owned(release: _Release) -> bool:
        """Every row read, and every one already in the library. At least one."""
        return release.item_id not in rows_unread and sweep.every_track_owned(
            resolutions[release.item_id]
        )

    by_kind, kind_unjudged = _judged_by_kind(declared, answered, followed, fully_owned)
    held: dict[str, _Held | _OutOfKind] = {**by_share, **by_kind}
    ungated = [
        (release, f"{unjudged[release.item_id]}, and {kind_unjudged[release.item_id]}")
        for release, _outcome in answered
        if release.item_id in unjudged and release.item_id in kind_unjudged
    ]
    for release, outcome in answered:
        if release.item_id in held:
            continue
        year = outcome.year
        if year is None:
            undated.append(release)
        resolved = match.MatchResult(matches=resolutions[release.item_id])
        if any(match_cli.touches_the_queue(one) for one in resolved.matches):
            # THE REVIEW STORE IS OPENED ONLY WHEN A ROW TOUCHES IT, a question
            # or a row a rule owns, as the intake worker opens it, and the
            # offer is idempotent on the question.
            with review.open_store(cfg) as items:
                resolved = match_cli.adjudicate(
                    items,
                    resolved,
                    handler_key=ctx.entry.handler_key,
                    suppresses=suppresses,
                    suppression_id=identify,
                )
        for settled in resolved.matches:
            if settled.state is match.MatchState.MATCHED:
                counts["owned"] += 1
            elif settled.state is match.MatchState.NEEDS_REVIEW:
                counts["offered"] += 1
            elif settled.state is match.MatchState.SUPPRESSED:
                counts["suppressed"] += 1
            elif settled.match_id in seen:
                counts["duplicate"] += 1
            else:
                seen.add(settled.match_id)
                counts["missing"] += 1
                missing.append(settled.wanted)
                origins.append((release, year))

    failed_detail = [one.to_json() for one in failures]
    settle = (
        "run this again once the provider answers",
        "a release that is gone, or an item naming no release, stays that way; "
        "revoke its acceptance with: crate review clear ITEM_ID",
    )
    if not read:
        # NO RELEASE READ IS NOT NOTHING MISSING. A no-op here would read like a
        # library that holds every approved release, over a provider nobody
        # got an answer from.
        raise _unusable(
            f"none of the {len(accepted)} accepted release(s) could be read from the "
            f"provider, so nothing is known about what they hold and nothing was "
            f"written: " + "; ".join(f"{_named(one.release)}: {one.why}" for one in failures),
            *settle,
            failed=failed_detail,
        )

    written = listdoc.Written(None, None, (), ())
    if missing:
        rows = listdoc.rows_of(missing)
        provenance = _provenance(rows, origins)
        try:
            body, _listed, _unlisted = listdoc.document(rows)
            written = listdoc.write(
                _out_dir(ctx, cfg), list_name(body, provenance), rows, provenance
            )
        except listdoc.ListDocRefused as exc:
            raise _unusable(
                str(exc), "move the file aside or name another folder with --out"
            ) from exc
        except OSError as exc:
            # A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL. The emitter
            # converts what it reads and lets a failed write through, and left
            # alone that reaches a person as an internal error telling them to
            # report a defect over a folder they cannot write to.
            raise _unusable(
                f"the list could not be written ({type(exc).__name__}: "
                f"{exc.strerror or exc}); nothing acquire download could read was "
                f"left behind",
                "name another folder with --out, or make this one writable",
                path=str(exc.filename or ""),
            ) from exc
    listed = len(written.listed)
    unlisted = len(written.unlisted)
    if missing and not listed:
        raise _unusable(
            f"{unlisted} missing track(s) and none carries a provider identifier, so "
            f"there is nothing acquire download could be asked for; nothing was written",
            "this is a defect in what the provider returned for these releases; "
            "run this again, and report it if it repeats",
            unlisted_tracks=[{"artist": row.artist, "title": row.title} for row in written.unlisted],
        )
    passed = read - len(held)
    if failures and not listed:
        # NOTHING LISTED WITH RELEASES UNREAD IS NOT A LIBRARY THAT HOLDS THEM.
        raise _unusable(
            f"nothing is missing from the {passed} release(s) that could be read"
            + (f" and passed the genre gate ({len(held)} more held by it)" if held else "")
            + f", and {len(failures)} could not be, so this is not a library holding "
            f"every approved release: "
            + "; ".join(f"{_named(one.release)}: {one.why}" for one in failures),
            *settle,
            failed=failed_detail,
        )

    command = (
        shlex.join(["crate", "acquire", "download", str(written.list_path)])
        if written.list_path is not None
        else None
    )
    checks = [
        _check(
            "written",
            "ok" if listed else "info",
            f"{listed} missing track(s) from {passed} accepted release(s) written to "
            f"{written.list_path}; next: {command}"
            if listed
            # A HELD RELEASE WAS NEVER RESOLVED, so the library is not said to
            # hold it.
            else f"nothing listed: the library holds every track of the {passed} "
            f"accepted release(s) the genre gate passed, and {len(held)} more were "
            f"held by it"
            if held
            else f"nothing listed: the library holds every track of the {read} "
            f"accepted release(s)",
        ),
        queue_check,
        _check("owned", "info", f"{counts['owned']} already in the library, not listed"),
        _check(
            "offered",
            "info",
            f"{counts['offered']} held in another version, offered for review and not "
            f"listed until answered; see: crate review list",
        ),
        _check("suppressed", "info", f"{counts['suppressed']} deleted on purpose, not listed"),
        _check(
            "duplicate",
            "info",
            f"{counts['duplicate']} the same recording as a track already listed from "
            f"an earlier release, listed once",
        ),
        _check(
            "unlisted",
            "fail" if unlisted else "ok",
            f"{unlisted} missing track(s) carry no provider identifier and are NOT in the list"
            if unlisted
            else "every missing track is in the list",
        ),
        _check(
            "unreadable",
            "fail" if unreadable else "ok",
            f"{len(unreadable)} track row(s) the provider returned could not be read "
            f"and are NOT in the list: "
            + "; ".join(f"{_named(release)}: {why}" for release, why in unreadable)
            if unreadable
            else "every track row the provider returned was read",
        ),
        _check(
            "undated",
            "fail" if undated else "ok",
            f"{len(undated)} release(s) carry no year the provider could be read for, "
            f"so their manifest rows say none: "
            + ", ".join(_named(release) for release in undated)
            if undated
            else "every release the genre gate passed carries its year",
        ),
        _check(
            "held",
            "info",
            f"{len(held)} accepted release(s) held by the genre gate and NOT in the list: "
            + ", ".join(_named(one.release) for one in held.values())
            if held
            else "no release was held by the genre gate",
        ),
        _check(
            "ungated",
            "fail" if ungated else "ok",
            f"{len(ungated)} release(s) the genre gate could not judge, so they are "
            f"listed unjudged: "
            + "; ".join(f"{_named(release)}: {why}" for release, why in ungated)
            if ungated
            else "every release read was judged by the genre gate",
        ),
        _check(
            "releases",
            "fail" if failures else "ok",
            f"{len(failures)} accepted release(s) could not be read and are NOT in the list"
            if failures
            else "every accepted release was read",
        ),
        *(_failure_check(one) for one in failures),
        *(_held_check(one) for one in held.values()),
    ]
    summary = _summary(
        written,
        accepted=len(accepted),
        rejected=rejected,
        open=still_open,
        read=read,
        next=command,
        missing=counts["missing"],
        owned=counts["owned"],
        offered=counts["offered"],
        suppressed=counts["suppressed"],
        duplicate=counts["duplicate"],
        unreadable=len(unreadable),
        undated=[release.release_id for release in undated],
        held=[one.to_json() for one in held.values()],
        ungated=[release.release_id for release, _why in ungated],
        failed=failed_detail,
    )
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if listed else Outcome.NO_OP,
    )


def _provenance(
    rows: tuple[listdoc.Row, ...], origins: list[tuple[_Release, int | None]]
) -> dict[str, listdoc.Provenance]:
    """Each listed id's provenance. First release wins, as the document's row does."""
    found: dict[str, listdoc.Provenance] = {}
    for row, (release, year) in zip(rows, origins, strict=True):
        ref = str(row.ref or "").strip()
        if not ref or ref in found:
            continue
        found[ref] = listdoc.Provenance(
            source=LABEL_SOURCE,
            source_ref=release.release_id,
            label_id=release.label_id,
            label_name=release.label_name,
            year=year,
            release_id=release.release_id,
        )
    return found


def _summary(written: listdoc.Written | None, **fields: Any) -> dict[str, Any]:
    held = written or listdoc.Written(None, None, (), ())
    base: dict[str, Any] = {
        "list": str(held.list_path) if held.list_path is not None else None,
        "manifest": str(held.manifest_path) if held.manifest_path is not None else None,
        "next": None,
        "written": len(held.listed),
        "unlisted": len(held.unlisted),
        "unlisted_tracks": [{"artist": row.artist, "title": row.title} for row in held.unlisted],
    }
    base.update(fields)
    return base


__all__ = [
    "DIGEST_BYTES",
    "GONE",
    "LABEL_SOURCE",
    "LIST_PREFIX",
    "NOT_ASKED",
    "NO_IDENTIFIER",
    "OUTAGE_AFTER",
    "PROVIDER",
    "build_approved",
    "label_approved",
    "list_name",
]
