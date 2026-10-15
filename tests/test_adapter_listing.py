"""U14: one pagination wrapper per listing shape, and no call site paging by hand.

THE DEFECT UNDER TEST is quiet by construction. The provider's client returns one
server page when asked for a listing without pagination arguments, and it returns
it without complaint, so a truncated answer and a short answer are the same
object. In the source system three independently written call sites each had to
rediscover this, and one of them never did.

So there are two kinds of test here, and both are needed:

* **Behavioural**, proving the wrappers page, retry, and deduplicate correctly
  against fakes.
* **Structural**, proving no module in the product calls a provider listing
  method directly. A behavioural test can only cover the call sites that exist;
  the structural one covers the ones somebody writes next month, which is where
  this defect came from all three previous times.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from cratekit.acquire import listing

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
LISTING_MODULE = SRC_ROOT / "cratekit" / "acquire" / "listing.py"
VENDOR_ROOT = SRC_ROOT / "cratekit" / "_vendor"


class Paged:
    """A provider listing that serves a fixed corpus in server pages.

    Called with no arguments it returns only the first page, exactly as the real
    client does. That is what lets a test assert the truncation is real rather
    than hypothetical.

    It publishes NO count, no ``num_tracks`` and no ``get_tracks_count``, so
    every wrapper driven against it exercises the degraded walk: a shape that
    declares the total rule and cannot get one falls back to ending on an empty
    page. ``Omitting`` is the fake that publishes a count.
    """

    def __init__(self, items: list, page_size: int) -> None:
        self._items = items
        self._page_size = page_size
        self.calls: list[tuple[int, int]] = []

    def tracks(self, limit: int | None = None, offset: int = 0) -> list:
        if limit is None:
            return self._items[: self._page_size]
        self.calls.append((limit, offset))
        return self._items[offset : offset + limit]


class Item:
    def __init__(self, identifier: str) -> None:
        self.id = identifier

    def __repr__(self) -> str:  # pragma: no cover - debugging aid only
        return f"Item({self.id!r})"


def corpus(count: int, prefix: str = "t") -> list[Item]:
    return [Item(f"{prefix}{n}") for n in range(count)]


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: a listing longer than one page returns fully
# ═══════════════════════════════════════════════════════════════════════════


def test_a_listing_longer_than_one_page_returns_fully():
    playlist = Paged(corpus(250), listing.PAGE_SIZES["playlist_tracks"])
    got = listing.playlist_tracks(playlist)
    assert len(got) == 250
    assert [item.id for item in got] == [item.id for item in playlist._items]


def test_the_same_fixture_truncates_under_an_unpaginated_re_fetch():
    """The plan's scenario, asserted as the failure it protects against.

    Without this assertion the test above proves the wrapper works but not that
    it was needed, and a reviewer removing the wrapper would see a green suite.
    """
    playlist = Paged(corpus(250), listing.PAGE_SIZES["playlist_tracks"])
    assert len(playlist.tracks()) == 100
    assert len(playlist.tracks()) != len(listing.playlist_tracks(playlist))


def test_a_listing_with_no_declared_total_walks_to_an_empty_page():
    """U65. The short page stop is what R-383 measured wrong, and this is its cost.

    This fixture publishes no count, so the walk takes the weaker rule. Reading
    150 items costs a third request that returns nothing. That request is the
    whole price of the fallback, and it is asserted here rather than described so
    that a later author reverting to the short page rule to save it has to delete
    a test that says what the saving buys.
    """
    playlist = Paged(corpus(150), 100)
    listing.playlist_tracks(playlist)
    assert playlist.calls == [(100, 0), (100, 100), (100, 200)]


def test_an_exact_multiple_of_the_page_size_needs_the_empty_page():
    """The case the short page rule could never have handled either.

    Undeclared again, so this is the fallback walk. A shape ending on a declared
    total pays no terminating request here at all.
    """
    playlist = Paged(corpus(200), 100)
    got = listing.playlist_tracks(playlist)
    assert len(got) == 200
    assert playlist.calls == [(100, 0), (100, 100), (100, 200)]


def test_an_empty_listing_reads_as_empty_and_not_as_an_error():
    assert listing.playlist_tracks(Paged([], 100)) == []


def test_a_runaway_offset_raises_rather_than_returning_what_it_collected():
    """U65. A provider that ignores the offset otherwise turns a read into a hang.

    This is not hypothetical tidiness: a full page every time is exactly what a
    broken or renamed offset parameter produces, and no stop condition arrives.

    What changed in U65 is the ENDING. The budget used to break the loop and
    return, which traded a hang for a capped length answer indistinguishable from
    a complete one, the exact thing ``ListingNotPaginated`` already refuses to do
    one function over. Spending the budget now raises.
    """

    def ignores_the_offset(limit: int, offset: int) -> list:
        return corpus(limit)

    with pytest.raises(listing.ListingTruncated) as raised:
        listing.paginate(
            ignores_the_offset,
            page_size=100,
            stop=listing.StopRule.EMPTY_PAGE,
            max_pages=3,
            shape="favorite_tracks",
        )
    message = str(raised.value)
    assert "favorite_tracks" in message
    assert "3 requests" in message
    assert "offset" in message


def test_the_budget_is_spent_on_requests_and_the_walk_is_not_restarted():
    """The count in the message is items collected, so a zero there is its own bug."""

    def ignores_the_offset(limit: int, offset: int) -> list:
        return corpus(limit)

    with pytest.raises(listing.ListingTruncated) as raised:
        listing.paginate(
            ignores_the_offset,
            page_size=10,
            stop=listing.StopRule.EMPTY_PAGE,
            max_pages=4,
        )
    assert "40 item(s)" in str(raised.value)


def test_the_short_page_rule_still_stops_short_when_a_caller_declares_it():
    """The rule no shape uses today is still the rule this module offers.

    Kept tested rather than deleted: an untested branch in a policy enum is how
    the next author discovers it does not work, at the moment they need it.
    """
    playlist = Paged(corpus(150), 100)
    got = listing.paginate(
        lambda limit, offset: playlist.tracks(limit=limit, offset=offset),
        page_size=100,
        stop=listing.StopRule.SHORT_PAGE,
        max_pages=10,
    )
    assert len(got) == 150
    assert playlist.calls == [(100, 0), (100, 100)]


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: the provider omits items from the window it serves (R-383)
# ═══════════════════════════════════════════════════════════════════════════


class Omitting:
    """A provider listing that OMITS items from the window it serves.

    R-383's mechanism as a fixture. The provider holds ``held`` rows and will not
    serve some of them, but it still COUNTS them when it slices the window, so a
    request for ``page_size`` at ``offset`` returns the servable subset of
    ``held[offset : offset + page_size]``. That subset is shorter than the page
    size while items remain past it, which is what makes a short page a lie here.

    Measured against tidalapi 0.8.11, the omission is the provider's and not the
    client's: ``user.Favorites.tracks`` hands the response straight to
    ``request.map_json``, which maps every item in ``items`` with no filtering.
    ``Favorites.get_tracks_count`` documents the other half, that the total the
    API reports "also includes track that may not be available for playback".
    """

    def __init__(self, held: list[Item], omitted: set[str], *, declares: bool = True) -> None:
        self._held = held
        self._omitted = omitted
        self.calls: list[tuple[int, int]] = []
        self.counted = 0
        # The count the provider publishes is the count of what it HOLDS, not of
        # what it serves. That is the whole reason it can end the walk: it is cut
        # from the same sequence the windows are cut from.
        self.num_tracks = len(held) if declares else -1
        self._declares = declares

    def get_tracks_count(self) -> int:
        self.counted += 1
        return len(self._held)

    def _serve(self, limit: int | None = None, offset: int = 0) -> list:
        self.calls.append((limit or 0, offset))
        window = self._held[offset : offset + (limit or len(self._held))]
        return [item for item in window if item.id not in self._omitted]

    tracks = _serve
    get_albums = _serve

    def get_ep_singles(self, limit: int | None = None, offset: int = 0) -> list:
        return []


def omitting_corpus(held: int, omit: range, prefix: str = "t") -> Omitting:
    """``held`` rows of which the ones at ``omit`` will not be served."""
    rows = corpus(held, prefix=prefix)
    return Omitting(rows, {rows[index].id for index in omit})


def test_the_favourites_listing_reads_the_whole_account_and_not_its_newest_fraction():
    """R-383, reproduced at the numbers it was measured at on 2026-09-17.

    204 rows counted, 7 of them unservable, page size 100. The shipped short page
    rule sees 93 on the first window, reads 93 as the end, and returns 93 out of
    the 197 the account actually serves. That is the live measurement exactly.

    The walk ends on the declared total of 204, so it spends three requests and
    one count, not four requests: the count replaces the page that would have
    ended it.
    """
    favorites = omitting_corpus(204, range(7))
    session = Session(User(favorites=favorites))

    assert len(favorites.tracks(limit=100, offset=0)) == 93  # the page that lied
    favorites.calls.clear()

    got = listing.favorite_tracks(session)
    assert len(got) == 197
    assert favorites.calls == [(100, 0), (100, 100), (100, 200)]
    assert favorites.counted == 1


def test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk():
    """The defect the empty page rule left behind, which the total closes.

    300 counted rows with rows 100 to 199 unservable. That middle window comes
    back EMPTY in the middle of the collection, so any rule reading the end off a
    page's shape stops there and returns 100 of the 200 servable rows, silently.
    Reachable here specifically: this listing is ordered by date added and a
    label catalogue is hearted in one batch, so a withdrawn label leaves exactly
    this, a contiguous run of unservable hearts one page long.
    """
    favorites = omitting_corpus(300, range(100, 200))
    session = Session(User(favorites=favorites))

    assert favorites.tracks(limit=100, offset=100) == []  # the empty middle

    got = listing.favorite_tracks(session)
    assert len(got) == 200
    assert [item.id for item in got[:2]] == ["t0", "t1"]
    assert [item.id for item in got[-2:]] == ["t298", "t299"]


def test_a_favourites_total_that_under_reports_does_not_truncate_the_walk():
    """The one way a declared total could stop early, and what settles it.

    A full window at the declared end means the count is behind the collection,
    so the walk carries on rather than trusting the number over what it can see.
    """

    class UnderReporting(Omitting):
        def get_tracks_count(self) -> int:
            self.counted += 1
            return 100

    favorites = UnderReporting(corpus(250), set())
    got = listing.favorite_tracks(Session(User(favorites=favorites)))
    assert len(got) == 250


def test_a_playlist_whose_provider_omits_a_track_reads_to_the_end():
    """The placeholder acquire walks this read, and nothing downstream sees a gap.

    The count is already on the playlist object, so this shape pays no request
    for its rule: three windows, no count call, no terminating page.
    """
    playlist = omitting_corpus(204, range(7))
    got = listing.playlist_tracks(playlist)
    assert len(got) == 197
    assert playlist.calls == [(100, 0), (100, 100), (100, 200)]
    assert playlist.counted == 0


def test_a_playlist_that_publishes_no_count_degrades_rather_than_refusing():
    """A weaker answer beats a failed read, and the weaker rule is still declared."""
    playlist = Omitting(corpus(150), set(), declares=False)
    got = listing.playlist_tracks(playlist)
    assert len(got) == 150
    assert playlist.calls == [(100, 0), (100, 100), (100, 200)]


def test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size():
    """Page size 50 here, not 100, so a shared constant would page this one wrong."""
    playlists = omitting_corpus(105, range(6), prefix="p")
    session = Session(User(serve=playlists._serve))
    got = listing.account_playlists(session)
    assert len(got) == 99
    assert playlists.calls == [(50, 0), (50, 50), (50, 100), (50, 150)]


def test_an_artist_release_listing_reads_to_the_end_across_both_methods():
    """A label catalogue that stops early is this product's core job done wrong."""
    artist = omitting_corpus(204, range(7), prefix="a")
    got = listing.artist_releases(artist)
    assert len(got) == 197


