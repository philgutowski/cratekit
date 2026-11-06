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
the whole module be proven against fakes with no account and no session. The
three folder shapes and the account playlists shape are the nearest thing to an
exception: they send their own request, but through the request object the
provider client hands them, so they reach the network by the same transport, and
the same pacing gate, as every client call.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Mapping, Sequence
from enum import Enum
from typing import Any

from cratekit.core.cause import CratekitError


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

    ``CURSOR`` is for an endpoint that ignores ``offset`` altogether and pages by
    a cursor it hands back with each response (R-878). The walk stops on the
    **exhausted cursor**, a response that carries no further cursor, or on an
    empty page, and then checks what it collected against the count the response
    declares, refusing when it falls short. It is walked by
    :func:`paginate_cursor` and never by :func:`paginate`, which refuses it,
    because an offset walk over such an endpoint reads its first page forever.
    """

    DECLARED_TOTAL = "declared total"
    EMPTY_PAGE = "empty page"
    SHORT_PAGE = "short page"
    CURSOR = "exhausted cursor"

#: Server page ceilings, per listing shape. These are the PROVIDER's numbers, not
#: preferences: asking for more returns the ceiling, and asking for fewer costs
#: extra round trips. Named per shape because they genuinely differ, and a single
#: shared constant would silently be wrong for one of them.
PAGE_SIZES: dict[str, int] = {
    "playlist_tracks": 100,
    "account_playlists": 50,
    "favorite_tracks": 100,
    "artist_releases": 100,
    # The provider's own ceiling for its collection folder endpoint, which both
    # folder shapes below read: the client documents it as "Cannot exceed 50".
    "account_folders": 50,
    "folder_playlists": 50,
    "folder_folders": 50,
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
    # R-878. The provider's folder endpoint ignores offset and returns its first
    # page at every one, so both folder listings walk its cursor instead.
    "account_folders": StopRule.CURSOR,
    "folder_playlists": StopRule.CURSOR,
    "folder_folders": StopRule.CURSOR,
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
    # A label roster held in memory spends none of it (R-888, ``HeldReleases``).
    "artist_releases": 100,
    # R-835. The figures are bounds rather than reads, and they assume the
    # provider fills the page it is asked for. The account holds one folder per
    # followed label, 47 when sitting 11 swept them and 55 declared at sitting
    # 30 (R-878), and a label folder holds one playlist per release year.
    "account_folders": 100,  # reaches 4,950 folders.
    "folder_playlists": 20,  # reaches 950 year playlists in one folder.
    "folder_folders": 20,  # reaches 950 nested folders in one folder.
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

    **A refusal that declares ``retryable=False`` is excluded on the same
    argument.** An adapter that finds the stored session expired mid page refuses
    ``credential-missing``, and the person has to log in before any attempt can
    differ from the first. The ladder slept the same 31 seconds on it until
    2026-09-18, when it surfaced as the slowest test in the suite. The exclusion
    reads the refusal's own flag rather than its type, so a rate limit an adapter
    spells as a retryable refusal still climbs the ladder.
    """
    attempt = 0
    while True:
        try:
            return fetch_page(limit, offset)
        except ListingNotPaginated:
            raise
        except Exception as exc:  # noqa: BLE001 - see docstring: bounded, then re-raised
            if isinstance(exc, CratekitError) and not exc.cause.retryable:
                raise
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

    **A shape that declares :attr:`StopRule.CURSOR` is refused here**, before any
    request. Its endpoint ignores ``offset``, so this walk would read the same
    first page until its budget ran out, which is R-878 exactly. That shape is
    walked by :func:`paginate_cursor`.
    """
    if stop is StopRule.CURSOR:
        raise ValueError(
            f"{shape or 'listing'} declares the {stop.value} rule, so its endpoint "
            f"ignores offset and must be walked by paginate_cursor, not paginate"
        )
    items: list[Any] = []
    seen: set[Any] = set()
    offset = 0
    pages = 0

    total: int | None = None
    if stop is StopRule.DECLARED_TOTAL and declared_total is not None:
        # THE SAME LADDER A PAGE GETS, and the asymmetry it would otherwise have
        # is the reason to say so. The count is a request this walk did not used
        # to make, against the same API and the same session, so the rate limit
        # that makes page one retry five times would make the count fail outright
        # and take the whole listing with it. A new failure path introduced BY a
        # correctness fix is a bad trade for a saved line. Retried here rather
        # than inside the callable because this is where the caller's retry
        # settings are, and a ladder that ignores them cannot be driven by a test
        # without sleeping for real.
        total = fetch_with_retry(
            lambda _limit, _offset: declared_total(), limit=0, offset=0, **retry
        )
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
            _take(items, seen, item, key)

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


def _take(items: list[Any], seen: set[Any], item: Any, key: Callable[[Any], Any] | None) -> None:
    """Append ``item`` unless ``key`` says it was already taken. Both walks."""
    if key is not None:
        identity = key(item)
        if identity in seen:
            return
        seen.add(identity)
    items.append(item)


def _declared(response: Any) -> int | None:
    """The ``totalNumberOfItems`` a raw response declares, or ``None``."""
    value = response.get("totalNumberOfItems") if isinstance(response, dict) else None
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def paginate_cursor(
    fetch_page: Callable[[int, str | None], Any],
    *,
    page_size: int,
    stop: StopRule,
    max_pages: int,
    parse: Callable[[Any], Any],
    shape: str | None = None,
    key: Callable[[Any], Any] | None = None,
    keep: Callable[[Any], bool] | None = None,
    **retry: Any,
) -> list[Any]:
    """Every item across every server page of an endpoint that pages by cursor.

    ``fetch_page(limit, cursor)`` returns the provider's RAW response, a mapping
    carrying ``items``, ``totalNumberOfItems`` and ``cursor``. The first request
    sends no cursor, and every later one sends the cursor the previous response
    carried. ``parse`` turns one raw item into the object the caller gets back.

    **``parse`` is retried on the same ladder, one item at a time**, because it
    can be a request of its own: the client's playlist parser fetches a playlist
    the account created to rebuild it as the account's own (R-878's review). It
    sat inside the page fetch before this walk existed, so a rate limit on it
    was retried, and a walk that stopped retrying it would turn one blip into a
    refused verb. Retried per item rather than with the page, so a blip on the
    thirtieth playlist does not fetch the other twenty nine again. The folder
    playlists walk has parsed without that fetch since R-1016, and the ladder
    stays, because a parser is the client's code and this walk cannot see
    whether a later version of it reaches the network.

    **A response that is not a page is refused, not read as the end.** One with
    neither an ``items`` list nor a declared count is retried on the ladder and
    then raised. Read as an empty last page it would have returned an empty
    listing, and an empty folder listing is what makes a caller create a folder
    the account already holds.

    **The walk stops on the exhausted cursor**, a response with no further
    cursor, or on a page with no items. Neither proves the listing is whole, so
    the count is checked after: when a response declared ``totalNumberOfItems``
    and the walk collected fewer, it raises :class:`ListingTruncated` rather than
    returning, on the argument that class makes. The latest count declared is
    the one checked, since the collection can change while it is read.

    **``keep`` filters raw items after they are counted, not before** (R-887).
    ``totalNumberOfItems`` counts every item the folder holds, folders and
    playlists alike, whatever the request's ``includeOnly`` asks for: the
    author's root read 26 folders and 29 playlists against a declared 55. So the
    walk asks for everything, counts every raw item it is served against the
    declared total, and parses only the ones ``keep`` passes. A filter applied
    by the provider would leave nothing to check the count against.

    ``stop``, ``max_pages``, ``key`` and ``shape`` mean what they mean to
    :func:`paginate`, and ``stop`` must be :attr:`StopRule.CURSOR`, so a shape
    cannot reach this walk while its table says it walks some other way. The
    budget is the same budget of requests and spending it raises the same way:
    a cursor the provider hands back unchanged is how this walk would otherwise
    loop for ever.
    """
    if stop is not StopRule.CURSOR:
        raise ValueError(
            f"{shape or 'listing'} declares the {stop.value} rule and is walked by "
            f"paginate; paginate_cursor walks only the {StopRule.CURSOR.value} rule"
        )
    items: list[Any] = []
    seen: set[Any] = set()
    cursor: str | None = None
    total: int | None = None
    pages = 0
    served: set[Any] = set()
    unkeyed = 0

    while True:
        if pages >= max_pages:
            raise ListingTruncated(
                f"{shape or 'listing'} spent its whole budget of {max_pages} requests "
                f"at {page_size} per page without reaching the end, having collected "
                f"{len(items)} item(s). The budget is sized far above any real "
                f"collection, so reaching it means the provider is not advancing its "
                f"cursor. Returning the {len(items)} would be a truncated listing "
                f"indistinguishable from a complete one, which is the thing this "
                f"module refuses to guess at"
            )

        def page_at(limit: int, _offset: int, cursor: str | None = cursor) -> dict:
            response = fetch_page(limit, cursor)
            if not isinstance(response, dict) or (
                not isinstance(response.get("items"), list) and _declared(response) is None
            ):
                raise ValueError(
                    f"{shape or 'listing'} was answered with neither a list of items "
                    f"nor a count, which is not a page of the listing; reading it as "
                    f"the end would return a listing that is not there"
                )
            return response

        response = fetch_with_retry(page_at, limit=page_size, offset=0, **retry)
        pages += 1
        page = list(response.get("items") or [])
        for raw in page:
            identity = _raw_identity(raw)
            if identity is None:
                unkeyed += 1
            else:
                served.add(identity)
            if keep is not None and not keep(raw):
                continue
            item = fetch_with_retry(lambda _l, _o, raw=raw: parse(raw), limit=0, offset=0, **retry)
            _take(items, seen, item, key)

        if _declared(response) is not None:
            total = _declared(response)
        following = response.get("cursor")
        if not page or not following:
            break
        cursor = str(following)

    counted = len(served) + unkeyed
    if total is not None and counted < total:
        raise ListingTruncated(
            f"{shape or 'listing'} reached the end of its cursor having collected "
            f"{counted} item(s) of every kind where the provider declared {total}. "
            f"Returning the {len(items)} kept would be a truncated listing "
            f"indistinguishable from a complete one, which is the thing this module "
            f"refuses to guess at"
        )
    return items


def _raw_identity(raw: Any) -> Any:
    """What one raw folder endpoint item is, for counting it against the total.

    The item's ``trn``, else its data's ``id`` or ``uuid``, else ``None``, which
    is counted once per appearance rather than deduplicated.
    """
    if not isinstance(raw, dict):
        return None
    if raw.get("trn"):
        return raw["trn"]
    data = raw.get("data")
    if isinstance(data, dict):
        return data.get("id") or data.get("uuid")
    return None


def _item_type(wanted: str) -> Callable[[Any], bool]:
    """Keep the raw folder endpoint items of one ``itemType``."""
    return lambda raw: isinstance(raw, dict) and raw.get("itemType") == wanted


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
    rather than raising, since a missing count is a weaker answer and not a
    broken one.

    It is a plain call and does no retrying of its own. :func:`paginate` puts it
    through the same ladder it puts a page through, which is the only place that
    knows the caller's retry settings, and the reason it must be retried at all is
    written there.
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


#: The provider's collection folder endpoint, the one both of the client's own
#: folder listings call, ``Favorites.playlist_folders`` and ``Folder.items``.
FOLDER_ENDPOINT = "my-collection/playlists/folders"

#: The ordering both of those listings send. The cursor is cut from an ordered
#: walk, so a walk that asked for another order than the client does would be
#: reading a listing nobody has measured.
FOLDER_ORDER = "NAME"

#: What a refusal from one of the three folder walks calls the walk.
FOLDER_WALK = "folder listing"


def _client_part(owner: Any, *path: str, walk: str) -> Any:
    """``owner.a.b``, or :class:`ListingNotPaginated` naming the missing part.

    The folder walks and the account playlists walk reach past the client's
    listing methods to its request object, its configuration and its parsers. A
    client version that moved one of those is an upgrade problem the user can
    act on, the same as a listing method that went away, and it is refused by
    name rather than retried. ``walk`` names the listing in that refusal.
    """
    value = owner
    for name in path:
        value = getattr(value, name, None)
        if value is None:
            raise ListingNotPaginated(
                f"{type(owner).__name__} has no {'.'.join(path)}; the provider client "
                f"changed shape and the {walk} needs updating with it"
            )
    return value


def _send(request: Any, walk: str, *args: Any, **kwargs: Any) -> Any:
    """``request.request(*args, **kwargs)``, a rejected signature refused by name.

    The walks that send the client's request themselves, the three folder walks
    and the account playlists walk, send it through here, so a client whose
    request object no longer takes the arguments is refused as
    :class:`ListingNotPaginated` in one wording, the walk named, rather than
    retried as though waiting could change a signature.
    """
    try:
        return request.request(*args, **kwargs)
    except TypeError as exc:
        raise ListingNotPaginated(
            f"{type(request).__name__}.request does not accept the arguments the "
            f"{walk} sends; the provider client changed shape and the {walk} "
            f"needs updating with it"
        ) from exc


def _folder_endpoint(
    request: Any, base_url: str, folder_id: str
) -> Callable[[int, str | None], Any]:
    """Bind the folder endpoint into the ``(limit, cursor)`` shape, raw.

    Sends what the client's own listing sends, the folder, the limit and the
    order, through the client's own request object, and adds the cursor the last
    response carried. It sends no ``offset``, which the endpoint ignores (R-878),
    and no ``includeOnly``, since the count the walk checks covers every kind of
    item and the walk filters after counting (R-887). The answer is the raw response, since the client's listing
    methods throw away the cursor this walk needs.
    """

    def call(limit: int, cursor: str | None) -> Any:
        params: dict[str, Any] = {
            "folderId": folder_id,
            "limit": limit,
            "order": FOLDER_ORDER,
        }
        if cursor is not None:
            params["cursor"] = cursor
        answer = _send(
            request, FOLDER_WALK, "GET", FOLDER_ENDPOINT, base_url=base_url, params=params
        )
        return answer.json()

    return call


#: The account listing's endpoint, the one ``User.playlist_and_favorite_playlists``
#: calls, the account's identifier in place of ``%s``.
ACCOUNT_PLAYLISTS_ENDPOINT = "users/%s/playlistsAndFavoritePlaylists"


def _account_playlists_endpoint(user: Any) -> Callable[[int, int], list[Any]]:
    """Bind the account listing into the ``(limit, offset)`` shape, parsed WITHOUT a fetch.

    Sends what ``User.playlist_and_favorite_playlists`` sends, through the user's
    own request object, and does its one reshaping, the listing's ``created``
    moved onto the playlist as ``dateAdded``. What it does not do is hand each
    item to ``Playlist.parse_factory``, the parser that method is wired to: that
    parser ends in ``Playlist.factory``, which builds a ``UserPlaylist`` for
    every playlist the account created, and that constructor fetches the
    playlist again, ``GET playlists/<id>``, to read its etag. Measured on the
    author's account on 2026-10-14, 624 playlists cost 637 requests, 13 pages and
    624 fetches (R-1016). ``Playlist.parse`` reads the same item data and makes
    no request, so a page costs one request.

    The objects come back as ``Playlist`` rather than ``UserPlaylist``. They
    read their tracks as before; what they lack is an etag, which only the
    client's own edit methods send, and no caller of this listing edits through
    the object it lists.
    """
    walk = "account playlist listing"
    request = _client_part(user, "request", walk=walk)
    parse = _client_part(user, "playlist", "parse", walk=walk)
    path = ACCOUNT_PLAYLISTS_ENDPOINT % _client_part(user, "id", walk=walk)

    def call(limit: int, offset: int) -> list[Any]:
        answer = _send(request, walk, "GET", path, params={"limit": limit, "offset": offset})
        page = answer.json()
        if not isinstance(page, dict) or not isinstance(page.get("items"), list):
            # Refused rather than read as the empty page that ends this walk:
            # an error body read as the end would return the account short.
            raise ValueError(
                f"the {walk} was answered with something that is neither a page "
                f"nor a list of items: {str(page)[:200]!r}"
            )
        found = []
        for item in page["items"]:
            playlist = item["playlist"]
            playlist["dateAdded"] = item["created"]
            found.append(parse(playlist))
        return found

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


def favorite_tracks_declared(session: Any, **kwargs: Any) -> tuple[list[Any], int | None]:
    """:func:`favorite_tracks`, and the count the provider declared for them (R-504).

    ENDING ON THE COUNT IS NOT THE SAME AS REACHING IT. The walk stops once the
    offset passes the declared total, and every window it read left out the
    hearts the provider will not serve, so the rows can come back short of the
    count with nothing wrong in the walk at all. Measured shape: 197 declared,
    12 unservable, 185 rows. This returns the count beside the rows so the
    caller can compare them, which :func:`favorite_tracks` alone gives nobody
    the means to do.

    THE COUNT IS THE ONE THE WALK ENDED ON, recorded as the walk asked for it,
    not a second request made afterwards, which could answer differently if a
    heart landed in between. ``None`` where the provider published no usable
    count, on the rule :func:`paginate` applies: a zero or negative total is
    not trusted as a count.
    """
    favorites = session.user.favorites
    count = kwargs.pop("declared_total", None) or _declared_count(favorites, "get_tracks_count")
    answered: list[int | None] = []

    def declared() -> int | None:
        value = count()
        answered.append(value)
        return value

    rows = favorite_tracks(session, declared_total=declared, **kwargs)
    total = answered[-1] if answered else None
    return rows, total if isinstance(total, int) and total > 0 else None


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

    ONE REQUEST PER PAGE AND NONE PER PLAYLIST (R-1016). The walk sends the
    client's listing request itself rather than calling the client's listing
    method, because that method parses each playlist the account created by
    fetching it again. :func:`_account_playlists_endpoint` says why.
    """
    kwargs.setdefault("key", lambda playlist: str(getattr(playlist, "id", "")))
    return paginate(
        _account_playlists_endpoint(session.user),
        **_shape("account_playlists", **kwargs),
    )


