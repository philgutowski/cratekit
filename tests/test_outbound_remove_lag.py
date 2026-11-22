"""R-1308: a removal from an account playlist whose read lags the removal is taken as done.

Driven against the U220 stand in, whose read can lag a write in its tracks, its
declared count, or both. Each reading of the read back is judged on those two
halves, each before the removal or after it: both after is done; either still
before is a lag, read again after a pause, bounded; anything else refuses at
once. Nothing is ever sent again. D1 applies.
"""

from __future__ import annotations

import pytest

from cratekit.core.cause import CratekitError
from cratekit.modules.outbound import tidal_account
from tests.test_outbound_order import Client, Movable, Provider, Stale, _adapter, _lands
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414 - fixture
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414 - fixture

#: The three ways a read can lag a write: the tracks alone, the count alone, and both.
LAGS = ("tracks", "count", "whole")

#: What a refusal over a read that never caught up says of each half (round one's review).
SAID = {
    "whole": "still read as it was before a removal",
    "tracks": "its declared count changed and its tracks still as they were before",
    "count": "its tracks changed as asked and its declared count still as it was before",
}


def _lagging(members: list[str], lag: int, how: str) -> Provider:
    provider = Provider(members, lag=lag if how != "count" else 0, whole=how == "whole")
    provider.count_lag = lag if how == "count" else 0
    return provider


def _removing_b(installed, provider: Provider):
    """The cause of taking ``b`` off ``mine``, which must refuse, and the pauses before it."""
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).remove_tracks("mine", ("b",))
    return refused.value.cause, slept


def _takes_b(installed, provider: Provider) -> list[float]:
    """The pauses of taking ``b`` off ``mine``, which must come back as taken."""
    slept: list[float] = []
    assert _adapter(installed, provider, slept).remove_tracks("mine", ("b",)) == ("b",)
    return slept


# ── a read that lags the removal ────────────────────────────────────────────


@pytest.mark.parametrize("how", LAGS)
def test_a_removal_whose_read_lags_one_write_is_taken_as_done(installed, how):
    provider = _lagging(["a", "b", "c", "d"], 1, how)
    slept = _takes_b(installed, provider)
    assert provider.members == ["a", "c", "d"]
    assert provider.removals == [(1,)], "a removal was sent twice"
    assert slept == [tidal_account.ORDER_PAUSES[0]], "a lagging read was read again with no pause"


@pytest.mark.parametrize("how", LAGS)
def test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed(installed, how):
    provider = _lagging(["a", "b", "c", "d"], 99, how)
    cause, slept = _removing_b(installed, provider)
    assert cause.reason == "outbound-remove-refused"
    assert cause.detail["problem"] == "read-back-differs"
    assert cause.detail["lagged"] == "yes"
    assert cause.retryable is False
    assert "may have landed" in cause.message
    assert "may have come off" not in cause.message
    assert f"after {tidal_account.ORDER_REREADS + 1} readings" in cause.message
    assert SAID[how] in cause.message
    assert all(said not in cause.message for half, said in SAID.items() if half != how)
    assert len(slept) == tidal_account.ORDER_REREADS
    assert provider.removals == [(1,)], "a removal was sent twice"
    assert provider.members == ["a", "c", "d"]


@pytest.mark.parametrize("lag", [99, 0])
def test_a_refused_read_back_forgets_what_was_remembered_of_the_playlist(installed, lag):
    """After any refusal what the playlist holds is not known, so nothing is remembered of it."""
    provider = _lagging(["a", "b", "c", "d"], lag, "whole")
    provider.wrong = None if lag else 0
    account = _adapter(installed, provider)
    with pytest.raises(CratekitError):
        account.remove_tracks("mine", ("b",))
    assert "mine" not in account._members


def test_a_read_that_catches_up_on_the_last_reading_is_taken_as_done(installed):
    provider = _lagging(["a", "b", "c", "d"], tidal_account.ORDER_REREADS, "whole")
    assert len(_takes_b(installed, provider)) == tidal_account.ORDER_REREADS
    assert provider.removals == [(1,)]


def test_the_pauses_are_the_orders_pauses(installed):
    _cause, slept = _removing_b(installed, _lagging(["a", "b", "c", "d"], 99, "whole"))
    assert slept == [tidal_account._pause(n) for n in range(1, tidal_account.ORDER_REREADS + 1)]


# ── a reading that is neither before nor after ──────────────────────────────


def test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause(installed):
    provider = Provider(["a", "b", "c", "d"])
    provider.wrong = 0
    cause, slept = _removing_b(installed, provider)
    assert cause.detail["problem"] == "read-back-differs"
    assert cause.detail["lagged"] == "no"
    assert "may have come off" in cause.message
    assert slept == []
    assert provider.removals == [(1,)]


def test_a_wrong_track_behind_a_lagging_count_refuses_at_once(installed):
    """Half before and half neither is not a lag: the tracks show a wrong removal."""
    provider = _lagging(["a", "b", "c", "d"], 99, "count")
    provider.wrong = 0
    cause, slept = _removing_b(installed, provider)
    assert cause.detail["lagged"] == "no"
    assert slept == []


@pytest.mark.parametrize(
    ("declared", "videos"),
    [(7, 0), (2, 0), (None, 0), (True, 0), (3, 1), (3, None)],
    ids=["count-neither", "count-short", "count-none", "count-flag", "a-video", "videos-none"],
)
def test_a_count_that_is_neither_before_nor_after_refuses_at_once(installed, declared, videos):
    """The tracks are after, the count or the videos something else: refused, no pause."""
    provider = Provider(["a", "b", "c", "d"])
    provider.shown = (declared, videos)
    cause, slept = _removing_b(installed, provider)
    assert cause.detail["problem"] == "read-back-differs"
    assert cause.detail["lagged"] == "no"
    assert slept == []
    assert len(provider.removals) == 1


@pytest.mark.parametrize(
    "drift", [["a", "d"], ["a", "x", "c", "d"]], ids=["then-wrong", "as-long-as-before"]
)
def test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound(installed, drift):
    """Before is judged by the tracks read, not by how many: a swapped track refuses at once."""
    provider = _lagging(["a", "b", "c", "d"], 1, "whole")
    provider.drift = drift
    cause, slept = _removing_b(installed, provider)
    assert cause.detail["lagged"] == "no"
    assert slept == [tidal_account.ORDER_PAUSES[0]]


# ── nothing is sent again ───────────────────────────────────────────────────


def test_a_removal_that_fails_is_never_resent(installed):
    provider = Provider(["a", "b", "c", "d"])
    provider.remove_fails = [RuntimeError("timed out")]
    _removing_b(installed, provider)
    assert provider.removals == [(1,)]
    assert provider.members == ["a", "b", "c", "d"]


def test_a_removal_answered_412_is_never_resent(installed):
    """A 412 changed nothing; it is raised as any failure is, and nothing is sent again."""
    provider = Provider(["a", "b", "c", "d"], stale_tags=1)
    _removing_b(installed, provider)
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
    """``sync pair``'s calls on one playlist: what the removal left is what the order expects."""
    provider = _lagging(["a", "b", "c", "d"], 1, how)
    account = _adapter(installed, provider)
    assert account.remove_tracks("mine", ("b",)) == ("b",)
    assert account.add_tracks("mine", ("x",)) == ("x",)
    _lands(account, ("x", "d", "a", "c"), provider)
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
