"""One pagination wrapper per listing shape. No call site pages by hand.

THE DEFECT THIS ENDS. The provider's client returns ONE server page when asked
for a listing without pagination arguments, and it returns it without complaint.
A playlist of 250 tracks reads back as 100, a favourites library of 1,400 reads
back as 100, and nothing anywhere reports a truncation, because from the caller's
side a short list and a complete list are the same object. In the source system
this was written three separate times, by three independent call sites, and each
one had to rediscover it. Two of them got the page size right; the third called a
listing method with no arguments at all.

That is why the wrappers live in the adapter unit rather than beside their
callers. The page size is a property of the PROVIDER, and the adapter is the one
place that is allowed to know about the provider. A listing helper next to its
caller is a listing helper that a fourth caller will not find.

THE THREE THINGS EACH WRAPPER DOES, and why each is not optional:

1. **Pages to exhaustion**, stopping on a short page rather than on an empty one.
   Stopping only on empty costs one wasted round trip per listing; stopping on
   short is correct and is what the source system's two working loops do.
2. **Retries a transient failure with capped exponential backoff.** A first full
   read of a large favourites library is dozens of requests, and a rate limit
   partway through drops a page. A dropped page in a paginated read is not an
   error the caller sees, it is a gap in the answer.
3. **Deduplicates by identifier where the provider can repeat one.** A listing
   that is being edited while it is read can return the same item on two pages.

WHAT IS NOT HERE. Nothing calls the network in this module by itself; every
wrapper takes the provider object or a page-fetching callable, which is what lets
the whole module be proven against fakes with no account and no session.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterable
from typing import Any

#: Server page ceilings, per listing shape. These are the PROVIDER's numbers, not
#: preferences: asking for more returns the ceiling, and asking for fewer costs
#: extra round trips. Named per shape because they genuinely differ, and a single
#: shared constant would silently be wrong for one of them.
PAGE_SIZES: dict[str, int] = {
    "playlist_tracks": 100,
    "account_playlists": 50,
    "favorite_tracks": 100,
    "artist_releases": 100,
}

DEFAULT_MAX_RETRIES = 5
DEFAULT_BASE_DELAY_S = 1.0
DEFAULT_MAX_DELAY_S = 30.0


class ListingNotPaginated(RuntimeError):
    """A provider listing method accepted no pagination arguments.

    Raised rather than silently taking the single page it can serve. The source
    system's fallback did take that page, which is defensible for a playlist read
    that is mostly short, and indefensible as a general rule: a listing that
    quietly truncates is indistinguishable from a listing that is short, and
    every downstream decision then treats absent items as deleted ones.
    """


def fetch_with_retry(
    fetch_page: Callable[[int, int], Any],
    *,
    limit: int,
    offset: int,
    max_retries: int = DEFAULT_MAX_RETRIES,
    base_delay: float = DEFAULT_BASE_DELAY_S,
    max_delay: float = DEFAULT_MAX_DELAY_S,
    sleep: Callable[[float], None] = time.sleep,
) -> Any:
    """One page, retried on any transient failure, then re-raised.

    Ported in rule from the source system's hearts reader. Retrying ANY exception
    is deliberate breadth: the failures worth retrying here are rate limits,
    timeouts, and server errors, and the client raises them as several unrelated
    types across versions. Bounding the retries and re-raising at the ceiling is
    what keeps that breadth honest, since a permanent failure still surfaces, just
    later.
    """
    attempt = 0
    while True:
        try:
            return fetch_page(limit, offset)
        except Exception:  # noqa: BLE001 - see docstring: bounded, then re-raised
            attempt += 1
            if attempt > max_retries:
                raise
            sleep(min(max_delay, base_delay * (2 ** (attempt - 1))))


def paginate(
    fetch_page: Callable[[int, int], Any],
    *,
    page_size: int,
    key: Callable[[Any], Any] | None = None,
    max_pages: int | None = None,
    **retry: Any,
) -> list[Any]:
    """Every item across every server page, in listing order.

    ``key`` turns on identifier-based deduplication. It is off by default because
    dropping a legitimate duplicate is its own defect: a playlist may contain the
    same track twice on purpose, and silently collapsing that changes the user's
    playlist. It is on for the listings where the provider itself can repeat an
    item across pages.

    ``max_pages`` is a runaway guard. A provider that keeps returning full pages
    forever, which a broken offset parameter produces exactly, otherwise turns a
    listing read into an unbounded loop that looks like a hang.
    """
    items: list[Any] = []
    seen: set[Any] = set()
    offset = 0
    pages = 0

    while True:
        page = fetch_with_retry(fetch_page, limit=page_size, offset=offset, **retry)
        page = list(page or [])
        if not page:
            break
        for item in page:
            if key is not None:
                identity = key(item)
                if identity in seen:
                    continue
                seen.add(identity)
            items.append(item)
        pages += 1
        if len(page) < page_size:
            break
        if max_pages is not None and pages >= max_pages:
            break
        offset += page_size

    return items


def _paged_caller(owner: Any, method: str) -> Callable[[int, int], Any]:
    """Bind a provider listing method into the ``(limit, offset)`` shape.

    A method that rejects those arguments raises ``ListingNotPaginated`` instead
    of falling back to its single page. The distinction matters: a client version
    that dropped pagination is an upgrade problem the user can act on, while a
    truncated answer is a data-loss problem nobody can see.
    """
    fn = getattr(owner, method, None)
    if fn is None:
        raise ListingNotPaginated(
            f"{type(owner).__name__} has no {method!r} listing method; the provider "
            f"client changed shape and this wrapper needs updating with it"
        )

    def call(limit: int, offset: int) -> Any:
        try:
            return fn(limit=limit, offset=offset)
        except TypeError as exc:
            raise ListingNotPaginated(
                f"{type(owner).__name__}.{method} does not accept pagination "
                f"arguments, so it can only ever serve one page; a truncated listing "
                f"is indistinguishable from a short one and must not be guessed at"
            ) from exc

    return call


# ---------------------------------------------------------------------------
# The listing shapes. One wrapper each, and no call site may re-implement one.
# ---------------------------------------------------------------------------


def playlist_tracks(playlist: Any, **kwargs: Any) -> list[Any]:
    """Every track in a playlist, in playlist order, across pages.

    No deduplication: a playlist that lists a track twice means it twice.
    """
    return paginate(
        _paged_caller(playlist, "tracks"), page_size=PAGE_SIZES["playlist_tracks"], **kwargs
    )


def favorite_tracks(session: Any, **kwargs: Any) -> list[Any]:
    """Every track the account has favourited, deduplicated by track identifier.

    Deduplicated because this listing is ordered by when the favourite was
    created, and a favourite added while the read is in progress shifts every
    later item by one, which re-serves the item on the page boundary.
    """
    favorites = session.user.favorites
    return paginate(
        _paged_caller(favorites, "tracks"),
        page_size=PAGE_SIZES["favorite_tracks"],
        key=lambda track: str(getattr(track, "id", "")),
        **kwargs,
    )


def account_playlists(session: Any, **kwargs: Any) -> list[Any]:
    """Every playlist the listing exposes for this account, across pages.

    Returns the provider's own objects rather than reduced dictionaries.
    Filtering to the ones the account CREATED is a policy question that differs
    per caller, and a wrapper that answered it would be two things at once: this
    one is pagination and nothing else.
    """
    return paginate(
        _paged_caller(session.user, "playlist_and_favorite_playlists"),
        page_size=PAGE_SIZES["account_playlists"],
        key=lambda playlist: str(getattr(playlist, "id", "")),
        **kwargs,
    )


#: The two release listings a provider artist exposes, and the ones
#: :func:`artist_releases` reads by default. Owned here so a caller that has to
#: ask "can this object be listed at all" (``label.crawl.can_list``) checks the
#: same names the crawl will try, without a second written copy of them.
RELEASE_METHODS: tuple[str, ...] = ("get_albums", "get_ep_singles")


def artist_releases(artist: Any, methods: Iterable[str] = RELEASE_METHODS,
                    **kwargs: Any) -> list[Any]:
    """Every release credited to an artist, across both release-type listings.

    Two methods rather than one because the provider splits albums from
    extended plays and singles, and a label catalogue lives mostly in the second.
    Deduplicated across the two because a release can appear in both.

    A method the client does not expose is skipped rather than fatal: the two
    names have moved between client versions, and losing one listing is a smaller
    failure than refusing to crawl at all. A method that exists but cannot page IS
    fatal, for the reason ``_paged_caller`` states.
    """
    releases: list[Any] = []
    seen: set[str] = set()
    for method in methods:
        if getattr(artist, method, None) is None:
            continue
        for release in paginate(
            _paged_caller(artist, method), page_size=PAGE_SIZES["artist_releases"], **kwargs
        ):
            identity = str(getattr(release, "id", "")) or f"{method}:{len(releases)}"
            if identity in seen:
                continue
            seen.add(identity)
            releases.append(release)
    return releases


#: Every listing shape this module covers, as name to wrapper. The guard in the
#: test suite reads this to decide which provider method names may only be called
#: from here, so adding a wrapper arms the guard for it automatically (P3).
WRAPPERS: dict[str, Callable[..., list[Any]]] = {
    "playlist_tracks": playlist_tracks,
    "favorite_tracks": favorite_tracks,
    "account_playlists": account_playlists,
    "artist_releases": artist_releases,
}

#: The provider listing methods that must not be called outside this module.
#: ``tracks`` is on the list but is only a violation when called WITH pagination
#: arguments, because "tracks" is an ordinary accessor name that this codebase
#: also uses for its own collections, and a guard that fires on correct code gets
#: routed around rather than obeyed (P7).
GUARDED_METHODS = frozenset(
    {"tracks", "playlist_and_favorite_playlists", "get_albums", "get_ep_singles"}
)
PAGINATION_KEYWORDS = frozenset({"limit", "offset"})


__all__ = [
    "DEFAULT_BASE_DELAY_S",
    "DEFAULT_MAX_DELAY_S",
    "DEFAULT_MAX_RETRIES",
    "GUARDED_METHODS",
    "PAGE_SIZES",
    "PAGINATION_KEYWORDS",
    "RELEASE_METHODS",
    "WRAPPERS",
    "ListingNotPaginated",
    "account_playlists",
    "artist_releases",
    "favorite_tracks",
    "fetch_with_retry",
    "paginate",
    "playlist_tracks",
]
