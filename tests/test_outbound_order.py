"""U220: the account adapter puts a playlist it just added to in order, over a provider that lags.

Sitting 62's live ``crate sync pair`` added six tracks to a paired playlist,
then its order failed: a 412 from the provider on the first move, then on each
continue a read back that was "not what it held with that track moved to the
end", although the moves had landed. These tests drive ``order_tracks``
against a stand in for the provider's client that keeps a version tag the way
the provider does, answers a write carrying a tag other than the current one
with a 412 and changes nothing, and can serve a read that lags its writes.

The three shapes the card names are each a provider here: one whose move to
the playlist's length lands one short of the end, one that answers 412 on a
stale tag until the playlist is read again, and one whose read lags a write.
Which of them the live provider is was not measured from this container; the
adapter is held to reaching the asked order under every one of them, or to
refusing before its first move with nothing moved.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from cratekit.core.cause import CratekitError
from cratekit.modules.outbound import pairs, tidal_account
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414 - fixture


class Stale(Exception):
    """The provider's answer to a write whose version tag is not the current one."""

    def __init__(self) -> None:
        super().__init__("412 Client Error: Precondition Failed")
        self.response = SimpleNamespace(status_code=412)


class Provider:
    """The provider's playlists, versioned, shared by every object the client opens.

    ``landing`` is where a move to the playlist's length lands: ``"end"``, or
    ``"short"`` for one short of the end. ``lag`` is how many reads of the
    tracks after each write still answer the playlist as it was before that
    write, with the tag it had then. ``stale_tags`` is how many reads answer
    the current tracks with the previous tag. ``elsewhere`` makes the next
    move land at position one whatever was asked.
    """

    def __init__(
        self,
        members: list[str],
        *,
        landing: str = "end",
        lag: int = 0,
        stale_tags: int = 0,
    ) -> None:
        self.members = list(members)
        self.version = 1
        self.previous: tuple[list[str], int] = (list(members), 0)
        self.landing = landing
        self.lag = lag
        self.lagging = 0
        self.stale_tags = stale_tags
        self.elsewhere = False
        #: Every move asked, as ``(indices, position, tag)``, refused or not.
        self.moves: list[tuple[tuple[int, ...], int, int]] = []
        #: Every move refused with a 412.
        self.refused = 0
        self.opened = 0
        self.reads = 0

    def wrote(self, before: list[str]) -> None:
        self.previous = (before, self.version)
        self.version += 1
        self.lagging = self.lag


class Movable:
    """One opened playlist, as the client's ``UserPlaylist`` behaves for what the adapter calls."""

    num_videos = 0

    def __init__(self, provider: Provider, playlist_id: str) -> None:
        provider.opened += 1
        self.provider = provider
        self.id = playlist_id
        self.num_tracks = len(provider.members)
        self._etag = provider.version

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[SimpleNamespace]:
        provider = self.provider
        provider.reads += 1
        size = 100 if limit is None else limit
        if provider.lagging:
            if offset + size >= len(provider.previous[0]):
                provider.lagging -= 1
            seen, self._etag = provider.previous
        elif provider.stale_tags:
            provider.stale_tags -= 1
            seen, self._etag = provider.members, provider.version - 1
        else:
            seen, self._etag = provider.members, provider.version
        return [SimpleNamespace(id=one) for one in seen[offset : offset + size]]

    def add(self, media_ids, allow_duplicates: bool = False) -> list[str]:
        del allow_duplicates
        provider = self.provider
        if self._etag != provider.version:
            raise Stale()
        before = list(provider.members)
        fresh = [str(one) for one in media_ids if str(one) not in provider.members]
        provider.members.extend(fresh)
        provider.wrote(before)
        self._etag = provider.version
        return fresh

    def move_by_indices(self, indices, position: int) -> bool:
        provider = self.provider
        asked = tuple(indices)
        provider.moves.append((asked, position, self._etag))
        if self._etag != provider.version:
            provider.refused += 1
            raise Stale()
        before = list(provider.members)
        moving = [before[i] for i in asked]
        kept = [one for i, one in enumerate(before) if i not in set(asked)]
        if provider.elsewhere:
            provider.elsewhere = False
            at = 1
        elif position >= len(before):
            at = len(kept) if provider.landing == "end" else len(kept) - 1
        else:
            at = position
        provider.members[:] = [*kept[:at], *moving, *kept[at:]]
        provider.wrote(before)
        # The client reads the playlist again after the request, for its tag.
        self._etag = provider.version
        return True