# ═══════════════════════════════════════════════════════════════════════════
# Scenario: a listing that cannot page refuses rather than truncating
# ═══════════════════════════════════════════════════════════════════════════


def test_a_listing_that_rejects_pagination_arguments_refuses():
    """The source system took the single page here. That is a silent truncation."""

    class Old:
        def tracks(self) -> list:
            return corpus(100)

    with pytest.raises(listing.ListingNotPaginated, match="one page"):
        listing.playlist_tracks(Old())


def test_the_refusal_is_immediate_and_is_not_slept_on():
    """U65. Waiting cannot change a client's signature.

    This refusal is raised by this module from the client's own shape, so it is
    permanent by construction, and the retry ladder used to catch it anyway: five
    attempts sleeping 1, 2, 4, 8 and 16 seconds, 31 in all, before re-raising the
    answer it had at the first attempt. It cost this very test file 31 of its 32
    seconds, which is how it was found.

    The cost is per listing. ``artist_releases`` reads one per release method per
    artist, so a label crawl over 200 artists would have slept for over three
    hours before reporting a fault it knew about immediately.

    The sleep is captured rather than timed. A wall clock assertion on a test that
    is fast when it passes measures the machine, and would go green on a slow
    machine for the wrong reason.
    """
    slept: list[float] = []

    class Old:
        def tracks(self) -> list:
            return corpus(100)

    with pytest.raises(listing.ListingNotPaginated):
        listing.playlist_tracks(Old(), sleep=slept.append)
    assert slept == []


def test_a_transient_failure_is_still_slept_on_the_full_ladder():
    """The exclusion above is one exception, not a narrowing of the policy.

    Paired with the test above deliberately: an exclusion written one line wide is
    one line away from swallowing the retry that this module's first full read of
    a large library depends on.
    """
    slept: list[float] = []
    attempts = {"n": 0}

    def flaky(limit: int, offset: int) -> list:
        attempts["n"] += 1
        raise TimeoutError("the provider is busy")

    with pytest.raises(TimeoutError):
        listing.fetch_with_retry(flaky, limit=10, offset=0, sleep=slept.append)
    assert attempts["n"] == listing.DEFAULT_MAX_RETRIES + 1
    assert slept == [1.0, 2.0, 4.0, 8.0, 16.0]


