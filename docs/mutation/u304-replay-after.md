# Mutation table: u304-replay-after

Measured by `scripts/mutate.py` on 2026-11-23 05:02 UTC, branch `HEAD` at `fd78d188`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22911 collected. pytest invocations for this batch: 95.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 93, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/5752b730-82d2-5bb0-b120-3c1da5ca9238/scratchpad/u304-replay-after-known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 648 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22911 against 22911. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1289.M10_warning_ready_filter` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 1 | killed |
| `r1289.M11_warning_absent` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `r1289.M12_warning_promise` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `r1289.M13_warning_names` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `r227.C6_composed_limit_spelled` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M5_unwired` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M6_no_append` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M7_note_before_describe` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r504-b.B10_check_no_numbers` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B7_sync_drops_short` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B8_check_passes` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B9_all_withheld_says_no_hearts` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r515-operator.S13_sweep_no_warning` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r835-c.S2_sync_hands_the_ledger_to_the_sweep_again` | `src/cratekit/sync/cli.py` | user | 4 file(s) | 315 | 1 | killed |
| `r837-a.A17_sweep_hand_off` | `src/cratekit/sync/cli.py` | user | 5 file(s) | 371 | 1 | killed |
| `u109-a.A1_plan_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 9 | killed |
| `u109-a.A2_guided_empty` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 6 | killed |
| `u109-a.A3_no_check_row` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u109-a.A4_summary_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u109-a.A5_gate_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A6_refusal_step_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u109-a.A7_refusal_step_first` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A8_row_reworded` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u147-c.M19_sweep_handoff` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u73-c.C3_next_only_with_intake_jobs` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 5 | killed |
| `u73-c.C4_next_counts_intake_jobs_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u73-c.C5_next_check_row` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B10_refused_check_status` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u74-b.B11_gate_screen` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B12_next_step_outbound_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B1_source_id_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 9 | killed |
| `u74-b.B2_compose_skips_inbound` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 16 | killed |
| `u74-b.B3_queue_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u74-b.B4_filed_outbound_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 10 | killed |
| `u74-b.B5_inbound_refusal_not_counted` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B6_inbound_warning` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B7_block_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 13 | killed |
| `u74-b.B8_check_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 10 | killed |
| `u74-b.B9_check_wording` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A10_export_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 15 | killed |
| `u74.A11_queue_not_bound` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 17 | killed |
| `u74.A12_run_id_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u74.A3_handler_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A4_source_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A5_library_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A6_open_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u74.A7_in_flight_guard` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u74.A8_empty_guard` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 4 | killed |
| `u74.A9_listing_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 19 | killed |
| `r1056.S1_no_landing_step_names_intake_missing` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 102 | 4 | killed |
| `r1056.S2_unreachable_step_names_sync` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 102 | 1 | killed |
| `r361-a.A7_mark_verb_forgets_debris` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 116 | 1 | killed |
| `r361-a.A8_mark_verb_respells_the_word` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 116 | 1 | killed |
| `r361-a.A9_reword_the_why` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 116 | 1 | killed |
| `r777-confirm.N4_plain_name` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777-confirm.N7_digest_marks` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N10_screen_says_pass` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N11_exclusive` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N12_no_landing_required` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 4 | killed |
| `r777.N18_unreachable_called_bridge` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N19_digest_landings` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N5_bridge_accepted` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 2 | killed |
| `r777.N6_no_reread` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 2 | killed |
| `r777.N9_proof_is_file` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 4 | killed |
| `u174.M10_dedupe` | `src/cratekit/sync/mark_cli.py` | maintainer | 3 file(s) | 191 | 1 | killed |
| `u174.M11_stranger_before_no_jobs` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M1_stranger_refusal` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 2 | killed |
| `u174.M2_narrowing` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 4 | killed |
| `u174.M3_unfinished_refusal` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 3 | killed |
| `u174.M4_unfinished_rows_outstanding` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M5_unfinished_job` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M6_unfinished_reports` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M7_digest_names_the_narrowing` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 2 | killed |
| `u174.M8_screen_names_the_narrowing` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M9_verb_passes_the_flag` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 5 | killed |
| `u174.P1_bridge_plans_no_native_pass` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.P2_unreachable_is_refused` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u242.M21_mark_cli_already_marked_by_title` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 115 | 1 | killed |
| `u82-b.B5_not_listed_is_skipped` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-b.B6_a_failed_job_is_skipped` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 2 | killed |
| `u82-b.B7_unread_reports_hold_the_playlist` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 2 | killed |
| `u82-b.B8_an_offered_track_is_owed` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-c.C1_a_tombstoned_track_is_settled` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-c.C2_one_outstanding_track_holds_the_playlist` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 9 | killed |
| `u82-c.C3_landed_is_told_from_owned` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 2 | killed |
| `u82-c.C9_the_accounts_reason_is_kept` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-d.B2_paths_compared_resolved_again` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `r838-c.R1_library_bound` | `src/cratekit/sync/mark_record.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-c.R2_remark_clears` | `src/cratekit/sync/mark_record.py` | maintainer | 1 file(s) | 32 | 1 | killed |
| `r838-d.R3b_stamp_target` | `src/cratekit/sync/mark_record.py` | user | 1 file(s) | 32 | 1 | killed |
| `u242.M6_record_v1_reads_a_taken_key` | `src/cratekit/sync/mark_record.py` | user | 2 file(s) | 78 | 1 | killed |
| `u242.M9_take_overwrites_a_held_entry` | `src/cratekit/sync/mark_record.py` | user | 2 file(s) | 115 | 1 | killed |
| `r777.N1_empty_proof` | `src/cratekit/sync/marks.py` | maintainer | 2 file(s) | 100 | 1 | killed |
| `r777.N2_neither_proof` | `src/cratekit/sync/marks.py` | maintainer | 2 file(s) | 100 | 1 | killed |
| `r777.N3_engine_unchecked` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 100 | 3 | killed |
| `u82-a.A1_stat_oserror_is_the_refusal` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 184 | 4 | killed |
| `u82-a.A2_a_folder_is_not_a_file` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 184 | 1 | killed |
| `u82-a.A3_an_empty_file_is_not_proof` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 184 | 2 | killed |
| `r1360.F1_walk_uncounted` | `src/cratekit/sync/pair_calls.py` | user | 15 file(s) | 827 | 8 | killed |
| `r1360.F2_step_a_page` | `src/cratekit/sync/pair_calls.py` | user | 15 file(s) | 827 | 3 | killed |
| `r1360.F3_judged_without_walk` | `src/cratekit/sync/pair_calls.py` | user | 15 file(s) | 827 | 4 | killed |
| `u210.R23_margin` | `src/cratekit/sync/pair_calls.py` | user | 8 file(s) | 265 | 1 | killed |
| `u220.C1_moves_head_rule` | `src/cratekit/sync/pair_calls.py` | user | 10 file(s) | 306 | 5 | killed |
| `u226.M24_estimate_no_unpaged` | `src/cratekit/sync/pair_calls.py` | user | 3 file(s) | 137 | 16 | killed |
| `u231.M24_forecast_without_the_settle_reading` | `src/cratekit/sync/pair_calls.py` | user | 2 file(s) | 46 | 4 | killed |
| `u246.S7_pair_calls_before_empty` | `src/cratekit/sync/pair_calls.py` | user | 2 file(s) | 46 | 5 | killed |
| `u246.S8_pair_calls_after_empty` | `src/cratekit/sync/pair_calls.py` | user | 2 file(s) | 46 | 1 | killed |
| `u246.S9_pair_calls_after_stale` | `src/cratekit/sync/pair_calls.py` | user | 2 file(s) | 46 | 1 | killed |
| `r1264-composites.M7_account_add_filter` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 20 | 1 | killed |
| `r1264.M12_record_holds_back` | `src/cratekit/sync/pair_write.py` | user | 2 file(s) | 49 | 5 | killed |
| `r1264.M14_check_unread_moved` | `src/cratekit/sync/pair_check.py` | user | 2 file(s) | 49 | 1 | killed |
| `r1264.M15_check_unread_as_tuple` | `src/cratekit/sync/pair_check.py` | user | 1 file(s) | 20 | 1 | killed |
| `r1264.M18_identity_unread` | `src/cratekit/sync/pair_model.py` | user | 2 file(s) | 49 | 1 | killed |
| `r1264.M19_warning` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 20 | 1 | killed |
| `r1264.M1_unread_dropped` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 95 | 17 | killed |
| `r1264.M20_item` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 20 | 7 | killed |
| `r1264.M2_unread_isrc_on_account` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 87 | 1 | killed |
| `r1264.M3_account_keys_listing_order` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 117 | 3 | killed |
| `r1264.M4_account_keys_filter` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 96 | 12 | killed |
| `r1264.M5_unread_keys_empty` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 66 | 4 | killed |
| `r1264.M6_base_strip` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 66 | 3 | killed |
| `r1264.M8_order_after_listing` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 117 | 3 | killed |
| `r1264.M9_firsts_keep_unread` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 96 | 2 | killed |
| `r1372.K17_no_let_go_at_snapshot` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 664 | 2 | killed |
| `r1372.K1_no_carry` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 664 | 9 | killed |
| `r1372.K22_mark_guard_gone` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 2 | killed |
| `r1372.K23_mark_guard_inclusive` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 1 | killed |
| `r1372.K4_carry_unwritten_not_refused` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 664 | 1 | killed |
| `r1372.K6_reader_ignores_carried` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 7 | killed |
| `r1372.K7_copy_never_gives_way` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 1 | killed |
| `r1372.K8_copy_gives_way_to_any_plan` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 1 | killed |
| `r1372.K9_carried_unread_unsaid` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 1 | killed |
| `r1376.F11_leader_lost` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 4 | killed |
| `r1376.F13_snapshot_guard_inclusive` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 34 | killed |
| `r1376.F1_first_stop_none` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 7 | killed |
| `r1376.F3_call_site_gone` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 6 | killed |
| `r1376.F4_first_sync_unrecorded_only` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 1 | killed |
| `r1376.F5_first_sync_marked_only` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 318 | killed |
| `r1376.F6_every_sync_first` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 4 | killed |
| `r1383-digest.M8_digest_drops_hold` | `src/cratekit/sync/pair_model.py` | user | 5 file(s) | 162 | 1 | killed |
| `r1383-digest.M9_digest_always_keyed` | `src/cratekit/sync/pair_model.py` | maintainer | 5 file(s) | 162 | 1 | killed |
| `r1383.M10_warning_never_said` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 137 | 5 | killed |
| `r1383.M12_unlisted_said_as_records` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 1 | killed |
| `r1383.M13_records_unnamed` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 2 | killed |
| `r1383.M14_hold_before_awaiting` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 2 | killed |
| `r1383.M15_hold_before_twin` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 1 | killed |
| `r1383.M16_zero_said_as_count` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 1 | killed |
| `r1383.M17_total_uncounted` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 108 | 2 | killed |
| `r1383.M18_sampled_own_landed_step` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 1 | killed |
| `r1383.M19_sampled_mirrors_empty` | `src/cratekit/sync/pair_read.py` | user | 3 file(s) | 137 | 11 | killed |
| `r1383.M1_scan_drops_unread` | `src/cratekit/sync/pair_read.py` | user | 4 file(s) | 183 | 5 | killed |
| `r1383.M2_hold_branch_removed` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 4 | killed |
| `r1383.M3_hold_without_isrc` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 1 | killed |
| `r1383.M4_hold_while_readable` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 27 | killed |
| `r1383.M5_hold_dropped_from_plan` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 2 | killed |
| `r1383.M6_gate_item_dropped` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 137 | 2 | killed |
| `r1383.M7_gate_item_side` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 108 | 2 | killed |
| `r1385.M10_reason_dropped` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 7 | killed |
| `r1385.M11_name_fallback` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 293 | 1 | killed |
| `r1385.M12_check_reads_no_job` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 293 | 2 | killed |
| `r1385.M13_warning_unsplit` | `src/cratekit/sync/pair_screen.py` | user | 8 file(s) | 293 | 1 | killed |
| `r1385.M14_warning_here_dropped` | `src/cratekit/sync/pair_screen.py` | user | 8 file(s) | 293 | 2 | killed |
| `r1385.M15_failed_jobs_hold` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 293 | 2 | killed |
| `r1385.M1_no_job_holds_anything` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 293 | 13 | killed |
| `r1385.M2_other_jobs_not_asked` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 6 | killed |
| `r1385.M4_plan_not_asked` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 3 | killed |
| `r1385.M6_ask_not_registered` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 3 | killed |
| `r1385.M8_own_reads_every_job` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 6 | killed |
| `r1385.M9_own_reads_no_job` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 8 | killed |
| `r1394.P1_counts_never_written` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 4 | killed |
| `r1394.P2_counts_not_carried` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 1 | killed |
| `r1394.P3_begun_answers_no_recorder` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 5 | killed |
| `r1394.P4_finish_from_landed` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 2 | killed |
| `r1394.P5_finish_from_any_path_reading` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 6 | killed |
| `r1394.P6_off_path_held` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 10 | killed |
| `r1394.P7_unknown_named_as_landed` | `src/cratekit/sync/pair_model.py` | user | 20 file(s) | 752 | 1 | killed |
| `r1394.P8_every_move_named_as_a_stop` | `src/cratekit/sync/pair_model.py` | user | 20 file(s) | 752 | 1 | killed |
| `r1394.P9_finish_not_held_to_the_agreed_reading` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 2 | killed |
| `r1404.S3_scope_every_pair` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 13 | killed |
| `r1411.W1_finish_passes_no_agreed` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 10 | killed |
| `r1411.W2_finish_passes_agreed_only_with_nothing_else` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 7 | killed |
| `r1411.W3_agreed_is_the_asked_order` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 10 | killed |
| `r1411.W4_agreed_is_the_checks_listing` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 2 | killed |
| `r1416.M10_cli_account_write_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 12 | killed |
| `r1416.M7_cli_tells_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 4 | killed |
| `r1416.M8_cli_tells_not_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 2 | killed |
| `r1416.M9_cli_scope_key_only` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 119 | killed |
| `r1416.S3_scope_under_the_folder` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 119 | killed |
| `r1418.F1_agreed_is_the_readable_tracks` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1418.F2_agreed_passed_for_an_empty_reading` | `src/cratekit/sync/pair_write.py` | maintainer | 10 file(s) | 394 | 1 | killed |
| `r1418.F3_agreed_passed_only_for_an_empty_reading` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 11 | killed |
| `r1418.F4_agreed_only_without_adds_or_removes` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 7 | killed |
| `r1418.F5_plans_reading_without_unread_ids` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1420-b.B2_beyond_tail_unread_pinned` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 1 | killed |
| `r1420.B1_beyond_order_unread` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 8 | killed |
| `r1420.B3_beyond_removals_asked` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 3 | killed |
| `r1420.C1_continued_ignored` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 764 | 4 | killed |
| `r1420.C3_continued_read_after_the_mark` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 764 | 1 | killed |
| `r1420.C4_carried_record_unread` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 764 | 2 | killed |
| `r1420.E2_finish_agreed_dropped` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 764 | 10 | killed |
| `r1420.N1_fix_reverted` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 7 | killed |
| `r1420.N2_moves_begun_ignored` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 4 | killed |
| `r1420.N3_finish_read_too` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 2 | killed |
| `r1420.N5_order_always_read` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 6 | killed |
| `r1420.N6_call_site_never_reads_order` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 764 | 8 | killed |
| `r1432-composites.C4_finish_reads_the_listing_unfinished` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 61 | killed |
| `r1432.E1_listed_rule_puts_it_first` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 18 | killed |
| `r1432.P10_warning_says_it_stays` | `src/cratekit/sync/pair_screen.py` | user | 10 file(s) | 394 | 2 | killed |
| `r1432.P3_target_id_no_longer_listed_put_back` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 3 | killed |
| `r1432.P4_target_id_already_held_put_twice` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 8 | killed |
| `r1432.P5_target_placed_by_the_listing` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 11 | killed |
| `r1432.P6_target_behind_the_first_held` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 19 | killed |
| `r1432.P7_none_held_goes_last` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 2 | killed |
| `r1432.P8_placed_in_front_of_its_neighbour` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 22 | killed |
| `r1434.F7_ordering_start_from_the_readable_tracks` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 3 | killed |
| `r1434.M1_write_that_sent_nothing_read_on_its_whole_path` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 2 | killed |
| `r1434.M2_plan_reads_a_write_that_sent_nothing_on_its_whole_path` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.M3_readable_move_after_a_write_that_sent_nothing_read_on_its_whole_path` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.M4_hold_promises_the_accounts_order_for_an_unread_move` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.M5_hold_withholds_the_lead_from_a_readable_reorder` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.S1_sent_nothing_off_path_waits_for_settled_readings` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 7 | killed |
| `r1434.S3_unread_track_placed_at_the_front` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 22 | killed |
| `r1434.S5_folded_base_keeps_unread_keys` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1446-b.C1_composite_no_unread_left_out` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 155 | 6 | killed |
| `r1446-c.F1_every_unread_kept_its_place` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 264 | 2 | killed |
| `r1446-c.F2_no_unread_id_read_as_moved` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 264 | 3 | killed |
| `r1446-c.F3_readable_ids_weighed_as_unread` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 264 | 3 | killed |
| `r1446.M14_plan_flag_dropped` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1446.M1_no_readable_check` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 6 | killed |
| `r1446.M4_unread_moved_not_set` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 7 | killed |
| `r1446.M8_no_settled_reading_reads_no_move` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1446.M9_unsettled_reading_compared` | `src/cratekit/sync/pair_plan.py` | maintainer | 10 file(s) | 394 | 1 | killed |
| `r1446.S3_u225_finish_whatever_was_read` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 12 | killed |
| `r1453.S4_unread_keys_keep_a_readable_release` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 2 | killed |
| `r1453.U1_unread_keys_unaliased` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1453.U2_base_keeps_unread_keys` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1453.U4_removal_takes_only_the_linked_release` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1453.U5_account_keys_take_unread_only_rows` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 30 | killed |
| `u130-b.B1_short_base_unnarrowed` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B4_no_isrc_still_asked` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B5_readd_old_rule` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B6_requeue` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 76 | 3 | killed |
| `u130-b.B7_set_playlist_in_scope` | `src/cratekit/sync/pair_model.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B8_tree_name_in_scope` | `src/cratekit/sync/pair_model.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B9_stale_pair_blocks_all` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-c.C1_half_written_snapshot` | `src/cratekit/sync/pair_write.py` | user | 1 file(s) | 76 | 6 | killed |
| `u147-c.M20_pair_scope` | `src/cratekit/sync/pair_model.py` | user | 1 file(s) | 35 | 1 | killed |
| `u198.C10_unpair_account_gone` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C11_unpair_rekordbox_gone` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 2 | killed |
| `u198.C1_miss_reuse` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 168 | 2 | killed |
| `u198.C2_miss_isrc` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C3_unread_remembered` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C4_tie_remembered` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C5_folder_twice` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C6_folder_others` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C7_title_taken` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C8_folder_gone` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C9_account_only` | `src/cratekit/sync/pair_write.py` | user | 3 file(s) | 168 | 1 | killed |
| `u202-composites.C10_reads_account` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 160 | 1 | killed |
| `u202-composites.C3_composite` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 160 | 3 | killed |
| `u202-composites.C8_scope` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 160 | 1 | killed |
| `u202.C1_after_synced` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 160 | 1 | killed |
| `u202.C4_dates_recorded` | `src/cratekit/sync/pair_write.py` | user | 3 file(s) | 160 | 6 | killed |
| `u202.C5_released` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 160 | 2 | killed |
| `u202.C7_twice` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 160 | 1 | killed |
| `u207.P1_pair_screens_remembered_miss` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 154 | 1 | killed |
| `u207.P2_pair_never_screens` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 154 | 2 | killed |
| `u208.M11_alias_off` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 5 | killed |
| `u208.M18_held_there_asks_provider` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 1 | killed |
| `u208.M1_ask_any_agreeing` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 16 | killed |
| `u208.M24_alias_unfrozen` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 2 | killed |
| `u208.M2_old_tie_miss_reused` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 1 | killed |
| `u208.M4_tie_flag_dropped` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 97 | 2 | killed |
| `u208.M5_tied_rows_not_gathered` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 97 | 2 | killed |
| `u208.M6_facts_line_dropped` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 97 | 1 | killed |
| `u208.M7_totals_tied_zero` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 97 | 2 | killed |
| `u208.M8_item_flag_dropped` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 97 | 1 | killed |
| `u208.M9_here_lookup_dropped` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 2 | killed |
| `u209.C10_reverse_recheck` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 2 | killed |
| `u209.C11_home_of` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C12_brought_folder` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C13_jobs_queued` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 2 | killed |
| `u209.C3_withheld` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C4_rekordbox_gone` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C5_memberships` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 5 | killed |
| `u209.C6_discovered_place` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 5 | killed |
| `u209.C7_made_left_behind` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C8_rows_gone` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C9_unpaired_back` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.H1_offer_mismatch_ignored` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u210.R10_check_todo` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R11_part_written` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 6 | killed |
| `u210.R12_our_folders` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 5 | killed |
| `u210.R14_asked_before` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 9 | killed |
| `u210.R16_forecast_line` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 2 | killed |
| `u210.R18_beyond_order` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R19_beyond_gained` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R1_made_step_read` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R20_beyond_lost` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R21_check_queued` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R22_landed_read` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R2_resumed_move` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R3_made_here_folder` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R4_rekordbox_landed` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 2 | killed |
| `u210.R5_queue_once` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R8_done_step` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 3 | killed |
| `u210.R9_skip_done` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 1 | killed |
| `u216-m14.M14_moment_any_folder` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 1 | killed |
| `u216.M13_unrecorded_off` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 3 | killed |
| `u216.M15_before_rule_off` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 10 | killed |
| `u216.M16_copy_rule_off` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 5 | killed |
| `u216.M18_copy_all_titles` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 2 | killed |
| `u216.M19_place_held_empty` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 7 | killed |
| `u216.M20_made_drops_held` | `src/cratekit/sync/pair_write.py` | user | 12 file(s) | 385 | 9 | killed |
| `u220.P2_session_tolerated` | `src/cratekit/sync/pair_model.py` | user | 10 file(s) | 306 | 2 | killed |
| `u220.P5_no_stop_after_loop` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 306 | 9 | killed |
| `u221.R10_digest_without_the_hold` | `src/cratekit/sync/pair_model.py` | user | 3 file(s) | 154 | 1 | killed |
| `u221.R11_no_warning_per_twin` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 78 | 1 | killed |
| `u221.R1_hold_only_a_twin` | `src/cratekit/sync/pair_plan.py` | user | 4 file(s) | 174 | 21 | killed |
| `u221.R2_recorded_hold_never_holds` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 9 | killed |
| `u221.R3_recorded_hold_holds_everything` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 8 | killed |
| `u221.R4_undated_not_held` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 2 | killed |
| `u221.R5_time_rule_never_holds` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 2 | killed |
| `u221.R6_time_rule_always_holds` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 2 | killed |
| `u221.R7_plan_ignores_the_hold` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 10 | killed |
| `u221.R8_hold_before_awaiting` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 1 | killed |
| `u221.R9_gate_names_no_held_track` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 78 | 10 | killed |
| `u225.M14_superseded_unchecked` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 664 | 4 | killed |
| `u225.M15_fold_despite_skip` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 1 | killed |
| `u225.M16_account_base_unfolded` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 1 | killed |
| `u225.M17_rekordbox_base_unfolded` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 1 | killed |
| `u225.M20_stopped_not_passed` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 664 | 3 | killed |
| `u225.M21_start_from_asked` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 664 | 1 | killed |
| `u225.M22_written_always` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 664 | 1 | killed |
| `u225.M23_links_dropped` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 664 | 1 | killed |
| `u225.M24_unread_unsaid` | `src/cratekit/sync/pair_screen.py` | user | 19 file(s) | 664 | 2 | killed |
| `u226.M19_plan_no_hold` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 267 | 2 | killed |
| `u226.M20_check_no_lag` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 267 | 1 | killed |
| `u226.M21_plan_window_only` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 267 | 4 | killed |
| `u226.M22_lagging_not_per_pair` | `src/cratekit/sync/pair_model.py` | user | 8 file(s) | 267 | 1 | killed |
| `u226.M23_totals_no_read_backs` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 267 | 1 | killed |
| `u229.M10_file_isrc_fallback` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 293 | 10 | killed |
| `u229.M11_mirror_cache` | `src/cratekit/sync/pair_read.py` | maintainer | 8 file(s) | 293 | 1 | killed |
| `u229.M12_own_mirrors_bypass_cache` | `src/cratekit/sync/pair_read.py` | maintainer | 8 file(s) | 293 | 1 | killed |
| `u229.M15_wide_landed_needs_rest` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 1 | killed |
| `u229.M1_wide_landed_step` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 7 | killed |
| `u229.M2_wide_landed_reads_own_only` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 293 | 1 | killed |
| `u229.M3_wide_jobs_step` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 1 | killed |
| `u229.M4_wide_jobs_own_only` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 1 | killed |
| `u229.M5_wide_jobs_strict` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 1 | killed |
| `u229.M6_config_error_not_caught` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 293 | 1 | killed |
| `u229.M8_own_landing_first` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 1 | killed |
| `u229.M9_landed_dedup` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 293 | 1 | killed |
| `u229.S1_ambiguous_count` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 2 | killed |
| `u229.S2_own_landed_step` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 293 | 1 | killed |
| `u231.M10_moved_unrecorded` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 1 | killed |
| `u231.M12_settle_takes_any_reading` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 12 | killed |
| `u231.M14_settle_reading_not_kept` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 2 | killed |
| `u231.M15_pending_not_read` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 26 | killed |
| `u231.M16_shown_order_not_finished` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 3 | killed |
| `u231.M18_reading_before_the_moves_kept` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 1 | killed |
| `u231.M20_every_reading_kept` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 1 | killed |
| `u231.M22_root_playlist_named_gig_ready` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 1 | killed |
| `u231.M23_carried_moving_unread` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 2 | killed |
| `u231.M7_continue_resends` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 6 | killed |
| `u231.M8_no_record_sends_blind` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 1 | killed |
| `u234.O11_after_not_replaced` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 1 | killed |
| `u234.O12_kept_reading_of_any_run` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 2 | killed |
| `u234.O13_kept_reading_before_the_stop` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 2 | killed |
| `u234.O1_off_path_dropped_from_the_finish` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 21 | killed |
| `u234.O21_gate_says_on_path` | `src/cratekit/sync/pair_screen.py` | user | 21 file(s) | 764 | 2 | killed |
| `u234.O22_finishing_note_silent` | `src/cratekit/sync/pair_screen.py` | user | 21 file(s) | 764 | 3 | killed |
| `u234.O23_off_path_flag_on_every_finish` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 1 | killed |
| `u234.O25_on_path_reading_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 5 | killed |
| `u234.O26_on_path_reading_keeps_the_order_after` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 1 | killed |
| `u234.O27_settled_order_keeps_the_order_after` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 1 | killed |
| `u234.O3_person_never_leads` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 10 | killed |
| `u234.O4_settled_order_read_as_moved` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 3 | killed |
| `u234.O5_unsettled_reading_read_as_settled` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 10 | killed |
| `u234.O6_reading_never_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 13 | killed |
| `u234.O8_moved_reading_not_kept_afresh` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 1 | killed |
| `u234.S1_sample_finish_held_to_the_plans_reading` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 764 | 10 | killed |
| `u246.S10_pair_cli_started_empty` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 237 | 1 | killed |
| `u246.S11_pair_cli_served_empty` | `src/cratekit/sync/pair_plan.py` | user | 4 file(s) | 132 | 1 | killed |
| `u246.S12_pair_cli_made_here_empty` | `src/cratekit/sync/pair_check.py` | user | 1 file(s) | 14 | 1 | killed |
| `u246.S13_pair_cli_per_element` | `src/cratekit/sync/pair_check.py` | maintainer | 2 file(s) | 79 | 1 | killed |
| `u198.D10_twins` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D11_two_homes` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D2_favorites_home` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 3 | killed |
| `u198.D3_held` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D4_skip` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 3 | killed |
| `u198.D5_smart` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D6_released` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D7_twice` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D8_top_names` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D9_foreign` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 2 | killed |
| `u202.D1_skip` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D2_two_tops` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D3_longest` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D5_name_taken` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D6_favourites` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u216.M11_paired_raw` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 6 | killed |
| `u216.M12_empty_rest` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 1 | killed |
| `u216.M1_held_record_ignored` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 7 | killed |
| `u216.M2_created_folder_by_time` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 2 | killed |
| `u216.M3_no_moment_reads_new` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 1 | killed |
| `u216.M4_no_time_reads_new` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 3 | killed |
| `u216.M5_naive_time_trusted` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 2 | killed |
| `u216.M6_equal_moment_new` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 1 | killed |
| `u216.M7_time_rule_off` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 3 | killed |
| `u216.M8_moment_latest` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 1 | killed |
| `u216.M9_moment_naive_kept` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 1 | killed |
| `u242.M25_copy_needs_the_prefix` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 76 | 1 | killed |
| `u242.M27_copy_pool_reads_no_taken` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 76 | 1 | killed |
| `r1404.M1_disagreeing_base_ignored` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 3 | killed |
| `r1404.M2_rekordbox_move_ignored` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 3 | killed |
| `r1404.M3_account_move_not_guarded` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 4 | killed |
| `r1404.M4_always_rekordbox` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 4 | killed |
| `r1404.M5_disagreement_read_now` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 2 | killed |
| `r1404.M6_disagreement_read_against_the_account_now` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 1 | killed |
| `r1404.S1_default_leader` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 16 | killed |
| `r1404.S2_stopped_leader_again` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 2 | killed |
| `r1416.M1_rekordbox_does_not_lead` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 2 | killed |
| `r1416.M2_order_kept_ignored` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 2 | killed |
| `r1416.M3_empty_rekordbox_leads` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 1 | killed |
| `r1416.M4_first_sync_unguarded` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 1 | killed |
| `r1416.M5_stopped_write_yields` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 1 | killed |
| `r1416.M6_default_not_kept` | `src/cratekit/sync/pair_merge.py` | maintainer | 5 file(s) | 225 | 2 | killed |
| `r1416.S2_placed_after_neighbour` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 22 | killed |
| `u130-a.A5_new_tracks_appended` | `src/cratekit/sync/pair_merge.py` | user | 2 file(s) | 126 | 8 | killed |
| `u130-a.A6_order_change_read_inverted` | `src/cratekit/sync/pair_merge.py` | user | 2 file(s) | 126 | 18 | killed |
| `u202.M1_since` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 2 | killed |
| `u202.M2_naive` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 1 | killed |
| `u202.M3_tie` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 1 | killed |
| `u202.M4_unknown` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 9 | killed |
| `u202.M5_adder` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 10 | killed |
| `u202.M6_account_readded` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 12 | killed |
| `u202.M7_removal_kept` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 2 | killed |
| `u225.M1_stopped_ignored` | `src/cratekit/sync/pair_merge.py` | user | 4 file(s) | 149 | 5 | killed |
| `u225.M2_rekordbox_since_dropped` | `src/cratekit/sync/pair_merge.py` | user | 4 file(s) | 149 | 2 | killed |
| `u225.M3_rekordbox_over_account` | `src/cratekit/sync/pair_merge.py` | user | 4 file(s) | 149 | 1 | killed |
| `u225.M5_leader_over_account` | `src/cratekit/sync/pair_merge.py` | user | 4 file(s) | 149 | 1 | killed |
| `u234.S2_sample_stopped_leader` | `src/cratekit/sync/pair_merge.py` | user | 6 file(s) | 313 | 3 | killed |
| `u202-composites.R2_confined` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202.R1_recheck_name` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202.W1_landed_then_raised` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1372.K19_passed_by_strict` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1372.K20_passed_by_any_pair` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1372.K21_made_pair_unmapped` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 2 | killed |
| `r1376.F14_finished_filter_gone` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1394.S10_later_unsent_write_hides_the_pending` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 3 | killed |
| `r1394.S1_counts_beyond_the_moves_trusted` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 1 | killed |
| `r1394.S2_missing_counts_read_as_none_sent` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 7 | killed |
| `r1394.S6_counts_not_wired` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 14 | killed |
| `r1394.S8_positions_first_only` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 2 | killed |
| `r1394.S9_moving_step_counts_dropped` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 19 | killed |
| `r1418.F7_composite_ordering_start_unread` | `src/cratekit/sync/pair_stopped.py` | user | 10 file(s) | 394 | 20 | killed |
| `r1434.S2_positions_compare_every_track_listed` | `src/cratekit/sync/pair_stopped.py` | user | 10 file(s) | 394 | 2 | killed |
| `u225.M6_front_keeps_nothing` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `u225.M8_reached_strict_membership` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 3 | killed |
| `u225.M9_finish_ignored` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 3 | killed |
| `u234.O15_reordered_counts_additions` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 1 | killed |
| `r1289.M1_sweep_reads_whole` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 6 | killed |
| `r1289.M2_unread_not_kept` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 5 | killed |
| `r1289.M3_all_unread_branch` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 2 | killed |
| `r1289.M4_unread_why_dropped` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r1289.M5_all_unread_message` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r1289.M6_report_unread_emptied` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r1289.M7_per_playlist_reraise` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r1289.M8_per_playlist_set` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r1289.M9_short_check` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 2 | killed |
| `r358.S10_mark_always_unbound` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 1 | killed |
| `r358.S1_set_is_the_cursor` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 2 | killed |
| `r358.S5_recheck_is_a_second_read` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 3 | killed |
| `r358.S7_lazy_listing` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 1 | killed |
| `r358.S9_mark_always_applied` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 4 | killed |
| `r359.M10_claims_downloaded` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 1 | killed |
| `r359.M1_drop_field` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 3 | killed |
| `r359.M2_token` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 2 | killed |
| `r359.M3_said_silent` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 2 | killed |
| `r359.M4_said_unconditional` | `src/cratekit/sync/playlists.py` | maintainer | 2 file(s) | 146 | 1 | killed |
| `r359.M8_drop_resolved` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 1 | killed |
| `r359.M9_drop_not_acquired` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 2 | killed |
| `r359.S1_record_on_any_state` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 6 | killed |
| `r361-a.A10_enum_value_respelled` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r361-a.A2_case_insensitive` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 3 | killed |
| `r361-a.A3_no_leading_space` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r361-a.A4_substring_not_suffix` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r361-a.D2_drop_the_placeholder` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 2 | killed |
| `r361-a.D3_drop_in_flight` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r382.M11_reconcile_source_jobs` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r382.M12_in_flight_source_jobs` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 2 | killed |
| `r382.M13_marking_source_jobs` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M15_completed_duplicates` | `src/cratekit/sync/playlists.py` | maintainer | 3 file(s) | 215 | 1 | killed |
| `r382.M1_restore_source_filter` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 7 | killed |
| `r382.M2_drop_handler_key` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M3_drop_library` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M4_hearts_recorded` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M5_no_verbatim_for_pass_jobs` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M6_no_parse` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r382.M7_invalid_records_nothing` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 3 | killed |
| `r382.M8_completed_raw` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r382.M9_open_raw` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r835-b.S1_built_year_excluded_from_sweep` | `src/cratekit/sync/playlists.py` | user | 4 file(s) | 271 | 1 | killed |
| `r837-a.A16_sweep_excludes_set` | `src/cratekit/sync/playlists.py` | user | 5 file(s) | 327 | 1 | killed |
| `u113-a.A6_sweep_passes_no_name` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 147 | 1 | killed |
| `u130-c.C9_sweep_takes_paired` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 76 | 2 | killed |
| `u147-c.M18_sweep_exclusion` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 35 | 1 | killed |
| `u242.M1_exclusion_reads_the_ledger` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 230 | 5 | killed |
| `u242.M2_is_taken_drops_the_id` | `src/cratekit/sync/playlists.py` | user | 4 file(s) | 286 | 14 | killed |
| `u242.M3_is_taken_drops_the_prefix` | `src/cratekit/sync/playlists.py` | user | 5 file(s) | 386 | 22 | killed |
| `u242.M4_plan_reads_no_ledger` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 161 | 5 | killed |
| `u242.M5_pending_marks_ignores_the_ledger` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 230 | 1 | killed |
| `u82-a.A5_only_narrows` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 184 | 9 | killed |
| `u82-a.A6_an_empty_only_is_nothing` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 184 | 1 | killed |
| `u82-a.A7_mark_swept_hands_only_through` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 184 | 8 | killed |
| `u221.R21_unknown_name_not_refused` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R22_all_beside_names` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R23_nothing_named` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R25_released_twin_asks_again` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `r1830.M18_plan_counts_nothing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `r1830.M19_digest_omits_the_count` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M22_applied_message_counts_nothing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287-m11.M11_gone_offers_nothing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `u287.M13_folder_separator` | `src/cratekit/sync/removed.py` | maintainer | 1 file(s) | 74 | 1 | killed |
| `u287.M14_twin_is_own_filing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 32 | killed |
| `u287.M17_gone_with_no_record_is_not_whole` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M18_set_aside_rows_count` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M19_old_prefix_is_synced` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M1_partial_read_stops_offers` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 8 | killed |
| `u287.M20_unreadable_record_is_not_whole` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M2_held_by_isrc` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `u287.M3_held_by_recording` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M4_held_before_the_pass` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M5_not_this_pass_file` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M6_on_another_synced` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 8 | killed |
| `u287.M7_in_a_playlist_of_yours` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `u287.M8_empty_read_untrusted` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M9_short_read_untrusted` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M16_stale_digest` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u288.M17_only_the_offered` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 8 | killed |
| `u288.M18_unmeasured_kept` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M19_first_position` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M20_read_back_refusal` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u320-m5.M5_retired_holds` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M10_reopened_keeps_its_retirement` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 2 | killed |
| `u320.M13_withheld_bound_widened` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M18_opened_and_refused_is_unopened` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M4_withheld_hearts_hold_nothing` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 2 | killed |
| `u320.M6_any_failure_is_a_sighting` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 4 | killed |
| `u320.M7_outage_forgets_the_record` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M8_retirement_never_applies` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 5 | killed |
| `u320.M9_relisted_keeps_its_retirement` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 2 | killed |
| `r1830.M20_screen_omits_the_count` | `src/cratekit/sync/removed_cli.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M21_gate_answer` | `src/cratekit/sync/removed_cli.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M22_closed_at_open` | `src/cratekit/sync/removed_cli.py` | user | 1 file(s) | 74 | 1 | killed |
| `u320.M20_retirable_without_this_reads_not_found` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 2 | killed |
| `u320.M21_retire_records_before_the_gate` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M22_retire_ignores_its_answer` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M23_reads_never_recorded` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 11 | killed |
| `u320.M24_record_read_as_empty` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 8 | killed |
| `u320.M25_person_retires_nothing` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 3 | killed |
| `r704-a.R1_increment_ignores_the_flag` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r704-a.R2_rate_limit_not_retryable` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r704-a.R3_remedy_retry_later` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r704-a.R4_detail_unmarked` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r704-a.R5_flag_not_stored` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 2 | killed |
| `r704-a.R6_sentence_reworded` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `u52-item-derivation.A1_acquires_early_return_gone` | `src/cratekit/sync/run.py` | user | 2 file(s) | 211 | 3 | killed |
| `u52-item-derivation.A2_acquires_default_false` | `src/cratekit/sync/run.py` | user | 2 file(s) | 211 | 6 | killed |
| `r259.S1_scope_owned_sample` | `src/cratekit/sync/scope.py` | maintainer | 1 file(s) | 31 | 1 | killed |
| `r263.S2_favorites_reason` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 146 | 1 | killed |
| `u109-b.B1_labels_not_guided` | `src/cratekit/sync/sources.py` | user | 3 file(s) | 228 | 13 | killed |
| `u109-b.B2_command_spelling` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 197 | 9 | killed |
| `u109-b.B3_no_cursor_reworded` | `src/cratekit/sync/sources.py` | user | 1 file(s) | 31 | 3 | killed |
| `u74.A1_no_inbound_key` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 146 | 26 | killed |
| `u74.A2_wrong_inbound_key` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 146 | 14 | killed |
| `u242.M11_strip_skips_the_held_check` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M12_composite` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 11 | killed |
| `u242.M12_strip_skips_the_migration` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 14 | killed |
| `u242.M13_strip_no_collision_with_others` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u242.M14_strip_no_collision_between_strips` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M15_strip_collision_case_exact` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M17_strip_no_recheck` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M18_strip_records_no_old_title` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 4 | killed |
| `u242.M19_migration_copies_an_unmarked_mark` | `src/cratekit/sync/taken_cli.py` | user | 1 file(s) | 46 | 3 | killed |
| `u149.T10_any_year_folder` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T11_excluded_read` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T13_paired_planned_again` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T15_unplanned_membership` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T16_unplanned_playlist_row` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 2 | killed |
| `u149.T20_short_snapshot` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T21_landing_paired_again` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 6 | 1 | killed |
| `u149.T2_two_folders_not_refused` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u149.T3_folder_names_unread` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 2 | killed |
| `u149.T4_removed_folder_live` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u149.T5_held_name_counted_free` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 3 | killed |
| `u149.T6_taken_name_free` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u149.T7_ambiguous_takes_first` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 2 | killed |
| `u149.T8_mirror_link_skipped` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T9_removed_row_linked` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u213.M14_backfill_reason_check` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M15_backfill_left_action` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 4 | killed |
| `u213.M16_backfill_digest_reason` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M17_backfill_unread_tracks` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 2 | killed |
| `u213.M18_backfill_unread_reasons` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M19_matched_ambiguous_first` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M20_backfill_whole` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M2_backfill_refused_reason` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u221.R19_short_listing_records_its_misses` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 78 | 1 | killed |
| `u221.R20_landing_records_no_hold` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 38 | 1 | killed |
| `u242.M8_twins_reads_the_title_alone` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 92 | 1 | killed |
| `u320.M11_apart_halved` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M12_apart_strict` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M14_any_status_is_not_found` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 8 | killed |
| `u320.M15_context_class_counts` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M16_damaged_record_reads_empty` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M17_other_library_read` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M19_none_drops_nothing` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 5 | killed |
| `u320.M3_any_not_found_name_counts` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 2 | killed |
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
| `u242.M22_unmark_releases_nothing` | `src/cratekit/sync/unmark_cli.py` | user | 4 file(s) | 190 | 7 | killed |
| `u242.M26_release_stamps_no_mark` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 78 | 3 | killed |
| `u246.S14_unmark_narrowed_empty` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 47 | 3 | killed |
| `u246.S15_unmark_narrowed_first_only` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `r263.W1_no_unrecorded_state` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 4 | killed |
| `r263.W2_state_word` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 3 | killed |
| `r263.W3_stale_record_as_completion` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 1 | killed |
| `r263.W4_stale_suffix` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 1 | killed |
| `r1446.S1_u234_settled_reorder_never_leads` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 10 | killed |
| `u198.C12_archive_move` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 3 | killed |
| `u208.M10_here_database_only` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 2 | killed |
| `u231.M11_snapshot_from_the_order_sent` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 15 | killed |
| `u231.M13_settle_sleeps_the_whole_window` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 752 | 2 | killed |
| `u231.M17_agreement_gap_ignored` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 752 | 1 | killed |
| `u234.O10_after_not_compared` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 1 | killed |
| `u234.O9_after_without_the_window` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 764 | 1 | killed |

