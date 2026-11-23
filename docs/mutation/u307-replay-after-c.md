# Mutation table: u307-replay-after-c

Measured by `scripts/mutate.py` on 2026-11-22 23:35 UTC, branch `HEAD` at `59f66e86`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22539 collected. pytest invocations for this batch: 319.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 54, each measured by this driver.

Known failures: 252 node ids whose failure is this machine's and not the tree's, read from `/tmp/known-u307.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22539 against 22539. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r502-a.G5_no_adjudicate` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 4 | killed |
| `r502-a.G6_no_mount_guard` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r502-a2.G7_frozen_config` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r502-b.E2_nothing_written_refusal` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r502-b.G10_since_keys_swapped` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 5 | killed |
| `r502-b.G12_since_check_detail` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r502-b.G9_missing_count_stale` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r502-b2.G13_written_line_for_gained` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r503-a.G10_owned_key` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 86 | killed |
| `r503-a.G1_no_lookup` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 3 | killed |
| `r503-a.G2_found_is_answered` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r503-a.G4_offered_not_decremented` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 3 | killed |
| `r503-a.G5_state_not_counted` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r503-a.G6_answered_not_counted` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 3 | killed |
| `r503-a.G7_answered_read_as_since` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 3 | killed |
| `r503-a.G8_rejected_not_kept` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r503-a.G9_answered_last` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r503-b.E2_offered_listed` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r503-b.G11_summary` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 3 | killed |
| `r503-b.G12_answered_check` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r503-b.G13_offered_check` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r503-b.G14_no_gone` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r503-b.G15_no_new` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r503-b.G16_json_uncaught` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r503-b.G17_no_hint` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r679-b.D5_missing_per_row_gate_on_question_alone` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 830 | 1 | killed |
| `u110-c.C5_missing_hint` | `src/cratekit/intake/missing_cli.py` | user | 5 file(s) | 187 | 1 | killed |
| `u207.I1_missing_never_screens` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 40 | 1 | killed |
| `u212.M10_left_out` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u212.M1_staged_match` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 5 | killed |
| `u212.M2_own_rows_both` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 3 | killed |
| `u212.M3_own_rows_by_id` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u212.M4_own_rows_by_isrc` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u212.M5_unread_is_empty` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u212.M6_absent_folder` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u212.M7_outcome_staged` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u212.M8_summary_count` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 4 | killed |
| `u212.M9_unread_status` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u69-b.M10_out_not_a_folder` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69-b.M12_unlisted_status` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69-b.M17_lists_folder` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 3 | killed |
| `u69-b.M18_inner_cause` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69-b.M19_resume_step` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69.M1_handler_key` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69.M2_succeeded_only` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `u69.M4_report_coverage` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69.M5_by_count` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69.M6_state_word` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73-b.B2_every_ref_kept` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73-b.B3_first_source_wins` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A10_every_job_skipped` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A1_blank_run` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A2_library_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A3_run_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A4_intake_key_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A5_oldest_first` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `u73.A7_open_refuses` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A8_failed_refuses` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A9_skip_failed_ignored` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `u78-a.A3_several_listed` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 48 | 2 | killed |
| `u78-a.A5_outage_read_as_none` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 48 | 1 | killed |
| `u78-a.A6_blank_id_dropped` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 48 | 1 | killed |
| `u78-b.B1_unwritable_refuses_whole` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 48 | 2 | killed |
| `u78-b.B3_ids_unsorted` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 48 | 1 | killed |
| `u78-d.A4_cratekit_error_passthrough_again` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 48 | 1 | killed |
| `u79-c.C3_accepted_held_listed_again` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 98 | 1 | killed |
| `u79-c.C4_nothing_found_is_a_no_op` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 98 | 2 | killed |
| `u79-c.C5_foreign_ref_names_a_row` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 98 | 2 | killed |
| `u79-c.C6_isrc_named_keeps_origin` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 98 | 1 | killed |
| `u79-c.C7_fixed_name` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 98 | 10 | killed |
| `u79-c.C8_asked_is_a_no_op` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 98 | 1 | killed |
| `r432-a.A1_key_casefold` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 89 | 3 | killed |
| `r432-a.A2_key_normalization` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 89 | 1 | killed |
| `r432-a.A3_lock_never_taken` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 89 | 17 | killed |
| `r432-a.A5_not_retryable` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 89 | 2 | killed |
| `r432-a.A7_holder_unreadable_name` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 89 | 1 | killed |
| `r432-a.A8_holder_left_out` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 89 | 2 | killed |
| `r432-a.A9_body_refusal_translated` | `src/cratekit/intake/landing.py` | maintainer | 3 file(s) | 89 | 1 | killed |
| `r432-b.A4c_lock_outlives_its_with` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 89 | 8 | killed |
| `r677.E1_export_asked_before_the_library` | `src/cratekit/intake/landing.py` | user | 5 file(s) | 192 | 69 | killed |
| `r677.E2_library_check_dropped` | `src/cratekit/intake/landing.py` | user | 5 file(s) | 192 | 5 | killed |
| `r677.E3_intake_file_check_dropped` | `src/cratekit/intake/landing.py` | user | 5 file(s) | 192 | 4 | killed |
| `r685-a.V2_composite_a_landing_under_an_alias` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 23 | 1 | killed |
| `r685-a.V2_landing_preflight_reads_the_shipped_text` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 41 | 2 | killed |
| `r746-b.N8_unsupported_file_moved_anyway` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 83 | 1 | killed |
| `r746-b.N9_placement_check_dropped_from_the_screen` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 110 | 3 | killed |
| `u110-c.C1_apply_playlist` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 198 | 8 | killed |
| `u110-c.C7_intake_lock_prefix` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 198 | 13 | killed |
| `u110-c.C8_plain_dot` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 198 | 3 | killed |
| `u113-b.B5_export_clash_unasked` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 65 | 1 | killed |
| `u113-b.B6_root_names_unheld` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 26 | 1 | killed |
| `u113-c.C6_names_checked_after_moves` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 60 | 1 | killed |
| `u128-b.B1_engine_stale_unchecked` | `src/cratekit/intake/landing.py` | user | 10 file(s) | 268 | 1 | killed |
| `u128-b.B2_foreign_host_indexed` | `src/cratekit/intake/landing.py` | user | 10 file(s) | 268 | 1 | killed |
| `u156.L25_shared_rule_near_match` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 69 | 1 | killed |
| `u164.W1_apply_folder` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 50 | 24 | killed |
| `u164.W2_preflight_target` | `src/cratekit/intake/landing.py` | maintainer | 2 file(s) | 50 | 1 | killed |
| `u71-b.B10_occupied_at_move` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 2 | killed |
| `u71-b.B11_nothing_moved` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71-b.B12_take_back_folder` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71-b.B1_target_under_staging` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71-b.B2_device` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71-b.B3_destination_exists` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71-b.B4_export_missing` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71-b.B5_trial_splice` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71-b.B6_trial_playlist` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71-c.C1_nothing_movable_rerun` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71.A10_root_absent` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71.A11_owned_folder` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71.A12_staging_inside_library` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 2 | killed |
| `u71.A1_listing_dotfile` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71.A2_listing_suffix` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 2 | killed |
| `u71.A3_listing_regular_file` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71.A4_digest_names_only` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 2 | killed |
| `u71.A5_digest_no_mtime` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 2 | killed |
| `u71.A6_stale_refusal` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 3 | killed |
| `u71.A7_stale_listing_only` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 2 | killed |
| `u71.A9_plan_empty` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u72-b.M23_listing_unfiltered` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 27 | 1 | killed |
| `u77-a.A1_label_source_filter` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 1 | killed |
| `u77-a.A2_engine_stale_digest` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 16 | killed |
| `u77-a.A4_export_reason_mapping` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 2 | killed |
| `u77-a.A5_needs_review_guard` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 1 | killed |
| `u77-a.A6_no_landed_file_guard` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 5 | killed |
| `u77-a.A7_year_absent_guard` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 1 | killed |
| `u77-a.A8_library_template` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 1 | killed |
| `u77-a.A9_this_runs_files_only` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 1 | killed |
| `u77-a2.A2_engine_stale_digest` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 1 | killed |
| `u77-b.B1_reported_ids_deduped` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 1 | killed |
| `u77-b.B2_disk_refusal_reported` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 1 | killed |
| `u77-b.B3_index_refusal_reported` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 1 | killed |
| `u77-b.B5_unmatched_sentence` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 255 | 1 | killed |
| `r1017.M3_landing_open_read` | `src/cratekit/intake/set_playlist.py` | user | 4 file(s) | 174 | 1 | killed |
| `r1017.M4_landing_uncommitted_read` | `src/cratekit/intake/set_playlist.py` | user | 4 file(s) | 174 | 1 | killed |
| `r1017.M5_landing_any_job` | `src/cratekit/intake/set_playlist.py` | user | 4 file(s) | 174 | 2 | killed |
| `r1017.M6_oldest_first` | `src/cratekit/intake/set_playlist.py` | user | 4 file(s) | 174 | 1 | killed |
| `r1017.M7_names_not_deduplicated` | `src/cratekit/intake/set_playlist.py` | maintainer | 4 file(s) | 174 | 1 | killed |
| `u121-b.S10r_folder_row_removed` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-b.S14r_stale_digest` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-b.S15r_member_order` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-c.S2c_separator` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 2 | killed |
| `u121-d.D1_record_ignored` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-d.D2_removed_namesake` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 2 | killed |
| `u121-d.D3_repeated_row_counted_twice` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-d.D4_record_on_nothing` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-d.D5_left_dropped_when_nothing_written` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-d.D6_recorded_but_removed` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121.S11_landed_by_target` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 13 | killed |
| `u121.S17_unresolved_dropped` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 4 | killed |
| `u121.S1_uploader_prefix` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 2 | killed |
| `u121.S3_answer_not_read` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121.S4_page_beats_flag` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121.S5_missing_word` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 6 | killed |
| `u121.S7_job_handler` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121.S8_job_state` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121.S9_two_folders` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u129-author.A18_frozen_name_ignored` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 20 | 2 | killed |
| `u135.A12_inspiration_join_broken` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 9 | 1 | killed |
| `u144-c.C9_parent_of_named` | `src/cratekit/intake/set_playlist.py` | user | 2 file(s) | 95 | 10 | killed |
| `u246.S3_set_playlist_order_set_empty` | `src/cratekit/intake/set_playlist.py` | user | 5 file(s) | 293 | 22 | killed |
| `u246.S4_set_playlist_order_set_read_back` | `src/cratekit/intake/set_playlist.py` | user | 5 file(s) | 293 | 1 | killed |
| `u154.G10_read_back_path_unchecked` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G11_kept_columns_unchecked` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G14_reserved_folders_are_candidates` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G15_stored_target_under_mounted_path` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G17_refusal_before_rename_rewrapped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G1_policy_not_registered` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 5 | killed |
| `u154.G2_confinement_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G3_rename_back_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 2 | killed |
| `u154.G4_stale_target_check_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G5_unmatched_file_shelved_anyway` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G6_subfolder_check_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G7_run_id_shape_unread` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 4 | killed |
| `u154.G8_free_target_no_suffix` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 3 | killed |
| `u154.R1_rows_under_target_not_consulted` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.R3_repeated_name_planned_twice` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.R6_device_probe_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.R7_exact_prefix_filter_dropped` | `src/cratekit/intake/shelve.py` | maintainer | 1 file(s) | 23 | 1 | killed |
| `u164.T1_filed_target` | `src/cratekit/intake/shelve.py` | user | 4 file(s) | 98 | 33 | killed |
| `u164.T2_free_disk` | `src/cratekit/intake/shelve.py` | user | 2 file(s) | 29 | 3 | killed |
| `u164.T3_free_stored` | `src/cratekit/intake/shelve.py` | user | 2 file(s) | 50 | 2 | killed |
| `u164.T4_undated_name` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 6 | 1 | killed |
| `u164.T5_empty_subject` | `src/cratekit/intake/shelve.py` | user | 2 file(s) | 29 | 1 | killed |
| `u164.T6_reuse_recorded` | `src/cratekit/intake/shelve.py` | user | 3 file(s) | 75 | 5 | killed |
| `u164.T7_reuse_gone` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 6 | 1 | killed |
| `u235.H1_shelve_four_hex_only` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 2 | killed |
| `u235.H2_shelve_sixteen_hex_only` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 2 | killed |
| `r501-b.I1_rollback_abandon` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 134 | 3 | killed |
| `r501-b.I2_rollback_unlink` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 134 | 1 | killed |
| `r501-b.I3_rollback_fresh_only` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 134 | 1 | killed |
| `r501-b.I4_mark_awaiting` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 134 | 23 | killed |
| `r685-b.P1_place_files_rereads_the_registry` | `src/cratekit/intake/ingest.py` | maintainer | 1 file(s) | 23 | 1 | killed |
| `r740-b.I1_tag_key_first` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 86 | 3 | killed |
| `r740-b.I3_stem_is_the_title` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 86 | 2 | killed |
| `r740-b.I4_lossy_is_the_parameter` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 86 | 1 | killed |
| `r740-b.I5_body_marker_marks` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 86 | 1 | killed |
| `r740-c.I2_no_stem_fallback` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 86 | 1 | killed |
| `r770-a.A1_switch_reads_the_other_mode` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 77 | 57 | killed |
| `r770-a.A2_unreachable_root_is_read_anyway` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 60 | 3 | killed |
| `r770-a.A3_assertion_refuses_nothing` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-a.A4_refusal_asks_for_a_defect_report` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-a.A5_tree_built_without_the_refusal` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-a.A6_splice_asks_only_after_the_export` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 1 | killed |
| `u113-b.B2_batch_keeps_claimed` | `src/cratekit/intake/ingest.py` | user | 3 file(s) | 73 | 9 | killed |
| `u113-b.B3_record_unnamed` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 26 | 3 | killed |
| `u113-b.B4_steps_name_one` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 53 | 1 | killed |
| `u128-b.B4_bridge_owned_dropped` | `src/cratekit/intake/ingest.py` | user | 8 file(s) | 201 | 1 | killed |
| `u128-b.B5_bridge_record_no_account` | `src/cratekit/intake/ingest.py` | user | 8 file(s) | 201 | 2 | killed |
| `u37-author-light.G4_staging` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 8 | 1 | killed |
| `r924.F1_no_start_line` | `src/cratekit/intake/fetch.py` | user | 2 file(s) | 52 | 2 | killed |
| `r924.F2_no_landed_line` | `src/cratekit/intake/fetch.py` | user | 2 file(s) | 52 | 1 | killed |
| `r924.F4_sum_not_largest` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 11 | 1 | killed |
| `r924.F5_watcher_not_joined` | `src/cratekit/intake/fetch.py` | maintainer | 1 file(s) | 22539 | 0 (promoted) | zero |
| `u104-a.F1_guard_string_layer` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-a.F2_guard_samefile_layer` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-a.F3_guard_absent_library_return` | `src/cratekit/intake/fetch.py` | maintainer | 1 file(s) | 41 | 1 | killed |
| `u104-a.F4_landing_inside_scratch` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-b.F5_landing_is_a_file` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-b.F6_clear_before_attempt` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-b.F7_remove_on_exit` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 11 | killed |
| `u104-b.F8_leftover_recorded` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-b.F9_scratch_prepare_is_its_own_kind` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-c.P1_numbered_output` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-c.P2_probe_bound` | `src/cratekit/intake/fetch.py` | maintainer | 1 file(s) | 41 | 1 | killed |
| `u104-c.P3_several_threshold` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-c.P4_timeout_is_its_own_kind` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-c.P5_stem_bound` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-c.P6_address_is_stripped` | `src/cratekit/intake/fetch.py` | maintainer | 1 file(s) | 41 | 1 | killed |
| `u121.S18_info_json_flag` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u166.C10_live_filter` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1041 | 5 | killed |
| `u166.C1_removed_row` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1041 | 1 | killed |
| `u166.C2_analysed_flag` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1041 | 1 | killed |
| `u166.C3_analysis_path` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1041 | 1 | killed |
| `u166.C4_blank_path` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1041 | 1 | killed |
| `u166.C5_missing_row` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1041 | 1 | killed |
| `u166.C6_stale_check` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1041 | 1 | killed |
| `u166.C7_clear_waits_too` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1041 | 3 | killed |
| `u166.C8_read_back_lost` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1041 | 1 | killed |
| `u166.C9_read_back_kept` | `src/cratekit/intake/analyzed.py` | user | 3 file(s) | 1041 | 2 | killed |
| `u259.M1_judge_no_row` | `src/cratekit/intake/analyzed.py` | user | 2 file(s) | 84 | 6 | killed |
| `u259.M5_member_reads_nothing` | `src/cratekit/intake/analyzed.py` | user | 2 file(s) | 84 | 16 | killed |
| `r770-b.B5_file_verb_never_takes_the_native_path` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 16 | killed |
| `r770-b.B6_export_taken_on_a_native_tree` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-b.B7_staging_not_asked_first` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-b.B8_target_spelled_as_resolved` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-c.C1_unplaceable_file_reaches_the_gate` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-c.C2_untyped_suffix_reaches_the_gate` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-c.C5_playlist_named_for_the_whole_file_name` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 3 | killed |
| `r770-d.C6_digest_without_the_collection_plan` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u154.G12_empty_plan_asks_a_gate` | `src/cratekit/intake/shelve_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G13_as_with_all_admitted` | `src/cratekit/intake/shelve_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.R2_subject_path_part_admitted` | `src/cratekit/intake/shelve_cli.py` | user | 1 file(s) | 23 | 1 | killed |
| `u164.S1_already_filed` | `src/cratekit/intake/shelve_cli.py` | user | 2 file(s) | 29 | 1 | killed |
| `u164.S2_music_folder_wins` | `src/cratekit/intake/shelve_cli.py` | user | 2 file(s) | 29 | 6 | killed |
| `r1255.F2_refill_warning_wording` | `src/cratekit/intake/refill_cli.py` | user | 2 file(s) | 28 | 2 | killed |
| `u134-b.B5_no_writes_no_op` | `src/cratekit/intake/refill_cli.py` | user | 1 file(s) | 13 | 3 | killed |
| `u134-b.B6_ack_before_gate` | `src/cratekit/intake/refill_cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `u144-c.C8_question_named` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 39 | 1 | killed |
| `r770-c.C3_failure_past_the_gate_loses_its_reason` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-c.C4_failure_past_the_gate_loses_its_remedy` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r706-c.C4_pipeline_drops_parts` | `src/cratekit/intake/pipeline.py` | user | 1 file(s) | 67 | 1 | killed |
| `u103-b.P2_digest_reaches_the_verb` | `src/cratekit/intake/pipeline.py` | user | 1 file(s) | 67 | 1 | killed |

## Zero rows and what they owe

- `r924.F5_watcher_not_joined` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `r502-a.G5_no_adjudicate`

Skip reading a person's answer back, so a row answered as another track reads as a fresh question and drops out

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-a.json`, row `G5_no_adjudicate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    if asked:
        with review.open_store(cfg) as items:
            for handler_key, at in asked.items():
```

