# Mutation table: u334-replay-after-7

Measured by `scripts/mutate.py` on 2026-11-24 04:59 UTC, branch `HEAD` at `90c0cc08`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23214 collected. pytest invocations for this batch: 317.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:59 UTC for commit `90c0cc0829da`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 56, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23214 against 23214. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u237.M6_substring_again` | `src/cratekit/label/verify.py` | user | 3 file(s) | 392 | 9 | killed |
| `u237.M7_left_word_boundary_only` | `src/cratekit/label/verify.py` | user | 3 file(s) | 392 | 7 | killed |
| `u105-b.S10_settings_to_engine` | `src/cratekit/master/cli.py` | user | 3 file(s) | 129 | 2 | killed |
| `u105-b.S1_parts_only_when_several` | `src/cratekit/master/cli.py` | user | 3 file(s) | 129 | 3 | killed |
| `u105-b.S2_lufs_frozen` | `src/cratekit/master/cli.py` | user | 3 file(s) | 129 | 2 | killed |
| `u105-b.S3_lufs_in_argv` | `src/cratekit/master/cli.py` | user | 3 file(s) | 129 | 1 | killed |
| `u105-b.S4_parts_in_argv` | `src/cratekit/master/cli.py` | user | 3 file(s) | 129 | 1 | killed |
| `u105-b.S5_queue_time_refusal` | `src/cratekit/master/cli.py` | user | 3 file(s) | 129 | 3 | killed |
| `u105-b.S6_join_order_notice` | `src/cratekit/master/cli.py` | user | 3 file(s) | 129 | 1 | killed |
| `u105-b.S7_staged_parts` | `src/cratekit/master/cli.py` | user | 3 file(s) | 129 | 1 | killed |
| `u105-b.S8_staged_target` | `src/cratekit/master/cli.py` | user | 3 file(s) | 129 | 1 | killed |
| `u105-b.S9_precheck_name` | `src/cratekit/master/cli.py` | user | 3 file(s) | 129 | 2 | killed |
| `u44-author.C2_argv_drops_overwrite` | `src/cratekit/master/cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u44-author.C3_argv_drops_output_dir` | `src/cratekit/master/cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u44-author.C4_refusal_not_translated` | `src/cratekit/master/cli.py` | user | 1 file(s) | 57 | 22 | killed |
| `u44-author.C6_overwrite_always_true` | `src/cratekit/master/cli.py` | user | 1 file(s) | 57 | 4 | killed |
| `u44-author.C7_output_dir_ignored_at_the_work` | `src/cratekit/master/cli.py` | user | 1 file(s) | 57 | 3 | killed |
| `u46-author.M1_no_items_enqueued` | `src/cratekit/master/cli.py` | user | 2 file(s) | 59 | 17 | killed |
| `u46-round-2.M6_staging_not_cleared` | `src/cratekit/master/cli.py` | user | 2 file(s) | 59 | 2 | killed |
| `u46-round-2.M7B_engine_refusal_swallowed` | `src/cratekit/master/cli.py` | user | 2 file(s) | 59 | 22 | killed |
| `r1305.A1_account_name_on_any_link` | `src/cratekit/modules/outbound/account.py` | user | 3 file(s) | 197 | 1 | killed |
| `r1305.A2_account_status_declared_only` | `src/cratekit/modules/outbound/account.py` | user | 3 file(s) | 197 | 6 | killed |
| `r1305.A4_account_reads_its_own_link_only` | `src/cratekit/modules/outbound/account.py` | user | 3 file(s) | 197 | 7 | killed |
| `u261.A1_account_forget_keeps_the_session` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 142 | 23 | killed |
| `u261.A2_account_reuse_ignores_the_hold` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 142 | 3 | killed |
| `u261.A3_account_records_no_session` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 142 | 5 | killed |
| `u261.A4_refusal_drops_no_session` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 142 | 1 | killed |
| `u97-c.C1_outbound_refusal_removed` | `src/cratekit/modules/outbound/account.py` | user | 1 file(s) | 113 | 1 | killed |
| `u131.K8_export_files_once` | `src/cratekit/modules/outbound/export.py` | user | 3 file(s) | 231 | 1 | killed |
| `u131.K9_export_refusal_kept` | `src/cratekit/modules/outbound/export.py` | user | 3 file(s) | 231 | 1 | killed |
| `u270.E1_already_on_the_playlist` | `src/cratekit/modules/outbound/export.py` | user | 4 file(s) | 257 | 6 | killed |
| `u270.E2_landed_only_what_was_answered` | `src/cratekit/modules/outbound/export.py` | user | 3 file(s) | 169 | 4 | killed |
| `u270.E3_second_row_of_one_track` | `src/cratekit/modules/outbound/export.py` | user | 2 file(s) | 145 | 1 | killed |
| `u270.E4_row_of_a_recorded_track` | `src/cratekit/modules/outbound/export.py` | user | 4 file(s) | 257 | 1 | killed |
| `u270.E5_noted_rows_are_written` | `src/cratekit/modules/outbound/export.py` | user | 3 file(s) | 134 | 1 | killed |
| `r836-c.F1_build_skips_pruned` | `src/cratekit/modules/outbound/folders.py` | user | 5 file(s) | 404 | 1 | killed |
| `r572.H1_hearts_drop_album` | `src/cratekit/modules/outbound/hearts.py` | user | 1 file(s) | 113 | 1 | killed |
| `u131.K10_kind_created_named` | `src/cratekit/modules/outbound/kinds.py` | maintainer | 2 file(s) | 111 | 1 | killed |
| `u131.K12_filing_as_shown` | `src/cratekit/modules/outbound/kinds.py` | user | 2 file(s) | 137 | 1 | killed |
| `u131.K4_ambiguous_kind` | `src/cratekit/modules/outbound/kinds.py` | user | 2 file(s) | 111 | 2 | killed |
| `u131.K5_recorded_folder` | `src/cratekit/modules/outbound/kinds.py` | user | 2 file(s) | 111 | 2 | killed |
| `u143-b.K1_legacy_name_exact` | `src/cratekit/modules/outbound/kinds.py` | user | 3 file(s) | 192 | 2 | killed |
| `r1031.M10_filter_against_raw_links` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 71 | 1 | killed |
| `r1031.M11_filter_removed` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 71 | 1 | killed |
| `r1031.M8_misses_not_a_map_read` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 71 | 1 | killed |
| `r1031.M9_malformed_miss_kept` | `src/cratekit/modules/outbound/ledger.py` | maintainer | 2 file(s) | 71 | 1 | killed |
| `r836-b.L1_adopted_anywhere_wins` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-b.L2_export_records_are_made_here` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 4 | killed |
| `r836-b.L5_older_export_refused` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 1 | killed |
| `r837-a.A8_load_carries_sets` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 419 | 23 | killed |
| `u131.K7_kind_folders_kept` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 111 | 5 | killed |
| `u147-c.M14_made_in_mirror` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 34 | 1 | killed |
| `u147-c.M15_malformed_mirrors_read` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 34 | 1 | killed |
| `u236.M19_ledger_normalizer_drops` | `src/cratekit/modules/outbound/ledger.py` | user | 8 file(s) | 225 | 8 | killed |
| `u309.U3_ledger_maps_of_maps` | `src/cratekit/modules/outbound/ledger.py` | user | 10 file(s) | 528 | 1 | killed |
| `r229.L12_the_first_of_several_is_adopted` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 2 | killed |
| `r229.L13_a_mismatch_is_never_said` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 2 | killed |
| `r229.L16_a_moved_record_is_not_followed` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 3 | killed |
| `r229.L18_contents_grow` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 5 | killed |
| `r229.L19_a_copy_not_a_move` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 6 | killed |
| `r229.L6_a_living_crate_is_a_candidate` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 3 | killed |
| `r229.L7_a_reused_path_keeps_its_record` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 2 | killed |
| `r836-b.L3_created_false_when_adopted` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 5 file(s) | 404 | 3 | killed |
| `r836-c.L6_date_on_the_confirmed_record` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 5 file(s) | 404 | 2 | killed |
| `u131.K6_adopt_not_made` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 14 | 1 | killed |
| `u147-c.M16_folder_made_twice` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 34 | 2 | killed |
| `u147-c.M17_playlist_made_twice` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 34 | 5 | killed |
| `u309.U4_reserve_recorded_wins` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 9 file(s) | 514 | 15 | killed |
| `u309.U5_reserve_written` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 9 file(s) | 514 | 136 | killed |
| `r1031.M12_link_keeps_its_miss` | `src/cratekit/modules/outbound/ledger_settle.py` | maintainer | 2 file(s) | 71 | 1 | killed |
| `r1031.M13_miss_written_over_a_link` | `src/cratekit/modules/outbound/ledger_settle.py` | maintainer | 2 file(s) | 71 | 1 | killed |
| `r836-b.L4_pruned_leaves_added` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 5 file(s) | 404 | 5 | killed |
| `r836-c.L7_row_only_for_a_written_track` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 5 file(s) | 404 | 1 | killed |
| `u150.L1_forget_checks_id` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 2 file(s) | 66 | 1 | killed |
| `u201-composites.C4_settle_none` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 5 file(s) | 187 | 5 | killed |
| `u201.L1_agreed_own_playlist` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 5 file(s) | 187 | 1 | killed |
| `u236.M17_ledger_settle_keeps_placement` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 2 file(s) | 25 | 4 | killed |
| `u236.M18_ledger_placement_not_written` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 2 file(s) | 25 | 8 | killed |
| `u236.M20_agreed_never_drops` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 8 file(s) | 225 | 3 | killed |
| `u270.L2_row_only_for_a_recorded_track` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 4 file(s) | 257 | 1 | killed |
| `r1031.M2_rematch_ignored` | `src/cratekit/modules/outbound/mirror.py` | user | 2 file(s) | 71 | 2 | killed |
| `r1031.M3_signature_keys_a_coded_row` | `src/cratekit/modules/outbound/mirror.py` | user | 2 file(s) | 71 | 1 | killed |
| `r1031.M4_signature_dropped` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 37 | 1 | killed |
| `r1031.M5_unread_miss_remembered` | `src/cratekit/modules/outbound/mirror.py` | user | 2 file(s) | 71 | 2 | killed |
| `r1031.M6_misses_never_gathered` | `src/cratekit/modules/outbound/mirror.py` | user | 2 file(s) | 71 | 6 | killed |
| `r1031.M7_remembered_not_counted` | `src/cratekit/modules/outbound/mirror.py` | user | 2 file(s) | 71 | 1 | killed |
| `r1032.M1_mirror_never_asks_any_agreeing` | `src/cratekit/modules/outbound/mirror.py` | user | 4 file(s) | 108 | 4 | killed |
| `u147-a.M1_two_root_folders` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 1 | killed |
| `u147-a.M5_persons_playlist` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 2 | killed |
| `u147-b.M11_agree_dropped` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 1 | killed |
| `u147-b.M13_links_unrecorded` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 4 | killed |
| `u147-b.M2_stale_folder_again` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 1 | killed |
| `u147-b.M8_move_new_only` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 1 | killed |
| `u147-b.M9_link_reused_blind` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 1 | killed |
| `u150.M10_link_before_known` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 2 | killed |
| `u150.M11_unmade_folder` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 2 | killed |
| `u150.M1_retire_flag` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 7 | killed |
| `u150.M2_present_guard` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 2 | killed |
| `u150.M3_retire_in_writes` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 5 | killed |
| `u150.M4_retire_in_digest` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 1 | killed |
| `u150.M5_apply_removes` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 4 | killed |
| `u150.M6_apply_forgets` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 3 | killed |
| `u150.M7_refusal_scope` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 2 | killed |
| `u150.M8_refusal_kept` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 32 | 1 | killed |
| `u150.M9_known_answers` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 1 | killed |
| `u201.M1_plan_keeps` | `src/cratekit/modules/outbound/mirror.py` | user | 5 file(s) | 187 | 6 | killed |
| `u201.M2_plan_skips` | `src/cratekit/modules/outbound/mirror.py` | user | 5 file(s) | 187 | 5 | killed |
| `u207.M1_mirror_screens_settled_rows` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 71 | 2 | killed |
| `u207.M2_mirror_counts_a_screen_as_one` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 71 | 2 | killed |
| `u309.U12_mirror_kept_source_only` | `src/cratekit/modules/outbound/mirror.py` | user | 4 file(s) | 145 | 2 | killed |
| `u201-composites.C1_two_bands_composite` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 1 file(s) | 42 | 1 | killed |
| `u201-composites.C2_agrees_never` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 1 | killed |
| `u201.E10_unknown_time` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 4 | killed |
| `u201.E11_later_strict` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 1 | killed |
| `u201.E13_snapshot_word` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 2 | killed |
| `u201.E1_never_agreed_base` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 1 | killed |
| `u201.E3_own_genre_derived_held` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 2 | killed |
| `u201.E4_own_genre_no_edit` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 1 | killed |
| `u201.E6_short_unread` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 3 | killed |
| `u201.E7_addition_beats_removal` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 1 | killed |
| `u204.P10_inbox_agreed` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.P11_inbox_hold_per_batch` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 224 | 4 | killed |
| `u204.P12_favorites_stay` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.P2_acquire_only_unknown` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 224 | 2 | killed |
| `u204.P3_off_and_into_month_held` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.P4_two_months_held` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.P6_filed_no_month` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 1 file(s) | 42 | 1 | killed |
| `u204.P9_unfavourite_settles_out` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u227.R3_all_to_any` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 7 file(s) | 187 | 2 | killed |
| `u227.R4_folder_compare` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 1 file(s) | 8 | 1 | killed |
| `u227.R5_landed_flag` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 7 file(s) | 187 | 2 | killed |
| `u227.R6_landed_item` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 7 file(s) | 187 | 1 | killed |
| `u230.K2_u227_known_guard` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 5 | killed |
| `u230.M11_empty_there` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 1 | killed |
| `u230.M12_queue_not_handed` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 6 | killed |
| `u230.M13_held_by_dropped` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 29 | killed |
| `u230.M14_no_titles_guard` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 6 | killed |
| `u230.M1_no_lift` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 6 | killed |
| `u230.M22_agreed_lifted` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 3 | killed |
| `u230.M23_short_lifted` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 1 | killed |
| `u230.M2_lift_not_in_was` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 6 | killed |
| `u230.M3_lift_not_in_held` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 5 | killed |
| `u230.M4_other_bases_ignored` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 5 | killed |
| `u230.M5_any_title` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 1 | killed |
| `u230.M6_no_landing_guard` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 2 | killed |
| `u230.M8_rekordbox_dropped` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 1 | killed |
| `u236.M1_ours_empty` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 10 | killed |
| `u236.M2_unfavourite_counts_ours` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 7 | killed |
| `u236.M3_moved_counts_ours` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 3 | killed |
| `u236.M4_moved_counts_to` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 1 | killed |
| `u236.M5_mine_not_left` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 3 | killed |
| `u236.M6_mine_includes_now` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 1 | killed |
| `u236.M7_placed_after_keeps_all` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 4 | killed |
| `u236.M8_placed_after_drops_unheld` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 3 | killed |
| `u236.M9_placed_after_ignores_hold` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 2 | killed |
| `r836-d.P1_only_created_years` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-e.P2b_mismatch_read_only_with_nothing_gone` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-e.P5_apply_asks_the_ledger_again` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-f.P7_unrowed_with_unmatched_left_alone` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-f.P8_drifted_match_left_alone` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-f.P9_row_in_playlist_keeps_its_track` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 3 | killed |
| `u243.L10_empties_never_said` | `src/cratekit/modules/outbound/prune.py` | user | 2 file(s) | 78 | 1 | killed |
| `u243.L9_prune_ignores_tombstones` | `src/cratekit/modules/outbound/prune.py` | user | 2 file(s) | 78 | 6 | killed |
| `u201.S1_short_undeclared` | `src/cratekit/modules/outbound/service.py` | user | 5 file(s) | 187 | 1 | killed |
| `u142.S1_folder_prefix` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 216 | 13 | killed |
| `u142.S2_plan_reads_the_year_key` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 216 | 3 | killed |
| `u142.S3_adopt_by_year_too` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 216 | 1 | killed |
| `u142.S5_create_under_the_year` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 216 | 6 | killed |
| `u142.S6_reserve_under_the_year` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 216 | 7 | killed |
| `u142.S7_adoption_is_a_write` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 216 | 2 | killed |
| `r227.S1_unknown_is_within_limit` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 1 | killed |
| `r227.S2_no_sentence_at_the_gate` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 5 | killed |
| `r227.S3_utc_date_in_the_sentence` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 1 | killed |
| `r227.S4_utc_instant_in_the_block` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 1 | killed |
| `r227.S5_envelope_drops_the_age` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 2 | killed |
| `r227.S6_no_stale_sentence` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 8 | killed |
| `r227.S7_floored_age_in_the_sentence` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 1 | killed |
| `r290-author.S13_outbound_shell_call_removed` | `src/cratekit/modules/outbound/shell.py` | user | 2 file(s) | 249 | 18 | killed |
| `r850-a.E10_concluded_not_called` | `src/cratekit/modules/outbound/shell.py` | user | 2 file(s) | 236 | 4 | killed |
| `r856-a.S1_tally_zero` | `src/cratekit/modules/outbound/shell.py` | user | 2 file(s) | 178 | 7 | killed |
| `r856-a.S2_tally_bool` | `src/cratekit/modules/outbound/shell.py` | user | 2 file(s) | 178 | 3 | killed |
| `u51-item-derivation.S3_empty_job_driven` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 1 | killed |
| `u51-item-derivation.S5_payload_shape` | `src/cratekit/modules/outbound/shell.py` | user | 2 file(s) | 143 | 65 | killed |
| `r227.A1_floored_days` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 372 | 2 | killed |
| `r227.A2_never_stale` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 372 | 13 | killed |
| `r227.A3_future_clamped` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 372 | 1 | killed |
| `r227.A4_no_tolerance` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 372 | 1 | killed |
| `r227.A5_half_a_pair` | `src/cratekit/modules/outbound/source.py` | maintainer | 4 file(s) | 372 | 1 | killed |
| `r227.A6_conversion_unguarded` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 372 | 1 | killed |
| `r227.A7_unreadable_reads_as_now` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 372 | 2 | killed |
| `r356-b.B1_naming_head_left_on_the_release_title` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 372 | 8 | killed |
| `r356-b.B2_template_declares_no_lossy_marker` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 372 | 1 | killed |
| `r356-b.B3_empty_marker_no_longer_guarded` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 372 | 1 | killed |
| `r356-b.B4_heart_candidate_carries_no_artist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 4 | killed |
| `r572.L1_local_track_drop_album` | `src/cratekit/modules/outbound/source.py` | user | 1 file(s) | 123 | 1 | killed |
| `r572.S1_album_not_read` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 3 | killed |
| `sitting4.G10_absent_root_reads_as_untagged` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 1 | killed |
| `sitting4.G3_builders_ignore_the_prefix_map` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 1 | killed |
| `u309.U25_source_reader_lazy_name` | `src/cratekit/modules/outbound/source.py` | user | 3 file(s) | 230 | 1 | killed |
| `u51-item-derivation.A2_default_favorites_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 27 | killed |
| `u51-item-derivation.D1_unknown_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 2 | killed |
| `u51-item-derivation.D2_ambiguous_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 1 | killed |
| `u51-item-derivation.D3_empty_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 1 | killed |
| `u51-item-derivation.D4_dangling_reported` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 2 | killed |
| `u51-item-derivation.D5_repeated_deduped` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 2 | killed |
| `u51-item-derivation.D6_export_required` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 2 | killed |
| `r1308.M11_count_before_ge` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 1 | killed |
| `r1308.M12_count_after_le` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 1 | killed |
| `r1308.M13_accept_tracks_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 8 | killed |
| `r1308.M14_lag_by_or` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 11 | killed |
| `r1308.M15_lag_always` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 12 | killed |
| `r1308.M16_no_break` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 10 | killed |
| `r1308.M18_not_forgotten` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 2 | killed |
| `r1308.M20_message_swapped` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 15 | killed |
| `r1308.M21_halves_swapped` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 1 | killed |
| `r1308.M22_retryable` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 75 | 14 | killed |
| `r1308.M23_read_back_bypassed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 34 | killed |
| `r1308.M24_positions_count` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 2 | killed |
| `r1308.M6_after_by_length` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 4 | killed |
| `r1308.M8_count_ignored` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 9 | killed |
| `r1308.M9_videos_unchecked` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 2 | killed |
| `r1394.A1_recorder_never_told` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 5 | killed |
| `r1394.A2_sent_one_short` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 5 | killed |
| `r1394.A3_landed_overstated` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 4 | killed |
| `r1394.A4_412_not_brought_down` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 2 | killed |
| `r1394.A5_any_failure_brought_down` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 3 | killed |
| `r1411.A1_agreed_order_always_stands` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 11 | killed |
| `r1411.A2_removed_tracks_asked_of_the_reading` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 3 | killed |
| `r1411.A3_added_tracks_asked_of_the_agreed_order` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 7 | killed |
| `r1411.A5_duplicates_counted_twice` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 1 | killed |
| `r1411.E1_expect_compared_as_membership` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 1 | killed |
| `r1411.E4_membership_always_agrees` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 2 | killed |
| `r1411.S1_settled_ignores_agreed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 2 | killed |
| `r1411.S2_agreed_stands_in_for_membership` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 1 | killed |
| `r1411.S3_order_does_not_pass_agreed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 2 | killed |
| `r358-round-2.A3_editor_check` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 1 | killed |
| `r358-round-2.A5_absent_answer` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 1 | killed |
| `r358-round-2.A7_empty_title_message` | `src/cratekit/modules/outbound/tidal_account.py` | maintainer | 1 file(s) | 113 | 3 | killed |
| `r358.A1_empty_title_refusal` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 3 | killed |
| `r358.A2_title_stripped_for_the_write` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 1 | killed |
| `r358.A4_false_answer` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 1 | killed |
| `r358.A6_retry_coefficient` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 1 | killed |
| `r834.M1_a_create_makes_the_playlist_private` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 4 | killed |
| `r834.M3_a_refused_private_step_does_not_lose_the_playlist` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 2 | killed |
| `r834.M5_a_create_is_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 1 | killed |
| `r836-a.A1_product_made_asked_first` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 112 | 3 | killed |
| `r836-a.A4_no_video_declared` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 498 | 1 | killed |
| `r836-a.A5_removal_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 498 | 1 | killed |
| `u143-c.A1_kind_named` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 447 | 1 | killed |
| `u143-c.A2_ledger_claimed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 447 | 1 | killed |
| `u143-c.A3_debris_served` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 447 | 2 | killed |
| `u143-c.A4_empty_videos` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 447 | 2 | killed |
| `u143-d.A5_playlist_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 447 | 5 | killed |
| `u143-d.A6_legacy_name` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 447 | 2 | killed |
| `u143-d.A7_folder_empty` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 447 | 1 | killed |
| `u143-d.A8_folder_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 447 | 1 | killed |
| `u220.A10_wrong_status` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 10 | killed |
| `u220.A11_cause_chain_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 1 | killed |
| `u220.A12_no_memory_guard` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 2 | killed |
| `u220.A13_exact_agrees` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 1 | killed |

## Row definitions

### `u237.M6_substring_again`

_words_within: back to a raw substring, so the Rawax needle confirms RAWAXXX

- File: `src/cratekit/label/verify.py`
- Source: `u237.json`, row `M6_substring_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_kept_listing.py`
- Collected: 392 against a baseline of 392
- Kills: 9 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Puls-Pulse]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[RAWAXXX-Rawax]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Rawax-RAWAXXX]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Rawax-Rawaxxx Records]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[adenza-Cadenza]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[ronos-Cronos]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[tide-Tidewater]`
  - `tests/modules/test_labels.py::test_a_release_credited_to_a_longer_act_name_is_a_mismatch_not_a_confirmation`
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`

Old text:

```
    return f" {needle} " in f" {credit} "
