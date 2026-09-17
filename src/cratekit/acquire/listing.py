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

   **The lesson underneath that, which cost this unit a whole fix round:** no
   page SHAPE can say where a filtered collection ends. Swapping the short page
   stop for an empty page stop only moves the boundary, since a window whose
   every counted item is unservable comes back empty mid collection. Only a count
   the provider declares for the collection it is serving closes the class, and
   two of the four shapes here have one.
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

    **The thing every rule here is up against** is a provider that serves a
    WINDOW of a counted collection and omits from that window the items it will
    not serve. The window is still ``page_size`` wide and the offset arithmetic
    is still right; what is wrong is any attempt to read the END of the
    collection off the SHAPE of a page.

    ``DECLARED_TOTAL`` stops when the offset has passed a total the provider
    itself declares, and reads no meaning into a page's shape at all. It is the
    only rule here that closes the class rather than narrowing it, and it is
    available only where the provider publishes a count for the same collection
    it is serving. It costs nothing extra: the count request replaces the
    terminating empty page, and for a playlist the count is already on the object.

    ``EMPTY_PAGE`` walks until a page comes back with nothing in it. It is
    SAFER than the short page rule and it is not safe. A window in which every
    counted item is unservable comes back empty in the middle of a collection,
    and this rule reads that as the end. That needs ``page_size`` consecutive
    unservable items, which is 100 for the track listings and 50 for account
    playlists, and a catalogue hearted in one batch and later withdrawn is how a
    run that long gets built. Declare it only where the provider publishes no
    total, and expect a residual to say so.

    ``SHORT_PAGE`` stops as soon as a page comes back with fewer items than the
    size it asked for. It saves one request and is correct ONLY where the
    provider is known to serve every window full. It is what R-383 was measured
    on. No shape declares it. It is kept declarable rather than deleted because
    the saving is real for a listing read per item in a crawl, and a future shape
    that can PROVE the provider serves it full should be able to say so in one
    word rather than reinventing the loop.
    """

    DECLARED_TOTAL = "declared total"
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

#: The stop rule each listing shape declares. Nothing here reads the end of a
#: collection off a page's shape any more. Two shapes can do better than that,
#: because the provider publishes a count for the same collection it serves; two
#: cannot, and they take the weaker rule and a residual saying so (R-385).
#: Each wrapper's docstring carries its own argument.
STOP_RULES: dict[str, StopRule] = {
    "playlist_tracks": StopRule.DECLARED_TOTAL,
    "account_playlists": StopRule.EMPTY_PAGE,
    "favorite_tracks": StopRule.DECLARED_TOTAL,
    "artist_releases": StopRule.EMPTY_PAGE,
}

#: REQUEST budgets, per listing shape, not item budgets. A walk that spends its
#: budget without reaching the end raises :class:`ListingTruncated` rather than
#: returning, because the only thing that produces a full page every time is an
#: offset parameter the provider is ignoring, and a capped length answer is
#: indistinguishable from a complete one.
#:
#: **The reachable item count is one page less than the budget times the page
#: size**, because a walk that does not end on a declared total spends its last
#: request on the page that ends it. The figures below are the real reachable
#: counts and not the product, which is what they said before and was wrong by a
#: page: a collection of exactly the product would have raised, blaming an offset
#: parameter that was working.
#:
#: Sized far above any real collection on purpose, since a budget that can fire
#: on real data turns a correctness fix into an outage. The largest reads this
#: project has actually measured, live on 2026-09-17, are written beside each one
#: so the margin is visible rather than asserted.
PAGE_CAPS: dict[str, int] = {
    "playlist_tracks": 200,  # reaches 19,900 tracks. Largest measured: 197.
    "account_playlists": 400,  # reaches 19,950 playlists. Largest measured: 599.
    "favorite_tracks": 200,  # reaches 19,900 tracks. Largest measured: 197.
    # Reaches 9,900 releases PER RELEASE METHOD. ``artist_releases`` walks each
    # method separately, so this is spent once per method, not once per artist.
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

    **:class:`ListingNotPaginated` is excluded from that breadth**, and this is
    not a narrowing of the retry policy but a correction to what the policy was
    ever about. That exception is raised by this module, from inspecting the
    client's own signature, and it says the method CANNOT page. Waiting cannot
    change a signature. Before U65 it went round the ladder five times and slept
    1, 2, 4, 8 and 16 seconds, 31 in all, before re-raising the answer it had at
    the first attempt. That cost is per listing, and ``artist_releases`` reads one
    per release method per artist, so a label crawl over 200 artists would have
    slept for over three hours before reporting a fault it knew about immediately.
    """
    attempt = 0
    while True:
        try:
            return fetch_page(limit, offset)
        except ListingNotPaginated:
            raise
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
    declared_total: Callable[[], int | None] | None = None,
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

    ``declared_total`` is how :attr:`StopRule.DECLARED_TOTAL` learns where the
    collection ends: a callable returning the provider's own count of the items
    it is serving, or ``None`` where it publishes none. It is called once, before
    the walk. A shape that declares that rule and then gets ``None`` degrades to
    stopping on an empty page rather than refusing, because a missing count is a
    weaker answer and not a broken one.

    ``shape`` names the listing in that exception and does nothing else. It is
    optional so this function stays a mechanism a test can drive directly, while
    :data:`STOP_RULES` and :data:`PAGE_CAPS` hold the policy.
    """
    items: list[Any] = []
    seen: set[Any] = set()
    offset = 0
    pages = 0

    total: int | None = None
    if stop is StopRule.DECLARED_TOTAL and declared_total is not None:
        total = declared_total()
        # A provider that has not parsed a count yet says so with a sentinel
        # rather than an absence. ``tidalapi``'s Playlist.num_tracks is -1 until
        # the object is parsed, and a zero total is indistinguishable from an
        # undeclared one, so neither is trusted as an end.
        if total is not None and total <= 0:
            total = None

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

        if total is not None:
            # An empty page means NOTHING here, which is the whole point of this
            # rule: a window whose every counted item is unservable comes back
            # empty in the middle of a collection. Only the offset says where the
            # end is. A last page that came back FULL still continues, because a
            # total that under reports is the one way this rule could truncate
            # and one more request settles it.
            if offset >= total and len(page) < page_size:
                break
        elif not page:
            break

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


def _declared_attribute(owner: Any, name: str) -> Callable[[], int | None]:
    """A count the provider has already parsed onto an object, read lazily.

    Free: no request. A client version that stopped parsing the attribute
    returns ``None`` here rather than raising, which degrades the walk to the
    empty page rule instead of failing a read that would otherwise succeed.
    """

    def total() -> int | None:
        value = getattr(owner, name, None)
        return value if isinstance(value, int) else None

    return total


def _declared_count(owner: Any, method: str) -> Callable[[], int | None]:
    """A count the provider serves from its own endpoint, read lazily.

    Costs one request, and saves the one the empty page rule would have spent
    ending the walk. A client that does not expose the method returns ``None``
    rather than raising, for the reason :func:`_declared_attribute` gives. A
    method that exists and FAILS is left to raise: it is the same API and the
    same session the listing itself is about to use, so a failure there is the
    caller's to see through its own provider boundary, not this module's to hide.
    """

    def total() -> int | None:
        fn = getattr(owner, method, None)
        if fn is None:
            return None
        value = fn()
        return value if isinstance(value, int) else None

    return total


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

    Stops on the **declared total**, and reads nothing from a page's shape. A
    playlist can hold a track the account cannot play, and the provider omits it
    from the window it serves while still counting it, so neither a short window
    nor an empty one says anything about where the playlist ends. The count comes
    from ``numberOfTracks``, which the client has already parsed onto the
    playlist object, so this shape pays no request at all for the rule.

    This is the read the quarterly placeholder acquire walks, so an early stop
    would silently drop the rest of a playlist of tracks Phillip does not own
    yet, which is the one listing whose omissions nothing downstream can notice.

    No deduplication: a playlist that lists a track twice means it twice.
    """
    kwargs.setdefault("declared_total", _declared_attribute(playlist, "num_tracks"))
    return paginate(_paged_caller(playlist, "tracks"), **_shape("playlist_tracks", **kwargs))


