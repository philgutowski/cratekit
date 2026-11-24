"""U220: the adapter orders a playlist it just added to, over a provider that lags. D1 applies."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from cratekit.core.cause import CratekitError
from cratekit.modules.outbound import pairs, tidal_account
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414 - fixture
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414 - fixture


class Stale(Exception):
    """The provider's answer to a write whose version tag is not the current one."""

    def __init__(self) -> None:
        super().__init__("412 Client Error: Precondition Failed")
        self.response = SimpleNamespace(status_code=412)


class Provider:
    """The provider's playlists, versioned, shared by every object the client opens.

    ``landing``: where a move to the length lands. ``lag``: readings after a write
    serving the old playlist and tag, ``whole`` the old count too. ``stale_tags``:
    readings with the previous tag. ``elsewhere``: the next move lands at one.
    Removals (R-1308): ``count_lag``, ``wrong``, ``remove_fails``, ``shown`` and
    ``drift``. U226's two readings: ``window_only``, ``unpaged_size``, ``walk_lags``
    (R-1360) and ``declared``.
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
        self.whole = whole
        #: How many reads lag after a move the provider refuses 412.
        self.lag_after_refusal = 0
        #: Every move asked, as ``(indices, position, tag)``, refused or not.
        self.moves: list[tuple[tuple[int, ...], int, int]] = []
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
        #: Whether this reading lags and whether it carries the previous tag.
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


class Refusing(Movable):
    """An opened playlist whose every move is answered 412, a tag that never comes fresh."""

    def move_by_indices(self, indices, position: int) -> bool:
        self.provider.moves.append((tuple(indices), position, self._etag))
        self.provider.refused += 1
        raise Stale()


class RefusingClient(Client):
    def playlist(self, playlist_id: str) -> Movable:
        return Refusing(self.provider, playlist_id)


def _adapter(cfg, provider: Provider, slept: list | None = None, *, client=Client, sleep=None):
    """An adapter over ``provider``, the playlist ``mine`` paired, its pauses kept in ``slept``."""
    pairs.PairStore(cfg).mark("mine", "rb-mine", name="Mine")
    pause = sleep or (slept.append if slept is not None else (lambda seconds: None))
    return tidal_account.TidalAccount(client(provider), sleep=pause, cfg=cfg)


def _moves(provider: Provider, part: int = 0) -> list:
    """One part of each move asked: 0 the indices, 1 the position, 2 the tag."""
    return [move[part] for move in provider.moves]


def _refused(call):
    """The cause ``call`` refuses with."""
    with pytest.raises(CratekitError) as refused:
        call()
    return refused.value.cause


def _lands(account, order: tuple[str, ...], provider: Provider | None = None, **kwargs) -> None:
    """Order ``mine`` as ``order``; given ``provider``, the playlist stands in it."""
    assert account.order_tracks("mine", order, **kwargs) == order
    if provider is not None:
        assert provider.members == list(order)


# ── where a move lands ──────────────────────────────────────────────────────


def test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order(installed):
    provider = Provider(["a", "b", "c", "d"], landing="short")
    _lands(_adapter(installed, provider), ("d", "c", "b", "a"), provider)


def test_every_move_is_to_the_front_where_both_ways_of_counting_agree(installed):
    provider = Provider(["a", "b", "c", "d"])
    _adapter(installed, provider).order_tracks("mine", ("c", "a", "b", "d"))
    # "a", "b", "d" already stand in order at the tail, so "c" alone moves.
    assert [(asked, to) for asked, to, _tag in provider.moves] == [((2,), 0)]
    assert provider.members == ["c", "a", "b", "d"]


def test_the_tracks_before_the_kept_tail_are_moved_last_first(installed):
    provider = Provider(["a", "b", "c", "d"])
    _adapter(installed, provider).order_tracks("mine", ("d", "c", "a", "b"))
    assert _moves(provider) == [(2,), (3,)]
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
    """An endless planner cannot keep the order writing: each planned move is sent once (U231)."""
    monkeypatch.setattr(
        tidal_account, "_to_the_front", lambda before, remote_ids: list(reversed(remote_ids))
    )
    provider = Provider(["a", "b", "c"])
    _adapter(installed, provider).order_tracks("mine", ("c", "a", "b"))
    assert len(provider.moves) == 3
    assert sorted(provider.members) == ["a", "b", "c"]


# ── a stale version tag ─────────────────────────────────────────────────────


def test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading(installed):
    provider = Provider(["a", "b", "c"], stale_tags=1)
    _lands(_adapter(installed, provider), ("c", "a", "b"))
    assert provider.refused == 1
    # The refused move carried the stale tag; the one after it the new reading's.
    assert _moves(provider, 2) == [0, 1]


def test_a_move_whose_tag_never_comes_fresh_is_sent_a_bounded_number_of_times(installed):
    provider = Provider(["a", "b", "c"])
    slept: list[float] = []
    account = _adapter(installed, provider, slept, client=RefusingClient)
    assert _refused(lambda: account.order_tracks("mine", ("c", "a", "b"))).reason == (
        "unavailable-transient"
    )
    assert provider.members == ["a", "b", "c"]
    assert provider.refused == len(provider.moves) == tidal_account.ORDER_REREADS + 1
    assert set(_moves(provider)) == {(2,)}, "another move was sent"
    assert slept == list(tidal_account.ORDER_PAUSES)
    record = account.read_backs()[-1]
    assert (record["after"], record["outcome"], record["stale"]) == (
        "moves",
        "refused",
        tidal_account.ORDER_REREADS,
    )


def test_a_failure_other_than_a_stale_tag_is_never_sent_again(installed, monkeypatch):
    provider = Provider(["a", "b", "c"])

    def dropped(self, indices, position: int) -> bool:
        provider.moves.append((tuple(indices), position, self._etag))
        raise TimeoutError("the connection dropped")

    monkeypatch.setattr(Movable, "move_by_indices", dropped)
    account = _adapter(installed, provider)
    cause = _refused(lambda: account.order_tracks("mine", ("c", "a", "b")))
    assert cause.reason == "unavailable-transient"
    assert len(provider.moves) == 1


# ── a read that lags a write ────────────────────────────────────────────────


def test_the_reading_after_adds_that_lags_them_is_read_again_before_the_first_move(installed):
    provider = Provider(["a", "b", "c"], lag=1)
    account = _adapter(installed, provider)
    assert account.add_tracks("mine", ("x", "y")) == ("x", "y")
    _lands(account, ("y", "a", "b", "c", "x"))
    assert provider.refused == 0


def test_a_reading_that_never_shows_the_adds_refuses_with_nothing_moved(installed):
    provider = Provider(["a", "b", "c"], lag=99)
    account = _adapter(installed, provider)
    account.add_tracks("mine", ("x",))
    cause = _refused(lambda: account.order_tracks("mine", ("x", "a", "b", "c")))
    assert cause.reason == "outbound-remove-refused"
    assert provider.moves == []
    assert provider.members == ["a", "b", "c", "x"]


def test_a_reading_holding_what_the_adds_left_in_another_order_is_not_stale(installed):
    """The guard after adds compares what the playlist holds, not where the adds went."""
    provider = Provider(["a", "b"])
    account = _adapter(installed, provider)
    account.add_tracks("mine", ("x",))
    provider.members[:] = ["x", "a", "b"]
    _lands(account, ("a", "b", "x"))


# ── a reading the caller expects ────────────────────────────────────────────


def test_a_reading_that_never_agrees_with_the_expected_one_refuses_with_nothing_moved(installed):
    provider = Provider(["a", "b", "c"])
    slept: list[float] = []
    account = _adapter(installed, provider, slept)
    cause = _refused(lambda: account.order_tracks("mine", ("c", "a", "b"), expect=("b", "a", "c")))
    assert cause.reason == "outbound-remove-refused"
    assert cause.detail["problem"] == "read-differs"
    assert provider.moves == []
    assert len(slept) == tidal_account.ORDER_REREADS


def test_a_reading_that_agrees_with_the_expected_one_takes_the_order(installed):
    _lands(_adapter(installed, Provider(["a", "b", "c"])), ("c", "a", "b"), expect=("a", "b", "c"))


def test_a_reading_that_lags_the_expected_one_is_read_again(installed):
    provider = Provider(["b", "a", "c"])
    provider.previous = (["a", "b", "c"], 0)
    provider.lagging = 1
    _lands(_adapter(installed, provider), ("c", "b", "a"), expect=("b", "a", "c"))


# ── round one's review ──────────────────────────────────────────────────────


@pytest.mark.parametrize("whole", [False, True])
def test_the_reading_after_a_412_is_held_to_what_the_adds_left(installed, whole):
    """R1 of round one: a reading after a 412 that lags the adds is not planned from."""
    provider = Provider(["a", "b", "c"], whole=whole)
    account = _adapter(installed, provider)
    account.add_tracks("mine", ("x", "y"))
    provider.stale_tags = 1
    provider.lag_after_refusal = 1
    _lands(account, ("y", "x", "a", "b", "c"), provider)
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
    slept: list[float] = []
    account = _adapter(installed, Provider(["a", "b", "c"]), slept, client=RefusingClient)
    with pytest.raises(CratekitError):
        account.order_tracks("mine", ("c", "a", "b"))
    last = tidal_account.ORDER_PAUSES[-1]
    assert slept == [*tidal_account.ORDER_PAUSES, last, last]


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

    live = _adapter(installed, Provider(before)).order_tracks("mine", order)
    fake = FakeAccount()
    fake.playlists["mine"] = list(before)
    assert fake.order_tracks("mine", order) == live


def _stale_on(monkeypatch, *sends: int) -> None:
    """Make the moves sent at these counts carry a stale tag, so each is refused 412 once."""
    real = Movable.move_by_indices
    sent: list[int] = []

    def stale_then_real(self, indices, position):
        sent.append(1)
        if len(sent) in sends:
            self._etag = -1
        return real(self, indices, position)

    monkeypatch.setattr(Movable, "move_by_indices", stale_then_real)


def test_the_pauses_after_a_412_start_again_for_each_move(installed, monkeypatch):
    """U231: a 412 on one move does not shorten the pauses another move's 412 is given."""
    provider = Provider(["a", "b", "c", "d"])
    _stale_on(monkeypatch, 1, 3)
    slept: list[float] = []
    _lands(_adapter(installed, provider, slept), ("d", "c", "a", "b"))
    assert provider.refused == 2
    assert slept == [tidal_account.ORDER_PAUSES[0], tidal_account.ORDER_PAUSES[0]]


