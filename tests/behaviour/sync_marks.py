"""Sync mark, unmark, strip and the taken ledger: the suite's own tests, driven through the stage (U304).

As ``sync_pair.py`` does, on the slim installation the marks suites build: a
pass marked after its answer, a playlist held back, a refusal before the gate,
an answer gone stale, the marks put back, the prefixes stripped and the
migration recorded.
"""

from __future__ import annotations

from tests import test_sync_mark, test_sync_unmark, test_u242_taken
from tests.behaviour.sync import borrowed
from tests.test_sync_mark import fresh_cache as fresh_cache  # noqa: PLC0414
from tests.test_sync_mark import slim as slim  # noqa: PLC0414


def test_a_landed_pass_marks_its_playlists_only_after_the_answer(stage, monkeypatch, slim):
    borrowed(stage, monkeypatch)
    test_sync_mark.test_a_landed_pass_marks_its_playlists_only_after_the_answer(slim, monkeypatch)


def test_a_playlist_with_one_row_not_landed_is_not_marked(stage, monkeypatch, slim):
    borrowed(stage, monkeypatch)
    test_sync_mark.test_a_playlist_with_one_row_not_landed_is_not_marked(slim, monkeypatch)


def test_a_missing_intake_file_refuses_the_verb_before_anything_is_listed(stage, monkeypatch, slim):
    borrowed(stage, monkeypatch)
    test_sync_mark.test_a_missing_intake_file_refuses_the_verb_before_anything_is_listed(
        slim, monkeypatch
    )


def test_an_answer_to_one_plan_does_not_carry_out_another(stage, monkeypatch, slim):
    borrowed(stage, monkeypatch)
    test_sync_mark.test_an_answer_to_one_plan_does_not_carry_out_another(slim, monkeypatch)


def test_a_playlist_renamed_after_the_plan_was_shown_is_skipped_and_said(stage, monkeypatch, slim):
    borrowed(stage, monkeypatch)
    test_sync_mark.test_a_playlist_renamed_after_the_plan_was_shown_is_skipped_and_said(
        slim, monkeypatch
    )


def test_an_abort_renames_nothing(stage, monkeypatch, slim):
    borrowed(stage, monkeypatch)
    test_sync_mark.test_an_abort_renames_nothing(slim, monkeypatch)


def test_a_pass_that_marked_three_plans_three_renames_back_and_applies_them(
    stage, monkeypatch, slim
):
    borrowed(stage, monkeypatch)
    test_sync_unmark.test_a_pass_that_marked_three_plans_three_renames_back_and_applies_them(
        slim, monkeypatch
    )


def test_a_playlist_the_pass_never_marked_is_refused_whatever_its_title(stage, monkeypatch, slim):
    borrowed(stage, monkeypatch)
    test_sync_unmark.test_a_playlist_the_pass_never_marked_is_refused_whatever_its_title(
        slim, monkeypatch
    )


def test_an_answer_is_stale_once_the_account_moves(stage, monkeypatch, slim):
    borrowed(stage, monkeypatch)
    test_sync_unmark.test_an_answer_is_stale_once_the_account_moves(slim, monkeypatch)


def test_an_unreadable_record_refuses_the_mark_before_its_gate(stage, monkeypatch, slim):
    borrowed(stage, monkeypatch)
    test_sync_unmark.test_an_unreadable_record_refuses_the_mark_before_its_gate(slim, monkeypatch)


def test_the_migration_records_every_prefix_and_standing_mark_once_and_says_how_many(
    stage, monkeypatch, slim
):
    borrowed(stage, monkeypatch)
    test_u242_taken.test_the_migration_records_every_prefix_and_standing_mark_once_and_says_how_many(
        slim, monkeypatch
    )


def test_a_collision_is_refused_and_named_and_the_rest_strip(stage, monkeypatch, slim):
    borrowed(stage, monkeypatch)
    test_u242_taken.test_a_collision_is_refused_and_named_and_the_rest_strip(slim, monkeypatch)


def test_the_gate_screen_lists_every_rename_and_every_refusal(stage, monkeypatch, slim):
    borrowed(stage, monkeypatch)
    test_u242_taken.test_the_gate_screen_lists_every_rename_and_every_refusal(slim, monkeypatch)


def test_every_old_title_is_restored_by_unmark_of_the_strip(stage, monkeypatch, slim):
    borrowed(stage, monkeypatch)
    test_u242_taken.test_every_old_title_is_restored_by_unmark_of_the_strip(slim, monkeypatch)
