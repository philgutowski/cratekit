"""``label.sync``: ask, label by label, about what is new, and record each answer.

U107, the asking half of the guided label sync. Each favourite label is asked
about the releases new since it was last asked, with four answers: download all
new, pick releases, not now, stop following. Every answer is saved as it is
given and asking downloads nothing; the walk then ends at the one gate over the
saved answers, as ``--go`` does, and :mod:`cratekit.label.go` is what a yes runs.

THE MARKER IS A SET OF RELEASE IDENTITIES, NOT A DATE (KTD11), taking places in
the sweep's offer window as a queued release does (R-790), so back catalogue
never returns. It is LIBRARY state, coupled with the review queue on a restore.

THE LISTING AND THE GENRE GATE ARE THE SWEEP'S, so a release the gate holds never
reaches a question, and a label's OPEN review items are offered once under the
same question. A QUESTION IS SAVED BEFORE IT IS ASKED, so ``--answer`` answers
exactly what ``--next`` showed. ``all`` and ``pick`` record each taken release
accepted and supersede the rest; nothing is downloaded that was not answered for.
ONE REFUSAL OF THE PROVIDER PARKS THE RUN with the answers given saved, while a
listing that could not be read fails only that label's line.
"""

from __future__ import annotations

import json
import math
from collections.abc import Callable, Container, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import partial
from typing import Any

from cratekit.acquire import match_cli
from cratekit.cli import prompt
from cratekit.cli.output import Envelope, count_of, from_cause, timestamp
from cratekit.core import active_taxonomy, config, provider_gate, review
from cratekit.core.cause import Cause, CratekitError, Outcome, Scope, refuse
from cratekit.core.review import Queue, Verdict
from cratekit.core.routing import KindVerdict
from cratekit.core.taxonomy import Taxonomy
from cratekit.label import catalogue, kept_listing, review_common, sweep
from cratekit.label import cli as label_cli
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.sync import run

RECORD_VERSION = 1

#: The marker a saved answer carries once a go has taken it (U108); an answer
#: without it is what the next go's summary covers.
SETTLED = "settled"

#: The four answers, in the order they are offered.
ALL = "all"
PICK = "pick"
NOT_NOW = "not-now"
STOP = "stop"
ANSWERS: tuple[str, ...] = (ALL, PICK, NOT_NOW, STOP)
#: The fifth word the prompt takes: leave this label unanswered and end the run.
#: Not an answer, and nothing is written for it.
QUIT = "quit"

#: The actor a verdict this verb writes carries.
ACTOR = "label sync"
#: The rule a superseded open item records: the label was answered.
ANSWERED_RULE = "label-sync-answered"

#: The size estimate: FLAC at 16 bit 44.1 kHz averages about 880 kilobits a
#: second on dance music, and a row with no duration counts as six minutes.
BYTES_PER_SECOND = 110_000
SECONDS_PER_TRACK = 360

QUEUE = str(Queue.LABEL_RELEASE)

#: The key of the line a walk over every label says its estimate in (U278).
_ESTIMATE_KEY = "label.sync.estimate"

#: The calls a label with no kept listing is estimated at when no followed
#: label has one to average (U278), about a small label's roster.
UNLISTED_ESTIMATE = 100

#: How the interactive path gets its prompter, a module attribute so a suite
#: can hand in a scripted one.
PROMPTER: Callable[[], prompt.Prompter] = prompt.Prompter


def build_sync(parser, entry) -> None:
    parser.add_argument(
        "--next", dest="next_question", action="store_true",
        help="print the next label's question instead of asking it at the terminal",
    )
    parser.add_argument(
        "--answer", choices=ANSWERS, default=None,
        help="record this answer for the label named with --label",
    )
    parser.add_argument(
        "--label", default=None, metavar="NAME",
        help=(
            "with --answer, the favourite label the answer is for; with --next, "
            "the one label to ask about"
        ),
    )
    parser.add_argument(
        "--release", dest="releases", action="append", default=None, metavar="RELEASE_ID",
        help="with --answer pick, a release to take; repeat for more",
    )
    parser.add_argument(
        "--go", action="store_true",
        help=(
            "show one summary over every answer saved since the last go, ask the "
            "one gate, and on apply download what was answered for; under the run "
            "of a go that started a download, take that download on to its landing "
            "with no new question; refuses while the staging folder holds anything "
            "that is not the go's own, naming how to land it"
        ),
    )
    parser.set_defaults(_handler=label_sync)


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


def _refusal(reason: str, message: str, *steps: str, **extra: Any) -> CratekitError:
    return refuse(reason, message, steps=steps, origin=("label.sync",), **extra)


def _unusable(path, what: str) -> CratekitError:
    return _refusal(
        "label-sync-unusable",
        f"the label sync record at {path.name} could not be read ({what}), so "
        f"which releases each label was already asked about is unknown; treating "
        f"it as empty would ask every question again and lose every answer given",
        "repair or restore the label sync record before running label sync",
        scope=Scope.RUN, detail={"problem": what, "path": str(path)},
    )


def load_record(cfg: config.Config) -> dict[str, Any]:
    """The record as stored, or an empty one when none has been written.

    REFUSES A RECORD IT CANNOT READ rather than reading it as empty, which
    would ask every question again.
    """
    path = config.state_path("label_sync", cfg)
    raw = config.read_json_map(path, lambda why: _unusable(path, why))
    if raw is None:
        return {"version": RECORD_VERSION, "labels": {}, "answers": []}
    version = raw.get("version")
    if version != RECORD_VERSION:
        raise _unusable(
            path, f"it says version {version!r} and this build writes {RECORD_VERSION}"
        )
    held = raw.get("labels", {})
    answers = raw.get("answers", [])
    if not isinstance(held, Mapping) or not all(isinstance(one, Mapping) for one in held.values()):
        raise _unusable(path, "its labels are not a map of records")
    if not isinstance(answers, list):
        raise _unusable(path, "its answers are not a list")
    labels_held = {str(key): dict(value) for key, value in held.items()}
    return {"version": RECORD_VERSION, "labels": labels_held, "answers": list(answers)}


