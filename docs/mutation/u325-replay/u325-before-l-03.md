# Mutation table: u325-before-l-03

Measured by `scripts/mutate.py` on 2026-11-22 22:24 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 146.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:24 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 4, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r227.C6_composed_limit_spelled` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M5_unwired` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M6_no_append` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M7_note_before_describe` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r504-b.B10_check_no_numbers` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B7_sync_drops_short` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B8_check_passes` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B9_all_withheld_says_no_hearts` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r515-operator.S13_sweep_no_warning` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A1_plan_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 9 | killed |
| `u109-a.A2_guided_empty` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 6 | killed |
| `u109-a.A3_no_check_row` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u109-a.A4_summary_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u109-a.A5_gate_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A6_refusal_step_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u109-a.A7_refusal_step_first` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A8_row_reworded` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
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
| `r187-a.C2_uncapped` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `r187-a.C3_mutex` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `r187-a.C4_key_beside_name` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `r187-a.C5_empty_name_scans` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `r187-a.C6_no_cache_path` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 3 | killed |
| `u43-author-light.A1_first_track_wins` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 4 | killed |
| `u43-author-light.A3_containment_not_checked` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.A4_empty_anchor_defaults` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.C1_no_lower_bound` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 4 | killed |
| `u43-author-light.C2_bound_off_by_one` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.P1_anchor_absent_from_digest` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.P3_pool_leads_the_items` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-light.P4_no_positions_at_all` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 4 | killed |
| `u43-author-light.P5_role_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u43-author-light.P7_vox_threshold_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.A2_no_resolved_second_pass` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.H2_empty_is_a_no_op` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.H3_missing_root_not_refused` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.H4_template_loses_the_marker` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.P2_items_absent_from_digest` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.P6_count_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.V1_pool_total_is_the_union` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.V2_marker_position_moved` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u43-author-round-2.V3_root_check_reports_instead_of_refusing` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-a.K1_key_off_wheel` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 7 | killed |
| `u98-a.T1_tempo_nonfinite` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u98-a.T2_tempo_zero` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-a.U1_empty_label` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-a.U2_key_missing` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u98-a.U3_reported_owned` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 5 | killed |
| `u98-a.U4_tempo_dropped` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 3 | killed |
| `u98-a.X1_mutex` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 3 | killed |
| `u98-b.E1_existing_containment` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 2 | killed |
| `u98-b.H1_held_not_excluded` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-b.H2_held_not_reported` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-b.H3_held_fuzzy` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `u98-b.S1_supplied_beside_path` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 3 | killed |
| `u98-b.S2_tempo_half` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 86 | 1 | killed |
| `r650-a.B5_artifact_drops_the_key` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 3 | killed |
| `r650-a.C1_summary_counts_nothing` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r650-a.C3_summary_drops_the_key` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 4 | killed |
| `r650-a.C4_warning_fires_on_a_clean_sweep` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r650-a.C6_warning_names_no_strings` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r650-a.C7_warning_order_is_the_walk_order` | `src/cratekit/tagging/cli.py` | maintainer | 1 file(s) | 102 | 1 | killed |
| `r650-a.C8_warning_code_reworded` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r650-a.C9_warning_counts_the_wrong_total` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r650-a.D3_unresolved_is_fed_by_declines` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u281.C2_challenge_never_named` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u281.C3_unsent_never_counted` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u281.C4_source_blocked_counts_unsent_as_sent` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u281.C5_partial_challenge_called_whole` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R19_folder_queues_no_items` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 41 | killed |
| `u56-catalogue-searcher-and-tag-workers.R20_unnamed_folder_sweeps_cwd` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R21_two_zeroes_read_as_one` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R22_vanished_file_reports_done` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R23_summary_from_the_queue` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 27 | killed |
| `u84-b.C1_artifact_carries_status` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u84-b.C2_summary_zero_filled` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u84-b.C3_old_reports_uncounted` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u85-a.A15_worker_hands_in_the_fetch` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 3 | killed |
| `u85-a.A16_summary_counts_art` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r1103.H3_message_names_no_file` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r1103.H4_detail_path` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r1103.H5_detail_genre` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r1103.H6_detail_current` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r816-e.E1_retag_names_the_verb` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R28_worker_trusts_the_frozen_row` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R29_blank_genre_is_corrected` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R30_specific_genre_is_overwritten` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R31_artifact_drops_the_previous_value` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R37_artifact_named_by_item_id` | `src/cratekit/tagging/artifacts.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R38_staging_not_cleared` | `src/cratekit/tagging/artifacts.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R33_no_op_job_id_is_null` | `src/cratekit/tagging/shell.py` | user | 1 file(s) | 102 | 9 | killed |
| `u56-catalogue-searcher-and-tag-workers.R34_empty_job_is_driven` | `src/cratekit/tagging/shell.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R35_extra_rides_beside_progress` | `src/cratekit/tagging/shell.py` | user | 1 file(s) | 102 | 47 | killed |
| `r312.W2_worker_writes_nothing` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 8 | killed |
| `r312.W3_success_exit_silent` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 5 | killed |
| `r312.W4_failure_exit_silent` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 2 | killed |
| `r312.W5_cause_steps_replaced` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r312.W7b_pre_drive_refusal_extended` | `src/cratekit/write/routing_cli.py` | maintainer | 2 file(s) | 244 | 1 | killed |
| `r312.W8_list_not_by_job` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 2 | killed |
| `r318-b.C7_trees_not_deduplicated` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318-b.N1_no_native_key_dropped` | `src/cratekit/write/routing_cli.py` | maintainer | 2 file(s) | 244 | 1 | killed |
| `r318-b.W2_cap_halved` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C1_skipped_files_always_empty` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 4 | killed |
| `r318.C2_tombstones_not_consulted` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C3_ambiguous_ids_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C4_withdrawn_ids_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C5_withdrawn_single_id_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C6_trees_emptied` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 2 | killed |
| `r318.C8_path_reduced_to_name` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C9_warnings_not_emitted` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 4 | killed |
| `r318.W1_cap_not_applied` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.W3_count_is_named_not_whole` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.W4_reasons_unsorted` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.W5_next_act_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u132.W6_resort_note` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u155.W3_gate_column` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 3 | killed |
| `u155.W4_gate_count` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 3 | killed |

## Row definitions

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

### `r187-a.C2_uncapped`

named_anchor: list every candidate, so a vague name prints a whole label

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C2_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_listing_is_capped_and_says_how_many_it_reached`

