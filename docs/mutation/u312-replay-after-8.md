# Mutation table: u312-replay-after-8

Measured by `scripts/mutate.py` on 2026-11-23 10:40 UTC, branch `HEAD` at `55e2f3b6`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22479 collected. pytest invocations for this batch: 248.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 47, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `~/known/scratch.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22479 against 22479. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u209.C3_withheld` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C4_rekordbox_gone` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C5_memberships` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 5 | killed |
| `u209.C6_discovered_place` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 5 | killed |
| `u209.C7_made_left_behind` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C8_rows_gone` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C9_unpaired_back` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.H1_offer_mismatch_ignored` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u130-a.A1_removal_beats_addition` | `src/cratekit/sync/pair_merge.py` | user | 2 file(s) | 22479 | 0 (promoted) | zero |
| `u130-a.A6_order_change_read_inverted` | `src/cratekit/sync/pair_merge.py` | user | 2 file(s) | 126 | 18 | killed |
| `u202.M1_since` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 2 | killed |
| `u202.M4_unknown` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 9 | killed |
| `u202.M5_adder` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 10 | killed |
| `u202.M6_account_readded` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 12 | killed |
| `u202.M7_removal_kept` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 2 | killed |
| `u220.P5_no_stop_after_loop` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 306 | 9 | killed |
| `u220.P2_session_tolerated` | `src/cratekit/sync/pair_model.py` | user | 10 file(s) | 306 | 2 | killed |
| `u246.S12_pair_cli_made_here_empty` | `src/cratekit/sync/pair_check.py` | user | 1 file(s) | 14 | 1 | killed |
| `u210.R10_check_todo` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R11_part_written` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 6 | killed |
| `u210.R12_our_folders` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 5 | killed |
| `u210.R14_asked_before` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 9 | killed |
| `u210.R18_beyond_order` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R19_beyond_gained` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R20_beyond_lost` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R21_check_queued` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R22_landed_read` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R16_forecast_line` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 2 | killed |
| `u210.R9_skip_done` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R1_made_step_read` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R2_resumed_move` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R4_rekordbox_landed` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 2 | killed |
| `u210.R5_queue_once` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R8_done_step` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 3 | killed |
| `u304.S5_settle_window_clock` | `src/cratekit/sync/pair_write.py` | user | 2 file(s) | 107 | 1 | killed |
| `u304.S6_settle_moment_clock` | `src/cratekit/sync/pair_write.py` | user | 2 file(s) | 107 | 1 | killed |
| `r1394.S10_later_unsent_write_hides_the_pending` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 3 | killed |
| `r1394.S2_missing_counts_read_as_none_sent` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 7 | killed |
| `r1394.S5_sent_read_as_landed` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 6 | killed |
| `r1394.S6_counts_not_wired` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 14 | killed |
| `r1394.S8_positions_first_only` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 2 | killed |
| `r1394.S9_moving_step_counts_dropped` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 19 | killed |
| `u304.S4_pending_agreement_clock` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 135 | 1 | killed |
| `r1446-b.C1_composite_no_unread_left_out` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 155 | 6 | killed |
| `r1446-c.F1_every_unread_kept_its_place` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 264 | 2 | killed |
| `r1446-c.F2_no_unread_id_read_as_moved` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 264 | 3 | killed |
| `r1446-c.F3_readable_ids_weighed_as_unread` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 264 | 3 | killed |
| `r1418.F5_plans_reading_without_unread_ids` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1432-composites.C4_finish_reads_the_listing_unfinished` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 61 | killed |
| `r1432.E1_listed_rule_puts_it_first` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 18 | killed |
| `r1432.P3_target_id_no_longer_listed_put_back` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 3 | killed |
| `r1432.P4_target_id_already_held_put_twice` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 8 | killed |
| `r1432.P5_target_placed_by_the_listing` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 11 | killed |
| `r1432.P6_target_behind_the_first_held` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 19 | killed |
| `r1432.P8_placed_in_front_of_its_neighbour` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 22 | killed |
| `r1434.M1_write_that_sent_nothing_read_on_its_whole_path` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 2 | killed |
| `r1434.M2_plan_reads_a_write_that_sent_nothing_on_its_whole_path` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.M3_readable_move_after_a_write_that_sent_nothing_read_on_its_whole_path` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.M4_hold_promises_the_accounts_order_for_an_unread_move` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.M5_hold_withholds_the_lead_from_a_readable_reorder` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.S1_sent_nothing_off_path_waits_for_settled_readings` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 7 | killed |
| `r1434.S3_unread_track_placed_at_the_front` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 22 | killed |
| `r1434.S5_folded_base_keeps_unread_keys` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1446.M14_plan_flag_dropped` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1446.M1_no_readable_check` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 6 | killed |
| `r1446.M4_unread_moved_not_set` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 7 | killed |
| `r1446.S1_u234_settled_reorder_never_leads` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 10 | killed |
| `r1446.S3_u225_finish_whatever_was_read` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 12 | killed |
| `r1432.P10_warning_says_it_stays` | `src/cratekit/sync/pair_screen.py` | user | 10 file(s) | 394 | 2 | killed |
| `r1418.F7_composite_ordering_start_unread` | `src/cratekit/sync/pair_stopped.py` | user | 10 file(s) | 394 | 20 | killed |
| `r1418.F1_agreed_is_the_readable_tracks` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1418.F3_agreed_passed_only_for_an_empty_reading` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 11 | killed |
| `r1418.F4_agreed_only_without_adds_or_removes` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 7 | killed |
| `r1434.F7_ordering_start_from_the_readable_tracks` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 3 | killed |
| `u246.S10_pair_cli_started_empty` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 237 | 1 | killed |
| `u208.M4_tie_flag_dropped` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 97 | 2 | killed |
| `u208.M5_tied_rows_not_gathered` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 97 | 2 | killed |
| `u208.M6_facts_line_dropped` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 97 | 1 | killed |
| `u208.M7_totals_tied_zero` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 97 | 2 | killed |
| `u208.M8_item_flag_dropped` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 97 | 1 | killed |
| `u208.M10_here_database_only` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 2 | killed |
| `u208.M11_alias_off` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 5 | killed |
| `u208.M18_held_there_asks_provider` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 1 | killed |
| `u208.M1_ask_any_agreeing` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 16 | killed |
| `u208.M24_alias_unfrozen` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 2 | killed |
| `u208.M2_old_tie_miss_reused` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 1 | killed |
| `u208.M9_here_lookup_dropped` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 2 | killed |
| `r1453.U2_base_keeps_unread_keys` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1453.U5_account_keys_take_unread_only_rows` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 30 | killed |
| `u226.M20_check_no_lag` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 267 | 1 | killed |
| `u226.M23_totals_no_read_backs` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 267 | 1 | killed |
| `u226.M22_lagging_not_per_pair` | `src/cratekit/sync/pair_model.py` | user | 8 file(s) | 267 | 1 | killed |
| `u226.M19_plan_no_hold` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 267 | 2 | killed |
| `u226.M21_plan_window_only` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 267 | 4 | killed |
| `u284.S8_refusal_not_retryable` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 381 | 2 | killed |
| `r1830.M10_planned_number_not_asked` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M11_held_object_left_stale` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M17_positions_never_read` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 15 | killed |
| `r1830.M23_unreadable_marker_passed_over` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M8_renumbering_stamps_updated_at` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 15 | killed |
| `r1830.M9_moved_row_not_refused` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M3_unmeasured_tables_skipped` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M8_memberships_kept` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 74 | 19 | killed |
| `r1830.M21_record_omits_the_rows` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M6_prepare_plans_no_renumbering` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 17 | killed |
| `r1830.M7_commit_skips_the_renumbering` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 17 | killed |
| `u288.M14_confinement_not_called` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 2 | killed |
| `u288.M5_prepare_liveness` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M7_prepare_identity` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M18_plan_counts_nothing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `r1830.M19_digest_omits_the_count` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M22_applied_message_counts_nothing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M10_gone_on_one_read` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 5 | killed |
| `u287.M14_twin_is_own_filing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 32 | killed |
| `u287.M16_gone_holds_what_was_recorded` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `u287.M19_old_prefix_is_synced` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M4_held_before_the_pass` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M5_not_this_pass_file` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M6_on_another_synced` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 8 | killed |
| `u287.M7_in_a_playlist_of_yours` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M16_stale_digest` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u288.M17_only_the_offered` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 8 | killed |
| `u288.M18_unmeasured_kept` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M20_read_back_refusal` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M20_screen_omits_the_count` | `src/cratekit/sync/removed_cli.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M21_gate_answer` | `src/cratekit/sync/removed_cli.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M22_closed_at_open` | `src/cratekit/sync/removed_cli.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M15_append_past_highest` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 87 | 2 | killed |
| `u320.M4_withheld_hearts_hold_nothing` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 2 | killed |
| `u320.M6_any_failure_is_a_sighting` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 4 | killed |
| `u320.M8_retirement_never_applies` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 5 | killed |
| `u320.M21_retire_records_before_the_gate` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M22_retire_ignores_its_answer` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M23_reads_never_recorded` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 11 | killed |
| `u320.M24_record_read_as_empty` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 8 | killed |
| `u320.M25_person_retires_nothing` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 3 | killed |
| `u320.M14_any_status_is_not_found` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 8 | killed |
| `u221.R1_hold_only_a_twin` | `src/cratekit/sync/pair_plan.py` | user | 4 file(s) | 174 | 21 | killed |
| `r838-c.R2_remark_clears` | `src/cratekit/sync/mark_record.py` | maintainer | 1 file(s) | 32 | 1 | killed |
| `r838-d.R3b_stamp_target` | `src/cratekit/sync/mark_record.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U1_refuse_stranger` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U3_pass_filter` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 2 | killed |
| `r838-a.U4_already_unmarked_stamp` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U5_marked_again` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U6_later_order` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U8_title_already_back` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U10_digest_names` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U13_recheck` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U15_rename_target` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 8 | killed |
| `r838-b.U16_part_way_names` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U9_renamed_since` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-c.U7b_not_listed_rerun` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `u246.S14_unmark_narrowed_empty` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 47 | 3 | killed |
| `u246.S15_unmark_narrowed_first_only` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u240.M1_two_names_take_the_first` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 337 | 4 | killed |
| `u240.M2_no_genre_label_named` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 337 | 4 | killed |
| `u240.M3_tag_no_longer_outranks_the_line` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 337 | 17 | killed |
| `u240.M5_wrong_field_read` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 337 | 11 | killed |
| `u240.M7_line_labels_dropped_from_result` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 337 | 3 | killed |
| `u172.C1_tail_skips_guess` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 5 | killed |
| `u172.C2_guess_without_pass` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R35_extra_rides_beside_progress` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 47 | killed |
| `u281.C4_source_blocked_counts_unsent_as_sent` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R19_folder_queues_no_items` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 41 | killed |
| `u281.C3_unsent_never_counted` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R23_summary_from_the_queue` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 27 | killed |
| `u192.F6_queue_only_never` | `src/cratekit/modules/foreground.py` | user | 4 file(s) | 409 | 20 | killed |
| `u281.C1_refusal_said_as_blocked` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 138 | 5 | killed |
| `u281.W7_worker_run_key_without_attempt` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 138 | 1 | killed |
| `r1103.H2_refusal_slug` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 331 | 4 | killed |
| `r791-b.C1_artifact_answers` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 239 | 15 | killed |
| `r791-b.C2_artifact_unread` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 239 | 6 | killed |
| `r791-b.C3_summary_counts_answers` | `src/cratekit/tagging/summary.py` | user | 3 file(s) | 239 | 15 | killed |
| `r791-b.C9_unread_skip_zero_filled` | `src/cratekit/tagging/summary.py` | user | 3 file(s) | 239 | 11 | killed |
| `r791-b.T1_sources_unread_disposition` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 239 | 12 | killed |
| `u244.M24_upgrade_keeps_a_held_table` | `src/cratekit/core/taxonomy_upgrade.py` | user | 2 file(s) | 468 | 22 | killed |
| `u302.W9c_configuration_rules_dropped` | `src/cratekit/write/trees.py` | user | 4 file(s) | 437 | 2 | killed |
| `u129-author.A4_archive_raise_fails_landing` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 76 | 2 | killed |
| `u129-author.A5_archive_return_discarded` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 76 | 2 | killed |
| `u242.M12_composite` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 11 | killed |
| `u242.M12_strip_skips_the_migration` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 14 | killed |
| `u242.M4_plan_reads_no_ledger` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 161 | 5 | killed |
| `u242.M1_exclusion_reads_the_ledger` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 230 | 5 | killed |
| `u242.M5_pending_marks_ignores_the_ledger` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 230 | 1 | killed |
| `u242.M2_is_taken_drops_the_id` | `src/cratekit/sync/playlists.py` | user | 4 file(s) | 285 | 14 | killed |
| `u242.M3_is_taken_drops_the_prefix` | `src/cratekit/sync/playlists.py` | user | 5 file(s) | 382 | 21 | killed |
| `u242.M26_release_stamps_no_mark` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 78 | 3 | killed |
| `u242.M22_unmark_releases_nothing` | `src/cratekit/sync/unmark_cli.py` | user | 4 file(s) | 197 | 7 | killed |
| `u181.C3_unscored_flag_ignored` | `src/cratekit/vocals/cli.py` | user | 2 file(s) | 105 | 4 | killed |
| `u181.V1_unavailable_ignores_bound_loader` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 522 | 5 | killed |
| `u181.T1_rescore_ignores_unable` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 215 | 4 | killed |
| `u300.S15_terminal_probe_local` | `src/cratekit/core/session_ack.py` | maintainer | 2 file(s) | 185 | 10 | killed |
| `r598-a.A5_holder_never_recorded` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 8 | killed |
| `r598-a.A1_state_check_widened_to_non_terminal` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 4 | killed |
| `r598-a.A2_no_holder_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r598-a.A3_liveness_not_consulted` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 8 | killed |
| `r647-a.B14_machine_not_read_back` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 5 | killed |
| `r647-a.B15_machine_not_written` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 5 | killed |

## Zero rows and what they owe

- `u130-a.A1_removal_beats_addition` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u209.C3_withheld`

check: read no change in the account's withheld count

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C3_withheld`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_withheld_count_changed_before_the_write_refuses_stale`

Old text:

```
            elif withheld != one.withheld:
```

New text:

```
            elif False:
