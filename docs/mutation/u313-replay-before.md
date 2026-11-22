# Mutation table: u313-replay-before

Measured by `scripts/mutate.py` on 2026-11-22 16:58 UTC, branch `HEAD` at `c9192091`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 296.

Full baseline: measured by this driver (the battery's verdict was not read: the tree was not clean throughout the battery's run).

Subset baselines: 27, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u276.K10_stage_script_default_whole` | `scripts/analyze_stages.py` | maintainer | 1 file(s) | 24 | 1 | killed |
| `u276.K16_json_totals_keep_harmonic` | `scripts/analyze_stages.py` | maintainer | 1 file(s) | 24 | 1 | killed |
| `u276.K7_stage_table_keeps_every_row` | `scripts/analyze_stages.py` | maintainer | 1 file(s) | 24 | 1 | killed |
| `u276.K8_stage_table_drops_too_much` | `scripts/analyze_stages.py` | maintainer | 1 file(s) | 24 | 3 | killed |
| `u297.B10_a_changed_mode_unseen` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 1 | killed |
| `u297.B11_a_changed_schema_unseen` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 5 | killed |
| `u297.B1_a_root_outside_the_temporary_directory` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 3 | killed |
| `u297.B2_the_temporary_directory_itself` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 1 | killed |
| `u297.B3_somebodys_directory_emptied` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 3 | killed |
| `u297.B4_a_failed_run_closed_as_a_capture` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 1 | killed |
| `u297.B5_a_scenario_with_no_record_closed_over` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 4 | killed |
| `u297.B6_any_two_texts_the_same` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 21 | killed |
| `u297.B7_a_word_read_inside_a_longer_one` | `scripts/behaviour_compare.py` | maintainer | 1 file(s) | 137 | 3 | killed |
| `u297.B8_a_changed_exit_code_unseen` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 2 | killed |
| `u297.B9_a_file_in_one_capture_only_unseen` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 2 | killed |
| `u122.H1_no_hold` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 8 | killed |
| `u122.H2_review_not_held` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 5 | killed |
| `u122.H3_progress_not_held` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 5 | killed |
| `u122.H4_hold_flattened` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 4 | killed |
| `u122.H5_units_only` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 4 | killed |
| `u122.H6_hold_beats_closure` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 4 | killed |
| `u122.H7_attended_beats_hold` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 2 | killed |
| `u122.N1_next_busy_progress_only` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 1 | killed |
| `u122.N2_next_offers_busy` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 2 | killed |
| `u122.N3_next_no_status` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 2 | killed |
| `u124-b19.B19_audit_reads_folder` | `scripts/board.py` | maintainer | 2 file(s) | 141 | 1 | killed |
| `u124.B10_validate_first` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u124.B11_relanded_title` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u124.B12_highest_not_count` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 5 | killed |
| `u124.B13_separator` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u124.B14_files_deleted` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 3 | killed |
| `u124.B15_closing_reads_folder` | `scripts/board.py` | maintainer | 2 file(s) | 141 | 3 | killed |
| `u124.B17_land_on_main_only` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u124.B18_behind_origin` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u124.B1_untracked_filter` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u124.B2_readme_excluded` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 2 | killed |
| `u124.B3_name_order` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 3 | killed |
| `u124.B4_fence_open` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 2 | killed |
| `u124.B5_unknown_key` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u124.B6_required_keys` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 5 | killed |
| `u124.B7_issue_values` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u124.B8_numbered_title` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u124.B9_empty_body` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u148.C1_one_short_allowed` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 2 | killed |
| `u148.C2_count_off` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 2 | killed |
| `u148.C3_no_count_skips` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 2 | killed |
| `u148.C4_only_none_refused` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 1 | killed |
| `u148.C5_issue_count_dropped` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 2 | killed |
| `u148.L1_old_limit` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 4 | killed |
| `u148.L2_issue_literal` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 8 | killed |
| `u148.N1_truncation_blamed_on_token` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 1 | killed |
| `u148.S1_branch_before_read` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 1 | killed |
| `u148.S2_claims_in_progress` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 1 | killed |
| `u148.W1_full_page_taken` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 3 | killed |
| `u148.W2_whole_off` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 3 | killed |
| `u148.W3_issue_whole_dropped` | `scripts/board.py` | maintainer | 4 file(s) | 182 | 3 | killed |
| `u151.A1_archived_read` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u151.C1_no_cursor_trusted` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u151.C2_page_bound_short` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u151.F1_cursor_typed` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u151.M1_membership_count_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u151.M2_issue_count_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 2 | killed |
| `u151.N1_number_filter_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u151.O1_owner_filter_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u151.O2_owner_case_sensitive` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u151.U1_unblocks_always_written` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 5 | killed |
| `u151.U2_added_card_zero` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u151.X1_next_skips_context` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u151.X2_no_org_fallback` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u151.X3_status_refusal_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u151.X4_unseen_project_trusted` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 2 | killed |
| `u151.X5_field_count_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 59 | 1 | killed |
| `u158.M1_card_not_judged` | `scripts/board.py` | maintainer | 1 file(s) | 101 | 2 | killed |
| `u158.M2_any_branch_names_a_card` | `scripts/board.py` | maintainer | 1 file(s) | 101 | 1 | killed |
| `u158.M3_implied_close_not_a_reference` | `scripts/board.py` | maintainer | 1 file(s) | 101 | 2 | killed |
| `u187.A1_relayed_answer_never_matches` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 3 | killed |
| `u187.A2_answer_counted_as_a_hold` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 3 | killed |
| `u187.A3_answer_not_read_as_reply` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 2 | killed |
| `u187.A4_heading_drifts` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 3 | killed |
| `u196.S1_any_word` | `scripts/board.py` | maintainer | 1 file(s) | 6 | 1 | killed |
| `u196.S2_case_sensitive` | `scripts/board.py` | maintainer | 1 file(s) | 6 | 2 | killed |
| `u196.S3_empty_search` | `scripts/board.py` | maintainer | 1 file(s) | 6 | 1 | killed |
| `u196.S4_missing_ledger_no_match` | `scripts/board.py` | maintainer | 1 file(s) | 6 | 1 | killed |
| `u203.M1_no_opening_span` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 4 | killed |
| `u203.M2_span_closer_any_follower` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u203.M3_no_sentence_cut` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 2 | killed |
| `u203.M4_sentence_cut_anywhere` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u203.M5_no_trailing_strip` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 7 | killed |
| `u203.M6_one_pass` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u203.M7_rule_line_is_a_heading` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u203.M8_ellipsis_not_trailing` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u203.M9_no_comma_cut` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u291.L1_lanes_back_to_five` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 4 | killed |
| `u291.L2_lanes_one_short` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 4 | killed |
| `u291.L3_lanes_one_over` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 4 | killed |
| `u291.L4_help_names_a_literal` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 1 | killed |
| `u291.L5_default_ignores_the_constant` | `scripts/board.py` | maintainer | 1 file(s) | 40 | 3 | killed |
| `u59.B1_per_message_split` | `scripts/board.py` | user | 1 file(s) | 101 | 1 | killed |
| `u59.B2_raw_true_on_range` | `scripts/board.py` | user | 1 file(s) | 101 | 1 | killed |
| `u59.B3_unit_mapping_ignored` | `scripts/board.py` | user | 1 file(s) | 101 | 1 | killed |
| `u59.B4_guess_caveat_dropped` | `scripts/board.py` | maintainer | 1 file(s) | 101 | 1 | killed |
| `u59.B6_duplicate_unit_kept` | `scripts/board.py` | maintainer | 1 file(s) | 101 | 2 | killed |
| `u59.B8_missing_file_raises` | `scripts/board.py` | maintainer | 1 file(s) | 101 | 1 | killed |
| `u81-round-2.B5_owed_argument_ignored` | `scripts/board.py` | user | 1 file(s) | 101 | 2 | killed |
| `u81-round-3.B5_audit_drops_the_detector` | `scripts/board.py` | user | 1 file(s) | 101 | 1 | killed |
| `u81-round-3.B5_audit_exit_code` | `scripts/board.py` | user | 1 file(s) | 101 | 1 | killed |
| `u81-round-3.B5_owed_default_dropped` | `scripts/board.py` | user | 1 file(s) | 101 | 2 | killed |
| `u81.B5_composite` | `scripts/board.py` | maintainer | 7 file(s) | 2398 | 1 | killed |
| `u81.B5_contradictions_by_number` | `scripts/board.py` | user | 1 file(s) | 101 | 3 | killed |
| `u81.B5_residual_repoint_dropped` | `scripts/board.py` | user | 1 file(s) | 101 | 1 | killed |
| `u200.M11_complete_clone_fetched` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 1 | killed |
| `u200.M1_unreadable_read_as_complete` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 1 | killed |
| `u200.M2_no_fetch` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 2 | killed |
| `u200.M3_no_reread` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 3 | killed |
| `u268.W11_error_count_singular_only` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 1 | killed |
| `u268.W1_id_cut_at_space` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 8 | killed |
| `u268.W2_errors_not_read` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 25 | killed |
| `u268.W3_no_report_read_as_clean` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 1 | killed |
| `u268.W4_counts_not_checked` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 1 | killed |
| `u268.W5_listed_not_checked` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 1 | killed |
| `u268.W6_id_with_line_break_stored` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 4 | killed |
| `u271-measured.B1_run_cleanliness_at_the_end_only` | `scripts/cloud_battery.py` | maintainer | 2 file(s) | 244 | 2 | killed |
| `u271-measured.B2_commit_read_after_the_run` | `scripts/cloud_battery.py` | maintainer | 2 file(s) | 244 | 1 | killed |
| `u271-measured.B3_status_unread` | `scripts/cloud_battery.py` | maintainer | 2 file(s) | 244 | 3 | killed |
| `u271-measured.B4_release_line_never_dirty` | `scripts/cloud_battery.py` | maintainer | 3 file(s) | 304 | 3 | killed |
| `u271-measured.B5_collection_errors_unlisted` | `scripts/cloud_battery.py` | maintainer | 2 file(s) | 244 | 1 | killed |
| `u271-measured.B6_count_unread_under_workers` | `scripts/cloud_battery.py` | maintainer | 2 file(s) | 244 | 2 | killed |
| `u271-measured.B7_boot_unrecorded` | `scripts/cloud_battery.py` | maintainer | 2 file(s) | 244 | 15 | killed |
| `u271-measured.B8_ran_uncounted` | `scripts/cloud_battery.py` | maintainer | 2 file(s) | 244 | 12 | killed |
| `u273.P10_placeless_baseline_read` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 3 | killed |
| `u273.P11_other_place_compared` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 2 | killed |
| `u273.P13_rerun_disk_unchecked_upfront` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 1 | killed |
| `u273.P1_memory_any_filesystem` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 1 | killed |
| `u273.P2_no_floor` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 3 | killed |
| `u273.P3_disk_on_memory_accepted` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 2 | killed |
| `u273.P4_mount_first_match` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 1 | killed |
| `u273.P5_tmpdir_not_set` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 9 | killed |
| `u273.P6_no_rerun_on_disk` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 6 | killed |
| `u273.P8_disk_run_unchecked` | `scripts/cloud_battery.py` | maintainer | 1 file(s) | 72 | 1 | killed |
| `u276.K9_agreement_script_default_whole` | `scripts/head_agreement.py` | maintainer | 2 file(s) | 89 | 1 | killed |
| `u297.K1_a_zero_row_counted_as_a_kill` | `scripts/killset.py` | maintainer | 1 file(s) | 77 | 6 | killed |
| `u297.K2_a_lost_kill_passes_check` | `scripts/killset.py` | user | 1 file(s) | 77 | 6 | killed |
| `u297.K3_mapped_to_a_row_that_is_not_killed` | `scripts/killset.py` | user | 1 file(s) | 77 | 2 | killed |
| `u297.K4_a_collection_error_counts_as_a_kill` | `scripts/killset.py` | maintainer | 1 file(s) | 77 | 3 | killed |
| `u297.K5_any_reason_vouches_for_a_move` | `scripts/killset.py` | user | 1 file(s) | 77 | 3 | killed |
| `u297.K6_a_twin_read_as_a_move` | `scripts/killset.py` | user | 1 file(s) | 77 | 3 | killed |
| `u297.K7_a_batch_in_progress_read_as_finished` | `scripts/killset.py` | maintainer | 1 file(s) | 77 | 1 | killed |
| `r343-composites.C2_no_timestamps_no_hash` | `scripts/mutate.py` | user | 1 file(s) | 172 | 1 | killed |
| `r343-composites.C3_path_only` | `scripts/mutate.py` | user | 1 file(s) | 172 | 1 | killed |
| `r343.G10_guard_not_checked_on_timeout` | `scripts/mutate.py` | user | 1 file(s) | 172 | 1 | killed |
| `r343.G1_guard_never_fires` | `scripts/mutate.py` | user | 1 file(s) | 172 | 6 | killed |
| `r343.G4_existence_not_fingerprinted` | `scripts/mutate.py` | user | 1 file(s) | 172 | 1 | killed |
| `r343.G5_row_loop_swallows_the_leak` | `scripts/mutate.py` | user | 1 file(s) | 172 | 1 | killed |
| `r343.G6_run_pytest_skips_the_check` | `scripts/mutate.py` | user | 1 file(s) | 172 | 3 | killed |
| `r343.G7_label_not_carried` | `scripts/mutate.py` | user | 1 file(s) | 172 | 3 | killed |
| `r343.G9_directories_not_fingerprinted` | `scripts/mutate.py` | user | 1 file(s) | 172 | 1 | killed |
| `r343.R1_config_override_ignored` | `scripts/mutate.py` | user | 1 file(s) | 172 | 1 | killed |
| `r343.R2_roots_not_deduplicated` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `r343.S1_no_home_redirect` | `scripts/mutate.py` | user | 1 file(s) | 172 | 3 | killed |
| `r343.S2_no_config_dir_override` | `scripts/mutate.py` | user | 1 file(s) | 172 | 3 | killed |
| `r343.S3_no_state_dir_override` | `scripts/mutate.py` | user | 1 file(s) | 172 | 3 | killed |
| `r343.S4_no_xdg_config_redirect` | `scripts/mutate.py` | user | 1 file(s) | 172 | 2 | killed |
| `u200.M10_driver_unreadable_read_as_complete` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u200.M9_driver_skips_shallow_check` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u251.W3_driver_strips_the_distribution` | `scripts/mutate.py` | maintainer | 2 file(s) | 175 | 1 | killed |
| `u251.W5_count_summed_over_workers` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 4 | killed |
| `u268.W10_driver_reads_cut_baseline` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 41 | killed |
| `u271-measured.D10_empty_count_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u271-measured.D11_verdict_disagreement_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 2 | killed |
| `u271-measured.D12_red_record_read_green` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u271-measured.D13_no_known_file_layer` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u271-measured.D14_read_named_measured` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 3 | killed |
| `u271-measured.D15_early_stop_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 2 | killed |
| `u271-measured.D16_edited_run_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u271-measured.D1_commit_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 2 | killed |
| `u271-measured.D2_run_cleanliness_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u271-measured.D3_tree_now_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 2 | killed |
| `u271-measured.D4_unreadable_status_read_as_clean` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u271-measured.D5_boot_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u271-measured.D6_checkout_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u271-measured.D7_interpreter_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u271-measured.D8_known_file_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u271-measured.D9_interrupted_run_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u273.D1_driver_placeless_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 4 | killed |
| `u273.D2_driver_tmpdir_inherited` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 4 | killed |
| `u273.D3_driver_no_rerun` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 4 | killed |
| `u273.D4_driver_reruns_every_subset` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 4 | killed |
| `u273.D5_driver_place_unchecked_upfront` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 2 | killed |
| `u273.D6_driver_errored_kept` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u273.D7_driver_lost_place_runs_elsewhere` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u273.D8_driver_disk_needed_without_rerun` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u297.D1_replay_row_without_a_source` | `scripts/mutate.py` | user | 1 file(s) | 172 | 1 | killed |
| `u297.D2_cap_lifted_for_every_pass` | `scripts/mutate.py` | user | 1 file(s) | 172 | 3 | killed |
| `u297.D3_mapped_to_no_row` | `scripts/mutate.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u297.D4_a_measured_row_loses_its_source` | `scripts/mutate.py` | maintainer | 2 file(s) | 249 | 2 | killed |
| `u297.D5_a_replay_resumed_from_anywhere` | `scripts/mutate.py` | user | 1 file(s) | 172 | 3 | killed |
| `u297.D6_sources_taken_on_trust` | `scripts/mutate.py` | user | 1 file(s) | 172 | 1 | killed |
| `u296.M10_type_checking_reads_as_running` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 4 | killed |
| `u296.M11_builder_imports_unread` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 2 | killed |
| `u296.M12_followed_through_a_blocked_module` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 1 | killed |
| `u296.M13_own_verbs_dangle` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 5 | killed |
| `u296.M14_core_names_everywhere` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 2 | killed |
| `u296.M15_shadowed_alias_counts` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 1 | killed |
| `u296.M16_prune_adds_lines` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 58 | 5 | killed |
| `u296.M18_vendored_tree_read` | `scripts/refactor_measure.py` | maintainer | 3 file(s) | 103 | 8 | killed |
| `u296.M1_block_size` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 58 | 16 | killed |
| `u296.M22_initializer_relative_import` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 1 | killed |
| `u296.M23_except_branch_names_unread` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 1 | killed |
| `u296.M24_builder_names_a_home_directly` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 1 | killed |
| `u296.M25_dotted_import_alias` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 1 | killed |
| `u296.M26_core_package_name` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 1 | killed |
| `u296.M2_imports_count_as_lines` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 58 | 3 | killed |
| `u296.M3_allowance_forgets_places` | `scripts/refactor_measure.py` | maintainer | 3 file(s) | 103 | 1 | killed |
| `u296.M4_allowance_shared_between_packages` | `scripts/refactor_measure.py` | maintainer | 3 file(s) | 103 | 1 | killed |
| `u296.M5_private_inside_its_package` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 3 | killed |
| `u296.M6_private_through_a_module` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 2 | killed |
| `u296.M7_interface_binds_the_lower_layers` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 2 | killed |
| `u296.M8_interface_list_ignored` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 6 | killed |
| `u296.M9_lazy_reads_as_top_level` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 80 | 4 | killed |
| `u159.M1_off_main_cut` | `scripts/release.py` | maintainer | 1 file(s) | 60 | 1 | killed |
| `u159.M2_dirty_tree_cut` | `scripts/release.py` | maintainer | 1 file(s) | 60 | 1 | killed |
| `u159.M3_behind_origin_cut` | `scripts/release.py` | maintainer | 1 file(s) | 60 | 2 | killed |
| `u159.M4_red_battery_cut` | `scripts/release.py` | maintainer | 1 file(s) | 60 | 2 | killed |
| `u159.M5_other_commit_verdict` | `scripts/release.py` | maintainer | 1 file(s) | 60 | 1 | killed |
| `u159.M7_unit_is_patch` | `scripts/release.py` | maintainer | 1 file(s) | 60 | 6 | killed |
| `u215.M10_main_sync_re_bare` | `scripts/release.py` | user | 1 file(s) | 60 | 1 | killed |
| `u215.M11_version_at_since` | `scripts/release.py` | user | 1 file(s) | 60 | 1 | killed |
| `u215.M12_crossed_tag` | `scripts/release.py` | user | 1 file(s) | 60 | 3 | killed |
| `u215.M13_crossed_tag_tip_excluded` | `scripts/release.py` | user | 1 file(s) | 60 | 2 | killed |
| `u215.M14_tip_needs_since` | `scripts/release.py` | user | 1 file(s) | 60 | 1 | killed |
| `u215.M15_ref_names_a_commit` | `scripts/release.py` | user | 1 file(s) | 60 | 1 | killed |
| `u215.M16_notes_empty_range` | `scripts/release.py` | user | 1 file(s) | 60 | 1 | killed |
| `u215.M18_reversed_range` | `scripts/release.py` | user | 1 file(s) | 60 | 1 | killed |
| `u215.M19_claim_filter_lands` | `scripts/release.py` | user | 1 file(s) | 60 | 1 | killed |
| `u215.M1_whole_range` | `scripts/release.py` | user | 1 file(s) | 60 | 9 | killed |
| `u215.M2_main_sync_never_lands` | `scripts/release.py` | user | 1 file(s) | 60 | 10 | killed |
| `u215.M3_off_line_landing_subject` | `scripts/release.py` | user | 1 file(s) | 60 | 5 | killed |
| `u215.M4_off_line_any_merge` | `scripts/release.py` | user | 1 file(s) | 60 | 2 | killed |
| `u215.M5_head_in_range` | `scripts/release.py` | user | 1 file(s) | 60 | 1 | killed |
| `u215.M6_landing_taker_first` | `scripts/release.py` | user | 1 file(s) | 60 | 1 | killed |
| `u215.M7_claim_every_landing_taker` | `scripts/release.py` | user | 1 file(s) | 60 | 2 | killed |
| `u215.M8_fast_forward_head` | `scripts/release.py` | user | 1 file(s) | 60 | 1 | killed |
| `u215.M9_landing_re_residual` | `scripts/release.py` | user | 1 file(s) | 60 | 1 | killed |
| `u124.S1_head_fixed` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 138 | 2 | killed |
| `u124.S2_sections` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 138 | 1 | killed |
| `u124.S3_record_opener` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 138 | 1 | killed |
| `u124.S4_wired` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 138 | 5 | killed |
| `u124.S5_only_restart` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 138 | 8 | killed |
| `u257.M10_no_value_check` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 116 | 1 | killed |
| `u257.M11_paired_by_label` | `scripts/scan_repo.py` | user | 2 file(s) | 116 | 1 | killed |
| `u257.M1_skip_after_match` | `scripts/scan_repo.py` | user | 2 file(s) | 116 | 2 | killed |
| `u257.M2_gate_never_passes` | `scripts/scan_repo.py` | user | 2 file(s) | 116 | 24 | killed |
| `u257.M3_gate_always_passes` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 116 | 1 | killed |
| `u257.M4_no_quote_landing` | `scripts/scan_repo.py` | user | 2 file(s) | 116 | 21 | killed |
| `u257.M5_no_whitespace_walk` | `scripts/scan_repo.py` | user | 2 file(s) | 116 | 4 | killed |
| `u257.M6_ascii_whitespace_only` | `scripts/scan_repo.py` | user | 2 file(s) | 116 | 1 | killed |
| `u257.M7_window_one_short` | `scripts/scan_repo.py` | user | 2 file(s) | 116 | 2 | killed |
| `u257.M8_no_source_check` | `scripts/scan_repo.py` | user | 2 file(s) | 116 | 1 | killed |
| `u257.M9_lead_ignores_ignorecase` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 116 | 2 | killed |
| `u28-skills-independent.X1_placeholder_exemption` | `scripts/scan_repo.py` | user | 1 file(s) | 98 | 2 | killed |
| `u28-skills-independent.X2_mount_rule_removed` | `scripts/scan_repo.py` | user | 1 file(s) | 98 | 4 | killed |
| `u196.C1_no_run_is_green` | `scripts/wait_ci.py` | maintainer | 1 file(s) | 25 | 4 | killed |
| `u196.C2_unfinished_ignored` | `scripts/wait_ci.py` | maintainer | 1 file(s) | 25 | 2 | killed |
| `u196.C3_neutral_red` | `scripts/wait_ci.py` | maintainer | 1 file(s) | 25 | 1 | killed |
| `u196.C4_deadline_overrun` | `scripts/wait_ci.py` | maintainer | 1 file(s) | 25 | 1 | killed |
| `u196.C5_unread_exits_pending` | `scripts/wait_ci.py` | maintainer | 1 file(s) | 25 | 1 | killed |
| `u196.C6_failures_never_reset` | `scripts/wait_ci.py` | maintainer | 1 file(s) | 25 | 1 | killed |

