"""U226: an account playlist read after a write reads it as it stands, not the window that lags it.

Sitting 84 measured the client's unpaged read (``playlist.tracks()``) showing a
move at once while the window read (``acquire.listing.playlist_tracks``) lagged
for minutes. Driven against the U220 stand in with ``window_only`` set: an
unpaged read holding the whole playlist is the one judged; an unpaged first page
that disagrees with the window is a lag, read again and then refused. R-1360
walks the unpaged read past a capped first page. D1 applies.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from cratekit.acquire import listing
from cratekit.modules.outbound import tidal_account
from tests.test_outbound_order import Provider, _adapter, _lands, _refused
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414 - fixture
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414 - fixture


def _window_lagging(
    members: list[str], lag: int, *, unpaged: int | None = None, walk_lags: bool = False
) -> Provider:
    """A provider whose window read lags each write ``lag`` readings, its unpaged read not.

    ``unpaged`` is how many tracks the unpaged read serves, a first page; None
    serves a hundred. ``walk_lags`` makes its later pages lag too (R-1360).
    """
    provider = Provider(members, lag=lag)
    provider.window_only = True
    provider.unpaged_size = unpaged
    provider.walk_lags = walk_lags
    return provider


def _moved_by_a_person(now: list[str], before: list[str], lagging: int, **window) -> Provider:
    """``now`` after a person's change, the window serving ``before`` for ``lagging`` readings."""
    provider = _window_lagging(now, 0, **window)
    provider.previous = (before, 0)
    provider.lagging = lagging
    return provider


#: An unpaged read of a two track first page whose later pages lag as the window does.
FIRST_PAGE = {"unpaged": 2, "walk_lags": True}


# ── the judge ───────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("paged", "unpaged", "declared", "judged"),
    [
        (["a", "b"], ["a", "b"], 2, listing.WINDOW_AGREES),
        # A track the account cannot play: both reads leave it out, both agree.
        (["a", "b"], ["a", "b"], 3, listing.WINDOW_AGREES),
        # The window lags a move; the unpaged read is whole.
        (["a", "b", "c"], ["c", "a", "b"], 3, listing.WINDOW_UNPAGED),
        # The window lags a removal; the unpaged read is whole at the new count.
        (["a", "b", "c"], ["a", "c"], 2, listing.WINDOW_UNPAGED),
        # The unpaged read a first part of a window short of the declared count.
        (["a", "b", "c"], ["a", "b"], 4, listing.WINDOW_AGREES),
        (["a", "b", "c"], [], 4, listing.WINDOW_AGREES),
        # R-1360. A first part of a window holding every declared track: the
        # window may lag a change past where the unpaged read reached.
        (["a", "b", "c", "d"], ["a", "b"], 4, listing.WINDOW_LAGS),
        (["a", "b", "c", "d"], [], 4, listing.WINDOW_LAGS),
        (["a", "b", "c", "d", "e"], ["a", "b"], 4, listing.WINDOW_LAGS),
        # A count that is not a count holds nothing to the window.
        (["a", "b", "c", "d"], ["a", "b"], None, listing.WINDOW_AGREES),
        # A first page that differs from the window's first part.
        (["a", "b", "c", "d"], ["d", "a"], 4, listing.WINDOW_LAGS),
        # A whole looking unpaged read beside a count that is not a count.
        (["a", "b", "c"], ["c", "a", "b"], None, listing.WINDOW_LAGS),
        (["a", "b", "c"], ["c", "a", "b"], True, listing.WINDOW_LAGS),
        (["a", "b", "c"], ["c", "a", "b"], -1, listing.WINDOW_LAGS),
        # The unpaged read longer than the window, not whole.
        (["a", "b"], ["a", "b", "c"], 4, listing.WINDOW_LAGS),
    ],
)
def test_the_judge_reads_the_two_reads_against_the_declared_count(paged, unpaged, declared, judged):
    assert listing.judge_window(paged, unpaged, declared) == judged