Old text:

```
    shown = matched.candidates[: setbuilder.CANDIDATE_LIMIT]
```

New text:

```
    shown = matched.candidates
```

### `r187-a.C3_mutex`

build: declare --named on the parser and not in the exclusive group, so it can sit beside a path or a label

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C3_mutex`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[path]`
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[unowned]`

Old text:

```
    anchor.add_argument(
        "--named",
```

New text:

```
    parser.add_argument(
        "--named",
```

### `r187-a.C4_key_beside_name`

set_build: a key beside --named is let through and silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C4_key_beside_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_key_beside_a_name_refuses_rather_than_being_ignored`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if ctx.args.named is None and (ctx.args.key is not None or ctx.args.tempo is not None):
```

### `r187-a.C5_empty_name_scans`

set_build: an empty name pays for the library walk before it is refused

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C5_empty_name_scans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_empty_name_refuses_before_any_scan`

Old text:

```
        index = _index(cfg, root) if names_something(ctx.args.named) else ()
```

New text:

```
        index = _index(cfg, root)
```

### `r187-a.C6_no_cache_path`

_index: pass no cache path, which is R-188 itself, every set a full scan

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C6_no_cache_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_second_run_reads_no_tag_it_already_holds`
  - `tests/test_setbuilder_cli.py::test_the_first_run_opens_each_file_once_and_the_second_none`
  - `tests/test_setbuilder_cli.py::test_the_verb_writes_its_declared_cache_and_nothing_of_the_librarys`

Old text:

```
        cache_path=config.state_path("setbuilder_index_cache", cfg),
```

New text:

```
        cache_path=None,
```

### `u43-author-light.A1_first_track_wins`

anchor_in_index returns the first indexed track instead of the one at the path, which is exactly what the fuzzy lookup this design replaces does when a version suffix is present

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A1_first_track_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_is_not_in_the_library_refuses_with_a_vocabulary_code`
  - `tests/test_setbuilder_cli.py::test_an_anchor_the_index_does_not_hold_is_absent_rather_than_approximated`
  - `tests/test_setbuilder_cli.py::test_an_exact_name_is_never_lost_to_a_longer_title_whichever_came_first`
  - `tests/test_setbuilder_cli.py::test_what_plays_after_a_track_is_asked_by_name`

Old text:

```
    wanted = str(path)
    for track in index:
        if track.path == wanted:
            return track
```

New text:

```
    wanted = str(path)
    for track in index:
        if track.path or wanted:
            return track
```

### `u43-author-light.A3_containment_not_checked`

anchor_path stops checking that the anchor is inside the library, so a path walking out with .. is scanned for and refused as unindexed rather than refused as outside

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A3_containment_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_outside_the_library_refuses_before_any_scan`
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_walks_out_of_the_library_is_refused`

Old text:

```
    if not _within(candidate, root):
```

New text:

```
    if _within(candidate, root) and False:
```

### `u43-author-light.A4_empty_anchor_defaults`

anchor_path stops refusing an empty anchor, which turns it into the library root and asks the index for a directory

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A4_empty_anchor_defaults`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_empty_anchor_is_refused_rather_than_defaulted`
  - `tests/test_setbuilder_cli.py::test_an_empty_anchor_refuses_through_the_dispatcher`

Old text:

```
    if not anchor:
        raise refuse(
```

New text:

```
    if anchor and not anchor:
        raise refuse(
```

### `u43-author-light.C1_no_lower_bound`

positive_count stops refusing zero and negatives, so build_plan's pool[: count or DEFAULT_POOL] silently turns 0 into 8 and -1 into a dropped last companion

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `C1_no_lower_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[-1]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[-8]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[0]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_the_parsers_verdict_and_not_a_refusal`

Old text:

```
    value = int(text)
    if value < 1:
        raise ValueError(f"{text!r} is not a positive count")
    return value
```

New text:

```
    return int(text)
```

### `u43-author-light.C2_bound_off_by_one`

The bound is loosened by one rather than removed, so zero passes and negatives do not. A guard whose constant can be moved without a death is a guard that pins nothing.

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `C2_bound_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_refused_at_the_parser[0]`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_the_parsers_verdict_and_not_a_refusal`

Old text:

```
    if value < 1:
```

New text:

```
    if value < 0:
```

### `u43-author-light.P1_anchor_absent_from_digest`

The digest stops covering the anchor, so two plans over the same companions and different anchors are indistinguishable

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P1_anchor_absent_from_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`

Old text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"], "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "setbuild", "items": items}),
```

### `u43-author-light.P3_pool_leads_the_items`

The pool leads and the sequence follows, so the recommendation is no longer at the top of the array a consumer reads

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P3_pool_leads_the_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_sequence_leads_the_items_and_carries_its_own_order`