```

### `u209.C4_rekordbox_gone`

check: read no rekordbox playlist deleted or turned into a folder

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C4_rekordbox_gone`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_rekordbox_playlist_deleted_before_the_write_refuses_stale`

Old text:

```
            if there is None or there.removed or not there.plain:
                moved.append(
                    Moved(
                        REKORDBOX_SIDE,
                        one.target.rekordbox_id,
```

New text:

```
            if there is None:
                moved.append(
                    Moved(
                        REKORDBOX_SIDE,
                        one.target.rekordbox_id,
```

### `u209.C5_memberships`

check: read no moved rekordbox membership

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C5_memberships`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale`
  - `tests/test_sync_pair_hold.py::test_a_moved_list_is_checked_whichever_side_was_skipped`
  - `tests/test_sync_pair_hold.py::test_a_rekordbox_membership_changed_before_the_write_refuses_stale_and_names_it`
  - `tests/test_sync_pair_hold.py::test_both_sides_moved_are_both_named`
  - `tests/test_sync_pair_hold_every.py::test_a_made_pair_whose_rekordbox_side_moved_before_the_write_refuses_stale`

Old text:

```
            if there.memberships() != tuple(tuple(row) for row in one.rekordbox_before):
```

New text:

```
            if False:
```

### `u209.C6_discovered_place`

check: read no move of a discovered playlist's place

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C6_discovered_place`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_dragged_into_archive_before_the_write_refuses_stale`
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_moved_into_a_subfolder_before_the_write_refuses_stale`
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_moved_to_another_folder_before_the_write_refuses_stale`
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_moved_to_the_root_before_the_write_refuses_stale`
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_moved_where_discovery_never_pairs_refuses_stale`

Old text:

```
                if now_found is None or (now_found.folder, now_found.title) != (
```

New text:

```
                if False and (now_found.folder, now_found.title) != (
```

### `u209.C7_made_left_behind`

check: read no made pair dragged where no pair is kept

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C7_made_left_behind`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_made_pair_dragged_into_archive_before_the_write_refuses_stale`

Old text:

```
                why = pair_discover.left_behind(db, there, favorites=favorites, skip=skip)
                if why:
```

New text:

```
                why = pair_discover.left_behind(db, there, favorites=favorites, skip=skip)
                if False:
```

### `u209.C8_rows_gone`

check: read no row the plan adds gone from the collection

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C8_rows_gone`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_row_the_plan_adds_gone_before_the_write_stops_every_pair`

Old text:

```
            gone = sorted(set(one.change.adds) - set(playlist_pair.content(db, one.change.adds)))
```

New text:

```
            gone = []
```

### `u209.C9_unpaired_back`

check: read no let go playlist back where its pair is kept

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C9_unpaired_back`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_made_pair_let_go_in_archive_and_dragged_back_before_the_write_refuses_stale`

Old text:

```
            if not pair_discover.left_behind(db, there, favorites=favorites, skip=skip):
```

New text:

```
            if False:
```

### `u209.H1_offer_mismatch_ignored`

_held_plan: read back a held plan whatever offer the run recorded

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `H1_offer_mismatch_ignored`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_held_plan_other_than_the_offer_is_planned_again`

Old text:

```
    if moved:
        return None, 0, f"the held plan is not the plan {', '.join(moved)} showed"
```

New text:

```
    if False:
        return None, 0, f"the held plan is not the plan {', '.join(moved)} showed"
```

### `u130-a.A1_removal_beats_addition`

A removal wins over an addition, so a track removed on one side and re-added on the other is dropped

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u130-a.json`, row `A1_removal_beats_addition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if added or not removed:
```

New text:

```
        if not removed:
```

### `u130-a.A6_order_change_read_inverted`

Read an unchanged order as changed and a changed one as unchanged

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u130-a.json`, row `A6_order_change_read_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair.py`
- Collected: 126 against a baseline of 126
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_whole_sync_after_a_skipped_one_finishes_both_sides_from_the_old_base`
  - `tests/test_sync_pair.py::test_when_both_sides_reorder_the_account_order_wins`
  - `tests/test_sync_pair.py::test_when_rekordbox_alone_reorders_the_account_follows`
  - `tests/test_sync_pair_merge.py::test_a_base_is_read_as_before_whatever_the_order`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_a_track_the_account_adds_is_placed_in_the_order_rekordbox_holds`
  - `tests/test_sync_pair_merge.py::test_only_the_tracks_both_sides_held_at_the_base_are_read_for_their_order`
  - `tests/test_sync_pair_merge.py::test_order_changed_reads_only_the_tracks_both_held`
  - `tests/test_sync_pair_merge.py::test_rekordbox_reordered_since_a_base_whose_sides_disagree_leads`
  - `tests/test_sync_pair_merge.py::test_rekordbox_reordered_since_the_stopped_write_leads`
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_a_base_whose_sides_disagree_still_leads`
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_the_stopped_write_leads_whatever_else_moved`
  - `tests/test_sync_pair_merge.py::test_the_stopped_writes_order_is_not_read_against_the_base`
  - `tests/test_sync_pair_merge.py::test_when_both_sides_reordered_the_account_order_wins`
  - `tests/test_sync_pair_merge.py::test_when_rekordbox_alone_reordered_its_order_wins`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    return [key for key in now if key in held_then] != [key for key in base if key in held_now]
```

New text:

```
    return [key for key in now if key in held_then] == [key for key in base if key in held_now]
```

### `u202.M1_since`

pair_merge.merge: a moment at or before the base's sync is read as a known moment

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M1_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_merge.py::test_a_moment_at_or_before_the_base_sync_is_no_moment`

Old text:

```
        if since is not None and (since.tzinfo is None or not at > since):
            return None
```

New text:

```
        if False:
            return None
```

### `u202.M4_unknown`

Call.outcome: an unknown moment lets the removal win

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M4_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_removed_on_the_account_and_put_back_in_rekordbox_is_kept`
  - `tests/test_sync_pair_back.py::test_a_removal_rekordbox_kept_no_moment_for_keeps_the_track_and_names_the_call`
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_in_rekordbox_after_the_account_took_it_out_stays_and_is_named`
  - `tests/test_sync_pair_merge.py::test_a_moment_at_or_before_the_base_sync_is_no_moment`
  - `tests/test_sync_pair_merge.py::test_a_moment_with_no_zone_is_no_moment`
  - `tests/test_sync_pair_merge.py::test_a_removal_on_one_side_and_a_re_add_on_the_other_keeps_the_track`
  - `tests/test_sync_pair_merge.py::test_a_removal_with_no_moment_never_beats_an_addition_and_is_called_unknown`
  - `tests/test_sync_pair_merge.py::test_an_account_removal_never_beats_a_rekordbox_addition`

Old text:

```
        if self.added_at is None or self.removed_at is None:
            return TIME_UNKNOWN
```

New text:

```
        if self.added_at is None or self.removed_at is None:
            return REMOVAL_LATER
```

### `u202.M5_adder`

pair_merge.merge: the adding side is mistaken for the removing one, so the moments are read off the wrong sides

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M5_adder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_in_rekordbox_after_the_account_took_it_out_stays_and_is_named`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`
  - `tests/test_sync_pair_merge.py::test_a_base_with_no_sync_moment_still_orders_two_known_moments`
  - `tests/test_sync_pair_merge.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_merge.py::test_a_tie_keeps_the_track`
  - `tests/test_sync_pair_merge.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`
  - `tests/test_sync_pair_merge.py::test_an_account_addition_later_than_a_rekordbox_removal_is_added_back_there`
  - `tests/test_sync_pair_merge.py::test_an_account_removal_never_beats_a_rekordbox_addition`

Old text:

```
                (ACCOUNT, account, rekordbox) if added_account else (REKORDBOX, rekordbox, account)
```

New text:

```
                (ACCOUNT, account, rekordbox) if not added_account else (REKORDBOX, rekordbox, account)
```

### `u202.M6_account_readded`

pair_merge.merge: a track the account put back is not read as added there (R-990 reopened)

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M6_account_readded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_back.py::test_a_removal_rekordbox_kept_no_moment_for_keeps_the_track_and_names_the_call`
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`
  - `tests/test_sync_pair_merge.py::test_a_base_with_no_sync_moment_still_orders_two_known_moments`
  - `tests/test_sync_pair_merge.py::test_a_moment_at_or_before_the_base_sync_is_no_moment`
  - `tests/test_sync_pair_merge.py::test_a_moment_with_no_zone_is_no_moment`
  - `tests/test_sync_pair_merge.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_merge.py::test_a_removal_with_no_moment_never_beats_an_addition_and_is_called_unknown`
  - `tests/test_sync_pair_merge.py::test_a_tie_keeps_the_track`
  - `tests/test_sync_pair_merge.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`

Old text:

```
            key not in then_account or key in account.readded
```

New text:

```
            key not in then_account
```

### `u202.M7_removal_kept`

pair_merge.merge: a call the removal won still keeps the track

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M7_removal_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_merge.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`

Old text:

```
            if call.kept:
                kept.add(key)
```

New text:

```
            if True:
                kept.add(key)
```

### `u220.P5_no_stop_after_loop`

sync_pair: end OK after the loop though an order did not finish

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u220.json`, row `P5_no_stop_after_loop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_tie.py`
- Collected: 306 against a baseline of 306
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_the_account_still_stands_in_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[refused]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_the_run_puts_the_refused_pair_in_order_and_moves_nothing_else`
  - `tests/test_sync_pair_order.py::test_a_refused_order_stops_its_pair_alone_and_every_other_write_lands`

Old text:

```
    if unordered:
```

New text:

```
    if False:
```

### `u220.P2_session_tolerated`

ORDER_REFUSALS: tolerate a rejected session too, so every later pair meets it

- File: `src/cratekit/sync/pair_model.py`
- Source: `u220.json`, row `P2_session_tolerated`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_tie.py`
- Collected: 306 against a baseline of 306
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_rejected_session_on_the_order_still_stops_the_whole_write`
  - `tests/test_sync_pair_order.py::test_the_order_refusals_that_stop_one_pair_are_the_two_an_order_raises`

Old text:

```
ORDER_REFUSALS = frozenset({"outbound-remove-refused", "unavailable-transient"})
```

New text:

```
ORDER_REFUSALS = frozenset({"outbound-remove-refused", "unavailable-transient", "credential-missing"})
```

### `u246.S12_pair_cli_made_here_empty`

pair: no account ids made this run, so discovery is told every pair, the ones this run made included, is already paired

- File: `src/cratekit/sync/pair_check.py`
- Source: `u246.json`, row `S12_pair_cli_made_here_empty`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[2-the make and the move]`

Old text:

```
            made_here = set(ours.values())
```

New text:

```
            made_here = set()
```

### `u210.R10_check_todo`

check: read every pair, a finished one included

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R10_check_todo`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue`

Old text:

```
    todo = [one for one in planned.pairs if not of(one).has(STEP_DONE)]
```

New text:

```
    todo = list(planned.pairs)
```

### `u210.R11_part_written`

check: read a part written existing pair exactly, as one not started

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R11_part_written`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_rekordbox_playlist_changed_after_this_run_wrote_it_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_inside_the_account_write_is_finished_without_writing_rekordbox_twice`
  - `tests/test_sync_pair_resume_one.py::test_a_track_lost_from_the_part_written_account_playlist_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_track_withheld_on_the_part_written_playlist_refuses_stale`

Old text:

```
            if one.target.new or of(one).has(STEP_ACCOUNT):
```

New text:

```
            if one.target.new:
```

### `u210.R12_our_folders`

check: read a folder this run made as not there for the pairs still to make in it

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R12_our_folders`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_ceiling_continue_above_the_hour_names_the_hour_and_finishes_the_run`
  - `tests/test_sync_pair_resume.py::test_a_ceiling_stop_after_three_of_five_pairs_is_finished_by_a_continue_of_the_run`
  - `tests/test_sync_pair_resume.py::test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue`
  - `tests/test_sync_pair_resume.py::test_a_title_taken_in_the_folder_before_the_continue_refuses_stale_naming_it`
  - `tests/test_sync_pair_resume.py::test_the_stop_names_the_run_and_the_calls_its_continue_needs`

Old text:

```
            folder_id = place.folder_id or our_folders.get(place.folder, "")
```

New text:

```
            folder_id = place.folder_id
```

### `u210.R14_asked_before`

_asked_before: compare what is asked now unchanged, so a continue after the run's own marks plans again

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R14_asked_before`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_ceiling_continue_above_the_hour_names_the_hour_and_finishes_the_run`
  - `tests/test_sync_pair_resume.py::test_a_ceiling_stop_after_three_of_five_pairs_is_finished_by_a_continue_of_the_run`
  - `tests/test_sync_pair_resume.py::test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue`
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[2-the make and the move]`
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[3-the move and the fill]`
  - `tests/test_sync_pair_resume.py::test_a_title_taken_in_the_folder_before_the_continue_refuses_stale_naming_it`
  - `tests/test_sync_pair_resume.py::test_a_track_put_on_a_part_made_playlist_before_the_continue_refuses_stale_naming_it`
  - `tests/test_sync_pair_resume.py::test_the_stop_names_the_run_and_the_calls_its_continue_needs`
  - `tests/test_sync_pair_resume_one.py::test_a_first_sync_named_by_hand_that_failed_after_its_mark_is_continued_on_its_plan`

Old text:

```
    return {**dict(asked), "targets": targets}
```

New text:

```
    return dict(asked)
```

### `u210.R18_beyond_order`

_beyond: read no order on a part written playlist

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R18_beyond_order`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`

Old text:

```
    if not parts and not ordering:
```

New text:

```
    if False:
```

### `u210.R19_beyond_gained`

_beyond: read no track gained

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R19_beyond_gained`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_track_put_on_a_part_made_playlist_before_the_continue_refuses_stale_naming_it`

Old text:

```
    gained = held - before - added
```

New text:

```
    gained = set()
```

### `u210.R20_beyond_lost`

_beyond: read no track lost

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R20_beyond_lost`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_track_lost_from_the_part_written_account_playlist_refuses_stale`

Old text:

```
    lost = (before - set(one.account_removes)) - held
```

New text:

```
    lost = set()
```

### `u210.R21_check_queued`

check: read the run's own queued job as another sync's

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R21_check_queued`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_job_queued_before_a_stop_is_not_queued_again_by_the_continue`

Old text:

```
    asking = [one for one in todo if one.acquire and not of(one).has(STEP_QUEUED)]
```

New text:

```
    asking = [one for one in todo if one.acquire]
```

### `u210.R22_landed_read`

check: read no rekordbox playlist this run's commit landed

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R22_landed_read`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_rekordbox_playlist_changed_after_this_run_wrote_it_refuses_stale`

Old text:

```
                _landed_moved(db, one, landed, moved)
```

New text:

```
                pass
```

### `u210.R16_forecast_line`

sync_pair: warn of the ceiling only at ten times over

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R16_forecast_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_gate_forecast_above_the_hour_names_the_hour_and_its_command_runs`
  - `tests/test_sync_pair_resume.py::test_a_gate_whose_ceiling_is_below_the_expected_calls_says_so_with_the_calls_value`

Old text:

```
        if writing > line:
```

New text:

```
        if writing > line * 10:
```

### `u210.R9_skip_done`

sync_pair: write a pair an earlier command finished

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R9_skip_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_ceiling_stop_after_three_of_five_pairs_is_finished_by_a_continue_of_the_run`

Old text:

```
                    if _steps_of(steps, one).has(STEP_DONE):
```

New text:

```
                    if False:
```

### `u210.R1_made_step_read`

apply_pair: never read a made side recorded by an earlier command, so a continue makes it again

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R1_made_step_read`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[3-the move and the fill]`

Old text:

```
        if isinstance(made, str) and made:
```

New text:

```
        if False:
```

### `u210.R2_resumed_move`

_made: move only a playlist this call made, so a stop between the make and the move leaves it at the root

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R2_resumed_move`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[2-the make and the move]`

Old text:

```
    if made or (resumed and _made_here(store.get(account_id), one)):
```

New text:

```
    if made:
```

### `u210.R4_rekordbox_landed`

apply_pair: write rekordbox again on a continue whose commit already landed

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R4_rekordbox_landed`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_first_sync_named_by_hand_that_failed_after_its_mark_is_continued_on_its_plan`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_inside_the_account_write_is_finished_without_writing_rekordbox_twice`

Old text:

```
        if isinstance(landed, dict):
```

New text:

```
        if False:
```

### `u210.R5_queue_once`

_queue_once: queue again a job an earlier command of the run queued

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R5_queue_once`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_job_queued_before_a_stop_is_not_queued_again_by_the_continue`

Old text:

```
    if steps.has(STEP_QUEUED):
```

New text:

```
    if False:
```

### `u210.R8_done_step`

apply_pair: record no done step, so a continue redoes a finished pair

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R8_done_step`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_ceiling_stop_after_three_of_five_pairs_is_finished_by_a_continue_of_the_run`
  - `tests/test_sync_pair_resume.py::test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue`
  - `tests/test_sync_pair_resume.py::test_the_stop_names_the_run_and_the_calls_its_continue_needs`

Old text:

```
    steps.mark(STEP_DONE, done.account_id or one.target.key)
```

New text:

```
    pass
```

### `u304.S5_settle_window_clock`

pair_write._settle: the settle window counted off the wall clock, not pair_model._now

- File: `src/cratekit/sync/pair_write.py`
- Source: `u304.json`, row `S5_settle_window_clock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_account.py`
- Collected: 107 against a baseline of 107
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`

Old text:

```
        left = SETTLE_SECONDS - (pair_model._now() - settle.moved_at).total_seconds()
```

New text:

```
        left = SETTLE_SECONDS - (datetime.now(settle.moved_at.tzinfo) - settle.moved_at).total_seconds()
```

### `u304.S6_settle_moment_clock`

pair_write._write_account: when the moves were sent is stamped off the wall clock, not pair_model._now

- File: `src/cratekit/sync/pair_write.py`
- Source: `u304.json`, row `S6_settle_moment_clock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_account.py`
- Collected: 107 against a baseline of 107
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_the_settle_window_counts_the_time_spent_on_other_writes`

Old text:

```
            one=one, steps=steps, end=sent, moved_at=pair_model._now(), rekordbox_after=None
```

New text:

```
            one=one, steps=steps, end=sent, moved_at=datetime.now(__import__("datetime").UTC), rekordbox_after=None
```

### `r1394.S10_later_unsent_write_hides_the_pending`

stopped writes: the latest record is read whether or not it sent a move, so a refused finish hides the pending write it was finishing, round two's BLOCKING row

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S10_later_unsent_write_hides_the_pending`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_stopped.py::test_a_later_write_that_sent_no_move_does_not_hide_a_pending_one`

Old text:

```
            if held is None or (write.pending, write.at) > (held[1].pending, held[1].at):
```

New text:

```
            if held is None or write.at > held[1].at:
```

### `r1394.S2_missing_counts_read_as_none_sent`

stopped write: a moving step with no counts reads as no move sent, so any agreed path reading finishes it, as before R-1394

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S2_missing_counts_read_as_none_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts0]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts1]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts2]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts4]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`

Old text:

```
        return 0, total
    return landed, sent
```

New text:

```
        return 0, 0
    return landed, sent
```

### `r1394.S5_sent_read_as_landed`

stopped write: the sent count is read from the landed field, so a move in flight reads as known not sent

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S5_sent_read_as_landed`
- Moved: Anchored where u325-replay-after.json replayed it: Same return in _moving; U298 replaced the module's _count with cli.output.count_of
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_stopped.py::test_a_moving_step_reads_back_its_counts`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts1]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts2]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`

Old text:

```
    return at, start, end, count_of(value.get(SENT)), count_of(value.get(LANDED))
```

New text:

```
    return at, start, end, count_of(value.get(LANDED)), count_of(value.get(LANDED))
```

### `r1394.S6_counts_not_wired`

stopped write: the counts read back never reach the stopped write, which keeps none landed and none sent

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S6_counts_not_wired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`
  - `tests/test_sync_pair_stopped.py::test_a_moving_step_reads_back_its_counts`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts0]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts1]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts2]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts4]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`
  - `tests/test_sync_pair_stopped.py::test_every_move_accepted_reads_as_every_move_landed_whatever_the_counts`

Old text:

```
        landed=landed,
        sent=reached_by,
