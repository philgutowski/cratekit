"""Sync pair's scenarios over every pair it finds: the suite's own tests, driven through the stage (U304).

As ``sync_pair.py`` does, on the world the discovery suite builds: a playlist
found and made on the other side, an order settling late and finished, a write
stopped part way and continued, an adopted folder, a window that lags, a
playlist brought back. Then the plan as a person reads it.
"""

from __future__ import annotations

from tests import (
    test_sync_pair_adopted,
    test_sync_pair_back,
    test_sync_pair_discover,
    test_sync_pair_settle,
    test_sync_pair_window_lag,
)
from tests.behaviour.sync import borrowed
from tests.test_sync_pair_adopted import trivia as trivia  # noqa: PLC0414
from tests.test_sync_pair_back import gig as gig  # noqa: PLC0414
from tests.test_sync_pair_discover import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_sync_pair_discover import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_sync_pair_discover import cfg as cfg  # noqa: PLC0414
from tests.test_sync_pair_discover import db as db  # noqa: PLC0414
from tests.test_sync_pair_discover import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_sync_pair_discover import library as library  # noqa: PLC0414
from tests.test_sync_pair_discover import world as world  # noqa: PLC0414
from tests.test_sync_pair_settle import longer as longer  # noqa: PLC0414
from tests.test_sync_pair_settle import owed as owed  # noqa: PLC0414


def test_a_gig_ready_playlist_is_made_on_the_account_in_its_folder_and_filled(
    stage, monkeypatch, world, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_pair_discover.test_a_gig_ready_playlist_is_made_on_the_account_in_its_folder_and_filled(
        world, cfg
    )
    stage.crate(*("sync", "pair"))


def test_a_second_run_plans_nothing(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair_discover.test_a_second_run_plans_nothing(world)
    stage.crate(*("sync", "pair"))


def test_two_playlists_taking_one_title_refuse_that_title_only(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair_discover.test_two_playlists_taking_one_title_refuse_that_title_only(world)
    stage.crate(*("sync", "pair"))


def test_skipping_rekordbox_makes_the_account_side_and_the_next_sync_finishes(
    stage, monkeypatch, world, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_pair_discover.test_skipping_rekordbox_makes_the_account_side_and_the_next_sync_finishes(
        world, cfg
    )
    stage.crate(*("sync", "pair"))


def test_an_order_the_provider_serves_at_once_finishes_in_the_one_run(
    stage, monkeypatch, world, owed, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_pair_settle.test_an_order_the_provider_serves_at_once_finishes_in_the_one_run(
        world, owed, cfg
    )
    stage.crate(*("sync", "pair"))


def test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok(
    stage, monkeypatch, world, owed, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_pair_settle.test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok(
        world, owed, cfg
    )
    stage.crate(*("sync", "pair"))


def test_a_late_order_finishes_in_the_next_run_with_no_rekordbox_write_between(
    stage, monkeypatch, world, owed, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_pair_settle.test_a_late_order_finishes_in_the_next_run_with_no_rekordbox_write_between(
        world, owed, cfg
    )
    stage.crate(*("sync", "pair"))


def test_a_stop_part_way_then_a_continue_sends_no_move_again(stage, monkeypatch, world, owed, cfg):
    borrowed(stage, monkeypatch)
    test_sync_pair_settle.test_a_stop_part_way_then_a_continue_sends_no_move_again(
        world, owed, cfg, monkeypatch
    )
    stage.crate(*("sync", "pair"))


def test_the_adoption_records_what_the_folder_held(stage, monkeypatch, world, cfg, trivia):
    borrowed(stage, monkeypatch)
    test_sync_pair_adopted.test_the_adoption_records_what_the_folder_held(world, cfg, trivia)
    stage.crate(*("sync", "pair"))


def test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made(
    stage, monkeypatch, world, trivia
):
    borrowed(stage, monkeypatch)
    test_sync_pair_adopted.test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made(
        world, trivia
    )
    stage.crate(*("sync", "pair"))


def test_a_window_that_serves_an_old_order_plans_no_rekordbox_order(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_pair_window_lag.test_a_window_that_serves_an_old_order_plans_no_rekordbox_order(
        world, monkeypatch, cfg
    )
    stage.crate(*("sync", "pair"))


def test_a_named_pair_whose_window_lags_refuses_as_itself(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair_window_lag.test_a_named_pair_whose_window_lags_refuses_as_itself(
        world, monkeypatch
    )
    stage.crate(*("sync", "pair"))


def test_a_playlist_made_on_the_account_in_gig_ready_lands_in_its_folder_and_is_paired(
    stage, monkeypatch, world, cfg, gig
):
    borrowed(stage, monkeypatch)
    test_sync_pair_back.test_a_playlist_made_on_the_account_in_gig_ready_lands_in_its_folder_and_is_paired(
        world, cfg, gig
    )
    stage.crate(*("sync", "pair"))


def test_a_made_pair_whose_rekordbox_playlist_is_deleted_releases_its_account_playlist(
    stage, monkeypatch, world, cfg, gig
):
    borrowed(stage, monkeypatch)
    test_sync_pair_back.test_a_made_pair_whose_rekordbox_playlist_is_deleted_releases_its_account_playlist(
        world, cfg, gig
    )
    stage.crate(*("sync", "pair"))


def test_a_missing_track_is_queued_once_and_then_awaits(stage, monkeypatch, world, gig):
    borrowed(stage, monkeypatch)
    test_sync_pair_back.test_a_missing_track_is_queued_once_and_then_awaits(world, gig)
    stage.crate(*("sync", "pair"))