# ── U231: the moves sent with no read back between them ─────────────────────


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
    _lands(account, ("e", "d", "c", "b", "a"), provider)
    assert len(set(reads)) == 1, "the playlist was read between two moves"
    assert provider.opened == 1


def test_a_read_that_lags_every_move_does_not_stop_the_order(installed):
    provider = Provider(["a", "b", "c", "d"], lag=99)
    slept: list[float] = []
    _lands(_adapter(installed, provider, slept), ("d", "c", "a", "b"), provider)
    assert len(provider.moves) == 2
    assert slept == []


def test_a_412_on_the_third_move_resends_that_move_once_and_no_other(installed, monkeypatch):
    provider = Provider(["a", "b", "c", "d", "e"])
    _stale_on(monkeypatch, 3)
    slept: list[float] = []
    _lands(_adapter(installed, provider, slept), ("e", "d", "c", "a", "b"), provider)
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
    told: list[object] = []
    after = _adapter(installed, Provider(["a", "b", "c"])).order_tracks(
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


# ── R-1394: the caller is told, before each move, how far the moves can have got ──


def _counting(provider: Provider, told: list[tuple[int, int, int]]):
    """A ``begun`` that answers a recorder, which notes each count with the moves sent by then."""

    def begun(start, end):
        def sending(sent: int, landed: int) -> None:
            told.append((sent, landed, len(provider.moves)))

        return sending

    return begun


def _counts(told: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
    return [(sent, landed) for sent, landed, _moves in told]


def test_the_caller_is_told_before_each_move_how_many_may_have_landed(installed):
    provider = Provider(["a", "b", "c", "d"])
    told: list[tuple[int, int, int]] = []
    _lands(_adapter(installed, provider), ("d", "c", "b", "a"), begun=_counting(provider, told))
    assert told == [(1, 0, 0), (2, 1, 1), (3, 2, 2)]


def test_a_move_spent_on_its_412s_is_told_as_not_landed(installed):
    provider = Provider(["a", "b", "c"])
    account = _adapter(installed, provider, client=RefusingClient)
    told: list[tuple[int, int, int]] = []
    with pytest.raises(CratekitError):
        account.order_tracks("mine", ("c", "a", "b"), begun=_counting(provider, told))
    # Told before each send and, after each 412, that the move changed nothing.
    assert _counts(told) == [(1, 0), (0, 0)] * (tidal_account.ORDER_REREADS + 1)


def test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight(installed):
    """Round one's row 4: the 412 is recorded before the pause, so a stop inside it reads true."""
    provider = Provider(["a", "b", "c"])

    def stopped(seconds: float) -> None:
        raise KeyboardInterrupt

    account = _adapter(installed, provider, client=RefusingClient, sleep=stopped)
    told: list[tuple[int, int, int]] = []
    with pytest.raises(KeyboardInterrupt):
        account.order_tracks("mine", ("c", "a", "b"), begun=_counting(provider, told))
    assert _counts(told) == [(1, 0), (0, 0)]
    assert provider.members == ["a", "b", "c"]


def test_a_move_that_failed_another_way_is_left_as_maybe_landed(installed, monkeypatch):
    provider = Provider(["a", "b", "c", "d"])
    real = Movable.move_by_indices

    def second_drops(self, indices, position):
        if len(provider.moves) == 1:
            provider.moves.append((tuple(indices), position, self._etag))
            raise TimeoutError("the connection dropped")
        return real(self, indices, position)

    monkeypatch.setattr(Movable, "move_by_indices", second_drops)
    told: list[tuple[int, int, int]] = []
    with pytest.raises(CratekitError):
        _adapter(installed, provider).order_tracks(
            "mine", ("d", "c", "b", "a"), begun=_counting(provider, told)
        )
    assert _counts(told) == [(1, 0), (2, 1)]


def test_a_recorder_that_cannot_record_has_no_further_move_sent(installed):
    provider = Provider(["a", "b", "c", "d"])
    told: list[int] = []

    def begun(start, end):
        def sending(sent, landed):
            if sent == 2:
                raise OSError("read only")
            told.append(sent)

        return sending

    with pytest.raises(OSError):
        _adapter(installed, provider).order_tracks("mine", ("d", "c", "b", "a"), begun=begun)
    assert told == [1]
    assert len(provider.moves) == 1, "a move was sent that no record names"


# ── R-1411: a reading the caller agreed on, beside what the write left ─────


def _one_move_in_then_added(installed, *, lag: int):
    """A stopped order then an add: every track the write left, in the order from before."""
    provider = Provider(["b", "a", "c"])
    account = _adapter(installed, provider)
    assert account.add_tracks("mine", ("x",)) == ("x",)
    assert provider.members == ["b", "a", "c", "x"]
    provider.previous = (["a", "b", "c", "x"], provider.version - 1)
    provider.lagging = lag
    return provider, account


def test_a_reading_that_lags_the_agreed_order_after_an_add_refuses_with_nothing_moved(
    installed,
):
    provider, account = _one_move_in_then_added(installed, lag=99)
    order = ("c", "b", "a", "x")
    cause = _refused(lambda: account.order_tracks("mine", order, agreed=("b", "a", "c")))
    assert cause.reason == "outbound-remove-refused"
    assert cause.detail["problem"] == "read-differs"
    assert provider.moves == [], "moves were planned from a reading that lags the agreed order"
    assert provider.members == ["b", "a", "c", "x"]


def test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order(installed):
    provider, account = _one_move_in_then_added(installed, lag=1)
    _lands(account, ("c", "b", "a", "x"), provider, agreed=("b", "a", "c"))


def test_an_added_track_the_provider_placed_elsewhere_is_not_refused(installed):
    provider = Provider(["b", "a", "c"])
    account = _adapter(installed, provider)
    account.add_tracks("mine", ("x",))
    provider.members[:] = ["b", "x", "a", "c"]
    _lands(account, ("c", "b", "a", "x"), provider, agreed=("b", "a", "c"))


def test_a_track_this_write_took_off_is_not_asked_of_the_reading(installed):
    provider = Provider(["b", "y", "a", "c"])
    account = _adapter(installed, provider)
    assert account.remove_tracks("mine", ("y",)) == ("y",)
    _lands(account, ("c", "b", "a"), provider, agreed=("b", "y", "a", "c"))


def test_the_agreed_order_does_not_stand_in_for_what_the_write_left(installed):
    """Beside the membership check, not instead of it: a reading lacking the add is refused."""
    provider = Provider(["b", "a", "c"], whole=True)
    account = _adapter(installed, provider)
    account.add_tracks("mine", ("x",))
    provider.previous = (["b", "a", "c"], provider.version - 1)
    provider.lagging = 99
    order = ("c", "b", "a", "x")
    cause = _refused(lambda: account.order_tracks("mine", order, agreed=("b", "a", "c")))
    assert cause.detail["problem"] == "read-differs"
    assert provider.moves == []


@pytest.mark.parametrize(
    ("reading", "agreed", "stands"),
    [
        (("b", "a", "c"), ("b", "a", "c"), True),
        (("a", "b", "c"), ("b", "a", "c"), False),
        (("b", "a", "c", "x"), ("b", "a", "c"), True),
        (("x", "b", "a", "c"), ("b", "a", "c"), True),
        (("b", "x", "a", "c"), ("b", "a", "c"), True),
        (("a", "x", "b", "c"), ("b", "a", "c"), False),
        (("b", "c"), ("b", "a", "c"), True),
        (("c", "b"), ("b", "a", "c"), False),
        (("b", "a", "b", "c"), ("b", "a", "c"), True),
        ((), ("b", "a", "c"), True),
        (("b", "a", "c"), (), True),
    ],
)
def test_the_agreed_order_is_read_over_the_tracks_both_hold(reading, agreed, stands):
    assert tidal_account._in_agreed_order(list(reading), agreed) is stands
