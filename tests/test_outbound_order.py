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

U231 changed what a lag after a move costs: Sitting 86's reads lagged the
moves for minutes, so the moves are now sent with no read back between them,
a 412 resends the same move, and one later reading (``settled_order``) says
whether the order landed. The read back tests U220 wrote are rewritten to
that contract here.

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

    R-1308 adds a removal by position, as the client's ``remove_by_indices``
    sends it, with the same tag and the same lag. ``count_lag`` is how many
    openings after each write declare the count the playlist had before it
    while the tracks read current; ``wrong`` takes that position instead of
    the asked ones, once; ``remove_fails`` raises before anything changes;
    ``shown`` is the ``(num_tracks, num_videos)`` every opening after a
    removal declares; ``drift`` is what the tracks become once a lag is spent.

    U226 reads every playlist twice, its window and then the client's unpaged
    read, so a lag is counted per READING, one opened playlist, decided at its
    first read and held for every read of that object. ``window_only`` makes a
    lag hold for the window read alone, the unpaged read serving the playlist
    as it is, as Sitting 84 measured; ``unpaged_size`` is how many tracks the
    unpaged read serves, a first page, None for all of them; ``walk_lags``
    makes the unpaged read's later pages, asked with an offset, lag as the
    window does (R-1360), so only its first page is current; ``declared``
    overrides the count every opening declares.
    """

    def __init__(
        self,
        members: list[str],
        *,
        landing: str = "end",
        lag: int = 0,
        stale_tags: int = 0,
        whole: bool = False,
    ) -> None:
        self.members = list(members)
        self.version = 1
        self.previous: tuple[list[str], int] = (list(members), 0)
        self.landing = landing
        self.lag = lag
        self.lagging = 0
        self.stale_tags = stale_tags
        self.elsewhere = False
        #: Whether a lagging read lags the declared count too, not the tracks alone.
        self.whole = whole
        #: How many reads lag after a move the provider refuses 412.
        self.lag_after_refusal = 0
        #: Every move asked, as ``(indices, position, tag)``, refused or not.
        self.moves: list[tuple[tuple[int, ...], int, int]] = []
        #: Every move refused with a 412.
        self.refused = 0
        self.opened = 0
        self.reads = 0
        self.count_lag = 0
        self.counting = 0
        #: Every removal asked, as its indices, refused or not.
        self.removals: list[tuple[int, ...]] = []
        self.wrong: int | None = None
        self.remove_fails: list[Exception] = []
        self.shown: tuple[object, object] | None = None
        self.drift: list[str] | None = None
        self.window_only = False
        self.unpaged_size: int | None = None
        self.walk_lags = False
        self.declared: int | None = None

    def wrote(self, before: list[str]) -> None:
        self.previous = (before, self.version)
        self.version += 1
        self.lagging = self.lag
        self.counting = self.count_lag


class Movable:
    """One opened playlist, as the client's ``UserPlaylist`` behaves for what the adapter calls."""

    num_videos = 0

    def __init__(self, provider: Provider, playlist_id: str) -> None:
        provider.opened += 1
        self.provider = provider
        self.id = playlist_id
        lagging = (provider.whole and provider.lagging) or provider.counting
        if provider.counting:
            provider.counting -= 1
        self.num_tracks = len(provider.previous[0] if lagging else provider.members)
        if provider.shown is not None and provider.removals:
            self.num_tracks, self.num_videos = provider.shown
        if provider.declared is not None:
            self.num_tracks = provider.declared
        self._etag = provider.version
        #: Whether this reading lags and whether it carries the previous tag,
        #: decided at its first read.
        self._read_as: tuple[bool, bool] | None = None

    def _reading(self) -> tuple[bool, bool]:
        provider = self.provider
        if self._read_as is None:
            behind = provider.lagging > 0
            stale = not behind and provider.stale_tags > 0
            if behind:
                provider.lagging -= 1
                if not provider.lagging and provider.drift is not None:
                    provider.members[:] = provider.drift
            elif stale:
                provider.stale_tags -= 1
            self._read_as = (behind, stale)
        return self._read_as

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[SimpleNamespace]:
        provider = self.provider
        provider.reads += 1
        unpaged = limit is None
        size = limit if not unpaged else (provider.unpaged_size or 100)
        behind, stale = self._reading()
        current = unpaged and provider.window_only and not (offset and provider.walk_lags)
        if behind and not current:
            seen, self._etag = provider.previous
        elif stale:
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

    def remove_by_indices(self, indices) -> bool:
        provider = self.provider
        asked = tuple(indices)
        provider.removals.append(asked)
        if provider.remove_fails:
            raise provider.remove_fails.pop(0)
        if self._etag != provider.version:
            raise Stale()
        before = list(provider.members)
        taken = {provider.wrong} if provider.wrong is not None else set(asked)
        provider.wrong = None
        provider.members[:] = [one for i, one in enumerate(before) if i not in taken]
        provider.wrote(before)
        # The client reads the playlist again after the request, for its tag.
        self._etag = provider.version
        return True

    def move_by_indices(self, indices, position: int) -> bool:
        provider = self.provider
        asked = tuple(indices)
        provider.moves.append((asked, position, self._etag))
        if self._etag != provider.version:
            provider.refused += 1
            provider.lagging = provider.lag_after_refusal
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


