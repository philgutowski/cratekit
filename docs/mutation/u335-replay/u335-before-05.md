# Mutation table: u335-before-05

Measured by `scripts/mutate.py` on 2026-11-24 05:31 UTC, branch `HEAD` at `8a92a344`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 271.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 05:31 UTC for commit `8a92a344ad01`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 52, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u128.L1_bridge_warning_unsaid` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 26 | 3 | killed |
| `u129-author.A19_plan_archive_always_none` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 56 | 3 | killed |
| `u307.R21_unrunnable_reason_lost` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 152 | 3 | killed |
| `u307.R4_land_cli_getattr_answers_none` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 116 | 23 | killed |
| `u72-b.M20_shown_files` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72-b.M21_empty_to_engine` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72-b.M22_listing_without_isdir` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M10_default_folder` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 19 | killed |
| `u72.M1_abort_applies` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 2 | killed |
| `u72.M2_empty_plan_applied` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M3_digest_drops_where` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M5_digest_drops_export` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 2 | killed |
| `u72.M9_default_name_colons` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u77-c.C6_gate_manifest_bytes` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-c.C7_digest_handed_to_engine` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-c.C8_unfiled_rows_warned` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 254 | 2 | killed |
| `r770-b.B2_gate_asked_before_the_acknowledgment` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 77 | 2 | killed |
| `r770-b.B3_an_abort_writes` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 77 | 2 | killed |
| `u126.P3_gate_fact` | `src/cratekit/intake/land_native.py` | user | 10 file(s) | 438 | 4 | killed |
| `u127.L7_land_warnings_unsaid` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 7 | killed |
| `u129-author.A4_archive_raise_fails_landing` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 76 | 2 | killed |
| `u129-author.A5_archive_return_discarded` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 76 | 2 | killed |
| `u135.A3_found_vs_made_collapsed` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 9 | 6 | killed |
| `u166.A11_warning_names_batch` | `src/cratekit/intake/land_native.py` | user | 7 file(s) | 185 | 3 | killed |
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
| `r746-b.N9_placement_check_dropped_from_the_screen` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 110 | 3 | killed |
| `r770-c.C3_failure_past_the_gate_loses_its_reason` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-c.C4_failure_past_the_gate_loses_its_remedy` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 33 | 1 | killed |
| `u110-c.C1_apply_playlist` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 201 | 8 | killed |
| `u110-c.C7_intake_lock_prefix` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 201 | 13 | killed |
| `u110-c.C8_plain_dot` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 201 | 3 | killed |
| `u113-b.B5_export_clash_unasked` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 65 | 1 | killed |
| `u113-b.B6_root_names_unheld` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 26 | 1 | killed |
| `u128-b.B1_engine_stale_unchecked` | `src/cratekit/intake/landing.py` | user | 10 file(s) | 271 | 1 | killed |
| `u128-b.B2_foreign_host_indexed` | `src/cratekit/intake/landing.py` | user | 10 file(s) | 271 | 1 | killed |
| `u156.L25_shared_rule_near_match` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 69 | 1 | killed |
| `u307.R6_refuse_past_drops_inner_message` | `src/cratekit/intake/landing.py` | user | 4 file(s) | 110 | 4 | killed |
| `u71-b.B10_occupied_at_move` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 2 | killed |
| `u71-b.B11_nothing_moved` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71-b.B12_take_back_folder` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71-b.B13_unlink_destination` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
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
| `u77-a.A1_label_source_filter` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-a.A2_engine_stale_digest` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 16 | killed |
| `u77-a.A4_export_reason_mapping` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 2 | killed |
| `u77-a.A5_needs_review_guard` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-a.A6_no_landed_file_guard` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 5 | killed |
| `u77-a.A7_year_absent_guard` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-a.A8_library_template` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-a.A9_this_runs_files_only` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-a2.A2_engine_stale_digest` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-b.B1_reported_ids_deduped` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-b.B2_disk_refusal_reported` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-b.B3_index_refusal_reported` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-b.B5_unmatched_sentence` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 1 | killed |
| `r503-a.G10_owned_key` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 86 | killed |
| `u115.F1_landing_keeps_random_id` | `src/cratekit/intake/native.py` | user | 6 file(s) | 197 | 27 | killed |
| `u121.S21_landing_skips_set` | `src/cratekit/intake/native.py` | user | 1 file(s) | 56 | 15 | killed |
| `u121.S22_record_unnamed` | `src/cratekit/intake/native.py` | user | 1 file(s) | 56 | 5 | killed |
| `u126.P2_not_shown` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 4 | killed |
| `u126.R1_binding_value_kept` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 37 | killed |
| `u126.R2_fill_if_null` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 37 | killed |
| `u126.R5_read_back_file_id` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 37 | killed |
| `u126.S1_file_id_kept` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 38 | killed |
| `u127.N14_read_back_skipped` | `src/cratekit/intake/native.py` | user | 9 file(s) | 253 | 4 | killed |
| `u127.N8_tag_never_written` | `src/cratekit/intake/native.py` | user | 9 file(s) | 253 | 6 | killed |
| `u127.N9_tag_every_added` | `src/cratekit/intake/native.py` | user | 9 file(s) | 253 | 50 | killed |
| `u135.A14_set_order_reverses` | `src/cratekit/intake/native.py` | user | 2 file(s) | 65 | 2 | killed |
| `u135.A1_removed_namesake_written_into` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A2_set_order_falls_to_name_order` | `src/cratekit/intake/native.py` | user | 1 file(s) | 9 | 1 | killed |
| `u135.A8_job_key_not_stamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 9 | 4 | killed |
| `u166.A4_no_add` | `src/cratekit/intake/native.py` | user | 7 file(s) | 185 | 14 | killed |
| `u166.A7_record_count` | `src/cratekit/intake/native.py` | user | 7 file(s) | 185 | 5 | killed |
| `r1255.N1_landings_of_pass_refuses` | `src/cratekit/intake/native_plan.py` | user | 2 file(s) | 84 | 2 | killed |
| `r1255.N2_landed_passes_refuses` | `src/cratekit/intake/native_plan.py` | user | 2 file(s) | 84 | 1 | killed |
| `r770-d.C7_unresolved_target_planned_as_an_add` | `src/cratekit/intake/native_plan.py` | user | 2 file(s) | 77 | 1 | killed |
| `r777.N15_any_pass` | `src/cratekit/intake/native_plan.py` | user | 6 file(s) | 197 | 2 | killed |
| `u126.P1_no_read` | `src/cratekit/intake/native_plan.py` | user | 7 file(s) | 210 | 7 | killed |
| `u127.N1_cut_strict` | `src/cratekit/intake/native_plan.py` | user | 9 file(s) | 253 | 2 | killed |
| `u127.N3_default_cut_when_uncalibrated` | `src/cratekit/intake/native_plan.py` | user | 9 file(s) | 253 | 2 | killed |
| `u135.A13_live_inbox_ignores_parent` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 9 | 1 | killed |
| `u135.A5_recorded_inbox_skips_job_key` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 9 | 1 | killed |
| `u135.A7_leftover_joins_numbered_twin` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 1 | 1 | killed |
| `u174.N1_landed_passes_closed` | `src/cratekit/intake/native_plan.py` | user | 3 file(s) | 210 | 1 | killed |
| `u174.N2_landed_passes_committed` | `src/cratekit/intake/native_plan.py` | user | 3 file(s) | 210 | 1 | killed |
| `u174.N3_landed_passes_workflow` | `src/cratekit/intake/native_plan.py` | maintainer | 3 file(s) | 210 | 1 | killed |
| `u174.N4_landed_passes_pass_key` | `src/cratekit/intake/native_plan.py` | maintainer | 3 file(s) | 210 | 1 | killed |
| `u37-author-light.G2_recognition_gate` | `src/cratekit/intake/recognize.py` | user | 1 file(s) | 8 | 1 | killed |
| `r1255.F2_refill_warning_wording` | `src/cratekit/intake/refill_cli.py` | user | 2 file(s) | 28 | 2 | killed |
| `r1255.R1_rotation_unlisted_from_scan` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 72 | 2 | killed |
| `r1255.R3_rotation_warning_gate` | `src/cratekit/intake/rotate_cli.py` | user | 3 file(s) | 72 | 3 | killed |
| `r1255.R4_rotation_warning_wording` | `src/cratekit/intake/rotate_cli.py` | user | 3 file(s) | 72 | 2 | killed |
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
| `u121.S5_missing_word` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 6 | killed |
| `u121.S7_job_handler` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121.S9_two_folders` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u129-author.A18_frozen_name_ignored` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 20 | 2 | killed |
| `u135.A12_inspiration_join_broken` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 9 | 1 | killed |
| `u144-c.C9_parent_of_named` | `src/cratekit/intake/set_playlist.py` | user | 2 file(s) | 94 | 10 | killed |
| `u246.S3_set_playlist_order_set_empty` | `src/cratekit/intake/set_playlist.py` | user | 5 file(s) | 300 | 22 | killed |
| `u307.R17_made_on_drops_posted` | `src/cratekit/intake/set_playlist.py` | user | 3 file(s) | 114 | 1 | killed |
| `u307.R19_flag_day_invalid_date_unrefused` | `src/cratekit/intake/set_playlist.py` | user | 2 file(s) | 94 | 3 | killed |
| `u108-c.G21_listing_skips_already` | `src/cratekit/label/approved_cli.py` | user | 4 file(s) | 364 | 2 | killed |
| `u108-c.G22_listing_excuse_applies` | `src/cratekit/label/approved_cli.py` | user | 4 file(s) | 364 | 1 | killed |
| `r382.M16_parser_moved_lowercase` | `src/cratekit/label/catalogue.py` | maintainer | 10 file(s) | 805 | 2 | killed |
| `r504-a.A10_block_listed` | `src/cratekit/label/catalogue.py` | user | 10 file(s) | 805 | 11 | killed |
| `r504-a.A8_withheld_sign` | `src/cratekit/label/catalogue.py` | user | 10 file(s) | 805 | 15 | killed |
| `r504-a.A9_summary_reworded` | `src/cratekit/label/catalogue.py` | user | 10 file(s) | 805 | 10 | killed |
| `r504-a.A11_boundary_refuses` | `src/cratekit/label/cli.py` | user | 4 file(s) | 0 | collection error | collect-error |
| `r504-a.A12_boundary_drops_short` | `src/cratekit/label/cli.py` | user | 4 file(s) | 552 | 5 | killed |
| `r1115.G3_warn_each_failed_track` | `src/cratekit/label/go.py` | user | 2 file(s) | 205 | 2 | killed |
| `r1115.G4_name_the_refused_on_the_check` | `src/cratekit/label/go.py` | user | 2 file(s) | 205 | 2 | killed |
| `r1115.G5_every_refused_fails_the_check` | `src/cratekit/label/go.py` | user | 2 file(s) | 205 | 4 | killed |
| `r1115.G6_no_commands_over_nothing` | `src/cratekit/label/go.py` | user | 2 file(s) | 205 | 2 | killed |
| `r1115.G8_report_names_the_refused` | `src/cratekit/label/go.py` | user | 2 file(s) | 205 | 4 | killed |
| `r1115.G9_resume_no_commands_over_nothing` | `src/cratekit/label/go.py` | user | 2 file(s) | 205 | 1 | killed |
| `r1467.M01_fresh_go_checks_before_gate` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 15 | killed |
| `r1467.M02_resumed_jobs_are_own` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 14 | killed |
| `r1467.M03_fresh_tail_checks_after_drive` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 14 | killed |
| `r1467.M04_resume_tail_checks` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `r1467.M05_carry_on_checks` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 14 | killed |
| `r1467.M14_carry_on_reads_the_record` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 2 | killed |
| `r1467.M15_beside_keeps_later_jobs` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 2 | killed |
| `r1467.M17_walk_answers_kept` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `r1467.M18_refused_tracks_carried` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 2 | killed |
| `r1467.M25_own_pass_handed_to_beside` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u108-a.G02_pick_takes_releases` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 2 | killed |
| `u108-a.G03_not_now_counted` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-a.G04_digest_covers_releases` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-a.G06_abort_downloads_nothing` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 2 | killed |
| `u108-a.G07_only_accepted_downloaded` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-a.G08_already_passed_to_listing` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 2 | killed |
| `u108-a.G09_gone_excused` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-b.G10_unread_answer_kept` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-b.G13_closed_job_retried` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-b.G15_time_pacing_coefficient` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-b.G17_done_tracks_held` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 2 | killed |
| `u108-c.G23_job_carries_origin` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 64 | killed |
| `u108-d.G11_waited_go_refuses_again` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-d.G14_retryable_cause_only_again` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-d.G16_origin_marker_filter_again` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 7 | killed |
| `u110-c.C4_go_tail` | `src/cratekit/label/go.py` | user | 2 file(s) | 130 | 2 | killed |
| `u190.G5_resume_one_job_only` | `src/cratekit/label/go.py` | user | 2 file(s) | 23216 | 0 (promoted) | zero |
| `u239-composites.M11b_land_only_landed_after_its_test` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 3 | killed |
| `u239.M01_own_needs_apply` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M02_own_skips_cancelled` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M03_own_job_by_run` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 13 | killed |
| `u239.M04_go_takes_own_on` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 19 | killed |
| `u239.M05_beside_later_only` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 8 | killed |
| `u239.M06_beside_open` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M07_beside_done` | `src/cratekit/label/go.py` | user | 3 file(s) | 23216 | 0 (promoted) | zero |
| `u239.M08_retry_half_failed` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M09_named_landing` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 4 | killed |
| `u239.M14_ceiling_fresh` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M15_ceiling_job_id` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 2 | killed |
| `u239.M16_other_stop_step` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 2 | killed |
| `u239.M17_wrote` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u252.L7_seam_drops_keywords` | `src/cratekit/label/harvest.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `r1056.N10_pass_not_required` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N1_no_refusal_of_an_unreadable_record` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 7 | killed |
| `r1056.N2_first_landing_only` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N3_years_from_the_argument` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N4_no_landings_in_digest` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `r1056.N5_no_reread_before_rename` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N6_no_nothing_filed_warning` | `src/cratekit/label/mark_cli.py` | user | 2 file(s) | 89 | 4 | killed |
| `r1056.N7_nothing_filed_against_any_year` | `src/cratekit/label/mark_cli.py` | user | 2 file(s) | 89 | 1 | killed |
| `r1056.N8_shown_pass_bare` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |

