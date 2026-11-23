"""Label catalogue listings. Every call goes through the pagination wrappers.

A hand written page loop here would bring back a listing that quietly returns
one page, which looks exactly like a short catalogue. A label roster, a
``listing.HeldReleases``, is read whole rather than paged (R-888).
"""

from __future__ import annotations

from typing import Any

from cratekit.acquire import listing

#: The listing methods a crawl tries, ``listing.artist_releases``'s own
#: constant rather than a copy that would go stale in silence.
LISTING_METHODS: tuple[str, ...] = listing.RELEASE_METHODS


def releases(artist: Any, **kwargs: Any) -> list[Any]:
    """Every release credited to the label artist, across both listing methods."""
    return listing.artist_releases(artist, **kwargs)


def can_list(artist: Any) -> bool:
    """Whether this artist object exposes any listing method a crawl can use.

    ``listing.artist_releases`` skips a method it cannot find, so with none
    present it returns an empty list from an object nobody read, and an
    unreadable catalogue looks like a label with nothing new (R-135). A caller
    asks this before it believes an empty answer. It answers about the default
    method set. A ``listing.HeldReleases`` is asked what it holds.
    """
    if isinstance(artist, listing.HeldReleases):
        return any(artist.held(method) is not None for method in LISTING_METHODS)
    return any(getattr(artist, method, None) is not None for method in LISTING_METHODS)
