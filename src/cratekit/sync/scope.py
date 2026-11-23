"""Most-recent-N minus owned identities. The watermark is never an input.

Watermarks are audit records that gate nothing (KTD11); using one as a date
floor is the silent zero-scope failure.
"""

from __future__ import annotations

from collections.abc import Container, Sequence
from typing import Protocol


class ScopedItem(Protocol):
    """Anything with a stable identity. Display names are not identities."""

    identity: str


def scoped(
    candidates: Sequence[ScopedItem],
    *,
    owned: Container[str],
    limit: int,
) -> list[ScopedItem]:
    """Return up to ``limit`` unowned candidates in source order (newest first).

    No sorting and no watermark; an empty owned set simply keeps the first
    ``limit`` items.
    """
    if limit < 0:
        raise ValueError("limit is a count, never negative")
    taken: list[ScopedItem] = []
    for item in candidates:
        if item.identity in owned:
            continue
        taken.append(item)
        if len(taken) >= limit:
            break
    return taken