## Zero rows and what they owe

- `u71-b.B13_unlink_destination` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u190.G5_resume_one_job_only` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u239.M07_beside_done` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u128.L1_bridge_warning_unsaid`

The bridge landing does not put the left rows on its warnings

- File: `src/cratekit/intake/land_cli.py`
- Source: `u128.json`, row `L1_bridge_warning_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`

Old text:

```
            *account_playlists.left_warning((*emptied, *landed.left)),
```

New text:

```
            *account_playlists.left_warning(()),
```

### `u129-author.A19_plan_archive_always_none`

A set landing never plans the account archive

- File: `src/cratekit/intake/land_cli.py`
- Source: `u129-author.json`, row `A19_plan_archive_always_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 3 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[not-renamed]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[raised]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`

Old text:

```
    try:
        return set_cli.plan_archive_named(cfg, name, pass_name=pass_name)
    except CratekitError:
        # Soft: the landing still lands; archive can run later via export archive.
        return None

```

New text:

```
    return None

```

### `u307.R21_unrunnable_reason_lost`

land_cli._unrunnable: a command line the landing cannot run is refused as internal-error, not intake-list-unusable

- File: `src/cratekit/intake/land_cli.py`
- Source: `u307.json`, row `R21_unrunnable_reason_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_land.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_intake_land_rehearse.py`
- Collected: 152 against a baseline of 152
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_rekordbox_running_or_an_export_on_a_native_tree_is_refused_before_the_gate`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_on_the_bridge_is_refused`
  - `tests/test_set_inspiration_playlist.py::test_a_playlist_job_named_with_set_is_refused_before_anything_moves`

Old text:

```
        "intake-list-unusable", message, remedy=Remedy.FIX_COMMAND_LINE, steps=steps,
```

New text:

```
        "internal-error", message, remedy=Remedy.FIX_COMMAND_LINE, steps=steps,
```

### `u307.R4_land_cli_getattr_answers_none`

land_cli.__getattr__: answer None for every native medium name read on the verb's module, so ask_then_write, the warning codes and the analysis step read as nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `u307.json`, row `R4_land_cli_getattr_answers_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_owned_hearts_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`, `tests/test_inbox_analyzed.py`
- Collected: 116 against a baseline of 116
- Kills: 23 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses`
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`
  - `tests/test_intake_land_hearts_native.py::test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it`
  - `tests/test_intake_land_hearts_native.py::test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made`
  - `tests/test_intake_land_hearts_native.py::test_two_source_playlists_skip_the_placement_too`
  - `tests/test_intake_land_hearts_native.py::test_with_no_source_playlist_the_batch_lands_and_the_placement_is_skipped_and_said`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`
  - `tests/test_intake_writers_native.py::test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy`
  - `tests/test_intake_writers_native.py::test_a_file_already_in_the_collection_gains_a_membership_and_no_second_row`
  - `tests/test_intake_writers_native.py::test_a_file_named_through_a_link_is_stored_under_the_configured_root`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    return getattr(land_native, name)
```

New text:

```
    return None
```

### `u72-b.M20_shown_files`

The gate context lists no file names

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M20_shown_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
        "files": [item.name for item in planned.items],
```

New text:

```
        "files": [],
```

### `u72-b.M21_empty_to_engine`

An empty folder goes to the engine, which refuses it

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M21_empty_to_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`

Old text:

```
    if folder.is_dir() and not landing.listing(folder):
```

New text:

```
    if False:
```

### `u72-b.M22_listing_without_isdir`

The empty check lists a folder that may not exist

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M22_listing_without_isdir`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`

Old text:

```
    if folder.is_dir() and not landing.listing(folder):
```

New text:

```
    if not landing.listing(folder):
```

### `u72.M10_default_folder`

The default folder is the library root, not download staging

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M10_default_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 19 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_absent-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_no_intake_folder-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_not_a_collection-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_what_went_missing`
  - `tests/test_intake_land.py::test_a_refused_file_is_warned_and_marked`
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[a file arrived]`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.paths.download_staging)
```

New text:

```
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.library.root)
```

### `u72.M1_abort_applies`

An abort no longer stops the verb: only an empty plan returns NO_OP

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M1_abort_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_what_went_missing`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
    if option != "apply" or not planned.items:
```

