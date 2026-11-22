"""Sync pair's scenarios on one marked pair: the suite's own tests, driven through the stage (U304).

Each scenario runs one test of the pair suites as written, with every command
it drives routed through the stage by ``tests/behaviour/sync.borrowed``, so
the capture holds each envelope, the gate it asked, and the database, the pairs
record and the held plans the verb left. The states the card names: a first
sync, a merge both ways, a reorder, a refusal on a moved list, a held plan
continued, a tie, a skipped side finished. Then the plan as a person reads it.
"""

from __future__ import annotations

from tests import test_sync_pair, test_sync_pair_hold, test_sync_pair_tie
from tests.behaviour.sync import borrowed
from tests.test_sync_pair import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_sync_pair import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_sync_pair import cfg as cfg  # noqa: PLC0414
from tests.test_sync_pair import db as db  # noqa: PLC0414
from tests.test_sync_pair import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_sync_pair import library as library  # noqa: PLC0414
from tests.test_sync_pair import world as world  # noqa: PLC0414
from tests.test_sync_pair_hold import counted as counted  # noqa: PLC0414
from tests.test_sync_pair_tie import tied as tied  # noqa: PLC0414


def test_the_first_sync_marks_the_pair_and_adds_only(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_the_first_sync_marks_the_pair_and_adds_only(world, cfg)
    stage.crate(*("sync", "pair"))


def test_a_track_removed_on_the_account_leaves_the_playlist_and_stays_in_the_collection(
    stage, monkeypatch, world, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_a_track_removed_on_the_account_leaves_the_playlist_and_stays_in_the_collection(
        world, cfg
    )
    stage.crate(*("sync", "pair"))


def test_a_track_removed_in_rekordbox_is_taken_off_the_account(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_a_track_removed_in_rekordbox_is_taken_off_the_account(world)
    stage.crate(*("sync", "pair"))


def test_when_rekordbox_alone_reorders_the_account_follows(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_when_rekordbox_alone_reorders_the_account_follows(world)
    stage.crate(*("sync", "pair"))


def test_an_unmatched_rekordbox_track_is_named_and_stays_in_rekordbox(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_an_unmatched_rekordbox_track_is_named_and_stays_in_rekordbox(world)
    stage.crate(*("sync", "pair"))


def test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row(
    stage, monkeypatch, world, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row(
        world, cfg
    )
    stage.crate(*("sync", "pair"))


def test_with_no_acknowledgment_the_verb_refuses_before_the_gate(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_with_no_acknowledgment_the_verb_refuses_before_the_gate(world, cfg)
    stage.crate(*("sync", "pair"))


def test_a_skipped_account_side_is_finished_by_the_next_sync(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_a_skipped_account_side_is_finished_by_the_next_sync(world, cfg)
    stage.crate(*("sync", "pair"))


def test_both_sides_skipped_writes_nothing_and_marks_nothing(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_both_sides_skipped_writes_nothing_and_marks_nothing(world, cfg)
    stage.crate(*("sync", "pair"))


def test_a_short_account_listing_reads_nothing_as_removed(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_a_short_account_listing_reads_nothing_as_removed(world)
    stage.crate(*("sync", "pair"))


def test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale(
    stage, monkeypatch, world, cfg
):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale(
        world, cfg
    )
    stage.crate(*("sync", "pair"))


def test_a_label_playlist_is_not_a_pair(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_a_label_playlist_is_not_a_pair(world, cfg)
    stage.crate(*("sync", "pair"))


def test_a_folder_is_not_a_pair(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_a_folder_is_not_a_pair(world)
    stage.crate(*("sync", "pair"))


def test_a_second_rekordbox_playlist_for_a_paired_account_playlist_is_refused(
    stage, monkeypatch, world
):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_a_second_rekordbox_playlist_for_a_paired_account_playlist_is_refused(world)
    stage.crate(*("sync", "pair"))


def test_with_no_argument_every_marked_pair_is_synced(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_with_no_argument_every_marked_pair_is_synced(world)
    stage.crate(*("sync", "pair"))


def test_two_rows_carrying_one_isrc_add_neither_and_say_so(stage, monkeypatch, world, cfg):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_two_rows_carrying_one_isrc_add_neither_and_say_so(world, cfg)
    stage.crate(*("sync", "pair"))


def test_a_track_another_account_playlist_landed_is_added_and_never_queued(
    stage, monkeypatch, world, cfg, tmp_path
):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_a_track_another_account_playlist_landed_is_added_and_never_queued(
        world, cfg, tmp_path
    )
    stage.crate(*("sync", "pair"))


def test_answers_continued_in_later_commands_ask_nothing_when_nothing_moved(
    stage, monkeypatch, world, counted
):
    borrowed(stage, monkeypatch)
    test_sync_pair_hold.test_answers_continued_in_later_commands_ask_nothing_when_nothing_moved(
        world, counted
    )
    stage.crate(*("sync", "pair"))


def test_an_account_list_changed_before_the_write_refuses_stale_and_names_it(
    stage, monkeypatch, world
):
    borrowed(stage, monkeypatch)
    test_sync_pair_hold.test_an_account_list_changed_before_the_write_refuses_stale_and_names_it(
        world
    )
    stage.crate(*("sync", "pair"))


def test_a_replanned_run_whose_list_moved_is_refused_by_the_gate(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair_hold.test_a_replanned_run_whose_list_moved_is_refused_by_the_gate(world)
    stage.crate(*("sync", "pair"))


def test_a_withheld_count_changed_before_the_write_refuses_stale(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair_hold.test_a_withheld_count_changed_before_the_write_refuses_stale(world)
    stage.crate(*("sync", "pair"))


def test_a_tie_with_none_hearted_is_linked_to_the_lowest_release(stage, monkeypatch, tied, cfg):
    borrowed(stage, monkeypatch)
    test_sync_pair_tie.test_a_tie_with_none_hearted_is_linked_to_the_lowest_release(tied, cfg)
    stage.crate(*("sync", "pair"))


def test_the_gate_names_how_many_rows_a_broken_tie_matched(stage, monkeypatch, tied):
    borrowed(stage, monkeypatch)
    test_sync_pair_tie.test_the_gate_names_how_many_rows_a_broken_tie_matched(tied)
    stage.crate(*("sync", "pair"))


def test_both_releases_taken_off_the_account_take_the_row_out_of_rekordbox(
    stage, monkeypatch, tied
):
    borrowed(stage, monkeypatch)
    test_sync_pair_tie.test_both_releases_taken_off_the_account_take_the_row_out_of_rekordbox(tied)
    stage.crate(*("sync", "pair"))
