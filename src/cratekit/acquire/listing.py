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

1. **Pages to exhaustion under a DECLARED stop rule and a DECLARED request
   budget.** This module shipped with one hard coded rule instead, stopping on a
   page shorter than the size it asked for, and that rule was wrong. The provider
   omits items it will not serve from a window while still counting them in it,
   so a full window arrives short and the walk ends inside the collection.
   Measured live on 2026-09-17: an account holding 197 favourite tracks read back
   as 93 (R-383, U65). Every shape now says which rule it uses and why, because
   the convention is an assumption about the PROVIDER and not a property of
   offset and limit APIs in general.
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
from enum import Enum
from typing import Any


class StopRule(Enum):
    """How a walk decides it has reached the end of a listing.

    The value of each member is the phrase a wrapper's docstring must use for it,
    so the prose and the table cannot drift apart unnoticed.

    ``EMPTY_PAGE`` walks until a page comes back with nothing in it. It is the
    only rule that is safe against a provider that omits items from a window,
    and it costs exactly one extra request per listing.

    ``SHORT_PAGE`` stops as soon as a page comes back with fewer items than the
    size it asked for. It saves that one request and is correct ONLY where the
    provider is known to serve every window full. No shape declares it today.
    It is kept declarable rather than deleted because the saving is real for a
    listing that is read per item in a crawl, and a future shape that can prove
    the provider serves it full should be able to say so in one word.
    """

    EMPTY_PAGE = "empty page"
    SHORT_PAGE = "short page"

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

#: The stop rule each listing shape declares. Every shape reads to an empty page,
#: and the reason is the same for all four: the evidence that any of them is safe
#: on the short page rule is one account read on one day that happened to contain
#: no omitted items, which is absence read as evidence of absence. The one that
#: was measured broken, ``favorite_tracks``, was also measured clean by that same
#: standard the week before. Each wrapper's docstring carries its own argument.
STOP_RULES: dict[str, StopRule] = {
    "playlist_tracks": StopRule.EMPTY_PAGE,
    "account_playlists": StopRule.EMPTY_PAGE,
    "favorite_tracks": StopRule.EMPTY_PAGE,
    "artist_releases": StopRule.EMPTY_PAGE,
}