def favorite_tracks(session: Any, **kwargs: Any) -> list[Any]:
    """Every track the account has favourited, deduplicated by track identifier.

    Stops on the **declared total**, and reads nothing from a page's shape. This
    is the listing R-383 was measured on: 197 favourites read back as 93, because
    the provider omits the tracks it will not serve from each window while
    counting them in it. ``Favorites.get_tracks_count`` is both the count this
    walk ends on and the evidence for the defect, its own docstring saying the
    total "also includes track that may not be available for playback", so the
    number that ends the walk is by construction the number the windows are cut
    from. It costs one request and saves the one an empty page ending would cost.

    The ordering is newest first, which is what made the defect hard to see: the
    rows that did come back were the recent ones, so it bit only on questions
    about OLD state, and ``TidalAccount.has_heart`` asks exactly that.

    Deduplicated because this listing is ordered by when the favourite was
    created, and a favourite added while the read is in progress shifts every
    later item by one, which re-serves the item on the page boundary.
    """
    favorites = session.user.favorites
    kwargs.setdefault("key", lambda track: str(getattr(track, "id", "")))
    kwargs.setdefault("declared_total", _declared_count(favorites, "get_tracks_count"))
    return paginate(_paged_caller(favorites, "tracks"), **_shape("favorite_tracks", **kwargs))


def account_playlists(session: Any, **kwargs: Any) -> list[Any]:
    """Every playlist the listing exposes for this account, across pages.

    Stops on an **empty page**, which is the weaker rule, because this endpoint
    publishes no total for what it serves. ``Favorites.get_playlists_count`` is
    the near miss and must not be used: it counts the root collection folder
    through ``my-collection/playlists/folders``, while this listing serves
    ``playlistsAndFavoritePlaylists``, which also carries the playlists the
    account merely follows. A count of a different collection used as this one's
    end is a wrong answer arriving with a confident number.

    So this shape is narrowed rather than closed, and R-385 says so on the
    ledger. It would take 50 consecutive unopenable playlists, this shape's page
    size, to break it. It read 599 both ways when walked by hand on 2026-09-17.

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

    Stops on an **empty page**, which is the weaker rule, because the client
    exposes no count for either release listing. R-385 says so on the ledger.

    This is also the shape where the extra request costs most: the walk runs once
    per release method per artist, and almost every artist fits inside one page,
    so a label crawl over A artists pays 2A requests it did not pay before. It is
    still the right trade. A label catalogue that stops early is this product's
    core job done wrong, and a prolific artist crossing the page boundary is
    exactly where an omission would land. Extra requests make a sweep slower,
    which :func:`fetch_with_retry` already absorbs; an early stop makes it wrong,
    which nothing absorbs. Recorded with its arithmetic as R-384.

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
