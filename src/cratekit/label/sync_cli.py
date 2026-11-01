"""``label.sync``: ask, label by label, about what is new, and record each answer.

U107, the asking half of the guided label sync brainstormed with the author on
2026-10-02 (``docs/ideation/2026-10-02-guided-label-sync.md``). Following a
label was meant to bring in its new music and instead filled review with back
catalogue: 2,416 label releases waited there that day. This verb walks the
favourite labels one at a time and asks, per label, about the releases that are
new since that label was last asked, with four answers: download all new, pick
releases, not now, stop following. Every answer is saved as it is given.
Asking downloads nothing. Once every label with something new is answered, the
walk ends at one gate over one summary of the saved answers, and ``--go`` asks
the same gate over answers already saved; U108's :mod:`cratekit.label.go` is
what a yes runs.

THE MARKER IS A SET OF RELEASE IDENTITIES, NOT A DATE, and it lives in LIBRARY
state. The catalogue dates a release by year alone and KTD11 forbids a date
floor, so "new since this label was last asked" is "not in the set of releases
a question already covered". The set takes places in the sweep's offer window
exactly as a queued release does (R-790), which is what keeps back catalogue
from returning: a label whose newest releases were all asked about offers
nothing, and a release published since takes the one place above them. This
reverses R-140's no cursor design for the labels source on purpose: the sweep
only offered, this verb asks, and an answer is the event the marker records.
Library state because what was asked depends on this library's holdings and
its review queue, and a copy run redirects library state so a rehearsal cannot
move the live marker; COUPLED because a restore that puts the review queue
back must put the asked set back with it.

THE LISTING IS THE SWEEP'S, AND THE GENRE GATE RUNS BEFORE A LABEL IS ASKED.
One :class:`~cratekit.label.sweep.LabelSource` per label, built as the worker
builds it, with the same ownership reader and the same
:class:`~cratekit.label.gate.SweepGate`, so a release the gate would not have
filed is held and never reaches a question, and a hold already standing stays
held. A label's OPEN review items are offered under the same question, once,
which is the first run's catch up: one whose recorded words the gate would now
hold is taken back the way ``label judge`` takes one back, with no request made,
and one the gate has no word for is offered unjudged and counted as such.

A QUESTION IS SAVED BEFORE IT IS ASKED, so the structured path answers exactly
what was shown. ``--next`` prints the next pending question and ``--answer``
records one answer for one named label; the interactive path does the same two
things inline. Both write the same saved answer, and a label answered once is
not asked about those releases again. ``all`` and ``pick`` file each taken
release into the label-release queue under the sweep's own key and record it
accepted, which is the shape ``label approved`` reads today and U108 reads
tomorrow. The open items an answer did not take are superseded, closed as
answered and never as a rejection. An untaken new release is never filed.
There is no "always download this label" answer, by the author's standing
rule: a label release is downloaded only after it was answered for.

ONE REFUSAL OF THE PROVIDER PARKS THE RUN. A ``CratekitError`` out of the
catalogue, a cooldown, a trip, an expired session, passes through the walk
with the labels already answered saved and the rest unasked, their markers
unmoved. A listing that could not be read fails that one label's line and the
walk goes on, since one unreadable label should not silence the other
twenty nine questions.

Questions go to standard error through :mod:`cratekit.cli.prompt`, the one
module allowed to read standard input, and this verb is the second the
registry marks interactive. The asking is not gated: it writes the review
database and its own record, and ``stop`` goes through the registry's own
remove. The go behind the one gate is what writes files, see
:mod:`cratekit.label.go`.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Container, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

from cratekit.acquire import match_cli
from cratekit.cli import prompt
from cratekit.cli.output import Envelope, from_cause, timestamp
from cratekit.core import active_taxonomy, config, review
from cratekit.core.cause import Cause, CratekitError, Outcome, Scope, refuse
from cratekit.core.review import Queue, Verdict
from cratekit.core.routing import KindVerdict
from cratekit.core.taxonomy import Taxonomy
from cratekit.label import catalogue, sweep
from cratekit.label import cli as label_cli
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.sync import run

RECORD_VERSION = 1

#: The marker a saved answer carries once a go has taken it (U108). An answer
#: without it is what the next go's summary covers. Added beside the fields an
#: answer already records, so a record U107 wrote reads unchanged.
SETTLED = "settled"

#: The four answers, in the order they are offered.
ALL = "all"
PICK = "pick"
NOT_NOW = "not-now"
STOP = "stop"
ANSWERS: tuple[str, ...] = (ALL, PICK, NOT_NOW, STOP)
#: The fifth word the interactive prompt takes: leave this label unanswered
#: and end the run. NOT an answer, and nothing is written for it. The prompt
#: has no default, so an empty line never moves a marker.
QUIT = "quit"

#: The actor a verdict this verb writes carries.
ACTOR = "label sync"
#: The rule a superseded open item records: the label was answered.
ANSWERED_RULE = "label-sync-answered"

#: The size estimate, which is an estimate and says so. FLAC at 16 bit, 44.1
#: kHz averages about 880 kilobits a second on dance music, and a track whose
#: row carries no duration is counted as six minutes.
BYTES_PER_SECOND = 110_000
SECONDS_PER_TRACK = 360

QUEUE = str(Queue.LABEL_RELEASE)

#: How the interactive path gets its prompter. A module attribute so a suite
#: can hand in a scripted one and drive the same ``_ask`` a person reaches.
PROMPTER: Callable[[], prompt.Prompter] = prompt.Prompter


def build_sync(parser, entry) -> None:
    parser.add_argument(
        "--next",
        dest="next_question",
        action="store_true",
        help="print the next label's question instead of asking it at the terminal",
    )
    parser.add_argument(
        "--answer",
        choices=ANSWERS,
        default=None,
        help="record this answer for the label named with --label",
    )
    parser.add_argument(
        "--label",
        default=None,
        metavar="NAME",
        help=(
            "with --answer, the favourite label the answer is for; with --next, "
            "the one label to ask about"
        ),
    )
    parser.add_argument(
        "--release",
        dest="releases",
        action="append",
        default=None,
        metavar="RELEASE_ID",
        help="with --answer pick, a release to take; repeat for more",
    )
    parser.add_argument(
        "--go",
        action="store_true",
        help=(
            "show one summary over every answer saved since the last go, ask the "
            "one gate, and on apply download what was answered for"
        ),
    )
    parser.set_defaults(_handler=label_sync)


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


def _unusable(path, what: str) -> CratekitError:
    return refuse(
        "label-sync-unusable",
        f"the label sync record at {path.name} could not be read ({what}), so "
        f"which releases each label was already asked about is unknown; treating "
        f"it as empty would ask every question again and lose every answer given",
        steps=("repair or restore the label sync record before running label sync",),
        scope=Scope.RUN,
        origin=("label.sync",),
        detail={"problem": what, "path": str(path)},
    )


def _empty() -> dict[str, Any]:
    return {"version": RECORD_VERSION, "labels": {}, "answers": []}


def load_record(cfg: config.Config) -> dict[str, Any]:
    """The record as stored, or an empty one when none has been written.

    REFUSES A RECORD IT CANNOT READ rather than reading it as empty, on the
    rule every state document here keeps: an unreadable marker read as unset
    asks every question again.
    """
    path = config.state_path("label_sync", cfg)
    if not path.exists():
        return _empty()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise _unusable(path, "it could not be opened") from exc
    except ValueError as exc:
        raise _unusable(path, "it is not JSON") from exc
    if not isinstance(raw, Mapping):
        raise _unusable(path, f"the document is a {type(raw).__name__}, not a map")
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
    return {
        "version": RECORD_VERSION,
        "labels": {str(key): dict(value) for key, value in held.items()},
        "answers": list(answers),
    }


def _write_record(cfg: config.Config, document: Mapping[str, Any]) -> None:
    config.atomic_write_bytes(
        (json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        config.state_path("label_sync", cfg),
    )


@contextmanager
def _locked(cfg: config.Config, doing: str) -> Iterator[None]:
    lock = config._exclusive_lock(config.state_path("label_sync_lock", cfg))
    try:
        lock.__enter__()
    except config.ConfigLockUnavailable as exc:
        raise refuse(
            "label-sync-unusable",
            f"the label sync record could not be locked ({exc}), and {doing} "
            f"unlocked discards an answer another run is recording at the same time",
            steps=("make the library state directory writable by this account",),
            scope=Scope.RUN,
            origin=("label.sync",),
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
    document: dict[str, Any],
    answers: Sequence[tuple[int, str, str]],
    *,
    marker: Mapping[str, Any],
    keep: Container[str] = frozenset(),
) -> int:
    """Mark, in ``document``, the saved answers a go took. Returns how many.

    The caller holds :func:`record_lock` and writes the document back with
    :func:`write_record`, which is what lets the go plan, queue and settle as
    one locked step. ``answers`` names each one as ``(place, label,
    answered_at)``, and one whose place now holds a different answer is left
    alone, so a record rewritten while the go waited never has the wrong
    answer settled. An answer that took a release named in ``keep`` is left
    for the next go.
    """
    entries = document["answers"]
    now = timestamp()
    count = 0
    for index, label_id, answered_at in answers:
        if index >= len(entries):
            continue
        entry = entries[index]
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


def write_record(cfg: config.Config, document: Mapping[str, Any]) -> None:
    """Write the record back. The caller holds :func:`record_lock`."""
    _write_record(cfg, document)


def record_lock(cfg: config.Config, doing: str):
    """The record's own lock, for a caller that reads, decides and writes as one step.

    BLOCKING, not refusing: a second go waits for the first to finish
    planning, and then sees the job the first one queued.
    """
    return _locked(cfg, doing)


def asked_releases(document: Mapping[str, Any], label_id: str) -> frozenset[str]:
    """The identities a question about ``label_id`` already covered: the marker."""
    held = document["labels"].get(label_id) or {}
    asked = held.get("asked")
    if not isinstance(asked, list):
        return frozenset()
    return frozenset(str(one) for one in asked if isinstance(one, str) and one)


# ---------------------------------------------------------------------------
# A question
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Offered:
    """One release a question offers.

    ``item_id`` names the OPEN review item it already is, for the catch up,
    and is None for a release the listing found, which is filed only when it
    is taken. ``tracks`` and ``size`` are None when its tracks could not be
    read, which the question counts rather than hides.
    """

    identity: str
    artist: str
    title: str
    year: str
    tracks: int | None
    size: int | None
    item_id: str | None
    payload: dict[str, Any]
    #: The release listed short of the count the provider declares (R-515),
    #: as ``ListingShortfall.block`` carries it, or None for a full listing.
    short: dict[str, int] | None = None

    @property
    def provider_withheld(self) -> int:
        """Tracks the provider counts on this release and did not serve."""
        return int((self.short or {}).get("withheld") or 0)

    def to_json(self) -> dict[str, Any]:
        return {
            "identity": self.identity,
            "artist": self.artist,
            "title": self.title,
            "year": self.year,
            "tracks": self.tracks,
            "size": self.size,
            "item_id": self.item_id,
            "payload": dict(self.payload),
            "shortfall": dict(self.short) if self.short else None,
        }

    @classmethod
    def from_json(cls, raw: Mapping[str, Any]) -> Offered:
        payload = raw.get("payload")
        return cls(
            identity=str(raw.get("identity") or ""),
            artist=str(raw.get("artist") or ""),
            title=str(raw.get("title") or ""),
            year=str(raw.get("year") or ""),
            tracks=_count(raw.get("tracks")),
            size=_count(raw.get("size")),
            item_id=str(raw["item_id"]) if raw.get("item_id") else None,
            payload=dict(payload) if isinstance(payload, Mapping) else {},
            short=_short_of(raw.get("shortfall")),
        )


def _short_of(raw: Any) -> dict[str, int] | None:
    """A saved shortfall block read back, or None when there is none to trust."""
    if not isinstance(raw, Mapping):
        return None
    block = {key: _count(raw.get(key)) for key in ("declared", "listed", "withheld")}
    if any(value is None for value in block.values()) or not block["withheld"]:
        return None
    return {key: int(value or 0) for key, value in block.items()}


def _count(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


@dataclass(frozen=True, slots=True)
class Question:
    """What one label is asked about, and the numbers a person judges it by."""

    label_id: str
    label_name: str
    run: str
    listed_at: str
    releases: tuple[Offered, ...]
    #: Releases the listing read and the window did not reach (R-790).
    beyond: int = 0
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
            "label_id": self.label_id,
            "label_name": self.label_name,
            "run": self.run,
            "listed_at": self.listed_at,
            "releases": [one.to_json() for one in self.releases],
            "new": len(self.releases),
            "tracks": self.tracks,
            "size": self.size,
            "unknown": self.unknown,
            "provider_withheld": self.provider_withheld,
            "beyond": self.beyond,
            "unread": self.unread,
            "withheld": self.withheld,
            "unjudged": self.unjudged,
            "answers": list(ANSWERS),
        }

    @classmethod
    def from_json(cls, raw: Mapping[str, Any]) -> Question:
        releases = raw.get("releases")
        return cls(
            label_id=str(raw.get("label_id") or ""),
            label_name=str(raw.get("label_name") or ""),
            run=str(raw.get("run") or ""),
            listed_at=str(raw.get("listed_at") or ""),
            releases=tuple(
                Offered.from_json(one)
                for one in (releases if isinstance(releases, list) else ())
                if isinstance(one, Mapping)
            ),
            beyond=_count(raw.get("beyond")) or 0,
            unread=_count(raw.get("unread")) or 0,
            withheld=_count(raw.get("withheld")) or 0,
            unjudged=_count(raw.get("unjudged")) or 0,
        )


def _duration(row: Any) -> int | None:
    value = row.get("duration") if isinstance(row, Mapping) else getattr(row, "duration", None)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        return None
    return int(value)


def _measured(
    reader: catalogue.ReleaseTracks, identity: str
) -> tuple[int, int, catalogue.ListingShortfall | None] | None:
    """A release's track count, estimated size and shortfall, or None when unread.

    THE SHORTFALL RIDES BESIDE THE COUNT (R-515). A release the provider
    lists short of its declared count is still measured over the rows it
    served, and the question says how many were withheld rather than reading
    the short count as the release.

    Through the SHARED reader, so a release the ownership question or the
    gate already read costs no second request, and the one outage rule
    covers this asker too. A ``CratekitError`` passes through: an expired
    session is the person's to act on, not a release with no tracks.
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
    """What one run shares across every label it lists.

    The catalogue, the taxonomy, one :class:`~cratekit.label.gate.Asking` so
    an unreachable general catalogue is given up on once, one walk of the
    library, and the open label-release items grouped by the label the
    registry holds them under. Built on first use, so a run that answers only
    a saved question logs in to nothing.
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
        """The open label-release items filed under one label, read once per run.

        GROUPED BY THE IDENTIFIER THE REGISTRY HOLDS THE LABEL UNDER. An item
        filed before a label's identifier moved (R-381) names the old one,
        and the registry's ``by_id`` follows the move.
        """
        if self.open_items is None:
            grouped: dict[str, list[review.Item]] = {}
            page = review.list_items(store, queue=QUEUE, kinds=(sweep.KIND,), limit=None)
            for item in page.items:
                named = str(item.payload.get("label_id") or "")
                entry = self.followed.by_id(named) if named else None
                grouped.setdefault(entry.label_id if entry is not None else named, []).append(
                    item
                )
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


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _question_for(
    tools: _Tools, store: review.ReviewStore, entry: labels.LabelEntry, asked: Container[str]
) -> _Listed:
    """List one label as the sweep would and build its question, or say why not.

    THE SWEEP'S OWN SOURCE, built as ``label.cli.handle`` builds it for one
    item, with ``asked`` taking places in the offer window beside the queued
    releases. Its gate records every hold it makes, so a release held here
    is held for the next sweep too.

    A CATALOGUE THAT CONFIRMS NOTHING IS NOT A LABEL WITH NOTHING NEW, the
    worker's rule (``_refuse_unfinished``), so such a label is skipped with
    the reason and its marker does not move: a question whose count came
    from a dead verifier is the clean report over unread state every
    refusal here exists for.
    """
    found = tools.catalogue()
    declared = tools.taxonomy()
    reader = catalogue.ReleaseTracks(found)
    owned = sweep.OwnedReleases(tools.cfg, reader, library=tools.library)
    source = sweep.LabelSource(
        tools.cfg,
        registry=labels.Registry(labels={entry.label_id: entry}),
        catalogue=found,
        store=store,
        owned=owned,
        gate=genre_gate.SweepGate(
            declared,
            tracks=reader.release_tracks,
            standing=genre_gate.StandingHolds(store),
            asking=tools.asking,
        ),
        run_id=tools.run_id,
        offered=asked,
    )
    try:
        candidates = source.list_recent(-1)
    except run.LookupFailure as exc:
        return _Listed(skipped=f"its catalogue could not be listed: {exc}")
    ((_swept, listing),) = source.listings
    unconfirmed = len(source.dropped) + source.held_unconfirmed
    if not candidates and source.dropped and unconfirmed == source.read:
        return _Listed(
            skipped=(
                f"the listing read {unconfirmed} release(s) from the catalogue and could "
                f"not confirm a single one of them, so this is not a label with nothing "
                f"new; what failed is verification rather than reach, and the registry's "
                f"--match needle is the usual repair"
            ),
            listing=listing,
        )

    releases: list[Offered] = []
    for candidate in candidates:
        measured = _measured(reader, candidate.identity)
        payload = dict(candidate.payload or {})
        releases.append(
            Offered(
                identity=candidate.identity,
                artist=_text(payload.get("artist")),
                title=_text(payload.get("title")),
                year=str(candidate.recency or ""),
                tracks=measured[0] if measured else None,
                size=measured[1] if measured else None,
                short=measured[2].block() if measured and measured[2] else None,
                item_id=None,
                payload=payload,
            )
        )

    # THE CATCH UP: this label's open items, offered once under the same
    # question. Judged first from the words they recorded, with no request,
    # and one the gate would now hold is taken back as ``label judge`` takes
    # one back. A release a person returned is theirs and is not judged.
    withheld = unjudged = 0
    for item in tools.open_for(store, entry.label_id):
        standing = review.find_hold(store, queue=QUEUE, item_id=item.item_id)
        if not genre_gate.returned_by(standing, item.payload):
            judged = genre_gate.judge_recorded(
                declared,
                entry.kind,
                genre_gate.recorded_genres(item.payload, genre_gate.GENRES_FIELD),
            )
            if judged is None or judged.verdict is KindVerdict.NOT_JUDGED:
                unjudged += 1
            elif judged.held:
                taken_back = review.withhold(
                    store,
                    item.item_id,
                    group=entry.label_id,
                    name=entry.name,
                    reason=judged.reason,
                    detail=judged.detail(),
                    run_id=tools.run_id,
                )
                if taken_back is not None:
                    withheld += 1
                    continue
        identity = genre_gate.release_id_of(store, item) or f"item:{item.item_id}"
        measured = _measured(reader, identity) if not identity.startswith("item:") else None
        releases.append(
            Offered(
                identity=identity,
                artist=_text(item.payload.get("artist")),
                title=_text(item.payload.get("title")),
                year=_text(item.payload.get("year")) or _text(item.payload.get("recency")),
                tracks=measured[0] if measured else None,
                size=measured[1] if measured else None,
                short=measured[2].block() if measured and measured[2] else None,
                item_id=item.item_id,
                payload=dict(item.payload),
            )
        )
    if not releases:
        return _Listed(listing=listing, withheld=withheld)
    # WHAT THE WINDOW DID NOT REACH IS RECORDED, as the sweep records it, so
    # ``review list --group-by label`` says how much more the label could offer.
    review.record_round(
        store,
        queue=QUEUE,
        run_id=tools.run_id,
        group=entry.label_id,
        name=entry.name,
        beyond=listing.beyond,
    )
    return _Listed(
        question=Question(
            label_id=entry.label_id,
            label_name=entry.name,
            run=tools.run_id,
            listed_at=timestamp(),
            releases=tuple(releases),
            beyond=listing.beyond,
            unread=len(listing.unread),
            withheld=withheld,
            unjudged=unjudged,
        ),
        listing=listing,
    )


def _save_pending(cfg: config.Config, question: Question) -> None:
    """Save the question under its label BEFORE it is asked.

    So the answer, from either path, applies to exactly what was shown, and
    a run that stops at the prompt leaves the question for ``--next`` to
    print again with no provider call.
    """
    with _locked(cfg, "saving a question"):
        document = load_record(cfg)
        held = dict(document["labels"].get(question.label_id) or {})
        held["name"] = question.label_name
        held["pending"] = question.to_json()
        document["labels"][question.label_id] = held
        _write_record(cfg, document)


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
            "label_id": self.label_id,
            "label_name": self.label_name,
            "answer": self.answer,
            "offered": self.offered,
            "taken": [one.identity for one in self.taken],
            "tracks": sum(one.tracks or 0 for one in self.taken),
            "size": sum(one.size or 0 for one in self.taken),
            "left": list(self.left),
            "removed": self.removed,
        }


def _selection_invalid(message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(
        "review-selection-invalid",
        message,
        steps=steps,
        origin=("label.sync",),
        detail=detail,
    )


def _take(store: review.ReviewStore, one: Offered, run_id: str) -> bool:
    """Record one release as accepted, filing it first when it was never filed.

    A NEW RELEASE IS FILED UNDER THE SWEEP'S KEY AND THEN ACCEPTED, so the
    item is the one the sweep would have filed and ``label approved`` reads
    it as any accepted release. An open catch up item is accepted as it
    stands. One that LEFT REVIEW or was DECIDED between the question and the
    answer is not taken, and False says so: an accepted one is already what
    the answer asked for, and any other verdict is a person's to clear.
    """
    if one.item_id is None:
        item = sweep.offer_release(
            store,
            run.Candidate(identity=one.identity, recency=one.year, payload=dict(one.payload)),
            run_id=run_id,
        )
    else:
        found = review.find(store, one.item_id)
        if found is None:
            return False
        item = found
    if item.verdict is Verdict.ACCEPTED:
        return True
    if item.stored_verdict is not None:
        return False
    review.resolve(store, item.item_id, Verdict.ACCEPTED, actor=ACTOR)
    return True


def record_answer(
    cfg: config.Config,
    store: review.ReviewStore,
    entry: labels.LabelEntry,
    answer: str,
    picks: Sequence[str],
    *,
    run_id: str,
) -> Answered:
    """Record one answer for one label, against the question saved for it.

    UNDER THE RECORD'S LOCK FOR THE WHOLE OF IT, so a structured answer
    landing beside an interactive one cannot read the question the other is
    answering. The review writes come first and the record last: a review
    write that refuses leaves the question pending and nothing claimed, and
    the record never says a release was taken that the queue does not hold.

    EVERY ANSWER MOVES THE MARKER over every release the question offered,
    ``not-now`` included, which is the author's decision: a release answered
    once never returns. ``stop`` removes the label through the registry's own
    path, after the review writes, so a remove that refuses leaves nothing
    half done.
    """
    if answer not in ANSWERS:
        raise _selection_invalid(
            f"{answer!r} is not an answer label sync records",
            f"answer with one of: {', '.join(ANSWERS)}",
            answer=answer,
        )
    with _locked(cfg, "recording an answer"):
        document = load_record(cfg)
        held = dict(document["labels"].get(entry.label_id) or {})
        pending = held.get("pending")
        if not isinstance(pending, Mapping) or not pending.get("releases"):
            # STOP WITH NOTHING WAITING names the registry's remove, since
            # ``--next`` asks nothing about a label with nothing new and the
            # remedy would send a person round in a circle.
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
        offered = {one.identity: one for one in question.releases}
        wanted: dict[str, None] = dict.fromkeys(str(pick).strip() for pick in picks if str(pick).strip())
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
                    f"take the identifiers from: crate label sync --next --label "
                    f"{entry.label_id}",
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
        chosen = [
            one
            for one in question.releases
            if answer == ALL or (answer == PICK and one.identity in wanted)
        ]
        taken: list[Offered] = []
        left: list[str] = []
        # FILED UNDER THE RUN THAT ASKED, which recorded the label's round, so
        # a grouping by run finds the round and its filings together when the
        # answer came from a later ``--answer``.
        filing_run = question.run or run_id
        for one in chosen:
            (taken if _take(store, one, filing_run) else left).append(one)
        taken_ids = {one.identity for one in taken}
        # SETTLED BY THE ID EACH RELEASE FILES UNDER, not only the ids the
        # question knew: a sweep that ran while the question waited filed its
        # new releases, and settling only the catch up items left those open
        # for the next run to ask about again. ``supersede`` passes over an id
        # nothing filed and over one already decided.
        review.supersede(
            store,
            [
                one.item_id or genre_gate.release_item_id(one.identity)
                for one in question.releases
                if one.identity not in taken_ids
            ],
            rule=ANSWERED_RULE,
        )
        removed = False
        if answer == STOP:
            removed = labels.RegistryStore().remove(entry.label_id)
        now = timestamp()
        asked = set(asked_releases(document, entry.label_id)) | set(question.identities())
        held.pop("pending", None)
        held.update(
            {
                "name": entry.name,
                "asked": sorted(asked),
                "asked_at": now,
                "answer": answer,
                "run": run_id,
            }
        )
        document["labels"][entry.label_id] = held
        result = Answered(
            label_id=entry.label_id,
            label_name=entry.name,
            answer=answer,
            offered=len(question.releases),
            taken=tuple(taken),
            left=tuple(one.identity for one in left),
            removed=removed,
        )
        document["answers"].append(
            {
                **result.to_json(),
                "run": run_id,
                "asked_run": question.run,
                "answered_at": now,
                "releases": [one.to_json() for one in taken],
            }
        )
        _write_record(cfg, document)
    return result


# ---------------------------------------------------------------------------
# The envelope
# ---------------------------------------------------------------------------


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return {"key": f"label.sync.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


def _named(one: Offered) -> str:
    said = f"{one.artist} - {one.title}" if one.artist else one.title or one.identity
    if one.year:
        said += f" ({one.year})"
    return said


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


def _counts(question: Question) -> str:
    said = (
        f"{len(question.releases)} new release(s), {question.tracks} track(s), "
        f"about {size_text(question.size)}"
    )
    if question.unknown:
        said += f", {question.unknown} with tracks unread"
    if question.provider_withheld:
        said += (
            f"; {question.provider_withheld} track(s) withheld by the provider "
            f"on {question.short_releases} release(s), counted but not listed"
        )
    if question.beyond:
        said += f"; {question.beyond} more past this run's window"
    if question.unread:
        said += f"; {question.unread} listing(s) of the label could not be read"
    if question.withheld:
        said += f"; {question.withheld} open item(s) taken back by the genre gate"
    if question.unjudged:
        said += f"; {question.unjudged} the genre gate has no word for"
    return said


def _question_checks(question: Question, *, how: str) -> list[dict[str, Any]]:
    return [
        _check(
            f"question.{question.label_id}",
            "info",
            f"{question.label_name}: {_counts(question)}; {how}",
        ),
        *(
            _check(
                f"release.{one.identity}",
                "info",
                f"{question.label_name}: {_named(one)}, "
                + _tracks_said(one)
                + (", waiting in review" if one.item_id else ""),
            )
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
    if listed.listing is not None and listed.listing.beyond:
        detail += f"; {listed.listing.beyond} release(s) past this run's window"
    if listed.withheld:
        detail += f"; {listed.withheld} open item(s) taken back by the genre gate"
    return _check(f"label.{entry.label_id}", "ok", detail)


def _skipped_check(entry: labels.LabelEntry, why: str) -> dict[str, Any]:
    return _check(f"label.{entry.label_id}", "fail", f"{entry.name}: not asked; {why}")


def _summary(
    *,
    question: Question | None = None,
    answered: Sequence[Answered] = (),
    labels_seen: Sequence[dict[str, Any]] = (),
    stopped_at: str | None = None,
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
    raise refuse(
        "label-registry-empty",
        "no favourite label is registered, so there is no label to ask about",
        steps=("register a label with: crate label registry add <name>",),
        origin=("label.sync",),
    )


def _entry_or_refuse(followed: labels.Registry, name: str) -> labels.LabelEntry:
    entry = followed.resolve(name)
    if entry is not None:
        return entry
    raise refuse(
        "label-unknown",
        f"no favourite label is named {name!r}",
        steps=("list the registry and take the name from it",),
        origin=("label.sync",),
        detail={"name": name},
    )


# ---------------------------------------------------------------------------
# The three paths
# ---------------------------------------------------------------------------


def _next(ctx, cfg: config.Config, name: str | None = None) -> Envelope:
    """Print the next question, saving it, and ask nothing.

    A SAVED QUESTION IS PRINTED AGAIN WITHOUT A PROVIDER CALL, so an agent
    session asking twice spends nothing twice. Labels are walked in registry
    order and the first with something to ask is the answer.

    ONE LABEL NAMED IS THE ONLY LABEL TOUCHED (U189). ``--next --label`` runs
    the same loop over that one entry, resolved before any provider is built,
    so no other label is listed and no other saved question is rewritten, and
    the label's own line is the whole report: a closing "no label has
    anything new" would speak for labels nobody asked about.

    A LABEL THAT COULD NOT BE READ IS NOT A LABEL WITH NOTHING NEW (R-1114).
    The closing line names only the labels that were listed, and a run whose
    every label was skipped refuses as ``label-sync-unlisted`` rather than
    ending ``no_op``, carrying each label's line, so neither the words nor
    the exit status read a failed listing as nothing to ask.
    """
    followed = _followed_or_refuse()
    only = _entry_or_refuse(followed, name) if name is not None else None
    entries = [only] if only is not None else list(followed.labels.values())
    tools = _Tools(cfg=cfg, run_id=ctx.run.run_id, followed=followed)
    document = load_record(cfg)
    seen: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []
    withheld = 0
    nothing: list[str] = []
    with review.open_store(cfg) as store:
        for entry in entries:
            held = document["labels"].get(entry.label_id) or {}
            pending = held.get("pending")
            if isinstance(pending, Mapping) and pending.get("releases"):
                question = Question.from_json(pending)
            else:
                listed = _question_for(tools, store, entry, asked_releases(document, entry.label_id))
                if listed.skipped is not None:
                    checks.append(_skipped_check(entry, listed.skipped))
                    seen.append({"label_id": entry.label_id, "state": "skipped"})
                    continue
                if listed.question is None:
                    checks.append(_nothing_check(entry, listed))
                    withheld += listed.withheld
                    nothing.append(entry.name)
                    seen.append({"label_id": entry.label_id, "state": "nothing-new"})
                    continue
                question = listed.question
                _save_pending(cfg, question)
            seen.append({"label_id": entry.label_id, "state": "asked"})
            checks.extend(
                _question_checks(
                    question,
                    how=(
                        f"answer with: crate label sync --answer all --label "
                        f"{entry.label_id}, or pick with --release, or not-now, or stop"
                    ),
                )
            )
            return ctx.envelope(
                data={"checks": checks, "summary": _summary(question=question, labels_seen=seen)}
            )
    data = {"checks": checks, "summary": _summary(labels_seen=seen)}
    if not nothing:
        # EVERY LABEL ASKED ABOUT WAS SKIPPED (R-1114), so nothing here was
        # read and nothing found: the ``no-evidence`` rule, at this verb. The
        # run refuses through ``from_cause`` with its own checks as the data,
        # so each label's line still says why it was not asked. The single
        # label form included, since its one label skipped is the same state.
        return from_cause(
            verb=ctx.entry.name,
            run_id=ctx.run.run_id,
            started=ctx.started,
            cause=_unlisted_cause(entries),
            schema=ctx.entry.output_schema,
            data=data,
        )
    if only is None:
        # THE CLOSING LINE SPEAKS ONLY FOR THE LABELS THAT WERE LISTED (R-1114).
        # A skipped label has its own ``fail`` line, and "nothing new" said of
        # it would be the clean report over a listing that never answered.
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


def _unlisted_cause(entries: Sequence[labels.LabelEntry]) -> Cause:
    """The refusal for a ``--next`` whose every label was skipped, as a cause."""
    names = ", ".join(entry.name for entry in entries)
    which = (
        f"the label asked about could not be read ({names}), so whether it has"
        if len(entries) == 1
        else f"none of the {len(entries)} labels asked about could be read ({names}), "
        f"so whether any of them has"
    )
    return refuse(
        "label-sync-unlisted",
        f"{which} anything new is unknown; no question was asked or saved",
        steps=(
            "read each label's line for why it was not asked",
            "a catalogue that could not be listed: run crate doctor, then ask again "
            "when the provider answers",
            "a listing that confirmed nothing: check the label's --match needle "
            "with: crate label registry",
        ),
        retryable=True,
        origin=("label.sync",),
        detail={"labels": [entry.label_id for entry in entries]},
    ).cause


def _answer(ctx, cfg: config.Config) -> Envelope:
    """Record the one answer named on the command line."""
    followed = _followed_or_refuse()
    entry = _entry_or_refuse(followed, str(ctx.args.label))
    with review.open_store(cfg) as store:
        answered = record_answer(
            cfg,
            store,
            entry,
            str(ctx.args.answer),
            list(ctx.args.releases or ()),
            run_id=ctx.run.run_id,
        )
    return ctx.envelope(
        data={
            "checks": [
                _answer_check(answered),
                _check("next", "info", "the next question: crate label sync --next"),
            ],
            "summary": _summary(answered=[answered]),
        }
    )


def _question_text(question: Question) -> str:
    lines = [f"\n{question.label_name}: {_counts(question)}\n"]
    for number, one in enumerate(question.releases, start=1):
        tracks = _tracks_said(one)
        waiting = ", waiting in review" if one.item_id else ""
        lines.append(f"  {number:>3}. {_named(one)}, {tracks}{waiting}\n")
    return "".join(lines)


def _ask(prompter: prompt.Prompter, question: Question) -> tuple[str, list[str]]:
    """Put one question to a person and return the answer and, for a pick, the releases.

    NO DEFAULT. An empty line is asked again and never read as an answer,
    because every answer moves the marker and an accidental return must not.
    ``quit`` leaves the label unanswered. A word outside the set is asked
    again, :data:`prompt.MAX_ATTEMPTS` times, then the prompt is given up on.
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
            # ``isdecimal`` and not ``isdigit``: a superscript two is a digit
            # that ``int`` refuses, and that crashed the walk mid question.
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