Old text:

```
    ordered = list(plan.sequence) + [s for s in plan.pool if id(s) not in placed]
```

New text:

```
    ordered = [s for s in plan.pool if id(s) not in placed] + list(plan.sequence)
```

### `u43-author-light.P4_no_positions_at_all`

Every item reports position null, so the suggested sequence is not recoverable from the payload

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P4_no_positions_at_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_sequence_places_each_companion_once`
  - `tests/test_setbuilder_cli.py::test_one_either_companion_of_an_owned_anchor_is_placed_once`
  - `tests/test_setbuilder_cli.py::test_plan_for_composes_the_engine_exactly_as_build_set_does`
  - `tests/test_setbuilder_cli.py::test_the_sequence_leads_the_items_and_carries_its_own_order`

Old text:

```
        {**entry, "position": placed.get(id(scored))}
```

New text:

```
        {**entry, "position": None}
```

### `u43-author-light.P5_role_ignored`

The role flag is dropped on the way to the engine, so --role before answers with both sides

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P5_role_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_role_narrows_the_answer_to_one_side`
  - `tests/test_setbuilder_cli.py::test_the_role_flag_reaches_the_engine`

Old text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=role)
```

New text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=None)
```

### `u43-author-light.P7_vox_threshold_ignored`

The vocal threshold is dropped on the way to the ranker, which makes the fifth ranking signal permanently neutral and its whole weight dead

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P7_vox_threshold_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_vocal_signal_is_reachable_only_because_a_threshold_can_be_supplied`

Old text:

```
        vox_threshold=vox_threshold,
    )
    plan = setbuilder.build_plan
```

New text:

```
        vox_threshold=None,
    )
    plan = setbuilder.build_plan
```

### `u43-author-round-2.A2_no_resolved_second_pass`

ROUND ONE: zero. Drop the resolved second pass in anchor_in_index, so a path spelled through a symlink or a different absolute form never matches

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `A2_no_resolved_second_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_spelled_through_a_symlink_still_resolves`

Old text:

```
    try:
        resolved = path.resolve()
    except OSError:
        return None
    for track in index:
        if not track.path:
            continue
        try:
            if Path(track.path).resolve() == resolved:
                return track
        except OSError:
            continue
    return None
```

New text:

```
    return None
```

### `u43-author-round-2.H2_empty_is_a_no_op`

ROUND ONE: zero. A plan with no companions reports NO_OP rather than OK, which tells a consumer nothing happened when the question was answered

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H2_empty_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`

Old text:

```
    return ctx.envelope(data=plan, outcome=Outcome.OK)
```

New text:

```
    return ctx.envelope(
        data=plan, outcome=Outcome.OK if plan["items"] else Outcome.NO_OP
    )
```

### `u43-author-round-2.H3_missing_root_not_refused`

ROUND ONE: zero. The configured library root is no longer checked before the scan, so an unmounted volume scans zero files and every anchor comes back unindexed

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H3_missing_root_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`

Old text:

```
    if not root.is_dir():
```

New text:

```
    if root.is_dir() and False:
```

### `u43-author-round-2.H4_template_loses_the_marker`

ROUND ONE: zero. The name template stops declaring the lossy marker, so a marked file's clean title keeps the marker and its match key gains a token

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H4_template_loses_the_marker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_lossy_marked_companion_comes_back_with_a_clean_title`

Old text:

```
    return NameTemplate(markers=(MarkerRule(field="lossy", literal=cfg.naming.lossy_marker),))
```

New text:

```
    return NameTemplate()
```

### `u43-author-round-2.P2_items_absent_from_digest`

ROUND ONE: zero. The digest stops covering the items, so two entirely different sets of recommendations for one anchor carry one identity

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `P2_items_absent_from_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_two_plans_over_the_same_anchor_and_different_companions_digest_apart`

Old text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"], "items": items}),
```

New text:

```
        "digest": digest_of({"kind": "setbuild", "anchor": rendered["anchor"]}),
```

### `u43-author-round-2.P6_count_ignored`

ROUND ONE: zero. The count flag is dropped on the way to the engine, so the pool is always the default eight

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `P6_count_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_caps_the_companions`

Old text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=role)
```

New text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=None, role=role)
```

### `u43-author-round-2.V1_pool_total_is_the_union`

totals reports the union size where it says pool, which is the wrong number and the one a reader would otherwise have to derive. The round-one arithmetic surprise is exactly this confusion, so the new count guard owes a death here

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `V1_pool_total_is_the_union`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_count_caps_the_companions`

Old text:

```
        "pool": len(plan.pool),
```

New text:

```
        "pool": len(items),
```

### `u43-author-round-2.V2_marker_position_moved`

The marker rule is declared with a separator that puts it somewhere the head parser does not strip. If the lossy guard passes this, its fixture is in a position where the declaration cannot matter, which is the mistake the first attempt at it made

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `V2_marker_position_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_lossy_marked_companion_comes_back_with_a_clean_title`

Old text:

```
    return NameTemplate(markers=(MarkerRule(field="lossy", literal=cfg.naming.lossy_marker),))
```

New text:

```
    return NameTemplate(markers=(MarkerRule(field="lossy", literal="[NOTAMARKER]"),))
```

