"""U226: an account playlist read after a write reads it as it stands, not the window that lags it.

Sitting 84 measured on the live account that after a move the client's
unpaged read (``playlist.tracks()`` with no window) returned the new order at
once, while the window read every listing in the product walks
(``acquire.listing.playlist_tracks``) returned the old order, and sometimes
the new, for at least thirteen minutes. ``order_tracks`` refused a move that
had landed as "still read as it was before the move after 4 readings".

These tests drive the account adapter against the U220 stand in for the
provider's client with ``window_only`` set: a read with a window lags each
write, the unpaged read does not. The read the adapter judges is the unpaged
one when it holds the whole playlist, so the move and the removal are taken
as done with nothing sent twice; when the unpaged read is a first page only
and disagrees with the window, it is a lag, read again and then refused.

R-1360: the unpaged read is walked past a capped first page, so a playlist
longer than the cap is judged by the read the provider serves current too;
``walk_lags`` makes the walk's later pages lag as the window does, so the
first page alone is current, which is how the tests above keep a lag.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from cratekit.acquire import listing
from cratekit.core.cause import CratekitError
from cratekit.modules.outbound import tidal_account
from tests.test_outbound_order import Provider, _adapter
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414 - fixture


def _window_lagging(
    members: list[str], lag: int, *, unpaged: int | None = None, walk_lags: bool = False
) -> Provider:
    """A provider whose window read lags each write ``lag`` readings and whose unpaged read does not.

    ``unpaged`` is how many tracks the unpaged read serves, a first page; None
    serves a hundred. ``walk_lags`` makes its later pages lag as the window
    does (R-1360), so a read past its first page cannot be taken whole.
    """
    provider = Provider(members, lag=lag)
    provider.window_only = True
    provider.unpaged_size = unpaged
    provider.walk_lags = walk_lags
    return provider


# ═══════════════════════════════════════════════════════════════════════════
# The judge
# ═══════════════════════════════════════════════════════════════════════════


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
        # The unpaged read a first part of a window short of the declared
        # count, a track the account cannot play left out of both.
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


# ═══════════════════════════════════════════════════════════════════════════
# A move
# ═══════════════════════════════════════════════════════════════════════════


def test_a_move_whose_window_lags_and_unpaged_read_does_not_is_taken_as_done(installed):
    """The measured refusal: every move landed, the window read the old order."""
    provider = _window_lagging(["a", "b", "c", "d"], 99)
    slept: list[float] = []
    account = _adapter(installed, provider, slept)
    after = account.order_tracks("mine", ("d", "c", "a", "b"))
    assert after == ("d", "c", "a", "b")
    assert provider.members == ["d", "c", "a", "b"]
    assert len(provider.moves) == 2, "a move was sent twice"
    assert provider.refused == 0
    assert slept == [], "a read back the unpaged read settled was waited on"


def test_each_move_carries_the_tag_the_unpaged_read_came_with(installed):
    """The window lags with its old tag; the move after it is sent with the current one."""
    provider = _window_lagging(["a", "b", "c", "d"], 99)
    _adapter(installed, provider).order_tracks("mine", ("d", "c", "a", "b"))
    assert [tag for _asked, _to, tag in provider.moves] == [1, 2]


def test_an_order_planned_after_a_lagging_window_is_planned_from_the_unpaged_read(installed):
    """A person's move the window has not caught up with: the moves start from where tracks stand."""
    provider = _window_lagging(["c", "a", "b"], 0)
    provider.previous = (["a", "b", "c"], 0)
    provider.lagging = 99
    after = _adapter(installed, provider).order_tracks("mine", ("a", "c", "b"))
    assert after == ("a", "c", "b")
    assert provider.members == ["a", "c", "b"]


def test_a_window_that_lags_beside_a_first_page_unpaged_read_refuses_saying_so(installed):
    provider = _window_lagging(["a", "b", "c", "d"], 99, unpaged=2, walk_lags=True)
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).order_tracks("mine", ("d", "c", "a", "b"))
    cause = refused.value.cause
    assert cause.reason == "outbound-remove-refused"
    assert cause.detail["problem"] == "read-back-differs"
    assert cause.detail["lagged"] == "yes"
    assert cause.detail["readings"] == str(tidal_account.ORDER_REREADS + 1)
    assert cause.detail["waited"] == f"{sum(tidal_account.ORDER_PAUSES):g}"
    assert "unpaged" in cause.message
    assert f"after {tidal_account.ORDER_REREADS + 1} readings" in cause.message
    assert len(provider.moves) == 1, "a move was sent twice"
    assert len(slept) == tidal_account.ORDER_REREADS