```

New text:

```
        landed=0,
        sent=0,
```

### `r1394.S8_positions_first_only`

positions: only the first count on the path that leaves the order is answered, so a track taken off since hides a later one

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S8_positions_first_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`

Old text:

```
    return tuple(
        index
        for index, state in enumerate(passed(start, target))
        if [one for one in dict.fromkeys(state) if one in common] == shown
    )
```

New text:

```
    return tuple(
        index
        for index, state in enumerate(passed(start, target))
        if [one for one in dict.fromkeys(state) if one in common] == shown
    )[:1]
```

### `r1394.S9_moving_step_counts_dropped`

moving step: the record written carries a sent count of 0 whatever it is told

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S9_moving_step_counts_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_with_no_unread_track_is_put_in_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_that_move_leaves_it_is_finished`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        SENT: int(sent),
```

New text:

```
        SENT: 0,
```

### `u304.S4_pending_agreement_clock`

pair_plan._pending: a pending pair's agreement read off the wall clock, not pair_model._now

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u304.json`, row `S4_pending_agreement_clock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 135 against a baseline of 135
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_two_readings_agree_only_once_minutes_apart`

Old text:

```
    agreed = kept and pair_model._now() - seen_at >= AGREE_AFTER
```

New text:

```
    agreed = kept and __import__("datetime").datetime.now(__import__("datetime").UTC) - seen_at >= AGREE_AFTER
```

### `r1446-b.C1_composite_no_unread_left_out`

the composite of r1446 rows M10 and M11, what they hold together: the settled reading and the reading now both compared with their unread ids in place, so a move of an unread track alone reads as a reorder again; either filter alone is equivalent, since reordered reads only the tracks both readings hold

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446-b.json`, row `C1_composite_no_unread_left_out`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 155 against a baseline of 155
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_settled_reorder_moved_a_readable_track_only_when_one_moved[kept0-reading0-unread0-False]`
  - `tests/test_sync_pair_settle.py::test_a_settled_reorder_moved_a_readable_track_only_when_one_moved[kept4-reading4-unread4-False]`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
        [one for one in kept.order if one not in left_out], readable
```

New text:

```
        list(kept.order), list(reading)
```

### `r1446-c.F1_every_unread_kept_its_place`

round one's BLOCKING reverted: once only unread tracks moved, no target at all, so an unread track nobody moved keeps the interrupted move's place

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446-c.json`, row `F1_every_unread_kept_its_place`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`
- Collected: 264 against a baseline of 264
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
                    else tuple(one for one in stopped_write.target if one not in moved_unread)
```

New text:

```
                    else ()
```

### `r1446-c.F2_no_unread_id_read_as_moved`

every unread id read as unmoved, so the one the person moved is put where the stopped order was taking it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446-c.json`, row `F2_no_unread_id_read_as_moved`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`
- Collected: 264 against a baseline of 264
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_the_unread_tracks_moved_since_the_stop_are_those_off_the_order_both_readings_share`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
    return frozenset(one for one in now if one in left_out and one not in held)
```

New text:

```
    return frozenset()
```

### `r1446-c.F3_readable_ids_weighed_as_unread`

the shared run unweighted, so it may keep unread ids in place of a readable one and read the wrong unread track as moved

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446-c.json`, row `F3_readable_ids_weighed_as_unread`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`
- Collected: 264 against a baseline of 264
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_the_unread_tracks_moved_since_the_stop_are_those_off_the_order_both_readings_share`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
        value = top[0] + (1 if one in left_out else heavy)
```

New text:

```
        value = top[0] + 1
```

### `r1418.F5_plans_reading_without_unread_ids`

existing guard, R-1264: the plan's reading of an account it orders is the readable tracks alone, unread ids left out of it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1418.json`, row `F5_plans_reading_without_unread_ids`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`

Old text:

```
            account_before = tuple(listed_order or account_now)
```

New text:

```
            account_before = tuple(account_now)
```

### `r1432-composites.C4_finish_reads_the_listing_unfinished`

what E4 holds: at a finish the readable tracks are read as the account lists them, with the stopped write's remaining moves not applied, so its half done order is read as the account's

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432-composites.json`, row `C4_finish_reads_the_listing_unfinished`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 61 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_with_no_unread_track_is_put_in_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_first_move_refused_on_its_412s_is_sent_again_from_the_start_once`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - ... and 46 more, see the JSON sidecar

Old text:

```
                for one in pair_stopped.finished(
                    listed_order or account_now, stopped_write.target
                )
```

New text:

```
                for one in (listed_order or account_now)
```

### `r1432.E1_listed_rule_puts_it_first`

existing guard, R-1264: an unread track not named by a target goes to the front rather than behind the track listed before it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `E1_listed_rule_puts_it_first`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered5-listed5-target5-expected5]`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        placed.insert(behind(listed[:index]), one)
```

New text:

```
        placed.insert(0, one)
```

### `r1432.P3_target_id_no_longer_listed_put_back`

an unread id the target names and the account no longer lists is put back into the asked order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P3_target_id_no_longer_listed_put_back`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered3-listed3-target3-expected3]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered6-listed6-target6-expected6]`

Old text:

```
        if one in held or one not in holding:
```

New text:

```
        if one in held:
```

### `r1432.P4_target_id_already_held_put_twice`

a target id the order already holds, a readable track, is inserted again, so the asked order holds it twice

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P4_target_id_already_held_put_twice`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered3-listed3-target3-expected3]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered4-listed4-target4-expected4]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered5-listed5-target5-expected5]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered6-listed6-target6-expected6]`
  - `tests/test_sync_pair_stopped_order.py::test_rekordbox_reordered_since_the_stop_leads`

Old text:

```
        if one in held or one not in holding:
```

New text:

```
        if one not in holding:
```

### `r1432.P5_target_placed_by_the_listing`

each unread id the target names is placed behind the track the listing shows before it, not the one the target puts before it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P5_target_placed_by_the_listing`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 11 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered3-listed3-target3-expected3]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered4-listed4-target4-expected4]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered5-listed5-target5-expected5]`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
        placed.insert(behind(target[:index]), one)
```

New text:

```
        placed.insert(behind(listed[: list(listed).index(one)]), one)
```

### `r1432.P6_target_behind_the_first_held`

an unread id is placed behind the first track the target puts before it that the order holds, not the nearest

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P6_target_behind_the_first_held`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        for one in reversed(before):
```

New text:

```
        for one in before:
```

### `r1432.P8_placed_in_front_of_its_neighbour`

an unread id is put in front of the track it follows rather than behind it, the target's and the listing's alike (R-1418's F6, in this unit's shape)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P8_placed_in_front_of_its_neighbour`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 22 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
                return placed.index(one) + 1
```

New text:

```
                return placed.index(one)
```

### `r1434.M1_write_that_sent_nothing_read_on_its_whole_path`

round two's shape: a write known to have sent no move is read against its whole path, so a person's drag of one track to the top, where its first move would have put it, is finished over

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M1_write_that_sent_nothing_read_on_its_whole_path`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`

Old text:

```
    return tuple(write.start) if write.sent_nothing else tuple(write.target)
```

New text:

```
    return tuple(write.target)
```

### `r1434.M2_plan_reads_a_write_that_sent_nothing_on_its_whole_path`

the plan's path read alone back on the whole path for a write that sent no move, R-1446's check of a readable move keeping the start

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M2_plan_reads_a_write_that_sent_nothing_on_its_whole_path`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`

Old text:

```
            stopped_write.start, _toward(stopped_write), reading
```

New text:

```
            stopped_write.start, stopped_write.target, reading
```

### `r1434.M3_readable_move_after_a_write_that_sent_nothing_read_on_its_whole_path`

R-1446's check of a readable move alone back on the whole path for a write that sent no move, so a drag of a readable track to the top with an unread track listed reads as an unread move

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M3_readable_move_after_a_write_that_sent_nothing_read_on_its_whole_path`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`

Old text:

```
        return not pair_stopped.reached(write.start, _toward(write), readable)
```

New text:

```
        return not pair_stopped.reached(write.start, write.target, readable)
```

### `r1434.M4_hold_promises_the_accounts_order_for_an_unread_move`

the hold while a move of unread tracks alone settles says the account's order is then read as the person's, though the others are finished in the stopped order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M4_hold_promises_the_accounts_order_for_an_unread_move`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`

Old text:

```
            if unread and not _readable_moved(write, kept, reading, unread, moved_nothing=False)
```

New text:

```
            if False
```

### `r1434.M5_hold_withholds_the_lead_from_a_readable_reorder`

the hold while a reorder of readable tracks settles says the others are finished in the stopped order, though the account's order then leads

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M5_hold_withholds_the_lead_from_a_readable_reorder`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`

Old text:

```
            if unread and not _readable_moved(write, kept, reading, unread, moved_nothing=False)
```

New text:

```
            if True
```

### `r1434.S1_sent_nothing_off_path_waits_for_settled_readings`

existing guard, U234: an order off the path of a write known to have sent no move no longer leads at once

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `S1_sent_nothing_off_path_waits_for_settled_readings`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_finish_stopped_before_its_first_send_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_this_version_recorded_with_no_move_sent_leaves_a_reorder_the_persons`

Old text:

```
        moved_nothing = off_path and stopped_write.sent_nothing
```

New text:

```
        moved_nothing = False
```

### `r1434.S3_unread_track_placed_at_the_front`

existing guard, R-1264: an unread track a reorder does not move is put at the front rather than behind the track listed before it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `S3_unread_track_placed_at_the_front`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 22 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
                return placed.index(one) + 1
```

New text:

```
                return 0
```

### `r1434.S5_folded_base_keeps_unread_keys`

existing guard, R-1264: the base keeps an unread track's key, so it is read as taken off the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `S5_folded_base_keeps_unread_keys`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`