```

New text:

```
    return needle in credit
```

### `u237.M7_left_word_boundary_only`

_words_within: pad only the front, so a needle that is a word's prefix still confirms

- File: `src/cratekit/label/verify.py`
- Source: `u237.json`, row `M7_left_word_boundary_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_kept_listing.py`
- Collected: 392 against a baseline of 392
- Kills: 7 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Puls-Pulse]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[RAWAXXX-Rawax]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Rawax-RAWAXXX]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Rawax-Rawaxxx Records]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[tide-Tidewater]`
  - `tests/modules/test_labels.py::test_a_release_credited_to_a_longer_act_name_is_a_mismatch_not_a_confirmation`
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`

Old text:

```
    return f" {needle} " in f" {credit} "
```

New text:

```
    return f" {needle}" in f" {credit} "
```

### `u105-b.S10_settings_to_engine`

Call the engine without the settings built from the frozen target

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S10_settings_to_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 129 against a baseline of 129
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_the_target_reaches_every_loudnorm_filter`

Old text:

```
            settings=settings,
            output_dir=Path(output_dir) if output_dir else None,
```

New text:

```
            output_dir=Path(output_dir) if output_dir else None,
```

### `u105-b.S1_parts_only_when_several`

Freeze the parts key for a single recording too

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S1_parts_only_when_several`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 129 against a baseline of 129
- Kills: 3 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`
  - `tests/test_master_cli.py::test_one_input_freezes_queues_and_resumes_exactly_as_before`

Old text:

```
    if len(frozen) > 1:
```

New text:

```
    if frozen:
```

### `u105-b.S2_lufs_frozen`

Do not freeze --lufs into the payload

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S2_lufs_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 129 against a baseline of 129
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_the_target_reaches_every_loudnorm_filter`

Old text:

```
        payload[TARGET_LUFS] = float(lufs)
```

New text:

```
        pass
```

### `u105-b.S3_lufs_in_argv`

Drop --lufs from the resume command line

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S3_lufs_in_argv`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`

Old text:

```
        argv.append(f"--lufs={lufs}")
```

New text:

```
        pass
```

### `u105-b.S4_parts_in_argv`

Rebuild the resume command line from the first part alone

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S4_parts_in_argv`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`

Old text:

```
    argv = ["master", *frozen_parts(payload)]
```

New text:

```
    argv = ["master", str(payload.get(SOURCE) or "")]
```

### `u105-b.S5_queue_time_refusal`

Stop validating --lufs at queue time

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S5_queue_time_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 129 against a baseline of 129
- Kills: 3 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-4]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-71]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[nan]`

Old text:

```
    settings_for(ctx.args.lufs)
```

New text:

```
    pass
```

### `u105-b.S6_join_order_notice`

Queue a split recording without saying its order back

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S6_join_order_notice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_the_order_printed_is_the_order_given`

Old text:

```
        notices = (join_order_warning(frozen_parts(payload)),) if PARTS in payload else ()
```

New text:

```
        notices = ()
```

### `u105-b.S7_staged_parts`

Stage a split recording's run without its parts, mastering part one alone

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S7_staged_parts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`

Old text:

```
        staged[PARTS] = [str(p) for p in parts]
```

New text:

```
        pass
```

### `u105-b.S8_staged_target`

Stage the run without the frozen target, mastering at the default

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S8_staged_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`

Old text:

```
        staged[TARGET_LUFS] = payload[TARGET_LUFS]
```

New text:

```
        pass
```

### `u105-b.S9_precheck_name`

Pre-check the destination with part one's master name instead of the joined one

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S9_precheck_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 129 against a baseline of 129
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`

Old text:

```
    final = mastering.planned_output(
        parts, output_dir=Path(str(output_dir)) if output_dir else None
    )
```

New text:

```
    final = mastering.output_path(
        parts[0], output_dir=Path(str(output_dir)) if output_dir else None
    )
```

### `u44-author.C2_argv_drops_overwrite`

Drop --overwrite from the resume argv, so a respawned child meets the refusal the first run was told to ignore

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C2_argv_drops_overwrite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`
  - `tests/test_master_cli.py::test_the_resume_argv_rebuilds_every_frozen_flag_and_omits_absent_ones`

Old text:

```
    if payload.get(OVERWRITE):
        argv.append("--overwrite")
```

New text:

```
(empty)
```

### `u44-author.C3_argv_drops_output_dir`

Drop --output-dir from the resume argv, so the child writes the master somewhere the person did not ask for

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C3_argv_drops_output_dir`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`
  - `tests/test_master_cli.py::test_the_resume_argv_rebuilds_every_frozen_flag_and_omits_absent_ones`

Old text:

```
    if output_dir:
        argv += ["--output-dir", str(output_dir)]
```

New text:

```
(empty)
```

### `u44-author.C4_refusal_not_translated`

Let MasteringRefused escape, so every engine refusal reaches the person as internal-error

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C4_refusal_not_translated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 57 against a baseline of 57
- Kills: 22 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone`
  - `tests/test_master_cli.py::test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy`
  - `tests/test_master_cli.py::test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding`
  - `tests/test_master_cli.py::test_a_failing_encode_does_not_report_success`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_part_refuses_as_missing`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_part_named_twice_or_in_another_container_refuses_before_any_command[containers]`
  - `tests/test_master_cli.py::test_a_part_named_twice_or_in_another_container_refuses_before_any_command[twice]`
  - `tests/test_master_cli.py::test_a_recording_that_is_not_there_refuses_rather_than_raising`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`
  - `tests/test_master_cli.py::test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`
  - ... and 7 more, see the JSON sidecar

Old text:

```
    except mastering.MasteringRefused as exc:
        raise refuse(
            str(exc.refusal),
            exc.detail,
            origin=("master", "cli"),
            detail={"path": str(exc.path) if exc.path is not None else None},
        ) from exc
```

New text:

```
    except ZeroDivisionError as exc:
        raise refuse(
            str(exc),
            "unreachable",
            origin=("master", "cli"),
        ) from exc
```

### `u44-author.C6_overwrite_always_true`

Freeze overwrite as always true, so every run replaces an existing master without being asked to

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C6_overwrite_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 57 against a baseline of 57
- Kills: 4 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_an_existing_master_refuses_without_overwrite_and_proceeds_with_it`
  - `tests/test_master_cli.py::test_one_input_freezes_queues_and_resumes_exactly_as_before`

Old text:

```
        OVERWRITE: bool(overwrite),
```

New text:

```
        OVERWRITE: True,
```

### `u44-author.C7_output_dir_ignored_at_the_work`

Ignore the frozen output directory, so the master lands beside the source whatever was asked for

- File: `src/cratekit/master/cli.py`
- Source: `u44-author.json`, row `C7_output_dir_ignored_at_the_work`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_master_cli.py`
- Collected: 57 against a baseline of 57
- Kills: 3 (killed)
- Killed:
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_the_encode_lands_in_staging_and_is_committed_rather_than_written_in_place`
  - `tests/test_master_cli.py::test_the_output_directory_is_honoured_and_never_the_source`

Old text:

```
            output_dir=Path(output_dir) if output_dir else None,
```

New text:

```
            output_dir=None,
```

### `u46-author.M1_no_items_enqueued`

Queue the recording with no item, so the driver has nothing to claim

- File: `src/cratekit/master/cli.py`
- Source: `u46-author.json`, row `M1_no_items_enqueued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 59 against a baseline of 59
- Kills: 17 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume`
  - `tests/test_master_cli.py::test_a_handler_that_raises_an_undeclared_error_fails_the_item_not_the_driver`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_nothing_is_created_beside_a_destination_for_a_recording_that_is_not_there`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_queueing_a_recording_gives_the_driver_one_item_to_claim`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            item_ids=(str(payload[SOURCE]),),
```

New text:

```
(empty)
```

### `u46-round-2.M6_staging_not_cleared`

Leave a previous attempt's partial encode in the staging directory

- File: `src/cratekit/master/cli.py`
- Source: `u46-round-2.json`, row `M6_staging_not_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)
```

New text:

```
(empty)
```

### `u46-round-2.M7B_engine_refusal_swallowed`

Translate the engine's encoder-failed into a generic internal defect

- File: `src/cratekit/master/cli.py`
- Source: `u46-round-2.json`, row `M7B_engine_refusal_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 59 against a baseline of 59
- Kills: 22 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone`
  - `tests/test_master_cli.py::test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy`
  - `tests/test_master_cli.py::test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding`
  - `tests/test_master_cli.py::test_a_failing_encode_does_not_report_success`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_part_refuses_as_missing`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_part_named_twice_or_in_another_container_refuses_before_any_command[containers]`
  - `tests/test_master_cli.py::test_a_part_named_twice_or_in_another_container_refuses_before_any_command[twice]`
  - `tests/test_master_cli.py::test_a_recording_that_is_not_there_refuses_rather_than_raising`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`
  - `tests/test_master_cli.py::test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`
  - ... and 7 more, see the JSON sidecar

Old text:

```
            str(exc.refusal),
            exc.detail,
```

New text:

```
            "internal-error",
            "the mastering engine refused",
```

### `r1305.A1_account_name_on_any_link`

_session_refused: read the client's authentication error by name on any link, so a reset met while handling one drops the account and asks for a login

- File: `src/cratekit/modules/outbound/account.py`
- Source: `r1305.json`, row `A1_account_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_failure_after_login_that_is_no_rejection_is_a_wait[context]`

Old text:

```
        if declared and type(link).__name__ == "AuthenticationError":
```

New text:

```
        if type(link).__name__ == "AuthenticationError":
```

### `r1305.A2_account_status_declared_only`

_session_refused: read a status on the declared chain only, so a session rejected mid sweep with a page is told to wait

- File: `src/cratekit/modules/outbound/account.py`
- Source: `r1305.json`, row `A2_account_status_declared_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`
- Collected: 197 against a baseline of 197
- Kills: 6 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_failure_after_login_that_is_no_rejection_is_a_wait[outage]`
  - `tests/test_provider_rejection_bodies.py::test_a_failure_whose_body_is_not_json_judges_the_held_account[a-rejection-drops-the-held-account]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_failure_that_is_no_rejection_is_a_wait[outage]`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_rewrapped_by_the_client_still_asks_for_a_login`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[403-html]`

Old text:

```
        if answered_status(link) in SESSION_REFUSED_STATUSES:
```

New text:

```
        if declared and answered_status(link) in SESSION_REFUSED_STATUSES:
```

### `r1305.A4_account_reads_its_own_link_only`

_session_refused: read the failure alone and no link of it, so a rejection the client rewraps is told to wait

- File: `src/cratekit/modules/outbound/account.py`
- Source: `r1305.json`, row `A4_account_reads_its_own_link_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`
- Collected: 197 against a baseline of 197
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rejection_the_client_rewraps_is_still_read_as_a_rejected_session`
  - `tests/test_provider_rejection_bodies.py::test_a_failure_after_login_that_is_no_rejection_is_a_wait[outage]`
  - `tests/test_provider_rejection_bodies.py::test_a_failure_whose_body_is_not_json_judges_the_held_account[a-rejection-drops-the-held-account]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_failure_that_is_no_rejection_is_a_wait[outage]`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_rewrapped_by_the_client_still_asks_for_a_login`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[403-html]`

Old text:

```
    for link, declared in failure_links(exc):
        if answered_status(link) in SESSION_REFUSED_STATUSES:
```

New text:

```
    for link, declared in [(exc, True)]:
        if answered_status(link) in SESSION_REFUSED_STATUSES:
```

### `u261.A1_account_forget_keeps_the_session`

account.forget: drop the adapter and keep the shared session, so a 401 on the account leaves the catalogue the refused client

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A1_account_forget_keeps_the_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 142 against a baseline of 142
- Kills: 23 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_a_login_that_fails_names_whether_to_log_in_again_or_wait[rejected]`
  - `tests/test_outbound_tidal_account.py::test_a_login_that_fails_names_whether_to_log_in_again_or_wait[unreachable]`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_export_runs_to_done_and_the_ledger_records_every_add`
  - `tests/test_outbound_tidal_account.py::test_a_provider_failure_on_one_heart_fails_that_item_and_no_other`
  - `tests/test_outbound_tidal_account.py::test_a_release_the_account_already_hearts_is_the_one_an_export_adds`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope`
  - `tests/test_outbound_tidal_account.py::test_one_process_logs_in_once_however_many_items_resolve`
  - `tests/test_provider_session_hold.py::test_a_lost_app_value_is_noted_on_every_resolve_that_falls_back`
  - `tests/test_provider_session_hold.py::test_a_refreshed_login_is_reused_while_the_keychain_holds_the_refresh`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    _OPENED_OVER = None
    provider_session.forget()
```

New text:

```
    _OPENED_OVER = None
```

### `u261.A2_account_reuse_ignores_the_hold`

account.resolve: hand out the held adapter whatever became of its session, so a client the catalogue saw refused is reused by the account

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A2_account_reuse_ignores_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 142 against a baseline of 142
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`

Old text:

```
    if _OPENED is not None and _OPENED_OVER is provider_session.held():
```

New text:

```
    if _OPENED is not None:
```

### `u261.A3_account_records_no_session`

account.resolve: record no session under the adapter, so the adapter is opened afresh on every resolve and the one login per process is lost

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A3_account_records_no_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 142 against a baseline of 142
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_one_process_logs_in_once_however_many_items_resolve`
  - `tests/test_provider_session_hold.py::test_a_process_resolving_both_seams_validates_the_session_once`
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`
  - `tests/test_provider_session_hold.py::test_an_old_clients_refusal_on_the_account_keeps_the_session_logged_in_since`

Old text:

```
    _OPENED_OVER = provider_session.held()
    return opened
```

New text:

```
    _OPENED_OVER = None
    return opened
```

### `u261.A4_refusal_drops_no_session`

account._forget_refused: drop the adapter and keep the shared session it was built over, so a 401 on the account leaves the catalogue the refused client

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A4_refusal_drops_no_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 142 against a baseline of 142
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_401_on_the_account_drops_the_shared_client_and_the_catalogue_logs_in_again`

Old text:

```
    else:
        provider_session.drop(over)
```

New text:

```
    else:
        pass
```

### `u97-c.C1_outbound_refusal_removed`

composite for B4: remove the outbound account's missing session refusal entirely, so the seam opens a client with no credential. Shows what the guard holds when its remedy holds nothing

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u97-c.json`, row `C1_outbound_refusal_removed`
- Moved: the missing session refusal stays in account.resolve but is now built by the shared _credential_missing helper rather than refuse; same condition reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_session_removed_after_an_open_is_refused_rather_than_reused`

Old text:

```
    if not secrets.exists(str(secrets.Credential.PROVIDER_SESSION)):
        raise _credential_missing(
```

New text:

```
    if False:
        raise _credential_missing(
```

### `u131.K8_export_files_once`

export.apply: file on every apply rather than only the one that created the playlist

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u131.json`, row `K8_export_files_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_export_collection.py`, `tests/test_outbound_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_new_export_is_filed_in_exports_at_creation`

Old text:

```
    if reserved.created:
        # FILED AT CREATION
```

New text:

```
    if True:
        # FILED AT CREATION
```

### `u131.K9_export_refusal_kept`

export.apply: let a ledger or raw error filing at creation fail the finished export

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u131.json`, row `K9_export_refusal_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_export_collection.py`, `tests/test_outbound_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`

Old text:

```
        except Exception as exc:  # noqa: BLE001 - reported as the warning
```

New text:

```
        except KeyError as exc:  # noqa: BLE001 - reported as the warning
```

### `u270.E1_already_on_the_playlist`