### `u43-author-round-2.V3_root_check_reports_instead_of_refusing`

The missing root produces an empty plan and an OK exit rather than a refusal, which is the clean-report-over-unreadable-state shape rather than the crash shape. A guard that only catches the crash is not the guard this row needs

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `V3_root_check_reports_instead_of_refusing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`

Old text:

```
    if not root.is_dir():
        raise refuse(
```

New text:

```
    if not root.is_dir():
        return ctx.envelope(
            data=plan_for(
                setbuilder.Track(
                    artist="", title="", key="", bpm=None, genre="",
                    energy=None, vox=None, voxgender=None, match="",
                ),
                (),
                declared=taxonomy.default_taxonomy(),
            ),
            outcome=Outcome.OK,
        )
    if False:
        raise refuse(
```

### `u98-a.K1_key_off_wheel`

camelot_key: drop the refusal, so a code off the wheel parses to the empty string

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `K1_key_off_wheel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 7 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[0A]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[13A]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[13C]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[8C]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_refused_at_the_parser[eight]`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_the_parsers_verdict`

Old text:

```
    if not canonical:
        raise ValueError(f"{text!r} is not a Camelot code between 1A and 12B")

```

New text:

```
(empty)
```

### `u98-a.T1_tempo_nonfinite`

positive_tempo: drop the finiteness half, so NaN and inf parse

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `T1_tempo_nonfinite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_tempo_that_would_empty_the_pool_is_refused_at_the_parser[inf]`
  - `tests/test_setbuilder_cli.py::test_a_tempo_that_would_empty_the_pool_is_refused_at_the_parser[nan]`

Old text:

```
if not math.isfinite(value) or value <= 0:
```

New text:

```
if value <= 0:
```

### `u98-a.T2_tempo_zero`

positive_tempo: move the bound to strictly negative, so zero parses

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `T2_tempo_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_tempo_that_would_empty_the_pool_is_refused_at_the_parser[0]`

Old text:

```
if not math.isfinite(value) or value <= 0:
```

New text:

```
if not math.isfinite(value) or value < 0:
```

### `u98-a.U1_empty_label`

unowned_anchor: drop the empty label refusal, so an empty label resolves by key alone

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U1_empty_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_empty_unowned_label_refuses_as_an_unknown_anchor`

Old text:

```
    if not label:
        raise refuse(
            "setbuild-anchor-unknown",
            "setbuild needs the track to build the set around",
            steps=("pass a label with --unowned, and its Camelot key with --key",),
            origin=("setbuilder", "cli"),
        )

```

New text:

```
(empty)
```

### `u98-a.U2_key_missing`

unowned_anchor: drop the key missing refusal, so an unresolved anchor reaches the engine

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U2_key_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_with_no_key_refuses`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_with_no_key_refuses_through_the_dispatcher`

Old text:

```
    if resolved.key is None:
```

New text:

```
    if False:
```

### `u98-a.U3_reported_owned`

unowned_anchor: return the anchor marked owned and confirmed, the envelope's honesty flags

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U3_reported_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 5 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_in_8a_ranks_the_library_against_it`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_is_ranked_through_the_dispatcher`
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_naming_an_owned_track_exactly_is_held_and_not_ranked`
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_that_names_an_owned_title_is_never_matched_to_it`

Old text:

```
            detail={"label": label, "unresolved": resolved.unresolved},
        )
    return resolved
```

New text:

```
            detail={"label": label, "unresolved": resolved.unresolved},
        )
    return setbuilder.Anchor(
        key=resolved.key, bpm=resolved.bpm, owned=True, display=resolved.display
    )
```

### `u98-a.U4_tempo_dropped`

unowned_anchor: pass no tempo to the engine, so --bpm is silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U4_tempo_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_tempo_narrows_an_unowned_anchor_to_its_band`
  - `tests/test_setbuilder_cli.py::test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_is_ranked_through_the_dispatcher`

Old text:

```
resolve_anchor(label, (), key=key, bpm=tempo)
```

New text:

```
resolve_anchor(label, (), key=key, bpm=None)
```

### `u98-a.X1_mutex`

build: declare the anchor and --unowned on the parser, not in an exclusive group

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `X1_mutex`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[path]`
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[unowned]`
  - `tests/test_setbuilder_cli.py::test_a_path_and_an_unowned_label_together_are_the_parsers_verdict`

Old text:

```
    anchor = parser.add_mutually_exclusive_group()
```

New text:

```
    anchor = parser
```

### `u98-b.E1_existing_containment`

existing sample: anchor_path drops the library containment refusal

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `E1_existing_containment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_outside_the_library_refuses_before_any_scan`
  - `tests/test_setbuilder_cli.py::test_an_anchor_that_walks_out_of_the_library_is_refused`

Old text:

```
    if not _within(candidate, root):
```

New text:

```
    if False:
```

### `u98-b.H1_held_not_excluded`

plan_for: report the exact match copies but leave them in the ranked index

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `H1_held_not_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_naming_an_owned_track_exactly_is_held_and_not_ranked`

Old text:

```
        index = [t for t in index if not (label and t.match == label)]
```

New text:

```
(empty)
```

### `u98-b.H2_held_not_reported`

plan_for: exclude the exact match copies but report none

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `H2_held_not_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_naming_an_owned_track_exactly_is_held_and_not_ranked`

Old text:

```
        totals["held"] = held
```

New text:

```
        totals["held"] = []