New text:

```
    if False:
        with review.open_store(cfg) as items:
            for handler_key, at in asked.items():
```

### `r502-a.G6_no_mount_guard`

Drop the absent music folder refusal before the library walk

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-a.json`, row `G6_no_mount_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`

Old text:

```
    if not music.is_dir():
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no track "
```

New text:

```
    if False:
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no track "
```

### `r502-a2.G7_frozen_config`

Ask the library at the root the first job froze rather than the current configuration (the review's finding)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-a2.json`, row `G7_frozen_config`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it`

Old text:

```
    cfg = intake_cli._load()
    music = Path(cfg.library.root) / cfg.library.music_dir
```

New text:

```
    cfg = jobs.frozen_config(origins[0])
    music = Path(cfg.library.root) / cfg.library.music_dir
```

### `r502-b.E2_nothing_written_refusal`

Existing guard sample: drop the refusal for missing tracks none of which could be written

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `E2_nothing_written_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_missing_tracks_none_named_and_none_writable_refuse_rather_than_no_op`

Old text:

```
    if missing and not listed and not in_file:
```

New text:

```
    if False:
```

### `r502-b.G10_since_keys_swapped`

Count a row held since under suppressed_since and a row deleted since under owned_since

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `G10_since_keys_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_whose_rows_were_all_acquired_since_names_no_download`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
    match.MatchState.MATCHED: "owned_since",
    match.MatchState.SUPPRESSED: "suppressed_since",
```

New text:

```
    match.MatchState.MATCHED: "suppressed_since",
    match.MatchState.SUPPRESSED: "owned_since",
```

### `r502-b.G12_since_check_detail`

Reword the since check so it no longer names the rows in the library since

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `G12_since_check_detail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
            f"{since['owned_since']} in the library since, {since['suppressed_since']} "
```

New text:

```
            f"{since['owned_since']} held now, {since['suppressed_since']} "
```

### `r502-b.G9_missing_count_stale`

Report the job's missing count rather than the count still missing now

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `G9_missing_count_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
        counts["missing"] = len(missing)

```

New text:

```
(empty)
```

### `r502-b2.G13_written_line_for_gained`

