"""Label catalogue listings. Every call goes through the pagination wrappers.

A hand-written page loop here would be the fourth copy of a defect this
repository already removed: a listing that quietly returns one page looks
exactly like a short catalogue.
"""

from __future__ import annotations

from typing import Any

from cratekit.acquire import listing


def releases(artist: Any, **kwargs: Any) -> list[Any]:
    """Every release credited to the label artist, across both listing methods."""
    return listing.artist_releases(artist, **kwargs)