Old text:

```
            base_account = tuple(key for key in base_account if key not in unread_keys)
```

New text:

```
            base_account = tuple(base_account)
```

### `r1446.M14_plan_flag_dropped`

the plan never carries the flag, so the gate says the stopped order takes the unread track where it was taking it and never that only unread tracks moved

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `M14_plan_flag_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`

Old text:

```
        stop_unread_moved=unread_moved,
```

New text:

```
        stop_unread_moved=False,
```

### `r1446.M1_no_readable_check`

the card's row: a reorder read after a stop stands whatever it moved, so a settled move of an unread track alone lets the account lead and undoes rekordbox's reorder

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `M1_no_readable_check`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
            reordered_since_stop
            and unread
            and not _readable_moved(
```

New text:

```
            False
            and unread
            and not _readable_moved(
```

### `r1446.M4_unread_moved_not_set`

the flag never set, so the finish places the moved unread track by the stopped write's target, over the person's place, and the gate says the stopped order takes it there

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `M4_unread_moved_not_set`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
            moved_nothing = False
            unread_moved = True
```

New text:

```
            moved_nothing = False
```

### `r1446.S1_u234_settled_reorder_never_leads`

sample, U234: a reorder settled readings show never leads

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `S1_u234_settled_reorder_never_leads`
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`

Old text:

```
        and pair_model._now() - since >= AGREE_AFTER
    ):
        return True
```

New text:

```
        and pair_model._now() - since >= AGREE_AFTER
    ):
        return False
```

### `r1446.S3_u225_finish_whatever_was_read`

sample, U225: the stop finished even when a reorder was read

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `S3_u225_finish_whatever_was_read`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_finish_stopped_before_its_first_send_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_this_version_recorded_with_no_move_sent_leaves_a_reorder_the_persons`

Old text:

```
    if stopped_write is not None and not reordered_since_stop:
```

New text:

```
    if stopped_write is not None:
```

### `r1432.P10_warning_says_it_stays`

the sync-pair-unread warning at a finish says only that each stays where it is

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1432.json`, row `P10_warning_says_it_stays`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`

Old text:

```
                        if finished_unread
```

New text:

```
                        if False
```

### `r1418.F7_composite_ordering_start_unread`

what F7 holds: a stopped write with no moving step reads no start from its ordering step, so the start F7 narrows is never read

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1418.json`, row `F7_composite_ordering_start_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 20 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_finish_stopped_before_its_first_send_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_stopped.py::test_a_write_begun_ordered_and_not_finished_is_read_back_whole`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    begin = sent[1] if sent is not None else start
```

New text:

```
    begin = sent[1] if sent is not None else ()
```

### `r1418.F1_agreed_is_the_readable_tracks`

the brief's row: a finish is held to the tracks the provider could read, so a lag differing only by where an unread track stands is planned from

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F1_agreed_is_the_readable_tracks`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
            {"agreed": tuple(one.account_before)}
```

New text:

```
            {"agreed": tuple(one.account_now)}
```

### `r1418.F3_agreed_passed_only_for_an_empty_reading`

the clause inverted, so a finish whose plan read the account passes no agreed order and is held to membership alone

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F3_agreed_passed_only_for_an_empty_reading`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 11 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_plan_read_no_account_passes_no_agreed_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            if one.finishing_order and one.account_before
            else {}
```

New text:

```
            if one.finishing_order and not one.account_before
            else {}
```

### `r1418.F4_agreed_only_without_adds_or_removes`

existing guard, R-1411: a finish that also adds or removes passes no agreed order, as before R-1411

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F4_agreed_only_without_adds_or_removes`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
            if one.finishing_order and one.account_before
            else {}
```

New text:

```
            if one.finishing_order
            and one.account_before
            and not (one.account_removes or one.account_adds)
            else {}
```

### `r1434.F7_ordering_start_from_the_readable_tracks`

R-1418's zero row, now the card's pin: the ordering step records its start from the readable tracks, so a track unread at the stop and read since is left out of the path read and its move by the person is put back

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1434.json`, row `F7_ordering_start_from_the_readable_tracks`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`

Old text:

```
                    one.account_before or one.account_now, removed, added
```

New text:

```
                    one.account_now, removed, added
```

### `u246.S10_pair_cli_started_empty`

pair: the stopped write's start as an empty set, so a folded base holds nothing it asked for

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u246.json`, row `S10_pair_cli_started_empty`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair.py`
- Collected: 237 against a baseline of 237
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_the_stopped_write_added_then_taken_off_in_rekordbox_comes_off_the_account`

Old text:

```
        started = set(stopped_write.start) if folded else set()
```

New text:

```
        started = set()
```

### `u208.M4_tie_flag_dropped`

_ask: never say a tie was broken, so the gate counts none

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M4_tie_flag_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - `tests/test_sync_pair_tie.py::test_two_hearted_releases_take_the_lower_hearted_one`

Old text:

```
        return remote_id, "", bool(remote.tie_broken(row.content_id))
```

New text:

```
        return remote_id, "", False
```

### `u208.M5_tied_rows_not_gathered`

plan_pair: gather no tied rows, so the facts line, the totals and the item flag say nothing

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M5_tied_rows_not_gathered`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - `tests/test_sync_pair_tie.py::test_two_hearted_releases_take_the_lower_hearted_one`

Old text:

```
        elif broke:
            tied.append(names[key])
```

New text:

```
        elif False:
            tied.append(names[key])
```

### `u208.M6_facts_line_dropped`

facts: leave the broken tie count off the pair's line on the gate

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u208.json`, row `M6_facts_line_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`

Old text:

```
                if one.tied
                else ""
```

New text:

```
                if False
                else ""
```

### `u208.M7_totals_tied_zero`

payload: report totals.tied as zero whatever the plan broke

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u208.json`, row `M7_totals_tied_zero`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - `tests/test_sync_pair_tie.py::test_two_hearted_releases_take_the_lower_hearted_one`

Old text:

```
            "tied": sum(len(one.tied) for one in planned.pairs),
```

New text:

```
            "tied": 0,
```

### `u208.M8_item_flag_dropped`

_items: mark no account add as chosen by a broken tie

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u208.json`, row `M8_item_flag_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`

Old text:

```
                **({"tied": True} if remote_id in broken else {}),
```

New text:

```
                **({}),
```

### `u208.M10_here_database_only`

here: read only the database ISRC, never the row's file

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M10_here_database_only`
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; file_identity is read through pair_read, its home since the split
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued[file-isrc]`

Old text:

```
            if code is None:
                code = match.isrc_token(row.isrc) or pair_read.file_identity(cfg, row.path)[0]
            if code:
                codes.setdefault(code, []).append(row.content_id)
```

New text:

```
            if code is None:
                code = match.isrc_token(row.isrc)
            if code:
                codes.setdefault(code, []).append(row.content_id)
```

### `u208.M11_alias_off`

alias: read every account track as its own key, so two releases of one row are two keys again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M11_alias_off`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_release_added_on_the_account_as_the_row_leaves_rekordbox_is_never_taken_off`
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[database-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_sibling_placed_at_the_top_of_the_account_is_left_where_the_person_put_it`
  - `tests/test_sync_pair_tie.py::test_the_first_release_taken_off_while_a_later_one_stays_keeps_the_row`

Old text:

```
        return aliased.get(remote_id) or remote_key(remote_id)
```

New text:

```
        return remote_key(remote_id)
```

### `u208.M18_held_there_asks_provider`

plan_pair: with several releases of the row on the account, ask the provider as round one did

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M18_held_there_asks_provider`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_two_releases_already_on_the_account_take_the_lower_and_add_no_third`

Old text:

```
            elif isrc and held_there:
```

New text:

```
            elif False:
```

### `u208.M1_ask_any_agreeing`

_ask: ask the account without any_agreeing, so a tie between agreeing releases is refused as before U208

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M1_ask_any_agreeing`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_release_added_on_the_account_as_the_row_leaves_rekordbox_is_never_taken_off`
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[database-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_second_sync_asks_the_provider_nothing_about_a_linked_tie`
  - `tests/test_sync_pair_tie.py::test_a_sibling_placed_at_the_top_of_the_account_is_left_where_the_person_put_it`
  - `tests/test_sync_pair_tie.py::test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued[database-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_tie_remembered_as_a_miss_before_this_unit_is_asked_once_and_linked`
  - `tests/test_sync_pair_tie.py::test_a_tie_with_none_hearted_is_linked_to_the_lowest_release`
  - `tests/test_sync_pair_tie.py::test_both_releases_taken_off_the_account_take_the_row_out_of_rekordbox`
  - `tests/test_sync_pair_tie.py::test_one_release_taken_off_the_account_while_another_stays_changes_nothing[database-isrc]`
  - `tests/test_sync_pair_tie.py::test_one_release_taken_off_the_account_while_another_stays_changes_nothing[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_the_files_album_narrows_the_tie_before_the_lowest_is_taken`
  - `tests/test_sync_pair_tie.py::test_the_first_release_taken_off_while_a_later_one_stays_keeps_the_row`
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - ... and 1 more, see the JSON sidecar

Old text:

```
            album=album,
            any_agreeing=True,
        )
        or ""
```

New text:

```
            album=album,
            any_agreeing=False,
        )
        or ""
```

### `u208.M24_alias_unfrozen`

alias: read the links live, as the first fix round did, so a link the library lookup makes after the merge changes the key space

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M24_alias_unfrozen`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_release_added_on_the_account_as_the_row_leaves_rekordbox_is_never_taken_off`
  - `tests/test_sync_pair_tie.py::test_a_sibling_placed_at_the_top_of_the_account_is_left_where_the_person_put_it`

Old text:

```
        return aliased.get(remote_id) or remote_key(remote_id)
```

New text:

```
        return remote_key(canon[known[remote_id]]) if known.get(remote_id) in canon else remote_key(remote_id)
```

### `u208.M2_old_tie_miss_reused`

_ask: reuse a miss remembered with the tie's words, so a tie remembered before U208 is never asked again nor linked

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M2_old_tie_miss_reused`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_tie_remembered_as_a_miss_before_this_unit_is_asked_once_and_linked`

Old text:

```
    if held is not None and held.isrc == isrc and AGREEING_RELEASES not in held.reason:
```

New text:

```
    if held is not None and held.isrc == isrc:
```

### `u208.M9_here_lookup_dropped`

_owned: never look among the pair's own rows, so a sibling of a file ISRC row is queued for acquisition

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M9_here_lookup_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued[file-isrc]`

Old text:

```
    if rest and here is not None:
```

New text:

```
    if False:
```

### `r1453.U2_base_keeps_unread_keys`

R-1264's base strip gone: the base keeps an unread key, so an unread track is read as taken off the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1453.json`, row `U2_base_keeps_unread_keys`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`

Old text:

```
        if unread_keys:
            unseen |= {key for key in base_account if key in unread_keys}
```

New text:

```
        if False:
            unseen |= {key for key in base_account if key in unread_keys}
```

### `r1453.U5_account_keys_take_unread_only_rows`

the account's keys read every listed id, an unread only row included, so it is placed by the merge as a readable row

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1453.json`, row `U5_account_keys_take_unread_only_rows`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 30 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_finish_stopped_before_its_first_send_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - ... and 15 more, see the JSON sidecar

Old text:

```
            for remote_id in (listed_order or account_now)
            if alias(remote_id) in readable_keys
```

New text:

```
            for remote_id in (listed_order or account_now)
```

### `u226.M20_check_no_lag`

check: a lagging listing is compared as read rather than named as moved

- File: `src/cratekit/sync/pair_check.py`
- Source: `u226.json`, row `M20_check_no_lag`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 267 against a baseline of 267
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved`

Old text:

```
            if listing.window == provider_listing.WINDOW_LAGS:
                # U226. Neither read
```

New text:

```
            if False:
                # U226. Neither read
```

### `u226.M23_totals_no_read_backs`

sync_pair: the run's totals carry no read backs

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u226.json`, row `M23_totals_no_read_backs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 267 against a baseline of 267
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_the_runs_totals_carry_each_read_backs_readings_and_wait`

Old text:

```
        "read_backs": [record for d in done for record in d.read_backs],
```

New text:

```
        "read_backs": [],
```

### `u226.M22_lagging_not_per_pair`

PER_PAIR_REASONS: a lagging pair refuses the whole sync of every pair

- File: `src/cratekit/sync/pair_model.py`
- Source: `u226.json`, row `M22_lagging_not_per_pair`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 267 against a baseline of 267
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_lags_beside_a_partial_unpaged_read_holds_the_pair_and_says_why`

Old text:

```
        # U226. Its account playlist's window read lags its unpaged read.
        LAGGING,

```

New text:

```
(empty)
```

### `u226.M19_plan_no_hold`

plan_pair: a lagging pair is planned from its window rather than held

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u226.json`, row `M19_plan_no_hold`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 267 against a baseline of 267
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_a_named_pair_whose_window_lags_refuses_as_itself`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_lags_beside_a_partial_unpaged_read_holds_the_pair_and_says_why`

Old text:

```
        if listing.window == provider_listing.WINDOW_LAGS:
            raise _lagging(target.account_id, name)
```

New text:

```
        if False:
            raise _lagging(target.account_id, name)
```

### `u226.M21_plan_window_only`

plan_pair: the account side listed from its window alone

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u226.json`, row `M21_plan_window_only`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 267 against a baseline of 267
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_a_named_pair_whose_window_lags_refuses_as_itself`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_lags_an_order_past_the_unpaged_reads_first_page_plans_no_order`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_lags_beside_a_partial_unpaged_read_holds_the_pair_and_says_why`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_serves_an_old_order_plans_no_rekordbox_order`

Old text:

```
            reader.found, target.account_id, current=True

```

New text:

```
            reader.found, target.account_id, current=False

```

### `u284.S8_refusal_not_retryable`

searchers._refused_by_all: the refusal is not retryable, so a resumed sweep cannot ask again

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S8_refusal_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 381 against a baseline of 381
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_with_no_token_a_refusing_beatport_names_itself_its_date_and_the_token`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
        retryable=True,
        origin=("tagging", "searchers"),
        detail={
            "sources": [outcome.source for outcome in outcomes],
            "answers": [outcome.answer.value for outcome in outcomes],
            "notes": [outcome.note for outcome in outcomes],
            REFUSED_DETAIL: since,
```

New text:

```
        retryable=False,
        origin=("tagging", "searchers"),
        detail={
            "sources": [outcome.source for outcome in outcomes],
            "answers": [outcome.answer.value for outcome in outcomes],
            "notes": [outcome.note for outcome in outcomes],
            REFUSED_DETAIL: since,
```

### `r1830.M10_planned_number_not_asked`

renumber_memberships: write the new number whatever the row holds now

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M10_planned_number_not_asked`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`

Old text:

```
        f'WHERE "ID" = :key AND "{TRACK_NUMBER_COLUMN}" = :before'
```

New text:

```
        f'WHERE "ID" = :key AND :before = :before'
```

### `r1830.M11_held_object_left_stale`

renumber_memberships: leave the session's mapped rows holding the old number

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M11_held_object_left_stale`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_renumbering_writes_trackno_alone_and_a_held_row_reads_the_new_number`

Old text:

```
            session.expire(held)
```

New text:

```
            pass
```

### `r1830.M17_positions_never_read`

database_reading: read no membership positions, so the confinement plans nothing

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M17_positions_never_read`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`
  - `tests/test_sync_removed.py::test_two_removed_members_of_one_playlist_and_a_member_on_two_playlists`

Old text:

```
            if placed is not None:
```

New text:

```
            if False:
```

### `r1830.M23_unreadable_marker_passed_over`

removal_renumbering: plan around a NULL marker rather than refusing it, review round two's X1

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M23_unreadable_marker_passed_over`
- Moved: Anchored where u300-replay-after-a.json replayed it: moved by U300's split from src/cratekit/core/rb_writer.py to rb_removal.py, the same refusal of an unreadable marker in the removal's renumbering
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_an_unreadable_marker_in_a_playlist_to_renumber_refuses_with_nothing_written`

Old text:

```
    if unreadable:
```

New text:

```
    if False:
```

### `r1830.M8_renumbering_stamps_updated_at`

renumber_memberships: write updated_at beside TrackNo, a byte rekordbox did not write

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M8_renumbering_stamps_updated_at`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`
  - `tests/test_sync_removed.py::test_two_removed_members_of_one_playlist_and_a_member_on_two_playlists`

Old text:

```
        f'UPDATE "{MEMBERSHIP_TABLE}" SET "{TRACK_NUMBER_COLUMN}" = :after '
```

New text:

```
        f'UPDATE "{MEMBERSHIP_TABLE}" SET "{TRACK_NUMBER_COLUMN}" = :after, "updated_at" = CURRENT_TIMESTAMP '
```

### `r1830.M9_moved_row_not_refused`

renumber_memberships: a row that moved since the prepare is passed over silently

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M9_moved_row_not_refused`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`

Old text:

```
        if result.rowcount != 1:
```

New text:

```
        if False:
```

### `u288.M3_unmeasured_tables_skipped`

content_references: ask no table, so a My Tag, sampler or unknown table naming the row is never refused nor kept

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M3_unmeasured_tables_skipped`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[CREATE TABLE "someFutureTable" (ID TEXT PRIMARY KEY, ContentID TEXT)-INSERT INTO "someFutureTable" (ID, ContentID) VALUES ('x-1', ?)]`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "djmdSongSampler" (ID, ContentID) VALUES ('x-1', ?)]`

Old text:

```
        asked = [CONTENT_REFERENCE_COLUMN] if CONTENT_REFERENCE_COLUMN in names else []