Drop the written line's gained branch, so a job whose rows were all gained reads as a job with nothing missing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b2.json`, row `G13_written_line_for_gained`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
    elif gained:
        said = (
```

New text:

```
    elif False:
        said = (
```

### `r503-a.G10_owned_key`

File an answered row now owned under answered_missing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G10_owned_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 86 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_credited_row_never_withholds_another_remix_of_the_recording`
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac-tags1-row1]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[07A - 128 - Traumer, antraum, Anton - Hyaku.flac-tags2-row2]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[08A - 124 - Aurora Bloom - Sun Path.flac-tags0-row0]`
  - `tests/test_intake_missing.py::test_a_job_with_nothing_missing_is_no_op_and_writes_nothing`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`
  - `tests/test_intake_missing.py::test_a_run_whose_rows_were_all_acquired_since_names_no_download`
  - `tests/test_intake_missing.py::test_a_run_with_nothing_missing_and_nothing_skipped_is_a_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_track_deleted_on_purpose_is_suppressed_and_not_listed`
  - ... and 71 more, see the JSON sidecar

Old text:

```
    match.MatchState.MATCHED: "answered_owned",
```

New text:

```
    match.MatchState.MATCHED: "answered_missing",
```

### `r503-a.G1_no_lookup`

Read no answer at all, so every offered row stays offered whatever a person said (R-503 as filed)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G1_no_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    answered = iter(_answered(offered))
```

New text:

```
    answered = iter([False] * len(offered))
```

### `r503-a.G2_found_is_answered`

Treat an item that exists as answered, so an unanswered row is asked again and offered again from the listing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G2_found_is_answered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`

Old text:

```
            said.append(held is not None and held.resolved)
```

New text:

```
            said.append(held is not None)
```

### `r503-a.G4_offered_not_decremented`

Leave an answered row in the offered count, so a rejected row still reads offered 1

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G4_offered_not_decremented`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
                counts["offered"] -= 1

```

New text:

```
(empty)
```

### `r503-a.G5_state_not_counted`

Do not count an answered row under the word it resolved to, so an accepted row is not owned

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G5_state_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
                counts[_WORD[one.state]] += 1

```

New text:

```
(empty)
```

### `r503-a.G6_answered_not_counted`

Do not count answered rows under answered_*

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G6_answered_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
                now_answered[_ANSWERED[one.state]] += 1

```

New text:

```
(empty)
```

### `r503-a.G7_answered_read_as_since`

Count an answered row as a missing row would be counted, under since, rather than as answered

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G7_answered_read_as_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
            if report["state"] == "offered":
                # COUNTED
```

New text:

```
            if report["state"] == "never":
                # COUNTED
```

### `r503-a.G8_rejected_not_kept`

Keep only rows the job found missing, so a rejected row is counted and never listed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G8_rejected_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
            if one.state is match.MatchState.MISSING:
                kept.append(n)
```

New text:

```
            if one.state is match.MatchState.MISSING and report["state"] == "missing":
                kept.append(n)
```

### `r503-a.G9_answered_last`

Ask answered rows after missing ones, so a rejected row is listed out of its playlist order

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G9_answered_last`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    asking = [
        (job, report)
        for job, report in rows_in
        if report["state"] == "missing" or next(answered)
    ]
```

New text:

```
    asking = sorted(
        [
            (job, report)
            for job, report in rows_in
            if report["state"] == "missing" or next(answered)
        ],
        key=lambda pair: pair[1]["state"] == "offered",
    )
```

### `r503-b.E2_offered_listed`

Existing: list every offered report as missing without asking, the shape the brief forbids

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `E2_offered_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`

Old text:

```
        if report["state"] == "missing" or next(answered)
```

New text:

```
        if report["state"] == "missing" or next(answered) or True
```

### `r503-b.G11_summary`

Drop the answered_* counts from the summary

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G11_summary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
        **now_answered,

```

New text:

```
(empty)
```

### `r503-b.G12_answered_check`

Reword the answered check's breakdown

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G12_answered_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
            f"missing, {now_answered['answered_owned']} in the library, "
```

New text:

```
            f"listed, {now_answered['answered_owned']} owned, "
```

### `r503-b.G13_offered_check`

Reword the offered check's route back to this listing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G13_offered_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`

Old text:

```
            f"see: crate review list, then list this again",
```

New text:

```
            f"see: crate review list",
```

### `r503-b.G14_no_gone`

Never name the tracks the earlier list holds and this one does not

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G14_no_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
    if gone:
        why.append(
```

New text:

```
    if False:
        why.append(
```

### `r503-b.G15_no_new`

Never name the tracks this list holds and the earlier one does not

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G15_no_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    if new:
        why.append(
```

New text:

```
    if False:
        why.append(
```

### `r503-b.G16_json_uncaught`

Let an earlier file that is not JSON escape the hint as an internal error

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G16_json_uncaught`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`

Old text:

```
    except (OSError, ValueError, KeyError, TypeError):
        return []
```

New text:

```
    except (OSError, KeyError, TypeError):
        return []
```

### `r503-b.G17_no_hint`

Drop the hint read from the earlier file altogether

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G17_no_hint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
        why = _changed_since(out, name, rows)
```

New text:

```
        why = []
```

### `r679-b.D5_missing_per_row_gate_on_question_alone`

missing pass, per row grouping: gate on the needs-review state alone while the other call site still names the predicate

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r679-b.json`, row `D5_missing_per_row_gate_on_question_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 830 against a baseline of 830
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_caller_of_adjudicate_gates_on_the_rows_that_touch_the_queue`

Old text:

```
        if match_cli.touches_the_queue(one):
```

New text:

```
        if one.state is match.MatchState.NEEDS_REVIEW:
```

### `u110-c.C5_missing_hint`

intake missing --run prints --name RUN again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u110-c.json`, row `C5_missing_hint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
f"--pass {name}, adding
```

New text:

```
f"--name {name}, adding
```

### `u207.I1_missing_never_screens`

intake missing: the askable codes are never screened

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u207.json`, row `I1_missing_never_screens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_intake_missing_isrc.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_intake_missing_screens_the_codes_it_will_ask_before_asking_any`

Old text:

```
        found.screen_isrcs(askable)

```

New text:

```
(empty)
```

### `u212.M10_left_out`

missing_cli._listed: drop the staged clause of the left out refusal, so a run with a failed job and every finished row staged refuses

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M10_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok`

Old text:

```
    if left_out and not listed and not unlisted and not staged_rows:
```

New text:

```
    if left_out and not listed and not unlisted:
```

### `u212.M1_staged_match`

missing_cli._staged: never record a staged row, so a track a staged file carries is listed and downloaded again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M1_staged_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[204.flac]`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[Lumen Drift - Salt Road.flac]`
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[neither]`

Old text:

```
        if held:
            found.append((n, held[0].path))
```

New text:

```
        if held and False:
            found.append((n, held[0].path))
```

### `u212.M2_own_rows_both`

missing_cli._staged: drop the own rows rule, so a continued pass subtracts its own staged downloads and its list is refused over its earlier copy

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M2_own_rows_both`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-isrc]`
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-provider-id]`

Old text:

```
        if (ref and ref in ids) or token in isrcs:
            continue
```

New text:

```
        if False:
            continue
```

### `u212.M3_own_rows_by_id`

missing_cli._staged: the own rows rule by ISRC alone, the provider id half removed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M3_own_rows_by_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-provider-id]`

Old text:

```
        if (ref and ref in ids) or token in isrcs:
```

New text:

```
        if token in isrcs:
```

### `u212.M4_own_rows_by_isrc`

missing_cli._staged: the own rows rule by provider id alone, the ISRC half removed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M4_own_rows_by_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-isrc]`

Old text:

```
        if (ref and ref in ids) or token in isrcs:
```

New text:

```
        if ref and ref in ids:
```

### `u212.M5_unread_is_empty`

missing_cli._staged: an unreadable staging folder read as one holding nothing, so the staged row says nothing failed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M5_unread_is_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`

Old text:

```
        return _Staged(folder, unread=str(exc.strerror or exc))
```

New text:

```
        return _Staged(folder)
```

### `u212.M6_absent_folder`

missing_cli._staged: drop the absent folder guard, so a machine with no staging folder yet reports the folder unreadable

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M6_absent_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`

Old text:

```
        if not folder.exists():
```

New text:

```
        if False:
```

### `u212.M7_outcome_staged`

missing_cli._listed: every row staged answers no_op, so a pass ends before the landing that takes them

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M7_outcome_staged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`

Old text:

```
        outcome=Outcome.OK if listed or unlisted or staged_rows else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if listed or unlisted else Outcome.NO_OP,
```

### `u212.M8_summary_count`

missing_cli._listed: the summary's staged count read as zero, the number the pass reads

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M8_summary_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[204.flac]`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[Lumen Drift - Salt Road.flac]`

Old text:

```
        "staged": len(staged_rows),
```

New text:

```
        "staged": 0,
```

### `u212.M9_unread_status`

missing_cli._staged_check: an unreadable staging folder said on an info row rather than a failing one

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M9_unread_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`

Old text:

```
            "staged",
            "fail",
```

New text:

```
            "staged",
            "info",
```

### `u69-b.M10_out_not_a_folder`

Drop the refusal of an --out that exists and is not a folder

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M10_out_not_a_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`

Old text:

```
    if out.exists() and not out.is_dir():
```

New text:

```
    if False:
```

### `u69-b.M12_unlisted_status`

Report unlisted missing tracks as a note instead of a failing check

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M12_unlisted_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
"fail" if unlisted else "ok",
```

New text:

```
"info" if unlisted else "ok",
```

### `u69-b.M17_lists_folder`

Write into download staging itself rather than its lists folder

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M17_lists_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_missing_tracks_none_of_which_can_be_listed_write_the_unlisted_list_not_a_no_op`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
out = intake_cli._load().paths.download_staging / LISTS_DIR
```

New text:

```
out = intake_cli._load().paths.download_staging
```

### `u69-b.M18_inner_cause`

Drop the failed job's own cause from the refusal

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M18_inner_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_failed_job_is_refused_carrying_its_own_cause`

Old text:

```
            inner=job.cause,
```

New text:

```
            inner=None,
```

### `u69-b.M19_resume_step`

Drop the resume command from an open job's refusal

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M19_resume_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_open_job_is_refused_and_nothing_is_written`

Old text:

```
            f"finish it with: crate {argv}" if job.is_open() else
```

New text:

```
            "finish it first" if job.is_open() else
```

### `u69.M1_handler_key`

Drop the refusal of a job queued under another verb's handler key

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M1_handler_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_job_of_another_verb_is_refused`

Old text:

```
    if job.handler_key not in intake_cli.INTAKE_KEYS:
```

New text:

```
    if False:
```

### `u69.M2_succeeded_only`

Drop the refusal of a job that is not succeeded (open, failed, cancelled)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M2_succeeded_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_failed_job_is_refused_carrying_its_own_cause`
  - `tests/test_intake_missing.py::test_an_open_job_is_refused_and_nothing_is_written`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
    if False:
```

### `u69.M4_report_coverage`

Drop the refusal when the reports do not cover the items one for one

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M4_report_coverage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
    if sorted(reported) != sorted(wanted):
```

New text:

```
    if False:
```

### `u69.M5_by_count`

Compare reports to items by count instead of by identifier

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M5_by_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
    if sorted(reported) != sorted(wanted):
```

New text:

```
    if len(reported) != len(wanted):
```

### `u69.M6_state_word`

Drop the refusal of a report whose state word this verb cannot read

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M6_state_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
        if report.get("state") not in _WORDS or not isinstance(report.get("track"), Mapping):
```

New text:

```
        if not isinstance(report.get("track"), Mapping):
```

### `u73-b.B2_every_ref_kept`

Stop accumulating every reference an id came from

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73-b.json`, row `B2_every_ref_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
            refs.append(said)
```

New text:

```
            pass
```

### `u73-b.B3_first_source_wins`

Let the last job an id came from win its provenance instead of the first

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73-b.json`, row `B3_first_source_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
        first.setdefault(ref, job)
```

New text:

```
        first[ref] = job
```

### `u73.A10_every_job_skipped`

Drop the refusal of a run whose every job failed, left to the layer after it

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A10_every_job_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_whose_every_job_failed_refuses_even_with_skip_failed`

Old text:

```
    if not kept:
```

New text:

```
    if False:
```

### `u73.A1_blank_run`

Drop the refusal of a blank --run, so a blank run is compared as it stands

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A1_blank_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_blank_run_is_refused_and_does_not_match_a_job_queued_with_no_run`

Old text:

```
    if not run_id.strip():
```

New text:

```
    if False:
```

### `u73.A2_library_filter`

Drop the library half of the run selection, so the run alone picks jobs

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A2_library_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
and job.library_id == library_id
```

New text:

```
and True
```

### `u73.A3_run_filter`

Drop the run half of the selection, so every intake job for the library is listed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A3_run_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
(job.payload or {}).get(RUN_ID) == run_id
```

New text:

```
True
```

### `u73.A4_intake_key_filter`

Drop the intake handler key filter, so a labels or favourites job in the run is selected

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A4_intake_key_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
            if job.handler_key in intake_cli.INTAKE_KEYS
```

New text:

```
            if True
```

### `u73.A5_oldest_first`

Reverse the job order, newest first, so first source wins picks the later playlist

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A5_oldest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
key=lambda job: (job.created, job.job_id),
```

New text:

```
key=lambda job: (job.created, job.job_id), reverse=True,
```

### `u73.A7_open_refuses`

Drop the refusal of a run holding an open job

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A7_open_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
    if still_open:
```

New text:

```
    if False:
```

### `u73.A8_failed_refuses`

Drop the refusal of a run holding a failed or cancelled job

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A8_failed_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
    if unfinished and not skip_failed:
```

New text:

```
    if False:
```

### `u73.A9_skip_failed_ignored`

Ignore --skip-failed, so a failed job refuses the run whatever the flag says

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A9_skip_failed_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`
  - `tests/test_intake_missing.py::test_a_run_whose_every_job_failed_refuses_even_with_skip_failed`

Old text:

```
    if unfinished and not skip_failed:
```

New text:

```
    if unfinished:
```

### `u78-a.A3_several_listed`

An ISRC filed under several tracks lists the first, the guess R-356 forbids

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-a.json`, row `A3_several_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_intake_missing_isrc.py::test_the_order_the_provider_answers_in_does_not_change_the_files`

Old text:

```
        elif len(answer) == 1:
```

New text:

```
        elif len(answer) >= 1:
```

### `u78-a.A5_outage_read_as_none`

A provider that could not answer is read as filing no track, so the row is handed on and the verb writes

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-a.json`, row `A5_outage_read_as_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`

Old text:

```
            except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
                raise refuse(
```

New text:

```
            except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
                answers[code] = ()
                continue
                raise refuse(
```

### `u78-a.A6_blank_id_dropped`

A track with no identifier in the answer is dropped, so one named and one unnamed reads as one id

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-a.json`, row `A6_blank_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_the_same_id_twice_in_one_answer_is_one_id_and_is_listed`

Old text:

```
    if any(not one for one in ids):
```

New text:

```
    ids = [one for one in ids if one]
    if False:
```

### `u78-b.B1_unwritable_refuses_whole`

The per row text line check before writing is removed, so one unwritable row refuses the verb again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-b.json`, row `B1_unwritable_refuses_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_track_that_cannot_be_a_text_line_is_named_and_the_rest_are_still_written`
  - `tests/test_intake_missing_isrc.py::test_missing_tracks_none_named_and_none_writable_refuse_rather_than_no_op`

Old text:

```
            try:
                listdoc.text_line(row)
            except listdoc.ListDocRefused:
```

New text:

```
            try:
                pass
            except listdoc.ListDocRefused:
```

### `u78-b.B3_ids_unsorted`

The identifiers in a several reason are written in provider order

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-b.json`, row `B3_ids_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_the_order_the_provider_answers_in_does_not_change_the_files`

Old text:

```
f"({', '.join(sorted(answer))}), and which release to download is "
```

New text:

```
f"({', '.join(answer)}), and which release to download is "
```

### `u78-d.A4_cratekit_error_passthrough_again`

A product refusal raised by the catalogue is relabelled unavailable-transient

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-d.json`, row `A4_cratekit_error_passthrough_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`

Old text:

```
            except CratekitError:
                raise
            except Exception as exc:
```

New text:

```
            except Exception as exc:
```

### `u79-c.C3_accepted_held_listed_again`

An accepted candidate the library now holds is listed for download again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C3_accepted_held_listed_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_accepted_candidate_the_library_now_holds_is_not_listed_again`

Old text:

```
            if now.state in (match.MatchState.MATCHED, match.MatchState.SUPPRESSED):
                proposals[n]
```

New text:

```
            if False:
                proposals[n]
```

### `u79-c.C4_nothing_found_is_a_no_op`

Missing rows with no route to any of them end as nothing to do

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C4_nothing_found_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_no_candidate_for_any_row_refuses_rather_than_reading_as_nothing_to_do`
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
    if unfound and not listed and not asked:
```

New text:

```
    if False:
```

### `u79-c.C5_foreign_ref_names_a_row`

Another service's identifier is read as the provider's, and the row is in no file

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C5_foreign_ref_names_a_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_missing_row_of_another_services_list_is_searched_for_and_not_dropped`
  - `tests/test_intake_missing_search.py::test_rows_asked_by_isrc_and_rows_searched_for_share_one_catalogue`

Old text:

```
    return str(wanted.ref or "").strip() if wanted.origin == match.TIDAL else ""
```

New text:

```
    return str(wanted.ref or "").strip()
```

### `u79-c.C6_isrc_named_keeps_origin`

A foreign row named by ISRC keeps its origin, so the emitter takes the ref off again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C6_isrc_named_keeps_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_rows_asked_by_isrc_and_rows_searched_for_share_one_catalogue`

Old text:

```
                named.append(replace(one, ref=answer, origin=match.TIDAL))
```

New text:

```
                named.append(replace(one, ref=answer))
```

### `u79-c.C7_fixed_name`

The found list takes one fixed name, so the run after an answer is refused

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C7_fixed_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 98 against a baseline of 98
- Kills: 10 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_one_exact_candidate_is_listed_without_review`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[.txt-txt-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[\xa7\xa7\xa7.txt-tracklist-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[friday set (2026).txt-friday-set-2026-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[intake-j1.unlisted.json-intake-j1-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[notes-notes-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[warmup.list.json-warmup-found]`
  - `tests/test_intake_missing_search.py::test_the_run_after_an_answer_lists_more_than_the_first_and_is_not_refused`
  - `tests/test_intake_missing_search.py::test_the_unlisted_list_is_read_and_its_found_list_sits_beside_the_jobs`
  - `tests/test_intake_missing_search.py::test_two_tracklists_of_one_file_name_in_two_folders_do_not_collide`

Old text:

```
    return f"{stem or 'tracklist'}{FOUND_SUFFIX}-{digest}"
```

New text:

```
    return f"{stem or 'tracklist'}{FOUND_SUFFIX}"
```

### `u79-c.C8_asked_is_a_no_op`

A run that only put a question to a person ends as nothing to do

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C8_asked_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
        outcome=Outcome.OK if listed or asked else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if listed else Outcome.NO_OP,
```

### `r432-a.A1_key_casefold`

lock_key: drop the casefold, so two spellings of one folder on a case insensitive volume each get their own lock

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A1_key_casefold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_landing.py::test_two_spellings_of_one_folder_share_one_lock[2026-09-18_ACQUIRED0]`
  - `tests/test_landing.py::test_two_spellings_of_one_folder_share_one_lock[2026-09-18_ACQUIRED1]`

Old text:

```
    folded = unicodedata.normalize("NFC", batch.casefold())
```

New text:

```
    folded = unicodedata.normalize("NFC", batch)
```

### `r432-a.A2_key_normalization`

lock_key: drop the normalization, so the composed and decomposed spellings of an accented name each get their own lock

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A2_key_normalization`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_composed_and_decomposed_spellings_share_one_lock`

Old text:

```
    folded = unicodedata.normalize("NFC", batch.casefold())
```

New text:

```
    folded = batch.casefold()
```

### `r432-a.A3_lock_never_taken`

batch_lock: hand back the lock's path without taking it, so nothing is excluded

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A3_lock_never_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 89 against a baseline of 89
- Kills: 17 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_refused_file_is_warned_and_marked`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_every_target_taken]`
  - `tests/test_landing.py::test_a_held_batch_name_refuses_a_second_holder_and_names_the_batch`
  - `tests/test_landing.py::test_a_held_job_lock_raised_under_the_batch_lock_is_not_called_a_landing`
  - `tests/test_landing.py::test_a_refusal_inside_the_batch_lock_releases_it`
  - `tests/test_landing.py::test_the_batch_lock_is_on_the_state_disk_and_a_released_one_leaves_its_file`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        path = lock.__enter__()
```

New text:

```
        path = jobs.lock_path(key, root=root)
```

### `r432-a.A5_not_retryable`

batch_lock: mark the held refusal as not retryable, though the holder ending is exactly what a retry waits for

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A5_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_landing.py::test_a_held_batch_name_refuses_a_second_holder_and_names_the_batch`

Old text:

```
            retryable=True,
            origin=_ORIGIN,
            detail={"batch": batch, "lock": str(held), "holder": who},
```

New text:

```
            retryable=False,
            origin=_ORIGIN,
            detail={"batch": batch, "lock": str(held), "holder": who},
```

### `r432-a.A7_holder_unreadable_name`

_holder: stop treating a lock file with no readable name in it as an unknown holder, so the refusal dies on a parse error instead

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A7_holder_unreadable_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_held_batch_name_refuses_a_second_holder_and_names_the_batch`

Old text:

```
    except (OSError, ValueError, TypeError, KeyError):
        return "holder unknown"
```

New text:

```
    except (OSError, TypeError, KeyError):
        return "holder unknown"
```

### `r432-a.A8_holder_left_out`

batch_lock: leave the holder out of the message, so a person is told a landing is running and not which

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A8_holder_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_landing.py::test_a_held_batch_name_refuses_a_second_holder_and_names_the_batch`

Old text:

```
            f"another landing under the batch name {batch!r} is running ({who}), "
```

New text:

```
            f"another landing under the batch name {batch!r} is running, "
```

### `r432-a.A9_body_refusal_translated`

batch_lock: translate a held job lock raised by the body as well as by the taking, so an unrelated refusal is reported as a second landing

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A9_body_refusal_translated`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_held_job_lock_raised_under_the_batch_lock_is_not_called_a_landing`

Old text:

```
    try:
        yield path
    finally:
```

New text:

```
    try:
        try:
            yield path
        except jobs.DriverHeld:
            raise refuse("job-driver-held", "a second landing", origin=_ORIGIN) from None
    finally:
```

### `r432-b.A4c_lock_outlives_its_with`

What the release tests do hold: drop the release AND keep the lock object alive, which is what a leaked lock is once the collector cannot free it

- File: `src/cratekit/intake/landing.py`
- Source: `r432-b.json`, row `A4c_lock_outlives_its_with`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`
- Collected: 89 against a baseline of 89
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_every_target_taken]`
  - `tests/test_landing.py::test_a_held_batch_name_refuses_a_second_holder_and_names_the_batch`
  - `tests/test_landing.py::test_a_refusal_inside_the_batch_lock_releases_it`
  - `tests/test_landing.py::test_the_batch_lock_is_on_the_state_disk_and_a_released_one_leaves_its_file`

Old text:

```
        lock.__exit__(None, None, None)
```

New text:

```
        globals().setdefault("_LEAKED", []).append(lock)
```

### `r677.E1_export_asked_before_the_library`

the preflight asks the export before the library, so an unmounted volume is named as a missing export

- File: `src/cratekit/intake/landing.py`
- Source: `r677.json`, row `E1_export_asked_before_the_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 69 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`
  - `tests/test_intake_imported.py::test_after_a_cutover_the_pass_placing_every_track_is_proof_and_closes_the_run`
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`
  - `tests/test_intake_imported.py::test_tracks_acknowledged_as_gone_are_not_proof_of_an_import`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_absent-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - ... and 54 more, see the JSON sidecar

Old text:

```
    _check_batch(plan.batch)
    _check_library(cfg, plan.folder, target_dir(cfg, plan.batch))
```

New text:

```
    _check_batch(plan.batch)
    _check_export(export, destination, tree_registry.read(cfg), label_rows)
    _check_library(cfg, plan.folder, target_dir(cfg, plan.batch))
```

### `r677.E2_library_check_dropped`

the preflight never asks the library

- File: `src/cratekit/intake/landing.py`
- Source: `r677.json`, row `E2_library_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`
  - `tests/test_landing.py::test_a_folder_the_library_already_owns_is_refused`
  - `tests/test_landing.py::test_a_landing_target_under_staging_is_refused`
  - `tests/test_landing.py::test_a_staging_folder_on_another_device_is_refused_by_name`
  - `tests/test_landing.py::test_an_absent_library_root_is_refused_before_the_device_probe`

Old text:

```
    _check_library(cfg, plan.folder, target_dir(cfg, plan.batch))
    if destination.exists():
```

New text:

```
    if destination.exists():
```

### `r677.E3_intake_file_check_dropped`

the preflight never asks whether the intake file is already there

- File: `src/cratekit/intake/landing.py`
- Source: `r677.json`, row `E3_intake_file_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`
  - `tests/test_landing.py::test_an_existing_intake_file_is_never_overwritten`

Old text:

```
    if destination.exists():
        raise refuse(
            "output-exists",
```

New text:

```
    if False:
        raise refuse(
            "output-exists",
```

### `r685-a.V2_composite_a_landing_under_an_alias`

What V2 holds without the guard's spelling: an aliased default loader at the preflight

- File: `src/cratekit/intake/landing.py`
- Source: `r685-a.json`, row `V2_composite_a_landing_under_an_alias`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_refuses_before_any_file_moves`

Old text:

```
    checked = Checked(registry=tree_registry.read(cfg), declared=active_taxonomy.load(cfg))

```

New text:

```
    from cratekit.core.taxonomy import default_taxonomy as shipped

    checked = Checked(registry=tree_registry.read(cfg), declared=shipped())

```

### `r685-a.V2_landing_preflight_reads_the_shipped_text`

The landing's preflight parses the shipped text, so an undeclared catalog tree is not seen

- File: `src/cratekit/intake/landing.py`
- Source: `r685-a.json`, row `V2_landing_preflight_reads_the_shipped_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`, `tests/test_landing_labels.py`
- Collected: 41 against a baseline of 41
- Kills: 2 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_no_module_but_the_loader_reads_the_shipped_template`
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_refuses_before_any_file_moves`

Old text:

```
    checked = Checked(registry=tree_registry.read(cfg), declared=active_taxonomy.load(cfg))

```

New text:

```
    checked = Checked(
        registry=tree_registry.read(cfg),
        declared=taxonomy.load_taxonomy(taxonomy.shipped_template_text("default")),
    )

```

### `r746-b.N8_unsupported_file_moved_anyway`

apply_native: a file the database has no type for is not refused per file and moves

- File: `src/cratekit/intake/landing.py`
- Source: `r746-b.json`, row `N8_unsupported_file_moved_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_landing.py`
- Collected: 83 against a baseline of 83
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`

Old text:

```
        if row.action == native.UNSUPPORTED
    }
```

New text:

```
        if False
    }
```

### `r746-b.N9_placement_check_dropped_from_the_screen`

_screen: a file whose tags resolve to no sub is moved on both media

- File: `src/cratekit/intake/landing.py`
- Source: `r746-b.json`, row `N9_placement_check_dropped_from_the_screen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_landing.py`, `tests/test_intake_land.py`
- Collected: 110 against a baseline of 110
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_landing.py::test_a_batch_where_nothing_lands_leaves_no_batch_folder`
  - `tests/test_landing.py::test_a_file_with_no_declared_sub_is_left_in_staging_naming_tag_folder`

Old text:

```
            named.get(item) or _unplaceable(item, declared) or _occupied(item, target / item.name)
```

New text:

```
            named.get(item) or _occupied(item, target / item.name)
```

### `u110-c.C1_apply_playlist`

The xml landing no longer hands its batch name to the splice, so the playlist is the intake file's stem again

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C1_apply_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 198 against a baseline of 198
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_label_go_landing_for_one_label_is_named_for_the_date_and_that_label`
  - `tests/test_intake_land_names.py::test_a_second_landing_the_same_day_gets_a_distinct_name_and_one_pass_is_never_merged`
  - `tests/test_intake_land_names.py::test_a_tidal_playlist_sync_landing_is_named_and_its_intake_file_keeps_the_pass`
  - `tests/test_intake_land_names.py::test_name_overrides_and_names_the_intake_file_when_no_pass_is_given`
  - `tests/test_landing.py::test_three_tagged_files_land_in_one_intake_file`
  - `tests/test_landing_labels.py::test_a_label_row_no_landed_file_matches_is_reported_by_name`
  - `tests/test_landing_labels.py::test_a_tree_the_disk_refuses_after_the_moves_is_named_and_the_file_stays`
  - `tests/test_landing_labels.py::test_two_labels_across_two_years_are_four_playlists_in_the_intake_file`

Old text:

```
            playlist=plan.batch,

```

New text:

```
(empty)
```

### `u110-c.C7_intake_lock_prefix`

The intake lock shares its key with a batch of the same name

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C7_intake_lock_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 198 against a baseline of 198
- Kills: 13 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_refused_file_is_warned_and_marked`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_every_target_taken]`
  - `tests/test_intake_land_names.py::test_a_landing_whose_intake_file_another_landing_is_writing_is_refused`
  - `tests/test_intake_land_names.py::test_name_overrides_and_names_the_intake_file_when_no_pass_is_given`

Old text:

```
lock_key("intake file\0" + stem)
```

New text:

```
lock_key(stem)
```

### `u110-c.C8_plain_dot`

A name starting with a dot passes the plain name rule

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C8_plain_dot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 198 against a baseline of 198
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[.hidden]`
  - `tests/test_landing.py::test_an_empty_folder_or_a_batch_name_that_is_no_plain_folder_is_refused[..]`
  - `tests/test_landing.py::test_an_empty_folder_or_a_batch_name_that_is_no_plain_folder_is_refused[.hidden]`

Old text:

```
        and not text.startswith(".")

```

New text:

```
(empty)
```

### `u113-b.B5_export_clash_unasked`

A name the export came to hold since it was chosen is not refused before the moves

- File: `src/cratekit/intake/landing.py`
- Source: `u113-b.json`, row `B5_export_clash_unasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_landing.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing`

Old text:

```
    clash = sorted(set(names) & set(held))
```

New text:

```
    clash: list[str] = []
```

### `u113-b.B6_root_names_unheld`

Names at the export's playlist root, where an import lands first, are not held

- File: `src/cratekit/intake/landing.py`
- Source: `u113-b.json`, row `B6_root_names_unheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`

Old text:

```
    return (*held, *at_root)
```

New text:

```
    return held
```

### `u113-c.C6_names_checked_after_moves`

The native landing no longer asks whether a chosen name was taken before its first move

- File: `src/cratekit/intake/landing.py`
- Source: `u113-c.json`, row `C6_names_checked_after_moves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_name_inbox_came_to_hold_after_the_plan_is_refused_and_nothing_is_written`

Old text:

```
    native.assert_names_still_free(db, rows)
```

New text:

```
    pass
```

### `u128-b.B1_engine_stale_unchecked`

The bridge engine does not read the owned entries again before its first move

- File: `src/cratekit/intake/landing.py`
- Source: `u128-b.json`, row `B1_engine_stale_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_the_engine_reads_the_owned_entries_again_before_the_first_move`

Old text:

```
    if now != planned:
```

New text:

```
    if False:
```

### `u128-b.B2_foreign_host_indexed`

Index an export entry whose Location names another machine, which raises out of the index

- File: `src/cratekit/intake/landing.py`
- Source: `u128-b.json`, row `B2_foreign_host_indexed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`

Old text:

```
        try:
            locations.location_to_path(recorded)
        except locations.LocationDecodeError:
            continue
        found.append
```

New text:

```
        found.append
```

### `u156.L25_shared_rule_near_match`

match_label_rows: file a row the batch holds only something close to, on both media

- File: `src/cratekit/intake/landing.py`
- Source: `u156.json`, row `L25_shared_rule_near_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_intake_land_labels_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_file_at_another_version_is_a_question_and_a_row_with_no_year_files_nothing`

Old text:

```
        if found.state is match.MatchState.NEEDS_REVIEW:
```

New text:

```
        if False:
```

### `u164.W1_apply_folder`

apply_native: move into the music folder's batch path whatever the plan chose

- File: `src/cratekit/intake/landing.py`
- Source: `u164.json`, row `W1_apply_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`
- Collected: 50 against a baseline of 50
- Kills: 24 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_filed_folder_on_another_device_is_refused_at_the_move`
  - `tests/test_intake_land_filed.py::test_a_folder_on_disk_or_one_the_collection_stores_rows_under_is_passed_over`
  - `tests/test_intake_land_filed.py::test_a_landing_on_the_27th_lands_in_its_year_folder_under_its_subject`
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_filed.py::test_a_name_that_is_a_date_alone_files_as_downloads`
  - `tests/test_intake_land_filed.py::test_a_second_unnamed_landing_that_day_takes_two_for_its_playlist_and_its_folder`
  - `tests/test_intake_land_native.py::test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[None]`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_file_id_lies_once]`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - ... and 9 more, see the JSON sidecar

Old text:

```
    target = rows.folder if rows.folder is not None else target_dir(cfg, plan.batch)
```

New text:

```
    target = target_dir(cfg, plan.batch)
```

### `u164.W2_preflight_target`

apply_native: check the library against the music folder rather than the chosen folder

- File: `src/cratekit/intake/landing.py`
- Source: `u164.json`, row `W2_preflight_target`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_land_filed.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_filed_folder_on_another_device_is_refused_at_the_move`

Old text:

```
    preflight_native(plan, cfg=cfg, target=target)
```

New text:

```
    preflight_native(plan, cfg=cfg)
```

### `u71-b.B10_occupied_at_move`

Drop the occupied check at the move, so os.replace can take a file's place

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B10_occupied_at_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_a_file_arriving_between_the_passes_is_not_replaced`
  - `tests/test_landing.py::test_every_file_taken_at_the_move_writes_no_intake_file`

Old text:

```
        occupied = _occupied(item, final)
```

New text:

```
        occupied = None
```

### `u71-b.B11_nothing_moved`

Drop the refusal after the move loop when nothing moved

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B11_nothing_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_every_file_taken_at_the_move_writes_no_intake_file`

Old text:

```
    if not moved:
        if made:
```

New text:

```
    if False:
        if made:
```

### `u71-b.B12_take_back_folder`

Keep the batch folder this call made when the first move fails

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B12_take_back_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_move_that_fails_names_what_moved_and_writes_no_xml[first]`

Old text:

```
            if made and not moved:
                _remove_if_empty(target)

```

New text:

```
(empty)
```

### `u71-b.B1_target_under_staging`

Drop the refusal of a landing target under download staging

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B1_target_under_staging`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_landing_target_under_staging_is_refused`

Old text:

```
    if resolved == staging or staging in resolved.parents:
```

New text:

```
    if False:
```

### `u71-b.B2_device`

Drop the cross device refusal, so a move across devices is attempted

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B2_device`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_staging_folder_on_another_device_is_refused_by_name`

Old text:

```
    if here is None or there is None or here != there:
```

New text:

```
    if False:
```

### `u71-b.B3_destination_exists`

Drop the refusal of an intake file that already exists

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B3_destination_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_existing_intake_file_is_never_overwritten`

Old text:

```
    if destination.exists():
```

New text:

```
    if False:
```

### `u71-b.B4_export_missing`

Drop the missing export refusal before any move

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B4_export_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_export_that_cannot_be_spliced_is_refused_before_any_move[missing]`

Old text:

```
    if not export.is_file():
```

New text:

```
    if False:
```

### `u71-b.B5_trial_splice`

Drop the trial splice on a copy, so a stub is met only after the moves

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B5_trial_splice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_export_that_cannot_be_spliced_is_refused_before_any_move[stub]`

Old text:

```
    collection_xml.splice_tracks(trial, [])

```

New text:

```
(empty)
```

### `u71-b.B6_trial_playlist`

Drop the refusal of an export whose intake playlist cannot be written

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B6_trial_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_export_that_cannot_be_spliced_is_refused_before_any_move[no-intake-folder]`

Old text:

```
    if error:
```

New text:

```
    if False:
```

### `u71-c.C1_nothing_movable_rerun`

Drop the refusal before the batch folder is made when nothing can move

- File: `src/cratekit/intake/landing.py`
- Source: `u71-c.json`, row `C1_nothing_movable_rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_batch_where_nothing_lands_leaves_no_batch_folder`

Old text:

```
    if not movable:
```

New text:

```
    if False:
```

### `u71.A10_root_absent`

Drop the refusal of an absent library root before the device probe

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A10_root_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_absent_library_root_is_refused_before_the_device_probe`

Old text:

```
    if not root.is_dir():
```

New text:

```
    if False:
```

### `u71.A11_owned_folder`

Drop the refusal of a source folder the library already owns

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A11_owned_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_folder_the_library_already_owns_is_refused`

Old text:

```
    if not in_staging and (source == owned or owned in source.parents):
```

New text:

```
    if False:
```

### `u71.A12_staging_inside_library`

Drop the exemption for staging configured inside the library root

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A12_staging_inside_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_a_landing_target_under_staging_is_refused`
  - `tests/test_landing.py::test_staging_configured_inside_the_library_still_lands`

Old text:

```
    in_staging = source == staging or staging in source.parents
```

New text:

```
    in_staging = False
```

### `u71.A1_listing_dotfile`

Drop the dotfile skip in the listing, so a hidden file is planned

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A1_listing_dotfile`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_the_listing_is_flat_audio_only_and_skips_dotfiles`

Old text:

```
    if name.startswith(".") or name == ACQUIRE_STAGING_DIRNAME:
```

New text:

```
    if name == ACQUIRE_STAGING_DIRNAME:
```

### `u71.A2_listing_suffix`

Drop the audio suffix filter, so a text file is planned and moved

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A2_listing_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_an_empty_folder_or_a_batch_name_that_is_no_plain_folder_is_refused[2026-09-18_acquired]`
  - `tests/test_landing.py::test_the_listing_is_flat_audio_only_and_skips_dotfiles`

Old text:

```
    if entry.suffix.lower() not in AUDIO_EXTS:
```

New text:

```
    if False:
```

### `u71.A3_listing_regular_file`

Drop the regular file check, so a directory named like audio is planned

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A3_listing_regular_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_the_listing_is_flat_audio_only_and_skips_dotfiles`

Old text:

```
    return entry.is_file() and not entry.is_symlink()
```

New text:

```
    return not entry.is_symlink()
```

### `u71.A4_digest_names_only`

Fingerprint names alone, so a file replaced under its name is not stale

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A4_digest_names_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_an_added_file_or_one_changed_under_the_same_name_makes_the_plan_stale[replaced]`
  - `tests/test_landing.py::test_an_added_file_or_one_changed_under_the_same_name_makes_the_plan_stale[touched]`

Old text:

```
        hasher.update(f"{item.name}\0{stat.st_size}\0{stat.st_mtime_ns}\n".encode())
```

New text:

```
        hasher.update(f"{item.name}\n".encode())
```

### `u71.A5_digest_no_mtime`

Drop the modification time from the fingerprint, keeping name and size

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A5_digest_no_mtime`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_an_added_file_or_one_changed_under_the_same_name_makes_the_plan_stale[replaced]`
  - `tests/test_landing.py::test_an_added_file_or_one_changed_under_the_same_name_makes_the_plan_stale[touched]`

Old text:

```
        hasher.update(f"{item.name}\0{stat.st_size}\0{stat.st_mtime_ns}\n".encode())
```

New text:

```
        hasher.update(f"{item.name}\0{stat.st_size}\n".encode())
```

### `u71.A6_stale_refusal`

Drop the stale plan refusal whole

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A6_stale_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 3 (killed)
- Killed:
  - `tests/test_landing.py::test_an_added_file_or_one_changed_under_the_same_name_makes_the_plan_stale[added]`
  - `tests/test_landing.py::test_an_added_file_or_one_changed_under_the_same_name_makes_the_plan_stale[replaced]`
  - `tests/test_landing.py::test_an_added_file_or_one_changed_under_the_same_name_makes_the_plan_stale[touched]`

Old text:

```
    if items != plan.items or _digest(items) != plan.digest:
```

New text:

```
    if False:
```

### `u71.A7_stale_listing_only`

Compare the relisting by path only, dropping the digest half

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A7_stale_listing_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_an_added_file_or_one_changed_under_the_same_name_makes_the_plan_stale[replaced]`
  - `tests/test_landing.py::test_an_added_file_or_one_changed_under_the_same_name_makes_the_plan_stale[touched]`

Old text:

```
    if items != plan.items or _digest(items) != plan.digest:
```

New text:

```
    if items != plan.items:
```

### `u71.A9_plan_empty`

Drop the refusal of a folder with nothing to land

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A9_plan_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_empty_folder_or_a_batch_name_that_is_no_plain_folder_is_refused[2026-09-18_acquired]`

Old text:

```
    if not items:
```

New text:

```
    if False:
```

### `u72-b.M23_listing_unfiltered`

The engine's public listing returns every entry, not only audio

- File: `src/cratekit/intake/landing.py`
- Source: `u72-b.json`, row `M23_listing_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`

Old text:

```
    return _list(folder)


def _digest(
```

New text:

```
    return tuple(folder.iterdir())


def _digest(
```

### `u77-a.A1_label_source_filter`

read_label_manifest: keep every manifest row whatever its source, so a favourites or playlist row is filed under a label

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A1_label_source_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_costs_a_landing_with_no_label_row_nothing[favourites]`

Old text:

```
rows=tuple(row for row in rows if row.provenance.source == LABEL_SOURCE),
```

New text:

```
rows=tuple(row for row in rows if row.provenance.source),
```

### `u77-a.A2_engine_stale_digest`

apply: never compare the manifest's bytes with the fingerprint the caller was shown, so a manifest rewritten after the gate is filed (the engine layer alone, the gate's own check left in place)

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A2_engine_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 16 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_batch_folder_that_cannot_be_indexed_reports_every_label_row`
  - `tests/test_landing_labels.py::test_a_catalog_tree_the_database_owns_refuses_before_any_file_moves`
  - `tests/test_landing_labels.py::test_a_file_already_in_the_batch_folder_is_not_filed_under_this_landing`
  - `tests/test_landing_labels.py::test_a_file_at_another_version_is_a_question_and_a_row_with_no_year_files_nothing`
  - `tests/test_landing_labels.py::test_a_held_year_playlist_the_writer_cannot_extend_refuses_before_any_move`
  - `tests/test_landing_labels.py::test_a_label_row_no_landed_file_matches_is_reported_by_name`
  - `tests/test_landing_labels.py::test_a_manifest_rewritten_after_it_was_fingerprinted_is_stale_and_moves_nothing`
  - `tests/test_landing_labels.py::test_a_marked_lossy_file_with_no_title_tag_is_still_filed`
  - `tests/test_landing_labels.py::test_a_second_landing_into_the_first_ones_file_merges_and_duplicates_nothing`
  - `tests/test_landing_labels.py::test_a_tree_the_disk_refuses_after_the_moves_is_named_and_the_file_stays`
  - `tests/test_landing_labels.py::test_an_export_holding_a_label_folder_twice_refuses_before_any_file_moves`
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_costs_a_landing_with_no_label_row_nothing[favourites]`
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_refuses_before_any_file_moves`
  - `tests/test_landing_labels.py::test_one_recording_listed_under_two_ids_is_in_its_year_once`
  - `tests/test_landing_labels.py::test_the_registry_is_read_before_the_first_move_and_never_after`
  - ... and 1 more, see the JSON sidecar

Old text:

```
if manifest_digest is not None and read.digest != manifest_digest:
```

New text:

```
if manifest_digest is None and read.digest != manifest_digest:
```

### `u77-a.A4_export_reason_mapping`

_check_export: pass the writer's internal-error through unchanged, so a doubled label folder in the person's export reaches them as a defect

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A4_export_reason_mapping`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_held_year_playlist_the_writer_cannot_extend_refuses_before_any_move`
  - `tests/test_landing_labels.py::test_an_export_holding_a_label_folder_twice_refuses_before_any_file_moves`

Old text:

```
if exc.cause.reason != "internal-error":
```

New text:

```
if exc.cause.reason:
```

### `u77-a.A5_needs_review_guard`

_file_labels: stop treating a needs review match as a question, so a row whose batch holds another version falls through to the unmatched answer

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A5_needs_review_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_file_at_another_version_is_a_question_and_a_row_with_no_year_files_nothing`

Old text:

```
if found.state is match.MatchState.NEEDS_REVIEW:
```

New text:

```
if found.state is match.MatchState.SUPPRESSED:
```

### `u77-a.A6_no_landed_file_guard`

_file_labels: file a row that resolved to no file this run placed, so a year playlist is written for a track the intake file gave no id

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A6_no_landed_file_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`
  - `tests/test_landing_labels.py::test_a_file_already_in_the_batch_folder_is_not_filed_under_this_landing`
  - `tests/test_landing_labels.py::test_a_label_row_no_landed_file_matches_is_reported_by_name`
  - `tests/test_landing_labels.py::test_a_second_landing_into_the_first_ones_file_merges_and_duplicates_nothing`

Old text:

```
        if not landed:
            # TRUE OF BOTH ROWS
```

New text:

```
        if landed is None:
            # TRUE OF BOTH ROWS
```

### `u77-a.A7_year_absent_guard`

_file_labels: file a label row that carries no year, so a playlist named for the label and None is written

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A7_year_absent_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_file_at_another_version_is_a_question_and_a_row_with_no_year_files_nothing`

Old text:

```
        if not label or year is None:
            absent =
```

New text:

```
        if not label:
            absent =
```

### `u77-a.A8_library_template`

_file_labels: index the batch folder with the bare default name template, so the library's lossy marker stays in a title read from the filename

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A8_library_template`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_marked_lossy_file_with_no_title_tag_is_still_filed`

Old text:

```
index = match.index_library(batch_dir, template=template)
```

New text:

```
index = match.index_library(batch_dir)
```

### `u77-a.A9_this_runs_files_only`

_file_labels: take a matched path's id without asking whether this run placed it (the membership test removed, the lookup defaulted), so a file an earlier landing left in the batch folder is filed under id None

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A9_this_runs_files_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_file_already_in_the_batch_folder_is_not_filed_under_this_landing`

Old text:

```
            ids[Path(path).resolve()]
            for path in (found.paths if found.state is match.MatchState.MATCHED else ())
            if Path(path).resolve() in ids

```

New text:

```
            ids.get(Path(path).resolve())
            for path in (found.paths if found.state is match.MatchState.MATCHED else ())

```

### `u77-a2.A2_engine_stale_digest`

apply: the same row as u77-a's, measured again with a mutation that only removes the guard. The first inverted the test for a fingerprint being given, so it refused every landing that gave none and its 19 deaths were mostly not the guard's. This one compares the fingerprint with itself, so the check can never fire and nothing else changes

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a2.json`, row `A2_engine_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_manifest_rewritten_after_it_was_fingerprinted_is_stale_and_moves_nothing`

Old text:

```
if manifest_digest is not None and read.digest != manifest_digest:
```

New text:

```
if manifest_digest is not None and manifest_digest != manifest_digest:
```

### `u77-b.B1_reported_ids_deduped`

_label: report a year's ids as collected instead of deduplicated, so a recording listed under two provider ids is reported twice while the file holds it once

- File: `src/cratekit/intake/landing.py`
- Source: `u77-b.json`, row `B1_reported_ids_deduped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_one_recording_listed_under_two_ids_is_in_its_year_once`

Old text:

```
track_ids=tuple(rbxml.dedupe_track_ids(years[label][year])),
```

New text:

```
track_ids=tuple(years[label][year]),
```

### `u77-b.B2_disk_refusal_reported`

_label: catch only a structured refusal from the tree write, so a disk that refuses after the moves raises out of a landing that already succeeded

- File: `src/cratekit/intake/landing.py`
- Source: `u77-b.json`, row `B2_disk_refusal_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_tree_the_disk_refuses_after_the_moves_is_named_and_the_file_stays`

Old text:

```
    except (CratekitError, OSError) as exc:
        said = f"the label tree could not be written ({exc})"
```

New text:

```
    except CratekitError as exc:
        said = f"the label tree could not be written ({exc})"
```

### `u77-b.B3_index_refusal_reported`

_label: stop catching a batch folder that cannot be read, so the index raises after the moves

- File: `src/cratekit/intake/landing.py`
- Source: `u77-b.json`, row `B3_index_refusal_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_batch_folder_that_cannot_be_indexed_reports_every_label_row`

Old text:

```
    except OSError as exc:
        said = f"the batch folder could not be read
```

New text:

```
    except KeyError as exc:
        said = f"the batch folder could not be read
```

### `u77-b.B5_unmatched_sentence`

_file_labels: reword the unmatched sentence so it no longer limits the claim to this run, which is false of a row an earlier landing filed

- File: `src/cratekit/intake/landing.py`
- Source: `u77-b.json`, row `B5_unmatched_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_label_row_no_landed_file_matches_is_reported_by_name`

Old text:

```
sentence=f"{spelled} was filed under no label playlist by this run, because {because}",
```

New text:

```
sentence=f"{spelled} was filed under no label playlist at all, because {because}",
```

### `r1017.M3_landing_open_read`

Landing records: read a record that never closed as a landing

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M3_landing_open_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_with_no_landing_record_and_no_matching_name_still_refuses[open]`

Old text:

```
        if record.state is session.SessionState.CLOSED
        and str(session.SourceState.COMMITTED) in record.sources.values()
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

New text:

```
        if record.state is not None
        and str(session.SourceState.COMMITTED) in record.sources.values()
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

### `r1017.M4_landing_uncommitted_read`

Landing records: read a record whose source never committed as a landing

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M4_landing_uncommitted_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_with_no_landing_record_and_no_matching_name_still_refuses[uncommitted]`

Old text:

```
        and str(session.SourceState.COMMITTED) in record.sources.values()
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

New text:

```
        and record.sources
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

### `r1017.M5_landing_any_job`

Landing records: read another job's landing as this job's

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M5_landing_any_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_with_no_landing_record_and_no_matching_name_still_refuses[another job]`
  - `tests/test_export_set_rename.py::test_recorded_names_reads_every_landing_of_the_job_the_newest_first`

Old text:

```
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

New text:

```
        and record.detail[RECORD_KEY].get("job") is not None
    ]
    return tuple(
```

### `r1017.M6_oldest_first`

Landing records: read them oldest first, which recorded_playlist also depends on

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M6_oldest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_recorded_names_reads_every_landing_of_the_job_the_newest_first`

Old text:

```
        for record in sorted(found, key=lambda one: one.session_id, reverse=True)
```

New text:

```
        for record in sorted(found, key=lambda one: one.session_id, reverse=False)
```

### `r1017.M7_names_not_deduplicated`

recorded_names: return a name twice when two landings recorded it

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M7_names_not_deduplicated`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_recorded_names_reads_every_landing_of_the_job_the_newest_first`

Old text:

```
        dict.fromkeys(name for kept in _landed(cfg, job_id) if (name := str(kept.get("name") or "")))
```

New text:

```
        list(name for kept in _landed(cfg, job_id) if (name := str(kept.get("name") or "")))
```

### `u121-b.S10r_folder_row_removed`

_folder_row: a folder rekordbox removed since the plan is still written into

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-b.json`, row `S10r_folder_row_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_engine_refuses_a_folder_removed_after_the_plan_even_with_no_gate_in_front`

Old text:

```
        if row is None or rb_writer.node_removed(row):
```

New text:

```
        if row is None:
```

### `u121-b.S14r_stale_digest`

apply_alone: a plan whose digest moved since the approval is written anyway

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-b.json`, row `S14r_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_engine_refuses_a_plan_whose_collection_moved_even_with_no_gate_in_front`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u121-b.S15r_member_order`

_members: members in title order rather than set order

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-b.json`, row `S15r_member_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
    return tuple(members), tuple(left)
```

New text:

```
    return tuple(sorted(members, key=lambda one: one.title)), tuple(left)
```

### `u121-c.S2c_separator`

_without_leading: keep the separator after the uploader's name

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-c.json`, row `S2c_separator`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_from_the_page_with_the_uploader_taken_off_the_title`

Old text:

```
    stripped = re.sub(r"^\s*(?:[-:|\u2013\u2014]+\s*)?", "", rest)
```

New text:

```
    stripped = rest.strip()
```

### `u121-d.D1_record_ignored`

plan_for_landing: the playlist an earlier landing recorded for the job is never read, so a second day makes a twin

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D1_record_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
    recorded = recorded_playlist(cfg, db, job.job_id, folder_id)
    staged = [source for source, _target in files]
```

New text:

```
    recorded = None
    staged = [source for source, _target in files]
```

### `u121-d.D2_removed_namesake`

_playlist_row: a removed playlist of the name under the folder is written into

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D2_removed_namesake`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_removed_namesake_under_the_folder_is_not_written_into`

Old text:

```
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
```

New text:

```
        if rb_writer.is_folder(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
```

### `u121-d.D3_repeated_row_counted_twice`

write_members: two reports resolving to one row count as two members

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D3_repeated_row_counted_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_two_rows_of_the_set_resolving_to_one_track_are_one_member`

Old text:

```
    distinct = tuple(dict.fromkeys(ids))
```

New text:

```
    distinct = tuple(ids)
```

### `u121-d.D4_record_on_nothing`

_record_set_commit: a rerun that added nothing still records the folder committed

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D4_record_on_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_second_write_that_fills_a_gap_mid_set_is_not_a_failed_write`

Old text:

```
    if not (written.added or written.playlist_created or written.folder_created):
        return

```

New text:

```
(empty)
```

### `u121-d.D5_left_dropped_when_nothing_written`

write_members: the members whose files did not land are dropped from the left list when nothing is written

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D5_left_dropped_when_nothing_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_when_every_landed_members_file_is_refused_the_left_list_names_them`

Old text:

```
            members=0,
            added=0,
            left=(*left, *plan.left),
        )
```

New text:

```
            members=0,
            added=0,
            left=tuple(plan.left),
        )
```

### `u121-d.D6_recorded_but_removed`

recorded_playlist: a recorded playlist rekordbox removed is still the one added to

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D6_recorded_but_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`

Old text:

```
            or rb_writer.node_removed(row)
            or str(getattr(row, "ParentID", "") or "") != folder_id
```

New text:

```
            or str(getattr(row, "ParentID", "") or "") != folder_id
```

### `u121.S11_landed_by_target`

write_members: a landed member's row is not looked up by its target

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S11_landed_by_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 13 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_names_the_playlist_for_the_posted_day[flag]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_names_the_playlist_for_the_posted_day[page]`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_posted_on_a_frozen_job_names_another_day_and_the_frozen_name_wins_with_a_warning`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
        held = one.content_id or rows.get(one.target, "")
```

New text:

```
        held = one.content_id
```

### `u121.S17_unresolved_dropped`

_members: a downloaded row tied to nothing is dropped silently rather than listed

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S17_unresolved_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_set_with_nothing_owned_or_landed_writes_no_playlist_and_says_so`
  - `tests/test_set_inspiration_playlist.py::test_an_unanswered_question_is_left_out_and_the_plan_offers_nothing`
  - `tests/test_set_inspiration_playlist.py::test_the_backfill_over_a_set_with_nothing_owned_asks_and_then_writes_nothing`

Old text:

```
        if not paths:
            left.append(Left(position, artist, title, state, NOT_RESOLVED))
            continue
        if how == LANDED:
```

New text:

```
        if not paths:
            continue
        if how == LANDED:
```

### `u121.S1_uploader_prefix`

_without_leading: never take the uploader's name off the front of the page title

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S1_uploader_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_from_the_page_with_the_uploader_taken_off_the_title`

Old text:

```
    if head.casefold() != dj.casefold():
```

New text:

```
    if True:
```

### `u121.S3_answer_not_read`

_LibraryView.resolve: a person's review answer is never read back, a question stays one

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S3_answer_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`

Old text:

```
        if found.state is not match.MatchState.NEEDS_REVIEW:
            return found
```

New text:

```
        if True:
            return found
```

### `u121.S4_page_beats_flag`

words_for: the page's uploader wins over --dj

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S4_page_beats_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_flag_wins_over_the_page_and_a_day_is_read_as_its_month`

Old text:

```
    who = (dj if dj is not None else str(page.get(fetch.PAGE_UPLOADER) or "")).strip()
```

New text:

```
    who = str(page.get(fetch.PAGE_UPLOADER) or dj or "").strip()
```

### `u121.S5_missing_word`

words_for: a missing word is not refused, the name is made with a hole

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S5_missing_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 6 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_playlist_job_named_with_set_is_refused_before_anything_moves`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page0-flags0-missing0]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page1-flags1-missing1]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page2-flags2-missing2]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page3-flags3-missing3]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page4-flags4-missing4]`

Old text:

```
    if missing:
```

New text:

```
    if False:
```

### `u121.S7_job_handler`

set_job_or_refuse: accept a playlist job as a set

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S7_job_handler`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_playlist_job_named_with_set_is_refused_before_anything_moves`

Old text:

```
    if job.handler_key != SET_KEY:
```

New text:

```
    if False:
```

### `u121.S8_job_state`

set_job_or_refuse: accept a job that has not finished

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S8_job_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_backfill_refuses_a_job_that_is_not_a_set_and_an_unfinished_one`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
    if False:
```

### `u121.S9_two_folders`

folder_for: two root folders of the name pass, the first is taken

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S9_two_folders`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_two_root_folders_of_the_name_are_refused_rather_than_one_chosen`

Old text:

```
    if len(live) > 1:
```

New text:

```
    if len(live) > 2:
```

### `u129-author.A18_frozen_name_ignored`

Ignore the frozen INSPIRATION name on the job and recompute it

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u129-author.json`, row `A18_frozen_name_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 20 against a baseline of 20
- Kills: 2 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_set_backfill_names_playlists_already_made_when_one_fails[credential]`
  - `tests/test_u129_set_account_playlist.py::test_export_set_backfill_names_playlists_already_made_when_one_fails[transient]`

Old text:

```
    return str(payload.get(intake_cli.PLAYLIST_NAME) or "").strip()

```

New text:

```
    return ""

```

### `u135.A12_inspiration_join_broken`

Second landing of a set remakes the INSPIRATION playlist instead of adding

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u135.json`, row `A12_inspiration_join_broken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_two_landings_of_one_set_make_one_inbox_playlist_in_set_order`

Old text:

```
        if row is None or rb_writer.is_folder(row) or rb_writer.node_removed(row):
            raise refuse(
                "decision-stale",
                f"the set's playlist {plan.name!r} (row {plan.playlist_id}) the plan "
                f"adds to is not live any more, so nothing was written",
                origin=_ORIGIN,
                detail={"playlist": plan.playlist_id, "name": plan.name},
            )
        return row, False

```

New text:

```
        return db.create_playlist(plan.name, parent=folder), True

```

### `u144-c.C9_parent_of_named`

Sample of an existing U121 guard, now shared: take a live playlist of the name under any parent

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u144-c.json`, row `C9_parent_of_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_organize_inspiration.py`
- Collected: 95 against a baseline of 95
- Kills: 10 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_posted_on_a_frozen_job_names_another_day_and_the_frozen_name_wins_with_a_warning`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
        if str(getattr(row, "ParentID", "") or "") == parent_id:
```

New text:

```
        if True:
```

### `u246.S3_set_playlist_order_set_empty`

assert_read_back (set playlist): an empty set of wanted ids, so a filled playlist always reads as out of order and refuses

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u246.json`, row `S3_set_playlist_order_set_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_export_set.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_write_session.py`, `tests/test_inbox_refill.py`
- Collected: 293 against a baseline of 293
- Kills: 22 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_backfill_a_week_later_adds_to_a_playlist_pre_made_under_the_posted_name`
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_filled_playlist_holding_a_row_it_found_still_reads_back_in_set_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[not-renamed]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[raised]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_names_the_playlist_for_the_posted_day[flag]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_names_the_playlist_for_the_posted_day[page]`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_removed_namesake_under_the_folder_is_not_written_into`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_second_write_that_fills_a_gap_mid_set_is_not_a_failed_write`
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`
  - ... and 7 more, see the JSON sidecar

Old text:

```
    named = set(wanted)
```

New text:

```
    named = set()
```

### `u246.S4_set_playlist_order_set_read_back`

assert_read_back (set playlist): the set built from the read back, so a stranger row in a filled playlist no longer breaks the order

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u246.json`, row `S4_set_playlist_order_set_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_export_set.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_write_session.py`, `tests/test_inbox_refill.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_filled_playlist_holding_a_row_it_found_still_reads_back_in_set_order`

Old text:

```
    named = set(wanted)
```

New text:

```
    named = set(written.read_back)
```

### `u154.G10_read_back_path_unchecked`

a row committed with a path other than the planned one is reported as shelved

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G10_read_back_path_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[path]`

Old text:

```
            if str(stored or "") != row.folder_path:

```

New text:

```
            if False:

```

### `u154.G11_kept_columns_unchecked`

a column the shelve does not own may change without the read back saying so

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G11_kept_columns_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[kept-column]`

Old text:

```
            if before.get(row.content_id) != after.get(row.content_id):

```

New text:

```
            if False:

```

### `u154.G14_reserved_folders_are_candidates`

the processed tree and the sets folder are planned as batches under --all

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G14_reserved_folders_are_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_two_batches_filing_to_one_name_get_two_and_a_taken_target_is_passed_over`

Old text:

```
        if entry.name.startswith(".") or entry.name in reserved:

```

New text:

```
        if entry.name.startswith("."):

```

### `u154.G15_stored_target_under_mounted_path`

the confinement check reads under the mounted target and not the stored one

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G15_stored_target_under_mounted_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`

Old text:

```
            {"prefix": _like_prefix(one.stored_target)},

```

New text:

```
            {"prefix": _like_prefix(str(one.target))},

```

### `u154.G17_refusal_before_rename_rewrapped`

a stale plan refusal before any rename is rewrapped as a write failure

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G17_refusal_before_rename_rewrapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
            if not moved and isinstance(exc, CratekitError):

```

New text:

```
            if False:

```

### `u154.G1_policy_not_registered`

the path column is written with no field policy registered for the commit

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G1_policy_not_registered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over`
  - `tests/test_intake_shelve.py::test_apply_moves_the_folder_rewrites_the_paths_keeps_the_rest_and_the_name_stays_taken`
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[kept-column]`
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[path]`

Old text:

```
            with rb_writer.field_policies_for_commit(rb_writer.SHELVE_POLICY):
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)

```

New text:

```
            if True:
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)

```

### `u154.G2_confinement_dropped`

the SQL confinement check is skipped before the commit

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G2_confinement_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over`

Old text:

```
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)

```

New text:

```
                rb_writer.commit_guarded(db)

```

### `u154.G3_rename_back_dropped`

a failure past the rename leaves the folder at its new name

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G3_rename_back_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over`
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
            failed = _rename_back(moved)

```

New text:

```
            failed: list[str] = []

```

### `u154.G4_stale_target_check_dropped`

a target made after the plan is renamed over at apply

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G4_stale_target_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
    if os.path.lexists(one.target):
        raise refuse(
            "decision-stale",
            f"{one.target} exists now and did not when the plan was made, so nothing "

```

New text:

```
    if False:
        raise refuse(
            "decision-stale",
            f"{one.target} exists now and did not when the plan was made, so nothing "

```

### `u154.G5_unmatched_file_shelved_anyway`

a batch with a file the collection does not hold is moved anyway

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G5_unmatched_file_shelved_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
        if unmatched is not None:
            leave(batch, _why_unmatched(*unmatched))
            continue

```

New text:

```
        if False:
            leave(batch, _why_unmatched(*unmatched))
            continue

```

### `u154.G6_subfolder_check_dropped`

a batch folder holding a subfolder is planned

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G6_subfolder_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
        if any(entry.is_dir() for entry in folder.iterdir()):

```

New text:

```
        if False:

```

### `u154.G7_run_id_shape_unread`

a batch named for its run identifier fits neither shape

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G7_run_id_shape_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[four-hex-before-u235]`
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[sixteen-hex-since-u235]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-09-23T222241Z-4773-expected5]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-11-07T164826Z-ce458ab7cceccb0b-expected6]`

Old text:

```
    run = _RUN_ID.match(batch)
    if run is not None:

```

New text:

```
    run = None
    if run is not None:

```

### `u154.G8_free_target_no_suffix`

a taken target is reused rather than given the next suffix

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G8_free_target_no_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over`
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`
  - `tests/test_intake_shelve.py::test_two_batches_filing_to_one_name_get_two_and_a_taken_target_is_passed_over`

Old text:

```
    while os.path.lexists(candidate) or candidate in planned or spell(candidate) in stored_dirs:

```

New text:

```
    while False:

```

### `u154.R1_rows_under_target_not_consulted`

a target free on disk but holding collection rows is chosen

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R1_rows_under_target_not_consulted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over`

Old text:

```
    while os.path.lexists(candidate) or candidate in planned or spell(candidate) in stored_dirs:

```

New text:

```
    while os.path.lexists(candidate) or candidate in planned:

```

### `u154.R3_repeated_name_planned_twice`

a batch named twice is planned twice

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R3_repeated_name_planned_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_apply_moves_the_folder_rewrites_the_paths_keeps_the_rest_and_the_name_stays_taken`

Old text:

```
    wanted = _candidates(cfg) if everything else list(dict.fromkeys(names))

```

New text:

```
    wanted = _candidates(cfg) if everything else list(names)

```

### `u154.R6_device_probe_dropped`

a processed tree on another device is planned and renamed into

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R6_device_probe_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
    _assert_one_device(cfg, root)

```

New text:

```
    pass

```

### `u154.R7_exact_prefix_filter_dropped`

the confinement check judges the case blind LIKE result as is

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R7_exact_prefix_filter_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_apply_moves_the_folder_rewrites_the_paths_keeps_the_rest_and_the_name_stays_taken`

Old text:

```
            if str(row[1] or "").startswith(one.stored_target + os.sep)

```

New text:

```
            if True

```

### `u164.T1_filed_target`

landing_target: land in the music folder's batch path rather than the filed folder

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T1_filed_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_shelve.py`, `tests/test_intake_land_rehearse.py`
- Collected: 98 against a baseline of 98
- Kills: 33 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_filed_folder_on_another_device_is_refused_at_the_move`
  - `tests/test_intake_land_filed.py::test_a_folder_on_disk_or_one_the_collection_stores_rows_under_is_passed_over`
  - `tests/test_intake_land_filed.py::test_a_landing_on_the_27th_lands_in_its_year_folder_under_its_subject`
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_filed.py::test_a_name_that_is_a_date_alone_files_as_downloads`
  - `tests/test_intake_land_filed.py::test_a_second_unnamed_landing_that_day_takes_two_for_its_playlist_and_its_folder`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[None]`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_file_id_lies_once]`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    when, said = filed_parts(batch, on=on)
    spell = _speller(db)
```

New text:

```
    return landing.target_dir(cfg, batch)
    when, said = filed_parts(batch, on=on)
    spell = _speller(db)
```

### `u164.T2_free_disk`

_free_target: never pass over a folder already on disk

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T2_free_disk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_shelve.py`
- Collected: 29 against a baseline of 29
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_folder_on_disk_or_one_the_collection_stores_rows_under_is_passed_over`
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`
  - `tests/test_intake_shelve.py::test_two_batches_filing_to_one_name_get_two_and_a_taken_target_is_passed_over`

Old text:

```
    while os.path.lexists(candidate) or candidate in planned or spell(candidate) in stored_dirs:
```

New text:

```
    while candidate in planned or spell(candidate) in stored_dirs:
```

### `u164.T3_free_stored`

landing_target: ask the disk alone, not the collection's stored folders

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T3_free_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_folder_on_disk_or_one_the_collection_stores_rows_under_is_passed_over`
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`

Old text:

```
        stored_dirs=_stored_dirs(recorded),
```

New text:

```
        stored_dirs=frozenset(),
```

### `u164.T4_undated_name`

filed_parts: file a name with no date under the whole name as a date-free folder

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T4_undated_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`

Old text:

```
    when, words = parsed if parsed is not None else (on, " ".join(batch.split()))
```

New text:

```
    when, words = parsed if parsed is not None else (on, "")
```

### `u164.T5_empty_subject`

filed_parts: leave an empty subject empty instead of Downloads

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T5_empty_subject`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_shelve.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_that_is_a_date_alone_files_as_downloads`

Old text:

```
    return when, words or batch_name.DOWNLOADS
```

New text:

```
    return when, words
```

### `u164.T6_reuse_recorded`

landing_target: never go back to the folder recorded for a batch landed into again

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T6_reuse_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_rehearse.py`
- Collected: 75 against a baseline of 75
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_folder_holds_is_refused_at_the_area`

Old text:

```
    if again is not None and os.path.isdir(again) and not os.path.islink(again):
        return Path(again)
```

New text:

```
    if False:
        return Path(again)
```

### `u164.T7_reuse_gone`

landing_target: reuse a recorded folder even when it is gone from disk

- File: `src/cratekit/intake/shelve.py`
- Source: `u164.json`, row `T7_reuse_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`

Old text:

```
    if again is not None and os.path.isdir(again) and not os.path.islink(again):
```

New text:

```
    if again is not None:
```

### `u235.H1_shelve_four_hex_only`

intake.shelve: the run named batch pattern takes a four hex tail only, the round one finding, so a batch named for a run minted since U235 is refused as carrying no date

- File: `src/cratekit/intake/shelve.py`
- Source: `u235.json`, row `H1_shelve_four_hex_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[sixteen-hex-since-u235]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-11-07T164826Z-ce458ab7cceccb0b-expected6]`

Old text:

```
T\d{6}Z-(?:[0-9a-f]{4}|[0-9a-f]{16})$")
```

New text:

```
T\d{6}Z-[0-9a-f]{4}$")
```

### `u235.H2_shelve_sixteen_hex_only`

intake.shelve: the run named batch pattern takes a sixteen hex tail only, so a batch named for a run from before U235 is refused as carrying no date

- File: `src/cratekit/intake/shelve.py`
- Source: `u235.json`, row `H2_shelve_sixteen_hex_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[four-hex-before-u235]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-09-23T222241Z-4773-expected5]`

Old text:

```
T\d{6}Z-(?:[0-9a-f]{4}|[0-9a-f]{16})$")
```

New text:

```
T\d{6}Z-[0-9a-f]{16}$")
```

### `r501-b.I1_rollback_abandon`

ingest.place_files: drop the abandon in the rollback, so a refused call leaves its session non terminal

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I1_rollback_abandon`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_failed_call_records_no_track_the_ledger_cannot_withdraw`
  - `tests/test_intake_imported.py::test_a_placed_call_ends_awaiting_import_with_the_action_persisted`
  - `tests/test_intake_imported.py::test_a_refusal_after_the_session_opens_abandons_it_and_removes_the_file`

Old text:

```
        with contextlib.suppress(Exception):
            routing_pass.close_run(record, cfg, state=session.SessionState.ABANDONED)
        raise
```

New text:

```
        raise
```

### `r501-b.I2_rollback_unlink`

ingest.place_files: drop the unlink in the rollback, so a refused call leaves an intake file with no run behind it

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I2_rollback_unlink`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_refusal_after_the_session_opens_abandons_it_and_removes_the_file`

Old text:

```
        if wrote and fresh:
            with contextlib.suppress(OSError):
                destination.unlink(missing_ok=True)
```

New text:

```
        if False:
            with contextlib.suppress(OSError):
                destination.unlink(missing_ok=True)
```

### `r501-b.I3_rollback_fresh_only`

ingest.place_files: unlink whatever is at the destination, so a failed call removes an earlier run's intake file

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I3_rollback_fresh_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_placed_call_ends_awaiting_import_with_the_action_persisted`

Old text:

```
        if wrote and fresh:
```

New text:

```
        if wrote:
```

### `r501-b.I4_mark_awaiting`

ingest.place_files: never mark the session awaiting-import, so every landing leaves an open record again

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I4_mark_awaiting`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 23 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_failed_call_records_no_track_the_ledger_cannot_withdraw`
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_placed_call_ends_awaiting_import_with_the_action_persisted`
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`
  - `tests/test_intake_imported.py::test_after_a_cutover_the_pass_placing_every_track_is_proof_and_closes_the_run`
  - `tests/test_intake_imported.py::test_intake_file_ends_pending_and_is_settled_the_same_way`
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`
  - `tests/test_intake_imported.py::test_tracks_acknowledged_as_gone_are_not_proof_of_an_import`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - ... and 8 more, see the JSON sidecar

Old text:

```
        wrote = True
        session.mark_awaiting_import(
```

New text:

```
        wrote = True
        session.pending_import if False else (lambda *a, **k: None)(
```

### `r685-b.P1_place_files_rereads_the_registry`

place_files ignores the registry the landing handed it and reads its own after the moves

- File: `src/cratekit/intake/ingest.py`
- Source: `r685-b.json`, row `P1_place_files_rereads_the_registry`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_the_registry_is_read_before_the_first_move_and_never_after`

Old text:

```
    if registry is None:
        registry = tree_registry.read(cfg)

```

New text:

```
    registry = tree_registry.read(cfg)

```

### `r740-b.I1_tag_key_first`

read_meta: prefer the key tag over the head's key, so a disagreeing tag drops the whole head

- File: `src/cratekit/intake/ingest.py`
- Source: `r740-b.json`, row `I1_tag_key_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/test_intake_land.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields5-05B - 98 - Body-8A]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields2-08A - 124 - Body-3B]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields3-08A - 124 - Body-Am]`

Old text:

```
            key=head.get("key") or key,