## Row definitions

### `r1289.M10_warning_ready_filter`

_plan_playlists: the unread warning covers a playlist that was not queued, saying its other tracks are

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M10_warning_ready_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`

Old text:

```
        identity: tracks for identity, tracks in sweep.unread.items() if identity in sweep.ready
```

New text:

```
        identity: tracks for identity, tracks in sweep.unread.items() if True
```

### `r1289.M11_warning_absent`

_plan_playlists: no unread warning at all

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M11_warning_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
    if left:
```

New text:

```
    if False:
```

### `r1289.M12_warning_promise`

_plan_playlists: the warning reworded to promise a later sync offers the playlist again, which is false once its job succeeds

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M12_warning_promise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
                    "playlist's intake job succeeds no later sync offers it again, so "
```

New text:

```
                    "playlist's intake job succeeds the next sync takes it up again, so "
```

### `r1289.M13_warning_names`

_plan_playlists: the warning names each playlist but not its unread tracks

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M13_warning_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
                        + ", ".join(f"{ref} ({one['why']})" for ref, one in tracks.items())
```

New text:

```
                        + "some tracks"
```

### `r227.C6_composed_limit_spelled`

sync all judges against a seven spelled in the shell

- File: `src/cratekit/sync/cli.py`
- Source: `r227.json`, row `C6_composed_limit_spelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_composed_gate_judges_against_the_configured_limit`

Old text:

```
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)
```

New text:

```
    age = source.export_age(exported, limit_days=7)
```

### `r359.M5_unwired`

The playlists planner no longer hands its note to the plan

- File: `src/cratekit/sync/cli.py`
- Source: `r359.json`, row `M5_unwired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
    plan = _Plan(spec=spec, describe=describe, detail=describe([]), note=playlists.said)
```

New text:

```
    plan = _Plan(spec=spec, describe=describe, detail=describe([]))
```

### `r359.M6_no_append`

The check computes the note and never appends it to the detail a person reads

- File: `src/cratekit/sync/cli.py`
- Source: `r359.json`, row `M6_no_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
        check["detail"] += f"; {noted}"
```

New text:

```
        pass
```

### `r359.M7_note_before_describe`

The note reads an empty block instead of the source's own, so it says nothing

- File: `src/cratekit/sync/cli.py`
- Source: `r359.json`, row `M7_note_before_describe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
    noted = plan.note(plan.detail or {}) if plan.note is not None else None
```

New text:

```
    noted = plan.note({}) if plan.note is not None else None
```

### `r504-b.B10_check_no_numbers`

The inbound check fails without naming the three numbers

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B10_check_no_numbers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
            f"; the listing came back short, {short.summary()}, which does not say which"
```

New text:

```
            "; the listing came back short, which does not say which"
```

### `r504-b.B7_sync_drops_short`

sync all lists the hearts and keeps no shortfall

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B7_sync_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
    inbound.shortfall = short
```

New text:

```
    inbound.shortfall = None
```

### `r504-b.B8_check_passes`

A short listing leaves the inbound check at its prior status instead of failing it

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B8_check_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        check["status"] = "fail"
        if inbound.not_queued == playlists.Excluded.EMPTY:
```

New text:

```
        if inbound.not_queued == playlists.Excluded.EMPTY:
```

### `r504-b.B9_all_withheld_says_no_hearts`

Every heart withheld still reads as an account that lists no hearts

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B9_all_withheld_says_no_hearts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`

Old text:

```
            check["detail"] = "not queued: the provider served none of the account's hearts"
```

New text:

```
            pass
```

### `r515-operator.S13_sweep_no_warning`

The sync all sweep says nothing of a short playlist

- File: `src/cratekit/sync/cli.py`
- Source: `r515-operator.json`, row `S13_sweep_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
    if sweep.short:
```

New text:

```
    if False:
```

### `r835-c.S2_sync_hands_the_ledger_to_the_sweep_again`

sync.cli._plan_playlists: the sweep is handed no label built playlists, so every year playlist is swept as intake

- File: `src/cratekit/sync/cli.py`
- Source: `r835-c.json`, row `S2_sync_hands_the_ledger_to_the_sweep_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_intake_writers_native.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`
- Collected: 315 against a baseline of 315
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_the_sync_pass_hands_the_sweep_every_year_playlist_a_build_recorded`

Old text:

```
    label_built = ledger.label_playlist_ids(cfg)
```

New text:

```
    label_built = frozenset()
```

### `r837-a.A17_sweep_hand_off`

sync.cli: the sweep is handed no set playlist, so the exclusion has nothing to exclude

- File: `src/cratekit/sync/cli.py`
- Source: `r837-a.json`, row `A17_sweep_hand_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_export_set.py`, `tests/test_intake_writers_native.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_sweep_never_reads_a_set_playlist_as_intake`

Old text:

```
            set_built=set_built,
```

New text:

```
            set_built=frozenset(),
```

### `u109-a.A1_plan_guided`

Plan every enabled source again, guided ones included, so labels is planned as a source with no worker

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A1_plan_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
    plans = [_plan(spec, ctx) for spec in enabled if spec.guided_by is None]
```

New text:

```
    plans = [_plan(spec, ctx) for spec in enabled]
```

### `u109-a.A2_guided_empty`

Collect no guided source, so nothing names crate label sync anywhere

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A2_guided_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
    guided = tuple(spec for spec in enabled if spec.guided_by is not None)
```

New text:

```
    guided = ()
```

### `u109-a.A3_no_check_row`

Drop the guided check row, the one line the human output prints

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A3_no_check_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
    checks.extend(_guided_check(spec) for spec in guided)
```

New text:

```
(empty)
```

### `u109-a.A4_summary_guided`

Drop summary.guided from the pass report

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A4_summary_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_profile_without_the_labels_module_names_no_guided_verb`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`

Old text:

```
        "guided": _guided(guided),
    }
    for plan in plans:
```

New text:

```
    }
    for plan in plans:
```

### `u109-a.A5_gate_guided`

Drop the guided block from what the favourites gate shows

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A5_gate_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`

Old text:

```
            if p.inbound is not None
        },
        "guided": _guided(guided),
    }
```

New text:

```
            if p.inbound is not None
        },
    }
```

### `u109-a.A6_refusal_step_dropped`

A pass that queued nothing refuses without the step naming the guided verb

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A6_refusal_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`

Old text:

```
            steps=(*first.remediation.steps, *(_guided_step(spec) for spec in guided)),
```

New text:

```
            steps=first.remediation.steps,
```

### `u109-a.A7_refusal_step_first`

Prepend the guided step instead of appending it, so it displaces the refusing source's own first step

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A7_refusal_step_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`

Old text:

```
            steps=(*first.remediation.steps, *(_guided_step(spec) for spec in guided)),
```

New text:

```
            steps=(*(_guided_step(spec) for spec in guided), *first.remediation.steps),
```

### `u109-a.A8_row_reworded`

Reword the guided row so it no longer says the source is not swept here

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A8_row_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
            f"not swept by sync all; {spec.command()} takes this source on its "
```

New text:

```
            f"left to another verb; {spec.command()} takes this source on its "
```

### `u147-c.M19_sweep_handoff`

sync.cli: the sync source hands the sweep no mirrored playlist

- File: `src/cratekit/sync/cli.py`
- Source: `u147-c.json`, row `M19_sweep_handoff`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_the_sync_pass_hands_the_sweep_every_mirrored_playlist`

Old text:

```
            mirrored=mirrored,
```

New text:

```
(empty)
```

### `u73-c.C3_next_only_with_intake_jobs`

Name intake missing --run on every pass, including one that queued no intake job

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C3_next_only_with_intake_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_pass_that_finds_only_debris_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_pass_that_queued_no_intake_job_names_no_run_verb`
  - `tests/test_sync_all.py::test_a_pass_whose_only_playlist_left_every_track_unread_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_playlist_with_no_tracks_queues_nothing_and_is_reported`

Old text:

```
    if not filed:
```

New text:

```
    if False:
```

### `u73-c.C4_next_counts_intake_jobs_only`

Count every filed job as an intake job when deciding to name the run verb

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C4_next_counts_intake_jobs_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`

Old text:

```
if job.handler_key in intake_cli.INTAKE_KEYS]
```

New text:

```
if True]
```

### `u73-c.C5_next_check_row`

Keep the command in the summary and drop the check row the human output prints

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C5_next_check_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_default_output_of_a_pass_that_queued_intake_jobs_names_the_run_verb`

Old text:

```
        checks.append(step["check"])
```

New text:

```
        pass
```

### `u74-b.B10_refused_check_status`

Report a hearts refusal as info rather than fail

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B10_refused_check_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`

Old text:

```
    elif inbound.refused is not None:
        check["status"] = "fail"
```

New text:

```
    elif inbound.refused is not None:
        check["status"] = "info"
```

### `u74-b.B11_gate_screen`

The gate screen says the hearts are queued whatever the answer when the listing refused

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B11_gate_screen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_gate_says_when_the_hearts_could_not_be_listed`

Old text:

```
                "queued_whatever_the_answer": p.inbound.queue is not None,
```

New text:

```
                "queued_whatever_the_answer": True,
```

### `u74-b.B12_next_step_outbound_only`

Name no intake missing --run step when only the hearts filed an intake job

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B12_next_step_outbound_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`

Old text:

```
    filed = [job for p in plans for job in _filed(p) if job.handler_key in intake_cli.INTAKE_KEYS]
```

New text:

```
    filed = [job for p in plans for job in p.filed if job.handler_key in intake_cli.INTAKE_KEYS]
```

### `u74-b.B1_source_id_dropped`

Queue the hearts job with no source_id, so the next pass cannot see it is open

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B1_source_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`

Old text:

```
                run_id=run_id,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
            )
```

New text:

```
                run_id=run_id,
                source_id=None,
            )
```

### `u74-b.B2_compose_skips_inbound`

The composer never queues the read half

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B2_compose_skips_inbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if p.inbound is not None and p.inbound.queue is not None:
            ready.append
```

New text:

```
        if False:
            ready.append
```

### `u74-b.B3_queue_refusal_raised`

Raise a queue time refusal instead of recording it against its half

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B3_queue_refusal_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_refusal_part_way_through_the_playlists_keeps_the_filed_ones_named`
  - `tests/test_sync_all.py::test_a_source_refused_at_queue_time_leaves_the_queued_ones_named`

Old text:

```
                    half.refused, half.not_queued = exc.cause, exc.cause.reason
```

New text:

```
                    raise
```

### `u74-b.B4_filed_outbound_only`

Count only the write half's jobs as filed, so a pass that queued only the hearts refuses or reads as a no-op

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B4_filed_outbound_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
    return [*plan.filed, *(plan.inbound.filed if plan.inbound is not None else ())]
```

New text:

```
    return [*plan.filed]
```

### `u74-b.B5_inbound_refusal_not_counted`

Leave the hearts refusal out of the refusal list, so a declined pass it alone stopped reads as a no-op

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B5_inbound_refusal_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op`

Old text:

```
        for cause in (p.refused, p.inbound.refused if p.inbound else None)
```

New text:

```
        for cause in (p.refused, None)
```

### `u74-b.B6_inbound_warning`

Emit no warning for a hearts refusal

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B6_inbound_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`

Old text:

```
        if plan.inbound is not None and plan.inbound.refused is not None:
            warnings.append(
```

New text:

```
        if False:
            warnings.append(
```

### `u74-b.B7_block_dropped`

Leave the favourites.inbound block out of the summary

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B7_block_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 13 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_half_refused_is_still_a_refusal`

Old text:

```
            plan.detail = {**(plan.detail or {}), "inbound": plan.inbound.block()}
```

New text:

```
            pass
```

### `u74-b.B8_check_dropped`

Leave the sync.favorites.inbound check out, which is all the default output prints

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B8_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
            checks.append(_inbound_check(plan, plan.inbound))
```

New text:

```
            pass
```

### `u74-b.B9_check_wording`

Say the hearts were not listed for a half that was listed and refused at the queue

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B9_check_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`

Old text:

```
            if inbound.hearts is None
```

New text:

```
            if True
```

### `u74.A10_export_refusal_raised`

Raise the write half's export refusal to _plan again, which drops the read half with it

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A10_export_refusal_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_half_refused_is_still_a_refusal`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        plan.refused, plan.not_queued = exc.cause, exc.cause.reason
        return plan
```

New text:

```
        raise
```

### `u74.A11_queue_not_bound`

Never bind the read half's queue callable, so a listed half queues nothing

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A11_queue_not_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 17 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_the_gate_refusal_queues_no_hearts_listing_either`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    inbound.queue = queue
    return inbound
```

New text:

```
    return inbound
```

### `u74.A12_run_id_dropped`

Queue the hearts job without the shared run id, so intake missing --run cannot find it

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A12_run_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`

Old text:

```
                tracks=tracks,
                run_id=run_id,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
```

New text:

```
                tracks=tracks,
                run_id=None,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
```

### `u74.A3_handler_filter`

Drop the handler key filter, so an open outbound favourites job holds the hearts listing

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A3_handler_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`

Old text:

```
        if job.handler_key == handler_key
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
```

New text:

```
        if True
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
```

### `u74.A4_source_filter`

Drop the source_id filter, so an open playlists job holds the hearts listing

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A4_source_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`

Old text:

```
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
        and job.library_id == cfg.library.volume_id
```

New text:

```
        and True
        and job.library_id == cfg.library.volume_id
```

### `u74.A5_library_filter`

Drop the library filter, so another library's open hearts job holds this one

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A5_library_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`

Old text:

```
        and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        and True
    )
```

### `u74.A6_open_filter`

Count a finished hearts job as open, so a failed job holds every later pass

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A6_open_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`

Old text:

```
                if job.is_open()
            )
```

New text:

```
                if True
            )
```

### `u74.A7_in_flight_guard`

Ignore an open hearts job, so every pass queues a second listing beside it

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A7_in_flight_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`

Old text:

```
        if in_flight:
            inbound.not_queued
```

New text:

```
        if False:
            inbound.not_queued
```

### `u74.A8_empty_guard`

Queue an empty hearts listing as a job, rather than reporting no hearts

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A8_empty_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_source_refused_at_queue_time_leaves_the_queued_ones_named`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`

Old text:

```
    if not tracks:
        inbound.not_queued = playlists.Excluded.EMPTY
```

New text:

```
    if False:
        inbound.not_queued = playlists.Excluded.EMPTY
```

### `u74.A9_listing_refusal_raised`

Raise a hearts listing refusal instead of recording it, so it ends the favourites source

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A9_listing_refusal_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op`
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_pass_over_a_recent_export_carries_no_age_warning`
  - `tests/test_sync_all.py::test_a_pass_that_queued_over_an_old_export_warns_and_still_queues`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_half_refused_is_still_a_refusal`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_composed_gate_judges_against_the_configured_limit`
  - `tests/test_sync_all.py::test_the_composed_gate_names_the_exports_date_beside_what_would_queue`
  - `tests/test_sync_all.py::test_the_composed_gate_shows_the_tracks_the_sweeps_digest_covers`
  - `tests/test_sync_all.py::test_the_composed_pass_carries_the_favourites_verb_standing_warning`
  - `tests/test_sync_all.py::test_the_favourites_job_carries_a_gate_run_its_own_verb_owns`
  - `tests/test_sync_all.py::test_the_gate_asks_over_the_digest_sync_favorites_itself_offers`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        inbound.refused, inbound.not_queued = exc.cause, exc.cause.reason
        return inbound
```

New text:

```
        raise
```

### `r1056.S1_no_landing_step_names_intake_missing`

_native_proof: drop the named source from the no landing step, so a label batch is told intake missing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r1056.json`, row `S1_no_landing_step_names_intake_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_sync_mark.py`
- Collected: 102 against a baseline of 102
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[abandoned]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[another-pass]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[never-committed]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[no-landing]`

Old text:

```
            f"land the pass with crate intake land --pass and {named}, then run {verb} "
```

New text:

```
            f"land the pass with crate intake land --pass and {SYNC_PASS_NAMED}, then run {verb} "
```

### `r1056.S2_unreachable_step_names_sync`

_native_proof: name sync mark in the unreachable library step whatever verb asked

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r1056.json`, row `S2_unreachable_step_names_sync`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_sync_mark.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_an_unreachable_library_names_label_mark_as_the_verb_to_run_again`

Old text:

```
            f"mount the library volume, then run {verb} again",
```

New text:

```
            "mount the library volume, then run crate sync mark again",
```

### `r361-a.A7_mark_verb_forgets_debris`

The mark verb's plan no longer decides label-debris, so the playlist falls through to the reports

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A7_mark_verb_forgets_debris`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
        elif playlists.is_library_debris(entry.name):
            entry.reason = LABEL_DEBRIS
        elif job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
        elif job.state is not jobs.JobState.SUCCEEDED:
```

### `r361-a.A8_mark_verb_respells_the_word`

The mark verb spells its own word for the reason instead of reading the enum

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A8_mark_verb_respells_the_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
LABEL_DEBRIS = str(playlists.Excluded.LABEL_DEBRIS)
```

New text:

```
LABEL_DEBRIS = "label-library"
```

### `r361-a.A9_reword_the_why`

The why sentence is reworded, never appended to, since the suite asserts with in

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A9_reword_the_why`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
        "its name is the source system's label run debris, which a sync never "
        "offers and never renames"
```

New text:

```
        "its name is a throwaway the other system left, which a sync never "
        "offers and never renames"
```

### `r777-confirm.N4_plain_name`

Confirm: _native_proof takes a pass name no landing could have been given, after the test that pins its message

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777-confirm.json`, row `N4_plain_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_pass_name_no_landing_could_have_been_given_is_refused`

Old text:

```
    if not landing.plain_name(name):
```

New text:

```
    if False:
```

### `r777-confirm.N7_digest_marks`

Confirm, the first table's old text was moved by the fix round: the native digest no longer covers the planned marks

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777-confirm.json`, row `N7_digest_marks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_answer_is_stale_once_another_playlist_becomes_whole`

Old text:

```
            "landings": list(proof.landings),
            "marks": planned,
```

New text:

```
            "landings": list(proof.landings),
```

### `r777.N10_screen_says_pass`

The gate screen on a native pass shows an intake file line instead of the pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N10_screen_says_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_whose_tracks_the_library_holds_is_marked_after_the_answer`

Old text:

```
        if isinstance(proof, marks.NativeLanding)
        else {"intake file": str(proof)}
```

New text:

```
        if False
        else {"intake file": str(proof)}
```

### `r777.N11_exclusive`

--xml and --pass are no longer one or the other

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N11_exclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_file_and_the_pass_are_one_or_the_other`

Old text:

```
    proof = parser.add_mutually_exclusive_group(required=True)
```

New text:

```
    proof = parser
```

### `r777.N12_no_landing_required`