def test_a_move_that_lands_anywhere_else_is_not_read_back_and_the_settle_reading_shows_it(
    installed,
):
    """U231: no read back between moves, so the order's one later reading is what tells."""
    provider = Provider(["a", "b", "c", "d"])
    provider.elsewhere = True
    slept: list[float] = []
    account = _adapter(installed, provider, slept)
    after = account.order_tracks("mine", ("d", "a", "b", "c"))
    assert after == ("d", "a", "b", "c"), "the return is the order as sent"
    assert len(provider.moves) == 1
    assert slept == []
    assert account.settled_order("mine") == ("a", "d", "b", "c")
    assert sorted(provider.members) == ["a", "b", "c", "d"]


def test_each_planned_move_is_sent_once_however_the_planner_answers(installed, monkeypatch):
    """A planner that never runs out of moves cannot keep the order writing (U231).

    The moves are planned once from one reading and each is sent once, so a
    planner that keeps no tail sends no more moves than it named. The
    mutation table's planner that kept no tail once moved the playlist until
    the run was killed; a write loop on the account with no bound is the
    hazard, so the bound is held here.
    """
    monkeypatch.setattr(
        tidal_account, "_to_the_front", lambda before, remote_ids: list(reversed(remote_ids))
    )
    provider = Provider(["a", "b", "c"])
    _adapter(installed, provider).order_tracks("mine", ("c", "a", "b"))
    assert len(provider.moves) == 3
    assert sorted(provider.members) == ["a", "b", "c"]


# ═══════════════════════════════════════════════════════════════════════════
# A stale version tag
# ═══════════════════════════════════════════════════════════════════════════


def test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading(installed):
    provider = Provider(["a", "b", "c"], stale_tags=1)
    after = _adapter(installed, provider).order_tracks("mine", ("c", "a", "b"))
    assert after == ("c", "a", "b")
    assert provider.refused == 1
    # The move the provider refused carried the stale tag and changed nothing;
    # the one after it was sent with the tag of the new reading.
    assert [tag for _asked, _to, tag in provider.moves] == [0, 1]


class Refusing(Movable):
    """An opened playlist whose every move the provider answers 412, a tag that never comes fresh."""

    def move_by_indices(self, indices, position: int) -> bool:
        self.provider.moves.append((tuple(indices), position, self._etag))
        self.provider.refused += 1
        raise Stale()


class RefusingClient(Client):
    def playlist(self, playlist_id: str) -> Movable:
        return Refusing(self.provider, playlist_id)


def test_a_move_whose_tag_never_comes_fresh_is_sent_a_bounded_number_of_times(installed):
    provider = Provider(["a", "b", "c"])
    pairs.PairStore(installed).mark("mine", "rb-mine", name="Mine")
    slept: list[float] = []
    account = tidal_account.TidalAccount(RefusingClient(provider), sleep=slept.append, cfg=installed)
    with pytest.raises(CratekitError) as refused:
        account.order_tracks("mine", ("c", "a", "b"))
    assert refused.value.cause.reason == "unavailable-transient"
    assert provider.members == ["a", "b", "c"]
    assert provider.refused == len(provider.moves) == tidal_account.ORDER_REREADS + 1
    assert {asked for asked, _to, _tag in provider.moves} == {(2,)}, "another move was sent"
    assert slept == list(tidal_account.ORDER_PAUSES)
    record = account.read_backs()[-1]
    assert (record["after"], record["outcome"], record["stale"]) == (
        "moves",
        "refused",
        tidal_account.ORDER_REREADS,
    )


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