## Row definitions

### `u276.K10_stage_script_default_whole`

analyze_stages.py stages: default --key to whole, so the stage report times a method the run does not ship

- File: `scripts/analyze_stages.py`
- Source: `u276.json`, row `K10_stage_script_default_whole`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_the_stage_script_times_the_default_method_when_none_is_named`

Old text:

```
    timed.add_argument("--key", default=detect.KEY_DEFAULT, choices=detect.KEY_METHODS)
```

New text:

```
    timed.add_argument("--key", default=detect.KEY_WHOLE, choices=detect.KEY_METHODS)
```

### `u276.K16_json_totals_keep_harmonic`

stage_totals: total every stage whatever the method, so the JSON of a plain run carries a harmonic separation of naught seconds

- File: `scripts/analyze_stages.py`
- Source: `u276.json`, row `K16_json_totals_keep_harmonic`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_the_stage_totals_under_plain_carry_no_separation_in_the_json_either`

Old text:

```
        if key not in detect.STAGES or key in met
    }
```

New text:

```
    }
```

### `u276.K7_stage_table_keeps_every_row`

stage_table: print every stage whatever the method, so a plain run's table shows a harmonic separation row of naught seconds

- File: `scripts/analyze_stages.py`
- Source: `u276.json`, row `K7_stage_table_keeps_every_row`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_the_stage_report_under_plain_counts_no_separation`

Old text:

```
        if key in detect.STAGES and key not in met:
            continue
```

New text:

```
        if False:
            continue
```

### `u276.K8_stage_table_drops_too_much`

stage_table: leave out every detector stage the method meets instead of the ones it does not, so a whole run's table loses its separation row

- File: `scripts/analyze_stages.py`
- Source: `u276.json`, row `K8_stage_table_drops_too_much`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_the_stage_report_under_a_separating_method_keeps_the_separation[whole]`
  - `tests/test_analysis_key_default.py::test_the_stage_report_under_a_separating_method_keeps_the_separation[windows]`
  - `tests/test_analysis_key_default.py::test_the_stage_report_under_plain_counts_no_separation`

Old text:

```
        if key in detect.STAGES and key not in met:
```

New text:

```
        if key in detect.STAGES and key in met and key == "harmonic":
```

### `u297.B10_a_changed_mode_unseen`

compare_files: stop comparing permission bits, so a private file written world readable compares clean

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B10_a_changed_mode_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_private_file_written_world_readable_is_reported`

Old text:

```
        if one.get("mode") != other.get("mode"):
```

New text:

```
        if False:
```

### `u297.B11_a_changed_schema_unseen`

compare_databases: compare no declarations, so a table that lost its key, a constraint or an index compares clean

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B11_a_changed_schema_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 5 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base0-changed0-said0]`
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base1-changed1-said1]`
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base2-changed2-said2]`
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base3-changed3-said3]`
  - `tests/test_behaviour_compare.py::test_a_table_in_one_dump_only_is_reported`

Old text:

```
            one.get("schema", []), other.get("schema", []), words, limit,
```

New text:

```
            [], [], words, limit,
```

### `u297.B1_a_root_outside_the_temporary_directory`

refuse_outside_temporary: accept any root, so a capture can be pointed at a directory somebody keeps

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B1_a_root_outside_the_temporary_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 3 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_link_inside_the_temporary_directory_that_leads_out_of_it_is_refused`
  - `tests/test_behaviour_compare.py::test_a_root_outside_the_temporary_directory_is_refused_before_anything_runs`
  - `tests/test_behaviour_compare.py::test_the_temporary_directory_itself_is_no_root`

Old text:

```
    if not is_inside(path, temporary_directory()):
```

New text:

```
    if False:
```

### `u297.B2_the_temporary_directory_itself`

is_inside: read a directory as inside itself, so the whole temporary directory can be a capture's root and be emptied

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B2_the_temporary_directory_itself`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_the_temporary_directory_itself_is_no_root`

Old text:

```
    return relative != Path(".")
```

New text:

```
    return True
```

### `u297.B3_somebodys_directory_emptied`

take_root: take a root, or the source directory beside it, that holds files no capture left

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B3_somebodys_directory_emptied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 3 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_file_that_is_only_named_like_a_holder_vouches_for_nothing`
  - `tests/test_behaviour_compare.py::test_a_root_that_holds_somebodys_files_is_refused_and_left_alone`
  - `tests/test_behaviour_compare.py::test_the_directory_beside_the_root_is_not_emptied_either`

Old text:

```
        if not left_by_a_capture(folder, holder):
```

New text:

```
        if False:
```

### `u297.B4_a_failed_run_closed_as_a_capture`

run_capture: write the manifest though the scenario run failed, so a capture missing scenarios reads as finished

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B4_a_failed_run_closed_as_a_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_run_that_failed_with_every_record_written_is_not_a_capture`

Old text:

```
    if done.returncode != 0 or not recorded or missing:
```

New text:

```
    if not recorded or missing:
```

### `u297.B5_a_scenario_with_no_record_closed_over`

run_capture: close the capture though a scenario the run collected, or a whole scenario file, left no record

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B5_a_scenario_with_no_record_closed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 4 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_run_that_did_not_list_what_it_collected_is_not_a_capture[None]`
  - `tests/test_behaviour_compare.py::test_a_run_that_did_not_list_what_it_collected_is_not_a_capture[expected1]`
  - `tests/test_behaviour_compare.py::test_a_scenario_file_that_collected_nothing_keeps_the_capture_open`
  - `tests/test_behaviour_compare.py::test_a_scenario_that_ran_and_left_no_record_keeps_the_capture_open`

Old text:

```
    if done.returncode != 0 or not recorded or missing:
```

New text:

```
    if done.returncode != 0 or not recorded:
```

### `u297.B6_any_two_texts_the_same`

same_but_for: read any two texts as the same once a capture has a word of its own, so no difference in output, a file or a row is seen

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B6_any_two_texts_the_same`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 21 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_changed_cell_is_a_row_gone_and_a_row_come`
  - `tests/test_behaviour_compare.py::test_a_changed_line_of_standard_error_is_reported`
  - `tests/test_behaviour_compare.py::test_a_changed_text_file_shows_the_line_that_changed`
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base0-changed0-said0]`
  - `tests/test_behaviour_compare.py::test_a_file_that_only_ends_like_a_sidecar_is_compared_as_a_file`
  - `tests/test_behaviour_compare.py::test_a_long_difference_is_cut_unless_asked_for_whole`
  - `tests/test_behaviour_compare.py::test_a_missing_final_newline_is_a_difference_and_says_how_the_texts_end`
  - `tests/test_behaviour_compare.py::test_a_word_that_stands_for_two_things_keeps_both_counterparts`
  - `tests/test_behaviour_compare.py::test_another_files_inode_in_that_row_is_a_difference`
  - `tests/test_behaviour_compare.py::test_one_changed_character_of_help_is_reported`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[8430 bytes, pid 3409-8431 bytes, pid 3467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[lock_3409-lock_3467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid 13409-pid 13467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid 34091-pid 34671-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid 3409\n-pid 3467-False]`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return re.fullmatch("".join(pattern), second, flags=re.DOTALL) is not None
```

New text:

```
    return True
```

### `u297.B7_a_word_read_inside_a_longer_one`

same_but_for: drop the leading end of the whole word rule, so a process id is read inside a longer number

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B7_a_word_read_inside_a_longer_one`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 3 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[lock_3409-lock_3467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid 13409-pid 13467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid x3409-pid x3467-False]`

Old text:

```
        r"(?<![0-9A-Za-z_])(?:" + "|".join(re.escape(one) for one in longest_first) + r")(?![0-9A-Za-z_])"
```

New text:

```
        r"(?:" + "|".join(re.escape(one) for one in longest_first) + r")(?![0-9A-Za-z_])"
```

### `u297.B8_a_changed_exit_code_unseen`

compare_commands: stop comparing exit codes

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B8_a_changed_exit_code_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_one_changed_exit_code_is_reported`
  - `tests/test_behaviour_compare.py::test_one_command_more_is_reported_once_and_the_rest_are_still_compared`

Old text:

```
            if one["exit"] != other["exit"]:
```

New text:

```
            if False:
```

### `u297.B9_a_file_in_one_capture_only_unseen`

compare_files: walk only the paths both captures hold, so an extra file and a missing one are never reported

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B9_a_file_in_one_capture_only_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_an_empty_directory_a_verb_made_is_an_entry_of_its_own`
  - `tests/test_behaviour_compare.py::test_one_extra_file_is_reported_and_so_is_one_that_is_gone`

Old text:

```
    for relative in sorted(set(before) | set(after)):
```

New text:

```
    for relative in sorted(set(before) & set(after)):
```

### `u122.H1_no_hold`

Remove the hold: derive_status ignores a held status and derives from the graph

- File: `scripts/board.py`
- Source: `u122.json`, row `H1_no_hold`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 8 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_attended_card_somebody_holds_keeps_the_hold[In Progress]`
  - `tests/test_board_status.py::test_an_attended_card_somebody_holds_keeps_the_hold[In review]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[4-In Progress]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[4-In review]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[5-In Progress]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[5-In review]`
  - `tests/test_board_status.py::test_an_open_unit_somebody_holds_keeps_the_status_it_holds[In Progress]`
  - `tests/test_board_status.py::test_an_open_unit_somebody_holds_keeps_the_status_it_holds[In review]`

Old text:

```
    if current in UNDERWAY:
```

New text:

```
    if False:
```

### `u122.H2_review_not_held`

UNDERWAY loses In review, the runner's status, so it reads as drift again

- File: `scripts/board.py`
- Source: `u122.json`, row `H2_review_not_held`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 5 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_attended_card_somebody_holds_keeps_the_hold[In review]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[4-In review]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[5-In review]`
  - `tests/test_board_status.py::test_an_open_unit_somebody_holds_keeps_the_status_it_holds[In review]`
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In review]`

Old text:

```
UNDERWAY = ("In Progress", "In review")
```

New text:

```
UNDERWAY = ("In Progress",)
```

### `u122.H3_progress_not_held`

UNDERWAY loses In Progress, a session's and a lane's status

- File: `scripts/board.py`
- Source: `u122.json`, row `H3_progress_not_held`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 5 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_attended_card_somebody_holds_keeps_the_hold[In Progress]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[4-In Progress]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[5-In Progress]`
  - `tests/test_board_status.py::test_an_open_unit_somebody_holds_keeps_the_status_it_holds[In Progress]`
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In Progress]`

Old text:

```
UNDERWAY = ("In Progress", "In review")
```

New text:

```
UNDERWAY = ("In review",)
```

### `u122.H4_hold_flattened`

A held card derives In Progress whatever it held, so In review becomes drift

- File: `scripts/board.py`
- Source: `u122.json`, row `H4_hold_flattened`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_attended_card_somebody_holds_keeps_the_hold[In review]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[4-In review]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[5-In review]`
  - `tests/test_board_status.py::test_an_open_unit_somebody_holds_keeps_the_status_it_holds[In review]`

Old text:

```
        return current

```

New text:

```
        return "In Progress"

```

### `u122.H5_units_only`

The hold applies to units only, the behaviour before the 2026-10-09 amendment

- File: `scripts/board.py`
- Source: `u122.json`, row `H5_units_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[4-In Progress]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[4-In review]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[5-In Progress]`
  - `tests/test_board_status.py::test_an_open_residual_somebody_holds_keeps_the_status_it_holds[5-In review]`

Old text:

```
    if current in UNDERWAY:
```

New text:

```
    if current in UNDERWAY and node["unit"]:
```

### `u122.H6_hold_beats_closure`

The hold is checked before closure, so a closed held card is not Done

- File: `scripts/board.py`
- Source: `u122.json`, row `H6_hold_beats_closure`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_status.py::test_a_closed_card_is_done_whatever_it_held[3-In Progress]`
  - `tests/test_board_status.py::test_a_closed_card_is_done_whatever_it_held[3-In review]`
  - `tests/test_board_status.py::test_a_closed_card_is_done_whatever_it_held[6-In Progress]`
  - `tests/test_board_status.py::test_a_closed_card_is_done_whatever_it_held[6-In review]`

Old text:

```
    if node["closed"]:
        return "Done"
    if current in UNDERWAY:
```

New text:

```
    if current in UNDERWAY:
        return current
    if node["closed"]:
        return "Done"
    if False:
```

### `u122.H7_attended_beats_hold`

Attended is checked before the hold, the order the review moved

- File: `scripts/board.py`
- Source: `u122.json`, row `H7_attended_beats_hold`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_attended_card_somebody_holds_keeps_the_hold[In Progress]`
  - `tests/test_board_status.py::test_an_attended_card_somebody_holds_keeps_the_hold[In review]`

Old text:

```
    if current in UNDERWAY:
```

New text:

```
    if node["attended"]:
        return "Attended"
    if current in UNDERWAY:
```

### `u122.N1_next_busy_progress_only`

next counts only In Progress as busy, so an In review card is offered again

- File: `scripts/board.py`
- Source: `u122.json`, row `N1_next_busy_progress_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In review]`

Old text:

```
.get("status") in UNDERWAY
```

New text:

```
.get("status") == "In Progress"
```

### `u122.N2_next_offers_busy`

next lists a busy card under underway but leaves it in the ready list

- File: `scripts/board.py`
- Source: `u122.json`, row `N2_next_offers_busy`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In Progress]`
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In review]`

Old text:

```
    ready = [n for n in ready if n["number"] not in busy]
```

New text:

```
    ready = list(ready)
```

### `u122.N3_next_no_status`

next drops the status column, so a reader cannot tell the runner's hold from a session's

- File: `scripts/board.py`
- Source: `u122.json`, row `N3_next_no_status`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In Progress]`
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In review]`

Old text:

```
            print(f"  #{node['number']:<3} {status:<11} {node['title']}")
```

New text:

```
            print(f"  #{node['number']:<3} {node['title']}")
```

### `u124-b19.B19_audit_reads_folder`

audit stops counting a malformed residual file as a contradiction, rerun after the audit test landed

- File: `scripts/board.py`
- Source: `u124-b19.json`, row `B19_audit_reads_folder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_pending_units.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_audit_counts_a_residual_file_that_cannot_land_as_a_contradiction`

Old text:

```
        clashes = clashes + malformed
```

New text:

```
        clashes = clashes
```

### `u124.B10_validate_first`

a malformed file is skipped instead of stopping the landing, so the good ones land

- File: `scripts/board.py`
- Source: `u124.json`, row `B10_validate_first`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_malformed_file_lands_nothing`

Old text:

```
    if problems:
        raise ValueError("; ".join(problems))
    if not parsed:
```

New text:

```
    if not parsed:
```

### `u124.B11_relanded_title`

a title the ledger already holds is numbered again

- File: `scripts/board.py`
- Source: `u124.json`, row `B11_relanded_title`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_file_that_landed_once_is_not_numbered_again`

Old text:

```
    if again:
        raise ValueError("; ".join(again))
```

New text:

```
(empty)
```

### `u124.B12_highest_not_count`

the next number is the ledger's count plus one rather than its highest plus one

- File: `scripts/board.py`
- Source: `u124.json`, row `B12_highest_not_count`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 5 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_an_untracked_draft_is_neither_judged_nor_landed`
  - `tests/test_restart_and_residual_files.py::test_the_landing_refuses_off_main`
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order0]`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order1]`

Old text:

```
    number = max(titles, default=0)
```

New text:

```
    number = len(titles)
```

### `u124.B13_separator`

landed entries lose the separator line

- File: `scripts/board.py`
- Source: `u124.json`, row `B13_separator`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`

Old text:

```
        text = text.rstrip("\n") + "\n\n---\n\n"
```

New text:

```
        text = text.rstrip("\n") + "\n\n"
```

### `u124.B14_files_deleted`

a landed file is left in the folder

- File: `scripts/board.py`
- Source: `u124.json`, row `B14_files_deleted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order0]`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order1]`

Old text:

```
    for path, _, _ in parsed:
        path.unlink()
```

New text:

```
    for path, _, _ in parsed:
        pass
```

### `u124.B15_closing_reads_folder`

closing stops reading the residual folder

- File: `scripts/board.py`
- Source: `u124.json`, row `B15_closing_reads_folder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_pending_units.py`
- Collected: 141 against a baseline of 141
- Kills: 3 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_an_unreadable_range_still_refuses_a_malformed_residual_file`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[hook]`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[range]`

Old text:

```
    malformed = residual_file_problems()
    if not problems and not malformed:
```

New text:

```
    malformed = []
    if not problems and not malformed:
```

### `u124.B17_land_on_main_only`

residuals --land runs on any branch

- File: `scripts/board.py`
- Source: `u124.json`, row `B17_land_on_main_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_landing_refuses_off_main`

Old text:

```
    if branch != "main":
        print(
            f"board: residuals are numbered on main
```

New text:

```
    if branch == "never":
        print(
            f"board: residuals are numbered on main
```

### `u124.B18_behind_origin`

residuals --land numbers on a main behind origin/main

- File: `scripts/board.py`
- Source: `u124.json`, row `B18_behind_origin`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_landing_refuses_off_main`

Old text:

```
    if behind.returncode == 0 and behind.stdout.strip() not in ("", "0"):
```

New text:

```
    if behind.returncode == 0 and behind.stdout.strip() not in ("", "0") and False:
```

### `u124.B1_untracked_filter`

residual_files returns every file, git's index ignored, so an untracked draft is judged and landed

- File: `scripts/board.py`
- Source: `u124.json`, row `B1_untracked_filter`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_an_untracked_draft_is_neither_judged_nor_landed`

Old text:

```
    if listed.returncode != 0:
        return paths

```

New text:

```
    if listed.returncode == 0 or listed.returncode != 0:
        return paths

```

### `u124.B2_readme_excluded`

the README is read as a residual file

- File: `scripts/board.py`
- Source: `u124.json`, row `B2_readme_excluded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`
  - `tests/test_restart_and_residual_files.py::test_the_shipped_residual_folder_holds_only_files_that_can_land`

Old text:

```
    paths = sorted(p for p in folder.glob("*.md") if p.name != "README.md")
```

New text:

```
    paths = sorted(p for p in folder.glob("*.md"))
```

### `u124.B3_name_order`

files land in folder listing order rather than name order

- File: `scripts/board.py`
- Source: `u124.json`, row `B3_name_order`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order0]`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order1]`

Old text:

```
    paths = sorted(p for p in folder.glob("*.md") if p.name != "README.md")
```

