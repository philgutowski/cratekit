"""Sync pair's scenarios on one marked pair: the suite's own tests, driven through the stage (U304).

Each scenario runs one test of the pair suites as written, with every command
it drives routed through the stage by ``tests/behaviour/sync.borrowed``, so
the capture holds each envelope, the gate it asked, and the database, the pairs
record and the held plans the verb left: a first sync, a removal and a reorder
carried across, a track queued, a skipped side finished, a short listing, a
refusal before the gate, one on a moved list and one of a label playlist, and
a held plan continued. Then the plan as a person reads it.

No tie and no ceiling stop: the ISRC cache and the provider gate stamp what
they write with a clock bound as a default argument, which the stage's pin
does not reach, so two captures of one commit differ there.
"""

from __future__ import annotations

from tests import test_sync_pair, test_sync_pair_hold
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


def test_a_track_removed_in_rekordbox_is_taken_off_the_account(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_a_track_removed_in_rekordbox_is_taken_off_the_account(world)
    stage.crate(*("sync", "pair"))


def test_when_rekordbox_alone_reorders_the_account_follows(stage, monkeypatch, world):
    borrowed(stage, monkeypatch)
    test_sync_pair.test_when_rekordbox_alone_reorders_the_account_follows(world)
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


def test_answers_continued_in_later_commands_ask_nothing_when_nothing_moved(
    stage, monkeypatch, world, counted
):
    borrowed(stage, monkeypatch)
    test_sync_pair_hold.test_answers_continued_in_later_commands_ask_nothing_when_nothing_moved(
        world, counted
    )
    stage.crate(*("sync", "pair"))
