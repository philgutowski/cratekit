# Mutation table: u331-before-b-02

Measured by `scripts/mutate.py` on 2026-11-23 23:03 UTC, branch `HEAD` at `c0bb16a4`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22808 collected. pytest invocations for this batch: 195.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 23:03 UTC for commit `c0bb16a4eaf3`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 33, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22808 against 22808. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1115.M1_failed_needs_a_failure` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 1 | killed |
| `r1115.M2_every_failure_for_good` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 5 | killed |
| `r1115.M3_nothing_left_to_run` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 1 | killed |
| `r1115.M4_retryable_is_not_for_good` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 4 | killed |
| `r1115.M5_declined_is_refused` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 8 | killed |
| `r1115.M6_landed_needs_a_track` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 3 | killed |
| `r1115.M7_done_counts_done` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 8 | killed |
| `r1115.M8_failed_names_the_failures` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 2 | killed |
| `r289-b.B1_reclaim_rmtree` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 366 | 2 | killed |
| `r289-b.B3_terminal_filter_gone` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 366 | 2 | killed |
| `r289-b.B4_unknown_job_read_as_terminal` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 366 | 1 | killed |
| `r289-b.B5_job_directory_before_its_items` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 366 | 2 | killed |
| `r289-b.B6_job_directory_never_reclaimed` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 366 | 2 | killed |
| `r289-b.C1_download_call_site` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 366 | 1 | killed |
| `r289-c.B2r_reclaim_reports_a_failure_as_a_removal` | `src/cratekit/acquire/cli.py` | maintainer | 6 file(s) | 366 | 1 | killed |
| `r289-c.B9r_children_unreadable_raises` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 22808 | 0 (promoted) | zero |
| `r290-author.S02_acquire_download_call_removed` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 195 | 11 | killed |
| `r668-a.M11_no_frozen_list_skip` | `src/cratekit/acquire/cli.py` | maintainer | 1 file(s) | 22808 | 0 (promoted) | zero |
| `r668-a.M1_list_required_again` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 39 | killed |
| `r668-a.M2_resume_argv_carries_the_list` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 2 | killed |
| `r668-a.M3_no_empty_job_guard` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r668-a.M4_no_missing_list_guard` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 2 | killed |
| `r668-a.M5_missing_list_guard_after_load` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r668-a.M6_no_list_check_on_resume` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 3 | killed |
| `r668-a.M7_list_compared_as_strings` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r668-a.M9_other_verbs_job_read` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r668-b.M12_home_expansion_raises` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r668-b.M8_named_not_absolutised` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u108-c.G25_drive_maps_ending` | `src/cratekit/acquire/cli.py` | user | 7 file(s) | 476 | 31 | killed |
| `u169.A1_retryable_policy_declined` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 1 | killed |
| `u169.A2_any_permanent_declined` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 7 | killed |
| `u169.A3_worker_never_declines` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 9 | killed |
| `u169.A4_no_declined_warning` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 4 | killed |
| `u169.A5_warning_names_failed_items` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 1 | killed |
| `u274.C1_worker_names_no_drive` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 450 | 17 | killed |
| `u42-author-round-2.C2_unknown_defaults_lossless` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.C1_undecided_derived` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 3 | killed |
| `u42-author.C3_strict_consults_the_marker` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 3 | killed |
| `u42-author.C4_marked_lossless_dropped` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.C5_empty_marker_matches_everything` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.P1_unresolved_from_the_page` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.P2_relative_path_leaks_the_root` | `src/cratekit/acquire/cli.py` | maintainer | 1 file(s) | 24 | 5 | killed |
| `u42-author.W1_onerror_hook` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 22808 | 0 (promoted) | zero |
| `u42-author.W2_unreadable_reported` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 229 | 2 | killed |
| `u42-author.W3_onerror_silent` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 22808 | 0 (promoted) | zero |
| `u54-acquisition-worker.G10_absent_result` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G11_not_acquired` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 8 | killed |
| `u54-acquisition-worker.G12_landing_check` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 5 | killed |
| `u54-acquisition-worker.G14_marker_applied` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 3 | killed |
| `u54-acquisition-worker.G15_no_marker_text` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G17_paced_sleep_bound` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 2 | killed |
| `u54-acquisition-worker.G19_frozen_config` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 40 | killed |
| `u54-acquisition-worker.G1_origin_refusal` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G20_output_exists` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G27_remedy_absent_stays_absent` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G28_marker_decided_by_the_file` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G29_auth_failure_parks` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 3 | killed |
| `u54-acquisition-worker.G2_missing_identifier` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G8_park_on_block` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G9_failed_invocation` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 5 | killed |
| `u54-zero-row-remeasured.G7_staging_cleared` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u172-b.C3_left_miscounted` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 1 | killed |
| `u172.C1_tail_skips_guess` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 5 | killed |
| `u172.C2_guess_without_pass` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 2 | killed |
| `u179.T2_rehearsal_ack_attends` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 214 | 1 | killed |
| `u179.T3_rehearsal_stop_wording` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 214 | 1 | killed |
| `u179.T4_commands_quoted` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 215 | 3 | killed |
| `u181.T1_rescore_ignores_unable` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 215 | 4 | killed |
| `u181.T2_rescore_ignores_profile` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 215 | 30 | killed |
| `u181.T3_rescore_keeps_stale` | `src/cratekit/cli/tail.py` | user | 1 file(s) | 34 | 1 | killed |
| `u181.T4_rescore_failure_ignored` | `src/cratekit/cli/tail.py` | user | 1 file(s) | 34 | 1 | killed |
| `u181.T5_rescore_never_run` | `src/cratekit/cli/tail.py` | user | 2 file(s) | 181 | 4 | killed |
| `u181.T6_plan_warnings_not_lifted` | `src/cratekit/cli/tail.py` | user | 2 file(s) | 181 | 1 | killed |
| `u190.T1_run_folder_absolute` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 1 | killed |
| `u190.T3_stale_matches_folder` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 1 | killed |
| `u190.T4_name_answers_inline` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 2 | killed |
| `u190.T6_chain_namespace` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 3 | killed |
| `u212.T1_reason_guard` | `src/cratekit/cli/tail.py` | maintainer | 11 file(s) | 1630 | 1 | killed |
| `u212.T2_done_only` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1630 | 1 | killed |
| `u212.T3_library` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1630 | 1 | killed |
| `u212.T4_earliest_first` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1630 | 1 | killed |
| `u212.T5_name_wraps` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1630 | 2 | killed |
| `u284.T1_pass_names_nothing` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 385 | 1 | killed |
| `u284.T2_pass_stop_unsaid` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 385 | 1 | killed |
| `u319.M10_sync_stop_drops_the_short_path` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 182 | 1 | killed |
| `u157.C1_at_the_cut` | `src/cratekit/core/drift.py` | user | 3 file(s) | 126 | 2 | killed |
| `u157.C2_verdict_tag_trusted` | `src/cratekit/core/drift.py` | user | 3 file(s) | 126 | 5 | killed |
| `u157.C3_negative_score` | `src/cratekit/core/drift.py` | user | 3 file(s) | 126 | 1 | killed |
| `r154-a.A3_named_shape_check` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 9 | killed |
| `r154-a.A5_listing_filter` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 1 | killed |
| `r154-a.A7_read_normalization` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 1 | killed |
| `r154-a.A8_empty_expected` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 2 | killed |
| `r154-b.B1_named_mismatch` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 8 | killed |
| `r154-b.B2_two_markers` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 2 | killed |
| `r154-b.B3_handed_down_stamp` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 1 | killed |
| `r154-b.B4_stated_volume_over_unmarked` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 1 | killed |
| `r154-b.B5_veto_not_select` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 3 | killed |
| `r154-b.B6_walk_bound` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 1 | killed |
| `r154-b.B7_walk_order` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 5 | killed |
| `r154-b.B8_walk_match` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 3 | killed |
| `r338-a.B3_capture_is_a_copy` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 2 | killed |
| `r338-a.B4_no_undo_archive` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r338-a.B5_one_mirror_for_every_library` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 4 | killed |
| `r338-a.B6_identity_interpolated_raw` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 3 | killed |
| `r338-a.B8_contained_share_copied_twice` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 8 | killed |
| `r338-b.R1_missing_directory_refuses` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r338-b.R4_empty_listing_read_as_held` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r338-b.R5_pulled_under_the_watch` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r338-b.R6_switch_ignored` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r338-b.R7_restore_is_a_sync` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 2 | killed |
| `r338-b.R8_unmarked_snapshot_orphans_the_share` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r338-b.R9_contained_restore_asks_about_a_share` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 2 | killed |
| `r338-c.C1_absent_share_never_said` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 4 | killed |
| `r338-c.C2_carried_share_still_warned` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 2 | killed |
| `r367.E2_an_unconfirmed_restore_is_allowed` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 1 | killed |
| `r367.E3_a_live_rekordbox_is_ignored` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 1 | killed |
| `r367.G12_listing_results_are_discarded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 2 | killed |
| `r367.G1_always_copy_the_restored_sidecar` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 6 | killed |
| `r367.G3_membership_is_inverted` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 4 | killed |
| `r367.G4_the_inventory_restored_flag_is_ignored` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 4 | killed |
| `r367.G5_absent_sidecars_are_not_recorded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 2 | killed |
| `r367.G7_the_listing_is_of_the_snapshot_root` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 1 | killed |
| `r367.G8_files_only_is_dropped` | `src/cratekit/modules/tools/backup_snapshot.py` | maintainer | 1 file(s) | 188 | 1 | killed |
| `r388-a.M1_named_identity_listing_back_to_absence` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 2 | killed |
| `r388-a.M2_identity_listing_message_reworded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r388-a.M3_contents_listing_back_to_absence` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 2 | killed |
| `r388-a.M4_contents_listing_message_reworded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r388-a.M5_root_listing_back_to_absence` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r388-a.M6_root_listing_message_reworded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r388-b.M10_named_stamp_absent_read_as_failure` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r388-b.M11_db_folder_absent_read_as_failure` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r388-b.M7_share_listing_back_to_absence` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r388-b.M8_share_listing_message_reworded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r388-b.M9_root_absent_read_as_failure` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r592-b.B6_restore_mirror_carries_the_database` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 3 file(s) | 22808 | 0 (promoted) | zero |
| `u211.B1_backup_database_portion_refuses_alone` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 3 file(s) | 167 | 1 | killed |
| `u27-restore-cli-independent.X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 3 file(s) | 430 | 3 | killed |
| `r1255.R5_organize_rotation_warns` | `src/cratekit/organize/rekordbox.py` | user | 3 file(s) | 72 | 1 | killed |
| `u112.R1_no_ack_planned` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 6 | killed |
| `u112.R2_applied_entries_outstanding` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.R3_bridge_tree_planned` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.R4_job_without_gate_run` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.R5_actor_invented` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.R7_every_batch_suggested` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.R8_inbox_mine_unlisted` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 2 | killed |
| `u137.R1_adopt_gate` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 3 | killed |
| `u137.R2_rotation_for_yours` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 2 | killed |
| `u137.R3_refused_rotation_shown` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u137.R4_rotation_shown_unselected` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u137.R5_record_labels_gate` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 4 | killed |
| `u144-c.C5_export_module` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-c.C6_native_only` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-c.C7_folder_warning` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 38 | 1 | killed |
| `u185.R1_organize_not_yours` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 2 | killed |
| `u185.R2_organize_fact` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 2 | killed |
| `u214.M14_old_not_yours` | `src/cratekit/organize/rekordbox.py` | user | 6 file(s) | 174 | 2 | killed |

## Zero rows and what they owe

- `r289-c.B9r_children_unreadable_raises` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r668-a.M11_no_frozen_list_skip` (maintainer facing): maintainer facing, composite not required
- `u42-author.W1_onerror_hook` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u42-author.W3_onerror_silent` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r592-b.B6_restore_mirror_carries_the_database` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r1115.M1_failed_needs_a_failure`

read_download: drop the rule that a FAILED job settles only with a failed track, so a FAILED job holding none reads as settled

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M1_failed_needs_a_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[failed-with-no-failed-track]`

