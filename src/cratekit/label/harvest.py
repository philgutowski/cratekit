"""Harvest record labels from a playlist's tracks. Imports nothing.

A copyright string is a discovery heuristic. Each candidate is verified
before it is offered, and an unconfirmed name never lands in the registry.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Any

from cratekit.acquire import listing
from cratekit.core import review
from cratekit.core.review import Queue

KIND = "harvested-label"
HANDLER_KEY = "label.harvest"

# THE MARK IS PARENTHESISED OR A SYMBOL, and nothing else (U237). A bare leading
# P or C is the label's own first letter: ``Cadenza``, ``Pressure Traxx``.
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)+", re.IGNORECASE)
# A year alone, with no name after it, names no label.
_YEAR_NUM = re.compile(r"^\d{4}(?:\s+|\.?$)")


@dataclass(frozen=True, slots=True)
class HarvestDrop:
    name: str
    reason: str


@dataclass(frozen=True, slots=True)
class HarvestReport:
    offered: tuple[review.Item, ...]
    dropped: tuple[HarvestDrop, ...]


@dataclass(frozen=True, slots=True)
class Decided:
    """The harvest's items on the queue, split by what a person decided.

    ``accepted`` pairs each accepted item's identifier with the label name it
    names. ``nameless`` is the accepted items that name no label at all, kept
    so they are reported rather than skipped. An item whose stored verdict this
    build cannot read counts as OPEN, the direction ``review`` argues for
    everywhere: undecided rather than decided the wrong way.
    """

    accepted: tuple[tuple[str, str], ...]
    nameless: tuple[str, ...]
    rejected: int
    still_open: int


def _text(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


def decided(store: review.ReviewStore) -> Decided:
    """Every harvested label on the queue, in queue order, split by verdict.

    The name is read from the item's IDENTITY before its payload, as
    ``label approved`` reads a release: the identity is what harvest keyed the
    item on, and an item that arrived through ``review import`` carries none,
    so the payload's copy is what is left.
    """
    page = review.list_items(
        store,
        queue=str(Queue.LABEL_RELEASE),
        kinds=(KIND,),
        include_resolved=True,
        limit=None,
    )
    accepted: list[tuple[str, str]] = []
    nameless: list[str] = []
    rejected = still_open = 0
    for item in page.items:
        if item.verdict is review.Verdict.ACCEPTED:
            identity = review.identity_of(store, item.item_id) or {}
            name = _text(identity.get("name")) or _text(item.payload.get("name"))
            if name is None:
                nameless.append(item.item_id)
            else:
                accepted.append((item.item_id, name))
        elif item.verdict is review.Verdict.REJECTED:
            rejected += 1
        else:
            still_open += 1
    return Decided(
        accepted=tuple(accepted),
        nameless=tuple(nameless),
        rejected=rejected,
        still_open=still_open,
    )


def labels_from_copyright(track: Any) -> tuple[str, ...]:
    """Pull a label name off a copyright or label credit, if one is there.

    Strips a leading ``(P)``, ``(C)``, ``℗`` or ``©`` and then a four digit
    year, and keeps every letter of the name after them.
    """
    text = getattr(track, "copyright", None) or getattr(track, "label", None) or ""
    cleaned = _YEAR.sub("", str(text)).strip()
    cleaned = _YEAR_NUM.sub("", cleaned).strip(" .")
    return (cleaned,) if cleaned else ()


def playlist_tracks(playlist: Any, **kwargs: Any) -> list[Any]:
    """Every track in the playlist, across pages."""
    return listing.playlist_tracks(playlist, **kwargs)


def from_tracks(
    tracks: Sequence[Any] | Iterable[Any],
    *,
    store: review.ReviewStore,
    verify: Callable[[str], dict[str, Any]],
    extract: Callable[[Any], Sequence[str]] = labels_from_copyright,
    handler_key: str = HANDLER_KEY,
) -> HarvestReport:
    """Offer verified labels. Does not add them to the registry and writes no audio."""
    seen: set[str] = set()
    offered: list[review.Item] = []
    dropped: list[HarvestDrop] = []
    for track in tracks:
        for name in extract(track):
            key = name.casefold()
            if key in seen:
                continue
            seen.add(key)
            verdict = verify(name)
            status = str(verdict.get("verdict") or "unconfirmed")
            if status != "confirmed":
                dropped.append(HarvestDrop(name=name, reason=status))
                continue
            offered.append(
                review.offer(
                    store,
                    queue=Queue.LABEL_RELEASE,
                    kind=KIND,
                    identity={"name": name},
                    payload={"name": name, "source": "harvest"},
                    handler_key=handler_key,
                )
            )
    return HarvestReport(offered=tuple(offered), dropped=tuple(dropped))