_native_proof makes a proof when no closed landing of the pass committed

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N12_no_landing_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[abandoned]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[another-pass]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[never-committed]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[no-landing]`

Old text:

```
    if not landings:
        raise _blocked(
```

New text:

```
    if False:
        raise _blocked(
```

### `r777.N18_unreachable_called_bridge`

An unreachable library falls through to the bridge refusal

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N18_unreachable_called_bridge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_unreachable_library_is_named_and_never_called_the_bridge`

Old text:

```
    if medium.declared is None:
        # AN UNREACHABLE ROOT
```

New text:

```
    if False:
        # AN UNREACHABLE ROOT
```

### `r777.N19_digest_landings`

The native digest no longer covers the landings that prove the pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N19_digest_landings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_second_landing_of_the_pass_since_the_plan_makes_the_answer_stale`

Old text:

```
            "landings": list(proof.landings),

```

New text:

```
(empty)
```

### `r777.N5_bridge_accepted`

_native_proof accepts --pass on an intake tree still on the xml bridge

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N5_bridge_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_pass_named_on_a_tree_still_on_the_bridge_is_refused_naming_the_file`
  - `tests/test_sync_mark.py::test_a_tree_put_back_on_the_bridge_after_the_plan_renames_nothing`

Old text:

```
    if not medium.native:
        raise _blocked(
```

New text:

```
    if False:
        raise _blocked(
```

### `r777.N6_no_reread`

apply_pass no longer reads the proof again before the first rename

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N6_no_reread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_landing_recorded_between_the_plan_and_the_apply_renames_nothing`
  - `tests/test_sync_mark.py::test_a_tree_put_back_on_the_bridge_after_the_plan_renames_nothing`

Old text:

```
        if _native_proof(cfg, planned.name) != planned.native:
```

New text:

```
        if False:
```

### `r777.N9_proof_is_file`

PassPlan.proof hands the engine the absent file on a native pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N9_proof_is_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_takes_playlist_as_the_file_does`
  - `tests/test_sync_mark.py::test_a_native_pass_whose_tracks_the_library_holds_is_marked_after_the_answer`
  - `tests/test_sync_mark.py::test_a_native_pass_with_one_track_not_held_leaves_that_playlist_alone`
  - `tests/test_sync_mark.py::test_organize_marks_a_native_pass_through_its_gate`

Old text:

```
        return self.native if self.native is not None else self.xml
```

New text:

```
        return self.xml
```

### `u174.M10_dedupe`

plan_pass: keep a playlist named twice twice in the narrowing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M10_dedupe`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_playlist_repeated_takes_each_named_and_no_playlist_is_the_whole_pass`

Old text:

```
    named = tuple(dict.fromkeys(str(one) for one in playlists_named))
```

New text:

```
    named = tuple(str(one) for one in playlists_named)
```

### `u174.M11_stranger_before_no_jobs`

plan_pass: refuse a stranger only after the no jobs return, so a file of no pass given --playlist asks a gate

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M11_stranger_before_no_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate`

Old text:

```
    _refuse_strangers(named, found, name)
    if not found:
```

New text:

```
    if found:
        _refuse_strangers(named, found, name)
    if not found:
```

### `u174.M1_stranger_refusal`

plan_pass: drop the refusal of a named playlist that is not the pass's, so it plans nothing and says nothing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M1_stranger_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_playlist_of_no_pass_of_this_name_is_refused_before_the_account_is_listed`
  - `tests/test_sync_mark.py::test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate`

Old text:

```
    strangers = [identity for identity in named if identity not in held]
    if strangers:
```

New text:

```
    strangers = [identity for identity in named if identity not in held]
    if False:
```

### `u174.M2_narrowing`

plan_pass: drop the narrowing of the decided playlists, so --playlist plans the whole pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M2_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_already_marked_is_a_skip_and_not_a_refusal`
  - `tests/test_sync_mark.py::test_a_native_pass_takes_playlist_as_the_file_does`
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`
  - `tests/test_sync_mark.py::test_the_library_is_walked_only_for_the_named_playlist`

Old text:

```
        decided = [entry for entry in decided if entry.identity in named]
```

New text:

```
        decided = list(decided)
```

### `u174.M3_unfinished_refusal`

plan_pass: drop the refusal of a named playlist the pass did not complete, so it is shown as a skip

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M3_unfinished_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_job_failed_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_reports_cannot_be_read_is_refused_by_name`

Old text:

```
    unfinished = [entry for entry in decided if entry.reason in UNFINISHED]
    if unfinished:
```

New text:

```
    unfinished = [entry for entry in decided if entry.reason in UNFINISHED]
    if False:
```

### `u174.M4_unfinished_rows_outstanding`

UNFINISHED: leave out rows-outstanding, so a playlist with a missing track is a skip when named

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M4_unfinished_rows_outstanding`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`

Old text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

New text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE})
```

### `u174.M5_unfinished_job`

UNFINISHED: leave out job-unfinished, so a playlist whose job failed is a skip when named

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M5_unfinished_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_job_failed_is_refused_by_name`

Old text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

New text:

```
UNFINISHED = frozenset({REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

### `u174.M6_unfinished_reports`

UNFINISHED: leave out reports-unreadable, so a playlist whose reports cannot be read is a skip when named

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M6_unfinished_reports`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_reports_cannot_be_read_is_refused_by_name`

Old text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

New text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, ROWS_OUTSTANDING})
```

### `u174.M7_digest_names_the_narrowing`

_payload: leave the narrowing out of the digest, so an answer to one playlist's screen carries out the whole pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M7_digest_names_the_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_answer_to_the_narrowed_plan_does_not_carry_out_the_whole_pass`
  - `tests/test_sync_mark.py::test_playlist_repeated_takes_each_named_and_no_playlist_is_the_whole_pass`

Old text:

```
        identity["only"] = sorted(named)
```

New text:

```
        pass
```

### `u174.M8_screen_names_the_narrowing`

_shown: drop the gate screen's line naming the playlists the plan was narrowed to

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M8_screen_names_the_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`

Old text:

```
        shown[ONLY_SAID] = list(named)
```

New text:

```
        pass
```

### `u174.M9_verb_passes_the_flag`

sync_mark: hand plan_pass no playlists, so --playlist is parsed and ignored

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M9_verb_passes_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_playlist_of_no_pass_of_this_name_is_refused_before_the_account_is_listed`
  - `tests/test_sync_mark.py::test_an_answer_to_the_narrowed_plan_does_not_carry_out_the_whole_pass`
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`
  - `tests/test_sync_mark.py::test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate`

Old text:

```
        playlists_named=list(getattr(ctx.args, "playlist", None) or ()),
```

New text:

```
        playlists_named=(),
```

### `u174.P1_bridge_plans_no_native_pass`

native_passes: read native records on a tree on the bridge too, so every old record is planned as a refusal

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `P1_bridge_plans_no_native_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_tree_on_the_bridge_plans_no_native_record`

Old text:

```
    if not medium.native:
        return ()
    return native.landed_passes(cfg)
```

New text:

```
    return native.landed_passes(cfg)
```

### `u174.P2_unreachable_is_refused`

native_passes: read an unreachable root as no pass, so organize asks over a clean plan

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `P2_unreachable_is_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_unreachable_root_is_a_refused_step_and_never_no_pass`

Old text:

```
    if medium.declared is None:
        raise _blocked(
```

New text:

```
    if medium.declared is None:
        return ()
        raise _blocked(
```

### `u242.M21_mark_cli_already_marked_by_title`

sync mark: decide already marked by the title alone, so a taken playlist is planned again

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u242.json`, row `M21_mark_cli_already_marked_by_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_u242_taken.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_partial_failure_names_what_was_marked`

Old text:

```
        elif playlists.is_taken(identity, entry.name, sweep.taken):
```

New text:

```
        elif playlists.is_swept_name(entry.name):
```

### `u82-b.B5_not_listed_is_skipped`

_decided: drop the not listed reason, so the plan declares a rename of a playlist the account no longer has

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-b.json`, row `B5_not_listed_is_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_playlist_the_account_no_longer_lists_is_said_and_not_planned`

Old text:

```
        if not entry.name:
            entry.reason = NOT_LISTED
```

New text:

```
        if False:
            entry.reason = NOT_LISTED
```

### `u82-b.B6_a_failed_job_is_skipped`

_decided: drop the unfinished job reason, so a playlist whose tracks were never all resolved is read from whatever reports it has

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-b.json`, row `B6_a_failed_job_is_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_job_failed_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_playlist_whose_job_failed_is_said_and_not_planned`

Old text:

```
        elif job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
        elif False:
```

### `u82-b.B7_unread_reports_hold_the_playlist`

_decided: stop catching the report reader's refusal, so one damaged report refuses the whole verb and the whole playlists beside it are never marked

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-b.json`, row `B7_unread_reports_hold_the_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_reports_cannot_be_read_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_playlist_whose_reports_cannot_be_read_is_left_alone`

Old text:

```
        except CratekitError as exc:
            # UNREAD IS NOT NOTHING OWED.
```

New text:

```
        except ZeroDivisionError as exc:
            # UNREAD IS NOT NOTHING OWED.
```

### `u82-b.B8_an_offered_track_is_owed`

_NOT_FOUND: count only missing reports, which is what the manifest carried, so a playlist holding a track the pass offered for review is marked over it

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-b.json`, row `B8_an_offered_track_is_owed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_track_the_pass_offered_for_review_holds_its_playlist_back`

Old text:

```
_NOT_FOUND = frozenset({"missing", "offered"})
```

New text:

```
_NOT_FOUND = frozenset({"missing"})
```

### `u82-c.C1_a_tombstoned_track_is_settled`

_settle: drop the suppressed branch, so a track deleted on purpose since the pass holds its playlist back for ever

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-c.json`, row `C1_a_tombstoned_track_is_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_track_deleted_on_purpose_since_the_pass_is_not_owed`

Old text:

```
            elif found.state is match.MatchState.SUPPRESSED:
```

New text:

```
            elif False:
```

### `u82-c.C2_one_outstanding_track_holds_the_playlist`

_settle: never set the outstanding reason, so a playlist with a track still not in the library is planned for the prefix

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-c.json`, row `C2_one_outstanding_track_holds_the_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_native_answer_is_stale_once_another_playlist_becomes_whole`
  - `tests/test_sync_mark.py::test_a_native_pass_with_one_track_not_held_leaves_that_playlist_alone`
  - `tests/test_sync_mark.py::test_a_playlist_with_one_row_not_landed_is_not_marked`
  - `tests/test_sync_mark.py::test_a_track_deleted_on_purpose_since_the_pass_is_not_owed`
  - `tests/test_sync_mark.py::test_a_track_the_pass_offered_for_review_holds_its_playlist_back`
  - `tests/test_sync_mark.py::test_a_track_two_playlists_share_holds_both_back_until_it_lands`
  - `tests/test_sync_mark.py::test_an_answer_to_one_plan_does_not_carry_out_another`
  - `tests/test_sync_mark.py::test_the_pass_is_decided_without_its_manifest`

Old text:

```
        if entry.outstanding:
            entry.reason = ROWS_OUTSTANDING
```

New text:

```
        if False:
            entry.reason = ROWS_OUTSTANDING
```

### `u82-c.C3_landed_is_told_from_owned`

_settle: call every matched track landed, so the screen credits this landing with files it did not bring

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-c.json`, row `C3_landed_is_told_from_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_whose_tracks_the_library_holds_is_marked_after_the_answer`
  - `tests/test_sync_mark.py::test_a_row_the_library_holds_and_the_file_does_not_name_is_owned`

Old text:

```
                entry.settled[LANDED if held & named else OWNED] += 1
```

New text:

```
                entry.settled[LANDED] += 1
```

### `u82-c.C9_the_accounts_reason_is_kept`

_failed_part_way: treat a refusal the account raised as a defect, so a provider timeout is reported as internal-error

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-c.json`, row `C9_the_accounts_reason_is_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_refusal_the_record_raised_keeps_its_reason_and_names_what_was_marked`

Old text:

```
    if isinstance(exc, CratekitError):
        cause = exc.cause
```

New text:

```
    if False:
        cause = exc.cause
```

### `u82-d.B2_paths_compared_resolved_again`

The zero of u82-b re-measured after test_a_library_reached_through_a_link_still_reads_its_files_as_landed. _comparable: compare the spelled path and not the resolved one

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-d.json`, row `B2_paths_compared_resolved_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_library_reached_through_a_link_still_reads_its_files_as_landed`

Old text:

```
    return locations.norm_for_compare(str(Path(path).resolve()))
```

New text:

```
    return locations.norm_for_compare(str(path))
```

### `r838-c.R1_library_bound`

mark_record._recognize: accept a record written for another library

- File: `src/cratekit/sync/mark_record.py`
- Source: `r838-c.json`, row `R1_library_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_an_unreadable_record_refuses_rather_than_reading_as_empty[{"version": 1, "library_id": "another-library", "marks": []}]`

Old text:

```
        if library_id != self.cfg.library.volume_id:
```

New text:

```
        if False:
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

### `u242.M6_record_v1_reads_a_taken_key`

mark record: drop the version 1 branch, so a record written before U242 is refused for having no taken list

- File: `src/cratekit/sync/mark_record.py`
- Source: `u242.json`, row `M6_record_v1_reads_a_taken_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_unmark.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_version_one_record_reads_as_one_with_nothing_taken`

Old text:

```
        if version == 1:
            # BEFORE U242 NOTHING WAS TAKEN HERE. A version 1 record that
            # somehow carries the key is still read as it was written.
            return []
```

New text:

```
        if False:
            return []
```

### `u242.M9_take_overwrites_a_held_entry`

take: replace an entry still held, so a second taker's stamp replaces the first and the migration is not idempotent

- File: `src/cratekit/sync/mark_record.py`
- Source: `u242.json`, row `M9_take_overwrites_a_held_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_mark.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_take_is_idempotent_and_a_released_entry_is_taken_afresh`

Old text:

```
                elif not taken[at].held:
```

New text:

```
                elif True:
```

### `r777.N1_empty_proof`

marks.require_proof accepts a NativeLanding naming no tree, no pass or no landing

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N1_empty_proof`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_mark.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_engine_refuses_a_mark_with_neither_proof`

Old text:

```
        if not local_output.tree_id or not local_output.pass_name or not local_output.landings:
```

New text:

```
        if False:
```

### `r777.N2_neither_proof`

marks.require_proof hands anything that is not a NativeLanding to require_output, so None is no longer refused by name

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N2_neither_proof`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_mark.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_engine_refuses_a_mark_with_neither_proof`

Old text:

```
    if not isinstance(local_output, Path):
```

New text:

```
    if False:
```

### `r777.N3_engine_unchecked`

apply_deferred no longer checks its proof before renaming

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N3_engine_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_mark.py`
- Collected: 100 against a baseline of 100
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_external_marks_wait_for_local_output_and_recheck`
  - `tests/test_sync_mark.py::test_the_engine_refuses_a_mark_with_neither_proof`
  - `tests/test_sync_mark.py::test_the_file_check_makes_one_stat_and_refuses_whatever_it_raises`

Old text:

```
    require_proof(local_output)
    applied: list[str] = []
```

New text:

```
    applied: list[str] = []
```

### `u82-a.A1_stat_oserror_is_the_refusal`

require_output: stop turning an OSError out of the one stat into sync-marks-blocked, so a file gone at that moment is a bare FileNotFoundError again, which is R-398

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A1_stat_oserror_is_the_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_that_did_not_land_is_offered_again_by_the_next_pass`
  - `tests/test_sync_all.py::test_a_mark_without_a_real_importable_file_renames_nothing`
  - `tests/test_sync_mark.py::test_a_missing_intake_file_refuses_the_verb_before_anything_is_listed`
  - `tests/test_sync_mark.py::test_the_file_check_makes_one_stat_and_refuses_whatever_it_raises`

Old text:

```
    except OSError as exc:
        raise _blocked(local_output, exc.strerror or type(exc).__name__) from exc
```

New text:

```
    except ZeroDivisionError as exc:
        raise _blocked(local_output, exc.strerror or type(exc).__name__) from exc
```

### `u82-a.A2_a_folder_is_not_a_file`

require_output: drop the regular file check, so a folder named like the intake file counts as the importable file

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A2_a_folder_is_not_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_folder_and_an_empty_file_are_not_an_importable_file`

Old text:

```
    if not stat.S_ISREG(found.st_mode):
```

New text:

```
    if False:
```

### `u82-a.A3_an_empty_file_is_not_proof`

require_output: drop the empty file check, so a zero byte file lets the renames through

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A3_an_empty_file_is_not_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_without_a_real_importable_file_renames_nothing`
  - `tests/test_sync_mark.py::test_a_folder_and_an_empty_file_are_not_an_importable_file`

Old text:

```
    if found.st_size == 0:
```

New text:

```
    if False:
```

### `r1360.F1_walk_uncounted`

unpaged_calls: the walk past a first page is not counted

- File: `src/cratekit/sync/pair_calls.py`
- Source: `r1360.json`, row `F1_walk_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 827 against a baseline of 827
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before3-order3]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[101-2]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[199-2]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[200-3]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[250-3]`

Old text:

```
    return UNPAGED_READ + math.ceil(beyond / (PLAYLIST_PAGE - 1))
```

New text:

```
    return UNPAGED_READ
```

### `r1360.F2_step_a_page`

unpaged_calls: each later request is counted as a whole new page

- File: `src/cratekit/sync/pair_calls.py`
- Source: `r1360.json`, row `F2_step_a_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 827 against a baseline of 827
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[200-3]`

Old text:

```
math.ceil(beyond / (PLAYLIST_PAGE - 1))
```

New text:

```
math.ceil(beyond / PLAYLIST_PAGE)
```

### `r1360.F3_judged_without_walk`

judged_calls: a judged reading counts one unpaged request whatever its length

- File: `src/cratekit/sync/pair_calls.py`
- Source: `r1360.json`, row `F3_judged_without_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 827 against a baseline of 827
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before3-order3]`

Old text:

```
    return listing_calls(count) + unpaged_calls(count)
```

New text:

```
    return listing_calls(count) + UNPAGED_READ
```

### `u210.R23_margin`

pair_calls.named: carry no margin over the estimate

- File: `src/cratekit/sync/pair_calls.py`
- Source: `u210.json`, row `R23_margin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_the_named_calls_carry_a_margin_round_up_and_never_fall_below_the_line`

Old text:

```
MARGIN = 1.25
```

New text:

```
MARGIN = 1.0
```

### `u220.C1_moves_head_rule`

pair_calls._moves: count the moves by the old head rule

- File: `src/cratekit/sync/pair_calls.py`
- Source: `u220.json`, row `C1_moves_head_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_tie.py`
- Collected: 306 against a baseline of 306
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before0-order0]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before1-order1]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before2-order2]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before3-order3]`

Old text:

```
    for one in reversed(before):
```

New text:

```
    for one in before:
```

### `u226.M24_estimate_no_unpaged`

pair_calls: a judged reading forecast at a listing's cost

- File: `src/cratekit/sync/pair_calls.py`
- Source: `u226.json`, row `M24_estimate_no_unpaged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair.py`
- Collected: 137 against a baseline of 137
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_add_is_counted_against_what_the_playlist_holds_after_its_removals[removes1-adds1]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[40-5-0]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before0-order0]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before1-order1]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before2-order2]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before3-order3]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[0-1]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[1-1]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[100-1]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[101-2]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[199-2]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[200-3]`
  - ... and 1 more, see the JSON sidecar

Old text:

```
UNPAGED_READ = 1

```

New text:

```
UNPAGED_READ = 0

```

### `u231.M24_forecast_without_the_settle_reading`

forecast: an order's settle reading is not counted

- File: `src/cratekit/sync/pair_calls.py`
- Source: `u231.json`, row `M24_forecast_without_the_settle_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_resume.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before1-order1]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before2-order2]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before3-order3]`

Old text:

```
            calls += moves * (1 + REPARSE) + judged_calls(len(now))
```

New text:

```
            calls += moves * (1 + REPARSE)
```

### `u246.S7_pair_calls_before_empty`

account_write: an empty set of what the playlist held, so no removal is counted as taking anything

- File: `src/cratekit/sync/pair_calls.py`
- Source: `u246.json`, row `S7_pair_calls_before_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_resume.py`
- Collected: 46 against a baseline of 46
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_add_is_counted_against_what_the_playlist_holds_after_its_removals[removes1-adds1]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[40-5-0]`

Old text:

```
    held_before = set(now)
```

New text:

```
    held_before = set()
```

### `u246.S8_pair_calls_after_empty`

account_write: an empty set of what the removals left, so an add the playlist already holds is counted as sent

- File: `src/cratekit/sync/pair_calls.py`
- Source: `u246.json`, row `S8_pair_calls_after_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_resume.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_an_add_is_counted_against_what_the_playlist_holds_after_its_removals[removes0-adds0]`

Old text:

```
    held_after = set(now)
```

New text:

```
    held_after = set()
```

### `u246.S9_pair_calls_after_stale`

account_write: the after set reuses the before set, so a track the removals took off reads as still held and its add is not counted

- File: `src/cratekit/sync/pair_calls.py`
- Source: `u246.json`, row `S9_pair_calls_after_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_resume.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_an_add_is_counted_against_what_the_playlist_holds_after_its_removals[removes1-adds1]`

Old text:

```
    held_after = set(now)
```

New text:

```
    held_after = held_before
```

### `r1264-composites.M7_account_add_filter`

plan_pair: offer an unread track to the account as an addition, which already lists it; reached on a first sync, where no base strips the unread key

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264-composites.json`, row `M7_account_add_filter`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists`

Old text:

```
        if remote_of(key) and key not in unseen and key not in unread_keys
```

New text:

```
        if remote_of(key) and key not in unseen
```

### `r1264.M12_record_holds_back`

_record: hold the snapshot back while a track is unread, the round one defect

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1264.json`, row `M12_record_holds_back`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_hold.py`
- Collected: 49 against a baseline of 49
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_in_rekordbox_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_on_the_account_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`
  - `tests/test_sync_pair_unread.py::test_unread_tracks_trading_places_after_the_plan_is_not_stale`

Old text:

```
    whole = rekordbox_after is not None and account_after is not None and not one.withheld
```

New text:

```
    whole = (
        rekordbox_after is not None
        and account_after is not None
        and not one.withheld
        and not one.unread
    )
```

### `r1264.M14_check_unread_moved`

check: never read the unread tracks as moved, so a new unread track after the plan is written over

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1264.json`, row `M14_check_unread_moved`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_hold.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_track_turning_unreadable_between_the_plan_and_the_write_refuses_stale`

Old text:

```
            unread_moved = set(listing.unread) != {named.remote_id for named in one.unread}
```

New text:

```
            unread_moved = False
```

### `r1264.M15_check_unread_as_tuple`

check: compare the unread tracks by place, so tracks trading places refuses stale

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1264.json`, row `M15_check_unread_as_tuple`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_unread_tracks_trading_places_after_the_plan_is_not_stale`

Old text:

```
            unread_moved = set(listing.unread) != {named.remote_id for named in one.unread}
```

New text:

```
            unread_moved = tuple(listing.unread) != tuple(named.remote_id for named in one.unread)
```

### `r1264.M18_identity_unread`

PairPlan.identity: leave the unread ids out of the digest

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1264.json`, row `M18_identity_unread`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_hold.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_plan_whose_unread_tracks_differ_digests_differently`

Old text:

```
                {"unread": [named.remote_id for named in self.unread]} if self.unread else {}
```

New text:

```
                {} if self.unread else {}
```

### `r1264.M19_warning`

_warnings: say nothing of the unread tracks

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1264.json`, row `M19_warning`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`

Old text:

```
    unread = [(one, named) for one in planned.pairs for named in one.unread]
    if unread:
```

New text:

```
    unread = [(one, named) for one in planned.pairs for named in one.unread]
    if False:
```

### `r1264.M1_unread_dropped`

plan_pair: read no unread tracks off the listing, so an untitled track the base holds reads as taken off the account and its linked row is removed from rekordbox

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M1_unread_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_hold.py`
- Collected: 95 against a baseline of 95
- Kills: 17 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists`
  - `tests/test_sync_pair_unread.py::test_a_plan_whose_unread_tracks_differ_digests_differently`
  - `tests/test_sync_pair_unread.py::test_a_rekordbox_reorder_while_a_track_is_unread_reaches_the_account_and_stands`
  - `tests/test_sync_pair_unread.py::test_a_rekordbox_row_carrying_an_unread_tracks_isrc_is_not_added_to_the_account`
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing0-t4]`
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing1-t24]`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_track_naming_no_artist_is_unread_the_same_way`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_in_rekordbox_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_on_the_account_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            listing.unread,
            listing.order,
```

New text:

```
            {},
            listing.order,
```

### `r1264.M20_item`

_items: list no unread track among the gate's items

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1264.json`, row `M20_item`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`
- Collected: 20 against a baseline of 20
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_track_naming_no_artist_is_unread_the_same_way`
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`

Old text:

```
        items.append(row("account", "unread", named))
```

New text:

```
        pass
```

### `r1264.M2_unread_isrc_on_account`

plan_pair: do not join an unread track's ISRC to the account's codes, so a rekordbox row carrying it asks the provider, which may name another release

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M2_unread_isrc_on_account`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_twins.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_rekordbox_row_carrying_an_unread_tracks_isrc_is_not_added_to_the_account`

Old text:

```
        code = match.isrc_token(one.isrc)
        if code:
```

New text:

```
        code = match.isrc_token(one.isrc)
        if False:
```

### `r1264.M3_account_keys_listing_order`

plan_pair: read the account's keys in the readable tracks' order, so a row's key sits at its readable release's place

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M3_account_keys_listing_order`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing0-t4]`
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing1-t24]`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`

Old text:

```
            for remote_id in (listed_order or account_now)
            if alias(remote_id) in readable_keys
```

New text:

```
            for remote_id in account_now
            if alias(remote_id) in readable_keys
```

### `r1264.M4_account_keys_filter`

plan_pair: keep an unread track's own key among the account's keys, so it reads as held on the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M4_account_keys_filter`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair.py`
- Collected: 96 against a baseline of 96
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_plan_whose_unread_tracks_differ_digests_differently`
  - `tests/test_sync_pair_unread.py::test_a_rekordbox_reorder_while_a_track_is_unread_reaches_the_account_and_stands`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_track_naming_no_artist_is_unread_the_same_way`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_in_rekordbox_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_on_the_account_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_a_track_turning_unreadable_between_the_plan_and_the_write_refuses_stale`
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`
  - `tests/test_sync_pair_unread.py::test_unread_tracks_trading_places_after_the_plan_is_not_stale`
  - `tests/test_sync_pair_unread.py::test_while_a_track_is_unread_a_rekordbox_removal_still_lands_on_the_account`

Old text:

```
            for remote_id in (listed_order or account_now)
            if alias(remote_id) in readable_keys
```

New text:

```
            for remote_id in (listed_order or account_now)
            if True
```

### `r1264.M5_unread_keys_empty`

plan_pair: no unread keys, so nothing is stripped from the base or kept from the account's additions

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M5_unread_keys_empty`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_twins.py`
- Collected: 66 against a baseline of 66
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`

Old text:

```
    unread_keys = {alias(remote_id) for remote_id in unread} - readable_keys
```

New text:

```
    unread_keys: set[str] = set()
```

### `r1264.M6_base_strip`

plan_pair: leave unread keys in the base account, so a row linked to an unread track reads as removed on the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M6_base_strip`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_twins.py`
- Collected: 66 against a baseline of 66
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`

Old text:

```
        if unread_keys:
            unseen |=
```

New text:

```
        if False:
            unseen |=
```

### `r1264.M8_order_after_listing`

plan_pair: compute the account order over the readable tracks only

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M8_order_after_listing`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing0-t4]`
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing1-t24]`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`

Old text:

```
        after = pair_merge.appended(listed_order or account_now, account_removes, account_adds)
```

New text:

```
        after = pair_merge.appended(account_now, account_removes, account_adds)
```

### `r1264.M9_firsts_keep_unread`

plan_pair: count unread keys among the account's order keys, so the order differs from the merge's whenever one is unread

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M9_firsts_keep_unread`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair.py`
- Collected: 96 against a baseline of 96
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`

Old text:

```
            alias(one) for one in after if alias(one) not in unread_keys
```

New text:

```
            alias(one) for one in after
```

### `r1372.K17_no_let_go_at_snapshot`

_record: a snapshot recorded whole lets go of no carried record of its pair

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1372.json`, row `K17_no_let_go_at_snapshot`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`

Old text:

```
    if whole:
        _let_go_passed(one.target.account_id, recorded.synced)
```

New text:

```
    if False:
        _let_go_passed(one.target.account_id, recorded.synced)
```

### `r1372.K1_no_carry`

write: the pair's steps are not carried past the run as its order begins

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1372.json`, row `K1_no_carry`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_run_that_finished_the_pair_without_moving_its_snapshot_keeps_nothing_of_its_own`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
        # whatever its age until the pair's snapshot passes it.
        steps.carry()
```

New text:

```
        # whatever its age until the pair's snapshot passes it.
        pass
```

### `r1372.K22_mark_guard_gone`

stopped_write: a stop that began before the pair was marked is read as the pair's

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K22_mark_guard_gone`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_first_sync_reads_the_stop_on_its_account_playlist_whatever_the_mark`
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`

Old text:

```
        if marked is not None and began < marked:
            return None
```

New text:

```
        if False:
            return None
```

### `r1372.K23_mark_guard_inclusive`

stopped_write: a stop that began at the very moment the pair was marked is refused

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K23_mark_guard_inclusive`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`

Old text:

```
        if marked is not None and began < marked:
```

New text:

```
        if marked is not None and began <= marked:
```

### `r1372.K4_carry_unwritten_not_refused`

PairSteps.carry: a carry that cannot be written is swallowed and the moves go on

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1372.json`, row `K4_carry_unwritten_not_refused`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_that_cannot_be_kept_past_its_run_moves_nothing`

Old text:

```
            held_plan.carry(self.steps, self.key)
        except OSError as exc:
            raise steps_unwritten(self.steps.run_id, exc) from None
```

New text:

```
            held_plan.carry(self.steps, self.key)
        except OSError as exc:
            exc = exc
```

### `r1372.K6_reader_ignores_carried`

reader: the carried records are not read, only the kept steps

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K6_reader_ignores_carried`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
        records = [*records, *(one for one in kept if (one.run_id, one.digest) not in current)]
```

New text:

```
        records = [*records]
```

### `r1372.K7_copy_never_gives_way`

reader: a carried copy is read beside its own run's steps kept under the same plan

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K7_copy_never_gives_way`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`

Old text:

```
        current = {(one.run_id, one.digest) for one in records}
```

New text:

```
        current = set()
```

### `r1372.K8_copy_gives_way_to_any_plan`

reader: a carried copy gives way to its run's steps under any plan, so a replanned run's fresh steps hide it

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K8_copy_gives_way_to_any_plan`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`

Old text:

```
        current = {(one.run_id, one.digest) for one in records}
        records = [*records, *(one for one in kept if (one.run_id, one.digest) not in current)]
```

New text:

```
        current = {one.run_id for one in records}
        records = [*records, *(one for one in kept if one.run_id not in current)]
```

### `r1372.K9_carried_unread_unsaid`

reader: a carried record that cannot be read is not named

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K9_carried_unread_unsaid`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`

Old text:

```
        problems = [*problems, *unread]
```

New text:

```
        problems = [*problems]
```

### `r1376.F11_leader_lost`

plan_pair: the stop is read as led by the account whatever side led it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F11_leader_lost`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_names_the_pair_as_finishing_the_stopped_run`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_says_the_account_was_read_off_the_moves_path`

Old text:

```
            leader=stopped_write.leader,
```

New text:

```
            leader=pair_merge.ACCOUNT,
```

### `r1376.F13_snapshot_guard_inclusive`

stopped_write (sample, U225): a stop that began after the snapshot by a hair is read as passed

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1376.json`, row `F13_snapshot_guard_inclusive`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 34 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_fresh_sync_orders_the_account_to_rekordbox_and_plans_no_rekordbox_order`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_reading_that_never_settled_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_later_reading_still_on_the_moves_path_is_finished_never_read_as_a_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_later_run_that_failed_before_its_order_began_does_not_hide_the_stopped_write`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_before_the_stop_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_for_another_run_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_on_the_path_is_never_the_baseline_so_the_partial_state_after_it_finishes`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            if synced is None or not began > synced:
```

New text:

```
            if synced is None or True:
```

### `r1376.F1_first_stop_none`

first_stop: a first sync is never handed the stop on its account playlist

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1376.json`, row `F1_first_stop_none`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_first_sync_reads_the_stop_on_its_account_playlist_whatever_the_mark`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`

Old text:

```
        _began, write = self.stopped[0].get(account_id, (None, None))
        return write
```

New text:

```
        _began, write = self.stopped[0].get(account_id, (None, None))
        return None
```

### `r1376.F3_call_site_gone`

plan_pair: a first sync never asks for the stop on its account playlist

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F3_call_site_gone`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`

Old text:

```
    if stopped_write is None and first_sync:
        stopped_write = reader.first_stop(target.account_id)
```

New text:

```
    if False:
        stopped_write = reader.first_stop(target.account_id)
```

### `r1376.F4_first_sync_unrecorded_only`

plan_pair: a pair marked with no snapshot is not read as a first sync, so its earlier stop is kept out by the mark

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F4_first_sync_unrecorded_only`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble`

Old text:

```
    first_sync = held is None or held.first
```

New text:

```
    first_sync = held is None