New text:

```
    if not planned.items:
```

### `u72.M2_empty_plan_applied`

An empty plan is handed to the engine after the answer instead of returning NO_OP

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M2_empty_plan_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`

Old text:

```
    if option != "apply" or not planned.items:
```

New text:

```
    if option != "apply":
```

### `u72.M3_digest_drops_where`

The digest drops the batch, the target and the intake file, so an answer for one name applies under another

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M3_digest_drops_where`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[batch name]`

Old text:

```
        "batch": planned.batch,
        "target": str(target),
        "destination": str(destination),

```

New text:

```
(empty)
```

### `u72.M5_digest_drops_export`

The digest drops the export path

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M5_digest_drops_export`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[export]`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`

Old text:

```
        "export": str(export),

```

New text:

```
(empty)
```

### `u72.M9_default_name_colons`

The default batch name keeps the run id's colons

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M9_default_name_colons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`

Old text:

```
    return run_id.replace(":", "")
```

New text:

```
    return run_id
```

### `u77-c.C6_gate_manifest_bytes`

_payload: leave the manifest's bytes out of the plan identity, so the gate accepts an answer given against other rows (the gate layer alone, the engine's own check left in place)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u77-c.json`, row `C6_gate_manifest_bytes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`

Old text:

```
identity["manifest_bytes"] = manifest.digest
```

New text:

```
identity["manifest_bytes"] = ""
```

### `u77-c.C7_digest_handed_to_engine`

intake_land: hand the engine no fingerprint, so a manifest rewritten between the gate and the first move is filed

- File: `src/cratekit/intake/land_cli.py`
- Source: `u77-c.json`, row `C7_digest_handed_to_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`

Old text:

```
manifest_digest=manifest.digest if manifest is not None else None,
```

New text:

```
manifest_digest=None,
```

### `u77-c.C8_unfiled_rows_warned`

intake_land: warn about refused files only, so a label row filed under nothing is named nowhere a person reads

- File: `src/cratekit/intake/land_cli.py`
- Source: `u77-c.json`, row `C8_unfiled_rows_warned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`

Old text:

```
for entry in (*landed.refused, *landed.unlabelled)
```

New text:

```
for entry in (*landed.refused,)
```

### `r770-b.B2_gate_asked_before_the_acknowledgment`

ask_then_write: ask the gate without reading the backup acknowledgment first, on both verbs

- File: `src/cratekit/intake/land_native.py`
- Source: `r770-b.json`, row `B2_gate_asked_before_the_acknowledgment`
- Moved: the same acknowledgment read before the gate is asked, in the shared ask then write of the native landing, which U307 moved from land_cli.py to land_native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_acknowledgment_refuses_before_the_gate`
  - `tests/test_intake_writers_native.py::test_no_acknowledgment_refuses_before_the_gate`

Old text:

```
        session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `r770-b.B3_an_abort_writes`

ask_then_write: write whatever the answer was

- File: `src/cratekit/intake/land_native.py`
- Source: `r770-b.json`, row `B3_an_abort_writes`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_an_abort_moves_nothing_and_writes_nothing, test_an_abort_writes_nothing, were folded by the trim into test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database, test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database, the abort test's steps and checks, verbatim at the end of each file's gate screen test
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
        if option != "apply":
```

New text:

```
        if option == "never":
```

### `u126.P3_gate_fact`

Rename the content link fact on the gate screen, so the value and its count are not where the person reads them

- File: `src/cratekit/intake/land_native.py`
- Source: `u126.json`, row `P3_gate_fact`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 438 against a baseline of 438
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_link_its_count_the_playlist_and_each_file_move_the_digest`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
        "content link": (
```

New text:

```
        "link": (
```

### `u127.L7_land_warnings_unsaid`

intake land gives no vox warning

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L7_land_warnings_unsaid`
- Moved: Anchored where u307-replay-after-b.json replayed it: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_no_category]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_uncalibrated]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_unreadable]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
    warnings.extend(vox_warnings(landed.collection))
```

New text:

```
    warnings.extend([])
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

### `u135.A3_found_vs_made_collapsed`

The gate screen always says found-or-made when no recorded INBOX playlist is named

- File: `src/cratekit/intake/land_native.py`
- Source: `u135.json`, row `A3_found_vs_made_collapsed`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`, `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
- Collected: 9 against a baseline of 9
- Kills: 6 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined`
  - `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
  - `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`
  - `tests/test_u135_set_inbox_join.py::test_a_recorded_inbox_playlist_removed_before_the_next_landing_is_not_joined`
  - `tests/test_u135_set_inbox_join.py::test_a_removed_set_named_inbox_playlist_is_not_written_into`
  - `tests/test_u135_set_inbox_join.py::test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order`

Old text:

```
        if rows.batch_playlist_id:
            facts["inbox"] = (
                f"adds to the playlist an earlier landing of this set made "
                f"(row {rows.batch_playlist_id})"
            )
        elif rows.inbox_found_by_name:
            facts["inbox"] = "found live by name, not recorded"
        else:
            facts["inbox"] = "made"

```

New text:

```
        facts["inbox"] = (
            f"adds to the playlist an earlier landing of this set made "
            f"(row {rows.batch_playlist_id})"
            if rows.batch_playlist_id
            else "found live by its name under INBOX, or made"
        )

```

### `u166.A11_warning_names_batch`

awaiting_analysis: name the batch playlist again instead of Analyze

- File: `src/cratekit/intake/land_native.py`
- Source: `u166.json`, row `A11_warning_names_batch`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`

Old text:

```
                f"{collection.analyze_name} playlist, which holds every row waiting "
```

New text:

```
                f"{collection.playlist} playlist, which holds every row waiting "
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

### `u110-c.C1_apply_playlist`

The xml landing no longer hands its batch name to the splice, so the playlist is the intake file's stem again

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C1_apply_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 201 against a baseline of 201
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
- Collected: 201 against a baseline of 201
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
- Collected: 201 against a baseline of 201
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

### `u128-b.B1_engine_stale_unchecked`

The bridge engine does not read the owned entries again before its first move

- File: `src/cratekit/intake/landing.py`
- Source: `u128-b.json`, row `B1_engine_stale_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 271 against a baseline of 271
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
- Collected: 271 against a baseline of 271
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

### `u307.R6_refuse_past_drops_inner_message`

landing.refuse_past: leave the inner failure's own sentence out of the message, so a person reads what was left but not what failed

- File: `src/cratekit/intake/landing.py`
- Source: `u307.json`, row `R6_refuse_past_drops_inner_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_land_dyn_native.py`, `tests/test_intake_writers_native.py`
- Collected: 110 against a baseline of 110
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[UPDATE djmdContent SET BPM = 12400 WHERE ID = :id-BPM]`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[UPDATE djmdContent SET KeyID = '283157525' WHERE ID = :id-KeyID]`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[sql2-djmdMixerParam]`
  - `tests/test_intake_writers_native.py::test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy`

Old text:

```
        f"{head} ({inner.message if inner is not None else exc}); {tail}",
```

New text:

```
        f"{head}; {tail}",
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

### `u71-b.B13_unlink_destination`

Leave the intake file behind when place_files fails after writing it

- File: `src/cratekit/intake/landing.py`
- Source: `u71-b.json`, row `B13_unlink_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        destination.unlink(missing_ok=True)

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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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

### `u115.F1_landing_keeps_random_id`

The native landing keeps the random rb_file_id the binding minted instead of the landed file's inode

- File: `src/cratekit/intake/native.py`
- Source: `u115.json`, row `F1_landing_keeps_random_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 197 against a baseline of 197
- Kills: 27 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[None]`
  - ... and 12 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.FILE_ID_COLUMN, file_id_of(row.target))

```

New text:

```
(empty)
```

### `u121.S21_landing_skips_set`

apply_rows: the landing's commit never writes the set playlist

- File: `src/cratekit/intake/native.py`
- Source: `u121.json`, row `S21_landing_skips_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 15 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_names_the_playlist_for_the_posted_day[flag]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_names_the_playlist_for_the_posted_day[page]`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_set_with_nothing_owned_or_landed_writes_no_playlist_and_says_so`
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_posted_on_a_frozen_job_names_another_day_and_the_frozen_name_wins_with_a_warning`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`
  - `tests/test_set_inspiration_playlist.py::test_when_every_landed_members_file_is_refused_the_left_list_names_them`

Old text:

```
            if plan.set_playlist is not None:
```

New text:

```
            if False:
```

### `u121.S22_record_unnamed`

_record_landing_commit: the set playlist is not named on the record

- File: `src/cratekit/intake/native.py`
- Source: `u121.json`, row `S22_record_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 5 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
    if set_written is not None and plan.set_playlist is not None:
```

New text:

```
    if False:
```

### `u126.P2_not_shown`

Drop ContentLink from a row's columns, so the screen and the row's part of the digest omit it

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `P2_not_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_link_its_count_the_playlist_and_each_file_move_the_digest`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
            **(
                {rb_writer.CONTENT_LINK_COLUMN: self.content_link}
                if self.content_link is not None
                else {}
            ),
```

New text:

```
(empty)
```

### `u126.R1_binding_value_kept`

Drop the restamp of ContentLink, so the row keeps the binding's value

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R1_binding_value_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 37 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - ... and 22 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
```

New text:

```
    pass
```

