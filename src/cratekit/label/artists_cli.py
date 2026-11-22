"""``label.artists``: give an open label release its artist's name back (R-840).

Before R-379 a sweep stringified the provider's artist object into the item,
which then reads ``<tidalapi.artist.Artist object at 0x...>``. This verb reads
each such release again by its identifier and writes the name. Not a step of
``label judge``, which is built to make no provider call; a repaired item no
longer reads an address, so a second run asks only about what the first left.

ONLY AN OPEN ITEM, AND ONLY ITS ARTIST, on the payload as it stands under the
store's write lock (:func:`cratekit.core.review.redescribe`). A held release is
not an open item. AN ADDRESS IS NEVER REPLACED BY NOTHING: a release not
served, unread, or naming no artist is counted, left, and asked about next run.
A failed read ends the run on ``unavailable-transient`` with the counts, early
after three in a row. The catalogue is opened only when an item needs it.

Layer: modules.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from functools import partial
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import review
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.review import Queue
from cratekit.label import catalogue, review_common
from cratekit.label import cli as label_cli
from cratekit.label import gate as genre_gate

ORIGIN = ("label", "artists_cli")

#: What ``str`` of an object with no ``__str__`` of its own reads: the class by
#: its dotted name and the address it lived at. The whole field and nothing
#: around it, so an artist whose name merely contains such text is a name.
ADDRESS = re.compile(r"<[A-Za-z_][\w.]* object at 0x[0-9A-Fa-f]+>")

#: What happened to one open item, as the summary counts it.
REPAIRED = "repaired"
NOT_SERVED = "not_served"
#: The artist does not read an address, an empty one included: nothing to put right.
ALREADY_FINE = "already_fine"
#: The provider was asked and could not answer. Asking again may.
UNREAD = "unread"
#: The provider served the release and names no artist for it.
UNNAMED = "unnamed"
#: The item names no release, or not the one it is addressed by.
UNADDRESSED = "unaddressed"
#: Decided, or gone from review, by the time it was looked at or written.
DECIDED = "decided"
OUTCOMES: tuple[str, ...] = (
    REPAIRED, NOT_SERVED, ALREADY_FINE, UNREAD, UNNAMED, UNADDRESSED, DECIDED
)


def build_artists(parser, entry) -> None:
    del entry
    parser.set_defaults(_handler=label_artists)


def is_address(value: Any) -> bool:
    """Whether a recorded artist is a provider object address and not a name."""
    return isinstance(value, str) and ADDRESS.fullmatch(value.strip()) is not None


@dataclass(frozen=True, slots=True)
class _Subject:
    """One open item reading an address, as it was listed, in its row's order."""

    release_id: str
    item_id: str
    label_id: str
    label_name: str
    title: str


_text = review_common.text
_check = partial(review_common.check, "label.artists")


def _named(subject: _Subject) -> str:
    return review_common.named(subject.release_id, subject.title, subject.label_name)


@dataclass
class _Run:
    """What one run did so far: the counts, the lines, and the reads it spent.

    ``addresses`` is the sum of every outcome but ``already_fine``. ``asked``
    counts the releases the provider was asked for, answered or not.
    """

    counts: dict[str, int] = field(default_factory=lambda: dict.fromkeys(OUTCOMES, 0))
    checks: list[dict[str, Any]] = field(default_factory=list)
    releases: list[dict[str, Any]] = field(default_factory=list)
    asked: int = 0

    @property
    def addresses(self) -> int:
        return sum(n for outcome, n in self.counts.items() if outcome != ALREADY_FINE)

    def record(self, subject: _Subject, outcome: str, status: str, said: str,
               artist: str | None = None) -> None:
        self.counts[outcome] += 1
        # Keyed by the item when no release is read for it, since such an item
        # may name another item's release.
        key = (
            f"item.{subject.item_id}"
            if outcome == UNADDRESSED
            else f"release.{subject.release_id}"
        )
        self.checks.append(_check(key, status, said))
        # The sentence rides the row too, since a refusal carries no check line.
        self.releases.append(
            {
                **asdict(subject),
                "outcome": outcome,
                "artist": artist,
                "said": said,
            }
        )

    def summary(self) -> dict[str, Any]:
        return {
            "addresses": self.addresses,
            **self.counts,
            "asked": self.asked,
            "releases": list(self.releases),
        }