# ═══════════════════════════════════════════════════════════════════════════
# Round one's review
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("whole", [False, True])
def test_the_reading_after_a_412_is_held_to_what_the_adds_left(installed, whole):
    """R1 of round one: a reading after a 412 that lags the adds is not planned from."""
    provider = Provider(["a", "b", "c"], whole=whole)
    account = _adapter(installed, provider)
    account.add_tracks("mine", ("x", "y"))
    provider.stale_tags = 1
    provider.lag_after_refusal = 1
    after = account.order_tracks("mine", ("y", "x", "a", "b", "c"))
    assert after == ("y", "x", "a", "b", "c")
    assert provider.members == ["y", "x", "a", "b", "c"]
    assert provider.refused == 1


def test_a_412_whose_body_is_not_json_is_still_read_as_a_stale_tag():
    """R3 of round one: the client raises a decode error while handling the HTTP error."""
    try:
        try:
            raise Stale()
        except Stale:
            raise ValueError("Expecting value: line 1 column 1 (char 0)") from None
    except ValueError as decoded:
        assert decoded.__cause__ is None and isinstance(decoded.__context__, Stale)
        wrapped = CratekitError.__new__(CratekitError)
        wrapped.__cause__ = decoded
        assert tidal_account._stale_tag(wrapped)
    assert not tidal_account._stale_tag(RuntimeError("a 500"))


def test_more_412s_than_pauses_repeat_the_last_pause(installed, monkeypatch):
    monkeypatch.setattr(tidal_account, "ORDER_REREADS", 5)
    provider = Provider(["a", "b", "c"])
    pairs.PairStore(installed).mark("mine", "rb-mine", name="Mine")
    slept: list[float] = []
    account = tidal_account.TidalAccount(RefusingClient(provider), sleep=slept.append, cfg=installed)
    with pytest.raises(CratekitError):
        account.order_tracks("mine", ("c", "a", "b"))
    assert slept == [*tidal_account.ORDER_PAUSES, tidal_account.ORDER_PAUSES[-1], tidal_account.ORDER_PAUSES[-1]]


@pytest.mark.parametrize(
    ("before", "order"),
    [
        (["a", "z", "b", "c"], ("c", "a", "b")),
        (["a", "b", "a", "c"], ("c", "a", "b")),
        (["d", "c", "b", "a"], ("a", "b", "c", "d")),
        (["a", "b", "c"], ("q", "c", "a")),
    ],
)
def test_the_fake_account_orders_by_the_adapters_rule(installed, before, order):
    """R4 of round one: a sync suite's snapshot is the one the live adapter would leave."""
    from tests.outbound_fakes import FakeAccount

    provider = Provider(before)
    live = _adapter(installed, provider).order_tracks("mine", order)
    fake = FakeAccount()
    fake.playlists["mine"] = list(before)
    assert fake.order_tracks("mine", order) == live


def test_the_pauses_after_a_412_start_again_for_each_move(installed, monkeypatch):
    """U231: a 412 on one move does not shorten the pauses another move's 412 is given."""
    provider = Provider(["a", "b", "c", "d"])
    real = Movable.move_by_indices
    sent: list[int] = []

    def stale_each_first(self, indices, position):
        sent.append(1)
        if len(sent) in (1, 3):
            self._etag = -1
        return real(self, indices, position)

    monkeypatch.setattr(Movable, "move_by_indices", stale_each_first)
    slept: list[float] = []
    after = _adapter(installed, provider, slept).order_tracks("mine", ("d", "c", "a", "b"))
    assert after == ("d", "c", "a", "b")
    assert provider.refused == 2
    assert slept == [tidal_account.ORDER_PAUSES[0], tidal_account.ORDER_PAUSES[0]]


