"""Sync twins, release and a pair's unread tracks: the suite's own tests, driven through the stage (U304).

As ``sync_pair.py`` does, on the world the twins suite builds: a twin
backfilled, an abort, a twin's held tracks released, a release refused, and a
pair listing a track it cannot read. Then the plan as a person reads it.
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


def test_releasing_the_twin_queues_its_three_at_the_next_sync(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_twins_hold.test_releasing_the_twin_queues_its_three_at_the_next_sync(world, cfg)
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