```

### `u98-b.H3_held_fuzzy`

plan_for: widen the exact match to containment, the fuzzy shape the empty index exists to avoid

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `H3_held_fuzzy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_that_names_an_owned_title_is_never_matched_to_it`

Old text:

```
        index = [t for t in index if not (label and t.match == label)]
```

New text:

```
        index = [t for t in index if not (label and label in t.match)]
```

### `u98-b.S1_supplied_beside_path`

set_build: drop the refusal of --key or --bpm beside a path anchor, so both are silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `S1_supplied_beside_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_key_beside_a_name_refuses_rather_than_being_ignored`
  - `tests/test_setbuilder_cli.py::test_a_supplied_value_beside_a_path_anchor_refuses_rather_than_being_ignored[key]`
  - `tests/test_setbuilder_cli.py::test_a_supplied_value_beside_a_path_anchor_refuses_rather_than_being_ignored[tempo]`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if False:
```

### `u98-b.S2_tempo_half`

set_build: drop only the tempo half of that refusal

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `S2_tempo_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_value_beside_a_path_anchor_refuses_rather_than_being_ignored[tempo]`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if ctx.args.key is not None:
```

### `r650-a.B5_artifact_drops_the_key`

The committed item report stops carrying the flag, so the summary reads it back as absent

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `B5_artifact_drops_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
            "off_taxonomy": result.off_taxonomy,
```

New text:

```
(empty)
```

### `r650-a.C1_summary_counts_nothing`

The report stops counting the strings, leaving the map empty on a folder that has them

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C1_summary_counts_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
            if report.get("off_taxonomy") and source_genre:
                off_taxonomy[source_genre] = off_taxonomy.get(source_genre, 0) + 1
```

New text:

```
(empty)
```

### `r650-a.C3_summary_drops_the_key`

The payload stops carrying the map at all

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C3_summary_drops_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_sweep_with_nothing_off_taxonomy_carries_no_such_warning`
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
        "off_taxonomy": off_taxonomy,
```

New text:

```
(empty)
```

### `r650-a.C4_warning_fires_on_a_clean_sweep`

The empty check goes, so an ordinary folder is warned about a gap it does not have

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C4_warning_fires_on_a_clean_sweep`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_with_nothing_off_taxonomy_carries_no_such_warning`

Old text:

```
    if not counted:
        return ()
```

New text:

```
(empty)
```

### `r650-a.C6_warning_names_no_strings`

The warning says a gap exists and not which word, which is the R24 mistake one verb over

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C6_warning_names_no_strings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
                f"these catalogue answers: {words}. Each word was written onto "
```

New text:

```
                f"these catalogue answers. Each word was written onto "
```

### `r650-a.C7_warning_order_is_the_walk_order`

The strings are listed in commit order, so two runs over one folder disagree

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C7_warning_order_is_the_walk_order`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
    words = ", ".join(sorted(counted))
```

New text:

```
    words = ", ".join(counted)
```

### `r650-a.C8_warning_code_reworded`

The code a log filter reads is reworded, never appended to

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C8_warning_code_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
OFF_TAXONOMY = "tag-folder-off-taxonomy"
```

New text:

```
OFF_TAXONOMY = "tag-folder-unknown-word"
```

### `r650-a.C9_warning_counts_the_wrong_total`

The warning names the file count as the sweep's whole tagged total

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C9_warning_counts_the_wrong_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
    files = sum(counted.values())
```

New text:

```
    files = summary.get("tagged", 0)
```

### `r650-a.D3_unresolved_is_fed_by_declines`

Existing: the unresolved map is filled from unmapped-genre and from nothing else

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `D3_unresolved_is_fed_by_declines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
        if reason == tag_engine.UNMAPPED_GENRE and source_genre:
```

New text:

```
        if source_genre:
```

### `u281.C2_challenge_never_named`

_summary: never count a Cloudflare challenge, so the warning cannot name one

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C2_challenge_never_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
                if searchers.CLOUDFLARE_CHALLENGE in note:
                    challenged[source] += 1
```

New text:

```
                if False:
                    challenged[source] += 1
```

### `u281.C3_unsent_never_counted`

_summary: never count a file a catalogue was not sent

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C3_unsent_never_counted`
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

### `u281.C5_partial_challenge_called_whole`

_unread_phrase: call every refusal a challenge when any one was

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C5_partial_challenge_called_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_some_of_whose_refusals_were_a_challenge_says_how_many`

Old text:

```
    if challenged >= count:
```

New text:

```
    if challenged:
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

### `u56-catalogue-searcher-and-tag-workers.R20_unnamed_folder_sweeps_cwd`

Path("") is the current directory, so an unnamed folder writes genres into whatever the person is standing in

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R20_unnamed_folder_sweeps_cwd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_empty_folder_argument_never_sweeps_the_working_directory`

Old text:

```
    named = str(ctx.args.folder or "")
    if not named.strip():
```

New text:

```
    named = str(ctx.args.folder or "")
    if False:
```

### `u56-catalogue-searcher-and-tag-workers.R21_two_zeroes_read_as_one`