def _walk(ctx, cfg: config.Config, prompter: prompt.Prompter) -> Envelope:
    """Ask every label with something new, in registry order, answer by answer.

    EVERY LABEL IS LISTED AFRESH, a saved question included, since the walk
    is the one path that can wait for a person, and what it asks should be
    what the catalogue holds now. A run that stops, by ``quit`` or by a
    prompt nobody can answer, has saved every answer given before it, so the
    next run asks about the first label still unanswered.
    """
    followed = _followed_or_refuse()
    tools = _Tools(cfg=cfg, run_id=ctx.run.run_id, followed=followed)
    answered: list[Answered] = []
    seen: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []
    stopped_at: str | None = None
    withheld = 0
    with review.open_store(cfg) as store:
        for entry in list(followed.labels.values()):
            document = load_record(cfg)
            listed = _question_for(tools, store, entry, asked_releases(document, entry.label_id))
            if listed.skipped is not None:
                checks.append(_skipped_check(entry, listed.skipped))
                seen.append({"label_id": entry.label_id, "state": "skipped"})
                continue
            if listed.question is None:
                checks.append(_nothing_check(entry, listed))
                withheld += listed.withheld
                seen.append({"label_id": entry.label_id, "state": "nothing-new"})
                continue
            _save_pending(cfg, listed.question)
            try:
                answer, picks = _ask(prompter, listed.question)
            except prompt.PromptUnavailable as exc:
                raise refuse(
                    "label-sync-unanswerable",
                    f"the question about {entry.name!r} could not be answered at this "
                    f"terminal ({exc}); the {len(answered)} answer(s) given before it are "
                    f"saved and the question is waiting",
                    steps=(
                        f"run label sync from a terminal, or drive it with: crate label "
                        f"sync --next --label {entry.label_id}, then crate label sync "
                        f"--answer ANSWER --label {entry.label_id}",
                    ),
                    origin=("label.sync",),
                    detail={
                        "label": entry.label_id,
                        "answered": [one.label_id for one in answered],
                    },
                ) from exc
            if answer == QUIT:
                stopped_at = entry.label_id
                seen.append({"label_id": entry.label_id, "state": "unanswered"})
                checks.append(
                    _check(
                        f"label.{entry.label_id}",
                        "info",
                        f"{entry.name}: left unanswered; the next run asks again",
                    )
                )
                break
            result = record_answer(cfg, store, entry, answer, picks, run_id=ctx.run.run_id)
            answered.append(result)
            seen.append({"label_id": entry.label_id, "state": "answered"})
            checks.append(_answer_check(result))
    checks.append(
        _check(
            "run",
            "info",
            f"{len(answered)} label(s) answered"
            + (f"; stopped at {stopped_at}, run label sync again to go on" if stopped_at else
               "; every label is answered"),
        )
    )
    data = {
        "checks": checks,
        "summary": _summary(answered=answered, labels_seen=seen, stopped_at=stopped_at),
    }
    if stopped_at is None:
        # EVERY LABEL WITH SOMETHING NEW IS ANSWERED, so the walk ends at the
        # one gate over the summary of every saved answer, in this verb (U108).
        # A walk that stopped asks nothing: the labels after it are unanswered.
        return _go(ctx, cfg, walk=[one["detail"] for one in checks], data=data,
                   wrote=bool(answered or withheld))
    return ctx.envelope(
        data=data,
        # A QUESTION LEFT UNANSWERED IS STILL A RUN THAT WROTE: the question
        # was saved, its round recorded, and any open item the gate took back
        # left review. NO_OP is a run that had nothing to ask and wrote nothing.
        outcome=Outcome.OK if answered or stopped_at or withheld else Outcome.NO_OP,
    )


def _go(ctx, cfg: config.Config, **kwargs: Any) -> Envelope:
    """The go, imported here because :mod:`cratekit.label.go` imports this module
    for the record, and a module scope import each way is a cycle."""
    from cratekit.label import go  # noqa: PLC0415 - see the docstring

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
    if args.go:
        return _go(ctx, cfg)
    if args.answer is not None:
        return _answer(ctx, cfg)
    if args.next_question:
        return _next(ctx, cfg, args.label)
    return _walk(ctx, cfg, PROMPTER())


__all__ = [
    "ACTOR",
    "ALL",
    "ANSWERED_RULE",
    "ANSWERS",
    "BYTES_PER_SECOND",
    "NOT_NOW",
    "PICK",
    "QUIT",
    "RECORD_VERSION",
    "SECONDS_PER_TRACK",
    "SETTLED",
    "STOP",
    "Answered",
    "Offered",
    "Question",
    "asked_releases",
    "build_sync",
    "label_sync",
    "load_record",
    "record_answer",
    "record_lock",
    "settle_in",
    "size_text",
    "unsettled",
    "write_record",
]