apply: read only the ledger for what is already there, so a track a person put on the playlist is sent and recorded as ours

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u270.json`, row `E1_already_on_the_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 257 against a baseline of 257
- Kills: 6 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice`
  - `tests/test_outbound_export_batches.py::test_a_stop_between_the_request_and_the_record_adds_nothing_twice_and_records_nothing_unanswered[ceiling-park]`
  - `tests/test_outbound_export_batches.py::test_a_stop_between_the_request_and_the_record_adds_nothing_twice_and_records_nothing_unanswered[refused-read]`
  - `tests/test_outbound_export_batches.py::test_a_track_a_person_adds_after_a_refused_add_is_never_claimed`
  - `tests/test_outbound_export_batches.py::test_a_track_on_the_playlist_or_recorded_is_not_sent`
  - `tests/test_outbound_export_batches.py::test_reads_refused_past_the_retry_fail_the_batch_and_the_resume_adds_nothing_twice`

Old text:

```
        if remote in already_on or remote in already_recorded:
```

New text:

```
        if remote in already_recorded:
```

### `u270.E2_landed_only_what_was_answered`

apply: record every track sent, answered or not, so the ledger names a track the playlist does not hold

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u270.json`, row `E2_landed_only_what_was_answered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`, `tests/test_outbound_add_requests.py`
- Collected: 169 against a baseline of 169
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_a_batch_answered_in_part_on_the_real_client_is_settled_by_one_read_back`
  - `tests/test_outbound_export_batches.py::test_a_batch_answered_in_part_records_only_what_the_answer_names`
  - `tests/test_outbound_export_batches.py::test_two_rows_matched_to_one_refused_track_are_both_refused`
  - `tests/test_outbound_workers.py::test_a_track_the_provider_would_not_add_fails_its_item_alone_and_is_never_recorded`

Old text:

```
    landed = {local: remote for local, remote in lacking.items() if remote in answered}
```

New text:

```
    landed = {local: remote for local, remote in lacking.items()}
```

### `u270.E3_second_row_of_one_track`

apply: report each row matched to one track as added, so the summary counts the track written twice

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u270.json`, row `E3_second_row_of_one_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_two_rows_matched_to_one_track_send_it_once_and_record_both_rows`

Old text:

```
        if said == ADDED and remote in added:
```

New text:

```
        if False:
```

### `u270.E4_row_of_a_recorded_track`

apply: never note the row of a track already recorded, so a prune cannot tell a row that left from a match that drifted

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u270.json`, row `E4_row_of_a_recorded_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/modules/test_outbound.py`, `tests/test_prune.py`, `tests/test_outbound_workers.py`
- Collected: 257 against a baseline of 257
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_a_re_export_names_the_rows_of_tracks_recorded_before_rows_were_kept`

Old text:

```
                noted[local] = remote
```

New text:

```
                pass
```

### `u270.E5_noted_rows_are_written`

apply: write the ledger only when a track landed, so the rows of tracks recorded before R-836 are never named

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u270.json`, row `E5_noted_rows_are_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/modules/test_outbound.py`, `tests/test_prune.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_a_re_export_names_the_rows_of_tracks_recorded_before_rows_were_kept`

Old text:

```
    if landed or noted:
```

New text:

```
    if landed:
```

### `r836-c.F1_build_skips_pruned`

folders.plan: a track a prune took off is added again by the next label build

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r836-c.json`, row `F1_build_skips_pruned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_pruned_track_is_not_put_back_by_the_next_build`

Old text:

```
            asked = recorded.added | recorded.refused | recorded.pruned
```

New text:

```
            asked = recorded.added | recorded.refused
```

### `r572.H1_hearts_drop_album`

The hearts engine stops passing the album to match_track

- File: `src/cratekit/modules/outbound/hearts.py`
- Source: `r572.json`, row `H1_hearts_drop_album`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`

Old text:

```
            album=item.album,
```

New text:

```
(empty)
```

### `u131.K10_kind_created_named`

kinds.reserve: do not name a kind folder created before a failed ledger write

- File: `src/cratekit/modules/outbound/kinds.py`
- Source: `u131.json`, row `K10_kind_created_named`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_each_kind_lands_in_its_own_folder`

Old text:

```
        if made is not None:
            made.append(folder.kind)
```

New text:

```
        pass
```

### `u131.K12_filing_as_shown`

kinds.file_new: file whatever the account says now rather than only the decision the gate showed

- File: `src/cratekit/modules/outbound/kinds.py`
- Source: `u131.json`, row `K12_filing_as_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_playlist_kinds.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning`

Old text:

```
    if token(folder) != planned:
```

New text:

```
    if False:
```

### `u131.K4_ambiguous_kind`

kinds.decide: take the first of two root folders named as the kind rather than leave its playlists

- File: `src/cratekit/modules/outbound/kinds.py`
- Source: `u131.json`, row `K4_ambiguous_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 2 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_an_export_whose_folder_a_name_cannot_decide_stays_at_the_root`
  - `tests/test_playlist_kinds.py::test_two_folders_named_mine_leave_the_authors_playlists_listed`

Old text:

```
    if len(named) > 1:
```

New text:

```
    if len(named) > 99:
```

### `u131.K5_recorded_folder`

kinds.decide: ignore the recorded folder, so a folder a person renamed is replaced by a new one

- File: `src/cratekit/modules/outbound/kinds.py`
- Source: `u131.json`, row `K5_recorded_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 2 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_playlist_marked_after_it_was_filed_in_mine_reaches_its_year`
  - `tests/test_playlist_kinds.py::test_a_renamed_playlist_and_a_renamed_folder_stay_where_they_are`

Old text:

```
    if recorded.folder_id and recorded.folder_id in root:
```

New text:

```
    if False:
```

### `u143-b.K1_legacy_name_exact`

Legacy name: search rather than match the whole name

- File: `src/cratekit/modules/outbound/kinds.py`
- Source: `u143-b.json`, row `K1_legacy_name_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`, `tests/test_outbound_workers.py`, `tests/test_playlist_kinds.py`
- Collected: 192 against a baseline of 192
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_only_a_year_and_these_exact_words_name_a_legacy_folder[2026 Custom Playlists 2-]`
  - `tests/test_organize_root.py::test_only_a_year_and_these_exact_words_name_a_legacy_folder[My 2026 Custom Playlists-]`

Old text:

```
    found = _LEGACY_YEAR.fullmatch(str(name or ""))
```

New text:

```
    found = _LEGACY_YEAR.search(str(name or ""))
```

### `r1031.M10_filter_against_raw_links`

ledger._load: drop a miss beside a raw link entry with no account track, the review's round one finding

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M10_filter_against_raw_links`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_link_with_no_account_track_does_not_hide_a_miss`

Old text:

```
            and str(content_id) not in linked
```

New text:

```
            and str(content_id) not in links
```

### `r1031.M11_filter_removed`

ledger._load: keep a miss of a row the ledger links

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M11_filter_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_ledger_holding_a_link_and_a_miss_of_one_row_reads_the_link`

Old text:

```
            and str(content_id) not in linked
```

New text:

```
            and True
```

### `r1031.M8_misses_not_a_map_read`

ledger._load: read a mirror_misses that is not a map instead of refusing

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M8_misses_not_a_map_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_ledger_whose_misses_are_not_a_map_refuses`

Old text:

```
    if not isinstance(misses, Mapping):
        raise _unusable(path, "mirror_misses must be a map of content row to its miss")
```

New text:

```
    if False:
        raise _unusable(path, "mirror_misses must be a map of content row to its miss")
```

### `r1031.M9_malformed_miss_kept`

ledger._load: keep a miss whose key is not a list

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M9_malformed_miss_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_malformed_miss_is_dropped_and_asked_again_rather_than_refusing`

Old text:

```
            and isinstance(value.get("under"), list)
```

New text:

```
            and True
```

### `r836-b.L1_adopted_anywhere_wins`

ledger.product_made: a label year adopted from the account no longer answers no, so another record of the same id vouches for it

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r836-b.json`, row `L1_adopted_anywhere_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_adopted_anywhere_wins_over_another_record_of_the_same_playlist`

Old text:

```
                if entry.get("created") is not True:
                    return False
                made = True
```

New text:

```
                if entry.get("created") is True:
                    made = True
```

### `r836-b.L2_export_records_are_made_here`

ledger.product_made: an exported playlist's record no longer vouches, so export prune can never take a track off

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r836-b.json`, row `L2_export_records_are_made_here`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 4 (killed)
- Killed:
  - `tests/test_prune.py::test_a_playlist_written_before_rows_is_pruned_by_match_when_every_row_agrees`
  - `tests/test_prune.py::test_a_row_whose_match_failed_today_does_not_stop_a_track_recorded_by_its_row`
  - `tests/test_prune.py::test_an_exported_playlist_whose_library_playlist_lost_a_track_plans_exactly_it`
  - `tests/test_prune.py::test_product_made_says_yes_only_where_a_record_does`

Old text:

```
    for record in (*document["playlists"].values(), *document["sets"].values()):
```

New text:

```
    for record in document["sets"].values():
```

### `r836-b.L5_older_export_refused`

ledger.older_than: an export whose date could not be read is not older, so it is read for a prune

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r836-b.json`, row `L5_older_export_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_the_export_worker_records_the_date_of_the_export_it_read`

Old text:

```
    return not given or _later(recorded, given)
```

New text:

```
    return bool(given) and _later(recorded, given)
```

### `r837-a.A8_load_carries_sets`

ledger._load: the sets map is dropped on read, so every later write forgets each set playlist

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r837-a.json`, row `A8_load_carries_sets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_export_set.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 419 against a baseline of 419
- Kills: 23 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_track_settled_twice_on_a_set_playlist_is_recorded_once`
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_name_with_a_slash_finds_the_set_it_named_at_build`
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_export_set.py::test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match`
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_tidal_list_documents_own_identifiers_are_used_without_a_search`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - ... and 8 more, see the JSON sidecar

Old text:

```
            for key, value in sets.items()
```

New text:

```
            for key, value in ()
```

### `u131.K7_kind_folders_kept`

ledger._load: drop the kind folder records on read, so the next write forgets them

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u131.json`, row `K7_kind_folders_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 5 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_playlist_marked_after_it_was_filed_in_mine_reaches_its_year`
  - `tests/test_playlist_kinds.py::test_a_renamed_playlist_and_a_renamed_folder_stay_where_they_are`
  - `tests/test_playlist_kinds.py::test_a_stale_kind_folder_record_is_replaced`
  - `tests/test_playlist_kinds.py::test_each_kind_lands_in_its_own_folder`
  - `tests/test_playlist_kinds.py::test_the_kind_folders_record_survives_another_write`

Old text:

```
            for kind, value in kind_folders.items()
            if value.get("folder_id")
```

New text:

```
            for kind, value in kind_folders.items()
            if False
```

### `u147-c.M14_made_in_mirror`

ledger._made_in: a mirrored playlist is no longer vouched for, so no track may come off it (R-836)

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u147-c.json`, row `M14_made_in_mirror`
- Moved: ledger._made_in's loop over every mirrored playlist's record became one any() over the shared _mirrored iterator, so the mirrored vouching is removed by returning False in its place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_track_added_by_hand_to_a_mirrored_playlist_is_removed_and_named`

Old text:

```
    # U147. A mirrored playlist is only ever created, never adopted.
    return any(str(entry.get("remote_id") or "") == wanted for entry in _mirrored(document))
```

New text:

```
    return False
```

### `u147-c.M15_malformed_mirrors_read`

ledger._load: a malformed mirror record is read rather than refused

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u147-c.json`, row `M15_malformed_mirrors_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_malformed_mirror_record_refuses_rather_than_reading_as_none`

Old text:

```
        raise _unusable(path, "mirrors must be a map of mirrored folder records")
```

New text:

```
        mirrors = {}
```

### `u236.M19_ledger_normalizer_drops`

ledger load: drop every folder's placements on read and write

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u236.json`, row `M19_ledger_normalizer_drops`
- Moved: the placements kept on load are still in ledger.py, but the mirrored folder normalizer was pulled out of _load into _mirror_document, so the lines sit eight spaces shallower; same placements dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 8 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_survives_the_ledgers_own_read_and_write`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
            {"placed": placed}
            if (placed := _placements(value.get("placed")))
            else {}

```

New text:

```
            {}

```

### `u309.U3_ledger_maps_of_maps`

The ledger's load takes a table whose values are not maps as well formed

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u309.json`, row `U3_ledger_maps_of_maps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_sync_twins.py`, `tests/test_export_set.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_edits.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`, `tests/test_playlist_kinds.py`
- Collected: 528 against a baseline of 528
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_malformed_mirror_record_refuses_rather_than_reading_as_none`

Old text:

```
    return isinstance(value, Mapping) and all(isinstance(one, Mapping) for one in value.values())
```

New text:

```
    return isinstance(value, Mapping)
```

### `r229.L12_the_first_of_several_is_adopted`

Two candidates are settled by taking the first rather than reported and left

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L12_the_first_of_several_is_adopted`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_two_candidates_are_both_named_and_neither_is_adopted`
  - `tests/test_outbound_workers.py::test_two_orphaned_records_that_could_each_be_it_adopt_neither`

Old text:

```
    if len(found) != 1:
        return Recognition(crate=len(wanted), candidates=candidates)
```

New text:

```
    if not found:
        return Recognition(crate=len(wanted), candidates=candidates)
```

### `r229.L13_a_mismatch_is_never_said`

A record under the crate's own path written from other music is reported as an ordinary update

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L13_a_mismatch_is_never_said`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_under_the_crates_own_path_written_from_other_music_is_said`
  - `tests/test_outbound_workers.py::test_a_path_reused_for_a_different_crate_is_said_at_the_gate`

Old text:

```
        mismatched = bool(written) and not _still_carries(written, wanted)
```

New text:

```
        mismatched = False
```

### `r229.L16_a_moved_record_is_not_followed`

The confirmed remote id is ignored, so a half driven job whose record moved creates a second playlist

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L16_a_moved_record_is_not_followed`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_job_confirmed_before_its_record_moved_goes_on_writing_to_it`
  - `tests/modules/test_outbound.py::test_a_job_whose_confirmed_remote_playlist_nothing_records_refuses`
  - `tests/test_outbound_workers.py::test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing`

Old text:

```
        if expected and own != expected:
```

New text:

```
        if False:
```

### `r229.L18_contents_grow`

The recorded contents are appended to rather than replaced, which is the ever growing log the review found

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L18_contents_grow`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_job_confirmed_before_its_record_moved_goes_on_writing_to_it`
  - `tests/modules/test_outbound.py::test_an_adopted_record_moves_and_no_playlist_is_created`
  - `tests/modules/test_outbound.py::test_the_move_is_reported_once_under_the_per_item_shape`
  - `tests/modules/test_outbound.py::test_the_recorded_contents_are_replaced_and_not_grown`
  - `tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`

Old text:

```
        record["tracks"] = contents
        dirty = True
```

New text:

```
        record["tracks"] = [*_listed(record, "tracks"), *contents]
        dirty = True
```

### `r229.L19_a_copy_not_a_move`

The adopted record is copied to the new key and left under the old one, so two keys name one remote playlist

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L19_a_copy_not_a_move`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 6 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_job_confirmed_before_its_record_moved_goes_on_writing_to_it`
  - `tests/modules/test_outbound.py::test_an_adopted_record_moves_and_no_playlist_is_created`
  - `tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`
  - `tests/test_outbound_workers.py::test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing`
  - `tests/test_outbound_workers.py::test_a_renamed_crate_updates_its_remote_playlist`
  - `tests/test_outbound_workers.py::test_two_crates_offered_one_orphan_do_not_both_get_it`

Old text:

```
    record = playlists.pop(recorded_key)
```

New text:

```
    record = dict(playlists[recorded_key])
```

### `r229.L6_a_living_crate_is_a_candidate`

A recorded key the export still carries is offered, so two crates sharing their tracks adopt each other

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L6_a_living_crate_is_a_candidate`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_key_the_export_still_carries_is_not_a_candidate`
  - `tests/modules/test_outbound.py::test_a_legacy_record_under_a_living_path_is_never_freed`
  - `tests/test_outbound_workers.py::test_a_crate_the_export_still_carries_is_never_adopted_from`

Old text:

```
        if key in living and (not written or _still_carries(written, living[key])):
```

New text:

```
        if False and (not written or _still_carries(written, living[key])):
```

### `r229.L7_a_reused_path_keeps_its_record`

A displaced record is never freed, so a crate renamed away from a reused path forks as it did before

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L7_a_reused_path_keeps_its_record`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_path_reused_for_a_different_crate_frees_its_record`
  - `tests/test_outbound_workers.py::test_a_path_reused_for_a_different_crate_is_said_at_the_gate`

Old text:

```
        if key in living and (not written or _still_carries(written, living[key])):
```

New text:

```
        if key in living:
```

### `r836-b.L3_created_false_when_adopted`

ledger.reserve_label_year: an adopted year is written as created, so a prune takes tracks off a playlist the source system made

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r836-b.json`, row `L3_created_false_when_adopted`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 3 (killed)
- Killed:
  - `tests/test_prune.py::test_a_year_adopted_from_the_account_is_said_and_left_alone`
  - `tests/test_prune.py::test_adopted_anywhere_wins_over_another_record_of_the_same_playlist`
  - `tests/test_prune.py::test_product_made_says_yes_only_where_a_record_does`

Old text:

```
            "created": not adopt,
```

New text:

```
            "created": True,
```

### `r836-c.L6_date_on_the_confirmed_record`

ledger._note_written: the export date goes on the key's own record, not the one the job was confirmed to update

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r836-c.json`, row `L6_date_on_the_confirmed_record`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing`
  - `tests/test_prune.py::test_the_export_date_goes_on_the_record_the_job_was_confirmed_to_update`

Old text:

```
    if expected and str((record or {}).get("remote_id") or "") != expected:
```

New text:

```
    if False:
```

### `u131.K6_adopt_not_made`

ledger.reserve_kind_folder: record an adopted folder as made here

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u131.json`, row `K6_adopt_not_made`
- Moved: reserve_kind_folder moved into ledger_reserve and records through _reserve_folder, which passes created False for an adopted folder to the kind's own keep lambda; that lambda's record is made to say created True, so an adopted kind folder is again recorded as made here and the answer is unchanged
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_hand_made_folder_named_mine_is_adopted_and_never_emptied`

Old text:

```
            {kind: {"folder_id": folder_id, "created": created}}

```

New text:

```
            {kind: {"folder_id": folder_id, "created": True}}

```

### `u147-c.M16_folder_made_twice`

ledger.reserve_mirror_folder: a recorded folder is not reused, so a resume makes a second

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u147-c.json`, row `M16_folder_made_twice`
- Moved: reserve_mirror_folder moved from ledger.py to ledger_reserve.py and its reuse of a recorded folder is now the shared _reserve_folder, used by the label, set and mirror folders alike; same reuse guard removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run`
  - `tests/test_organize_mirror.py::test_an_apply_stopped_after_the_folder_was_created_resumes_without_a_second_folder`

Old text:

```
        recorded = entry(document)
        if recorded and recorded != stale:
            return recorded, False

```

New text:

```
        recorded = entry(document)

```

### `u147-c.M17_playlist_made_twice`

ledger.reserve_mirror_playlist: a recorded playlist is not reused, so a resume makes a second

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u147-c.json`, row `M17_playlist_made_twice`
- Moved: the reuse of a recorded playlist moved from ledger.reserve_mirror_playlist into ledger_reserve._reserve, shared by reserve_mirror_playlist and the other playlist reserves, where the mirror entry arrives as a table and the key as a parameter; the same lookup and early return are deleted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run`
  - `tests/test_organize_mirror.py::test_a_removal_the_account_refuses_is_kept_named_and_the_apply_goes_on`
  - `tests/test_organize_mirror.py::test_a_track_added_by_hand_to_a_mirrored_playlist_is_removed_and_named`
  - `tests/test_organize_mirror.py::test_a_track_moved_from_med_to_high_is_added_to_one_and_removed_from_the_other`
  - `tests/test_organize_mirror.py::test_an_apply_stopped_after_the_folder_was_created_resumes_without_a_second_folder`

Old text:

```
        held = table(document)
        recorded = str((held.get(key) or {}).get("remote_id") or "")
        if recorded:
            return recorded, False