def account_folders(session: Any, **kwargs: Any) -> list[Any]:
    """Every folder at the root of the account's playlist collection, across pages.

    Stops on the **exhausted cursor**, and checks the count the response
    declares. The endpoint ignores ``offset``: on the author's account
    ``playlist_folders`` returned the same first folders at every offset from 0
    to 1,000, while the raw response carried ``totalNumberOfItems`` of 55 and a
    ``cursor`` that, sent back, returned the next page (R-878). The client
    exposes no cursor, so this walk sends the client's own request, root folder,
    ordered by name, and parses each folder with the client's own
    ``parse_folder``. The 55 were 26 folders and 29 playlists, so the walk reads
    both and keeps the folders (R-887).

    The client's own folder lookup reads ONE page of fifty and gives up, so an
    account with a fifty first folder would have it reported absent; this walk
    is why the outbound adapter never asks that lookup anything (R-835).

    Deduplicated by identifier, since a folder created while the listing is read
    can shift the window it falls in.
    """
    kwargs.setdefault("key", lambda folder: str(getattr(folder, "id", "")))
    fetch = _folder_endpoint(
        _client_part(session, "request", walk=FOLDER_WALK),
        _client_part(session, "config", "api_v2_location", walk=FOLDER_WALK),
        "root",
    )
    return paginate_cursor(
        fetch,
        keep=_item_type("FOLDER"),
        parse=_client_part(session, "parse_folder", walk=FOLDER_WALK),
        **_shape("account_folders", **kwargs),
    )