```

New text:

```
        asked = []
```

### `u288.M8_memberships_kept`

remove_from_collection: delete from the five tables after the membership table only, so the track's memberships stay naming a row that is gone

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M8_memberships_kept`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removal_that_changes_anything_it_did_not_plan_is_refused_before_its_commit`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moves_any_other_membership_is_refused_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_commit_proves_the_removal_confined_before_it_commits`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    for table in COLLECTION_REMOVAL_TABLES[1:]:
```

New text:

```
    for table in COLLECTION_REMOVAL_TABLES[2:]:
```

### `r1830.M21_record_omits_the_rows`

write_into: name no renumbered row in the session record

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1830.json`, row `M21_record_omits_the_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`

Old text:

```
        if self.renumbered:
```

New text:

```
        if False:
```

### `r1830.M6_prepare_plans_no_renumbering`

CollectionRemoval.prepare: plan no renumbering, so the gap stays

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1830.json`, row `M6_prepare_plans_no_renumbering`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 17 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_an_unreadable_marker_in_a_playlist_to_renumber_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        return cls(db, ids, identity, columns, database_reading(db), removal_renumbering(db, ids))
```

New text:

```
        return cls(db, ids, identity, columns, database_reading(db), {})
```

### `r1830.M7_commit_skips_the_renumbering`

CollectionRemoval.commit: delete and never write the renumbering

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1830.json`, row `M7_commit_skips_the_renumbering`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 17 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_only_the_collection_removal_renumbers_memberships`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        renumber_memberships(self.db, self.renumbered)

```

New text:

```
(empty)
```

### `u288.M14_confinement_not_called`

CollectionRemoval.commit: skip the SQL confinement before the commit

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M14_confinement_not_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_renumbering_that_moves_any_other_membership_is_refused_with_nothing_written`
  - `tests/test_sync_removed.py::test_commit_proves_the_removal_confined_before_it_commits`

Old text:

```
        assert_collection_removal_confined(self.db, self.before, removed=self.content_ids)
        commit_guarded(
```

New text:

```
        commit_guarded(
```

### `u288.M5_prepare_liveness`

