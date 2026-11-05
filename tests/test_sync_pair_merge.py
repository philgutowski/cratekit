"""U130's merge, pure: the last sync, the account now, rekordbox now, and the list both should hold.

Every scenario the brief names, at the level of keys, where each rule is one
assertion and no database, account or gate stands between the rule and the
answer. ``tests/test_sync_pair.py`` drives the same scenarios through the verb.
"""

from __future__ import annotations

from cratekit.sync import pair_merge
from cratekit.sync.pair_merge import Base, Side, merge


def test_the_first_sync_adds_only_and_keeps_every_track_either_side_holds():
    merged = merge(None, Side(("a", "b")), Side(("b", "c")))
    assert merged.first is True
    assert merged.order == ("a", "b", "c")
    assert merged.add_account == ("c",)
    assert merged.add_rekordbox == ("a",)
    assert merged.remove_account == () and merged.remove_rekordbox == ()


def test_a_track_added_on_the_account_only_is_added_in_rekordbox():
    base = Base(account=("a", "b"), rekordbox=("a", "b"))
    merged = merge(base, Side(("a", "x", "b")), Side(("a", "b")))
    assert merged.add_rekordbox == ("x",)
    assert merged.order == ("a", "x", "b")
    assert merged.add_account == () and merged.remove_account == ()
    assert merged.remove_rekordbox == ()


def test_a_track_added_in_rekordbox_only_is_added_on_the_account():
    base = Base(account=("a", "b"), rekordbox=("a", "b"))
    merged = merge(base, Side(("a", "b")), Side(("a", "b", "y")))
    assert merged.add_account == ("y",)
    assert merged.order == ("a", "b", "y")
    assert merged.add_rekordbox == ()


def test_a_track_removed_on_one_side_is_removed_on_the_other():
    base = Base(account=("a", "b", "c"), rekordbox=("a", "b", "c"))
    on_account = merge(base, Side(("a", "c")), Side(("a", "b", "c")))
    assert on_account.remove_rekordbox == ("b",)
    assert on_account.order == ("a", "c")
    in_rekordbox = merge(base, Side(("a", "b", "c")), Side(("a", "c")))
    assert in_rekordbox.remove_account == ("b",)
    assert in_rekordbox.order == ("a", "c")


def test_a_track_removed_on_both_sides_is_simply_gone():
    base = Base(account=("a", "b"), rekordbox=("a", "b"))
    merged = merge(base, Side(("a",)), Side(("a",)))
    assert merged.order == ("a",)
    assert merged.changes == 0


def test_a_removal_on_one_side_and_a_re_add_on_the_other_keeps_the_track():
    base = Base(account=("a", "b"), rekordbox=("a", "b"))
    merged = merge(base, Side(("a",)), Side(("a", "b"), readded=frozenset({"b"})))
    assert "b" in merged.order
    assert merged.add_account == ("b",)
    assert merged.remove_rekordbox == ()
    assert merged.readded_over_removal == ("b",)


def test_a_re_add_across_two_syncs_is_an_addition_like_any_other():
    """Removed on the account at one sync, put back in rekordbox before the next."""
    base = Base(account=("a",), rekordbox=("a",))
    merged = merge(base, Side(("a",)), Side(("a", "b")))
    assert merged.add_account == ("b",)


def test_a_track_both_sides_still_hold_is_kept_whatever_the_bases_say():
    merged = merge(Base(account=(), rekordbox=()), Side(("a",)), Side(("a",)))
    assert merged.order == ("a",)
    assert merged.changes == 0


def test_when_both_sides_reordered_the_account_order_wins():
    base = Base(account=("a", "b", "c"), rekordbox=("a", "b", "c"))
    merged = merge(base, Side(("c", "b", "a")), Side(("b", "a", "c")))
    assert merged.leader == pair_merge.ACCOUNT
    assert merged.order == ("c", "b", "a")


def test_when_rekordbox_alone_reordered_its_order_wins():
    base = Base(account=("a", "b", "c"), rekordbox=("a", "b", "c"))
    merged = merge(base, Side(("a", "b", "c")), Side(("c", "a", "b")))
    assert merged.leader == pair_merge.REKORDBOX
    assert merged.order == ("c", "a", "b")


