"""R-1308: a removal from an account playlist whose read lags the removal is taken as done.

U220 measured on Sitting 62 that the provider's read of a playlist can lag a
write it accepted, and taught ``order_tracks`` to read again after a pause.
``remove_tracks`` read its removal back once and refused at once, so a
removal that landed was refused either as "nothing was taken off it" (the
declared count current, the tracks lagging) or as "a track other than the
asked ones may have come off" (both lagging).

These tests drive ``remove_tracks`` against the U220 stand in for the
provider's client, whose read can lag a write in its tracks, its declared
count, or both. Each reading of the read back is judged on its two halves:
each must be the playlist before the removal or after it. Both after is done;
either still before is a lag, read again after a pause, bounded; anything else
refuses at once. Nothing is ever sent again.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import pytest

from cratekit.core.cause import CratekitError
from cratekit.modules.outbound import tidal_account
from tests.test_outbound_order import Client, Movable, Provider, Stale, _adapter
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414 - fixture

#: The three ways a read can lag a write: the tracks alone, the declared count
#: alone, and both.
LAGS = ("tracks", "count", "whole")


def _lagging(members: list[str], lag: int, how: str) -> Provider:
    provider = Provider(members, lag=lag if how != "count" else 0, whole=how == "whole")
    provider.count_lag = lag if how == "count" else 0
    return provider


# ═══════════════════════════════════════════════════════════════════════════
# A read that lags the removal
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("how", LAGS)
def test_a_removal_whose_read_lags_one_write_is_taken_as_done(installed, how):
    provider = _lagging(["a", "b", "c", "d"], 1, how)
    slept: list[float] = []
    gone = _adapter(installed, provider, slept).remove_tracks("mine", ("b",))
    assert gone == ("b",)
    assert provider.members == ["a", "c", "d"]
    assert provider.removals == [(1,)], "a removal was sent twice"
    assert slept == [tidal_account.ORDER_PAUSES[0]], "a lagging read was read again with no pause"


@pytest.mark.parametrize("how", LAGS)
def test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed(installed, how):
    provider = _lagging(["a", "b", "c", "d"], 99, how)
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).remove_tracks("mine", ("b",))
    cause = refused.value.cause
    assert cause.reason == "outbound-remove-refused"
    assert cause.detail["problem"] == "read-back-differs"
    assert cause.detail["lagged"] == "yes"
    assert cause.retryable is False
    assert "may have landed" in cause.message
    assert "may have come off" not in cause.message
    assert len(slept) == tidal_account.ORDER_REREADS
    assert provider.removals == [(1,)], "a removal was sent twice"
    assert provider.members == ["a", "c", "d"]


def test_a_read_that_catches_up_on_the_last_reading_is_taken_as_done(installed):
    provider = _lagging(["a", "b", "c", "d"], tidal_account.ORDER_REREADS, "whole")
    slept: list[float] = []
    assert _adapter(installed, provider, slept).remove_tracks("mine", ("b",)) == ("b",)
    assert len(slept) == tidal_account.ORDER_REREADS
    assert provider.removals == [(1,)]


def test_the_pauses_are_the_orders_pauses(installed):
    provider = _lagging(["a", "b", "c", "d"], 99, "whole")
    slept: list[float] = []
    with pytest.raises(CratekitError):
        _adapter(installed, provider, slept).remove_tracks("mine", ("b",))
    assert slept == [tidal_account._pause(n) for n in range(1, tidal_account.ORDER_REREADS + 1)]


# ═══════════════════════════════════════════════════════════════════════════
# A reading that is neither before nor after
# ═══════════════════════════════════════════════════════════════════════════


def test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause(installed):
    provider = Provider(["a", "b", "c", "d"])
    provider.wrong = 0
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).remove_tracks("mine", ("b",))
    cause = refused.value.cause
    assert cause.detail["problem"] == "read-back-differs"
    assert cause.detail["lagged"] == "no"
    assert "may have come off" in cause.message
    assert slept == []
    assert provider.removals == [(1,)]


def test_a_wrong_track_behind_a_lagging_count_refuses_at_once(installed):
    """Half before and half neither is not a lag: the tracks show a wrong removal."""
    provider = _lagging(["a", "b", "c", "d"], 99, "count")
    provider.wrong = 0
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).remove_tracks("mine", ("b",))
    assert refused.value.cause.detail["lagged"] == "no"
    assert slept == []


@pytest.mark.parametrize(
    ("declared", "videos"),
    [(7, 0), (2, 0), (None, 0), (True, 0), (3, 1), (3, None)],
    ids=["count-neither", "count-short", "count-none", "count-flag", "a-video", "videos-none"],
)
def test_a_count_that_is_neither_before_nor_after_refuses_at_once(installed, declared, videos):
    """The tracks are after, the count or the videos are something else: refused, no pause."""
    provider = Provider(["a", "b", "c", "d"])
    provider.shown = (declared, videos)
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).remove_tracks("mine", ("b",))
    cause = refused.value.cause
    assert cause.detail["problem"] == "read-back-differs"
    assert cause.detail["lagged"] == "no"
    assert slept == []
    assert len(provider.removals) == 1


def test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound(installed):
    provider = _lagging(["a", "b", "c", "d"], 1, "whole")
    provider.drift = ["a", "d"]
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).remove_tracks("mine", ("b",))
    assert refused.value.cause.detail["lagged"] == "no"
    assert slept == [tidal_account.ORDER_PAUSES[0]]


# ═══════════════════════════════════════════════════════════════════════════
# Nothing is sent again
# ═══════════════════════════════════════════════════════════════════════════


def test_a_removal_that_fails_is_never_resent(installed):
    provider = Provider(["a", "b", "c", "d"])
    provider.remove_fails = [RuntimeError("timed out")]
    with pytest.raises(CratekitError):
        _adapter(installed, provider).remove_tracks("mine", ("b",))
    assert provider.removals == [(1,)]
    assert provider.members == ["a", "b", "c", "d"]


def test_a_removal_answered_412_is_never_resent(installed):
    """A 412 changed nothing; it is raised as any failure is, and nothing is sent again."""
    provider = Provider(["a", "b", "c", "d"], stale_tags=1)
    with pytest.raises(CratekitError):
        _adapter(installed, provider).remove_tracks("mine", ("b",))
    assert len(provider.removals) == 1
    assert provider.members == ["a", "b", "c", "d"]


def test_a_second_chunk_after_a_lagged_first_is_planned_from_the_caught_up_reading(installed):
    members = [f"t{index}" for index in range(tidal_account.REMOVE_CHUNK + 3)]
    provider = _lagging([*members, "keep"], 1, "whole")
    slept: list[float] = []
    gone = _adapter(installed, provider, slept).remove_tracks("mine", tuple(members))
    assert gone == tuple(members)
    assert provider.members == ["keep"]
    assert provider.removals == [tuple(range(tidal_account.REMOVE_CHUNK)), (0, 1, 2)]
    assert len(slept) == 2, "each chunk's read back lagged once"


@pytest.mark.parametrize("how", LAGS)
def test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write(installed, how):
    """``sync pair``'s order of calls on one playlist: what the removal left is what the order expects."""
    provider = _lagging(["a", "b", "c", "d"], 1, how)
    account = _adapter(installed, provider)
    assert account.remove_tracks("mine", ("b",)) == ("b",)
    assert account.add_tracks("mine", ("x",)) == ("x",)
    assert account.order_tracks("mine", ("x", "d", "a", "c")) == ("x", "d", "a", "c")
    assert provider.members == ["x", "d", "a", "c"]
    assert provider.removals == [(1,)]


def test_the_stand_in_answers_the_removal_the_client_offers():
    import tidalapi.playlist

    assert callable(getattr(tidalapi.playlist.UserPlaylist, "remove_by_indices", None))
    assert callable(getattr(Movable, "remove_by_indices", None))
    provider = Provider(["a", "b"])
    playlist = Client(provider).playlist("mine")
    playlist.tracks()
    assert playlist.remove_by_indices([0]) is True
    assert provider.members == ["b"]
    provider.members.append("c")
    provider.version += 1
    with pytest.raises(Stale):
        playlist.remove_by_indices([0])