CollectionRemoval.prepare: drop the soft delete check, so a row rekordbox already removed is taken out as live

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M5_prepare_liveness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_prepare_refuses_a_row_not_live_and_a_database_with_no_identity`

Old text:

```
            if row is None or soft_deleted(
                row,
                message=(
                    f"the collection row {key!r} cannot say whether rekordbox removed it, "
```

New text:

```
            if row is None or False and soft_deleted(
                row,
                message=(
                    f"the collection row {key!r} cannot say whether rekordbox removed it, "
```

### `u288.M7_prepare_identity`

CollectionRemoval.prepare: drop the refusal of a database with no identity, so the record is bound to nothing

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M7_prepare_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_prepare_refuses_a_row_not_live_and_a_database_with_no_identity`

Old text:

```
        identity = database_id(db)
        if not identity:
```

New text:

```
        identity = database_id(db)
        if False:
```

### `r1830.M18_plan_counts_nothing`

plan_removed: count no renumbering, so the screen shows none

- File: `src/cratekit/sync/removed.py`
- Source: `r1830.json`, row `M18_plan_counts_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`

Old text:

```
        renumbered=len(rb_writer.CollectionRemoval.renumbering(db, offered)) if offered else 0,
```

New text:

```
        renumbered=0,
```

### `r1830.M19_digest_omits_the_count`

identity: leave the renumbering count out of the digest

- File: `src/cratekit/sync/removed.py`
- Source: `r1830.json`, row `M19_digest_omits_the_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`

Old text:

```
        "renumbered": plan.renumbered,
    }
```

New text:

```
    }
```

### `r1830.M22_applied_message_counts_nothing`

apply_removed: the result counts no renumbered membership, so the applied message says none

- File: `src/cratekit/sync/removed.py`
- Source: `r1830.json`, row `M22_applied_message_counts_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`

Old text:

```
        renumbered=len(removal.renumbered),
```

New text:

```
        renumbered=0,
```

### `u287.M10_gone_on_one_read`

read_one: read a playlist the account's list omits as gone without opening it by its id

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M10_gone_on_one_read`
- Moved: Anchored where u325-replay-after.json replayed it: Same read_one; the merged U320 work made the name a multi line expression that also reads a remembered name, and the row still inserts the early GONE return right after it, before the playlist is opened by its id
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_synced_playlist_nothing_records_that_neither_read_finds_offers_nothing`

Old text:

```
    name = (
        shown.name
        if shown is not None
        else (names or {}).get(account) or (prior.name if prior is not None else "")
    )

```

New text:

```
    name = (
        shown.name
        if shown is not None
        else (names or {}).get(account) or (prior.name if prior is not None else "")
    )
    if shown is None:
        return Listing(account=account, name=name, state=GONE, why="")

```

### `u287.M14_twin_is_own_filing`

plan_removed: leave the recorded twins out of the pass's own filing, so the landing's own twin keeps a track

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M14_twin_is_own_filing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 32 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[True]`
  - `tests/test_sync_removed.py::test_a_genre_playlist_of_a_native_routing_tree_keeps_nothing`
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before`
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_says_holds_none_is_read_empty_and_every_new_track_offered`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_refused_removal_gives_the_deletion_pass_no_position`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`
  - ... and 17 more, see the JSON sidecar

Old text:

```
            own = own_nodes.union(
                *(made.get(account, frozenset()) for account in held.accounts),
            )
```

New text:

```
            own = own_nodes
```

### `u287.M16_gone_holds_what_was_recorded`

Listing.holds: a gone playlist holds nothing, so a track its pass recorded on it can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M16_gone_holds_what_was_recorded`
- Moved: Anchored where u325-replay-after.json replayed it: Same Listing.holds guard; the merged U320 work named the holding states HOLDING and added WITHHELD to it, so the mutation takes GONE out of that set and leaves the rest, which is what removing GONE from (READ, GONE) did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_listing_holds_a_track_by_any_of_three_tests_and_only_a_read_or_gone_one_holds`

Old text:

```
        if self.state not in HOLDING:
```

New text:

```
        if self.state not in HOLDING - {GONE}:
```

### `u287.M19_old_prefix_is_synced`

synced: leave a playlist still titled with the retired swept prefix out of the synced set

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M19_old_prefix_is_synced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_playlist_still_titled_with_the_old_prefix_is_synced`

Old text:

```
                    if playlists.is_swept_name(one.name)
```

New text:

```
                    if False
```

### `u287.M4_held_before_the_pass`

_answer: drop the held before the pass keep, so a track the library owned when the job ran can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M4_held_before_the_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_says_holds_none_is_read_empty_and_every_new_track_offered`

Old text:

```
    if not held.carried:
        return replace(shown, why=HELD_BEFORE)
```

New text:

```
    if False:
        return replace(shown, why=HELD_BEFORE)
```

### `u287.M5_not_this_pass_file`

_answer: drop the filed folder keep, so a hand brought file the match found can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M5_not_this_pass_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_file_another_pass_filed_is_not_this_pass_s_file`
  - `tests/test_sync_removed.py::test_a_match_on_a_file_the_pass_did_not_file_is_kept`

Old text:

```
    if not held.brought:
        return replace(shown, why=NOT_THIS_PASS)
```

New text:

```
    if False:
        return replace(shown, why=NOT_THIS_PASS)
```

### `u287.M6_on_another_synced`

_answer: drop the still on another synced playlist keep

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M6_on_another_synced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_playlist_a_later_pass_swept_and_never_landed_still_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_playlist_still_titled_with_the_old_prefix_is_synced`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc`
  - `tests/test_sync_removed.py::test_a_track_hearted_on_the_account_is_kept_by_the_hearts`
  - `tests/test_sync_removed.py::test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording`

Old text:

```
    if still:
        return replace(shown, why=ON_ANOTHER, kept_by=still)
```

New text:

```
    if False:
        return replace(shown, why=ON_ANOTHER, kept_by=still)
```

### `u287.M7_in_a_playlist_of_yours`

_answer: drop the playlist of yours keep, so a track in a hand made playlist or All Favorites can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M7_in_a_playlist_of_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_genre_playlist_of_a_native_routing_tree_keeps_nothing`
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_track_in_a_playlist_of_yours_is_kept_and_its_own_filing_keeps_nothing`

Old text:

```
    if yours:
        return replace(shown, why=IN_YOURS, kept_by=yours)
```

New text:

```
    if False:
        return replace(shown, why=IN_YOURS, kept_by=yours)
```

### `u288.M16_stale_digest`

apply_removed: never refuse a plan that moved between the gate and the write

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M16_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u288.M17_only_the_offered`

apply_removed: take out every answered row that has one, kept rows included, not only the offered

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M17_only_the_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`

Old text:

```
    offered = plan.offered
    if not offered:
```

New text:

```
    offered = tuple(one for one in plan.answers if one.content_id)
    if not offered:
```

### `u288.M18_unmeasured_kept`

_answer: drop the keep of a row an unmeasured table names, so a vox tagged track is offered and then refuses the apply

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M18_unmeasured_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`

Old text:

```
    if unmeasured:
        return replace(shown, why=UNMEASURED, kept_by=tuple(sorted(unmeasured)))
```

New text:

```
    if False:
        return replace(shown, why=UNMEASURED, kept_by=tuple(sorted(unmeasured)))
```

### `u288.M20_read_back_refusal`

apply_removed: report a read back that disagrees as success

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M20_read_back_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`

Old text:

```
        violations = removal.read_back()
        if violations:
```

New text:

```
        violations = removal.read_back()
        if False:
```

### `r1830.M20_screen_omits_the_count`

facts: the gate's screen shows no renumbering

- File: `src/cratekit/sync/removed_cli.py`
- Source: `r1830.json`, row `M20_screen_omits_the_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`

Old text:

```
        "kept or left": len(plan.answers) - len(plan.offered),
        "memberships renumbered": plan.renumbered,
```

New text:

```
        "kept or left": len(plan.answers) - len(plan.offered),
        "memberships renumbered": 0,
```

### `u288.M21_gate_answer`

sync_removed: apply whatever the gate is answered, abort included

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u288.json`, row `M21_gate_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before`
  - `tests/test_sync_removed.py::test_abort_writes_nothing`
  - `tests/test_sync_removed.py::test_nothing_is_written_and_the_digest_holds_until_an_answer_moves`

Old text:

```
    if ctx.gate.require(_gate(ctx.entry), plan=data, context=facts(plan)) != "apply":
```

New text:

```
    if ctx.gate.require(_gate(ctx.entry), plan=data, context=facts(plan)) == "never":
```

### `u288.M22_closed_at_open`

written: open the write handle without refusing a running rekordbox

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u288.json`, row `M22_closed_at_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_rekordbox_running_at_the_write_refuses_before_any_session_opens`

Old text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
```

New text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=False, cfg=cfg)
```

### `u288.M15_append_past_highest`

add_memberships: keep the binding's count plus one, so an append after a removal lands on a live row's position

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u288.json`, row `M15_append_past_highest`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`, `tests/test_inbox_refill.py`
- Collected: 87 against a baseline of 87
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_track_added_after_a_removal_goes_past_the_highest_position`
  - `tests/test_sync_removed.py::test_two_appends_after_a_removal_each_take_the_next_position`

Old text:

```
        if added is not None and number <= highest:
```

New text:

```
        if False:
```

### `u320.M4_withheld_hearts_hold_nothing`

Listing.holds: leave the withheld hearts out of the holding states, so a hearted track they served is offered

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M4_withheld_hearts_hold_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_hearts_short_by_the_withheld_count_hold_every_heart_served`
  - `tests/test_sync_removed_gone.py::test_hearts_short_only_by_what_the_provider_withholds_read_whole_and_still_keep_a_heart`

Old text:

```
HOLDING = frozenset({READ, GONE, WITHHELD})
```

New text:

```
HOLDING = frozenset({READ, GONE})
```

### `u320.M6_any_failure_is_a_sighting`

read_one: record a sighting for any failure of an unlisted playlist, an outage included

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M6_any_failure_is_a_sighting`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_downloaded_playlist_gone_from_the_account_is_named_and_offers_nothing`
  - `tests/test_sync_removed_gone.py::test_a_playlist_that_failed_any_other_way_twice_a_day_apart_is_never_retired`
  - `tests/test_sync_removed_gone.py::test_pythons_own_not_found_classes_are_no_sighting_and_never_retire[file-not-found]`
  - `tests/test_sync_removed_gone.py::test_pythons_own_not_found_classes_are_no_sighting_and_never_retire[module-not-found]`

Old text:

```
                if said_none
                else prior
```

New text:

```
                if True
                else prior
```

### `u320.M8_retirement_never_applies`

read_one: never read a retired entry as retired

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M8_retirement_never_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a179s_shape_offers_the_track_once_the_gone_playlist_answers_not_found_a_day_apart`
  - `tests/test_sync_removed_gone.py::test_a_retired_downloaded_playlist_offers_none_of_its_tracks_and_holds_none_of_them`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_now_fails_another_way_stops_offers_this_run_and_stays_retired`
  - `tests/test_sync_removed_gone.py::test_retire_answered_retire_records_the_playlist_and_the_next_run_offers_past_it`
  - `tests/test_sync_removed_gone.py::test_the_control_taken_off_one_of_two_synced_playlists_is_kept_naming_the_other`

Old text:

```
            if said_none and noted is not None and noted.is_retired:
```

New text:

```
            if False:
```

### `u320.M21_retire_records_before_the_gate`

retire: record the reads before the gate, so its abort writes

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u320.json`, row `M21_retire_records_before_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_retire_lists_each_playlist_behind_its_gate_and_its_abort_writes_nothing`

Old text:

```
    reads = _read_synced(cfg, found, every=True, record_now=False)
```

New text:

```
    reads = _read_synced(cfg, found, every=True, record_now=True)
```

### `u320.M22_retire_ignores_its_answer`

retire: retire whatever the gate was answered

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u320.json`, row `M22_retire_ignores_its_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_retire_lists_each_playlist_behind_its_gate_and_its_abort_writes_nothing`

Old text:

```
    if ctx.gate.require(_gate(ctx.entry, RETIRE_GATE), plan=data, context=context) != "retire":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
```

New text:

```
    ctx.gate.require(_gate(ctx.entry, RETIRE_GATE), plan=data, context=context)
```

### `u320.M23_reads_never_recorded`

_read_synced: never write the record after the reads

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u320.json`, row `M23_reads_never_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 11 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a179s_shape_offers_the_track_once_the_gone_playlist_answers_not_found_a_day_apart`
  - `tests/test_sync_removed_gone.py::test_a_gone_downloaded_playlist_is_named_by_what_cratekit_calls_it`
  - `tests/test_sync_removed_gone.py::test_a_retired_downloaded_playlist_offers_none_of_its_tracks_and_holds_none_of_them`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_that_opens_again_is_read_again_and_the_retirement_cleared`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_the_account_lists_again_stops_every_offer_again`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_now_fails_another_way_stops_offers_this_run_and_stays_retired`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_opens_and_whose_rows_are_refused_is_cleared`
  - `tests/test_sync_removed_gone.py::test_a_sighting_on_a_later_date_but_under_a_day_after_the_first_retires_nothing`
  - `tests/test_sync_removed_gone.py::test_retire_offers_no_playlist_seen_before_whose_id_now_fails_another_way_and_says_so`
  - `tests/test_sync_removed_gone.py::test_retire_writes_every_reads_answer_with_the_retirement`
  - `tests/test_sync_removed_gone.py::test_the_control_taken_off_one_of_two_synced_playlists_is_kept_naming_the_other`

Old text:

```
    if record_now:
        record.update(removed.noted(reads))
```

New text:

```
    if False:
        record.update(removed.noted(reads))
```

### `u320.M24_record_read_as_empty`

_read_synced: plan over an empty record whatever it holds

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u320.json`, row `M24_record_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a179s_shape_offers_the_track_once_the_gone_playlist_answers_not_found_a_day_apart`
  - `tests/test_sync_removed_gone.py::test_a_retired_downloaded_playlist_offers_none_of_its_tracks_and_holds_none_of_them`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_that_opens_again_is_read_again_and_the_retirement_cleared`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_the_account_lists_again_stops_every_offer_again`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_now_fails_another_way_stops_offers_this_run_and_stays_retired`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_opens_and_whose_rows_are_refused_is_cleared`
  - `tests/test_sync_removed_gone.py::test_retire_answered_retire_records_the_playlist_and_the_next_run_offers_past_it`
  - `tests/test_sync_removed_gone.py::test_the_control_taken_off_one_of_two_synced_playlists_is_kept_naming_the_other`

Old text:

```
    sightings = record.read()
```

New text:

```
    sightings = record.read() and {}
```

### `u320.M25_person_retires_nothing`

retire: record the named playlists as sighted, never retired

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u320.json`, row `M25_person_retires_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_retire_answered_retire_records_the_playlist_and_the_next_run_offers_past_it`
  - `tests/test_sync_removed_gone.py::test_retire_writes_every_reads_answer_with_the_retirement`
  - `tests/test_sync_removed_gone.py::test_the_retire_gate_binds_across_midnight`

Old text:

```
                one.account: unavailable.retired_by_person(one.noted, moment)
```

New text:

```
                one.account: one.noted
```

### `u320.M14_any_status_is_not_found`

answered_unavailable: read any status as a not found

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M14_any_status_is_not_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_not_found_met_only_while_handling_another_failure_is_not_one`
  - `tests/test_sync_removed_gone.py::test_a_playlist_that_failed_any_other_way_twice_a_day_apart_is_never_retired`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_now_fails_another_way_stops_offers_this_run_and_stays_retired`
  - `tests/test_sync_removed_gone.py::test_only_a_not_found_answer_is_read_as_unavailable`
  - `tests/test_sync_removed_gone.py::test_retire_names_a_gone_playlist_whose_id_now_fails_another_way`
  - `tests/test_sync_removed_gone.py::test_retire_offers_no_playlist_seen_before_whose_id_now_fails_another_way_and_says_so`
  - `tests/test_sync_removed_gone.py::test_retire_offers_no_playlist_whose_id_failed_any_other_way`
  - `tests/test_sync_removed_gone.py::test_the_real_adapter_reads_a_404_as_unavailable_and_a_server_error_not`

Old text:

```
            return answered_not_found(link)
```

New text:

```
            return True
```

### `u221.R1_hold_only_a_twin`

held_for_choice: drop the twin test, so a pair that is no twin reads by time and holds every undated track the library lacks

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R1_hold_only_a_twin`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_unread.py`
- Collected: 174 against a baseline of 174
- Kills: 21 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_a_track_carrying_no_isrc_is_still_queued_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_still_queued`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[cancelled]`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[failed]`
  - `tests/test_sync_pair.py::test_a_track_this_pair_alone_lists_is_queued_once_beside_anothers_job`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`
  - `tests/test_sync_pair.py::test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale`
  - `tests/test_sync_pair.py::test_another_pairs_job_that_no_longer_reads_stops_no_plan`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    if pair is None or not getattr(pair, "twin", False):
        return False
```

New text:

```
    if pair is None:
        return False
```

### `r838-c.R2_remark_clears`

mark_record.record_marked: append a second entry for a re-mark by the same pass rather than replacing the first

- File: `src/cratekit/sync/mark_record.py`
- Source: `r838-c.json`, row `R2_remark_clears`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_mark_after_an_unmark_clears_the_stamp`

Old text:

```
                    if (entry.pass_name, entry.playlist_id) == (pass_name, playlist_id):
                        entries[index] = fresh
                        break
```

New text:

```
                    if False:
                        entries[index] = fresh
                        break
```

### `r838-d.R3b_stamp_target`

mark_record.record_unmarked: stamp the playlist's mark under any pass, so another pass's mark reads as put back

- File: `src/cratekit/sync/mark_record.py`
- Source: `r838-d.json`, row `R3b_stamp_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`

Old text:

```
                if (entry.pass_name, entry.playlist_id) == (pass_name, playlist_id):
                    entries[index] = replace(entry, unmarked=when)
```

New text:

```
                if entry.playlist_id == playlist_id:
                    entries[index] = replace(entry, unmarked=when)
```

### `r838-a.U1_refuse_stranger`

unmark._narrowed: drop the refusal, so a playlist the pass never marked is silently passed over rather than refused

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U1_refuse_stranger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_the_pass_never_marked_is_refused_whatever_its_title`

Old text:

```
    if strangers:
        raise _blocked(
```

New text:

```
    if False:
        raise _blocked(
```

### `r838-a.U3_pass_filter`

unmark: take every pass's marks as the named pass's, so a playlist the pass never marked is planned

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U3_pass_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`
  - `tests/test_sync_unmark.py::test_a_pass_the_record_holds_nothing_for_is_a_gated_plan_of_nothing`

Old text:

```
        tuple(entry for entry in every if entry.pass_name == name),
```

New text:

```
        tuple(entry for entry in every),
```

### `r838-a.U4_already_unmarked_stamp`

unmark._item: ignore the unmarked stamp, so a second run is decided by the title alone

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U4_already_unmarked_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_second_run_plans_nothing_and_still_asks`

Old text:

```
    if entry.unmarked:
        return {
```

New text:

```
    if False:
        return {
```

### `r838-a.U5_marked_again`

unmark._item: ignore a later mark by another pass, so this pass's unmark takes off that pass's prefix

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U5_marked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`

Old text:

```
    later = _later(entry, every)
    if later:
```

New text:

```
    later = _later(entry, every)
    if False:
```

### `r838-a.U6_later_order`

unmark._later: an EARLIER mark by another pass also supersedes, so the latest pass's own unmark is refused

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U6_later_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`

Old text:

```
        and other.marked > entry.marked
```

New text:

```
        and other.marked != entry.marked
```

### `r838-a.U8_title_already_back`

unmark._item: no already-put-back branch, so a title already restored is reported as retitled by hand

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U8_title_already_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_title_already_put_back_is_skipped_without_a_stamp`

Old text:

```
    if current == entry.name:
```

New text:

```
    if False:
```

### `r838-b.U10_digest_names`

unmark._payload: the digest omits the planned renames, so an answer to one plan carries out another

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U10_digest_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_an_answer_is_stale_once_the_account_moves`

Old text:

```
            (item["id"], item["marked_as"], item["to"])
            for item in items
            if item["action"] == UNMARK
```

New text:

```
            (item["id"], item["marked_as"], item["to"])
            for item in items
            if False
```

### `r838-b.U13_recheck`

unmark: no recheck against the second listing, so a title changed after the answer is renamed anyway

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U13_recheck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_that_changes_between_the_plan_and_the_rename_is_said`

Old text:

```
            if now.get(identity) != entry.to:
```

New text:

```
            if False:
```

### `r838-b.U15_rename_target`

unmark: rename to the title the mark wrote rather than the one before it

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U15_rename_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`
  - `tests/test_sync_unmark.py::test_a_pass_that_marked_three_plans_three_renames_back_and_applies_them`
  - `tests/test_sync_unmark.py::test_a_playlist_retitled_by_hand_since_the_mark_is_listed_and_left`
  - `tests/test_sync_unmark.py::test_a_playlist_that_changes_between_the_plan_and_the_rename_is_said`
  - `tests/test_sync_unmark.py::test_a_playlist_the_account_no_longer_lists_is_said_and_left`
  - `tests/test_sync_unmark.py::test_a_title_already_put_back_is_skipped_without_a_stamp`
  - `tests/test_sync_unmark.py::test_playlist_given_twice_narrows_to_both_marks_named`
  - `tests/test_sync_unmark.py::test_playlist_narrows_to_the_marks_named`

Old text:

```
            remote.rename_playlist(identity, entry.name)
```

New text:

```
            remote.rename_playlist(identity, entry.to)
```

### `r838-b.U16_part_way_names`

unmark._failed_part_way: report nothing put back, so a partial failure loses what landed

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U16_part_way_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_failure_part_way_names_what_was_put_back`

Old text:

```
        "unmarked": list(landed),
```

New text:

```
        "unmarked": [],
```

### `r838-b.U9_renamed_since`

unmark._item: plan any title carrying the prefix, so a playlist retitled by hand with the prefix kept is renamed

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U9_renamed_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_retitled_by_hand_since_the_mark_is_listed_and_left`

Old text:

```
    if current != entry.to:
        how =
```

New text:

```
    if not playlists.is_swept_name(current):
        how =
```

### `r838-c.U7b_not_listed_rerun`

U7 measured again after the not-listed test was added: no NOT_LISTED branch, so a playlist the account dropped falls through to the title comparison

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-c.json`, row `U7b_not_listed_rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_the_account_no_longer_lists_is_said_and_left`

Old text:

```
    if current is None:
        return {
            **base,
            "action": SKIP,
            "reason": NOT_LISTED,
```

New text:

```
    if current is None and False:
        return {
            **base,
            "action": SKIP,
            "reason": NOT_LISTED,
```

### `u246.S14_unmark_narrowed_empty`

unmark: an empty narrowed set, so --playlist narrows every mark away and the verb puts nothing back

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u246.json`, row `S14_unmark_narrowed_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`, `tests/test_gate_shown_plan.py`
- Collected: 47 against a baseline of 47
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_playlist_given_twice_narrows_to_both_marks_named`
  - `tests/test_sync_unmark.py::test_playlist_narrows_to_the_marks_named`
  - `tests/test_sync_unmark.py::test_the_mark_screen_says_a_playlist_was_put_back`

Old text:

```
    narrowed = set(named)
```

New text:

```
    narrowed = set()
```

### `u246.S15_unmark_narrowed_first_only`

unmark: narrow to the first playlist named alone, so a second --playlist is dropped

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u246.json`, row `S15_unmark_narrowed_first_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`, `tests/test_gate_shown_plan.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_playlist_given_twice_narrows_to_both_marks_named`

Old text:

```
    narrowed = set(named)
```

New text:

```
    narrowed = set(named[:1])
```

### `u240.M1_two_names_take_the_first`

_by_label: a line naming two registered labels gives the file the first one's genre

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M1_two_names_take_the_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 337 against a baseline of 337
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_two_registered_labels_is_refused_for_that_file`
  - `tests/test_tag_folder_copyright.py::test_a_searchers_park_reaches_the_job_as_a_park_on_a_file_its_line_could_not_settle`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`

Old text:

```
    if len(named) != 1 or not named[0].genre:
```

New text:

```
    if not named or not named[0].genre:
```

### `u240.M2_no_genre_label_named`

_by_label: a line naming one label with no genre is not recorded on the file

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M2_no_genre_label_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 337 against a baseline of 337
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_one_label_with_no_genre_is_asked_of_the_catalogues`
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_two_registered_labels_is_refused_for_that_file`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`

Old text:

```
        return _Labelled(None, own, copyright_labels=tuple(found.label for found in named))
```

New text:

```
        return _Labelled(None, own, copyright_labels=())
```

### `u240.M3_tag_no_longer_outranks_the_line`

_by_label: a file's own label tag no longer comes first, so the line or --label decides a tagged file

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M3_tag_no_longer_outranks_the_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 337 against a baseline of 337
- Kills: 17 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`
  - `tests/test_label_genre.py::test_a_file_of_a_label_with_no_genre_is_searched_as_today`
  - `tests/test_label_genre.py::test_a_folder_of_mixed_labels_tags_each_by_its_own`
  - `tests/test_label_genre.py::test_a_label_tag_reaches_its_genre_with_no_label_named`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_puls_file_with_no_genre_gets_its_labels_genre_with_no_searcher_called`
  - `tests/test_label_genre.py::test_a_puls_file_with_no_picture_is_searched_for_its_art_only`
  - `tests/test_label_genre.py::test_a_refusal_on_the_art_search_does_not_fail_a_puls_file`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_an_art_search_for_a_labelled_file_never_offers_the_general_catalogue_its_isrc`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_verbs_label_names_the_label_of_a_file_with_no_tag_and_the_tag_wins`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    if own:

```

New text:

```
    if False:

```

### `u240.M5_wrong_field_read`

_by_label: the label tag read where the copyright line should be

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M5_wrong_field_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 337 against a baseline of 337
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_label_batch_with_every_catalogue_blocked_lands_tagged_by_label`
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_one_label_with_no_genre_is_asked_of_the_catalogues`
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_two_registered_labels_is_refused_for_that_file`
  - `tests/test_tag_folder_copyright.py::test_a_mixed_folder_with_every_catalogue_blocked_tags_each_file_by_its_line`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_an_unregistered_file_in_the_batch_is_left_untagged_and_its_item_fails`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`
  - `tests/test_tag_folder_copyright.py::test_the_needles_are_frozen_with_the_genres_when_the_sweep_is_queued`
  - `tests/test_tag_folder_copyright.py::test_the_report_names_each_file_by_label_by_catalogue_or_not_at_all`
  - `tests/test_tag_folder_copyright.py::test_the_tails_tag_step_lands_a_label_batch_with_every_catalogue_blocked`
  - `tests/test_tag_folder_copyright.py::test_two_labels_sharing_a_display_name_never_lend_each_other_a_genre`

Old text:

```
        line = held["copyright"] or ""
```

New text:

```
        line = held["label"] or ""
```

### `u240.M7_line_labels_dropped_from_result`

tag_one: the labels an unsettled line named never reach the result

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M7_line_labels_dropped_from_result`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 337 against a baseline of 337
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_one_label_with_no_genre_is_asked_of_the_catalogues`
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_two_registered_labels_is_refused_for_that_file`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`

Old text:

```
        copyright_labels=tier.copyright_labels,
```

New text:

```
        copyright_labels=(),
```

### `u172.C1_tail_skips_guess`

through_name: never run the guess after tag folder

- File: `src/cratekit/cli/tail.py`
- Source: `u172.json`, row `C1_tail_skips_guess`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`
- Collected: 333 against a baseline of 333
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_sync_bandcamp.py::test_a_labels_new_release_and_its_owned_one_reach_the_gate_named_for_the_label`
  - `tests/test_sync_bandcamp.py::test_the_labels_release_reaches_the_same_gate_with_rekordbox_open_on_the_host`
  - `tests/test_sync_bandcamp.py::test_the_tail_runs_on_the_absolute_batch_folder`
  - `tests/test_sync_land.py::test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`

Old text:

```
        if step == TAG:
            guess(chain, folder, pass_name)
```

New text:

```
        if False:
            guess(chain, folder, pass_name)
```

### `u172.C2_guess_without_pass`

guess_argv: never name the pass, so no playlist votes in a pass

- File: `src/cratekit/cli/tail.py`
- Source: `u172.json`, row `C2_guess_without_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`
- Collected: 333 against a baseline of 333
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`
  - `tests/test_tag_guess.py::test_the_guess_is_named_with_a_pass_only_when_one_is_given`

Old text:

```
*([PASS_FLAG, pass_name] if pass_name else [])
```

New text:

```
*([])
```

### `u56-catalogue-searcher-and-tag-workers.R35_extra_rides_beside_progress`

A per verb detail at the top level is an undeclared field on job_state/1, so a consumer generated from the committed schema rejects every envelope

- File: `src/cratekit/core/jobs.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R35_extra_rides_beside_progress`
- Moved: Anchored where u325-replay-after.json replayed it: U298 replaced tagging.shell.reported with core.jobs.reported, which the tagging shell imports under the same name; the same placement of extra under progress, with the local renamed counted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 47 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[-read_back1-no-genre]`
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[Ambient-read_back0-genre-specific]`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - ... and 32 more, see the JSON sidecar

Old text:

```
    counted = dict(progress(store, job.job_id))
    if extra:
        counted.update(extra)
    return {
        "job_id": job.job_id,
```

New text:

```
    counted = dict(progress(store, job.job_id))
    return {
        **dict(extra or {}),
        "job_id": job.job_id,
```

### `u281.C4_source_blocked_counts_unsent_as_sent`

_unread_warnings: count the unsent files among the searches sent, so the warning claims searches never made

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C4_source_blocked_counts_unsent_as_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
        sent = asked - held
```

New text:

```
        sent = asked
```

### `u56-catalogue-searcher-and-tag-workers.R19_folder_queues_no_items`

The zero item rule broken at its source: a job with nothing to claim drives straight to SUCCEEDED over a folder nothing walked

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R19_folder_queues_no_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 41 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_real_track_beside_the_staging_tree_is_still_queued`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_retried_job_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_a_searcher_that_raises_part_way_fails_only_its_own_item`
  - ... and 26 more, see the JSON sidecar

Old text:

```
            item_ids=tuple(str(path.relative_to(folder)) for path in files),
```

New text:

```
            item_ids=(),
```

### `u281.C3_unsent_never_counted`

_summary: never count a file a catalogue was not sent

- File: `src/cratekit/tagging/summary.py`
- Source: `u281.json`, row `C3_unsent_never_counted`
- Moved: Anchored where u306-replay-after-c.json replayed it: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
                if note.startswith(searchers.NOT_SENT):
                    not_sent[source] += 1
```

New text:

```
                if False:
                    not_sent[source] += 1
```

### `u56-catalogue-searcher-and-tag-workers.R23_summary_from_the_queue`

The report counts what was queued rather than what ran, so a half finished sweep reports every file as handled

- File: `src/cratekit/tagging/summary.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R23_summary_from_the_queue`
- Moved: Anchored where u306-replay-after-c.json replayed it: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 27 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_report_from_before_the_repair_is_counted_under_no_status`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - ... and 12 more, see the JSON sidecar

Old text:

```
    for report in artifacts.committed(cfg, job_id):
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
```

New text:

```
    for report in []:
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
```

### `u192.F6_queue_only_never`

queue_only: always False, so --queue-only drives the job anyway

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F6_queue_only_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`, `tests/test_label_genre.py`, `tests/test_sync_land.py`
- Collected: 409 against a baseline of 409
- Kills: 20 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`
  - `tests/test_analysis_workers.py::test_an_item_renamed_before_its_row_moved_resumes_as_finished`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[restamp]`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[run]`
  - `tests/test_analysis_workers.py::test_the_shared_tail_step_queues_only_and_drives_its_job_once`
  - `tests/test_label_genre.py::test_an_unreadable_registry_warns_and_refuses_only_a_sweep_that_named_a_label`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    return bool(getattr(args, "queue_only", False))
```

New text:

```
    return False
```

### `u281.C1_refusal_said_as_blocked`

_unread_phrase: say a refusal as 'blocked on N' again, the wording the card replaces

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C1_refusal_said_as_blocked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_beatport_refusal.py`
- Collected: 138 against a baseline of 138
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_some_of_whose_refusals_were_a_challenge_says_how_many`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`

Old text:

```
    if word != searchers.Answer.BLOCKED.value:
        return f"{source} {word} on {count}"
```

New text:

```
    if True:
        return f"{source} {word} on {count}"
```

### `u281.W7_worker_run_key_without_attempt`

tagging.cli.handle: name the run by the job alone, so a resumed run inherits the last run's stop

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `W7_worker_run_key_without_attempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_beatport_refusal.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
            declared, refusals=searchers.for_run(f"{job.job_id}@{job.attempts}")
```

New text:

```
            declared, refusals=searchers.for_run(f"{job.job_id}")
```

### `r1103.H2_refusal_slug`

handle: the item fails under the general analysis-write-failed slug instead of retag's own

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H2_refusal_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_reserved_causes.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
        raise refuse(
            retag.UNWRITTEN_REASON,
```

New text:

```
        raise refuse(
            "analysis-write-failed",
```

### `r791-b.C1_artifact_answers`

handle: the artifact records only the first source's answer

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C1_artifact_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_four_real_misses_are_no_hit_and_carry_no_unread_warning`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
                for said in result.answers
            ],
```

New text:

```
                for said in result.answers[:1]
            ],
```

### `r791-b.C2_artifact_unread`

handle: the artifact's unread map is always empty

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C2_artifact_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
                if said.source in result.unread
```

New text:

```
                if False
```

### `r791-b.C3_summary_counts_answers`

_summary: count no answers

- File: `src/cratekit/tagging/summary.py`
- Source: `r791-b.json`, row `C3_summary_counts_answers`
- Moved: Anchored where u306-replay-after-d.json replayed it: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
                counted[word] += 1
```

New text:

```
                counted[word] += 0
```

### `r791-b.C9_unread_skip_zero_filled`

_summary: count only the three skip reasons that predate R-791

- File: `src/cratekit/tagging/summary.py`
- Source: `r791-b.json`, row `C9_unread_skip_zero_filled`
- Moved: Anchored where u306-replay-after-d.json replayed it: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_skip_reason_reaches_the_report_and_not_only_the_artifact`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
    skipped = dict.fromkeys(tag_engine.SKIP_REASONS, 0)
```

New text:

```
    skipped = dict.fromkeys(tag_engine.SKIP_REASONS[:3], 0)
```

### `r791-b.T1_sources_unread_disposition`

tag_one: a decline naming unread sources is reported no-hit

- File: `src/cratekit/tagging/tag.py`
- Source: `r791-b.json`, row `T1_sources_unread_disposition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 12 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`
  - `tests/test_tagging_engine.py::test_a_decline_beside_an_unread_catalogue_is_sources_unread_and_not_no_hit`

Old text:

```
        elif hit.unread:
```

New text:

```
        elif False:
```

### `u244.M24_upgrade_keeps_a_held_table`

_vocabularies: do not pass over a vocabulary table the copy already declares

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u244.json`, row `M24_upgrade_keeps_a_held_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`, `tests/test_doctor.py`
- Collected: 468 against a baseline of 468
- Kills: 22 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_current_copy_with_every_entry_is_ok`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_made_before_u133_takes_the_discogs_table_and_loads_after_the_holds_edits`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_made_before_u244_gains_the_discogs_table_whole`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_that_declares_its_vocabulary_inline_is_held_not_forced`
  - `tests/test_taxonomy_upgrade.py::test_a_discogs_table_the_copy_declares_is_never_touched`
  - `tests/test_taxonomy_upgrade.py::test_a_rerun_plans_nothing`
  - `tests/test_taxonomy_upgrade.py::test_a_second_playlist_class_under_another_id_holds_favorites`
  - `tests/test_taxonomy_upgrade.py::test_a_second_run_plans_nothing_and_asks_nothing`
  - `tests/test_taxonomy_upgrade.py::test_a_table_whose_row_names_no_folder_in_the_copy_is_held_with_the_loaders_words`
  - `tests/test_taxonomy_upgrade.py::test_a_version_2_copy_gains_favorites_and_soul_in_place_and_keeps_every_line`
  - `tests/test_taxonomy_upgrade.py::test_a_version_4_copy_with_every_entry_plans_nothing`
  - `tests/test_taxonomy_upgrade.py::test_a_vocabulary_row_whose_tag_files_where_the_template_shares_the_word_is_not_named`
  - `tests/test_taxonomy_upgrade.py::test_a_word_the_shipped_template_files_twice_is_not_a_clash`
  - `tests/test_taxonomy_upgrade.py::test_every_bucket_of_the_copy_filing_a_word_is_named_not_the_first`
  - `tests/test_taxonomy_upgrade.py::test_jazz_is_held_while_non_electronic_still_files_its_words_and_every_place_is_named`
  - ... and 7 more, see the JSON sidecar

Old text:

```
        if isinstance(present, dict) and source in present:
            continue
```

New text:

```
        if False:
            continue
```

### `u302.W9c_configuration_rules_dropped`

what W9 holds: prefix_rules with no caller map returns no rules, so a recorded path is never resolved through the configuration

- File: `src/cratekit/write/trees.py`
- Source: `u302.json`, row `W9c_configuration_rules_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_naming_apply_cli.py`, `tests/test_routing_workers.py`, `tests/test_deferred_routing.py`
- Collected: 437 against a baseline of 437
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_a_remapped_volume_still_protects_its_file[prefix_map0]`
  - `tests/test_routing_workers.py::test_an_export_location_under_a_retired_volume_name_resolves_through_the_prefix_map`

Old text:

```
        return list(locations.prefix_rules(cfg.resolved_prefix_map()))
```

New text:

```
        return []
```

### `u129-author.A4_archive_raise_fails_landing`

Let an account archive raise escape the landing write after rows are in the library

- File: `src/cratekit/intake/land_native.py`
- Source: `u129-author.json`, row `A4_archive_raise_fails_landing`
- Moved: Anchored where u307-replay-after-b.json replayed it: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[raised]`
  - `tests/test_u129_set_account_playlist.py::test_landing_archive_failure_after_write_is_a_warning[transient]`

Old text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    except Exception as exc:
        message = (
            exc.cause.message if isinstance(exc, CratekitError) else f"{type(exc).__name__}: {exc}"
        )
        return [
            {
                "code": LAND_ARCHIVE_FAILED,
                "message": (
                    f"the account archive could not finish after the landing wrote "
                    f"({message}); the batch is in the library, run crate export "
                    f"archive over the set once the account can be reached"
                ),
            }
        ]
    return list(warnings)

```

New text:

```
    _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    return list(warnings)

```

### `u129-author.A5_archive_return_discarded`

Discard apply_archive warnings so a not-renamed return is silent on the landed envelope

- File: `src/cratekit/intake/land_native.py`
- Source: `u129-author.json`, row `A5_archive_return_discarded`
- Moved: Anchored where u307-replay-after-b.json replayed it: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_a_landing_archive_not_renamed_is_a_warning_on_the_envelope, test_landing_archive_surfaces_changed_since_plan_as_a_warning, were folded by the trim into test_a_landing_archive_failure_is_a_warning_on_the_envelope, test_landing_archive_failure_after_write_is_a_warning, the archive warning checks, now the not renamed case beside the changed since plan one
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[not-renamed]`
  - `tests/test_u129_set_account_playlist.py::test_landing_archive_failure_after_write_is_a_warning[changed]`

Old text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    except Exception as exc:

```

New text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
        warnings = []
    except Exception as exc:

```

### `u242.M12_composite`

strip: neither record first nor confirm the hold, so a stripped playlist is in no record

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M12_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 11 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_ceiling_stop_names_what_landed_and_a_second_run_resumes`
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_a_stripped_playlist_named_like_a_followed_label_is_still_filed_by_its_mark`
  - `tests/test_u242_taken.py::test_every_old_title_is_restored_by_unmark_of_the_strip`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_no_rename_is_made_for_a_playlist_the_record_does_not_hold`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    taken_cli.migrate(cfg, listed)
    held = record.taken_ids()
    unheld = [identity for identity in planned if identity not in held]
```

New text:

```
    held = record.taken_ids()
    unheld = []
```

### `u242.M12_strip_skips_the_migration`

strip: rename without recording the prefixed playlists as taken first

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M12_strip_skips_the_migration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 14 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_ceiling_stop_names_what_landed_and_a_second_run_resumes`
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_a_stripped_playlist_named_like_a_followed_label_is_still_filed_by_its_mark`
  - `tests/test_u242_taken.py::test_a_title_changed_since_the_plan_is_not_renamed`
  - `tests/test_u242_taken.py::test_every_old_title_is_restored_by_unmark_of_the_strip`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_playlist_narrows_and_refuses_a_playlist_with_no_prefix`
  - `tests/test_u242_taken.py::test_the_strip_records_each_old_title_before_its_rename`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_is_put_back_renames_back`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    taken_cli.migrate(cfg, listed)
    held = record.taken_ids()
```

New text:

```
    held = record.taken_ids()
```

### `u242.M4_plan_reads_no_ledger`

plan: hand exclusion an empty ledger, so sync all offers every stripped playlist

- File: `src/cratekit/sync/playlists.py`
- Source: `u242.json`, row `M4_plan_reads_no_ledger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_all.py`
- Collected: 161 against a baseline of 161
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_that_landed_is_not_owed_a_second_time`
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_mark_since_u242_writes_no_title_and_the_playlist_is_never_offered`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    taken = taken_ids(cfg)

    sweep = Sweep(
```

New text:

```
    taken = frozenset()

    sweep = Sweep(
```

### `u242.M1_exclusion_reads_the_ledger`

exclusion: answer SWEPT from the legacy prefix alone, so a stripped taken playlist is offered as new

- File: `src/cratekit/sync/playlists.py`
- Source: `u242.json`, row `M1_exclusion_reads_the_ledger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 230 against a baseline of 230
- Kills: 5 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_mark_since_u242_writes_no_title_and_the_playlist_is_never_offered`
  - `tests/test_u242_taken.py::test_exclusion_answers_swept_for_a_taken_playlist_with_no_prefix`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    if is_taken(playlist.playlist_id, playlist.name, taken):
        return Excluded.SWEPT
```

New text:

```
    if is_swept_name(playlist.name):
        return Excluded.SWEPT
```

### `u242.M5_pending_marks_ignores_the_ledger`

pending_marks: skip only a prefixed title, so a playlist already taken is taken again

- File: `src/cratekit/sync/playlists.py`
- Source: `u242.json`, row `M5_pending_marks_ignores_the_ledger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 230 against a baseline of 230
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_that_landed_is_not_owed_a_second_time`

Old text:

```
        and not is_taken(identity, listed[identity], sweep.taken)
```

New text:

```
        and not is_swept_name(listed[identity])
```

### `u242.M2_is_taken_drops_the_id`

is_taken: read the title alone, the ledger ignored by every reader

- File: `src/cratekit/sync/playlists.py`
- Source: `u242.json`, row `M2_is_taken_drops_the_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_organize_root.py`
- Collected: 285 against a baseline of 285
- Kills: 14 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_year_playlist_held_as_taken_with_no_prefix_proves_its_tracks_downloaded`
  - `tests/test_organize_root.py::test_filing_reads_a_stripped_hand_mark_as_it_read_the_prefixed_one`
  - `tests/test_sync_all.py::test_a_mark_that_landed_is_not_owed_a_second_time`
  - `tests/test_sync_mark.py::test_a_partial_failure_names_what_was_marked`
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_mark_since_u242_writes_no_title_and_the_playlist_is_never_offered`
  - `tests/test_u242_taken.py::test_a_stripped_playlist_named_like_a_followed_label_is_still_filed_by_its_mark`
  - `tests/test_u242_taken.py::test_exclusion_answers_swept_for_a_taken_playlist_with_no_prefix`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_is_taken_holds_a_recorded_id_whatever_its_title_and_a_legacy_prefix`
  - `tests/test_u242_taken.py::test_the_inspiration_set_rule_reads_a_stripped_set_as_the_prefixed_one`
  - `tests/test_u242_taken.py::test_twins_reads_a_stripped_custom_playlist_as_downloaded`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    return str(playlist_id or "") in taken or is_swept_name(name)
```

New text:

```
    return is_swept_name(name)
```

### `u242.M3_is_taken_drops_the_prefix`

is_taken: read the ledger alone, so a legacy prefixed title the migration has not recorded reads as new

- File: `src/cratekit/sync/playlists.py`
- Source: `u242.json`, row `M3_is_taken_drops_the_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_organize_root.py`, `tests/test_organize.py`
- Collected: 382 against a baseline of 382
- Kills: 21 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mark_put_back_is_no_mark_and_the_playlist_stays`
  - `tests/test_organize.py::test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine`
  - `tests/test_organize.py::test_only_root_removes_debris_and_empties_on_the_gate_and_files_the_legacy_folder`
  - `tests/test_organize_root.py::test_a_debris_copy_given_a_track_since_the_plan_is_kept_and_the_rest_removed`
  - `tests/test_organize_root.py::test_a_debris_copy_whose_tracks_could_not_all_be_read_is_left`
  - `tests/test_organize_root.py::test_a_debris_copy_with_a_track_the_label_folder_lacks_is_left_naming_it`
  - `tests/test_organize_root.py::test_a_followed_labels_recorded_folder_is_read_whatever_it_is_called_now`
  - `tests/test_organize_root.py::test_a_refusal_part_way_stops_and_names_what_was_removed`
  - `tests/test_organize_root.py::test_a_second_run_on_a_clean_root_plans_nothing`
  - `tests/test_organize_root.py::test_filing_reads_a_stripped_hand_mark_as_it_read_the_prefixed_one`
  - `tests/test_organize_root.py::test_four_identical_debris_copies_with_every_track_filed_plan_four_removals`
  - `tests/test_organize_root.py::test_the_plans_digest_moves_when_a_row_changes`
  - `tests/test_sync_all.py::test_a_playlist_the_source_system_already_prefixed_is_not_prefixed_twice`
  - `tests/test_sync_all.py::test_a_slim_pass_queues_each_new_account_playlist_under_the_shared_run`
  - `tests/test_sync_all.py::test_the_label_batch_debris_is_not_queued_as_intake`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return str(playlist_id or "") in taken or is_swept_name(name)
```

New text:

```
    return str(playlist_id or "") in taken
```

### `u242.M26_release_stamps_no_mark`

sync unmark: a release leaves the pass's legacy mark unstamped, so the next migration or strip takes it again

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u242.json`, row `M26_release_stamps_no_mark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_unmark.py`
- Collected: 78 against a baseline of 78
- Kills: 3 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_release_that_fails_part_way_names_what_was_let_go`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`

Old text:

```
            if identity in by_id and not by_id[identity].unmarked:
                record.record_unmarked(name, identity)
```

New text:

```
            if False:
                record.record_unmarked(name, identity)
```

### `u242.M22_unmark_releases_nothing`

sync unmark: never plan a release, so a pass's taken playlists cannot be let go

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u242.json`, row `M22_unmark_releases_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_unmark.py`, `tests/test_label_playlists.py`, `tests/test_export_set.py`
- Collected: 197 against a baseline of 197
- Kills: 7 (killed)
- Killed:
  - `tests/test_export_set.py::test_sync_unmark_takes_the_archive_mark_off_again`
  - `tests/test_label_playlists.py::test_sync_unmark_takes_the_label_mark_off_again`
  - `tests/test_u242_taken.py::test_a_release_that_fails_part_way_names_what_was_let_go`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_unmark_lets_go_a_pass_mark_with_no_write_to_the_account`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`
  - `tests/test_u242_taken.py::test_unmark_playlist_narrows_the_releases`

Old text:

```
    taken_held = held is not None and held.held
```

New text:

```
    taken_held = False
```

### `u181.C3_unscored_flag_ignored`

analyze vocals: ignore --unscored, so the whole folder is queued

- File: `src/cratekit/vocals/cli.py`
- Source: `u181.json`, row `C3_unscored_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`
- Collected: 105 against a baseline of 105
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_analyze_step_rescores_after_analyze_run_and_before_the_restamp`
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_over_a_folder_whose_headed_files_all_carry_a_score_queues_nothing`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`

Old text:

```
    unscored = bool(getattr(ctx.args, "unscored", False))
```

New text:

```
    unscored = False
```

### `u181.V1_unavailable_ignores_bound_loader`

vocals.unavailable: ask missing_requirement even with a loader bound, so a bound fake reads as unable

- File: `src/cratekit/analysis/vocals.py`
- Source: `u181.json`, row `V1_unavailable_ignores_bound_loader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`, `tests/test_doctor.py`
- Collected: 522 against a baseline of 522
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_pass_whose_vocal_model_can_score_says_so_and_asks_nothing`
  - `tests/test_sync_land.py::test_the_analyze_step_rescores_after_analyze_run_and_before_the_restamp`
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`
  - `tests/test_sync_land.py::test_the_outbound_hearts_write_stays_behind_its_own_gate`
  - `tests/test_vocals_cli.py::test_the_one_test_takes_a_bound_loader_as_able`

Old text:

```
    return None if loader_bound() else missing_requirement()
```

New text:

```
    return missing_requirement()
```

### `u181.T1_rescore_ignores_unable`

tail.rescore: queue the rescore although the model cannot score here

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T1_rescore_ignores_unable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_sync_land.py::test_the_answered_gate_takes_the_pass_on_and_the_summary_says_vocals_were_skipped`
  - `tests/test_sync_land.py::test_the_tail_asks_the_vocal_model_before_analyze_run_binds_its_loader`
  - `tests/test_vocals_cli.py::test_the_tails_rescore_asks_nothing_of_a_model_that_cannot_score`

Old text:

```
    if unable is not None:
        chain.summary["vocal_rescore"] = "skipped"
```

New text:

```
    if False:
        chain.summary["vocal_rescore"] = "skipped"
```

### `u300.S15_terminal_probe_local`

record_acknowledgment asks the part's own terminal probe, so a patched probe is not asked

- File: `src/cratekit/core/session_ack.py`
- Source: `u300.json`, row `S15_terminal_probe_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_second_mint_replaces_the_record_and_moves_the_window`
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`
  - `tests/test_session_cli.py::test_the_cli_mints_an_acknowledgment_a_real_destructive_verb_then_spends`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`
  - `tests/test_write_session.py::test_the_terminal_probe_the_mint_uses_by_default_is_the_real_one`

Old text:

```
        probe = terminal or _session().has_controlling_terminal
```

New text:

```
        probe = terminal or has_controlling_terminal
```

### `r598-a.A5_holder_never_recorded`

open_session: drop the holder instead of recording it, so no record is ever provably orphaned and a hard kill is a dead end again

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A5_holder_never_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 8 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_release_that_only_abandons_is_a_change_and_passes_the_contract`
  - `tests/test_write_session.py::test_a_supplied_holder_reaches_the_record_as_well_as_the_lock`
  - `tests/test_write_session.py::test_abandon_orphaned_sessions_ends_only_the_orphans`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`
  - `tests/test_write_session.py::test_the_sweep_ends_only_the_orphans_it_was_shown`

Old text:

```
        detail={HOLDER_KEY: holder.to_json()} if holder is not None else {},
```

New text:

```
        detail={},
```

### `r598-a.A1_state_check_widened_to_non_terminal`

orphaned: accept any non terminal record rather than only open, so awaiting-import and committed-unverified records with a dead holder are abandoned and their own remedies hidden

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A1_state_check_widened_to_non_terminal`
- Moved: Anchored where u300-replay-after-b.json replayed it: moved by U300's split from src/cratekit/core/session.py to session_holders.py, the same check in orphaned, its names read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_the_two_states_with_their_own_remedy_are_never_abandoned[awaiting-import]`
  - `tests/test_session_cli.py::test_the_two_states_with_their_own_remedy_are_never_abandoned[committed-unverified]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[awaiting-import-gone-False]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[committed-unverified-gone-False]`

Old text:

```
    if record.state is not _session().SessionState.OPEN:
        return False
    recorded = record.detail.get(_session().HOLDER_KEY)
```

New text:

```
    if record.terminal:
        return False
    recorded = record.detail.get(_session().HOLDER_KEY)
```

### `r598-a.A2_no_holder_read_as_gone`

orphaned: read a record with no recorded holder as orphaned, so every intake landing left open for a deferred placement is abandoned

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A2_no_holder_read_as_gone`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_open_record_that_names_no_holder_is_never_abandoned`
  - `tests/test_write_session.py::test_abandon_orphaned_sessions_ends_only_the_orphans`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-None-False]`

Old text:

```
    if not isinstance(recorded, Mapping):
        return False
```

New text:

```
    if not isinstance(recorded, Mapping):
        return True
```

### `r598-a.A3_liveness_not_consulted`

orphaned: skip holder_alive and judge every open record with a holder orphaned, so a running write's record is ended behind it

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A3_liveness_not_consulted`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 8 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[alive]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_write_session.py::test_abandon_orphaned_sessions_ends_only_the_orphans`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-here-False]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-other-host-False]`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
    return not holder_alive(holder, here=here)
```

New text:

```
    return True
```

### `r647-a.B14_machine_not_read_back`

Holder.from_json: ignore the recorded machine, so a record or lock read from disk never names one

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B14_machine_not_read_back`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_write_session.py::test_the_holder_carries_all_five_identifying_fields`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
            machine=str(data.get("machine", UNKNOWN_IDENTITY)),
```

New text:

```
            machine=UNKNOWN_IDENTITY,
```

### `r647-a.B15_machine_not_written`

Holder.to_json: omit the machine, so nothing on disk carries it

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B15_machine_not_written`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_write_session.py::test_the_holder_carries_all_five_identifying_fields`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
            "machine": self.machine,

```

New text:

```
(empty)
```