New text:

```
    paths = sorted((p for p in folder.glob("*.md") if p.name != "README.md"), reverse=True)
```

### `u124.B4_fence_open`

a file with no opening fence is not refused

- File: `scripts/board.py`
- Source: `u124.json`, row `B4_fence_open`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[**The mechanism.** No frontmatter at all.\n-does not open]`
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[title: T\nfound: today.\n---\n\nBody.\n-does not open]`

Old text:

```
    if not lines or lines[0] != "---":
        raise ValueError("does not open with a frontmatter fence")
```

New text:

```
    if not lines:
        raise ValueError("does not open with a frontmatter fence")
```

### `u124.B5_unknown_key`

an unknown frontmatter key is accepted

- File: `scripts/board.py`
- Source: `u124.json`, row `B5_unknown_key`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\ntitle: T\nfound: today.\nfond: typo\n---\n\nBody.\n-fond]`

Old text:

```
        if key not in RESIDUAL_REQUIRED and key not in RESIDUAL_OPTIONAL:
```

New text:

```
        if key not in RESIDUAL_REQUIRED and key not in RESIDUAL_OPTIONAL and False:
```

### `u124.B6_required_keys`

a missing title or found line is accepted

- File: `scripts/board.py`
- Source: `u124.json`, row `B6_required_keys`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 5 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\nfound: today.\n---\n\nBody.\n-no title]`
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\ntitle: No found line\n---\n\nBody.\n-no found]`
  - `tests/test_restart_and_residual_files.py::test_audit_counts_a_residual_file_that_cannot_land_as_a_contradiction`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[hook]`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[range]`

Old text:

```
        if not meta.get(key):
            raise ValueError(f"frontmatter has no {key}")
```

New text:

```
        if key not in meta and False:
            raise ValueError(f"frontmatter has no {key}")
```

### `u124.B7_issue_values`

issue takes any value

- File: `scripts/board.py`
- Source: `u124.json`, row `B7_issue_values`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\ntitle: T\nfound: today.\nissue: maybe\n---\n\nBody.\n-issue]`

Old text:

```
        if key in meta and meta[key] not in allowed:
```

New text:

```
        if key in meta and meta[key] not in allowed and False:
```

### `u124.B8_numbered_title`

the number shape widened back to any leading R number

- File: `scripts/board.py`
- Source: `u124.json`, row `B8_numbered_title`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_title_citing_another_residual_is_not_a_number`

Old text:

```
    if re.match(r"R-\d+\.", meta["title"]):
```

New text:

```
    if re.match(r"R-\d+", meta["title"]):
```

### `u124.B9_empty_body`

a file with frontmatter and no body is accepted

- File: `scripts/board.py`
- Source: `u124.json`, row `B9_empty_body`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\ntitle: T\nfound: today.\n---\n\n\n-no body]`

Old text:

```
    if not body.strip():
        raise ValueError("has frontmatter and no body")
```

New text:

```
    if body is None:
        raise ValueError("has frontmatter and no body")
```

### `u148.C1_one_short_allowed`

short_of_count lets a read one row short of the count through

- File: `scripts/board.py`
- Source: `u148.json`, row `C1_one_short_allowed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_issues_short_of_the_repositorys_own_count_are_refused`
  - `tests/test_board_reads.py::test_items_short_of_the_repositorys_own_count_are_refused`

Old text:

```
    if len(rows) < total:
```

New text:

```
    if len(rows) < total - 1:
```

### `u148.C2_count_off`

short_of_count never compares rows to the count

- File: `scripts/board.py`
- Source: `u148.json`, row `C2_count_off`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_issues_short_of_the_repositorys_own_count_are_refused`
  - `tests/test_board_reads.py::test_items_short_of_the_repositorys_own_count_are_refused`

Old text:

```
    if len(rows) < total:
```

New text:

```
    if False:
```

### `u148.C3_no_count_skips`

a read with no count skips the check, the shape before the review

- File: `scripts/board.py`
- Source: `u148.json`, row `C3_no_count_skips`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_an_issue_count_that_is_not_a_number_is_refused`
  - `tests/test_board_reads.py::test_an_item_read_with_no_count_is_refused`

Old text:

```
    if not isinstance(total, int):
        # No count means no check, and a read nobody could check is not whole.
        raise Truncated(
```

New text:

```
    if not isinstance(total, int):
        return
        raise Truncated(
```

### `u148.C4_only_none_refused`

only a missing count is refused, a count that is not a number falls through

- File: `scripts/board.py`
- Source: `u148.json`, row `C4_only_none_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_an_issue_count_that_is_not_a_number_is_refused`

Old text:

```
    if not isinstance(total, int):
```

New text:

```
    if total is None:
```

### `u148.C5_issue_count_dropped`

load_issues never checks its read against the repository's count

- File: `scripts/board.py`
- Source: `u148.json`, row `C5_issue_count_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_an_issue_count_that_is_not_a_number_is_refused`
  - `tests/test_board_reads.py::test_issues_short_of_the_repositorys_own_count_are_refused`

Old text:

```
    short_of_count(issues, int(total) if total.isdigit() else total, "issue")
```

New text:

```
    pass
```

### `u148.L1_old_limit`

READ_LIMIT back to 300, the ceiling the board passed

- File: `scripts/board.py`
- Source: `u148.json`, row `L1_old_limit`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_reads.py::test_every_issue_and_project_item_is_read_past_three_hundred`
  - `tests/test_board_reads.py::test_issues_filed_after_the_count_are_read_and_not_refused`
  - `tests/test_board_reads.py::test_issues_short_of_the_repositorys_own_count_are_refused`
  - `tests/test_board_reads.py::test_the_audit_reads_an_item_past_three_hundred_as_on_the_board`

Old text:

```
READ_LIMIT = 5000
```

New text:

```
READ_LIMIT = 300
```

### `u148.L2_issue_literal`

load_issues asks gh for a literal 300 instead of READ_LIMIT

- File: `scripts/board.py`
- Source: `u148.json`, row `L2_issue_literal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 8 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[315]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[316]`
  - `tests/test_board_reads.py::test_every_issue_and_project_item_is_read_past_three_hundred`
  - `tests/test_board_reads.py::test_issues_filed_after_the_count_are_read_and_not_refused`
  - `tests/test_board_reads.py::test_issues_short_of_the_repositorys_own_count_are_refused`
  - `tests/test_board_reads.py::test_one_row_under_the_limit_is_taken_as_whole`
  - `tests/test_board_reads.py::test_the_audit_reads_an_item_past_three_hundred_as_on_the_board`
  - `tests/test_board_reads.py::test_the_issue_read_asks_gh_for_the_limit_and_the_card_read_pages`

Old text:

```
        "all",
        "--limit",
        str(READ_LIMIT),
```

New text:

```
        "all",
        "--limit",
        "300",
```

### `u148.N1_truncation_blamed_on_token`

next catches a truncation as a token that cannot read the board

- File: `scripts/board.py`
- Source: `u148.json`, row `N1_truncation_blamed_on_token`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_next_refuses_a_truncated_item_read_rather_than_blame_the_token`

Old text:

```
    except Truncated:
        # A cut short read is not a token that cannot see the board, and the
        # queue below would offer a held card the read missed.
        raise

```

New text:

```
(empty)
```

### `u148.S1_branch_before_read`

start creates the branch before it reads the board, the shape before the review

- File: `scripts/board.py`
- Source: `u148.json`, row `S1_branch_before_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_start_reads_the_board_before_it_branches`

Old text:

```
    ctx = project_context(owner)
    items = project_items(owner)
    item = items.get(node["number"])

    subprocess.run(["git", "checkout", "-b", branch], check=True)

```

New text:

```
    subprocess.run(["git", "checkout", "-b", branch], check=True)
    ctx = project_context(owner)
    items = project_items(owner)
    item = items.get(node["number"])

```

### `u148.S2_claims_in_progress`

start says a card not on the board is In Progress

- File: `scripts/board.py`
- Source: `u148.json`, row `S2_claims_in_progress`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_start_says_so_when_the_card_is_not_on_the_board`

Old text:

```
        print(f"Branch {branch} is checked out, but #{node['number']} is NOT on the")
```

New text:

```
        print(f"Branch {branch} is checked out and #{node['number']} is In Progress.")
```

### `u148.W1_full_page_taken`

whole accepts a read of exactly the limit, a full page read as complete

- File: `scripts/board.py`
- Source: `u148.json`, row `W1_full_page_taken`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[315]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[316]`
  - `tests/test_board_reads.py::test_the_old_three_hundred_limit_is_what_lost_them`

Old text:

```
    if len(rows) >= READ_LIMIT:
```

New text:

```
    if len(rows) > READ_LIMIT:
```

### `u148.W2_whole_off`

whole checks nothing

- File: `scripts/board.py`
- Source: `u148.json`, row `W2_whole_off`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[315]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[316]`
  - `tests/test_board_reads.py::test_the_old_three_hundred_limit_is_what_lost_them`

Old text:

```
    if len(rows) >= READ_LIMIT:
```

New text:

```
    if False:
```

### `u148.W3_issue_whole_dropped`

load_issues no longer passes its read through whole

- File: `scripts/board.py`
- Source: `u148.json`, row `W3_issue_whole_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 182 against a baseline of 182
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[315]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[316]`
  - `tests/test_board_reads.py::test_the_old_three_hundred_limit_is_what_lost_them`

Old text:

```
    whole(issues, "issue")

```

New text:

```
    pass

```

### `u151.A1_archived_read`

archived cards are read as on the board

- File: `scripts/board.py`
- Source: `u151.json`, row `A1_archived_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_the_card_read_leaves_archived_cards_out_as_the_listing_did`

Old text:

```
includeArchived: false
```

New text:

```
includeArchived: true
```

### `u151.C1_no_cursor_trusted`

a page that says more and gives no cursor is followed from the start again

- File: `scripts/board.py`
- Source: `u151.json`, row `C1_no_cursor_trusted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_page_that_says_more_and_gives_no_cursor_is_refused`

Old text:

```
        if not after:
            raise Truncated("the project membership read said there was more and gave no cursor")

```

New text:

```
(empty)
```

### `u151.C2_page_bound_short`

the page bound drops its last page, a read of 317 issues refused

- File: `scripts/board.py`
- Source: `u151.json`, row `C2_page_bound_short`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_one_row_under_the_limit_is_taken_as_whole`

Old text:

```
    for _ in range(READ_LIMIT // 100 + 1):
```

New text:

```
    for _ in range(READ_LIMIT // 100):
```

### `u151.F1_cursor_typed`

the cursor goes as -F, which gh would type

- File: `scripts/board.py`
- Source: `u151.json`, row `F1_cursor_typed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_the_card_read_is_a_page_per_hundred_issues_not_a_call_per_card`

Old text:

```
            args += ["-f", f"after={after}"]
```

New text:

```
            args += ["-F", f"after={after}"]
```

### `u151.M1_membership_count_dropped`

an issue whose memberships come back short is trusted

- File: `scripts/board.py`
- Source: `u151.json`, row `M1_membership_count_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_an_issue_whose_memberships_come_back_short_is_refused`

Old text:

```
            short_of_count(
                memberships["nodes"], memberships.get("totalCount"),
                f"#{issue['number']} project membership",
            )

```

New text:

```
(empty)
```

### `u151.M2_issue_count_dropped`

an issue read shorter than the repository count is trusted

- File: `scripts/board.py`
- Source: `u151.json`, row `M2_issue_count_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_an_item_read_with_no_count_is_refused`
  - `tests/test_board_reads.py::test_items_short_of_the_repositorys_own_count_are_refused`

Old text:

```
    short_of_count(seen, total, "project membership")

```

New text:

```
(empty)
```

### `u151.N1_number_filter_dropped`

a card on another project of the same owner counts as this board's

- File: `scripts/board.py`
- Source: `u151.json`, row `N1_number_filter_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_card_on_another_project_or_owner_is_not_this_boards`

Old text:

```
                if str(project.get("number")) != PROJECT_NUMBER:
                    continue

```

New text:

```
                pass

```

### `u151.O1_owner_filter_dropped`

a card on this project number under another owner counts as this board's

- File: `scripts/board.py`
- Source: `u151.json`, row `O1_owner_filter_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_card_on_another_project_or_owner_is_not_this_boards`

Old text:

```
                if login.lower() != owner.lower():
                    continue

```

New text:

```
                pass

```

### `u151.O2_owner_case_sensitive`

the owner match becomes case sensitive

- File: `scripts/board.py`
- Source: `u151.json`, row `O2_owner_case_sensitive`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_the_owner_is_matched_whatever_its_case`

Old text:

```
                if login.lower() != owner.lower():
```

New text:

```
                if login != owner:
```

### `u151.U1_unblocks_always_written`

Unblocks is rewritten on every card again, the U151 cost

- File: `scripts/board.py`
- Source: `u151.json`, row `U1_unblocks_always_written`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 5 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_card_with_no_unblocks_number_gets_one`
  - `tests/test_board_cost.py::test_a_changed_unblocks_number_is_written_once_with_the_derived_count`
  - `tests/test_board_cost.py::test_a_sync_with_no_drift_lists_nothing_and_writes_nothing`
  - `tests/test_board_cost.py::test_an_issue_off_the_board_is_added_then_given_its_status_and_number`
  - `tests/test_board_cost.py::test_an_unchanged_unblocks_number_is_not_written`

Old text:

```
 and apply and item.get("unblocks") != unblocks:
```

New text:

```
 and apply:
```

### `u151.U2_added_card_zero`

a card sync just added reads as holding 0, so a derived 0 is never written

- File: `scripts/board.py`
- Source: `u151.json`, row `U2_added_card_zero`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_an_issue_off_the_board_is_added_then_given_its_status_and_number`

Old text:

```
"status": None, "unblocks": None}
```

New text:

```
"status": None, "unblocks": 0}
```

### `u151.X1_next_skips_context`

next trusts the card read without asking for the project first

- File: `scripts/board.py`
- Source: `u151.json`, row `X1_next_skips_context`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_next_asks_for_the_project_before_trusting_an_empty_card_read`

Old text:

```
        project_context(owner)
        items = project_items(owner)
```

New text:

```
        items = project_items(owner)
```

### `u151.X2_no_org_fallback`

the context never asks for an organization project

- File: `scripts/board.py`
- Source: `u151.json`, row `X2_no_org_fallback`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_the_context_asks_the_organization_when_the_owner_is_not_a_user`

Old text:

```
    for kind in ("user", "organization"):
```

New text:

```
    for kind in ("user",):