def test_a_client_that_cannot_read_with_no_window_says_so_at_once():
    """Round one's review: a signature fault is not climbed as a wait."""

    class Playlist:
        def tracks(self, limit, offset):
            return []

    slept: list[float] = []
    with pytest.raises(listing.ListingNotPaginated):
        listing.playlist_tracks_unpaged(Playlist(), sleep=slept.append)
    assert slept == []


def test_the_unpaged_read_asks_the_client_with_no_window():
    asked: list[dict] = []

    class Playlist:
        def tracks(self, **kwargs):
            asked.append(kwargs)
            return ["one"]

    assert listing.playlist_tracks_unpaged(Playlist()) == ["one"]
    assert asked == [{}]


# ── a move ──────────────────────────────────────────────────────────────────


def test_a_move_whose_window_lags_and_unpaged_read_does_not_is_taken_as_done(installed):
    """The measured refusal: every move landed, the window read the old order."""
    provider = _window_lagging(["a", "b", "c", "d"], 99)
    slept: list[float] = []
    _lands(_adapter(installed, provider, slept), ("d", "c", "a", "b"), provider)
    assert len(provider.moves) == 2, "a move was sent twice"
    assert provider.refused == 0
    assert slept == [], "a read back the unpaged read settled was waited on"


def test_each_move_carries_the_tag_the_unpaged_read_came_with(installed):
    """The window lags with its old tag; the move after it is sent with the current one."""
    provider = _window_lagging(["a", "b", "c", "d"], 99)
    _adapter(installed, provider).order_tracks("mine", ("d", "c", "a", "b"))
    assert [tag for _asked, _to, tag in provider.moves] == [1, 2]


def test_an_order_planned_after_a_lagging_window_is_planned_from_the_unpaged_read(installed):
    """A person's move the window has not caught up with: the moves start where tracks stand."""
    provider = _moved_by_a_person(["c", "a", "b"], ["a", "b", "c"], 99)
    _lands(_adapter(installed, provider), ("a", "c", "b"), provider)


def test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves(installed):
    """U231: a window lagging every move no longer stops the order; its settle reading says so."""
    provider = _window_lagging(["a", "b", "c", "d"], 99, unpaged=2, walk_lags=True)
    slept: list[float] = []
    account = _adapter(installed, provider, slept)
    assert account.order_tracks("mine", ("d", "c", "a", "b")) == ("d", "c", "a", "b")
    assert len(provider.moves) == 2, "a move was sent twice"
    assert slept == []
    assert account.settled_order("mine") is None
    assert account.read_backs()[-1]["window_lagged"] == 1


def test_a_window_that_catches_up_beside_a_first_page_settles_as_done(installed):
    provider = _window_lagging(["a", "b", "c", "d"], 1, unpaged=2, walk_lags=True)
    account = _adapter(installed, provider)
    assert account.order_tracks("mine", ("d", "a", "b", "c")) == ("d", "a", "b", "c")
    assert len(provider.moves) == 1
    assert account.settled_order("mine") is None, "the first reading after the move lags"
    assert account.settled_order("mine") == ("d", "a", "b", "c")


def test_a_first_reading_whose_window_lags_is_read_again_before_any_move(installed):
    provider = _moved_by_a_person(["c", "a", "b", "d"], ["a", "b", "c", "d"], 1, **FIRST_PAGE)
    slept: list[float] = []
    _lands(_adapter(installed, provider, slept), ("a", "c", "b", "d"))
    assert slept == [tidal_account.ORDER_PAUSES[0]]


def test_a_first_reading_whose_window_never_catches_up_refuses_with_nothing_moved(installed):
    provider = _moved_by_a_person(["c", "a", "b", "d"], ["a", "b", "c", "d"], 99, **FIRST_PAGE)
    account = _adapter(installed, provider)
    cause = _refused(lambda: account.order_tracks("mine", ("a", "c", "b", "d")))
    assert cause.detail["problem"] == "window-lags"
    assert cause.detail["lagged"] == "yes"
    assert "no track was moved" in cause.message
    assert provider.moves == []