```

New text:

```
        held = table(document)

```

### `u309.U4_reserve_recorded_wins`

A reservation creates again over the playlist the ledger already records

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u309.json`, row `U4_reserve_recorded_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_sync_twins.py`, `tests/test_export_set.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_edits.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 514 against a baseline of 514
- Kills: 15 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_organize_mirror.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run`
  - `tests/test_organize_mirror.py::test_a_removal_the_account_refuses_is_kept_named_and_the_apply_goes_on`
  - `tests/test_organize_mirror.py::test_a_track_added_by_hand_to_a_mirrored_playlist_is_removed_and_named`
  - `tests/test_organize_mirror.py::test_a_track_moved_from_med_to_high_is_added_to_one_and_removed_from_the_other`
  - `tests/test_organize_mirror.py::test_an_apply_stopped_after_the_folder_was_created_resumes_without_a_second_folder`
  - `tests/test_organize_mirror_edits.py::test_a_folder_that_is_not_a_genre_folder_is_mirrored_one_way`
  - `tests/test_organize_mirror_edits.py::test_a_move_in_rekordbox_after_an_edit_was_taken_is_rekordboxs`
  - `tests/test_organize_mirror_edits.py::test_a_short_playlists_snapshot_advances_so_a_rekordbox_move_is_never_read_as_an_edit`
  - `tests/test_organize_mirror_edits.py::test_an_edit_on_a_playlist_never_agreed_is_put_back_and_nothing_in_the_library_changes`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_rekordbox_move`

Old text:

```
        if recorded:
            return recorded, False
        remote_id = create()
```

New text:

```
        if False:
            return recorded, False
        remote_id = create()
```

### `u309.U5_reserve_written`

A reservation's new identifier is never written to the ledger

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u309.json`, row `U5_reserve_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_sync_twins.py`, `tests/test_export_set.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_edits.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 514 against a baseline of 514
- Kills: 136 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_track_settled_twice_on_a_set_playlist_is_recorded_once`
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_name_with_a_slash_finds_the_set_it_named_at_build`
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_export_set.py::test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match`
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_tidal_list_documents_own_identifiers_are_used_without_a_search`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - ... and 121 more, see the JSON sidecar

Old text:

```
        held[key] = record(remote_id)
        ledger._write(cfg, document)
        return remote_id, True
```

New text:

```
        held[key] = record(remote_id)
        return remote_id, True
```

### `r1031.M12_link_keeps_its_miss`

ledger.record_mirror_links: leave the row's miss in the document when it is linked

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `r1031.json`, row `M12_link_keeps_its_miss`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_linking_a_row_takes_its_miss_out_of_the_document`

Old text:

```
                document["mirror_misses"].pop(str(content_id), None)
```

New text:

```
                pass
```

### `r1031.M13_miss_written_over_a_link`

ledger.record_mirror_misses: write a miss for a row the ledger already links

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `r1031.json`, row `M13_miss_written_over_a_link`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_miss_over_a_linked_row_is_never_written_to_the_document`

Old text:

```
            if str(content_id) in document["mirror_links"]:
                continue
```

New text:

```
            if False:
                continue
```

### `r836-b.L4_pruned_leaves_added`

ledger._moved_to_pruned: a taken track stays in added, so the next prune asks the account for it again

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `r836-b.json`, row `L4_pruned_leaves_added`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 5 (killed)
- Killed:
  - `tests/test_prune.py::test_a_held_release_plans_exactly_its_tracks_and_approved_only_they_leave`
  - `tests/test_prune.py::test_a_refusal_part_way_resumes_without_taking_anything_off_twice`
  - `tests/test_prune.py::test_a_second_run_plans_nothing`
  - `tests/test_prune.py::test_a_track_already_off_the_playlist_is_settled_through_the_removals_own_read`
  - `tests/test_prune.py::test_an_exported_playlist_whose_library_playlist_lost_a_track_plans_exactly_it`

Old text:

```
    entry["added"] = [one for one in _listed(entry, "added") if one not in gone]
```

New text:

```
(empty)
```

### `r836-c.L7_row_only_for_a_written_track`

ledger.record_playlist_row: a row is recorded for a track this product never wrote, which a prune then reads as its own

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `r836-c.json`, row `L7_row_only_for_a_written_track`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_row_is_never_recorded_for_a_track_this_product_did_not_write`

Old text:

```
        if not record or str(remote_id) not in _listed(record, "added"):
            return
        rows = _rows(record)
```

New text:

```
        if not record:
            return
        rows = _rows(record)
```

### `u150.L1_forget_checks_id`

ledger.forget_mirror_playlist: drop the identifier check, so a playlist recorded under the title since is forgotten in its place

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u150.json`, row `L1_forget_checks_id`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_forgetting_a_mirrored_playlist_drops_only_the_record_of_that_identifier`

Old text:

```
        if not entry or str(entry.get("remote_id") or "") != str(remote_id):
            return
```

New text:

```
        if not entry:
            return
```

### `u201-composites.C4_settle_none`

settle_mirror_tracks: the library step settles nothing, the thing L2 narrows

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u201-composites.json`, row `C4_settle_none`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_move_in_rekordbox_after_an_edit_was_taken_is_rekordboxs`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_removed_on_the_account_and_added_nowhere_is_unfiled_and_listed`
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
    wanted = list(settled)
```

New text:

```
    wanted = []
```

### `u201.L1_agreed_own_playlist`

record_mirror_agreed: a snapshot lands on a playlist recorded under the title with another identifier

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u201.json`, row `L1_agreed_own_playlist`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`

Old text:

```
            if not entry or str(entry.get("remote_id") or "") != str(remote_id):
                continue
            base =
```

New text:

```
            if not entry:
                continue
            base =
```

### `u236.M17_ledger_settle_keeps_placement`

ledger settle: a settled track keeps its placement on that title

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u236.json`, row `M17_ledger_settle_keeps_placement`
- Moved: settle_mirror_tracks moved from ledger.py to ledger_settle.py and the kept placements are now named before the _place call; same check reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits_u236.py`
- Collected: 25 against a baseline of 25
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`

Old text:

```
                if str(track) in before:
                    kept = {one: at for one, at in before.items() if one != str(track)}
                    _place(record, name, kept)
                    wrote = True
```

New text:

```
                if False:
                    kept = {one: at for one, at in before.items() if one != str(track)}
                    _place(record, name, kept)
                    wrote = True
```

### `u236.M18_ledger_placement_not_written`

ledger settle: never write a placement

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u236.json`, row `M18_ledger_placement_not_written`
- Moved: the placement write in settle_mirror_tracks moved from ledger.py into ledger_settle.settle_mirror_tracks, with record and name now on one line; the same _place call is deleted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits_u236.py`
- Collected: 25 against a baseline of 25
- Kills: 8 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_survives_the_ledgers_own_read_and_write`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
            _place(
                record, name,
                {**_placements(record.get("placed")).get(str(name), {}), str(track): str(at)},
            )
            wrote = True

```

New text:

```
            wrote = True

```

### `u236.M20_agreed_never_drops`

record_mirror_agreed: never drop a placement the account now holds

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u236.json`, row `M20_agreed_never_drops`
- Moved: record_mirror_agreed moved from ledger.py into ledger_settle.py and reads the mirrored folder's record once into record, so the same placed_after call is written shorter there and is bypassed the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_hand_addition_after_the_placement_is_dropped_is_read_as_one`
  - `tests/test_organize_mirror_edits_u236.py::test_the_organize_after_the_favourite_puts_it_in_the_accounts_month`

Old text:

```
            _place(record, name, mirror_edits.placed_after(
                _placements(record.get("placed")).get(name, {}), after, held
            ))
```

New text:

```
            _place(record, name, _placements(record.get("placed")).get(name, {}))
```

### `u270.L2_row_only_for_a_recorded_track`

record_playlist_tracks: note a row for a track not recorded as added, claiming a person's track by its row

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u270.json`, row `L2_row_only_for_a_recorded_track`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 257 against a baseline of 257
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_the_ledger_never_notes_a_row_for_a_track_it_does_not_hold_as_added`

Old text:

```
            if str(track) in added:
                known[str(row)] = str(track)
```

New text:

```
            if True:
                known[str(row)] = str(track)
```

### `r1031.M2_rematch_ignored`

Matcher: keep the remembered misses under rematch, so --rematch asks nothing

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1031.json`, row `M2_rematch_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_row_matched_later_loses_its_miss`
  - `tests/test_organize_mirror_frozen.py::test_rematch_asks_every_remembered_miss_again`

Old text:

```
        self._misses = {} if rematch else dict(misses or {})
```

New text:

```
        self._misses = dict(misses or {})
```

### `r1031.M3_signature_keys_a_coded_row`

Matcher.under: key every miss on its file signature, so a coded row is asked again on any file touch

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1031.json`, row `M3_signature_keys_a_coded_row`
- Moved: Matcher.under in mirror.py now returns its key tuple on one line instead of one field a line; same signature made to key a coded row
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_coded_rows_miss_is_kept_whatever_its_file_does`

Old text:

```
"" if row.isrc else self._signature(row))
```

New text:

```
self._signature(row))
```

### `r1031.M4_signature_dropped`

Matcher.under: drop the file signature, so a file that gains a code is never asked again

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1031.json`, row `M4_signature_dropped`
- Moved: Matcher.under in mirror.py now returns its tuple on one line instead of one element per line; the same signature element is replaced by an empty string
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_file_that_gains_a_code_is_asked_again_and_an_unchanged_one_is_not`

Old text:

```
        return (row.isrc, row.title, row.artist, row.path, "" if row.isrc else self._signature(row))

```

New text:

```
        return (row.isrc, row.title, row.artist, row.path, "")

```

### `r1031.M5_unread_miss_remembered`

Matcher._missed: remember a miss over a candidate that could not be read

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1031.json`, row `M5_unread_miss_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_miss_over_a_candidate_that_could_not_be_read_is_never_remembered`
  - `tests/test_organize_mirror_frozen.py::test_the_frozen_matches_answer_a_row_the_ledger_could_not_remember`

Old text:

```
        if UNREAD not in reason:
```

New text:

```
        if True:
```

### `r1031.M6_misses_never_gathered`

Matcher._missed: gather no miss, so nothing is remembered

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1031.json`, row `M6_misses_never_gathered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_coded_rows_miss_is_kept_whatever_its_file_does`
  - `tests/test_organize_mirror_frozen.py::test_a_file_that_gains_a_code_is_asked_again_and_an_unchanged_one_is_not`
  - `tests/test_organize_mirror_frozen.py::test_a_miss_is_recorded_by_the_run_that_shows_the_gate_with_nothing_applied`
  - `tests/test_organize_mirror_frozen.py::test_a_miss_over_a_candidate_that_could_not_be_read_is_never_remembered`
  - `tests/test_organize_mirror_frozen.py::test_a_refresh_asks_only_the_rows_new_since_the_last_and_names_the_rest_remembered`
  - `tests/test_organize_mirror_frozen.py::test_a_row_matched_later_loses_its_miss`

Old text:

```
            self.missed[row.content_id] = (reason, under)
```

New text:

```
            pass
```

### `r1031.M7_remembered_not_counted`

Matcher._match: count no remembered miss, so the gate never says misses were reused

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1031.json`, row `M7_remembered_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_refresh_asks_only_the_rows_new_since_the_last_and_names_the_rest_remembered`

Old text:

```
            self.remembered += 1
```

New text:

```
            self.remembered += 0
```

### `r1032.M1_mirror_never_asks_any_agreeing`

Matcher._match: ask the provider without any_agreeing, so the mirror refuses a tie as a heart does

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1032.json`, row `M1_mirror_never_asks_any_agreeing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_tie.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 108 against a baseline of 108
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_release_that_does_not_agree_is_never_the_one_taken`
  - `tests/test_organize_mirror_tie.py::test_a_tie_between_agreeing_releases_is_mirrored_as_one_and_recorded`
  - `tests/test_organize_mirror_tie.py::test_a_tie_remembered_as_a_miss_before_the_tie_was_broken_is_asked_again`
  - `tests/test_organize_mirror_tie.py::test_the_next_refresh_keeps_the_chosen_release_and_asks_the_provider_nothing`

Old text:

```
            any_agreeing=True,
```

New text:

```
            any_agreeing=False,
```

### `u147-a.M1_two_root_folders`

mirror.plan: drop the refusal of two root folders of the mirror's name, so the first is adopted

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-a.json`, row `M1_two_root_folders`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_two_root_folders_of_the_name_refuse_that_genre_and_the_rest_proceeds`

Old text:

```
        if len(named) > 1:
            raise ambiguous(folder.name, named)

```

New text:

```
(empty)
```

### `u147-a.M5_persons_playlist`

mirror.plan: never leave a person's playlist of the same title, make one beside it

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-a.json`, row `M5_persons_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_persons_playlist_left_alone_costs_no_match`
  - `tests/test_organize_mirror.py::test_a_persons_playlist_of_the_same_title_is_left_and_nothing_made_beside_it`

Old text:

```
        theirs = sorted(pid for pid, name in inside.items() if name == source.name)
        if theirs:
```

New text:

```
        theirs = sorted(pid for pid, name in inside.items() if name == source.name)
        if False:
```

### `u147-b.M11_agree_dropped`

Matcher: never ask the one track to agree, a file's code included (R-879)

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-b.json`, row `M11_agree_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_code_read_off_the_file_asks_the_one_track_to_agree_and_a_database_code_does_not`

Old text:

```
            agree=said.agree,
```

New text:

```
            agree=False,
```

### `u147-b.M13_links_unrecorded`

mirror.apply: record no link, so every refresh matches every row again

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-b.json`, row `M13_links_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_second_run_plans_nothing_writes_nothing_and_asks_no_match_again`
  - `tests/test_organize_mirror.py::test_a_write_elsewhere_in_the_ledger_carries_the_mirror_record_through`
  - `tests/test_organize_mirror.py::test_rows_a_folder_with_nothing_to_write_matched_are_linked_by_another_folders_apply`
  - `tests/test_organize_mirror.py::test_the_plan_screens_every_code_its_rows_will_ask_before_asking_any`

Old text:

```
    ledger.record_mirror_links(cfg, planned.links if links is None else links)
```

New text:

```
    pass
```

### `u147-b.M2_stale_folder_again`

Batch a's zero, measured again after its test: reuse a recorded folder whether or not the root still lists it

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-b.json`, row `M2_stale_folder_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_recorded_folder_deleted_on_the_account_is_made_again_rather_than_reused`

Old text:

```
    if held_id and held_id in root:
```

New text:

```
    if held_id:
```

### `u147-b.M8_move_new_only`

mirror.apply: move only a playlist made now, never one made earlier and left at the root

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-b.json`, row `M8_move_new_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run`

Old text:

```
        if made or step.move:
```

New text:

```
        if made:
```

### `u147-b.M9_link_reused_blind`

Matcher: reuse a link even when the row's database code changed

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-b.json`, row `M9_link_reused_blind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_row_whose_database_code_changed_is_matched_again`

Old text:

```
        if linked is not None and (not row.isrc or row.isrc == linked[1]):
```

New text:

```
        if linked is not None:
```

### `u150.M10_link_before_known`

Matcher: take the landing track before the ledger's link, so a linked row is switched to another track

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M10_link_before_known`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_live_batch_made_by_a_label_landing_plans_its_playlist_with_the_batchs_tracks`
  - `tests/test_organize_mirror_inbox.py::test_a_row_the_ledger_already_links_keeps_its_link_over_a_landing_track`

Old text:

```
        linked = self._links.get(row.content_id)
        if linked is not None and (not row.isrc or row.isrc == linked[1]):
```

New text:

```
        linked = self._links.get(row.content_id)
        if row.content_id in self._known:
            return self._known[row.content_id], row.isrc, ""
        if linked is not None and (not row.isrc or row.isrc == linked[1]):
```

### `u150.M11_unmade_folder`

mirror.plan: make the retiring folder even when nothing goes in it, so an empty INBOX root folder is created

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M11_unmade_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_deleted_inbox_folder_with_only_removals_left_is_not_made_again`
  - `tests/test_organize_mirror_inbox.py::test_an_inbox_with_no_live_batch_makes_no_empty_folder`

Old text:

```
    if folder_action == CREATE and folder.retire and not folder.playlists:
        folder_action = UNMADE
```

New text:

```
    if False:
        folder_action = UNMADE
```

### `u150.M1_retire_flag`

mirror.plan: drop the retiring folder's flag, so a playlist whose batch left INBOX is left on the account instead of removed

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M1_retire_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 7 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_batch_still_under_inbox_that_no_longer_reads_as_one_is_left_not_removed`
  - `tests/test_organize_mirror_inbox.py::test_a_batch_the_rotation_moved_into_old_plans_the_removal_of_its_playlist_and_nothing_else`
  - `tests/test_organize_mirror_inbox.py::test_a_deleted_inbox_folder_with_only_removals_left_is_not_made_again`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_already_gone_from_the_account_is_still_forgotten`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_for_any_other_reason_is_raised`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_with_nothing_sent_is_kept_named_and_planned_again`
  - `tests/test_organize_mirror_inbox.py::test_the_digest_covers_the_removal`

Old text:

```
        if not folder.retire:
            left.append(
```

New text:

```
        if True:
            left.append(
```

### `u150.M2_present_guard`

mirror.plan: drop the still present test, so a batch still under INBOX that only no longer reads as one is removed from the account

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M2_present_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_batch_still_under_inbox_that_no_longer_reads_as_one_is_left_not_removed`
  - `tests/test_organize_mirror_inbox.py::test_the_digest_covers_the_removal`

Old text:

```
        elif name in folder.present:
```

New text:

```
        elif False:
```

### `u150.M3_retire_in_writes`

FolderPlan.writes: leave the retirements out, so a folder whose only write is a removal plans nothing and never removes

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M3_retire_in_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_batch_the_rotation_moved_into_old_plans_the_removal_of_its_playlist_and_nothing_else`
  - `tests/test_organize_mirror_inbox.py::test_a_deleted_inbox_folder_with_only_removals_left_is_not_made_again`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_already_gone_from_the_account_is_still_forgotten`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_for_any_other_reason_is_raised`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_with_nothing_sent_is_kept_named_and_planned_again`

Old text:

```
            or bool(self.retire)
        )
```

New text:

```
            or False
        )
```

### `u150.M4_retire_in_digest`

FolderPlan.identity: leave the retirements out of the digest, so an approval given for one removal covers another

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M4_retire_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_the_digest_covers_the_removal`

Old text:

```
            "retire": [list(one) for one in self.retire],
```

New text:

```
            "retire": [],
```

### `u150.M5_apply_removes`

mirror.apply: skip the playlist removal, so the gate names a removal the apply never performs

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M5_apply_removes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_batch_the_rotation_moved_into_old_plans_the_removal_of_its_playlist_and_nothing_else`
  - `tests/test_organize_mirror_inbox.py::test_a_deleted_inbox_folder_with_only_removals_left_is_not_made_again`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_for_any_other_reason_is_raised`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_with_nothing_sent_is_kept_named_and_planned_again`

Old text:

```
            account.remove_playlist(remote_id)
        except CratekitError as exc:
```

New text:

```
            pass
        except CratekitError as exc:
```

### `u150.M6_apply_forgets`

mirror.apply: keep the ledger record of a removed playlist, so every later refresh plans the removal again

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M6_apply_forgets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_batch_the_rotation_moved_into_old_plans_the_removal_of_its_playlist_and_nothing_else`
  - `tests/test_organize_mirror_inbox.py::test_a_deleted_inbox_folder_with_only_removals_left_is_not_made_again`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_already_gone_from_the_account_is_still_forgotten`

Old text:

```
        ledger.forget_mirror_playlist(cfg, planned.name, name, remote_id)
        done.retired.append(name)