def test_a_refusal_that_says_waiting_cannot_help_is_not_slept_on():
    """A non retryable refusal passes through on the first attempt.

    An adapter that finds the stored session expired mid page refuses
    ``credential-missing``, and that refusal declares ``retryable=False``: the
    person has to log in, and no amount of waiting does that for them. Before
    this test the ladder slept 31 seconds on it and then re-raised the answer it
    already had, per listing, which is the ``ListingNotPaginated`` cost over
    again one exception type along. It was found as the slowest test in the
    suite rather than by reading the ladder.
    """
    from cratekit.core.cause import CratekitError, refuse

    slept: list[float] = []
    attempts = {"n": 0}

    def expired(limit: int, offset: int) -> list:
        attempts["n"] += 1
        raise refuse("credential-missing", "the session expired mid page", origin=("tests",))

    with pytest.raises(CratekitError) as excinfo:
        listing.fetch_with_retry(expired, limit=10, offset=0, sleep=slept.append)
    assert excinfo.value.cause.reason == "credential-missing"
    assert attempts["n"] == 1
    assert slept == []


def test_a_refusal_that_declares_itself_retryable_still_climbs_the_ladder():
    """The exclusion reads the refusal's own flag, never its type.

    Paired with the test above for the same reason the two before it are paired:
    excluding every ``CratekitError`` would swallow a rate limit an adapter chose
    to spell as a retryable refusal.
    """
    from cratekit.core.cause import CratekitError, refuse

    slept: list[float] = []

    def walled(limit: int, offset: int) -> list:
        raise refuse(
            "credential-missing", "try again shortly", retryable=True, origin=("tests",)
        )

    with pytest.raises(CratekitError):
        listing.fetch_with_retry(walled, limit=10, offset=0, sleep=slept.append)
    assert slept == [1.0, 2.0, 4.0, 8.0, 16.0]


def test_a_listing_method_that_does_not_exist_refuses_by_name():
    class Renamed:
        pass

    with pytest.raises(listing.ListingNotPaginated, match="tracks"):
        listing.playlist_tracks(Renamed())


# ═══════════════════════════════════════════════════════════════════════════
# Retry: a dropped page in a paginated read is a gap, not an error
# ═══════════════════════════════════════════════════════════════════════════


def test_a_transient_failure_retries_with_capped_exponential_backoff():
    attempts: list[int] = []
    slept: list[float] = []

    def flaky(limit: int, offset: int) -> list:
        attempts.append(offset)
        if len(attempts) < 3:
            raise RuntimeError("429 Too Many Requests")
        return corpus(5)

    got = listing.fetch_with_retry(flaky, limit=100, offset=0, sleep=slept.append)
    assert len(got) == 5
    assert slept == [1.0, 2.0]


def test_the_backoff_is_capped_rather_than_doubling_forever():
    slept: list[float] = []

    def always_fails(limit: int, offset: int) -> list:
        raise RuntimeError("503 Service Unavailable")

    with pytest.raises(RuntimeError):
        listing.fetch_with_retry(
            always_fails,
            limit=100,
            offset=0,
            max_retries=8,
            base_delay=4.0,
            max_delay=10.0,
            sleep=slept.append,
        )
    assert max(slept) == 10.0
    assert len(slept) == 8


def test_a_permanent_failure_surfaces_after_the_retry_ceiling():
    """Breadth in what is retried is only honest if it is bounded."""
    calls: list[int] = []

    def always_fails(limit: int, offset: int) -> list:
        calls.append(offset)
        raise ValueError("the listing method is gone")

    with pytest.raises(ValueError):
        listing.fetch_with_retry(
            always_fails, limit=100, offset=0, max_retries=2, sleep=lambda _: None
        )
    assert len(calls) == 3


# ═══════════════════════════════════════════════════════════════════════════
# Deduplication: only where the provider can genuinely repeat an item
# ═══════════════════════════════════════════════════════════════════════════


class Favorites:
    def __init__(self, pages: list[list[Item]]) -> None:
        self._pages = pages

    def tracks(self, limit: int | None = None, offset: int = 0) -> list:
        index = offset // (limit or 1)
        return self._pages[index] if index < len(self._pages) else []


class Session:
    def __init__(self, user) -> None:
        self.user = user


class _ItemParser:
    """The client's playlist parser, reduced to the identifier it reads."""

    @staticmethod
    def parse(data: dict) -> Item:
        return Item(data["uuid"])


class AccountRequest:
    """The account playlist endpoint behind the user's request object (R-1016).

    Serves whatever ``serve(limit, offset)`` returns, wrapped the way the
    endpoint wraps it, each playlist under ``playlist`` beside the ``created``
    the walk moves onto it.
    """

    def __init__(self, serve) -> None:
        self._serve = serve
        self.sent: list[tuple[str, str, dict]] = []

    def request(self, method: str, path: str, params: dict | None = None) -> _Answer:
        self.sent.append((method, path, dict(params or {})))
        window = self._serve(limit=params["limit"], offset=params["offset"])
        return _Answer(
            {
                "items": [
                    {"created": "2026-01-01T00:00:00Z", "playlist": {"uuid": item.id}}
                    for item in window
                ]
            }
        )


class User:
    def __init__(
        self, favorites=None, playlists: list[list[Item]] | None = None, serve=None
    ) -> None:
        self.favorites = favorites
        self._playlists = playlists or []
        self.id = 42
        self.playlist = _ItemParser()
        self.request = AccountRequest(serve or self._page)

    def _page(self, limit: int | None = None, offset: int = 0) -> list:
        index = offset // (limit or 1)
        return self._playlists[index] if index < len(self._playlists) else []


def test_a_favourite_repeated_across_a_page_boundary_is_returned_once():
    """A favourite added mid-read shifts the window and re-serves an item."""
    size = listing.PAGE_SIZES["favorite_tracks"]
    first = corpus(size)
    second = [first[-1], *corpus(3, prefix="later")]
    session = Session(User(favorites=Favorites([first, second])))

    got = listing.favorite_tracks(session)
    assert len(got) == size + 3
    assert len({item.id for item in got}) == len(got)


def test_a_playlist_that_lists_a_track_twice_keeps_both():
    """Deduplicating here would silently edit the user's playlist."""
    twice = Item("same")
    playlist = Paged([twice, Item("other"), twice], 100)
    assert [item.id for item in listing.playlist_tracks(playlist)] == ["same", "other", "same"]


def test_account_playlists_page_and_deduplicate():
    size = listing.PAGE_SIZES["account_playlists"]
    first = corpus(size, prefix="p")
    session = Session(User(playlists=[first, [first[0], Item("p-new")]]))
    got = listing.account_playlists(session)
    assert len(got) == size + 1


def test_account_playlists_are_returned_unfiltered():
    """Pagination and nothing else. Whose playlist it is differs per caller."""
    session = Session(User(playlists=[[Item("mine"), Item("followed")]]))
    assert [p.id for p in listing.account_playlists(session)] == ["mine", "followed"]


# ═══════════════════════════════════════════════════════════════════════════
# Artist releases: two listings, one answer
# ═══════════════════════════════════════════════════════════════════════════


class Artist:
    def __init__(self, albums: list[Item], singles: list[Item] | None) -> None:
        self._albums = albums
        self._singles = singles

    def get_albums(self, limit: int | None = None, offset: int = 0) -> list:
        return self._albums[offset : offset + (limit or len(self._albums))]

    def get_ep_singles(self, limit: int | None = None, offset: int = 0) -> list:
        if self._singles is None:
            raise AttributeError("get_ep_singles")
        return self._singles[offset : offset + (limit or len(self._singles))]


