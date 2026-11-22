"""Sync twins, release and the unread tracks of a pair: the suite's own tests, driven through the stage (U304).

As ``sync_pair.py`` does, on the world the twins suite builds: a twin planned
and backfilled, an abort, a twin whose playlist went, a twin's held tracks and
their release, and a pair listing a track it cannot read. Then the plan as a
person reads it.
"""

from __future__ import annotations

from tests import test_sync_pair_unread, test_sync_twins, test_sync_twins_hold
from tests.behaviour.sync import borrowed
from tests.test_sync_twins import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_sync_twins import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_sync_twins import cfg as cfg  # noqa: PLC0414
from tests.test_sync_twins import db as db  # noqa: PLC0414
from tests.test_sync_twins import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_sync_twins import ladder_waits as ladder_waits  # noqa: PLC0414
from tests.test_sync_twins import library as library  # noqa: PLC0414
from tests.test_sync_twins import world as world  # noqa: PLC0414


def test_a_downloaded_playlist_plans_its_twin_with_the_owned_rows_and_names_the_rest(
    stage, monkeypatch, world
):
    borrowed(stage, monkeypatch)
    test_sync_twins.test_a_downloaded_playlist_plans_its_twin_with_the_owned_rows_and_names_the_rest(
        world
    )
    stage.crate(*("sync", "twins"))


def test_the_backfill_makes_the_folder_and_twin_in_the_accounts_order_and_pairs_it(
    stage, monkeypatch, world, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_twins.test_the_backfill_makes_the_folder_and_twin_in_the_accounts_order_and_pairs_it(
        world, cfg
    )
    stage.crate(*("sync", "twins"))


def test_an_abort_writes_nothing_and_pairs_nothing(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_twins.test_an_abort_writes_nothing_and_pairs_nothing(world, cfg)
    stage.crate(*("sync", "twins"))


def test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once(
    stage, monkeypatch, world, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_twins.test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once(
        world, cfg
    )
    stage.crate(*("sync", "twins"))


def test_a_twin_whose_account_playlist_is_deleted_is_unpaired_and_left_named(
    stage, monkeypatch, world, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_twins.test_a_twin_whose_account_playlist_is_deleted_is_unpaired_and_left_named(
        world, cfg
    )
    stage.crate(*("sync", "twins"))


def test_a_folder_made_after_the_approval_refuses_as_stale(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_twins.test_a_folder_made_after_the_approval_refuses_as_stale(world, cfg)
    stage.crate(*("sync", "twins"))


def test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned(
    stage, monkeypatch, world, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_twins.test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned(
        world, cfg
    )
    stage.crate(*("sync", "twins"))


def test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold(
    stage, monkeypatch, world, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_twins_hold.test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold(
        world, cfg
    )
    stage.crate(*("sync", "twins"))


def test_releasing_the_twin_queues_its_three_at_the_next_sync(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_twins_hold.test_releasing_the_twin_queues_its_three_at_the_next_sync(world, cfg)
    stage.crate(*("sync", "twins"))


def test_release_all_lets_every_twin_go(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_twins_hold.test_release_all_lets_every_twin_go(world, cfg)
    stage.crate(*("sync", "twins"))


def test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_twins_hold.test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned(world, cfg)
    stage.crate(*("sync", "twins"))


def test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways(
    stage, monkeypatch, world, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_pair_unread.test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways(
        world, cfg
    )
    stage.crate(*("sync", "twins"))


def test_a_track_turning_unreadable_between_the_plan_and_the_write_refuses_stale(
    stage, monkeypatch, world, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_pair_unread.test_a_track_turning_unreadable_between_the_plan_and_the_write_refuses_stale(
        world, cfg
    )
    stage.crate(*("sync", "twins"))