def folder_playlists(folder: Any, **kwargs: Any) -> list[Any]:
    """Every playlist one account folder holds, across pages.

    Stops on the **exhausted cursor**, for the reason :func:`account_folders`
    gives: the folder's ``items`` reads the same endpoint, and on the author's
    account a folder's second page of five was its first (R-878). ``folder`` is
    the client's folder object, and the walk sends what its ``items`` sends, the
    folder's identifier, through its own request object, keeps the playlists, and
    parses each one's ``data`` with the playlist parser ``items`` uses, less its
    factory step. ``items`` parses with ``Playlist.parse_factory``, which fetches
    every playlist the account created again, one request each (R-1016), so the
    walk parses with ``Playlist.parse``, which reads the same data and fetches
    nothing. Deduplicated by identifier on the same argument.
    """
    kwargs.setdefault("key", lambda playlist: str(getattr(playlist, "id", "")))
    fetch = _folder_endpoint(
        _client_part(folder, "request", walk=FOLDER_WALK),
        _client_part(folder, "session", "config", "api_v2_location", walk=FOLDER_WALK),
        str(_client_part(folder, "id", walk=FOLDER_WALK)),
    )
    parse_playlist = _client_part(folder, "playlist", "parse", walk=FOLDER_WALK)
    return paginate_cursor(
        fetch,
        keep=_item_type("PLAYLIST"),
        parse=lambda item: parse_playlist(item["data"]),
        **_shape("folder_playlists", **kwargs),
    )