### `u126.R2_fill_if_null`

Set ContentLink only when the binding left it NULL, which it never does

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R2_fill_if_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 37 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - ... and 22 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
```

New text:

```
    if getattr(content, rb_writer.CONTENT_LINK_COLUMN, None) is None:
        setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
```

### `u126.R5_read_back_file_id`

Read back the file id column where the link should be

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R5_read_back_file_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 37 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - ... and 22 more, see the JSON sidecar

Old text:

```
        None if row[3] is None else int(row[3]),
```

New text:

```
        None if row[2] is None else int(row[2]),
```

### `u126.S1_file_id_kept`

Sample, U115: drop the file id restamp, so the row keeps the binding's random id

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `S1_file_id_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 38 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - ... and 23 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.FILE_ID_COLUMN, file_id_of(row.target))
```

New text:

```
    pass
```

### `u127.N14_read_back_skipped`

Never read the tag back, so every landed row reports untagged

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N14_read_back_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[above]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`

Old text:

```
            _vox_read_back(db) if any(row.vox for row, _ in added_ids) else (frozenset(), "")
```

New text:

```
            (frozenset(), "") if any(row.vox for row, _ in added_ids) else (frozenset(), "")
```

### `u127.N8_tag_never_written`

Write no tag at the apply, the defect R-841 measured

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N8_tag_never_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_hand_placed_tag_on_a_row_already_present_survives`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[above]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_land_vox_native.py::test_a_library_with_another_category_only_gains_the_vocals_category`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`

Old text:

```
            vox_written = _tag_vox(db, added_ids)
```

New text:

```
            vox_written = 0
```

### `u127.N9_tag_every_added`

Write the tag on every added row, not only those the plan tagged

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N9_tag_every_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 50 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - ... and 35 more, see the JSON sidecar

Old text:

```
    content_ids = [content_id for row, content_id in added if row.vox]
```

New text:

```
    content_ids = [content_id for row, content_id in added]
```

### `u135.A14_set_order_reverses`

INBOX set-order walk appends members in reverse position order

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A14_set_order_reverses`
- Moved: Anchored where u307-replay-after-a.json replayed it: the same walk over the set's members in position order, now in native.py's _batch_order (U307 folded the loop)
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`
- Collected: 65 against a baseline of 65
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_u135_set_inbox_join.py::test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order`

Old text:

```
    members = plan.set_playlist.members if plan.set_playlist is not None else ()
```

New text:

```
    members = tuple(reversed(plan.set_playlist.members)) if plan.set_playlist is not None else ()
```

### `u135.A1_removed_namesake_written_into`

Drop the node_removed skip so a soft-deleted set-named INBOX playlist is written into

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A1_removed_namesake_written_into`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_removed_set_named_inbox_playlist_is_not_written_into`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_removed_set_named_inbox_playlist_is_not_written_into`

Old text:

```
    for row in list(db.get_playlist(Name=plan.playlist)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
            return row
    return db.create_playlist(plan.playlist, parent=anchor)

```

New text:

```
    return rb_writer.ensure_playlist(db, plan.playlist, anchor)

```

### `u135.A2_set_order_falls_to_name_order`

INBOX members follow landing file name order even when a set playlist is planned

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A2_set_order_falls_to_name_order`
- Moved: the same set order first branch, now in native.py's _batch_order (U307 folded the loop)
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order`

Old text:

```
    members = plan.set_playlist.members if plan.set_playlist is not None else ()
```

New text:

```
    members = ()
```

### `u135.A8_job_key_not_stamped`

A set landing's batch playlist record carries no job key

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A8_job_key_not_stamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 9 against a baseline of 9
- Kills: 4 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
  - `tests/test_u135_set_inbox_join.py::test_a_removed_set_named_inbox_playlist_is_not_written_into`
  - `tests/test_u135_set_inbox_join.py::test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order`
  - `tests/test_u135_set_inbox_join.py::test_two_landings_of_one_set_make_one_inbox_playlist_in_set_order`

Old text:

```
        if plan.set_job_id:
            kept[INBOX_JOB_KEY] = plan.set_job_id

```

New text:

```
        if False:
            kept[INBOX_JOB_KEY] = plan.set_job_id

```

### `u166.A4_no_add`

apply_rows: add nothing to Analyze

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A4_no_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 14 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses`
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`
  - `tests/test_inbox_analyzed.py::test_a_removed_smart_or_outside_node_named_analyze_is_never_written_into`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_with_no_analysis_path_or_analysed_unset_stays`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`
  - `tests/test_inbox_analyzed.py::test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name`
  - `tests/test_inbox_analyzed.py::test_nothing_analysed_asks_a_late_analysis_is_stale_a_track_held_twice_clears_once_then_nothing`
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_hearts_native.py::test_once_a_band_holds_the_heart_the_additive_refresh_puts_it_in_that_folders_favorites`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
            if added_ids:
                analyze = _analyze_row(db, plan, anchor)
```

New text:

```
            if False:
                analyze = _analyze_row(db, plan, anchor)
```

### `u166.A7_record_count`

apply_rows: record the batch's memberships only on success

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A7_record_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 5 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`
  - `tests/test_intake_land_hearts_native.py::test_once_a_band_holds_the_heart_the_additive_refresh_puts_it_in_that_folders_favorites`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships + analyze_added,
```

New text:

```
        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships,
```

### `r1255.N1_landings_of_pass_refuses`

native.landings_of_pass: drop the unread half again, so sync mark says a recorded landing never committed

- File: `src/cratekit/intake/native_plan.py`
- Source: `r1255.json`, row `N1_landings_of_pass_refuses`
- Moved: Anchored where u307-replay-after-a.json replayed it: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_sync_mark.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_sync_mark.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_landing`

Old text:

```
    land the pass again.
    """
    records = session.records(cfg)
```

New text:

```
    land the pass again.
    """
    records = session.scan_log(cfg)[0]
```

### `r1255.N2_landed_passes_refuses`

native.landed_passes: drop the unread half again, so organize plans no native pass over a log it could not list

- File: `src/cratekit/intake/native_plan.py`
- Source: `r1255.json`, row `N2_landed_passes_refuses`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_sync_mark.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`

Old text:

```
    cannot list refuses rather than reading as no landing (R-1255).
    """
    records = session.records(cfg)
```

New text:

```
    cannot list refuses rather than reading as no landing (R-1255).
    """
    records = session.scan_log(cfg)[0]
```

### `r770-d.C7_unresolved_target_planned_as_an_add`

native.plan_rows: read a target the matcher could not resolve as a file the collection does not hold

- File: `src/cratekit/intake/native_plan.py`
- Source: `r770-d.json`, row `C7_unresolved_target_planned_as_an_add`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_the_engine_refuses_a_target_it_cannot_resolve_instead_of_planning_an_add`

Old text:

```
        if match.outcome is trees.MatchOutcome.UNRESOLVED:
```

New text:

```
        if False:
```

### `r777.N15_any_pass`

landings_of_pass counts a landing of another pass

- File: `src/cratekit/intake/native_plan.py`
- Source: `r777.json`, row `N15_any_pass`
- Moved: Anchored where u307-replay-after-a.json replayed it: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[another-pass]`

Old text:

```
            and record.detail.get(PASS_KEY) == name

```

New text:

```
(empty)
```

### `u126.P1_no_read`

Skip the library read and plan a fixed value, the binding's shape of a guess

- File: `src/cratekit/intake/native_plan.py`
- Source: `u126.json`, row `P1_no_read`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - `tests/test_intake_land_native.py::test_an_approval_at_one_link_is_not_applied_at_another_and_no_majority_refuses`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_landed_rows_carry_what_rekordbox_loads_and_no_analysis_value`
  - `tests/test_intake_land_native.py::test_the_link_its_count_the_playlist_and_each_file_move_the_digest`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
        row_link.library_link(db) if any(row.action == ADD for row in rows) else None
```

New text:

```
        row_link.LibraryLink(value=7, carriers=0, rows=0)
        if any(row.action == ADD for row in rows)
        else None
```

### `u127.N1_cut_strict`

Compare the score strictly above the cut, so a file exactly at the cut is not tagged

- File: `src/cratekit/intake/native_plan.py`
- Source: `u127.json`, row `N1_cut_strict`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`

Old text:

```
        values = metadata_cli.vocal_tag_values(level, None, cut)
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
```

New text:

```
        values = metadata_cli.vocal_tag_values(level, None, cut + 0.5)
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
```

### `u127.N3_default_cut_when_uncalibrated`

Tag from the vocals verb's default cut on a library with no calibration instead of blocking

- File: `src/cratekit/intake/native_plan.py`
- Source: `u127.json`, row `N3_default_cut_when_uncalibrated`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_uncalibrated]`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`

Old text:

```
    if cut is None:
        return rows, None, VOX_UNCALIBRATED
```

New text:

```
    if cut is None:
        cut = metadata_cli.DEFAULT_VOCAL_THRESHOLD
```

### `u135.A13_live_inbox_ignores_parent`

live_inbox_named matches the name anywhere, not only under the intake root

- File: `src/cratekit/intake/native_plan.py`
- Source: `u135.json`, row `A13_live_inbox_ignores_parent`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined`

Old text:

```
        if str(getattr(row, "ParentID", "") or "") == str(root_id):
            return True

```

New text:

```
        if True:
            return True