```

New text:

```
        done.retired.append(name)
```

### `u150.M7_refusal_scope`

mirror.apply: keep a playlist removal refused at run scope instead of raising, so a removal whose read back differs reads as kept

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M7_refusal_scope`
- Moved: the playlist removal refusal in mirror.apply now goes through the helper _kept, shared with the track removals, instead of its own inline check; same scope test dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_removal_whose_read_back_differs_is_raised_never_kept`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_for_any_other_reason_is_raised`

Old text:

```
    if exc.cause.reason != "outbound-remove-refused" or exc.cause.scope != Scope.SOURCE:

```

New text:

```
    if exc.cause.reason != "outbound-remove-refused":

```

### `u150.M8_refusal_kept`

mirror.apply: raise a playlist removal refused with nothing sent, so one unvouched playlist stops the folder's apply

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M8_refusal_kept`
- Moved: the retire loop in mirror.apply now keeps a refused removal through the _kept helper it shares with the track removals, which raises any other refusal itself; the same keep and continue at the retire call site are replaced by a raise
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_with_nothing_sent_is_kept_named_and_planned_again`

Old text:

```
            _kept(exc, name, done)
            continue
        ledger.forget_mirror_playlist
```

New text:

```
            raise
        ledger.forget_mirror_playlist
```

### `u150.M9_known_answers`

Matcher: ignore a row's recorded landing track, so a label batch is matched by ISRC and misses on a tie

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M9_known_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_live_batch_made_by_a_label_landing_plans_its_playlist_with_the_batchs_tracks`

Old text:

```
        own = self._known.get(row.content_id)
        if own:
```

New text:

```
        own = self._known.get(row.content_id)
        if False:
```

### `u201.M1_plan_keeps`

mirror.plan: removes an account track the hold keeps

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u201.json`, row `M1_plan_keeps`
- Moved: the reused playlist's plan left the body of mirror.plan for the helper mirror._reused, so the same line sits eight spaces shallower; same hold.keep test dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_short_listing_changes_nothing_in_the_library_and_undoes_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_to_its_own_genres_with_vox_is_held_and_nothing_is_written`
  - `tests/test_organize_mirror_edits.py::test_a_track_the_library_lacks_added_on_the_account_is_held_there`
  - `tests/test_organize_mirror_edits.py::test_a_track_whose_file_is_gone_is_named_and_nothing_of_it_is_written`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
    remove = tuple(one for one in names if one not in keep and one not in hold.keep)
```

New text:

```
    remove = tuple(one for one in names if one not in keep)
```

### `u201.M2_plan_skips`

mirror.plan: adds back a track the hold skips

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u201.json`, row `M2_plan_skips`
- Moved: the reused playlist's plan left the body of mirror.plan for the helper mirror._reused, where the comprehension is folded onto one line; same hold.skip test dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_short_listing_changes_nothing_in_the_library_and_undoes_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_to_its_own_genres_with_vox_is_held_and_nothing_is_written`
  - `tests/test_organize_mirror_edits.py::test_a_track_removed_on_the_account_and_added_nowhere_is_unfiled_and_listed`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
            one for one in wanted if one not in on and one not in mine.refused and one not in hold.skip
```

New text:

```
            one for one in wanted if one not in on and one not in mine.refused
```

### `u207.M1_mirror_screens_settled_rows`

mirror: the matcher screens every row with a code, a link, a recorded track and a remembered miss included

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u207.json`, row `M1_mirror_screens_settled_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_tie.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_the_mirror_screens_only_the_rows_it_would_ask_the_provider_about`
  - `tests/test_organize_mirror.py::test_the_plan_screens_every_code_its_rows_will_ask_before_asking_any`

Old text:

```
            if self._settled(row) is None and (said := self._identity(row)).isrc
```

New text:

```
            if (said := self._identity(row)).isrc
```

### `u207.M2_mirror_counts_a_screen_as_one`

mirror: Counted counts a screen as one request whatever it spent

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u207.json`, row `M2_mirror_counts_a_screen_as_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_tie.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_the_mirrors_request_count_holds_what_the_screen_spent_and_no_more`
  - `tests/test_organize_mirror.py::test_soul_with_six_playlists_and_no_mirror_plans_one_folder_and_six_playlists`

Old text:

```
            if name in SCREENS:
```

New text:

```
            if False:
```

### `u309.U12_mirror_kept_source_only`

The mirror keeps and names a removal refused at any scope, not only one refused with nothing sent

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u309.json`, row `U12_mirror_kept_source_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_removal_whose_read_back_differs_is_raised_never_kept`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_for_any_other_reason_is_raised`

Old text:

```
    if exc.cause.reason != "outbound-remove-refused" or exc.cause.scope != Scope.SOURCE:
```

New text:

```
    if exc.cause.reason != "outbound-remove-refused":
```

### `u201-composites.C1_two_bands_composite`

E2 with the guard after it: neither the two bands guard nor the still in two bands guard, so a track added to two bands at once is moved to one

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201-composites.json`, row `C1_two_bands_composite`
- Moved: both guards stay in mirror_edits._intent, whose held answers are now written as one tuple and name places through _named, so the text around the two conditions differs; both conditions reverted as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_track_added_to_two_bands_at_once_is_held_on_both_sides`

Old text:

```
    if len(added) > 1:
        return HELD, None, (
            f"added on the account to {len(added)} band playlists at once "
            f"({_named(added)}), so which one it belongs in is not something the account says"
        )
    if removed and len(now) == 1:
        (place,) = now
        return MOVE, place, f"taken off {_named(removed)} on the account, left in {place.title}"
    if removed and len(now) > 1:
        return HELD, None, (
```

New text:

```
    if False:
        return HELD, None, (
            f"added on the account to {len(added)} band playlists at once "
            f"({_named(added)}), so which one it belongs in is not something the account says"
        )
    if removed and len(now) == 1:
        (place,) = now
        return MOVE, place, f"taken off {_named(removed)} on the account, left in {place.title}"
    if False:
        return HELD, None, (
```

### `u201-composites.C2_agrees_never`

_agrees: a MOVE never agrees with rekordbox, the thing E5's exactness narrows

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201-composites.json`, row `C2_agrees_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_both_sides_moving_a_track_to_one_place_agree`

Old text:

```
        return now == frozenset({to})
```

New text:

```
        return False
```

### `u201.E10_unknown_time`

_later: a time unknown lets the account's move win

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E10_unknown_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[-2026-11-04 10:00:00.000 +00:00]`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[2026-11-04T12:00:00+00:00-]`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[2026-11-04T12:00:00-2026-11-04 10:00:00.000 +00:00]`
  - `tests/test_organize_mirror_edits.py::test_two_moves_with_the_account_time_unknown_keep_rekordboxs`

Old text:

```
    if account_at is None or rekordbox_at is None:
```

New text:

```
    if False:
```

### `u201.E11_later_strict`

_later: equal times let the account's move win

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E11_later_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_two_moves_at_one_moment_keep_rekordboxs`

Old text:

```
    if account_at > rekordbox_at:
```

New text:

```
    if account_at >= rekordbox_at:
```

### `u201.E13_snapshot_word`

agreed_after: a held track takes the account's word rather than the snapshot's

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E13_snapshot_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_the_snapshot_after_keeps_its_word_on_a_held_track`
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`

Old text:

```
    before = now if base is None else frozenset(base)
```

New text:

```
    before = now
```

### `u201.E1_never_agreed_base`

Mirrored.base: a playlist never agreed reads an empty snapshot, so every account track reads as an edit on the first run

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E1_never_agreed_base`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_playlist_never_agreed_reads_every_difference_as_rekordboxs`

Old text:

```
        return self.account if self.agreed is None else self.agreed
```

New text:

```
        return frozenset() if self.agreed is None else self.agreed
```

### `u201.E3_own_genre_derived_held`

_intent: a track taken off its band and left in its own genre's with vox is decided as a genre change

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E3_own_genre_derived_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_track_taken_off_its_band_and_put_in_its_own_genres_with_vox_is_held`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_to_its_own_genres_with_vox_is_held_and_nothing_is_written`

Old text:

```
    if removed and not now and folders[0] in {place.folder for place in removed}:
```

New text:

```
    if False:
```

### `u201.E4_own_genre_no_edit`

_intent: a track added to its own genre's with vox while keeping its band reads as an edit

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E4_own_genre_no_edit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_track_added_to_its_own_genres_with_vox_is_no_edit`

Old text:

```
    if not removed and folders[0] in {place.folder for place in now}:
```

New text:

```
    if False:
```

### `u201.E6_short_unread`

decide: a short listing marks nothing unread, so a counted, unlisted track reads as taken off

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E6_short_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_short_favorites_listing_holds_what_it_left_out`
  - `tests/test_mirror_edits.py::test_a_short_listing_carries_no_edit_and_holds_what_it_read_differently`
  - `tests/test_organize_mirror_edits.py::test_a_short_listing_changes_nothing_in_the_library_and_undoes_nothing`

Old text:

```
            unread |= one.agreed - one.account
```

New text:

```
            unread |= set()
```

### `u201.E7_addition_beats_removal`

decide: an unfile on the account against rekordbox placing the track is carried, the removal beating the addition

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E7_addition_beats_removal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_an_unfile_on_the_account_against_a_move_in_rekordbox_keeps_rekordboxs`

Old text:

```
            if kind == UNFILE:
```

New text:

```
            if False:
```

### `u204.P10_inbox_agreed`

_decide_inbox: a change both sides made to a batch is carried again rather than agreed

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P10_inbox_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_an_inbox_change_both_sides_made_is_agreed`

Old text:

```
            if (track in one.rekordbox) is added:
```

New text:

```
            if False:
```

### `u204.P11_inbox_hold_per_batch`

_holds: an INBOX edit holds every batch rather than its own

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P11_inbox_hold_per_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_an_inbox_edit_holds_its_own_batch_and_no_other`
  - `tests/test_mirror_edits.py::test_an_inbox_track_put_in_joins_and_one_taken_off_leaves`
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_an_inbox_batch_joins_it_and_one_taken_off_leaves_it`
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_inbox_or_favorites_that_the_library_lacks_is_queued`

Old text:

```
            key = one.to.title if one.tree == INBOX and one.to is not None else one.tree
```

New text:

```
            key = one.tree
```

### `u204.P12_favorites_stay`

_holds: a Favorites edit keeps no snapshot word on a playlist the plan finds level

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P12_favorites_stay`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_favorites_edit_planned_and_not_applied_is_taken_whole_by_the_next_run`

Old text:

```
        stay = frozenset(mine) if one.place.tree == FAVORITES else frozenset()
```

New text:

```
        stay = frozenset()
```

### `u204.P2_acquire_only_unknown`

_carry: an addition the library lacks is queued whatever the snapshots held

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P2_acquire_only_unknown`
- Moved: _carry's two held Decisions were folded into one whose acquire flag is computed first, so the same condition now assigns acquire instead of opening an if, and is reverted the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_an_addition_the_library_lacks_is_queued_in_favorites_and_inbox_and_a_known_one_never`
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_a_snapshot_once_held_is_never_queued_again`

Old text:

```
        acquire = kind in ADDITIONS and track not in known
```

New text:

```
        acquire = kind in ADDITIONS
```

### `u204.P3_off_and_into_month_held`

_decide_favorites: a track taken off All Favorites and put in a month at once is unfavourited rather than held

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P3_off_and_into_month_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_favorites_edit_the_account_does_not_decide_is_held[af2-oct_2-nov2-at once]`

Old text:

```
        if removed_s and added_m:
```

New text:

```
        if False:
```

### `u204.P4_two_months_held`

_decide_favorites: a track added to two months at once is favourited into one of them rather than held

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P4_two_months_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_favorites_edit_the_account_does_not_decide_is_held[af1-oct_1-nov1-2 month playlists]`

Old text:

```
        elif len(added_m) > 1:
```

New text:

```
        elif False:
```

### `u204.P6_filed_no_month`

_decide_favorites: a track put in All Favorites that sits in a month is given a second month by its time

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P6_filed_no_month`
- Moved: the extra carried for a track put in All Favorites in _decide_favorites was folded from a multi line dict onto one line with its when read into a local first; the same filed flag is forced False
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_track_put_in_all_favorites_that_sits_in_a_month_takes_no_month`

Old text:

```
            extra = {"when": next(when, ""), "filed": bool(now_m or there_m)}

```

New text:

```
            extra = {"when": next(when, ""), "filed": False}

```

### `u204.P9_unfavourite_settles_out`

_decide_favorites: the settle after an unfavourite reads rekordbox as still holding the track

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P9_unfavourite_settles_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_track_taken_off_all_favorites_is_unfavourited_and_settled_out_of_the_folder`

Old text:

```
            if kind == UNFAVOURITE or one.place in extra.get("away", ()):
```

New text:

```
            if one.place in extra.get("away", ()):
```

### `u227.R3_all_to_any`

_landed_there: one band the landing filed is enough, so a second band a person added loses

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u227.json`, row `R3_all_to_any`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 187 against a baseline of 187
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits_u227.py::test_a_second_band_added_in_rekordbox_after_the_landing_stands`
  - `tests/test_organize_mirror_edits_u227.py::test_a_refiling_through_adoption_after_the_landing_is_not_the_landings`

Old text:

```
    return bool(there) and all((place.folder, place.playlist) in places for place in there)
```

New text:

```
    return bool(there) and any((place.folder, place.playlist) in places for place in there)
```

### `u227.R4_folder_compare`

_landed_there: compare the playlist alone, so another genre's band of the same name reads as the landing's

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u227.json`, row `R4_folder_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits_u227.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u227.py::test_another_genres_band_of_the_landings_name_is_not_the_landings`

Old text:

```
    return bool(there) and all((place.folder, place.playlist) in places for place in there)
```

New text:

```
    return bool(there) and all(any(place.playlist == one[1] for one in places) for place in there)
```

### `u227.R5_landed_flag`

decide genre: carry the landed edit without its landed flag on the plan

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u227.json`, row `R5_landed_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 187 against a baseline of 187
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits_u227.py::test_a_folder_edit_for_a_landed_track_takes_the_folder_over_the_landings_band`
  - `tests/test_mirror_edits_u227.py::test_a_landings_own_filing_does_not_beat_the_edit_that_queued_it`

Old text:

```
                extra = {"landed": True}
```

New text:

```
                extra = {}
```

### `u227.R6_landed_item`

Decision.item: drop the landed flag from what the gate shows

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u227.json`, row `R6_landed_item`
- Moved: Decision.item now shows its optional keys from one table of pairs kept when true, so the landed flag is its own entry there rather than an if; same flag left off what the gate shows
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u227.py::test_a_landings_own_filing_does_not_beat_the_edit_that_queued_it`

Old text:

```
            ("landed", self.landed),

```

New text:

```
(empty)
```

### `u230.K2_u227_known_guard`

_landed_there (U227, sample): a track a snapshot held is still read as landed

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `K2_u227_known_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 5 (killed)
- Killed:
  - `tests/test_mirror_edits_u227.py::test_a_hand_move_back_into_the_landings_band_after_the_edit_was_carried_stands`
  - `tests/test_mirror_edits_u230.py::test_a_later_account_move_then_a_rekordbox_move_back_into_the_landings_band_stands`
  - `tests/test_mirror_edits_u230.py::test_another_playlist_the_account_still_lists_it_on_counts_too`
  - `tests/test_mirror_edits_u230.py::test_another_playlists_snapshot_holding_the_track_is_never_read_as_landed`
  - `tests/test_organize_mirror_edits_u230.py::test_another_playlists_snapshot_holding_the_track_keeps_rekordboxs_place`

Old text:

```
    if not places or held:
```

New text:

```
    if not places:
```

### `u230.M11_empty_there`

_filed_by_landing: a track rekordbox holds in no band reads as the landing's filing

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M11_empty_there`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_row_taken_out_of_the_tree_in_rekordbox_is_not_lifted_over`

Old text:

```
    return bool(there) and all((place.folder, place.playlist) in places for place in there)
```

New text:

```
    return all((place.folder, place.playlist) in places for place in there)
```

### `u230.M12_queue_not_handed`

decide: hand the genre rule no queue

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M12_queue_not_handed`
- Moved: decide now builds its decisions in one list, so the _decide_genre call in mirror_edits.py sits four spaces shallower; same queue emptied
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 6 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_folder_edit_on_a_never_agreed_derived_playlist_is_carried_too`
  - `tests/test_mirror_edits_u230.py::test_a_never_agreed_playlist_whose_account_side_holds_the_track_carries_it`
  - `tests/test_mirror_edits_u230.py::test_another_playlist_the_account_still_lists_it_on_counts_too`
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_move_in_rekordbox_after_the_carry_still_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it`

Old text:

```
            queued=by_queue,
```

New text:

```
            queued={},
```

### `u230.M13_held_by_dropped`

decide: hand the genre rule no per playlist holders, so the lift never reaches the landed check

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M13_held_by_dropped`
- Moved: decide now builds its decisions in one list, so the _decide_genre call in mirror_edits.py sits four spaces shallower; same holders argument dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 29 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_two_moves_at_one_moment_keep_rekordboxs`
  - `tests/test_mirror_edits.py::test_two_moves_follow_the_account_when_its_is_the_later`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[-2026-11-04 10:00:00.000 +00:00]`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[2026-11-04T12:00:00+00:00-]`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[2026-11-04T12:00:00-2026-11-04 10:00:00.000 +00:00]`
  - `tests/test_mirror_edits_u227.py::test_a_folder_edit_for_a_landed_track_takes_the_folder_over_the_landings_band`
  - `tests/test_mirror_edits_u227.py::test_a_hand_move_back_into_the_landings_band_after_the_edit_was_carried_stands`
  - `tests/test_mirror_edits_u227.py::test_a_landings_own_filing_does_not_beat_the_edit_that_queued_it`
  - `tests/test_mirror_edits_u227.py::test_a_move_made_in_rekordbox_after_the_landing_stands`
  - `tests/test_mirror_edits_u227.py::test_a_second_band_added_in_rekordbox_after_the_landing_stands`
  - `tests/test_mirror_edits_u227.py::test_another_genres_band_of_the_landings_name_is_not_the_landings`
  - `tests/test_mirror_edits_u230.py::test_a_folder_edit_on_a_never_agreed_derived_playlist_is_carried_too`
  - `tests/test_mirror_edits_u230.py::test_a_later_account_move_then_a_rekordbox_move_back_into_the_landings_band_stands`
  - `tests/test_mirror_edits_u230.py::test_a_never_agreed_playlist_whose_account_side_holds_the_track_carries_it`
  - `tests/test_mirror_edits_u230.py::test_another_playlist_the_account_still_lists_it_on_counts_too`
  - ... and 14 more, see the JSON sidecar

Old text:

```
            held_by={track: frozenset(titles) for track, titles in held_by.items()},
```

New text:

```
            held_by=None,
```

### `u230.M14_no_titles_guard`

_as_queued: a track with landing places and no queue is lifted on every playlist

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M14_no_titles_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 6 (killed)
- Killed:
  - `tests/test_mirror_edits_u227.py::test_a_folder_edit_for_a_landed_track_takes_the_folder_over_the_landings_band`
  - `tests/test_mirror_edits_u227.py::test_a_hand_move_back_into_the_landings_band_after_the_edit_was_carried_stands`
  - `tests/test_mirror_edits_u227.py::test_a_landing_filed_into_the_place_the_account_asked_agrees`
  - `tests/test_mirror_edits_u227.py::test_a_landings_own_filing_does_not_beat_the_edit_that_queued_it`
  - `tests/test_mirror_edits_u227.py::test_a_track_a_snapshot_held_is_read_by_the_later_change_rule_alone`
  - `tests/test_mirror_edits_u230.py::test_the_same_reading_without_the_queue_is_no_edit_at_all_as_before`

Old text:

```
    if not titles or not places:
```

New text:

```
    if not places:
        titles = frozenset(one.place.title for one in playlists)
    if not places:
```

### `u230.M1_no_lift`

decide genre: never lift the queuing playlist's base, so sitting 86's shape reads no edit

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M1_no_lift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 6 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_folder_edit_on_a_never_agreed_derived_playlist_is_carried_too`
  - `tests/test_mirror_edits_u230.py::test_a_never_agreed_playlist_whose_account_side_holds_the_track_carries_it`
  - `tests/test_mirror_edits_u230.py::test_another_playlist_the_account_still_lists_it_on_counts_too`
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_move_in_rekordbox_after_the_carry_still_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it`

Old text:

```
        lifted = _as_queued(track, playlists, filed, queued)
```

New text:

```
        lifted = frozenset()
```

### `u230.M22_agreed_lifted`

_as_queued: lift an agreed snapshot too, so a drag back after the carry is carried back (round one's BLOCKING)

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M22_agreed_lifted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_an_agreed_snapshot_that_holds_the_track_is_the_librarys_word`
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_an_agreed_snapshot_holding_the_track_is_the_librarys_word`

Old text:

```
        and one.agreed is None

```

New text:

```
        and True

```

### `u230.M23_short_lifted`

_as_queued: lift a short listing, so an edit is read off an account side nobody read (round one's row 3)

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M23_short_lifted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_short_listing_of_the_queuing_playlist_lifts_nothing`

Old text:

```
        and not one.short

```

New text:

```
        and True

```

### `u230.M2_lift_not_in_was`

placed: the lift is ignored in the base places, so the account side still reads as no change

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M2_lift_not_in_was`
- Moved: decide's inner placed closure became the module function mirror_edits._placed, which takes lifted as an argument, so the same condition sits four spaces shallower and is reverted the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 6 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_folder_edit_on_a_never_agreed_derived_playlist_is_carried_too`
  - `tests/test_mirror_edits_u230.py::test_a_never_agreed_playlist_whose_account_side_holds_the_track_carries_it`
  - `tests/test_mirror_edits_u230.py::test_another_playlist_the_account_still_lists_it_on_counts_too`
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_move_in_rekordbox_after_the_carry_still_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it`

Old text:

```
        and not (side == "base" and one.place.title in lifted)
    )
```

New text:

```
        and True
    )