def folder_folders(folder: Any, **kwargs: Any) -> list[Any]:
    """Every folder one account folder holds, across pages.

    Stops on the **exhausted cursor**, for the reason :func:`account_folders`
    gives: the same endpoint that lists a folder's playlists also lists the
    folders it holds, and the walk that ignores offset must walk the cursor
    (R-878). ``folder`` is the client's folder object; the walk keeps folders
    and parses each with the client's ``parse_folder``. Deduplicated by
    identifier on the same argument.
    """
    kwargs.setdefault("key", lambda nested: str(getattr(nested, "id", "")))
    fetch = _folder_endpoint(
        _client_part(folder, "request", walk=FOLDER_WALK),
        _client_part(folder, "session", "config", "api_v2_location", walk=FOLDER_WALK),
        str(_client_part(folder, "id", walk=FOLDER_WALK)),
    )
    return paginate_cursor(
        fetch,
        keep=_item_type("FOLDER"),
        parse=_client_part(folder, "session", "parse_folder", walk=FOLDER_WALK),
        **_shape("folder_folders", **kwargs),
    )


#: The two release listings a provider artist exposes, and the ones
#: :func:`artist_releases` reads by default. Owned here so a caller that has to
#: ask "can this object be listed at all" (``label.crawl.can_list``) checks the
#: same names the crawl will try, without a second written copy of them.
RELEASE_METHODS: tuple[str, ...] = ("get_albums", "get_ep_singles")