```

### `u135.A5_recorded_inbox_skips_job_key`

recorded_inbox_playlist ignores the job key so any closed batch playlist is treated as this job's

- File: `src/cratekit/intake/native_plan.py`
- Source: `u135.json`, row `A5_recorded_inbox_skips_job_key`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined`

Old text:

```
        and record.detail[BATCH_PLAYLIST_KEY].get(INBOX_JOB_KEY) == job_id

```

New text:

```
        and True

```

### `u135.A7_leftover_joins_numbered_twin`

A numbered twin of the set name under INBOX is no longer named as a leftover

- File: `src/cratekit/intake/native_plan.py`
- Source: `u135.json`, row `A7_leftover_joins_numbered_twin`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`

Old text:

```
        if held.startswith(prefix) and held[len(prefix) :].isdigit():
            named.append(held)

```

New text:

```
        if False:
            named.append(held)

```

### `u174.N1_landed_passes_closed`

landed_passes: drop the closed state check, so an open landing's pass is planned

- File: `src/cratekit/intake/native_plan.py`
- Source: `u174.json`, row `N1_landed_passes_closed`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 210 against a baseline of 210
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N2_landed_passes_committed`

landed_passes: drop the committed source check, so a refused landing's pass is planned

- File: `src/cratekit/intake/native_plan.py`
- Source: `u174.json`, row `N2_landed_passes_committed`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 210 against a baseline of 210
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and record.state is session.SessionState.CLOSED
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N3_landed_passes_workflow`

landed_passes: drop the workflow check, so any closed session naming a pass is read as a landing

- File: `src/cratekit/intake/native_plan.py`
- Source: `u174.json`, row `N3_landed_passes_workflow`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 210 against a baseline of 210
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                if record.workflow == WORKFLOW
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                if record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N4_landed_passes_pass_key`

landed_passes: drop the pass key check, so a landing of no pass is listed as a pass named None

- File: `src/cratekit/intake/native_plan.py`
- Source: `u174.json`, row `N4_landed_passes_pass_key`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 210 against a baseline of 210
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
            }