A mistyped path reports as a folder with nothing to tag, which is the answer most likely to stop somebody looking

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R21_two_zeroes_read_as_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`

Old text:

```
            if folder.is_dir()
            else _empty(
                "tag-folder-absent",
```

New text:

```
            if True
            else _empty(
                "tag-folder-absent",
```

### `u56-catalogue-searcher-and-tag-workers.R22_vanished_file_reports_done`

An item whose file is gone reports done having tagged nothing, which is the clean report over unreadable state the merge bar names

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R22_vanished_file_reports_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`

Old text:

```
    path = folder / item.item_id
    if not path.is_file():
```

New text:

```
    path = folder / item.item_id
    if False:
```

### `u56-catalogue-searcher-and-tag-workers.R23_summary_from_the_queue`

The report counts what was queued rather than what ran, so a half finished sweep reports every file as handled

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R23_summary_from_the_queue`
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

### `u84-b.C1_artifact_carries_status`

The item artifact drops the repair status, so nothing on disk records what the repair did

- File: `src/cratekit/tagging/cli.py`
- Source: `u84-b.json`, row `C1_artifact_carries_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`

Old text:

```
            "art_repair": result.art_repair,

```

New text:

```
(empty)
```

### `u84-b.C2_summary_zero_filled`

The summary lists only the statuses it saw, so none repaired and not counted read the same

- File: `src/cratekit/tagging/cli.py`
- Source: `u84-b.json`, row `C2_summary_zero_filled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_report_from_before_the_repair_is_counted_under_no_status`
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`

Old text:

```
        "art_repair": art_repair,
```

New text:

```
        "art_repair": {key: value for key, value in art_repair.items() if value},
```

### `u84-b.C3_old_reports_uncounted`

A report committed before the repair existed is counted as ok, a status nobody measured

- File: `src/cratekit/tagging/cli.py`
- Source: `u84-b.json`, row `C3_old_reports_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_report_from_before_the_repair_is_counted_under_no_status`

Old text:

```
        status = str(report.get("art_repair") or "")
```

New text:

```
        status = str(report.get("art_repair") or art.REPAIR_OK)
```

### `u85-a.A15_worker_hands_in_the_fetch`

The worker passes no image fetch, so the verb never embeds art

- File: `src/cratekit/tagging/cli.py`
- Source: `u85-a.json`, row `A15_worker_hands_in_the_fetch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`

Old text:

```
        fetch_image=searchers.for_images(),

```

New text:

```
(empty)
```

### `u85-a.A16_summary_counts_art`

The job summary never counts an art status

- File: `src/cratekit/tagging/cli.py`
- Source: `u85-a.json`, row `A16_summary_counts_art`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`

Old text:

```
            art_fetch[fetched] += 1
```

New text:

```
            pass
```

### `r1103.H3_message_names_no_file`

handle: reword the refusal so it names no file

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H3_message_names_no_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`

Old text:

```
            f"{path} would not take the genre {result.proposed!r}, so it still "
```

New text:

```
            f"the file would not take the genre {result.proposed!r}, so it still "
```

### `r1103.H4_detail_path`

handle: the refusal's detail loses the file's path

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H4_detail_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
                "path": str(path),
```

New text:

```
                "path": "",
```

### `r1103.H5_detail_genre`

handle: the refusal's detail names the genre the file still carries as the one it would not take

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H5_detail_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`

Old text:

```
                "genre": result.proposed,
```

New text:

```
                "genre": result.current,
```

### `r1103.H6_detail_current`

handle: the refusal's detail loses the genre the file still carries

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H6_detail_current`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`

Old text:

```
                "current": result.current,
```

New text:

```
                "current": "",
```

### `r816-e.E1_retag_names_the_verb`

library_row_warning: name no verb, reworded

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r816-e.json`, row `E1_retag_names_the_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`

Old text:

```
because this verb writes the file half only; run `crate tag "
            f"rows` so the rows catch up
```

New text:

```
because this verb writes the file half only; run the row "
            f"verb so the rows catch up
```

### `u56-catalogue-searcher-and-tag-workers.R28_worker_trusts_the_frozen_row`

The genre is not re-read at drive time, so a file somebody corrected by hand between the confirmation and the drive is corrected again

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R28_worker_trusts_the_frozen_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`

Old text:

```
    current = tags.read_genre_from_file(path) or ""
    if not current:
```

New text:

```
    current = tags.read_genre_from_file(path) or ""
    if False:
```

### `u56-catalogue-searcher-and-tag-workers.R29_blank_genre_is_corrected`

The retag writes into a field tag.folder owns under fill if empty, which is one field under two policies

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R29_blank_genre_is_corrected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`

Old text:

```
    if not current:
        result = retag.RetagResult(path=path, current=current, reason=retag.NO_GENRE)
```

New text:

```
    if current == "\\u0000":
        result = retag.RetagResult(path=path, current=current, reason=retag.NO_GENRE)
```

### `u56-catalogue-searcher-and-tag-workers.R30_specific_genre_is_overwritten`

A queued job overwrites somebody's own curation, which is the write this verb exists to avoid making

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R30_specific_genre_is_overwritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_the_report_is_derived_from_what_ran_rather_than_from_what_was_planned`

Old text:

```
    elif not declared.is_too_coarse_as_source(current):
```

New text:

```
    elif False:
```

### `u56-catalogue-searcher-and-tag-workers.R31_artifact_drops_the_previous_value`

R-185's only record: without the previous genre the artifacts stop naming which library rows went stale, so the deferred database half has no population to read

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R31_artifact_drops_the_previous_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_interrupted_retag_leaves_a_library_row_stale_and_the_artifact_recovers_it`

Old text:

```
            "current": result.current,
            "written": result.written,
```

New text:

```
            "written": result.written,
```

### `u56-catalogue-searcher-and-tag-workers.R37_artifact_named_by_item_id`

A filename built from a tagging item identifier is a path traversal wearing a report, because the identifier is a path relative to a folder

- File: `src/cratekit/tagging/artifacts.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R37_artifact_named_by_item_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_item_identifier_holding_a_separator_cannot_escape_the_directory`

Old text:

```
    directory = _job_dir(ARTIFACTS_DIRNAME, cfg, job_id)
    config._mkdir_private(directory)
    return directory / f"{ordinal:04d}.json"
```

New text:

```
    directory = _job_dir(ARTIFACTS_DIRNAME, cfg, job_id)
    config._mkdir_private(directory)
    return directory / f"{ordinal}.json"
```

### `u56-catalogue-searcher-and-tag-workers.R38_staging_not_cleared`

A half written report from an attempt that did not finish is committed by the next attempt as though it described that attempt

- File: `src/cratekit/tagging/artifacts.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R38_staging_not_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_staging_is_cleared_before_an_attempt_writes_into_it`

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)
```

New text:

```
    if False:
        shutil.rmtree(directory)
```

### `u56-catalogue-searcher-and-tag-workers.R33_no_op_job_id_is_null`

R-234 reintroduced: cli.output types job_id as a required string, so a null fails the verb's own schema on every zero path

- File: `src/cratekit/tagging/shell.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R33_no_op_job_id_is_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 9 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_holding_no_audio_queues_nothing_and_says_which_zero_it_is`
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_one_with_nothing_coarse`
  - `tests/test_tag_workers.py::test_an_empty_folder_argument_never_sweeps_the_working_directory`
  - `tests/test_tag_workers.py::test_an_empty_plan_is_still_asked_about_and_still_queues_nothing`
  - `tests/test_tag_workers.py::test_answering_the_confirmation_with_abort_queues_nothing_and_writes_nothing`
  - `tests/test_tag_workers.py::test_tagging_the_download_root_queues_nothing_from_the_acquisition_staging_tree`
  - `tests/test_tag_workers.py::test_the_honest_zero_names_an_empty_job_id_rather_than_a_null`
  - `tests/test_tag_workers.py::test_the_honest_zero_validates_against_the_job_state_surface`

Old text:

```
    return {"job_id": "", "state": state, "cause": None, "progress": {}}
```

New text:

```
    return {"job_id": None, "state": state, "cause": None, "progress": {}}
```

### `u56-catalogue-searcher-and-tag-workers.R34_empty_job_is_driven`

A job frozen with no items drives straight to SUCCEEDED, which is a clean report over work it never did

- File: `src/cratekit/tagging/shell.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R34_empty_job_is_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_job_with_no_items_is_refused_rather_than_driven`

Old text:

```
        if not jobs.items(store, job.job_id):
```

New text:

```
        if False:
```

### `u56-catalogue-searcher-and-tag-workers.R35_extra_rides_beside_progress`

A per verb detail at the top level is an undeclared field on job_state/1, so a consumer generated from the committed schema rejects every envelope

- File: `src/cratekit/tagging/shell.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R35_extra_rides_beside_progress`
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
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - ... and 32 more, see the JSON sidecar

Old text:

```
    progress = dict(jobs.progress(store, job.job_id))
    if extra:
        progress.update(extra)
    return {
        "job_id": job.job_id,
```

New text:

```
    progress = dict(jobs.progress(store, job.job_id))
    return {
        **dict(extra or {}),
        "job_id": job.job_id,
```

### `r312.W2_worker_writes_nothing`

handle_resort: the item report always says nothing was left

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W2_worker_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 8 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
            "left_behind": [rebuild.left_behind_record(entry) for entry in left],
```

New text:

```
            "left_behind": [],
```

### `r312.W3_success_exit_silent`

_resume: the success envelope carries no leftover warning

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W3_success_exit_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
                *rebuild.left_behind_warnings(records, listed_in=listed_in),

```

New text:

```
(empty)
```

### `r312.W4_failure_exit_silent`

_resume: a refusal is re-raised as it came, the leftovers never added to it

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W4_failure_exit_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left`

Old text:

```
        raise _with_left_behind(failed, frozen, job.job_id) from failed
```

New text:

```
        raise
```

### `r312.W5_cause_steps_replaced`

_with_left_behind: replace the recorded steps with the leftover step, not append to them

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W5_cause_steps_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left`

Old text:

```
                cause.remediation, steps=(*cause.remediation.steps, message)
```

New text:

```
                cause.remediation, steps=(message,)
```

### `r312.W7b_pre_drive_refusal_extended`

_resume: drop the guard that re-raises a refusal raised before the drive. Measured ZERO on the first pass over a full run of 9679, then re-measured after test_a_refusal_raised_before_the_drive_carries_no_leftover_step was written against it

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W7b_pre_drive_refusal_extended`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`

Old text:

```
        if frozen is None:
            raise
        raise _with_left_behind
```

New text:

```
        raise _with_left_behind
```

### `r312.W8_list_not_by_job`

_left_behind: point at the shared reports directory, not this job's

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W8_list_not_by_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
    return records, str(jobs.store_dir(cfg) / RESORT_ARTIFACTS.final / job_id)
```

New text:

```
    return records, str(jobs.store_dir(cfg) / RESORT_ARTIFACTS.final)
```

### `r318-b.C7_trees_not_deduplicated`

_skipped_files: a tree the writer skipped a file in twice is listed twice

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318-b.json`, row `C7_trees_not_deduplicated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_file_skipped_twice_in_one_tree_names_that_tree_once`

Old text:

```
                "trees": sorted(set(tree_ids)),
```

New text:

```
                "trees": sorted(tree_ids),
```

### `r318-b.N1_no_native_key_dropped`

apply_inbox: the no-native-tree answer carries no skipped_files key, so the payload shape differs by branch

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318-b.json`, row `N1_no_native_key_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_on_a_library_with_no_native_tree_says_so`

Old text:

```
            "skipped": 0,
            "skipped_files": [],
        }
```

New text:

```
            "skipped": 0,
        }
```

### `r318-b.W2_cap_halved`

Halve the cap on how many skipped files a warning names, 10 to 5

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318-b.json`, row `W2_cap_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_skip_warning_counts_every_file_and_caps_the_names`

Old text:

```
SKIPPED_NAMED = 10
```

New text:

```
SKIPPED_NAMED = 5
```

### `r318.C1_skipped_files_always_empty`

apply_inbox: skipped_files is always empty, the headline defect R-318 measured, a count and no file

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C1_skipped_files_always_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_the_human_output_names_the_skipped_file`

Old text:

```
        "skipped_files": _skipped_files(cfg, rows, missed),
```

New text:

```
        "skipped_files": [],
```

### `r318.C2_tombstones_not_consulted`

_skipped_files: match against the live index instead of the tombstoned one, so withdrawn can never be told from not imported

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C2_tombstones_not_consulted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`

Old text:

```
        paths, index.by_tombstoned_location, root=cfg.library.root, prefix_map=rules
```

New text:

```
        paths, index.by_active_location, root=cfg.library.root, prefix_map=rules
```

### `r318.C3_ambiguous_ids_dropped`

_skipped_files: an ambiguous file names no rows, so a person cannot see which two rows to choose between

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C3_ambiguous_ids_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`

Old text:

```
            ids = alive.content_ids
        elif
```

New text:

```
            ids = ()
        elif
```

### `r318.C4_withdrawn_ids_dropped`

_skipped_files: a withdrawn file names no tombstoned row

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C4_withdrawn_ids_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`

Old text:

```
            ids = dead.content_ids or ((dead.content_id,) if dead.content_id else ())
```

New text:

```
            ids = ()
```

### `r318.C5_withdrawn_single_id_dropped`

_skipped_files: a withdrawn file with ONE tombstone names nothing, only the ambiguous-tombstone ids survive

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C5_withdrawn_single_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`

Old text:

```
            ids = dead.content_ids or ((dead.content_id,) if dead.content_id else ())
```

New text:

```
            ids = dead.content_ids
```

### `r318.C6_trees_emptied`

_skipped_files: the record names no tree it was declared into

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C6_trees_emptied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - `tests/test_routing_workers.py::test_a_file_skipped_twice_in_one_tree_names_that_tree_once`

Old text:

```
                "trees": sorted(set(tree_ids)),
```

New text:

```
                "trees": [],
```

### `r318.C8_path_reduced_to_name`

_skipped_files: the payload carries the file name instead of the full path

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C8_path_reduced_to_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`

Old text:

```
                "path": path,
```

New text:

```
                "path": Path(path).name,
```

### `r318.C9_warnings_not_emitted`

route_inbox: the skip warnings never reach the envelope, so the human output, which prints warnings and no totals, names no file

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C9_warnings_not_emitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_the_human_output_names_the_skipped_file`

Old text:

```
                *skipped_warnings(result["skipped_files"]),
```

New text:

```
(empty)
```

### `r318.W1_cap_not_applied`

skipped_warnings: name every file, the cap never applied

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W1_cap_not_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_skip_warning_counts_every_file_and_caps_the_names`

Old text:

```
        named = names[:SKIPPED_NAMED]
```

New text:

```
        named = names
```

### `r318.W3_count_is_named_not_whole`

skipped_warnings: the count is the number named rather than the whole set, so a long list reads as a short one

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W3_count_is_named_not_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_skip_warning_counts_every_file_and_caps_the_names`

Old text:

```
                    f"{len(names)} file(s) in the intake folder were not filed because "
```

New text:

```
                    f"{len(named)} file(s) in the intake folder were not filed because "
```

### `r318.W4_reasons_unsorted`

skipped_warnings: reasons in arrival order, so two runs over one state say things in two orders

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W4_reasons_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_skip_warnings_are_one_per_reason_in_a_stable_order`

Old text:

```
    for reason in sorted(by_reason):
```

New text:

```
    for reason in by_reason:
```

### `r318.W5_next_act_dropped`

skipped_warnings: the reason sentence and its next act are replaced by a bare phrase

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W5_next_act_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`

Old text:

```
        why = SKIP_NEXT_ACT[routing_pass.Placement(reason)]
```

New text:

```
        why = "of its state"
```

### `u132.W6_resort_note`

The resort resume carries no skipped step note

- File: `src/cratekit/write/routing_cli.py`
- Source: `u132.json`, row `W6_resort_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`

Old text:

```
                *rebuild.favorites_skipped_warnings(declared, driven),

```

New text:

```
(empty)
```

### `u155.W3_gate_column`

_column: show a genre sub placement in the energy sub column, the round 1 defect

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W3_gate_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_unplaced_export_names_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
    if routing.genre_sub_named(declared, placement.bucket, placement.sub):
        return genre
```

New text:

```
(empty)
```

### `u155.W4_gate_count`

_placed_counts: count no track as filed into a genre sub

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W4_gate_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_gate_counts_tracks_filed_into_a_genre_sub`

Old text:

```
        "genre sub": sum(1 for item in tracks if item.get("genre")),
```

New text:

```
        "genre sub": 0,
```