```

### `u230.M3_lift_not_in_held`

landed check: the lifted playlist's base still counts as a snapshot holding the track

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M3_lift_not_in_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 5 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_folder_edit_on_a_never_agreed_derived_playlist_is_carried_too`
  - `tests/test_mirror_edits_u230.py::test_a_never_agreed_playlist_whose_account_side_holds_the_track_carries_it`
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_move_in_rekordbox_after_the_carry_still_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it`

Old text:

```
bool(held_by.get(track, frozenset()) - lifted)
```

New text:

```
bool(held_by.get(track, frozenset()))
```

### `u230.M4_other_bases_ignored`

landed check: no snapshot counts, so another playlist's word on the row is lost

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M4_other_bases_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 5 (killed)
- Killed:
  - `tests/test_mirror_edits_u227.py::test_a_hand_move_back_into_the_landings_band_after_the_edit_was_carried_stands`
  - `tests/test_mirror_edits_u230.py::test_a_later_account_move_then_a_rekordbox_move_back_into_the_landings_band_stands`
  - `tests/test_mirror_edits_u230.py::test_another_playlist_the_account_still_lists_it_on_counts_too`
  - `tests/test_mirror_edits_u230.py::test_another_playlists_snapshot_holding_the_track_is_never_read_as_landed`
  - `tests/test_organize_mirror_edits_u230.py::test_another_playlists_snapshot_holding_the_track_keeps_rekordboxs_place`

Old text:

```
bool(held_by.get(track, frozenset()) - lifted)
```

New text:

```
False
```

### `u230.M5_any_title`

_as_queued: lift every playlist holding the track, not only the queuing one

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M5_any_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u230.py::test_a_job_queued_from_another_playlist_does_not_lift_the_edited_ones_base`

Old text:

```
        if one.place.title in titles

```

New text:

```
        if True

```

### `u230.M6_no_landing_guard`

_as_queued: lift whatever rekordbox holds, so a band a person chose after the landing is beaten

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M6_no_landing_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_band_a_person_chose_before_any_carry_is_not_lifted_over`
  - `tests/test_mirror_edits_u230.py::test_a_row_taken_out_of_the_tree_in_rekordbox_is_not_lifted_over`

Old text:

```
    if not _filed_by_landing(there, places):
        return frozenset()
```

New text:

```
    if False:
        return frozenset()
```

### `u230.M8_rekordbox_dropped`

_as_queued: lift though rekordbox already holds it where the account put it

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M8_rekordbox_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_landing_filed_where_the_account_asked_is_no_edit`

Old text:

```
        and track not in one.rekordbox

```

New text:

```
        and True

```

### `u236.M1_ours_empty`

decide favorites: read no placement, so the library's own month beats the unfavourite again (sitting 88)

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M1_ours_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 10 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_favourite_both_sides_put_in_another_month_leaves_the_placed_one`
  - `tests/test_mirror_edits_u236.py::test_a_favourite_put_in_another_month_leaves_the_placed_one`
  - `tests/test_mirror_edits_u236.py::test_an_unfavourite_over_the_month_the_library_placed_is_carried`
  - `tests/test_mirror_edits_u236.py::test_the_same_over_a_placed_month_never_agreed`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
        ours = frozenset(
            one.place for one in playlists if not one.place.primary and track in one.placed
        )
```

New text:

```
        ours = frozenset()
```

### `u236.M2_unfavourite_counts_ours`

decide favorites: count a placed month as rekordbox's addition against an UNFAVOURITE

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M2_unfavourite_counts_ours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 7 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_an_unfavourite_over_the_month_the_library_placed_is_carried`
  - `tests/test_mirror_edits_u236.py::test_the_same_over_a_placed_month_never_agreed`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
                if (there_s and not was_s) or (there_m - was_m - ours):
```

New text:

```
                if (there_s and not was_s) or (there_m - was_m):
```

### `u236.M3_moved_counts_ours`

decide favorites: count a placed month as a move of rekordbox's against a FAVOURITE

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M3_moved_counts_ours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_favourite_both_sides_put_in_another_month_leaves_the_placed_one`
  - `tests/test_mirror_edits_u236.py::test_a_favourite_put_in_another_month_leaves_the_placed_one`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`

Old text:

```
                moved = there_m - was_m - ours - {to}
```

New text:

```
                moved = there_m - was_m - {to}
```

### `u236.M4_moved_counts_to`

decide favorites: count the month the account asked for as rekordbox's move (round one, finding 5)

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M4_moved_counts_to`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_favourite_both_sides_put_in_another_month_leaves_the_placed_one`

Old text:

```
                moved = there_m - was_m - ours - {to}
```

New text:

```
                moved = there_m - was_m - ours
```

### `u236.M5_mine_not_left`

decide favorites: a favourite put in another month keeps the placed month

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M5_mine_not_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_favourite_both_sides_put_in_another_month_leaves_the_placed_one`
  - `tests/test_mirror_edits_u236.py::test_a_favourite_put_in_another_month_leaves_the_placed_one`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`

Old text:

```
            mine = ours - now_m
```

New text:

```
            mine = frozenset()
```

### `u236.M6_mine_includes_now`

decide favorites: leave a placed month the account holds too

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M6_mine_includes_now`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_favourite_put_in_the_placed_month_on_the_account_is_agreed`

Old text:

```
            mine = ours - now_m
```

New text:

```
            mine = ours
```

### `u236.M7_placed_after_keeps_all`

placed_after: never drop a placement, so a later hand membership could outlast it

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M7_placed_after_keeps_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_is_dropped_once_the_account_holds_its_track_with_no_hold`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_hand_addition_after_the_placement_is_dropped_is_read_as_one`
  - `tests/test_organize_mirror_edits_u236.py::test_the_organize_after_the_favourite_puts_it_in_the_accounts_month`

Old text:

```
    return {track: at for track, at in placed.items() if track in kept or track not in now}
```

New text:

```
    return dict(placed)
```

### `u236.M8_placed_after_drops_unheld`

placed_after: drop every placement no hold covers, round one's finding 1

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M8_placed_after_drops_unheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_is_dropped_once_the_account_holds_its_track_with_no_hold`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`

Old text:

```
    return {track: at for track, at in placed.items() if track in kept or track not in now}
```

New text:

```
    return {track: at for track, at in placed.items() if track in kept}
```

### `u236.M9_placed_after_ignores_hold`

placed_after: drop a held placement the account holds

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M9_placed_after_ignores_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_is_dropped_once_the_account_holds_its_track_with_no_hold`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`

Old text:

```
    return {track: at for track, at in placed.items() if track in kept or track not in now}
```

New text:

```
    return {track: at for track, at in placed.items() if track not in now}
```

### `r836-d.P1_only_created_years`

prune.plan_label: a year recorded before the created field is pruned as though made here

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `r836-d.json`, row `P1_only_created_years`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_year_recorded_before_the_field_is_said_as_such_not_as_adopted`

Old text:

```
        if recorded.created is not True:
```

New text:

```
        if recorded.created is False:
```

### `r836-e.P2b_mismatch_read_only_with_nothing_gone`

prune.plan_label: a release credited elsewhere is read and judged while a confirmed release is gone, so a track the gone one carries can leave. P2 measured the same guard's second copy in the leaving rule at zero; that copy was removed as redundant and this is the one left

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `r836-e.json`, row `P2b_mismatch_read_only_with_nothing_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_release_the_provider_no_longer_has_stops_the_unconfirmed_judgement`

Old text:

```
    if judged:
        unread += sorted(set(catalogue.mismatched) - set(catalogue.by_release))
```

New text:

```
    unread += sorted(set(catalogue.mismatched) - set(catalogue.by_release))
```

### `r836-e.P5_apply_asks_the_ledger_again`

prune.apply: a plan built in another invocation removes from a playlist the ledger no longer vouches for

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `r836-e.json`, row `P5_apply_asks_the_ledger_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_the_apply_asks_the_ledger_again_and_refuses_a_playlist_it_no_longer_vouches_for`

Old text:

```
        if not ledger.product_made(cfg, step.remote_id):
            raise _not_made(step.remote_id)
```

New text:

```
(empty)
```

### `r836-f.P7_unrowed_with_unmatched_left_alone`

prune.plan_export: a playlist written before rows were kept is pruned by match while a row matched nothing today

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `r836-f.json`, row `P7_unrowed_with_unmatched_left_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_an_unmatched_row_leaves_a_playlist_written_before_rows_alone`

Old text:

```
    elif unrowed and unmatched:
```

New text:

```
    elif False:
```

### `r836-f.P8_drifted_match_left_alone`

prune.plan_export: a row matching a track never written here does not stop the match reading, so a drifted match takes a track off

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `r836-f.json`, row `P8_drifted_match_left_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_match_that_moved_leaves_a_playlist_written_before_rows_alone`

Old text:

```
    elif unrowed and fresh:
```

New text:

```
    elif False:
```

### `r836-f.P9_row_in_playlist_keeps_its_track`

prune.plan_export: a track whose row is still in the playlist leaves when today's match of that row failed

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `r836-f.json`, row `P9_row_in_playlist_keeps_its_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 3 (killed)
- Killed:
  - `tests/test_prune.py::test_a_match_that_moved_never_takes_off_a_track_recorded_by_its_row`
  - `tests/test_prune.py::test_a_row_the_export_names_and_does_not_carry_keeps_its_track`
  - `tests/test_prune.py::test_a_row_whose_match_failed_today_does_not_stop_a_track_recorded_by_its_row`

Old text:

```
    staying = matched_now | {one for row, one in record.rows.items() if row in rows_now}
```

New text:

```
    staying = matched_now
```

### `u243.L10_empties_never_said`

prune._step: a playlist the plan empties is never marked, so the screen does not say so

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `u243.json`, row `L10_empties_never_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_year_playlist_the_prune_empties_is_named_and_kept`

Old text:

```
        empties=bool(take) and set(order) <= {one.remote_id for one in take},
```

New text:

```
        empties=False,
```

### `u243.L9_prune_ignores_tombstones`

prune.plan_label: a tombstoned track leaves only when a held or mismatched release says so

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `u243.json`, row `L9_prune_ignores_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`
- Collected: 78 against a baseline of 78
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_removed_single_is_taken_off_though_its_release_is_suppressed`
  - `tests/test_label_tombstoned.py::test_a_removed_track_stays_off_after_a_full_build`
  - `tests/test_label_tombstoned.py::test_a_tombstone_matches_the_version_and_every_billed_artist`
  - `tests/test_label_tombstoned.py::test_a_tombstoned_track_on_a_year_playlist_is_pruned`
  - `tests/test_label_tombstoned.py::test_a_year_playlist_the_prune_empties_is_named_and_kept`
  - `tests/test_label_tombstoned.py::test_hearing_a_dated_playlist_never_puts_a_removed_track_back`

Old text:

```
            if one in taken_away
            or (one not in staying(year) and (one in on_held or one in on_other))
```

New text:

```
            if (one not in staying(year) and (one in on_held or one in on_other))
```

### `u201.S1_short_undeclared`

PlaylistListing.short: a listing that declares no count is whole

- File: `src/cratekit/modules/outbound/service.py`
- Source: `u201.json`, row `S1_short_undeclared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_listing_with_no_declared_count_is_short`

Old text:

```
        return self.declared is None or self.listed < self.declared
```

New text:

```
        return self.declared is not None and self.listed < self.declared
```

### `u142.S1_folder_prefix`

sets: drop the Downloaded Sets prefix, so a set is filed into the plain year folder the filing owns

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S1_folder_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 216 against a baseline of 216
- Kills: 13 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_export_set.py::test_the_archive_takes_records_and_files_it_in_a_year_folder_made_once`
  - `tests/test_export_set.py::test_two_folders_named_as_the_year_refuse_and_write_nothing`
  - `tests/test_organize.py::test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year`
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`
  - `tests/test_organize.py::test_a_set_found_prefixed_by_the_migration_is_still_filed_by_the_archive`
  - `tests/test_organize.py::test_a_set_in_its_folder_with_its_built_title_is_taken_and_not_moved`
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`
  - `tests/test_organize.py::test_a_year_record_whose_folder_now_carries_the_sets_name_is_not_the_filings`
  - `tests/test_organize.py::test_no_downloaded_sets_folder_is_made_once_and_the_year_folder_beside_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`

Old text:

```
FOLDER_PREFIX = "Downloaded Sets "
```

New text:

```
FOLDER_PREFIX = ""
```

### `u142.S2_plan_reads_the_year_key`

plan_archive: read the ledger's folder record under the year, so the filing's plain year folder is reused for a set

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S2_plan_reads_the_year_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 216 against a baseline of 216
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_organize.py::test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year`
  - `tests/test_organize.py::test_a_year_record_whose_folder_now_carries_the_sets_name_is_not_the_filings`

Old text:

```
    recorded = ledger.set_folder(cfg, name)
```

New text:

```
    recorded = ledger.set_folder(cfg, year)
```

### `u142.S3_adopt_by_year_too`

plan_archive: adopt a root folder named as the plain year as well, so the year folder competes with the sets' folder

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S3_adopt_by_year_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 216 against a baseline of 216
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year`

Old text:

```
        named = sorted(fid for fid, title in root.items() if title == name)
```

New text:

```
        named = sorted(fid for fid, title in root.items() if title in (name, year))
```

### `u142.S5_create_under_the_year`

apply_archive: create the folder under the plain year, so a set's folder is made with the filing's name

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S5_create_under_the_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 216 against a baseline of 216
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_archive_takes_records_and_files_it_in_a_year_folder_made_once`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`
  - `tests/test_organize.py::test_an_existing_year_folder_on_the_account_is_adopted_not_made_again`
  - `tests/test_organize.py::test_no_downloaded_sets_folder_is_made_once_and_the_year_folder_beside_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`

Old text:

```
        lambda: account.create_folder(planned.folder_name),
```

New text:

```
        lambda: account.create_folder(planned.year),
```

### `u142.S6_reserve_under_the_year`

apply_archive: record the folder under the plain year key, so the filing reuses the sets' folder

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S6_reserve_under_the_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 216 against a baseline of 216
- Kills: 7 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_organize.py::test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_year_record_whose_folder_now_carries_the_sets_name_is_not_the_filings`
  - `tests/test_organize.py::test_an_existing_year_folder_on_the_account_is_adopted_not_made_again`
  - `tests/test_organize.py::test_no_downloaded_sets_folder_is_made_once_and_the_year_folder_beside_it`

Old text:

```
        planned.folder_name,
        lambda: account.create_folder(planned.folder_name),
```

New text:

```
        planned.year,
        lambda: account.create_folder(planned.folder_name),
```

### `u142.S7_adoption_is_a_write`

ArchivePlan.writes: count an adoption alone as a write again, so a set already filed by hand reads as planned

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S7_adoption_is_a_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 216 against a baseline of 216
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`

Old text:

```
        return self.move or self.mark
```

New text:

```
        return self.folder_action in (CREATE, ADOPT) or self.move or self.mark
```

### `r227.S1_unknown_is_within_limit`

An age that could not be read is called within the limit

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S1_unknown_is_within_limit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_age_that_cannot_be_read_is_unknown_rather_than_fresh`

Old text:

```
    if not age.known:
        return AGE_UNKNOWN
```

New text:

```
    if not age.known:
        return AGE_WITHIN_LIMIT
```

### `r227.S2_no_sentence_at_the_gate`

The shown block carries no warning sentence, so the advice arrives only after the answer

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S2_no_sentence_at_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_date_well_in_the_future_is_not_the_freshest_export_there_could_be`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[export.playlist]`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[sync.favorites]`

Old text:

```
        export["warning"] = warning["message"]
```

New text:

```
        pass
```

### `r227.S3_utc_date_in_the_sentence`

The warning names the UTC date rather than the person's own

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S3_utc_date_in_the_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_date_is_the_persons_own_and_not_greenwichs`

Old text:

```
    return moment.astimezone().date().isoformat()
```

New text:

```
    return moment.date().isoformat()
```

### `r227.S4_utc_instant_in_the_block`

The shown block spells the instant in UTC rather than in the machine's zone

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S4_utc_instant_in_the_block`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_date_is_the_persons_own_and_not_greenwichs`

Old text:

```
            age.written.astimezone().replace(microsecond=0).isoformat()
```

New text:

```
            age.written.replace(microsecond=0).isoformat()
```

### `r227.S5_envelope_drops_the_age`

queue_warnings takes the age and says nothing about it

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S5_envelope_drops_the_age`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[sync.favorites]`

Old text:

```
    warnings: list[dict[str, str]] = [*age_warnings(age)]
```

New text:

```
    warnings: list[dict[str, str]] = []
```

### `r227.S6_no_stale_sentence`

A stale export produces no warning at all

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S6_no_stale_sentence`
- Moved: age_warnings in shell.py was rewritten as one if and elif chain that sets the code and message, so the stale branch is now an elif rather than its own if returning the warning; the same stale condition is made false
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 8 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[export.playlist]`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_date_is_the_persons_own_and_not_greenwichs`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_sentence_does_not_say_seven_is_past_seven`

Old text:

```
    elif age.stale:

```

New text:

```
    elif False:

```

### `r227.S7_floored_age_in_the_sentence`

The age is spelled in whole days only, so the sentence says seven is past seven

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S7_floored_age_in_the_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_sentence_does_not_say_seven_is_past_seven`

Old text:

```
    return f"{elapsed.days} days {hours} hours"
```

New text:

```
    return f"{elapsed.days} days"
```