def write_record(cfg: config.Config, document: Mapping[str, Any]) -> None:
    """Write the record back. The caller holds :func:`record_lock`."""
    config.atomic_write_bytes(
        (json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        config.state_path("label_sync", cfg),
    )


@contextmanager
def record_lock(cfg: config.Config, doing: str) -> Iterator[None]:
    """The record's own lock, for a caller that reads, decides and writes as one step.

    BLOCKING, not refusing: a second go waits for the first to finish
    planning, and then sees the job the first one queued.
    """
    lock = config.exclusive_lock(config.state_path("label_sync_lock", cfg))
    try:
        lock.__enter__()
    except config.ConfigLockUnavailable as exc:
        raise _refusal(
            "label-sync-unusable",
            f"the label sync record could not be locked ({exc}), and {doing} "
            f"unlocked discards an answer another run is recording at the same time",
            "make the library state directory writable by this account",
            scope=Scope.RUN,
        ) from exc
    try:
        yield
    finally:
        lock.__exit__(None, None, None)


def unsettled(document: Mapping[str, Any]) -> list[tuple[int, Mapping[str, Any]]]:
    """Every saved answer no go has taken yet, with its place in the record."""
    return [
        (index, entry)
        for index, entry in enumerate(document["answers"])
        if isinstance(entry, Mapping) and not entry.get(SETTLED)
    ]


def settle_in(
    document: dict[str, Any], answers: Sequence[tuple[int, str, str]], *,
    marker: Mapping[str, Any], keep: Container[str] = frozenset(),
) -> int:
    """Mark, in ``document``, the saved answers a go took. Returns how many.

    The caller holds :func:`record_lock` and writes back with
    :func:`write_record`, so a go plans, queues and settles as one locked step.
    ``answers`` names each as ``(place, label, answered_at)``; one whose place
    now holds a different answer is left alone, and so is one that took a
    release named in ``keep``, for the next go.
    """
    entries = document["answers"]
    now = timestamp()
    count = 0
    for index, label_id, answered_at in answers:
        entry = entries[index] if index < len(entries) else None
        if not isinstance(entry, Mapping) or entry.get(SETTLED):
            continue
        if (
            _text(entry.get("label_id")) != label_id
            or _text(entry.get("answered_at")) != answered_at
        ):
            continue
        taken = entry.get("taken")
        if isinstance(taken, list) and any(one in keep for one in taken):
            continue
        entries[index] = {**entry, SETTLED: {**marker, "at": now}}
        count += 1
    return count


def _pending(document: Mapping[str, Any], label_id: str) -> Mapping[str, Any] | None:
    """The question saved for ``label_id`` and not yet answered, or None."""
    pending = (document["labels"].get(label_id) or {}).get("pending")
    return pending if isinstance(pending, Mapping) and pending.get("releases") else None


def asked_releases(document: Mapping[str, Any], label_id: str) -> frozenset[str]:
    """The identities a question about ``label_id`` already covered: the marker."""
    asked = (document["labels"].get(label_id) or {}).get("asked")
    if not isinstance(asked, list):
        return frozenset()
    return frozenset(str(one) for one in asked if isinstance(one, str) and one)


# ---------------------------------------------------------------------------
# A question
# ---------------------------------------------------------------------------

_OFFERED_FIELDS = ("identity", "artist", "title", "year", "tracks", "size", "item_id")


@dataclass(frozen=True, slots=True)
class Offered:
    """One release a question offers.

    ``item_id`` names the OPEN review item it already is, for the catch up,
    and is None for a release the listing found, filed only when taken.
    ``tracks`` and ``size`` are None when its tracks could not be read.
    """

    identity: str
    artist: str
    title: str
    year: str
    tracks: int | None
    size: int | None
    item_id: str | None
    payload: dict[str, Any]
    #: The release listed short of its declared count (R-515), as
    #: ``ListingShortfall.block`` carries it, or None for a full listing.
    short: dict[str, int] | None = None

    @property
    def provider_withheld(self) -> int:
        """Tracks the provider counts on this release and did not serve."""
        return int((self.short or {}).get("withheld") or 0)

    def to_json(self) -> dict[str, Any]:
        return {
            **{name: getattr(self, name) for name in _OFFERED_FIELDS},
            "payload": dict(self.payload),
            "shortfall": dict(self.short) if self.short else None,
        }

    @classmethod
    def from_json(cls, raw: Mapping[str, Any]) -> Offered:
        payload = raw.get("payload")
        return cls(
            *(str(raw.get(name) or "") for name in _OFFERED_FIELDS[:4]),
            tracks=count_of(raw.get("tracks")),
            size=count_of(raw.get("size")),
            item_id=str(raw["item_id"]) if raw.get("item_id") else None,
            payload=dict(payload) if isinstance(payload, Mapping) else {},
            short=_short_of(raw.get("shortfall")),
        )


def _short_of(raw: Any) -> dict[str, int] | None:
    """A saved shortfall block read back, or None when there is none to trust."""
    if not isinstance(raw, Mapping):
        return None
    block = {key: count_of(raw.get(key)) for key in ("declared", "listed", "withheld")}
    if any(value is None for value in block.values()) or not block["withheld"]:
        return None
    return {key: int(value or 0) for key, value in block.items()}


_QUESTION_HEAD = ("label_id", "label_name", "run", "listed_at")
_QUESTION_COUNTS = (
    "tracks", "size", "unknown", "provider_withheld",
    "beyond", "beyond_unchecked", "unread", "withheld", "unjudged",
)


@dataclass(frozen=True, slots=True)
class Question:
    """What one label is asked about, and the numbers a person judges it by."""

    label_id: str
    label_name: str
    run: str
    listed_at: str
    releases: tuple[Offered, ...]
    #: Releases past the window that may still be the label's (R-790, U238):
    #: see :attr:`sweep.LabelListing.beyond`.
    beyond: int = 0
    #: The part of ``beyond`` with no copyright line, so not yet checked (U238).
    beyond_unchecked: int = 0
    #: Listings of the label the crawl could not read (R-261).
    unread: int = 0
    #: Open review items the gate took back before this question was made.
    withheld: int = 0
    #: Releases offered that the gate has no word for.
    unjudged: int = 0

    @property
    def tracks(self) -> int:
        return sum(one.tracks or 0 for one in self.releases)

    @property
    def size(self) -> int:
        return sum(one.size or 0 for one in self.releases)

    @property
    def provider_withheld(self) -> int:
        """Tracks the provider counts on the offered releases and did not serve (R-515)."""
        return sum(one.provider_withheld for one in self.releases)

    @property
    def short_releases(self) -> int:
        """Releases that listed short of their declared count (R-515)."""
        return sum(1 for one in self.releases if one.provider_withheld)

    @property
    def unknown(self) -> int:
        """Releases whose tracks could not be read, so the counts leave them out."""
        return sum(1 for one in self.releases if one.tracks is None)

    def identities(self) -> tuple[str, ...]:
        return tuple(one.identity for one in self.releases)

    def to_json(self) -> dict[str, Any]:
        return {
            **{name: getattr(self, name) for name in _QUESTION_HEAD},
            "releases": [one.to_json() for one in self.releases],
            "new": len(self.releases),
            **{name: getattr(self, name) for name in _QUESTION_COUNTS},
            "answers": list(ANSWERS),
        }

    @classmethod
    def from_json(cls, raw: Mapping[str, Any]) -> Question:
        releases = raw.get("releases")
        beyond = count_of(raw.get("beyond")) or 0
        unchecked = count_of(raw.get("beyond_unchecked"))
        return cls(
            *(str(raw.get(name) or "") for name in _QUESTION_HEAD),
            releases=tuple(
                Offered.from_json(one)
                for one in (releases if isinstance(releases, list) else ())
                if isinstance(one, Mapping)
            ),
            beyond=beyond,
            # A QUESTION SAVED BEFORE U238 HAS NO SPLIT, so its ``beyond`` is read
            # whole as unchecked, a bound and never the label's; so is a split
            # that is present and unreadable.
            beyond_unchecked=beyond if unchecked is None else min(beyond, unchecked),
            **{name: count_of(raw.get(name)) or 0 for name in _QUESTION_COUNTS[-3:]},
        )


def _duration(row: Any) -> int | None:
    value = row.get("duration") if isinstance(row, Mapping) else getattr(row, "duration", None)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        return None
    return int(value)


def _measured(
    reader: catalogue.ReleaseTracks, identity: str
) -> tuple[int, int, catalogue.ListingShortfall | None] | None:
    """A release's track count, estimated size and shortfall (R-515), or None
    when unread, through the SHARED reader so no release is read twice. A
    ``CratekitError`` passes through: an expired session is the person's to act on.
    """
    try:
        rows, _year, short = reader.release_tracks(identity)
    except CratekitError:
        raise
    except Exception:  # noqa: BLE001 - counted as unread, never guessed at
        return None
    seconds = sum(_duration(row) or SECONDS_PER_TRACK for row in rows)
    return len(rows), seconds * BYTES_PER_SECOND, short


def size_text(size: int) -> str:
    """An estimate a person reads: whole megabytes, gigabytes past one."""
    if size >= 1_000_000_000:
        return f"{size / 1_000_000_000:.1f} GB"
    return f"{size / 1_000_000:.0f} MB"


@dataclass
class _Tools:
    """What one run shares across every label it lists, built on first use so a
    run that answers only a saved question logs in to nothing.

    One :class:`~cratekit.label.gate.Asking`, so an unreachable general
    catalogue is given up on once, one walk of the library, and the open
    label-release items grouped by the label the registry holds them under.
    """

    cfg: config.Config
    run_id: str
    followed: labels.Registry
    found: catalogue.Catalogue | None = None
    declared: Taxonomy | None = None
    asking: genre_gate.Asking = field(default_factory=genre_gate.Asking)
    _view: sweep.LibraryView | None = None
    open_items: dict[str, list[review.Item]] | None = None

    def catalogue(self) -> catalogue.Catalogue:
        if self.found is None:
            # THE DECLARATION BEFORE THE FIRST LOGIN (R-685), as the worker
            # reads it: an active taxonomy that cannot be read refuses here.
            self.declared = active_taxonomy.load(self.cfg)
            self.found = catalogue.resolve(self.cfg)
        return self.found

    def taxonomy(self) -> Taxonomy:
        if self.declared is None:
            self.declared = active_taxonomy.load(self.cfg)
        return self.declared

    def library(self) -> sweep.LibraryView:
        if self._view is None:
            self._view = match_cli.library_view(self.cfg)
        return self._view

    def open_for(self, store: review.ReviewStore, label_id: str) -> list[review.Item]:
        """The open label-release items filed under one label, read once per run,
        grouped by the identifier the registry holds the label under, so an item
        filed before the label's identifier moved (R-381) follows the move."""
        if self.open_items is None:
            grouped: dict[str, list[review.Item]] = {}
            page = review.list_items(store, queue=QUEUE, kinds=(sweep.KIND,), limit=None)
            for item in page.items:
                named = str(item.payload.get("label_id") or "")
                entry = self.followed.by_id(named) if named else None
                grouped.setdefault(entry.label_id if entry is not None else named, []).append(item)
            self.open_items = grouped
        return self.open_items.get(label_id, [])


@dataclass(frozen=True, slots=True)
class _Listed:
    """What listing one label produced: a question, nothing to ask, or a skip."""

    question: Question | None = None
    skipped: str | None = None
    listing: sweep.LabelListing | None = None
    #: Open items the gate took back, counted when no question was left to
    #: carry the count, so the run still reports what it wrote.
    withheld: int = 0


def _offered(
    reader: catalogue.ReleaseTracks, identity: str, payload: Mapping[str, Any], year: str,
    item_id: str | None = None,
) -> Offered:
    """One release as a question offers it, measured unless an open item names no release."""
    unnamed = item_id is not None and identity.startswith("item:")
    measured = _measured(reader, identity) if not unnamed else None
    tracks, size, short = measured or (None, None, None)
    return Offered(
        identity, _text(payload.get("artist")), _text(payload.get("title")), year, tracks, size,
        item_id, dict(payload), short.block() if short else None,
    )


def _question_for(
    tools: _Tools, store: review.ReviewStore, entry: labels.LabelEntry, asked: Container[str]
) -> _Listed:
    """List one label as the sweep would and build its question, or say why not.

    THE SWEEP'S OWN SOURCE, with ``asked`` taking places in the offer window
    beside the queued releases; its gate records every hold, so a release held
    here is held for the next sweep too. A CATALOGUE THAT CONFIRMS NOTHING IS
    NOT A LABEL WITH NOTHING NEW (the worker's ``_refuse_unfinished``), so such
    a label is skipped with the reason and its marker does not move.
    """
    found = tools.catalogue()
    declared = tools.taxonomy()
    reader = catalogue.ReleaseTracks(found)
    source = sweep.LabelSource(
        tools.cfg, registry=labels.Registry(labels={entry.label_id: entry}), catalogue=found,
        store=store, owned=sweep.OwnedReleases(tools.cfg, reader, library=tools.library),
        gate=genre_gate.SweepGate(
            declared, tracks=reader.release_tracks, standing=genre_gate.StandingHolds(store),
            asking=tools.asking,
        ),
        run_id=tools.run_id, offered=asked,
    )
    try:
        candidates = source.list_recent(-1)
    except run.LookupFailure as exc:
        return _Listed(skipped=f"its catalogue could not be listed: {exc}")
    ((_swept, listing),) = source.listings
    unconfirmed = len(source.dropped) + source.held_unconfirmed
    if not candidates and source.dropped and unconfirmed == source.read:
        why = (
            f"the listing read {unconfirmed} release(s) from the catalogue and could "
            f"not confirm a single one of them, so this is not a label with nothing "
            f"new; what failed is verification rather than reach, and the registry's "
            f"--match needle is the usual repair"
        )
        return _Listed(skipped=why, listing=listing)
    releases = [
        _offered(reader, one.identity, dict(one.payload or {}), str(one.recency or ""))
        for one in candidates
    ]

    # THE CATCH UP: this label's open items, offered once under the same
    # question, judged first from the words they recorded with no request; one
    # the gate would now hold is taken back as ``label judge`` takes one back.
    # A release a person returned is theirs and is not judged.
    withheld = unjudged = 0
    for item in tools.open_for(store, entry.label_id):
        standing = review.find_hold(store, queue=QUEUE, item_id=item.item_id)
        if not genre_gate.returned_by(standing, item.payload):
            words = genre_gate.recorded_genres(item.payload, genre_gate.GENRES_FIELD)
            judged = genre_gate.judge_recorded(declared, entry.kind, words)
            if judged is None or judged.verdict is KindVerdict.NOT_JUDGED:
                unjudged += 1
            elif judged.held:
                taken_back = review.withhold(
                    store, item.item_id, group=entry.label_id, name=entry.name,
                    reason=judged.reason, detail=judged.detail(), run_id=tools.run_id,
                )
                if taken_back is not None:
                    withheld += 1
                    continue
        identity = genre_gate.release_id_of(store, item) or f"item:{item.item_id}"
        year = _text(item.payload.get("year")) or _text(item.payload.get("recency"))
        releases.append(_offered(reader, identity, item.payload, year, item.item_id))
    if not releases:
        return _Listed(listing=listing, withheld=withheld)
    # WHAT THE WINDOW DID NOT REACH IS RECORDED, as the sweep records it, so
    # ``review list --group-by label`` says how much more the label could offer.
    review.record_round(
        store, queue=QUEUE, run_id=tools.run_id, group=entry.label_id, name=entry.name,
        beyond=listing.beyond,
    )
    return _Listed(listing=listing, question=Question(
        entry.label_id, entry.name, tools.run_id, timestamp(), tuple(releases),
        beyond=listing.beyond,
        beyond_unchecked=listing.beyond_unchecked,
        unread=len(listing.unread), withheld=withheld, unjudged=unjudged,
    ))


def _save_pending(cfg: config.Config, question: Question) -> None:
    """Save the question under its label BEFORE it is asked, so an answer from
    either path applies to exactly what was shown and ``--next`` can print it
    again with no provider call."""
    with record_lock(cfg, "saving a question"):
        document = load_record(cfg)
        held = dict(document["labels"].get(question.label_id) or {})
        held.update(name=question.label_name, pending=question.to_json())
        document["labels"][question.label_id] = held
        write_record(cfg, document)


# ---------------------------------------------------------------------------
# An answer
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Answered:
    """What recording one answer did."""

    label_id: str
    label_name: str
    answer: str
    offered: int
    taken: tuple[Offered, ...]
    #: Releases picked that had left review, or been decided, between the
    #: question and the answer, so they were not taken.
    left: tuple[str, ...] = ()
    removed: bool = False

    def to_json(self) -> dict[str, Any]:
        return {
            "label_id": self.label_id, "label_name": self.label_name, "answer": self.answer,
            "offered": self.offered, "taken": [one.identity for one in self.taken],
            "tracks": sum(one.tracks or 0 for one in self.taken),
            "size": sum(one.size or 0 for one in self.taken),
            "left": list(self.left), "removed": self.removed,
        }


def _selection_invalid(message: str, *steps: str, **detail: Any) -> CratekitError:
    return _refusal("review-selection-invalid", message, *steps, detail=detail)


def _take(store: review.ReviewStore, one: Offered, run_id: str) -> bool:
    """Record one release as accepted, filing it first under the sweep's key
    when it was never filed, so ``label approved`` reads it as any accepted release.

    One that LEFT REVIEW or was DECIDED between the question and the answer is
    not taken, and False says so; an accepted one is already what was asked.
    """
    if one.item_id is None:
        candidate = run.Candidate(one.identity, one.year, dict(one.payload))
        item = sweep.offer_release(store, candidate, run_id=run_id)
    else:
        item = review.find(store, one.item_id)
        if item is None:
            return False
    if item.verdict is Verdict.ACCEPTED:
        return True
    if item.stored_verdict is not None:
        return False
    review.resolve(store, item.item_id, Verdict.ACCEPTED, actor=ACTOR)
    return True


def _chosen(
    question: Question, entry: labels.LabelEntry, answer: str, picks: Sequence[str]
) -> list[Offered]:
    """The releases an answer takes, refusing a pick the question did not offer."""
    offered = {one.identity for one in question.releases}
    wanted = dict.fromkeys(str(pick).strip() for pick in picks if str(pick).strip())
    if answer == PICK:
        unknown = [pick for pick in wanted if pick not in offered]
        if unknown or not wanted:
            raise _selection_invalid(
                (
                    f"{', '.join(repr(one) for one in unknown)} "
                    f"{'is' if len(unknown) == 1 else 'are'} not among the "
                    f"{len(offered)} release(s) the question for {entry.name!r} "
                    f"offered, so picking would record a choice nobody was shown"
                    if unknown
                    else f"pick names at least one of the {len(offered)} release(s) "
                    f"the question for {entry.name!r} offered; to take none, "
                    f"answer not-now"
                ),
                f"take the identifiers from: crate label sync --next --label {entry.label_id}",
                label=entry.label_id,
                unknown=unknown,
            )
    elif wanted:
        raise _selection_invalid(
            f"--release goes with --answer pick, and {answer} would ignore the "
            f"{len(wanted)} named",
            "drop --release, or answer pick",
            label=entry.label_id,
        )
    return [
        one
        for one in question.releases
        if answer == ALL or (answer == PICK and one.identity in wanted)
    ]


def record_answer(
    cfg: config.Config, store: review.ReviewStore, entry: labels.LabelEntry, answer: str,
    picks: Sequence[str], *, run_id: str,
) -> Answered:
    """Record one answer for one label, against the question saved for it.

    UNDER THE RECORD'S LOCK FOR THE WHOLE OF IT. The review writes come first
    and the record last, so a review write that refuses leaves the question
    pending, and ``stop`` removes the label through the registry's own path
    after them. EVERY ANSWER MOVES THE MARKER over every release offered,
    ``not-now`` included: a release answered once never returns.
    """
    if answer not in ANSWERS:
        raise _selection_invalid(
            f"{answer!r} is not an answer label sync records",
            f"answer with one of: {', '.join(ANSWERS)}",
            answer=answer,
        )
    with record_lock(cfg, "recording an answer"):
        document = load_record(cfg)
        held = dict(document["labels"].get(entry.label_id) or {})
        pending = _pending(document, entry.label_id)
        if pending is None:
            # STOP WITH NOTHING WAITING names the registry's remove, since
            # ``--next`` asks nothing about a label with nothing new.
            raise _selection_invalid(
                f"no question is waiting for {entry.name!r}, so there is nothing an "
                f"answer could apply to; nothing was recorded",
                (
                    f"to stop following it with nothing to answer: crate label "
                    f"registry remove {entry.label_id}"
                    if answer == STOP
                    else f"ask it first with: crate label sync --next --label {entry.label_id}"
                ),
                label=entry.label_id,
            )
        question = Question.from_json(pending)
        taken: list[Offered] = []
        left: list[Offered] = []
        # FILED UNDER THE RUN THAT ASKED, which recorded the label's round.
        filing_run = question.run or run_id
        for one in _chosen(question, entry, answer, picks):
            (taken if _take(store, one, filing_run) else left).append(one)
        taken_ids = {one.identity for one in taken}
        # SETTLED BY THE ID EACH RELEASE FILES UNDER, so a release a sweep filed
        # while the question waited is settled too; ``supersede`` passes over an
        # id nothing filed and one already decided.
        superseded = [
            one.item_id or genre_gate.release_item_id(one.identity)
            for one in question.releases if one.identity not in taken_ids
        ]
        review.supersede(store, superseded, rule=ANSWERED_RULE)
        removed = labels.RegistryStore().remove(entry.label_id) if answer == STOP else False
        now = timestamp()
        asked = set(asked_releases(document, entry.label_id)) | set(question.identities())
        held.pop("pending", None)
        held.update(name=entry.name, asked=sorted(asked), asked_at=now, answer=answer, run=run_id)
        document["labels"][entry.label_id] = held
        result = Answered(
            entry.label_id, entry.name, answer, len(question.releases), tuple(taken),
            left=tuple(one.identity for one in left), removed=removed,
        )
        document["answers"].append({
            **result.to_json(), "run": run_id, "asked_run": question.run, "answered_at": now,
            "releases": [one.to_json() for one in taken],
        })
        write_record(cfg, document)
    return result


# ---------------------------------------------------------------------------
# The envelope
# ---------------------------------------------------------------------------


_check = partial(review_common.check, "label.sync")
_text = review_common.text


def _named(one: Offered) -> str:
    said = f"{one.artist} - {one.title}" if one.artist else one.title or one.identity
    return said + (f" ({one.year})" if one.year else "")


def _tracks_said(one: Offered) -> str:
    """One release's track count as a person reads it, a short listing said (R-515)."""
    if one.tracks is None:
        return "tracks unread"
    said = f"{one.tracks} track(s)"
    if one.short:
        said += (
            f" ({one.short['declared']} declared, {one.short['listed']} listed, "
            f"{one.short['withheld']} withheld by the provider)"
        )
    return said


def _past_window(beyond: int, unchecked: int) -> str:
    """What lies past the window, as a count of the label's and a bound on the rest (U238).

    The unchecked part has no copyright line, so it is only a bound and never
    called the label's. Nothing past the window says nothing, never "0 more".
    """
    unchecked = max(0, min(unchecked, beyond))
    own = beyond - unchecked
    said = f"{own} more of the label's release(s) past this run's window" if own else ""
    if unchecked and own:
        said += f", and up to {unchecked} more not yet checked"
    elif unchecked:
        said = f"up to {unchecked} more past this run's window, not yet checked"
    return said


def _counts(question: Question) -> str:
    said = (
        f"{len(question.releases)} new release(s), {question.tracks} track(s), "
        f"about {size_text(question.size)}"
    )
    past = _past_window(question.beyond, question.beyond_unchecked)
    for count, more in (
        (question.unknown, f", {question.unknown} with tracks unread"),
        (question.provider_withheld, f"; {question.provider_withheld} track(s) withheld by "
         f"the provider on {question.short_releases} release(s), counted but not listed"),
        (past, f"; {past}"),
        (question.unread, f"; {question.unread} listing(s) of the label could not be read"),
        (question.withheld, f"; {question.withheld} open item(s) taken back by the genre gate"),
        (question.unjudged, f"; {question.unjudged} the genre gate has no word for"),
    ):
        if count:
            said += more
    return said


def _release_said(one: Offered) -> str:
    return f"{_named(one)}, {_tracks_said(one)}" + (", waiting in review" if one.item_id else "")


def _question_checks(question: Question, *, how: str) -> list[dict[str, Any]]:
    name = question.label_name
    return [
        _check(f"question.{question.label_id}", "info", f"{name}: {_counts(question)}; {how}"),
        *(
            _check(f"release.{one.identity}", "info", f"{name}: {_release_said(one)}")
            for one in question.releases
        ),
    ]


def _answer_check(answered: Answered) -> dict[str, Any]:
    if answered.answer == STOP:
        what = (
            f"no longer followed, and its {answered.offered} release(s) answered"
            if answered.removed
            else f"was already gone from the registry; its {answered.offered} "
            f"release(s) answered"
        )
    elif answered.answer == NOT_NOW:
        what = f"not now, {answered.offered} release(s) answered and none taken"
    else:
        what = (
            f"{answered.answer}, {len(answered.taken)} of {answered.offered} release(s) "
            f"taken and recorded accepted"
        )
    if answered.left:
        what += (
            f"; {len(answered.left)} picked release(s) had been decided or had left "
            f"review since the question and were not taken: {', '.join(answered.left)}"
        )
    return _check(f"answered.{answered.label_id}", "ok", f"{answered.label_name}: {what}")


def _nothing_check(entry: labels.LabelEntry, listed: _Listed) -> dict[str, Any]:
    detail = f"{entry.name}: nothing new since it was last asked"
    if listed.listing is not None:
        past = _past_window(listed.listing.beyond, listed.listing.beyond_unchecked)
        if past:
            detail += f"; {past}"
    if listed.withheld:
        detail += f"; {listed.withheld} open item(s) taken back by the genre gate"
    return _check(f"label.{entry.label_id}", "ok", detail)


def _listing_checks(entry: labels.LabelEntry, listed: _Listed) -> list[dict[str, Any]]:
    """Where a listing this run made came from (U217), and the release it
    re-verified (U277), with what the verifier answered and how (R-1634)."""
    listing = listed.listing
    if listing is None:
        return []
    said: list[dict[str, Any]] = []
    if listing.kept is not None:
        said.append(
            _check(f"listing.{entry.label_id}", "info", f"{entry.name}: {listing.kept.said()}")
        )
    if listing.canary is not None:
        said.append(_check(
            f"reverified.{entry.label_id}", "info",
            f"{entry.name}: every release the listing asked about was turned down, "
            f"so one already asked about or in review was verified again, "
            f"{listing.canary.how()}: {listing.canary.said()}",
        ))
    return said


def _unasked(
    entry: labels.LabelEntry, listed: _Listed, checks: list[dict[str, Any]],
    seen: list[dict[str, Any]], nothing: list[str] | None = None,
) -> bool:
    """Report a label listed with no question, skipped or with nothing new, and
    say True; False when it has a question to ask."""
    if listed.skipped is not None:
        said = f"{entry.name}: not asked; {listed.skipped}"
        checks.append(_check(f"label.{entry.label_id}", "fail", said))
        state = "skipped"
    elif listed.question is None:
        checks.append(_nothing_check(entry, listed))
        if nothing is not None:
            nothing.append(entry.name)
        state = "nothing-new"
    else:
        return False
    checks.extend(_listing_checks(entry, listed))
    seen.append({"label_id": entry.label_id, "state": state})
    return True


def _summary(
    *, question: Question | None = None, answered: Sequence[Answered] = (),
    labels_seen: Sequence[dict[str, Any]] = (), stopped_at: str | None = None,
) -> dict[str, Any]:
    return {
        "question": question.to_json() if question is not None else None,
        "answered": [one.to_json() for one in answered],
        "labels": list(labels_seen),
        "stopped_at": stopped_at,
    }


def _followed_or_refuse() -> labels.Registry:
    followed = labels.RegistryStore().load()
    if followed.labels:
        return followed
    raise _refusal(
        "label-registry-empty",
        "no favourite label is registered, so there is no label to ask about",
        "register a label with: crate label registry add <name>",
    )


def _entry_or_refuse(followed: labels.Registry, name: str) -> labels.LabelEntry:
    entry = followed.resolve(name)
    if entry is not None:
        return entry
    raise _refusal(
        "label-unknown", f"no favourite label is named {name!r}",
        "list the registry and take the name from it", detail={"name": name},
    )


# ---------------------------------------------------------------------------
# The three paths
# ---------------------------------------------------------------------------


def _estimate(
    entries: Sequence[labels.LabelEntry], document: Mapping[str, Any]
) -> tuple[int, int]:
    """The calls a walk over ``entries`` may make at most, and how many labels it
    may list (U278): each kept listing's aged answers, the mean size for a label
    with none (or :data:`UNLISTED_ESTIMATE`), ending at a saved question."""
    costs: list[kept_listing.Cost | None] = []
    for entry in entries:
        if _pending(document, entry.label_id) is not None:
            break
        costs.append(kept_listing.cost(entry))
    known = [one for one in costs if one is not None]
    each = math.ceil(sum(one.held for one in known) / len(known)) if known else UNLISTED_ESTIMATE
    return sum(one.aged for one in known) + (len(costs) - len(known)) * each, len(costs)


def _sweep_check(
    cfg: config.Config, entries: Sequence[labels.LabelEntry], document: Mapping[str, Any]
) -> dict[str, Any]:
    """Say what a walk over every followed label may cost, or refuse it before
    its first call when the account's hour cannot hold it outside the reserve (U278).

    The label crawl is the account's (U205). A gate file that cannot be read
    is read as the gate reads it, as nothing spent, and said.
    """
    calls, listed = _estimate(entries, document)
    line = provider_gate.line_for(provider_gate.GateSettings.from_config(cfg))
    standing = provider_gate.read_standing()
    spent = standing.spent(provider_gate.ACCOUNT) if standing is not None else 0
    left = max(0, line - spent)
    unread = "" if standing is not None else " (the gate's file could not be read, so as none spent)"
    labels_said = "label" if listed == 1 else "labels"
    if calls > left:
        # THE MOMENT THE WINDOW HOLDS AT MOST ``line - calls``; an estimate past
        # the whole line never fits, and says so.
        at = line - calls + 1
        wait = (
            f"or wait until {provider_gate.iso(standing.frees_at(provider_gate.ACCOUNT, at))}, "
            "when the hour holds it"
            if standing is not None and calls <= line
            else "or raise the hour's budget for one run with crate --calls-per-hour N "
            "before the verb"
        )
        raise _refusal(
            provider_gate.BUDGET,
            f"walking the followed labels may ask the streaming provider about {calls} "
            f"calls over {listed} {labels_said}, an estimate from each label's kept "
            f"listing, and the account has {left} of its {line} read calls left this "
            f"hour{unread}, the rest kept for writes and downloads; nothing was asked",
            "ask about one label at a time with: crate label sync --next --label NAME",
            wait,
            scope=Scope.RUN,
            detail={"estimate": calls, "labels": listed, "left": left, "line": line,
                    "spent": spent},
        )
    return _check(
        "estimate",
        "info",
        f"about {calls} calls to the streaming provider over {listed} {labels_said}, "
        f"an estimate from each label's kept listing; the account has {left} of its "
        f"{line} read calls left this hour{unread}",
    )


def _next(ctx, cfg: config.Config, name: str | None = None) -> Envelope:
    """Print the next question in registry order, saving it, and ask nothing.

    A saved question is printed again with no provider call. ONE LABEL NAMED IS
    THE ONLY LABEL TOUCHED (U189). A LABEL THAT COULD NOT BE READ IS NOT A LABEL
    WITH NOTHING NEW (R-1114): a run whose every label was skipped refuses.
    """
    followed = _followed_or_refuse()
    only = _entry_or_refuse(followed, name) if name is not None else None
    entries = [only] if only is not None else list(followed.labels.values())
    tools = _Tools(cfg=cfg, run_id=ctx.run.run_id, followed=followed)
    document = load_record(cfg)
    seen: list[dict[str, Any]] = []
    # A WALK OVER EVERY LABEL SAYS ITS COST FIRST (U278); one label named is
    # one listing, held by the gate call by call like any other.
    checks = [_sweep_check(cfg, entries, document)] if only is None else []
    withheld = 0
    nothing: list[str] = []
    with review.open_store(cfg) as store:
        for entry in entries:
            pending = _pending(document, entry.label_id)
            if pending is not None:
                question = Question.from_json(pending)
            else:
                listed = _question_for(tools, store, entry, asked_releases(document, entry.label_id))
                withheld += listed.withheld
                if _unasked(entry, listed, checks, seen, nothing):
                    continue
                question = listed.question
                _save_pending(cfg, question)
                checks.extend(_listing_checks(entry, listed))
            seen.append({"label_id": entry.label_id, "state": "asked"})
            checks.extend(_question_checks(question, how=(
                f"answer with: crate label sync --answer all --label "
                f"{entry.label_id}, or pick with --release, or not-now, or stop"
            )))
            return review_common.ended(ctx, checks, _summary(question=question, labels_seen=seen))
    data = {"checks": checks, "summary": _summary(labels_seen=seen)}
    if not nothing:
        # EVERY LABEL ASKED ABOUT WAS SKIPPED (R-1114), the ``no-evidence`` rule:
        # the run refuses with its own checks as the data, so each label's line
        # still says why. THE REMEDY IS A LINE OF ITS OWN, because the human
        # rendering shows only a refusal's summary when the run carries checks.
        checks.append(_check("next", "info", _UNLISTED_REMEDY))
        return from_cause(
            verb=ctx.entry.name,
            run_id=ctx.run.run_id,
            started=ctx.started,
            cause=_unlisted_cause(entries),
            data=data,
        )
    if only is None:
        # THE CLOSING LINE SPEAKS ONLY FOR THE LABELS THAT WERE LISTED (R-1114).
        said = (
            "no label has anything new to ask about"
            if len(nothing) == len(entries)
            else f"no label listed has anything new to ask about: {', '.join(nothing)}"
        )
        checks.append(_check("question", "ok", said))
    return ctx.envelope(
        data=data,
        # NO_OP only when nothing was written: an open item the gate took
        # back has left review even when no question was left to ask.
        outcome=Outcome.OK if withheld else Outcome.NO_OP,
    )


#: What to do about a label ``--next`` could not read, by why it could not.
_UNLISTED_STEPS = (
    "a catalogue that could not be listed: run crate doctor, then ask again "
    "when the provider answers",
    "a listing that confirmed nothing: check the label's --match needle "
    "with: crate label registry",
)
_UNLISTED_REMEDY = "; ".join(_UNLISTED_STEPS)


def _unlisted_cause(entries: Sequence[labels.LabelEntry]) -> Cause:
    """The refusal for a ``--next`` whose every label was skipped, as a cause."""
    names = ", ".join(entry.name for entry in entries)
    which = (
        f"the label asked about could not be read ({names}), so whether it has"
        if len(entries) == 1
        else f"none of the {len(entries)} labels asked about could be read ({names}), "
        f"so whether any of them has"
    )
    return _refusal(
        "label-sync-unlisted",
        f"{which} anything new is unknown; no question was asked or saved",
        "read each label's line for why it was not asked", *_UNLISTED_STEPS,
        retryable=True,
        detail={"labels": [entry.label_id for entry in entries]},
    ).cause


def _answer(ctx, cfg: config.Config) -> Envelope:
    """Record the one answer named on the command line."""
    entry = _entry_or_refuse(_followed_or_refuse(), str(ctx.args.label))
    with review.open_store(cfg) as store:
        answered = record_answer(
            cfg, store, entry, str(ctx.args.answer), list(ctx.args.releases or ()),
            run_id=ctx.run.run_id,
        )
    return review_common.ended(ctx, [
        _answer_check(answered),
        _check("next", "info", "the next question: crate label sync --next"),
    ], _summary(answered=[answered]))


def _question_text(question: Question) -> str:
    numbered = enumerate(question.releases, start=1)
    return f"\n{question.label_name}: {_counts(question)}\n" + "".join(
        f"  {number:>3}. {_release_said(one)}\n" for number, one in numbered
    )


def _ask(prompter: prompt.Prompter, question: Question) -> tuple[str, list[str]]:
    """Put one question to a person and return the answer and, for a pick, the releases.

    NO DEFAULT: an empty line is asked again, because every answer moves the
    marker and an accidental return must not. ``quit`` leaves the label
    unanswered; a word outside the set is asked again,
    :data:`prompt.MAX_ATTEMPTS` times, then the prompt is given up on.
    """
    prompter.write(_question_text(question))
    words = (*ANSWERS, QUIT)
    for _ in range(prompt.MAX_ATTEMPTS):
        answer = prompter.ask(f"Answer ({', '.join(words)})").lower()
        if answer not in words:
            prompter.write(f"  {answer!r} is not one of {', '.join(words)}\n")
            continue
        if answer != PICK:
            return answer, []
        picked = _pick(prompter, question)
        if picked is not None:
            return PICK, picked
    raise prompt.PromptUnavailable(f"no usable answer for {question.label_name!r}")


def _pick(prompter: prompt.Prompter, question: Question) -> list[str] | None:
    """The releases a person picks, by number, or None when nothing usable was typed."""
    count = len(question.releases)
    for _ in range(prompt.MAX_ATTEMPTS):
        typed = prompter.ask("Which releases? numbers, separated by spaces")
        numbers: list[int] = []
        bad: list[str] = []
        for word in typed.replace(",", " ").split():
            # ``isdecimal``, not ``isdigit``: a superscript two is a digit ``int`` refuses.
            if word.isdecimal() and 1 <= int(word) <= count:
                numbers.append(int(word))
            else:
                bad.append(word)
        if bad or not numbers:
            prompter.write(
                f"  {', '.join(bad) if bad else 'nothing'} is not a release number "
                f"between 1 and {count}\n"
            )
            continue
        return [question.releases[number - 1].identity for number in dict.fromkeys(numbers)]
    return None


def _unanswerable(entry: labels.LabelEntry, answered: Sequence[Answered], exc) -> CratekitError:
    return _refusal(
        "label-sync-unanswerable",
        f"the question about {entry.name!r} could not be answered at this "
        f"terminal ({exc}); the {len(answered)} answer(s) given before it are "
        f"saved and the question is waiting",
        f"run label sync from a terminal, or drive it with: crate label "
        f"sync --next --label {entry.label_id}, then crate label sync "
        f"--answer ANSWER --label {entry.label_id}",
        detail={"label": entry.label_id, "answered": [one.label_id for one in answered]},
    )


def _walk(ctx, cfg: config.Config, prompter: prompt.Prompter) -> Envelope:
    """Ask every label with something new, in registry order, answer by answer.

    EVERY LABEL IS LISTED AFRESH, a saved question included, since the walk can
    wait for a person and should ask what the catalogue holds now (through the
    roster's kept listing, U217). A run that stops, by ``quit`` or a prompt
    nobody can answer, has saved every answer given before it.
    """
    followed = _followed_or_refuse()
    entries = list(followed.labels.values())
    tools = _Tools(cfg=cfg, run_id=ctx.run.run_id, followed=followed)
    answered: list[Answered] = []
    seen: list[dict[str, Any]] = []
    # Every label is listed afresh, so the estimate is asked over an empty record (U278).
    checks = [_sweep_check(cfg, entries, {"labels": {}})]
    stopped_at: str | None = None
    withheld = 0
    with review.open_store(cfg) as store:
        for entry in entries:
            document = load_record(cfg)
            listed = _question_for(tools, store, entry, asked_releases(document, entry.label_id))
            withheld += listed.withheld
            if _unasked(entry, listed, checks, seen):
                continue
            checks.extend(_listing_checks(entry, listed))
            _save_pending(cfg, listed.question)
            try:
                answer, picks = _ask(prompter, listed.question)
            except prompt.PromptUnavailable as exc:
                raise _unanswerable(entry, answered, exc) from exc
            if answer == QUIT:
                stopped_at = entry.label_id
                seen.append({"label_id": entry.label_id, "state": "unanswered"})
                said = f"{entry.name}: left unanswered; the next run asks again"
                checks.append(_check(f"label.{entry.label_id}", "info", said))
                break
            result = record_answer(cfg, store, entry, answer, picks, run_id=ctx.run.run_id)
            answered.append(result)
            seen.append({"label_id": entry.label_id, "state": "answered"})
            checks.append(_answer_check(result))
    went = f"; stopped at {stopped_at}, run label sync again to go on" if stopped_at else (
        "; every label is answered"
    )
    checks.append(_check("run", "info", f"{len(answered)} label(s) answered{went}"))
    data = {
        "checks": checks,
        "summary": _summary(answered=answered, labels_seen=seen, stopped_at=stopped_at),
    }
    if stopped_at is None:
        # EVERY LABEL WITH SOMETHING NEW IS ANSWERED, so the walk ends at the
        # one gate over the summary of every saved answer (U108). THE ESTIMATE
        # IS NOT AN ANSWER (U278), so it is left out of what the gate shows.
        walk = [one["detail"] for one in checks if one["key"] != _ESTIMATE_KEY]
        return _go(ctx, cfg, walk=walk, data=data, wrote=bool(answered or withheld))
    return ctx.envelope(
        data=data,
        # A QUESTION LEFT UNANSWERED IS STILL A RUN THAT WROTE: the question was
        # saved and its round recorded. NO_OP is a run that wrote nothing.
        outcome=Outcome.OK if answered or stopped_at or withheld else Outcome.NO_OP,
    )


def _go(ctx, cfg: config.Config, **kwargs: Any) -> Envelope:
    """The go, imported here because :mod:`cratekit.label.go` imports this module
    for the record, and a module scope import each way is a cycle."""
    from cratekit.label import go  # noqa: PLC0415 - see the docstring

    # THE GO SPENDS THE RESERVE (U278), the walk's go too.
    with provider_gate.spending():
        return go.go(ctx, cfg, **kwargs)


def label_sync(ctx) -> Envelope:
    """Ask label by label at the terminal, print one question, record one answer, or go."""
    args = ctx.args
    if args.go and (args.answer is not None or args.next_question):
        raise _selection_invalid(
            "--go asks the one gate over the answers already saved, and --next and "
            "--answer each do something else; one invocation does one",
            "run them one at a time",
        )
    if args.answer is not None and args.next_question:
        raise _selection_invalid(
            "--next prints a question and --answer records one; one invocation does one",
            "run them one at a time",
        )
    if args.answer is not None:
        if not args.label:
            raise _selection_invalid(
                f"--answer {args.answer} needs the label it answers for, and guessing "
                f"one would record an answer for a label nobody named",
                "pass --label with the label's name or identifier",
            )
        if args.answer == PICK and not args.releases:
            raise _selection_invalid(
                "--answer pick needs the releases to take; to take none, answer not-now",
                f"pass --release RELEASE_ID for each release, from: crate label sync "
                f"--next --label {args.label!r}",
            )
    elif args.next_question and args.label is not None and not args.label.strip():
        raise _selection_invalid(
            "--label with --next names the one label to ask about, and an empty name "
            "names none",
            "pass --label with the label's name or identifier, or drop it to ask the "
            "next label with something new",
        )
    elif args.next_question and args.releases:
        raise _selection_invalid(
            "--release goes with --answer pick, and --next would ignore the releases "
            "it names",
            "drop --release to print the question, then answer with: crate label sync "
            "--answer pick --label NAME --release RELEASE_ID",
        )
    elif not args.next_question and (args.label is not None or args.releases):
        raise _selection_invalid(
            "--label and --release go with --answer, and --label with --next, and "
            "without one they would name a label nothing is recorded for",
            "to ask about one label: crate label sync --next --label NAME",
            "to record an answer, pass --answer; or drop them to ask at the terminal",
        )
    cfg = label_cli._load()
    # ONLY THE GO SPENDS THE HOUR'S RESERVE (U278). Asking, answering and the
    # walk stop where every read stops, and a ``--calls`` past the hour's budget
    # is refused here, before the first call.
    if args.go:
        return _go(ctx, cfg)
    provider_gate.reading(provider_gate.GateSettings.from_config(cfg))
    if args.answer is not None:
        return _answer(ctx, cfg)
    if args.next_question:
        return _next(ctx, cfg, args.label)
    return _walk(ctx, cfg, PROMPTER())


__all__ = [
    "ACTOR", "ALL", "ANSWERED_RULE", "ANSWERS", "BYTES_PER_SECOND", "NOT_NOW", "PICK", "QUIT",
    "RECORD_VERSION", "SECONDS_PER_TRACK", "SETTLED", "UNLISTED_ESTIMATE", "STOP", "Answered",
    "Offered", "Question", "asked_releases", "build_sync", "label_sync", "load_record",
    "record_answer", "record_lock", "settle_in", "size_text", "unsettled", "write_record",
]
