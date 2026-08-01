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

    ``unpaginated_cap`` is the interesting part: called with no arguments it
    returns only the first page, exactly as the real client does. That is what
    lets a test assert the truncation is real rather than hypothetical.
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


def test_paging_stops_on_a_short_page_rather_than_on_an_empty_one():
    """One saved round trip per listing, and the reason the page size matters."""
    playlist = Paged(corpus(150), 100)
    listing.playlist_tracks(playlist)
    assert playlist.calls == [(100, 0), (100, 100)]


def test_an_exact_multiple_of_the_page_size_needs_the_empty_page():
    """The one case where stopping on short cannot help, asserted so it is known."""
    playlist = Paged(corpus(200), 100)
    got = listing.playlist_tracks(playlist)
    assert len(got) == 200
    assert playlist.calls == [(100, 0), (100, 100), (100, 200)]


def test_an_empty_listing_reads_as_empty_and_not_as_an_error():
    assert listing.playlist_tracks(Paged([], 100)) == []


def test_a_runaway_offset_cannot_loop_forever():
    """A provider that ignores the offset otherwise turns a read into a hang.

    This is not hypothetical tidiness: a full page every time is exactly what a
    broken or renamed offset parameter produces, and the loop's stop condition is
    "a page shorter than the page size", which never arrives.
    """

    def ignores_the_offset(limit: int, offset: int) -> list:
        return corpus(limit)

    assert len(listing.paginate(ignores_the_offset, page_size=100, max_pages=3)) == 300


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


class User:
    def __init__(self, favorites=None, playlists: list[list[Item]] | None = None) -> None:
        self.favorites = favorites
        self._playlists = playlists or []

    def playlist_and_favorite_playlists(self, limit: int | None = None, offset: int = 0) -> list:
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
        def get_albums(self, limit: int | None = None, offset: int = 0) -> list:
            return corpus(2, prefix="a")

    assert len(listing.artist_releases(OnlyAlbums())) == 2


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


def test_the_guard_catches_a_hand_written_pagination_loop():
    source = (
        "def read(playlist):\n"
        "    out = []\n"
        "    offset = 0\n"
        "    while True:\n"
        "        page = playlist.tracks(limit=100, offset=offset)\n"
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
    and a wrapper with no page size is a wrapper guessing.
    """
    assert set(listing.WRAPPERS) == set(listing.PAGE_SIZES)
    for name, wrapper in listing.WRAPPERS.items():
        assert callable(wrapper), name
