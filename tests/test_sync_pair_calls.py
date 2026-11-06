"""U210: the calls a sync pair write is expected to make, held to the real account adapter.

``sync/pair_calls.py`` estimates a write's provider calls from the account
adapter's shape, for the gate's forecast and for the ``--calls`` a stopped
run's continue is named. This drives the shipped adapter,
``modules/outbound/tidal_account.TidalAccount``, over a fake client that
counts every request it is asked for, and holds each estimate to the count.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import pytest

from cratekit.acquire import listing
from cratekit.modules.outbound import tidal_account
from cratekit.sync import pair_calls


class Track:
    def __init__(self, track_id: str) -> None:
        self.id = int(track_id)


class Counter:
    def __init__(self) -> None:
        self.requests = 0


class Playlist:
    """One opened playlist over the account's live members: every request counted."""

    num_videos = 0

    def __init__(self, counter: Counter, playlist_id: str, members: list[str]) -> None:
        self.counter = counter
        self.id = playlist_id
        self.members = members

    @property
    def num_tracks(self) -> int:
        return len(self.members)

    def tracks(self, limit: int | None = None, offset: int = 0) -> list[Track]:
        self.counter.requests += 1
        size = 100 if limit is None else limit
        return [Track(one) for one in self.members[offset : offset + size]]

    def add(self, media_ids: list[str], allow_duplicates: bool = False) -> list[str]:
        del allow_duplicates
        self.counter.requests += 1
        fresh = [one for one in media_ids if one not in self.members]
        self.members.extend(fresh)
        return list(media_ids)

    def remove_by_indices(self, indices: list[int]) -> bool:
        self.counter.requests += 1
        gone = set(indices)
        self.members[:] = [one for at, one in enumerate(self.members) if at not in gone]
        return True

    def move_by_indices(self, indices: list[int], position: int) -> bool:
        self.counter.requests += 1
        (at,) = indices
        self.members.insert(position, self.members.pop(at))
        return True

    def set_playlist_private(self) -> bool:
        self.counter.requests += 1
        return True


class Folder:
    def __init__(self, counter: Counter) -> None:
        self.counter = counter
        self.id = ""

    def move_items_to_folder(self, items: list[str], folder: str) -> bool:
        del items, folder
        self.counter.requests += 1
        return True


class User:
    def __init__(self, client: Client) -> None:
        self.client = client

    def create_playlist(self, title: str, description: str) -> Playlist:
        del title, description
        self.client.counter.requests += 1
        playlist_id = f"pl-{len(self.client.members) + 1}"
        self.client.members[playlist_id] = []
        return Playlist(self.client.counter, playlist_id, self.client.members[playlist_id])


class Client:
    """The provider's client in the shape the adapter calls, every request counted."""

    def __init__(self) -> None:
        self.counter = Counter()
        self.members: dict[str, list[str]] = {}
        self.user = User(self)

    def playlist(self, playlist_id: str) -> Playlist:
        self.counter.requests += 1
        return Playlist(self.counter, playlist_id, self.members[playlist_id])

    def folder(self) -> Folder:
        return Folder(self.counter)


@pytest.fixture
def client(monkeypatch) -> Client:
    # Every playlist here is one a pair vouches for, so a removal is asked.
    monkeypatch.setattr(tidal_account.ledger, "product_made", lambda cfg, playlist_id: False)
    monkeypatch.setattr(tidal_account.pairs, "paired", lambda cfg, playlist_id: True)
    return Client()


def adapter(client: Client) -> tidal_account.TidalAccount:
    return tidal_account.TidalAccount(client, sleep=lambda seconds: None, cfg=object())


def ids(start: int, count: int) -> list[str]:
    return [str(index) for index in range(start, start + count)]


@pytest.mark.parametrize(("count", "requests"), [(0, 1), (1, 1), (99, 1), (100, 2), (101, 2), (250, 3)])
def test_a_listings_pages_are_what_the_listing_seam_asks(client, count, requests):
    client.members["acc"] = ids(1, count)
    listing.playlist_tracks(Playlist(client.counter, "acc", client.members["acc"]))
    assert client.counter.requests == requests == pair_calls.pages(count)


def test_the_estimators_chunks_are_the_adapters():
    assert pair_calls.ADD_CHUNK == tidal_account.ADD_CHUNK
    assert pair_calls.REMOVE_CHUNK == tidal_account.REMOVE_CHUNK
    assert pair_calls.PLAYLIST_PAGE == listing.PAGE_SIZES["playlist_tracks"]


@pytest.mark.parametrize("count", [0, 1, 150, 201])
def test_a_made_playlist_filled_costs_its_make_and_its_fill(client, count):
    account = adapter(client)
    made = account.create_playlist("GIG READY Opener")
    account.move_to_folder(made, "folder-1")
    account.add_tracks(made, tuple(ids(1, count)))
    account.playlist_tracks(made)
    expected = pair_calls.MAKE_PLAYLIST + pair_calls.account_write((), adds=ids(1, count), made=True)
    assert client.counter.requests == expected


@pytest.mark.parametrize(
    ("held", "removes", "adds"),
    [
        (250, 60, 120),
        (40, 0, 3),
        (40, 5, 0),
        (120, 51, 0),
        (0, 0, 2),
    ],
)
def test_an_existing_playlists_removals_and_additions_cost_what_is_expected(
    client, held, removes, adds
):
    before = ids(1, held)
    client.members["acc"] = list(before)
    account = adapter(client)
    taking = tuple(before[:removes])
    adding = tuple(ids(1000, adds))
    if taking:
        account.remove_tracks("acc", taking)
    if adding:
        account.add_tracks("acc", adding)
    account.playlist_tracks("acc")
    expected = pair_calls.account_write(before, adds=adding, removes=taking, listed=False)
    assert client.counter.requests == expected


@pytest.mark.parametrize(
    ("before", "order"),
    [
        (["1", "2", "3", "4"], ["1", "2", "3", "4"]),
        (["1", "2", "3", "4"], ["2", "1", "3", "4"]),
        (["1", "2", "3", "4"], ["4", "3", "2", "1"]),
        (ids(1, 130), list(reversed(ids(1, 130)))[:5] + ids(1, 125)),
    ],
)
def test_an_order_costs_its_read_and_one_move_and_read_back_per_track_moved(
    client, before, order
):
    client.members["acc"] = list(before)
    account = adapter(client)
    account.order_tracks("acc", tuple(order))
    assert client.counter.requests == pair_calls.account_write(before, order=order)


def test_a_playlist_with_nothing_to_write_costs_nothing_once_the_check_listed_it():
    assert pair_calls.account_write(ids(1, 300)) == 0
    assert pair_calls.account_write(ids(1, 300), listed=False) == pair_calls.listing_calls(300)


def test_the_named_calls_carry_a_margin_round_up_and_never_fall_below_the_line():
    assert pair_calls.named(27, 10) == 100
    assert pair_calls.named(800, 5000) == 5000
    assert pair_calls.named(4100, 5000) == 5200
    assert pair_calls.named(0, 10) == 10