class Client:
    def __init__(self, provider: Provider) -> None:
        self.provider = provider

    def playlist(self, playlist_id: str) -> Movable:
        return Movable(self.provider, playlist_id)


def _adapter(cfg, provider: Provider, slept: list[float] | None = None):
    pairs.PairStore(cfg).mark("mine", "rb-mine", name="Mine")
    pause = slept.append if slept is not None else (lambda seconds: None)
    return tidal_account.TidalAccount(Client(provider), sleep=pause, cfg=cfg)


# ═══════════════════════════════════════════════════════════════════════════
# Where a move lands
# ═══════════════════════════════════════════════════════════════════════════


def test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order(installed):
    provider = Provider(["a", "b", "c", "d"], landing="short")
    after = _adapter(installed, provider).order_tracks("mine", ("d", "c", "b", "a"))
    assert after == ("d", "c", "b", "a")
    assert provider.members == ["d", "c", "b", "a"]


def test_every_move_is_to_the_front_where_both_ways_of_counting_agree(installed):
    provider = Provider(["a", "b", "c", "d"])
    _adapter(installed, provider).order_tracks("mine", ("c", "a", "b", "d"))
    # "a", "b", "d" already stand in order at the tail of the asked order, so
    # "c" alone is moved, from position two to the front.
    assert [(asked, to) for asked, to, _tag in provider.moves] == [((2,), 0)]
    assert provider.members == ["c", "a", "b", "d"]


def test_the_tracks_before_the_kept_tail_are_moved_last_first(installed):
    provider = Provider(["a", "b", "c", "d"])
    _adapter(installed, provider).order_tracks("mine", ("d", "c", "a", "b"))
    assert [asked for asked, _to, _tag in provider.moves] == [(2,), (3,)]
    assert provider.members == ["d", "c", "a", "b"]


def test_a_move_that_lands_anywhere_else_refuses_at_once_with_every_track_kept(installed):
    provider = Provider(["a", "b", "c"])
    provider.elsewhere = True
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).order_tracks("mine", ("c", "b", "a"))
    assert refused.value.cause.reason == "outbound-remove-refused"
    assert refused.value.cause.detail["problem"] == "read-back-differs"
    assert len(provider.moves) == 1
    assert slept == [], "a read back that is neither before nor after was read again"
    assert sorted(provider.members) == ["a", "b", "c"]


# ═══════════════════════════════════════════════════════════════════════════
# A stale version tag
# ═══════════════════════════════════════════════════════════════════════════


def test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading(installed):
    provider = Provider(["a", "b", "c"], stale_tags=1)
    after = _adapter(installed, provider).order_tracks("mine", ("c", "a", "b"))
    assert after == ("c", "a", "b")
    assert provider.refused == 1
    # The move the provider refused changed nothing, and the one after it was
    # sent with the tag of the reading its position came from.
    assert [tag for _asked, _to, tag in provider.moves] == [1, 1]


def test_a_tag_that_never_comes_fresh_refuses_with_nothing_moved(installed):
    provider = Provider(["a", "b", "c"], stale_tags=99)
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider).order_tracks("mine", ("c", "a", "b"))
    assert refused.value.cause.reason == "unavailable-transient"
    assert provider.members == ["a", "b", "c"]
    assert provider.refused == len(provider.moves) == tidal_account.ORDER_REREADS + 1


def test_a_failure_other_than_a_stale_tag_is_never_sent_again(installed):
    provider = Provider(["a", "b", "c"])

    class Dropped(Movable):
        def move_by_indices(self, indices, position: int) -> bool:
            provider.moves.append((tuple(indices), position, self._etag))
            raise TimeoutError("the connection dropped")

    class DroppingClient(Client):
        def playlist(self, playlist_id: str) -> Movable:
            return Dropped(self.provider, playlist_id)

    pairs.PairStore(installed).mark("mine", "rb-mine", name="Mine")
    account = tidal_account.TidalAccount(
        DroppingClient(provider), sleep=lambda seconds: None, cfg=installed
    )
    with pytest.raises(CratekitError) as refused:
        account.order_tracks("mine", ("c", "a", "b"))
    assert refused.value.cause.reason == "unavailable-transient"
    assert len(provider.moves) == 1


