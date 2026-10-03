"""Label catalogue listings. Every call goes through the pagination wrappers.

A hand-written page loop here would be the fourth copy of a defect this
repository already removed: a listing that quietly returns one page looks
exactly like a short catalogue. The wrapper reads a label roster, a
``listing.HeldReleases``, whole rather than paging it (R-888).
"""

from __future__ import annotations

from typing import Any

from cratekit.acquire import listing

#: The listing methods a crawl will actually TRY, which are the ones
#: ``listing.artist_releases`` tries by default, imported from the constant it
#: owns rather than restated here. A second written copy of the names is a copy
#: that goes stale in silence: the wrapper skips a method it cannot find, so a
#: caller checking an artist object against a stale list would either refuse
#: one the crawl could have read or accept one it could not. The first draft
#: read them off that function's signature with ``inspect``, which met the same
#: goal and broke the whole label package at import the day the parameter was
#: renamed or the default resolved inside the body.
LISTING_METHODS: tuple[str, ...] = listing.RELEASE_METHODS


def releases(artist: Any, **kwargs: Any) -> list[Any]:
    """Every release credited to the label artist, across both listing methods."""
    return listing.artist_releases(artist, **kwargs)


def can_list(artist: Any) -> bool:
    """Whether this artist object exposes any listing method a crawl can use.

    ``listing.artist_releases`` SKIPS a method it cannot find rather than
    raising, and that is right where it sits: the two names have moved between
    client versions and losing one of two listings is a smaller failure than
    refusing to crawl at all. When NONE of them is present the same rule returns
    an empty list from an object nobody ever read, and an unreadable catalogue
    becomes indistinguishable from a label with nothing new in it. That is
    R-135.

    This is the question a caller asks BEFORE it is willing to believe an empty
    answer. It is a separate function rather than a raise inside
    :func:`releases`, because ``releases`` has other callers and the decision of
    what an absence MEANS belongs to the caller that is about to report it.

    It answers about the DEFAULT method set. A caller that overrides ``methods``
    on :func:`releases` is asking a different question and must ask it itself,
    which no caller in this package does.

    A ``listing.HeldReleases`` is asked what it holds, the same question the
    read asks it, rather than probed for paging methods it has no need of.
    """
    if isinstance(artist, listing.HeldReleases):
        return any(artist.held(method) is not None for method in LISTING_METHODS)
    return any(getattr(artist, method, None) is not None for method in LISTING_METHODS)