# ── a removal ───────────────────────────────────────────────────────────────


def test_a_removal_whose_window_lags_and_unpaged_read_does_not_is_taken_as_done(installed):
    provider = _window_lagging(["a", "b", "c", "d"], 99)
    slept: list[float] = []
    assert _adapter(installed, provider, slept).remove_tracks("mine", ("b",)) == ("b",)
    assert provider.members == ["a", "c", "d"]
    assert provider.removals == [(1,)], "a removal was sent twice"
    assert slept == []


def test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound(installed):
    # The removal changes the unpaged read's first page, so the two disagree,
    # and the walk past it lags as the window does, so it is never whole.
    provider = _window_lagging(["a", "b", "c", "d"], 99, unpaged=2, walk_lags=True)
    slept: list[float] = []
    cause = _refused(lambda: _adapter(installed, provider, slept).remove_tracks("mine", ("a",)))
    assert cause.detail["problem"] == "read-back-differs"
    assert cause.detail["lagged"] == "yes"
    assert "may have landed" in cause.message
    assert "unpaged" in cause.message
    assert cause.detail["readings"] == str(tidal_account.ORDER_REREADS + 1)
    assert len(slept) == tidal_account.ORDER_REREADS
    assert provider.removals == [(0,)], "a removal was sent twice"


def test_a_removal_planned_from_a_lagging_window_takes_the_track_where_it_stands(installed):
    """A person's move the window has not caught up with: the position is the unpaged read's."""
    provider = _moved_by_a_person(["b", "a", "c"], ["a", "b", "c"], 99)
    assert _adapter(installed, provider).remove_tracks("mine", ("b",)) == ("b",)
    assert provider.removals == [(0,)]
    assert provider.members == ["a", "c"]


def test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing(installed):
    provider = _moved_by_a_person(["b", "a", "c"], ["a", "b", "c"], 99, **FIRST_PAGE)
    slept: list[float] = []
    cause = _refused(lambda: _adapter(installed, provider, slept).remove_tracks("mine", ("b",)))
    assert cause.detail["problem"] == "window-lags"
    assert cause.detail["readings"] == str(tidal_account.ORDER_REREADS + 1)
    assert "nothing was taken off it" in cause.message
    assert len(slept) == tidal_account.ORDER_REREADS
    assert provider.removals == []


def test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands(installed):
    """Round one's review: a lag at the positions read pauses rather than stopping the write."""
    provider = _moved_by_a_person(["b", "a", "c"], ["a", "b", "c"], 1, **FIRST_PAGE)
    slept: list[float] = []
    assert _adapter(installed, provider, slept).remove_tracks("mine", ("b",)) == ("b",)
    assert provider.removals == [(0,)]
    assert provider.members == ["a", "c"]
    assert slept == [tidal_account.ORDER_PAUSES[0]]


def test_a_window_short_of_the_declared_total_still_refuses_with_nothing_sent(installed):
    provider = _window_lagging(["a", "b", "c"], 0)
    provider.declared = 4
    cause = _refused(lambda: _adapter(installed, provider).remove_tracks("mine", ("b",)))
    assert cause.detail["problem"] == "positions-unknown"
    assert provider.removals == []


# ── the measurement ─────────────────────────────────────────────────────────


def test_every_judged_reading_records_its_readings_and_wait(installed):
    provider = _window_lagging(["a", "b", "c", "d"], 1, unpaged=2, walk_lags=True)
    account = _adapter(installed, provider)
    account.order_tracks("mine", ("d", "a", "b", "c"))
    assert account.settled_order("mine", wait=3.0) is None
    account.remove_tracks("mine", ("b",))
    assert [(one["after"], one["outcome"]) for one in account.read_backs()] == [
        ("order", "done"),
        ("moves", "done"),
        ("settle", "lags"),
        ("removal positions", "done"),
        ("removal", "done"),
    ]
    moves, settle = account.read_backs()[1:3]
    assert (moves["playlist_id"], moves["moved"], moves["stale"]) == ("mine", 1, 0)
    assert (settle["readings"], settle["waited"], settle["window_lagged"]) == (1, 3.0, 1)


