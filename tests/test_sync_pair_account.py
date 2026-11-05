"""U130's two account changes over a stand in for the client, and the pairs record.

The removal guard (R-836) now admits a playlist the author paired as well as one
the product made, and nothing else. ``order_tracks`` is held to the same guard,
moves each track to the front in turn (U220) and reads back after each move.
"""

from __future__ import annotations

import pytest

from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.modules.outbound import pairs, tidal_account
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414 - fixture
from tests.test_prune import _Client, _made, _Playlist, _Store


class _Movable(_Playlist):
    """The prune suite's playlist, able to move one position to another."""

    def move_by_indices(self, indices, position) -> bool:
        asked = list(indices)
        self.store.moves.append((self.id, tuple(asked), position))
        if self.store.misplace:
            self.store.misplace = False
            return True
        members = self.store.members[self.id]
        moving = [members[i] for i in asked]
        kept = [one for i, one in enumerate(members) if i not in set(asked)]
        at = len(kept) if position >= len(members) else position
        self.store.members[self.id] = [*kept[:at], *moving, *kept[at:]]
        return True


class _MovableClient(_Client):
    def playlist(self, playlist_id: str) -> _Movable:
        self.store.opened.append(playlist_id)
        return _Movable(self.store, playlist_id)


def _store() -> _Store:
    store = _Store()
    store.moves = []
    store.misplace = False
    return store


def _adapter(cfg, store: _Store) -> tidal_account.TidalAccount:
    return tidal_account.TidalAccount(_MovableClient(store), sleep=lambda seconds: None, cfg=cfg)


def _paired(cfg, store: _Store, playlist_id: str, members: list[str]) -> None:
    pairs.PairStore(cfg).mark(playlist_id, f"rb-{playlist_id}", name="Mine")
    store.members[playlist_id] = list(members)


def test_a_paired_playlist_takes_a_removal(installed):
    store = _store()
    _paired(installed, store, "mine", ["a", "b", "c"])
    assert _adapter(installed, store).remove_tracks("mine", ("b",)) == ("b",)
    assert store.members["mine"] == ["a", "c"]


def test_an_unpaired_playlist_of_the_author_is_still_refused_before_any_call(installed):
    store = _store()
    _paired(installed, store, "mine", ["a"])
    store.members["theirs"] = ["a", "b"]
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, store).remove_tracks("theirs", ("a",))
    assert refused.value.cause.reason == "outbound-remove-refused"
    assert refused.value.cause.detail["problem"] == "not-product-made"
    assert store.opened == [] and store.removals == []


def test_a_paired_playlist_is_never_removed_whole(installed):
    store = _store()
    _paired(installed, store, "mine", ["a"])
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, store).remove_playlist("mine")
    assert refused.value.cause.reason == "outbound-remove-refused"
    assert store.opened == []


def test_the_order_moves_each_track_to_the_front_and_reads_back(installed):
    store = _store()
    _paired(installed, store, "mine", ["a", "b", "c", "d"])
    after = _adapter(installed, store).order_tracks("mine", ("a", "d", "b", "c"))
    assert after == ("a", "d", "b", "c")
    assert store.members["mine"] == ["a", "d", "b", "c"]
    # "b" and "c" already stand in order at the tail of the asked order (U220);
    # only what comes before them is moved, the last first, each to the front.
    assert [(asked, to) for _pid, asked, to in store.moves] == [((3,), 0), ((1,), 0)]


def test_an_order_already_standing_sends_nothing(installed):
    store = _store()
    _paired(installed, store, "mine", ["a", "b"])
    assert _adapter(installed, store).order_tracks("mine", ("a", "b")) == ("a", "b")
    assert store.moves == []


def test_the_order_of_an_unpaired_playlist_is_refused_before_any_call(installed):
    store = _store()
    store.members["theirs"] = ["b", "a"]
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, store).order_tracks("theirs", ("a", "b"))
    assert refused.value.cause.reason == "outbound-remove-refused"
    assert store.opened == [] and store.moves == []