def test_artist_releases_merge_both_listings_and_deduplicate():
    shared = Item("a1")
    artist = Artist([shared, Item("a2")], [shared, Item("s1")])
    assert [r.id for r in listing.artist_releases(artist)] == ["a1", "a2", "s1"]


def test_a_missing_release_listing_is_skipped_rather_than_fatal():
    """Losing one listing beats refusing to crawl a label at all."""

    class OnlyAlbums:
        # Honours the offset. Under U65's empty page rule a fake that ignores it
        # is a runaway, which is a different test's subject and would mask this
        # one's: the assertion here is about a MISSING method being skipped.
        def get_albums(self, limit: int | None = None, offset: int = 0) -> list:
            return corpus(2, prefix="a")[offset : offset + (limit or 2)]

    assert len(listing.artist_releases(OnlyAlbums())) == 2


def test_a_skipped_release_listing_is_named_to_a_caller_that_asks():
    """R-261: the skip stands, and it leaves a record rather than nothing."""

    class OnlyAlbums:
        def get_albums(self, limit: int | None = None, offset: int = 0) -> list:
            return corpus(2, prefix="a")[offset : offset + (limit or 2)]

    skipped: list[str] = []
    assert len(listing.artist_releases(OnlyAlbums(), skipped=skipped)) == 2
    assert skipped == ["get_ep_singles"]

    whole: list[str] = []
    listing.artist_releases(Artist([Item("a1")], [Item("s1")]), skipped=whole)
    assert whole == []


def test_an_artist_listing_longer_than_a_page_is_read_fully():
    artist = Artist(corpus(180, prefix="a"), [])
    assert len(listing.artist_releases(artist)) == 180


# ═══════════════════════════════════════════════════════════════════════════
# The structural guard: nothing outside this module pages by hand
# ═══════════════════════════════════════════════════════════════════════════


def direct_listing_calls(source: str, module: str) -> list[str]:
    """Return every direct call to a provider listing method in ``source``.

    ``tracks`` is only a violation when called WITH a pagination argument.
    "tracks" is an ordinary accessor name that this codebase uses for its own
    collections, and a guard that fires on correct code gets routed around rather
    than obeyed, which is the same failure it was written to prevent (P7). What
    unmistakably identifies a raw provider listing call is the caller doing the
    paging itself, and that is exactly what a ``limit`` or ``offset`` keyword is.
    """
    problems: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        attribute = node.func.attr
        if attribute not in listing.GUARDED_METHODS:
            continue
        keywords = {kw.arg for kw in node.keywords}
        ambiguous = attribute == "tracks"
        if ambiguous and not (keywords & listing.PAGINATION_KEYWORDS):
            continue
        problems.append(
            f"{module}:{node.lineno} calls .{attribute}() directly; provider listings "
            f"go through cratekit.acquire.listing, which is the only place that knows "
            f"the server page size"
        )
    return problems


PLANTED_PAGINATION_METHODS = frozenset(
    {
        "tracks",
        "playlist_and_favorite_playlists",
        "get_albums",
        "get_ep_singles",
        "playlist_folders",
    }
)


def test_the_planted_pagination_loop_cases_cover_the_guarded_set():
    """P4: the planted names and the production set describe the same thing.

    The names live in this file because the mutation driver edits ``src`` and
    never the suite. Parametrising over the live ``GUARDED_METHODS`` would drop
    the case for a name the set just lost, and removing a member would stay
    green. Adding a name without a planted case fails here, and a planted case
    for a name not in the set fails here too.
    """
    assert PLANTED_PAGINATION_METHODS == listing.GUARDED_METHODS


@pytest.mark.parametrize("method", sorted(PLANTED_PAGINATION_METHODS))
def test_the_guard_catches_a_hand_written_pagination_loop(method):
    source = (
        "def read(obj):\n"
        "    out = []\n"
        "    offset = 0\n"
        "    while True:\n"
        f"        page = obj.{method}(limit=100, offset=offset)\n"
        "        if not page:\n"
        "            break\n"
        "        out.extend(page)\n"
        "        offset += 100\n"
        "    return out\n"
    )
    assert len(direct_listing_calls(source, "cratekit.label.sweep")) == 1


def test_the_guard_catches_the_call_that_never_pages_at_all():
    source = "playlists = session.user.playlist_and_favorite_playlists()\n"
    assert len(direct_listing_calls(source, "cratekit.sync.sources")) == 1


@pytest.mark.parametrize(
    "source",
    [
        "count = len(playlist.tracks)\n",
        "for track in album.tracks():\n    pass\n",
        "rows = report.tracks(genre=genre)\n",
    ],
)
def test_the_guard_leaves_ordinary_accessors_alone(source):
    """P7: a guard with false positives gets suppressed, and protects nothing."""
    assert direct_listing_calls(source, "cratekit.reports.library") == []


def test_no_product_module_calls_a_provider_listing_directly():
    """The real tree, which is where the previous three violations lived.

    The vendored tree is excluded. It IS the provider client wrapper, so it calls
    those methods by definition, and it is third-party source that Cratekit does
    not restyle. The rule is about Cratekit's own call sites.
    """
    problems: list[str] = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        if path == LISTING_MODULE or VENDOR_ROOT in path.parents:
            continue
        module = ".".join(path.relative_to(SRC_ROOT).with_suffix("").parts)
        problems += direct_listing_calls(path.read_text(), module)
    assert not problems, "provider listings called outside the wrappers:\n" + "\n".join(problems)


def test_every_declared_listing_shape_has_a_wrapper():
    """P4: the guarded set and the wrapper set describe the same thing.

    A page size declared with no wrapper is a shape somebody will page by hand,
    and a wrapper with no page size is a wrapper guessing. U65 adds two more
    tables to the set, and a shape missing from either one is a shape whose stop
    rule or whose budget somebody picked at the call site.
    """
    assert set(listing.WRAPPERS) == set(listing.PAGE_SIZES)
    assert set(listing.WRAPPERS) == set(listing.STOP_RULES)
    assert set(listing.WRAPPERS) == set(listing.PAGE_CAPS)
    for name, wrapper in listing.WRAPPERS.items():
        assert callable(wrapper), name


# ═══════════════════════════════════════════════════════════════════════════
# U65: the stop rule is declared per listing, and the declaration is guarded
# ═══════════════════════════════════════════════════════════════════════════


def test_every_shape_declares_the_rule_its_provider_can_actually_support():
    """Asserted from the table, not from behaviour.

    A behavioural test proves a shape reads to the end against the fixture it was
    handed. This one proves which rule it SAYS it uses. The split is not a
    preference: the two shapes on the declared total are the two whose provider
    publishes a count of the collection it serves, and the other two take the
    weaker rule because it publishes none, which R-385 records. A shape moved
    onto a rule its provider cannot support fails here by name.
    """
    assert listing.STOP_RULES == {
        "playlist_tracks": listing.StopRule.DECLARED_TOTAL,
        "favorite_tracks": listing.StopRule.DECLARED_TOTAL,
        "account_playlists": listing.StopRule.EMPTY_PAGE,
        "artist_releases": listing.StopRule.EMPTY_PAGE,
        # R-878. The folder endpoint ignores offset and pages by its cursor.
        "account_folders": listing.StopRule.CURSOR,
        "folder_playlists": listing.StopRule.CURSOR,
        "folder_folders": listing.StopRule.CURSOR,
    }
    assert listing.StopRule.SHORT_PAGE not in listing.STOP_RULES.values()