def test_the_pause_after_a_412_is_counted_in_the_moves_record(installed):
    """Round two's review of U226: the one pause outside every record is now in one."""
    slept: list[float] = []
    account = _adapter(installed, Provider(["a", "b", "c"], stale_tags=1), slept)
    account.order_tracks("mine", ("c", "a", "b"))
    assert slept == [tidal_account.ORDER_PAUSES[0]]
    assert sum(one["waited"] for one in account.read_backs()) == sum(slept)
    assert [one["after"] for one in account.read_backs()] == ["order", "moves"]
    assert account.read_backs()[1]["stale"] == 1


# ── R-1360: past the unpaged read's first page ──────────────────────────────
# The client's unpaged read is most likely capped at the provider's page of a
# hundred, so it walks on past its first page, and a first part read beside a
# whole window is a lag.

CAP = listing.PAGE_SIZES["playlist_tracks"]


class Capped:
    """A playlist in the client's shape, its unpaged read capped at ``cap``, every request kept."""

    def __init__(self, members: list[str], cap: int = CAP, *, declared: object = "len") -> None:
        self.members = list(members)
        self.cap = cap
        self.num_tracks = len(members) if declared == "len" else declared
        self._etag = 7
        self.asked: list[dict] = []

    def tracks(self, **kwargs) -> list[SimpleNamespace]:
        self.asked.append(kwargs)
        offset = kwargs.get("offset", 0)
        return [SimpleNamespace(id=one) for one in self.served(offset)[offset : offset + self.cap]]

    def served(self, offset: int) -> list[str]:
        return self.members


def _long(count: int) -> list[str]:
    return [f"t{index:03d}" for index in range(count)]


def _unpaged(playlist: Capped, **kwargs) -> list[str]:
    return [listing.row_id(row) for row in listing.playlist_tracks_unpaged(playlist, **kwargs)]


def test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back():
    playlist = Capped(_long(250))
    assert _unpaged(playlist) == _long(250)
    assert playlist.asked == [{}, {"offset": CAP - 1}, {"offset": 2 * CAP - 2}]


@pytest.mark.parametrize("count", [0, 1, CAP - 1, CAP])
def test_a_playlist_its_first_read_holds_whole_is_read_once(count):
    playlist = Capped(_long(count))
    assert _unpaged(playlist) == _long(count)
    assert playlist.asked == [{}]


@pytest.mark.parametrize("declared", [None, True, -1, "150"])
def test_a_playlist_declaring_no_count_is_read_once(declared):
    playlist = Capped(_long(150), declared=declared)
    assert _unpaged(playlist) == _long(CAP)
    assert playlist.asked == [{}]


def test_a_cap_of_one_track_is_read_once_rather_than_walked_forever():
    playlist = Capped(_long(5), cap=1)
    assert _unpaged(playlist) == ["t000"]
    assert playlist.asked == [{}]


def test_a_page_that_does_not_start_where_the_last_ended_ends_the_walk_before_it():
    """A track the account cannot play, or a change between requests, shifts later positions."""

    class Shifted(Capped):
        def served(self, offset):
            return self.members if not offset else self.members[1:]

    playlist = Shifted(_long(250))
    assert _unpaged(playlist) == _long(CAP)
    assert len(playlist.asked) == 2


def test_a_page_carrying_another_version_tag_ends_the_walk_before_it():
    """A later page served from before a write carries the tag it had then."""

    class Stale(Capped):
        def tracks(self, **kwargs):
            if kwargs.get("offset"):
                self._etag = 6
            return super().tracks(**kwargs)

    playlist = Stale(_long(250))
    assert _unpaged(playlist) == _long(CAP)
    assert len(playlist.asked) == 2