Old text:

```
        and bool(failed)

```

New text:

```
        and True

```

### `r1115.M2_every_failure_for_good`

read_download: drop the rule that every failed track is refused for good, so a transient failure settles and the go lands over it

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M2_every_failure_for_good`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-failure-a-retry-could-clear]`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-failure-recording-no-cause]`
  - `tests/test_label_sync_go.py::test_a_transient_failure_still_ends_the_go_on_its_refusal_with_no_tail`
  - `tests/test_sync_land.py::test_a_transient_download_failure_ends_the_pass_and_lands_nothing`

Old text:

```
        and len(for_good) == len(failed)

```

New text:

```
        and len(for_good) >= 0

```

### `r1115.M3_nothing_left_to_run`

read_download: drop the rule that no track is still to run, so a FAILED job with a track never attempted settles

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M3_nothing_left_to_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-track-never-attempted]`

Old text:

```
        and all(item.state in finished for item in held)

```

New text:

```
        and any(item.state in finished for item in held)

```

### `r1115.M4_retryable_is_not_for_good`

read_download: read every failure with a cause as refused for good, retryable or not

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M4_retryable_is_not_for_good`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-failure-a-retry-could-clear]`
  - `tests/test_label_sync_go.py::test_a_transient_failure_still_ends_the_go_on_its_refusal_with_no_tail`
  - `tests/test_sync_land.py::test_a_transient_download_failure_ends_the_pass_and_lands_nothing`

Old text:

```
        item.item_id for item in failed if item.cause is not None and not item.cause.retryable

```

New text:

```
        item.item_id for item in failed if item.cause is not None

```

### `r1115.M5_declined_is_refused`

read_download: leave a declined track out of the refused rows, so a lossy only track is named nowhere on the go's check

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M5_declined_is_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[succeeded-with-a-declined-track]`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tail_refused_beside_a_download_still_names_the_tracks_refused_for_good`
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`

Old text:

```
        and (item.item_id in for_good or item.state is jobs.ItemState.SKIPPED)

```

New text:

```
        and (item.item_id in for_good)

```

### `r1115.M6_landed_needs_a_track`

DownloadRead.landed: read a settled download with no track done as landed, so a tail is set over an empty folder

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M6_landed_needs_a_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
        return self.settled and self.done > 0

```

New text:

```
        return self.settled

```

### `r1115.M7_done_counts_done`

read_download: count a skipped track as done too

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M7_done_counts_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[failed-with-no-failed-track]`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[succeeded-with-a-declined-track]`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`
  - `tests/test_sync_land.py::test_the_newest_download_over_the_list_is_the_one_the_pass_reads`

Old text:

```
        done=sum(1 for item in held if item.state is jobs.ItemState.DONE),

```

New text:

```
        done=sum(1 for item in held if item.state in (jobs.ItemState.DONE, jobs.ItemState.SKIPPED)),

```

### `r1115.M8_failed_names_the_failures`

read_download: name no failed track, so the go's own warning for one is never raised

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M8_failed_names_the_failures`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`

Old text:

```
        failed=tuple(item.item_id for item in failed if item.item_id in for_good),

```

New text:

```
        failed=(),

```

### `r289-b.B1_reclaim_rmtree`

Reclaim with rmtree, so a refused landing kept as evidence is deleted

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B1_reclaim_rmtree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 366 against a baseline of 366
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_refused_landing_left_as_evidence_survives_the_sweep`
  - `tests/test_acquire_workers.py::test_the_sweep_does_not_report_a_directory_it_could_not_remove`

Old text:

```
    try:
        directory.rmdir()
    except OSError:
        return
    removed.append(directory)
```

New text:

```
    try:
        shutil.rmtree(directory)
    except OSError:
        return
    removed.append(directory)
```

### `r289-b.B3_terminal_filter_gone`

Sweep every job's staging, open ones included

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B3_terminal_filter_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 366 against a baseline of 366
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_directory_naming_a_job_this_queue_does_not_hold_is_left_alone`
  - `tests/test_acquire_workers.py::test_an_open_jobs_staging_survives_the_sweep`

Old text:

```
        if states.get(job_dir.name) not in jobs.TERMINAL_STATES:
```

New text:

```
        if False:
```

### `r289-b.B4_unknown_job_read_as_terminal`

Read a directory naming a job this queue does not hold as finished

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B4_unknown_job_read_as_terminal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_directory_naming_a_job_this_queue_does_not_hold_is_left_alone`

Old text:

```
        if states.get(job_dir.name) not in jobs.TERMINAL_STATES:
```

New text:

```
        if states.get(job_dir.name, jobs.JobState.SUCCEEDED) not in jobs.TERMINAL_STATES:
```

### `r289-b.B5_job_directory_before_its_items`

Reclaim the job directory first, so its item directories never go

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B5_job_directory_before_its_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 366 against a baseline of 366
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_emptied_staging_of_a_finished_job_is_reclaimed_by_the_next_run`
  - `tests/test_acquire_workers.py::test_the_sweep_reports_what_it_removed_deepest_first`

Old text:

```
        for item_dir in _children(job_dir):
            if item_dir.is_dir():
                _reclaim(item_dir, removed)
        _reclaim(job_dir, removed)
```

New text:

```
        _reclaim(job_dir, removed)
        for item_dir in _children(job_dir):
            if item_dir.is_dir():
                _reclaim(item_dir, removed)
```

### `r289-b.B6_job_directory_never_reclaimed`

Reclaim the item directories and leave the job directory behind

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B6_job_directory_never_reclaimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 366 against a baseline of 366
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_emptied_staging_of_a_finished_job_is_reclaimed_by_the_next_run`
  - `tests/test_acquire_workers.py::test_the_sweep_reports_what_it_removed_deepest_first`

Old text:

```
                _reclaim(item_dir, removed)
        _reclaim(job_dir, removed)
```

New text:

```
                _reclaim(item_dir, removed)
```

### `r289-b.C1_download_call_site`

Drop the sweep at the head of acquire download

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `C1_download_call_site`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_emptied_staging_of_a_finished_job_is_reclaimed_by_the_next_run`

Old text:

```
        sweep_staging(Path(cfg.paths.download_staging), store)

```

New text:

```
(empty)
```

### `r289-c.B2r_reclaim_reports_a_failure_as_a_removal`

Report a directory that could not be removed as one that was

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-c.json`, row `B2r_reclaim_reports_a_failure_as_a_removal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_sweep_does_not_report_a_directory_it_could_not_remove`

Old text:

```
    try:
        directory.rmdir()
    except OSError:
        return
    removed.append(directory)
```

New text:

```
    try:
        directory.rmdir()
    except OSError:
        pass
    removed.append(directory)
```

### `r289-c.B9r_children_unreadable_raises`

Let an unlistable directory raise out of the sweep and fail the verb

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-c.json`, row `B9r_children_unreadable_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 22808 against a baseline of 22808
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        return tuple(sorted(directory.iterdir()))
    except OSError:
        return ()
```

New text:

```
    return tuple(sorted(directory.iterdir()))
```

### `r290-author.S02_acquire_download_call_removed`

Remove the one jobs.raise_for_state call from acquire/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/acquire/cli.py`
- Source: `r290-author.json`, row `S02_acquire_download_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_acquire_workers.py`
- Collected: 195 against a baseline of 195
- Kills: 11 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r668-a.M11_no_frozen_list_skip`

a job whose payload names no list is compared against an empty path and refuses any list named beside it

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M11_no_frozen_list_skip`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 22808 against a baseline of 22808
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not frozen:
        return
    try:
```

New text:

```
    try:
```

### `r668-a.M1_list_required_again`

the list positional is required again, so --job alone is argparse's usage error, the defect sitting 7 hit

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M1_list_required_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 39 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_command_naming_nothing_is_refused_before_the_configuration_is_read`
  - `tests/test_acquire_workers.py::test_a_configuration_naming_an_unknown_adapter_fails_the_item_by_name`
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_a_download_job_runs_pending_to_done_through_the_resume_path`
  - `tests/test_acquire_workers.py::test_a_lossless_landing_under_the_permissive_policy_is_not_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_the_permissive_policy_is_committed_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_partial_file_left_in_staging_does_not_poison_the_next_attempt`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_rate_limit_is_retried_under_backoff_and_then_lands`
  - `tests/test_acquire_workers.py::test_a_rate_limit_that_never_clears_fails_the_item_as_transient`
  - ... and 24 more, see the JSON sidecar

Old text:

```
        "list",
        nargs="?",
        default=None,

```

New text:

```
        "list",

```

### `r668-a.M2_resume_argv_carries_the_list`