#: REQUEST budgets, per listing shape, not item budgets. A walk that spends its
#: budget without reaching the end raises :class:`ListingTruncated` rather than
#: returning, because the only thing that produces a full page every time is an
#: offset parameter the provider is ignoring, and a capped length answer is
#: indistinguishable from a complete one.
#:
#: Sized far above any real collection on purpose, since a cap that can fire on
#: real data turns a correctness fix into an outage. The largest reads this
#: project has actually measured, live on 2026-09-17, are written beside each one
#: so the margin is visible rather than asserted.
PAGE_CAPS: dict[str, int] = {
    "playlist_tracks": 200,  # 20,000 tracks. Largest measured: 197 in one playlist.
    "account_playlists": 400,  # 20,000 playlists. Largest measured: 599.
    "favorite_tracks": 200,  # 20,000 tracks. Largest measured: 197.
    # 10,000 releases PER RELEASE METHOD. ``artist_releases`` walks each method
    # separately, so this budget is spent once per method and not once per artist.
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


class ListingTruncated(RuntimeError):
    """A walk spent its whole request budget without reaching the end.

    Raised rather than returning what was collected, on the same argument
    :class:`ListingNotPaginated` makes: a truncated listing is indistinguishable
    from a short one, and every downstream decision then treats absent items as
    deleted ones. Before U65 this condition returned silently, which meant the
    runaway guard converted a hang into a wrong answer.
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
    stop: StopRule,
    max_pages: int,
    shape: str | None = None,
    key: Callable[[Any], Any] | None = None,
    **retry: Any,
) -> list[Any]:
    """Every item across every server page, in listing order.

    **``stop`` and ``max_pages`` are required and have no defaults, deliberately.**
    A wrapper that forgets to choose fails to call rather than inheriting whatever
    the last author assumed. That is the whole shape of R-383: one rule, written
    once into this function, silently governing four listings that were never
    individually checked against it. A default here would rebuild that.

    ``key`` turns on identifier-based deduplication. It is off by default because
    dropping a legitimate duplicate is its own defect: a playlist may contain the
    same track twice on purpose, and silently collapsing that changes the user's
    playlist. It is on for the listings where the provider itself can repeat an
    item across pages.

    ``max_pages`` is a budget of REQUESTS, and spending it raises. A provider that
    keeps returning full pages forever, which a broken offset parameter produces
    exactly, otherwise turns a listing read into an unbounded loop that looks like
    a hang. Stopping quietly at the budget is not the fix for that: it trades a
    hang for a wrong answer nobody can see.

    ``shape`` names the listing in that exception and does nothing else. It is
    optional so this function stays a mechanism a test can drive directly, while
    :data:`STOP_RULES` and :data:`PAGE_CAPS` hold the policy.
    """
    items: list[Any] = []
    seen: set[Any] = set()
    offset = 0
    pages = 0

    while True:
        if pages >= max_pages:
            raise ListingTruncated(
                f"{shape or 'listing'} spent its whole budget of {max_pages} requests "
                f"at {page_size} per page without reaching the end, having collected "
                f"{len(items)} item(s). The budget is sized far above any real "
                f"collection, so reaching it means the provider is not advancing its "
                f"window and the offset parameter is the suspect. Returning the "
                f"{len(items)} would be a truncated listing indistinguishable from a "
                f"complete one, which is the thing this module refuses to guess at"
            )
        page = fetch_with_retry(fetch_page, limit=page_size, offset=offset, **retry)
        page = list(page or [])
        pages += 1
        if not page:
            break
        for item in page:
            if key is not None:
                identity = key(item)
                if identity in seen:
                    continue
                seen.add(identity)
            items.append(item)
        if stop is StopRule.SHORT_PAGE and len(page) < page_size:
            break
        offset += page_size

    return items


def _shape(name: str, **overrides: Any) -> dict[str, Any]:
    """The declared pagination policy for one listing shape, as call arguments.

    Read from the tables rather than written out at each wrapper, so a shape's
    rule and its budget cannot come to disagree with what the tables say about
    it, and so adding a shape is one row in each table rather than a literal
    copied into a function body.
    """
    return {
        "shape": name,
        "page_size": PAGE_SIZES[name],
        "stop": STOP_RULES[name],
        "max_pages": PAGE_CAPS[name],
        **overrides,
    }


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

    Stops on an **empty page**, not a short one. A playlist can hold a track the
    account cannot play, and the provider omits it from the window it serves
    while still counting it, so a full window arrives short. This is the read the
    quarterly placeholder acquire walks, so a short page taken as the end would
    drop the rest of a playlist of tracks Phillip does not own yet, which is the
    one listing whose omissions nothing downstream can notice.

    No deduplication: a playlist that lists a track twice means it twice.
    """
    return paginate(_paged_caller(playlist, "tracks"), **_shape("playlist_tracks", **kwargs))


def favorite_tracks(session: Any, **kwargs: Any) -> list[Any]:
    """Every track the account has favourited, deduplicated by track identifier.

    Stops on an **empty page**, not a short one. This is the listing R-383 was
    measured on: 197 favourites read back as 93, because the provider omits the
    tracks it will not serve from each window while counting them in it. Its own
    client corroborates that, ``Favorites.get_tracks_count`` documenting that the
    total it returns "also includes track that may not be available for
    playback". The ordering is newest first, which is what made it hard to see:
    the rows that do come back are the recent ones, so the defect bites only on
    questions about OLD state, and ``TidalAccount.has_heart`` asks exactly that.

    Deduplicated because this listing is ordered by when the favourite was
    created, and a favourite added while the read is in progress shifts every
    later item by one, which re-serves the item on the page boundary.
    """
    favorites = session.user.favorites
    kwargs.setdefault("key", lambda track: str(getattr(track, "id", "")))
    return paginate(_paged_caller(favorites, "tracks"), **_shape("favorite_tracks", **kwargs))


def account_playlists(session: Any, **kwargs: Any) -> list[Any]:
    """Every playlist the listing exposes for this account, across pages.

    Stops on an **empty page**, not a short one. This listing read 599 both ways
    when it was walked by hand on 2026-09-17, so nothing was omitted from it that
    day, and that is the whole of the evidence for it. A playlist the account can
    no longer open is the same shape of omission the favourites listing was
    measured on, and one clean read is not a property of the endpoint. The cost
    of being wrong here is `sync all` silently skipping playlists; the cost of
    being right is one request.

    Returns the provider's own objects rather than reduced dictionaries.
    Filtering to the ones the account CREATED is a policy question that differs
    per caller, and a wrapper that answered it would be two things at once: this
    one is pagination and nothing else.
    """
    kwargs.setdefault("key", lambda playlist: str(getattr(playlist, "id", "")))
    return paginate(
        _paged_caller(session.user, "playlist_and_favorite_playlists"),
        **_shape("account_playlists", **kwargs),
    )


#: The two release listings a provider artist exposes, and the ones
#: :func:`artist_releases` reads by default. Owned here so a caller that has to
#: ask "can this object be listed at all" (``label.crawl.can_list``) checks the
#: same names the crawl will try, without a second written copy of them.
RELEASE_METHODS: tuple[str, ...] = ("get_albums", "get_ep_singles")


def artist_releases(artist: Any, methods: Iterable[str] = RELEASE_METHODS,
                    **kwargs: Any) -> list[Any]:
    """Every release credited to an artist, across both release-type listings.

    Stops on an **empty page**, not a short one, and this is the shape where that
    costs the most: the walk runs once per release method per artist, and almost
    every artist fits inside a single page today, so a label crawl over A artists
    pays 2A requests it did not pay before. It is still the right rule. A label
    catalogue that stops early is this product's core job done wrong, and a
    prolific artist crossing the page boundary is exactly where the omission
    would land. The extra requests make a sweep slower, which
    :func:`fetch_with_retry` already absorbs; an early stop makes it wrong, which
    nothing absorbs. Recorded with its arithmetic as R-384.

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
            _paged_caller(artist, method), **_shape("artist_releases", **kwargs)
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
    "PAGE_CAPS",
    "PAGE_SIZES",
    "PAGINATION_KEYWORDS",
    "RELEASE_METHODS",
    "STOP_RULES",
    "WRAPPERS",
    "ListingNotPaginated",
    "ListingTruncated",
    "StopRule",
    "account_playlists",
    "artist_releases",
    "favorite_tracks",
    "fetch_with_retry",
    "paginate",
    "playlist_tracks",
]