def test_when_the_account_alone_reordered_its_order_wins():
    base = Base(account=("a", "b", "c"), rekordbox=("a", "b", "c"))
    merged = merge(base, Side(("b", "c", "a")), Side(("a", "b", "c")))
    assert merged.leader == pair_merge.ACCOUNT
    assert merged.order == ("b", "c", "a")


def test_a_track_added_mid_list_on_the_other_side_keeps_its_place():
    base = Base(account=("a", "b", "c"), rekordbox=("a", "b", "c"))
    merged = merge(base, Side(("a", "b", "c")), Side(("a", "y", "b", "c")))
    assert merged.order == ("a", "y", "b", "c")


def test_a_run_of_new_tracks_at_the_head_of_the_other_side_keeps_its_own_order():
    assert pair_merge.placed(("a", "b"), ("x", "y", "a")) == ("x", "y", "a", "b")


def test_an_addition_is_kept_when_the_other_side_dropped_its_neighbour():
    base = Base(account=("a", "b"), rekordbox=("a", "b"))
    merged = merge(base, Side(("b",)), Side(("a", "z", "b")))
    assert merged.order == ("z", "b")
    assert merged.remove_rekordbox == ("a",)
    assert merged.add_account == ("z",)


def test_a_side_with_no_base_of_its_own_reads_every_track_as_added():
    """The account half of the first sync was skipped: its base is empty."""
    base = Base(account=(), rekordbox=("a", "b"))
    merged = merge(base, Side(("a", "c")), Side(("a",)))
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


# ═══════════════════════════════════════════════════════════════════════════
# U202: the later of two opposite changes wins
# ═══════════════════════════════════════════════════════════════════════════

from datetime import datetime, timedelta, timezone  # noqa: E402

from cratekit.sync.pair_merge import (  # noqa: E402
    ACCOUNT,
    ADDITION_LATER,
    REKORDBOX,
    REMOVAL_LATER,
    TIME_UNKNOWN,
)

SYNCED = datetime(2026, 11, 4, 12, 0, tzinfo=timezone.utc)


def at(minutes: int) -> datetime:
    return SYNCED + timedelta(minutes=minutes)


def test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both():
    base = Base(account=("a", "b"), rekordbox=("a", "b"), synced=SYNCED)
    merged = merge(
        base,
        Side(("a", "b"), frozenset({"b"}), added_at={"b": at(20)}),
        Side(("a",), removed_at={"b": at(10)}),
    )
    assert merged.order == ("a", "b")
    assert merged.add_rekordbox == ("b",)
    assert merged.remove_account == ()
    (call,) = merged.calls
    assert (call.key, call.added_on, call.outcome) == ("b", ACCOUNT, ADDITION_LATER)
    assert call.removed_on == REKORDBOX and call.kept


def test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both():
    base = Base(account=("a", "b"), rekordbox=("a", "b"), synced=SYNCED)
    merged = merge(
        base,
        Side(("a", "b"), frozenset({"b"}), added_at={"b": at(10)}),
        Side(("a",), removed_at={"b": at(20)}),
    )
    assert merged.order == ("a",)
    assert merged.remove_account == ("b",)
    assert merged.add_rekordbox == ()
    assert merged.readded_over_removal == ()
    (call,) = merged.calls
    assert call.outcome == REMOVAL_LATER and not call.kept


def test_an_account_addition_later_than_a_rekordbox_removal_is_added_back_there():
    base = Base(account=("a",), rekordbox=("a", "b"), synced=SYNCED)
    merged = merge(
        base,
        Side(("a", "b"), added_at={"b": at(30)}),
        Side(("a",), removed_at={"b": at(5)}),
    )
    assert merged.add_rekordbox == ("b",)
    assert merged.calls[0].outcome == ADDITION_LATER