# ═══════════════════════════════════════════════════════════════════════════
# U231: the moves sent with no read back between them
# ═══════════════════════════════════════════════════════════════════════════


def test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between(
    installed, monkeypatch
):
    """Sitting 86: a read back after each move spent four readings on a lag of minutes."""
    provider = Provider(["a", "b", "c", "d", "e"])
    account = _adapter(installed, provider)
    reads: list[int] = []
    real = Movable.move_by_indices

    def counted(self, indices, position):
        reads.append(provider.reads)
        return real(self, indices, position)

    monkeypatch.setattr(Movable, "move_by_indices", counted)
    after = account.order_tracks("mine", ("e", "d", "c", "b", "a"))
    assert after == ("e", "d", "c", "b", "a")
    assert provider.members == ["e", "d", "c", "b", "a"]
    assert len(set(reads)) == 1, "the playlist was read between two moves"
    assert provider.opened == 1


def test_a_read_that_lags_every_move_does_not_stop_the_order(installed):
    provider = Provider(["a", "b", "c", "d"], lag=99)
    slept: list[float] = []
    after = _adapter(installed, provider, slept).order_tracks("mine", ("d", "c", "a", "b"))
    assert after == ("d", "c", "a", "b")
    assert provider.members == ["d", "c", "a", "b"]
    assert len(provider.moves) == 2
    assert slept == []


def test_a_412_on_the_third_move_resends_that_move_once_and_no_other(installed, monkeypatch):
    provider = Provider(["a", "b", "c", "d", "e"])
    real = Movable.move_by_indices
    sent: list[int] = []

    def third_stale(self, indices, position):
        sent.append(1)
        if len(sent) == 3:
            self._etag = -1
        return real(self, indices, position)

    monkeypatch.setattr(Movable, "move_by_indices", third_stale)
    slept: list[float] = []
    after = _adapter(installed, provider, slept).order_tracks("mine", ("e", "d", "c", "a", "b"))
    assert after == ("e", "d", "c", "a", "b")
    assert provider.members == ["e", "d", "c", "a", "b"]
    assert provider.refused == 1
    assert len(provider.moves) == 4, "a move was sent twice, or one was missed"
    assert provider.moves[2][0] == provider.moves[3][0], "the 412's move was not the one resent"
    assert slept == [tidal_account.ORDER_PAUSES[0]]


def test_the_caller_is_told_what_is_sent_before_the_first_move(installed):
    provider = Provider(["a", "b", "c"])
    told: list[tuple[tuple[str, ...], tuple[str, ...], int]] = []
    _adapter(installed, provider).order_tracks(
        "mine",
        ("c", "a", "b"),
        begun=lambda start, end: told.append((start, end, len(provider.moves))),
    )
    assert told == [(("a", "b", "c"), ("c", "a", "b"), 0)]


def test_a_caller_that_cannot_record_the_moves_has_none_sent(installed):
    provider = Provider(["a", "b", "c"])

    def unwritable(start, end):
        raise OSError("read only")

    with pytest.raises(OSError):
        _adapter(installed, provider).order_tracks("mine", ("c", "a", "b"), begun=unwritable)
    assert provider.moves == []


def test_nothing_to_move_tells_the_caller_nothing(installed):
    provider = Provider(["a", "b", "c"])
    told: list[object] = []
    after = _adapter(installed, provider).order_tracks(
        "mine", ("a", "b", "c"), begun=lambda start, end: told.append(start)
    )
    assert after == ("a", "b", "c") and told == []


def test_the_settle_reading_waits_then_reads_once_and_names_a_lag(installed):
    provider = Provider(["a", "b", "c"])
    slept: list[float] = []
    account = _adapter(installed, provider, slept)
    assert account.settled_order("mine", wait=12.5) == ("a", "b", "c")
    assert slept == [12.5]
    provider.members[:] = ["c", "a", "b"]
    provider.previous = (["a", "b", "c"], 0)
    provider.lagging = 1
    provider.window_only = True
    provider.declared = 4
    assert account.settled_order("mine") is None
    record = account.read_backs()[-1]
    assert record["after"] == "settle" and record["window_lagged"] == 1
    assert record["outcome"] == "lags"
