"""U130's merge, pure: the last sync, the account now, rekordbox now, and the list both should hold.

Each rule is one assertion on keys, with no database, account or gate between;
``tests/test_sync_pair.py`` drives the same scenarios through the verb.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from cratekit.sync import pair_merge
from cratekit.sync.pair_merge import (
    ACCOUNT,
    ADDITION_LATER,
    REKORDBOX,
    REMOVAL_LATER,
    TIME_UNKNOWN,
    Base,
    Side,
    merge,
)


def _base(account: str, rekordbox: str, **kwargs) -> Base:
    """A base of one letter keys, ``"abc"`` for ``("a", "b", "c")``."""
    return Base(account=tuple(account), rekordbox=tuple(rekordbox), **kwargs)


def test_the_first_sync_adds_only_and_keeps_every_track_either_side_holds():
    merged = merge(None, Side(("a", "b")), Side(("b", "c")))
    assert merged.first is True
    assert merged.order == ("a", "b", "c")
    assert merged.add_account == ("c",)
    assert merged.add_rekordbox == ("a",)
    assert merged.remove_account == () and merged.remove_rekordbox == ()


def test_a_track_added_on_the_account_only_is_added_in_rekordbox():
    merged = merge(_base("ab", "ab"), Side(("a", "x", "b")), Side(("a", "b")))
    assert merged.add_rekordbox == ("x",)
    assert merged.order == ("a", "x", "b")
    assert merged.add_account == () and merged.remove_account == ()
    assert merged.remove_rekordbox == ()


def test_a_track_added_in_rekordbox_only_is_added_on_the_account():
    merged = merge(_base("ab", "ab"), Side(("a", "b")), Side(("a", "b", "y")))
    assert merged.add_account == ("y",)
    assert merged.order == ("a", "b", "y")
    assert merged.add_rekordbox == ()


def test_a_track_removed_on_one_side_is_removed_on_the_other():
    base = _base("abc", "abc")
    on_account = merge(base, Side(("a", "c")), Side(("a", "b", "c")))
    assert on_account.remove_rekordbox == ("b",)
    assert on_account.order == ("a", "c")
    in_rekordbox = merge(base, Side(("a", "b", "c")), Side(("a", "c")))
    assert in_rekordbox.remove_account == ("b",)
    assert in_rekordbox.order == ("a", "c")


def test_a_track_removed_on_both_sides_is_simply_gone():
    merged = merge(_base("ab", "ab"), Side(("a",)), Side(("a",)))
    assert merged.order == ("a",)
    assert merged.changes == 0


def test_a_removal_on_one_side_and_a_re_add_on_the_other_keeps_the_track():
    merged = merge(_base("ab", "ab"), Side(("a",)), Side(("a", "b"), readded=frozenset({"b"})))
    assert "b" in merged.order
    assert merged.add_account == ("b",)
    assert merged.remove_rekordbox == ()
    assert merged.readded_over_removal == ("b",)


def test_a_re_add_across_two_syncs_is_an_addition_like_any_other():
    """Removed on the account at one sync, put back in rekordbox before the next."""
    merged = merge(_base("a", "a"), Side(("a",)), Side(("a", "b")))
    assert merged.add_account == ("b",)


def test_a_track_both_sides_still_hold_is_kept_whatever_the_bases_say():
    merged = merge(Base(account=(), rekordbox=()), Side(("a",)), Side(("a",)))
    assert merged.order == ("a",)
    assert merged.changes == 0


def test_a_track_added_mid_list_on_the_other_side_keeps_its_place():
    merged = merge(_base("abc", "abc"), Side(("a", "b", "c")), Side(("a", "y", "b", "c")))
    assert merged.order == ("a", "y", "b", "c")


def test_a_run_of_new_tracks_at_the_head_of_the_other_side_keeps_its_own_order():
    assert pair_merge.placed(("a", "b"), ("x", "y", "a")) == ("x", "y", "a", "b")


def test_an_addition_is_kept_when_the_other_side_dropped_its_neighbour():
    merged = merge(_base("ab", "ab"), Side(("b",)), Side(("a", "z", "b")))
    assert merged.order == ("z", "b")
    assert merged.remove_rekordbox == ("a",)
    assert merged.add_account == ("z",)


def test_a_side_with_no_base_of_its_own_reads_every_track_as_added():
    """The account half of the first sync was skipped: its base is empty."""
    merged = merge(_base("", "ab"), Side(("a", "c")), Side(("a",)))
    assert merged.order == ("a", "c")
    assert merged.add_rekordbox == ("c",)
    assert merged.remove_account == ()


def test_a_duplicate_on_one_side_is_one_track():
    merged = merge(None, Side(("a", "a", "b")), Side(("b",)))
    assert merged.order == ("a", "b")
    assert merged.add_rekordbox == ("a",)


def test_order_changed_reads_only_the_tracks_both_held():
    assert pair_merge.order_changed(("a", "x", "b"), ("a", "b")) is False
    assert pair_merge.order_changed(("b", "a"), ("a", "b", "c")) is True


def test_appended_is_removals_then_plain_appends():
    assert pair_merge.appended(("a", "b", "c"), ("b",), ("d", "a")) == ("a", "c", "d")


# U202: the later of two opposite changes wins

SYNCED = datetime(2026, 11, 4, 12, 0, tzinfo=timezone.utc)


def at(minutes: int) -> datetime:
    return SYNCED + timedelta(minutes=minutes)


def _put_back(added: datetime, removed: datetime | None, *, synced: datetime | None = SYNCED):
    """``b`` put back on the account at ``added`` and taken out in rekordbox at ``removed``."""
    removal = {} if removed is None else {"removed_at": {"b": removed}}
    return merge(
        _base("ab", "ab", synced=synced),
        Side(("a", "b"), frozenset({"b"}), added_at={"b": added}),
        Side(("a",), **removal),
    )


def test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both():
    merged = _put_back(at(20), at(10))
    assert merged.order == ("a", "b")
    assert merged.add_rekordbox == ("b",)
    assert merged.remove_account == ()
    (call,) = merged.calls
    assert (call.key, call.added_on, call.outcome) == ("b", ACCOUNT, ADDITION_LATER)
    assert call.removed_on == REKORDBOX and call.kept


def test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both():
    merged = _put_back(at(10), at(20))
    assert merged.order == ("a",)
    assert merged.remove_account == ("b",)
    assert merged.add_rekordbox == ()
    assert merged.readded_over_removal == ()
    (call,) = merged.calls
    assert call.outcome == REMOVAL_LATER and not call.kept


def test_an_account_addition_later_than_a_rekordbox_removal_is_added_back_there():
    merged = merge(
        _base("a", "ab", synced=SYNCED),
        Side(("a", "b"), added_at={"b": at(30)}),
        Side(("a",), removed_at={"b": at(5)}),
    )
    assert merged.add_rekordbox == ("b",)
    assert merged.calls[0].outcome == ADDITION_LATER


def test_a_removal_with_no_moment_never_beats_an_addition_and_is_called_unknown():
    merged = _put_back(at(10), None)
    assert merged.order == ("a", "b") and merged.add_rekordbox == ("b",)
    (call,) = merged.calls
    assert call.outcome == TIME_UNKNOWN and call.removed_at is None and call.kept
    assert merged.readded_over_removal == ("b",)


def test_an_account_removal_never_beats_a_rekordbox_addition():
    merged = merge(
        _base("ab", "ab", synced=SYNCED),
        Side(("a",)),
        Side(("a", "b"), frozenset({"b"}), added_at={"b": at(1)}),
    )
    assert merged.add_account == ("b",)
    (call,) = merged.calls
    assert (call.added_on, call.outcome) == (REKORDBOX, TIME_UNKNOWN)


def test_a_moment_at_or_before_the_base_sync_is_no_moment():
    for removed in (SYNCED, at(-5)):
        merged = _put_back(at(10), removed)
        assert merged.calls[0].outcome == TIME_UNKNOWN, removed
        assert merged.remove_account == ()
    merged = _put_back(SYNCED, at(20))
    assert merged.calls[0].added_at is None and merged.calls[0].kept


def test_a_moment_with_no_zone_is_no_moment():
    merged = _put_back(at(10), at(20).replace(tzinfo=None))
    assert merged.calls[0].outcome == TIME_UNKNOWN
    assert merged.remove_account == ()


def test_a_tie_keeps_the_track():
    merged = _put_back(at(10), at(10))
    assert merged.calls[0].outcome == ADDITION_LATER and merged.add_rekordbox == ("b",)


def test_a_base_with_no_sync_moment_still_orders_two_known_moments():
    assert _put_back(at(10), at(20), synced=None).calls[0].outcome == REMOVAL_LATER


def test_a_track_put_back_on_the_account_with_nothing_removed_is_no_call():
    merged = merge(
        _base("ab", "ab", synced=SYNCED),
        Side(("a", "b"), frozenset({"b"}), added_at={"b": at(10)}),
        Side(("a", "b")),
    )
    assert merged.calls == () and merged.changes == 0


def test_moments_change_nothing_where_no_side_both_added_and_removed():
    merged = merge(
        _base("ab", "ab", synced=SYNCED),
        Side(("a",), added_at={"a": at(1)}),
        Side(("a", "b"), added_at={"b": at(99)}, removed_at={"b": at(1)}),
    )
    assert merged.remove_rekordbox == ("b",) and merged.calls == ()


def test_the_first_sync_makes_no_call_whatever_the_moments():
    merged = merge(None, Side(("a",), added_at={"a": at(1)}), Side(("b",), removed_at={"a": at(9)}))
    assert merged.calls == () and set(merged.order) == {"a", "b"}


# U225: the order after a write stopped part way through it

#: The base, and what a stopped write left while putting rekordbox's order on the account.
_BASE = _base("abc", "abc")
_LEFT = pair_merge.Stopped(account=("c", "a", "b"), rekordbox=("c", "a", "b"), leader=REKORDBOX)
_ACCOUNT_LED = pair_merge.Stopped(account=_LEFT.account, rekordbox=_LEFT.rekordbox, leader=ACCOUNT)
#: R-1404. A pair whose account order is not kept, after rekordbox led a reorder.
_APART = _base("abc", "cab")


def _lead(*cases):
    """Each case as its old test's name, ``-`` and a part where it held two."""
    return [pytest.param(*case[1:], id=case[0]) for case in cases]