```

New text:

```
            key=key or head.get("key"),
```

### `r740-b.I3_stem_is_the_title`

read_meta: pass the title as the stem, so the filename's head never reaches normalize_spec

- File: `src/cratekit/intake/ingest.py`
- Source: `r740-b.json`, row `I3_stem_is_the_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/test_intake_land.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields4-05B - 98 - Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields5-05B - 98 - Body-8A]`

Old text:

```
            stem=path.stem,
            suffix=path.suffix,
            key=head.get("key") or key,
```

New text:

```
            stem=title,
            suffix=path.suffix,
            key=head.get("key") or key,
```

### `r740-b.I4_lossy_is_the_parameter`

read_meta: report the caller's lossy parameter, not the flag the Name was rendered from

- File: `src/cratekit/intake/ingest.py`
- Source: `r740-b.json`, row `I4_lossy_is_the_parameter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/test_intake_land.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_head.py::test_the_lossy_flag_reported_is_the_one_the_name_was_rendered_from`

Old text:

```
        "lossy": spec.lossy,
```

New text:

```
        "lossy": lossy,
```

### `r740-b.I5_body_marker_marks`

read_meta: read the marker anywhere in the title or stem, the round one defect, doubling an acquired marker

- File: `src/cratekit/intake/ingest.py`
- Source: `r740-b.json`, row `I5_body_marker_marks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/test_intake_land.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body [MP3].flac-fields7-Body-None]`

Old text:

```
            lossy=lossy,
            title=title,
