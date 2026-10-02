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
write. Every other field of the payload is written back as it was read a moment
before the write, so what a judging job stamped meanwhile is kept.

AN ADDRESS IS NEVER REPLACED BY NOTHING. A release the provider no longer
serves, one it could not answer about, and one it names no artist for are each
counted and left reading what they read.

IT DECIDES NOTHING AND DOWNLOADS NOTHING. Each release asked about costs one
provider read, paced by the provider gate the catalogue is opened with, and the
catalogue is not opened at all when no item reads an address.

Layer: modules.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from typing import Any

from cratekit.cli.output import Envelope
from cratekit.core import config, review
from cratekit.core.cause import CratekitError, Outcome, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.review import Queue
from cratekit.label import catalogue, sweep
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


def _listed(cfg: config.Config) -> tuple[list[_Subject], dict[str, int]]:
    """Every open item that reads an address, and the counts of the ones left out.

    READ OFF THE REVIEW QUEUE AND NOTHING ELSE. ``list_items`` lists what is
    unresolved, so a decided item is never seen here. An item carrying a verdict
    this build cannot read is listed and is somebody's decision all the same,
    so it is counted decided and not asked about.
    """
    counts = dict.fromkeys(OUTCOMES, 0)
    found: list[_Subject] = []
    with review.open_store(cfg) as store:
        page = review.list_items(
            store, queue=str(Queue.LABEL_RELEASE), kinds=(sweep.KIND,), limit=None
        )
        for item in page.items:
            if not is_address(item.payload.get("artist")):
                counts[ALREADY_FINE] += 1
                continue
            if item.stored_verdict is not None:
                counts[DECIDED] += 1
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
    return found, counts


def _written(cfg: config.Config, subject: _Subject, name: str) -> bool:
    """Write ``name`` as the item's artist, over the payload AS IT IS NOW.

    READ AGAIN BEFORE THE WRITE. The listing is as old as every paced read
    since, and a payload written from it would take back whatever a judging job
    stamped on the item meanwhile. False when the item was decided, left
    review, or stopped reading an address in that time: nothing is written.
    """
    with review.open_store(cfg) as store:
        current = review.find(store, subject.item_id)
        if current is None or current.stored_verdict is not None:
            return False
        if not is_address(current.payload.get("artist")):
            return False
        changed = review.redescribe(
            store, subject.item_id, {**current.payload, "artist": name}
        )
    return changed is not None


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
    """What one run did so far: the counts, the lines, and the calls it spent."""

    counts: dict[str, int]
    checks: list[dict[str, Any]]
    releases: list[dict[str, Any]]
    asked: int = 0

    def record(self, subject: _Subject, outcome: str, status: str, detail: str,
               artist: str | None = None) -> None:
        self.counts[outcome] += 1
        self.checks.append(
            _check(f"release.{subject.release_id or subject.item_id}", status, detail)
        )
        self.releases.append(
            {
                "release_id": subject.release_id,
                "item_id": subject.item_id,
                "label_id": subject.label_id,
                "label_name": subject.label_name,
                "title": subject.title,
                "outcome": outcome,
                "artist": artist,
            }
        )

    def summary(self, addresses: int) -> dict[str, Any]:
        return {
            "addresses": addresses,
            **self.counts,
            "provider_reads": self.asked,
            "releases": list(self.releases),
        }


def _with_counts(
    error: CratekitError, done: _Run, addresses: int, listed: int
) -> CratekitError:
    """The same refusal, carrying what the run did before it stopped.

    A refusal is the exit a person most needs the counts from: items were
    repaired before it. The cause is extended and never rebuilt by hand, so its
    remedy and its trail come through unchanged. ``left`` is counted against
    the items this run set out to read, each of which is recorded once reached.
    """
    left = listed - len(done.releases)
    cause = error.cause
    step = (
        f"{done.counts[REPAIRED]} release(s) were given their artist before this "
        f"and {left} were not reached; run crate label artists again, which asks "
        f"only about the ones still reading an address"
    )
    return rebuilt(
        error,
        replace(
            cause,
            remediation=replace(cause.remediation, steps=(*cause.remediation.steps, step)),
            detail={**cause.detail, "artists": done.summary(addresses), "left": left},
        ),
    )


def _repair_one(cfg: config.Config, found: catalogue.Catalogue, subject: _Subject,
                done: _Run) -> bool:
    """Read one release's artist and write it. Whether the provider FAILED the read.

    ONLY THE SEAM'S OWN EXCEPTION MEANS NOT SERVED, on the reasoning
    ``label approved`` gives for its own read: ``LookupError`` would also catch
    a client that failed to parse a payload, and that release is unread, not
    gone. A ``CratekitError`` is the catalogue or the gate refusing the run and
    is the caller's to stop on.
    """
    done.asked += 1
    try:
        name = found.release_artist(subject.release_id)
    except CratekitError:
        raise
    except catalogue.ReleaseUnresolvable as exc:
        done.record(
            subject, NOT_SERVED, "info",
            f"{_named(subject)} is no longer served by the provider ({exc}); its "
            f"item is left as it is",
        )
        return False
    except Exception as exc:  # noqa: BLE001 - named per release, never swallowed
        done.record(
            subject, UNREAD, "fail",
            f"{_named(subject)} could not be read from the provider "
            f"({type(exc).__name__}: {exc}); its item is left as it is, and "
            f"another run asks again",
        )
        return True
    name = _text(name)
    if not name:
        done.record(
            subject, UNNAMED, "info",
            f"the provider names no artist for {_named(subject)}; its item is "
            f"left as it is",
        )
    elif _written(cfg, subject, name):
        done.record(
            subject, REPAIRED, "ok",
            f"{_named(subject)} now reads its artist, {name}", artist=name,
        )
    else:
        done.record(
            subject, DECIDED, "info",
            f"{_named(subject)} was decided, or left review, while it was being "
            f"read, so it was not rewritten",
        )
    return False


def label_artists(ctx) -> Envelope:
    """Give every open label release that reads an address its artist's name."""
    cfg = label_cli._load()
    subjects, counts = _listed(cfg)
    done = _Run(counts=counts, checks=[], releases=[])
    addresses = len(subjects) + counts[DECIDED]
    found: catalogue.Catalogue | None = None
    failed_in_a_row = 0
    try:
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
            if failed_in_a_row >= catalogue.READS_FAILED_IN_A_ROW:
                # THE RUN STOPS BEFORE A READ IT ALREADY KNOWS IS WASTED, on the
                # bound a sweep and a judging pass give an outage.
                raise refuse(
                    "unavailable-transient",
                    f"the provider failed {catalogue.READS_FAILED_IN_A_ROW} release "
                    f"reads in a row, so the run stopped reading. Those releases "
                    f"still read an address",
                    remedy=Remedy.RETRY_LATER,
                    origin=ORIGIN,
                )
            if found is None:
                # OPENED ON THE FIRST RELEASE THAT NEEDS IT, so a queue with no
                # address in it spends no login and meets no credential refusal.
                found = catalogue.resolve(cfg)
            failed = _repair_one(cfg, found, subject, done)
            failed_in_a_row = failed_in_a_row + 1 if failed else 0
    except CratekitError as stopped:
        raise _with_counts(stopped, done, addresses, len(subjects)) from stopped

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
            f"{done.counts[ALREADY_FINE]} open label release(s) already read an "
            f"artist and were not asked about",
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
        data={"checks": [*lines, *done.checks], "summary": done.summary(addresses)},
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