the resume argv and the drive it with line name the frozen list again

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M2_resume_argv_carries_the_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_download_argv_round_trips_the_frozen_payload_and_carries_no_run`
  - `tests/test_acquire_workers.py::test_queueing_a_download_names_the_job_and_the_command_that_drives_it`

Old text:

```
    return ["acquire", "download", "--job", job.job_id]
```

New text:

```
    return ["acquire", "download", str((job.payload or {}).get(LIST) or ""), "--job", job.job_id]
```

### `r668-a.M3_no_empty_job_guard`

an empty --job identifier is not refused, so it falls through to the queueing path and queues the list a second time

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M3_no_empty_job_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_an_empty_job_identifier_is_refused_rather_than_queueing_the_list_again`

Old text:

```
    if ctx.args.job is not None and not ctx.args.job.strip():
        raise _unusable(
```

New text:

```
    if False:
        raise _unusable(
```

### `r668-a.M4_no_missing_list_guard`

a command naming neither a list nor a job is not refused by the verb, and reads a list called None

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M4_no_missing_list_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_command_naming_nothing_is_refused_before_the_configuration_is_read`
  - `tests/test_acquire_workers.py::test_neither_a_list_nor_a_job_is_refused_by_the_verb_and_queues_nothing`

Old text:

```
    if ctx.args.list is None and ctx.args.job is None:
        raise _unusable(
```

New text:

```
    if False:
        raise _unusable(
```

### `r668-a.M5_missing_list_guard_after_load`

the missing list refusal runs after the configuration is read, so a command naming nothing has side effects first

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M5_missing_list_guard_after_load`
- Moved: Same order in acquire_download; U298 replaced the private _load with cli.output.load_config, so the configuration read the guard is moved after is reworded
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_command_naming_nothing_is_refused_before_the_configuration_is_read`

Old text:

```
    if ctx.args.list is None and ctx.args.job is None:
        raise _unusable(
            "no list was named and no job was given, so there is nothing to acquire",
            "name the list of tracks to acquire",
            "or continue an acquisition already queued with --job JOB_ID",
        )
    cfg = load_config(("acquire.cli",))

```

New text:

```
    cfg = load_config(("acquire.cli",))
    if ctx.args.list is None and ctx.args.job is None:
        raise _unusable(
            "no list was named and no job was given, so there is nothing to acquire",
            "name the list of tracks to acquire",
            "or continue an acquisition already queued with --job JOB_ID",
        )

```

### `r668-a.M6_no_list_check_on_resume`

a list named beside --job is never compared with the frozen one, so a different list is silently ignored and the job driven

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M6_no_list_check_on_resume`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_different_list_named_beside_the_job_is_refused_and_nothing_is_fetched`
  - `tests/test_acquire_workers.py::test_a_list_under_a_home_that_cannot_be_expanded_is_refused_by_name`
  - `tests/test_acquire_workers.py::test_a_refused_list_leaves_a_dead_drivers_claim_for_the_resume_to_reconcile`

Old text:

```
            _same_list_or_refuse(
                ctx.args.list, jobs.get(store, ctx.args.job), ctx.entry.handler_key
            )

```

New text:

```
            pass

```

### `r668-a.M7_list_compared_as_strings`

the named and frozen lists are compared as strings, so a symlinked or /private spelling of the frozen list is refused

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M7_list_compared_as_strings`
- Moved: Same comparison in _same_list_or_refuse; U298 renamed preflight._names_one_path to names_one_path
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_frozen_list_spelled_through_a_symlink_still_drives`

Old text:

```
    if preflight.names_one_path(given, Path(frozen)):
```

New text:

```
    if str(given) == frozen:
```

### `r668-a.M9_other_verbs_job_read`

another verb's job payload is read as a frozen download list

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M9_other_verbs_job_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_another_verbs_job_is_not_read_as_a_frozen_download_list`

Old text:

```
    if named is None or job.handler_key != handler_key:
```

New text:

```
    if named is None:
```

### `r668-b.M12_home_expansion_raises`

a named list under a home directory that cannot be expanded raises instead of being compared as typed

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-b.json`, row `M12_home_expansion_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_list_under_a_home_that_cannot_be_expanded_is_refused_by_name`

Old text:

```
    except RuntimeError:
        given = Path(named).absolute()
```

New text:

```
    except RuntimeError:
        raise
```

### `r668-b.M8_named_not_absolutised`

the named list is compared without the freeze's absolutising, so a relative spelling from the queueing directory is refused

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-b.json`, row `M8_named_not_absolutised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_deleted_frozen_list_named_relative_from_where_it_was_queued_still_drives`

Old text:

```
        given = Path(named).expanduser().absolute()
    except RuntimeError:
```

New text:

```
        given = Path(named).expanduser()
    except RuntimeError:
```

### `u108-c.G25_drive_maps_ending`

acquire_cli.drive_queued: a parked or half failed job is returned as if it ended clean

- File: `src/cratekit/acquire/cli.py`
- Source: `u108-c.json`, row `G25_drive_maps_ending`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_label_sync_go.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 476 against a baseline of 476
- Kills: 31 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_while_a_go_resumed_another_refuses_the_resumes_tail`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park`
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_names_its_own_go_to_continue_not_the_job`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_cancelled_still_refuses_and_lands_nothing`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - ... and 16 more, see the JSON sidecar

Old text:

```
    jobs.raise_for_state(job)
    return job, warnings
```

New text:

```
    return job, warnings
```

### `u169.A1_retryable_policy_declined`

refused_for_good: drop the retryable clause, so a retryable policy refusal is skipped

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A1_retryable_policy_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_only_a_permanent_cause_in_the_policy_class_is_refused_for_good`

Old text:

```
    return cause.code is ExitCode.REFUSED_BY_POLICY and not cause.retryable
```

New text:

```
    return cause.code is ExitCode.REFUSED_BY_POLICY
```

### `u169.A2_any_permanent_declined`

refused_for_good: drop the policy class, so any permanent failure (output-exists) is skipped

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A2_any_permanent_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 7 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_an_existing_file_at_the_destination_refuses_rather_than_replacing_it`
  - `tests/test_acquire_workers.py::test_only_a_permanent_cause_in_the_policy_class_is_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`

Old text:

```
    return cause.code is ExitCode.REFUSED_BY_POLICY and not cause.retryable
```

New text:

```
    return not cause.retryable
```

### `u169.A3_worker_never_declines`

handle: re-raise a policy refusal instead of declining it, the base's behaviour

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A3_worker_never_declines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 9 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_label_sync_go.py::test_a_go_job_whose_track_was_refused_for_good_is_not_resumed`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`

Old text:

```
            raise jobs.Declined(exc.cause) from exc
```

New text:

```
            raise
```

### `u169.A4_no_declined_warning`

drive_queued: add no warning for the skipped tracks

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A4_no_declined_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`

Old text:

```
    warnings = (*warnings, *declined_warnings(store, job))
```

New text:

```
    warnings = tuple(warnings)
```

### `u169.A5_warning_names_failed_items`

declined_warnings: name every item with a cause, failed ones included (unreachable through the verb, which refuses a failed job before its warnings; killed at the function)

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A5_warning_names_failed_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`

Old text:

```
        if item.state is not jobs.ItemState.SKIPPED or item.cause is None:
```

New text:

```
        if item.cause is None:
```

### `u274.C1_worker_names_no_drive`

acquire.cli: the download worker names no per drive holder, so a download logs in once a track

- File: `src/cratekit/acquire/cli.py`
- Source: `u274.json`, row `C1_worker_names_no_drive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 17 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_broken_item_fails_alone_and_the_job_stays_resumable`
  - `tests/test_vendored_drive.py::test_a_defect_at_the_close_of_a_finished_drive_is_raised`
  - `tests/test_vendored_drive.py::test_a_drive_reads_the_keychain_as_a_one_track_drive_does_and_writes_nothing`
  - `tests/test_vendored_drive.py::test_a_drive_signalled_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_drive_torn_down_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest`
  - `tests/test_vendored_drive.py::test_a_ten_track_job_logs_in_once_and_spends_four_calls_a_track`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`
  - `tests/test_vendored_drive.py::test_every_call_of_the_drive_goes_through_the_gate`
  - `tests/test_vendored_drive.py::test_the_download_worker_names_the_vendored_drive`
  - ... and 2 more, see the JSON sidecar

Old text:

```
handle.per_drive = vendored.drive  # type: ignore[attr-defined]

```

New text:

```
(empty)
```

### `u42-author-round-2.C2_unknown_defaults_lossless`

Classify an unrecognised suffix as lossless instead of 'other'

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author-round-2.json`, row `C2_unknown_defaults_lossless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_non_audio_files_are_not_reported`

Old text:

```
    return "other"
```

New text:

```
    return "lossless"
```

### `u42-author.C1_undecided_derived`

Empty the undecided remainder, so an MP4 container falls out as 'other'

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C1_undecided_derived`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_an_mp4_container_is_reported_undecided_rather_than_assumed`
  - `tests/test_acquire_cli.py::test_every_audio_container_the_renamer_knows_has_a_classification`
  - `tests/test_acquire_cli.py::test_the_undecided_remainder_is_the_mp4_container_today`

Old text:

```
UNDECIDED_EXTS: frozenset[str] = frozenset(naming.AUDIO_EXTS) - LOSSLESS_EXTS - LOSSY_EXTS
```

New text:

```
UNDECIDED_EXTS: frozenset[str] = frozenset()
```

### `u42-author.C3_strict_consults_the_marker`

Make strict behave like the permissive policy, admitting a marked lossy file

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C3_strict_consults_the_marker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_configuration_with_no_marker_text_decides_no_marker_question`
  - `tests/test_acquire_cli.py::test_strict_policy_reports_every_lossy_file_marked_or_not`
  - `tests/test_acquire_cli.py::test_the_audit_reads_the_policy_the_configuration_actually_holds`

Old text:

```
                if policy is LosslessPolicy.STRICT:
                    found.append(_item(path, root, "lossy-under-strict"))
                elif marker and not marked:
```

New text:

```
                if policy is LosslessPolicy.STRICT and marker and not marked:
                    found.append(_item(path, root, "lossy-under-strict"))
                elif marker and not marked:
```

### `u42-author.C4_marked_lossless_dropped`

Stop reporting a lossless file that wears the lossy marker

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C4_marked_lossless_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_lossless_file_wearing_the_marker_is_reported`

Old text:

```
            elif marked:
                found.append(_item(path, root, "marked-lossless"))
```

New text:

```
            elif False:
                found.append(_item(path, root, "marked-lossless"))
```

### `u42-author.C5_empty_marker_matches_everything`

Drop the empty-marker guard, so '' in stem marks every file

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C5_empty_marker_matches_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_configuration_with_no_marker_text_decides_no_marker_question`

Old text:

```
            marked = bool(marker) and marker in path.stem
```

New text:

```
            marked = marker in path.stem
```

### `u42-author.P1_unresolved_from_the_page`

Report zero outstanding regardless of what the walk found

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `P1_unresolved_from_the_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_the_audit_reads_the_policy_the_configuration_actually_holds`

Old text:

```
            "unresolved": len(found),
```

New text:

```
            "unresolved": 0,
```

### `u42-author.P2_relative_path_leaks_the_root`

Report the absolute path, putting a real directory layout in the payload (R1)

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `P2_relative_path_leaks_the_root`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_configuration_with_no_marker_text_decides_no_marker_question`
  - `tests/test_acquire_cli.py::test_a_lossless_file_wearing_the_marker_is_reported`
  - `tests/test_acquire_cli.py::test_an_mp4_container_is_reported_undecided_rather_than_assumed`
  - `tests/test_acquire_cli.py::test_permissive_policy_reports_only_the_unmarked_lossy_file`
  - `tests/test_acquire_cli.py::test_strict_policy_reports_every_lossy_file_marked_or_not`

Old text:

```
        where = str(path.relative_to(root))
```

New text:

```
        where = str(path)
```

### `u42-author.W1_onerror_hook`

Revert the walk to Path.rglob, which swallows the PermissionError

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `W1_onerror_hook`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 22808 against a baseline of 22808
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    for dirpath, _dirnames, filenames in os.walk(root, onerror=note):
        here = Path(dirpath)
        for name in filenames:
            path = here / name
```

New text:

```
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if True:
```

### `u42-author.W2_unreadable_reported`

Collect the unreadable directories and then never report them

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `W2_unreadable_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    found += [_item(path, root, "path-unreadable") for path in unreadable]
```

New text:

```
(empty)
```

### `u42-author.W3_onerror_silent`

Keep os.walk but make the error hook a no-op, the half-fix

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `W3_onerror_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 22808 against a baseline of 22808
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        unreadable.append(Path(exc.filename) if exc.filename else root)
```

New text:

```
        return None
```

### `u54-acquisition-worker.G10_absent_result`

Drop the refusal for a run that reported OK with no result for this key

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G10_absent_result`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_run_reporting_nothing_for_the_key_is_refused_rather_than_read_as_success`

Old text:

```
    if result is None:
        raise refuse(
            "unavailable-transient",
            f"{invocation.adapter} finished without reporting on {request.key}, "
            f"so nothing is known about it and it stays queued",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=True,
            origin=("acquire.cli",),
            detail={"adapter": invocation.adapter, "key": request.key},
        )

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G11_not_acquired`

Commit a per-track result that is not an acquisition

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G11_not_acquired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 8 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`

Old text:

```
    if result.outcome is not TrackOutcome.ACQUIRED:
        raise _refused_track(result, invocation.adapter)

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G12_landing_check`

Take the adapter's word for the landed file, skipping the policy check at the file

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G12_landing_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_an_unreadable_landing_is_transient_and_not_a_policy_refusal`
  - `tests/test_acquire_workers.py::test_the_frozen_policy_reaches_the_worker_not_the_live_one`
  - `tests/test_acquire_workers.py::test_the_refused_landing_left_as_evidence_survives_the_sweep`
  - `tests/test_acquire_workers.py::test_the_sweep_does_not_report_a_directory_it_could_not_remove`

Old text:

```
    landed = checked_landing(Path(str(result.path)), request.key, policy=per_item.lossless_policy)
```

New text:

```
    landed = Path(str(result.path))
```

### `u54-acquisition-worker.G14_marker_applied`

Commit a lossy landing under its unmarked name whatever the policy required

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G14_marker_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_the_permissive_policy_is_committed_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_with_no_marker_text_is_refused_rather_than_committed_unmarked`
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`

Old text:

```
    if not required:
        return landed.name

```

New text:

```
    return landed.name

```

### `u54-acquisition-worker.G15_no_marker_text`

Commit a lossy landing unmarked when the configuration names no marker text

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G15_no_marker_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_with_no_marker_text_is_refused_rather_than_committed_unmarked`

Old text:

```
    if not text:
        raise refuse(
            "lossy-refused",
            f"{landed.name} landed lossy under a policy that permits lossy only "
            f"when marked, and the configuration names no marker text, so it "
            f"cannot be marked and is not kept",
            remedy=Remedy.RELAX_LOSSLESS_POLICY,
            scope=Scope.ITEM,
            origin=("acquire.cli",),
            detail={"path": str(landed)},
        )

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G17_paced_sleep_bound`

Let the pool bind its own definition time sleep instead of the one the frozen configuration paces

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G17_paced_sleep_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_rate_limit_that_never_clears_fails_the_item_as_transient`
  - `tests/test_acquire_workers.py::test_the_pacing_delay_comes_from_the_frozen_configuration_not_a_fresh_load`

Old text:

```
    run = download.acquire_paced(adapter, (request,), sleep=_SLEEP)
```

New text:

```
    run = download.acquire_paced(adapter, (request,))
```

### `u54-acquisition-worker.G19_frozen_config`

Build the adapter settings from a fresh load rather than the configuration the job was frozen against

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G19_frozen_config`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 40 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_configuration_naming_an_unknown_adapter_fails_the_item_by_name`
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_a_deleted_frozen_list_named_relative_from_where_it_was_queued_still_drives`
  - `tests/test_acquire_workers.py::test_a_download_job_runs_pending_to_done_through_the_resume_path`
  - `tests/test_acquire_workers.py::test_a_lossless_landing_under_the_permissive_policy_is_not_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_the_permissive_policy_is_committed_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_partial_file_left_in_staging_does_not_poison_the_next_attempt`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_rate_limit_is_retried_under_backoff_and_then_lands`
  - `tests/test_acquire_workers.py::test_a_rate_limit_that_never_clears_fails_the_item_as_transient`
  - ... and 25 more, see the JSON sidecar

Old text:

```
    settings = AdapterSettings.from_config(cfg)
```

New text:

```
    settings = AdapterSettings.from_config(_load())
```

### `u54-acquisition-worker.G1_origin_refusal`

Queue a list from any provider, dropping the refusal that only the provider's own list carries acquirable identifiers

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G1_origin_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_pasted_tracklist_is_refused_at_the_queue_rather_than_queued_unacquirable`

Old text:

```
    if origin != match.TIDAL:
        raise _unusable(
            f"this is a {origin} list, and acquiring needs the provider's own track "
            f"identifiers, which only a list fetched from the provider carries",
            "fetch the playlist from the provider into a list document first, "
            "then acquire that",
            "a pasted tracklist is matched against the library with match.run; "
            "its missing rows carry acquisition options, not identifiers",
            origin=origin,
        )

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G20_output_exists`

Replace a file already at the destination instead of refusing

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G20_output_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_an_existing_file_at_the_destination_refuses_rather_than_replacing_it`

Old text:

```
    if final.exists():
```

New text:

```
    if False:
```

### `u54-acquisition-worker.G27_remedy_absent_stays_absent`

Restore the non-transient remedy fallback, so a delisted track is told to relax the lossless policy

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G27_remedy_absent_stays_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`

Old text:

```
        remedy=_remedy(result.remedy, Remedy.RETRY_LATER if transient else None),
```

New text:

```
        remedy=_remedy(result.remedy, Remedy.RETRY_LATER if transient else Remedy.RELAX_LOSSLESS_POLICY),
```

### `u54-acquisition-worker.G28_marker_decided_by_the_file`

Take the marker requirement from the offer's claim alone, so a lying offer commits an unmarked lossy file

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G28_marker_decided_by_the_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`

Old text:

```
    required = result.requires_lossy_marker or lossy_landing(
        landed, policy=per_item.lossless_policy
    )
```

New text:

```
    required = result.requires_lossy_marker
```

### `u54-acquisition-worker.G29_auth_failure_parks`

Fail the item on a dead credential instead of parking, so the driver re-authenticates once per remaining track

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G29_auth_failure_parks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_the_shipped_adapter_is_constructed_through_build_and_refuses_with_a_named_remedy`

Old text:

```
        if invocation.outcome is InvocationOutcome.AUTH_FAILED:
```

New text:

```
        if False:
```

### `u54-acquisition-worker.G2_missing_identifier`

Queue a provider list whose rows carry no identifier, dropping the by-position refusal

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G2_missing_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_row_without_an_identifier_is_refused_by_position`

Old text:

```
    if missing:
        raise _unusable(
            f"{len(missing)} track(s) in this list carry no provider identifier "
            f"(positions {', '.join(str(p) for p in missing[:5])}"
            f"{', ...' if len(missing) > 5 else ''}), so nothing can ask the "
            f"provider for them",
            "fetch the list from the provider again so every row carries its id",
            positions=missing,
        )

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G8_park_on_block`

Read a parked run as an ordinary result, so the driver claims the next item into a provider block

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G8_park_on_block`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`

Old text:

```
    if run.parked is not None:
        raise jobs.Parked(run.parked)

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G9_failed_invocation`

Ignore an invocation the adapter could not run at all

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G9_failed_invocation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_the_shipped_adapter_is_constructed_through_build_and_refuses_with_a_named_remedy`

Old text:

```
    if invocation.outcome in FAILED_INVOCATIONS:
```

New text:

```
    if False:
```

### `u54-zero-row-remeasured.G7_staging_cleared`

Keep whatever a killed attempt left in the item's staging directory, re-measured after the fake was taught to skip

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-zero-row-remeasured.json`, row `G7_staging_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_partial_file_left_in_staging_does_not_poison_the_next_attempt`

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)

```

New text:

```
(empty)
```

### `u172-b.C3_left_miscounted`

guess: count the files left as the candidates written rather than the files still without a genre

- File: `src/cratekit/cli/tail.py`
- Source: `u172-b.json`, row `C3_left_miscounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`
- Collected: 333 against a baseline of 333
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_the_files_left_are_the_files_still_without_a_genre`

Old text:

```
    left = count - after - unread
```

New text:

```
    left = count - before - written - unread
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

### `u179.T2_rehearsal_ack_attends`

rehearse: a missing acknowledgment at the rehearsal ends the verb as a failure, not for a person

- File: `src/cratekit/cli/tail.py`
- Source: `u179.json`, row `T2_rehearsal_ack_attends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing`

Old text:

```
        if cause.reason == ACK_STOP or cause.code in gates.GATE_CODES:
            raise Attend(REHEARSE, argv, cause)
```

New text:

```
        if cause.code in gates.GATE_CODES:
            raise Attend(REHEARSE, argv, cause)
```

### `u179.T3_rehearsal_stop_wording`

attended: word a rehearsal's acknowledgment stop as a landing's, naming no rehearsal

- File: `src/cratekit/cli/tail.py`
- Source: `u179.json`, row `T3_rehearsal_stop_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing`

Old text:

```
            if stop.step == REHEARSE
            else (f"then plan the landing again: crate {command}",)
```

New text:

```
            if False
            else (f"then plan the landing again: crate {command}",)
```

### `u179.T4_commands_quoted`

attended: join the step's command with plain spaces, so a batch folder with a space cannot be pasted

- File: `src/cratekit/cli/tail.py`
- Source: `u179.json`, row `T4_commands_quoted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 215 against a baseline of 215
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_failed_rehearsal_plans_no_live_landing`
  - `tests/test_sync_bandcamp.py::test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing`
  - `tests/test_sync_bandcamp_native.py::test_one_new_puls_release_and_one_owned_land_one_batch_filed_under_its_label`

Old text:

```
    command = shlex.join(stop.argv)
```

New text:

```
    command = " ".join(stop.argv)
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

### `u181.T2_rescore_ignores_profile`

tail.rescore: run the vocals verb on a profile with the vocals module off

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T2_rescore_ignores_profile`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_vocals_cli.py`
- Collected: 215 against a baseline of 215
- Kills: 30 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_a_landing_that_needs_the_backup_acknowledgment_stops_without_minting_one`
  - `tests/test_sync_land.py::test_a_name_apply_refusal_ends_the_pass_before_the_landing`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes`
  - `tests/test_sync_land.py::test_a_profile_with_the_vocals_module_off_is_not_asked`
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`
  - ... and 15 more, see the JSON sidecar

Old text:

```
    if not vocals_on(cfg):
        chain.summary["vocal_rescore"] = "off"
```

New text:

```
    if False:
        chain.summary["vocal_rescore"] = "off"
```

### `u181.T3_rescore_keeps_stale`

tail.rescore: leave a stale vocals job over the folder open

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T3_rescore_keeps_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_tails_rescore_replaces_a_stale_vocals_job_over_the_folder`

Old text:

```
        replace_stale(chain, ANALYZE, VOCALS_VERB, folder, cfg)
```

New text:

```
        pass
```

### `u181.T4_rescore_failure_ignored`

tail.rescore: a vocals job that did not succeed is reported scored and the chain goes on

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T4_rescore_failure_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_rescore_job_that_does_not_succeed_ends_the_chain_at_the_analyze_step`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED:
        raise Stop(ANALYZE, job_error(chain, job))
    chain.summary["vocal_rescore"] = count
```

New text:

```
    chain.summary["vocal_rescore"] = count
```

### `u181.T5_rescore_never_run`

tail.run: the analyze step never rescores

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T5_rescore_never_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 181 against a baseline of 181
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_profile_with_the_vocals_module_off_is_not_asked`
  - `tests/test_sync_land.py::test_the_analyze_step_rescores_after_analyze_run_and_before_the_restamp`
  - `tests/test_sync_land.py::test_the_answered_gate_takes_the_pass_on_and_the_summary_says_vocals_were_skipped`
  - `tests/test_sync_land.py::test_the_tail_asks_the_vocal_model_before_analyze_run_binds_its_loader`

Old text:

```
        if step == ANALYZE:
            rescore(chain, folder, cfg, unable=unable)
```

New text:

```
        if False:
            rescore(chain, folder, cfg, unable=unable)
```

### `u181.T6_plan_warnings_not_lifted`

tail.land: the landing gate screen's warnings are not lifted onto the chain

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T6_plan_warnings_not_lifted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 181 against a baseline of 181
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_warning_the_landing_plan_carries_rides_the_passes_own_warnings`

Old text:

```
        lift_plan_warnings(chain, cause)
```

New text:

```
        pass
```

### `u190.T1_run_folder_absolute`

run: trust the folder handed in as absolute

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T1_run_folder_absolute`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_chain_runs_on_the_absolute_folder_whatever_it_is_handed`

Old text:

```
    folder = folder.expanduser().absolute()
    chain.summary["staging"] = str(folder)
```

New text:

```
    chain.summary["staging"] = str(folder)
```

### `u190.T3_stale_matches_folder`

replace_stale: cancel open tail jobs over any folder, so another folder's work is lost

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T3_stale_matches_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_stale_job_over_another_folder_or_library_is_left_alone`

Old text:

```
            and str((job.payload or {}).get("folder") or "") == str(folder)
```

New text:

```
            and True
```

### `u190.T4_name_answers_inline`

name_argv: leave name apply's confirm unanswered, so the chain stops at a gate a person running the tail answers on the command line

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T4_name_answers_inline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_name_apply_has_its_confirm_answered_inline_over_the_absolute_staging_folder`
  - `tests/test_sync_land.py::test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`

Old text:

```
    return ["-d", f"{NAME_GATE}={NAME_OPTION}", "name", "apply", "--root", str(folder)]
```

New text:

```
    return ["name", "apply", "--root", str(folder)]
```

### `u190.T6_chain_namespace`

Chain.check: key every check sync.land whatever the chain, so the go's checks read as a sync pass's

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T6_chain_namespace`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 276 against a baseline of 276
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_landing_that_planned_nothing_ends_the_go_with_its_own_outcome`

Old text:

```
                "key": f"{self.namespace}.{step}",
```

New text:

```
                "key": f"sync.land.{step}",
```

### `u212.T1_reason_guard`

tail.second_copies: read any refusal's outstanding files, not only rename-incomplete's

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T1_reason_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1630 against a baseline of 1630
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_stop_that_is_not_rename_incomplete_or_cannot_read_the_queue_is_unchanged`

Old text:

```
    if cause.reason != RENAME_INCOMPLETE:
        return stop
```

New text:

```
(empty)
```

### `u212.T2_done_only`

tail._downloaded_by: a job that froze the track and never acquired it is named as its source

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T2_done_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1630 against a baseline of 1630
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_the_passes_named_are_this_librarys_finished_downloads_earliest_first`

Old text:

```
            if refs & done:
```

New text:

```
            if refs:
```

### `u212.T3_library`

tail._downloaded_by: another library's download job is named

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T3_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1630 against a baseline of 1630
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_the_passes_named_are_this_librarys_finished_downloads_earliest_first`

Old text:

```
            if cfg is not None and job.library_id != cfg.library.volume_id:
                continue
```

New text:

```
(empty)
```

### `u212.T4_earliest_first`

tail._downloaded_by: the passes named newest first, though the step says earliest first

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T4_earliest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1630 against a baseline of 1630
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_the_passes_named_are_this_librarys_finished_downloads_earliest_first`

Old text:

```
        for job in reversed(jobs.list_jobs(store)):
```

New text:

```
        for job in jobs.list_jobs(store):
```

### `u212.T5_name_wraps`

tail.name: the name step's stop passed on without the passes that downloaded the copy

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T5_name_wraps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1630 against a baseline of 1630
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_name_stop_over_a_second_copy_names_the_pass_that_downloaded_it`
  - `tests/test_sync_land_staged.py::test_a_second_copy_no_download_job_records_is_said_so`

Old text:

```
        raise second_copies(stop, cfg) from None
```

New text:

```
        raise stop from None
```

### `u284.T1_pass_names_nothing`

tail.tail_step: the pass never names the files the catalogues refused

- File: `src/cratekit/cli/tail.py`
- Source: `u284.json`, row `T1_pass_names_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_tag_guess.py`, `tests/test_tag_folder_copyright.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_with_a_token_the_pass_reaches_its_landing_and_names_the_refused_files`

Old text:

```
    if step == TAG:
        refused_files(chain, chain.settled.get(step))
```

New text:

```
    if False:
        refused_files(chain, chain.settled.get(step))
```

### `u284.T2_pass_stop_unsaid`

tail.tail_step: the pass's stop at its tag step says nothing of who refused or the token

- File: `src/cratekit/cli/tail.py`
- Source: `u284.json`, row `T2_pass_stop_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_tag_guess.py`, `tests/test_tag_folder_copyright.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
        raise Stop(step, refused_stop(error, chain.settled.get(step)) if step == TAG else error)
```

New text:

```
        raise Stop(step, error)
```

### `u319.M10_sync_stop_drops_the_short_path`

tail: the step crate sync land prints names one path again

- File: `src/cratekit/cli/tail.py`
- Source: `u319.json`, row `M10_sync_stop_drops_the_short_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_label_sync_go.py`
- Collected: 182 against a baseline of 182
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_the_sync_stop_offers_the_auto_analysis_path_after_the_selections_it_stands_in_for`

Old text:

```
    f"carrying the dyn My Tag, if any: {drift.DYNAMIC_SETTINGS}; "
    f"{AUTO_ANALYSIS_STEP}",
```

New text:

```
    f"carrying the dyn My Tag, if any: {drift.DYNAMIC_SETTINGS}",
```

### `u157.C1_at_the_cut`

verdict: at the cut reads steady

- File: `src/cratekit/core/drift.py`
- Source: `u157.json`, row `C1_at_the_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 126 against a baseline of 126
- Kills: 2 (killed)
- Killed:
  - `tests/test_drift.py::test_a_drift_at_or_above_the_cut_is_variable_and_no_measurement_is_unknown[at-the-cut]`
  - `tests/test_intake_land_dyn_native.py::test_a_landed_row_is_tagged_dyn_exactly_when_its_drift_reads_variable[exactly-at-the-cut]`

Old text:

```
VARIABLE if drift >= cut else STEADY
```

New text:

```
VARIABLE if drift > cut else STEADY
```

### `u157.C2_verdict_tag_trusted`

reading: a verdict tag with no score is read as itself, so a stray variable lands dyn

- File: `src/cratekit/core/drift.py`
- Source: `u157.json`, row `C2_verdict_tag_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 126 against a baseline of 126
- Kills: 5 (killed)
- Killed:
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[infinite]`
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[negative]`
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[not-a-number]`
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[verdict-without-score]`
  - `tests/test_intake_land_dyn_native.py::test_a_file_with_no_drift_reading_or_no_number_is_counted_unscored_and_untagged[lots-variable]`

Old text:

```
    if (verdict_text or "").strip() == UNKNOWN:
        return None, UNKNOWN
```

New text:

```
    if (verdict_text or "").strip() in VERDICTS:
        return None, (verdict_text or "").strip()
```

### `u157.C3_negative_score`

parse: accept a negative drift

- File: `src/cratekit/core/drift.py`
- Source: `u157.json`, row `C3_negative_score`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_a_landing_reads_the_score_against_the_cut_now_and_the_verdict_only_for_unknown[negative]`

Old text:

```
    if not math.isfinite(value) or value < 0.0:
```

New text:

```
    if not math.isfinite(value):
```

### `r154-a.A3_named_shape_check`

Never refuse a named snapshot on shape, which is the finding itself: the traversal value reaches the remote path again

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-a.json`, row `A3_named_shape_check`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 9 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[../another-library-snapshots/2020-01-01T000000Z]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-08-01T000000Z ]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-08-01T000000Z/../../elsewhere]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-08-01]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-13-01T000000Z]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-8-01T000000Z]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[newest]`
  - `tests/test_restore_cli.py::test_the_ledgers_traversal_value_is_refused_at_the_verb`

Old text:

```
        if not is_snapshot_name(snapshot):
```

New text:

```
        if False:
```

### `r154-a.A5_listing_filter`

List every folder under the snapshot root as a snapshot, so a stray folder sorting last is the newest

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-a.json`, row `A5_listing_filter`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_newest_snapshot_ignores_folders_that_are_not_stamps`

Old text:

```
            if is_snapshot_name(name)
```

New text:

```
            if name
```

### `r154-a.A7_read_normalization`

Compare a marker's identity as spelled on the remote, so a marker written in another letter case names a foreign volume

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-a.json`, row `A7_read_normalization`
- Moved: U311 split the snapshot listing out of backup.py into backup_snapshot.py with this line unchanged, and folded test_the_identity_is_compared_case_blind_like_the_volume_gate into test_a_snapshot_marked_for_this_library_is_planned_and_compared_case_blind, whose second half lists the same upper case marker and asserts the same lower case recorded volume, so it is the same guard held by the same assertion
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_marked_for_this_library_is_planned_and_compared_case_blind`

Old text:

```
        preflight.normalize_identity(name[len(IDENTITY_MARKER_PREFIX):])
```

New text:

```
        name[len(IDENTITY_MARKER_PREFIX):]
```

### `r154-a.A8_empty_expected`

Let an expected identity of nothing stay the empty string, so it matches a marker with nothing after its prefix

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-a.json`, row `A8_empty_expected`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_empty_expected_identity_never_matches_an_empty_marker[   ]`
  - `tests/modules/test_tools.py::test_an_empty_expected_identity_never_matches_an_empty_marker[]`

Old text:

```
    expected = (preflight.normalize_identity(wanted) or None) if wanted is not None else None
```

New text:

```
    expected = preflight.normalize_identity(wanted) if wanted is not None else None
```

### `r154-b.B1_named_mismatch`

Accept a named snapshot carrying ANY marker, which is the finding's real half: a well formed stamp from another library is pulled

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B1_named_mismatch`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 8 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_replaced_drive_restores_the_old_volumes_snapshot_by_naming_it`
  - `tests/modules/test_tools.py::test_a_snapshot_marked_for_another_library_is_refused`
  - `tests/modules/test_tools.py::test_an_empty_expected_identity_never_matches_an_empty_marker[   ]`
  - `tests/modules/test_tools.py::test_an_empty_expected_identity_never_matches_an_empty_marker[]`
  - `tests/modules/test_tools.py::test_two_identities_or_an_empty_marker_refuse_as_another_librarys`
  - `tests/modules/test_tools.py::test_two_markers_are_refused_without_offering_an_identity_to_pass`
  - `tests/test_restore_cli.py::test_another_librarys_snapshot_is_refused_at_the_verb_and_names_both_volumes`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`

Old text:

```
        if recorded == (expected,):
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
```

New text:

```
        if recorded:
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
```

### `r154-b.B2_two_markers`

Accept a named snapshot when the expected identity is AMONG its markers, so a folder two libraries wrote passes on either one

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B2_two_markers`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_two_identities_or_an_empty_marker_refuse_as_another_librarys`
  - `tests/modules/test_tools.py::test_two_markers_are_refused_without_offering_an_identity_to_pass`

Old text:

```
        if recorded == (expected,):
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
```

New text:

```
        if expected in recorded:
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
```

### `r154-b.B3_handed_down_stamp`

Ignore accept_unrecorded, so a stamp the verb resolved and handed down arrives looking typed and an unmarked one is pulled

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B3_handed_down_stamp`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_resolved_stamp_handed_down_is_not_mistaken_for_one_a_person_named`

Old text:

```
        accepted = True if accept_unrecorded is None else accept_unrecorded
```

New text:

```
        accepted = True
```

### `r154-b.B4_stated_volume_over_unmarked`

Pull an unmarked named snapshot even when a person stated the volume it should record, so the statement is checked against nothing

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B4_stated_volume_over_unmarked`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_replaced_drive_restores_the_old_volumes_snapshot_by_naming_it`

Old text:

```
        if not recorded and snapshot_volume is None and accepted:
```

New text:

```
        if not recorded and accepted:
```

### `r154-b.B5_veto_not_select`

Read only the newest folder, which is the first cut: a shared root refuses whenever the other library backed up last

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B5_veto_not_select`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_default_takes_the_newest_snapshot_that_is_this_librarys`
  - `tests/modules/test_tools.py::test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked`
  - `tests/modules/test_tools.py::test_the_replaced_drive_identity_selects_the_newest_of_the_old_volumes`

Old text:

```
    newest = names[::-1][:NEWEST_WALK]
```

New text:

```
    newest = names[::-1][:1]
```

### `r154-b.B6_walk_bound`

Multiply the walk bound by ten, so a remote of foreign snapshots is read far past what the refusal says it looked at

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B6_walk_bound`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked`

Old text:

```
NEWEST_WALK = 8
```

New text:

```
NEWEST_WALK = 80
```

### `r154-b.B7_walk_order`

Walk oldest first, so the default pulls the OLDEST snapshot that is this library's

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B7_walk_order`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_default_takes_the_newest_snapshot_that_is_this_librarys`
  - `tests/modules/test_tools.py::test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked`
  - `tests/modules/test_tools.py::test_the_replaced_drive_identity_selects_the_newest_of_the_old_volumes`
  - `tests/test_restore_cli.py::test_a_backup_landing_between_the_two_acts_moves_the_digest`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled_and_reported`

Old text:

```
    newest = names[::-1][:NEWEST_WALK]
```

New text:

```
    newest = names[:NEWEST_WALK]
```

### `r154-b.B8_walk_match`

Stop the walk at the first folder carrying ANY marker, so the default pulls another library's snapshot under a shared root

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B8_walk_match`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_default_takes_the_newest_snapshot_that_is_this_librarys`
  - `tests/modules/test_tools.py::test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked`
  - `tests/modules/test_tools.py::test_the_replaced_drive_identity_selects_the_newest_of_the_old_volumes`

Old text:

```
        if seen[name] == (expected,):
            return ResolvedSnapshot(stamp=name, recorded_volume=expected, named=False)
```

New text:

```
        if seen[name]:
            return ResolvedSnapshot(stamp=name, recorded_volume=expected, named=False)
```

### `r338-a.B3_capture_is_a_copy`

_plan_database: capture the share with copy and not sync, so a grid rekordbox deleted stays in the mirror for ever and the mirror stops being the share

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B3_capture_is_a_copy`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_outside_share_rides_the_database_portion_to_its_own_mirror`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`

Old text:

```
                    rclone, "sync", str(share), f"{kept}/current",
```

New text:

```
                    rclone, "copy", str(share), f"{kept}/current",
```

### `r338-a.B4_no_undo_archive`

_plan_database: drop the backup-dir, so a share emptied by a reinstall empties its only copy with nothing to undo it

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B4_no_undo_archive`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_outside_share_rides_the_database_portion_to_its_own_mirror`

Old text:

```
                    "--backup-dir", f"{kept}/archive/{stamp}",

```

New text:

```
(empty)
```

### `r338-a.B5_one_mirror_for_every_library`

share_destination: key every library's share under the one unrecorded folder, so two libraries under one snapshot root archive each other's grids

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B5_one_mirror_for_every_library`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_restore_puts_an_outside_share_back_beside_the_database`
  - `tests/test_analysis_store.py::test_an_outside_share_rides_the_database_portion_to_its_own_mirror`
  - `tests/test_analysis_store.py::test_an_unmarked_snapshot_pulls_this_librarys_share`
  - `tests/test_analysis_store.py::test_two_libraries_under_one_snapshot_root_keep_two_share_mirrors`

Old text:

```
    key = SHARE_UNRECORDED if marker is None else marker[len(IDENTITY_MARKER_PREFIX):]
```

New text:

```
    key = SHARE_UNRECORDED
```

### `r338-a.B6_identity_interpolated_raw`

share_destination: interpolate the configured identity as typed and unvalidated, so a value with a separator writes the share somewhere else on the remote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B6_identity_interpolated_raw`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_library_with_no_usable_identity_still_carries_its_share`
  - `tests/test_analysis_store.py::test_an_outside_share_rides_the_database_portion_to_its_own_mirror`
  - `tests/test_analysis_store.py::test_an_unmarked_snapshot_pulls_this_librarys_share`

Old text:

```
    key = SHARE_UNRECORDED if marker is None else marker[len(IDENTITY_MARKER_PREFIX):]
```

New text:

```
    key = SHARE_UNRECORDED if identity is None else identity
```

### `r338-a.B8_contained_share_copied_twice`

_outside_share: read every layout as the outside one, so a share the mirror already carries is synced a second time

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B8_contained_share_copied_twice`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 8 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_portion_with_no_prune_command_carries_no_warning`
  - `tests/modules/test_tools.py::test_the_prune_keeps_the_newest_removes_the_rest_and_warns_about_nothing`
  - `tests/test_analysis_store.py::test_a_contained_restore_neither_lists_nor_pulls_a_share`
  - `tests/test_analysis_store.py::test_a_contained_share_is_not_copied_twice`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`

Old text:

```
    if analysis_store.watch_roots(cfg) == (Path(cfg.library.root),):
        return None
    return analysis_store.share_root(cfg)
```

New text:

```
    if False:
        return None
    return analysis_store.share_root(cfg)
```

### `r338-b.R1_missing_directory_refuses`

share_is_held: stop reading rclone's missing directory exit as no mirror, so every backup older than this fix refuses its restore

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R1_missing_directory_refuses`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_the_share_is_listed_before_anything_is_cleared`

Old text:

```
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        return False
```

New text:

```
    if False:
        return False
```

### `r338-b.R4_empty_listing_read_as_held`

share_is_held: read a listing that names nothing as a mirror, so a copy from an empty folder is planned and reported as pulled

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R4_empty_listing_read_as_held`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_mirror_that_lists_empty_is_absent_too`

Old text:

```
    return bool(result.stdout.strip())
```

New text:

```
    return True
```

### `r338-b.R5_pulled_under_the_watch`

_plan_restore_inside_the_gates: stop withholding a landing place the analysis watch covers, the defect the built in review found: a live restore ends refused after the database is replaced

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R5_pulled_under_the_watch`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_that_would_land_under_the_analysis_watch_is_withheld_and_not_asked_about`

Old text:

```
        if not pull_share or analysis_store.is_watched(cfg, landing):
```

New text:

```
        if not pull_share:
```

### `r338-b.R6_switch_ignored`

_plan_restore_inside_the_gates: ignore pull_share, so the bare metal recovery asks the remote about a share it will not pull and can be refused over it

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R6_switch_ignored`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_caller_that_will_not_spend_the_database_half_is_not_refused_over_the_share`

Old text:

```
        if not pull_share or analysis_store.is_watched(cfg, landing):
```

New text:

```
        if analysis_store.is_watched(cfg, landing):
```

### `r338-b.R7_restore_is_a_sync`

_plan_restore_inside_the_gates: pull the share with sync, which deletes every analysis file beside the restored database that the mirror never saw

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R7_restore_is_a_sync`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_restore_puts_an_outside_share_back_beside_the_database`
  - `tests/test_analysis_store.py::test_a_restore_writes_the_share_with_a_copy_and_only_beside_the_database`

Old text:

```
                        rclone, "copy",
                        f"{share_destination(cfg, identity=whose)}/current",
```

New text:

```
                        rclone, "sync",
                        f"{share_destination(cfg, identity=whose)}/current",
```

### `r338-b.R8_unmarked_snapshot_orphans_the_share`

_plan_restore_inside_the_gates: drop the fallback to this library's identity, so a snapshot whose marker failed to write looks for its share under the unrecorded folder

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R8_unmarked_snapshot_orphans_the_share`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_unmarked_snapshot_pulls_this_librarys_share`

Old text:

```
        whose = resolved.recorded_volume or cfg.library.volume_id
```

New text:

```
        whose = resolved.recorded_volume
```

### `r338-b.R9_contained_restore_asks_about_a_share`

_plan_restore_inside_the_gates: treat every layout as the outside one on restore, so a contained library lists and pulls a share mirror it never wrote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R9_contained_restore_asks_about_a_share`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_contained_restore_neither_lists_nor_pulls_a_share`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`

Old text:

```
    share = ShareRestore.MIRRORED
    if _outside_share(cfg) is not None:
```

New text:

```
    share = ShareRestore.MIRRORED
    if True:
```

### `r338-c.C1_absent_share_never_said`

absent_analysis_share: never warn, so an outside share that is not a directory reads as a share that was carried

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-c.json`, row `C1_absent_share_never_said`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_outside_share_that_is_not_there_is_said_and_not_synced`
  - `tests/test_analysis_store.py::test_the_absent_share_warning_survives_a_refused_database_portion`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_that_is_absent_is_warned_at_queue_and_at_resume`
  - `tests/test_backup_cli.py::test_the_warnings_beside_a_reported_job_describe_that_job`

Old text:

```
    share = _outside_share(cfg)
    if share is None or share.is_dir():
        return ()
```

New text:

```
    share = _outside_share(cfg)
    if True:
        return ()
```

### `r338-c.C2_carried_share_still_warned`

absent_analysis_share: warn whenever the share is outside the root, carried or not, which is the retired warning back under a new code

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-c.json`, row `C2_carried_share_still_warned`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_outside_share_rides_the_database_portion_to_its_own_mirror`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`

Old text:

```
    share = _outside_share(cfg)
    if share is None or share.is_dir():
        return ()
```

New text:

```
    share = _outside_share(cfg)
    if share is None:
        return ()
```

### `r367.E2_an_unconfirmed_restore_is_allowed`

existing guard sample: a restore proceeds without the named decision

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `E2_an_unconfirmed_restore_is_allowed`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_restore_is_a_named_decision_and_never_a_prompt`

Old text:

```
    if not confirmed:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
```

New text:

```
    if confirmed and False:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
```

### `r367.E3_a_live_rekordbox_is_ignored`

existing guard sample: a restore proceeds while rekordbox holds the database

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `E3_a_live_rekordbox_is_ignored`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_restore_refuses_while_rekordbox_holds_the_database`

Old text:

```
    if running:
        raise BackupRefused(
            Refusal.REKORDBOX_RUNNING,
```

New text:

```
    if running and False:
        raise BackupRefused(
            Refusal.REKORDBOX_RUNNING,
```

### `r367.G12_listing_results_are_discarded`

the listing runs and its names are thrown away, so every sidecar is treated as absent

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G12_listing_results_are_discarded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_writes_back_the_log_and_never_the_shared_memory_index`

Old text:

```
    held = snapshot_filenames(cfg, chosen, runner=runner)
```

New text:

```
    snapshot_filenames(cfg, chosen, runner=runner)
    held = frozenset()
```

### `r367.G1_always_copy_the_restored_sidecar`

the original defect: copy every restored sidecar whether the snapshot holds it or not

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G1_always_copy_the_restored_sidecar`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 6 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-contents-2026-08-01T000000Z-holds no database folder]`
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/modules/test_tools.py::test_a_snapshot_that_cannot_be_listed_refuses_before_clearing`
  - `tests/modules/test_tools.py::test_the_snapshot_listing_is_of_the_database_folder`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
    held = snapshot_filenames(cfg, chosen, runner=runner)
    absent: list[str] = []
    for sidecar in config.state_file("rekordbox_db").sidecars:
        if not sidecar.restored:
            continue
        name = f"{database_target.name}{sidecar.suffix}"
        if name not in held:
            absent.append(sidecar.suffix)
            continue
        commands.append(

```

New text:

```
    absent: list[str] = []
    for sidecar in config.state_file("rekordbox_db").sidecars:
        if not sidecar.restored:
            continue
        name = f"{database_target.name}{sidecar.suffix}"
        commands.append(

```

### `r367.G3_membership_is_inverted`

copy the sidecar when it is absent and skip it when it is present

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G3_membership_is_inverted`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_writes_back_the_log_and_never_the_shared_memory_index`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
        if name not in held:
```

New text:

```
        if name in held:
```

### `r367.G4_the_inventory_restored_flag_is_ignored`

a listed shared memory index is written back beside a fresh log

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G4_the_inventory_restored_flag_is_ignored`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_writes_back_the_log_and_never_the_shared_memory_index`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
        if not sidecar.restored:
            continue

```

New text:

```
(empty)
```

### `r367.G5_absent_sidecars_are_not_recorded`

the plan copies nothing extra and also does not name what it skipped

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G5_absent_sidecars_are_not_recorded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
            absent.append(sidecar.suffix)

```

New text:

```
(empty)
```

### `r367.G7_the_listing_is_of_the_snapshot_root`

list the dated folder, not the db folder inside it, so the log is never seen

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G7_the_listing_is_of_the_snapshot_root`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_snapshot_listing_is_of_the_database_folder`

Old text:

```
                f"{cfg.backup.db_dest_root}/{snapshot}/db/",
```

New text:

```
                f"{cfg.backup.db_dest_root}/{snapshot}/",
```

### `r367.G8_files_only_is_dropped`

directories in the snapshot folder can be read as sidecar names

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G8_files_only_is_dropped`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_snapshot_listing_is_of_the_database_folder`

Old text:

```
                f"{cfg.backup.db_dest_root}/{snapshot}/db/",
                "--files-only",
```

New text:

```
                f"{cfg.backup.db_dest_root}/{snapshot}/db/",
```

### `r388-a.M1_named_identity_listing_back_to_absence`

A named snapshot whose identity marker listing exits 1 raises no-snapshot-available again, the defect the unit fixes

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M1_named_identity_listing_back_to_absence`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-identity]`
  - `tests/modules/test_tools.py::test_an_identity_listing_that_fails_is_not_read_as_an_unmarked_snapshot`

Old text:

```
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} could not "
            f"be listed, so which library
```

New text:

```
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} could not "
            f"be listed, so which library
```

### `r388-a.M2_identity_listing_message_reworded`

Reword could not be listed to could not be read in the identity listing refusal (R-387's row)

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M2_identity_listing_message_reworded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-identity]`

Old text:

```
could not "
            f"be listed, so which library
```

New text:

```
could not "
            f"be read, so which library
```

### `r388-a.M3_contents_listing_back_to_absence`

A named snapshot whose db folder listing exits 1 raises no-snapshot-available again

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M3_contents_listing_back_to_absence`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`
  - `tests/modules/test_tools.py::test_a_snapshot_that_cannot_be_listed_refuses_before_clearing`

Old text:

```
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} could not "
            f"be listed; a restore
```

New text:

```
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} could not "
            f"be listed; a restore
```

### `r388-a.M4_contents_listing_message_reworded`

Reword could not be listed to could not be read in the contents listing refusal, the sidecar row R-387 recorded as G9

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M4_contents_listing_message_reworded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`

Old text:

```
could not "
            f"be listed; a restore
```

New text:

```
could not "
            f"be read; a restore
```

### `r388-a.M5_root_listing_back_to_absence`

A snapshot root listing that exits 1 raises no-snapshot-available again

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M5_root_listing_back_to_absence`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_root_that_cannot_be_listed_is_not_reported_as_empty`

Old text:

```
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the dated database snapshots under {root} could not be listed
```

New text:

```
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the dated database snapshots under {root} could not be listed
```

### `r388-a.M6_root_listing_message_reworded`

Reword could not be listed to could not be read in the root listing refusal

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M6_root_listing_message_reworded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_root_that_cannot_be_listed_is_not_reported_as_empty`

Old text:

```
snapshots under {root} could not be listed, so 
```

New text:

```
snapshots under {root} could not be read, so 
```

### `r388-b.M10_named_stamp_absent_read_as_failure`

Drop the exit 3 branch on the identity listing, so a mistyped stamp sends the person to the remote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M10_named_stamp_absent_read_as_failure`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-identity-2026-08-01T000000Z-the snapshot 2026-08-01T000000Z was not found]`

Old text:

```
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A mistyped or pruned stamp.
```

New text:

```
    if False:
        # A mistyped or pruned stamp.
```

### `r388-b.M11_db_folder_absent_read_as_failure`

Drop the exit 3 branch on the contents listing, so a cut off backup sends the person to the remote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M11_db_folder_absent_read_as_failure`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-contents-2026-08-01T000000Z-holds no database folder]`

Old text:

```
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A backup cut off before its database folder was written.
```

New text:

```
    if False:
        # A backup cut off before its database folder was written.
```

### `r388-b.M7_share_listing_back_to_absence`

An analysis share listing that exits 1 raises no-snapshot-available again

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M7_share_listing_back_to_absence`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_mirror_that_could_not_be_listed_refuses_before_the_sidecars_go`

Old text:

```
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the analysis share mirror
```

New text:

```
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the analysis share mirror
```

### `r388-b.M8_share_listing_message_reworded`

Reword could not be listed to could not be read in the share listing refusal

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M8_share_listing_message_reworded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_mirror_that_could_not_be_listed_refuses_before_the_sidecars_go`

Old text:

```
could not "
            f"be listed (exit {result.returncode})
```

New text:

```
could not "
            f"be read (exit {result.returncode})
```

### `r388-b.M9_root_absent_read_as_failure`

Drop the exit 3 branch on the root listing, so a root no backup wrote is a listing failure

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M9_root_absent_read_as_failure`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshots-None-no dated database snapshot was found]`

Old text:

```
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A root no backup has written yet is an empty root, not a remote that
        # did not answer, and its answer is to take a backup.
        return ()