```

### `r1376.F5_first_sync_marked_only`

plan_pair: a pair with no record at all, a hand pairing before its mark, is not read as a first sync

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F5_first_sync_marked_only`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 318 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_rekordbox_running_refusal_still_ends_the_run_as_failed`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - `tests/test_sync_pair.py::test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale`
  - `tests/test_sync_pair.py::test_a_rekordbox_row_with_no_isrc_column_is_matched_on_its_files_isrc`
  - `tests/test_sync_pair.py::test_a_row_with_no_isrc_anywhere_is_named_and_the_provider_is_not_asked`
  - `tests/test_sync_pair.py::test_a_second_rekordbox_playlist_for_a_paired_account_playlist_is_refused`
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - ... and 303 more, see the JSON sidecar

Old text:

```
    first_sync = held is None or held.first
```

New text:

```
    first_sync = held is not None and held.first
```

### `r1376.F6_every_sync_first`

plan_pair: every sync reads the stop whatever its snapshot, so a stop the snapshot passed is finished again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F6_every_sync_first`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_a_fresh_sync_finished_is_left_behind_by_the_snapshot`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
    if stopped_write is None and first_sync:
```

New text:

```
    if stopped_write is None:
```

### `r1383-digest.M8_digest_drops_hold`

PairPlan.identity: leave the held tracks out of the digest, so a plan whose hold moved is not stale at its gate

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1383-digest.json`, row `M8_digest_drops_hold`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`
- Collected: 162 against a baseline of 162
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_the_pairs_digest_moves_with_the_landing_hold_and_only_when_any`

Old text:

```
                {"landing_unread": sorted(named.remote_id for named in self.landing_unread)}
                if self.landing_unread
                else {}
```

New text:

```
                {}
```

### `r1383-digest.M9_digest_always_keyed`

PairPlan.identity: put the key in every digest, so a plan reading every record no longer digests as it did (round one's zero)

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1383-digest.json`, row `M9_digest_always_keyed`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`
- Collected: 162 against a baseline of 162
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_the_pairs_digest_moves_with_the_landing_hold_and_only_when_any`

Old text:

```
                if self.landing_unread
                else {}
```

New text:

```
                if True
                else {}
```

### `r1383.M10_warning_never_said`

plan: carry no unread entry to the warning, so the hold is silent

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M10_warning_never_said`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_held_while_a_record_is_unread`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
                _landings_said(cfg, reader.landings[1]) if "landings" in reader.__dict__ else ()
```

New text:

```
                ()
```

### `r1383.M12_unlisted_said_as_records`

_landings_said: never say the log is unlisted, so a refused listing is named as a record to repair

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M12_unlisted_said_as_records`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`

Old text:

```
    if session.log_unlisted(unread, cfg):
        return (
```

New text:

```
    if False:
        return (
```

### `r1383.M13_records_unnamed`

_landings_said: name no record, so the warning cannot say which record to look at

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M13_records_unnamed`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
        f"the record {Path(path).name} in {Path(path).parent}, which reads under the "
```

New text:

```
        f"a record in {Path(path).parent}, which reads under the "
```

### `r1383.M14_hold_before_awaiting`

plan_pair: decide the landing hold before awaiting, so a track an earlier sync queued is shown held with the wrong remedy

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M14_hold_before_awaiting`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record`

Old text:

```
        if remote_id in queued_before:
            awaiting.append(names[key])
```

New text:

```
        if match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]:
            landing_unread.append(names[key])
        elif remote_id in queued_before:
            awaiting.append(names[key])
```

### `r1383.M15_hold_before_twin`

plan_pair: decide the landing hold before a twin's hold, so a twin's held track loses its sync release remedy

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M15_hold_before_twin`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record`

Old text:

```
        elif held_for_choice(held, remote_id, dates):
```

New text:

```
        elif match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]:
            landing_unread.append(names[key])
        elif held_for_choice(held, remote_id, dates):
```

### `r1383.M16_zero_said_as_count`

_warnings: say a scan nothing waited on as zero tracks held, round one's finding 7

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M16_zero_said_as_count`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`

Old text:

```
                        if waiting
                        # THE SCAN
```

New text:

```
                        if True
                        # THE SCAN
```

### `r1383.M17_total_uncounted`

payload: count no held track in the totals

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M17_total_uncounted`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
            "landing_unread": count("library", LANDING_UNREAD_ACTION),
```

New text:

```
            "landing_unread": 0,
```

### `r1383.M18_sampled_own_landed_step`

sampled U128 guard: _owned asks no landing made for this account playlist, so its own landed track is found only by the widened step

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M18_sampled_own_landed_step`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`

Old text:

```
        landed = _mirror_isrcs(reader, account_id)
```

New text:

```
        landed = {}
```

### `r1383.M19_sampled_mirrors_empty`

sampled: _Reader.mirrors answers no INBOX playlist, so every landed track is queued again, the half R-1383 keeps beside it

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1383.json`, row `M19_sampled_mirrors_empty`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 11 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_is_added_and_never_queued`
  - `tests/test_sync_pair.py::test_each_landed_file_is_read_once_per_plan`
  - `tests/test_sync_pair.py::test_one_row_landed_in_two_inbox_playlists_is_one_row`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[torn]`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[unknown-state]`
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`
  - `tests/test_sync_pair.py::test_two_landed_rows_carrying_the_code_are_ambiguous_and_queue_nothing`
  - `tests/test_sync_pair_hold.py::test_a_track_found_by_another_landing_costs_the_plan_no_call[by another account playlist's landing]`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`

Old text:

```
        return self.landings[0]
```

New text:

```
        return {}
```

### `r1383.M1_scan_drops_unread`

landed_inbox_playlists: answer no unread entry, the defect the card closes, so an unreadable landing record is read as no landing and its track queued

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1383.json`, row `M1_scan_drops_unread`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_hold.py`
- Collected: 183 against a baseline of 183
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_held_while_a_record_is_unread`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
    return {account_id: frozenset(ids) for account_id, ids in found.items()}, tuple(unreadable)
```

New text:

```
    return {account_id: frozenset(ids) for account_id, ids in found.items()}, ()
```

### `r1383.M2_hold_branch_removed`

plan_pair: never hold, so a track an unreadable landing record may have brought in is queued with the warning beside it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M2_hold_branch_removed`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_held_while_a_record_is_unread`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]
        ):
```

New text:

```
            False
        ):
```

### `r1383.M3_hold_without_isrc`

plan_pair: hold a track carrying no ISRC as well, so a track no landing could name waits on the record forever

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M3_hold_without_isrc`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_carrying_no_isrc_is_still_queued_beside_an_unreadable_record`

Old text:

```
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]
        ):
```

New text:

```
            reader.landings[1]
        ):
```

### `r1383.M4_hold_while_readable`

plan_pair: hold whenever the track carries an ISRC, so every new track waits though every record reads

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M4_hold_while_readable`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 27 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_still_queued`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[cancelled]`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[failed]`
  - `tests/test_sync_pair.py::test_a_track_this_pair_alone_lists_is_queued_once_beside_anothers_job`
  - `tests/test_sync_pair.py::test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row`
  - `tests/test_sync_pair.py::test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale`
  - `tests/test_sync_pair.py::test_another_pairs_job_that_no_longer_reads_stops_no_plan`
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - ... and 12 more, see the JSON sidecar

Old text:

```
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]
        ):
```

New text:

```
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc"))
        ):
```

### `r1383.M5_hold_dropped_from_plan`

plan_pair: build the pair with no held tracks, so the gate names none and the total counts none

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M5_hold_dropped_from_plan`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
        landing_unread=tuple(landing_unread),
```

New text:

```
        landing_unread=(),
```

### `r1383.M6_gate_item_dropped`

_items: name no held track on the gate, so a person approving sees nothing of what waits

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M6_gate_item_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
    for named in one.landing_unread:
        items.append(row("library", LANDING_UNREAD_ACTION, named))
```

New text:

```
    for named in ():
        items.append(row("library", LANDING_UNREAD_ACTION, named))
```

### `r1383.M7_gate_item_side`

_items: name a held track on the rekordbox side rather than the library's

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M7_gate_item_side`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
        items.append(row("library", LANDING_UNREAD_ACTION, named))
```

New text:

```
        items.append(row("rekordbox", LANDING_UNREAD_ACTION, named))
```

### `r1385.M10_reason_dropped`

plan_pair: name a track another pair holds awaiting with no reason, so the gate never says which pair holds it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M10_reason_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
            awaiting.append(_with_reason(names[key], why))
```

New text:

```
            awaiting.append(names[key])
```

### `r1385.M11_name_fallback`

_Reader.held_by_jobs: no fallback to the account playlist for a job naming no playlist, so its reason names nothing

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1385.json`, row `M11_name_fallback`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`

Old text:

```
            name = str(payload.get(intake_cli.PLAYLIST_NAME) or "") or source
```

New text:

```
            name = str(payload.get(intake_cli.PLAYLIST_NAME) or "")
```

### `r1385.M12_check_reads_no_job`

check: read no job at apply time, so a job another sync queued since the plan is queued again beside it

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1385.json`, row `M12_check_reads_no_job`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale`
  - `tests/test_sync_pair_hold.py::test_tracks_another_sync_queued_before_the_write_refuse_stale_not_twice`

Old text:

```
            for job in pair_jobs(cfg, store)
            for item in (job.payload or {}).get(intake_cli.TRACKS) or {}
        }
```

New text:

```
            for job in ()
            for item in (job.payload or {}).get(intake_cli.TRACKS) or {}
        }
```

### `r1385.M13_warning_unsplit`