@pytest.mark.parametrize(
    ("base", "account", "rekordbox", "told", "leader", "order"),
    _lead(
        ("when_both_sides_reordered_the_account_order_wins",
         _base("abc", "abc"), "cba", "bac", {}, ACCOUNT, "cba"),
        ("when_rekordbox_alone_reordered_its_order_wins",
         _base("abc", "abc"), "abc", "cab", {}, REKORDBOX, "cab"),
        ("when_the_account_alone_reordered_its_order_wins",
         _base("abc", "abc"), "bca", "abc", {}, ACCOUNT, "bca"),
        # U225. The stopped write's order, never the base's.
        ("with_no_change_since_the_stopped_write_the_side_that_led_it_leads_again-rekordbox",
         _BASE, "cab", "cab", {"stopped": _LEFT}, REKORDBOX, None),
        ("with_no_change_since_the_stopped_write_the_side_that_led_it_leads_again-account",
         _BASE, "cab", "cab", {"stopped": _ACCOUNT_LED}, ACCOUNT, None),
        # Against the base both sides changed order, and the account would lead.
        ("the_stopped_writes_order_is_not_read_against_the_base-base",
         _BASE, "cab", "cab", {}, ACCOUNT, None),
        ("the_stopped_writes_order_is_not_read_against_the_base-stopped",
         _BASE, "cab", "cab", {"stopped": _LEFT}, REKORDBOX, None),
        ("rekordbox_reordered_since_the_stopped_write_leads",
         _BASE, "cab", "bca", {"stopped": _ACCOUNT_LED}, REKORDBOX, "bca"),
        ("the_account_reordered_since_the_stopped_write_leads_whatever_else_moved-alone",
         _BASE, "acb", "cab", {"stopped": _LEFT}, ACCOUNT, "acb"),
        ("the_account_reordered_since_the_stopped_write_leads_whatever_else_moved-both",
         _BASE, "acb", "bca", {"stopped": _LEFT}, ACCOUNT, None),
        # R-1404. A base whose two sides stand in different orders.
        ("with_no_change_since_a_base_whose_sides_disagree_rekordbox_leads",
         _APART, "abc", "cab", {}, REKORDBOX, "cab"),
        ("a_track_the_account_adds_is_placed_in_the_order_rekordbox_holds",
         _APART, "axbc", "cab", {}, REKORDBOX, "caxb"),
        ("the_account_reordered_since_a_base_whose_sides_disagree_still_leads-alone",
         _APART, "bca", "cab", {}, ACCOUNT, "bca"),
        ("the_account_reordered_since_a_base_whose_sides_disagree_still_leads-both",
         _APART, "bca", "acb", {}, ACCOUNT, None),
        ("rekordbox_reordered_since_a_base_whose_sides_disagree_leads",
         _APART, "abc", "bac", {}, REKORDBOX, "bac"),
        # Inside the order's scope nothing changes, the tie between two additions included.
        ("a_base_whose_sides_agree_leaves_the_account_leading_when_neither_side_moved",
         _base("ab", "ab"), "axb", "ayb", {}, ACCOUNT, "ayxb"),
        # A track one side alone held says nothing of whether the two orders disagree.
        ("only_the_tracks_both_sides_held_at_the_base_are_read_for_their_order-alone",
         _base("abx", "rab"), "abx", "rab", {}, ACCOUNT, None),
        ("only_the_tracks_both_sides_held_at_the_base_are_read_for_their_order-shared",
         _base("abz", "zabr"), "abz", "zabr", {}, REKORDBOX, None),
        # The same track added on both sides at two places is no disagreement at the base.
        ("the_base_s_disagreement_is_read_at_the_base_not_between_the_sides_now",
         _base("ab", "ab"), "axb", "xab", {}, ACCOUNT, "axb"),
        # A track only rekordbox held at the base decides nothing, wherever the account holds it.
        ("the_base_s_disagreement_is_read_against_the_account_s_base_not_the_account_now",
         _base("ab", "arb"), "rab", "arb", {}, ACCOUNT, "rab"),
        # R-1416. A first sync led by rekordbox only when its order is not kept.
        ("a_first_sync_whose_order_is_kept_leads_with_the_account-default",
         None, "abc", "cab", {}, ACCOUNT, "abc"),
        ("a_first_sync_whose_order_is_kept_leads_with_the_account-told",
         None, "abc", "cab", {"order_kept": True}, ACCOUNT, "abc"),
        ("a_first_sync_into_an_empty_rekordbox_side_is_led_by_the_account_whatever_the_order",
         None, "cab", "", {"order_kept": False}, ACCOUNT, "cab"),
        # Neither side changed order since the stopped write, which the account led, so
        # "c" follows "b", its predecessor in rekordbox.
        ("a_first_sync_after_a_stopped_write_reads_its_order_against_it_whatever_the_order",
         None, "ba", "abc", {"order_kept": False, "stopped": pair_merge.Stopped(
             account=("b", "a"), rekordbox=("a", "b", "c"), leader=ACCOUNT)}, ACCOUNT, "bca"),
        ("a_base_is_read_as_before_whatever_the_order-kept",
         _base("abc", "abc"), "bca", "abc", {"order_kept": True}, ACCOUNT, "bca"),
        ("a_base_is_read_as_before_whatever_the_order-not-kept",
         _base("abc", "abc"), "bca", "abc", {"order_kept": False}, ACCOUNT, "bca"),
    ),
)
def test_the_side_that_leads_the_order(base, account, rekordbox, told, leader, order):
    """Which side's order leads, and the order it gives where the old test read it."""
    merged = merge(base, Side(tuple(account)), Side(tuple(rekordbox)), **told)
    assert merged.leader == leader
    if order is not None:
        assert merged.order == tuple(order)