def test_a_move_that_landed_elsewhere_stops_the_order_with_every_track_kept(installed):
    store = _store()
    _paired(installed, store, "mine", ["a", "b", "c"])
    store.misplace = True
    with pytest.raises(CratekitError) as refused:
        _adapter(installed, store).order_tracks("mine", ("c", "b", "a"))
    assert refused.value.cause.detail["problem"] == "read-back-differs"
    assert len(store.moves) == 1
    assert sorted(store.members["mine"]) == ["a", "b", "c"]


def test_a_track_held_twice_is_not_moved(installed):
    store = _store()
    _paired(installed, store, "mine", ["a", "b", "a", "c"])
    after = _adapter(installed, store).order_tracks("mine", ("c", "a", "b"))
    # "a" is held twice, so it is not one of the moves; "b" is the asked
    # order's tail and stays, so "c" alone goes to the front (U220).
    assert after == ("c", "a", "b", "a")
    assert [asked for _pid, asked, _to in store.moves] == [(3,)]


def test_a_playlist_made_by_the_product_still_takes_the_order(installed):
    store = _store()
    _made(installed, store, "set", ["b", "a"])
    assert _adapter(installed, store).order_tracks("set", ("a", "b")) == ("a", "b")


# ═══════════════════════════════════════════════════════════════════════════
# The pairs record
# ═══════════════════════════════════════════════════════════════════════════


def test_one_account_playlist_pairs_with_one_rekordbox_playlist(installed):
    store = pairs.PairStore(installed)
    store.mark("acc", "rb1", name="Mine")
    assert store.mark("acc", "rb1", name="Mine").rekordbox_id == "rb1"
    with pytest.raises(CratekitError) as twice:
        store.mark("acc", "rb2", name="Mine")
    assert twice.value.cause.reason == "sync-pair-conflict"
    with pytest.raises(CratekitError) as shared:
        store.mark("other", "rb1", name="Other")
    assert shared.value.cause.reason == "sync-pair-conflict"


def test_a_side_recorded_alone_keeps_the_other_sides_snapshot(installed):
    store = pairs.PairStore(installed)
    store.mark("acc", "rb1", name="Mine")
    store.record("acc", account=("t1",), links={"t1": "1"})
    store.record("acc", rekordbox=(pairs.Membership("1", "m1"),), links={"t2": "2"})
    held = store.get("acc")
    assert held.account == ("t1",)
    assert held.rekordbox == (pairs.Membership("1", "m1"),)
    assert dict(held.links) == {"t1": "1", "t2": "2"}
    assert held.first is False


def test_a_marked_pair_with_no_snapshot_is_a_first_sync(installed):
    store = pairs.PairStore(installed)
    store.mark("acc", "rb1", name="Mine")
    assert store.get("acc").first is True


@pytest.mark.parametrize(
    "document",
    [
        "not json",
        '{"version": 2, "pairs": {}}',
        '{"version": 1, "library_id": "another", "pairs": {}}',
        '{"version": 1, "library_id": "@", "pairs": {"acc": {"rekordbox_id": ""}}}',
        '{"version": 1, "library_id": "@", "pairs": {"acc": {"rekordbox_id": "r", '
        '"account": [1]}}}',
        '{"version": 1, "library_id": "@", "pairs": {"acc": {"rekordbox_id": "r", '
        '"rekordbox": [["1"]]}}}',
    ],
)
def test_an_unreadable_pairs_document_refuses_rather_than_reading_as_empty(installed, document):
    path = config.state_path("playlist_pairs", installed)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document.replace("@", installed.library.volume_id))
    with pytest.raises(CratekitError) as refused:
        pairs.PairStore(installed).all()
    assert refused.value.cause.reason == "sync-pair-store-unusable"


def test_paired_answers_no_without_a_configuration_or_an_identifier(installed):
    pairs.PairStore(installed).mark("acc", "rb1", name="Mine")
    assert pairs.paired(installed, "acc") is True
    assert pairs.paired(None, "acc") is False
    assert pairs.paired(installed, "") is False
    assert pairs.paired(installed, "other") is False