def test_each_wrapper_docstring_names_the_rule_its_table_declares():
    """The prose and the table cannot drift apart unnoticed.

    Phillip's requirement for this unit was that each listing says which rule it
    uses AND why. The why is prose and cannot be machine checked. That the prose
    is talking about the rule actually in force can be, and this is the half that
    goes stale first: a rule changes in a dict and the paragraph under it keeps
    arguing for the old one.
    """
    for name, wrapper in listing.WRAPPERS.items():
        phrase = listing.STOP_RULES[name].value
        doc = (wrapper.__doc__ or "").lower()
        assert phrase in doc, f"{name} declares {phrase!r} and its docstring never says so"


@pytest.mark.parametrize("missing", ["stop", "max_pages"])
def test_paginate_refuses_to_be_called_without_a_declared_rule_or_budget(missing):
    """The guard that makes the declaration real rather than conventional.

    R-383's shape was one rule written once into this function, silently
    governing four listings nobody had checked against it. A default on either
    argument rebuilds that, so both are required and a wrapper that forgets to
    choose fails to call.
    """
    arguments = {
        "page_size": 100,
        "stop": listing.StopRule.EMPTY_PAGE,
        "max_pages": 5,
    }
    del arguments[missing]
    with pytest.raises(TypeError) as raised:
        listing.paginate(lambda limit, offset: [], **arguments)
    assert missing in str(raised.value)


def test_every_budget_clears_the_largest_collection_this_project_has_measured():
    """A budget that can fire on real data turns a correctness fix into an outage.

    The numbers on the right are the live reads of 2026-09-17. The margin is the
    assertion: each budget is checked against a collection an order of magnitude
    past anything measured, so a future edit that tightens a budget toward real
    data fails here rather than in a sweep.
    """
    measured = {
        "playlist_tracks": 197,
        "account_playlists": 599,
        "favorite_tracks": 197,
        "artist_releases": 197,
        # R-835. Not reads: one folder per followed label, 47 at sitting 11,
        # and one year playlist per release year, under forty on any label.
        "account_folders": 47,
        "folder_playlists": 40,
        "folder_folders": 10,
    }
    assert set(measured) == set(listing.PAGE_CAPS)
    for name, largest in measured.items():
        reachable = listing.PAGE_CAPS[name] * listing.PAGE_SIZES[name]
        if listing.STOP_RULES[name] is not listing.StopRule.DECLARED_TOTAL:
            # A walk that does not end on a total spends its last request on the
            # page that ends it, so one page of the budget buys no items. Leaving
            # this out overstates every ceiling by a page, and a collection of
            # exactly the product would raise while blaming a working offset.
            reachable -= listing.PAGE_SIZES[name]
        assert reachable >= largest * 10, f"{name} budget reaches only {reachable}"


def test_the_declared_count_is_retried_on_the_same_ladder_every_page_is():
    """U65's own P6 row: the count is a request the walk did not used to make.

    Against the same API and the same session, so the rate limit that makes page
    one retry five times would otherwise make the count fail outright and take the
    whole listing with it. A correctness fix that introduces a new failure path is
    a bad trade for a saved line.
    """
    slept: list[float] = []
    attempts = {"n": 0}

    class Flaky(Omitting):
        def get_tracks_count(self) -> int:
            attempts["n"] += 1
            if attempts["n"] < 3:
                raise TimeoutError("the provider is busy")
            return len(self._held)

    favorites = Flaky(corpus(150), set())
    got = listing.favorite_tracks(Session(User(favorites=favorites)), sleep=slept.append)
    assert len(got) == 150
    assert attempts["n"] == 3
    assert slept == [1.0, 2.0]


def test_a_permanent_count_failure_still_surfaces_at_the_ceiling():
    """Retrying it must not become swallowing it."""

    class Broken(Omitting):
        def get_tracks_count(self) -> int:
            raise RuntimeError("the count endpoint is gone")

    favorites = Broken(corpus(150), set())
    with pytest.raises(RuntimeError, match="count endpoint"):
        listing.favorite_tracks(Session(User(favorites=favorites)), sleep=lambda _: None)


# ═══════════════════════════════════════════════════════════════════════════
# R-878: the folder endpoint ignores offset and pages by cursor
# ═══════════════════════════════════════════════════════════════════════════


class _Answer:
    def __init__(self, body: dict) -> None:
        self._body = body

    def json(self) -> dict:
        return self._body


def _raw_folder(index: int) -> dict:
    """One root item as the endpoint serves it, in the shape ``parse_folder`` reads."""
    return {
        "trn": f"trn:folder:f{index}",
        "itemType": "FOLDER",
        "name": f"Label {index:02d}",
        "addedAt": "2026-01-01T00:00:00Z",
        "data": {
            "id": f"f{index}",
            "createdAt": "2026-01-01T00:00:00Z",
            "lastModifiedAt": "2026-01-01T00:00:00Z",
            "totalNumberOfItems": 0,
        },
    }


def _raw_playlist(index: int) -> dict:
    """One folder item as the endpoint serves it, its ``data`` a playlist."""
    return {
        "trn": f"trn:playlist:p{index}",
        "itemType": "PLAYLIST",
        "name": f"Kompakt {2000 + index}",
        "data": {
            "uuid": f"p{index}",
            "title": f"Kompakt {2000 + index}",
            "type": "USER",
            "numberOfTracks": 0,
            "numberOfVideos": 0,
            "description": "",
            "duration": 0,
            "image": None,
            "squareImage": None,
            "promotedArtists": [],
            "creator": None,
        },
    }


class CursorEndpoint:
    """The provider's collection folder endpoint as R-878 measured it.

    ``offset`` is IGNORED: a request without a cursor is served the first window
    whatever offset it names, which is what the author's account did at every
    offset from 0 to 1,000. Each response carries ``items``, the declared
    ``totalNumberOfItems`` and, while more remain, a ``cursor`` that sent back
    serves the next window. ``page`` is the window the provider serves, which can
    be narrower than the limit asked for, as the live 26 at a limit of 50 was.

    ``stuck`` hands back the same cursor for ever, and sending it serves the same
    second window, so the walk never ends unless its budget does.
    """

    def __init__(self, held: list[dict], *, page: int, total: int | None = -1,
                 cursors: bool = True, stuck: bool = False) -> None:
        self.held = held
        self.page = page
        self.total = len(held) if total == -1 else total
        self.cursors = cursors
        self.stuck = stuck
        self.sent: list[dict] = []
        self.fail: list[Exception] = []

    def request(self, method: str, path: str, params: dict | None = None,
                data: dict | None = None, headers: dict | None = None,
                base_url: str | None = None) -> _Answer:
        self.sent.append(
            {"method": method, "path": path, "base_url": base_url, **dict(params or {})}
        )
        if self.fail:
            raise self.fail.pop(0)
        cursor = (params or {}).get("cursor")
        start = int(cursor.removeprefix("after-")) if cursor else 0
        window = self.held[start : start + min(params["limit"], self.page)]
        end = start + len(window)
        body: dict = {"items": window, "lastModifiedAt": "2026-10-03T00:00:00Z"}
        if self.total is not None:
            body["totalNumberOfItems"] = self.total
        if self.cursors and end < len(self.held):
            body["cursor"] = f"after-{self.page if self.stuck else end}"
        return _Answer(body)