class HeldReleases(ABC):
    """An artist shaped object whose release listings are already in memory.

    :func:`artist_releases` reads such an object's lists WHOLE and never pages
    it, because a request budget guards against a provider that is not
    advancing its window and memory cannot fail to advance. R-888 is what paging
    one cost: a label roster of 756 artists held 27,002 releases, the walk spent
    the ``artist_releases`` budget at 10,000 on one listing, and the refusal
    blamed the provider's offset for a list that never left the process. A budget
    drawn from the list's own length was the other way to close it and was not
    taken, since a guard sized to what it guards can never fire.

    A subclass answers :meth:`held` for each release method and needs no paging
    method at all: ``label.crawl.can_list`` asks :meth:`held` too, so the probe
    and the read cannot disagree about what the object can list. Abstract, so a
    subclass that forgets :meth:`held` fails when it is built rather than mid
    crawl, where a sweep would report it as a provider that could not be read.
    """

    @abstractmethod
    def held(self, method: str) -> list[Any] | None:
        """Every release this object holds for ``method``, or ``None`` when it holds no such listing."""


def artist_releases(artist: Any, methods: Iterable[str] = RELEASE_METHODS, *,
                    skipped: list[str] | None = None, **kwargs: Any) -> list[Any]:
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

    **THE SKIP LEAVES A RECORD WHEN A CALLER ASKS FOR ONE.** Each skipped method
    name is appended to ``skipped``. Without it a half read catalogue returned
    here in the same shape as a whole one, and a sweep reported the albums of a
    label whose singles were never listed as a complete crawl (R-261). Deciding
    what the skip means stays with the caller about to report it.

    **A :class:`HeldReleases` object is read whole, not paged**, through the same
    deduplication, and spends none of this shape's budget (R-888). A listing it
    does not hold is skipped and recorded the same way. The remaining keywords
    configure the paged walk, so the held read has no use for them.
    """
    releases: list[Any] = []
    seen: set[str] = set()
    held = isinstance(artist, HeldReleases)
    for method in methods:
        listed = artist.held(method) if held else getattr(artist, method, None)
        if listed is None:
            if skipped is not None:
                skipped.append(method)
            continue
        if not held:
            listed = paginate(_paged_caller(artist, method), **_shape("artist_releases", **kwargs))
        for release in listed:
            identity = str(getattr(release, "id", "")) or f"{method}:{len(releases)}"
            if identity in seen:
                continue
            seen.add(identity)
            releases.append(release)
    return releases


# ── U226: the window read beside the client's unpaged read ──────────────────

#: U226. The two reads agree, or the unpaged one is a first page the window
#: read begins with: the window read is the reading.
WINDOW_AGREES = "agrees"
#: U226. The two differ and the unpaged read holds every track the playlist
#: declares: the window lags a change the provider already serves unpaged, and
#: the unpaged read is the reading.
WINDOW_UNPAGED = "unpaged"
#: U226. The two differ and the unpaged read is not whole, so neither can be
#: taken as the playlist as it stands: a lag, read again or held.
WINDOW_LAGS = "lags"


def row_id(row: Any) -> str:
    """One listed row's provider identifier as text, a track object's or a mapping's."""
    if isinstance(row, Mapping):
        return str(row.get("id", "") or "")
    return str(getattr(row, "id", "") or "")


