"""Most-recent-N plus owned-dedup. The watermark is not an input.

KTD11: watermarks are audit records that gate nothing on their own. Scope comes
from the newest N candidates the source listed, minus identities already owned.
Using the watermark as a date floor is the silent zero-scope failure this
repository already removed once.
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
    """Return up to ``limit`` unowned candidates, preserving source order.

    The source lists newest first. This function does not sort, does not read a
    watermark, and does not treat an empty owned set as "everything is new" in
    any special way: empty owned simply keeps the first ``limit`` items.
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