```

### `u151.X3_status_refusal_dropped`

a project with no Status field is not refused

- File: `scripts/board.py`
- Source: `u151.json`, row `X3_status_refusal_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_project_with_no_status_field_is_refused_by_name`

Old text:

```
    if not status or "options" not in status:
        raise Fail(
```

New text:

```
    if False:
        raise Fail(
```

### `u151.X4_unseen_project_trusted`

a project the token cannot see is not refused

- File: `scripts/board.py`
- Source: `u151.json`, row `X4_unseen_project_trusted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_project_the_token_cannot_see_is_refused_and_says_why`
  - `tests/test_board_cost.py::test_next_asks_for_the_project_before_trusting_an_empty_card_read`

Old text:

```
    if not project:
        raise Fail(
```

New text:

```
    if False:
        raise Fail(
```

### `u151.X5_field_count_dropped`

a project whose fields come back short is trusted

- File: `scripts/board.py`
- Source: `u151.json`, row `X5_field_count_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_project_whose_fields_come_back_short_is_refused`

Old text:

```
    short_of_count(fields["nodes"], fields.get("totalCount"), "project field")

```

New text:

```
(empty)
```

### `u158.M1_card_not_judged`

cmd_closing: never judge the card a pull request's head names, so an owed unit merges

- File: `scripts/board.py`
- Source: `u158.json`, row `M1_card_not_judged`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_pull_request_range_closing_a_unit_still_owed_is_refused`
  - `tests/test_pending_units.py::test_the_card_a_head_names_is_judged_even_when_the_range_is_unreadable`

Old text:

```
        if card is not None:
```

New text:

```
        if False:
```

### `u158.M2_any_branch_names_a_card`

pull_request_card: read a card off any owner/N-slug branch, not only a cloud one

- File: `scripts/board.py`
- Source: `u158.json`, row `M2_any_branch_names_a_card`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_only_a_cloud_branch_names_the_card_its_merge_closes[feature/36-x-None]`

Old text:

```
CLOUD_BRANCH_RE = re.compile(r"^cloud/(\d+)-")
```

New text:

```
CLOUD_BRANCH_RE = re.compile(r"^\w+/(\d+)-")
```

### `u158.M3_implied_close_not_a_reference`

cmd_closing: write the implied trailer without its hash, so it closes nothing

- File: `scripts/board.py`
- Source: `u158.json`, row `M3_implied_close_not_a_reference`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_pull_request_range_closing_a_unit_still_owed_is_refused`
  - `tests/test_pending_units.py::test_the_card_a_head_names_is_judged_even_when_the_range_is_unreadable`

Old text:

```
            problems += unresolved_closes(f"Closes #{card}", raw=False)
```

New text:

```
            problems += unresolved_closes(f"Closes {card}", raw=False)
```

### `u187.A1_relayed_answer_never_matches`

_relayed_answer: never match, so the relay thread's Answer from Phillip is read as a session hold and never as his reply

- File: `scripts/board.py`
- Source: `u187.json`, row `A1_relayed_answer_never_matches`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_punctuated_relayed_answer_is_phillips_reply_not_a_hold`
  - `tests/test_board_cloud.py::test_a_relayed_answer_alone_is_not_a_hold`
  - `tests/test_board_cloud.py::test_an_answer_relayed_from_the_decisions_page_releases_the_card`

Old text:

```
    return comment_heading(comment.get("body") or "") == HEAD_ANSWER
```

New text:

```
    return False
```

### `u187.A2_answer_counted_as_a_hold`

cloud_state: count a relayed answer among the session's own comments, so an answer alone holds the card

- File: `scripts/board.py`
- Source: `u187.json`, row `A2_answer_counted_as_a_hold`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_punctuated_relayed_answer_is_phillips_reply_not_a_hold`
  - `tests/test_board_cloud.py::test_a_relayed_answer_alone_is_not_a_hold`
  - `tests/test_board_cloud.py::test_an_answer_relayed_from_the_decisions_page_releases_the_card`

Old text:

```
    mine = [c for c in ordered if SESSION_MARK in (c.get("body") or "") and not _relayed_answer(c)]
```

New text:

```
    mine = [c for c in ordered if SESSION_MARK in (c.get("body") or "")]
```

### `u187.A3_answer_not_read_as_reply`

cloud_state: drop the relayed answer from the replies after a question, so the card is never offered as answered

- File: `scripts/board.py`
- Source: `u187.json`, row `A3_answer_not_read_as_reply`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_punctuated_relayed_answer_is_phillips_reply_not_a_hold`
  - `tests/test_board_cloud.py::test_an_answer_relayed_from_the_decisions_page_releases_the_card`

Old text:

```
        if _when(c) > since and (SESSION_MARK not in (c.get("body") or "") or _relayed_answer(c))
```

New text:

```
        if _when(c) > since and (SESSION_MARK not in (c.get("body") or ""))
```

### `u187.A4_heading_drifts`

HEAD_ANSWER: a nearby heading, answer from phil, so the documented heading no longer matches

- File: `scripts/board.py`
- Source: `u187.json`, row `A4_heading_drifts`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_punctuated_relayed_answer_is_phillips_reply_not_a_hold`
  - `tests/test_board_cloud.py::test_a_relayed_answer_alone_is_not_a_hold`
  - `tests/test_board_cloud.py::test_an_answer_relayed_from_the_decisions_page_releases_the_card`

Old text:

```
HEAD_ANSWER = "answer from phillip"
```

New text:

```
HEAD_ANSWER = "answer from phil"
```

### `u196.S1_any_word`

search_residuals: match a heading carrying any word rather than every word

- File: `scripts/board.py`
- Source: `u196.json`, row `S1_any_word`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_every_word_must_appear_in_any_case`

Old text:

```
        if all(word in title.casefold() for word in wanted)
```

New text:

```
        if any(word in title.casefold() for word in wanted)
```

### `u196.S2_case_sensitive`

search_residuals: compare without folding case, so a heading in capitals is missed

- File: `scripts/board.py`
- Source: `u196.json`, row `S2_case_sensitive`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`
- Collected: 6 against a baseline of 6
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_every_word_must_appear_in_any_case`
  - `tests/test_board_residual_search.py::test_one_word_finds_every_heading_carrying_it_newest_first`

Old text:

```
        if all(word in title.casefold() for word in wanted)
```

New text:

```
        if all(word in title for word in wanted)
```

### `u196.S3_empty_search`

cmd_residuals: drop the refusal of an empty search, which matches every heading

- File: `scripts/board.py`
- Source: `u196.json`, row `S3_empty_search`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_the_command_prints_hits_and_refuses_an_empty_search`

Old text:

```
        if args.land or not words:
```

New text:

```
        if args.land:
```

### `u196.S4_missing_ledger_no_match`

search_residuals: drop the refusal of a missing ledger, so a search over a file never read says no match

- File: `scripts/board.py`
- Source: `u196.json`, row `S4_missing_ledger_no_match`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_a_missing_ledger_is_refused_never_read_as_no_match`

Old text:

```
    if not source.is_file():
        # A missing
```

New text:

```
    if False:
        # A missing
```

### `u203.M1_no_opening_span`

comment_heading: never take an opening emphasised span, so **Brainstorm.** One question waits reads as a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M1_no_opening_span`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_known_heading_reads_through_trailing_punctuation_and_emphasis`
  - `tests/test_board_cloud.py::test_each_cut_and_strip_is_needed_on_its_own`
  - `tests/test_board_cloud.py::test_punctuated_landings_and_set_asides_keep_their_states`
  - `tests/test_board_cloud.py::test_the_489_comment_reads_as_a_brainstorm`

Old text:

```
        span = _OPENING_EMPHASIS.match(text)
```

New text:

```
        span = None
```

### `u203.M2_span_closer_any_follower`

_OPENING_EMPHASIS: accept a closer followed by a letter, so **Brainstorm**s reads as a brainstorm

- File: `scripts/board.py`
- Source: `u203.json`, row `M2_span_closer_any_follower`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_heading_whose_words_differ_is_still_a_hold`

Old text:

```
_OPENING_EMPHASIS = re.compile(r"([*_]+)(.+?)\1(?=$|[\s.,:;?!\u2026])")
```

New text:

```
_OPENING_EMPHASIS = re.compile(r"([*_]+)(.+?)\1")
```

### `u203.M3_no_sentence_cut`

_HEADING_END: cut only at a colon or comma, so Needs the machine. The card needs rekordbox is a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M3_no_sentence_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_known_heading_reads_through_trailing_punctuation_and_emphasis`
  - `tests/test_board_cloud.py::test_a_sentence_after_a_heading_on_its_line_is_cut`

Old text:

```
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026](?=\s)")
```

New text:

```
_HEADING_END = re.compile(r"[:,]")
```

### `u203.M4_sentence_cut_anywhere`

_HEADING_END: cut at any stop, whitespace after it or not, so Landed v0.6.0 today is cut inside the version

- File: `scripts/board.py`
- Source: `u203.json`, row `M4_sentence_cut_anywhere`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_old_readings_stand`

Old text:

```
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026](?=\s)")
```

New text:

```
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026]")
```

### `u203.M5_no_trailing_strip`

comment_heading: strip emphasis but no trailing punctuation, so ## Brainstorm. reads as a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M5_no_trailing_strip`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 7 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_known_heading_reads_through_trailing_punctuation_and_emphasis`
  - `tests/test_board_cloud.py::test_a_punctuated_question_waits_on_phillip_however_old`
  - `tests/test_board_cloud.py::test_a_punctuated_relayed_answer_is_phillips_reply_not_a_hold`
  - `tests/test_board_cloud.py::test_each_cut_and_strip_is_needed_on_its_own`
  - `tests/test_board_cloud.py::test_progress_with_a_full_stop_still_only_refreshes_the_hold`
  - `tests/test_board_cloud.py::test_punctuated_landings_and_set_asides_keep_their_states`
  - `tests/test_board_cloud.py::test_the_489_comment_reads_as_a_brainstorm`

Old text:

```
            text = text.strip().strip("*_").rstrip(_TRAILING)
```

New text:

```
            text = text.strip().strip("*_")
```

### `u203.M6_one_pass`

comment_heading: strip once instead of to a fixed point, so emphasis left behind a full stop survives

- File: `scripts/board.py`
- Source: `u203.json`, row `M6_one_pass`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_each_cut_and_strip_is_needed_on_its_own`

Old text:

```
        while text != settled:
```

New text:

```
        for _ in (1,):
```

### `u203.M7_rule_line_is_a_heading`

comment_heading: read a line of emphasis markers alone as the heading, so a rule above Started reads as empty

- File: `scripts/board.py`
- Source: `u203.json`, row `M7_rule_line_is_a_heading`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_old_readings_stand`

Old text:

```
        if not text.strip("*_").strip():
            continue
```

New text:

```
        if not text:
            continue
```

### `u203.M8_ellipsis_not_trailing`

_TRAILING: leave the ellipsis character out, so Brainstorm followed by one reads as a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M8_ellipsis_not_trailing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_known_heading_reads_through_trailing_punctuation_and_emphasis`

Old text:

```
_TRAILING = ".?!;\u2026# \t"
```

New text:

```
_TRAILING = ".?!;# \t"
```

### `u203.M9_no_comma_cut`

_HEADING_END: drop the comma cut, so Started, 2026-10-13. reads as a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M9_no_comma_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_each_cut_and_strip_is_needed_on_its_own`

Old text:

```
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026](?=\s)")
```

New text:

```
_HEADING_END = re.compile(r"[:]|[.?!;\u2026](?=\s)")
```

### `u291.L1_lanes_back_to_five`

CLOUD_LANES: put the cap back at five, the count before 2026-11-21

- File: `scripts/board.py`
- Source: `u291.json`, row `L1_lanes_back_to_five`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_cloud_runs_ten_lanes`
  - `tests/test_board_cloud.py::test_the_default_offers_a_card_with_nine_held`
  - `tests/test_board_cloud.py::test_the_default_offers_nothing_with_ten_held`
  - `tests/test_board_cloud.py::test_the_lanes_help_names_the_default_of_ten`

Old text:

```
CLOUD_LANES = 10
```

New text:

```
CLOUD_LANES = 5
```

### `u291.L2_lanes_one_short`

CLOUD_LANES: nine lanes, one short of the cap

- File: `scripts/board.py`
- Source: `u291.json`, row `L2_lanes_one_short`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_cloud_runs_ten_lanes`
  - `tests/test_board_cloud.py::test_the_default_offers_a_card_with_nine_held`
  - `tests/test_board_cloud.py::test_the_default_offers_nothing_with_ten_held`
  - `tests/test_board_cloud.py::test_the_lanes_help_names_the_default_of_ten`

Old text:

```
CLOUD_LANES = 10
```

New text:

```
CLOUD_LANES = 9
```

### `u291.L3_lanes_one_over`

CLOUD_LANES: eleven lanes, one over the cap

- File: `scripts/board.py`
- Source: `u291.json`, row `L3_lanes_one_over`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_cloud_runs_ten_lanes`
  - `tests/test_board_cloud.py::test_the_default_offers_a_card_with_nine_held`
  - `tests/test_board_cloud.py::test_the_default_offers_nothing_with_ten_held`
  - `tests/test_board_cloud.py::test_the_lanes_help_names_the_default_of_ten`

Old text:

```
CLOUD_LANES = 10
```

New text:

```
CLOUD_LANES = 11
```

### `u291.L4_help_names_a_literal`

--lanes help: name a literal five rather than read the constant

- File: `scripts/board.py`
- Source: `u291.json`, row `L4_help_names_a_literal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_lanes_help_names_the_default_of_ten`

Old text:

```
        help=f"how many cards the cloud builds at once (default {CLOUD_LANES})",
```

New text:

```
        help="how many cards the cloud builds at once (default 5)",
```

### `u291.L5_default_ignores_the_constant`

cmd_cloud: with no --lanes, count four lanes rather than CLOUD_LANES

- File: `scripts/board.py`
- Source: `u291.json`, row `L5_default_ignores_the_constant`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_default_is_the_configured_lane_count`
  - `tests/test_board_cloud.py::test_the_default_offers_a_card_with_nine_held`
  - `tests/test_board_cloud.py::test_the_default_offers_nothing_with_ten_held`

Old text:

```
    lanes = max(1, getattr(args, "lanes", None) or CLOUD_LANES)
```

New text:

```
    lanes = max(1, getattr(args, "lanes", None) or 4)
```

### `u59.B1_per_message_split`

Concatenate the range again, manufacturing a trailer across two commits

- File: `scripts/board.py`
- Source: `u59.json`, row `B1_per_message_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closing_reference_is_never_manufactured_across_two_commit_messages`

Old text:

```
            ["git", "log", "--format=%B%x00", f"{args.since}..HEAD"],
```

New text:

```
            ["git", "log", "--format=%B", f"{args.since}..HEAD"],
```

### `u59.B2_raw_true_on_range`

Strip comments on the CI path, which can only delete a real trailer

- File: `scripts/board.py`
- Source: `u59.json`, row `B2_raw_true_on_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_hash_leading_body_line_survives_the_range_check`

Old text:

```
                problems += unresolved_closes(message, raw=False)
```

New text:

```
                problems += unresolved_closes(message, raw=True)
```

### `u59.B3_unit_mapping_ignored`

Ignore the supplied issue-to-unit map, restoring the number conflation

- File: `scripts/board.py`
- Source: `u59.json`, row `B3_unit_mapping_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_an_issue_number_is_resolved_to_its_unit_when_the_board_says_they_differ`

Old text:

```
        uid = reference if units is None else units.get(reference)
```

New text:

```
        uid = reference
```

### `u59.B4_guess_caveat_dropped`

Stop saying the unit number was guessed, so the reader trusts it

- File: `scripts/board.py`
- Source: `u59.json`, row `B4_guess_caveat_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_network_free_path_says_that_it_guessed_the_unit_number`

Old text:

```
        if units is None and reference == uid:
```

New text:

```
        if False:
```

### `u59.B6_duplicate_unit_kept`

Let a duplicated unit number resolve to whichever issue was seen last

- File: `scripts/board.py`
- Source: `u59.json`, row `B6_duplicate_unit_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_register_owing_a_unit_with_no_issue_at_all_is_silence_not_a_crash`
  - `tests/test_pending_units.py::test_the_unit_to_issue_map_is_read_off_the_titles_and_drops_a_duplicate`

Old text:

```
    return {unit: number for unit, number in seen.items() if unit not in duplicated}
```

New text:

```
    return seen
```

### `u59.B8_missing_file_raises`

Let a missing message file raise instead of refusing with a sentence

- File: `scripts/board.py`
- Source: `u59.json`, row `B8_missing_file_raises`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_missing_message_file_refuses_with_a_sentence_not_a_traceback`

Old text:

```
        if not path.is_file():
```

New text:

```
        if False:
```

### `u81-round-2.B5_owed_argument_ignored`

Ignore a supplied register and always read the live one

- File: `scripts/board.py`
- Source: `u81-round-2.json`, row `B5_owed_argument_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closed_unit_a_register_still_owes_is_the_contradiction_the_audit_exits_2_on`
  - `tests/test_pending_units.py::test_the_register_defaults_to_the_live_one_when_no_caller_supplies_it`

Old text:

```
    owed = owed_by_unit() if owed is None else owed
    issues_by_unit = units_by_issue_number(graph)
```

New text:

```
    owed = owed_by_unit()
    issues_by_unit = units_by_issue_number(graph)
```

### `u81-round-3.B5_audit_drops_the_detector`

Have the audit find no contradictions at all, keeping its drift report

- File: `scripts/board.py`
- Source: `u81-round-3.json`, row `B5_audit_drops_the_detector`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`

Old text:

```
    clashes = contradictions(graph)
```

New text:

```
    clashes = []
```

### `u81-round-3.B5_audit_exit_code`

Report a contradiction as exit 1, the code that sends a session to sync

- File: `scripts/board.py`
- Source: `u81-round-3.json`, row `B5_audit_exit_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`

Old text:

```
    return 2 if clashes else 1
```

New text:

```
    return 1
```

### `u81-round-3.B5_owed_default_dropped`

Collapse the no-register default into a falsy test, so an empty register reads as none

- File: `scripts/board.py`
- Source: `u81-round-3.json`, row `B5_owed_default_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`
  - `tests/test_pending_units.py::test_the_register_defaults_to_the_live_one_when_no_caller_supplies_it`

Old text:

```
    owed = owed_by_unit() if owed is None else owed
    issues_by_unit = units_by_issue_number(graph)
```

New text:

```
    owed = owed or {}
    issues_by_unit = units_by_issue_number(graph)
```

### `u81.B5_composite`

What B5 does hold: report a contradiction over an OPEN issue as well

- File: `scripts/board.py`
- Source: `u81.json`, row `B5_composite`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_mutation_driver.py`, `tests/test_pool_sizing.py`, `tests/test_restore.py`
- Collected: 2398 against a baseline of 2398
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closed_unit_a_register_still_owes_is_the_contradiction_the_audit_exits_2_on`

Old text:

```
        if node and node["unit"] and node["closed"]:
```

New text:

```
        if node and node["unit"]:
```

### `u81.B5_contradictions_by_number`

Index the graph by unit number again in contradictions()

- File: `scripts/board.py`
- Source: `u81.json`, row `B5_contradictions_by_number`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 3 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closed_unit_a_register_still_owes_is_the_contradiction_the_audit_exits_2_on`
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`
  - `tests/test_pending_units.py::test_the_register_defaults_to_the_live_one_when_no_caller_supplies_it`

Old text:

```
        number = issues_by_unit.get(uid)
        node = graph.get(number) if number is not None else None
```

New text:

```
        node = graph.get(uid)
```

### `u81.B5_residual_repoint_dropped`

Return only the register contradictions, dropping the repointed residuals

- File: `scripts/board.py`
- Source: `u81.json`, row `B5_residual_repoint_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_repointed_residual_issue_is_reported_through_the_same_call`

Old text:

```
    return found + repointed_residuals(graph)
```

New text:

```
    return found
```

### `u200.M11_complete_clone_fetched`

ensure_full_history: fetch a complete clone too, the review's survivor its fix round pins

- File: `scripts/cloud_battery.py`
- Source: `u200.json`, row `M11_complete_clone_fetched`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_complete_clone_runs_no_fetch`

Old text:

```
    if state == "false":
        return None
    if state != "true":
        return state
```

New text:

```
    if state not in ("true", "false"):
        return state
```

### `u200.M1_unreadable_read_as_complete`

ensure_full_history: read any answer but true as a complete clone, so a directory git cannot read passes

- File: `scripts/cloud_battery.py`
- Source: `u200.json`, row `M1_unreadable_read_as_complete`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_directory_git_cannot_read_is_refused_not_read_as_complete`

Old text:

```
    if state != "true":
        return state
```

New text:

```
    if state != "true":
        return None
```

### `u200.M2_no_fetch`

ensure_full_history: never fetch, so a shallow clone stays shallow

- File: `scripts/cloud_battery.py`
- Source: `u200.json`, row `M2_no_fetch`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_baseline_header_says_it_was_measured_with_full_history`
  - `tests/test_cloud_battery.py::test_a_shallow_clone_is_unshallowed_and_its_history_read_passes_after`

Old text:

```
["git", "fetch", "--unshallow", "origin", "main"]
```

New text:

```
["git", "--version"]
```

### `u200.M3_no_reread`

ensure_full_history: trust the fetch and skip reading the clone again, so a failed fetch passes

- File: `scripts/cloud_battery.py`
- Source: `u200.json`, row `M3_no_reread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_baseline_that_cannot_fetch_the_history_writes_nothing`
  - `tests/test_cloud_battery.py::test_a_remote_that_cannot_serve_the_history_is_refused`
  - `tests/test_cloud_battery.py::test_compare_refuses_a_branch_it_cannot_unshallow`

Old text:

```
    after = _shallow(root)
```

New text:

```
    after = "false"
```

### `u268.W11_error_count_singular_only`

read_report: read only the singular error count, so a run with two errors is refused

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W11_error_count_singular_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_plural_count_on_the_summary_line_is_read`

Old text:

```
        "error": _summary_count(summary, "errors?"),
```

New text:

```
        "error": _summary_count(summary, "error"),
```

### `u268.W1_id_cut_at_space`

read_report: keep each id up to its first space, as the summary line reader did, so a sibling's failure reads as the machine's

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W1_id_cut_at_space`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 8 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_complete_run_records_what_it_collected_and_pytests_exit`
  - `tests/test_cloud_battery.py::test_a_new_failure_that_differs_from_the_machines_only_after_a_space_is_yours`
  - `tests/test_cloud_battery.py::test_a_plural_count_on_the_summary_line_is_read`
  - `tests/test_cloud_battery.py::test_a_red_compare_is_recorded_red`
  - `tests/test_cloud_battery.py::test_a_report_that_agrees_with_the_summary_line_is_read`
  - `tests/test_cloud_battery.py::test_an_erroring_id_is_read_whole`
  - `tests/test_cloud_battery.py::test_an_id_holding_the_summary_separator_is_read_whole`
  - `tests/test_cloud_battery.py::test_compare_records_every_key_the_driver_reads`

Old text:

```
            ids.add(nodeid)
```

New text:

```
            ids.add(nodeid.split(" ")[0])
```

### `u268.W2_errors_not_read`

PLUGIN_SOURCE: read only the failed category, so an erroring test is never listed

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W2_errors_not_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 25 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_baseline_header_names_its_place_and_lists_its_tests_on_disk`
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[before]`
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[during]`
  - `tests/test_cloud_battery.py::test_a_commit_made_during_the_run_is_never_recorded_as_measured`
  - `tests/test_cloud_battery.py::test_a_complete_run_records_what_it_collected_and_pytests_exit`
  - `tests/test_cloud_battery.py::test_a_failure_that_moved_between_workers_is_read_by_its_id`
  - `tests/test_cloud_battery.py::test_a_file_that_cannot_be_collected_is_read_by_its_path`
  - `tests/test_cloud_battery.py::test_a_listed_test_failing_on_disk_is_recorded_failing`
  - `tests/test_cloud_battery.py::test_a_new_failure_that_differs_from_the_machines_only_after_a_space_is_yours`
  - `tests/test_cloud_battery.py::test_a_red_compare_is_recorded_red`
  - `tests/test_cloud_battery.py::test_a_run_in_memory_records_the_ids_after_its_rerun_and_the_memory_counts`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[serial]`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[workers]`
  - `tests/test_cloud_battery.py::test_an_erroring_id_is_read_whole`
  - `tests/test_cloud_battery.py::test_an_id_holding_the_summary_separator_is_read_whole`
  - ... and 10 more, see the JSON sidecar

Old text:

```
    for category in ("failed", "error"):
        reports = terminalreporter.stats.get(category, [])
```

New text:

```
    for category in ("failed",):
        reports = terminalreporter.stats.get(category, [])
```

### `u268.W3_no_report_read_as_clean`

failing_ids: drop the refusal of a run that wrote no report

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W3_no_report_read_as_clean`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_run_that_wrote_no_report_is_refused`

Old text:

```
        if not report_path.is_file():
            print(result.stdout[-3000:])
```

New text:

```
        if False:
            print(result.stdout[-3000:])
```

### `u268.W4_counts_not_checked`

read_report: drop the check of the report's counts against the summary line

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W4_counts_not_checked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_report_that_cannot_be_read_whole_is_refused[an-error-the-summary-never-counted]`

Old text:

```
        if not isinstance(entry, dict) or entry.get("counted") != count:
```

New text:

```
        if not isinstance(entry, dict):
```

### `u268.W5_listed_not_checked`

read_report: drop the check that the report lists as many ids as it counts

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W5_listed_not_checked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_report_that_cannot_be_read_whole_is_refused[counted-but-not-listed]`

Old text:

```
        if not isinstance(listed, list) or len(listed) < count:
```

New text:

```
        if not isinstance(listed, list):
```

### `u268.W6_id_with_line_break_stored`

read_report: store an id holding a line break, which the file would split in two

- File: `scripts/cloud_battery.py`
- Source: `u268.json`, row `W6_id_with_line_break_stored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 4 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_report_that_cannot_be_read_whole_is_refused[a-carriage-return]`
  - `tests/test_cloud_battery.py::test_a_report_that_cannot_be_read_whole_is_refused[a-line-break]`
  - `tests/test_cloud_battery.py::test_a_report_that_cannot_be_read_whole_is_refused[a-line-separator]`
  - `tests/test_cloud_battery.py::test_a_report_that_cannot_be_read_whole_is_refused[a-vertical-tab]`

Old text:

```
                or nodeid.splitlines() != [nodeid]

```

New text:

```
(empty)
```

### `u271-measured.B1_run_cleanliness_at_the_end_only`

measured_tree: read cleanliness after the run only, so a change made before it and a moved HEAD are missed

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B1_run_cleanliness_at_the_end_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`, `tests/test_mutation_driver.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_commit_made_during_the_run_is_never_recorded_as_measured`
  - `tests/test_cloud_battery.py::test_the_baseline_header_names_the_commit_read_before_the_run`

Old text:

```
    clean = before.clean and after.clean and before.commit == after.commit
```

New text:

```
    clean = after.clean
```

### `u271-measured.B2_commit_read_after_the_run`

measured_tree: name the commit read after the run, as last-compare.txt did before U271

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B2_commit_read_after_the_run`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`, `tests/test_mutation_driver.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_commit_made_during_the_run_is_never_recorded_as_measured`

Old text:

```
    return TreeState(commit=before.commit, clean=clean)
```

New text:

```
    return TreeState(commit=after.commit, clean=clean)
```

### `u271-measured.B3_status_unread`

tree_state in the battery: read only git's exit, so a tree with changes reads clean

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B3_status_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`, `tests/test_mutation_driver.py`
- Collected: 244 against a baseline of 244
- Kills: 3 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[before]`
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[during]`
  - `tests/test_cloud_battery.py::test_an_untracked_file_hidden_by_git_config_is_still_seen`

Old text:

```
    clean = bool(commit) and status.returncode == 0 and not status.stdout.strip()
    return TreeState(commit=commit, clean=clean)
```

New text:

```
    clean = bool(commit) and status.returncode == 0
    return TreeState(commit=commit, clean=clean)
```

### `u271-measured.B4_release_line_never_dirty`

record_verdict: never write dirty, so the release reads a moved tree as clean

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B4_release_line_never_dirty`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`, `tests/test_mutation_driver.py`, `tests/test_release.py`
- Collected: 304 against a baseline of 304
- Kills: 3 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[before]`
  - `tests/test_cloud_battery.py::test_a_change_to_the_tree_marks_the_run_unclean[during]`
  - `tests/test_cloud_battery.py::test_a_commit_made_during_the_run_is_never_recorded_as_measured`

Old text:

```
    if not tree.clean:
        verdict = "dirty"
```

New text:

```
    if False:
        verdict = "dirty"
```

### `u271-measured.B5_collection_errors_unlisted`

the reporting plugin: list no collection errors

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B5_collection_errors_unlisted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`, `tests/test_mutation_driver.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_the_suite_run_reads_the_collected_count_and_the_collection_errors`

Old text:

```
            if getattr(report, "when", None) == "collect"
```

New text:

```
            if getattr(report, "when", None) == "never"
```

### `u271-measured.B6_count_unread_under_workers`

the reporting plugin: drop the xdist hook, so a run with workers records no collected count

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B6_count_unread_under_workers`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`, `tests/test_mutation_driver.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[workers]`
  - `tests/test_cloud_battery.py::test_the_collected_count_is_read_under_the_repositorys_distribution`

Old text:

```
def pytest_xdist_node_collection_finished(node, ids):
    _COLLECTED["count"] = len(ids)
```

New text:

```
def pytest_xdist_node_collection_finished(node, ids):
    pass
```

### `u271-measured.B7_boot_unrecorded`

record_run: record no boot id, which the driver then reads as another machine

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B7_boot_unrecorded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`, `tests/test_mutation_driver.py`
- Collected: 244 against a baseline of 244
- Kills: 15 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_clean_verdict_for_this_commit_stands_for_the_full_baseline`
  - `tests/test_mutation_driver.py::test_a_red_verdict_for_this_commit_refuses_the_batch`
  - `tests/test_mutation_driver.py::test_a_run_that_stopped_early_with_exit_one_is_not_read`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-collection-error-read-clean]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-verdict-its-ids-contradict]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[an-edited-run]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[an-interrupted-run]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-checkout]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-interpreter]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-known-failures-file]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[fewer-ran-than-collected]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[no-count-of-what-ran]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[nothing-collected]`
  - `tests/test_mutation_driver.py::test_the_command_line_reads_the_verdict_and_measures_on_request`
  - `tests/test_mutation_driver.py::test_the_table_says_the_full_baseline_was_read_and_what_was_measured`

Old text:

```
        "boot_id": boot_id(),
```

New text:

```
        "boot_id": "",
```

### `u271-measured.B8_ran_uncounted`

the reporting plugin: count no test as having reported

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B8_ran_uncounted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`, `tests/test_mutation_driver.py`
- Collected: 244 against a baseline of 244
- Kills: 12 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_complete_run_records_what_it_collected_and_pytests_exit`
  - `tests/test_cloud_battery.py::test_a_run_in_memory_records_the_ids_after_its_rerun_and_the_memory_counts`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[serial]`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[workers]`
  - `tests/test_cloud_battery.py::test_compare_records_every_key_the_driver_reads`
  - `tests/test_mutation_driver.py::test_a_clean_verdict_for_this_commit_stands_for_the_full_baseline`
  - `tests/test_mutation_driver.py::test_a_red_verdict_for_this_commit_refuses_the_batch`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-collection-error-read-clean]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-verdict-its-ids-contradict]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[an-edited-run]`
  - `tests/test_mutation_driver.py::test_the_command_line_reads_the_verdict_and_measures_on_request`
  - `tests/test_mutation_driver.py::test_the_table_says_the_full_baseline_was_read_and_what_was_measured`

Old text:

```
    _RAN.add(report.nodeid)
```

New text:

```
    pass
```

### `u273.P10_placeless_baseline_read`

read_baseline: read a baseline that names no place, as every one before U273

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P10_placeless_baseline_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_baseline_naming_a_place_that_is_not_one_is_refused[a-filesystem]`
  - `tests/test_cloud_battery.py::test_a_baseline_naming_a_place_that_is_not_one_is_refused[unknown]`
  - `tests/test_cloud_battery.py::test_a_baseline_naming_no_place_was_measured_before_u273_and_is_refused`

Old text:

```
    if match.group(3) not in PLACES:
```

New text:

```
    if False:
```

### `u273.P11_other_place_compared`

cmd_compare: run a compare in the place it asks for even when the baseline was measured in the other

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P11_other_place_compared`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_compare_in_the_other_place_from_its_baseline_is_refused[disk-memory]`
  - `tests/test_cloud_battery.py::test_a_compare_in_the_other_place_from_its_baseline_is_refused[memory-disk]`

Old text:

```
    if requested is not None and requested != base.place:
```

New text:

```
    if False:
```

### `u273.P13_rerun_disk_unchecked_upfront`

refusal_for: check only the run's own place, so a disk the rerun cannot have refuses after a whole run in memory

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P13_rerun_disk_unchecked_upfront`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_memory_run_whose_disk_rerun_cannot_be_given_is_refused_before_it_runs`

Old text:

```
    return (MEMORY, DISK) if place == MEMORY and ON_DISK else (place,)
```

New text:

```
    return (place,)
```

### `u273.P1_memory_any_filesystem`

place_root: accept any filesystem as memory, so a run named memory may be on disk

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P1_memory_any_filesystem`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_memory_is_a_place_only_on_a_memory_filesystem_with_room`

Old text:

```
        if kind not in MEMORY_FILESYSTEMS:
            return None, f"{root} is not a memory filesystem here ({kind or 'no mount table'})"
```

New text:

```
        if False:
            return None, f"{root} is not a memory filesystem here ({kind or 'no mount table'})"
```

### `u273.P2_no_floor`

place_root: drop the free space floor, so a small /dev/shm fills partway through a run

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P2_no_floor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_baseline_in_a_place_the_machine_cannot_give_is_refused`
  - `tests/test_cloud_battery.py::test_a_compare_is_refused_when_the_machine_cannot_give_the_baselines_place_now`
  - `tests/test_cloud_battery.py::test_memory_is_a_place_only_on_a_memory_filesystem_with_room`

Old text:

```
        if free < MEMORY_FLOOR:
```

New text:

```
        if False:
```

### `u273.P3_disk_on_memory_accepted`

place_root: accept a disk TMPDIR that is itself on a memory filesystem

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P3_disk_on_memory_accepted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_memory_run_whose_disk_rerun_cannot_be_given_is_refused_before_it_runs`
  - `tests/test_cloud_battery.py::test_disk_is_refused_when_the_temporary_directory_is_itself_in_memory`

Old text:

```
        if kind in MEMORY_FILESYSTEMS:
            return None, (
```

New text:

```
        if False:
            return None, (
```

### `u273.P4_mount_first_match`

filesystem_of: take every mount point holding the path rather than the longest

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P4_mount_first_match`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_mount_table_is_read_by_its_longest_mount_point`

Old text:

```
        if inside and len(point) >= len(best):
```

New text:

```
        if inside:
```

### `u273.P5_tmpdir_not_set`

_run_suite: do not point the run's TMPDIR at its place, so it inherits the caller's

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P5_tmpdir_not_set`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 9 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_complete_run_records_what_it_collected_and_pytests_exit`
  - `tests/test_cloud_battery.py::test_a_run_in_memory_records_the_ids_after_its_rerun_and_the_memory_counts`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[serial]`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[workers]`
  - `tests/test_cloud_battery.py::test_an_unlisted_test_failing_in_memory_stays_failing`
  - `tests/test_cloud_battery.py::test_in_memory_the_whole_suite_runs_there_and_the_listed_tests_again_on_disk`
  - `tests/test_cloud_battery.py::test_the_collected_count_is_read_under_the_repositorys_distribution`
  - `tests/test_cloud_battery.py::test_the_suite_command_leaves_the_distribution_to_addopts`
  - `tests/test_cloud_battery.py::test_the_suite_run_reads_the_collected_count_and_the_collection_errors`

Old text:

```
        env["TMPDIR"] = str(temp)

```

New text:

```
(empty)
```

### `u273.P6_no_rerun_on_disk`

failing_ids: never run the listed tests again on disk after a run in memory

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P6_no_rerun_on_disk`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 6 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_baseline_header_names_its_place_and_lists_its_tests_on_disk`
  - `tests/test_cloud_battery.py::test_a_listed_test_failing_on_disk_is_recorded_failing`
  - `tests/test_cloud_battery.py::test_a_run_in_memory_records_the_ids_after_its_rerun_and_the_memory_counts`
  - `tests/test_cloud_battery.py::test_an_on_disk_run_that_did_not_run_a_listed_test_is_refused[not-collected]`
  - `tests/test_cloud_battery.py::test_an_on_disk_run_that_did_not_run_a_listed_test_is_refused[skipped-on-disk]`
  - `tests/test_cloud_battery.py::test_in_memory_the_whole_suite_runs_there_and_the_listed_tests_again_on_disk`

Old text:

```
    listed = tuple(ON_DISK) if place == MEMORY else ()
```

New text:

```
    listed = ()
```

### `u273.P8_disk_run_unchecked`

failing_ids: accept an on disk run that skipped or never collected a listed test

- File: `scripts/cloud_battery.py`
- Source: `u273.json`, row `P8_disk_run_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_an_on_disk_run_that_did_not_run_a_listed_test_is_refused[skipped-on-disk]`

Old text:

```
    if unread or stray:
```

New text:

```
    if False:
```

### `u276.K9_agreement_script_default_whole`

head_agreement.py: default --key to whole, so the attended sitting's run with no --key reads the old method, not the shipped one

- File: `scripts/head_agreement.py`
- Source: `u276.json`, row `K9_agreement_script_default_whole`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`, `tests/test_head_agreement.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_the_agreement_script_reads_the_default_method_when_none_is_named`

Old text:

```
        default=detect.KEY_DEFAULT,
```

New text:

```
        default=detect.KEY_WHOLE,
```

### `u297.K1_a_zero_row_counted_as_a_kill`

killed: count a row with zero deaths as killed, so the kill set holds rows no test ever killed

- File: `scripts/killset.py`
- Source: `u297.json`, row `K1_a_zero_row_counted_as_a_kill`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 6 (killed)
- Killed:
  - `tests/test_killset.py::test_a_row_is_live_stale_ambiguous_or_gone_by_what_the_tree_holds`
  - `tests/test_killset.py::test_a_row_that_broke_collection_before_is_held_to_no_less_after`
  - `tests/test_killset.py::test_a_table_of_the_older_form_is_read_by_its_deaths`
  - `tests/test_killset.py::test_check_passes_when_every_kill_is_kept`
  - `tests/test_killset.py::test_list_prints_the_counts_and_one_line_a_file`
  - `tests/test_killset.py::test_rows_after_leaves_text_it_cannot_place_for_the_author`

Old text:

```
    return isinstance(deaths, int) and not isinstance(deaths, bool) and deaths > 0
```

New text:

```
    return isinstance(deaths, int) and not isinstance(deaths, bool) and deaths >= 0
```

### `u297.K2_a_lost_kill_passes_check`

compare_tables: stop reading a row that is weaker after than before as lost, so check passes a refactor that lost a kill

- File: `scripts/killset.py`
- Source: `u297.json`, row `K2_a_lost_kill_passes_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 6 (killed)
- Killed:
  - `tests/test_killset.py::test_a_kill_that_became_a_collection_error_is_lost_though_it_records_a_death`
  - `tests/test_killset.py::test_a_row_that_broke_collection_before_is_held_to_no_less_after`
  - `tests/test_killset.py::test_a_table_of_the_older_form_is_read_by_its_deaths`
  - `tests/test_killset.py::test_check_fails_on_one_lost_kill_and_names_it`
  - `tests/test_killset.py::test_check_matches_tables_that_are_not_replays_by_row_id`
  - `tests/test_killset.py::test_recorded_kills_replay_through_the_driver_and_check_clean`

Old text:

```
            if strength(now) < held:
```

New text:

```
            if False:
```

### `u297.K3_mapped_to_a_row_that_is_not_killed`

compare_tables: accept a mapping whose target row is weaker after than the kill it covers

- File: `scripts/killset.py`
- Source: `u297.json`, row `K3_mapped_to_a_row_that_is_not_killed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_killset.py::test_a_mapping_onto_a_row_that_only_broke_collection_does_not_cover_a_kill`
  - `tests/test_killset.py::test_check_fails_a_row_mapped_to_a_row_that_is_not_killed`

Old text:

```
        elif strength(target) < held:
```

New text:

```
        elif False:
```

### `u297.K4_a_collection_error_counts_as_a_kill`

strength: rank a row that broke collection with a death as high as a clean kill, so a kill that became one is kept

- File: `scripts/killset.py`
- Source: `u297.json`, row `K4_a_collection_error_counts_as_a_kill`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 3 (killed)
- Killed:
  - `tests/test_killset.py::test_a_kill_that_became_a_collection_error_is_lost_though_it_records_a_death`
  - `tests/test_killset.py::test_a_mapping_onto_a_row_that_only_broke_collection_does_not_cover_a_kill`
  - `tests/test_killset.py::test_a_row_that_broke_collection_before_is_held_to_no_less_after`

Old text:

```
    return 2 if row.get("status") in (None, "killed") else 1
```

New text:

```
    return 2
```

### `u297.K5_any_reason_vouches_for_a_move`

unvouched_move: accept the reason rows --after wrote with no test in common, so a row killed at another guard's line passes check

- File: `scripts/killset.py`
- Source: `u297.json`, row `K5_any_reason_vouches_for_a_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 3 (killed)
- Killed:
  - `tests/test_killset.py::test_a_line_written_new_elsewhere_reads_as_a_move_and_check_is_what_catches_it`
  - `tests/test_killset.py::test_a_replay_at_another_guards_line_does_not_bring_a_dead_row_back`
  - `tests/test_killset.py::test_a_row_the_tool_moved_must_still_die_by_a_test_that_killed_it_before`

Old text:

```
    if killers_before & now or not reason.startswith(AUTOMATIC_MOVE):
```

New text:

```
    if reason:
```

### `u297.K6_a_twin_read_as_a_move`

moved_to: place a row at the one file that holds its text now though the text stood in two places at the measured commit

- File: `scripts/killset.py`
- Source: `u297.json`, row `K6_a_twin_read_as_a_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 3 (killed)
- Killed:
  - `tests/test_killset.py::test_a_deleted_guard_is_not_anchored_on_its_twin_wherever_the_twin_is_now[_twin_is_renamed]`
  - `tests/test_killset.py::test_a_deleted_guard_is_not_anchored_on_its_twin_wherever_the_twin_is_now[_twin_is_split]`
  - `tests/test_killset.py::test_a_deleted_guard_is_not_anchored_on_its_twin_wherever_the_twin_is_now[_twin_stays]`

Old text:

```
    if stood != 1:
```

New text:

```
    if False:
```

### `u297.K7_a_batch_in_progress_read_as_finished`

read_measured: read a table still in progress as a finished batch, so its unmeasured rows are compared as if measured

- File: `scripts/killset.py`
- Source: `u297.json`, row `K7_a_batch_in_progress_read_as_finished`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_killset.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_killset.py::test_check_refuses_a_table_that_is_not_a_finished_valid_batch[extra1-in progress]`

Old text:

```
    if table.get("valid") is not True or table.get("invalid_reason"):
```

New text:

```
    if table.get("valid") is not True:
```

### `r343-composites.C2_no_timestamps_no_hash`

composite for G8 in r343.md: drop mtime, ctime and the content hash together, leaving path, size and inode; a same size rewrite must now pass unseen, so the test that rewrites in place is the death

- File: `scripts/mutate.py`
- Source: `r343-composites.json`, row `C2_no_timestamps_no_hash`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_same_size_rewrite_of_a_small_file_is_a_leak`

Old text:

```
                f"\t{info.st_mtime_ns}\t{info.st_ctime_ns}"
            )
            if info.st_size <= SMALL_FILE_BYTES and not os.path.islink(path):
```

New text:

```
                ""
            )
            if False:
```

### `r343-composites.C3_path_only`

composite for G3 in r343.md: drop size, inode, timestamps and the hash, leaving the path alone; only a new or removed entry is seen

- File: `scripts/mutate.py`
- Source: `r343-composites.json`, row `C3_path_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_same_size_rewrite_of_a_small_file_is_a_leak`

Old text:

```
                f"{relative}\t{info.st_size}\t{info.st_ino}"
                f"\t{info.st_mtime_ns}\t{info.st_ctime_ns}"
            )
            if info.st_size <= SMALL_FILE_BYTES and not os.path.islink(path):
```

New text:

```
                f"{relative}"
            )
            if False:
```

### `r343.G10_guard_not_checked_on_timeout`

the check leaves the finally, so a child that leaks and then hangs is filed as a timeout

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G10_guard_not_checked_on_timeout`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_that_leaks_and_then_hangs_is_still_caught`

Old text:

```
        finally:
            # In a finally, so a child that leaks and then hangs past the
```

New text:

```
        except subprocess.TimeoutExpired:
            raise
        else:
            # In a finally, so a child that leaks and then hangs past the
```

### `r343.G1_guard_never_fires`

check_state_guard treats every digest as unchanged

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G1_guard_never_fires`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 6 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_that_leaks_and_then_hangs_is_still_caught`
  - `tests/test_mutation_driver.py::test_a_directory_created_inside_the_real_root_is_a_leak`
  - `tests/test_mutation_driver.py::test_a_leak_during_the_baseline_names_the_phase`
  - `tests/test_mutation_driver.py::test_a_leak_under_a_row_names_that_row_and_stops_the_batch`
  - `tests/test_mutation_driver.py::test_a_same_size_rewrite_of_a_small_file_is_a_leak`
  - `tests/test_mutation_driver.py::test_an_absent_installation_state_that_a_child_creates_is_a_leak`

Old text:

```
        if now == before:
            continue
```

New text:

```
        if True:
            continue
```

### `r343.G4_existence_not_fingerprinted`

a child that creates the real directory is not a change

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G4_existence_not_fingerprinted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_an_absent_installation_state_that_a_child_creates_is_a_leak`

Old text:

```
    entries: list[str] = [f"exists={root.is_dir()}"]
```

New text:

```
    entries: list[str] = ["exists=True"]
```

### `r343.G5_row_loop_swallows_the_leak`

the row loop's StateLeak handler stops re-raising, so the blanket handler files it as an error row and the batch continues

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G5_row_loop_swallows_the_leak`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_leak_under_a_row_names_that_row_and_stops_the_batch`

Old text:

```
            # spending children against a machine it had just damaged.
            raise
```

New text:

```
            # spending children against a machine it had just damaged.
            pass
```

### `r343.G6_run_pytest_skips_the_check`

run_pytest never calls check_state_guard

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G6_run_pytest_skips_the_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_that_leaks_and_then_hangs_is_still_caught`
  - `tests/test_mutation_driver.py::test_a_leak_during_the_baseline_names_the_phase`
  - `tests/test_mutation_driver.py::test_a_leak_under_a_row_names_that_row_and_stops_the_batch`

Old text:

```
            if guard is not None:
                check_state_guard(guard, label=label)
```

New text:

```
            if False:
                check_state_guard(guard, label=label)
```

### `r343.G7_label_not_carried`

every leak is reported as a generic child run rather than the row or phase that caused it

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G7_label_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_that_leaks_and_then_hangs_is_still_caught`
  - `tests/test_mutation_driver.py::test_a_leak_during_the_baseline_names_the_phase`
  - `tests/test_mutation_driver.py::test_a_leak_under_a_row_names_that_row_and_stops_the_batch`

Old text:

```
            check_state_guard(guard, label=label)
```

New text:

```
            check_state_guard(guard, label="a child run")
```

### `r343.G9_directories_not_fingerprinted`

a directory created inside the real root is not an entry

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G9_directories_not_fingerprinted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_directory_created_inside_the_real_root_is_a_leak`

Old text:

```
        for name in dirnames:
            entries.append(f"{(here / name).relative_to(root).as_posix()}\tdir")
```

New text:

```
        for name in ():
            entries.append(f"{(here / name).relative_to(root).as_posix()}\tdir")
```

### `r343.R1_config_override_ignored`

installation_state_roots resolves through platformdirs even when CRATEKIT_CONFIG_DIR is set, so the suite would guard the real machine's directory

- File: `scripts/mutate.py`
- Source: `r343.json`, row `R1_config_override_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_the_guarded_roots_follow_the_overrides_this_process_carries`

Old text:

```
        if config_override
        else Path(platformdirs.user_config_dir(APP_NAME)),
```

New text:

```
        if False
        else Path(platformdirs.user_config_dir(APP_NAME)),
```

### `r343.R2_roots_not_deduplicated`

a config and state directory that agree are walked twice

- File: `scripts/mutate.py`
- Source: `r343.json`, row `R2_roots_not_deduplicated`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_the_guarded_roots_follow_the_overrides_this_process_carries`

Old text:

```
    return tuple(dict.fromkeys(roots))
```

New text:

```
    return tuple(roots)
```

### `r343.S1_no_home_redirect`

the child keeps the caller's HOME, so platformdirs resolves the real config directory

- File: `scripts/mutate.py`
- Source: `r343.json`, row `S1_no_home_redirect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_writing_a_config_does_not_reach_the_callers_own`
  - `tests/test_mutation_driver.py::test_the_child_starts_in_a_sandboxed_installation_state`
  - `tests/test_mutation_driver.py::test_the_sandbox_covers_every_variable_the_conftest_isolates`

Old text:

```
    "HOME": "home",
```

New text:

```
    "HOME_UNSET": "home",
```

### `r343.S2_no_config_dir_override`

the child keeps the caller's CRATEKIT_CONFIG_DIR

- File: `scripts/mutate.py`
- Source: `r343.json`, row `S2_no_config_dir_override`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_writing_a_config_does_not_reach_the_callers_own`
  - `tests/test_mutation_driver.py::test_the_child_starts_in_a_sandboxed_installation_state`
  - `tests/test_mutation_driver.py::test_the_sandbox_covers_every_variable_the_conftest_isolates`

Old text:

```
    "CRATEKIT_CONFIG_DIR": f"config/{APP_NAME}",
```

New text:

```
    "CRATEKIT_CONFIG_DIR_UNSET": f"config/{APP_NAME}",
```

### `r343.S3_no_state_dir_override`

the child keeps the caller's CRATEKIT_STATE_DIR

- File: `scripts/mutate.py`
- Source: `r343.json`, row `S3_no_state_dir_override`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_writing_a_config_does_not_reach_the_callers_own`
  - `tests/test_mutation_driver.py::test_the_child_starts_in_a_sandboxed_installation_state`
  - `tests/test_mutation_driver.py::test_the_sandbox_covers_every_variable_the_conftest_isolates`

Old text:

```
    "CRATEKIT_STATE_DIR": f"state/{APP_NAME}",
```

New text:

```
    "CRATEKIT_STATE_DIR_UNSET": f"state/{APP_NAME}",
```

### `r343.S4_no_xdg_config_redirect`

the child keeps the caller's XDG_CONFIG_HOME; platformdirs ignores XDG on macOS, so this row measures the Linux half of the redirect from a Mac

- File: `scripts/mutate.py`
- Source: `r343.json`, row `S4_no_xdg_config_redirect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_writing_a_config_does_not_reach_the_callers_own`
  - `tests/test_mutation_driver.py::test_the_sandbox_covers_every_variable_the_conftest_isolates`

Old text:

```
    "XDG_CONFIG_HOME": "config",
```

New text:

```
    "XDG_CONFIG_HOME_UNSET": "config",
```

### `u200.M10_driver_unreadable_read_as_complete`

refuse_a_shallow_clone: refuse only an answer of true, so a repository git cannot read passes

- File: `scripts/mutate.py`
- Source: `u200.json`, row `M10_driver_unreadable_read_as_complete`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_known_failures_are_refused_on_a_shallow_clone`

Old text:

```
    if done.returncode != 0 or answer != "false":
```

New text:

```
    if answer == "true":
```

### `u200.M9_driver_skips_shallow_check`

main: subtract known failures without checking the clone is complete

- File: `scripts/mutate.py`
- Source: `u200.json`, row `M9_driver_skips_shallow_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_known_failures_are_refused_on_a_shallow_clone`

Old text:

```
            refuse_a_shallow_clone(args.repo_root)

```

New text:

```
            pass

```

### `u251.W3_driver_strips_the_distribution`

mutate.pytest_addopts: strip --dist and worksteal as well as -q, so the driver's children run under the default distribution

- File: `scripts/mutate.py`
- Source: `u251.json`, row `W3_driver_strips_the_distribution`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_suite_distribution.py`, `tests/test_mutation_driver.py`
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/test_suite_distribution.py::test_the_mutation_driver_passes_the_distribution_on`

Old text:

```
    return " ".join(token for token in tokens if token not in {"-q", "-qq", "--quiet"})
```

New text:

```
    return " ".join(
        token for token in tokens if token not in {"-q", "-qq", "--quiet", "--dist", "worksteal"}
    )
```

### `u251.W5_count_summed_over_workers`

mutate plugin: add each worker's collection to the count rather than take one, so a parallel run reports every worker's copy

- File: `scripts/mutate.py`
- Source: `u251.json`, row `W5_count_summed_over_workers`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_kill_under_parallel_workers_names_the_same_tests_as_a_serial_run`
  - `tests/test_mutation_driver.py::test_a_three_file_subset_still_collects_and_reports_under_a_steal`
  - `tests/test_mutation_driver.py::test_the_collected_count_survives_parallel_workers`
  - `tests/test_mutation_driver.py::test_the_count_and_the_failure_survive_a_steal`

Old text:

```
    _STATE["collected"] = len(ids)
```

New text:

```
    _STATE["collected"] += len(ids)
```

### `u268.W10_driver_reads_cut_baseline`

read_known_failures: accept a header that ends history full, a baseline written before U268

- File: `scripts/mutate.py`
- Source: `u268.json`, row `W10_driver_reads_cut_baseline`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 41 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_baseline_red_only_by_the_machines_known_failures_is_green`
  - `tests/test_mutation_driver.py::test_a_clean_verdict_for_this_commit_stands_for_the_full_baseline`
  - `tests/test_mutation_driver.py::test_a_disk_the_rerun_cannot_have_is_refused_before_anything_runs`
  - `tests/test_mutation_driver.py::test_a_known_failure_whose_id_holds_a_space_is_subtracted_whole`
  - `tests/test_mutation_driver.py::test_a_place_this_machine_cannot_give_is_refused_before_anything_runs`
  - `tests/test_mutation_driver.py::test_a_red_verdict_for_this_commit_refuses_the_batch`
  - `tests/test_mutation_driver.py::test_a_run_that_stopped_early_with_exit_one_is_not_read`
  - `tests/test_mutation_driver.py::test_a_status_git_cannot_read_is_never_a_clean_tree`
  - `tests/test_mutation_driver.py::test_a_verdict_for_another_commit_is_not_read`
  - `tests/test_mutation_driver.py::test_a_verdict_is_not_read_over_a_tree_with_changes`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-collection-error-read-clean]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-verdict-its-ids-contradict]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[an-edited-run]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[an-interrupted-run]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-boot]`
  - ... and 26 more, see the JSON sidecar

Old text:

```
    whole = f" {KNOWN_FAILURES_FULL_HISTORY} {KNOWN_FAILURES_WHOLE_IDS}"