def test_a_removal_with_no_moment_never_beats_an_addition_and_is_called_unknown():
    base = Base(account=("a", "b"), rekordbox=("a", "b"), synced=SYNCED)
    merged = merge(
        base,
        Side(("a", "b"), frozenset({"b"}), added_at={"b": at(10)}),
        Side(("a",)),
    )
    assert merged.order == ("a", "b") and merged.add_rekordbox == ("b",)
    (call,) = merged.calls
    assert call.outcome == TIME_UNKNOWN and call.removed_at is None and call.kept
    assert merged.readded_over_removal == ("b",)


def test_an_account_removal_never_beats_a_rekordbox_addition():
    base = Base(account=("a", "b"), rekordbox=("a", "b"), synced=SYNCED)
    merged = merge(
        base,
        Side(("a",)),
        Side(("a", "b"), frozenset({"b"}), added_at={"b": at(1)}),
    )
    assert merged.add_account == ("b",)
    (call,) = merged.calls
    assert (call.added_on, call.outcome) == (REKORDBOX, TIME_UNKNOWN)


def test_a_moment_at_or_before_the_base_sync_is_no_moment():
    base = Base(account=("a", "b"), rekordbox=("a", "b"), synced=SYNCED)
    for removed in (SYNCED, at(-5)):
        merged = merge(
            base,
            Side(("a", "b"), frozenset({"b"}), added_at={"b": at(10)}),
            Side(("a",), removed_at={"b": removed}),
        )
        assert merged.calls[0].outcome == TIME_UNKNOWN, removed
        assert merged.remove_account == ()
    merged = merge(
        base,
        Side(("a", "b"), frozenset({"b"}), added_at={"b": SYNCED}),
        Side(("a",), removed_at={"b": at(20)}),
    )
    assert merged.calls[0].added_at is None and merged.calls[0].kept


def test_a_moment_with_no_zone_is_no_moment():
    base = Base(account=("a", "b"), rekordbox=("a", "b"), synced=SYNCED)
    merged = merge(
        base,
        Side(("a", "b"), frozenset({"b"}), added_at={"b": at(10)}),
        Side(("a",), removed_at={"b": at(20).replace(tzinfo=None)}),
    )
    assert merged.calls[0].outcome == TIME_UNKNOWN
    assert merged.remove_account == ()


def test_a_tie_keeps_the_track():
    base = Base(account=("a", "b"), rekordbox=("a", "b"), synced=SYNCED)
    merged = merge(
        base,
        Side(("a", "b"), frozenset({"b"}), added_at={"b": at(10)}),
        Side(("a",), removed_at={"b": at(10)}),
    )
    assert merged.calls[0].outcome == ADDITION_LATER and merged.add_rekordbox == ("b",)


def test_a_base_with_no_sync_moment_still_orders_two_known_moments():
    base = Base(account=("a", "b"), rekordbox=("a", "b"))
    merged = merge(
        base,
        Side(("a", "b"), frozenset({"b"}), added_at={"b": at(10)}),
        Side(("a",), removed_at={"b": at(20)}),
    )
    assert merged.calls[0].outcome == REMOVAL_LATER


def test_a_track_put_back_on_the_account_with_nothing_removed_is_no_call():
    base = Base(account=("a", "b"), rekordbox=("a", "b"), synced=SYNCED)
    merged = merge(
        base,
        Side(("a", "b"), frozenset({"b"}), added_at={"b": at(10)}),
        Side(("a", "b")),
    )
    assert merged.calls == () and merged.changes == 0


def test_moments_change_nothing_where_no_side_both_added_and_removed():
    base = Base(account=("a", "b"), rekordbox=("a", "b"), synced=SYNCED)
    merged = merge(
        base,
        Side(("a",), added_at={"a": at(1)}),
        Side(("a", "b"), added_at={"b": at(99)}, removed_at={"b": at(1)}),
    )
    assert merged.remove_rekordbox == ("b",) and merged.calls == ()


def test_the_first_sync_makes_no_call_whatever_the_moments():
    merged = merge(
        None,
        Side(("a",), added_at={"a": at(1)}),
        Side(("b",), removed_at={"a": at(9)}),
    )
    assert merged.calls == () and set(merged.order) == {"a", "b"}