def test_a_window_that_catches_up_beside_a_first_page_is_taken_as_done(installed):
    provider = _window_lagging(["a", "b", "c", "d"], 1, unpaged=2, walk_lags=True)
    slept: list[float] = []
    after = _adapter(installed, provider, slept).order_tracks("mine", ("d", "a", "b", "c"))
    assert after == ("d", "a", "b", "c")
    assert len(provider.moves) == 1
    assert slept == [tidal_account.ORDER_PAUSES[0]]


def test_a_first_reading_whose_window_lags_is_read_again_before_any_move(installed):
    provider = _window_lagging(["c", "a", "b", "d"], 0, unpaged=2, walk_lags=True)
    provider.previous = (["a", "b", "c", "d"], 0)
    provider.lagging = 1
    slept: list[float] = []
    after = _adapter(installed, provider, slept).order_tracks("mine", ("a", "c", "b", "d"))
    assert after == ("a", "c", "b", "d")
    assert slept == [tidal_account.ORDER_PAUSES[0]]


def test_a_first_reading_whose_window_never_catches_up_refuses_with_nothing_moved(installed):
    provider = _window_lagging(["c", "a", "b", "d"], 0, unpaged=2, walk_lags=True)
    provider.previous = (["a", "b", "c", "d"], 0)
    provider.lagging = 99
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider).order_tracks("mine", ("a", "c", "b", "d"))
    cause = refused.value.cause
    assert cause.detail["problem"] == "window-lags"
    assert cause.detail["lagged"] == "yes"
    assert "no track was moved" in cause.message
    assert provider.moves == []


# ═══════════════════════════════════════════════════════════════════════════
# A removal
# ═══════════════════════════════════════════════════════════════════════════


def test_a_removal_whose_window_lags_and_unpaged_read_does_not_is_taken_as_done(installed):
    provider = _window_lagging(["a", "b", "c", "d"], 99)
    slept: list[float] = []
    gone = _adapter(installed, provider, slept).remove_tracks("mine", ("b",))
    assert gone == ("b",)
    assert provider.members == ["a", "c", "d"]
    assert provider.removals == [(1,)], "a removal was sent twice"
    assert slept == []


def test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound(installed):
    # The removal changes the unpaged read's first page, so the two disagree,
    # and the walk past it lags as the window does, so it is never whole.
    provider = _window_lagging(["a", "b", "c", "d"], 99, unpaged=2, walk_lags=True)
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).remove_tracks("mine", ("a",))
    cause = refused.value.cause
    assert cause.detail["problem"] == "read-back-differs"
    assert cause.detail["lagged"] == "yes"
    assert "may have landed" in cause.message
    assert "unpaged" in cause.message
    assert cause.detail["readings"] == str(tidal_account.ORDER_REREADS + 1)
    assert len(slept) == tidal_account.ORDER_REREADS
    assert provider.removals == [(0,)], "a removal was sent twice"


def test_a_removal_planned_from_a_lagging_window_takes_the_track_where_it_stands(installed):
    """A person's move the window has not caught up with: the position is the unpaged read's."""
    provider = _window_lagging(["b", "a", "c"], 0)
    provider.previous = (["a", "b", "c"], 0)
    provider.lagging = 99
    gone = _adapter(installed, provider).remove_tracks("mine", ("b",))
    assert gone == ("b",)
    assert provider.removals == [(0,)]
    assert provider.members == ["a", "c"]


def test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing(installed):
    provider = _window_lagging(["b", "a", "c"], 0, unpaged=2, walk_lags=True)
    provider.previous = (["a", "b", "c"], 0)
    provider.lagging = 99
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).remove_tracks("mine", ("b",))
    cause = refused.value.cause
    assert cause.detail["problem"] == "window-lags"
    assert cause.detail["readings"] == str(tidal_account.ORDER_REREADS + 1)
    assert "nothing was taken off it" in cause.message
    assert len(slept) == tidal_account.ORDER_REREADS
    assert provider.removals == []


def test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands(installed):
    """Round one's review: a lag at the positions read pauses rather than stopping the write."""
    provider = _window_lagging(["b", "a", "c"], 0, unpaged=2, walk_lags=True)
    provider.previous = (["a", "b", "c"], 0)
    provider.lagging = 1
    slept: list[float] = []
    gone = _adapter(installed, provider, slept).remove_tracks("mine", ("b",))
    assert gone == ("b",)
    assert provider.removals == [(0,)]
    assert provider.members == ["a", "c"]
    assert slept == [tidal_account.ORDER_PAUSES[0]]