def _listed(store: review.ReviewStore, done: _Run) -> list[_Subject]:
    """Every open item that reads an address. The ones left out are counted.

    Read off the review queue a page at a time. An item carrying a verdict
    this build cannot read is somebody's decision all the same: counted
    decided and not asked about.
    """
    found: list[_Subject] = []
    wanted = review.Predicate(queue=str(Queue.LABEL_RELEASE), kind=genre_gate.RELEASE_KIND)
    for item in review.iter_items(store, predicate=wanted):
        if not is_address(item.payload.get("artist")):
            done.counts[ALREADY_FINE] += 1
            continue
        if item.stored_verdict is not None:
            done.counts[DECIDED] += 1
            continue
        found.append(_Subject(
            genre_gate.release_id_of(store, item), item.item_id,
            *(_text(item.payload.get(name)) for name in ("label_id", "label_name", "title")),
        ))
    return found


def _write(store: review.ReviewStore, subject: _Subject, name: str) -> str:
    """Write ``name`` as the item's artist, on the payload AS IT STANDS.

    Under the store's write lock, so a judging job's stamp since is kept.
    :data:`ALREADY_FINE` when somebody put it right meanwhile, :data:`DECIDED`
    when it was decided or left review.
    """
    seen: list[bool] = []

    def named(current: dict[str, Any]) -> dict[str, Any] | None:
        seen.append(True)
        if not is_address(current.get("artist")):
            return None
        return {**current, "artist": name}

    if review.redescribe(store, subject.item_id, named) is not None:
        return REPAIRED
    return ALREADY_FINE if seen else DECIDED


def _with_counts(error: CratekitError, done: _Run, listed: int) -> CratekitError:
    """The same refusal, carrying what the run did before it stopped.

    ``left`` counts the items this run set out to read and did not reach, and
    is added to the addresses to say how many there were.
    """
    left = listed - len(done.releases)
    step = (
        f"{done.counts[REPAIRED]} release(s) were given their artist before this "
        f"and {left} were not reached; run crate label artists again, which asks "
        f"only about the ones still reading an address"
    )
    summary = done.summary()
    summary["addresses"] += left
    return review_common.extended(error, step, artists=summary, left=left)


def _repair_one(store: review.ReviewStore, found: catalogue.Catalogue, subject: _Subject,
                done: _Run) -> bool:
    """Read one release's artist and write it. Whether the provider FAILED the read.

    Only the seam's own exception means not served (``LookupError`` would also
    catch a parse failure). A ``CratekitError`` is the run refused, and is the
    caller's to stop on.
    """
    try:
        name = found.release_artist(subject.release_id)
    except CratekitError:
        raise
    except catalogue.ReleaseUnresolvable as exc:
        done.asked += 1
        done.record(
            subject, NOT_SERVED, "info",
            f"{_named(subject)} is no longer served by the provider ({exc}); its "
            f"item is left as it is",
        )
        return False
    except Exception as exc:  # noqa: BLE001 - named per release, never swallowed
        done.asked += 1
        done.record(
            subject, UNREAD, "fail",
            f"{_named(subject)} could not be read from the provider "
            f"({type(exc).__name__}: {exc}); its item is left as it is, and "
            f"another run asks again",
        )
        return True
    done.asked += 1
    name = _text(name)
    if not name:
        done.record(
            subject, UNNAMED, "info",
            f"the provider names no artist for {_named(subject)}; its item is "
            f"left as it is",
        )
        return False
    outcome = _write(store, subject, name)
    said = {
        REPAIRED: f"{_named(subject)} now reads its artist, {name}",
        ALREADY_FINE: f"{_named(subject)} stopped reading an address while it was being "
        f"read, so what it reads now was kept",
        DECIDED: f"{_named(subject)} was decided, or left review, while it was being "
        f"read, so it was not rewritten",
    }[outcome]
    repaired = outcome == REPAIRED
    done.record(subject, outcome, "ok" if repaired else "info", said, name if repaired else None)
    return False


