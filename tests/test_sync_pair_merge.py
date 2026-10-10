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