_warnings: say every awaited track was queued, so a skip that queued nothing is reported as queued (round one's finding)

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1385.json`, row `M13_warning_unsplit`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`

Old text:

```
        before = [row for row in awaiting if not row.reason.startswith(QUEUED_HERE)]
```

New text:

```
        before = awaiting
```

### `r1385.M14_warning_here_dropped`

_warnings: never say a track another pair of this sync is to queue

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1385.json`, row `M14_warning_here_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
        if here:
            parts.append(
```

New text:

```
        if False:
            parts.append(
```

### `r1385.M15_failed_jobs_hold`

pair_jobs: read a failed or cancelled job as holding its tracks, so a track whose download failed is never queued again (sampled guard)

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1385.json`, row `M15_failed_jobs_hold`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[cancelled]`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[failed]`

Old text:

```
        and job.state not in (jobs.JobState.FAILED, jobs.JobState.CANCELLED)
    )
```

New text:

```
    )
```

### `r1385.M1_no_job_holds_anything`

_Reader.held_by_jobs: read no job's tracks, so every track a job holds is queued again, a pair's own included

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1385.json`, row `M1_no_job_holds_anything`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 13 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`
  - `tests/test_sync_pair_back.py::test_a_missing_track_is_queued_once_and_then_awaits`
  - `tests/test_sync_pair_discover.py::test_an_unowned_track_added_on_the_account_is_queued_once_and_then_awaiting`
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`

Old text:

```
        return {remote_id: tuple(held) for remote_id, held in found.items()}
```

New text:

```
        return {}
```

### `r1385.M2_other_jobs_not_asked`

_queued_elsewhere: ask no other pair's job, so a track another pair's pending job holds is queued again (the card's second scenario)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M2_other_jobs_not_asked`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
    for source, name in reader.held_by_jobs.get(remote_id, ()):
```

New text:

```
    for source, name in ():
```

### `r1385.M4_plan_not_asked`

_queued_elsewhere: ask nothing of this plan, so two pairs listing one lacking track queue it twice (the card's first scenario)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M4_plan_not_asked`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_the_runs_own_job_for_an_earlier_pair_stops_no_later_command`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
    asked = reader.asked.get(remote_id)
```

New text:

```
    asked = None
```

### `r1385.M6_ask_not_registered`

plan_pair: register nothing this pair asks to acquire, so a later pair of the plan queues it again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M6_ask_not_registered`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_the_runs_own_job_for_an_earlier_pair_stops_no_later_command`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
        reader.asked.setdefault(remote_id, (target.key, name))
```

New text:

```
        pass
```

### `r1385.M8_own_reads_every_job`

_queued: read every pair's job as this pair's own, so another pair's job is named with no pair and asked before a twin's hold

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M8_own_reads_every_job`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`

Old text:

```
        if any(source == account_id for source, _name in held)
```

New text:

```
        if held
```

### `r1385.M9_own_reads_no_job`

_queued: read none of this pair's own jobs, so its own queued track is named for no pair or held on a twin

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M9_own_reads_no_job`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`
  - `tests/test_sync_pair_back.py::test_a_missing_track_is_queued_once_and_then_awaits`
  - `tests/test_sync_pair_discover.py::test_an_unowned_track_added_on_the_account_is_queued_once_and_then_awaiting`
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`

Old text:

```
        if any(source == account_id for source, _name in held)
```

New text:

```
        if False
```

### `r1394.P1_counts_never_written`

pair write: the recorder writes the moving step with no progress, sent and landed always 0

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P1_counts_never_written`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`

Old text:

```
                        at=at, start=start, end=end, sent=sent, landed=landed
```

New text:

```
                        at=at, start=start, end=end, sent=0, landed=0
```

### `r1394.P2_counts_not_carried`

pair write: the recorder's counts are marked in the run's steps but not carried past the run

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P2_counts_not_carried`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`

Old text:

```
                steps.carry()

            return sending
```

New text:

```
                pass

            return sending
```

### `r1394.P3_begun_answers_no_recorder`

pair write: begun answers no recorder, so the adapter tells the record nothing between moves

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P3_begun_answers_no_recorder`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`

Old text:

```
            return sending
```

New text:

```
            return None
```

### `r1394.P4_finish_from_landed`

pending order: an agreed reading at the moves the provider accepted is finished from even with a move whose landing is not known after it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1394.json`, row `P4_finish_from_landed`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`

Old text:

```
        if not at or max(at) >= write.sent:
```

New text:

```
        if not at or max(at) >= write.landed:
```

### `r1394.P5_finish_from_any_path_reading`

pending order: any agreed reading on the moves' path is finished from, R-1394's own defect

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1394.json`, row `P5_finish_from_any_path_reading`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`

Old text:

```
        if not at or max(at) >= write.sent:
```

New text:

```
        if not at or max(at) >= 0:
```

### `r1394.P6_off_path_held`

pending order: an agreed reading off the moves' path, the person's change, is held instead of merged as theirs

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1394.json`, row `P6_off_path_held`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
        if not at or max(at) >= write.sent:
```

New text:

```
        if at and max(at) >= write.sent:
```

### `r1394.P7_unknown_named_as_landed`

held message: a reading at a move whose landing is not known is named as before the moves accepted

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1394.json`, row `P7_unknown_named_as_landed`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`

Old text:

```
    elif at < write.landed:
```

New text:

```
    elif at <= write.landed:
```

### `r1394.P8_every_move_named_as_a_stop`

held message: every move accepted is named as a write that stopped part way

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1394.json`, row `P8_every_move_named_as_a_stop`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`

Old text:

```
    elif write is None or write.moved:
```

New text:

```
    elif write is None:
```

### `r1394.P9_finish_not_held_to_the_agreed_reading`

pair write: a write that finishes a stopped order lets the adapter plan its moves from any reading holding the same tracks, round one's row 1

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P9_finish_not_held_to_the_agreed_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_that_move_leaves_it_is_finished`

Old text:

```
                or (one.finishing_order and not (one.account_removes or one.account_adds))
```

New text:

```
                or False
```

### `r1404.S3_scope_every_pair`

sample, U231: every pair keeps the account's order, so a root pair's account is written rekordbox's order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1404.json`, row `S3_scope_every_pair`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 13 (killed)
- Killed:
  - `tests/test_sync_pair_root_order.py::test_a_hand_pairs_first_sync_outside_gig_ready_keeps_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_rekordbox_reorder_outside_gig_ready_stays_sync_after_sync`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_rekordbox_holds_is_appended_to_the_account_and_nothing_else_moves`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_tidal_holds_lands_after_its_neighbour_in_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_track_placed_in_rekordbox_outside_gig_ready_keeps_its_place`
  - `tests/test_sync_pair_root_order.py::test_after_the_first_sync_a_tidal_reorder_still_leads_and_a_rekordbox_reorder_stands`
  - `tests/test_sync_pair_root_order.py::test_an_account_addition_outside_gig_ready_is_placed_in_rekordbox_s_order`
  - `tests/test_sync_pair_settle.py::test_a_pair_outside_gig_ready_gets_no_order_write_and_its_membership_still_syncs`
  - `tests/test_sync_pair_settle.py::test_a_rekordbox_side_to_be_made_is_under_gig_ready_only_inside_the_folder`
  - `tests/test_sync_pair_settle.py::test_a_root_playlist_named_gig_ready_is_not_under_gig_ready`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_of_an_account_playlist_with_no_stop_is_planned_as_before`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_left_off_its_path_outside_gig_ready_leaves_rekordbox_untouched`

Old text:

```
    if cfg.outbound.pair_order_every_pair:
        return True
```

New text:

```
    if True:
        return True
```

### `r1411.W1_finish_passes_no_agreed`

the pair write passes no agreed reading at a finish, the measured cost R-1411 names

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1411.json`, row `W1_finish_passes_no_agreed`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            if one.finishing_order and one.account_before
```

New text:

```
            if False
```

### `r1411.W2_finish_passes_agreed_only_with_nothing_else`

the pair write passes agreed only at a finish that adds and removes nothing, as before this card

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1411.json`, row `W2_finish_passes_agreed_only_with_nothing_else`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
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
```

New text:

```
            if one.finishing_order
            and one.account_before
            and not (one.account_removes or one.account_adds)
```

### `r1411.W3_agreed_is_the_asked_order`

the pair write passes the order it asks as the agreed reading rather than the plan's reading

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1411.json`, row `W3_agreed_is_the_asked_order`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            {"agreed": tuple(one.account_before)}
```

New text:

```
            {"agreed": tuple(one.account_order)}
```

### `r1411.W4_agreed_is_the_checks_listing`

round one's BLOCKING shape: the pair write passes the check's listing as the agreed reading when there is one

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1411.json`, row `W4_agreed_is_the_checks_listing`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`

Old text:

```
            {"agreed": tuple(one.account_before)}
```

New text:

```
            {"agreed": tuple(account_listed or one.account_before)}
```

### `r1416.M10_cli_account_write_kept`

pair_cli: the account write reads the order as always kept, so a root pair's first sync writes rekordbox's order onto the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M10_cli_account_write_kept`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_root_order.py::test_a_hand_pairs_first_sync_outside_gig_ready_keeps_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_rekordbox_reorder_outside_gig_ready_stays_sync_after_sync`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_rekordbox_holds_is_appended_to_the_account_and_nothing_else_moves`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_tidal_holds_lands_after_its_neighbour_in_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_track_placed_in_rekordbox_outside_gig_ready_keeps_its_place`
  - `tests/test_sync_pair_root_order.py::test_after_the_first_sync_a_tidal_reorder_still_leads_and_a_rekordbox_reorder_stands`
  - `tests/test_sync_pair_root_order.py::test_an_account_addition_outside_gig_ready_is_placed_in_rekordbox_s_order`
  - `tests/test_sync_pair_settle.py::test_a_pair_outside_gig_ready_gets_no_order_write_and_its_membership_still_syncs`
  - `tests/test_sync_pair_settle.py::test_a_root_playlist_named_gig_ready_is_not_under_gig_ready`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_of_an_account_playlist_with_no_stop_is_planned_as_before`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_left_off_its_path_outside_gig_ready_leaves_rekordbox_untouched`

Old text:

```
        order_unkept = wanted_keys != firsts and not order_kept
```

New text:

```
        order_unkept = False
```

### `r1416.M7_cli_tells_kept`

pair_cli: the merge is always told the order is kept, so a root pair's first sync puts rekordbox in the account's order again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M7_cli_tells_kept`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_root_order.py::test_a_hand_pairs_first_sync_outside_gig_ready_keeps_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_rekordbox_holds_is_appended_to_the_account_and_nothing_else_moves`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_tidal_holds_lands_after_its_neighbour_in_rekordbox_s_order`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_of_an_account_playlist_with_no_stop_is_planned_as_before`

Old text:

```
        order_kept=order_kept,
```

New text:

```
        order_kept=True,
```

### `r1416.M8_cli_tells_not_kept`

pair_cli: the merge is always told the order is not kept, so a GIG READY pair's first sync keeps rekordbox's order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M8_cli_tells_not_kept`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_root_order.py::test_a_hand_pairs_first_sync_with_every_pairs_order_kept_follows_tidal`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_of_an_account_playlist_with_no_stop_under_gig_ready_follows_the_account`

Old text:

```
        order_kept=order_kept,
```

New text:

```
        order_kept=False,
```

### `r1416.M9_cli_scope_key_only`

pair_cli: the flag read before the merge is the config key alone, so a GIG READY pair reads as not kept

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M9_cli_scope_key_only`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 119 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_the_account_still_stands_in_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[refused]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_the_run_puts_the_refused_pair_in_order_and_moves_nothing_else`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`
  - `tests/test_sync_pair_order.py::test_a_first_order_is_asked_with_nothing_to_agree_with_but_what_the_adapter_wrote`
  - ... and 104 more, see the JSON sidecar

Old text:

```
    order_kept = _keeps_order(cfg, rekordbox, home)
```

New text:

```
    order_kept = cfg.outbound.pair_order_every_pair
```

### `r1416.S3_scope_under_the_folder`

sample, U231: a playlist under GIG READY is no longer read as kept, so its first sync is led by rekordbox

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `S3_scope_under_the_folder`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 119 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_the_account_still_stands_in_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[refused]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_the_run_puts_the_refused_pair_in_order_and_moves_nothing_else`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`
  - `tests/test_sync_pair_order.py::test_a_first_order_is_asked_with_nothing_to_agree_with_but_what_the_adapter_wrote`
  - ... and 104 more, see the JSON sidecar

Old text:

```
        return bool(rekordbox.ancestors) and rekordbox.top[1] == ORDER_FOLDER
```

New text:

```
        return False
```

### `r1418.F1_agreed_is_the_readable_tracks`

the brief's row: a finish is held to the tracks the provider could read, so a lag differing only by where an unread track stands is planned from

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F1_agreed_is_the_readable_tracks`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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

### `r1418.F2_agreed_passed_for_an_empty_reading`

the clause for an empty plan reading dropped, so a finish whose plan read no account passes an empty agreed order to an adapter that may not take it

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F2_agreed_passed_for_an_empty_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_plan_read_no_account_passes_no_agreed_reading`

Old text:

```
            if one.finishing_order and one.account_before
            else {}
```

New text:

```
            if one.finishing_order
            else {}
```

### `r1418.F3_agreed_passed_only_for_an_empty_reading`

the clause inverted, so a finish whose plan read the account passes no agreed order and is held to membership alone

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F3_agreed_passed_only_for_an_empty_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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

### `r1418.F5_plans_reading_without_unread_ids`

existing guard, R-1264: the plan's reading of an account it orders is the readable tracks alone, unread ids left out of it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1418.json`, row `F5_plans_reading_without_unread_ids`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `r1420-b.B2_beyond_tail_unread_pinned`

sample: the part written check reads the kept tracks' order but not that this write's additions stand after them, measured again once a test pins it

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420-b.json`, row `B2_beyond_tail_unread_pinned`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`

Old text:

```
        if kept != [track for track in one.account_now if track in held] or (
            list(now) != kept + tail
        ):
```

New text:

```
        if kept != [track for track in one.account_now if track in held] or (
            list(now) != list(now)
        ):
```

### `r1420.B1_beyond_order_unread`

sample: the part written check never reads the order, whatever ordering says

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `B1_beyond_order_unread`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
    if not parts and not ordering:
```

New text:

```
    if not parts and ordering is None:
```

### `r1420.B3_beyond_removals_asked`

sample: the kept order is compared to the whole plan's reading, so a track this write took off reads as a reorder

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `B3_beyond_removals_asked`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_rekordbox_playlist_changed_after_this_run_wrote_it_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_inside_the_account_write_is_finished_without_writing_rekordbox_twice`
  - `tests/test_sync_pair_resume_one.py::test_a_track_withheld_on_the_part_written_playlist_refuses_stale`

Old text:

```
        if kept != [track for track in one.account_now if track in held] or (
```

New text:

```
        if kept != [track for track in one.account_now] or (
```

### `r1420.C1_continued_ignored`

a continue of an order parked or stopped with the whole write before any move passes the adapter no listing to agree with

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `C1_continued_ignored`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`

Old text:

```
                or (continued and not one.finishing_order)
```

New text:

```
                or (continued and one.finishing_order and False)
```

### `r1420.C3_continued_read_after_the_mark`

whether an earlier command began the order is read as always yes, so a first order is asked to agree with the check's listing

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `C3_continued_read_after_the_mark`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_first_order_is_asked_with_nothing_to_agree_with_but_what_the_adapter_wrote`

Old text:

```
        continued = steps.has(STEP_ORDERING)
```

New text:

```
        continued = steps.has(STEP_ORDERING) or True
```

### `r1420.C4_carried_record_unread`

a continue whose run's steps cannot be read does not read the carried record, so its order of a pair that moved nothing is asked with no listing to agree with

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `C4_carried_record_unread`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`

Old text:

```
        continued = steps.has(STEP_ORDERING) or steps.carried(STEP_ORDERING) is not None
```

New text:

```
        continued = steps.has(STEP_ORDERING) or steps.carried(STEP_ORDERING) is None and False
```

### `r1420.E2_finish_agreed_dropped`

sample: a finish of a stopped order is not held to the plan's reading at the adapter

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `E2_finish_agreed_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
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
            if False and one.finishing_order and one.account_before
            else {}
```

### `r1420.N1_fix_reverted`

the check leaves the order unread once ordering is marked, as before R-1420, so a person's reorder after an order that moved nothing is written over

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N1_fix_reverted`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return steps.has(STEP_ORDERING)
```

### `r1420.N2_moves_begun_ignored`

a pair whose moves began has its order read, so a continue of a stop part way through the moves refuses the moves' own order as moved

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N2_moves_begun_ignored`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_whose_moves_all_landed_finishes_on_the_continue`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return steps.has(STEP_ORDERING) and one.finishing_order
```

### `r1420.N3_finish_read_too`

a finish of a stopped order has its order read by the check, so a continue of a refused finish whose check lists the lag is held as moved rather than refused at the adapter

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N3_finish_read_too`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return steps.has(STEP_ORDERING) and steps.has(STEP_MOVING)
```

### `r1420.N5_order_always_read`

every part written pair has its order read, the moves' own included

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N5_order_always_read`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_whose_moves_all_landed_finishes_on_the_continue`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return False and steps.has(STEP_ORDERING)
```

### `r1420.N6_call_site_never_reads_order`

the check passes ordering as true for every part written pair, so no order is read once an account write began

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N6_call_site_never_reads_order`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
                why = _beyond(one, now, ordering=_ordered_by_this_run(one, of(one)))
```

New text:

```
                why = _beyond(one, now, ordering=True)
```

### `r1432-composites.C4_finish_reads_the_listing_unfinished`

what E4 holds: at a finish the readable tracks are read as the account lists them, with the stopped write's remaining moves not applied, so its half done order is read as the account's

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432-composites.json`, row `C4_finish_reads_the_listing_unfinished`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `r1432.P10_warning_says_it_stays`

the sync-pair-unread warning at a finish says only that each stays where it is

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1432.json`, row `P10_warning_says_it_stays`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
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

### `r1432.P3_target_id_no_longer_listed_put_back`

an unread id the target names and the account no longer lists is put back into the asked order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P3_target_id_no_longer_listed_put_back`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `r1432.P7_none_held_goes_last`

an unread id with no held track before it goes to the end rather than the front

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P7_none_held_goes_last`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered4-listed4-target4-expected4]`
  - `tests/test_sync_pair_settle.py::test_with_no_stopped_write_an_unread_track_follows_the_one_listed_before_it[ordered0-listed0-expected0]`

Old text:

```
                return placed.index(one) + 1
        return 0
```

New text:

```
                return placed.index(one) + 1
        return len(placed)
```

### `r1432.P8_placed_in_front_of_its_neighbour`

an unread id is put in front of the track it follows rather than behind it, the target's and the listing's alike (R-1418's F6, in this unit's shape)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P8_placed_in_front_of_its_neighbour`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `r1434.F7_ordering_start_from_the_readable_tracks`

R-1418's zero row, now the card's pin: the ordering step records its start from the readable tracks, so a track unread at the stop and read since is left out of the path read and its move by the person is put back

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1434.json`, row `F7_ordering_start_from_the_readable_tracks`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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

### `r1434.M1_write_that_sent_nothing_read_on_its_whole_path`

round two's shape: a write known to have sent no move is read against its whole path, so a person's drag of one track to the top, where its first move would have put it, is finished over

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M1_write_that_sent_nothing_read_on_its_whole_path`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `r1446-b.C1_composite_no_unread_left_out`

the composite of r1446 rows M10 and M11, what they hold together: the settled reading and the reading now both compared with their unread ids in place, so a move of an unread track alone reads as a reorder again; either filter alone is equivalent, since reordered reads only the tracks both readings hold

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446-b.json`, row `C1_composite_no_unread_left_out`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `r1446.M14_plan_flag_dropped`

the plan never carries the flag, so the gate says the stopped order takes the unread track where it was taking it and never that only unread tracks moved

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `M14_plan_flag_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `r1446.M8_no_settled_reading_reads_no_move`

with no settled reading kept, the reorder is read as moving no readable track, so a reorder U234 read is dropped

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `M8_no_settled_reading_reads_no_move`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_with_no_settled_reading_a_reorder_stands_as_read`

Old text:

```
    if kept is None or not kept.settled:
        return True
```

New text:

```
    if kept is None or not kept.settled:
        return False
```

### `r1446.M9_unsettled_reading_compared`

an unsettled kept reading compared as though settled; unreachable while U234 reads a reorder only from a settled one

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `M9_unsettled_reading_compared`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_with_no_settled_reading_a_reorder_stands_as_read`

Old text:

```
    if kept is None or not kept.settled:
```

New text:

```
    if kept is None:
```

### `r1446.S3_u225_finish_whatever_was_read`

sample, U225: the stop finished even when a reorder was read

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `S3_u225_finish_whatever_was_read`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `r1453.S4_unread_keys_keep_a_readable_release`

the brief's row, R-1434's S4: the unread keys keep a key a readable release carries, so a row held as an unread release and a readable one is unread, left out of the order and its removal not read

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1453.json`, row `S4_unread_keys_keep_a_readable_release`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`

Old text:

```
    unread_keys = {alias(remote_id) for remote_id in unread} - readable_keys
```

New text:

```
    unread_keys = {alias(remote_id) for remote_id in unread}
```

### `r1453.U1_unread_keys_unaliased`

a nearby value: the unread keys read by each release's own key rather than its row's, so an unread release of a row held twice never meets the readable release's key

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1453.json`, row `U1_unread_keys_unaliased`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`

Old text:

```
    unread_keys = {alias(remote_id) for remote_id in unread} - readable_keys
```

New text:

```
    unread_keys = {remote_key(remote_id) for remote_id in unread} - readable_keys
```

### `r1453.U2_base_keeps_unread_keys`

R-1264's base strip gone: the base keeps an unread key, so an unread track is read as taken off the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1453.json`, row `U2_base_keeps_unread_keys`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `r1453.U4_removal_takes_only_the_linked_release`

U208's every release of a removed track goes, narrowed to the key's own release, so the readable release of a row held twice stays on the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1453.json`, row `U4_removal_takes_only_the_linked_release`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`

Old text:

```
                    [held for held in account_now if alias(held) == key] or [remote_of(key)]
```

New text:

```
                    [remote_of(key)]
```

### `r1453.U5_account_keys_take_unread_only_rows`

the account's keys read every listed id, an unread only row included, so it is placed by the merge as a readable row

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1453.json`, row `U5_account_keys_take_unread_only_rows`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `u130-b.B1_short_base_unnarrowed`

A short listing's withheld tracks read as removed on the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u130-b.json`, row `B1_short_base_unnarrowed`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_short_account_listing_reads_nothing_as_removed`

Old text:

```
        if short is not None:
            # A WITHHELD TRACK IS NOT A REMOVED ONE.
```

New text:

```
        if False:
            # A WITHHELD TRACK IS NOT A REMOVED ONE.
```

### `u130-b.B4_no_isrc_still_asked`

A row with no ISRC anywhere is still matched through the provider

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u130-b.json`, row `B4_no_isrc_still_asked`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_row_with_no_isrc_anywhere_is_named_and_the_provider_is_not_asked`

Old text:

```
            elif not isrc:
                reason = NO_ISRC
```

New text:

```
            elif False:
                reason = NO_ISRC
```

### `u130-b.B5_readd_old_rule`

A re-add is any change of the first row, so a duplicate losing one copy reads as put back

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u130-b.json`, row `B5_readd_old_rule`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_held_twice_that_lost_one_copy_is_not_read_as_put_back`

Old text:

```
            if content_id in base_rows and not (row_ids & base_rows[content_id])
```

New text:

```
            if content_id in base_rows and row_ids != base_rows[content_id]
```

### `u130-b.B6_requeue`

A track an earlier sync queued is queued again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u130-b.json`, row `B6_requeue`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
        if remote_id in queued_before:
```

New text:

```
        if False:
```

### `u130-b.B7_set_playlist_in_scope`

A set's playlist may be paired

- File: `src/cratekit/sync/pair_model.py`
- Source: `u130-b.json`, row `B7_set_playlist_in_scope`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_label_playlist_is_not_a_pair`

Old text:

```
    if account_id in set_built:
```

New text:

```
    if False:
```

### `u130-b.B8_tree_name_in_scope`

A playlist under a top level node the taxonomy names is in scope

- File: `src/cratekit/sync/pair_model.py`
- Source: `u130-b.json`, row `B8_tree_name_in_scope`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_playlist_under_one_of_cratekits_trees_is_not_a_pair`

Old text:

```
    if any(node_id in roots for node_id, _name in chain) or top_name in names:
```

New text:

```
    if any(node_id in roots for node_id, _name in chain):
```

### `u130-b.B9_stale_pair_blocks_all`

With no argument, one pair whose playlist is gone refuses every pair

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u130-b.json`, row `B9_stale_pair_blocks_all`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`

Old text:

```
                if not every or exc.cause.reason not in PER_PAIR_REASONS:
```

New text:

```
                if True:
```

### `u130-c.C1_half_written_snapshot`

Record the snapshot when either side was written, not both

- File: `src/cratekit/sync/pair_write.py`
- Source: `u130-c.json`, row `C1_half_written_snapshot`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_skipped_account_side_is_finished_by_the_next_sync`
  - `tests/test_sync_pair.py::test_a_skipped_rekordbox_side_is_finished_by_the_next_sync`
  - `tests/test_sync_pair.py::test_a_whole_sync_after_a_skipped_one_finishes_both_sides_from_the_old_base`
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_skipping_the_only_side_with_changes_answers_no_op`

Old text:

```
    whole = rekordbox_after is not None and account_after is not None and not one.withheld
```

New text:

```
    whole = (rekordbox_after is not None or account_after is not None) and not one.withheld
```

### `u147-c.M20_pair_scope`

sync.pair_cli._scope_account: a mirrored playlist may be paired

- File: `src/cratekit/sync/pair_model.py`
- Source: `u147-c.json`, row `M20_pair_scope`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_sync_pair_refuses_to_pair_a_mirrored_playlist`

Old text:

```
    if account_id in mirrored:
```

New text:

```
    if False:
```

### `u198.C10_unpair_account_gone`

plan: a made pair whose account playlist is gone is planned, not unpaired

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C10_unpair_account_gone`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_on_the_account_unpairs_stays_and_is_not_made_again`

Old text:

```
            if pair is not None and (pair.twin or pair.made) and target.account_id not in listed:
```

New text:

```
            if pair is not None and pair.twin and target.account_id not in listed:
```

### `u198.C11_unpair_rekordbox_gone`

plan: a made pair whose rekordbox playlist is gone is left out, not released

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C11_unpair_rekordbox_gone`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_made_pair_deleted_inside_archive_is_said_to_be_gone`
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_in_rekordbox_unpairs_and_leaves_the_account_playlist`

Old text:

```
                if there is None or there.removed:
```

New text:

```
                if False:
```

### `u198.C1_miss_reuse`

pair_cli._ask: a remembered miss is never reused

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u198.json`, row `C1_miss_reuse`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_sync_screens_every_code_it_will_ask_and_never_a_linked_row_or_a_remembered_miss`
  - `tests/test_sync_pair_discover.py::test_rows_the_account_cannot_carry_are_counted_skipped_and_never_asked_again`

Old text:

```
    if held is not None and held.isrc == isrc and AGREEING_RELEASES not in held.reason:
```

New text:

```
    if False:
```

### `u198.C2_miss_isrc`

pair_cli._ask: a remembered miss is reused whatever the row's ISRC

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u198.json`, row `C2_miss_isrc`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_remembered_miss_is_asked_again_when_the_rows_isrc_changes`

Old text:

```
    if held is not None and held.isrc == isrc and AGREEING_RELEASES not in held.reason:
```

New text:

```
    if held is not None and AGREEING_RELEASES not in held.reason:
```

### `u198.C3_unread_remembered`

pair_cli._ask: an unreadable candidate is remembered

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u198.json`, row `C3_unread_remembered`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_an_unreadable_candidate_is_never_remembered`

Old text:

```
    if UNREADABLE_CANDIDATE not in reason and AGREEING_RELEASES not in reason:
```

New text:

```
    if AGREEING_RELEASES not in reason:
```

### `u198.C4_tie_remembered`

pair_cli._ask: a tie is remembered

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u198.json`, row `C4_tie_remembered`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_tie_is_never_remembered_and_is_asked_again`

Old text:

```
    if UNREADABLE_CANDIDATE not in reason and AGREEING_RELEASES not in reason:
```

New text:

```
    if UNREADABLE_CANDIDATE not in reason:
```

### `u198.C5_folder_twice`

pair_cli._discovered: two root folders of the name adopt the first

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C5_folder_twice`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_two_root_folders_of_the_name_leave_that_folder_out`

Old text:

```
            if len(named) > 1:
```

New text:

```
            if len(named) > 2:
```

### `u198.C6_folder_others`

pair_cli._discovered: a folder another list keeps is adopted

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C6_folder_others`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_root_folder_another_list_of_cratekits_keeps_is_not_adopted`

Old text:

```
            elif named and named[0] in others:
```

New text:

```
            elif False:
```

### `u198.C7_title_taken`

pair_cli._discovered: a person's playlist of the title gets a second beside it

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C7_title_taken`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_an_existing_root_folder_of_the_name_is_reused_and_a_persons_title_is_left`

Old text:

```
            if one.title in taken:
```

New text:

```
            if False:
```

### `u198.C8_folder_gone`

pair_cli._discovered: a recorded folder is reused though the account deleted it

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C8_folder_gone`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_recorded_folder_deleted_on_the_account_is_made_again`

Old text:

```
        if recorded is not None and recorded.folder_id in root:
```

New text:

```
        if recorded is not None:
```

### `u198.C9_account_only`

apply_pair: a new pair is made when only rekordbox was approved

- File: `src/cratekit/sync/pair_write.py`
- Source: `u198.json`, row `C9_account_only`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_skipping_the_account_gate_makes_and_marks_nothing`

Old text:

```
        if not account:
            return done
```

New text:

```
        if False:
            return done
```

### `u202-composites.C10_reads_account`

plan: a sync of every pair with no marked pair never lists the account, so nothing comes back

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u202-composites.json`, row `C10_reads_account`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_with_every_pair_released_a_new_playlist_in_a_recorded_folder_still_comes`

Old text:

```
    reads_account = bool(wanted) or (every and bool(document.folders))
```

New text:

```
    reads_account = bool(wanted)
```

### `u202-composites.C3_composite`

composite for C3_removed_only in u202.md: plan_pair never dates a rekordbox removal, so a removal later than the account's put back reads as no moment

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u202-composites.json`, row `C3_composite`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`

Old text:

```
                rekordbox_removed[as_key(content_id)] = max(
```

New text:

```
                _undated = max(
```

### `u202-composites.C8_scope`

_discovered_back: an account playlist a pair may not hold is brought over

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u202-composites.json`, row `C8_scope`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_set_playlist_sharing_a_name_does_not_stop_the_authors_own`

Old text:

```
            try:
                _scope_account(
                    account_id, reader.listed, reader.label_owned, reader.set_built, reader.mirrored
                )
            except CratekitError as exc:
```

New text:

```
            try:
                pass
            except CratekitError as exc:
```

### `u202.C1_after_synced`

plan_pair: an account date not after the base's sync still reads the track as put back

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u202.json`, row `C1_after_synced`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_put_back_dated_before_the_last_sync_is_no_put_back`

Old text:

```
                    and now > was
                    and now > synced
```

New text:

```
                    and now > was
```

### `u202.C4_dates_recorded`

_record: the account's added dates are never recorded with the snapshot

- File: `src/cratekit/sync/pair_write.py`
- Source: `u202.json`, row `C4_dates_recorded`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_back.py::test_a_removal_rekordbox_kept_no_moment_for_keeps_the_track_and_names_the_call`
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`
  - `tests/test_sync_pair_back.py::test_the_snapshot_records_each_account_tracks_added_date`

Old text:

```
            if whole
            else None
        ),
        rekordbox=(
```

New text:

```
            if False
            else None
        ),
        rekordbox=(
```

### `u202.C5_released`

_discovered_back: a released account playlist is made in rekordbox again

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u202.json`, row `C5_released`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_made_pair_whose_rekordbox_playlist_is_deleted_releases_its_account_playlist`
  - `tests/test_sync_pair_back.py::test_a_released_account_playlist_is_never_made_again`

Old text:

```
            if account_id in released:
```

New text:

```
            if False:
```

### `u202.C7_twice`

_discovered_back: two account playlists of one rekordbox name are both made

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u202.json`, row `C7_twice`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_two_account_playlists_of_one_rekordbox_name_refuse_that_name_only`

Old text:

```
        if many > 1:
```

New text:

```
        if many > 2:
```

### `u207.P1_pair_screens_remembered_miss`

sync pair: a remembered miss's code is screened though it is never asked

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u207.json`, row `P1_pair_screens_remembered_miss`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_isrc_screen.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_sync_screens_every_code_it_will_ask_and_never_a_linked_row_or_a_remembered_miss`

Old text:

```
        and _remembered_miss(reader, content_id, code) is None

```

New text:

```
(empty)
```

### `u207.P2_pair_never_screens`

sync pair: the plan never screens, so every code is asked alone

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u207.json`, row `P2_pair_never_screens`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_isrc_screen.py`
- Collected: 154 against a baseline of 154
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_code_the_account_playlist_already_holds_is_never_screened`
  - `tests/test_sync_pair_discover.py::test_a_sync_screens_every_code_it_will_ask_and_never_a_linked_row_or_a_remembered_miss`

Old text:

```
    if asked:
        reader.remote.screen_isrcs(asked)
```

New text:

```
    if False:
        reader.remote.screen_isrcs(asked)
```

### `u208.M11_alias_off`

alias: read every account track as its own key, so two releases of one row are two keys again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M11_alias_off`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `u208.M4_tie_flag_dropped`

_ask: never say a tie was broken, so the gate counts none

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M4_tie_flag_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
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

### `u208.M9_here_lookup_dropped`

_owned: never look among the pair's own rows, so a sibling of a file ISRC row is queued for acquisition

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M9_here_lookup_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `u209.C10_reverse_recheck`

check: run no recheck of a made rekordbox side's home before the write

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C10_reverse_recheck`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_brought_playlists_folder_gone_reads_as_one_sentence`
  - `tests/test_sync_pair_hold_every.py::test_a_rekordbox_name_taken_before_the_write_stops_every_pair_before_any_is_written`

Old text:

```
                    pair_reverse.recheck(db, one.home, one.change.order)
```

New text:

```
                    pass
```

### `u209.C11_home_of`

check: compare no home a made rekordbox side goes to with the plan's

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C11_home_of`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_brought_playlists_rekordbox_folder_archived_before_the_write_refuses_stale`

Old text:

```
                if now != one.home:
```

New text:

```
                if False:
```

### `u209.C12_brought_folder`

check: read no brought playlist taken out of its account folder

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C12_brought_folder`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_brought_playlist_taken_out_of_its_account_folder_before_the_write_refuses_stale`

Old text:

```
            if listing.get(one.target.account_id) != one.target.title:
```

New text:

```
            if False:
```

### `u209.C13_jobs_queued`

check: read no acquisitions another sync queued since the plan

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C13_jobs_queued`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale`
  - `tests/test_sync_pair_hold.py::test_tracks_another_sync_queued_before_the_write_refuse_stale_not_twice`

Old text:

```
            again = sorted(set(one.acquire) & now)
```

New text:

```
            again = []
```

### `u209.C3_withheld`

check: read no change in the account's withheld count

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C3_withheld`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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

### `u210.R10_check_todo`

check: read every pair, a finished one included

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R10_check_todo`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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

### `u210.R18_beyond_order`

_beyond: read no order on a part written playlist

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R18_beyond_order`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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

### `u210.R1_made_step_read`

apply_pair: never read a made side recorded by an earlier command, so a continue makes it again

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R1_made_step_read`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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

### `u210.R20_beyond_lost`

_beyond: read no track lost

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R20_beyond_lost`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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

### `u210.R2_resumed_move`

_made: move only a playlist this call made, so a stop between the make and the move leaves it at the root

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R2_resumed_move`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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

### `u210.R3_made_here_folder`

_made_here: read a reservation in any folder as made here

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R3_made_here_folder`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_made_here_reads_only_a_pair_made_for_this_playlist_in_this_folder`

Old text:

```
        and held.folder == place.folder
```

New text:

```
        and True
```

### `u210.R4_rekordbox_landed`

apply_pair: write rekordbox again on a continue whose commit already landed

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R4_rekordbox_landed`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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

### `u216-m14.M14_moment_any_folder`

_discovered_back: the adoption moment reads made pairs in every folder, not only this one

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u216-m14.json`, row `M14_moment_any_folder`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_moment_is_read_from_this_folders_own_pairs`

Old text:

```
                if pair.made and pair.folder == folder
```

New text:

```
                if pair.made
```

### `u216.M13_unrecorded_off`

_discovered_back: no folder reads as unrecorded, so a pre U216 adoption is read as a created folder

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u216.json`, row `M13_unrecorded_off`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_without_a_record_or_a_creation_time_every_unpaired_playlist_is_named`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_creation_time_decides`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_moment_is_read_from_this_folders_own_pairs`

Old text:

```
        unrecorded = recorded.held is None and not recorded.created
```

New text:

```
        unrecorded = False
```

### `u216.M15_before_rule_off`

_discovered_back: the before adoption rule is not applied

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u216.json`, row `M15_before_rule_off`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_a_creation_time_without_a_zone_is_no_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_or_a_creation_time_every_unpaired_playlist_is_named`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_creation_time_decides`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_moment_is_read_from_this_folders_own_pairs`

Old text:

```
            if before:
                left(account_id, title, folder, pair_discover.BEFORE, before)
```

New text:

```
            if False:
                left(account_id, title, folder, pair_discover.BEFORE, before)
```

### `u216.M16_copy_rule_off`

_discovered_back: the DOWNLOADED copy rule is not applied

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u216.json`, row `M16_copy_rule_off`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_in_a_created_folder_is_named_a_copy`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`

Old text:

```
            if copied:
                whose = (
```

New text:

```
            if False:
                whose = (
```

### `u216.M18_copy_all_titles`

_discovered_back: the paired titles are every title in the folder, paired or not

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u216.json`, row `M18_copy_all_titles`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`

Old text:

```
            title for account_id, title in inside.items() if account_id in paired_ids
        ]
```

New text:

```
            title for account_id, title in inside.items()
        ]
```

### `u216.M19_place_held_empty`

_discovered: an adopted folder's plan carries an empty listing, so the adoption records it held nothing

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u216.json`, row `M19_place_held_empty`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
                        held=frozenset(inside) if action == FOLDER_ADOPT else None,
```

New text:

```
                        held=frozenset() if action == FOLDER_ADOPT else None,
```

### `u216.M20_made_drops_held`

_made: the plan's listing is not passed to the folder's reservation

- File: `src/cratekit/sync/pair_write.py`
- Source: `u216.json`, row `M20_made_drops_held`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_playlist_no_pair_names_still_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_the_adopted_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
        stale=place.stale,
        held=place.held,
    )
```

New text:

```
        stale=place.stale,
    )
```

### `u220.P2_session_tolerated`

ORDER_REFUSALS: tolerate a rejected session too, so every later pair meets it

- File: `src/cratekit/sync/pair_model.py`
- Source: `u220.json`, row `P2_session_tolerated`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
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

### `u221.R10_digest_without_the_hold`

PairPlan.identity: leave the held tracks out of the digest, so an approval over one hold is read as approving another

- File: `src/cratekit/sync/pair_model.py`
- Source: `u221.json`, row `R10_digest_without_the_hold`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_the_plans_digest_moves_with_the_hold`

Old text:

```
                {"on_hold": sorted(named.remote_id for named in self.on_hold)}
                if self.on_hold
                else {}
```

New text:

```
                {}
```

### `u221.R11_no_warning_per_twin`

_warnings: drop the on hold warning, so the answer never counts the held tracks per twin or names the release command

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u221.json`, row `R11_no_warning_per_twin`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`

Old text:

```
    holding = [one for one in planned.pairs if one.on_hold]
```

New text:

```
    holding = []
```

### `u221.R1_hold_only_a_twin`

held_for_choice: drop the twin test, so a pair that is no twin reads by time and holds every undated track the library lacks

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R1_hold_only_a_twin`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `u221.R2_recorded_hold_never_holds`

held_for_choice: a recorded hold holds nothing, so a twin made since U221 queues its missing tracks

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R2_recorded_hold_never_holds`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_pair_that_is_no_twin_never_holds`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_a_plain_pair_lists_is_queued_once_and_still_held`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record`

Old text:

```
    if recorded is not None:
        return remote_id in recorded
```

New text:

```
    if recorded is not None:
        return False
```

### `u221.R3_recorded_hold_holds_everything`

held_for_choice: a recorded hold holds every track, so a track added later and a released twin's tracks are never queued

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R3_recorded_hold_holds_everything`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_pair_that_is_no_twin_never_holds`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_is_released_by_name_and_counted_by_time`
  - `tests/test_sync_twins_hold.py::test_release_all_lets_every_twin_go`
  - `tests/test_sync_twins_hold.py::test_releasing_the_twin_queues_its_three_at_the_next_sync`

Old text:

```
    if recorded is not None:
        return remote_id in recorded
```

New text:

```
    if recorded is not None:
        return True
```

### `u221.R4_undated_not_held`

held_for_choice: a pre U221 twin's undated track is read as added after the mark and queued

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R4_undated_not_held`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_short_listings_twin_records_no_hold_and_holds_a_track_served_later`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_holds_what_the_account_dates_before_its_mark`

Old text:

```
    if marked is None or added is None:
        return True
```

New text:

```
    if marked is None or added is None:
        return False
```

### `u221.R5_time_rule_never_holds`

held_for_choice: a pre U221 twin's dated track is never held, so a track dated before the mark is queued

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R5_time_rule_never_holds`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_track_dated_at_the_very_mark_is_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_holds_what_the_account_dates_before_its_mark`

Old text:

```
    return not added > marked
```

New text:

```
    return False
```

### `u221.R6_time_rule_always_holds`

held_for_choice: a pre U221 twin holds a track dated after the mark, so one put on by hand since is never queued

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R6_time_rule_always_holds`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_track_dated_at_the_very_mark_is_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_holds_what_the_account_dates_before_its_mark`

Old text:

```
    return not added > marked
```

New text:

```
    return True
```

### `u221.R7_plan_ignores_the_hold`

plan_pair: drop the hold branch, so every held track is queued as before U221

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R7_plan_ignores_the_hold`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_short_listings_twin_records_no_hold_and_holds_a_track_served_later`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_holds_what_the_account_dates_before_its_mark`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_a_plain_pair_lists_is_queued_once_and_still_held`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record`

Old text:

```
        elif held_for_choice(held, remote_id, dates):
```

New text:

```
        elif False:
```

### `u221.R8_hold_before_awaiting`

plan_pair: read the hold before the queued before check, so a track an earlier sync queued is named on hold rather than awaiting

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R8_hold_before_awaiting`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`

Old text:

```
        if remote_id in queued_before:
            awaiting.append(names[key])
        elif held_for_choice(held, remote_id, dates):
```

New text:

```
        if held_for_choice(held, remote_id, dates):
            on_hold.append(names[key])
        elif remote_id in queued_before:
            awaiting.append(names[key])
        elif held_for_choice(held, remote_id, dates):
```

### `u221.R9_gate_names_no_held_track`

_items: drop the on-hold rows, so the gate names no held track

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u221.json`, row `R9_gate_names_no_held_track`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_short_listings_twin_records_no_hold_and_holds_a_track_served_later`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_holds_what_the_account_dates_before_its_mark`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_a_plain_pair_lists_is_queued_once_and_still_held`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record`

Old text:

```
    for named in one.on_hold:
        items.append(row("library", ON_HOLD_ACTION, named))
```

New text:

```
    for named in ():
        items.append(row("library", ON_HOLD_ACTION, named))
```

### `u225.M14_superseded_unchecked`

stopped_write: a write the pair's snapshot came after is still finished

- File: `src/cratekit/sync/pair_read.py`
- Source: `u225.json`, row `M14_superseded_unchecked`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_a_fresh_sync_finished_is_left_behind_by_the_snapshot`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
            if synced is None or not began > synced:
```

New text:

```
            if synced is None:
```

### `u225.M15_fold_despite_skip`

plan_pair: both bases move to the stopped write's though it skipped rekordbox

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u225.json`, row `M15_fold_despite_skip`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_that_skipped_rekordbox_leaves_the_accounts_removal_to_be_made`

Old text:

```
    folded = stopped_write is not None and stopped_write.written
```

New text:

```
    folded = stopped_write is not None
```

### `u225.M16_account_base_unfolded`

plan_pair: the account base is the snapshot's, not what the stopped write left

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u225.json`, row `M16_account_base_unfolded`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_the_stopped_write_added_then_taken_off_in_rekordbox_comes_off_the_account`

Old text:

```
                if folded
                else held.account or ()
```

New text:

```
                if False
                else held.account or ()
```

### `u225.M17_rekordbox_base_unfolded`

plan_pair: the rekordbox base is the snapshot's, not what the stopped write left

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u225.json`, row `M17_rekordbox_base_unfolded`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_the_stopped_write_added_then_taken_off_in_rekordbox_comes_off_the_account`

Old text:

```
            if folded
            else tuple(held.rekordbox or ())
```

New text:

```
            if False
            else tuple(held.rekordbox or ())
```

### `u225.M20_stopped_not_passed`

plan_pair: the stopped write is not handed to the merge

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u225.json`, row `M20_stopped_not_passed`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_names_the_pair_as_finishing_the_stopped_run`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_says_the_account_was_read_off_the_moves_path`

Old text:

```
        stopped=stopped,
```

New text:

```
        stopped=None,
```

### `u225.M21_start_from_asked`

_write_account: the start is built from the asked removals and additions, not the adapter's answer

- File: `src/cratekit/sync/pair_write.py`
- Source: `u225.json`, row `M21_start_from_asked`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_an_addition_the_provider_left_out_is_never_read_as_taken_off`

Old text:

```
                    one.account_before or one.account_now, removed, added
```

New text:

```
                    one.account_before or one.account_now, one.account_removes, one.account_adds
```

### `u225.M22_written_always`

_write_account: the step says rekordbox was committed though its gate was skipped

- File: `src/cratekit/sync/pair_write.py`
- Source: `u225.json`, row `M22_written_always`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_that_skipped_rekordbox_leaves_the_accounts_removal_to_be_made`

Old text:

```
                written=rekordbox_after is not None,
```

New text:

```
                written=True,
```

### `u225.M23_links_dropped`

_write_account: the step records none of the write's links

- File: `src/cratekit/sync/pair_write.py`
- Source: `u225.json`, row `M23_links_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_the_stopped_write_added_then_taken_off_in_rekordbox_comes_off_the_account`

Old text:

```
                written=rekordbox_after is not None,
                links=one.links,
```

New text:

```
                written=rekordbox_after is not None,
                links={},
```

### `u225.M24_unread_unsaid`

_warnings: runs' steps that could not be read are not named

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u225.json`, row `M24_unread_unsaid`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 664 against a baseline of 664
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`
  - `tests/test_sync_pair_stopped_order.py::test_a_runs_steps_that_cannot_be_read_are_named_never_read_as_no_write`

Old text:

```
    if planned.stopped_unread:
```

New text:

```
    if False:
```

### `u226.M19_plan_no_hold`

plan_pair: a lagging pair is planned from its window rather than held

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u226.json`, row `M19_plan_no_hold`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `u226.M20_check_no_lag`

check: a lagging listing is compared as read rather than named as moved

- File: `src/cratekit/sync/pair_check.py`
- Source: `u226.json`, row `M20_check_no_lag`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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

### `u226.M21_plan_window_only`

plan_pair: the account side listed from its window alone

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u226.json`, row `M21_plan_window_only`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `u226.M22_lagging_not_per_pair`

PER_PAIR_REASONS: a lagging pair refuses the whole sync of every pair

- File: `src/cratekit/sync/pair_model.py`
- Source: `u226.json`, row `M22_lagging_not_per_pair`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
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

### `u229.M10_file_isrc_fallback`

mirror_codes: read only the database ISRC, so a landed row whose code is in its file alone is never found

- File: `src/cratekit/sync/pair_read.py`
- Source: `u229.json`, row `M10_file_isrc_fallback`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_is_added_and_never_queued`
  - `tests/test_sync_pair.py::test_each_landed_file_is_read_once_per_plan`
  - `tests/test_sync_pair.py::test_one_row_landed_in_two_inbox_playlists_is_one_row`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[torn]`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[unknown-state]`
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`
  - `tests/test_sync_pair.py::test_two_landed_rows_carrying_the_code_are_ambiguous_and_queue_nothing`
  - `tests/test_sync_pair_hold.py::test_a_track_found_by_another_landing_costs_the_plan_no_call[by another account playlist's landing]`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`

Old text:

```
    for row in playlist_pair.members(db, mirror):
        code = match.isrc_token(row.isrc) or file_identity(cfg, row.path)[0]
        if code:
            found.append((code, row.content_id))
```

New text:

```
    for row in playlist_pair.members(db, mirror):
        code = match.isrc_token(row.isrc)
        if code:
            found.append((code, row.content_id))
```

### `u229.M11_mirror_cache`

_Reader.mirror_codes: read the playlist's files on every ask, so a plan reads a landed file once per step

- File: `src/cratekit/sync/pair_read.py`
- Source: `u229.json`, row `M11_mirror_cache`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_each_landed_file_is_read_once_per_plan`

Old text:

```
        if mirror not in self.landed_codes:
```

New text:

```
        if True:
```

### `u229.M12_own_mirrors_bypass_cache`

_mirror_isrcs: read this pair's landings without the plan's copy, so the widened step reads each own landed file again

- File: `src/cratekit/sync/pair_read.py`
- Source: `u229.json`, row `M12_own_mirrors_bypass_cache`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_each_landed_file_is_read_once_per_plan`

Old text:

```
        reader.cfg, reader.db, reader.mirrors.get(account_id, ()), read=reader.mirror_codes
    )
```

New text:

```
        reader.cfg, reader.db, reader.mirrors.get(account_id, ())
    )
```

### `u229.M15_wide_landed_needs_rest`

_owned: the widened landed step answers a track an earlier step already found, overwriting its row

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `M15_wide_landed_needs_rest`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`

Old text:

```
    if rest:
        landed = reader.landed_anywhere
        for remote_id in rest:
```

New text:

```
    if rest:
        landed = reader.landed_anywhere
        for remote_id in [one for one in lacking if codes.get(one)]:
```

### `u229.M1_wide_landed_step`