def _client_over(endpoint: CursorEndpoint):
    """A real ``tidalapi`` session whose request object is the fake endpoint.

    Real rather than a stand in, so the walk is proven against the client's own
    ``parse_folder``, its folder object and its playlist parser, the parts R-878
    has the walk reach past the client's listing methods for. Building one makes
    no request.
    """
    tidalapi = pytest.importorskip("tidalapi")
    session = tidalapi.Session()
    session.request = endpoint
    return session


def test_the_root_folders_are_walked_by_cursor_past_an_endpoint_that_ignores_offset():
    """The brief's first scenario: 55 folders over pages of 10, all returned once."""
    import tidalapi.playlist

    endpoint = CursorEndpoint([_raw_folder(n) for n in range(55)], page=10)
    session = _client_over(endpoint)
    found = listing.account_folders(session, sleep=lambda _: None)

    assert [folder.id for folder in found] == [f"f{n}" for n in range(55)]
    assert all(isinstance(folder, tidalapi.playlist.Folder) for folder in found)
    assert found[54].name == "Label 54"
    assert len(endpoint.sent) == 6
    assert [sent.get("cursor") for sent in endpoint.sent] == [
        None, "after-10", "after-20", "after-30", "after-40", "after-50",
    ]


def test_the_folder_request_is_the_one_the_client_sends_with_a_cursor_and_no_offset():
    """The walk asks what ``Favorites.playlist_folders`` asks, through its transport."""
    endpoint = CursorEndpoint([_raw_folder(n) for n in range(15)], page=10)
    session = _client_over(endpoint)
    listing.account_folders(session, sleep=lambda _: None)

    first, second = endpoint.sent
    assert first == {
        "method": "GET",
        "path": "my-collection/playlists/folders",
        "base_url": session.config.api_v2_location,
        "folderId": "root",
        "limit": listing.PAGE_SIZES["account_folders"],
        "order": "NAME",
    }
    assert second == {**first, "cursor": "after-10"}


def test_a_folders_playlists_are_walked_by_cursor_through_the_folders_own_parser():
    """The brief's fourth scenario: a folder holding 12 playlists over pages of 5."""
    import tidalapi.playlist

    endpoint = CursorEndpoint([_raw_playlist(n) for n in range(12)], page=5)
    session = _client_over(endpoint)
    handle = session.folder()
    handle.id = "folder-kompakt"
    found = listing.folder_playlists(handle, sleep=lambda _: None)

    assert [playlist.id for playlist in found] == [f"p{n}" for n in range(12)]
    assert all(isinstance(playlist, tidalapi.playlist.Playlist) for playlist in found)
    assert found[11].name == "Kompakt 2011"
    assert [sent.get("cursor") for sent in endpoint.sent] == [None, "after-5", "after-10"]
    assert {sent["folderId"] for sent in endpoint.sent} == {"folder-kompakt"}
    assert all("includeOnly" not in sent for sent in endpoint.sent)
    assert all("offset" not in sent for sent in endpoint.sent)


def test_the_root_count_covers_playlists_too_so_folders_are_kept_after_counting():
    """R-887. The live root declared 55 and held 26 folders beside 29 playlists.

    The endpoint is asked for everything, every item is counted against the
    declared total, and only the folders come back.
    """
    held = [_raw_folder(n) for n in range(26)] + [_raw_playlist(n) for n in range(29)]
    endpoint = CursorEndpoint(held, page=10)
    found = listing.account_folders(_client_over(endpoint), sleep=lambda _: None)

    assert [folder.id for folder in found] == [f"f{n}" for n in range(26)]
    assert all("includeOnly" not in sent for sent in endpoint.sent)


def test_a_folder_holding_a_folder_keeps_only_its_playlists():
    """R-887. A folder's count covers a folder nested in it as well."""
    endpoint = CursorEndpoint([_raw_folder(0)] + [_raw_playlist(n) for n in range(7)], page=5)
    session = _client_over(endpoint)
    handle = session.folder()
    handle.id = "folder-kompakt"
    found = listing.folder_playlists(handle, sleep=lambda _: None)

    assert [playlist.id for playlist in found] == [f"p{n}" for n in range(7)]


def test_a_short_walk_over_a_mixed_root_still_refuses():
    """R-887 keeps R-878's refusal: served fewer of any kind than declared."""
    held = [_raw_folder(n) for n in range(5)] + [_raw_playlist(n) for n in range(5)]
    endpoint = CursorEndpoint(held, page=10, total=11)
    with pytest.raises(listing.ListingTruncated, match="collected 10 item"):
        listing.account_folders(_client_over(endpoint), sleep=lambda _: None)


def test_a_response_with_no_cursor_ends_the_walk():
    """The brief's second scenario. More is held, none is offered, one request."""
    endpoint = CursorEndpoint(
        [_raw_folder(n) for n in range(30)], page=10, cursors=False, total=None
    )
    found = listing.account_folders(_client_over(endpoint), sleep=lambda _: None)
    assert len(found) == 10
    assert len(endpoint.sent) == 1


def test_an_empty_page_ends_the_walk_even_when_it_carries_a_cursor():
    pages = iter([
        {"items": [_raw_folder(0)], "cursor": "a"},
        {"items": [], "cursor": "b"},
        {"items": [_raw_folder(1)], "cursor": None},
    ])
    sent: list[str | None] = []

    def fetch(limit: int, cursor: str | None) -> dict:
        sent.append(cursor)
        return next(pages)

    got = listing.paginate_cursor(
        fetch, parse=lambda raw: raw["data"]["id"], **listing._shape("account_folders")
    )
    assert got == ["f0"]
    assert sent == [None, "a"]


def test_a_walk_that_collects_fewer_than_the_declared_count_refuses():
    """The brief's third scenario: ending is not the same as reaching the count."""
    endpoint = CursorEndpoint([_raw_folder(n) for n in range(30)], page=10, total=31)
    with pytest.raises(listing.ListingTruncated) as raised:
        listing.account_folders(_client_over(endpoint), sleep=lambda _: None)
    assert "collected 30" in str(raised.value)
    assert "declared 31" in str(raised.value)


def test_the_latest_declared_count_is_the_one_checked():
    """A folder removed mid walk lowers the count; the first answer must not win."""
    pages = iter([
        {"items": [_raw_folder(0), _raw_folder(1)], "totalNumberOfItems": 4, "cursor": "a"},
        {"items": [_raw_folder(2)], "totalNumberOfItems": 3},
    ])
    got = listing.paginate_cursor(
        lambda limit, cursor: next(pages),
        parse=lambda raw: raw["data"]["id"],
        **listing._shape("account_folders"),
    )
    assert got == ["f0", "f1", "f2"]


def test_a_folder_served_on_two_pages_is_returned_once():
    held = [_raw_folder(n) for n in range(12)]
    held.insert(10, _raw_folder(9))
    endpoint = CursorEndpoint(held, page=10, total=12)
    found = listing.account_folders(_client_over(endpoint), sleep=lambda _: None)
    assert [folder.id for folder in found] == [f"f{n}" for n in range(12)]