```

New text:

```
    whole = f" {KNOWN_FAILURES_FULL_HISTORY}"
```

### `u271-measured.D10_empty_count_read`

read_battery_verdict: accept a record that collected nothing

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D10_empty_count_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[nothing-collected]`

Old text:

```
record["collected"] > 0,
```

New text:

```
record["collected"] >= 0,
```

### `u271-measured.D11_verdict_disagreement_read`

read_battery_verdict: drop the check that the verdict agrees with the ids it lists

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D11_verdict_disagreement_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-collection-error-read-clean]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-verdict-its-ids-contradict]`

Old text:

```
    if green != (record["verdict"] == "clean"):
```

New text:

```
    if False:
```

### `u271-measured.D12_red_record_read_green`

read_battery_verdict: build the read baseline with no failures, so a red verdict reads green

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D12_red_record_read_green`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_red_verdict_for_this_commit_refuses_the_batch`

Old text:

```
        failed=tuple(beyond),
```

New text:

```
        failed=(),
```

### `u271-measured.D13_no_known_file_layer`

read_battery_verdict: drop the refusal of a run with no known failures file, the layer before the digest key

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D13_no_known_file_layer`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_no_known_failures_file_means_the_verdict_is_not_read`

Old text:

```
    if not known_digest:
```

New text:

```
    if False:
```

### `u271-measured.D14_read_named_measured`

measure_batch: record a read baseline as measured, so the table names the wrong one

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D14_read_named_measured`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_clean_verdict_for_this_commit_stands_for_the_full_baseline`
  - `tests/test_mutation_driver.py::test_the_command_line_reads_the_verdict_and_measures_on_request`
  - `tests/test_mutation_driver.py::test_the_table_says_the_full_baseline_was_read_and_what_was_measured`

Old text:

```
        header["baseline_source"] = "read"
```

New text:

```
        header["baseline_source"] = "measured"
```

### `u271-measured.D15_early_stop_read`

read_battery_verdict: drop the check that every collected test reported, so a run stopped early reads complete

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D15_early_stop_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_run_that_stopped_early_with_exit_one_is_not_read`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[fewer-ran-than-collected]`

Old text:

```
record["ran"] == record["collected"],
```

New text:

```
record["ran"] <= record["collected"],
```

### `u271-measured.D16_edited_run_read`

read_battery_verdict: drop the refusal of a run that inherited PYTEST_ADDOPTS

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D16_edited_run_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[an-edited-run]`

Old text:

```
            record.get("pytest_addopts") == "",
```

New text:

```
            True,
```

### `u271-measured.D1_commit_unchecked`

read_battery_verdict: drop the commit key, so a verdict for another commit is read

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D1_commit_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_for_another_commit_is_not_read`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[no-commit]`

Old text:

```
            bool(commit) and recorded == commit,
```

New text:

```
            True,
```

### `u271-measured.D2_run_cleanliness_unchecked`

read_battery_verdict: drop the key saying the tree was clean throughout the battery's run

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D2_run_cleanliness_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[dirty-during-the-run]`

Old text:

```
        (record.get("clean_tree") is True, "the tree was not clean throughout the battery's run"),
```

New text:

```
        (True, "the tree was not clean throughout the battery's run"),
```

### `u271-measured.D3_tree_now_unchecked`

read_battery_verdict: drop the check that this tree is clean now

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D3_tree_now_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_is_not_read_over_a_tree_with_changes`
  - `tests/test_mutation_driver.py::test_untracked_files_hidden_by_git_config_still_make_the_tree_unclean`

Old text:

```
        (clean_now is True, "this tree has uncommitted or untracked changes"),
```

New text:

```
        (True, "this tree has uncommitted or untracked changes"),
```

### `u271-measured.D4_unreadable_status_read_as_clean`

tree_state in the driver: drop the None for a status git could not read, so an empty failed status reads clean

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D4_unreadable_status_read_as_clean`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_status_git_cannot_read_is_never_a_clean_tree`

Old text:

```
    if not commit or status.returncode != 0:
        return commit, None
```

New text:

```
    if not commit:
        return commit, None
```

### `u271-measured.D5_boot_unchecked`

read_battery_verdict: key the machine on the host name alone, which every cloud container shares

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D5_boot_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-boot]`

Old text:

```
            record.get("host") == socket.gethostname() and record.get("boot_id") == boot_id(),
```

New text:

```
            record.get("host") == socket.gethostname(),
```

### `u271-measured.D6_checkout_unchecked`

read_battery_verdict: drop the checkout key

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D6_checkout_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-checkout]`

Old text:

```
        (record.get("root") == str(repo_root.resolve()), "it was measured in another checkout"),
```

New text:

```
        (True, "it was measured in another checkout"),
```

### `u271-measured.D7_interpreter_unchecked`

read_battery_verdict: drop the interpreter key

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D7_interpreter_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-interpreter]`

Old text:

```
        (record.get("python") == sys.executable, "it was measured with another interpreter"),
```

New text:

```
        (True, "it was measured with another interpreter"),
```

### `u271-measured.D8_known_file_unchecked`

read_battery_verdict: drop the known failures file's digest key

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D8_known_file_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-known-failures-file]`

Old text:

```
            record.get("known_failures_sha256") == known_digest,
```

New text:

```
            True,
```

### `u271-measured.D9_interrupted_run_read`

read_battery_verdict: accept pytest's exit 2, an interrupted run

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D9_interrupted_run_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[an-interrupted-run]`

Old text:

```
record["exit_code"] in {0, 1},
```

New text:

```
record["exit_code"] in {0, 1, 2},
```

### `u273.D1_driver_placeless_read`

read_known_failures: read a known failures file that names no place

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D1_driver_placeless_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_known_failures_naming_no_place_are_refused_with_the_command[before-u273]`
  - `tests/test_mutation_driver.py::test_known_failures_naming_no_place_are_refused_with_the_command[no-field]`
  - `tests/test_mutation_driver.py::test_known_failures_naming_no_place_are_refused_with_the_command[no-place]`
  - `tests/test_mutation_driver.py::test_known_failures_naming_no_place_are_refused_with_the_command[not-a-place]`

Old text:

```
    if place not in BATTERY.PLACES:
        raise DriverRefusal(
```

New text:

```
    if False:
        raise DriverRefusal(
```

### `u273.D2_driver_tmpdir_inherited`

run_pytest: do not point the child's TMPDIR at the known failures' place

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D2_driver_tmpdir_inherited`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_batch_in_memory_reads_the_listed_test_on_disk_and_says_so`
  - `tests/test_mutation_driver.py::test_a_child_runs_in_the_known_failures_place_and_the_listed_test_again_on_disk`
  - `tests/test_mutation_driver.py::test_a_listed_test_erroring_in_memory_and_passing_on_disk_is_read_passing`
  - `tests/test_mutation_driver.py::test_a_run_on_disk_runs_once_and_one_with_no_place_inherits_the_temporary_directory`

Old text:

```
            env["TMPDIR"] = str(temp)

```

New text:

```
(empty)
```

### `u273.D3_driver_no_rerun`

run_pytest: never run the listed tests again on disk after a run in memory

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D3_driver_no_rerun`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_batch_in_memory_reads_the_listed_test_on_disk_and_says_so`
  - `tests/test_mutation_driver.py::test_a_child_runs_in_the_known_failures_place_and_the_listed_test_again_on_disk`
  - `tests/test_mutation_driver.py::test_a_child_whose_place_is_gone_is_refused_rather_than_run_elsewhere`
  - `tests/test_mutation_driver.py::test_a_listed_test_erroring_in_memory_and_passing_on_disk_is_read_passing`

Old text:

```
    rerun = [one for one in on_disk if runs_node(one, paths)] if place == BATTERY.MEMORY else []
```

New text:

```
    rerun = []
```

### `u273.D4_driver_reruns_every_subset`

runs_node: read every listed test as collected by any subset

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D4_driver_reruns_every_subset`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_listed_test_is_rerun_only_by_a_run_that_collects_it[tests/a.py::t-paths7-False]`
  - `tests/test_mutation_driver.py::test_a_listed_test_is_rerun_only_by_a_run_that_collects_it[tests/a.py::tt-paths9-False]`
  - `tests/test_mutation_driver.py::test_a_listed_test_is_rerun_only_by_a_run_that_collects_it[tests/ab.py::t-paths8-False]`
  - `tests/test_mutation_driver.py::test_a_subset_that_does_not_collect_the_listed_test_runs_nothing_on_disk`

Old text:

```
    if not paths:
        return True
    for path in paths:
```

New text:

```
    if True:
        return True
    for path in paths:
```

### `u273.D5_driver_place_unchecked_upfront`

main: skip the refusal of a place this machine cannot give before the batch starts

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D5_driver_place_unchecked_upfront`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_disk_the_rerun_cannot_have_is_refused_before_anything_runs`
  - `tests/test_mutation_driver.py::test_a_place_this_machine_cannot_give_is_refused_before_anything_runs`

Old text:

```
            refuse_a_place_this_machine_cannot_give(known)
        except DriverRefusal as refusal:
```

New text:

```
            pass
        except DriverRefusal as refusal:
```

### `u273.D6_driver_errored_kept`

run_pytest: keep a listed test's memory error beside its disk outcome

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D6_driver_errored_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_listed_test_erroring_in_memory_and_passing_on_disk_is_read_passing`

Old text:

```
        errored = tuple(i for i in errored if i not in rerun) + again.errored
```

New text:

```
        errored = errored + again.errored
```

### `u273.D7_driver_lost_place_runs_elsewhere`

run_pytest: drop the refusal of a place lost after main's check, so the child runs in the inherited temporary directory

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D7_driver_lost_place_runs_elsewhere`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_whose_place_is_gone_is_refused_rather_than_run_elsewhere`

Old text:

```
        root, why = BATTERY.place_root(place)
        if root is None:
            raise DriverRefusal(
```

New text:

```
        root, why = BATTERY.place_root(place)
        if False:
            raise DriverRefusal(
```

### `u273.D8_driver_disk_needed_without_rerun`

refuse_a_place_this_machine_cannot_give: require the disk for every memory file, even one with nothing to run on disk

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D8_driver_disk_needed_without_rerun`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_disk_the_rerun_cannot_have_is_refused_before_anything_runs`

Old text:

```
    if known.place == BATTERY.MEMORY and known.on_disk:
```

New text:

```
    if known.place == BATTERY.MEMORY:
```

### `u297.D1_replay_row_without_a_source`

load_spec: accept a replay row that names no source, so an uncapped pass takes rows no table recorded

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D1_replay_row_without_a_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_replay_row_that_names_no_source_is_refused`

Old text:

```
            if source is None:
                raise DriverRefusal(
                    f"row {row_id}: a replay row names where it came from and this one "
```

New text:

```
            if False:
                raise DriverRefusal(
                    f"row {row_id}: a replay row names where it came from and this one "
```

### `u297.D2_cap_lifted_for_every_pass`

load_spec: read the cap as the row count for every pass kind, so a light pass of 26 rows and a full pass of 46 load

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D2_cap_lifted_for_every_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_full_pass_of_46_rows_is_still_refused`
  - `tests/test_mutation_driver.py::test_a_light_pass_of_26_rows_is_still_refused_whatever_they_name`
  - `tests/test_mutation_driver.py::test_exceeding_the_pass_cap_is_refused_and_names_the_log`

Old text:

```
    cap = ROW_CAPS.get(pass_kind, len(rows))
```

New text:

```
    cap = len(rows)
```

### `u297.D3_mapped_to_no_row`

load_mapped: accept a mapping whose target is no row in the batch, so a lost kill is covered by nothing

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D3_mapped_to_no_row`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_mapping_nothing_stands_behind_is_refused[entry1-it maps to 'u1.G7', which is no row in this batch]`

Old text:

```
        if target not in ids:
```

New text:

```
        if False:
```

### `u297.D4_a_measured_row_loses_its_source`

measure_row: stop carrying a replay row's source and moved reason into its result, so check has nothing to match the row by

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D4_a_measured_row_loses_its_source`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`, `tests/test_killset.py`
- Collected: 249 against a baseline of 249
- Kills: 2 (killed)
- Killed:
  - `tests/test_killset.py::test_recorded_kills_replay_through_the_driver_and_check_clean`
  - `tests/test_mutation_driver.py::test_a_replay_batch_spends_one_baseline_and_one_control_and_carries_its_sources`

Old text:

```
        head_verified=head_verify,
        **replay_fields(row),
    )
```

New text:

```
        head_verified=head_verify,
    )
```

### `u297.D5_a_replay_resumed_from_anywhere`

measure_batch: let a replay reuse rows from any sidecar, another commit's or one measured before a tracked file changed

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D5_a_replay_resumed_from_anywhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_replay_reuses_nothing_from_a_sidecar_measured_at_another_commit`
  - `tests/test_mutation_driver.py::test_a_replay_reuses_nothing_while_a_tracked_file_differs_from_the_commit`
  - `tests/test_mutation_driver.py::test_resuming_a_replay_from_another_commits_sidecar_says_nothing_is_reused`

Old text:

```
    stale = pass_kind == REPLAY and bool(replay_resume_refusal(repo_root, prior))
```

New text:

```
    stale = False
```

### `u297.D6_sources_taken_on_trust`

main: skip the reading of each replay row's source against the table it names, so new rows ride past the caps under a table's name

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D6_sources_taken_on_trust`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_the_command_checks_the_sources_and_hands_the_mappings_to_the_table`

Old text:

```
        if pass_kind == REPLAY:
            refuse_unrecorded_sources(args.repo_root, rows, mapped)
```

New text:

```
        if False:
            refuse_unrecorded_sources(args.repo_root, rows, mapped)
```

### `u296.M10_type_checking_reads_as_running`

Tree._read_file: read an import under TYPE_CHECKING as one that runs, so a typing only import fails rule three

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M10_type_checking_reads_as_running`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 4 (killed)
- Killed:
  - `tests/test_import_rules.py::test_an_import_under_type_checking_is_never_loaded_for_a_verb`
  - `tests/test_import_rules.py::test_an_import_under_type_checking_never_runs_and_passes`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_type_checking_spelled_through_its_module_is_read_the_same`

Old text:

```
            typing_only = inside(node.lineno, typing_blocks)
```

New text:

```
            typing_only = False
```

### `u296.M11_builder_imports_unread`