_owned: drop the step that reads every landed INBOX playlist, so a track another account playlist landed is queued again (sitting 86)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `M1_wide_landed_step`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_is_added_and_never_queued`
  - `tests/test_sync_pair.py::test_one_row_landed_in_two_inbox_playlists_is_one_row`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[torn]`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[unknown-state]`
  - `tests/test_sync_pair.py::test_two_landed_rows_carrying_the_code_are_ambiguous_and_queue_nothing`
  - `tests/test_sync_pair_hold.py::test_a_track_found_by_another_landing_costs_the_plan_no_call[by another account playlist's landing]`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`

Old text:

```
        landed = reader.landed_anywhere
```

New text:

```
        landed = {}
```

### `u229.M2_wide_landed_reads_own_only`

_Reader.landed_anywhere: read only the first account playlist's landings, so most accounts' landed tracks are queued again

- File: `src/cratekit/sync/pair_read.py`
- Source: `u229.json`, row `M2_wide_landed_reads_own_only`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_two_landed_rows_carrying_the_code_are_ambiguous_and_queue_nothing`

Old text:

```
        for ids in self.mirrors.values():
            every.update(ids)
```

New text:

```
        for ids in list(self.mirrors.values())[:1]:
            every.update(ids)
```

### `u229.M3_wide_jobs_step`

_owned: drop the step that reads every other pair's intake jobs, so a track another pair's job found owned is queued

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `M3_wide_jobs_step`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_another_pairs_intake_job_found_owned_is_added`

Old text:

```
        for remote_id, content_id in _owned_by_jobs(reader, others, rest, own=False).items():
```

New text:

```
        for remote_id, content_id in {}.items():
```

### `u229.M4_wide_jobs_own_only`

_owned: the widened job step reads this pair's own jobs again, never another pair's

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `M4_wide_jobs_own_only`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_another_pairs_intake_job_found_owned_is_added`

Old text:

```
        others = tuple(job for job in reader.pair_jobs if job.job_id not in mine)
```

New text:

```
        others = tuple(job for job in reader.pair_jobs if job.job_id in mine)
```

### `u229.M5_wide_jobs_strict`

_owned: read other pairs' jobs as the pair's own, so one pair's job whose configuration no longer reads refuses every plan

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `M5_wide_jobs_strict`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_another_pairs_job_that_no_longer_reads_stops_no_plan`

Old text:

```
_owned_by_jobs(reader, others, rest, own=False)
```

New text:

```
_owned_by_jobs(reader, others, rest, own=True)
```

### `u229.M6_config_error_not_caught`

_Reader.job_reports: catch only a refusal, so a configuration error from any job's reports escapes

- File: `src/cratekit/sync/pair_read.py`
- Source: `u229.json`, row `M6_config_error_not_caught`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_another_pairs_job_that_no_longer_reads_stops_no_plan`

Old text:

```
            except (CratekitError, config.ConfigError) as error:
```

New text:

```
            except CratekitError as error:
```

### `u229.M8_own_landing_first`

_owned: this pair's own landing step reads every landing, so another account's row carrying the code makes the pair's own row ambiguous

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `M8_own_landing_first`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`

Old text:

```
        landed = _mirror_isrcs(reader, account_id)
```

New text:

```
        landed = reader.landed_anywhere
```

### `u229.M9_landed_dedup`

landed_isrcs: append a row once for each INBOX playlist holding it, so one row landed twice reads as ambiguous

- File: `src/cratekit/sync/pair_read.py`
- Source: `u229.json`, row `M9_landed_dedup`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_one_row_landed_in_two_inbox_playlists_is_one_row`

Old text:

```
            if content_id not in found.setdefault(code, []):
                found[code].append(content_id)
```

New text:

```
            found.setdefault(code, []).append(content_id)
```

### `u229.S1_ambiguous_count`

plan_pair (sample, U130): add the first of several rows carrying the code rather than naming it ambiguous

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `S1_ambiguous_count`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_two_landed_rows_carrying_the_code_are_ambiguous_and_queue_nothing`
  - `tests/test_sync_pair.py::test_two_rows_carrying_one_isrc_add_neither_and_say_so`

Old text:

```
            if len(answer) == 1:
                content_id = answer[0]
```

New text:

```
            if len(answer) >= 1:
                content_id = answer[0]
```

### `u229.S2_own_landed_step`

_owned (sample, U128): drop this pair's own landed step, so a track its own landing brought is answered only by the widened step

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `S2_own_landed_step`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`

Old text:

```
        landed = _mirror_isrcs(reader, account_id)
        for remote_id in rest:
```

New text:

```
        landed = {}
        for remote_id in rest:
```

### `u231.M10_moved_unrecorded`

write: every move accepted is not recorded, so a later lag on the path is finished from

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M10_moved_unrecorded`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`

Old text:

```
        steps.mark(STEP_MOVED, timestamp())
```

New text:

```
        pass
```

### `u231.M12_settle_takes_any_reading`

settle: any reading finishes the pair, the order the moves leave or not

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M12_settle_takes_any_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_pair_that_never_settles_stays_pending_past_the_age_a_plan_is_kept`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_is_held_whole_until_a_later_reading_agrees`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_pending_run_does_not_count_its_pending_pair_as_synced`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_write_that_keeps_no_record_sends_no_order`
  - `tests/test_sync_pair_settle.py::test_an_agreeing_reading_too_soon_after_the_last_is_not_agreement`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`

Old text:

```
        if reading is not None and tuple(reading) == tuple(settle.end):
```

New text:

```
        if reading is not None:
```

### `u231.M14_settle_reading_not_kept`

settle: a reading short of the order is not kept on the pair for the next plan to agree with

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M14_settle_reading_not_kept`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok`

Old text:

```
        if reading is not None:
            pairs.PairStore(cfg).see(settle.one.target.account_id, reading, at=timestamp())
```

New text:

```
        if False:
            pairs.PairStore(cfg).see(settle.one.target.account_id, reading, at=timestamp())
```

### `u231.M15_pending_not_read`

plan: a pending order is planned as U225 would, with no agreement asked

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M15_pending_not_read`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 26 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_pair_that_never_settles_stays_pending_past_the_age_a_plan_is_kept`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_is_held_whole_until_a_later_reading_agrees`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_settle.py::test_a_reading_kept_from_before_the_moves_is_no_agreement`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    if stopped_write is not None and stopped_write.pending:
```

New text:

```
    if False:
```

### `u231.M16_shown_order_not_finished`

plan: a reading showing the order the moves leave still waits for agreement

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M16_shown_order_not_finished`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_late_order_finishes_in_the_next_run_with_no_rekordbox_write_between`
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`

Old text:

```
    if pair_stopped.shows(write.end, now):
        return
```

New text:

```
    if False:
        return
```

### `u231.M18_reading_before_the_moves_kept`

plan: a reading kept before the moves began counts toward agreement

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M18_reading_before_the_moves_kept`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_reading_kept_from_before_the_moves_is_no_agreement`

Old text:

```
    kept = seen_at is not None and seen_at >= write.moving_at and tuple(held.seen) == now
```

New text:

```
    kept = seen_at is not None and tuple(held.seen) == now
```

### `u231.M20_every_reading_kept`

plan: every reading replaces the one kept, so one too soon resets the wait

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M20_every_reading_kept`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_two_readings_agree_only_once_minutes_apart`

Old text:

```
    if not kept:
        reader.see(target.account_id, now)
```

New text:

```
    if True:
        reader.see(target.account_id, now)
```

### `u231.M22_root_playlist_named_gig_ready`

scope: a root playlist named GIG READY is read as under the folder (round one's row 6)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M22_root_playlist_named_gig_ready`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_root_playlist_named_gig_ready_is_not_under_gig_ready`

Old text:

```
        return bool(rekordbox.ancestors) and rekordbox.top[1] == ORDER_FOLDER
```

New text:

```
        return rekordbox.top[1] == ORDER_FOLDER
```

### `u231.M23_carried_moving_unread`

continue: the carried record is not read when the run's steps cannot show the moves (round two's row 4)

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M23_carried_moving_unread`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[gone]`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[unreadable]`

Old text:

```
            moving = steps.carried(STEP_MOVING)
```

New text:

```
            moving = None
```

### `u231.M7_continue_resends`

write: a continue whose pair's moves began sends the order again rather than only reading it

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M7_continue_resends`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[gone]`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[unreadable]`
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_whose_moves_all_landed_finishes_on_the_continue`

Old text:

```
        if isinstance(moving, Mapping):
```

New text:

```
        if False:
```

### `u231.M8_no_record_sends_blind`

write: a write that keeps no record sends its order's moves anyway (round one's BLOCKING row)

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M8_no_record_sends_blind`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_write_that_keeps_no_record_sends_no_order`

Old text:

```
        if steps.steps is None:
            # U231, ROUND ONE'S REVIEW.
```

New text:

```
        if False:
            # U231, ROUND ONE'S REVIEW.
```

### `u234.O11_after_not_replaced`

an order after a settled one that moves again is not kept afresh, so the order it moved to is held for good

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O11_after_not_replaced`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`

Old text:

```
    if kept.after is None or since is None or pair_stopped.reordered(kept.after, reading):
```

New text:

```
    if kept.after is None or since is None:
```

### `u234.O12_kept_reading_of_any_run`

_kept_after takes a reading kept for another run as this stop's

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O12_kept_reading_of_any_run`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_kept_reading_counts_only_for_its_run_at_or_after_its_moves`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_for_another_run_shows_no_reorder`

Old text:

```
    if kept is None or kept.run != write.run_id:
```

New text:

```
    if kept is None:
```

### `u234.O13_kept_reading_before_the_stop`

_kept_after takes a reading kept before the stop as one after it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O13_kept_reading_before_the_stop`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_kept_reading_counts_only_for_its_run_at_or_after_its_moves`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_before_the_stop_shows_no_reorder`

Old text:

```
    if seen_at is None or seen_at < began:
```

New text:

```
    if seen_at is None:
```

### `u234.O1_off_path_dropped_from_the_finish`

the defect back: an account off the stopped write's path is left out of the finish, so the folded base reads it as reordered and it is written into rekordbox

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O1_off_path_dropped_from_the_finish`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 21 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_reading_that_never_settled_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_before_the_stop_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_for_another_run_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_on_the_path_is_never_the_baseline_so_the_partial_state_after_it_finishes`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    if stopped_write is not None and not reordered_since_stop:
```

New text:

```
    if stopped_write is not None and not reordered_since_stop and not off_path:
```

### `u234.O21_gate_says_on_path`

the gate line says on the path for an account read off it

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u234.json`, row `O21_gate_says_on_path`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_says_the_account_was_read_off_the_moves_path`

Old text:

```
                    if one.finishing_off_path
                    else "so its moves are not read as anybody's; "
```

New text:

```
                    if False
                    else "so its moves are not read as anybody's; "
```

### `u234.O22_finishing_note_silent`

the sync-pair-finishing note leaves out that the account was read off the path

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u234.json`, row `O22_finishing_note_silent`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_says_the_account_was_read_off_the_moves_path`

Old text:

```
                            "it is not read as a reorder; "
                            if one.finishing_off_path
```

New text:

```
                            "it is not read as a reorder; "
                            if False
```

### `u234.O23_off_path_flag_on_every_finish`

finishing_off_path is set on every finish, so the gate says off the path for one on it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O23_off_path_flag_on_every_finish`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_names_the_pair_as_finishing_the_stopped_run`

Old text:

```
        finishing_off_path=stopped is not None and off_path,
```

New text:

```
        finishing_off_path=stopped is not None,
```

### `u234.O25_on_path_reading_kept`

round two's fix undone: a reading on the moves' path is kept and settled as the baseline, so a lag of the whole write then the partial state is read as a reorder

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O25_on_path_reading_kept`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_reading_that_never_settled_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_later_reading_still_on_the_moves_path_is_finished_never_read_as_a_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_on_the_path_is_never_the_baseline_so_the_partial_state_after_it_finishes`
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`

Old text:

```
    kept = _kept_after(held, write)
    if not off_path:
```

New text:

```
    kept = _kept_after(held, write)
    if False:
```

### `u234.O26_on_path_reading_keeps_the_order_after`

a reading on the path leaves an order held as the one after on its old clock, so read again it leads at once

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O26_on_path_reading_keeps_the_order_after`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`

Old text:

```
        # any order held as the one after, so that order waits afresh.
        if kept is not None and kept.after is not None:
```

New text:

```
        # any order held as the one after, so that order waits afresh.
        if False:
```

### `u234.O27_settled_order_keeps_the_order_after`

a reading back at the settled order leaves an order held as the one after on its old clock, so read again it leads at once

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O27_settled_order_keeps_the_order_after`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`

Old text:

```
        # as the one after waits afresh if it is read again.
        if kept.after is not None:
```

New text:

```
        # as the one after waits afresh if it is read again.
        if False:
```

### `u234.O3_person_never_leads`

an order after a settled one that agrees over the window never leads, so a person's reorder is held for good

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O3_person_never_leads`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
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
        return True
    if kept.after is None or since is None
```

New text:

```
        return False
    if kept.after is None or since is None
```

### `u234.O4_settled_order_read_as_moved`

a reading back at the settled order is read as differing from it, so the order after is held for it and the stop is never finished

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O4_settled_order_read_as_moved`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_added_on_the_account_between_two_readings_is_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`
  - `tests/test_sync_pair_stopped_order.py::test_two_syncs_reading_the_same_order_off_the_path_are_no_reorder`

Old text:

```
    if not pair_stopped.reordered(kept.order, reading):
        # BACK AT THE SETTLED ORDER
```

New text:

```
    if False:
        # BACK AT THE SETTLED ORDER
```

### `u234.O5_unsettled_reading_read_as_settled`

round one's defect back: a kept reading counts before it settles, so the provider moving between two plans is read as the person

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O5_unsettled_reading_read_as_settled`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`

Old text:

```
    if not kept.settled:
```

New text:

```
    if False:
```

### `u234.O6_reading_never_kept`

the plan keeps no reading after the stop, so no later sync can show a person's reorder

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O6_reading_never_kept`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 13 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`

Old text:

```
    if kept is None:
        reader.see_stop(target.account_id, pairs.StopReading(write.run_id, reading, stamp))
        return False
```

New text:

```
    if kept is None:
        return False
```

### `u234.O8_moved_reading_not_kept_afresh`

a reading in another order before the kept one settles does not replace it, so a lag is settled as the first reading

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O8_moved_reading_not_kept_afresh`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`

Old text:

```
        if pair_stopped.reordered(kept.order, reading):
            reader.see_stop(target.account_id, pairs.StopReading(write.run_id, reading, stamp))
        elif
```

New text:

```
        if False:
            pass
        elif
```

### `u234.S1_sample_finish_held_to_the_plans_reading`

sample, R-1411: the finish is not held to the plan's reading, so the rest of an off path order is moved from whatever the adapter reads

- File: `src/cratekit/sync/pair_write.py`
- Source: `u234.json`, row `S1_sample_finish_held_to_the_plans_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            if one.finishing_order and one.account_before
```

New text:

```
            if False and one.finishing_order and one.account_before
```

### `u246.S10_pair_cli_started_empty`

pair: the stopped write's start as an empty set, so a folded base holds nothing it asked for

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u246.json`, row `S10_pair_cli_started_empty`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
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

### `u246.S11_pair_cli_served_empty`

pair: the served keys as an empty set, so under a short listing every base key reads as withheld

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u246.json`, row `S11_pair_cli_served_empty`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_hold.py`
- Collected: 132 against a baseline of 132
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_short_listing_removes_nothing_from_the_account`

Old text:

```
            served = set(account_keys)
```

New text:

```
            served = set()
```

### `u246.S12_pair_cli_made_here_empty`

pair: no account ids made this run, so discovery is told every pair, the ones this run made included, is already paired

- File: `src/cratekit/sync/pair_check.py`
- Source: `u246.json`, row `S12_pair_cli_made_here_empty`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
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

### `u246.S13_pair_cli_per_element`

pair: build the made here set once per pair again (the shape on main)

- File: `src/cratekit/sync/pair_check.py`
- Source: `u246.json`, row `S13_pair_cli_per_element`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_comprehension_sets.py`, `tests/test_sync_pair_discover.py`
- Collected: 79 against a baseline of 79
- Kills: 1 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`

Old text:

```
                        if pair.account_id not in made_here
```

New text:

```
                        if pair.account_id not in set(ours.values())
```

### `u198.D10_twins`

pair_discover: a twins folder is walked

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D10_twins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_cratekits_own_trees_and_the_favorites_folder_are_never_discovered`

Old text:

```
        if _attribute(top) == FOLDER and TWIN_FOLDER.fullmatch(top_name):
```

New text:

```
        if False:
```

### `u198.D11_two_homes`

pair_discover: two favourites playlists read as one home, hidden

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D11_two_homes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_two_favourites_playlists_leave_both_folders_out_and_say_so`

Old text:

```
        if len(named) > 1
```

New text:

```
        if len(named) > 2
```

### `u198.D2_favorites_home`

pair_discover: the one favourites home is walked like any folder

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D2_favorites_home`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_favourites_name_inside_another_apps_folder_does_not_unsettle_the_home`
  - `tests/test_sync_pair_discover.py::test_a_favourites_playlist_at_the_root_is_not_discovered`
  - `tests/test_sync_pair_discover.py::test_cratekits_own_trees_and_the_favorites_folder_are_never_discovered`

Old text:

```
            if not unsure:
                return
```

New text:

```
            if False:
                return
```

### `u198.D3_held`

pair_discover: a playlist a pair holds is found again

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D3_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_paired_playlist_is_not_listed_on_a_later_run`

Old text:

```
        if node_id in held:
            return
```

New text:

```
        if False:
            return
```

### `u198.D4_skip`

pair_discover: a playlist under a skipped folder is found

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D4_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_an_archive_playlist_is_listed_and_never_written`
  - `tests/test_sync_pair_discover.py::test_the_skip_list_is_the_configurations`
  - `tests/test_sync_pair_discover.py::test_two_favourites_playlists_leave_both_folders_out_and_say_so`

Old text:

```
        if skip_why:
```

New text:

```
        if False:
```

### `u198.D5_smart`

pair_discover: a smart playlist is found as a plain one

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D5_smart`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_smart_playlist_is_listed_not_paired`

Old text:

```
        if attribute != PLAIN:
```

New text:

```
        if False:
```

### `u198.D6_released`

pair_discover: a released playlist is found again

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D6_released`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_on_the_account_unpairs_stays_and_is_not_made_again`

Old text:

```
        if node_id in gone:
```

New text:

```
        if False:
```

### `u198.D7_twice`

pair_discover: two playlists of one title are both found

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D7_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_two_playlists_taking_one_title_refuse_that_title_only`

Old text:

```
        if counted[one.title] > 1:
```

New text:

```
        if counted[one.title] > 2:
```

### `u198.D8_top_names`

pair_discover: a top folder the taxonomy names is walked

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D8_top_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_cratekits_own_trees_and_the_favorites_folder_are_never_discovered`

Old text:

```
        if top_id in roots or top_name in names or top_id in foreign:
```

New text:

```
        if top_id in roots or top_id in foreign:
```

### `u198.D9_foreign`

pair_discover: another app's top folder is walked

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D9_foreign`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_favourites_name_inside_another_apps_folder_does_not_unsettle_the_home`
  - `tests/test_sync_pair_discover.py::test_another_apps_top_folder_is_never_discovered`

Old text:

```
        if top_id in roots or top_name in names or top_id in foreign:
```

New text:

```
        if top_id in roots or top_name in names:
```

### `u202.D1_skip`

home_of: a folder the skip list names is made in

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D1_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_home_of_refuses_each_place_it_cannot_decide`

Old text:

```
        if folder in set(str(one) for one in skip):
```

New text:

```
        if False:
```

### `u202.D2_two_tops`

home_of: two top folders of the name, the first is taken

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D2_two_tops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_home_of_refuses_each_place_it_cannot_decide`

Old text:

```
        if len(top) > 1:
```

New text:

```
        if len(top) > 2:
```

### `u202.D3_longest`

home_of: the shortest subfolder name is read first

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D3_longest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_home_of_reads_the_longest_subfolder_and_strips_the_prefix`

Old text:

```
            longest = max(len(named(row)) for row in fits)
```

New text:

```
            longest = min(len(named(row)) for row in fits)
```

### `u202.D5_name_taken`

home_of: a name the folder already holds is made again beside it

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D5_name_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_playlist_of_the_name_no_pair_holds_is_left_and_named`

Old text:

```
    if here:
        where = " / ".join(path) or "the rekordbox root"
```

New text:

```
    if False:
        where = " / ".join(path) or "the rekordbox root"
```

### `u202.D6_favourites`

home_of: the folder holding the favourites is made in

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D6_favourites`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_home_of_refuses_the_folder_holding_the_favourites`

Old text:

```
            _attribute(row) == PLAIN
            and named(row) == favorites
            and str(getattr(row, "ParentID", "") or "") in above
```

New text:

```
            False
```

### `u216.M11_paired_raw`

downloaded_copy: compare the paired title as it stands, its folder prefix kept

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M11_paired_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_in_a_created_folder_is_named_a_copy`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_downloaded_copy_names_the_paired_title_it_copies`

Old text:

```
        if name_of(folder, one).casefold() == wanted:
```

New text:

```
        if one.casefold() == wanted:
```

### `u216.M12_empty_rest`

downloaded_copy: a title with nothing left after the prefix copies a playlist titled as the folder alone

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M12_empty_rest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_downloaded_copy_names_the_paired_title_it_copies`

Old text:

```
    if not wanted:
        return ""
    for one in sorted
```

New text:

```
    for one in sorted
```

### `u216.M1_held_record_ignored`

before_adoption: a playlist the record says the folder held reads as new, so it is made in rekordbox

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M1_held_record_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_before_adoption_reads_the_record_first`

Old text:

```
        if account_id in held:
            return (
```

New text:

```
        if False:
            return (
```

### `u216.M2_created_folder_by_time`

before_adoption: drop the created folder answer, so an unrecorded created folder is read by time and its new playlists named

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M2_created_folder_by_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_created_folder_without_a_record_still_brings_in`
  - `tests/test_sync_pair_adopted.py::test_before_adoption_reads_the_record_first`

Old text:

```
    if created:
        return ""
    unrecorded = (
```

New text:

```
    unrecorded = (
```

### `u216.M3_no_moment_reads_new`

before_adoption: an unrecorded folder with no made pair to date it reads every playlist as new

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M3_no_moment_reads_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`

Old text:

```
    if adopted is None:
        return (
```

New text:

```
    if adopted is None:
        return "" if True else (
```

### `u216.M4_no_time_reads_new`

before_adoption: a playlist with no creation time in an unrecorded folder reads as new

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M4_no_time_reads_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_a_creation_time_without_a_zone_is_no_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_or_a_creation_time_every_unpaired_playlist_is_named`

Old text:

```
    if made is None or made.tzinfo is None:
        return (
```

New text:

```
    if made is None or made.tzinfo is None:
        return "" if True else (
```

### `u216.M5_naive_time_trusted`

before_adoption: a creation time without a zone is compared as given

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M5_naive_time_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_a_creation_time_without_a_zone_is_no_time`

Old text:

```
    if made is None or made.tzinfo is None:
```

New text:

```
    if made is None:
```

### `u216.M6_equal_moment_new`

before_adoption: a playlist made at the adoption moment itself reads as new

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M6_equal_moment_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`

Old text:

```
    if made <= adopted:
```

New text:

```
    if made < adopted:
```

### `u216.M7_time_rule_off`

before_adoption: an unrecorded folder's playlist with a time never reads as held

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M7_time_rule_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_creation_time_decides`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_moment_is_read_from_this_folders_own_pairs`

Old text:

```
    if made <= adopted:
```

New text:

```
    if False:
```

### `u216.M8_moment_latest`

adoption_moment: the latest mark rather than the earliest, so a playlist made between two marks reads as held before

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M8_moment_latest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_the_adoption_moment_is_the_earliest_readable_mark`

Old text:

```
    return min(found) if found else None
```

New text:

```
    return max(found) if found else None
```

### `u216.M9_moment_naive_kept`

adoption_moment: keep a mark without a zone, which cannot be compared with the account's times

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M9_moment_naive_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_the_adoption_moment_is_the_earliest_readable_mark`

Old text:

```
        if moment.tzinfo is not None:
            found.append(moment)
```

New text:

```
        found.append(moment)
```

### `u242.M25_copy_needs_the_prefix`

pair discovery: read a copy only by its prefix, so a stripped copy is made in rekordbox again

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u242.json`, row `M25_copy_needs_the_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_pair_adopted.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_pairing_techno_with_a_stripped_former_downloaded_techno`

Old text:

```
    if not prefixed and not taken:
```

New text:

```
    if not prefixed:
```

### `u242.M27_copy_pool_reads_no_taken`

pair discovery: a taken title with no prefix reads every taken playlist beside it, so two of one name are each the other's copy

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u242.json`, row `M27_copy_pool_reads_no_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_pair_adopted.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_prefixed_copy_beside_a_taken_original_is_still_its_copy`

Old text:

```
        if other_id != account_id and not (plain_taken and other_id in held)
```

New text:

```
        if other_id != account_id
```

### `r1404.M1_disagreeing_base_ignored`

merge: a base whose two sides disagree on order no longer lets rekordbox lead, the defect R-1404 names

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M1_disagreeing_base_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_track_the_account_adds_is_placed_in_the_order_rekordbox_holds`
  - `tests/test_sync_pair_merge.py::test_only_the_tracks_both_sides_held_at_the_base_are_read_for_their_order`
  - `tests/test_sync_pair_merge.py::test_with_no_change_since_a_base_whose_sides_disagree_rekordbox_leads`

Old text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, base.account
        ):
```

New text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or False:
```

### `r1404.M2_rekordbox_move_ignored`

merge: rekordbox's own reorder since the base no longer leads, only a disagreeing base does

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M2_rekordbox_move_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_whole_sync_after_a_skipped_one_finishes_both_sides_from_the_old_base`
  - `tests/test_sync_pair.py::test_when_rekordbox_alone_reorders_the_account_follows`
  - `tests/test_sync_pair_merge.py::test_when_rekordbox_alone_reordered_its_order_wins`

Old text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, base.account
        ):
```

New text:

```
        if False or order_changed(
            base.rekordbox, base.account
        ):
```

### `r1404.M3_account_move_not_guarded`

merge: rekordbox leads over a disagreeing base even when the account changed order since it, so an account reorder no longer reaches rekordbox

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M3_account_move_not_guarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_when_both_sides_reorder_the_account_order_wins`
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_a_base_whose_sides_disagree_still_leads`
  - `tests/test_sync_pair_merge.py::test_the_stopped_writes_order_is_not_read_against_the_base`
  - `tests/test_sync_pair_merge.py::test_when_both_sides_reordered_the_account_order_wins`

Old text:

```
    elif base is not None and not order_changed(account.keys, base.account):
```

New text:

```
    elif base is not None:
```

### `r1404.M4_always_rekordbox`

merge: with neither side changed, rekordbox leads whatever the base, so a base whose sides agree takes the other tie between two additions

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M4_always_rekordbox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_base_whose_sides_agree_leaves_the_account_leading_when_neither_side_moved`
  - `tests/test_sync_pair_merge.py::test_only_the_tracks_both_sides_held_at_the_base_are_read_for_their_order`
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_against_the_account_s_base_not_the_account_now`
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_at_the_base_not_between_the_sides_now`

Old text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, base.account
        ):
```

New text:

```
        if True:
```

### `r1404.M5_disagreement_read_now`

merge: the disagreement is read between the sides as they stand now rather than at the base

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M5_disagreement_read_now`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_against_the_account_s_base_not_the_account_now`
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_at_the_base_not_between_the_sides_now`

Old text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, base.account
        ):
```

New text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            rekordbox.keys, account.keys
        ):
```

### `r1404.M6_disagreement_read_against_the_account_now`

merge: the base's rekordbox order is compared with the account as it stands, not the account's base

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M6_disagreement_read_against_the_account_now`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_against_the_account_s_base_not_the_account_now`

Old text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, base.account
        ):
```

New text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, account.keys
        ):
```

### `r1404.S1_default_leader`

sample: the account no longer leads by default, so a first sync and a both reordered pair take rekordbox's order

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `S1_default_leader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_when_both_sides_reorder_the_account_order_wins`
  - `tests/test_sync_pair_merge.py::test_a_base_is_read_as_before_whatever_the_order`
  - `tests/test_sync_pair_merge.py::test_a_base_whose_sides_agree_leaves_the_account_leading_when_neither_side_moved`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_reads_its_order_against_it_whatever_the_order`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_into_an_empty_rekordbox_side_is_led_by_the_account_whatever_the_order`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_whose_order_is_kept_leads_with_the_account`
  - `tests/test_sync_pair_merge.py::test_only_the_tracks_both_sides_held_at_the_base_are_read_for_their_order`
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_a_base_whose_sides_disagree_still_leads`
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_the_stopped_write_leads_whatever_else_moved`
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_against_the_account_s_base_not_the_account_now`
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_at_the_base_not_between_the_sides_now`
  - `tests/test_sync_pair_merge.py::test_the_stopped_writes_order_is_not_read_against_the_base`
  - `tests/test_sync_pair_merge.py::test_when_both_sides_reordered_the_account_order_wins`
  - `tests/test_sync_pair_merge.py::test_when_the_account_alone_reordered_its_order_wins`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    leader = ACCOUNT
    if stopped is not None:
```

New text:

```
    leader = REKORDBOX
    if stopped is not None:
```

### `r1404.S2_stopped_leader_again`

sample, U225: with no change since a stopped write, the side that led it no longer leads again

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `S2_stopped_leader_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_the_stopped_writes_order_is_not_read_against_the_base`
  - `tests/test_sync_pair_merge.py::test_with_no_change_since_the_stopped_write_the_side_that_led_it_leads_again`

Old text:

```
        elif not account_moved and stopped.leader == REKORDBOX:
```

New text:

```
        elif False:
```

### `r1416.M1_rekordbox_does_not_lead`

merge: a first sync whose account order is not kept is led by the account again, the defect R-1416 names

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `M1_rekordbox_does_not_lead`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_led_by_rekordbox_places_the_accounts_tracks_after_their_neighbours`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_whose_order_is_not_kept_leads_with_rekordbox`

Old text:

```
        # order rekordbox stands in, or the DJ's arrangement is lost for good.
        leader = REKORDBOX
```

New text:

```
        # order rekordbox stands in, or the DJ's arrangement is lost for good.
        leader = ACCOUNT
```

### `r1416.M2_order_kept_ignored`

merge: the flag is ignored, so a first sync under GIG READY or with every pair's order kept is led by rekordbox

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `M2_order_kept_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_whose_order_is_kept_leads_with_the_account`

Old text:

```
    elif base is None and not order_kept and rekordbox.keys:
```

New text:

```
    elif base is None and rekordbox.keys:
```

### `r1416.M3_empty_rekordbox_leads`

merge: an empty rekordbox side leads its first sync, so the gate says the order follows rekordbox's where it takes the account's

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `M3_empty_rekordbox_leads`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_into_an_empty_rekordbox_side_is_led_by_the_account_whatever_the_order`

Old text:

```
    elif base is None and not order_kept and rekordbox.keys:
```

New text:

```
    elif base is None and not order_kept:
```

### `r1416.M4_first_sync_unguarded`

merge: a pair whose order is not kept is led by rekordbox whatever its base, so an account reorder after the first sync no longer reaches rekordbox

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `M4_first_sync_unguarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_base_is_read_as_before_whatever_the_order`

Old text:

```
    elif base is None and not order_kept and rekordbox.keys:
```

New text:

```
    elif not order_kept and rekordbox.keys:
```

### `r1416.M5_stopped_write_yields`

merge: outside the scope a stopped write no longer decides the order, so the new first sync rule takes its place

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `M5_stopped_write_yields`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_reads_its_order_against_it_whatever_the_order`

Old text:

```
    if stopped is not None:
        # U225.
```

New text:

```
    if stopped is not None and order_kept:
        # U225.
```

### `r1416.M6_default_not_kept`

merge: the keyword's default reads the order as not kept, so a caller that says nothing is led by rekordbox on a first sync

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `M6_default_not_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_whose_order_is_kept_leads_with_the_account`

Old text:

```
    order_kept: bool = True,
```

New text:

```
    order_kept: bool = False,
```

### `r1416.S2_placed_after_neighbour`

sample, U130: a track only the following side holds goes to the start rather than after its neighbour

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `S2_placed_after_neighbour`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 22 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_short_account_listing_reads_nothing_as_removed`
  - `tests/test_sync_pair.py::test_a_skipped_account_side_is_finished_by_the_next_sync`
  - `tests/test_sync_pair.py::test_a_track_added_in_rekordbox_only_lands_on_the_account`
  - `tests/test_sync_pair.py::test_an_unmatched_rekordbox_track_is_named_and_stays_in_rekordbox`
  - `tests/test_sync_pair.py::test_the_first_sync_marks_the_pair_and_adds_only`
  - `tests/test_sync_pair_back.py::test_a_removal_rekordbox_kept_no_moment_for_keeps_the_track_and_names_the_call`
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_hold.py::test_a_held_plan_other_than_the_offer_is_planned_again`
  - `tests/test_sync_pair_hold.py::test_a_no_change_sync_of_a_linked_pair_makes_no_isrc_lookup`
  - `tests/test_sync_pair_hold.py::test_a_two_gate_sync_makes_one_plans_lookups`
  - `tests/test_sync_pair_hold.py::test_an_unreadable_held_plan_is_planned_again_and_says_why`
  - `tests/test_sync_pair_hold.py::test_answers_continued_in_later_commands_ask_nothing_when_nothing_moved`
  - `tests/test_sync_pair_merge.py::test_a_base_whose_sides_agree_leaves_the_account_leading_when_neither_side_moved`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_reads_its_order_against_it_whatever_the_order`
  - ... and 7 more, see the JSON sidecar

Old text:

```
        anchor += 1
        result.insert(anchor, key)
```

New text:

```
        result.insert(0, key)
```

### `u130-a.A5_new_tracks_appended`

A track only the other side holds goes to the end instead of after its predecessor

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u130-a.json`, row `A5_new_tracks_appended`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair.py`
- Collected: 126 against a baseline of 126
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_base_whose_sides_agree_leaves_the_account_leading_when_neither_side_moved`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_reads_its_order_against_it_whatever_the_order`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_led_by_rekordbox_places_the_accounts_tracks_after_their_neighbours`
  - `tests/test_sync_pair_merge.py::test_a_run_of_new_tracks_at_the_head_of_the_other_side_keeps_its_own_order`
  - `tests/test_sync_pair_merge.py::test_a_track_added_mid_list_on_the_other_side_keeps_its_place`
  - `tests/test_sync_pair_merge.py::test_a_track_the_account_adds_is_placed_in_the_order_rekordbox_holds`
  - `tests/test_sync_pair_merge.py::test_an_addition_is_kept_when_the_other_side_dropped_its_neighbour`

Old text:

```
        anchor += 1
        result.insert(anchor, key)
```

New text:

```
        result.append(key)
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

### `u202.M2_naive`

pair_merge.merge: a moment with no zone is read as a known moment

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M2_naive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_moment_with_no_zone_is_no_moment`

Old text:

```
        if not isinstance(at, datetime) or at.tzinfo is None:
```

New text:

```
        if not isinstance(at, datetime):
```

### `u202.M3_tie`

Call.outcome: a tie goes to the removal, so a track is lost on equal moments

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M3_tie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_tie_keeps_the_track`

Old text:

```
        return REMOVAL_LATER if self.removed_at > self.added_at else ADDITION_LATER
```

New text:

```
        return REMOVAL_LATER if self.removed_at >= self.added_at else ADDITION_LATER
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

### `u225.M1_stopped_ignored`

merge: a stopped write handed in is ignored and the order is read against the base

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u225.json`, row `M1_stopped_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 149 against a baseline of 149
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_reads_its_order_against_it_whatever_the_order`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_rekordbox_reordered_since_the_stopped_write_leads`
  - `tests/test_sync_pair_merge.py::test_the_stopped_writes_order_is_not_read_against_the_base`
  - `tests/test_sync_pair_merge.py::test_with_no_change_since_the_stopped_write_the_side_that_led_it_leads_again`

Old text:

```
    if stopped is not None:
        # U225.
```

New text:

```
    if False:
        # U225.
```

### `u225.M2_rekordbox_since_dropped`

merge: rekordbox reordered since the stopped write does not lead

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u225.json`, row `M2_rekordbox_since_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 149 against a baseline of 149
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_rekordbox_reordered_since_the_stopped_write_leads`

Old text:

```
        if order_changed(rekordbox.keys, stopped.rekordbox) and not account_moved:
```

New text:

```
        if False and not account_moved:
```

### `u225.M3_rekordbox_over_account`

merge: rekordbox reordered since leads even when the account was reordered since

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u225.json`, row `M3_rekordbox_over_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_the_stopped_write_leads_whatever_else_moved`

Old text:

```
        if order_changed(rekordbox.keys, stopped.rekordbox) and not account_moved:
```

New text:

```
        if order_changed(rekordbox.keys, stopped.rekordbox):
```

### `u225.M5_leader_over_account`

merge: the stopped write's leader leads even when the account was reordered since

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u225.json`, row `M5_leader_over_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_the_stopped_write_leads_whatever_else_moved`

Old text:

```
        elif not account_moved and stopped.leader == REKORDBOX:
```

New text:

```
        elif stopped.leader == REKORDBOX:
```

### `u234.S2_sample_stopped_leader`

sample, U225: the side that led the stopped write is not followed, so the account leads a finish

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u234.json`, row `S2_sample_stopped_leader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_twins_hold.py`
- Collected: 313 against a baseline of 313
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_the_stopped_writes_order_is_not_read_against_the_base`
  - `tests/test_sync_pair_merge.py::test_with_no_change_since_the_stopped_write_the_side_that_led_it_leads_again`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`

Old text:

```
        elif not account_moved and stopped.leader == REKORDBOX:
```

New text:

```
        elif False and not account_moved and stopped.leader == REKORDBOX:
```

### `u202-composites.R2_confined`

pair_reverse.create: the twins' confinement check is not run before the commit

- File: `src/cratekit/sync/pair_reverse.py`
- Source: `u202-composites.json`, row `R2_confined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_write_outside_the_playlist_made_is_refused_with_nothing_written`

Old text:

```
                twins.assert_confined(
                    db,
```

New text:

```
                (lambda *a, **k: None)(
                    db,
```

### `u202.R1_recheck_name`

pair_reverse.recheck: a name taken since the plan is made again

- File: `src/cratekit/sync/pair_reverse.py`
- Source: `u202.json`, row `R1_recheck_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_the_write_refuses_a_name_taken_since_the_plan`

Old text:

```
    if taken:
        raise _stale(
```

New text:

```
    if False:
        raise _stale(
```

### `u202.W1_landed_then_raised`

pair_reverse.create: a commit that lands and then raises no longer tells the caller, so the playlist made stays unpaired (the second review's BLOCKING finding)

- File: `src/cratekit/sync/pair_reverse.py`
- Source: `u202.json`, row `W1_landed_then_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_commit_that_lands_and_then_raises_still_pairs_the_playlist`

Old text:

```
                    if on_commit is not None and playlist_id:
                        on_commit(playlist_id)
                raise
```

New text:

```
                raise
```

### `r1372.K19_passed_by_strict`

passed_by: a write that began at the snapshot's very moment is not passed

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K19_passed_by_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
            if began is not None and not began > moment:
```

New text:

```
            if began is not None and began < moment:
```

### `r1372.K20_passed_by_any_pair`

passed_by: a snapshot lets go of every pair's carried records, not its own

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K20_passed_by_any_pair`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
            if _account_of(key, steps, new=new, made=made) != account_id:
                continue
            began = placeholders.parse_hearted(steps.get(account))
            if began is not None
```

New text:

```
            began = placeholders.parse_hearted(steps.get(account))
            if began is not None
```

### `r1372.K21_made_pair_unmapped`

_account_of: a made pair is read under its key, not the account playlist it was made as

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K21_made_pair_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_made_pair_is_read_under_the_account_playlist_it_was_made_as`
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
    if key.startswith(new):
        return steps.get(made) if isinstance(steps.get(made), str) else ""
    return key
```

New text:

```
    return key
```

### `r1376.F14_finished_filter_gone`

stopped_writes (sample, U225): a stop a later run finished is still read, by a first sync among others

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1376.json`, row `F14_finished_filter_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_later_run_that_finished_the_pair_hides_the_stopped_write_in_either_order`

Old text:

```
        if account_id not in finished or not finished[account_id] > began
```

New text:

```
        if True
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

### `r1394.S1_counts_beyond_the_moves_trusted`

stopped write: counts larger than the write's moves are trusted rather than read as nothing known

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S1_counts_beyond_the_moves_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`

Old text:

```
    if sent is None or landed is None or not landed <= sent <= total:
```

New text:

```
    if sent is None or landed is None or not landed <= sent:
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

### `r1434.S2_positions_compare_every_track_listed`

existing guard, U225: the path compares every track listed now, a track added since included, so an addition reads the account off the path

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1434.json`, row `S2_positions_compare_every_track_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_since_is_left_out_of_the_comparison`
  - `tests/test_sync_pair_stopped.py::test_positions_counts_the_moves_that_leave_each_order_on_the_path`

Old text:

```
    common = set(current) & set(start)
```

New text:

```
    common = set(current)
```

### `u225.M6_front_keeps_nothing`

front_moves: no tail is kept, every asked track is moved

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M6_front_keeps_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`

Old text:

```
            keep += 1
    return list(reversed(wanted[: len(wanted) - keep]))
```

New text:

```
            keep += 0
    return list(reversed(wanted[: len(wanted) - keep]))
```

### `u225.M8_reached_strict_membership`

reached: a track added or taken off since is compared too

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M8_reached_strict_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_since_is_left_out_of_the_comparison`
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`
  - `tests/test_sync_pair_stopped.py::test_positions_counts_the_moves_that_leave_each_order_on_the_path`

Old text:

```
    common = set(current) & set(start)
```

New text:

```
    common = set(current) | set(start)
```

### `u225.M9_finish_ignored`

stopped_writes: a later run that finished the pair does not hide the stopped write

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M9_finish_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_finished_or_unordered_write_is_no_stopped_one`
  - `tests/test_sync_pair_stopped.py::test_a_later_run_that_finished_the_pair_hides_the_stopped_write_in_either_order`

Old text:

```
            if done in steps:
                if account_id not in finished
```

New text:

```
            if False:
                if account_id not in finished
```

### `u234.O15_reordered_counts_additions`

reordered compares the readings whole, so a track added between them is read as a reorder

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u234.json`, row `O15_reordered_counts_additions`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_between_two_readings_is_no_reorder`

Old text:

```
    return [one for one in current if one in common] != [
        one for one in dict.fromkeys(kept) if one in common
    ]


__all__
```

New text:

```
    return current != list(dict.fromkeys(kept))


__all__
```

### `r1289.M1_sweep_reads_whole`

plan: read each swept playlist whole again (the declared reader is asked first), so one untitled row leaves the whole playlist out as unreadable

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M1_sweep_reads_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_playlist_with_no_tracks_queues_nothing_and_is_reported`
  - `tests/test_sync_all.py::test_a_queued_playlist_that_left_a_track_unread_is_recorded_when_its_job_succeeds`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
            listing = intake_cli.list_playlist_readable(found, playlist.playlist_id)
```

New text:

```
            intake_cli.list_playlist_declared(found, playlist.playlist_id)
            listing = intake_cli.list_playlist_readable(found, playlist.playlist_id)
```

### `r1289.M2_unread_not_kept`

plan: keep no unread track on the sweep, so the summary names none and a playlist with every track unread reads as empty

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M2_unread_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_whose_only_playlist_left_every_track_unread_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
        if listing.unread:
```

New text:

```
        if False:
```

### `r1289.M3_all_unread_branch`

plan: drop the every track unread branch, so such a playlist is excluded as empty rather than unreadable

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M3_all_unread_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_whose_only_playlist_left_every_track_unread_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`

Old text:

```
            if not tracks:
                # EVERY TRACK UNREAD
```

New text:

```
            if False:
                # EVERY TRACK UNREAD
```

### `r1289.M4_unread_why_dropped`

plan: record an unread track without the reader's why

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M4_unread_why_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_queued_playlist_that_left_a_track_unread_is_recorded_when_its_job_succeeds`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
                ref: {**one.said(), "why": one.why} for ref, one in listing.unread.items()
```

New text:

```
                ref: {**one.said()} for ref, one in listing.unread.items()
```

### `r1289.M5_all_unread_message`

plan: the every track unread playlist's unreadable message reworded so it names no track

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M5_all_unread_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`

Old text:

```
                    "no track on it could be queued: "
                    + ", ".join(f"{ref} ({one.why})" for ref, one in listing.unread.items())
```

New text:

```
                    "the playlist could not be read"
```

### `r1289.M6_report_unread_emptied`

report: the unread block names each playlist with no tracks under it

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M6_report_unread_emptied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
            identity: {"name": names.get(identity, ""), "tracks": dict(tracks)}
```

New text:

```
            identity: {"name": names.get(identity, ""), "tracks": {}}
```

### `r1289.M7_per_playlist_reraise`

plan (existing guard, sample): take any refusal as one playlist's, so an expired session reads as one unreadable playlist and the sweep goes on

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M7_per_playlist_reraise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_refusal_not_about_one_playlist_still_stops_the_sweep`

Old text:

```
            if exc.cause.reason not in PER_PLAYLIST_REASONS:
                raise
            sweep.excluded[playlist.playlist_id] = Excluded.UNREADABLE
```

New text:

```
            if False:
                raise
            sweep.excluded[playlist.playlist_id] = Excluded.UNREADABLE
```

### `r1289.M8_per_playlist_set`

PER_PLAYLIST_REASONS (existing guard, sample): drop the reader's refusal, so a row with no provider id stops the whole sweep

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M8_per_playlist_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_row_with_no_provider_id_still_leaves_its_playlist_out_by_name`

Old text:

```
PER_PLAYLIST_REASONS = frozenset({"label-playlist-unreadable", "intake-list-unusable"})
```

New text:

```
PER_PLAYLIST_REASONS = frozenset({"label-playlist-unreadable"})
```

### `r1289.M9_short_check`

plan (existing guard, sample): drop the declared count check, so a short listing is queued without saying what the provider withheld

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M9_short_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
        if listing.short is not None:
```

New text:

```
        if False:
```

### `r358.S10_mark_always_unbound`

Report the mark unbound whether or not the step ran

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S10_mark_always_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_block_tells_a_mark_that_ran_apart_from_a_mark_that_never_ran`

Old text:

```
        "mark": MARK_UNBOUND if marked is None else MARK_APPLIED,
```

New text:

```
        "mark": MARK_UNBOUND,
```

### `r358.S1_set_is_the_cursor`

Take the mark set from recorded_now again, the review's finding 1

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S1_set_is_the_cursor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_that_did_not_land_is_offered_again_by_the_next_pass`
  - `tests/test_sync_all.py::test_a_recorded_debris_playlist_is_not_pending_at_all`

Old text:

```
        for identity in sorted(sweep.recorded)
```

New text:

```
        for identity in sorted(sweep.recorded_now)
```

### `r358.S5_recheck_is_a_second_read`

Serve the recheck from the plan's own listing instead of a fresh read

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S5_recheck_is_a_second_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_after_a_real_importable_file_takes_the_recorded_playlist`
  - `tests/test_sync_all.py::test_a_playlist_gone_from_the_account_since_the_plan_is_not_marked`
  - `tests/test_sync_all.py::test_a_playlist_renamed_on_the_account_since_the_plan_is_left_alone`

Old text:

```
        name = listed.get(mark.target_id) or ""
        return bool(name) and current().get(mark.target_id) == name
```

New text:

```
        name = listed.get(mark.target_id) or ""
        return bool(name) and listed.get(mark.target_id) == name
```

### `r358.S7_lazy_listing`

Read the account eagerly, so a call with no file still spends a listing

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S7_lazy_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_without_a_real_importable_file_renames_nothing`

Old text:

```
    held: list[dict[str, str]] = []

    def current() -> dict[str, str]:
```

New text:

```
    held: list[dict[str, str]] = [
        {playlist.playlist_id: playlist.name for playlist in _listed_or_refuse(found)}
    ]

    def current() -> dict[str, str]:
```

### `r358.S9_mark_always_applied`

Report the mark applied whether or not the step ran

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S9_mark_always_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_renames_nothing_even_over_a_recorded_playlist_with_its_file_landed`
  - `tests/test_sync_all.py::test_a_slim_pass_queues_each_new_account_playlist_under_the_shared_run`
  - `tests/test_sync_all.py::test_the_block_tells_a_mark_that_ran_apart_from_a_mark_that_never_ran`
  - `tests/test_sync_all.py::test_the_current_intake_path_marks_nothing_and_still_reports_unbound`

Old text:

```
        "mark": MARK_UNBOUND if marked is None else MARK_APPLIED,
```

New text:

```
        "mark": MARK_APPLIED,
```

### `r359.M10_claims_downloaded`

Reword the sentence into the false claim the defect is about, that the files were downloaded

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M10_claims_downloaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
            "the library, crate intake missing lists it, and no later sync offers "
```

New text:

```
            "the library until downloaded, and no later sync offers "
```

### `r359.M1_drop_field`

Drop the swept_means field from the playlists block, the row the brief names

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M1_drop_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_json_its_tracks_were_resolved_not_acquired`
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
        "swept_means": SWEPT_MEANS,

```

New text:

```
(empty)
```

### `r359.M2_token`

Change the machine token to a nearby word that no longer says not acquired

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M2_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_json_its_tracks_were_resolved_not_acquired`
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
SWEPT_MEANS = "resolved-not-acquired"
```

New text:

```
SWEPT_MEANS = "resolved"
```

### `r359.M3_said_silent`

said returns nothing, so the check carries no sentence while the json field stays

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M3_said_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
    return SWEPT_MEANS_SAID.get(str(block.get("swept_means") or ""))
```

New text:

```
    return None
```

### `r359.M4_said_unconditional`

said answers whatever the block carries, decoupling the sentence from the field

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M4_said_unconditional`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
    return SWEPT_MEANS_SAID.get(str(block.get("swept_means") or ""))
```

New text:

```
    return SWEPT_MEANS_SAID[SWEPT_MEANS]
```

### `r359.M8_drop_resolved`

Reword the sentence so it no longer says the tracks were resolved

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M8_drop_resolved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
            "a recorded playlist had its tracks resolved against the library, not "
```

New text:

```
            "a recorded playlist had its tracks checked against the library, not "
```

### `r359.M9_drop_not_acquired`

Reword the sentence so it no longer says the tracks were not acquired

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M9_drop_not_acquired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
            "acquired, so a track its intake job reported missing is still not in "
```

New text:

```
            "fetched, so a track its intake job reported missing is still not in "
```

### `r359.S1_record_on_any_state`

Existing guard sample: the cursor records a playlist whatever state its job ended in

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `S1_record_on_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_failed_job_is_not_recorded_and_its_playlist_is_offered_again`
  - `tests/test_sync_all.py::test_a_playlist_intake_by_hand_that_did_not_succeed_is_not_recorded[cancelled]`
  - `tests/test_sync_all.py::test_a_playlist_intake_by_hand_that_did_not_succeed_is_not_recorded[failed]`
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`
  - `tests/test_sync_all.py::test_the_cursor_records_ids_only_once_a_job_succeeds`

Old text:

```
        if job.state == jobs.JobState.SUCCEEDED and identity and identity not in seen:
```

New text:

```
        if identity and identity not in seen:
```

### `r361-a.A10_enum_value_respelled`

The enum member's kebab value changes, so the report and the check say another word

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A10_enum_value_respelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`
  - `tests/test_sync_all.py::test_a_pass_that_finds_only_debris_says_so_on_the_check`
  - `tests/test_sync_all.py::test_the_label_batch_debris_is_not_queued_as_intake`
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
    LABEL_DEBRIS = "label-debris"
```

New text:

```
    LABEL_DEBRIS = "label-library"
```

### `r361-a.A2_case_insensitive`

The rule widens to any case, so a person's Colorize Library is excluded too

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A2_case_insensitive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`
  - `tests/test_sync_all.py::test_a_recorded_debris_playlist_is_not_pending_at_all`
  - `tests/test_sync_all.py::test_the_label_batch_debris_is_not_queued_as_intake`

Old text:

```
    return str(name or "").endswith(LIBRARY_PLAYLIST_SUFFIX)
```

New text:

```
    return str(name or "").upper().endswith(LIBRARY_PLAYLIST_SUFFIX)
```

### `r361-a.A3_no_leading_space`

The suffix loses its leading space, so ColorizeLIBRARY is debris

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A3_no_leading_space`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`

Old text:

```
LIBRARY_PLAYLIST_SUFFIX = " LIBRARY"
```

New text:

```
LIBRARY_PLAYLIST_SUFFIX = "LIBRARY"
```

### `r361-a.A4_substring_not_suffix`

endswith becomes in, so LIBRARY Colorize and Colorize LIBRARY 2 are debris

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A4_substring_not_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`

Old text:

```
    return str(name or "").endswith(LIBRARY_PLAYLIST_SUFFIX)
```

New text:

```
    return LIBRARY_PLAYLIST_SUFFIX in str(name or "")
```

### `r361-a.D2_drop_the_placeholder`

Existing: the favourites placeholder is queued by the playlists source

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `D2_drop_the_placeholder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_playlist_exclusions_in_the_order_a_person_is_told`
  - `tests/test_sync_all.py::test_the_favourites_placeholders_are_left_to_the_favourites_source`

Old text:

```
    if placeholders.is_placeholder(playlist.name):
        return Excluded.PLACEHOLDER

```

New text:

```
(empty)
```

### `r361-a.D3_drop_in_flight`

Existing: an open job no longer holds its playlist back, so it is queued twice

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `D3_drop_in_flight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_playlist_exclusions_in_the_order_a_person_is_told`
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`
  - `tests/test_sync_all.py::test_the_cursor_records_ids_only_once_a_job_succeeds`

Old text:

```
    if playlist.playlist_id in in_flight:
        return Excluded.IN_FLIGHT

```

New text:

```
(empty)
```

### `r382.M11_reconcile_source_jobs`

reconcile reads source_jobs again instead of playlist_jobs

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M11_reconcile_source_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_ingested_by_hand_is_recorded_on_the_next_pass`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://listen.tidal.com/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1?u]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://tidal.com/browse/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1]`

Old text:

```
        for identity in completed(playlist_jobs(store, cfg, handler_key=handler_key))
```

New text:

```
        for identity in completed(source_jobs(store, cfg, handler_key=handler_key))
```

### `r382.M12_in_flight_source_jobs`

plan's in flight set reads source_jobs again instead of playlist_jobs

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M12_in_flight_source_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`

Old text:

```
    in_flight = open_playlists(playlist_jobs(store, cfg, handler_key=handler_key))
```

New text:

```
    in_flight = open_playlists(source_jobs(store, cfg, handler_key=handler_key))
```

### `r382.M13_marking_source_jobs`

marking_sweep reads source_jobs again instead of playlist_jobs

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M13_marking_source_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_reads_a_playlist_ingested_by_hand_as_recorded`

Old text:

```
    held.update(completed(playlist_jobs(store, cfg, handler_key=handler_key)))
```

New text:

```
    held.update(completed(source_jobs(store, cfg, handler_key=handler_key)))
```

### `r382.M15_completed_duplicates`

Sample of an existing guard: completed records a playlist once per succeeded job

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M15_completed_duplicates`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_two_succeeded_jobs_for_one_playlist_record_it_once`

Old text:

```
        if job.state == jobs.JobState.SUCCEEDED and identity and identity not in seen:
```

New text:

```
        if job.state == jobs.JobState.SUCCEEDED and identity:
```

### `r382.M1_restore_source_filter`

Restore the source_id == playlists filter on playlist_jobs, the brief's named row: a hand queued job is no longer reconciled or in flight

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M1_restore_source_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_reads_a_playlist_ingested_by_hand_as_recorded`
  - `tests/test_sync_all.py::test_a_playlist_ingested_by_hand_is_recorded_on_the_next_pass`
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://listen.tidal.com/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1?u]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://tidal.com/browse/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1]`

Old text:

```
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
        and (job.payload or {}).get("source_id") == SOURCE_ID
    )
```

### `r382.M2_drop_handler_key`

Drop the handler key filter from playlist_jobs, so an intake.set job naming a playlist is reconciled

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M2_drop_handler_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_set_intake_naming_the_playlist_is_not_a_playlist_intake`

Old text:

```
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        if job.library_id == cfg.library.volume_id
    )
```

### `r382.M3_drop_library`

Drop the library filter from playlist_jobs, so another library's finished job records here

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M3_drop_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_another_librarys_finished_job_is_not_this_librarys_sweep`

Old text:

```
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        if job.handler_key == handler_key
    )
```

### `r382.M4_hearts_recorded`

Drop the reserved hearts reference check in recorded_as, so a hearts job records favorites

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M4_hearts_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_intake_is_not_recorded_as_a_playlist`

Old text:

```
    if intake_cli.is_favorites(reference):
        return ""
```

New text:

```
(empty)
```

### `r382.M5_no_verbatim_for_pass_jobs`

Drop the verbatim return for a pass's own job, so its listing id goes through the lowercasing parser

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M5_no_verbatim_for_pass_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_queued_job_records_the_listing_identifier_verbatim`

Old text:

```
    if (job.payload or {}).get("source_id") == SOURCE_ID:
        return reference

```

New text:

```
(empty)
```

### `r382.M6_no_parse`

Record a hand typed reference verbatim instead of parsing it, so a typed URL is recorded as the URL

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M6_no_parse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://listen.tidal.com/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1?u]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://tidal.com/browse/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1]`

Old text:

```
        return typed_playlist_id(reference)
```

New text:

```
        return reference
```

### `r382.M7_invalid_records_nothing`

An unparseable hand reference records nothing instead of itself

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M7_invalid_records_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_reads_a_playlist_ingested_by_hand_as_recorded`
  - `tests/test_sync_all.py::test_a_playlist_ingested_by_hand_is_recorded_on_the_next_pass`
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`

Old text:

```
    except PlaylistReferenceInvalid:
        return reference
```

New text:

```
    except PlaylistReferenceInvalid:
        return ""
```

### `r382.M8_completed_raw`

completed reads the raw payload reference instead of recorded_as

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M8_completed_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_intake_is_not_recorded_as_a_playlist`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://listen.tidal.com/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1?u]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://tidal.com/browse/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1]`

Old text:

```
        identity = recorded_as(job)
        if job.state == jobs.JobState.SUCCEEDED
```

New text:

```
        identity = _playlist_of(job)
        if job.state == jobs.JobState.SUCCEEDED
```

### `r382.M9_open_raw`

open_playlists reads the raw payload reference instead of recorded_as

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M9_open_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`

Old text:

```
    return frozenset(recorded_as(job) for job in found if job.is_open() and recorded_as(job))
```

New text:

```
    return frozenset(_playlist_of(job) for job in found if job.is_open() and _playlist_of(job))
```

### `r835-b.S1_built_year_excluded_from_sweep`

sync.playlists.exclusion: a year playlist a label build recorded is swept as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `r835-b.json`, row `S1_built_year_excluded_from_sweep`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 271 against a baseline of 271
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_the_sweep_never_reads_a_built_year_playlist_as_intake`

Old text:

```
    if playlist.playlist_id in label_built:
        return Excluded.LABEL_FOLDER
```

New text:

```
    if False:
        return Excluded.LABEL_FOLDER
```

### `r837-a.A16_sweep_excludes_set`

sync.playlists.exclusion: a set playlist export set recorded is swept as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `r837-a.json`, row `A16_sweep_excludes_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_incremental_sync.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 327 against a baseline of 327
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_sweep_never_reads_a_set_playlist_as_intake`

Old text:

```
    if playlist.playlist_id in set_built:
        return Excluded.SET_PLAYLIST
```

New text:

```
    if False:
        return Excluded.SET_PLAYLIST
```

### `u113-a.A6_sweep_passes_no_name`

The sweep queues each playlist job without the account's name

- File: `src/cratekit/sync/playlists.py`
- Source: `u113-a.json`, row `A6_sweep_passes_no_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_sync_all.py`
- Collected: 147 against a baseline of 147
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_sync_all_records_the_name_the_account_listed_on_each_playlist_job`

Old text:

```
                name=names.get(playlist_id),
```

New text:

```
                name=None,
```

### `u130-c.C9_sweep_takes_paired`

The playlists sweep offers a paired playlist as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `u130-c.json`, row `C9_sweep_takes_paired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_the_sweep_excludes_a_paired_playlist`
  - `tests/test_sync_pair.py::test_the_sync_pass_hands_the_pairs_to_the_sweep`

Old text:

```
    if playlist.playlist_id in paired:
```

New text:

```
    if False:
```

### `u147-c.M18_sweep_exclusion`

sync.playlists.exclusion: a mirrored playlist is swept as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `u147-c.json`, row `M18_sweep_exclusion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_the_intake_sweep_leaves_a_mirrored_playlist_alone`

Old text:

```
    if playlist.playlist_id in mirrored:
        return Excluded.MIRROR

```

New text:

```
(empty)
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

### `u242.M2_is_taken_drops_the_id`

is_taken: read the title alone, the ledger ignored by every reader

- File: `src/cratekit/sync/playlists.py`
- Source: `u242.json`, row `M2_is_taken_drops_the_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_organize_root.py`
- Collected: 286 against a baseline of 286
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
- Collected: 386 against a baseline of 386
- Kills: 22 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mark_put_back_is_no_mark_and_the_playlist_stays`
  - `tests/test_organize.py::test_a_prefixed_but_unmarked_playlist_has_its_own_reason`
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
  - ... and 7 more, see the JSON sidecar

Old text:

```
    return str(playlist_id or "") in taken or is_swept_name(name)
```

New text:

```
    return str(playlist_id or "") in taken
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

### `u82-a.A5_only_narrows`

pending_marks: drop the only filter, so every recorded playlist is pending whatever the caller named

- File: `src/cratekit/sync/playlists.py`
- Source: `u82-a.json`, row `A5_only_narrows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_debris_playlist_is_not_pending_at_all`
  - `tests/test_sync_mark.py::test_a_native_pass_takes_playlist_as_the_file_does`
  - `tests/test_sync_mark.py::test_a_native_pass_with_one_track_not_held_leaves_that_playlist_alone`
  - `tests/test_sync_mark.py::test_a_playlist_whose_reports_cannot_be_read_is_left_alone`
  - `tests/test_sync_mark.py::test_a_playlist_with_one_row_not_landed_is_not_marked`
  - `tests/test_sync_mark.py::test_a_track_the_pass_offered_for_review_holds_its_playlist_back`
  - `tests/test_sync_mark.py::test_only_narrows_the_pending_set_and_an_empty_set_is_nothing`
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`
  - `tests/test_sync_mark.py::test_the_pass_is_decided_without_its_manifest`

Old text:

```
        and (only is None or identity in only)
```

New text:

```
(empty)
```

### `u82-a.A6_an_empty_only_is_nothing`

pending_marks: read only by truth and not by None, so an empty set, which is no finished playlist, marks every pending one

- File: `src/cratekit/sync/playlists.py`
- Source: `u82-a.json`, row `A6_an_empty_only_is_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_only_narrows_the_pending_set_and_an_empty_set_is_nothing`

Old text:

```
        and (only is None or identity in only)
```

New text:

```
        and (not only or identity in only)
```

### `u82-a.A7_mark_swept_hands_only_through`

mark_swept: stop handing only to pending_marks, so the verb's finished set is ignored at the one place it is applied

- File: `src/cratekit/sync/playlists.py`
- Source: `u82-a.json`, row `A7_mark_swept_hands_only_through`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_takes_playlist_as_the_file_does`
  - `tests/test_sync_mark.py::test_a_native_pass_with_one_track_not_held_leaves_that_playlist_alone`
  - `tests/test_sync_mark.py::test_a_playlist_whose_reports_cannot_be_read_is_left_alone`
  - `tests/test_sync_mark.py::test_a_playlist_with_one_row_not_landed_is_not_marked`
  - `tests/test_sync_mark.py::test_a_track_the_pass_offered_for_review_holds_its_playlist_back`
  - `tests/test_sync_mark.py::test_only_narrows_the_pending_set_and_an_empty_set_is_nothing`
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`
  - `tests/test_sync_mark.py::test_the_pass_is_decided_without_its_manifest`

Old text:

```
        pending_marks(sweep, only=only),
```

New text:

```
        pending_marks(sweep),
```

### `u221.R21_unknown_name_not_refused`

release plan: drop the refusal of a name that is no twin's, so it reaches the lookup

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R21_unknown_name_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned`

Old text:

```
        if missing:
            raise _not_a_twin(missing)
```

New text:

```
        if False:
            raise _not_a_twin(missing)
```

### `u221.R22_all_beside_names`

sync_release: drop the refusal of names beside --all

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R22_all_beside_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args1]`

Old text:

```
    if every and named:
```

New text:

```
    if False:
```

### `u221.R23_nothing_named`

sync_release: drop the refusal of a run naming nothing, so it plans nothing silently

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R23_nothing_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args0]`

Old text:

```
    if not every and not named:
```

New text:

```
    if False:
```

### `u221.R25_released_twin_asks_again`

Planned.action: a twin holding nothing reads as one to release, so a second run asks again over nothing

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R25_released_twin_asks_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_released_twin_asks_nothing_the_second_time`

Old text:

```
        return NOTHING_HELD if self.held is not None and not self.held else RELEASE
```

New text:

```
        return RELEASE
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

### `u287-m11.M11_gone_offers_nothing`

removals: read a playlist not read whole as removing every track, measured again after the zero of the first table was given a test

- File: `src/cratekit/sync/removed.py`
- Source: `u287-m11.json`, row `M11_gone_offers_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[empty]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[short]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[unreadable]`

Old text:

```
        if one.account in reads and reads[one.account].state == READ
```

New text:

```
        if one.account in reads
```

### `u287.M13_folder_separator`

_under: compare the folder as a bare prefix, so a sibling folder sharing its name's start reads as the pass's

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M13_folder_separator`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_path_is_under_a_folder_only_past_a_separator_and_in_one_unicode_form`

Old text:

```
        if root and (held.startswith(root + "/") or held.startswith(root + "\\")):
```

New text:

```
        if root and held.startswith(root):
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

### `u287.M17_gone_with_no_record_is_not_whole`

read_one: read a playlist neither read finds and nothing records as gone, holding nothing, rather than not read whole

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M17_gone_with_no_record_is_not_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_nothing_records_that_neither_read_finds_offers_nothing`

Old text:

```
            if not known:
                return Listing(
```

New text:

```
            if False:
                return Listing(
```

### `u287.M18_set_aside_rows_count`

read_one: leave the reader's set aside rows out of the identity sets

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M18_set_aside_rows_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc`

Old text:

```
        for one in readable.unread.values()
    )
```

New text:

```
        for one in ()
    )
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

### `u287.M1_partial_read_stops_offers`