def test_the_stopped_write_decides_the_order_alone_and_never_membership():
    plain = merge(_BASE, Side(("c", "a", "x")), Side(("c", "a", "b", "y")))
    left = merge(_BASE, Side(("c", "a", "x")), Side(("c", "a", "b", "y")), stopped=_LEFT)
    for field in ("add_account", "remove_account", "add_rekordbox", "remove_rekordbox"):
        assert getattr(left, field) == getattr(plain, field), field


def test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it():
    left = pair_merge.Stopped(account=("b", "a"), rekordbox=("b", "a", "c"), leader=ACCOUNT)
    # Rekordbox was reordered since the stopped write, the account was not.
    assert merge(None, Side(("b", "a")), Side(("a", "b", "c"))).order == ("b", "c", "a")
    merged = merge(None, Side(("b", "a")), Side(("a", "b", "c")), stopped=left)
    assert merged.first is True
    assert merged.remove_account == () and merged.remove_rekordbox == ()
    assert merged.leader == REKORDBOX
    assert merged.order == ("a", "b", "c")


# R-1416: a first sync whose account order is not kept, led by rekordbox


def test_a_first_sync_whose_order_is_not_kept_leads_with_rekordbox():
    merged = merge(None, Side(("a", "b", "c")), Side(("c", "a", "b")), order_kept=False)
    assert merged.first is True
    assert merged.leader == REKORDBOX
    assert merged.order == ("c", "a", "b")
    assert merged.add_account == () and merged.add_rekordbox == ()


def test_a_first_sync_led_by_rekordbox_places_the_accounts_tracks_after_their_neighbours():
    merged = merge(None, Side(("a", "b", "c", "d")), Side(("c", "y", "a", "b")), order_kept=False)
    assert merged.order == ("c", "d", "y", "a", "b")
    assert merged.add_rekordbox == ("d",)
    assert merged.add_account == ("y",)
    assert merged.remove_account == () and merged.remove_rekordbox == ()