# ═══════════════════════════════════════════════════════════════════════════
# A read that lags a write
# ═══════════════════════════════════════════════════════════════════════════


def test_a_read_back_that_lags_one_move_is_read_again_not_refused(installed):
    provider = Provider(["a", "b", "c", "d"], lag=1)
    slept: list[float] = []
    after = _adapter(installed, provider, slept).order_tracks("mine", ("d", "c", "a", "b"))
    assert after == ("d", "c", "a", "b")
    assert provider.members == ["d", "c", "a", "b"]
    assert len(provider.moves) == 2, "a move was sent twice"
    assert slept, "a lagging read was read again with no pause"


def test_a_read_back_that_never_catches_up_refuses_after_one_move(installed):
    provider = Provider(["a", "b", "c"], lag=99)
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).order_tracks("mine", ("c", "a", "b"))
    assert refused.value.cause.detail["problem"] == "read-back-differs"
    assert len(provider.moves) == 1
    assert len(slept) == tidal_account.ORDER_REREADS
    assert sorted(provider.members) == ["a", "b", "c"]


def test_the_reading_after_adds_that_lags_them_is_read_again_before_the_first_move(installed):
    provider = Provider(["a", "b", "c"], lag=1)
    account = _adapter(installed, provider)
    assert account.add_tracks("mine", ("x", "y")) == ("x", "y")
    after = account.order_tracks("mine", ("y", "a", "b", "c", "x"))
    assert after == ("y", "a", "b", "c", "x")
    assert provider.refused == 0


def test_a_reading_that_never_shows_the_adds_refuses_with_nothing_moved(installed):
    provider = Provider(["a", "b", "c"], lag=99)
    account = _adapter(installed, provider)
    account.add_tracks("mine", ("x",))
    with pytest.raises(CratekitError) as refused:
        account.order_tracks("mine", ("x", "a", "b", "c"))
    assert refused.value.cause.reason == "outbound-remove-refused"
    assert provider.moves == []
    assert provider.members == ["a", "b", "c", "x"]


def test_a_reading_holding_what_the_adds_left_in_another_order_is_not_stale(installed):
    """The guard after adds compares what the playlist holds, not where the adds went."""
    provider = Provider(["a", "b"])
    account = _adapter(installed, provider)
    account.add_tracks("mine", ("x",))
    provider.members[:] = ["x", "a", "b"]
    assert account.order_tracks("mine", ("a", "b", "x")) == ("a", "b", "x")


# ═══════════════════════════════════════════════════════════════════════════
# A reading the caller expects
# ═══════════════════════════════════════════════════════════════════════════


def test_a_reading_that_never_agrees_with_the_expected_one_refuses_with_nothing_moved(installed):
    provider = Provider(["a", "b", "c"])
    slept: list[float] = []
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, provider, slept).order_tracks(
            "mine", ("c", "a", "b"), expect=("b", "a", "c")
        )
    assert refused.value.cause.reason == "outbound-remove-refused"
    assert refused.value.cause.detail["problem"] == "read-differs"
    assert provider.moves == []
    assert len(slept) == tidal_account.ORDER_REREADS


def test_a_reading_that_agrees_with_the_expected_one_takes_the_order(installed):
    provider = Provider(["a", "b", "c"])
    after = _adapter(installed, provider).order_tracks(
        "mine", ("c", "a", "b"), expect=("a", "b", "c")
    )
    assert after == ("c", "a", "b")


def test_a_reading_that_lags_the_expected_one_is_read_again(installed):
    provider = Provider(["b", "a", "c"])
    provider.previous = (["a", "b", "c"], 0)
    provider.lagging = 1
    after = _adapter(installed, provider).order_tracks(
        "mine", ("c", "b", "a"), expect=("b", "a", "c")
    )
    assert after == ("c", "b", "a")