plan_removed: never read a synced listing as partial, so an unreadable, short or empty playlist or hearts no longer stops any offer

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M1_partial_read_stops_offers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[empty]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[short]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[unreadable]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_nothing_records_that_neither_read_finds_offers_nothing`
  - `tests/test_sync_removed.py::test_hearts_not_read_whole_offer_nothing[empty]`
  - `tests/test_sync_removed.py::test_hearts_not_read_whole_offer_nothing[short]`
  - `tests/test_sync_removed.py::test_hearts_not_read_whole_offer_nothing[unreadable]`

Old text:

```
    partial = any(one.state in NOT_WHOLE for one in listings)
```

New text:

```
    partial = False
```

### `u287.M20_unreadable_record_is_not_whole`

recorded_contents: read a gone playlist whose job reports cannot be read as holding nothing recorded, refusing the verb

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M20_unreadable_record_is_not_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`

Old text:

```
        except CratekitError:
            return None
        return tuple(found) or None
```

New text:

```
        except ZeroDivisionError:
            return None
        return tuple(found) or None
```

### `u287.M2_held_by_isrc`

Listing.holds: drop the ISRC test, so a track relisted under another id with its ISRC reads as removed

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M2_held_by_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_listing_holds_a_track_by_any_of_three_tests_and_only_a_read_or_gone_one_holds`
  - `tests/test_sync_removed.py::test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc`
  - `tests/test_sync_removed.py::test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording`

Old text:

```
        if wanted.isrc and wanted.isrc.strip().upper() in self.isrcs:
```

New text:

```
        if False and wanted.isrc and wanted.isrc.strip().upper() in self.isrcs:
```

### `u287.M3_held_by_recording`

Listing.holds: drop the folded recording test, so a relinked track with its artist and title reads as removed

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M3_held_by_recording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_listing_holds_a_track_by_any_of_three_tests_and_only_a_read_or_gone_one_holds`
  - `tests/test_sync_removed.py::test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording`

Old text:

```
        return recording(wanted) in self.recordings
```

New text:

```
        return False
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

### `u287.M8_empty_read_untrusted`

read_one: trust an empty read with an unknown count, so a provider fault reads every track removed

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M8_empty_read_untrusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[empty]`

Old text:

```
    if not readable.order and (shown is None or shown.tracks != 0):
```

New text:

```
    if False:
```

### `u287.M9_short_read_untrusted`

read_one: trust a listing short of its declared count

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M9_short_read_untrusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[short]`

Old text:

```
    if readable.short is not None:
        block = readable.short.block()
```

New text:

```
    if False:
        block = readable.short.block()
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

### `u288.M19_first_position`

apply_removed: give the deletion pass no first position, so a first delete review accepts the removal as history

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M19_first_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`

Old text:

```
        first = _first_deletion_position(cfg, db)
```

New text:

```
        first = None
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

### `u320-m5.M5_retired_holds`

Listing.holds: count a retired playlist among the holding states

- File: `src/cratekit/sync/removed.py`
- Source: `u320-m5.json`, row `M5_retired_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_retired_listing_holds_nothing_whatever_it_carries`

Old text:

```
HOLDING = frozenset({READ, GONE, WITHHELD})
```

New text:

```
HOLDING = frozenset({READ, GONE, WITHHELD, RETIRED})
```

### `u320.M10_reopened_keeps_its_retirement`

read_one: a playlist that opens again keeps its entry, so its retirement survives

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M10_reopened_keeps_its_retirement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_that_opens_again_is_read_again_and_the_retirement_cleared`
  - `tests/test_sync_removed_gone.py::test_retire_writes_every_reads_answer_with_the_retirement`

Old text:

```
        state=READ,
        refs=frozenset(str(one) for one in readable.order),
```

New text:

```
        state=READ,
        noted=prior,
        refs=frozenset(str(one) for one in readable.order),
```

### `u320.M13_withheld_bound_widened`

WITHHELD_AT_MOST: read the hearts whole when short by up to half their count, so a dropped window reads as withheld

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M13_withheld_bound_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_hearts_short_by_more_than_a_tenth_of_their_count_stay_partial[over-a-tenth]`

Old text:

```
WITHHELD_AT_MOST = 0.10
```

New text:

```
WITHHELD_AT_MOST = 0.5
```

### `u320.M18_opened_and_refused_is_unopened`

read_one: read a playlist that opened and whose rows the reader refused as unlisted and unopened, so it keeps its retirement

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M18_opened_and_refused_is_unopened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_opens_and_whose_rows_are_refused_is_cleared`

Old text:

```
        if shown is None and exc.cause.reason != SERVED_UNREADABLE:
```

New text:

```
        if shown is None:
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

### `u320.M7_outage_forgets_the_record`

read_one: an unlisted playlist whose id failed some other way drops its entry, a retirement included

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M7_outage_forgets_the_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_now_fails_another_way_stops_offers_this_run_and_stays_retired`

Old text:

```
                if said_none
                else prior
```

New text:

```
                if said_none
                else None
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

### `u320.M9_relisted_keeps_its_retirement`

read_one: a playlist the account lists again keeps its entry, so its retirement survives

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M9_relisted_keeps_its_retirement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_the_account_lists_again_stops_every_offer_again`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_opens_and_whose_rows_are_refused_is_cleared`

Old text:

```
        return Listing(account=account, name=name, state=UNREADABLE, why=exc.cause.message)
```

New text:

```
        return Listing(account=account, name=name, state=UNREADABLE, why=exc.cause.message, noted=prior)
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

### `u320.M20_retirable_without_this_reads_not_found`

retirable: offer a playlist for retirement on its record alone, whatever its id answered now

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u320.json`, row `M20_retirable_without_this_reads_not_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_retire_names_a_gone_playlist_whose_id_now_fails_another_way`
  - `tests/test_sync_removed_gone.py::test_retire_offers_no_playlist_seen_before_whose_id_now_fails_another_way_and_says_so`

Old text:

```
        if one.not_found and one.noted is not None and not one.noted.is_retired
```

New text:

```
        if one.noted is not None and not one.noted.is_retired
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

### `r704-a.R1_increment_ignores_the_flag`

the increment never takes the rate limited branch, every lookup failure is permanent as before R-704

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R1_increment_ignores_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
            if exc.rate_limited:
```

New text:

```
            if False:
```

### `r704-a.R2_rate_limit_not_retryable`

the rate limited refusal says resume and records the item permanent, so the job verdict and jobs.retry still refuse

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R2_rate_limit_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    retryable=True,
                    origin=("sync.run",),
```

New text:

```
                    retryable=False,
                    origin=("sync.run",),
```

### `r704-a.R3_remedy_retry_later`

the rate limited refusal names retry later rather than resuming the job

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R3_remedy_retry_later`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    remedy=Remedy.RESUME_JOB,
```

New text:

```
                    remedy=Remedy.RETRY_LATER,
```

### `r704-a.R4_detail_unmarked`

the refusal's detail no longer says rate limited, so a machine reader cannot tell it from an outage

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R4_detail_unmarked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    detail={"source_id": source.id, "rate_limited": True},
```

New text:

```
                    detail={"source_id": source.id},
```

### `r704-a.R5_flag_not_stored`

LookupFailure drops the flag it was handed

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R5_flag_not_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
        self.rate_limited = rate_limited
```

New text:

```
        self.rate_limited = False
```

### `r704-a.R6_sentence_reworded`

the refusal no longer says the provider rate limited the lookup

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R6_sentence_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    f"the provider rate limited a lookup {source.id} needed "
```

New text:

```
                    f"the provider throttled a lookup {source.id} needed "
```

### `u52-item-derivation.A1_acquires_early_return_gone`

R-140: an offering source writes the intake row, registers the artifact and moves the watermark over releases nobody accepted

- File: `src/cratekit/sync/run.py`
- Source: `u52-item-derivation.json`, row `A1_acquires_early_return_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`
- Collected: 211 against a baseline of 211
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_an_offering_run_leaves_the_source_watermark_unset`
  - `tests/test_incremental_sync.py::test_an_offering_source_writes_no_intake_file`
  - `tests/test_incremental_sync.py::test_one_run_records_only_the_acquiring_source_of_a_mixed_pair`

Old text:

```
        if not getattr(source, "acquires", True):
```

New text:

```
        if False:
```

### `u52-item-derivation.A2_acquires_default_false`

MUTATE THE COEFFICIENT: flip the getattr default, so every source written before the attribute existed stops recording what it acquired

- File: `src/cratekit/sync/run.py`
- Source: `u52-item-derivation.json`, row `A2_acquires_default_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`
- Collected: 211 against a baseline of 211
- Kills: 6 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_rerun_after_a_clean_sync_processes_only_unowned_items`
  - `tests/test_incremental_sync.py::test_a_watermark_does_not_empty_the_scope_of_unowned_items`
  - `tests/test_incremental_sync.py::test_an_acquiring_source_still_writes_the_intake_file_and_advances`
  - `tests/test_incremental_sync.py::test_one_run_records_only_the_acquiring_source_of_a_mixed_pair`
  - `tests/test_incremental_sync.py::test_one_source_failing_does_not_block_the_other`
  - `tests/test_incremental_sync.py::test_two_sources_in_one_run_share_one_importable_file`

Old text:

```
        if not getattr(source, "acquires", True):
```

New text:

```
        if not getattr(source, "acquires", False):
```

### `r259.S1_scope_owned_sample`

Existing guard sample: scope.scoped no longer drops owned identities

- File: `src/cratekit/sync/scope.py`
- Source: `r259.json`, row `S1_scope_owned_sample`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_rerun_after_a_clean_sync_processes_only_unowned_items`

Old text:

```
        if item.identity in owned:
```

New text:

```
        if False:
```

### `r263.S2_favorites_reason`

Favorites declares no reason, so its absent record reads as never again

- File: `src/cratekit/sync/sources.py`
- Source: `r263.json`, row `S2_favorites_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
        no_cursor="no favorites worker records a cursor, so a completed sync "
```

New text:

```
        no_cursor="" and "no favorites worker records a cursor, so a completed sync "
```

### `u109-b.B1_labels_not_guided`

Drop guided_by from the labels spec, so labels is an ordinary source with no worker

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B1_labels_not_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 228 against a baseline of 228
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_every_guided_source_names_a_verb_the_registry_declares_and_queues_nothing`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
        guided_by="label.sync",
```

New text:

```
(empty)
```

### `u109-b.B2_command_spelling`

Spell the guided command with the registry's dotted name, crate label.sync

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B2_command_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_label_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 9 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_every_guided_source_names_a_verb_the_registry_declares_and_queues_nothing`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
        return "crate " + self.guided_by.replace(".", " ")
```

New text:

```
        return "crate " + self.guided_by
```

### `u109-b.B3_no_cursor_reworded`

Reword the labels no_cursor sentence so it no longer names the guided verb

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B3_no_cursor_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_doctor_prints_the_labels_row_it_is_given`

Old text:

```
        no_cursor="label releases are taken by crate label sync, which keeps "
```

New text:

```
        no_cursor="label releases are taken by the guided verb, which keeps "
```

### `u74.A1_no_inbound_key`

The favourites spec declares no read half, so sync all never lists the hearts

- File: `src/cratekit/sync/sources.py`
- Source: `u74.json`, row `A1_no_inbound_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 26 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - ... and 11 more, see the JSON sidecar

Old text:

```
        inbound_key="intake.playlist",
```

New text:

```
        inbound_key=None,
```

### `u74.A2_wrong_inbound_key`

The read half is queued under intake.set, a key whose worker reads a tracklist, not a listing

- File: `src/cratekit/sync/sources.py`
- Source: `u74.json`, row `A2_wrong_inbound_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_only_favourites_declares_a_read_half_and_its_key_is_a_bound_intake_key`

Old text:

```
        inbound_key="intake.playlist",
```

New text:

```
        inbound_key="intake.set",
```

### `u242.M11_strip_skips_the_held_check`

strip: rename without confirming the record holds each planned playlist

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M11_strip_skips_the_held_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_no_rename_is_made_for_a_playlist_the_record_does_not_hold`

Old text:

```
    unheld = [identity for identity in planned if identity not in held]
```

New text:

```
    unheld = []
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

### `u242.M13_strip_no_collision_with_others`

strip plan: never refuse a stripped title another playlist already carries

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M13_strip_no_collision_with_others`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`
  - `tests/test_u242_taken.py::test_the_gate_screen_lists_every_rename_and_every_refusal`

Old text:

```
        clash = others.get(to.casefold())
```

New text:

```
        clash = None
```

### `u242.M14_strip_no_collision_between_strips`

strip plan: never refuse two prefixed playlists stripped to one title

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M14_strip_no_collision_between_strips`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`

Old text:

```
        twins = sorted(prefixed[one] for one in writes[to.casefold()] if one != identity)
```

New text:

```
        twins = []
```

### `u242.M15_strip_collision_case_exact`

strip plan: compare titles case exactly, so Techno beside techno is renamed

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M15_strip_collision_case_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_the_gate_screen_lists_every_rename_and_every_refusal`

Old text:

```
            others.setdefault(name.strip().casefold(), name)
```

New text:

```
            others.setdefault(name.strip(), name)
```

### `u242.M17_strip_no_recheck`

strip apply: rename a playlist retitled since the plan was shown

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M17_strip_no_recheck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_title_changed_since_the_plan_is_not_renamed`

Old text:

```
            if now.get(identity) != item["name"]:
                changed.append(identity)
                continue
            # RECORDED BEFORE THE RENAME
```

New text:

```
            if False:
                changed.append(identity)
                continue
            # RECORDED BEFORE THE RENAME
```

### `u242.M18_strip_records_no_old_title`

strip apply: rename without recording the old title, so unmark cannot put it back

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M18_strip_records_no_old_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_every_old_title_is_restored_by_unmark_of_the_strip`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_the_strip_records_each_old_title_before_its_rename`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_is_put_back_renames_back`

Old text:

```
            record.record_marked(PASS, {identity: (item["name"], item["to"])})
            remote.rename_playlist(identity, item["to"])
```

New text:

```
            remote.rename_playlist(identity, item["to"])
```

### `u242.M19_migration_copies_an_unmarked_mark`

migration: copy a mark sync unmark already put back

- File: `src/cratekit/sync/taken_cli.py`
- Source: `u242.json`, row `M19_migration_copies_an_unmarked_mark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_the_migration_records_every_prefix_and_standing_mark_once_and_says_how_many`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`

Old text:

```
        if mark.unmarked or not playlists.is_swept_name(mark.to):
```

New text:

```
        if not playlists.is_swept_name(mark.to):
```

### `u149.T10_any_year_folder`

candidates: read every root folder, not only one titled as a year

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T10_any_year_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_only_downloaded_own_playlists_in_a_year_folder_are_read`

Old text:

```
        if not YEAR.fullmatch(year):
            continue
```

New text:

```
        if False:
            continue
```

### `u149.T11_excluded_read`

candidates: drop the label, set and mirror exclusion

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T11_excluded_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_set_playlist_in_a_year_folder_gets_no_twin`

Old text:

```
            if name is None or playlist_id in kept or playlist_id in seen:
```

New text:

```
            if name is None or playlist_id in seen:
```

### `u149.T13_paired_planned_again`

plan_backfill: plan a twin for an already paired playlist, so a second run plans again

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T13_paired_planned_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_existing_folder_is_reused_and_two_of_one_year_place_nothing`

Old text:

```
    wanted = [one for one in listed if one[1] not in held]
```

New text:

```
    wanted = list(listed)
```

### `u149.T15_unplanned_membership`

addition_violations: admit a membership no twin planned

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T15_unplanned_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_confinement_refuses_what_no_twin_explains[changes4]`

Old text:

```
        if row[m_marker] or wanted is None or content_id not in wanted[2]:
```

New text:

```
        if row[m_marker] or wanted is None:
```

### `u149.T16_unplanned_playlist_row`

addition_violations: admit a playlist row no twin made

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T16_unplanned_playlist_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_confinement_refuses_an_unplanned_playlist_read_from_sql`
  - `tests/test_sync_twins.py::test_the_confinement_refuses_what_no_twin_explains[changes0]`

Old text:

```
    for key in sorted(set(after.playlists) - set(before.playlists) - set(made)):
```

New text:

```
    for key in sorted(set()):
```

### `u149.T20_short_snapshot`

pair_backfilled: record the account snapshot when the listing was short

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T20_short_snapshot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_short_listing_pairs_the_twin_with_no_snapshot`

Old text:

```
            account=list(one.account) if one.whole else None,
```

New text:

```
            account=list(one.account),
```

### `u149.T21_landing_paired_again`

plan_landing: plan a twin for an account playlist already paired

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T21_landing_paired_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_twins.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_an_account_playlist_already_paired_gets_no_second_twin`

Old text:

```
    wanted = [(account_id, name) for account_id, name in accounts if account_id not in held]
```

New text:

```
    wanted = list(accounts)
```

### `u149.T2_two_folders_not_refused`

find_folder: drop the refusal of two live top level folders of one year, so the first is written to

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T2_two_folders_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_existing_folder_is_reused_and_two_of_one_year_place_nothing`

Old text:

```
    if len(found) > 1:
```

New text:

```
    if len(found) > 2:
```

### `u149.T3_folder_names_unread`

find_folder: read no names inside a live folder, so a held name is not seen

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T3_folder_names_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_a_twin_name_the_folder_holds_is_left_and_named_and_the_landing_still_lands`
  - `tests/test_sync_twins.py::test_a_name_the_folder_already_holds_is_refused_by_name_never_counted`

Old text:

```
held=_live_children(db, found[0]))
```

New text:

```
held=frozenset())
```

### `u149.T4_removed_folder_live`

_live_top_folders: drop the soft delete filter, so a removed folder is reused

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T4_removed_folder_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_removed_year_folder_is_not_reused_and_a_live_one_is_made`

Old text:

```
        f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0 ORDER BY ID"
```

New text:

```
        f"ORDER BY ID"
```

### `u149.T5_held_name_counted_free`

place: drop the refusal of a name the folder holds, so a second twin of one name is made

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T5_held_name_counted_free`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_a_twin_name_the_folder_holds_is_left_and_named_and_the_landing_still_lands`
  - `tests/test_sync_twins.py::test_a_name_the_folder_already_holds_is_refused_by_name_never_counted`
  - `tests/test_sync_twins.py::test_place_refuses_a_held_name_a_taken_name_an_empty_name_and_an_unplaced_year`

Old text:

```
    if name in folder.held:
```

New text:

```
    if False:
```

### `u149.T6_taken_name_free`

place: drop the refusal of a name this run already gave, so two twins share one name

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T6_taken_name_free`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_place_refuses_a_held_name_a_taken_name_an_empty_name_and_an_unplaced_year`

Old text:

```
    if name in taken:
```

New text:

```
    if False:
```

### `u149.T7_ambiguous_takes_first`

matched: take the first of several library rows, so an ambiguous track is guessed

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T7_ambiguous_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_account_track_two_library_rows_carry_is_named_and_neither_is_guessed`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
        if len(found) == 1:
```

New text:

```
        if found:
```

### `u149.T8_mirror_link_skipped`

Library.find: skip the mirror's link to the very track, so the database ISRC decides

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T8_mirror_link_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_mirrors_link_to_a_track_wins_and_a_link_to_a_removed_row_falls_through`

Old text:

```
            self.by_remote.get(remote_id, ()),
```

New text:

```
            (),
```

### `u149.T9_removed_row_linked`

_grouped: drop the live filter, so a mirror link to a removed row is an answer

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T9_removed_row_linked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_mirrors_link_to_a_track_wins_and_a_link_to_a_removed_row_falls_through`

Old text:

```
        if key and content_id in alive and content_id not in found.setdefault(key, []):
```

New text:

```
        if key and content_id not in found.setdefault(key, []):
```

### `u213.M14_backfill_reason_check`

plan_backfill: leave a playlist for any refusal, so an expired session leaves every playlist instead of naming its act

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M14_backfill_reason_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_refusal_that_is_not_about_one_playlist_still_stops_the_run`

Old text:

```
            if exc.cause.reason not in PER_PLAYLIST_REASONS:
                raise
            twins.append(
```

New text:

```
            if False:
                raise
            twins.append(
```

### `u213.M15_backfill_left_action`

plan_backfill: plan a playlist whose listing was refused as a twin to make, with no rows

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M15_backfill_left_action`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`
  - `tests/test_sync_twins.py::test_a_playlist_the_provider_cannot_list_is_left_named_and_the_other_is_made`
  - `tests/test_sync_twins.py::test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned`
  - `tests/test_sync_twins.py::test_every_playlist_left_writes_nothing_and_opens_no_gate`

Old text:

```
                    action=LEFT,
                    why=f"the account playlist could not be read: {exc.cause.message}",
```

New text:

```
                    action=CREATE,
                    why=f"the account playlist could not be read: {exc.cause.message}",
```

### `u213.M16_backfill_digest_reason`

Twin.identity: put the provider's words in the digest again, so a varying message makes the approved run stale

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M16_backfill_digest_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`

Old text:

```
            "why": self.refused or self.why,
```

New text:

```
            "why": self.why,
```

### `u213.M17_backfill_unread_tracks`

plan_backfill: plan from the read tracks alone, so an unread track is in neither the twin's misses nor its snapshot

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M17_backfill_unread_tracks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
            ref: listing.tracks[ref] if ref in listing.tracks else listing.unread[ref].said()
            for ref in listing.order
```

New text:

```
            ref: listing.tracks[ref]
            for ref in listing.order
            if ref in listing.tracks
```

### `u213.M18_backfill_unread_reasons`

plan_backfill: hand matched no unread reasons, so an unread track the library lacks reads as merely not owned

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M18_backfill_unread_reasons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`

Old text:

```
            {ref: one.why for ref, one in listing.unread.items()},
```

New text:

```
            {},
```

### `u213.M19_matched_ambiguous_first`

matched: say an unread track two rows carry is unreadable rather than ambiguous

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M19_matched_ambiguous_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
                    AMBIGUOUS
                    if found
                    else f"{unread[remote_id]}, {UNREAD_NOT_FOUND}"
                    if remote_id in unread
                    else NOT_OWNED
```

New text:

```
                    f"{unread[remote_id]}, {UNREAD_NOT_FOUND}"
                    if remote_id in unread
                    else AMBIGUOUS
                    if found
                    else NOT_OWNED
```

### `u213.M20_backfill_whole`

plan_backfill: read every listing as whole, so a short one is paired with a snapshot it does not have

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M20_backfill_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_short_listing_pairs_the_twin_with_no_snapshot`

Old text:

```
                whole=listing.short is None,
```

New text:

```
                whole=True,
```

### `u213.M2_backfill_refused_reason`

plan_backfill: record no refusal reason on a left playlist, so its digest carries the provider's words

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M2_backfill_refused_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`

Old text:

```
                    refused=exc.cause.reason,
```

New text:

```
                    refused="",
```

### `u221.R19_short_listing_records_its_misses`

pair_backfilled: record a short listing's misses as its hold, so a track the account withheld and serves later is queued with no choice

- File: `src/cratekit/sync/twins.py`
- Source: `u221.json`, row `R19_short_listing_records_its_misses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_short_listings_twin_records_no_hold_and_holds_a_track_served_later`

Old text:

```
                {miss.remote_id: miss.held_as() for miss in one.misses} if one.whole else None
```

New text:

```
                {miss.remote_id: miss.held_as() for miss in one.misses}
```

### `u221.R20_landing_records_no_hold`

pair_landed: mark a landing's twin with no hold, so it is read by time and its misses are held

- File: `src/cratekit/sync/twins.py`
- Source: `u221.json`, row `R20_landing_records_no_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_intake_land_twins.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`

Old text:

```
                one.account_id, one.playlist_id, name=one.account_name, twin=True, on_hold={}
```

New text:

```
                one.account_id, one.playlist_id, name=one.account_name, twin=True, on_hold=None
```

### `u242.M8_twins_reads_the_title_alone`

twins backfill: read a downloaded custom playlist by its prefix alone, so a stripped one gets no twin

- File: `src/cratekit/sync/twins.py`
- Source: `u242.json`, row `M8_twins_reads_the_title_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_twins.py`
- Collected: 92 against a baseline of 92
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_twins_reads_a_stripped_custom_playlist_as_downloaded`

Old text:

```
            if not is_taken(playlist_id, name, held):
```

New text:

```
            if not name.startswith("DOWNLOADED "):
```

### `u320.M11_apart_halved`

APART: retire twelve hours after the first sighting rather than a day

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M11_apart_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_sighting_retires_only_a_day_after_the_first_and_a_retirement_stands`

Old text:

```
APART = timedelta(hours=24)
```

New text:

```
APART = timedelta(hours=12)
```

### `u320.M12_apart_strict`

sighted: retire only past a day, not at a day

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M12_apart_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_sighting_retires_only_a_day_after_the_first_and_a_retirement_stands`

Old text:

```
    if latest - datetime.fromisoformat(held.first) >= APART:
```

New text:

```
    if latest - datetime.fromisoformat(held.first) > APART:
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

### `u320.M15_context_class_counts`

answered_unavailable: read the not found class off a link met only while handling another failure

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M15_context_class_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_not_found_met_only_while_handling_another_failure_is_not_one`

Old text:

```
        if declared and type(link).__name__ == CLIENT_NOT_FOUND:
```

New text:

```
        if type(link).__name__ == CLIENT_NOT_FOUND:
```

### `u320.M16_damaged_record_reads_empty`

UnavailableRecord.read: read a record that is not JSON as holding nothing

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M16_damaged_record_reads_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_an_unreadable_record_refuses_before_the_account_is_asked`

Old text:

```
            # Not UTF-8 is a ``ValueError`` too, and as unreadable.
            raise self._unusable("it is not JSON") from exc
```

New text:

```
            return {}
```

### `u320.M17_other_library_read`

UnavailableRecord: read a record written for another library

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M17_other_library_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_damaged_record_refuses_and_is_never_read_as_empty[library]`

Old text:

```
        if raw.get("library_id") != self.cfg.library.volume_id:
```

New text:

```
        if False:
```

### `u320.M19_none_drops_nothing`

UnavailableRecord._apply: a change of None drops nothing, so a reopened playlist stays retired

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M19_none_drops_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_that_opens_again_is_read_again_and_the_retirement_cleared`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_the_account_lists_again_stops_every_offer_again`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_opens_and_whose_rows_are_refused_is_cleared`
  - `tests/test_sync_removed_gone.py::test_retire_writes_every_reads_answer_with_the_retirement`
  - `tests/test_sync_removed_gone.py::test_the_record_reads_back_what_it_wrote_and_drops_an_entry_given_none`

Old text:

```
        after = {key: value for key, value in entries.items() if key not in changes}
```

New text:

```
        after = dict(entries)
```

### `u320.M3_any_not_found_name_counts`

answered_unavailable: read any class whose name holds not found, Python's FileNotFoundError included, round one's BLOCKING finding

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M3_any_not_found_name_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_pythons_own_not_found_classes_are_no_sighting_and_never_retire[file-not-found]`
  - `tests/test_sync_removed_gone.py::test_pythons_own_not_found_classes_are_no_sighting_and_never_retire[module-not-found]`

Old text:

```
        if declared and type(link).__name__ == CLIENT_NOT_FOUND:
```

New text:

```
        if declared and "notfound" in type(link).__name__.lower():
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

### `u242.M22_unmark_releases_nothing`

sync unmark: never plan a release, so a pass's taken playlists cannot be let go

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u242.json`, row `M22_unmark_releases_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_unmark.py`, `tests/test_label_playlists.py`, `tests/test_export_set.py`
- Collected: 190 against a baseline of 190
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

### `r263.W1_no_unrecorded_state`

status_rows ignores the declared no_cursor reason, so every absent record reads as never

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W1_no_unrecorded_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 4 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_doctor_prints_the_labels_row_it_is_given`
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
        reason = no_cursor.get(source_id)
```

New text:

```
        reason = None
```

### `r263.W2_state_word`

A cursorless source is reported with state never, detail unchanged

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W2_state_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
"state": "unrecorded"
```

New text:

```
"state": "never"
```

### `r263.W3_stale_record_as_completion`

A stale record on a cursorless source is reported as its last completion again

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W3_stale_record_as_completion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`

Old text:

```
        if reason is not None:
```

New text:

```
        if reason is not None and mark is None:
```

### `r263.W4_stale_suffix`

Drop the note that an earlier build's cursor no longer moves

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W4_stale_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`

Old text:

```
            if mark is not None:
                detail += (
```

New text:

```
            if False:
                detail += (
```

### `r1446.S1_u234_settled_reorder_never_leads`

sample, U234: a reorder settled readings show never leads

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `S1_u234_settled_reorder_never_leads`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
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

### `u198.C12_archive_move`

plan: a made pair moved under a skipped folder keeps syncing

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C12_archive_move`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py; the line also stands in favorites/order.py, another package's own guard, so rows --after would not choose
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_made_pair_moved_into_another_apps_or_the_favorites_folder_is_let_go[favorites]`
  - `tests/test_sync_pair_discover.py::test_a_made_pair_moved_into_another_apps_or_the_favorites_folder_is_let_go[foreign]`
  - `tests/test_sync_pair_discover.py::test_a_made_pair_moved_into_archive_is_let_go_and_never_written_again`

Old text:

```
                if moved:
```

New text:

```
                if False:
```

### `u208.M10_here_database_only`

here: read only the database ISRC, never the row's file

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M10_here_database_only`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; file_identity is read through pair_read, its home since the split
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

### `u231.M11_snapshot_from_the_order_sent`

write: the order as sent is recorded as the snapshot, with no settle reading

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M11_snapshot_from_the_order_sent`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[gone]`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[unreadable]`
  - `tests/test_sync_pair_settle.py::test_a_pair_that_never_settles_stays_pending_past_the_age_a_plan_is_kept`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_is_held_whole_until_a_later_reading_agrees`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_pending_run_does_not_count_its_pending_pair_as_synced`
  - `tests/test_sync_pair_settle.py::test_a_settle_reading_refused_for_another_reason_stops_the_write`
  - `tests/test_sync_pair_settle.py::test_a_write_that_keeps_no_record_sends_no_order`
  - `tests/test_sync_pair_settle.py::test_an_agreeing_reading_too_soon_after_the_last_is_not_agreement`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_at_once_finishes_in_the_one_run`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`
  - `tests/test_sync_pair_settle.py::test_the_settle_window_counts_the_time_spent_on_other_writes`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`

Old text:

```
        done.settle = Settle(
            one=one, steps=steps, end=sent, moved_at=pair_model._now(), rekordbox_after=None
        )
        return None
```

New text:

```
        return sent
```

### `u231.M13_settle_sleeps_the_whole_window`

settle: the whole window is waited, the time spent on other pairs' writes not counted

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M13_settle_sleeps_the_whole_window`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_the_settle_window_counts_the_time_spent_on_other_writes`

Old text:

```
        left = SETTLE_SECONDS - (pair_model._now() - settle.moved_at).total_seconds()
```

New text:

```
        left = SETTLE_SECONDS
```

### `u231.M17_agreement_gap_ignored`

plan: a reading equal to the one kept agrees however soon after it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M17_agreement_gap_ignored`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 752 against a baseline of 752
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_two_readings_agree_only_once_minutes_apart`

Old text:

```
    agreed = kept and pair_model._now() - seen_at >= AGREE_AFTER
```

New text:

```
    agreed = kept
```

### `u234.O10_after_not_compared`

the order after a settled one leads whatever the reading now, so an order that moved again leads unsettled

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O10_after_not_compared`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`

Old text:

```
        and not pair_stopped.reordered(kept.after, reading)
        and pair_model._now() - since
```

New text:

```
        and pair_model._now() - since
```

### `u234.O9_after_without_the_window`

the order after a settled one leads on its next reading however soon

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O9_after_without_the_window`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 764 against a baseline of 764
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`

Old text:

```
        and pair_model._now() - since >= AGREE_AFTER
    ):
        return True
```

New text:

```
    ):
        return True
```

