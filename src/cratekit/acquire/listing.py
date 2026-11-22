"""One pagination wrapper per listing shape. No call site pages by hand.

The provider's client returns one server page, without complaint, for a listing
asked without pagination arguments, so a short list and a complete one look the
same. The page size is a property of the provider, so the wrappers live in the
adapter, the one place allowed to know it. Each wrapper:

1. pages to the end under a declared stop rule and a declared request budget,
   because no page shape says where a filtered collection ends (R-383, U65);
2. retries a transient failure with capped exponential backoff, since a dropped
   page is a silent gap in the answer;
3. deduplicates by identifier where the provider can repeat an item.

Nothing here reaches the network by itself; the folder and account playlist walks
send their own request through the client's request object, so the same transport
and pacing gate apply.
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

    Each value is the phrase a wrapper's docstring must use for it. The provider
    omits unservable items from a window while still counting them, so no page
    shape marks the end of a collection.

    ``DECLARED_TOTAL`` stops once the offset passes the provider's own count, the
    one rule that closes the class. ``EMPTY_PAGE`` walks to an empty page, broken by
    ``page_size`` consecutive unservable items, so it is declared only where no
    total is published, with a residual. ``SHORT_PAGE`` is correct only where every
    window is served full, and no shape declares it. ``CURSOR`` is for an endpoint
    that ignores ``offset``, walked only by :func:`paginate_cursor` (R-878).
    """

    DECLARED_TOTAL = "declared total"
    EMPTY_PAGE = "empty page"
    SHORT_PAGE = "short page"
    CURSOR = "exhausted cursor"

#: Server page ceilings per listing shape, the provider's numbers: asking for more
#: returns the ceiling, and asking for fewer costs round trips.
PAGE_SIZES: dict[str, int] = {
    "playlist_tracks": 100,
    "account_playlists": 50,
    "favorite_tracks": 100,
    "artist_releases": 100,
    # The client documents the folder endpoint as "Cannot exceed 50".
    "account_folders": 50,
    "folder_playlists": 50,
    "folder_folders": 50,
}

#: The stop rule each shape declares; each wrapper's docstring argues its own (R-385).
STOP_RULES: dict[str, StopRule] = {
    "playlist_tracks": StopRule.DECLARED_TOTAL,
    "account_playlists": StopRule.EMPTY_PAGE,
    "favorite_tracks": StopRule.DECLARED_TOTAL,
    "artist_releases": StopRule.EMPTY_PAGE,
    # The folder endpoint ignores offset, so these walk its cursor (R-878).
    "account_folders": StopRule.CURSOR,
    "folder_playlists": StopRule.CURSOR,
    "folder_folders": StopRule.CURSOR,
}

#: Request budgets per shape, sized far above any real collection. Spending one
#: raises :class:`ListingTruncated`, since a capped answer looks complete. A walk
#: not ending on a declared total spends its last request on the ending page, so the
#: reachable count, noted beside each, is one page less than budget times page size.
PAGE_CAPS: dict[str, int] = {
    "playlist_tracks": 200,  # reaches 19,900 tracks. Largest measured: 197.
    "account_playlists": 400,  # reaches 19,950 playlists. Largest measured: 599.
    "favorite_tracks": 200,  # reaches 19,900 tracks. Largest measured: 197.
    # Reaches 9,900 releases, spent once per release method.
    # A label roster held in memory spends none of it (R-888, ``HeldReleases``).
    "artist_releases": 100,
    # R-835. Bounds rather than reads: a folder per followed label, a playlist per year.
    "account_folders": 100,  # reaches 4,950 folders.
    "folder_playlists": 20,  # reaches 950 year playlists in one folder.
    "folder_folders": 20,  # reaches 950 nested folders in one folder.
}

DEFAULT_MAX_RETRIES = 5
DEFAULT_BASE_DELAY_S = 1.0
DEFAULT_MAX_DELAY_S = 30.0