dangling: do not read the imports written in a verb's builder, so intake.set's shape builds on paper and dangles in fact

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M11_builder_imports_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_home_imported_directly_in_the_builder_dangles_the_verb`
  - `tests/test_import_rules.py::test_an_import_written_in_the_builder_runs_when_the_verb_builds_and_dangles`

Old text:

```
            built = tree.function_loads(verb.module, verb.builder)
```

New text:

```
            built = frozenset()
```

### `u296.M12_followed_through_a_blocked_module`

Tree.loaded_from: follow imports through a module that cannot be imported, so an import nothing reaches is named as a cause

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M12_followed_through_a_blocked_module`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`

Old text:

```
                if module in seen or within(module, blocked):
```

New text:

```
                if module in seen:
```

### `u296.M13_own_verbs_dangle`

dangling: count the switched off toggle's own verbs, so every gated verb reads as dangling

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M13_own_verbs_dangle`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 5 (killed)
- Killed:
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_the_toggles_own_verbs_are_off_and_so_never_dangle`
  - `tests/test_refactor_measure.py::test_imports_prints_the_seam_counts`
  - `tests/test_refactor_measure.py::test_table_fails_when_something_stands_beyond_an_allowance`
  - `tests/test_refactor_measure.py::test_table_prints_points_two_to_five_and_is_clean_on_a_full_allowance`

Old text:

```
            if verb.toggle == toggle:
                continue
```

New text:

```
            if verb.toggle == "":
                continue
```

### `u296.M14_core_names_everywhere`

core_names: count the names core, write and the shell use too, so the ceiling measures something else

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M14_core_names_everywhere`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_import_rules.py::test_core_names_are_counted_across_feature_packages_and_only_there`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`

Old text:

```
    out: dict[str, set[str]] = collections.defaultdict(set)
    for path, uses in tree.uses.items():
        importer = package_of_path(path)
        if importer in LOWER_PACKAGES:
            continue
        for use in uses:
            if use.name is not None and (use.target == core or use.target.startswith(core + ".")):
```

New text:

```
    out: dict[str, set[str]] = collections.defaultdict(set)
    for path, uses in tree.uses.items():
        importer = package_of_path(path)
        for use in uses:
            if use.name is not None and (use.target == core or use.target.startswith(core + ".")):
```

### `u296.M15_shadowed_alias_counts`

Tree.uses: count a name reached through a module whether or not the module defines it, so a local variable named as an imported module is reads as a use

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M15_shadowed_alias_counts`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_local_variable_named_as_an_imported_module_is_not_a_use_of_it`

Old text:

```
                or use.name in defined[use.target]
```

New text:

```
                or use.name is not None
```

### `u296.M16_prune_adds_lines`

pruned: keep what is found or allowed, so prune writes newly found lines into an allowance

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M16_prune_adds_lines`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`, `tests/test_refactor_measure.py`
- Collected: 58 against a baseline of 58
- Kills: 5 (killed)
- Killed:
  - `tests/test_duplication.py::test_pruning_keeps_what_is_still_found_and_can_never_add_a_line`
  - `tests/test_refactor_measure.py::test_prune_never_adds_a_line_for_something_newly_found`
  - `tests/test_refactor_measure.py::test_prune_removes_what_is_gone_keeps_the_header_and_touches_no_other_package`
  - `tests/test_refactor_measure.py::test_prune_still_lowers_the_file_of_a_package_that_left_the_tree`
  - `tests/test_refactor_measure.py::test_table_fails_when_something_stands_beyond_an_allowance`

Old text:

```
    return found & allowed
```

New text:

```
    return found | allowed
```

### `u296.M18_vendored_tree_read`

python_files: read the vendored tree, which is never refactored and never measured

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M18_vendored_tree_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`, `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 103 against a baseline of 103
- Kills: 8 (killed)
- Killed:
  - `tests/test_duplication.py::test_no_package_holds_a_copied_block_beyond_its_allowance`
  - `tests/test_refactor_measure.py::test_duplicates_prints_blocks_lines_files_and_window_places`
  - `tests/test_refactor_measure.py::test_duplicates_takes_the_block_size_and_lists_the_longest_first`
  - `tests/test_refactor_measure.py::test_in_a_checkout_the_files_are_the_ones_git_tracks_or_would`
  - `tests/test_refactor_measure.py::test_lines_prints_each_package_the_total_and_the_large_files`
  - `tests/test_refactor_measure.py::test_table_prints_points_two_to_five_and_is_clean_on_a_full_allowance`
  - `tests/test_refactor_measure.py::test_the_renamed_reading_is_printed_only_when_asked_and_matches_changed_names`
  - `tests/test_refactor_measure.py::test_the_vendored_tree_is_never_read`

Old text:

```
        and f"/{VENDOR}/" not in f"/{path}"
```

New text:

```
        and f"/{VENDOR}x/" not in f"/{path}"
```

### `u296.M1_block_size`

BLOCK_LINES: a block needs seven logical lines, so a new copy of exactly six passes the duplication check

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M1_block_size`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`, `tests/test_refactor_measure.py`
- Collected: 58 against a baseline of 58
- Kills: 16 (killed)
- Killed:
  - `tests/test_duplication.py::test_a_block_on_the_allowance_passes_and_a_new_one_beside_it_fails`
  - `tests/test_duplication.py::test_a_copy_inside_one_file_is_found`
  - `tests/test_duplication.py::test_a_copy_of_six_lines_is_found_in_both_packages`
  - `tests/test_duplication.py::test_a_copy_that_was_only_reindented_recommented_and_rewrapped_is_still_found`
  - `tests/test_duplication.py::test_a_deletion_that_brings_two_stretches_together_is_a_new_copy`
  - `tests/test_duplication.py::test_a_longer_copy_is_its_run_of_windows`
  - `tests/test_duplication.py::test_a_third_copy_of_an_allowed_block_in_the_same_package_fails`
  - `tests/test_duplication.py::test_a_window_is_described_by_where_it_stands`
  - `tests/test_duplication.py::test_an_allowance_is_its_own_packages_and_excuses_no_other`
  - `tests/test_duplication.py::test_no_package_holds_a_copied_block_beyond_its_allowance`
  - `tests/test_duplication.py::test_overlapping_windows_in_one_file_are_two_places`
  - `tests/test_duplication.py::test_the_block_size_is_six_logical_lines`
  - `tests/test_refactor_measure.py::test_duplicates_prints_blocks_lines_files_and_window_places`
  - `tests/test_refactor_measure.py::test_prune_removes_what_is_gone_keeps_the_header_and_touches_no_other_package`
  - `tests/test_refactor_measure.py::test_table_prints_points_two_to_five_and_is_clean_on_a_full_allowance`
  - ... and 1 more, see the JSON sidecar

Old text:

```
BLOCK_LINES = 6
```

New text:

```
BLOCK_LINES = 7
```

### `u296.M22_initializer_relative_import`

Tree._base_of: resolve a relative import in a package initializer as in any other module, one package too high, so a crossing written there is read against the wrong module (the review's row 7)

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M22_initializer_relative_import`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_relative_import_in_a_package_initializer_starts_from_that_package`

Old text:

```
        if not path.endswith("/__init__.py"):
            parts = parts[:-1]
```

New text:

```
        parts = parts[:-1]
```

### `u296.M23_except_branch_names_unread`

_defined_names: do not read the names bound in except branches, so a name defined there is taken for a local variable's attribute and dropped (the review's row 7)

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M23_except_branch_names_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_name_bound_in_an_except_branch_is_a_name_the_module_defines`

Old text:

```
            pending.extend(
                inner for handler in getattr(node, "handlers", ()) for inner in handler.body
            )
```

New text:

```
            pass
```

### `u296.M24_builder_names_a_home_directly`

dangling: forget the homes a builder imports directly, so only what its other imports reach can dangle the verb (the review's row 7)

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M24_builder_names_a_home_directly`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_home_imported_directly_in_the_builder_dangles_the_verb`

Old text:

```
            crossing = {(verb.module, target) for target in built if within(target, owned)}
```

New text:

```
            crossing = set()
```

### `u296.M25_dotted_import_alias`

Tree._read_file: bind an import under another name to the root package, so a private name reached through it passes (the review's row 7)

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M25_dotted_import_alias`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_dotted_import_under_another_name_is_followed_to_its_module`

Old text:

```
                    aliases[alias.asname or top] = alias.name if alias.asname else top
```

New text:

```
                    aliases[alias.asname or top] = top
```

### `u296.M26_core_package_name`

core_names: count names of core's modules only, so a name imported from the core package itself is not a core name (the review's row 7)

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M26_core_package_name`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_name_imported_from_the_core_package_itself_is_a_core_name`

Old text:

```
            if use.name is not None and (use.target == core or use.target.startswith(core + ".")):
                out[importer].add(use.dotted)
```

New text:

```
            if use.name is not None and use.target.startswith(core + "."):
                out[importer].add(use.dotted)
```

### `u296.M2_imports_count_as_lines`

logical_lines: stop dropping import statements, so two module headers read as a copied block

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M2_imports_count_as_lines`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`, `tests/test_refactor_measure.py`
- Collected: 58 against a baseline of 58
- Kills: 3 (killed)
- Killed:
  - `tests/test_duplication.py::test_comments_blank_lines_docstrings_and_imports_are_not_logical_lines`
  - `tests/test_duplication.py::test_imports_do_not_count_toward_the_six_lines`
  - `tests/test_duplication.py::test_no_package_holds_a_copied_block_beyond_its_allowance`

Old text:

```
                an_import = first.type == tokenize.NAME and first.string in ("import", "from")
```

New text:

```
                an_import = False
```

### `u296.M3_allowance_forgets_places`

over_allowance: compare which lines are held and not how many places hold each, so a third copy of an allowed block passes

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M3_allowance_forgets_places`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`, `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_duplication.py::test_a_third_copy_of_an_allowed_block_in_the_same_package_fails`

Old text:

```
        excess = counts - allowed.get(package, collections.Counter())
```

New text:

```
        excess = collections.Counter(set(counts) - set(allowed.get(package, ())))
```

### `u296.M4_allowance_shared_between_packages`

over_allowance: read every package against one merged allowance, so a block allowed in one package is allowed in all

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M4_allowance_shared_between_packages`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`, `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_duplication.py::test_an_allowance_is_its_own_packages_and_excuses_no_other`

Old text:

```
    for package, counts in found.items():
        excess = counts - allowed.get(package, collections.Counter())
```

New text:

```
    for package, counts in found.items():
        excess = counts - sum(allowed.values(), collections.Counter())
```

### `u296.M5_private_inside_its_package`

private_crossings: drop the comparison of packages, so a private name used inside its own package is a crossing

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M5_private_inside_its_package`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 3 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_relative_import_in_a_package_initializer_starts_from_that_package`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_the_same_private_import_inside_its_own_package_passes`

Old text:

```
            if private and tree.package(use.target) != importer:
```

New text:

```
            if private:
```

### `u296.M6_private_through_a_module`

private_crossings: read the private rule off import statements only, so a private name reached through an imported module passes

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M6_private_through_a_module`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_dotted_import_under_another_name_is_followed_to_its_module`
  - `tests/test_import_rules.py::test_a_private_name_reached_through_an_imported_module_fails`

Old text:

```
        for use in uses:
            parts = use.target.split(".")[1:]
            if VENDOR in parts:
```

New text:

```
        for use in uses:
            parts = use.target.split(".")[1:]
            if VENDOR in parts or use.kind != "import":
```

### `u296.M7_interface_binds_the_lower_layers`

core_modules_reached: stop exempting core, write and the shell, so the interface list binds packages it was never for

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M7_interface_binds_the_lower_layers`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_the_same_import_passes_from_core_write_and_the_shell`

Old text:

```
    core = f"{tree.root_package}.core"
    for path, uses in tree.uses.items():
        importer = package_of_path(path)
        if importer in LOWER_PACKAGES:
            continue
        for use in uses:
            if use.target.startswith(core + "."):
```

New text:

```
    core = f"{tree.root_package}.core"
    for path, uses in tree.uses.items():
        importer = package_of_path(path)
        for use in uses:
            if use.target.startswith(core + "."):
```

### `u296.M8_interface_list_ignored`

off_interface: treat every core module as off the list, so the named interface allows nothing

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M8_interface_list_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 6 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_core_module_off_the_list_fails_from_a_feature_package`
  - `tests/test_import_rules.py::test_a_module_on_the_list_passes_from_a_feature_package`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_refactor_measure.py::test_imports_prints_the_seam_counts`
  - `tests/test_refactor_measure.py::test_table_fails_when_something_stands_beyond_an_allowance`
  - `tests/test_refactor_measure.py::test_table_prints_points_two_to_five_and_is_clean_on_a_full_allowance`

Old text:

```
        if module in named:
            continue
```

New text:

```
        if module in ():
            continue
```

### `u296.M9_lazy_reads_as_top_level`

Tree._read_file: read every import as top level, so an import under a function fails rule three and dangles a verb

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M9_lazy_reads_as_top_level`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 80 against a baseline of 80
- Kills: 4 (killed)
- Killed:
  - `tests/test_import_rules.py::test_an_import_under_a_function_does_not_dangle_a_verb`
  - `tests/test_import_rules.py::test_an_import_written_in_the_builder_runs_when_the_verb_builds_and_dangles`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_the_same_import_under_a_function_passes`

Old text:

```
            lazy = inside(node.lineno, functions)
```

New text:

```
            lazy = False
```

### `u159.M1_off_main_cut`

refusals: drop the refusal off main, so a release is cut from a branch

- File: `scripts/release.py`
- Source: `u159.json`, row `M1_off_main_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_cut_refuses_off_main`

Old text:

```
    if branch != "main":
```

New text:

```
    if False:
```

### `u159.M2_dirty_tree_cut`

refusals: drop the clean tree refusal, so uncommitted work rides into a release

- File: `scripts/release.py`
- Source: `u159.json`, row `M2_dirty_tree_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_cut_refuses_on_a_dirty_tree`

Old text:

```
    if git(runner, "status", "--porcelain"):
```

New text:

```
    if False:
```

### `u159.M3_behind_origin_cut`

refusals: drop the origin/main equality, so a stale or unpushed main is released

- File: `scripts/release.py`
- Source: `u159.json`, row `M3_behind_origin_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_release.py::test_cut_refuses_ahead_of_origin_main`
  - `tests/test_release.py::test_cut_refuses_behind_origin_main`

Old text:

```
    elif remote.stdout.strip() != head:
```

New text:

```
    elif False:
```

### `u159.M4_red_battery_cut`

verdict_problem: accept a red verdict

- File: `scripts/release.py`
- Source: `u159.json`, row `M4_red_battery_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_release.py::test_cut_refuses_on_a_red_battery[dirty]`
  - `tests/test_release.py::test_cut_refuses_on_a_red_battery[red]`

Old text:

```
    if fields[1] != "clean":
```

New text:

```
    if False:
```

### `u159.M5_other_commit_verdict`

verdict_problem: accept a verdict measured on another commit

- File: `scripts/release.py`
- Source: `u159.json`, row `M5_other_commit_verdict`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_cut_refuses_without_a_verdict_or_with_another_commit_s`

Old text:

```
    if len(fields) < 2 or fields[0] != head:
```

New text:

```
    if len(fields) < 2:
```

### `u159.M7_unit_is_patch`

classify: a unit asks for a patch, so new behaviour ships as a repair

- File: `scripts/release.py`
- Source: `u159.json`, row `M7_unit_is_patch`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 6 (killed)
- Killed:
  - `tests/test_release.py::test_plan_reruns_a_past_range_and_prints_its_notes`
  - `tests/test_release.py::test_the_bump_a_title_asks_for[U158: a unit reaches main through a pull request-minor]`
  - `tests/test_release.py::test_the_bump_a_title_asks_for[merge(u57): the converge verb-minor]`
  - `tests/test_release.py::test_the_bump_a_title_asks_for[merge(u99-b): label registry verbs-minor]`
  - `tests/test_release.py::test_the_bump_over_a_minor_unit_behind_a_local_merge_is_minor`
  - `tests/test_release.py::test_the_proposal_is_the_largest_bump_with_a_reason_per_landing`

Old text:

```
        return "minor", "a unit, new verbs or behaviour"
```

New text:

```
        return "patch", "a unit, new verbs or behaviour"
```

### `u215.M10_main_sync_re_bare`

MAIN_SYNC_RE: drop the bare Merge origin/main alternative

- File: `scripts/release.py`
- Source: `u215.json`, row `M10_main_sync_re_bare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_a_local_merge_of_main_is_never_a_landing[Merge origin/main]`

Old text:

```
    r"|(?:[\w.-]+/)?main)(?: into main)?$"
```

New text:

```
    r")(?: into main)?$"
```

### `u215.M11_version_at_since`

cmd_plan: read the base version from the checkout, not from --since, round one's second BLOCKING finding

- File: `scripts/release.py`
- Source: `u215.json`, row `M11_version_at_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_plan_reads_the_bump_from_the_version_the_range_starts_at`

Old text:

```
        current = version_at(runner, asked_since)

```

New text:

```
        current = read_versions(ROOT)[0]

```

### `u215.M12_crossed_tag`

cmd_plan: drop the refusal of a range crossing a version tag

- File: `scripts/release.py`
- Source: `u215.json`, row `M12_crossed_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 3 (killed)
- Killed:
  - `tests/test_release.py::test_plan_reads_the_bump_from_the_version_the_range_starts_at`
  - `tests/test_release.py::test_plan_refuses_a_range_that_crosses_a_version_tag`
  - `tests/test_release.py::test_plan_refuses_a_reversed_range`

Old text:

```
        tip_tag = refuse_a_crossed_tag(runner, asked_since, tip)

```

New text:

```
        tip_tag = None

```

### `u215.M13_crossed_tag_tip_excluded`

refuse_a_crossed_tag: count the tag at the tip as crossed, so every rerun of a past release is refused

- File: `scripts/release.py`
- Source: `u215.json`, row `M13_crossed_tag_tip_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_release.py::test_plan_reads_the_bump_from_the_version_the_range_starts_at`
  - `tests/test_release.py::test_plan_reruns_a_past_range_and_prints_its_notes`

Old text:

```
        if git(runner, "rev-parse", f"{name}^{{commit}}") != tip_sha:

```

New text:

```
        if True:

```

### `u215.M14_tip_needs_since`

cmd_plan: drop the refusal of --tip without --since

- File: `scripts/release.py`
- Source: `u215.json`, row `M14_tip_needs_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_plan_refuses_a_tip_without_a_start_and_a_ref_that_names_nothing`

Old text:

```
    if tip and not asked_since:

```

New text:

```
    if False:

```

### `u215.M15_ref_names_a_commit`

gather: drop the check that --since and --tip name commits

- File: `scripts/release.py`
- Source: `u215.json`, row `M15_ref_names_a_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_plan_refuses_a_tip_without_a_start_and_a_ref_that_names_nothing`

Old text:

```
        if found.returncode != 0:
            raise ReleaseError(f"{ref!r} names no commit here
```

New text:

```
        if False:
            raise ReleaseError(f"{ref!r} names no commit here
```

### `u215.M16_notes_empty_range`

cmd_plan: print notes over an empty range instead of refusing

- File: `scripts/release.py`
- Source: `u215.json`, row `M16_notes_empty_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_plan_notes_over_an_empty_range_print_nothing_and_fail`

Old text:

```
    if getattr(args, "notes", False):
        if bump is None:

```

New text:

```
    if getattr(args, "notes", False):
        if False:

```

### `u215.M18_reversed_range`

refuse_a_crossed_tag: drop the refusal of a --since that is not behind --tip, so a reversed range reads as empty

- File: `scripts/release.py`
- Source: `u215.json`, row `M18_reversed_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_plan_refuses_a_reversed_range`

Old text:

```
    if runner(["git", "merge-base", "--is-ancestor", since, tip]).returncode != 0:

```

New text:

```
    if False:

```

### `u215.M19_claim_filter_lands`

landings_since: claim only landing subject takers, so a second merge on the line under GitHub's default subject is listed again

- File: `scripts/release.py`
- Source: `u215.json`, row `M19_claim_filter_lands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_a_pull_request_merged_twice_under_github_s_default_subject_is_listed_once`

Old text:

```
        claimed.update(sha for sha in taking if lands(sha))

```

New text:

```
        claimed.update(sha for sha in taking if LANDING_RE.match(by_sha[sha][0]))

```

### `u215.M1_whole_range`

landings_since: walk only the first parent line, the defect U215 repairs

- File: `scripts/release.py`
- Source: `u215.json`, row `M1_whole_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 9 (killed)
- Killed:
  - `tests/test_release.py::test_a_pull_request_merged_through_the_api_off_the_first_parent_line_is_listed`
  - `tests/test_release.py::test_a_pull_request_merged_twice_under_github_s_default_subject_is_listed_once`
  - `tests/test_release.py::test_a_residual_merge_behind_a_local_merge_of_main_is_listed`
  - `tests/test_release.py::test_a_unit_merged_both_locally_and_through_its_pull_request_is_listed_once`
  - `tests/test_release.py::test_a_unit_reachable_through_its_head_and_its_merge_is_listed_once`
  - `tests/test_release.py::test_plan_reruns_a_past_range_and_prints_its_notes`
  - `tests/test_release.py::test_the_bump_over_a_minor_unit_behind_a_local_merge_is_minor`
  - `tests/test_release.py::test_the_notes_list_exactly_the_pull_requests_since_the_last_tag`
  - `tests/test_release.py::test_two_unit_merges_behind_a_local_merge_of_main_are_both_listed`

Old text:

```
    commits = range_commits(runner, since, tip)