### `r290-author.S13_outbound_shell_call_removed`

Remove the one jobs.raise_for_state call from modules/outbound/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r290-author.json`, row `S13_outbound_shell_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_outbound_workers.py`
- Collected: 249 against a baseline of 249
- Kills: 18 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[export.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[sync.favorites]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_outbound_workers.py::test_a_cancelled_job_does_not_report_a_clean_resume`
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_track_the_provider_would_not_add_fails_its_item_alone_and_is_never_recorded`
  - ... and 3 more, see the JSON sidecar

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r850-a.E10_concluded_not_called`

shell.resume: never ask the verb what its finished run says, so the unmatched warning is never given

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r850-a.json`, row `E10_concluded_not_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - `tests/test_outbound_workers.py::test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers`

Old text:

```
        said = concluded(data["progress"]["outbound"]) if concluded is not None else ()
```

New text:

```
        said = ()
```

### `r856-a.S1_tally_zero`

shell.unmatched_tally: report a tally when nothing went unmatched, so a clean sweep and a clean export carry the warning

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r856-a.json`, row `S1_tally_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_created_playlist_is_filed_in_exports_as_its_gate_showed`
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - `tests/test_outbound_workers.py::test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning`
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_an_export_where_every_track_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_the_sweep_warning_counts_only_whole_numbers`
  - `tests/test_outbound_workers.py::test_the_unmatched_warning_reads_only_whole_counts[none-left-out]`

Old text:

```
    if not _whole(missed) or missed <= 0:
```

New text:

```
    if not _whole(missed) or missed < 0:
```

### `r856-a.S2_tally_bool`

shell._whole: take a bool for a count, so True reads as one unmatched and as one in the total

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r856-a.json`, row `S2_tally_bool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_sweep_warning_counts_only_whole_numbers`
  - `tests/test_outbound_workers.py::test_the_unmatched_warning_reads_only_whole_counts[bool-is-no-count]`
  - `tests/test_outbound_workers.py::test_the_unmatched_warning_reads_only_whole_counts[bool-unmatched]`

Old text:

```
    return isinstance(value, int) and not isinstance(value, bool)
```

New text:

```
    return isinstance(value, int)
```

### `u51-item-derivation.S3_empty_job_driven`

Drive a job with no items, which core.jobs reports as SUCCEEDED

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `u51-item-derivation.json`, row `S3_empty_job_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_job_with_no_items_refuses_rather_than_reporting_a_clean_success`

Old text:

```
            if not jobs.items(store, job.job_id):
```

New text:

```
            if False:
```

### `u51-item-derivation.S5_payload_shape`

Put the outbound summary back at the top level, off the declared schema

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `u51-item-derivation.json`, row `S5_payload_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 65 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_cancelled_job_does_not_report_a_clean_resume`
  - `tests/test_outbound_workers.py::test_a_confirmed_adoption_does_not_authorise_a_create`
  - `tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`
  - `tests/test_outbound_workers.py::test_a_crate_the_export_still_carries_is_never_adopted_from`
  - `tests/test_outbound_workers.py::test_a_created_playlist_is_filed_in_exports_as_its_gate_showed`
  - `tests/test_outbound_workers.py::test_a_dangling_track_is_named_in_the_queued_envelope`
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_favourites_sweep_runs_to_done_and_hearts_every_matched_row`
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - `tests/test_outbound_workers.py::test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning`
  - `tests/test_outbound_workers.py::test_a_fresh_export_shows_its_date_and_warns_of_nothing[export.playlist]`
  - `tests/test_outbound_workers.py::test_a_fresh_export_shows_its_date_and_warns_of_nothing[sync.favorites]`
  - `tests/test_outbound_workers.py::test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing`
  - ... and 50 more, see the JSON sidecar

Old text:

```
        "progress": {
            **jobs.progress(store, job.job_id),
            "outbound": dict(summary(cfg, job.job_id)),
        },
```

New text:

```
        "progress": jobs.progress(store, job.job_id),
        "outbound": dict(summary(cfg, job.job_id)),
```

### `r227.A1_floored_days`

Staleness is judged on floored whole days, so seven days and one second is not past seven

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A1_floored_days`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 372 against a baseline of 372
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_old_means_past_the_limit_and_not_at_it`
  - `tests/test_outbound_workers.py::test_the_sentence_does_not_say_seven_is_past_seven`

Old text:

```
        return age is not None and age.total_seconds() > self.limit_days * _SECONDS_PER_DAY
```

New text:

```
        return age is not None and age.days > self.limit_days
```

### `r227.A2_never_stale`

No export is ever stale, which is the tree before this unit

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A2_never_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 372 against a baseline of 372
- Kills: 13 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[export.playlist]`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[sync.favorites]`
  - `tests/test_outbound_workers.py::test_old_means_past_the_limit_and_not_at_it`
  - `tests/test_outbound_workers.py::test_the_date_is_the_persons_own_and_not_greenwichs`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_sentence_does_not_say_seven_is_past_seven`
  - `tests/test_sync_all.py::test_a_pass_that_queued_over_an_old_export_warns_and_still_queues`
  - `tests/test_sync_all.py::test_the_composed_gate_names_the_exports_date_beside_what_would_queue`

Old text:

```
        return age is not None and age.total_seconds() > self.limit_days * _SECONDS_PER_DAY
```

New text:

```
        return False
```

### `r227.A3_future_clamped`

A date far in the future is never future dated, so it clamps to an age of nothing and reads as recent

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A3_future_clamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 372 against a baseline of 372
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_date_well_in_the_future_is_not_the_freshest_export_there_could_be`

Old text:

```
        return self.written - self.judged_at > FUTURE_TOLERANCE
```

New text:

```
        return False
```

### `r227.A4_no_tolerance`

No tolerance at all, so a volume whose clock runs a few hours ahead is future dated

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A4_no_tolerance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 372 against a baseline of 372
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_few_hours_ahead_is_a_clock_and_reads_as_written_just_now`

Old text:

```
FUTURE_TOLERANCE = timedelta(days=1)
```

New text:

```
FUTURE_TOLERANCE = timedelta(0)
```

### `r227.A5_half_a_pair`

The constructor accepts a date with no instant to judge it at

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A5_half_a_pair`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 372 against a baseline of 372
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_age_is_built_whole_or_not_at_all`

Old text:

```
        if (self.written is None) != (self.judged_at is None):
```

New text:

```
        if False:
```

### `r227.A6_conversion_unguarded`

Only the stat is guarded, so a modification time no date can hold escapes as a traceback

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A6_conversion_unguarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 372 against a baseline of 372
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_modification_time_no_date_can_hold_is_unknown_rather_than_a_crash`

Old text:

```
    except (OSError, OverflowError, ValueError):
```

New text:

```
    except FileNotFoundError:
```

### `r227.A7_unreadable_reads_as_now`

A file that cannot be asked its date is reported as written this instant

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A7_unreadable_reads_as_now`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 372 against a baseline of 372
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_modification_time_no_date_can_hold_is_unknown_rather_than_a_crash`
  - `tests/test_outbound_workers.py::test_an_age_that_cannot_be_read_is_unknown_rather_than_fresh`

Old text:

```
        return ExportAge(path=located, limit_days=limit_days)

```

New text:

```
        return ExportAge(path=located, limit_days=limit_days, written=datetime.now(timezone.utc), judged_at=datetime.now(timezone.utc))

```

### `r356-b.B1_naming_head_left_on_the_release_title`

The release title is the display title, key and tempo head and all, which agrees with no provider title

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r356-b.json`, row `B1_naming_head_left_on_the_release_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 372 against a baseline of 372
- Kills: 8 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_configuration_with_no_marker_text_still_strips_the_head`
  - `tests/test_outbound_tidal_account.py::test_a_release_the_account_already_hearts_is_the_one_an_export_adds`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_the_release_title_is_the_display_title_with_the_naming_head_off`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
    return naming.strip_heads(entry.name, template=template)
```

New text:

```
    return entry.name
```

### `r356-b.B2_template_declares_no_lossy_marker`

The template never declares the marker, so a marked lossy copy keeps it in its release title

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r356-b.json`, row `B2_template_declares_no_lossy_marker`
- Moved: U298 folded this function's strip, empty check and marker rule into naming.NameTemplate.lossy_if_marked, which it now returns; returning the plain template here is what forcing the empty branch did, local to this caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 372 against a baseline of 372
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_the_release_title_is_the_display_title_with_the_naming_head_off`

Old text:

```
    return naming.NameTemplate.lossy_if_marked(cfg.naming.lossy_marker)
```

New text:

```
    return naming.NameTemplate()
```

### `r356-b.B3_empty_marker_no_longer_guarded`

A configuration with no marker text builds a marker rule with an empty literal, which is refused at construction, so every item fails over a naming policy

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r356-b.json`, row `B3_empty_marker_no_longer_guarded`
- Moved: U298 folded this function's strip, empty check and marker rule into naming.NameTemplate.lossy_if_marked; calling NameTemplate.lossy on the stripped text here skips only the empty check, so an empty marker reaches the rule's construction as it did, local to this caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 372 against a baseline of 372
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_configuration_with_no_marker_text_still_strips_the_head`

Old text:

```
    return naming.NameTemplate.lossy_if_marked(cfg.naming.lossy_marker)
```

New text:

```
    return naming.NameTemplate.lossy((cfg.naming.lossy_marker or "").strip())
```

### `r356-b.B4_heart_candidate_carries_no_artist`

A favourite reaches the account with a title and no artist, which chooses nothing

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r356-b.json`, row `B4_heart_candidate_carries_no_artist`
- Moved: heart_candidates now reads each row through the shared source._identified, so the release title arrives as title rather than a release_title call; the artist keyword is dropped as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 236 against a baseline of 236
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
            release_title=title,
            artist=entry.artist,

```

New text:

```
            release_title=title,

```

### `r572.L1_local_track_drop_album`

local_tracks stops carrying the file's album

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r572.json`, row `L1_local_track_drop_album`
- Moved: local_tracks now builds each LocalTrack on one line from the shared _identified rows, with the other fields positional; the same album keyword is dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_local_tracks_carries_the_files_album_to_the_export_plan`

Old text:

```
        LocalTrack(track_id, entry.name, entry.artist, found.isrc, title, album=found.album)

```

New text:

```
        LocalTrack(track_id, entry.name, entry.artist, found.isrc, title)

```

### `r572.S1_album_not_read`

file_identity drops the album it read

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r572.json`, row `S1_album_not_read`
- Moved: source.file_identity still reads the album, its FileIdentity now built on one line with the ISRC positional; same album dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 236 against a baseline of 236
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_workers.py::test_local_tracks_carries_the_files_album_to_the_export_plan`
  - `tests/test_outbound_workers.py::test_the_files_album_is_read_beside_its_isrc_in_one_read`

Old text:

```
album=str(read["album"] or "").strip())
```

New text:

```
album="")
```

### `sitting4.G10_absent_root_reads_as_untagged`

The mount guard is removed, so an unplugged volume reads as a library of untagged files and the sweep succeeds unmatched

- File: `src/cratekit/modules/outbound/source.py`
- Source: `sitting4.json`, row `G10_absent_root_reads_as_untagged`
- Moved: the mount guard is still in source.py, its refusal message rewrapped onto longer lines so the old anchor's message line no longer matches; same condition forced true
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_absent_library_root_refuses_rather_than_reading_every_row_untagged`

Old text:

```
    root = Path(cfg.library.root)
    if root.is_dir():
        return
    raise refuse(
        "library-volume-unmounted",

```

New text:

```
    root = Path(cfg.library.root)
    if True:
        return
    raise refuse(
        "library-volume-unmounted",

```

### `sitting4.G3_builders_ignore_the_prefix_map`

The builders hand the resolver an empty map, so a renamed drive resolves no row (R-372)

- File: `src/cratekit/modules/outbound/source.py`
- Source: `sitting4.json`, row `G3_builders_ignore_the_prefix_map`
- Moved: source.prefix_rules builds the same list in one comprehension line, its loop name shortened to prefix; same map replaced by an empty one
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_row_builders_use_the_configured_prefix_map`

Old text:

```
    return [locations.PrefixRule(prefix, target) for prefix, target in cfg.resolved_prefix_map()]

```

New text:

```
    return []

```

### `u309.U25_source_reader_lazy_name`

source.library_export no longer answers, so a patch on the export reader misses

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u309.json`, row `U25_source_reader_lazy_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_export_collection.py`, `tests/test_favorites_pink.py`
- Collected: 230 against a baseline of 230
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_export_document_is_parsed_once_per_process`

Old text:

```
    if name == "library_export":
```

New text:

```
    if name == "library_export_unused":
```

### `u51-item-derivation.A2_default_favorites_playlist`

Default the sweep to the FOLDER name the live library uses

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `A2_default_favorites_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 27 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_favourites_sweep_runs_to_done_and_hearts_every_matched_row`
  - `tests/test_outbound_workers.py::test_a_fresh_export_shows_its_date_and_warns_of_nothing[sync.favorites]`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[sync.favorites]`
  - `tests/test_outbound_workers.py::test_a_provider_that_already_hearts_a_row_is_reported_rather_than_written`
  - `tests/test_outbound_workers.py::test_a_second_sweep_writes_nothing_because_the_ledger_remembers`
  - `tests/test_outbound_workers.py::test_a_sweep_runs_with_rekordbox_open_and_never_opens_the_database`
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_an_empty_playlist_refuses_distinguishably_from_an_absent_one`
  - `tests/test_outbound_workers.py::test_an_item_report_carries_no_empty_colored_list`
  - `tests/test_outbound_workers.py::test_an_unmatched_favourite_is_reported_and_does_not_fail_its_item`
  - `tests/test_outbound_workers.py::test_job_show_reports_the_bound_worker_for_a_queued_job[sweep]`
  - `tests/test_outbound_workers.py::test_no_colour_writer_reaches_the_engine_from_a_queued_sweep`
  - ... and 12 more, see the JSON sidecar

Old text:

```
DEFAULT_FAVORITES_PLAYLIST = "All Favorites"
```

New text:

```
DEFAULT_FAVORITES_PLAYLIST = "Favorites"
```

### `u51-item-derivation.D1_unknown_playlist`

Drop the refusal for a playlist name the document does not carry

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D1_unknown_playlist`
- Moved: the same refusal in source.resolve, rewrapped to longer lines with its origin read from the module's _ORIGIN, so the whole if block is deleted at its new text
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_name_that_is_a_folder_refuses_rather_than_resolving`
  - `tests/test_outbound_workers.py::test_an_export_naming_a_playlist_the_document_lacks_queues_nothing`

Old text:

```
    if not matched:
        raise refuse(
            "export-playlist-unknown",
            f"no playlist in {library.path.name} is named {wanted!r}. A folder of that name is "
            f"not a match either, because a folder holds playlists rather than tracks",
            steps=("name the playlist by its display name, or by its full path joined with /",),
            scope=Scope.RUN,
            origin=_ORIGIN,
            detail={"playlist": wanted},
        )

```

New text:

```
(empty)
```

### `u51-item-derivation.D2_ambiguous_playlist`

Take the first match instead of refusing when several carry the name

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D2_ambiguous_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_name_two_playlists_carry_refuses_and_names_both_paths`

Old text:

```
    if len(matched) > 1:
```

New text:

```
    if False:
```

### `u51-item-derivation.D3_empty_playlist`

THE ZERO ITEM RULE: let a playlist with no writable track queue

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D3_empty_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_empty_playlist_refuses_distinguishably_from_an_absent_one`

Old text:

```
    if not kept:
```

New text:

```
    if False:
```

### `u51-item-derivation.D4_dangling_reported`

Stop reporting a TrackID the playlist names and the collection lacks

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D4_dangling_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_dangling_track_id_is_reported_and_not_queued`
  - `tests/test_outbound_workers.py::test_the_queued_envelope_names_a_missing_and_a_repeated_track`

Old text:

```
            dangling.append(track_id)
            continue
```

New text:

```
            continue
```

### `u51-item-derivation.D5_repeated_deduped`

Queue a repeated identifier twice instead of once

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D5_repeated_deduped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_repeated_track_id_becomes_one_item`
  - `tests/test_outbound_workers.py::test_the_queued_envelope_names_a_missing_and_a_repeated_track`

Old text:

```
        if track_id in seen:
```

New text:

```
        if False:
```

### `u51-item-derivation.D6_export_required`

Let a verb queue with no export document named

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D6_export_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_neither_verb_queues_anything_without_an_export[export.playlist]`
  - `tests/test_outbound_workers.py::test_neither_verb_queues_anything_without_an_export[sync.favorites]`

Old text:

```
    if not text:
```

New text:

```
    if False:
```

### `r1308.M11_count_before_ge`

_removal_read_back: a count at or over before's reads as before

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M11_count_before_ge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`

Old text:

```
if declared == len(before)
```

New text:

```
if declared >= len(before)
```

### `r1308.M12_count_after_le`

_removal_read_back: a count at or under after's reads as after

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M12_count_after_le`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`

Old text:

```
if declared == len(expected)
```

New text:

```
if declared <= len(expected)
```

### `r1308.M13_accept_tracks_only`

_removal_read_back: accept a reading whose tracks are after, whatever its count

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M13_accept_tracks_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 8 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_whose_read_lags_one_write_is_taken_as_done[count]`

Old text:

```
if tracks == counted == "after":
```

New text:

```
if tracks == "after":
```

### `r1308.M14_lag_by_or`

_removal_read_back: a lag needs only one half known, the other may be neither

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M14_lag_by_or`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 11 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[as-long-as-before]`
  - `tests/test_outbound_remove_lag.py::test_a_refused_read_back_forgets_what_was_remembered_of_the_playlist[0]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`
  - `tests/test_prune.py::test_a_removal_that_took_the_wrong_position_is_read_back_and_refused`

Old text:

```
lagged = tracks is not None and counted is not None
```

New text:

```
lagged = tracks is not None or counted is not None
```

### `r1308.M15_lag_always`

_removal_read_back: every reading is a lag, so a wrong track is read again to the bound

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M15_lag_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 12 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[as-long-as-before]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[then-wrong]`
  - `tests/test_outbound_remove_lag.py::test_a_refused_read_back_forgets_what_was_remembered_of_the_playlist[0]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`
  - `tests/test_prune.py::test_a_removal_that_took_the_wrong_position_is_read_back_and_refused`

Old text:

```
lagged = tracks is not None and counted is not None
```

New text:

```
lagged = True
```

### `r1308.M16_no_break`

_removal_read_back: no break on a wrong reading, so it is read again

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M16_no_break`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 10 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[as-long-as-before]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[then-wrong]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`

Old text:

```
            if not lagged:
                break
        # WHAT
```

New text:

```
            if not lagged:
                pass
        # WHAT
```

### `r1308.M18_not_forgotten`

_removal_read_back: keep what was remembered of the playlist after a refusal

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M18_not_forgotten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_refused_read_back_forgets_what_was_remembered_of_the_playlist[0]`
  - `tests/test_outbound_remove_lag.py::test_a_refused_read_back_forgets_what_was_remembered_of_the_playlist[99]`

Old text:

```
        self._members.pop(identifier, None)
        shown
```

New text:

```
        shown
```

### `r1308.M20_message_swapped`