class ListingNotPaginated(RuntimeError):
    """A provider listing method accepted no pagination arguments. Raised rather than
    taking its one page, since a truncated listing is indistinguishable from a short one."""


class ListingTruncated(RuntimeError):
    """A walk spent its whole request budget without reaching the end. Raised rather
    than returning what was collected, on the same argument (U65)."""


def fetch_with_retry(
    fetch_page: Callable[[int, int], Any], *, limit: int, offset: int,
    max_retries: int = DEFAULT_MAX_RETRIES, base_delay: float = DEFAULT_BASE_DELAY_S,
    max_delay: float = DEFAULT_MAX_DELAY_S, sleep: Callable[[float], None] = time.sleep,
) -> Any:
    """One page, retried on any transient failure with capped backoff, then re-raised.

    Any exception is retried because the client raises rate limits, timeouts and
    server errors as unrelated types; the bound keeps a permanent failure surfacing.
    :class:`ListingNotPaginated` and a refusal declaring ``retryable=False`` are
    raised at once, since waiting cannot change a signature or a lapsed login (U65).
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

    ``stop`` and ``max_pages`` have no defaults, so a wrapper must choose (R-383).
    ``max_pages`` is a request budget, and spending it raises rather than hiding a
    truncation. ``key`` turns on deduplication, off by default because a playlist
    may hold a track twice on purpose. ``declared_total`` returns the provider's
    count for :attr:`StopRule.DECLARED_TOTAL`, called once before the walk, and
    ``None`` degrades to the empty page rule. ``shape`` names the listing in
    refusals. A :attr:`StopRule.CURSOR` shape is refused, its endpoint ignoring
    ``offset``.
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
        # The count is retried on the page's ladder, so a rate limit cannot fail the listing.
        total = fetch_with_retry(
            lambda _limit, _offset: declared_total(), limit=0, offset=0, **retry
        )
        # A zero or negative total (``num_tracks`` is -1 until parsed) is not an end.
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
            # An empty page means nothing here; a full last page still continues,
            # since an under reported total is the one way this rule could truncate.
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
    fetch_page: Callable[[int, str | None], Any], *, page_size: int, stop: StopRule, max_pages: int,
    parse: Callable[[Any], Any], shape: str | None = None, key: Callable[[Any], Any] | None = None,
    keep: Callable[[Any], bool] | None = None, **retry: Any,
) -> list[Any]:
    """Every item across every server page of an endpoint that pages by cursor.

    ``fetch_page(limit, cursor)`` returns the raw response (``items``,
    ``totalNumberOfItems``, ``cursor``), and the first request sends no cursor.
    ``parse`` turns one raw item into the returned object and is retried per item,
    since a client parser may make a request of its own. A response that is not a
    page is refused rather than read as the end, since an empty folder listing makes
    a caller create a folder the account holds. The walk stops on the exhausted
    cursor or an empty page, then raises :class:`ListingTruncated` when it counted
    fewer items than the latest declared total. ``keep`` filters after counting,
    because the total counts every kind of item (R-887). The rest mean what they mean
    to :func:`paginate`, and ``stop`` must be :attr:`StopRule.CURSOR`.
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
    """What one raw folder item is, for counting: its ``trn``, else its data's ``id``
    or ``uuid``, else ``None``, counted once per appearance."""
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
    """The declared policy for one shape as call arguments, read from the tables."""
    return {
        "shape": name,
        "page_size": PAGE_SIZES[name],
        "stop": STOP_RULES[name],
        "max_pages": PAGE_CAPS[name],
        **overrides,
    }


def _declared_attribute(owner: Any, name: str) -> Callable[[], int | None]:
    """A count already parsed onto an object, read lazily, or ``None``."""

    def total() -> int | None:
        value = getattr(owner, name, None)
        return value if isinstance(value, int) else None

    return total