```

New text:

```
    commits = range_commits(runner, since, tip, first_parent=True)

```

### `u215.M2_main_sync_never_lands`

lands: drop the refusal of a merge of main into a local main, so a local pull is listed as a landing

- File: `scripts/release.py`
- Source: `u215.json`, row `M2_main_sync_never_lands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 10 (killed)
- Killed:
  - `tests/test_release.py::test_a_local_merge_of_main_is_never_a_landing[Merge branch 'main' of github.com:philgutowski/cratekit]`
  - `tests/test_release.py::test_a_local_merge_of_main_is_never_a_landing[Merge branch 'main' of https://github.com/philgutowski/cratekit]`
  - `tests/test_release.py::test_a_local_merge_of_main_is_never_a_landing[Merge origin/main]`
  - `tests/test_release.py::test_a_local_merge_of_main_is_never_a_landing[Merge remote-tracking branch 'origin/main']`
  - `tests/test_release.py::test_a_pull_request_merged_through_the_api_off_the_first_parent_line_is_listed`
  - `tests/test_release.py::test_a_pull_request_merged_twice_under_github_s_default_subject_is_listed_once`
  - `tests/test_release.py::test_a_residual_merge_behind_a_local_merge_of_main_is_listed`
  - `tests/test_release.py::test_a_unit_merged_both_locally_and_through_its_pull_request_is_listed_once`
  - `tests/test_release.py::test_a_unit_reachable_through_its_head_and_its_merge_is_listed_once`
  - `tests/test_release.py::test_two_unit_merges_behind_a_local_merge_of_main_are_both_listed`

Old text:

```
        if MAIN_SYNC_RE.match(subject):
            return False

```

New text:

```
        if False:
            return False

```

### `u215.M3_off_line_landing_subject`

lands: list only first parent merges, so a unit merge behind a local pull is dropped

- File: `scripts/release.py`
- Source: `u215.json`, row `M3_off_line_landing_subject`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 5 (killed)
- Killed:
  - `tests/test_release.py::test_a_residual_merge_behind_a_local_merge_of_main_is_listed`
  - `tests/test_release.py::test_a_unit_reachable_through_its_head_and_its_merge_is_listed_once`
  - `tests/test_release.py::test_plan_reruns_a_past_range_and_prints_its_notes`
  - `tests/test_release.py::test_the_bump_over_a_minor_unit_behind_a_local_merge_is_minor`
  - `tests/test_release.py::test_two_unit_merges_behind_a_local_merge_of_main_are_both_listed`

Old text:

```
        return sha in first_line or bool(LANDING_RE.match(subject))

```

New text:

```
        return sha in first_line

```

### `u215.M4_off_line_any_merge`

lands: list every off line merge, so branch syncs are counted as landings

- File: `scripts/release.py`
- Source: `u215.json`, row `M4_off_line_any_merge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_release.py::test_a_range_with_no_local_merge_lists_what_the_first_parent_line_lists`
  - `tests/test_release.py::test_a_unit_shipped_in_the_last_tag_is_not_listed_again_through_a_sibling_sync`

Old text:

```
        return sha in first_line or bool(LANDING_RE.match(subject))

```

New text:

```
        return True

```

### `u215.M5_head_in_range`

landings_since: consult the head's takers whether or not the head is in the range, round one's first BLOCKING finding

- File: `scripts/release.py`
- Source: `u215.json`, row `M5_head_in_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_a_unit_shipped_in_the_last_tag_is_not_listed_again_through_a_sibling_sync`

Old text:

```
            if head_sha in by_sha
            else []

```

New text:

```
            if True
            else []

```

### `u215.M6_landing_taker_first`

landings_since: invert the taker preference, so a branch sync is chosen over the landing merge

- File: `scripts/release.py`
- Source: `u215.json`, row `M6_landing_taker_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_a_unit_reachable_through_its_head_and_its_merge_is_listed_once`

Old text:

```
                key=lambda sha: (not lands(sha), order[sha]),

```

New text:

```
                key=lambda sha: (lands(sha), order[sha]),

```

### `u215.M7_claim_every_landing_taker`

landings_since: claim only the commit a pull request landed at, so a local merge of the same head is listed again

- File: `scripts/release.py`
- Source: `u215.json`, row `M7_claim_every_landing_taker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_release.py::test_a_pull_request_merged_twice_under_github_s_default_subject_is_listed_once`
  - `tests/test_release.py::test_a_unit_merged_both_locally_and_through_its_pull_request_is_listed_once`

Old text:

```
        claimed.update(sha for sha in taking if lands(sha))

```

New text:

```
        claimed.update(())

```

### `u215.M8_fast_forward_head`

landings_since: drop the fast forward fallback, so a pull request fast forwarded onto main is unlisted

- File: `scripts/release.py`
- Source: `u215.json`, row `M8_fast_forward_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_a_pull_request_fast_forwarded_onto_main_lands_at_its_head`

Old text:

```
        elif head_sha in by_sha:
            landed_at = head_sha

```

New text:

```
        elif False:
            landed_at = head_sha

```

### `u215.M9_landing_re_residual`

LANDING_RE: drop the residual alternation, so merge(r-N) behind a local pull is dropped

- File: `scripts/release.py`
- Source: `u215.json`, row `M9_landing_re_residual`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_a_residual_merge_behind_a_local_merge_of_main_is_listed`

Old text:

```
LANDING_RE = re.compile(r"^merge\((?:u\d+|r-?\d+)[a-z0-9-]*\):", re.IGNORECASE)
```

New text:

```
LANDING_RE = re.compile(r"^merge\((?:u\d+)[a-z0-9-]*\):", re.IGNORECASE)
```

### `u124.S1_head_fixed`

the scan stops comparing RESTART's head to the fixed reader's line

- File: `scripts/scan_repo.py`
- Source: `u124.json`, row `S1_head_fixed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_portability.py`
- Collected: 138 against a baseline of 138
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-head0]`
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-head1]`

Old text:

```
    if head != RESTART_HEAD:
```

New text:

```
    if head != RESTART_HEAD and False:
```

### `u124.S2_sections`

the scan accepts any section heading

- File: `scripts/scan_repo.py`
- Source: `u124.json`, row `S2_sections`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_portability.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-U999]`

Old text:

```
        if heading not in RESTART_SECTIONS:
```

New text:

```
        if heading not in RESTART_SECTIONS and False:
```

### `u124.S3_record_opener`

the record opener narrowed back to units and residuals marked built or done, so a sitting passes

- File: `scripts/scan_repo.py`
- Source: `u124.json`, row `S3_record_opener`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_portability.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-opens a unit's record1]`

Old text:

```
_UNIT_RECORD = re.compile(r"^\*\*(?:U\d+|R-\d+|A\d+|Sitting \d+)\b", re.M)
```

New text:

```
_UNIT_RECORD = re.compile(r"^\*\*(?:U\d+|R-\d+)(?: with R-\d+)? (?:built|done)\b", re.M)
```

### `u124.S4_wired`

scan_tree stops calling restart_violations

- File: `scripts/scan_repo.py`
- Source: `u124.json`, row `S4_wired`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_portability.py`
- Collected: 138 against a baseline of 138
- Kills: 5 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-U999]`
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-head0]`
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-head1]`
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-opens a unit's record0]`
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-opens a unit's record1]`

Old text:

```
        findings += [f"{relative}: {p}" for p in restart_violations(relative, text)]

```

New text:

```
(empty)
```

### `u124.S5_only_restart`

the restart rule judges every file, so a fragment is refused

- File: `scripts/scan_repo.py`
- Source: `u124.json`, row `S5_only_restart`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_portability.py`
- Collected: 138 against a baseline of 138
- Kills: 8 (killed)
- Killed:
  - `tests/test_portability.py::test_a_relative_symlink_inside_the_repository_is_allowed`
  - `tests/test_portability.py::test_the_archive_rule_stays_quiet_on_what_is_not_an_archive[ar-prose]`
  - `tests/test_portability.py::test_the_archive_rule_stays_quiet_on_what_is_not_an_archive[bzh-prose]`
  - `tests/test_portability.py::test_the_archive_rule_stays_quiet_on_what_is_not_an_archive[cpio-prose]`
  - `tests/test_portability.py::test_the_archive_rule_stays_quiet_on_what_is_not_an_archive[empty]`
  - `tests/test_portability.py::test_the_archive_rule_stays_quiet_on_what_is_not_an_archive[pk-prose]`
  - `tests/test_portability.py::test_the_repository_itself_is_clean`
  - `tests/test_restart_and_residual_files.py::test_the_scan_judges_no_other_file_by_the_restart_rule`

Old text:

```
    if relative_path != RESTART_FILE:
        return []
```

New text:

```
    if relative_path == "":
        return []
```

### `u257.M10_no_value_check`

_keyword_gate_passes: skip the value check at the separator, exact but more texts handed to the alternations

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M10_no_value_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_scan_secret_equality.py::test_the_keyword_gate_hands_over_almost_no_tracked_file`

Old text:

```
        if gate.value.match(text, separator) is None:
            continue
```

New text:

```
        pass
```

### `u257.M11_paired_by_label`

_secret_violations_over: pair each pattern with its shortcut by label, so a repeated label borrows another pattern's literal and its finding is lost

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M11_paired_by_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_scan_secret_equality.py::test_two_patterns_sharing_a_label_never_borrow_each_others_shortcut`

Old text:

```
    for (label, pattern), shortcut in zip(patterns, shortcuts, strict=True):
```

New text:

```
    by_label = dict(zip((label for label, _ in patterns), shortcuts))
    for label, pattern in patterns:
        shortcut = by_label[label]
```

### `u257.M1_skip_after_match`

_matches_at_literal: look for the next literal one past the match's start rather than at its end, so a literal inside a reported secret is reported again

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M1_skip_after_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 116 against a baseline of 116
- Kills: 2 (killed)
- Killed:
  - `tests/test_scan_secret_equality.py::test_the_fast_scan_equals_the_reference_on_generated_texts`
  - `tests/test_scan_secret_equality.py::test_the_fast_scan_equals_the_reference_on_the_whole_generated_corpus_at_once`

Old text:

```
            position = text.find(literal, match.end())
```

New text:

```
            position = text.find(literal, position + 1)
```

### `u257.M2_gate_never_passes`

_keyword_gate_passes: return False always, so the two alternations never scan and every keyword credential is missed

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M2_gate_never_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 116 against a baseline of 116
- Kills: 24 (killed)
- Killed:
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[CLIENTSECRET]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[accessToken]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[access_token]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[apiKey]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[api_key]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[apikey]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[client-secret]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[clientId]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[clientSecret]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[client_id]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[client_secret]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[refreshToken]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[refresh_token]`
  - `tests/test_portability.py::test_credential_shapes_are_caught[api_key = "aB3xQ7zK9mN2pR4tV6wY8cE1gJ5"-credential assignment]`
  - `tests/test_portability.py::test_credential_shapes_are_caught[{"access_token": "aB3xQ7zK9mN2pR4tV6wY8cE1gJ5"}-OAuth token field]`
  - ... and 9 more, see the JSON sidecar

Old text:

```
    for run in _SEPARATOR_RUN.finditer(text):
        separator = run.start()
```

New text:

```
    for run in ():
        separator = run.start()
```

### `u257.M3_gate_always_passes`

_keyword_gate_passes: return True always, exact but every text is scanned by both alternations again, the whole saving lost

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M3_gate_always_passes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_scan_secret_equality.py::test_the_keyword_gate_hands_over_almost_no_tracked_file`

Old text:

```
def _keyword_gate_passes(gate: _KeywordGate, text: str) -> bool:
```

New text:

```
def _keyword_gate_passes(gate: _KeywordGate, text: str) -> bool:
    return True
```

### `u257.M4_no_quote_landing`

_keyword_gate_passes: do not step back over a quote after the keyword, so the JSON form "key": "value" is missed

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M4_no_quote_landing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 116 against a baseline of 116
- Kills: 21 (killed)
- Killed:
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[CLIENTSECRET]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[accessToken]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[access_token]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[apiKey]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[api_key]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[apikey]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[client-secret]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[clientId]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[clientSecret]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[client_id]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[client_secret]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[refreshToken]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[refresh_token]`
  - `tests/test_portability.py::test_credential_shapes_are_caught[{"access_token": "aB3xQ7zK9mN2pR4tV6wY8cE1gJ5"}-OAuth token field]`
  - `tests/test_portability.py::test_credential_shapes_are_caught[{"refresh_token": "aB3xQ7zK9mN2pR4tV6wY8cE1gJ5"}-OAuth token field]`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        ends = (end, end - 1) if end > 0 and text[end - 1] in _QUOTES else (end,)
```

New text:

```
        ends = (end,)
```

### `u257.M5_no_whitespace_walk`

_keyword_gate_passes: do not walk back over whitespace, so key = "value" with a space before the separator is missed

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M5_no_whitespace_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 116 against a baseline of 116
- Kills: 4 (killed)
- Killed:
  - `tests/test_portability.py::test_credential_shapes_are_caught[api_key = "aB3xQ7zK9mN2pR4tV6wY8cE1gJ5"-credential assignment]`
  - `tests/test_scan_secret_equality.py::test_one_planted_secret_per_pattern_is_still_reported`
  - `tests/test_scan_secret_equality.py::test_the_fast_scan_equals_the_reference_on_generated_texts`
  - `tests/test_scan_secret_equality.py::test_the_fast_scan_equals_the_reference_on_the_planted_corpus`

Old text:

```
        while end > 0 and _SPACE.match(text, end - 1):
```

New text:

```
        while False:
```

### `u257.M6_ascii_whitespace_only`

_SPACE: only the ASCII space, so a keyword separated from its colon by a tab, a newline or a Unicode space is missed

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M6_ascii_whitespace_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_scan_secret_equality.py::test_the_fast_scan_equals_the_reference_on_generated_texts`

Old text:

```
_SPACE = re.compile(r"\s")
```

New text:

```
_SPACE = re.compile(r" ")
```

### `u257.M7_window_one_short`

_keyword_gate_passes: search a window one character narrower than the longest keyword, so consumer_secret is missed

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M7_window_one_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 116 against a baseline of 116
- Kills: 2 (killed)
- Killed:
  - `tests/test_scan_secret_equality.py::test_the_fast_scan_equals_the_reference_on_generated_texts`
  - `tests/test_scan_secret_equality.py::test_the_keyword_lookback_window_reaches_the_longest_keyword`

Old text:

```
            if gate.keyword_end.search(text, max(0, keyword_end - gate.width), keyword_end):
```

New text:

```
            if gate.keyword_end.search(text, max(0, keyword_end - gate.width + 1), keyword_end):
```

### `u257.M8_no_source_check`

_keyword_gate: build the gate whatever the pattern's source, so a widened alternation is gated on the old keywords and its new keyword is missed

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M8_no_source_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_scan_secret_equality.py::test_a_pattern_that_drifted_from_its_shortcut_is_scanned_plainly`

Old text:

```
    if pattern.pattern != opening + keywords + _KEY_CLOSE + value:
        return None
```

New text:

```
    pass
```

### `u257.M9_lead_ignores_ignorecase`

_literal_lead: give a case insensitive pattern a literal lead, so a lower case spelling of its literal is never tried

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M9_lead_ignores_ignorecase`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 116 against a baseline of 116
- Kills: 2 (killed)
- Killed:
  - `tests/test_scan_secret_equality.py::test_a_pattern_that_may_match_off_its_literal_gets_no_literal_lead[(?i)\\bBearer\\s+[A-Za-z0-9]{24,}-0]`
  - `tests/test_scan_secret_equality.py::test_a_pattern_that_may_match_off_its_literal_gets_no_literal_lead[\\bBearer\\s+[A-Za-z0-9]{24,}-re.IGNORECASE]`

Old text:

```
    if parsed is None or (pattern.flags | parsed.state.flags) & re.IGNORECASE:
```

New text:

```
    if parsed is None:
```

### `u28-skills-independent.X1_placeholder_exemption`

the portability scanner stops exempting a placeholder home segment, so a documented path shape is reported

- File: `scripts/scan_repo.py`
- Source: `u28-skills-independent.json`, row `X1_placeholder_exemption`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_portability.py::test_placeholder_paths_are_allowed`
  - `tests/test_portability.py::test_the_repository_itself_is_clean`

Old text:

```
    for match in _HOME_DIR.finditer(text):
        segment = match.group(1)
        if _is_placeholder_segment(segment):
            continue
```

New text:

```
    for match in _HOME_DIR.finditer(text):
        segment = match.group(1)
        del segment
```

### `u28-skills-independent.X2_mount_rule_removed`

the portability scanner stops looking for a hardcoded volume path at all

- File: `scripts/scan_repo.py`
- Source: `u28-skills-independent.json`, row `X2_mount_rule_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 98 against a baseline of 98
- Kills: 4 (killed)
- Killed:
  - `tests/test_portability.py::test_any_volume_is_caught_not_just_one`
  - `tests/test_portability.py::test_guard_covers_every_shipped_surface[docs/install.md-Put the library at /Volumes/BigAudioDrive/Music\n]`
  - `tests/test_portability.py::test_guard_covers_every_shipped_surface[scripts/backup.sh-VOLUME=/Volumes/BigAudioDrive/Music\n]`
  - `tests/test_portability.py::test_guard_covers_every_shipped_surface[src/cratekit/core/config.py-ROOT = "/Volumes/BigAudioDrive/Music"\n]`

Old text:

```
    for match in _MOUNT.finditer(text):
        segment = match.group(1)
        if _is_placeholder_segment(segment):
            continue
        problems.append(
            f"hardcoded volume path {match.group(0)!r}; the library root is "
            f"configuration, not a literal"
        )
```

New text:

```
(empty)
```

### `u196.C1_no_run_is_green`

verdict: read no pull request run yet as green, so a session merges before CI has started

- File: `scripts/wait_ci.py`
- Source: `u196.json`, row `C1_no_run_is_green`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_wait_ci.py`
- Collected: 25 against a baseline of 25
- Kills: 4 (killed)
- Killed:
  - `tests/test_wait_ci.py::test_main_exits_by_verdict`
  - `tests/test_wait_ci.py::test_no_run_yet_is_pending_never_green`
  - `tests/test_wait_ci.py::test_wait_returns_once_the_runs_finish`
  - `tests/test_wait_ci.py::test_wait_times_out_as_pending_and_says_so`

Old text:

```
    if not runs:
        return PENDING, "no pull request run on this head yet"
```

New text:

```
    if not runs:
        return PASSED, "no pull request run on this head yet"
```

### `u196.C2_unfinished_ignored`

verdict: drop the unfinished check, so a run still going reads as its null conclusion

- File: `scripts/wait_ci.py`
- Source: `u196.json`, row `C2_unfinished_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_wait_ci.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/test_wait_ci.py::test_a_run_still_going_is_pending_and_named`
  - `tests/test_wait_ci.py::test_wait_returns_once_the_runs_finish`

Old text:

```
    if unfinished:
        names
```

New text:

```
    if False:
        names
```

### `u196.C3_neutral_red`

GREEN: drop neutral, so a neutral run makes a green head red

- File: `scripts/wait_ci.py`
- Source: `u196.json`, row `C3_neutral_red`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_wait_ci.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_wait_ci.py::test_every_run_completed_green_is_green[neutral]`

Old text:

```
GREEN = ("success", "neutral", "skipped")
```

New text:

```
GREEN = ("success", "skipped")
```

### `u196.C4_deadline_overrun`

wait: sleep past the deadline before giving up

- File: `scripts/wait_ci.py`
- Source: `u196.json`, row `C4_deadline_overrun`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_wait_ci.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_wait_ci.py::test_wait_times_out_as_pending_and_says_so`

Old text:

```
        if clock() + every > deadline:
```

New text:

```
        if clock() > deadline:
```

### `u196.C5_unread_exits_pending`

main: drop the unread exit, so a wait that could not read the runs exits 2 as if it timed out

- File: `scripts/wait_ci.py`
- Source: `u196.json`, row `C5_unread_exits_pending`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_wait_ci.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_wait_ci.py::test_main_exits_3_when_the_runs_cannot_be_read`

Old text:

```
    return {PASSED: 0, FAILED: 1, UNREAD: 3}.get(state, 2)
```

New text:

```
    return {PASSED: 0, FAILED: 1}.get(state, 2)
```

### `u196.C6_failures_never_reset`

wait: never reset the failure count after a good read, so failures that are not in a row end the wait as unread

- File: `scripts/wait_ci.py`
- Source: `u196.json`, row `C6_failures_never_reset`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_wait_ci.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_wait_ci.py::test_failures_count_in_a_row_only`

Old text:

```
            failures = 0
            state, line = verdict(runs)
```

New text:

```
            state, line = verdict(runs)
```