```

New text:

```
            lossy=lossy or "[MP3]" in title or "[MP3]" in path.stem,
            title=title,
```

### `r740-c.I2_no_stem_fallback`

round two, after the disagreeing key tag test, read_meta: read the head from the title only, never the filename stem

- File: `src/cratekit/intake/ingest.py`
- Source: `r740-c.json`, row `I2_no_stem_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/test_intake_land.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields5-05B - 98 - Body-8A]`

Old text:

```
        or naming.parse_head(path.stem, template=template)

```

New text:

```
(empty)
```

### `r770-a.A1_switch_reads_the_other_mode`

IntakeMedium.native: answer native for a tree on the bridge and bridge for a native one

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A1_switch_reads_the_other_mode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
- Collected: 77 against a baseline of 77
- Kills: 57 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_decision_recorded_against_the_path_bearing_digest_is_stale_and_writes_nothing`
  - `tests/test_intake_land_native.py::test_a_default_name_taken_after_the_approval_is_refused_and_writes_nothing`
  - `tests/test_intake_land_native.py::test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[None]`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_file_id_lies_once]`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[UPDATE djmdContent SET BPM = 12400 WHERE ID = :id-BPM]`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[UPDATE djmdContent SET KeyID = '283157525' WHERE ID = :id-KeyID]`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[sql2-djmdMixerParam]`
  - ... and 42 more, see the JSON sidecar

