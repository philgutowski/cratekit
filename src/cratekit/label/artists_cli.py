"""``label.artists``: give an open label release its artist's name back (R-840).

WHAT THIS VERB IS FOR. Before R-379 a sweep stringified the provider's artist
object into the review item, so the item reads ``<tidalapi.artist.Artist object
at 0x...>`` where the artist belongs. R-379 fixed the producer. The items
already filed kept the address, because a sweep never offers a release again
while it holds a place in its label's window, and ``label judge`` rewrites the
gate's fields and not the artist. This verb reads each such release again by
its identifier and writes the name.

A VERB OF ITS OWN AND NOT A STEP OF ``label judge``, for three reasons.

* ``label judge`` gives a verdict on every pending release and moves the ones
  the gate would not have filed into a hold. A person who wants 29 names put
  right has not asked for 2,000 releases to be judged, and here no gate
  decision can change because no gate is consulted.
* Most releases a judging pass meets cost no provider call at all. An artist
  read inside that worker would put a call on the path built to avoid them.
* The repair picks up where it stopped with no job behind it: a repaired item
  no longer reads an address, so a second run asks only about what the first
  left.

ONLY AN OPEN ITEM, AND ONLY ITS ARTIST. A decided item keeps the payload it was
decided on, which :func:`cratekit.core.review.redescribe` checks inside its
write. The artist is changed on the payload as it stands under the store's
write lock, so a field another writer put on the item since it was listed is
kept, and an artist somebody put right in that time is not written over.

A RELEASE HELD OUT OF REVIEW IS NOT AN OPEN ITEM and is not read here. A hold
carries the payload its item had, the address included, and ``label held
return`` files it back as it was, after which this verb repairs it.

AN ADDRESS IS NEVER REPLACED BY NOTHING. A release the provider no longer
serves, one it could not answer about, and one it names no artist for are each
counted and left reading what they read. Nothing marks such an item, so every
run asks about it again, one read each, until a person decides it.

A READ THE PROVIDER FAILED IS A REFUSAL AND NOT A CLEAN RUN. The walk goes on,
since the next release may answer, and stops early only when three reads in a
row fail. Either way the run ends on ``unavailable-transient`` carrying the
counts, because asking again may finish what this run could not.

IT DECIDES NOTHING AND DOWNLOADS NOTHING. Each release asked about costs one
provider read, paced by the provider gate the catalogue is opened with, and the
catalogue is not opened at all when no item reads an address.

Layer: modules.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import review
from cratekit.core.cause import CratekitError, Outcome, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.review import Queue
from cratekit.label import catalogue
from cratekit.label import cli as label_cli
from cratekit.label import gate as genre_gate

ORIGIN = ("label", "artists_cli")

#: What ``str`` of an object with no ``__str__`` of its own reads: the class by
#: its dotted name and the address it lived at. The whole field and nothing
#: around it, so an artist whose name merely contains such text is a name.
ADDRESS = re.compile(r"<[A-Za-z_][\w.]* object at 0x[0-9A-Fa-f]+>")

#: What happened to one open item, as the summary counts it. The first three
#: are the brief's. The rest are the ways an address is left where it is.
REPAIRED = "repaired"
NOT_SERVED = "not_served"
#: The artist does not read an address, so there is nothing here to put right.
#: An empty artist is counted here too: it is not an address, and a release
#: with no artist recorded is not this verb's to fill.
ALREADY_FINE = "already_fine"
#: The provider was asked and could not answer. Asking again may.
UNREAD = "unread"
#: The provider served the release and names no artist for it.
UNNAMED = "unnamed"
#: The item names no release, or not the one it is addressed by, so nothing
#: says which release to read.
UNADDRESSED = "unaddressed"
#: Decided, or gone from review, by the time it was looked at or written.
DECIDED = "decided"
OUTCOMES: tuple[str, ...] = (
    REPAIRED,
    NOT_SERVED,
    ALREADY_FINE,
    UNREAD,
    UNNAMED,
    UNADDRESSED,
    DECIDED,
)


def build_artists(parser, entry) -> None:
    del entry
    parser.set_defaults(_handler=label_artists)


def is_address(value: Any) -> bool:
    """Whether a recorded artist is a provider object address and not a name."""
    return isinstance(value, str) and ADDRESS.fullmatch(value.strip()) is not None


@dataclass(frozen=True, slots=True)
class _Subject:
    """One open item reading an address, as it was listed."""

    item_id: str
    release_id: str
    label_id: str
    label_name: str
    title: str


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return {"key": f"label.artists.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


def _named(subject: _Subject) -> str:
    """One release as a person names it: identifier, title, label."""
    said = f"release {subject.release_id or '(no identifier)'}"
    if subject.title:
        said += f" ({subject.title!r})"
    return said + (f" on {subject.label_name}" if subject.label_name else "")


@dataclass
class _Run:
    """What one run did so far: the counts, the lines, and the reads it spent.

    ``addresses`` IS EVERY OPEN ITEM LEFT READING AN ADDRESS OR GIVEN A NAME BY
    THIS RUN, so it is always the sum of every outcome but ``already_fine``.
    An item that stopped reading an address while it was being read is not one
    of them any more, and is counted with the items that never did.

    ``asked`` counts the releases THE PROVIDER WAS ASKED FOR, whether or not it
    answered. A read the catalogue or the provider gate refused is not counted,
    since a refusal may come before any call is made.
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
        # KEYED BY THE ITEM WHEN NO RELEASE IS READ FOR IT. An item that does
        # not name the release it is addressed by may name another item's, and
        # two lines under one release's key would read as one release twice.
        key = (
            f"item.{subject.item_id}"
            if outcome == UNADDRESSED
            else f"release.{subject.release_id}"
        )
        self.checks.append(_check(key, status, said))
        # THE SENTENCE RIDES THE ROW TOO. A refusal carries the summary and no
        # check line, and why a read failed is what a person needs from it.
        self.releases.append(
            {
                "release_id": subject.release_id,
                "item_id": subject.item_id,
                "label_id": subject.label_id,
                "label_name": subject.label_name,
                "title": subject.title,
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

    READ OFF THE REVIEW QUEUE AND NOTHING ELSE, a page at a time. The walk
    lists what is unresolved, so a decided item is never seen here. An item
    carrying a verdict this build cannot read is listed and is somebody's
    decision all the same, so it is counted decided and not asked about.
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
        found.append(
            _Subject(
                item_id=item.item_id,
                release_id=genre_gate.release_id_of(store, item),
                label_id=_text(item.payload.get("label_id")),
                label_name=_text(item.payload.get("label_name")),
                title=_text(item.payload.get("title")),
            )
        )
    return found


def _write(store: review.ReviewStore, subject: _Subject, name: str) -> str:
    """Write ``name`` as the item's artist, on the payload AS IT STANDS.

    THE STORE CHANGES THE ONE FIELD UNDER ITS OWN WRITE LOCK. The listing is
    as old as every paced read since, and a payload written from it would take
    back whatever a judging job stamped on the item meanwhile.

    The outcome, one of three. :data:`REPAIRED` when the name was written.
    :data:`ALREADY_FINE` when the item stopped reading an address in that
    time, which is somebody else having put it right, and their word is kept.
    :data:`DECIDED` when it was decided or left review: the store does not
    hand a payload over for an item that is not open.
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

    A refusal is the exit a person most needs the counts from: items were
    repaired before it. The cause is extended and never rebuilt by hand, so its
    remedy and its trail come through unchanged. ``left`` is counted against
    the items this run set out to read, each of which is recorded once reached.
    The addresses in the summary are the ones reached, so the ones not reached
    are added to say how many there were.
    """
    left = listed - len(done.releases)
    cause = error.cause
    step = (
        f"{done.counts[REPAIRED]} release(s) were given their artist before this "
        f"and {left} were not reached; run crate label artists again, which asks "
        f"only about the ones still reading an address"
    )
    summary = done.summary()
    summary["addresses"] += left
    return rebuilt(
        error,
        replace(
            cause,
            remediation=replace(cause.remediation, steps=(*cause.remediation.steps, step)),
            detail={**cause.detail, "artists": summary, "left": left},
        ),
    )


def _repair_one(store: review.ReviewStore, found: catalogue.Catalogue, subject: _Subject,
                done: _Run) -> bool:
    """Read one release's artist and write it. Whether the provider FAILED the read.

    ONLY THE SEAM'S OWN EXCEPTION MEANS NOT SERVED, on the reasoning
    ``label approved`` gives for its own read: ``LookupError`` would also catch
    a client that failed to parse a payload, and that release is unread, not
    gone. A ``CratekitError`` is the catalogue or the gate refusing the run and
    is the caller's to stop on.
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
    if outcome == REPAIRED:
        done.record(
            subject, REPAIRED, "ok",
            f"{_named(subject)} now reads its artist, {name}", artist=name,
        )
    elif outcome == ALREADY_FINE:
        done.record(
            subject, ALREADY_FINE, "info",
            f"{_named(subject)} stopped reading an address while it was being "
            f"read, so what it reads now was kept",
        )
    else:
        done.record(
            subject, DECIDED, "info",
            f"{_named(subject)} was decided, or left review, while it was being "
            f"read, so it was not rewritten",
        )
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
            # OPENED ON THE FIRST RELEASE THAT NEEDS IT, so a queue with no
            # address in it spends no login and meets no credential refusal.
            found = catalogue.resolve(cfg)
        failed = _repair_one(store, found, subject, done)
        failed_in_a_row = failed_in_a_row + 1 if failed else 0
        if failed_in_a_row >= catalogue.READS_FAILED_IN_A_ROW:
            # THE RUN STOPS BEFORE A READ IT ALREADY KNOWS IS WASTED, on the
            # bound a sweep and a judging pass give an outage.
            break
    if done.counts[UNREAD]:
        # AFTER THE WALK AND NOT ONLY BEFORE THE NEXT READ, so an outage over
        # the last releases of a run is the same refusal as one over the
        # first, and a run that left a release unread never exits clean.
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
    # ONE OPEN OF THE STORE FOR THE RUN. It holds no transaction between
    # writes, so the paced reads keep nobody out of the queue.
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
        _check(
            "fine",
            "ok",
            f"{done.counts[ALREADY_FINE]} open label release(s) do not read an "
            f"address and were not rewritten",
        ),
    ]
    if done.counts[DECIDED]:
        lines.append(
            _check(
                "decided",
                "info",
                f"{done.counts[DECIDED]} release(s) reading an address are decided "
                f"or left review, and a decided item is never rewritten",
            )
        )
    return ctx.envelope(
        data={"checks": [*lines, *done.checks], "summary": done.summary()},
        outcome=Outcome.OK if done.counts[REPAIRED] else Outcome.NO_OP,
    )


__all__ = [
    "ADDRESS",
    "ALREADY_FINE",
    "DECIDED",
    "NOT_SERVED",
    "OUTCOMES",
    "REPAIRED",
    "UNADDRESSED",
    "UNNAMED",
    "UNREAD",
    "build_artists",
    "is_address",
    "label_artists",
]