def _declared_count(owner: Any, method: str) -> Callable[[], int | None]:
    """A count the provider serves from its own endpoint, read lazily, or ``None``.
    Not retried here: :func:`paginate` puts it through the ladder."""

    def total() -> int | None:
        fn = getattr(owner, method, None)
        if fn is None:
            return None
        value = fn()
        return value if isinstance(value, int) else None

    return total


def _paged_caller(owner: Any, method: str) -> Callable[[int, int], Any]:
    """Bind a provider listing method into the ``(limit, offset)`` shape. A method
    rejecting those arguments raises ``ListingNotPaginated`` rather than serving a page."""
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


#: The collection folder endpoint both of the client's folder listings call.
FOLDER_ENDPOINT = "my-collection/playlists/folders"

#: The order the client sends, since the cursor is cut from an ordered walk.
FOLDER_ORDER = "NAME"

#: What a refusal from one of the three folder walks calls the walk.
FOLDER_WALK = "folder listing"


def _client_part(owner: Any, *path: str, walk: str) -> Any:
    """``owner.a.b``, or :class:`ListingNotPaginated` naming the missing part and
    ``walk``, since a client that moved a part is an upgrade problem, not a retry."""
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
    """``request.request(*args, **kwargs)``, a rejected signature refused as
    :class:`ListingNotPaginated` naming ``walk`` rather than retried."""
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
    """Bind the folder endpoint into the ``(limit, cursor)`` shape, answering raw.
    Sends no ``offset`` (R-878) and no ``includeOnly`` (R-887)."""

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


#: The endpoint ``User.playlist_and_favorite_playlists`` calls, the account id for ``%s``.
ACCOUNT_PLAYLISTS_ENDPOINT = "users/%s/playlistsAndFavoritePlaylists"


def _account_playlists_endpoint(user: Any) -> Callable[[int, int], list[Any]]:
    """Bind the account listing into the ``(limit, offset)`` shape, parsed without a fetch.

    Sends what ``User.playlist_and_favorite_playlists`` sends and moves ``created``
    onto each playlist as ``dateAdded``, but parses with ``Playlist.parse`` rather
    than ``parse_factory``, which fetches every playlist the account created again
    (R-1016). The objects are ``Playlist``, lacking only the etag an edit sends.
    """
    walk = "account playlist listing"
    request = _client_part(user, "request", walk=walk)
    parse = _client_part(user, "playlist", "parse", walk=walk)
    path = ACCOUNT_PLAYLISTS_ENDPOINT % _client_part(user, "id", walk=walk)

    def call(limit: int, offset: int) -> list[Any]:
        answer = _send(request, walk, "GET", path, params={"limit": limit, "offset": offset})
        page = answer.json()
        if not isinstance(page, dict) or not isinstance(page.get("items"), list):
            # Refused, since an error body read as the end returns the account short.
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


# The listing shapes. One wrapper each, and no call site may re-implement one.


def playlist_tracks(playlist: Any, **kwargs: Any) -> list[Any]:
    """Every track in a playlist, in playlist order, across pages.

    Stops on the **declared total**, ``numberOfTracks`` already parsed onto the
    playlist, because an unplayable track is omitted from a window yet counted.
    No deduplication: a playlist that lists a track twice means it twice.
    """
    kwargs.setdefault("declared_total", _declared_attribute(playlist, "num_tracks"))
    return paginate(_paged_caller(playlist, "tracks"), **_shape("playlist_tracks", **kwargs))


def favorite_tracks(session: Any, **kwargs: Any) -> list[Any]:
    """Every track the account has favourited, deduplicated by track identifier.

    Stops on the **declared total** from ``Favorites.get_tracks_count``, which counts
    the unservable tracks the windows omit (R-383). Deduplicated because a favourite
    added mid read shifts the newest first order and re-serves a boundary item.
    """
    favorites = session.user.favorites
    kwargs.setdefault("key", lambda track: str(getattr(track, "id", "")))
    kwargs.setdefault("declared_total", _declared_count(favorites, "get_tracks_count"))
    return paginate(_paged_caller(favorites, "tracks"), **_shape("favorite_tracks", **kwargs))