def _is_count(declared: Any) -> bool:
    """Whether a playlist's declared track total is a count a read can be held to."""
    return isinstance(declared, int) and not isinstance(declared, bool) and declared >= 0


def playlist_tracks_unpaged(playlist: Any, **retry: Any) -> list[Any]:
    """The client's own read of a playlist with no window, as it is served now (U226), walked past a capped first page (R-1360).

    MEASURED ON THE LIVE ACCOUNT on 2026-11-06 (Sitting 84): after a move,
    this read returned the new order at once while the window read
    :func:`playlist_tracks` walks returned the old one, and sometimes the
    new, for at least thirteen minutes.

    ONE REQUEST, AND MORE ONLY PAST A FIRST PAGE. The client fills a missing
    limit with its session's own ``item_limit``, 1000 by default, and
    :data:`PAGE_SIZES` records the provider's ceiling for this shape as 100,
    so a playlist of more than 100 tracks is most likely served its first
    hundred alone (the cap was not measured live). When the first request
    holds fewer tracks than the playlist declares, the read walks on with an
    offset and still no limit, each request starting ONE TRACK BACK, so its
    first track must be the last one already read. A page is taken only
    while it holds together with what came before: it starts on that track,
    it is no longer than the first page, and it carries the version tag the
    first page carried, when the client keeps one (``_etag``, which a page
    served from before a write carries as it was then). The walk stops at
    the declared count, at a page shorter than the first, or at the first
    page that does not hold together, and returns only the pages that did,
    so a walk that broke reads as a first part, which :func:`judge_window`
    does not take as the playlist when the window is whole. Not measured
    live: whether a later page is current after a move as the first is
    (owed at an attended sitting). The cap is not assumed, so a provider
    that serves the read whole is read with one request, as before.

    NEVER WHOLE ON ITS OWN WORD. :func:`judge_window` holds the result to the
    declared count. A track the account cannot play is left out of a page
    and still counted (R-1362), so a page after it starts one track late,
    and the walk stops there; one left out of the last stretch only leaves
    the read short of the count. Each request goes through
    the retry ladder a page gets; a client that cannot be called with no
    window raises :class:`ListingNotPaginated` at once.
    """
    def call(offset: int) -> Callable[[int, int], Any]:
        def ask(_limit: int, _offset: int) -> Any:
            try:
                return playlist.tracks(offset=offset) if offset else playlist.tracks()
            except TypeError as exc:
                # A signature fault, not a wait (round one's review): the ladder
                # would sleep 31 seconds on an answer it has at the first attempt.
                raise ListingNotPaginated(
                    f"{type(playlist).__name__}.tracks cannot be called with no "
                    f"window, so the playlist cannot be read as the provider serves "
                    f"it unpaged; the provider client changed shape"
                ) from exc

        return ask

    rows = list(fetch_with_retry(call(0), limit=0, offset=0, **retry) or [])
    declared = getattr(playlist, "num_tracks", None)
    if not _is_count(declared) or len(rows) >= declared or len(rows) < 2:
        return rows
    step = len(rows)
    tag = getattr(playlist, "_etag", None)
    while len(rows) < declared:
        offset = len(rows) - 1
        page = list(fetch_with_retry(call(offset), limit=0, offset=offset, **retry) or [])
        if (
            not page
            or len(page) > step
            or row_id(page[0]) != row_id(rows[-1])
            or getattr(playlist, "_etag", None) != tag
        ):
            break
        rows.extend(page[1:])
        if len(page) < step:
            break
    return rows