Old text:

```
        return self.registry.is_database_native(self.declared.intake.id)
```

New text:

```
        return self.registry.is_on_the_bridge(self.declared.intake.id)
```

### `r770-a.A2_unreachable_root_is_read_anyway`

intake_medium: read the taxonomy and the registry of a library root that is not there

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A2_unreachable_root_is_read_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land.py`
- Collected: 60 against a baseline of 60
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_what_went_missing`
  - `tests/test_intake_writers_native.py::test_the_switch_reads_the_recorded_mode_and_nothing_else`

Old text:

```
    if not Path(cfg.library.root).is_dir():
```

New text:

```
    if False:
```

### `r770-a.A3_assertion_refuses_nothing`

assert_intake_on_the_bridge: return for every tree, so a splice at a native tree reaches the emitter guard and its report-defect

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A3_assertion_refuses_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_the_bridge_landing_engine_refuses_a_native_tree_the_same_way_and_moves_nothing`
  - `tests/test_intake_writers_native.py::test_the_splice_refuses_a_native_intake_tree_naming_the_landing`

Old text:

```
    if not IntakeMedium(declared=declared, registry=registry).native:
```

New text:

```
    if True:
```

### `r770-a.A4_refusal_asks_for_a_defect_report`

assert_intake_on_the_bridge: give the refusal the remedy the finding was about

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A4_refusal_asks_for_a_defect_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_the_bridge_landing_engine_refuses_a_native_tree_the_same_way_and_moves_nothing`
  - `tests/test_intake_writers_native.py::test_the_splice_refuses_a_native_intake_tree_naming_the_landing`