```

### `u37-author-light.G2_recognition_gate`

Skip the recognition presence gate

- File: `src/cratekit/intake/recognize.py`
- Source: `u37-author-light.json`, row `G2_recognition_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_pipeline.py::test_identification_only_downloads_nothing_and_writes_a_tracklist`

Old text:

```
    missing = recognition_ready()
    if not missing:
        return
    raise refuse(
```

New text:

```
    missing = recognition_ready()
    if True:
        return
    raise refuse(
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

### `r1255.R1_rotation_unlisted_from_scan`

landings: never read the listing off the scan, so the classifier's reason counts one record

- File: `src/cratekit/intake/rotate.py`
- Source: `r1255.json`, row `R1_rotation_unlisted_from_scan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_the_rotation_reads_the_listing_from_the_scan`

Old text:

```
    unlisted = session.log_unlisted(unreadable, cfg)
```

New text:

```
    unlisted = False
```

### `r1255.R3_rotation_warning_gate`

records_warnings: never warn, so the rotation ages a batch from its playlist's date unsaid

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `r1255.json`, row `R3_rotation_warning_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_the_rotation_warns_on_a_log_it_could_not_list_or_records_it_could_not_read[given0-the session log could not be listed]`
  - `tests/test_session_log_unlisted.py::test_the_rotation_warns_on_a_log_it_could_not_list_or_records_it_could_not_read[given1-2 session record(s) could not be read]`

Old text:

```
    if not plan.unreadable_records:
        return []
    unread = (
```

New text:

```
    if True:
        return []
    unread = (
```

### `r1255.R4_rotation_warning_wording`

records_warnings: word an unlisted log as a count of records

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `r1255.json`, row `R4_rotation_warning_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_the_rotation_warns_on_a_log_it_could_not_list_or_records_it_could_not_read[given0-the session log could not be listed]`

Old text:

```
        if plan.log_unlisted
        else f"{plan.unreadable_records} session record(s) could not be read, so a "
```

New text:

```
        if False
        else f"{plan.unreadable_records} session record(s) could not be read, so a "
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
- Collected: 94 against a baseline of 94
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
- Collected: 300 against a baseline of 300
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

### `u307.R17_made_on_drops_posted`

set_playlist._made_on: a pinned day wins over --posted, so a posted override does not survive a re-plan

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u307.json`, row `R17_made_on_drops_posted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_organize_inspiration.py`, `tests/test_u129_set_account_playlist.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_second_write_that_fills_a_gap_mid_set_is_not_a_failed_write`

Old text:

```
    if on is not None and posted is None:
```

New text:

```
    if on is not None:
```

### `u307.R19_flag_day_invalid_date_unrefused`

set_playlist._flag_day: a date flag that matches the pattern but names no real day raises a bare ValueError, not the refusal naming the flag

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u307.json`, row `R19_flag_day_invalid_date_unrefused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_organize_inspiration.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_set_date_that_is_not_a_month_is_refused_by_name[2026-00]`
  - `tests/test_set_inspiration_playlist.py::test_a_set_date_that_is_not_a_month_is_refused_by_name[2026-02-30]`
  - `tests/test_set_inspiration_playlist.py::test_a_set_date_that_is_not_a_month_is_refused_by_name[2026-13]`

Old text:

```
    try:
        return date(int(found.group(1)), int(found.group(2)), int(found.group(3) or 1))
    except ValueError as exc:
        raise _not_a(flag, value, kind, forms, exc) from exc
```

New text:

```
    return date(int(found.group(1)), int(found.group(2)), int(found.group(3) or 1))
```

### `u108-c.G21_listing_skips_already`

approved_cli.list_releases: a track another job already holds is listed again

- File: `src/cratekit/label/approved_cli.py`
- Source: `u108-c.json`, row `G21_listing_skips_already`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_sync_go.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_landing_labels.py`
- Collected: 364 against a baseline of 364
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`

Old text:

```
            elif str(settled.wanted.ref or "").strip() in already:
```

New text:

```
            elif False:
```

### `u108-c.G22_listing_excuse_applies`

approved_cli.list_releases: an excused failure kind still refuses an empty listing

- File: `src/cratekit/label/approved_cli.py`
- Source: `u108-c.json`, row `G22_listing_excuse_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_sync_go.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_landing_labels.py`
- Collected: 364 against a baseline of 364
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_release_gone_from_the_provider_does_not_refuse_every_go_after_it`

Old text:

```
    unexcused = [one for one in failures if one.kind not in excuse]
```

New text:

```
    unexcused = list(failures)
```

### `r382.M16_parser_moved_lowercase`

The moved parser keeps a bare identifier's case, checking the move kept its tests

- File: `src/cratekit/label/catalogue.py`
- Source: `r382.json`, row `M16_parser_moved_lowercase`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 805 against a baseline of 805
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_url_a_share_link_and_a_bare_id_all_name_the_playlist[bare-upper]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`

Old text:

```
    if _UUID.fullmatch(text):
        return text.lower()
```

New text:

```
    if _UUID.fullmatch(text):
        return text
```

### `r504-a.A10_block_listed`

The report block carries the declared count where the listed count belongs

- File: `src/cratekit/label/catalogue.py`
- Source: `r504-a.json`, row `A10_block_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 805 against a baseline of 805
- Kills: 11 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_playlist_listing_carries_the_shortfall_beside_its_rows`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
        return {"declared": self.declared, "listed": self.listed, "withheld": self.withheld}
```

New text:

```
        return {"declared": self.declared, "listed": self.declared, "withheld": self.withheld}
```

### `r504-a.A8_withheld_sign`

The seam subtracts the wrong way round, so the withheld count is negative

- File: `src/cratekit/label/catalogue.py`
- Source: `r504-a.json`, row `A8_withheld_sign`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 805 against a baseline of 805
- Kills: 15 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_a_release_listed_short_of_its_count_carries_the_shortfall_and_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_playlist_listing_carries_the_shortfall_beside_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_label_workers.py::test_a_harvest_over_a_short_playlist_offers_what_it_read_and_warns`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
        return self.declared - self.listed
```

New text:

```
        return self.listed - self.declared
```

### `r504-a.A9_summary_reworded`

The seam's one spelling of the three numbers is reworded

- File: `src/cratekit/label/catalogue.py`
- Source: `r504-a.json`, row `A9_summary_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 805 against a baseline of 805
- Kills: 10 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_a_release_listed_short_of_its_count_carries_the_shortfall_and_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_workers.py::test_a_harvest_over_a_short_playlist_offers_what_it_read_and_warns`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
            f"{self.withheld} withheld by the provider"
```

New text:

```
            f"{self.withheld} held back by the provider"
```

### `r504-a.A11_boundary_refuses`

The verb boundary no longer catches the shortfall, so it is refused as an unreadable listing

- File: `src/cratekit/label/cli.py`
- Source: `r504-a.json`, row `A11_boundary_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 0 against a baseline of 552
- Kills: 0 (collect-error)
- Note: collection changed: 0 collected against a baseline of 552. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Collection errors: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`

Old text:

```
    except catalogue.HeartsShortfall as short:
        return list(short.rows), short

```

New text:

```
(empty)
```

### `r504-a.A12_boundary_drops_short`

The verb boundary keeps the rows and drops the shortfall, passing the short listing off as the account

- File: `src/cratekit/label/cli.py`
- Source: `r504-a.json`, row `A12_boundary_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 552 against a baseline of 552
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        return list(short.rows), short
```

New text:

```
        return list(short.rows), None
```

### `r1115.G3_warn_each_failed_track`

go _drive: raise no warning for a track that failed for good

- File: `src/cratekit/label/go.py`
- Source: `r1115.json`, row `G3_warn_each_failed_track`
- Moved: _drive builds the refused warnings as a generator over read.failed; emptying it raises no warning, as the loop did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 205 against a baseline of 205
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`

Old text:

```
        for item_id in read.failed

```

New text:

```
        for item_id in ()

```

### `r1115.G4_name_the_refused_on_the_check`

go _downloaded: leave the refused tracks out of the check's words

- File: `src/cratekit/label/go.py`
- Source: `r1115.json`, row `G4_name_the_refused_on_the_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 205 against a baseline of 205
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`

Old text:

```
    if read.refused:
        said +=
```

New text:

```
    if False:
        said +=
```

### `r1115.G5_every_refused_fails_the_check`

go: the downloaded check is ok over a go whose every track was refused

- File: `src/cratekit/label/go.py`
- Source: `r1115.json`, row `G5_every_refused_fails_the_check`
- Moved: the downloaded check of a fresh go is now built by the shared helper _driven, whose status line is this same guard
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 205 against a baseline of 205
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_resumed_download_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
    status = "fail" if nothing and read.refused else "ok"
```

New text:

```
    status = "ok"
```

### `r1115.G6_no_commands_over_nothing`

go: name the tail's commands over a folder nothing landed in

- File: `src/cratekit/label/go.py`
- Source: `r1115.json`, row `G6_no_commands_over_nothing`
- Moved: the fresh go and the carry on name their tail through one helper, _tail_of, whose not nothing test is this guard
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 205 against a baseline of 205
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
    landed = tail(staging, manifest, run_of) if manifest is not None and not nothing else []
```

New text:

```
    landed = tail(staging, manifest, run_of) if manifest is not None else []
```

### `r1115.G8_report_names_the_refused`

go: the report's refused list is empty whatever was refused

- File: `src/cratekit/label/go.py`
- Source: `r1115.json`, row `G8_report_names_the_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 205 against a baseline of 205
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`

Old text:

```
        refused = list(read.refused)

```

New text:

```
        refused = []

```

### `r1115.G9_resume_no_commands_over_nothing`

go _resume: name the tail's commands over a resumed download that landed nothing

- File: `src/cratekit/label/go.py`
- Source: `r1115.json`, row `G9_resume_no_commands_over_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 205 against a baseline of 205
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_resumed_download_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
            if isinstance(manifest, str) and manifest and not nothing:
```

New text:

```
            if isinstance(manifest, str) and manifest:
```

### `r1467.M01_fresh_go_checks_before_gate`

go: never refuse before the gate, so a fresh go queues beside a download no landing took and its tail lands both

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M01_fresh_go_checks_before_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 15 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_of_another_verb_with_its_track_in_the_folder_refuses_the_go`
  - `tests/test_label_sync_go.py::test_a_fresh_go_with_nothing_new_names_an_unlanded_download_rather_than_end_quietly`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_were_recorded_in_another_folder_is_not_named_for_this_one`
  - `tests/test_label_sync_go.py::test_a_go_with_tracks_in_the_folder_is_named_once_beside_files_no_download_names`
  - `tests/test_label_sync_go.py::test_a_landing_proof_of_another_pass_proves_nothing`
  - `tests/test_label_sync_go.py::test_a_plain_download_a_tail_renamed_refuses_a_fresh_go_before_its_gate`
  - `tests/test_label_sync_go.py::test_a_plain_download_in_the_folder_refuses_a_fresh_go_before_the_gate`
  - `tests/test_label_sync_go.py::test_a_proven_pass_whose_tracks_are_still_at_their_download_names_is_still_waiting`
  - `tests/test_label_sync_go.py::test_a_retired_intake_file_proves_the_pass`
  - `tests/test_label_sync_go.py::test_a_track_no_download_names_refuses_the_fresh_go_and_only_an_unproven_go_is_named[bridge]`
  - `tests/test_label_sync_go.py::test_a_track_no_download_names_refuses_the_fresh_go_and_only_an_unproven_go_is_named[native]`
  - `tests/test_label_sync_go.py::test_an_earlier_download_the_fresh_go_resumes_is_its_own_and_a_plain_one_is_not`
  - `tests/test_label_sync_go.py::test_an_earlier_go_whose_tail_renamed_its_tracks_at_the_landings_gate_still_refuses`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_finished_by_hand_refuses_a_fresh_go_before_it_queues`
  - `tests/test_label_sync_go.py::test_the_walk_refused_beside_a_download_keeps_what_it_answered`

Old text:

```
    if found:
        raise _waiting_refusal(found, staging, walk)
```

New text:

```
    if False:
        raise _waiting_refusal(found, staging, walk)
```

### `r1467.M02_resumed_jobs_are_own`

go: read the jobs a fresh go resumes as beside it, so a go that resumes an earlier download refuses over that download's own tracks

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M02_resumed_jobs_are_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 14 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_while_a_go_resumed_another_refuses_the_resumes_tail`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_cancelled_still_refuses_and_lands_nothing`
  - `tests/test_label_sync_go.py::test_a_go_with_an_earlier_download_to_resume_resumes_it_and_queues_nothing_new`
  - `tests/test_label_sync_go.py::test_a_job_stopped_halfway_resumes_and_downloads_only_the_rest`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`
  - `tests/test_label_sync_go.py::test_an_abort_recorded_after_the_stop_is_not_taken_on`
  - `tests/test_label_sync_go.py::test_an_earlier_download_the_fresh_go_resumes_alone_is_asked_about`
  - `tests/test_label_sync_go.py::test_an_earlier_download_the_fresh_go_resumes_is_its_own_and_a_plain_one_is_not`

Old text:

```
found = beside(cfg, store, staging, {job_id for job_id, _left in summary.open_jobs})
```

New text:

```
found = beside(cfg, store, staging, set())
```

### `r1467.M03_fresh_tail_checks_after_drive`

go: run the fresh go's tail without reading the folder after its drive, so a download that finished meanwhile lands with it

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M03_fresh_tail_checks_after_drive`
- Moved: the fresh go's beside check after its drive is now the one _refuse_beside call in _tail_of
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 14 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_pass_landed_reads_nothing_by_its_tails_record`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_ran_still_refuses_a_file_more_than_its_own_renamed`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_another_tail_renamed_does_not_read_them_as_its_own`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_left_reads_no_file_put_there_since_as_its_own`
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_a_tail_renamed_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tail_refused_beside_a_download_still_names_the_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tails_record_that_cannot_be_read_reads_nothing_as_the_gos_own`

Old text:

```
        _refuse_beside(
            cfg, store, job, staging, manifest, run_of, landed, own={job.job_id},
```

New text:

```
        (lambda *_a, **_k: None)(
            cfg, store, job, staging, manifest, run_of, landed, own={job.job_id},
```

### `r1467.M04_resume_tail_checks`

_resume: run a single resume's tail without reading the folder, so a download beside it lands under the resumed go's pass

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M04_resume_tail_checks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_that_finished_while_a_go_resumed_another_refuses_the_resumes_tail`

Old text:

```
    if land is not None:
        # NOT BESIDE ANOTHER DOWNLOAD
```

New text:

```
    if False:
        # NOT BESIDE ANOTHER DOWNLOAD
```

### `r1467.M05_carry_on_checks`

_carry_on: run the run's own tail without reading the folder, so a plain download beside it lands under its pass

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M05_carry_on_checks`
- Moved: the carry on's beside check moved into _tail_of, which the carry on calls; the same read.landed test guards it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 14 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_pass_landed_reads_nothing_by_its_tails_record`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_ran_still_refuses_a_file_more_than_its_own_renamed`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_another_tail_renamed_does_not_read_them_as_its_own`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_left_reads_no_file_put_there_since_as_its_own`
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_a_tail_renamed_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tail_refused_beside_a_download_still_names_the_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tails_record_that_cannot_be_read_reads_nothing_as_the_gos_own`

Old text:

```
    if read.landed:
        _refuse_beside(
```

New text:

```
    if False:
        _refuse_beside(
```

### `r1467.M14_carry_on_reads_the_record`

_carry_on: never read what the run's own tail left, so its renamed tracks refuse its own go

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M14_carry_on_reads_the_record`
- Moved: the carry on asks _tail_of with own_tail, which reads what its own tail left; dropping the read is the same mutant
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`

Old text:

```
            kept=kept_tail(cfg, job.job_id) if own_tail else frozenset(), refused=read.refused,
```

New text:

```
            kept=frozenset(), refused=read.refused,
```

### `r1467.M15_beside_keeps_later_jobs`

_refuse_beside: leave the later go jobs out of the detail's beside list

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M15_beside_keeps_later_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`

Old text:

```
            "beside": [*known, *(one.job_id for one in extra.waiting)],
```

New text:

```
            "beside": [one.job_id for one in extra.waiting],
```

### `r1467.M17_walk_answers_kept`

_waiting_refusal: drop what the walk answered from the refusal

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M17_walk_answers_kept`
- Moved: the walk answers are now merged into the detail from this local; an empty one drops them as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_walk_refused_beside_a_download_keeps_what_it_answered`

Old text:

```
    answered = {"answered_this_run": list(walk)} if walk is not None else {}
```

New text:

```
    answered = {}
```

### `r1467.M18_refused_tracks_carried`

_refuse_beside: drop the tracks refused for good from the tail's refusal

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M18_refused_tracks_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tail_refused_beside_a_download_still_names_the_tracks_refused_for_good`

Old text:

```
            "refused": list(refused),
```

New text:

```
            "refused": [],
```

### `r1467.M25_own_pass_handed_to_beside`

_refuse_beside: never hand the go's own pass to beside, so a landed pass's record is still read

- File: `src/cratekit/label/go.py`
- Source: `r1467.json`, row `M25_own_pass_handed_to_beside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_whose_pass_landed_reads_nothing_by_its_tails_record`

Old text:

```
own_pass=default_name(run_of) if kept else None
```

New text:

```
own_pass=None
```

### `u108-a.G02_pick_takes_releases`

go.summarise: only an all answer takes releases, so a pick's releases are left out of the summary and the download

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G02_pick_takes_releases`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_release_accepted_by_hand_and_answered_for_by_nobody_is_not_downloaded`
  - `tests/test_label_sync_go.py::test_two_labels_answered_all_and_one_picked_produce_one_summary_and_one_gate`

Old text:

```
        if word in TAKING:
```

New text:

```
        if word == sync_cli.ALL:
```

### `u108-a.G03_not_now_counted`

go.summarise: a not-now answer is not counted in the summary

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G03_not_now_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_two_labels_answered_all_and_one_picked_produce_one_summary_and_one_gate`

Old text:

```
        elif word == sync_cli.NOT_NOW:
            not_now.setdefault(name)
```

New text:

```
        elif word == sync_cli.NOT_NOW:
            pass
```

### `u108-a.G04_digest_covers_releases`

Summary.plan: the digest leaves out the releases, so an answer saved after the decision does not make it stale

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G04_digest_covers_releases`
- Moved: the digest literal is now opened on the digest_of line, so the same key stands four spaces shallower
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_an_answer_saved_after_the_decision_makes_the_decision_stale`

Old text:

```
                "releases": [[one.label_id, one.identity] for one in self.taken],
```

New text:

```
                "releases": [],
```

### `u108-a.G06_abort_downloads_nothing`

go.go: an abort at the gate goes on to download

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G06_abort_downloads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_declined_go_runs_no_tail`
  - `tests/test_label_sync_go.py::test_aborting_at_the_gate_downloads_nothing_and_keeps_the_answers`

Old text:

```
    if option == "abort":
```

New text:

```
    if False:
```

### `u108-a.G07_only_accepted_downloaded`

go.go: a release an answer took is downloaded even after a person cleared it in review

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G07_only_accepted_downloaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_release_cleared_after_answering_is_named_and_not_downloaded`

Old text:

```
                    if item is not None and item.verdict is Verdict.ACCEPTED:
```

New text:

```
                    if item is not None:
```

### `u108-a.G08_already_passed_to_listing`

go.go: the tracks an earlier go holds are not passed to the listing, so a second start asks for them again

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G08_already_passed_to_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`

Old text:

```
                already=held.tracks,
```

New text:

```
                already=frozenset(),
```

### `u108-a.G09_gone_excused`

go.go: a release gone from the provider refuses the go again when nothing else is listed

- File: `src/cratekit/label/go.py`
- Source: `u108-a.json`, row `G09_gone_excused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_release_gone_from_the_provider_does_not_refuse_every_go_after_it`

Old text:

```
                excuse=frozenset({approved_cli.GONE, approved_cli.NO_IDENTIFIER}),
```

New text:

```
                excuse=frozenset(),
```

### `u108-b.G10_unread_answer_kept`

go.go: an answer holding a release the provider did not answer for is settled anyway, so it is never asked for again

- File: `src/cratekit/label/go.py`
- Source: `u108-b.json`, row `G10_unread_answer_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`

Old text:

```
            keep=retry,
        )
```

New text:

```
            keep=frozenset(),
        )
```

### `u108-b.G13_closed_job_retried`

go._resume: a job that ended half failed is driven without being re-armed, so its failed tracks are never asked for again

- File: `src/cratekit/label/go.py`
- Source: `u108-b.json`, row `G13_closed_job_retried`
- Moved: the once used job local of _resume was inlined, so the re-arm turns on the same is_open read
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`

Old text:

```
            if not jobs.get(store, job_id).is_open():
                # STOPPED BY A SIGNAL
```

New text:

```
            if False:
                # STOPPED BY A SIGNAL
```

### `u108-b.G15_time_pacing_coefficient`

Summary.seconds: the pacing delay counted at half its value per track

- File: `src/cratekit/label/go.py`
- Source: `u108-b.json`, row `G15_time_pacing_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_estimated_time_is_the_pacing_and_the_transfer_of_the_size`

Old text:

```
        return round(self.tracks * self.pace_s + self.size / TRANSFER_BYTES_PER_SECOND)
```

New text:

```
        return round(self.tracks * self.pace_s / 2 + self.size / TRANSFER_BYTES_PER_SECOND)
```

### `u108-b.G17_done_tracks_held`

go.held_by_goes: a track a finished go job downloaded is not held, so a later go asks for it again

- File: `src/cratekit/label/go.py`
- Source: `u108-b.json`, row `G17_done_tracks_held`
- Moved: held_by_goes adds the held tracks with one update over a generator; its filter is the same done or resumed test
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`

Old text:

```
        tracks.update(item.item_id for item in items if item.state is jobs.ItemState.DONE or (
            again and item.state is not jobs.ItemState.SKIPPED
        ))
```

New text:

```
        tracks.update(item.item_id for item in items if (
            again and item.state is not jobs.ItemState.SKIPPED
        ))
```

### `u108-c.G23_job_carries_origin`

go.go: the download job is queued without the go's marker, so no later go knows it holds those tracks

- File: `src/cratekit/label/go.py`
- Source: `u108-c.json`, row `G23_job_carries_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 64 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_while_a_go_resumed_another_refuses_the_resumes_tail`
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_fresh_go_with_nothing_new_names_an_unlanded_download_rather_than_end_quietly`
  - `tests/test_label_sync_go.py::test_a_go_job_whose_track_was_refused_for_good_is_not_resumed`
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park`
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - ... and 49 more, see the JSON sidecar

Old text:

```
                        extra={
                            ORIGIN_KEY: {"run": run_id, "manifest": str(written.manifest_path)},
                            RUN_KEY: run_id,
                        },
```

New text:

```
                        extra={
                            RUN_KEY: run_id,
                        },
```

### `u108-d.G11_waited_go_refuses_again`

go.go: a go that waited for the record's lock while another queued goes on to list and queue

- File: `src/cratekit/label/go.py`
- Source: `u108-d.json`, row `G11_waited_go_refuses_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_second_go_that_waited_for_the_first_refuses_rather_than_queue_its_tracks_again`

Old text:

```
        if held.resume:
            raise refuse(
```

New text:

```
        if False:
            raise refuse(
```

### `u108-d.G14_retryable_cause_only_again`

go.resumable: a job whose cause says no retry can succeed is resumed anyway

- File: `src/cratekit/label/go.py`
- Source: `u108-d.json`, row `G14_retryable_cause_only_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_job_whose_failures_cannot_succeed_on_a_retry_is_not_resumed`

Old text:

```
    return job.cause is None or job.cause.retryable
```

New text:

```
    return True
```

### `u108-d.G16_origin_marker_filter_again`

go.held_by_goes: every acquire download job counts as a go's, so a download queued by hand is resumed and its tracks held by the go

- File: `src/cratekit/label/go.py`
- Source: `u108-d.json`, row `G16_origin_marker_filter_again`
- Moved: held_by_goes now asks _goes_job whether a job is a go's; the origin marker test moved there unchanged
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_queued_by_hand_is_not_resumed_or_held_by_a_go`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_left_reads_no_file_put_there_since_as_its_own`
  - `tests/test_label_sync_go.py::test_a_plain_download_a_tail_renamed_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_plain_download_already_landed_refuses_nothing`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`

Old text:

```
    return job.handler_key == DOWNLOAD and isinstance((job.payload or {}).get(ORIGIN_KEY), Mapping)
```

New text:

```
    return job.handler_key == DOWNLOAD
```

### `u110-c.C4_go_tail`

The label go tail prints --name RUN again

- File: `src/cratekit/label/go.py`
- Source: `u110-c.json`, row `C4_go_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`, `tests/test_label_sync_go.py`
- Collected: 130 against a baseline of 130
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_the_label_go_tail_hands_the_run_as_the_pass_and_names_no_batch`
  - `tests/test_label_sync_go.py::test_the_download_lands_as_an_intake_under_the_runs_one_batch`

Old text:

```
"--pass", default_name(run_id)]
```

New text:

```
"--name", default_name(run_id)]
```

### `u190.G5_resume_one_job_only`

_resume: take the first earlier job's tail whatever the count, so two manifests share one landing

- File: `src/cratekit/label/go.py`
- Source: `u190.json`, row `G5_resume_one_job_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    land = lands[0] if len(lands) == 1 else None
```

New text:

```
    land = lands[0] if lands else None
```

### `u239-composites.M11b_land_only_landed_after_its_test`

M11 measured again after its test: name the landing whatever the download read

- File: `src/cratekit/label/go.py`
- Source: `u239-composites.json`, row `M11b_land_only_landed_after_its_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
    if read.landed and manifest is not None:
```

New text:

```
    if manifest is not None:
```

### `u239.M01_own_needs_apply`

_own: take the run's job on whatever answer is recorded, so an abort recorded after the stop downloads and lands

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M01_own_needs_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_an_abort_recorded_after_the_stop_is_not_taken_on`

Old text:

```
    if recorded is None or recorded.option != APPLY:
```

New text:

```
    if recorded is None:
```

### `u239.M02_own_skips_cancelled`

_own: take a cancelled job on too, so a person's cancel is resumed and landed with no question

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M02_own_skips_cancelled`
- Moved: _own returns through one conditional; the cancelled test is the same clause of it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_cancelled_still_refuses_and_lands_nothing`

Old text:

```
    return None if job is None or job.state is jobs.JobState.CANCELLED else job.job_id
```

New text:

```
    return None if job is None else job.job_id
```

### `u239.M03_own_job_by_run`

own_job: take any go job on, not only the one this run's go queued

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M03_own_job_by_run`
- Moved: own_job asks _goes_job for the origin marker; the run match is the same comparison after it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_a_go_with_an_earlier_download_to_resume_resumes_it_and_queues_nothing_new`
  - `tests/test_label_sync_go.py::test_a_job_stopped_halfway_resumes_and_downloads_only_the_rest`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_resumed_download_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_second_go_that_waited_for_the_first_refuses_rather_than_queue_its_tracks_again`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download[bridge]`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download[native]`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_landed_download_does_not_refuse_a_later_runs_tail`
  - `tests/test_label_sync_go.py::test_answers_saved_beside_a_finished_go_wait_and_are_not_landed_with_it`

Old text:

```
        if _goes_job(job) and job.payload[ORIGIN_KEY].get("run") == run_id:
```

New text:

```
        if _goes_job(job) and True:
```

### `u239.M04_go_takes_own_on`

go: never take the run's own download on, so the go asks the gate again as before U239

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M04_go_takes_own_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 19 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_reached_its_landing_names_that_landing_and_runs_nothing_again`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    if own is not None:
```

New text:

```
    if False:
```

### `u239.M05_beside_later_only`

_beside: count earlier go jobs too, so a later run's tail is refused over an earlier landed go

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M05_beside_later_only`
- Moved: _beside folds its two skips into one test; the earlier job clause is the same comparison
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_with_an_earlier_download_to_resume_resumes_it_and_queues_nothing_new`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download[bridge]`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download[native]`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_landed_download_does_not_refuse_a_later_runs_tail`
  - `tests/test_label_sync_go.py::test_answers_saved_beside_a_finished_go_wait_and_are_not_landed_with_it`

Old text:

```
        if other.job_id == job.job_id or other.created < job.created or not _goes_job(other):
```

New text:

```
        if other.job_id == job.job_id or not _goes_job(other):
```

### `u239.M06_beside_open`

_beside: count only a later go job that downloaded, so one parked before any track is ignored

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M06_beside_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`

Old text:

```
        if other.is_open() or any(
```

New text:

```
        if any(
```

### `u239.M07_beside_done`

_beside: count only an open later go job, so one that downloaded and settled is ignored

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M07_beside_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if other.is_open() or any(
```

New text:

```
        if other.is_open() or False and any(
```

### `u239.M08_retry_half_failed`

_carry_on: never re-arm a half failed own job, so a transient failure ends every go under the run

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M08_retry_half_failed`
- Moved: _carry_on reads the job's items once, so the left count is passed inline to the same resumable test
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`

Old text:

```
        if not job.is_open() and resumable(job, _left(items)):
```

New text:

```
        if False:
```

### `u239.M09_named_landing`

_carry_on: ignore the recorded landing, so the tail runs a second time

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M09_named_landing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_reached_its_landing_names_that_landing_and_runs_nothing_again`
  - `tests/test_label_sync_go.py::test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op`

Old text:

```
        if named:
```

New text:

```
        if False:
```

### `u239.M14_ceiling_fresh`

_carried: drop fresh, so the continue keeps the command line's own --run

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M14_ceiling_fresh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`

Old text:

```
        detail.update({"job": job.job_id, "run_id": run, "fresh": True})
```

New text:

```
        detail.update({"job": job.job_id, "run_id": run})
```

### `u239.M15_ceiling_job_id`

_carried: keep job_id on the ceiling cause, so the continue is job resume again

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M15_ceiling_job_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_names_its_own_go_to_continue_not_the_job`

Old text:

```
        detail = {key: value for key, value in (cause.detail or {}).items() if key != "job_id"}
```

New text:

```
        detail = dict(cause.detail or {})
```

### `u239.M16_other_stop_step`

_carried: add no step to a park or a retryable failure, so it names no way to the landing

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M16_other_stop_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park`

Old text:

```
    if job.state is jobs.JobState.BLOCKED or (
```

New text:

```
    if False and (
```

### `u239.M17_wrote`

_carry_on: a walk that wrote answers under a landed run reports no_op

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M17_wrote`
- Moved: the named landing branch of _carry_on returns through the shared _ended helper with the same wrote outcome
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op`

Old text:

```
            return _ended(ctx, checks, report, Outcome.OK if wrote else Outcome.NO_OP)
        items
```

New text:

```
            return _ended(ctx, checks, report, Outcome.NO_OP)
        items
```

### `u252.L7_seam_drops_keywords`

harvest.playlist_tracks: stop handing its keywords to the listing, so the fixture's sleep never reaches the ladder

- File: `src/cratekit/label/harvest.py`
- Source: `u252.json`, row `L7_seam_drops_keywords`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`
  - `tests/test_sync_twins.py::test_a_playlist_the_provider_cannot_list_is_left_named_and_the_other_is_made`
  - `tests/test_sync_twins.py::test_every_playlist_left_writes_nothing_and_opens_no_gate`

Old text:

```
    return listing.playlist_tracks(playlist, **kwargs)
```

New text:

```
    return listing.playlist_tracks(playlist)
```

### `r1056.N10_pass_not_required`

build_mark: neither --xml nor --pass required, so a bare mark reaches the handler

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N10_pass_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_the_pass_is_named_by_exactly_one_of_the_file_and_the_name[neither]`

Old text:

```
    proof = parser.add_mutually_exclusive_group(required=True)
```

New text:

```
    proof = parser.add_mutually_exclusive_group(required=False)
```

### `r1056.N1_no_refusal_of_an_unreadable_record`

native_years: read a record this build cannot read as one that filed nothing

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N1_no_refusal_of_an_unreadable_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-bool-tracks]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-bool-year]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-list-of-strings]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-string]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-text-year]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[no-label]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[no-tracks]`

Old text:

```
        if filed is None:
            raise _blocked(
```

New text:

```
        if filed is None:
            filed = frozenset()
        if False:
            raise _blocked(
```

### `r1056.N2_first_landing_only`

native_years: read only the first landing the proof names, so a pass landed twice loses the second's years

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N2_first_landing_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_every_committed_landing_of_the_pass_counts_and_no_other_does`

Old text:

```
    for session_id in proof.landings:
```

New text:

```
    for session_id in proof.landings[:1]:
```

### `r1056.N3_years_from_the_argument`

label_mark: read the native years under the name given on the command line, not the registry's name

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N3_years_from_the_argument`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_label_named_by_its_registry_identifier_is_compared_under_its_name`

Old text:

```
native_years(cfg, native, label)
```

New text:

```
native_years(cfg, native, name)
```

### `r1056.N4_no_landings_in_digest`

_payload: leave the landings out of the native digest, so a landing after the answer is not stale

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N4_no_landings_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_landing_of_the_pass_after_the_answer_makes_it_stale`
  - `tests/test_label_mark_native.py::test_the_gate_digest_names_the_landings`

Old text:

```
        identity["landings"] = list(native.landings)
```

New text:

```
        pass
```

### `r1056.N5_no_reread_before_rename`

label_mark: drop the reread of the native proof before the first rename

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N5_no_reread_before_rename`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_landing_between_the_plan_and_the_first_rename_renames_nothing`

Old text:

```
    if native is not None and native_proof(cfg, pass_name, verb=_VERB, named=_NAMED) != native:
```

New text:

```
    if False:
```

### `r1056.N6_no_nothing_filed_warning`

label_mark: never say a batch filed none of the built years

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N6_no_nothing_filed_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_label_playlists.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_bridge_batch_of_another_label_says_it_filed_nothing_too`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[a-year-never-built]`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[another-label]`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[no-label-filed]`

Old text:

```
    if not filed & {year.year for year in built}:
```

New text:

```
    if False:
```

### `r1056.N7_nothing_filed_against_any_year`

label_mark: warn only when the batch filed no year at all, not none of the built ones

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N7_nothing_filed_against_any_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_label_playlists.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[a-year-never-built]`

Old text:

```
    if not filed & {year.year for year in built}:
```

New text:

```
    if not filed:
```

### `r1056.N8_shown_pass_bare`

_shown: name the native pass with no word that it landed on the database native tree

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N8_shown_pass_bare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_native_pass_marks_exactly_the_years_its_landing_filed`

Old text:

```
            else f"{pass_name}, landed on the database native {native.tree_id!r} tree"
```

New text:

```
            else pass_name
```