def judge_window(paged: Sequence[str], unpaged: Sequence[str], declared: Any) -> str:
    """How the window read of a playlist stands beside its unpaged read (U226).

    :data:`WINDOW_AGREES` when the two are the same. :data:`WINDOW_UNPAGED`
    when they differ and the unpaged read holds exactly the declared count,
    so it is the playlist as it stands. :data:`WINDOW_LAGS` otherwise, with
    one exception kept from U226.

    A FIRST PART AGREES ONLY BESIDE A WINDOW SHORT OF THE COUNT (R-1360). An
    unpaged read shorter than the window and its first part is agreement
    when the window holds fewer tracks than the playlist declares, a track
    the account cannot play left out of both (R-1362), or when nothing is
    declared. Beside a window holding every declared track, or more, it is
    :data:`WINDOW_LAGS`: :func:`playlist_tracks_unpaged` walks past a capped
    first page, so a read that still stops short of a whole window is one
    whose walk broke, and the window may lag a change past where it reached.
    Before R-1360 that agreement took a window lagging a change past the
    first hundred tracks as the playlist.

    THE DECLARED TOTAL RULE STANDS. A track the account cannot play is left
    out of both reads and still counted, so two reads short of the declared
    count that agree are :data:`WINDOW_AGREES`, and the caller refuses them
    as it always has.
    """
    paged, unpaged = list(paged), list(unpaged)
    if unpaged == paged:
        return WINDOW_AGREES
    counted = _is_count(declared)
    if counted and len(unpaged) == declared:
        return WINDOW_UNPAGED
    if len(unpaged) < len(paged) and paged[: len(unpaged)] == unpaged:
        return WINDOW_LAGS if counted and len(paged) >= declared else WINDOW_AGREES
    return WINDOW_LAGS