Old text:

```
        remedy=Remedy.FIX_COMMAND_LINE,
```

New text:

```
        remedy=Remedy.REPORT_DEFECT,
```

### `r770-a.A5_tree_built_without_the_refusal`

bridge_intake_tree: build the tree without asking first, the layer the landing's pre-move check rests on alone

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A5_tree_built_without_the_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_every_intake_emitter_caller_builds_its_tree_through_the_one_refusing_builder`
  - `tests/test_intake_writers_native.py::test_the_bridge_landing_engine_refuses_a_native_tree_the_same_way_and_moves_nothing`

Old text:

```
    assert_intake_on_the_bridge(declared, registry)
    return rbxml.intake_tree(declared, registry)
```

New text:

```
    return rbxml.intake_tree(declared, registry)
```

### `r770-a.A6_splice_asks_only_after_the_export`

place_files: drop the refusal made before the export is looked for, leaving the one made where the tree is built

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A6_splice_asks_only_after_the_export`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_the_splice_refuses_a_native_intake_tree_naming_the_landing`

Old text:

```
    if declared is not None and registry is not None:
        assert_intake_on_the_bridge(declared, registry)
```

New text:

```
    if declared is not None and registry is not None:
        pass
```

### `u113-b.B2_batch_keeps_claimed`

The batch playlist in the intake file holds the claimed files too

- File: `src/cratekit/intake/ingest.py`
- Source: `u113-b.json`, row `B2_batch_keeps_claimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`
- Collected: 73 against a baseline of 73
- Kills: 9 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_a_row_that_only_resembles_a_file_does_not_claim_it`
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists.py::test_an_account_playlist_whose_dated_name_is_the_batchs_takes_two`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`
  - `tests/test_intake_land_account_playlists.py::test_two_swept_playlists_land_as_two_inbox_playlists_under_their_exact_names`

Old text:

```
    rest = [item.track_id for item in placed if item.path not in claimed]
```

New text:

```
    rest = [item.track_id for item in placed]
```

### `u113-b.B3_record_unnamed`

The intake session record does not list the account playlists, so the rotation cannot age them

- File: `src/cratekit/intake/ingest.py`
- Source: `u113-b.json`, row `B3_record_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_rerun_of_the_same_pass_is_a_no_op`
  - `tests/test_intake_land_account_playlists.py::test_the_intake_record_names_each_playlist_and_its_batch_folder`

Old text:

```
        record.detail[INBOX_PLAYLISTS_KEY] = [
```

New text:

```
        record.detail["inbox_playlists_unread"] = [
```

### `u113-b.B4_steps_name_one`

The import steps name only the first playlist when the file holds several

- File: `src/cratekit/intake/ingest.py`
- Source: `u113-b.json`, row `B4_steps_name_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`

Old text:

```
    if len(playlists) > 1:
```

New text:

```
    if len(playlists) > 99:
```

### `u128-b.B4_bridge_owned_dropped`

The intake file's playlist names no owned TrackID, the new files alone

- File: `src/cratekit/intake/ingest.py`
- Source: `u128-b.json`, row `B4_bridge_owned_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`

Old text:

```
            else:
                held.append(member)
        return list(dict.fromkeys(held))
```

New text:

```
        return list(dict.fromkeys(held))
```

### `u128-b.B5_bridge_record_no_account`

The intake file's record names no account, so a rerun cannot find what it mirrored

- File: `src/cratekit/intake/ingest.py`
- Source: `u128-b.json`, row `B5_bridge_record_no_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`
- Collected: 201 against a baseline of 201
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_rerun_of_the_same_pass_is_a_no_op`
  - `tests/test_intake_land_account_playlists.py::test_the_intake_record_names_each_playlist_and_its_batch_folder`

Old text:

```
                INBOX_ACCOUNT_KEY: one.account,
```

New text:

```
                INBOX_ACCOUNT_KEY: "",
```

### `u37-author-light.G4_staging`

Allow inbox of files still under download staging

- File: `src/cratekit/intake/ingest.py`
- Source: `u37-author-light.json`, row `G4_staging`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_pipeline.py::test_staging_files_are_refused`

Old text:

```
    if resolved == staging or staging in resolved.parents:
```

New text:

```
    if False and (resolved == staging or staging in resolved.parents):
```

### `r924.F1_no_start_line`

The fetch never says it started

- File: `src/cratekit/intake/fetch.py`
- Source: `r924.json`, row `F1_no_start_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_fetch_that_raises_still_stops_the_watcher`
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`

Old text:

```
            progress(f"fetching: {address}")
```

New text:

```
            pass
```

### `r924.F2_no_landed_line`

The fetch never says what landed

- File: `src/cratekit/intake/fetch.py`
- Source: `r924.json`, row `F2_no_landed_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`

Old text:

```
            progress(f"fetched: {megabytes(landed.stat().st_size)} in {elapsed}s")
```

New text:

```
            pass
```

### `r924.F4_sum_not_largest`

The bytes said are the sum of every file in the folder rather than the largest

- File: `src/cratekit/intake/fetch.py`
- Source: `r924.json`, row `F4_sum_not_largest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 11 against a baseline of 11
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_the_bytes_said_are_the_largest_file_and_not_the_sum`

Old text:

```
                largest = max(largest, one.stat().st_size)
```

New text:

```
                largest += one.stat().st_size
```

### `r924.F5_watcher_not_joined`

The watcher is told to stop and not waited for, so it can outlive the fetch

- File: `src/cratekit/intake/fetch.py`
- Source: `r924.json`, row `F5_watcher_not_joined`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 22539 against a baseline of 22539
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        stop.set()
        watcher.join()
```

New text:

```
        stop.set()
```

### `u104-a.F1_guard_string_layer`

Drop the textual half of the library guard: a scratch folder that resolves to the library or to a path under it is no longer refused by name

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-a.json`, row `F1_guard_string_layer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_library_that_is_not_there_is_still_refused_by_name`

Old text:

```
    if here == library or library in here.parents:
        raise ScratchUnderLibrary(here, library)
    if not library.exists():
```

New text:

```
    if not library.exists():
```

### `u104-a.F2_guard_samefile_layer`

Drop the filesystem half of the library guard: two spellings of one folder that resolve does not settle are no longer compared with samefile

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-a.json`, row `F2_guard_samefile_layer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_library_guard_asks_the_filesystem_and_not_only_the_strings`

Old text:

```
        if ancestor.exists() and ancestor.samefile(library):
            raise ScratchUnderLibrary(here, library)
```

New text:

```
        if ancestor.exists() and ancestor.samefile(library):
            pass
```

### `u104-a.F3_guard_absent_library_return`

Drop the early return for a library root that is not there, so samefile is asked about a folder that does not exist

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-a.json`, row `F3_guard_absent_library_return`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_library_that_is_not_there_has_nothing_to_be_inside`

Old text:

```
    if not library.exists():
        return

```

New text:

```
(empty)
```

### `u104-a.F4_landing_inside_scratch`

Drop the half of the landing check that requires the fetched file to be inside the scratch folder it was handed

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-a.json`, row `F4_landing_inside_scratch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch[outside]`

Old text:

```
        if not landed.is_file() or scratch.resolve() not in landed.resolve().parents:
```

New text:

```
        if not landed.is_file():
```

### `u104-b.F5_landing_is_a_file`

Drop the half of the landing check that requires the fetcher's answer to be a file that exists

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-b.json`, row `F5_landing_is_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch[not-there]`

Old text:

```
        if not landed.is_file() or scratch.resolve() not in landed.resolve().parents:
```

New text:

```
        if scratch.resolve() not in landed.resolve().parents:
```

### `u104-b.F6_clear_before_attempt`

Stop clearing the scratch folder before an attempt: reuse whatever a killed process left in it

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-b.json`, row `F6_clear_before_attempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_mix_url_runs_the_ordinary_set_pipeline_over_the_fetched_file`

Old text:

```
            if scratch.exists():
                shutil.rmtree(scratch)
            scratch.mkdir(parents=True)
```

New text:

```
            scratch.mkdir(parents=True, exist_ok=True)
```

### `u104-b.F7_remove_on_exit`

Drop the removal of the scratch folder when the pass ends, so a fetched mix stays on disk

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-b.json`, row `F7_remove_on_exit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 11 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[failed]`
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[several]`
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[timed-out]`
  - `tests/intake/test_set_fetch.py::test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch[not-there]`
  - `tests/intake/test_set_fetch.py::test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch[outside]`
  - `tests/intake/test_set_fetch.py::test_a_mix_nobody_recognised_is_an_honest_zero_that_names_the_address`
  - `tests/intake/test_set_fetch.py::test_a_mix_url_runs_the_ordinary_set_pipeline_over_the_fetched_file`
  - `tests/intake/test_set_fetch.py::test_a_refusal_from_inside_the_identifier_names_the_address_and_not_the_scratch_file`
  - `tests/intake/test_set_fetch.py::test_identification_that_raises_still_removes_the_fetched_mix`
  - `tests/intake/test_set_fetch.py::test_identify_over_a_url_writes_a_tracklist_named_for_the_address`
  - `tests/intake/test_set_fetch.py::test_the_page_a_mix_came_from_is_frozen_on_the_set_job`

Old text:

```
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
        if scratch.exists():
```

New text:

```
    finally:
        if scratch.exists():
```

### `u104-b.F8_leftover_recorded`

Drop the record of a scratch folder that could not be removed, so the envelope says nothing about it

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-b.json`, row `F8_leftover_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_scratch_folder_that_cannot_be_removed_is_said_on_the_envelope`

Old text:

```
        if scratch.exists():
            held.leftover = str(scratch)
```

New text:

```
        if scratch.exists():
            pass
```

### `u104-b.F9_scratch_prepare_is_its_own_kind`

Report a scratch folder that cannot be made as an ordinary failed fetch rather than as a fact about this machine

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-b.json`, row `F9_scratch_prepare_is_its_own_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_scratch_folder_that_cannot_be_made_is_a_fact_about_this_machine`

Old text:

```
            raise ScratchUnusable(
                f"the scratch folder {scratch} could not be prepared "
```

New text:

```
            raise SetFetchFailed(
                f"the scratch folder {scratch} could not be prepared "
```

### `u104-c.P1_numbered_output`

Put the fixed output name back, so every entry of a playlist address lands on one file name and a set page reads as one recording

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-c.json`, row `P1_numbered_output`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_shipped_fetcher_runs_u80s_download_under_a_mix_sized_bound`

Old text:

```
        argv[template] = str(directory / f"{fallback.FETCH_STEM}-%(autonumber)s.%(ext)s")
```

New text:

```
        argv[template] = str(directory / f"{fallback.FETCH_STEM}.%(ext)s")
```

### `u104-c.P2_probe_bound`

Raise the playlist probe from two entries to twenty, a realistic nearby value that downloads most of a set page to learn it is one

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-c.json`, row `P2_probe_bound`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_shipped_fetcher_runs_u80s_download_under_a_mix_sized_bound`

Old text:

```
PLAYLIST_PROBE = 2
```

New text:

```
PLAYLIST_PROBE = 20
```

### `u104-c.P3_several_threshold`

Move the several recordings threshold from more than one to more than two, so exactly two landed recordings read as an ordinary failure

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-c.json`, row `P3_several_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_shipped_fetcher_refuses_a_playlist_that_landed_two_recordings`

Old text:

```
            if len(landed) > 1:
```

New text:

```
            if len(landed) > 2:
```

### `u104-c.P4_timeout_is_its_own_kind`

Drop the branch that tells a timed out download from every other failed one, so nothing is ever called retryable

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-c.json`, row `P4_timeout_is_its_own_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_shipped_fetcher_says_a_timeout_as_the_one_retryable_kind`

Old text:

```
            if isinstance(exc.__cause__, subprocess.TimeoutExpired):
                raise SetFetchTimedOut(str(exc)) from exc

```

New text:

```
(empty)
```

### `u104-c.P5_stem_bound`

Multiply the tracklist stem bound by ten, 80 to 800, past what a file name may hold

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-c.json`, row `P5_stem_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_tracklist_stem_is_the_last_segment_reduced_to_a_safe_name[url6-E3-81-82-E3-81-82-E3-81-82-E3-81-82-E3-81-82-E3-81-82-E3-81-82-E3-81-82-E3-81-82]`

Old text:

```
STEM_MAX_CHARS = 80
```

New text:

```
STEM_MAX_CHARS = 800
```

### `u104-c.P6_address_is_stripped`

Stop stripping the address before it is digested, so a stray space names a second scratch folder for one mix

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-c.json`, row `P6_address_is_stripped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_scratch_entry_is_declared_under_the_installation_root`

Old text:

```
    token = hashlib.sha256(url.strip().encode("utf-8")).hexdigest()[:SCRATCH_DIGEST_CHARS]
```

New text:

```
    token = hashlib.sha256(url.encode("utf-8")).hexdigest()[:SCRATCH_DIGEST_CHARS]
```

### `u121.S18_info_json_flag`

_MixDownload.argv: do not ask yt-dlp for the info document

- File: `src/cratekit/intake/fetch.py`
- Source: `u121.json`, row `S18_info_json_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_shipped_fetcher_runs_u80s_download_under_a_mix_sized_bound`

Old text:

```
        argv[1:1] = ["--playlist-end", str(PLAYLIST_PROBE), "--write-info-json"]
```

New text:

```
        argv[1:1] = ["--playlist-end", str(PLAYLIST_PROBE)]
```

### `u166.C10_live_filter`

live_members: count a removed membership as held

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C10_live_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1041 against a baseline of 1041
- Kills: 5 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_with_no_analysis_path_or_analysed_unset_stays`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`
  - `tests/test_inbox_analyzed.py::test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name`
  - `tests/test_inbox_analyzed.py::test_nothing_analysed_asks_a_late_analysis_is_stale_a_track_held_twice_clears_once_then_nothing`

Old text:

```
        if not rb_writer.membership_removed(song)
```

New text:

```
        if True
```

### `u166.C1_removed_row`

_member: clear a row whose collection row was removed

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C1_removed_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1041 against a baseline of 1041
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`

Old text:

```
    if removed:
        return Member(content_id=content_id, title=title, action=WAIT, why=ROW_REMOVED)
```

New text:

```
    if False:
        return Member(content_id=content_id, title=title, action=WAIT, why=ROW_REMOVED)
```

### `u166.C2_analysed_flag`

_member: clear a row whose Analysed is unset

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C2_analysed_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1041 against a baseline of 1041
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_with_no_analysis_path_or_analysed_unset_stays`