def test_a_page_longer_than_the_first_ends_the_walk_before_it():
    class Growing(Capped):
        def tracks(self, **kwargs):
            if kwargs.get("offset"):
                self.cap = CAP + 1
            return super().tracks(**kwargs)

    assert _unpaged(Growing(_long(250))) == _long(CAP)


def test_an_empty_later_page_ends_the_walk():
    class Ends(Capped):
        def served(self, offset):
            return self.members if not offset else []

    playlist = Ends(_long(250))
    assert _unpaged(playlist) == _long(CAP)
    assert len(playlist.asked) == 2


def test_a_short_later_page_is_the_last_one_asked_for():
    """A count that declares more than the provider serves stops at the first short page."""
    playlist = Capped(_long(150), declared=400)
    assert _unpaged(playlist) == _long(150)
    assert len(playlist.asked) == 2


def test_the_walk_stops_once_it_holds_the_declared_count():
    playlist = Capped(_long(400), declared=150)
    assert len(listing.playlist_tracks_unpaged(playlist)) == 2 * CAP - 1
    assert len(playlist.asked) == 2


def test_each_later_page_goes_through_the_retry_ladder():
    class Flaky(Capped):
        failed = False

        def tracks(self, **kwargs):
            if kwargs.get("offset") and not self.failed:
                self.failed = True
                raise ConnectionError("reset")
            return super().tracks(**kwargs)

    slept: list[float] = []
    assert _unpaged(Flaky(_long(150)), sleep=slept.append) == _long(150)
    assert len(slept) == 1


def _long_lagging(*, walk_lags: bool = False) -> Provider:
    """150 tracks, the unpaged read capped at 100, the window serving the order before a
    person put the last track at position 120."""
    old = _long(150)
    moved = list(old)
    moved.insert(120, moved.pop())
    return _moved_by_a_person(moved, old, 99, unpaged=CAP, walk_lags=walk_lags)


def _t130_first(provider: Provider) -> tuple[str, ...]:
    return ("t130", *[one for one in provider.members if one != "t130"])


def test_an_order_past_the_first_hundred_moves_the_track_where_it_stands(installed):
    """On main the stale window put t130 at 130, where t129 stands: the wrong track was moved."""
    provider = _long_lagging()
    asked = _t130_first(provider)
    _lands(_adapter(installed, provider), asked, provider)
    assert [indices for indices, _to, _tag in provider.moves] == [(131,)]


def test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands(installed):
    provider = _long_lagging()
    assert _adapter(installed, provider).remove_tracks("mine", ("t130",)) == ("t130",)
    assert provider.removals == [(131,)], "a track was taken off by its stale position"
    assert "t130" not in provider.members and "t129" in provider.members


def test_an_order_whose_later_pages_lag_too_is_held_with_nothing_moved(installed):
    provider = _long_lagging(walk_lags=True)
    slept: list[float] = []
    account = _adapter(installed, provider, slept)
    cause = _refused(lambda: account.order_tracks("mine", _t130_first(provider)))
    assert cause.detail["problem"] == "window-lags"
    assert provider.moves == []
    assert len(slept) == tidal_account.ORDER_REREADS


def test_a_removal_whose_later_pages_lag_too_is_held_with_nothing_taken_off(installed):
    provider = _long_lagging(walk_lags=True)
    cause = _refused(lambda: _adapter(installed, provider).remove_tracks("mine", ("t130",)))
    assert cause.detail["problem"] == "window-lags"
    assert provider.removals == []


def test_a_long_playlist_nothing_changed_is_read_whole_and_written_once(installed):
    """Past the cap with no lag: the walk agrees with the window and the order lands."""
    provider = Provider(_long(150))
    provider.unpaged_size = CAP
    asked = ("t140", *[one for one in _long(150) if one != "t140"])
    assert _adapter(installed, provider).order_tracks("mine", asked) == asked
    assert [indices for indices, _to, _tag in provider.moves] == [(140,)]