def test_a_cursor_that_never_changes_spends_the_budget_and_refuses():
    """The brief's fifth scenario. A fixed cursor serves the same window for ever."""
    endpoint = CursorEndpoint([_raw_folder(n) for n in range(30)], page=10, stuck=True)
    with pytest.raises(listing.ListingTruncated) as raised:
        listing.account_folders(_client_over(endpoint), sleep=lambda _: None)
    assert len(endpoint.sent) == listing.PAGE_CAPS["account_folders"]
    assert "not advancing its cursor" in str(raised.value)
    assert "collected 20" in str(raised.value)


def test_a_transient_failure_retries_the_same_cursor_and_not_the_first_page():
    endpoint = CursorEndpoint([_raw_folder(n) for n in range(25)], page=10)
    real = endpoint.request
    calls = {"n": 0}

    def flaky(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 2:
            endpoint.sent.append({"failed": True, **kwargs["params"]})
            raise TimeoutError("the provider is busy")
        return real(*args, **kwargs)

    endpoint.request = flaky
    slept: list[float] = []
    found = listing.account_folders(_client_over(endpoint), sleep=slept.append)
    assert len(found) == 25
    assert slept == [1.0]
    assert [sent.get("cursor") for sent in endpoint.sent] == [
        None, "after-10", "after-10", "after-20",
    ]


def test_a_client_without_the_request_object_refuses_by_name_and_is_not_retried():
    class Bare:
        config = None

    with pytest.raises(listing.ListingNotPaginated, match="request"):
        listing.account_folders(Bare(), sleep=lambda _: pytest.fail("slept"))


def test_paginate_refuses_a_shape_that_walks_by_cursor():
    """An offset walk over the folder endpoint reads its first page for ever."""
    calls: list[tuple[int, int]] = []
    with pytest.raises(ValueError, match="paginate_cursor"):
        listing.paginate(
            lambda limit, offset: calls.append((limit, offset)) or [Item("x")],
            **listing._shape("account_folders"),
        )
    assert calls == []


def test_paginate_cursor_refuses_a_shape_that_walks_by_offset():
    with pytest.raises(ValueError, match="paginate"):
        listing.paginate_cursor(
            lambda limit, cursor: pytest.fail("requested"),
            parse=lambda raw: raw,
            **listing._shape("account_playlists"),
        )


def test_a_parse_that_fails_transiently_is_retried_alone_without_refetching_the_page():
    """R-878 review: the playlist parser can be a request of its own.

    ``Playlist.parse_factory`` fetches a playlist the account created, so a rate
    limit can land on it. It sat inside the page fetch before the cursor walk,
    and was retried there; it must still be retried, and only itself.
    """
    pages = iter([{"items": [_raw_folder(n) for n in range(3)], "totalNumberOfItems": 3}])
    fetched: list[str | None] = []
    parsed: list[str] = []

    def fetch(limit: int, cursor: str | None) -> dict:
        fetched.append(cursor)
        return next(pages)

    def parse(raw: dict) -> str:
        parsed.append(raw["data"]["id"])
        if parsed == ["f0", "f1"]:
            raise TimeoutError("the playlist read was rate limited")
        return raw["data"]["id"]

    slept: list[float] = []
    got = listing.paginate_cursor(
        fetch, parse=parse, sleep=slept.append, **listing._shape("folder_playlists")
    )
    assert got == ["f0", "f1", "f2"]
    assert parsed == ["f0", "f1", "f1", "f2"]
    assert fetched == [None]
    assert slept == [1.0]


@pytest.mark.parametrize(
    "answer",
    [{"error": "upstream"}, {"items": None}, ["not", "a", "page"], None],
    ids=["no-items-no-count", "items-null", "a-list", "nothing"],
)
def test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing(answer):
    """R-878 review: an empty folder listing is what makes a caller create a folder.

    Read as an empty last page, any of these returned no folders at all, and the
    label playlists verb would have planned a second folder for every label.
    """
    calls: list[str | None] = []
    slept: list[float] = []

    def fetch(limit: int, cursor: str | None):
        calls.append(cursor)
        return answer

    with pytest.raises(ValueError, match="neither a list of items nor a count"):
        listing.paginate_cursor(
            fetch, parse=lambda raw: raw, sleep=slept.append,
            **listing._shape("account_folders"),
        )
    assert len(calls) == listing.DEFAULT_MAX_RETRIES + 1
    assert len(slept) == listing.DEFAULT_MAX_RETRIES


def test_a_response_with_a_count_and_no_items_is_an_empty_listing():
    """The other half: a folder the provider declares empty is empty."""
    got = listing.paginate_cursor(
        lambda limit, cursor: {"totalNumberOfItems": 0},
        parse=lambda raw: raw,
        **listing._shape("folder_playlists"),
    )
    assert got == []


def test_a_client_whose_request_rejects_the_arguments_refuses_by_name_unslept():
    """R-878 review: the translation ``_paged_caller`` made, kept for the raw call."""

    class Older:
        def request(self, method: str, path: str, params: dict | None = None):
            pytest.fail("a request that cannot carry its base url was sent")

    session = _client_over(CursorEndpoint([], page=10))
    session.request = Older()
    with pytest.raises(listing.ListingNotPaginated, match="changed shape"):
        listing.account_folders(session, sleep=lambda _: pytest.fail("slept"))


# ═══════════════════════════════════════════════════════════════════════════
# R-1016: a playlist listing costs its pages and nothing more
# ═══════════════════════════════════════════════════════════════════════════
#
# Measured on the author's account on 2026-10-14: 624 playlists cost 637
# requests, 13 pages and 624 single fetches, because the client's playlist
# parser ends in ``Playlist.factory``, which rebuilds every playlist the account
# created as a ``UserPlaylist``, and that constructor fetches it again. The
# tests below drive the REAL client over a transport that counts every request
# by path, since a method level fake cannot make the fetch the defect is.

OWNER = 42


class _Sent:
    def __init__(self, url: str) -> None:
        self.url = url


class _Response:
    """What ``requests`` hands the client back, as far as the client reads it."""

    def __init__(self, url: str, body: dict) -> None:
        self.request = _Sent(url)
        self.status_code = 200
        self.ok = True
        self.headers = {"etag": '"1"'}
        self.text = ""
        self._body = body

    def json(self) -> dict:
        return self._body

    def raise_for_status(self) -> None:
        return None


def _owned_playlist(index: int, owner: int = OWNER) -> dict:
    """One playlist's data as the provider serves it, created by ``owner``."""
    return {
        "uuid": f"pl{index}",
        "title": f"List {index:03d}",
        "type": "USER",
        "numberOfTracks": index % 7,
        "numberOfVideos": 0,
        "description": "",
        "duration": 0,
        "image": None,
        "squareImage": None,
        "promotedArtists": [],
        "creator": {"id": owner},
    }


class CountingTransport:
    """The HTTP session under a real client, counting every request by path.

    Serves the account playlist endpoint by offset, the folder endpoint by
    cursor, one playlist by identifier, and a playlist's tracks, empty. The
    single playlist read is served rather than refused so the client's own
    listing method can be watched making it (the paired test below).
    """

    def __init__(self, playlists: list[dict], *, page: int = 50) -> None:
        self.playlists = playlists
        self.page = page
        self.paths: dict[str, int] = {}

    def request(self, method: str, url: str, params: dict | None = None, **_: object):
        from urllib.parse import urlsplit

        path = urlsplit(url).path
        self.paths[path] = self.paths.get(path, 0) + 1
        params = params or {}
        if path.endswith("/playlistsAndFavoritePlaylists"):
            start = int(params.get("offset") or 0)
            window = self.playlists[start : start + min(int(params["limit"]), self.page)]
            items = [{"created": "2026-01-01T00:00:00Z", "playlist": dict(p)} for p in window]
            return _Response(url, {"items": items, "totalNumberOfItems": len(self.playlists)})
        if path.endswith("/my-collection/playlists/folders"):
            start = int(params.get("cursor") or 0)
            window = self.playlists[start : start + min(int(params["limit"]), self.page)]
            body: dict = {
                "items": [
                    {"itemType": "PLAYLIST", "trn": f"trn:playlist:{p['uuid']}", "data": dict(p)}
                    for p in window
                ],
                "totalNumberOfItems": len(self.playlists),
            }
            if start + len(window) < len(self.playlists):
                body["cursor"] = str(start + len(window))
            return _Response(url, body)
        if path.endswith("/tracks"):
            return _Response(url, {"items": [], "totalNumberOfItems": 0})
        if "/playlists/" in path:
            wanted = path.rsplit("/", 1)[-1]
            return _Response(url, next(p for p in self.playlists if p["uuid"] == wanted))
        raise AssertionError(f"the transport serves no {path}")

    def single_fetches(self) -> int:
        """Requests for one playlist by identifier, the cost R-1016 removes."""
        return sum(
            count
            for path, count in self.paths.items()
            if path.startswith("/v1/playlists/") and not path.endswith("/tracks")
        )


def _logged_in_over(transport: CountingTransport):
    """A real client, logged in as ``OWNER``, whose HTTP session is the transport."""
    tidalapi = pytest.importorskip("tidalapi")
    session = tidalapi.Session()
    session.request_session = transport
    session.user = tidalapi.user.LoggedInUser(session, OWNER)
    return session


def test_an_account_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch():
    """The brief's first scenario: N playlists over P pages make P requests."""
    held = [_owned_playlist(n) for n in range(130)]
    transport = CountingTransport(held)
    found = listing.account_playlists(_logged_in_over(transport), sleep=lambda _: None)

    assert [p.id for p in found] == [p["uuid"] for p in held]
    assert transport.single_fetches() == 0
    # Three pages of 50 hold the 130, and the empty fourth ends the walk.
    assert transport.paths == {f"/v1/users/{OWNER}/playlistsAndFavoritePlaylists": 4}


def test_the_clients_own_account_listing_fetches_every_owned_playlist_again():
    """The pair to the test above: the mechanism R-1016 measured, on this client.

    If a later client stops making the fetch this goes red, which says the
    listing could return to the client's own method, rather than the walk
    carrying a workaround for a cost that no longer exists unnoticed.
    """
    held = [_owned_playlist(n) for n in range(5)] + [_owned_playlist(5, owner=7)]
    transport = CountingTransport(held)
    _logged_in_over(transport).user.playlist_and_favorite_playlists(limit=50, offset=0)

    assert transport.single_fetches() == 5


def test_a_folder_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch():
    """The brief's second scenario, over the cursor walk."""
    held = [_owned_playlist(n) for n in range(12)]
    transport = CountingTransport(held, page=5)
    session = _logged_in_over(transport)
    handle = session.folder()
    handle.id = "folder-kompakt"
    found = listing.folder_playlists(handle, sleep=lambda _: None)

    assert [p.id for p in found] == [p["uuid"] for p in held]
    assert transport.single_fetches() == 0
    assert transport.paths == {"/v2/my-collection/playlists/folders": 3}


def test_a_listed_playlist_carries_the_fields_the_callers_read():
    """Identifier, name, track count and creator, read off the page alone."""
    transport = CountingTransport([_owned_playlist(3)])
    (playlist,) = listing.account_playlists(_logged_in_over(transport), sleep=lambda _: None)

    assert (playlist.id, playlist.name, playlist.num_tracks) == ("pl3", "List 003", 3)
    assert playlist.creator.id == OWNER
    assert playlist.user_date_added is not None


def test_a_listed_playlist_still_reads_its_tracks_through_the_playlist():
    """The brief's last scenario: the object is the client's, and it pages its tracks."""
    transport = CountingTransport([_owned_playlist(0)])
    (playlist,) = listing.account_playlists(_logged_in_over(transport), sleep=lambda _: None)
    before = dict(transport.paths)

    assert listing.playlist_tracks(playlist, sleep=lambda _: None) == []
    after = {path: n - before.get(path, 0) for path, n in transport.paths.items()}
    assert {path: n for path, n in after.items() if n} == {"/v1/playlists/pl0/tracks": 1}


def test_the_catalogue_and_the_folder_reads_hand_the_plans_what_the_pages_said():
    """The brief's third scenario: the filing and root plans read these two."""
    from cratekit.label import tidal_catalogue
    from cratekit.label.catalogue import AccountPlaylist
    from cratekit.modules.outbound.tidal_account import TidalAccount

    held = [_owned_playlist(n) for n in range(60)] + [_owned_playlist(60, owner=7)]
    transport = CountingTransport(held)
    session = _logged_in_over(transport)

    listed = tidal_catalogue.TidalCatalogue(session).account_playlists()
    assert listed == tuple(
        AccountPlaylist(p["uuid"], p["title"], p["numberOfTracks"]) for p in held[:60]
    )
    inside = TidalAccount(session, sleep=lambda _: None).folder_playlists("folder-kompakt")
    assert inside == {p["uuid"]: p["title"] for p in held}
    assert transport.single_fetches() == 0


def test_a_listing_of_624_playlists_is_paced_in_seconds_not_minutes(tmp_path):
    """The brief's verification, on the transport: the author's 624 at the default pace.

    The real gate, at the configuration's default interval, over a clock that
    moves only when the gate sleeps. Fourteen requests, thirteen pages and the
    empty one, against the 637 the live read made.
    """
    from cratekit.core.provider_gate import Gate, GateSettings

    class Clock:
        def __init__(self) -> None:
            self.now = 1_700_000_000.0

        def __call__(self) -> float:
            return self.now

        def sleep(self, seconds: float) -> None:
            self.now += seconds

    clock = Clock()
    transport = CountingTransport([_owned_playlist(n) for n in range(624)])
    session = _logged_in_over(transport)
    gate = Gate(
        path=tmp_path / "gate.json", lock_path=tmp_path / "gate.lock",
        clock=clock, sleep=clock.sleep,
    )
    assert gate.attach(session)
    start = clock.now
    found = listing.account_playlists(session, sleep=lambda _: None)

    assert len(found) == 624
    assert transport.single_fetches() == 0
    assert gate.calls == 14
    # Paced, so the gate really is under the walk, and at most one interval a
    # call, which at the default of one second is fourteen against 640 live.
    elapsed = clock.now - start
    assert 0 < elapsed <= gate.calls * GateSettings().min_interval_s
    assert elapsed < 60