Old text:

```
    if not int(getattr(row, "Analysed", 0) or 0):
```

New text:

```
    if False:
```

### `u166.C3_analysis_path`

_member: clear a row with no analysis path

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C3_analysis_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1041 against a baseline of 1041
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_with_no_analysis_path_or_analysed_unset_stays`

Old text:

```
    if not str(getattr(row, "AnalysisDataPath", "") or "").strip():
```

New text:

```
    if False:
```

### `u166.C4_blank_path`

_member: read a blank analysis path as present

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C4_blank_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1041 against a baseline of 1041
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_with_no_analysis_path_or_analysed_unset_stays`

Old text:

```
    if not str(getattr(row, "AnalysisDataPath", "") or "").strip():
```

New text:

```
    if not str(getattr(row, "AnalysisDataPath", "") or ""):
```

### `u166.C5_missing_row`

_member: clear a membership whose collection row is missing

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C5_missing_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1041 against a baseline of 1041
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`

Old text:

```
    if row is None:
        return Member(content_id=content_id, title="", action=WAIT, why=NO_ROW)
```

New text:

```
    if row is None:
        return Member(content_id=content_id, title="", action=CLEAR)
```

### `u166.C6_stale_check`

apply_clear: apply a plan whose digest moved

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C6_stale_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1041 against a baseline of 1041
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_nothing_analysed_asks_a_late_analysis_is_stale_a_track_held_twice_clears_once_then_nothing`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u166.C7_clear_waits_too`

apply_clear: remove every member, waiting ones too

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C7_clear_waits_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1041 against a baseline of 1041
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_with_no_analysis_path_or_analysed_unset_stays`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`

Old text:

```
rb_writer.remove_memberships(db, playlist, plan.clears())
```

New text:

```
rb_writer.remove_memberships(db, playlist, [m.content_id for m in plan.members])
```

### `u166.C8_read_back_lost`

assert_read_back: stop refusing a waiting row gone

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C8_read_back_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1041 against a baseline of 1041
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_read_back_refuses_a_waiting_row_gone_or_a_cleared_row_kept_and_the_digest_reads_all`

Old text:

```
    if lost or kept:
```

New text:

```
    if kept:
```

### `u166.C9_read_back_kept`

assert_read_back: stop refusing a cleared row kept

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C9_read_back_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1041 against a baseline of 1041
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`
  - `tests/test_inbox_analyzed.py::test_the_read_back_refuses_a_waiting_row_gone_or_a_cleared_row_kept_and_the_digest_reads_all`

Old text:

```
    if lost or kept:
```

New text:

```
    if lost:
```

### `u259.M1_judge_no_row`

analyzed.judge: drop the answer for a row the collection lacks, so None reaches the removal marker read

- File: `src/cratekit/intake/analyzed.py`
- Source: `u259.json`, row `M1_judge_no_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`, `tests/test_inbox_analyzed.py`
- Collected: 84 against a baseline of 84
- Kills: 6 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_row_whose_id_is_not_text_stays_out_of_every_row_as_it_did`
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_read_row_handed_no_row_reads_it_and_answers_as_handed_one`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_for_a_named_landing`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_in_inbox_analyze`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`

Old text:

```
    if row is None:
        return Member(content_id=content_id, title="", action=WAIT, why=NO_ROW)
```

New text:

```
    if False:
        return Member(content_id=content_id, title="", action=WAIT, why=NO_ROW)
```

### `u259.M5_member_reads_nothing`

analyzed.member: judge no row instead of the row read by ID, so the clear reads every member as missing

- File: `src/cratekit/intake/analyzed.py`
- Source: `u259.json`, row `M5_member_reads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`, `tests/test_inbox_analyzed.py`
- Collected: 84 against a baseline of 84
- Kills: 16 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[analyze]`
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[unanalysed]`
  - `tests/test_analyze_check.py::test_a_row_the_binding_cannot_load_after_one_that_refuses_still_refuses_as_it_did`
  - `tests/test_analyze_check.py::test_a_row_whose_id_is_not_text_stays_out_of_every_row_as_it_did`
  - `tests/test_analyze_check.py::test_a_row_whose_removal_marker_cannot_be_read_refuses_as_it_did[analyze]`
  - `tests/test_analyze_check.py::test_a_row_whose_removal_marker_cannot_be_read_refuses_as_it_did[unanalysed]`
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_for_a_named_landing`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_in_inbox_analyze`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_over_every_row`
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_with_no_analysis_path_or_analysed_unset_stays`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`
  - `tests/test_inbox_analyzed.py::test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    return judge(content_id, db.get_content(ID=content_id))
```

New text:

```
    return judge(content_id, None)
```

### `r770-b.B5_file_verb_never_takes_the_native_path`

intake_file: ignore the switch, which is the verb as it was before this unit

- File: `src/cratekit/intake/file_cli.py`
- Source: `r770-b.json`, row `B5_file_verb_never_takes_the_native_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 16 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy`
  - `tests/test_intake_writers_native.py::test_a_file_already_in_the_collection_gains_a_membership_and_no_second_row`
  - `tests/test_intake_writers_native.py::test_a_file_named_through_a_link_is_stored_under_the_configured_root`
  - `tests/test_intake_writers_native.py::test_a_file_the_native_medium_cannot_take_is_refused_before_the_gate[_from_staging-intake-staging-refused]`
  - `tests/test_intake_writers_native.py::test_a_file_the_native_medium_cannot_take_is_refused_before_the_gate[_outside_the_library-intake-list-unusable]`
  - `tests/test_intake_writers_native.py::test_a_file_the_native_medium_cannot_take_is_refused_before_the_gate[_rekordbox_running-rekordbox-running]`
  - `tests/test_intake_writers_native.py::test_a_file_the_native_medium_cannot_take_is_refused_before_the_gate[_unplaceable-intake-list-unusable]`
  - `tests/test_intake_writers_native.py::test_a_file_the_native_medium_cannot_take_is_refused_before_the_gate[_untyped-intake-list-unusable]`
  - `tests/test_intake_writers_native.py::test_an_answer_is_stale_once_the_file_changed_after_it[_grown]`
  - `tests/test_intake_writers_native.py::test_an_answer_is_stale_once_the_file_changed_after_it[_reartisted]`
  - `tests/test_intake_writers_native.py::test_an_answer_is_stale_once_the_file_changed_after_it[_retitled]`
  - `tests/test_intake_writers_native.py::test_an_export_on_a_native_tree_is_refused_by_name_and_not_as_a_defect`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`
  - `tests/test_intake_writers_native.py::test_no_acknowledgment_refuses_before_the_gate`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    if medium.native:
```

New text:

```
    if False:
```

### `r770-b.B6_export_taken_on_a_native_tree`

_file_native: do not refuse --export, so an export named on a native tree is silently ignored

- File: `src/cratekit/intake/file_cli.py`
- Source: `r770-b.json`, row `B6_export_taken_on_a_native_tree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_an_export_on_a_native_tree_is_refused_by_name_and_not_as_a_defect`

Old text:

```
    if ctx.args.export is not None:
```

New text:

```
    if False:
```

### `r770-b.B7_staging_not_asked_first`

_file_native: drop the staging refusal, so a staged file is told it is outside the library

- File: `src/cratekit/intake/file_cli.py`
- Source: `r770-b.json`, row `B7_staging_not_asked_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_file_the_native_medium_cannot_take_is_refused_before_the_gate[_from_staging-intake-staging-refused]`

Old text:

```
    ingest.assert_not_staging(path, cfg)

```

New text:

```
(empty)
```

### `r770-b.B8_target_spelled_as_resolved`

_in_the_library: answer the resolved path, so a file outside the library is not refused and a linked root is spelled through

- File: `src/cratekit/intake/file_cli.py`
- Source: `r770-b.json`, row `B8_target_spelled_as_resolved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_file_named_through_a_link_is_stored_under_the_configured_root`
  - `tests/test_intake_writers_native.py::test_a_file_the_native_medium_cannot_take_is_refused_before_the_gate[_outside_the_library-intake-list-unusable]`

Old text:

```
        return root / path.resolve().relative_to(root.resolve())
```

New text:

```
        return path.resolve()
```

### `r770-c.C1_unplaceable_file_reaches_the_gate`

_file_native: do not ask whether a declared sub would take the file

- File: `src/cratekit/intake/file_cli.py`
- Source: `r770-c.json`, row `C1_unplaceable_file_reaches_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_file_the_native_medium_cannot_take_is_refused_before_the_gate[_unplaceable-intake-list-unusable]`

Old text:

```
    if ingest.decide_placement(meta, declared) is None:
```

New text:

```
    if False:
```

### `r770-c.C2_untyped_suffix_reaches_the_gate`

_file_native: do not refuse a suffix the database has no file type for

- File: `src/cratekit/intake/file_cli.py`
- Source: `r770-c.json`, row `C2_untyped_suffix_reaches_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_file_the_native_medium_cannot_take_is_refused_before_the_gate[_untyped-intake-list-unusable]`

Old text:

```
    if native.file_type_of(target) is None:
```

New text:

```
    if False:
```

### `r770-c.C5_playlist_named_for_the_whole_file_name`

_file_native: name the batch playlist with the suffix on, a nearby name

- File: `src/cratekit/intake/file_cli.py`
- Source: `r770-c.json`, row `C5_playlist_named_for_the_whole_file_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_file_already_in_the_collection_gains_a_membership_and_no_second_row`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
            batch=path.stem,
```

New text:

```
            batch=path.name,
```

### `r770-d.C6_digest_without_the_collection_plan`

_native_payload: take the digest over the verb's own plan alone, so a changed row is not a changed plan

- File: `src/cratekit/intake/file_cli.py`
- Source: `r770-d.json`, row `C6_digest_without_the_collection_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_an_answer_is_stale_once_the_file_changed_after_it[_grown]`

Old text:

```
    identity = {"kind": "file", "file": plan["digest"], "collection": rows.digest}
```

New text:

```
    identity = {"kind": "file", "file": plan["digest"]}
```

### `u154.G12_empty_plan_asks_a_gate`

a plan that moves nothing is put to the gate

- File: `src/cratekit/intake/shelve_cli.py`
- Source: `u154.json`, row `G12_empty_plan_asks_a_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_plan_of_nothing_and_every_command_line_refusal_refuse_before_a_gate`

Old text:

```
    if planned.batches:
        return
    raise refuse(

```

New text:

```
    if True:
        return
    raise refuse(

```

### `u154.G13_as_with_all_admitted`

one subject is applied to every batch under --all

- File: `src/cratekit/intake/shelve_cli.py`
- Source: `u154.json`, row `G13_as_with_all_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_plan_of_nothing_and_every_command_line_refusal_refuse_before_a_gate`

Old text:

```
    if subject is not None and (everything or len(names) != 1):

```

New text:

```
    if False:

```

### `u154.R2_subject_path_part_admitted`

a subject carrying a slash composes a nested target

- File: `src/cratekit/intake/shelve_cli.py`
- Source: `u154.json`, row `R2_subject_path_part_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
    if subject is not None and not landing.plain_name(subject.strip()):

```

New text:

```
    if False:

```

### `u164.S1_already_filed`

intake shelve: plan a filed batch as before, refusing it as no folder

- File: `src/cratekit/intake/shelve_cli.py`
- Source: `u164.json`, row `S1_already_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_shelve.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_landing_on_the_27th_lands_in_its_year_folder_under_its_subject`

Old text:

```
    filed = _already_filed(cfg, names)
```

New text:

```
    filed = {}
```

### `u164.S2_music_folder_wins`

_already_filed: call a batch filed even when a folder of its name is under the music folder

- File: `src/cratekit/intake/shelve_cli.py`
- Source: `u164.json`, row `S2_music_folder_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_shelve.py`
- Collected: 29 against a baseline of 29
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over`
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[four-hex-before-u235]`
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[sixteen-hex-since-u235]`
  - `tests/test_intake_shelve.py::test_apply_moves_the_folder_rewrites_the_paths_keeps_the_rest_and_the_name_stays_taken`
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
        if name in folders and not os.path.lexists(landing.target_dir(cfg, name))
```

New text:

```
        if name in folders
```

### `r1255.F2_refill_warning_wording`

warnings_of: word an unlisted log as a count of records

- File: `src/cratekit/intake/refill_cli.py`
- Source: `r1255.json`, row `F2_refill_warning_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_refill.py`
- Collected: 28 against a baseline of 28
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_matches_by_name_and_an_unlisted_log_is_named_as_one`
  - `tests/test_session_log_unlisted.py::test_the_refill_warns_on_a_log_it_could_not_list_or_records_it_could_not_read`

Old text:

```
                        if plan.log_unlisted
```

New text:

```
                        if False
```

### `u134-b.B5_no_writes_no_op`

Apply a plan that adds nothing instead of ending no_op

- File: `src/cratekit/intake/refill_cli.py`
- Source: `u134-b.json`, row `B5_no_writes_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_in_account_order_and_once`
  - `tests/test_inbox_refill.py::test_two_playlists_of_the_accounts_name_are_neither_filled_and_one_is_found_by_it`

Old text:

```
    if not plan.writes:
```

New text:

```
    if False:
```

### `u134-b.B6_ack_before_gate`

Drop the backup acknowledgment read before the plan and the gate

- File: `src/cratekit/intake/refill_cli.py`
- Source: `u134-b.json`, row `B6_ack_before_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `u144-c.C8_question_named`

Library rows: name an unanswered question as a track the library lacks

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u144-c.json`, row `C8_question_named`
- Moved: the same answer for a track whose match waits on a person, now one entry of set_playlist.py's _NO_MATCH table, which U307 made of the branches
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_near_match_is_a_question_named_as_a_miss_and_never_written`

Old text:

```
_NO_MATCH = {match.MatchState.NEEDS_REVIEW: UNANSWERED,
```

New text:

```
_NO_MATCH = {match.MatchState.NEEDS_REVIEW: NOT_HELD,
```

### `r770-c.C3_failure_past_the_gate_loses_its_reason`

write: report every failure past the gate as internal-error, whatever refused

- File: `src/cratekit/intake/landing.py`
- Source: `r770-c.json`, row `C3_failure_past_the_gate_loses_its_reason`
- Moved: the same reason kept for a failure past the gate, now in landing.refuse_past, which U307 made of the copies in file_cli.py and the other landing verbs; file_cli.py calls it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy`

Old text:

```
        inner.reason if inner is not None else "internal-error",
```

New text:

```
        "internal-error",
```

### `r770-c.C4_failure_past_the_gate_loses_its_remedy`

write: drop the inner refusal's remedy, so the reason's default answers

- File: `src/cratekit/intake/landing.py`
- Source: `r770-c.json`, row `C4_failure_past_the_gate_loses_its_remedy`
- Moved: the same remedy kept for a failure past the gate, now in landing.refuse_past, which U307 made of the copies in file_cli.py and the other landing verbs; file_cli.py calls it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy`

Old text:

```
        remedy=inner.remediation.remedy if inner is not None else None,
```

New text:

```
        remedy=None,
```

### `r706-c.C4_pipeline_drops_parts`

identify_only does not carry parts through, so every verb sees one

- File: `src/cratekit/intake/pipeline.py`
- Source: `r706-c.json`, row `C4_pipeline_drops_parts`
- Moved: the same copy of parts into the verb's result, which U307 made one comprehension over the fields; leaving parts out gives its default of one, as the dropped argument did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`

Old text:

```
    copied = {one.name: getattr(found, one.name) for one in fields(recognize.Identified)}
```

New text:

```
    copied = {one.name: getattr(found, one.name) for one in fields(recognize.Identified) if one.name != "parts"}
```

### `u103-b.P2_digest_reaches_the_verb`

Drop the recording's digest between the identifier and the verb, so the tracklist falls back to a path name

- File: `src/cratekit/intake/pipeline.py`
- Source: `u103-b.json`, row `P2_digest_reaches_the_verb`
- Moved: the same copy of the digest into the verb's result, which U307 made one comprehension over the fields; leaving digest out gives its empty default, as the dropped argument did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_set_and_identify_write_the_same_tracklist_naming_every_row_in_order`

Old text:

```
    copied = {one.name: getattr(found, one.name) for one in fields(recognize.Identified)}
```

New text:

```
    copied = {one.name: getattr(found, one.name) for one in fields(recognize.Identified) if one.name != "digest"}
```

