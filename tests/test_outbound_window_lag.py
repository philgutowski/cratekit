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

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import pytest

from cratekit.acquire import listing
from cratekit.core.cause import CratekitError
from cratekit.modules.outbound import tidal_account
from tests.test_outbound_order import Provider, _adapter
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414 - fixture


def _window_lagging(members: list[str], lag: int, *, unpaged: int | None = None) -> Provider:
    """A provider whose window read lags each write ``lag`` readings and whose unpaged read does not.

    ``unpaged`` is how many tracks the unpaged read serves, a first page; None serves them all.
    """
    provider = Provider(members, lag=lag)
    provider.window_only = True
    provider.unpaged_size = unpaged
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
        # The unpaged read is a first page the window begins with.
        (["a", "b", "c", "d"], ["a", "b"], 4, listing.WINDOW_AGREES),
        (["a", "b", "c", "d"], [], 4, listing.WINDOW_AGREES),
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
    provider = _window_lagging(["a", "b", "c", "d"], 99, unpaged=2)
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
    provider = _window_lagging(["a", "b", "c", "d"], 1, unpaged=2)
    slept: list[float] = []
    after = _adapter(installed, provider, slept).order_tracks("mine", ("d", "a", "b", "c"))
    assert after == ("d", "a", "b", "c")
    assert len(provider.moves) == 1
    assert slept == [tidal_account.ORDER_PAUSES[0]]


def test_a_first_reading_whose_window_lags_is_read_again_before_any_move(installed):
    provider = _window_lagging(["c", "a", "b", "d"], 0, unpaged=2)
    provider.previous = (["a", "b", "c", "d"], 0)
    provider.lagging = 1
    slept: list[float] = []
    after = _adapter(installed, provider, slept).order_tracks("mine", ("a", "c", "b", "d"))
    assert after == ("a", "c", "b", "d")
    assert slept == [tidal_account.ORDER_PAUSES[0]]


def test_a_first_reading_whose_window_never_catches_up_refuses_with_nothing_moved(installed):
    provider = _window_lagging(["c", "a", "b", "d"], 0, unpaged=2)
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
    # The removal changes the unpaged read's first page, so the two disagree;
    # past it they cannot, and the read back judges the window as ever.
    provider = _window_lagging(["a", "b", "c", "d"], 99, unpaged=1)
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
    provider = _window_lagging(["b", "a", "c"], 0, unpaged=1)
    provider.previous = (["a", "b", "c"], 0)
    provider.lagging = 99
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider).remove_tracks("mine", ("b",))
    assert refused.value.cause.detail["problem"] == "window-lags"
    assert provider.removals == []


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
    provider = _window_lagging(["a", "b", "c", "d"], 1, unpaged=2)
    account = _adapter(installed, provider)
    account.order_tracks("mine", ("d", "a", "b", "c"))
    account.remove_tracks("mine", ("b",))
    assert [(one["after"], one["outcome"]) for one in account.read_backs()] == [
        ("order", "done"),
        ("move", "done"),
        ("removal", "done"),
    ]
    move = account.read_backs()[1]
    assert move["playlist_id"] == "mine"
    assert move["readings"] == 2
    assert move["waited"] == tidal_account.ORDER_PAUSES[0]
    assert move["window_lagged"] == 1


def test_a_refused_read_back_is_recorded_as_refused(installed):
    provider = _window_lagging(["a", "b", "c", "d"], 99, unpaged=2)
    account = _adapter(installed, provider)
    with pytest.raises(CratekitError):
        account.order_tracks("mine", ("d", "a", "b", "c"))
    last = account.read_backs()[-1]
    assert (last["after"], last["outcome"]) == ("move", "refused")
    assert last["readings"] == tidal_account.ORDER_REREADS + 1
    assert last["window_lagged"] == tidal_account.ORDER_REREADS + 1
    assert last["waited"] == sum(tidal_account.ORDER_PAUSES)