#: Every listing shape this module covers, as name to wrapper. The guard in the
#: test suite reads this to decide which provider method names may only be called
#: from here, so adding a wrapper arms the guard for it automatically (P3).
WRAPPERS: dict[str, Callable[..., list[Any]]] = {
    "playlist_tracks": playlist_tracks,
    "favorite_tracks": favorite_tracks,
    "account_playlists": account_playlists,
    "artist_releases": artist_releases,
    "account_folders": account_folders,
    "folder_playlists": folder_playlists,
    "folder_folders": folder_folders,
}

#: The provider listing methods that must not be called outside this module.
#: ``tracks`` is on the list but is only a violation when called WITH pagination
#: arguments, because "tracks" is an ordinary accessor name that this codebase
#: also uses for its own collections, and a guard that fires on correct code gets
#: routed around rather than obeyed (P7).
GUARDED_METHODS = frozenset(
    {
        "tracks",
        "playlist_and_favorite_playlists",
        "get_albums",
        "get_ep_singles",
        "playlist_folders",
    }
)
PAGINATION_KEYWORDS = frozenset({"limit", "offset"})


__all__ = [
    "ACCOUNT_PLAYLISTS_ENDPOINT",
    "DEFAULT_BASE_DELAY_S",
    "DEFAULT_MAX_DELAY_S",
    "DEFAULT_MAX_RETRIES",
    "FOLDER_ENDPOINT",
    "FOLDER_ORDER",
    "FOLDER_WALK",
    "GUARDED_METHODS",
    "PAGE_CAPS",
    "PAGE_SIZES",
    "PAGINATION_KEYWORDS",
    "RELEASE_METHODS",
    "STOP_RULES",
    "WINDOW_AGREES",
    "WINDOW_LAGS",
    "WINDOW_UNPAGED",
    "WRAPPERS",
    "HeldReleases",
    "ListingNotPaginated",
    "ListingTruncated",
    "StopRule",
    "account_folders",
    "account_playlists",
    "artist_releases",
    "favorite_tracks",
    "favorite_tracks_declared",
    "fetch_with_retry",
    "folder_folders",
    "folder_playlists",
    "paginate",
    "paginate_cursor",
    "judge_window",
    "playlist_tracks",
    "playlist_tracks_unpaged",
    "row_id",
]