def _walk(cfg, store: review.ReviewStore, subjects: list[_Subject], done: _Run) -> None:
    """Read and repair each listed item, and refuse if the provider failed a read."""
    found: catalogue.Catalogue | None = None
    failed_in_a_row = 0
    for subject in subjects:
        if (
            not subject.release_id
            or genre_gate.release_item_id(subject.release_id) != subject.item_id
        ):
            done.record(
                subject, UNADDRESSED, "info",
                f"review item {subject.item_id} reads an address and does not "
                f"name the release it is addressed by, so nothing was read "
                f"for it",
            )
            continue
        if found is None:
            # Opened on the first release that needs it, so a queue with no
            # address in it spends no login.
            found = catalogue.resolve(cfg)
        failed = _repair_one(store, found, subject, done)
        failed_in_a_row = failed_in_a_row + 1 if failed else 0
        if failed_in_a_row >= catalogue.READS_FAILED_IN_A_ROW:
            # THE RUN STOPS before a read it already knows is wasted.
            break
    if done.counts[UNREAD]:
        # AFTER THE WALK, so an outage over the last releases refuses too.
        stopped_early = failed_in_a_row >= catalogue.READS_FAILED_IN_A_ROW
        raise refuse(
            "unavailable-transient",
            (
                f"the provider failed {catalogue.READS_FAILED_IN_A_ROW} release "
                f"reads in a row, so the run stopped reading"
                if stopped_early
                else f"the provider could not answer about "
                f"{done.counts[UNREAD]} of the {done.asked} release(s) it was "
                f"asked for"
            )
            + ". Each release it failed on still reads an address",
            remedy=Remedy.RETRY_LATER,
            origin=ORIGIN,
        )


def label_artists(ctx) -> Envelope:
    """Give every open label release that reads an address its artist's name."""
    cfg = label_cli._load()
    done = _Run()
    # One open of the store for the run; it holds no transaction between writes.
    with review.open_store(cfg) as store:
        subjects = _listed(store, done)
        try:
            _walk(cfg, store, subjects, done)
        except CratekitError as stopped:
            raise _with_counts(stopped, done, len(subjects)) from stopped

    addresses = done.addresses
    left = addresses - done.counts[REPAIRED]
    if not addresses:
        said = "no open label release reads an address where its artist belongs"
    else:
        said = (
            f"{addresses} open label release(s) read an address where the artist "
            f"belongs; {done.counts[REPAIRED]} were given the artist's name"
            + (f" and {left} were left as they are" if left else "")
        )
    lines = [
        _check("addresses", "info" if left else "ok", said),
        _check("fine", "ok", f"{done.counts[ALREADY_FINE]} open label release(s) do not "
               "read an address and were not rewritten"),
    ]
    if done.counts[DECIDED]:
        lines.append(_check("decided", "info", f"{done.counts[DECIDED]} release(s) reading "
                            "an address are decided or left review, and a decided item is "
                            "never rewritten"))
    return ctx.envelope(
        data={"checks": [*lines, *done.checks], "summary": done.summary()},
        outcome=Outcome.OK if done.counts[REPAIRED] else Outcome.NO_OP,
    )


__all__ = [
    "ADDRESS", "ALREADY_FINE", "DECIDED", "NOT_SERVED", "OUTCOMES", "REPAIRED", "UNADDRESSED",
    "UNNAMED", "UNREAD", "build_artists", "is_address", "label_artists",
]