# ═══════════════════════════════════════════════════════════════════════════
# The declared total rule stands
# ═══════════════════════════════════════════════════════════════════════════


def test_a_window_short_of_the_declared_total_still_refuses_with_nothing_sent(installed):
    provider = _window_lagging(["a", "b", "c"], 0)
    provider.declared = 4
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider).remove_tracks("mine", ("b",))
    assert refused.value.cause.detail["problem"] == "positions-unknown"
    assert provider.removals == []


# ═══════════════════════════════════════════════════════════════════════════
# The measurement
# ═══════════════════════════════════════════════════════════════════════════


def test_every_read_back_records_its_readings_and_wait(installed):
    provider = _window_lagging(["a", "b", "c", "d"], 1, unpaged=2, walk_lags=True)
    account = _adapter(installed, provider)
    account.order_tracks("mine", ("d", "a", "b", "c"))
    account.remove_tracks("mine", ("b",))
    assert [(one["after"], one["outcome"]) for one in account.read_backs()] == [
        ("order", "done"),
        ("move", "done"),
        ("removal positions", "done"),
        ("removal", "done"),
    ]
    move = account.read_backs()[1]
    assert move["playlist_id"] == "mine"
    assert move["readings"] == 2
    assert move["waited"] == tidal_account.ORDER_PAUSES[0]
    assert move["window_lagged"] == 1


def test_a_refused_read_back_is_recorded_as_refused(installed):
    provider = _window_lagging(["a", "b", "c", "d"], 99, unpaged=2, walk_lags=True)
    account = _adapter(installed, provider)
    with pytest.raises(CratekitError):
        account.order_tracks("mine", ("d", "a", "b", "c"))
    last = account.read_backs()[-1]
    assert (last["after"], last["outcome"]) == ("move", "refused")
    assert last["readings"] == tidal_account.ORDER_REREADS + 1
    assert last["window_lagged"] == tidal_account.ORDER_REREADS + 1
    assert last["waited"] == sum(tidal_account.ORDER_PAUSES)


def test_the_pause_after_a_412_is_counted_in_the_readings_record(installed):
    """Round two's review: the one pause outside every record is now in one."""
    provider = Provider(["a", "b", "c"], stale_tags=1)
    slept: list[float] = []
    account = _adapter(installed, provider, slept)
    account.order_tracks("mine", ("c", "a", "b"))
    assert slept == [tidal_account.ORDER_PAUSES[0]]
    assert sum(one["waited"] for one in account.read_backs()) == sum(slept)
    assert [one["after"] for one in account.read_backs()][:2] == ["order", "order"]


# ═══════════════════════════════════════════════════════════════════════════
# R-1360: past the unpaged read's first page
# ═══════════════════════════════════════════════════════════════════════════
#
# U226 judged a playlist by its unpaged read beside the window, but the
# client's unpaged read is most likely capped at the provider's page of a
# hundred, and a first page the window began with agreed with it, so a change
# past the first hundred the window lagged was planned from and written at a
# stale position. The unpaged read now walks on past its first page, and a
# first part read beside a whole window is a lag.

CAP = listing.PAGE_SIZES["playlist_tracks"]


class Capped:
    """A playlist read through the client's shape, its unpaged read capped at ``cap``: every request recorded."""

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


def _ids(rows) -> list[str]:
    return [listing.row_id(row) for row in rows]


def test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back():
    playlist = Capped(_long(250))
    assert _ids(listing.playlist_tracks_unpaged(playlist)) == _long(250)
    assert playlist.asked == [{}, {"offset": CAP - 1}, {"offset": 2 * CAP - 2}]


@pytest.mark.parametrize("count", [0, 1, CAP - 1, CAP])
def test_a_playlist_its_first_read_holds_whole_is_read_once(count):
    playlist = Capped(_long(count))
    assert _ids(listing.playlist_tracks_unpaged(playlist)) == _long(count)
    assert playlist.asked == [{}]


@pytest.mark.parametrize("declared", [None, True, -1, "150"])
def test_a_playlist_declaring_no_count_is_read_once(declared):
    playlist = Capped(_long(150), declared=declared)
    assert _ids(listing.playlist_tracks_unpaged(playlist)) == _long(CAP)
    assert playlist.asked == [{}]


def test_a_cap_of_one_track_is_read_once_rather_than_walked_forever():
    playlist = Capped(_long(5), cap=1)
    assert _ids(listing.playlist_tracks_unpaged(playlist)) == ["t000"]
    assert playlist.asked == [{}]