def favorite_tracks_declared(session: Any, **kwargs: Any) -> tuple[list[Any], int | None]:
    """:func:`favorite_tracks`, and the count the provider declared for them (R-504).

    Rows can fall short of the count with nothing wrong, unservable hearts being
    counted, so the caller compares them. The count is the one the walk ended on,
    ``None`` where no usable (positive) count was published.
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

    Stops on an **empty page**, the weaker rule, because this endpoint publishes no
    total; ``Favorites.get_playlists_count`` counts a different collection (R-385).
    Returns the provider's objects unfiltered, and sends the listing request itself
    so a page costs one request and no playlist a fetch (R-1016).
    """
    kwargs.setdefault("key", lambda playlist: str(getattr(playlist, "id", "")))
    return paginate(
        _account_playlists_endpoint(session.user),
        **_shape("account_playlists", **kwargs),
    )


def account_folders(session: Any, **kwargs: Any) -> list[Any]:
    """Every folder at the root of the account's playlist collection, across pages.

    Stops on the **exhausted cursor** and checks the declared count, because the
    endpoint ignores ``offset`` (R-878). It reads every item and keeps the folders
    (R-887); the client's own lookup reads one page only (R-835). Deduplicated by
    identifier, since a folder created mid read can shift its window.
    """
    kwargs.setdefault("key", lambda folder: str(getattr(folder, "id", "")))
    fetch = _folder_endpoint(
        _client_part(session, "request", walk=FOLDER_WALK),
        _client_part(session, "config", "api_v2_location", walk=FOLDER_WALK), "root",
    )
    return paginate_cursor(
        fetch, keep=_item_type("FOLDER"),
        parse=_client_part(session, "parse_folder", walk=FOLDER_WALK),
        **_shape("account_folders", **kwargs),
    )


def folder_playlists(folder: Any, **kwargs: Any) -> list[Any]:
    """Every playlist one account folder holds, across pages.

    Stops on the **exhausted cursor**, as :func:`account_folders` does, and parses
    each with ``Playlist.parse``, which fetches nothing (R-1016). Deduplicated by
    identifier.
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

    Stops on the **exhausted cursor**, as :func:`account_folders` does, parsing each
    with the client's ``parse_folder``. Deduplicated by identifier.
    """
    kwargs.setdefault("key", lambda nested: str(getattr(nested, "id", "")))
    fetch = _folder_endpoint(
        _client_part(folder, "request", walk=FOLDER_WALK),
        _client_part(folder, "session", "config", "api_v2_location", walk=FOLDER_WALK),
        str(_client_part(folder, "id", walk=FOLDER_WALK)),
    )
    return paginate_cursor(
        fetch, keep=_item_type("FOLDER"),
        parse=_client_part(folder, "session", "parse_folder", walk=FOLDER_WALK),
        **_shape("folder_folders", **kwargs),
    )


#: The two release listings a provider artist exposes, read by default; owned here
#: so ``label.crawl.can_list`` checks the same names.
RELEASE_METHODS: tuple[str, ...] = ("get_albums", "get_ep_singles")


class HeldReleases(ABC):
    """An artist shaped object whose release listings are already in memory.

    :func:`artist_releases` reads its lists whole and never pages them, since memory
    cannot fail to advance and a request budget would refuse a large roster (R-888).
    Abstract, so a subclass missing :meth:`held` fails when built, not mid crawl.
    """

    @abstractmethod
    def held(self, method: str) -> list[Any] | None:
        """Every release held for ``method``, or ``None`` for no such listing."""


