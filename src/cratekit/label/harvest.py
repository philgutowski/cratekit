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

_YEAR = re.compile(r"^\(?[PC]\)?\s*", re.IGNORECASE)
_YEAR_NUM = re.compile(r"^\d{4}\s+")


@dataclass(frozen=True, slots=True)
class HarvestDrop:
    name: str
    reason: str


@dataclass(frozen=True, slots=True)
class HarvestReport:
    offered: tuple[review.Item, ...]
    dropped: tuple[HarvestDrop, ...]


def labels_from_copyright(track: Any) -> tuple[str, ...]:
    """Pull a label name off a copyright or label credit, if one is there."""
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