def test_a_page_that_does_not_start_where_the_last_ended_ends_the_walk_before_it():
    """A track the account cannot play, or a change between two requests, shifts every later position."""

    class Shifted(Capped):
        def served(self, offset):
            return self.members if not offset else self.members[1:]

    playlist = Shifted(_long(250))
    assert _ids(listing.playlist_tracks_unpaged(playlist)) == _long(CAP)
    assert len(playlist.asked) == 2


def test_a_page_carrying_another_version_tag_ends_the_walk_before_it():
    """A later page served from before a write carries the tag it had then, even where its tracks line up."""

    class Stale(Capped):
        def tracks(self, **kwargs):
            if kwargs.get("offset"):
                self._etag = 6
            return super().tracks(**kwargs)

    playlist = Stale(_long(250))
    assert _ids(listing.playlist_tracks_unpaged(playlist)) == _long(CAP)
    assert len(playlist.asked) == 2


def test_a_page_longer_than_the_first_ends_the_walk_before_it():
    class Growing(Capped):
        def tracks(self, **kwargs):
            if kwargs.get("offset"):
                self.cap = CAP + 1
            return super().tracks(**kwargs)

    playlist = Growing(_long(250))
    assert _ids(listing.playlist_tracks_unpaged(playlist)) == _long(CAP)


def test_an_empty_later_page_ends_the_walk():
    class Ends(Capped):
        def served(self, offset):
            return self.members if not offset else []

    playlist = Ends(_long(250))
    assert _ids(listing.playlist_tracks_unpaged(playlist)) == _long(CAP)
    assert len(playlist.asked) == 2


def test_a_short_later_page_is_the_last_one_asked_for():
    """A count that declares more than the provider serves stops at the first short page."""
    playlist = Capped(_long(150), declared=400)
    assert _ids(listing.playlist_tracks_unpaged(playlist)) == _long(150)
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
    playlist = Flaky(_long(150))
    assert _ids(listing.playlist_tracks_unpaged(playlist, sleep=slept.append)) == _long(150)
    assert len(slept) == 1


def _tail_moved(old: list[str]) -> list[str]:
    """A person's move past the first hundred: the last track put at position 120."""
    moved = list(old)
    moved.insert(120, moved.pop())
    return moved


def _long_lagging(*, walk_lags: bool = False) -> tuple[Provider, list[str]]:
    """A hundred and fifty tracks, the unpaged read capped at a hundred, the window serving the order before a person's move past them."""
    old = _long(150)
    provider = _window_lagging(_tail_moved(old), 0, unpaged=CAP, walk_lags=walk_lags)
    provider.previous = (old, 0)
    provider.lagging = 99
    return provider, old


def test_an_order_past_the_first_hundred_moves_the_track_where_it_stands(installed):
    """On main the stale window put t130 at 130, where t129 stands: the wrong track was moved."""
    provider, _old = _long_lagging()
    asked = ("t130", *[one for one in provider.members if one != "t130"])
    after = _adapter(installed, provider).order_tracks("mine", asked)
    assert after == asked
    assert provider.members == list(asked)
    assert [indices for indices, _to, _tag in provider.moves] == [(131,)]


def test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands(installed):
    provider, _old = _long_lagging()
    gone = _adapter(installed, provider).remove_tracks("mine", ("t130",))
    assert gone == ("t130",)
    assert provider.removals == [(131,)], "a track was taken off by its stale position"
    assert "t130" not in provider.members and "t129" in provider.members


def test_an_order_whose_later_pages_lag_too_is_held_with_nothing_moved(installed):
    provider, _old = _long_lagging(walk_lags=True)
    asked = ("t130", *[one for one in provider.members if one != "t130"])
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).order_tracks("mine", asked)
    assert refused.value.cause.detail["problem"] == "window-lags"
    assert provider.moves == []
    assert len(slept) == tidal_account.ORDER_REREADS


def test_a_removal_whose_later_pages_lag_too_is_held_with_nothing_taken_off(installed):
    provider, _old = _long_lagging(walk_lags=True)
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider).remove_tracks("mine", ("t130",))
    assert refused.value.cause.detail["problem"] == "window-lags"
    assert provider.removals == []


def test_a_long_playlist_nothing_changed_is_read_whole_and_written_once(installed):
    """Past the cap with no lag: the walk agrees with the window and the order lands."""
    provider = Provider(_long(150))
    provider.unpaged_size = CAP
    asked = ("t140", *[one for one in _long(150) if one != "t140"])
    after = _adapter(installed, provider).order_tracks("mine", asked)
    assert after == asked
    assert [indices for indices, _to, _tag in provider.moves] == [(140,)]