def artist_releases(artist: Any, methods: Iterable[str] = RELEASE_METHODS, *,
                    skipped: list[str] | None = None, **kwargs: Any) -> list[Any]:
    """Every release credited to an artist, across both release-type listings.

    Stops on an **empty page**, the weaker rule, because the client exposes no count
    (R-385); the extra request per method is worth it (R-384). Deduplicated across
    the two. A method the client lacks is skipped and appended to ``skipped`` when
    given (R-261); one that cannot page is fatal. A :class:`HeldReleases` object is
    read whole and spends no budget (R-888).
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

#: U226. The reads agree, or the unpaged one is a first part of the window read.
WINDOW_AGREES = "agrees"
#: U226. They differ and the unpaged read holds the declared count: it is the reading.
WINDOW_UNPAGED = "unpaged"
#: U226. They differ and the unpaged read is not whole: a lag, read again or held.
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
    """The client's own read of a playlist with no window, as served now (U226).

    The window read can lag a move for minutes while this read is current. The
    client may cap it at a first page, so when it holds fewer tracks than declared
    the read walks on by offset, each request starting one track back, and takes a
    page only while it starts on the last track read, is no longer than the first
    and carries the first page's ``_etag``. It stops at the declared count, a short
    page or a page that does not hold together, so a broken walk reads as a first
    part (R-1360). That a later page is served current and that the tag is per
    playlist are not measured live. :func:`judge_window` holds the result to the
    declared count, and a signature fault raises :class:`ListingNotPaginated`.
    """
    def call(offset: int) -> Callable[[int, int], Any]:
        def ask(_limit: int, _offset: int) -> Any:
            try:
                return playlist.tracks(offset=offset) if offset else playlist.tracks()
            except TypeError as exc:
                # A signature fault, not a wait: the ladder would only sleep on it.
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
    for _ask in range(declared):
        if len(rows) >= declared:
            break
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

    :data:`WINDOW_AGREES` when the two are the same, :data:`WINDOW_UNPAGED` when the
    unpaged read holds exactly the declared count, else :data:`WINDOW_LAGS`. An
    unpaged first part of the window agrees only when the window is short of the
    count or nothing is declared, since unplayable tracks are left out of both
    (R-1362); beside a whole window it is a broken walk and lags (R-1360).
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


#: Every listing shape as name to wrapper. The test suite's guard reads it, so a new
#: wrapper arms the guard for its methods (P3).
WRAPPERS: dict[str, Callable[..., list[Any]]] = {
    "playlist_tracks": playlist_tracks, "favorite_tracks": favorite_tracks,
    "account_playlists": account_playlists, "artist_releases": artist_releases,
    "account_folders": account_folders, "folder_playlists": folder_playlists,
    "folder_folders": folder_folders,
}

#: Provider listing methods not to be called outside this module. ``tracks`` is a
#: violation only with pagination arguments, being an ordinary name here too (P7).
GUARDED_METHODS = frozenset(
    {
        "tracks", "playlist_and_favorite_playlists", "get_albums", "get_ep_singles",
        "playlist_folders",
    }
)
PAGINATION_KEYWORDS = frozenset({"limit", "offset"})


__all__ = [
    "ACCOUNT_PLAYLISTS_ENDPOINT", "DEFAULT_BASE_DELAY_S", "DEFAULT_MAX_DELAY_S",
    "DEFAULT_MAX_RETRIES", "FOLDER_ENDPOINT", "FOLDER_ORDER", "FOLDER_WALK", "GUARDED_METHODS",
    "PAGE_CAPS", "PAGE_SIZES", "PAGINATION_KEYWORDS", "RELEASE_METHODS", "STOP_RULES",
    "WINDOW_AGREES", "WINDOW_LAGS", "WINDOW_UNPAGED", "WRAPPERS", "HeldReleases",
    "ListingNotPaginated", "ListingTruncated", "StopRule", "account_folders", "account_playlists",
    "artist_releases", "favorite_tracks", "favorite_tracks_declared", "fetch_with_retry",
    "folder_folders", "folder_playlists", "paginate", "paginate_cursor", "judge_window",
    "playlist_tracks", "playlist_tracks_unpaged", "row_id",
]