```

New text:

```
(empty)
```

### `r592-b.B6_restore_mirror_carries_the_database`

_plan_restore_inside_the_gates: exclude volume clutter only from the restore mirror, so a mirror still holding the database lands it where the database half writes

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r592-b.json`, row `B6_restore_mirror_carries_the_database`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_backup_cli.py`, `tests/test_restore.py`
- Collected: 22808 against a baseline of 22808
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    rclone, "copy", str(cfg.backup.dest), str(target),
                    *_exclude_args(_mirror_excludes(cfg)),
```

New text:

```
                    rclone, "copy", str(cfg.backup.dest), str(target),
                    *_exclude_args(VOLUME_EXCLUDES),
```

### `u211.B1_backup_database_portion_refuses_alone`

backup _plan_database: let the unconfirmed refusal escape the plan, so the files portion is lost with the database portion

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `u211.json`, row `B1_backup_database_portion_refuses_alone`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_backup_cli.py`, `tests/test_analysis_store.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_backup_refuses_the_database_portion_alone_and_still_mirrors`

Old text:

```
    except AbsenceUnconfirmed as exc:
        return PortionPlan(
```

New text:

```
    except LookupError as exc:
        return PortionPlan(
```

### `u27-restore-cli-independent.X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore`

What the from-backup zeros DO leave held: remove the refusal that stops a restore with no recorded decision, in the backup module the verb calls. Paired with I_A1 and with the whole from-backup family of zeros, which are one hole rather than eleven

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `u27-restore-cli-independent.json`, row `X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 430 against a baseline of 430
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_restore_is_a_named_decision_and_never_a_prompt`
  - `tests/test_write_session.py::test_the_restore_is_the_recovery_and_reaches_its_own_refusals`
  - `tests/test_write_session.py::test_the_restores_own_refusals_survive_the_gates_being_added`

Old text:

```
    if not confirmed:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
            "a restore replaces the live database and is not performed without an "
            "explicit decision naming this library and this snapshot.",
        )
```

New text:

```
(empty)
```

### `r1255.R5_organize_rotation_warns`

organize _rotation: drop the shared warning, so crate organize ages a batch unsaid

- File: `src/cratekit/organize/rekordbox.py`
- Source: `r1255.json`, row `R5_organize_rotation_warns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
    step.warnings.extend(rotate_cli.records_warnings(plan))
```

New text:

```
    pass
```

### `u112.R1_no_ack_planned`

With no backup acknowledgment the database area is planned and asked anyway

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R1_no_ack_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize.py::test_a_playlist_marked_twice_is_filed_by_its_latest_mark`
  - `tests/test_organize.py::test_a_year_folder_already_on_the_account_is_adopted_with_no_set_to_make_it`
  - `tests/test_organize.py::test_an_answer_ahead_of_a_gate_the_continue_may_not_reach_promises_no_stop_there`
  - `tests/test_organize.py::test_only_files_digest_is_not_the_full_areas_and_an_answer_over_one_is_stale_for_the_other`
  - `tests/test_organize.py::test_the_plan_is_empty_and_still_asks_when_the_root_is_clean`
  - `tests/test_organize.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
        if not report:
            area.cause = unacknowledged.cause
            return area
```

New text:

```
        if False:
            area.cause = unacknowledged.cause
            return area
```

### `u112.R2_applied_entries_outstanding`

Adoption plans every placeable entry, the ones a finished apply already filed included

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R2_applied_entries_outstanding`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`

Old text:

```
        pending = apply_engine.outstanding(plan, apply_engine.read(cfg))
```

New text:

```
        pending = plan.applicable()
```

### `u112.R3_bridge_tree_planned`

Adoption over a routing tree still on the bridge is planned rather than refused

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R3_bridge_tree_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_an_area_with_nothing_to_do_still_asks`

Old text:

```
    if not registry.is_database_native(declared.tree.id):
```

New text:

```
    if False:
```

### `u112.R4_job_without_gate_run`

The adoption job is queued with no gate run, so its resume can never be answered

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R4_job_without_gate_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_adoption_job_carries_a_run_its_own_resume_can_answer`

Old text:

```
                    jobs.GATE_RUN_KEY: gate_run,

```

New text:

```
(empty)
```

### `u112.R5_actor_invented`

The adoption job's approving actor is the process rather than the person who answered

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R5_actor_invented`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_adoption_job_carries_a_run_its_own_resume_can_answer`

Old text:

```
                    apply_cli.ACTOR_KEY: decision.actor if decision is not None else "",
```

New text:

```
                    apply_cli.ACTOR_KEY: "cli",
```

### `u112.R7_every_batch_suggested`

Every batch is suggested a rename, a readably named one included

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R7_every_batch_suggested`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_what_the_author_made_is_listed_with_a_home_and_never_a_write`

Old text:

```
        if batch.recognised_by == rotate.BY_SUFFIX:
```

New text:

```
        if True:
```

### `u112.R8_inbox_mine_unlisted`

A playlist of the author's that the rotation leaves alone under INBOX is not listed

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R8_inbox_mine_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_what_the_author_made_is_listed_with_a_home_and_never_a_write`

Old text:

```
    for node in plan.left:
```

New text:

```
    for node in ():
```

### `u137.R1_adopt_gate`

Plan the adoption whatever the selection

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R1_adopt_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
    if area.wants(ADOPT):
```

New text:

```
    if True:
```

### `u137.R2_rotation_for_yours`

Skip the rotation plan when yours is selected without rotate

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R2_rotation_for_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
    if area.wants(ROTATE) or area.wants(YOURS):
```

New text:

```
    if area.wants(ROTATE):
```

### `u137.R3_refused_rotation_shown`

Hide a rotation that refused when it was planned only for yours

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R3_refused_rotation_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
        if area.wants(ROTATE) or rotation.cause is not None:
```

New text:

```
        if area.wants(ROTATE):
```

### `u137.R4_rotation_shown_unselected`

Show a planned rotation that was planned only for yours

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R4_rotation_shown_unselected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`

Old text:

```
        if area.wants(ROTATE) or rotation.cause is not None:
```

New text:

```
        if True:
```

### `u137.R5_record_labels_gate`

Plan the record labels listing whatever the selection

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R5_record_labels_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_only_a_database_kind_asks_the_database_alone`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
    if area.wants(RECORD_LABELS):
```

New text:

```
    if True:
```

### `u144-c.C5_export_module`

Area: plan the step with the export module off

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u144-c.json`, row `C5_export_module`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_profile_without_the_export_module_lists_the_step`

Old text:

```
    if available is not None and EXPORT_MODULE not in available:
```

New text:

```
    if False:
```

### `u144-c.C6_native_only`

Area: drop the refusal of an intake tree still on the xml bridge

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u144-c.json`, row `C6_native_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_an_intake_tree_on_the_bridge_refuses_the_step`

Old text:

```
        set_playlist.assert_native(ingest.intake_medium(cfg), landing=False)
```

New text:

```
        pass
```

### `u144-c.C7_folder_warning`

Area: warn only for an unread set, not for an unread sets folder

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u144-c.json`, row `C7_folder_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_sets_folder_that_cannot_be_listed_is_named_and_the_rest_still_plan`

Old text:

```
        if row.action in (inspiration.UNREAD, inspiration.FOLDER_UNREAD)
```

New text:

```
        if row.action == inspiration.UNREAD
```

### `u185.R1_organize_not_yours`

organize: list the DEADCA7 folder among the author's own with a home

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u185.json`, row `R1_organize_not_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_deadca7s_folder_is_named_once_as_foreign_and_a_full_apply_leaves_it_as_it_was`

Old text:

```
        if name in declared_roots or str(row.ID) in foreign:
```

New text:

```
        if name in declared_roots:
```

### `u185.R2_organize_fact`

organize: name the folder nowhere, so the report is silent about it

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u185.json`, row `R2_organize_fact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_deadca7s_folder_is_named_once_as_foreign_and_a_full_apply_leaves_it_as_it_was`

Old text:

```
    if foreign:
        area.facts[FOREIGN_FACT]
```

New text:

```
    if foreign and False:
        area.facts[FOREIGN_FACT]
```

### `u214.M14_old_not_yours`

organize rotation step: list Old as the author's own again

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u214.json`, row `M14_old_not_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_organize_rotation_step_does_not_list_old_as_yours`

Old text:

```
        if node.kind == rotate.LEFT_OLD:
```

New text:

```
        if False:
```

