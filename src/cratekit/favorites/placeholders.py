"""The quarterly favourites placeholder playlists, named once.

The source system puts the hearts the library does not own into one private
provider playlist per UTC quarter, ``Favorites 2026-Q2``, and those playlists are
the favourites source's to sweep. They are account playlists like any other, so
the playlists source would sweep them a second time unless it can tell them
apart, and the name is the only thing that tells them apart: no identifier for
them is recorded anywhere this build reads.

A MODULE OF ITS OWN, WITH NO IMPORTS FROM THE PRODUCT, so the playlists source,
which is core and runs on the slim profile, can ask the question without
importing the favourites CLI or the outbound engines behind it (KTD7).
``cratekit.favorites.cli`` re-exports both names, which is where a reader of the
favourites source looks for them.

Layer: modules.
"""

from __future__ import annotations

import re

#: The leading word every placeholder name carries, followed by its quarter.
PLACEHOLDER_PREFIX = "Favorites "

#: The quarter the source system could not date a heart into. Its hearts sit in
#: this one playlist until a later run resolves a date and moves them, so it is
#: the favourites source's in exactly the way a dated quarter is.
BACKLOG = "(undated backlog)"

#: A whole placeholder name, a dated quarter or the backlog. Anchored at both
#: ends by ``fullmatch`` at the call site, so ``All Favorites`` and
#: ``Favorites 2026-Q2 copy`` are not placeholders.
PLACEHOLDER_NAME = re.compile(
    re.escape(PLACEHOLDER_PREFIX) + r"(?:\d{4}-Q[1-4]|" + re.escape(BACKLOG) + r")"
)


def placeholder_name(quarter: str) -> str:
    """The placeholder playlist name for a quarter label such as ``2026-Q2``."""
    return f"{PLACEHOLDER_PREFIX}{quarter}"


def is_placeholder(name: str) -> bool:
    """Whether ``name`` is exactly a favourites placeholder's name, dated or backlog."""
    return PLACEHOLDER_NAME.fullmatch(str(name or "")) is not None


__all__ = [
    "BACKLOG",
    "PLACEHOLDER_NAME",
    "PLACEHOLDER_PREFIX",
    "is_placeholder",
    "placeholder_name",
]