_removal_read_back: a lag says a wrong track may have come off

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M20_message_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 15 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[as-long-as-before]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[then-wrong]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[whole]`
  - `tests/test_outbound_remove_lag.py::test_a_refused_read_back_forgets_what_was_remembered_of_the_playlist[0]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`
  - `tests/test_prune.py::test_a_removal_that_took_the_wrong_position_is_read_back_and_refused`

Old text:

```
            if lagged
            else (
                f"the playlist {identifier} read back after a removal is not "
```

New text:

```
            if not lagged
            else (
                f"the playlist {identifier} read back after a removal is not "
```

### `r1308.M21_halves_swapped`

_removal_read_back: the message names the other half

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M21_halves_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`

Old text:

```
("before", "after"): (
                "read after a removal with its declared count changed
```

New text:

```
("after", "before"): (
                "read after a removal with its declared count changed
```

### `r1308.M22_retryable`

_removal_read_back: the refusal as provider_failure, retryable, whose remedy is to run again

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M22_retryable`
- Moved: the read back refusal stays in TidalAccount._removal_read_back but is now raised through the shared _refused helper rather than refuse with its slug; the same retryable failure is raised ahead of it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_prune.py`
- Collected: 75 against a baseline of 75
- Kills: 14 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[as-long-as-before]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[then-wrong]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[whole]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`
  - `tests/test_prune.py::test_a_removal_that_took_the_wrong_position_is_read_back_and_refused`

Old text:

```
        raise _refused(
            (
                f"the playlist {identifier} {shown
```

New text:

```
        raise account.provider_failure(RuntimeError('lag'), 'remove')
        raise _refused(
            (
                f"the playlist {identifier} {shown
```

### `r1308.M23_read_back_bypassed`

remove_tracks: take the expected list as read back without reading

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M23_read_back_bypassed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 34 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[as-long-as-before]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[then-wrong]`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[count]`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[whole]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_catches_up_on_the_last_reading_is_taken_as_done`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            playlist, before = self._removal_read_back(identifier, before, expected)
```

New text:

```
            playlist, before = self._playlist(identifier), expected
```

### `r1308.M24_positions_count`

_positions: drop the declared count's match with the tracks read, the guard _reading was split from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M24_positions_count`
- Moved: the same count check in _positions, whose four conditions were joined onto one line, so the declared count's match is dropped from that line instead of deleting a line of its own
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 2 (killed)
- Killed:
  - `tests/test_prune.py::test_a_playlist_with_a_track_the_account_cannot_see_is_refused_with_nothing_sent`
  - `tests/test_prune.py::test_a_settled_track_the_listing_hides_is_not_recorded_as_off`

Old text:

```
        if not _count(declared) or declared != len(members) or not _count(videos) or videos != 0:
```

New text:

```
        if not _count(declared) or not _count(videos) or videos != 0:
```

### `r1308.M6_after_by_length`

_removal_read_back: judge the tracks after by their number, not their content

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M6_after_by_length`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_refused_read_back_forgets_what_was_remembered_of_the_playlist[0]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`
  - `tests/test_prune.py::test_a_removal_that_took_the_wrong_position_is_read_back_and_refused`

Old text:

```
else "after" if reading == expected else None
```

New text:

```
else "after" if len(reading) == len(expected) else None
```

### `r1308.M8_count_ignored`

_removal_read_back: take the count as after whatever it declares

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M8_count_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 9 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[whole]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_whose_read_lags_one_write_is_taken_as_done[count]`

Old text:

```
            counted = (
                None
                if not _count(declared)
```

New text:

```
            counted = "after" or (
                None
                if not _count(declared)
```

### `r1308.M9_videos_unchecked`

_removal_read_back: drop the no video check

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M9_videos_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`

Old text:

```
if not _count(declared) or not _count(videos) or videos != 0
```

New text:

```
if not _count(declared)
```

### `r1394.A1_recorder_never_told`

adapter order: the recorder begun answers is never told before a move, so the record keeps sent and landed at 0 while moves land

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A1_recorder_never_told`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_recorder_that_cannot_record_has_no_further_move_sent`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`

Old text:

```
                if told is not None:
                    told(number, number - 1)
```

New text:

```
                if False:
                    told(number, number - 1)
```

### `r1394.A2_sent_one_short`

adapter order: the recorder is told one move fewer sent than is about to go, so a move in flight is read as known not to have landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A2_sent_one_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_recorder_that_cannot_record_has_no_further_move_sent`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`

Old text:

```
                    told(number, number - 1)
```

New text:

```
                    told(number - 1, number - 1)
```

### `r1394.A3_landed_overstated`

adapter order: the recorder is told the move about to go has already landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A3_landed_overstated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`

Old text:

```
                    told(number, number - 1)
```

New text:

```
                    told(number, number)
```

### `r1394.A4_412_not_brought_down`

adapter order: a move spent on its 412s is left as maybe landed, its sent count never brought back down

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A4_412_not_brought_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`

Old text:

```
                        told(number - 1, number - 1)
```

New text:

```
                        pass
```

### `r1394.A5_any_failure_brought_down`

adapter order: a move that failed any way, a dropped connection included, is told as not landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A5_any_failure_brought_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`

Old text:

```
                    if not _stale_tag(exc):
                        raise
                    if told is not None:
```

New text:

```
                    if told is not None:
                        told(number - 1, number - 1)
                    if not _stale_tag(exc):
                        raise
                    if told is not None:
```

### `r1411.A1_agreed_order_always_stands`

the agreed order check passes every reading, so a reading in the order from before the stopped moves is planned from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A1_agreed_order_always_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 11 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_after_an_add_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading1-agreed1-False]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading5-agreed5-False]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading7-agreed7-False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
    return [one for one in dict.fromkeys(reading) if one in named] == [
        one for one in dict.fromkeys(str(one) for one in agreed) if one in held
    ]
```

New text:

```
    return bool(named or held or True)
```

### `r1411.A2_removed_tracks_asked_of_the_reading`

the agreed order check asks every agreed track of the reading, so a track this write took off refuses the finish

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A2_removed_tracks_asked_of_the_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading6-agreed6-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading9-agreed9-True]`

Old text:

```
        one for one in dict.fromkeys(str(one) for one in agreed) if one in held
```

New text:

```
        one for one in dict.fromkeys(str(one) for one in agreed)
```

### `r1411.A3_added_tracks_asked_of_the_agreed_order`

the agreed order check reads every track of the reading, so a track this write added refuses the finish

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A3_added_tracks_asked_of_the_agreed_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading10-agreed10-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading2-agreed2-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading3-agreed3-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading4-agreed4-True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`

Old text:

```
    return [one for one in dict.fromkeys(reading) if one in named] == [
```

New text:

```
    return [one for one in dict.fromkeys(reading)] == [
```

### `r1411.A5_duplicates_counted_twice`

the agreed order check reads a track the reading holds twice at both places

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A5_duplicates_counted_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading8-agreed8-True]`

Old text:

```
    return [one for one in dict.fromkeys(reading) if one in named] == [
```

New text:

```
    return [one for one in reading if one in named] == [
```

### `r1411.E1_expect_compared_as_membership`

existing guard, U220: an expected reading is compared by the tracks it holds, not their order

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `E1_expect_compared_as_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_never_agrees_with_the_expected_one_refuses_with_nothing_moved`

Old text:

```
                return list(dict.fromkeys(reading)) == list(dict.fromkeys(known))
```

New text:

```
                return sorted(dict.fromkeys(reading)) == sorted(dict.fromkeys(known))
```

### `r1411.E4_membership_always_agrees`

existing guard, U220: a reading after this command's own writes is taken whatever it holds

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `E4_membership_always_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[whole]`

Old text:

```
            return sorted(reading) == sorted(known)
```

New text:

```
            return bool(reading) or True
```

### `r1411.S1_settled_ignores_agreed`

the judged reading never asks the agreed order, so only what it holds is checked

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `S1_settled_ignores_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_after_an_add_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`

Old text:

```
            if agreed is not None and not _in_agreed_order(reading, agreed):
                return False
```

New text:

```
            if False:
                return False
```

### `r1411.S2_agreed_stands_in_for_membership`

a reading in the agreed order is taken without the check of what it holds

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `S2_agreed_stands_in_for_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`

Old text:

```
            if agreed is not None and not _in_agreed_order(reading, agreed):
                return False
```

New text:

```
            if agreed is not None:
                return _in_agreed_order(reading, agreed)
```

### `r1411.S3_order_does_not_pass_agreed`

order_tracks takes agreed and never hands it to the judged reading

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `S3_order_does_not_pass_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_after_an_add_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`

Old text:

```
            agreed=tuple(str(one) for one in agreed) if agreed is not None else None,
```

New text:

```
            agreed=None,
```

### `r358-round-2.A3_editor_check`

Drop the editor check, so a playlist the account cannot edit is renamed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358-round-2.json`, row `A3_editor_check`
- Moved: the editor check in rename_playlist stays in tidal_account.py with its refusal folded onto fewer lines and one message string; same check removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_the_account_cannot_edit_refuses_rather_than_reporting_a_rename`

Old text:

```
        if not callable(retitle):
            raise account.provider_failure(LookupError(
                f"the provider's playlist {playlist_id!r} cannot be retitled by this account"
            ), doing)

```

New text:

```
(empty)
```

### `r358-round-2.A5_absent_answer`

Accept an explicit not found as a rename that landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358-round-2.json`, row `A5_absent_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_deleted_between_the_open_and_the_edit_is_the_items_cause`

Old text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted))
        if accepted is False or accepted is _ABSENT:
```

New text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted))
        if accepted is False:
```

### `r358-round-2.A7_empty_title_message`

Reword the empty-title refusal, never append to it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358-round-2.json`, row `A7_empty_title_message`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[   ]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[\n]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[]`

Old text:

```
                f"a rename of the playlist {playlist_id} was asked for with no "
                f"title; the client reads a falsy title as keep the current one "
                f"and answers that it succeeded, so nothing was sent",
```

New text:

```
                f"the playlist {playlist_id} was given a blank title, which the "
                f"client would read as an instruction to keep the current one",
```

### `r358.A1_empty_title_refusal`

Drop the empty-title refusal, so a blank title reaches the client

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358.json`, row `A1_empty_title_refusal`
- Moved: the empty title refusal stays in TidalAccount.rename_playlist, with its comment shortened and its keywords joined on one line; the whole refusal is removed as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[   ]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[\n]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[]`

Old text:

```
        if not wanted.strip():
            # NOT ``provider_failure``, whose remedy, resume to retry, cannot work.
            raise refuse(
                "internal-error",
                f"a rename of the playlist {playlist_id} was asked for with no "
                f"title; the client reads a falsy title as keep the current one "
                f"and answers that it succeeded, so nothing was sent",
                scope=Scope.SOURCE, origin=("outbound", "account"),
                detail={"playlist_id": str(playlist_id)},
            )

```

New text:

```
(empty)
```

### `r358.A2_title_stripped_for_the_write`

Strip the title for the write as well as for the emptiness test

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358.json`, row `A2_title_stripped_for_the_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_title_the_caller_padded_is_written_as_the_caller_asked`

Old text:

```
        wanted = str(name)
        doing = f"rename the playlist {playlist_id} to {wanted!r}"
```

New text:

```
        wanted = str(name).strip()
        doing = f"rename the playlist {playlist_id} to {wanted!r}"
```

### `r358.A4_false_answer`

Accept a False answer as a rename that landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358.json`, row `A4_false_answer`
- Moved: the rename refusal in tidal_account is the same check with the provider_failure call rewrapped, its doing argument joined to the message line; the same False case is dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_the_client_answers_false_is_the_items_cause_not_a_quiet_return`

Old text:

```
        if accepted is False or accepted is _ABSENT:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the new playlist title"), doing

```

New text:

```
        if accepted is _ABSENT:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the new playlist title"), doing

```

### `r358.A6_retry_coefficient`

Take the rename's retry to zero, the way a create takes it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358.json`, row `A6_retry_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_the_provider_refuses_once_is_retried_once_into_the_same_title`

Old text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted))
```

New text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted), retries=0)
```

### `r834.M1_a_create_makes_the_playlist_private`

TidalAccount.create_playlist: drop the private step, so a created playlist keeps whatever visibility the provider defaults to, the defect R-834 named

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r834.json`, row `M1_a_create_makes_the_playlist_private`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_created_playlist_is_made_private_once`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_export_runs_to_done_and_the_ledger_records_every_add`
  - `tests/test_outbound_tidal_account.py::test_a_private_step_refused_once_is_retried_once_and_lands`
  - `tests/test_outbound_tidal_account.py::test_a_private_step_refused_twice_still_hands_back_the_one_playlist`

Old text:

```
        self._make_private(created, identifier)

```

New text:

```
(empty)
```

### `r834.M3_a_refused_private_step_does_not_lose_the_playlist`

_make_private: raise the refusal instead of passing over it, so the create fails after the playlist exists and the ledger never records it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r834.json`, row `M3_a_refused_private_step_does_not_lose_the_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_created_playlist_the_client_offers_no_private_call_for_is_still_returned`
  - `tests/test_outbound_tidal_account.py::test_a_private_step_refused_twice_still_hands_back_the_one_playlist`

Old text:

```
        except CratekitError:
            return
```

New text:

```
        except CratekitError:
            raise
```

### `r834.M5_a_create_is_never_retried`

create_playlist: retry the create like a write, so a create that reached the provider and timed out is retried into a second playlist (an existing guard, sampled)

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r834.json`, row `M5_a_create_is_never_retried`
- Moved: create_playlist in tidal_account.py now makes its call on one line with a shared doing string; same retries=0 removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_create_is_never_retried_into_a_second_playlist`

Old text:

```
lambda: self._session.user.create_playlist(name, ""), retries=0)
```

New text:

```
lambda: self._session.user.create_playlist(name, ""))
```

### `r836-a.A1_product_made_asked_first`

tidal_account.remove_tracks: the ledger is never asked, so a playlist the product did not create loses tracks

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r836-a.json`, row `A1_product_made_asked_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_organize_root.py`, `tests/test_sync_pair_account.py`
- Collected: 112 against a baseline of 112
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_heard.py::test_the_adapter_refuses_a_playlist_the_ledger_does_not_vouch_for_unasked`
  - `tests/test_organize_root.py::test_the_generic_removal_still_refuses_an_unrecorded_playlist`
  - `tests/test_sync_pair_account.py::test_a_paired_playlist_is_never_removed_whole`

Old text:

```
        if self._cfg is None or not ledger.product_made(self._cfg, identifier):
```

New text:

```
        if False:
```

### `r836-a.A4_no_video_declared`

tidal_account._positions: a playlist holding a video is read by track position, which the item removal does not use

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r836-a.json`, row `A4_no_video_declared`
- Moved: the video check in tidal_account._positions is now one if line instead of a parenthesised condition a clause a line; same videos clause removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_export_collection.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_playlist_holding_a_video_is_refused_with_nothing_sent`

Old text:

```
declared != len(members) or not _count(videos) or videos != 0:
```

New text:

```
declared != len(members) or not _count(videos):
```

### `r836-a.A5_removal_never_retried`

tidal_account.remove_tracks: a removal by position is retried once, so a request that landed and timed out takes off whatever moved up

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r836-a.json`, row `A5_removal_never_retried`
- Moved: remove_tracks' removal by position stays in tidal_account.py, now one line with a lambda that binds nothing, since it is called before the loop moves on; same retries=0 dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_export_collection.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_removal_the_provider_refuses_once_is_never_sent_again`

Old text:

```
            accepted = self._call(doing, lambda: playlist.remove_by_indices(at), retries=0)
```

New text:

```
            accepted = self._call(doing, lambda: playlist.remove_by_indices(at))
```

### `u143-c.A1_kind_named`

Adapter: drop the refusal of a kind other than debris or empty

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A1_kind_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_ledger_claimed_playlist_or_another_kind_is_refused_with_no_provider_call`

Old text:

```
        if kind not in kinds.ROOT_REMOVALS:
```

New text:

```
        if False:
```

### `u143-c.A2_ledger_claimed`

Adapter: remove a root playlist a ledger record names

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A2_ledger_claimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_ledger_claimed_playlist_or_another_kind_is_refused_with_no_provider_call`

Old text:

```
        if self._cfg is None or self._claimed(identifier):
```

New text:

```
        if self._cfg is None:
```

### `u143-c.A3_debris_served`

Adapter: accept any served name as debris

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A3_debris_served`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 447 against a baseline of 447
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served0-debris]`
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served1-debris]`

Old text:

```
            served = is_library_debris(name)
```

New text:

```
            served = True
```

### `u143-c.A4_empty_videos`

Adapter: an empty playlist need not declare zero videos

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A4_empty_videos`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 447 against a baseline of 447
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served3-empty]`
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served4-empty]`

Old text:

```
            served = _count(tracks) and _count(videos) and tracks == 0 and videos == 0
```

New text:

```
            served = _count(tracks) and tracks == 0
```

### `u143-d.A5_playlist_read_back`

Adapter: report a root playlist removed though the provider still serves it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A5_playlist_read_back`
- Moved: the root removal's read back moved into tidal_account._sent_and_read_back, shared with remove_playlist, which reads the playlist through _served and answers None for absent; same still served check reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 447 against a baseline of 447
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_label_heard.py::test_the_adapter_removes_a_vouched_playlist_and_reads_it_back_gone`
  - `tests/test_organize_root.py::test_a_root_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_organize_root.py::test_the_adapter_removes_a_root_playlist_of_its_kind_and_reads_it_back_gone[served0-debris]`
  - `tests/test_organize_root.py::test_the_adapter_removes_a_root_playlist_of_its_kind_and_reads_it_back_gone[served1-empty]`

Old text:

```
        if self._served(doing, identifier) is not None:
```

New text:

```
        if False:
```

### `u143-d.A6_legacy_name`

Adapter: remove a root folder whatever its name

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A6_legacy_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 447 against a baseline of 447
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_folder_not_legacy_or_not_empty_is_refused_before_any_removal[2026-0-not-a-legacy-folder]`
  - `tests/test_organize_root.py::test_a_folder_not_legacy_or_not_empty_is_refused_before_any_removal[Phil's Spotify-0-not-a-legacy-folder]`

Old text:

```
        if not kinds.legacy_year(name):
```

New text:

```
        if False:
```

### `u143-d.A7_folder_empty`

Adapter: remove a legacy folder that still holds playlists

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A7_folder_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_folder_not_legacy_or_not_empty_is_refused_before_any_removal[2026 Custom Playlists-2-not-empty]`

Old text:

```
        held = len(self.folder_playlists(identifier)) + len(self.folder_folders(identifier))
```

New text:

```
        held = 0
```

### `u143-d.A8_folder_read_back`

Adapter: report a folder removed though the root still lists it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A8_folder_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_legacy_folder_still_listed_after_its_removal_is_refused`

Old text:

```
        if identifier in self.folders():
```

New text:

```
        if False:
```

### `u220.A10_wrong_status`

_stale_tag: look for a 409 rather than the 412 the provider answers

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A10_wrong_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 10 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading`
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_412_whose_body_is_not_json_is_still_read_as_a_stale_tag`
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_whose_tag_never_comes_fresh_is_sent_a_bounded_number_of_times`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_more_412s_than_pauses_repeat_the_last_pause`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`

Old text:

```
        if status == PRECONDITION_FAILED:
```

New text:

```
        if status == 409:
```

### `u220.A11_cause_chain_only`

_stale_tag: walk the cause chain alone, so a 412 the client failed to decode is missed (round one R3)

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A11_cause_chain_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_whose_body_is_not_json_is_still_read_as_a_stale_tag`

Old text:

```
(one.__cause__, one.__context__)
```

New text:

```
(one.__cause__,)
```

### `u220.A12_no_memory_guard`

order_tracks: ignore what this command's adds left, so a first reading lagging them is planned from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A12_no_memory_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`
  - `tests/test_outbound_order.py::test_the_reading_after_adds_that_lags_them_is_read_again_before_the_first_move`

Old text:

```
        known = self._members.get(identifier)
```

New text:

```
        known = None
```

### `u220.A13_exact_agrees`

_settled: read any reading as agreeing with the caller's expected one

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A13_exact_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_never_agrees_with_the_expected_one_refuses_with_nothing_moved`

Old text:

```
            if exact:
                return list(dict.fromkeys(reading)) == list(dict.fromkeys(known))
```

New text:

```
            if exact:
                return True
```

